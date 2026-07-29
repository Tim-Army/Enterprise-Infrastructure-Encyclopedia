# Chapter 05: Group Policy — Processing, Preferences, Filtering, and the Central Store

## Learning Objectives

- Explain Group Policy architecture: GPOs, links, the Group Policy container and template, and versioning.
- Predict the order of policy processing (LSDOU) and the effect of Enforced and Block Inheritance.
- Scope a GPO precisely with security filtering, WMI filters, and item-level targeting.
- Distinguish policy settings from Group Policy Preferences and use each correctly.
- Deploy the ADMX central store and troubleshoot policy with `gpresult` and the Group Policy Modeling tools.

## Theory and Architecture

Group Policy delivers configuration to users and computers from Active
Directory. A **Group Policy Object (GPO)** has two parts: the **Group
Policy Container** in AD (metadata, version, status) and the **Group Policy
Template** in `SYSVOL` (the actual `.pol`, script, and ADMX-driven files),
replicated to every DC. A GPO does nothing until it is **linked** to a
**site**, **domain**, or **OU**. A computer or user object receives every
GPO linked to the containers above it in the directory path.

Processing order is **LSDOU**: **Local** policy first, then **Site**, then
**Domain**, then each **OU** from the top of the tree down to the object's
own OU. Later wins, so an OU-level setting overrides a domain-level one for
the same policy — unless the higher link is **Enforced** (formerly
"No Override"), which makes it win and survive **Block Inheritance** on a
lower OU. Computer settings apply at startup and refresh; user settings
apply at logon and refresh; the default background refresh is about every 90
minutes with a random offset.

Two categories of content share the editor. **Policy settings** are
authoritative — the user cannot change them and they revert if the GPO no
longer applies (they live in the managed portion of the registry). **Group
Policy Preferences** set an initial or ongoing configuration — mapped
drives, scheduled tasks, registry values, local group membership, printers
— that can be changed by the user unless re-applied, and that support
powerful **item-level targeting** (apply only if the machine is a laptop,
in an IP range, a member of a group, and so on).

**Scoping** beyond the link uses **security filtering** (the GPO applies
only to principals with Read and Apply Group Policy — by default
Authenticated Users, tightened to specific groups) and **WMI filters** (a
WQL query gates application, for example only to workstations or a specific
OS build). The **ADMX central store** is a `SYSVOL` folder holding one
authoritative copy of the administrative template definitions so every
admin edits the same settings regardless of their workstation's local ADMX
version.

## Design Considerations

Design GPOs to be **few, focused, and well-named** — a "Baseline-Servers"
GPO, a "Security-Workstations" GPO, a "Mapped-Drives-Sales" preference GPO
— rather than one giant GPO or dozens of single-setting ones. Link at the
**lowest** container that covers the target audience to keep scope
predictable. Reserve **Enforced** for genuinely non-negotiable settings
(security baselines) and **Block Inheritance** for exceptional OUs; overuse
of either makes resultant policy hard to reason about.

Prefer **security filtering by group** over per-object exceptions, and use
**WMI filters** sparingly because each one is evaluated at every refresh and
adds cost. Use **Preferences with item-level targeting** where a single GPO
must behave differently by device attribute, instead of proliferating GPOs.
Always deploy the **central store** so ADMX drift between admin workstations
cannot cause inconsistent editing. Keep **loopback processing** (apply user
settings based on the computer's location) for kiosks, RDS hosts, and
shared machines, and know it changes how user policy is scoped.

## Implementation and Automation

The `GroupPolicy` module scripts the whole lifecycle:

```powershell
New-GPO -Name "Baseline-Servers" -Comment "Server security baseline"
Set-GPRegistryValue -Name "Baseline-Servers" `
  -Key "HKLM\System\CurrentControlSet\Control\Lsa" -ValueName "LimitBlankPasswordUse" `
  -Type DWord -Value 1
New-GPLink -Name "Baseline-Servers" -Target "OU=Servers,DC=corp,DC=contoso,DC=lab" -LinkEnabled Yes
```

Security-filter a GPO to a group instead of everyone:

```powershell
Set-GPPermission -Name "Baseline-Servers" -TargetName "Authenticated Users" `
  -TargetType Group -PermissionLevel None -Replace
Set-GPPermission -Name "Baseline-Servers" -TargetName "GG-Member-Servers" `
  -TargetType Group -PermissionLevel GpoApply
```

Create the ADMX central store by copying local definitions into `SYSVOL`:

```powershell
$cs = "\\corp.contoso.lab\SYSVOL\corp.contoso.lab\Policies\PolicyDefinitions"
New-Item $cs -ItemType Directory -Force
Copy-Item "C:\Windows\PolicyDefinitions\*" $cs -Recurse -Force   # includes the en-US language folder
```

## Validation and Troubleshooting

`gpresult` shows what actually applied and, crucially, what did **not** and
why:

```powershell
gpupdate /force
gpresult /r                     # summary of applied GPOs for user + computer
gpresult /h C:\gpreport.html    # full HTML Resultant Set of Policy
Get-GPResultantSetOfPolicy -ReportType Html -Path C:\rsop.html -Computer FS01
```

The RSoP report lists **applied** GPOs, **denied** GPOs with the reason
(access denied by security filtering, disabled link, WMI filter mismatch,
empty), and the winning setting for each policy. Common issues: a GPO not
applying because **Authenticated Users** was removed from security
filtering without also granting Read to the target group (since a 2016
security update, the computer account needs Read to read the GPO); a
setting not taking effect because a higher **Enforced** link overrides it;
**SYSVOL replication** lag so a new GPO has not reached the client's DC; and
Preferences appearing not to apply because item-level targeting excluded the
device. `dcgpofix` restores the default domain GPOs if they are damaged.

## Security and Best Practices

Use Group Policy to deploy **security baselines** (the Microsoft Security
Compliance Toolkit baselines are a strong starting point) via Enforced links
so they cannot be blocked. Keep GPO **delegation** tight — linking and
editing rights are powerful. Store secrets **never** in Preferences: the old
"set local admin password via Preferences" pattern was broken by a published
decryption key, so use **Windows LAPS** (Chapter 10) instead. Audit GPO
changes and back up GPOs (`Backup-GPO`) so a bad edit can be rolled back.
Prefer **policy settings** over Preferences for anything that must be
enforced, since Preferences can be changed by the user unless continually
re-applied.

## References and Knowledge Checks

- Microsoft Learn: *Group Policy overview*; *Group Policy processing and precedence*; *Central Store for ADMX*.
- Microsoft Learn: AZ-800 — *Manage Group Policy Objects*.

**Knowledge checks**

1. State the LSDOU order and where Enforced and Block Inheritance change it.
2. What is the practical difference between a policy setting and a Preference?
3. After removing Authenticated Users from security filtering, what else must you grant, and why?

## Hands-On Lab

Topic-level walkthroughs for AZ-800's Group Policy skills.

**Shared prerequisites for Labs 5.1–5.4** — the `corp.contoso.lab` domain,
a `Servers` OU with a member server, and Domain Admin rights. **Cost:** none.

### Lab 5.1 — Create, configure, and link a GPO (Topic: Author policy)

**Objective:** Deliver a registry-backed setting to an OU.

```powershell
New-GPO -Name "Baseline-Servers"
Set-GPRegistryValue -Name "Baseline-Servers" `
  -Key "HKLM\SOFTWARE\Policies\Microsoft\Windows\Explorer" -ValueName "NoDrives" -Type DWord -Value 0
New-GPLink -Name "Baseline-Servers" -Target "OU=Servers,DC=corp,DC=contoso,DC=lab"
Get-GPInheritance -Target "OU=Servers,DC=corp,DC=contoso,DC=lab" | Select-Object -Expand GpoLinks
```

**Expected result:** the GPO is linked to the Servers OU and appears in its
inheritance list — a GPO does nothing until linked to a site, domain, or OU.

**Negative test:** create the GPO but do not link it; `gpresult` on a server
never lists it — an unlinked GPO is inert.

**Cleanup:** `Remove-GPLink -Name "Baseline-Servers" -Target "OU=Servers,DC=corp,DC=contoso,DC=lab"; Remove-GPO "Baseline-Servers"`.

### Lab 5.2 — Security-filter a GPO to a group (Topic: Scope policy)

**Objective:** Apply a GPO only to member servers, not everyone.

```powershell
New-ADGroup -Name "GG-Member-Servers" -GroupScope Global -Path "OU=Groups,DC=corp,DC=contoso,DC=lab" -ErrorAction SilentlyContinue
Set-GPPermission "Baseline-Servers" -TargetName "Authenticated Users" -TargetType Group -PermissionLevel None -Replace
Set-GPPermission "Baseline-Servers" -TargetName "GG-Member-Servers" -TargetType Group -PermissionLevel GpoApply
Get-GPPermission "Baseline-Servers" -All | Select-Object Trustee, Permission
```

**Expected result:** only `GG-Member-Servers` has Apply — security filtering
narrows a broadly linked GPO to a specific set of principals.

**Negative test:** remove Authenticated Users without granting the computer
group Read; the GPO stops applying because the computer account can no
longer read it — grant the target group Read (GpoApply includes Read).

**Cleanup:** restore Authenticated Users or remove the test GPO.

### Lab 5.3 — Deploy the ADMX central store (Topic: Manage administrative templates)

**Objective:** Make one authoritative set of ADMX definitions.

```powershell
$cs = "\\corp.contoso.lab\SYSVOL\corp.contoso.lab\Policies\PolicyDefinitions"
New-Item $cs -ItemType Directory -Force
Copy-Item "C:\Windows\PolicyDefinitions\*" $cs -Recurse -Force
Test-Path "$cs\en-US\Windows.adml"
```

**Expected result:** the central store exists and contains the language
folder; the Group Policy editor now shows "Policy definitions (ADMX files)
retrieved from the central store" — every admin edits the same templates.

**Negative test:** copy the ADMX files but omit the `en-US` language folder;
the editor shows errors for missing ADML — ADMX (settings) need matching
ADML (language) files.

**Cleanup:** `Remove-Item $cs -Recurse -Force` (lab only).

### Lab 5.4 — Diagnose resultant policy (Topic: Troubleshoot Group Policy)

**Objective:** Prove what applied and why something did not.

```powershell
gpupdate /force
gpresult /r /scope:computer
Get-GPResultantSetOfPolicy -ReportType Html -Path C:\rsop.html
```

**Expected result:** the RSoP report lists `Baseline-Servers` under applied
GPOs (for a member of the filtered group) and lists denied GPOs with a
reason — RSoP is the authoritative "why" for Group Policy.

**Negative test:** run `gpresult /r` in a non-elevated prompt for computer
scope; it refuses — computer-scope RSoP requires elevation.

**Cleanup:** `Remove-Item C:\rsop.html`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Group Policy applies configuration from AD in LSDOU order, with Enforced and
Block Inheritance as the exceptions. GPOs are scoped by link, security
filtering, and WMI filters; policy settings are authoritative while
Preferences are changeable and support item-level targeting; the ADMX
central store keeps editing consistent; and `gpresult`/RSoP is the tool for
proving and diagnosing what applied.

- [ ] I can predict resultant policy from LSDOU, Enforced, and Block Inheritance.
- [ ] I can scope a GPO with security filtering and know the Read requirement.
- [ ] I can choose between a policy setting and a Preference.
- [ ] I can deploy the central store and diagnose with RSoP.
- [ ] I completed Labs 5.1–5.4 including each negative test.
