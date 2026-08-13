# Chapter 04: AD DS Objects — Users, Groups, OUs, Delegation, and Trusts

## Learning Objectives

- Create and manage users, computers, and service accounts at scale with PowerShell.
- Choose the correct group scope and nesting strategy (AGDLP) for resource access.
- Design an organizational-unit structure for delegation and Group Policy.
- Delegate administration to the correct scope without granting excess rights.
- Apply fine-grained password policies, deploy read-only domain controllers, and create trusts.

## Theory and Architecture

Everything in AD DS is an **object** with attributes defined by the schema:
**users**, **computers**, **groups**, **organizational units (OUs)**,
service accounts, and more. Each object has a globally unique **objectGUID**
and a **security identifier (SID)** for security principals. Users and
computers are principals that authenticate; groups collect principals to
simplify access control.

**Groups** have a **scope** and a **type**. Security groups grant rights;
distribution groups are for email only. The three scopes control where a
group's members and the group itself can come from and be used:
**Domain Local** groups can contain principals from anywhere but grant
access only in their own domain; **Global** groups contain principals only
from their own domain but can be used anywhere in the forest; **Universal**
groups can contain principals from any domain and be used anywhere, at the
cost of global-catalog replication. The canonical nesting strategy is
**AGDLP** — Accounts go into Global groups, Global groups go into Domain
Local groups, and permissions are assigned to the Domain Local group. This
keeps membership management (Global groups by role) separate from resource
permissioning (Domain Local groups by resource).

**Organizational units** are containers used for two purposes: **delegation
of administration** and **Group Policy targeting** (Chapter 05). Unlike the
default `Users` and `Computers` containers, OUs can have GPOs linked and
permissions delegated. A good OU design mirrors administrative and policy
boundaries, not the org chart.

**Delegation** uses the object's access control list: you grant a group
specific rights (reset passwords, create users, link GPOs) over an OU
subtree. **Fine-grained password policies (FGPP)**, expressed as Password
Settings Objects, let different principals have different password rules
within one domain — for example, stronger rules for administrators.
**Read-only domain controllers (RODCs)** hold a read-only copy of the
directory and cache only permitted credentials, safe for insecure branch
locations. **Trusts** extend authentication across domains and forests: a
domain within a forest trusts every other transitively, while a **forest
trust** or **external trust** connects separate forests for cross-boundary
access.

## Design Considerations

Adopt **AGDLP** from day one — assigning permissions directly to users or
to Global groups creates unmanageable ACLs. Reserve **Universal** groups
for genuinely forest-wide membership because they replicate to every global
catalog; use Global groups for role membership and Domain Local groups for
resource permissions.

Design the **OU tree** around delegation and policy: a common pattern is
top-level OUs for **Users**, **Computers/Workstations**, **Servers**, and
**Groups**, with sub-OUs by department or function where different admins or
policies apply. Keep principals out of the default containers so policy and
delegation apply. Delegate to **groups**, never to individuals, and
delegate the **least** right that accomplishes the task — "reset password
and force change at next logon" for a help desk, not "full control."

Use **FGPP** to raise requirements for privileged accounts rather than
lowering the domain baseline for everyone. Deploy **RODCs** where physical
security is weak. Add **trusts** only for a real cross-boundary requirement,
prefer **selective authentication** on forest trusts so access is explicit,
and remember that a trust is an authentication path, not automatic access —
permissions still gate resources.

## Implementation and Automation

Bulk user creation and group nesting are routine PowerShell:

```powershell
# OU, a role group, a resource group, and a user placed correctly
New-ADOrganizationalUnit -Name "Sales" -Path "OU=Users,DC=corp,DC=contoso,DC=lab"
New-ADGroup -Name "GG-Sales" -GroupScope Global -Path "OU=Groups,DC=corp,DC=contoso,DC=lab"
New-ADGroup -Name "DL-SalesShare-RW" -GroupScope DomainLocal -Path "OU=Groups,DC=corp,DC=contoso,DC=lab"
Add-ADGroupMember -Identity "DL-SalesShare-RW" -Members "GG-Sales"   # AGDLP: G into DL

New-ADUser -Name "Ana Ruiz" -SamAccountName "aruiz" `
  -Path "OU=Sales,OU=Users,DC=corp,DC=contoso,DC=lab" `
  -AccountPassword (Read-Host -AsSecureString) -Enabled $true
Add-ADGroupMember -Identity "GG-Sales" -Members "aruiz"              # AGDLP: A into G
```

A fine-grained password policy for administrators:

```powershell
New-ADFineGrainedPasswordPolicy -Name "PSO-Admins" -Precedence 10 `
  -MinPasswordLength 16 -ComplexityEnabled $true -LockoutThreshold 5 `
  -MaxPasswordAge "60.00:00:00"
Add-ADFineGrainedPasswordPolicySubject -Identity "PSO-Admins" -Subjects "GG-Domain-Admins"
```

Delegation with `dsacls` (or the Delegation of Control Wizard) grants the
help desk password resets on the Sales OU:

```powershell
dsacls "OU=Sales,OU=Users,DC=corp,DC=contoso,DC=lab" /I:S `
  /G "CORP\GG-Helpdesk:CA;Reset Password;user"
```

## Validation and Troubleshooting

Verify membership, effective policy, and delegation:

```powershell
Get-ADGroupMember "DL-SalesShare-RW"                       # should include GG-Sales
Get-ADUserResultantPasswordPolicy -Identity "aruiz"        # which PSO applies?
(Get-Acl "AD:\OU=Sales,OU=Users,DC=corp,DC=contoso,DC=lab").Access |
  Where-Object IdentityReference -like "*Helpdesk*"
```

`Get-ADUserResultantPasswordPolicy` returns the winning PSO by precedence
(lowest number wins), or nothing if only the default domain policy applies.
Common issues: a user in the default `Users` container gets no OU-linked
policy or delegation; a permission assigned to a **Global** group for a
resource in **another** domain silently fails (scope rules); nested group
membership not reflecting because the user has not obtained a new Kerberos
ticket (log off/on or `klist purge`); and trust failures caused by name
resolution or missing DNS conditional forwarders between forests.

## Security and Best Practices

Follow **least privilege** through AGDLP and scoped delegation. Keep
privileged groups (**Domain Admins**, **Enterprise Admins**, **Schema
Admins**) as small as possible and empty of day-to-day accounts — use them
only when required and protect them with FGPP and the **Protected Users**
group (Chapter 10). Enable **AD Recycle Bin** so an accidental delete is
recoverable, and turn on **accidental-deletion protection** on OUs. Audit
group-membership and delegation changes. Use **managed service accounts**
(gMSA, Chapter 10) instead of user accounts for services so passwords
rotate automatically. Deploy **RODCs** with a filtered attribute set at
insecure sites so a stolen DC leaks minimal credentials.

## References and Knowledge Checks

- Microsoft Learn: *Manage AD DS users and groups*; *Group scopes*; *Fine-grained password policies*; *RODC*.
- Microsoft Learn: AZ-800 — *Create and manage AD DS objects; configure trusts*.

**Knowledge checks**

1. In AGDLP, what goes into a Global group and what goes into a Domain Local group, and why?
2. When is a Universal group the right scope, and what is its cost?
3. Why does a trust not automatically grant access to resources?

## Hands-On Lab

Topic-level walkthroughs for AZ-800's object-management and trust skills.

**Shared prerequisites for Labs 4.1–4.4** — the `corp.contoso.lab` domain
from Chapter 03 and Domain Admin rights. **Cost:** none.

### Lab 4.1 — Build an OU and AGDLP groups (Topic: Manage groups and OUs)

**Objective:** Create the role/resource group pattern correctly.

```powershell
New-ADOrganizationalUnit -Name "Groups" -Path "DC=corp,DC=contoso,DC=lab" -ProtectedFromAccidentalDeletion $true
New-ADGroup -Name "GG-Sales" -GroupScope Global -Path "OU=Groups,DC=corp,DC=contoso,DC=lab"
New-ADGroup -Name "DL-SalesShare-RW" -GroupScope DomainLocal -Path "OU=Groups,DC=corp,DC=contoso,DC=lab"
Add-ADGroupMember "DL-SalesShare-RW" -Members "GG-Sales"
Get-ADGroupMember "DL-SalesShare-RW"
```

**Expected result:** `GG-Sales` (Global) is a member of `DL-SalesShare-RW`
(Domain Local) — the AGDLP nesting that keeps role membership separate from
resource permissioning.

**Negative test:** try `Add-ADGroupMember` to put a Domain Local group into
a Global group; AD rejects it — scope rules forbid that nesting direction.

**Rollback:** remove the two groups and the OU.

### Lab 4.2 — Create a user and confirm placement (Topic: Manage users)

**Objective:** Provision a user in the right OU and role group.

```powershell
New-ADOrganizationalUnit -Name "Sales" -Path "OU=Users,DC=corp,DC=contoso,DC=lab" -ErrorAction SilentlyContinue
New-ADUser -Name "Ana Ruiz" -SamAccountName "aruiz" `
  -Path "OU=Sales,OU=Users,DC=corp,DC=contoso,DC=lab" `
  -AccountPassword (ConvertTo-SecureString 'Start-123!' -AsPlainText -Force) `
  -ChangePasswordAtLogon $true -Enabled $true
Add-ADGroupMember "GG-Sales" -Members "aruiz"
Get-ADUser aruiz -Properties MemberOf | Select-Object DistinguishedName, MemberOf
```

**Expected result:** `aruiz` is in the Sales OU and a member of `GG-Sales` —
accounts go into Global role groups (the "A into G" of AGDLP).

**Negative test:** create the user without `-Path`; it lands in the default
`Users` container where OU-linked GPOs and delegation do not apply.

**Rollback:** `Remove-ADUser aruiz -Confirm:$false`.

### Lab 4.3 — Delegate password resets to the help desk (Topic: Delegate administration)

**Objective:** Grant a scoped right, not full control.

```powershell
New-ADGroup -Name "GG-Helpdesk" -GroupScope Global -Path "OU=Groups,DC=corp,DC=contoso,DC=lab"
dsacls "OU=Sales,OU=Users,DC=corp,DC=contoso,DC=lab" /I:S /G "CORP\GG-Helpdesk:CA;Reset Password;user"
(Get-Acl "AD:\OU=Sales,OU=Users,DC=corp,DC=contoso,DC=lab").Access |
  Where-Object IdentityReference -like "*Helpdesk*" | Select-Object ActiveDirectoryRights, ObjectType
```

**Expected result:** `GG-Helpdesk` has the "Reset Password" control right on
the Sales OU and its user objects — least privilege, delegated to a group at
a scope.

**Negative test:** grant the help desk `GENERIC_ALL` instead; they gain full
control including group membership — over-delegation is a privilege-escalation
path, so grant the specific control right only.

**Rollback:** `dsacls "OU=Sales,OU=Users,DC=corp,DC=contoso,DC=lab" /R "CORP\GG-Helpdesk"`.

### Lab 4.4 — Apply a fine-grained password policy (Topic: Configure password policies)

**Objective:** Raise requirements for a privileged group only.

```powershell
New-ADFineGrainedPasswordPolicy -Name "PSO-Helpdesk" -Precedence 20 `
  -MinPasswordLength 16 -ComplexityEnabled $true -LockoutThreshold 5 -LockoutDuration "00:30:00"
Add-ADFineGrainedPasswordPolicySubject "PSO-Helpdesk" -Subjects "GG-Helpdesk"
Add-ADGroupMember "GG-Helpdesk" -Members "aruiz"   # temporary, to test resolution
Get-ADUserResultantPasswordPolicy aruiz | Select-Object Name, MinPasswordLength
```

**Expected result:** the resultant policy for a `GG-Helpdesk` member is
`PSO-Helpdesk` with a 16-character minimum — FGPP raises the bar for the
group without changing the domain default.

**Negative test:** create a second PSO with the same precedence; AD requires
unique precedence values to resolve ties deterministically.

**Rollback:** remove the PSO and the temporary membership.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

AD DS objects are users, computers, groups, and OUs. Group scope plus AGDLP
nesting keep access control manageable; OUs exist for delegation and Group
Policy; delegation grants the least right to a group at a scope; FGPP raises
requirements for privileged principals; and RODCs and trusts extend the
directory to insecure sites and other forests.

- [ ] I can apply AGDLP and choose the correct group scope.
- [ ] I can design OUs for delegation and policy, not the org chart.
- [ ] I can delegate a scoped right to a group.
- [ ] I can apply FGPP and explain RODCs and trusts.
- [ ] I completed Labs 4.1–4.4 including each negative test.
