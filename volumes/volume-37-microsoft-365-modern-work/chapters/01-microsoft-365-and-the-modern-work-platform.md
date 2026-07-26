# Chapter 01: Microsoft 365 and the Modern Work Platform

## Learning Objectives

- Describe what a Microsoft 365 tenant is and how subscriptions and licensing map to services.
- Navigate the specialist admin centers and explain what each governs.
- Assign administrative roles using least privilege and role-based access control.
- Connect to the tenant with the Microsoft Graph PowerShell SDK for repeatable administration.
- Monitor service health and the message center and know where change is announced.

## Theory and Architecture

**Microsoft 365** is a suite of cloud services delivered from a single
logical container called a **tenant** — an isolated instance of Microsoft
Entra ID (formerly Azure AD) with a default `*.onmicrosoft.com` domain, into
which custom domains, users, groups, and subscriptions are added. Every
Microsoft 365 and Azure service the organization consumes trusts that one
tenant's identity directory, which is why identity (Chapters 02–04) is the
foundation of everything else.

**Subscriptions** (for example Microsoft 365 E3/E5, Business Premium) grant
**licenses**, and each license is a bundle of **service plans** (Exchange
Online, SharePoint, Teams, Intune, Entra ID P1/P2, Defender, Purview). A
user must be assigned a license that includes a service plan before they can
use it — a large share of "the feature is missing" tickets are really
licensing. Licenses are best assigned to **groups** (group-based licensing)
rather than individuals so membership drives entitlement automatically.

Administration is split across **specialist admin centers**, each governing
its workload: the **Microsoft 365 admin center** (users, licenses, tenant
settings, service health), **Microsoft Entra admin center** (identity,
access, Conditional Access), **Intune admin center** (endpoints), **Exchange**,
**SharePoint**, and **Teams** admin centers, and the **Purview** and
**Defender** portals. Underneath every portal is **Microsoft Graph**, the
unified REST API; the **Microsoft Graph PowerShell SDK** is the supported,
scriptable way to do at scale what the portals do by click.

Least-privilege administration uses **Entra role-based access control**:
built-in roles (Global Administrator, User Administrator, Exchange
Administrator, Intune Administrator, Security Administrator, and dozens more)
grant scoped rights, and **administrative units** can scope a role to a
subset of the directory. Global Administrator is powerful and should be rare,
protected, and eligible-only through Privileged Identity Management
(Chapter 04).

## Design Considerations

Plan **licensing** as a group-based model: create license groups aligned to
job function, assign the subscription to the group, and let membership grant
service plans. This makes onboarding and offboarding a group-membership
change and keeps entitlement auditable. Watch **service-plan dependencies**
(for example, some Purview or Defender features need E5 or an add-on).

Plan **administrative roles** around least privilege. Reserve **Global
Administrator** for a very small number of break-glass and senior accounts,
protect them with the strongest authentication and PIM, and use **workload-
specific roles** (Exchange, Intune, Teams, Security) for day-to-day admins.
Use **administrative units** where administration is delegated by region or
department. Keep at least two **emergency-access (break-glass)** accounts,
excluded from Conditional Access, with credentials in a vault.

Standardize on **Microsoft Graph PowerShell** for automation. The older
service-specific modules (MSOnline, AzureAD) are deprecated; Graph PowerShell
and Graph itself are the durable surface. Decide early which **permissions
(scopes)** your automation needs and consent to only those.

## Implementation and Automation

Install and connect the Graph PowerShell SDK with least-privilege scopes:

```powershell
Install-Module Microsoft.Graph -Scope AllUsers
Connect-MgGraph -Scopes "User.Read.All","Group.ReadWrite.All","Organization.Read.All"
Get-MgContext | Select-Object Account, Scopes
Get-MgOrganization | Select-Object DisplayName, Id
```

Inspect subscriptions and licenses, then assign a license via a group:

```powershell
Get-MgSubscribedSku | Select-Object SkuPartNumber, ConsumedUnits, @{n='Enabled';e={$_.PrepaidUnits.Enabled}}
$sku = (Get-MgSubscribedSku | Where-Object SkuPartNumber -eq 'SPE_E3').SkuId
$grp = New-MgGroup -DisplayName "LIC-M365-E3" -MailEnabled:$false -SecurityEnabled:$true `
  -MailNickname "LIC-M365-E3"
Set-MgGroupLicense -GroupId $grp.Id -AddLicenses @(@{SkuId=$sku}) -RemoveLicenses @()
```

Assign a scoped admin role (Intune Administrator) to a user:

```powershell
$roleId = (Get-MgDirectoryRole -Filter "displayName eq 'Intune Administrator'").Id
New-MgDirectoryRoleMemberByRef -DirectoryRoleId $roleId `
  -BodyParameter @{ "@odata.id" = "https://graph.microsoft.com/v1.0/users/aruiz@contoso.com" }
```

## Validation and Troubleshooting

Confirm connection, licensing, and role assignment:

```powershell
Get-MgContext | Select-Object Scopes
Get-MgUserLicenseDetail -UserId "aruiz@contoso.com" | Select-Object SkuPartNumber
Get-MgDirectoryRole | ForEach-Object {
  [pscustomobject]@{ Role=$_.DisplayName; Members=(Get-MgDirectoryRoleMember -DirectoryRoleId $_.Id).Count } }
```

Common issues: a feature unavailable because the user's license lacks the
**service plan** (check `Get-MgUserLicenseDetail`); a Graph command failing
with **insufficient privileges** because the session was not consented the
right **scope** (re-run `Connect-MgGraph` with the scope, and an admin may
need to grant admin consent); a **built-in role not found** because it has
not been "activated" in the tenant yet (`Get-MgDirectoryRole` shows only
activated roles — activate from the role template if needed); and changes not
appearing because portals and Graph can lag a few minutes on directory
replication. **Service health** and the **message center** in the Microsoft
365 admin center explain outages and upcoming changes — check them before
deep troubleshooting.

## Security and Best Practices

Minimize **Global Administrators**, protect them with phishing-resistant MFA
(Chapter 03) and PIM (Chapter 04), and maintain break-glass accounts. Assign
day-to-day admins **workload-specific roles**, scoped with **administrative
units** where possible. Use **group-based licensing** so entitlement is
auditable and offboarding is reliable. Grant automation the **least Graph
scopes** it needs and prefer app registrations with certificate credentials
over stored secrets for unattended jobs. Enable **unified audit logging**
(Purview, Chapter 10) so administrative actions are recorded. Review the
**message center** so security-relevant service changes are not a surprise.

## References and Knowledge Checks

- Microsoft Learn: *Microsoft 365 admin center*; *Microsoft Entra roles*; *Group-based licensing*; *Microsoft Graph PowerShell SDK*.
- Microsoft Learn: MS-102 study guide — *Deploy and manage a Microsoft 365 tenant*.

**Knowledge checks**

1. What is a tenant, and why is identity the foundation of Microsoft 365?
2. Why assign licenses to groups rather than individual users?
3. How does least privilege apply to Microsoft 365 administrative roles?

## Hands-On Lab

Topic-level walkthroughs for MS-102's "manage a Microsoft 365 tenant" skills,
using Microsoft Graph PowerShell.

**Shared prerequisites for Labs 1.1–1.4** — a Microsoft 365 tenant (a free
Developer tenant is fine), a Global Administrator account for setup, and the
`Microsoft.Graph` PowerShell module. **Cost:** none.

### Lab 1.1 — Connect to Microsoft Graph with scoped consent (Topic: Administer the tenant)

**Objective:** Establish a least-privilege admin session.

```powershell
Connect-MgGraph -Scopes "User.Read.All","Organization.Read.All"
Get-MgContext | Select-Object Account, Scopes
Get-MgOrganization | Select-Object DisplayName, VerifiedDomains
```

**Expected result:** the session lists the consented scopes and returns the
tenant's display name and verified domains — Graph PowerShell is the
scriptable equivalent of the admin center.

**Negative test:** run `Get-MgUser` after connecting with only
`Organization.Read.All`; it fails with insufficient privileges — Graph
enforces per-scope consent.

**Cleanup:** `Disconnect-MgGraph`.

### Lab 1.2 — Inspect subscriptions and service plans (Topic: Manage licensing)

**Objective:** See what the tenant is licensed for.

```powershell
Get-MgSubscribedSku | Select-Object SkuPartNumber, ConsumedUnits,
  @{n='Enabled';e={$_.PrepaidUnits.Enabled}}
(Get-MgSubscribedSku | Where-Object SkuPartNumber -eq 'SPE_E5').ServicePlans.ServicePlanName
```

**Expected result:** the tenant's SKUs, seats consumed/available, and the
service plans inside a SKU — a service must be in the license before a user
can use it.

**Negative test:** query `SkuPartNumber -eq 'NOT_A_SKU'`; it returns nothing —
SKU part numbers are exact.

**Cleanup:** none (read-only).

### Lab 1.3 — Create a group and assign a license through it (Topic: Group-based licensing)

**Objective:** Drive entitlement from group membership.

```powershell
$sku = (Get-MgSubscribedSku | Where-Object SkuPartNumber -eq 'SPE_E3').SkuId
$g = New-MgGroup -DisplayName "LIC-M365-E3" -MailEnabled:$false -SecurityEnabled:$true -MailNickname "LICM365E3"
Set-MgGroupLicense -GroupId $g.Id -AddLicenses @(@{SkuId=$sku}) -RemoveLicenses @()
Get-MgGroup -GroupId $g.Id -Property AssignedLicenses | Select-Object -Expand AssignedLicenses
```

**Expected result:** the group carries the E3 license; any user added to the
group inherits it — group-based licensing makes entitlement auditable.

**Negative test:** assign a SKU the tenant has zero available seats of; users
show a licensing error until seats are freed — assignment needs available
units.

**Cleanup:** `Remove-MgGroup -GroupId $g.Id`.

### Lab 1.4 — Assign a workload admin role (Topic: Role-based access control)

**Objective:** Delegate Intune administration with least privilege.

```powershell
$role = Get-MgDirectoryRole -Filter "displayName eq 'Intune Administrator'"
if (-not $role) { $tpl = Get-MgDirectoryRoleTemplate -Filter "displayName eq 'Intune Administrator'"
  $role = New-MgDirectoryRole -RoleTemplateId $tpl.Id }
New-MgDirectoryRoleMemberByRef -DirectoryRoleId $role.Id `
  -BodyParameter @{ "@odata.id"="https://graph.microsoft.com/v1.0/users/aruiz@$((Get-MgOrganization).VerifiedDomains[0].Name)" }
Get-MgDirectoryRoleMember -DirectoryRoleId $role.Id
```

**Expected result:** the user is an Intune Administrator only — a scoped role,
not Global Admin, for endpoint work.

**Negative test:** try to add a member to a role that was never activated;
`Get-MgDirectoryRole` returns nothing for it — activate from the role
template first.

**Cleanup:** `Remove-MgDirectoryRoleMemberByRef -DirectoryRoleId $role.Id -DirectoryObjectId <userId>`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsoft 365 is delivered from a single Entra ID **tenant**; subscriptions
grant **licenses** made of **service plans**, best assigned through
**groups**. Administration spans specialist **admin centers** over the
unified **Microsoft Graph**, scripted with the **Graph PowerShell SDK**, and
governed by least-privilege **RBAC**. Service health and the message center
announce outages and change.

- [ ] I can explain tenants, subscriptions, licenses, and service plans.
- [ ] I can navigate the admin centers and connect Graph PowerShell.
- [ ] I can assign licenses through groups and roles with least privilege.
- [ ] I can find service health and upcoming-change information.
- [ ] I completed Labs 1.1–1.4 including each negative test.
