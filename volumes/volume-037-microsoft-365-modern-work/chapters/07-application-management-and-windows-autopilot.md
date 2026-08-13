# Chapter 07: Application Management and Windows Autopilot

## Learning Objectives

- Deploy applications through Intune across Windows, iOS/iPadOS, Android, and macOS.
- Choose the right Windows app format: Win32, MSI/line-of-business, Microsoft Store, and Enterprise App Catalog.
- Protect corporate data in apps with App Protection Policies (MAM) for BYOD.
- Provision Windows devices zero-touch with Windows Autopilot.
- Validate app installation and Autopilot enrollment and troubleshoot the common failures.

## Theory and Architecture

**Application management** in Intune delivers and protects software. Apps are
**assigned** to Entra groups with an **intent**: **Required** (installed
automatically), **Available** (offered in Company Portal for user-initiated
install), or **Uninstall**. Assignments are user- or device-targeted, and app
**supersedence** and **dependencies** model upgrades and prerequisites.

Windows apps come in several **formats**. **Win32** apps are packaged as
`.intunewin` with the Content Prep Tool and offer the richest control —
install/uninstall commands, **detection rules**, **requirement rules**, and
**return-code** handling — making them the workhorse for enterprise software.
**Line-of-business (MSI)** apps are simpler single-MSI deployments. **Microsoft
Store apps** (the new store) install modern packaged apps, and the **Enterprise
App Catalog** provides Microsoft-packaged, ready-to-deploy Win32 apps that
reduce packaging effort. iOS/Android use **store apps**, **VPP** (volume
purchase) apps from Apple Business Manager, and **managed Google Play** apps;
macOS supports `.pkg`/`.dmg`, store, and LOB.

**App Protection Policies (APP / MAM)** protect corporate data **inside apps**
without managing the device — essential for BYOD. They enforce PIN, encryption,
copy/paste and save-as restrictions, and selective **wipe of corporate data
only**, applied at the app layer (for example, Outlook and Teams on a personal
phone) and often paired with Conditional Access "require approved client app"
or "require app protection policy."

**Windows Autopilot** provisions new Windows devices **zero-touch**. A device's
**hardware hash** is registered (by the OEM/reseller or manually) to the
tenant; on first boot the device recognizes it is corporate, applies an
**Autopilot deployment profile** (user-driven or self-deploying/kiosk), joins
Entra, enrolls in Intune, and applies policies and apps through the
**Enrollment Status Page (ESP)** before the user reaches the desktop —
no imaging. **Autopilot device preparation** is the newer, faster provisioning
flow. The result is a corporate-configured device delivered straight to the
user.

## Design Considerations

Package enterprise software as **Win32** for control, writing robust
**detection rules** (file/registry/MSI product code) so Intune knows whether
an app is installed, and correct **requirement rules** (OS, architecture,
disk) so it targets the right devices. Use the **Enterprise App Catalog** to
avoid hand-packaging common apps. Assign with the right **intent** — Required
for baseline software, Available for optional — and model **supersedence** for
upgrades so old versions are replaced cleanly.

For **BYOD**, lead with **App Protection Policies** rather than full MDM, and
require them (or approved client apps) in Conditional Access so personal
devices can use Outlook/Teams with corporate data contained and selectively
wipeable. For corporate Windows, standardize on **Autopilot**: user-driven
Entra-join profiles for most users, self-deploying for kiosks/shared devices.
Tune the **Enrollment Status Page** to block use until critical apps and
policies land, but keep the blocking app set small so provisioning is not
painfully slow.

## Implementation and Automation

Win32 packaging and detection are typically defined in the portal; the Content
Prep Tool creates the package:

```text
IntuneWinAppUtil.exe -c C:\source -s setup.exe -o C:\output
# Upload the .intunewin in Intune, then set:
#   Install command:   setup.exe /qn
#   Uninstall command: msiexec /x {PRODUCT-GUID} /qn
#   Detection rule:    MSI product code {PRODUCT-GUID}  (or a file/registry check)
```

Query apps and assignments with Graph:

```powershell
Connect-MgGraph -Scopes "DeviceManagementApps.ReadWrite.All","DeviceManagementServiceConfig.ReadWrite.All"
Get-MgDeviceAppManagementMobileApp -Top 10 |
  Select-Object DisplayName, @{n='Type';e={$_.AdditionalProperties["@odata.type"]}}, PublishingState
```

Create an App Protection Policy for iOS (structure abbreviated):

```powershell
New-MgDeviceAppManagementiOSManagedAppProtection -BodyParameter @{
  displayName="APP - iOS BYOD"; pinRequired=$true; allowedInboundDataTransferSources="managedApps"
  allowedOutboundDataTransferDestinations="managedApps"; saveAsBlocked=$true }
```

Inspect Autopilot registrations and profiles:

```powershell
Get-MgDeviceManagementWindowsAutopilotDeviceIdentity -Top 10 |
  Select-Object SerialNumber, GroupTag, EnrollmentState, DeploymentProfileAssignmentStatus
```

## Validation and Troubleshooting

Confirm app install status and Autopilot readiness:

```powershell
# App install status per device (portal: App > Device install status)
Get-MgDeviceManagementWindowsAutopilotDeviceIdentity |
  Select-Object SerialNumber, DeploymentProfileAssignmentStatus, EnrollmentState
```

Common issues: a **Win32 app** reporting installed when it is not (or vice
versa) because the **detection rule** is wrong — detection, not the installer
exit code alone, decides "installed"; an app **not offered** because the
intent is Available but the user is not in Company Portal or not licensed; an
**App Protection Policy** not applying because the app is not a
managed/approved app or the user opened it with a personal account; an
**Autopilot** device not recognizing itself because the **hardware hash** was
not imported or the **deployment profile** is not assigned
(`DeploymentProfileAssignmentStatus` shows this); and the **Enrollment Status
Page** timing out because it is set to block on an app that fails to install.
Autopilot troubleshooting starts with the ESP details and the device's
`mdmdiagnosticstool` logs.

## Security and Best Practices

Deliver a **standard app baseline** as Required and keep optional software
Available. Write **strong detection rules** so state is accurate, and use
**supersedence** for clean upgrades. For **BYOD**, require **App Protection
Policies** (and approved client apps via Conditional Access) so corporate data
is contained and selectively wipeable without touching personal data — the
right balance of security and privacy. Provision corporate Windows with
**Autopilot** for a consistent, zero-touch, policy-enforced build, and use the
**ESP** to ensure security policies and apps are present before first use.
Keep packaging **least-privilege** (system context where possible, signed
installers) and monitor **app install** and **Autopilot** reporting.

## References and Knowledge Checks

- Microsoft Learn: *Add apps to Intune*; *Win32 app management*; *App protection policies*; *Windows Autopilot*.
- Microsoft Learn: MD-102 — *Deploy and manage applications; deploy Windows client with Autopilot*.

**Knowledge checks**

1. Why is the detection rule, not the installer exit code, what determines "installed"?
2. When is an App Protection Policy the right control instead of full MDM?
3. What does Autopilot do on first boot, and what role does the Enrollment Status Page play?

## Hands-On Lab

Topic-level walkthroughs for MD-102 application and provisioning skills.

**Shared prerequisites for Labs 7.1–7.4** — a Microsoft 365 tenant with Intune,
a Graph session with `DeviceManagementApps.ReadWrite.All`, a test Windows
device, and admin rights. **Cost:** none.

### Lab 7.1 — List apps and their intents (Topic: Application deployment)

**Objective:** See deployed apps and types.

```powershell
Get-MgDeviceAppManagementMobileApp -Top 20 |
  Select-Object DisplayName, @{n='Type';e={$_.AdditionalProperties["@odata.type"] -replace '#microsoft.graph.',''}}, PublishingState
```

**Expected result:** apps list with their type (win32LobApp, winGetApp,
iosStoreApp, etc.) and publishing state — the app catalog Intune manages.

**Negative test:** query for an app that was never added; nothing returns —
only added apps appear.

**Rollback:** none (read-only).

### Lab 7.2 — Reason about a Win32 detection rule (Topic: Win32 apps)

**Objective:** Confirm detection governs install state.

```text
# In the portal, define a Win32 app's detection rule as the MSI product code,
# then check App > Device install status. A device with the product code
# installed reports "Installed"; removing it flips to "Not installed".
```

**Expected result:** the install-status report follows the **detection rule**,
not the installer's return code — accurate detection is what makes reporting
trustworthy.

**Negative test:** set a detection rule pointing at a file that always exists
(e.g., a system DLL); every device reports installed even without the app —
detection must be specific to the app.

**Rollback:** correct or remove the test detection rule.

### Lab 7.3 — Create an iOS App Protection Policy (Topic: MAM for BYOD)

**Objective:** Contain corporate data in apps.

```powershell
New-MgDeviceAppManagementiOSManagedAppProtection -BodyParameter @{
  displayName="APP - iOS BYOD"; pinRequired=$true; saveAsBlocked=$true
  allowedInboundDataTransferSources="managedApps"; allowedOutboundDataTransferDestinations="managedApps" }
Get-MgDeviceAppManagementiOSManagedAppProtection | Select-Object DisplayName, PinRequired, SaveAsBlocked
```

**Expected result:** a policy requiring a PIN and blocking save-as/transfer to
unmanaged apps — corporate data is contained without managing the personal
device.

**Negative test:** expect the policy to protect a personal account's data; it
applies only to the corporate (managed) account context — MAM protects the
corporate identity's data.

**Rollback:** remove the app protection policy.

### Lab 7.4 — Check Autopilot device registration (Topic: Windows Autopilot)

**Objective:** Confirm a device will provision zero-touch.

```powershell
Get-MgDeviceManagementWindowsAutopilotDeviceIdentity -Top 10 |
  Select-Object SerialNumber, GroupTag, EnrollmentState, DeploymentProfileAssignmentStatus
```

**Expected result:** registered devices list a serial, group tag, and
`DeploymentProfileAssignmentStatus` of `assignedInSync` — a profile-assigned
device provisions itself on first boot.

**Negative test:** boot a device whose hardware hash was never imported; it
goes through normal OOBE, not Autopilot — registration is the prerequisite.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Intune deploys apps with intents and formats (Win32 with detection rules is
the workhorse), protects BYOD data with App Protection Policies, and
provisions corporate Windows zero-touch with Autopilot and the Enrollment
Status Page. Accurate detection and profile assignment are what make reporting
and provisioning reliable.

- [ ] I can deploy apps with the right format and intent.
- [ ] I can write detection rules that make install state accurate.
- [ ] I can protect BYOD data with App Protection Policies.
- [ ] I can provision Windows with Autopilot and the ESP.
- [ ] I completed Labs 7.1–7.4 including each negative test.
