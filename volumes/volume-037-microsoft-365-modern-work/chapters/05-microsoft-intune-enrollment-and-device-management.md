# Chapter 05: Microsoft Intune — Enrollment and Device Management

## Learning Objectives

- Describe Microsoft Intune's place in the endpoint-management stack and the MDM/MAM models.
- Configure the enrollment prerequisites: MDM authority, automatic enrollment, and platform connectors.
- Enroll Windows, iOS/iPadOS, Android, and macOS devices with the right method per platform.
- Manage the device lifecycle: inventory, categories, primary user, and retire/wipe.
- Validate enrollment and troubleshoot the common failure modes.

## Theory and Architecture

**Microsoft Intune** is the cloud service for managing endpoints in Microsoft
365. It provides **mobile device management (MDM)** — enrolling and managing
the whole device — and **mobile application management (MAM)** — protecting
corporate data inside apps without managing the device, used for BYOD. Intune
is the enforcement point behind Conditional Access device-compliance
(Chapter 03): a device reports compliant to Intune, and Conditional Access
then allows access.

Enrollment has **prerequisites**. Intune must be the **MDM authority**
(default in modern tenants). **Automatic enrollment** links Entra join to
Intune so a corporate Windows device that joins Entra is enrolled without
extra steps (configured in the MDM user scope). Each platform needs a
**connector or certificate**: **Apple MDM push certificate** for iOS/iPadOS
and macOS, **Apple Business Manager** for automated device enrollment, and a
**Managed Google Play** connection for Android Enterprise.

**Enrollment methods** differ by platform and ownership. Windows: **Entra
join + automatic enrollment** (corporate), **Autopilot** (zero-touch, Chapter
07), **group policy / bulk** enrollment, or **BYOD** enrollment. iOS/iPadOS
and macOS: **Automated Device Enrollment (ADE)** via Apple Business Manager
(corporate, supervised) or **user enrollment** (BYOD). Android:
**fully managed**, **dedicated** (kiosk), or **corporate-owned work profile**
for corporate, and **personally owned work profile** for BYOD. Choosing the
method sets how much control and how much user-data separation you get.

The **device lifecycle** runs from enrollment through inventory, categories,
primary-user assignment, and compliance/configuration (Chapters 06–07) to
**retire** (remove corporate data, leave personal) or **wipe** (factory
reset). Intune records hardware and software inventory and surfaces it for
reporting and targeting.

## Design Considerations

Decide the **management model per scenario**: full **MDM** for corporate-owned
devices, **MAM/app protection** for BYOD where you must not manage the whole
personal device. Configure **automatic enrollment** so corporate Windows
devices are managed the moment they join Entra, and scope the **MDM user
scope** to the right groups. Stand up the **Apple** and **Android**
connectors before enrolling those platforms — they are hard prerequisites.

Choose **enrollment methods** that match ownership: **Autopilot/ADE** for
zero-touch corporate provisioning, **work profile** for Android BYOD to keep
personal and work data separate, and **user enrollment** for iOS BYOD.
Restrict enrollment with **enrollment restrictions** (block personal devices
on a platform, cap devices per user, require a minimum OS). Assign **device
categories** so devices land in the right dynamic groups for policy, and set
a meaningful **primary user** for user-targeted policies and app licensing.

Remember the split between **device-targeted** and **user-targeted** policy:
device policies apply regardless of who signs in (kiosks, shared devices),
user policies follow the person. Design group targeting accordingly.

## Implementation and Automation

Intune management uses the **DeviceManagement** Graph endpoints. Check
enrollment configuration and inventory:

```powershell
Connect-MgGraph -Scopes "DeviceManagementServiceConfig.ReadWrite.All","DeviceManagementManagedDevices.ReadWrite.All","DeviceManagementConfiguration.ReadWrite.All"
# Managed device inventory
Get-MgDeviceManagementManagedDevice -Top 10 |
  Select-Object DeviceName, OperatingSystem, ComplianceState, ManagedDeviceOwnerType, EnrolledDateTime
# Enrollment restrictions (device platform restrictions)
Get-MgDeviceManagementDeviceEnrollmentConfiguration | Select-Object DisplayName, "@odata.type"
```

Create an enrollment restriction that blocks personal Android and requires a
minimum iOS version (portal is the usual path; Graph shown for automation):

```powershell
# Example: cap devices per user via the device limit restriction (portal-managed)
Get-MgDeviceManagementDeviceEnrollmentConfiguration |
  Where-Object { $_.AdditionalProperties["@odata.type"] -match "Limit" } |
  Select-Object Id, DisplayName
```

Retire or wipe a device:

```powershell
$d = Get-MgDeviceManagementManagedDevice -Filter "deviceName eq 'LAPTOP-01'"
# Retire: remove corporate data, keep personal
Invoke-MgRetireDeviceManagementManagedDevice -ManagedDeviceId $d.Id
# Wipe: factory reset
Clear-MgDeviceManagementManagedDevice -ManagedDeviceId $d.Id -KeepEnrollmentData:$false -KeepUserData:$false
```

## Validation and Troubleshooting

Confirm enrollment, ownership, and the compliance link:

```powershell
Get-MgDeviceManagementManagedDevice -Filter "deviceName eq 'LAPTOP-01'" |
  Select-Object DeviceName, ManagementAgent, ComplianceState, AzureAdRegistered, ManagedDeviceOwnerType
# On a Windows device: dsregcmd /status shows AzureAdJoined + MDMUrl (enrolled)
```

`dsregcmd /status` on Windows shows `AzureAdJoined : YES` and an `MDMUrl`
when enrolled. Common issues: a Windows device Entra-joined but **not
enrolled** because automatic enrollment or the MDM user scope was not
configured; **iOS/Android enrollment failing** because the Apple MDM push
certificate expired or the Managed Google Play connection lapsed (both need
renewal); a device blocked by an **enrollment restriction** (personal device
on a blocked platform, or over the per-user limit); a device showing
**not compliant** because a compliance policy has not yet evaluated
(Chapter 06); and Conditional Access denying access because the device is not
yet reporting compliant. The **Company Portal** app is the user-side
enrollment and status surface.

## Security and Best Practices

Require **enrolled, compliant devices** for access to corporate data via
Conditional Access. Use **MAM/app protection** for BYOD so corporate data is
containerized without managing personal devices. Set **enrollment
restrictions** to block unmanaged platforms and cap devices per user. Keep
the **Apple push certificate** and **Managed Google Play** connections
monitored and renewed — an expired certificate silently breaks enrollment.
Prefer **supervised/ADE** and **Android Enterprise work profiles** for strong
separation and control. Scope **retire** for offboarding personal devices
(leave personal data) and **wipe** for lost or corporate devices. Record a
**primary user** and **device category** so policy targeting and licensing
are correct.

## References and Knowledge Checks

- Microsoft Learn: *Microsoft Intune enrollment*; *Enrollment restrictions*; *Apple/Android connectors*; *Device lifecycle*.
- Microsoft Learn: MD-102 — *Deploy Windows client; manage identity and compliance; manage devices*.

**Knowledge checks**

1. What is the difference between MDM and MAM, and when is each appropriate?
2. What prerequisites must exist before enrolling iOS and Android devices?
3. What is the difference between retire and wipe?

## Hands-On Lab

Topic-level walkthroughs for MD-102 enrollment and device-management skills.

**Shared prerequisites for Labs 5.1–5.4** — a Microsoft 365 tenant with Intune
(EMS/E3+), a Graph session with the DeviceManagement scopes above, at least
one enrollable device, and admin rights. **Cost:** none (trial licensing).

### Lab 5.1 — Confirm automatic enrollment and MDM scope (Topic: Enrollment prerequisites)

**Objective:** Verify corporate Windows devices will auto-enroll.

```powershell
# MDM user scope is set in Entra > Mobility (MDM and MAM) > Microsoft Intune (portal)
Get-MgDeviceManagementDeviceEnrollmentConfiguration | Select-Object DisplayName,
  @{n='Type';e={$_.AdditionalProperties["@odata.type"]}}
```

**Expected result:** enrollment configurations (platform restrictions, device
limit, Windows Hello) are listed; with the MDM user scope set to a group,
Entra-joined Windows devices for those users enroll automatically.

**Negative test:** leave the MDM user scope as `None`; Entra-joined Windows
devices join but never enroll in Intune — automatic enrollment needs the scope.

**Rollback:** none (read-only).

### Lab 5.2 — Read the managed-device inventory (Topic: Device inventory)

**Objective:** See enrolled devices and their state.

```powershell
Get-MgDeviceManagementManagedDevice -Top 20 |
  Select-Object DeviceName, OperatingSystem, ComplianceState, ManagedDeviceOwnerType, EnrolledDateTime |
  Sort-Object EnrolledDateTime -Descending
```

**Expected result:** enrolled devices list OS, compliance state, ownership
(company/personal), and enrollment date — the inventory Intune reports.

**Negative test:** filter for a device name that is not enrolled; nothing
returns — inventory only contains enrolled/managed devices.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Inspect enrollment restrictions (Topic: Restrict enrollment)

**Objective:** See which platforms and limits are enforced.

```powershell
Get-MgDeviceManagementDeviceEnrollmentConfiguration |
  Where-Object { $_.AdditionalProperties["@odata.type"] -match "PlatformRestriction|Limit" } |
  Select-Object DisplayName, Priority
```

**Expected result:** platform-restriction and device-limit configurations
appear with priorities — restrictions block unwanted platforms and cap
devices per user.

**Negative test:** with no restriction blocking personal devices, a user
enrolls a personal phone into full MDM — set a platform restriction to block
personal ownership where required.

**Rollback:** none (read-only).

### Lab 5.4 — Retire a device (Topic: Device lifecycle)

**Objective:** Remove corporate data on offboarding.

```powershell
$d = Get-MgDeviceManagementManagedDevice -Filter "deviceName eq 'TEST-BYOD-01'"
Invoke-MgRetireDeviceManagementManagedDevice -ManagedDeviceId $d.Id
Get-MgDeviceManagementManagedDevice -ManagedDeviceId $d.Id | Select-Object DeviceName, ManagementState
```

**Expected result:** the device is retired — corporate data and management are
removed while personal data remains, the correct action for BYOD offboarding.

**Negative test:** wipe a personal BYOD device instead of retiring; the user's
personal data is factory-reset — use retire, not wipe, for personal devices.

**Rollback:** none (the device is removed from management).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Intune manages endpoints through MDM (whole device) and MAM (app data), and
is the compliance enforcement point behind Conditional Access. Enrollment
needs the MDM authority, automatic enrollment/scope, and Apple/Android
connectors; methods are chosen by platform and ownership. The lifecycle runs
from enrollment and inventory to retire or wipe.

- [ ] I can distinguish MDM and MAM and choose per scenario.
- [ ] I can configure enrollment prerequisites and restrictions.
- [ ] I can enroll each platform with the right method.
- [ ] I can manage the lifecycle and retire vs wipe correctly.
- [ ] I completed Labs 5.1–5.4 including each negative test.
