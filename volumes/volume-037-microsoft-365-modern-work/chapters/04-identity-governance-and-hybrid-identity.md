# Chapter 04: Identity Governance and Hybrid Identity

## Learning Objectives

- Apply Privileged Identity Management to make privileged roles just-in-time and eligible.
- Run access reviews to recertify membership and guest access.
- Automate the access lifecycle with entitlement management access packages.
- Explain hybrid identity and the Entra Connect / cloud sync options and sign-in methods.
- Protect the synchronization pipeline and reconcile common hybrid identity failures.

## Theory and Architecture

**Identity governance** answers three questions continuously: who should have
access, are they still using it, and how is it granted and removed. Microsoft
Entra provides four building blocks.

**Privileged Identity Management (PIM)** (Entra ID P2) makes privileged roles
**just-in-time**. Instead of standing membership, an admin is made
**eligible** for a role and must **activate** it — with justification, MFA,
a time limit, and optionally approval — so privilege exists only while used
and every activation is logged. PIM covers Entra roles, Azure roles, and
role-assignable groups.

**Access reviews** recertify access on a schedule: reviewers (the resource
owner, the user's manager, or self) confirm whether each member or guest
still needs membership of a group, access to an app, or a privileged role;
unreviewed or denied access can be removed automatically.

**Entitlement management** packages related resources — groups, apps,
SharePoint sites — into an **access package** with a **policy** that defines
who can request it, who approves, and when it expires. Users request access
from the **My Access** portal; approval, provisioning, and time-bound removal
are automated, which is how joiner-mover-leaver is handled at scale,
including for guests.

**Hybrid identity** bridges on-premises Active Directory (Volume XXXVI) to
Entra ID. **Microsoft Entra Connect Sync** (the full server-based tool) or
**Entra Cloud Sync** (a lightweight agent) synchronize users, groups, and
(optionally) password hashes. The **sign-in method** determines where the
password is validated: **password hash synchronization (PHS)** — the most
resilient, cloud validates a hash of the hash; **pass-through authentication
(PTA)** — an on-premises agent validates against a DC; or **federation
(AD FS)** — an on-premises federation service, now largely superseded.
**Seamless SSO** and, increasingly, **cloud Kerberos trust** improve the
hybrid sign-in experience.

## Design Considerations

Put every **privileged role** behind **PIM**: eligible-not-active by default,
MFA on activation, short activation windows, approval for the most sensitive
roles (Global Administrator, Privileged Role Administrator), and alerting on
activations. Schedule **access reviews** for privileged roles (frequent),
group and app membership (periodic), and **guest access** (regular, with
auto-removal of stale guests).

Use **entitlement management** to make access **requestable and time-bound**
rather than permanently assigned, especially for cross-team and external
collaboration. Design **access packages** around business roles and set
expiration so access lapses unless renewed.

For **hybrid identity**, prefer **PHS** as the sign-in method for most
organizations because cloud authentication keeps working if the on-premises
environment is down, and add **cloud Kerberos trust** for Windows Hello.
Choose **Cloud Sync** for simpler topologies or multi-forest merges and
**Connect Sync** where advanced filtering or writeback is required. Never
synchronize **privileged on-premises accounts** to the cloud, scope the sync
to the right OUs, and monitor with **Entra Connect Health**.

## Implementation and Automation

Make a user eligible for a role through PIM (Graph):

```powershell
Connect-MgGraph -Scopes "RoleManagement.ReadWrite.Directory","AccessReview.ReadWrite.All","EntitlementManagement.ReadWrite.All"
$roleDef = (Get-MgRoleManagementDirectoryRoleDefinition -Filter "displayName eq 'Helpdesk Administrator'").Id
$uid = (Get-MgUser -UserId "aruiz@$((Get-MgOrganization).VerifiedDomains[0].Name)").Id
New-MgRoleManagementDirectoryRoleEligibilityScheduleRequest -BodyParameter @{
  action="adminAssign"; principalId=$uid; roleDefinitionId=$roleDef; directoryScopeId="/"
  scheduleInfo=@{ startDateTime=(Get-Date).ToString("o"); expiration=@{ type="afterDuration"; duration="P90D" } }
  justification="JIT helpdesk eligibility" }
```

Create an access review of a group's guest members:

```powershell
New-MgIdentityGovernanceAccessReviewDefinition -BodyParameter @{
  displayName="Quarterly guest review - DYN-Sales"
  scope=@{ "@odata.type"="#microsoft.graph.accessReviewQueryScope"
    query="/groups/$grpId/members/microsoft.graph.user/?\$filter=(userType eq 'Guest')"; queryType="MicrosoftGraph" }
  reviewers=@(@{ query="./manager"; queryType="MicrosoftGraph" })
  settings=@{ recurrence=@{ pattern=@{ type="absoluteMonthly"; interval=3 }; range=@{ type="noEnd" } }
    autoApplyDecisionsEnabled=$true; defaultDecision="Deny" } }
```

For hybrid identity, confirm the sync method and health from Entra:

```powershell
Get-MgOrganization | Select-Object -Expand OnPremisesSyncEnabled
Get-MgDirectoryOnPremiseSynchronization | Select-Object Features
```

## Validation and Troubleshooting

Confirm eligibility, review status, and sync state:

```powershell
Get-MgRoleManagementDirectoryRoleEligibilitySchedule -Filter "principalId eq '$uid'" |
  Select-Object RoleDefinitionId, Status
Get-MgIdentityGovernanceAccessReviewDefinition | Select-Object DisplayName, Status
Get-MgUser -UserId "aruiz@$dom" -Property OnPremisesSyncEnabled, OnPremisesLastSyncDateTime |
  Select-Object OnPremisesSyncEnabled, OnPremisesLastSyncDateTime
```

Common issues: an admin **cannot activate** a PIM role because they were
assigned active rather than eligible, or an approval is pending; an **access
review** auto-removing access unexpectedly because `defaultDecision` was
`Deny` and reviewers did not respond — communicate before enabling
auto-apply; a **synced user** cannot be edited in the cloud because
attributes are mastered on-premises (`OnPremisesSyncEnabled = true` means
edit on-premises); **duplicate/soft-match** conflicts when a cloud object and
an on-premises object share a proxy address or UPN; and **PHS not working**
because password hash sync was never enabled or the sync account lost rights
— check Entra Connect Health. Sign-in failures after federation changes
usually trace to the on-premises AD FS or agents.

## Security and Best Practices

Place **all privileged roles under PIM**, eligible-not-active, with MFA,
short windows, approval for the most sensitive, and activation alerts.
**Recertify** privileged roles, group/app access, and guests with **access
reviews**, and auto-remove stale access after clear communication. Use
**entitlement management** so access is requested, approved, time-bound, and
automatically removed — the reliable answer to leaver risk. For hybrid,
prefer **PHS** for resilience, **never sync privileged on-premises
accounts**, scope synchronization tightly, protect the **Entra Connect
server as a Tier-0 asset**, and monitor **Connect Health**. Governance is
continuous, not a one-time project.

## References and Knowledge Checks

- Microsoft Learn: *Privileged Identity Management*; *Access reviews*; *Entitlement management*; *Microsoft Entra Connect and cloud sync*; *Choose a sign-in method*.
- Microsoft Learn: SC-300 — *Plan and implement identity governance*; MS-102 — *Manage identity and access*.

**Knowledge checks**

1. What does PIM change about how privileged roles are held and used?
2. How does entitlement management handle joiner-mover-leaver at scale?
3. Why is password hash synchronization often the most resilient sign-in method?

## Hands-On Lab

Topic-level walkthroughs for SC-300 governance skills. PIM and access-review
labs require Entra ID P2.

**Shared prerequisites for Labs 4.1–4.4** — a Microsoft 365 tenant with Entra
ID P2, a Graph session with the governance scopes above, and admin rights.
**Cost:** none (trial P2).

### Lab 4.1 — Make a role eligible with PIM (Topic: Privileged access)

**Objective:** Convert standing privilege to just-in-time.

```powershell
$dom=(Get-MgOrganization).VerifiedDomains[0].Name; $uid=(Get-MgUser -UserId "aruiz@$dom").Id
$rd=(Get-MgRoleManagementDirectoryRoleDefinition -Filter "displayName eq 'Helpdesk Administrator'").Id
New-MgRoleManagementDirectoryRoleEligibilityScheduleRequest -BodyParameter @{
  action="adminAssign"; principalId=$uid; roleDefinitionId=$rd; directoryScopeId="/"
  scheduleInfo=@{ startDateTime=(Get-Date).ToString("o"); expiration=@{ type="afterDuration"; duration="P90D" } }
  justification="JIT" }
Get-MgRoleManagementDirectoryRoleEligibilitySchedule -Filter "principalId eq '$uid'" | Select-Object Status
```

**Expected result:** the user is **eligible** (not active) for Helpdesk
Administrator — they must activate with justification and MFA to use it.

**Negative test:** assign the role actively instead; the user holds standing
privilege 24/7 — the opposite of least privilege.

**Cleanup:** remove the eligibility schedule request.

### Lab 4.2 — Schedule a guest access review (Topic: Access reviews)

**Objective:** Recertify guest membership automatically.

```powershell
$grpId=(Get-MgGroup -Filter "displayName eq 'DYN-Sales'").Id
New-MgIdentityGovernanceAccessReviewDefinition -BodyParameter @{
  displayName="Guest review - DYN-Sales"
  scope=@{ "@odata.type"="#microsoft.graph.accessReviewQueryScope"; queryType="MicrosoftGraph"
    query="/groups/$grpId/members" }
  reviewers=@(@{ query="./manager"; queryType="MicrosoftGraph" })
  settings=@{ recurrence=@{ pattern=@{ type="absoluteMonthly"; interval=3 }; range=@{ type="noEnd" } }
    autoApplyDecisionsEnabled=$true; defaultDecision="Deny" } }
Get-MgIdentityGovernanceAccessReviewDefinition | Select-Object DisplayName, Status
```

**Expected result:** a recurring review exists that will remove members whose
reviewers do not approve — stale guest access lapses automatically.

**Negative test:** set `autoApplyDecisionsEnabled=$true` with `defaultDecision=Deny`
and no reviewer communication; legitimate members lose access — communicate
and pilot before auto-apply.

**Cleanup:** remove the review definition.

### Lab 4.3 — Confirm the hybrid sign-in method (Topic: Hybrid identity)

**Objective:** Read the tenant's synchronization and sign-in configuration.

```powershell
Get-MgOrganization | Select-Object DisplayName, OnPremisesSyncEnabled
Get-MgUser -UserId "synceduser@$dom" -Property OnPremisesSyncEnabled, OnPremisesLastSyncDateTime |
  Select-Object OnPremisesSyncEnabled, OnPremisesLastSyncDateTime
```

**Expected result:** the tenant shows sync enabled and a synced user shows a
recent on-premises sync time — synced objects are mastered on-premises.

**Negative test:** try to change a synced user's display name in the cloud; it
is blocked or overwritten at next sync — edit mastered attributes on-premises.

**Cleanup:** none (read-only).

### Lab 4.4 — Detect a soft-match conflict (Topic: Troubleshoot hybrid)

**Objective:** Recognize a duplicate-attribute sync error.

```powershell
# List directory sync errors surfaced to the tenant
Get-MgDirectoryOnPremiseSynchronization | Select-Object -Expand Features
# In the admin center: Health > Directory sync errors shows duplicate proxyAddresses/UPN
```

**Expected result:** a user with a proxy address or UPN that already exists in
the cloud fails to sync and appears under directory sync errors — soft-match
requires unique matching attributes.

**Negative test:** create a cloud user with the same UPN as a pending synced
object; the sync conflicts — resolve by removing the duplicate before sync.

**Cleanup:** remove any test duplicate.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Identity governance keeps access right over time: PIM makes privilege
just-in-time; access reviews recertify membership and guests; entitlement
management makes access requestable and time-bound. Hybrid identity bridges
on-premises AD to Entra with Connect Sync or Cloud Sync and a sign-in method
(prefer PHS for resilience), protecting the sync pipeline as Tier 0.

- [ ] I can put privileged roles behind PIM.
- [ ] I can schedule access reviews with auto-apply.
- [ ] I can automate access with entitlement management.
- [ ] I can choose a hybrid sign-in method and troubleshoot sync.
- [ ] I completed Labs 4.1–4.4 including each negative test.
