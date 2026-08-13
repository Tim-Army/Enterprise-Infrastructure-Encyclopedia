# Chapter 06: Compliance Policies, Configuration Profiles, and Endpoint Security

## Learning Objectives

- Build device compliance policies and connect them to Conditional Access.
- Configure devices with configuration profiles and the settings catalog.
- Apply endpoint security policies and security baselines.
- Manage Windows updates with update rings and feature-update policies.
- Interpret policy assignment, conflicts, and per-setting reporting.

## Theory and Architecture

Once devices are enrolled (Chapter 05), Intune governs them with three
policy families that often blur together but do different jobs.

**Compliance policies** define what a **healthy** device is — minimum OS
version, BitLocker/FileVault encryption, firewall on, no jailbreak/root, a
minimum Defender risk score — and set a **compliance state** and **actions
for noncompliance** (mark noncompliant after a grace period, notify, or
remotely lock). Compliance is the signal Conditional Access consumes: "allow
only compliant devices." A device with **no compliance policy assigned** is,
by a tenant setting, treated as compliant or noncompliant — a setting worth
getting right.

**Configuration profiles** set how a device is **configured** — Wi-Fi, VPN,
certificates, email profiles, browser and OS settings, and the modern
**settings catalog**, a searchable library of thousands of individual
settings that has largely replaced the older per-template profiles. Profiles
push desired configuration to enrolled devices.

**Endpoint security** is a focused workspace for security posture:
**antivirus** (Defender), **disk encryption** (BitLocker/FileVault),
**firewall**, **endpoint detection and response** (onboarding to Defender for
Endpoint), **attack surface reduction**, and **account protection**, plus
**security baselines** — Microsoft-recommended, pre-configured bundles of
hardening settings for Windows, Edge, and Defender that you deploy and then
tune.

**Windows Update for Business** is managed in Intune through **update rings**
(defer quality and feature updates, set deadlines and active hours),
**feature update** policies (target a specific Windows version), and
**expedite** policies (push a critical update fast). This replaces WSUS for
cloud-managed devices and pairs with **Windows Autopatch** for hands-off
patching.

Every policy is **assigned** to Entra groups (user or device). When two
profiles set the same setting differently, there is a **conflict**, and the
device reports the setting as in conflict until resolved — which is why
per-setting reporting matters.

## Design Considerations

Write **compliance policies per platform** with the controls Conditional
Access will require (encryption, OS floor, Defender risk), set a **grace
period** so a briefly noncompliant device is not instantly blocked, and set
the **"no policy = noncompliant"** tenant default so unmanaged states fail
safe. Then require **compliant devices** in Conditional Access for sensitive
apps.

Prefer the **settings catalog** over legacy templates for new configuration —
it is granular, searchable, and consistently reported. Keep profiles
**focused** (a Wi-Fi profile, a security profile) rather than monolithic, and
assign by **device group** for machine settings and **user group** for
user settings. Deploy **security baselines** as the hardening starting point,
review each changed setting, and layer endpoint-security policies for AV,
encryption, firewall, ASR, and EDR onboarding.

Design **update rings** in waves — a pilot ring with short deferrals and a
broad ring with longer deferrals and deadlines — so a bad update is caught
early. Consider **Autopatch** to offload ring management. Plan for
**conflicts**: fewer, well-scoped policies mean fewer collisions.

## Implementation and Automation

Compliance and configuration use Graph `deviceManagement` endpoints. Create a
Windows compliance policy requiring BitLocker and a minimum build:

```powershell
Connect-MgGraph -Scopes "DeviceManagementConfiguration.ReadWrite.All"
New-MgDeviceManagementDeviceCompliancePolicy -BodyParameter @{
  "@odata.type"="#microsoft.graph.windows10CompliancePolicy"
  displayName="Win - Baseline compliance"
  bitLockerEnabled=$true; secureBootEnabled=$true; osMinimumVersion="10.0.26100.0"
  scheduledActionsForRule=@(@{ ruleName="PasswordRequired"
    scheduledActionConfigurations=@(@{ actionType="block"; gracePeriodHours=24 }) }) }
```

Create a settings-catalog configuration policy (structure abbreviated):

```powershell
New-MgDeviceManagementConfigurationPolicy -BodyParameter @{
  name="Win - Edge hardening"; platforms="windows10"; technologies="mdm"
  settings=@( <# settingInstance objects from the settings catalog #> ) }
```

Create a Windows update ring:

```powershell
New-MgDeviceManagementDeviceConfiguration -BodyParameter @{
  "@odata.type"="#microsoft.graph.windowsUpdateForBusinessConfiguration"
  displayName="Update ring - Pilot"
  qualityUpdatesDeferralPeriodInDays=2; featureUpdatesDeferralPeriodInDays=7
  automaticUpdateMode="autoInstallAtMaintenanceTime"; deadlineForQualityUpdatesInDays=3 }
```

## Validation and Troubleshooting

Check compliance state, profile assignment, and conflicts:

```powershell
Get-MgDeviceManagementManagedDevice -Filter "complianceState eq 'noncompliant'" |
  Select-Object DeviceName, OperatingSystem, ComplianceState
Get-MgDeviceManagementDeviceCompliancePolicy | Select-Object DisplayName
# Per-device configuration status (portal: Device > Device configuration shows per-setting state)
```

The portal's **per-setting status** and **device configuration** views show
`Succeeded`, `Error`, or `Conflict` for each setting. Common issues: a device
**noncompliant** because encryption or an OS floor is not met (fix the device
or adjust the policy), or because the compliance policy simply has not
evaluated yet (there is a check-in interval — force a sync from Company
Portal); a setting in **Conflict** because two profiles set it differently
(remove the duplicate or scope them apart); a **baseline** breaking an app
because a hardening setting is too strict (tune the baseline); and Conditional
Access blocking access because the device is not yet reporting compliant.
Update rings not applying usually means the device is targeted by a
conflicting update policy or is co-managed with the workload still on
Configuration Manager.

## Security and Best Practices

Make **compliance the gate** for Conditional Access and require encryption,
secure boot, an OS floor, and an acceptable Defender risk level. Deploy
**security baselines** and layer **endpoint security** policies for AV,
BitLocker/FileVault, firewall, **ASR**, and **Defender for Endpoint EDR
onboarding**. Prefer the **settings catalog** for clarity and reporting.
Patch continuously with **update rings** in waves (or Autopatch), never
leaving devices unmanaged for updates. Minimize policy count to avoid
**conflicts**, and monitor **per-setting reporting** so drift and errors are
visible. Set the tenant default so **devices with no compliance policy are
noncompliant** — fail safe, not open.

## References and Knowledge Checks

- Microsoft Learn: *Device compliance policies*; *Configuration profiles and settings catalog*; *Endpoint security and baselines*; *Windows Update for Business / Autopatch*.
- Microsoft Learn: MD-102 — *Manage, maintain, and protect devices*.

**Knowledge checks**

1. How does a compliance policy connect to Conditional Access?
2. Why prefer the settings catalog over legacy configuration templates?
3. What causes a setting to report "Conflict," and how do you resolve it?

## Hands-On Lab

Topic-level walkthroughs for MD-102 protect-and-configure skills.

**Shared prerequisites for Labs 6.1–6.4** — a Microsoft 365 tenant with Intune,
a Graph session with `DeviceManagementConfiguration.ReadWrite.All`, an
enrolled Windows device, and admin rights. **Cost:** none.

### Lab 6.1 — Create a compliance policy (Topic: Device compliance)

**Objective:** Define a healthy Windows device.

```powershell
New-MgDeviceManagementDeviceCompliancePolicy -BodyParameter @{
  "@odata.type"="#microsoft.graph.windows10CompliancePolicy"; displayName="Win - Baseline compliance"
  bitLockerEnabled=$true; secureBootEnabled=$true; osMinimumVersion="10.0.26100.0"
  scheduledActionsForRule=@(@{ ruleName="PasswordRequired"
    scheduledActionConfigurations=@(@{ actionType="block"; gracePeriodHours=24 }) }) }
Get-MgDeviceManagementDeviceCompliancePolicy | Select-Object DisplayName
```

**Expected result:** the policy exists requiring BitLocker, Secure Boot, and a
minimum build, with a 24-hour grace period — the signal Conditional Access will
require.

**Negative test:** assign it and then require compliant devices in CA before
the policy evaluates; devices are briefly blocked — the grace period and
report-only staging avoid surprise lockouts.

**Rollback:** remove the compliance policy.

### Lab 6.2 — Confirm noncompliant devices (Topic: Monitor compliance)

**Objective:** Find devices failing the policy.

```powershell
Get-MgDeviceManagementManagedDevice -Filter "complianceState eq 'noncompliant'" |
  Select-Object DeviceName, OperatingSystem, ComplianceState
```

**Expected result:** any noncompliant devices are listed — the same set
Conditional Access would block from sensitive apps.

**Negative test:** expect an unenrolled device to appear as noncompliant; it
does not appear at all — only managed devices report compliance.

**Rollback:** none (read-only).

### Lab 6.3 — Create a Windows update ring (Topic: Update management)

**Objective:** Stage patch deployment.

```powershell
New-MgDeviceManagementDeviceConfiguration -BodyParameter @{
  "@odata.type"="#microsoft.graph.windowsUpdateForBusinessConfiguration"; displayName="Update ring - Pilot"
  qualityUpdatesDeferralPeriodInDays=2; featureUpdatesDeferralPeriodInDays=7
  automaticUpdateMode="autoInstallAtMaintenanceTime"; deadlineForQualityUpdatesInDays=3 }
Get-MgDeviceManagementDeviceConfiguration | Where-Object DisplayName -like "Update ring*" | Select-Object DisplayName
```

**Expected result:** a pilot ring defers updates two/seven days with a
three-day deadline — waves catch a bad update before broad rollout.

**Negative test:** assign two update rings to the same device with different
deferrals; the settings conflict and the device reports an error — a device
should be in one ring.

**Rollback:** remove the update-ring configuration.

### Lab 6.4 — Inspect per-setting configuration status (Topic: Troubleshoot configuration)

**Objective:** See how a profile actually landed.

```powershell
# Portal: Devices > <device> > Device configuration shows per-setting Succeeded/Error/Conflict
Get-MgDeviceManagementManagedDevice -Filter "deviceName eq 'LAPTOP-01'" |
  Select-Object DeviceName, ComplianceState, ManagementState
```

**Expected result:** the device shows configuration and compliance state; the
portal's per-setting view flags any setting in `Conflict` — the authoritative
place to diagnose configuration.

**Negative test:** deploy two profiles that set the same setting to different
values; the per-setting status shows `Conflict` — resolve by removing the
duplicate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Intune governs enrolled devices with compliance policies (the Conditional
Access health signal), configuration profiles and the settings catalog (how a
device is configured), endpoint security and baselines (posture), and Windows
Update for Business rings (patching). Assignment, conflicts, and per-setting
reporting determine what actually applies.

- [ ] I can build compliance policies wired to Conditional Access.
- [ ] I can configure devices with the settings catalog.
- [ ] I can deploy endpoint-security baselines and update rings.
- [ ] I can interpret assignment, conflicts, and per-setting status.
- [ ] I completed Labs 6.1–6.4 including each negative test.
