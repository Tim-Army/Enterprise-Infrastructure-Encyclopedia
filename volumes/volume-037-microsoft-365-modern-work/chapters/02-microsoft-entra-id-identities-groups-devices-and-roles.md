# Chapter 02: Microsoft Entra ID — Identities, Groups, Devices, and Roles

## Learning Objectives

- Distinguish the identity types in Microsoft Entra ID: member, guest, service principal, and managed identity.
- Create and manage users and groups, including dynamic and role-assignable groups.
- Explain device identity and the three device-join states.
- Scope administration with administrative units and role-based access control.
- Manage external identities and B2B collaboration safely.

## Theory and Architecture

**Microsoft Entra ID** is the cloud identity provider behind Microsoft 365
and Azure. Its directory holds **security principals**: **users** (member
identities native to the tenant, or **guest** identities invited from other
organizations through B2B), **groups**, **service principals** (an
application's identity in the tenant), and **managed identities** (Azure
resource identities with no stored credential). Every access decision — sign
in, open a mailbox, enroll a device — is evaluated against this directory.

**Groups** come in two membership models and two types. **Security groups**
control access and licensing; **Microsoft 365 groups** additionally
provision a shared mailbox, SharePoint site, and Teams team. Membership is
**assigned** (managed by hand) or **dynamic** (rule-based, so membership
updates automatically from user or device attributes — for example
`user.department -eq "Sales"`). **Role-assignable groups** are a special,
protected group type that can be granted an Entra role, so role assignment
can be managed as membership (with PIM, Chapter 04).

**Device identity** is what lets Conditional Access and Intune reason about
the machine, not just the user. A device is **Entra registered**
(personal/BYOD, a light identity), **Entra joined** (corporate, cloud-only,
signed in with an Entra account), or **Entra hybrid joined** (domain-joined
on-premises and synchronized to Entra — the bridge from Volume XXXVI). Joined
and registered devices appear in the directory and can be targeted by policy.

**Administration** is scoped by **role-based access control**. Built-in roles
grant rights across the tenant; **administrative units (AUs)** restrict a
role to a subset of users, groups, or devices — for example a regional help
desk that can reset passwords only for its region. **Restricted management
AUs** can even protect their members from tenant-wide admins.

## Design Considerations

Model **groups** deliberately. Use **dynamic groups** for attribute-driven
populations (department, country, device type) so membership is self-
maintaining, and **assigned** groups for curated sets. Reserve **Microsoft
365 groups** for collaboration (they create a site/mailbox/team) and
**security groups** for access and licensing. Adopt a **naming convention**
(`SG-`, `LIC-`, `DYN-`) so purpose is obvious. Use **role-assignable groups**
for privileged role delegation and protect them accordingly.

Plan **device identity** to match the workforce: **Entra joined** for
cloud-first corporate devices, **hybrid joined** where on-premises AD and
Group Policy still matter (bridged by Entra Connect, Chapter 04), and
**registered** for BYOD that must be known but not fully managed. Device
identity is the prerequisite for device-based **Conditional Access**
(Chapter 03) and Intune management (Chapter 05).

Delegate with **administrative units** by region, department, or function so
help desks and workload admins hold least privilege over only their scope.
For **external collaboration**, decide the B2B posture: which domains may be
invited, what guests can see, and whether **cross-tenant access settings**
should automatically trust another organization's MFA and device claims.

## Implementation and Automation

Create users and both group membership models with Graph PowerShell:

```powershell
$dom = (Get-MgOrganization).VerifiedDomains[0].Name
$pw  = @{ Password = 'Start-123!'; ForceChangePasswordNextSignIn = $true }
New-MgUser -DisplayName "Ana Ruiz" -UserPrincipalName "aruiz@$dom" `
  -MailNickname "aruiz" -AccountEnabled -PasswordProfile $pw -UsageLocation "US"

# Dynamic security group: all Sales users
New-MgGroup -DisplayName "DYN-Sales" -MailEnabled:$false -SecurityEnabled:$true `
  -MailNickname "DYNSales" -GroupTypes "DynamicMembership" `
  -MembershipRule '(user.department -eq "Sales")' -MembershipRuleProcessingState "On"
```

Create a role-assignable group and an administrative unit:

```powershell
New-MgGroup -DisplayName "SG-Helpdesk-Admins" -MailEnabled:$false -SecurityEnabled:$true `
  -MailNickname "SGHelpdesk" -IsAssignableToRole:$true
$au = New-MgDirectoryAdministrativeUnit -DisplayName "AU-EMEA"
New-MgDirectoryAdministrativeUnitMemberByRef -AdministrativeUnitId $au.Id `
  -BodyParameter @{ "@odata.id"="https://graph.microsoft.com/v1.0/users/$((Get-MgUser -Filter "userPrincipalName eq 'aruiz@$dom'").Id)" }
```

Invite a B2B guest:

```powershell
New-MgInvitation -InvitedUserEmailAddress "partner@example.com" `
  -InviteRedirectUrl "https://myapps.microsoft.com" -SendInvitationMessage:$true
```

## Validation and Troubleshooting

Confirm users, dynamic membership, devices, and AU scope:

```powershell
Get-MgUser -Filter "department eq 'Sales'" -CountVariable c -ConsistencyLevel eventual | Select-Object DisplayName
Get-MgGroup -Filter "displayName eq 'DYN-Sales'" -Property Members | Select-Object -Expand Members
Get-MgDevice -Top 5 | Select-Object DisplayName, TrustType, IsManaged, OperatingSystem
Get-MgDirectoryAdministrativeUnitMember -AdministrativeUnitId $au.Id
```

`TrustType` shows `Workplace` (registered), `AzureAd` (joined), or
`ServerAd` (hybrid joined). Common issues: a **dynamic group** not
populating because the rule references an attribute that is empty (dynamic
membership needs the attribute set and the processing state `On`, and can
take minutes to evaluate); a **guest** who cannot access a resource because
external sharing or cross-tenant settings block it; a device missing from
the directory because it is only **registered** on a personal account; and a
**role-assignable group** that cannot be created without the right privilege
(only Privileged Role Administrator or Global Admin can make them). Directory
changes replicate within minutes, not instantly.

## Security and Best Practices

Keep **guest access** governed: limit who can invite, restrict what guests
can enumerate, use **cross-tenant access settings** to decide which
organizations to trust, and run **access reviews** (Chapter 04) on guest
membership. Protect **role-assignable groups** and privileged groups with
PIM and strong authentication. Prefer **dynamic groups** for lifecycle-driven
membership so leavers lose access automatically. Ensure devices have an
**identity** (registered at minimum) so Conditional Access can require
compliant or joined devices. Avoid attribute sprawl in dynamic rules that is
hard to audit, and monitor **sign-in and audit logs** for anomalous identity
activity.

## References and Knowledge Checks

- Microsoft Learn: *Microsoft Entra users and groups*; *Dynamic membership rules*; *Device identity*; *Administrative units*; *B2B collaboration*.
- Microsoft Learn: SC-300 — *Implement an identity management solution*; MS-102 — *Manage users, groups, and devices*.

**Knowledge checks**

1. What extra resources does a Microsoft 365 group provision that a security group does not?
2. What are the three device-join states and when is each appropriate?
3. What does an administrative unit let you do that a tenant-wide role does not?

## Hands-On Lab

Topic-level walkthroughs for SC-300/MS-102 identity-object skills.

**Shared prerequisites for Labs 2.1–2.4** — a Microsoft 365 tenant, a
Graph PowerShell session with `User.ReadWrite.All`, `Group.ReadWrite.All`,
`AdministrativeUnit.ReadWrite.All`, and admin rights. **Cost:** none.

### Lab 2.1 — Create a user with a usage location (Topic: Manage users)

**Objective:** Provision a licensable user.

```powershell
$dom = (Get-MgOrganization).VerifiedDomains[0].Name
New-MgUser -DisplayName "Ana Ruiz" -UserPrincipalName "aruiz@$dom" -MailNickname "aruiz" `
  -AccountEnabled -UsageLocation "US" `
  -PasswordProfile @{ Password='Start-123!'; ForceChangePasswordNextSignIn=$true }
Get-MgUser -UserId "aruiz@$dom" | Select-Object DisplayName, UsageLocation, AccountEnabled
```

**Expected result:** the user exists with `UsageLocation US` — a usage
location is required before most licenses can be assigned.

**Negative test:** omit `-UsageLocation` and later assign a license; it fails
with a location error — licensing needs a usage location.

**Cleanup:** `Remove-MgUser -UserId "aruiz@$dom"`.

### Lab 2.2 — Build a dynamic group (Topic: Manage groups)

**Objective:** Create attribute-driven membership.

```powershell
Update-MgUser -UserId "aruiz@$dom" -Department "Sales"
New-MgGroup -DisplayName "DYN-Sales" -MailEnabled:$false -SecurityEnabled:$true -MailNickname "DYNSales" `
  -GroupTypes "DynamicMembership" -MembershipRule '(user.department -eq "Sales")' -MembershipRuleProcessingState "On"
Start-Sleep 60
Get-MgGroup -Filter "displayName eq 'DYN-Sales'" -Property Members | Select-Object -Expand Members
```

**Expected result:** after evaluation, the Sales user is a member automatically
— dynamic membership self-maintains from attributes.

**Negative test:** set the rule to reference a blank attribute; the group stays
empty — the attribute must be populated for the rule to match.

**Cleanup:** remove the group.

### Lab 2.3 — Inspect device join states (Topic: Manage devices)

**Objective:** Read device identity from the directory.

```powershell
Get-MgDevice -Top 10 | Select-Object DisplayName, TrustType, IsManaged, OperatingSystem, IsCompliant
```

**Expected result:** devices list a `TrustType` of `Workplace`, `AzureAd`, or
`ServerAd` — the join state that Conditional Access and Intune reason about.

**Negative test:** query devices in a brand-new tenant with none enrolled; the
list is empty — device identity requires join/registration first.

**Cleanup:** none (read-only).

### Lab 2.4 — Scope a help desk with an administrative unit (Topic: Delegate administration)

**Objective:** Restrict a role to a subset of the directory.

```powershell
$au = New-MgDirectoryAdministrativeUnit -DisplayName "AU-EMEA"
$uid = (Get-MgUser -UserId "aruiz@$dom").Id
New-MgDirectoryAdministrativeUnitMemberByRef -AdministrativeUnitId $au.Id `
  -BodyParameter @{ "@odata.id"="https://graph.microsoft.com/v1.0/users/$uid" }
Get-MgDirectoryAdministrativeUnitMember -AdministrativeUnitId $au.Id
```

**Expected result:** the user is a member of `AU-EMEA`; a role scoped to this
AU would grant rights only over its members — least privilege by scope.

**Negative test:** assign a tenant-wide User Administrator and expect it to be
limited to the AU; it is not — tenant roles are not AU-scoped unless assigned
over the AU.

**Cleanup:** `Remove-MgDirectoryAdministrativeUnit -AdministrativeUnitId $au.Id`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Entra ID holds members, guests, service principals, and managed identities.
Groups are security or Microsoft 365, with assigned or dynamic membership,
and role-assignable groups delegate privileged roles. Devices are registered,
joined, or hybrid joined — the identity Conditional Access and Intune use.
Administrative units and RBAC scope administration; B2B and cross-tenant
settings govern external collaboration.

- [ ] I can distinguish the Entra identity and group types.
- [ ] I can build assigned and dynamic groups with a naming convention.
- [ ] I can explain the three device-join states.
- [ ] I can scope administration with administrative units.
- [ ] I completed Labs 2.1–2.4 including each negative test.
