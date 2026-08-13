# Chapter 02: Host Preparation

## Learning Objectives

- Verify a Windows 11 host can run hardware-accelerated virtual machines.
- Decide, deliberately, how to resolve the Hyper-V/VBS performance conflict.
- Install VMware Workstation Pro and confirm its services are healthy.

## Hands-On Lab

### Lab 2.1 — Verify Windows 11 host readiness

**Objective.** Confirm the host can run hardware-accelerated VMs before
you waste an hour discovering it cannot.

**Walkthrough**

**Step 1.** Open PowerShell as Administrator: press `Win`, type
`powershell`, press `Ctrl+Shift+Enter`.

**Step 2.** Confirm the edition and build.

```powershell
Get-ComputerInfo -Property WindowsProductName, WindowsVersion, OsHardwareAbstractionLayer

```

Expected — Windows 11 Education, a current build:

```text
WindowsProductName          : Windows 11 Education
WindowsVersion              : 2009
OsHardwareAbstractionLayer  : 10.0.26100.xxxx

```

**Step 3.** Confirm hardware virtualization is enabled in firmware.

```text
systeminfo | Select-String -Pattern "Hyper-V", "Virtualization", "VM Monitor"

```

On a machine where the firmware setting is correct you will see one of
two things. If Hyper-V is *not* installed you get the four requirement
lines, all `Yes`:

```text
Hyper-V Requirements:      VM Monitor Mode Extensions: Yes
                           Virtualization Enabled In Firmware: Yes
                           Second Level Address Translation: Yes
                           Data Execution Prevention Available: Yes

```

If Hyper-V *is* installed you get instead:

```text
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.

```

That single line is important. Note it and continue to Lab 2.2.

**Step 4.** Check free space on the drive that will hold the VMs.

```powershell
Get-Volume -DriveLetter C | Select-Object DriveLetter, FileSystemLabel,
    @{n='FreeGB';e={[math]::Round($_.SizeRemaining/1GB,1)}},
    @{n='TotalGB';e={[math]::Round($_.Size/1GB,1)}}

```

**Step 5.** Check physical memory and core count.

```powershell
Get-CimInstance Win32_ComputerSystem |
    Select-Object @{n='RAM_GB';e={[math]::Round($_.TotalPhysicalMemory/1GB,1)}},
                  NumberOfProcessors, NumberOfLogicalProcessors

```

**Expected result.** Windows 11 Education;
`Virtualization Enabled In Firmware: Yes` (or the hypervisor- detected
message); at least 250 GB free; at least 16 GB RAM and 4 physical cores.

**Negative test.** If `Virtualization Enabled In Firmware: No`, stop.
Reboot into UEFI firmware setup — usually `F2`, `F10`, or `Del` during
POST, or from Windows via **Settings → System → Recovery → Advanced
startup → Restart now → Troubleshoot → Advanced options → UEFI Firmware
Settings**. Enable **Intel VT-x** (sometimes “Intel Virtualization
Technology”) or **AMD-V** / **SVM Mode**. Save and reboot. VMware
Workstation will install without VT-x but every 64-bit guest will refuse
to power on, which is a confusing failure to debug later.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Resolve the Hyper-V / VBS conflict

**Objective.** Understand and deliberately decide the single biggest
performance trap on a Windows 11 Education host.

**Why this matters**

Windows 11 ships with **Virtualization-Based Security (VBS)** and, on
many builds and most managed images, **Memory Integrity**
(Hypervisor-Protected Code Integrity, HVCI) enabled. Both run the
Microsoft hypervisor underneath Windows. Windows 11 Education, being an
enterprise-lineage SKU, is especially likely to have these on, and if
the machine is domain-joined they may be enforced by Group Policy.

When the Microsoft hypervisor is present, VMware Workstation cannot take
direct control of VT-x. Instead it falls back to running on top of
Hyper-V through the **Windows Hypervisor Platform (WHP)** API — what
VMware calls **User Level Monitor (ULM)** mode. Your VMs will still run.
They will run **noticeably slower** — commonly 20–40% slower on
CPU-bound work, worse on I/O — and nested virtualization (“Virtualize
Intel VT-x/EPT” in VM settings) becomes unavailable or unreliable.

This lab does not require nested virtualization, so ULM mode is
*survivable*. You have a real choice to make, and you should make it
consciously.

|  | Leave VBS on (ULM mode) | Turn VBS off (native VT-x) |
|:---|:---|:---|
| Lab works? | Yes | Yes |
| Speed | Slower, sometimes markedly | Full speed |
| Host security posture | Unchanged | **Reduced** — you are disabling a real defense |
| Reversible? | n/a | Yes, fully |
| Recommended for | Work machines, managed devices, anything domain-joined | Dedicated lab machines you own |

**If this is a work-managed or domain-joined machine, leave VBS enabled
and accept ULM mode.** Do not disable a security control on a corporate
asset for a lab. The exercises all complete either way. If it is your
own dedicated lab box, disabling gives a distinctly better experience.

**Walkthrough**

**Step 1.** Determine your current state.

```powershell
Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard |
    Select-Object VirtualizationBasedSecurityStatus,
                  SecurityServicesConfigured, SecurityServicesRunning

```

Interpretation:

- `VirtualizationBasedSecurityStatus` — `0` = off, `1` = enabled but not
  running, `2` = **running**.
- In `SecurityServicesRunning`, a value of `2` in the array means
  **Memory Integrity (HVCI) is active**.

**Step 2.** Check whether the boot-time hypervisor launch is on.

```powershell
bcdedit /enum "{current}" | Select-String hypervisorlaunchtype

```

`hypervisorlaunchtype  Auto` means the Microsoft hypervisor starts at
boot.

**Step 3 — Decision point.**

**If you are leaving VBS enabled**, skip to Step 6. Nothing more to do;
note that Workstation will display a message about running in a
reduced-performance mode, which is expected and not an error.

**Step 4 — Disabling VBS (dedicated lab machines only).** Turn off
Memory Integrity through the UI first, because the setting is
user-visible and you want to be able to find it again: **Settings →
Privacy & security → Windows Security → Device security → Core isolation
details → Memory integrity → Off**.

If the toggle is grayed out with “This setting is managed by your
administrator”, your machine is policy-managed. Stop here and use ULM
mode. Do not fight Group Policy on a corporate device.

**Step 5.** Disable the remaining Hyper-V surfaces and the boot
hypervisor.

```powershell
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform      -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform  -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName Windows-Defender-ApplicationGuard -NoRestart
bcdedit /set hypervisorlaunchtype off

```

Note that `VirtualMachinePlatform` is what WSL2 and Windows Sandbox
depend on. If you use WSL2 daily, leave that one enabled and disable
only the others — WSL2 will keep working and Workstation will still be
pushed into ULM mode, which is the trade you have chosen.

Reboot:

```powershell
Restart-Computer

```

**Step 6.** After reboot, re-verify.

```powershell
Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard |
    Select-Object VirtualizationBasedSecurityStatus
bcdedit /enum "{current}" | Select-String hypervisorlaunchtype

```

**Expected result.** Either a documented, deliberate decision to remain
in ULM mode, or `VirtualizationBasedSecurityStatus : 0` and
`hypervisorlaunchtype  Off`, giving Workstation native VT-x.

**Negative test.** Attempt to run this lab with Memory Integrity on and
then compare. Boot `ct-gw` and time a fixed workload:

```bash
time openssl speed -elapsed rsa2048 2>/dev/null | tail -3

```

Run it in ULM mode and again in native mode. The difference is not
theoretical; you will see it. This is worth doing once so that when a
colleague reports “Workstation is slow on my Windows 11 box” you know
the first question to ask.

**Rollback / reversal.** To restore VBS at any time:

```powershell
bcdedit /set hypervisorlaunchtype auto
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform     -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
Restart-Computer

```

Then re-enable Memory Integrity in Windows Security. Do this when you
finish the lab if you disabled it on a machine you also use for anything
else.

### Lab 2.3 — Install VMware Workstation Pro 17.6.3

**Objective.** Get a working, license-free Workstation Pro installation.

**Walkthrough**

**Step 1.** Create a free account at the Broadcom Support Portal
(`support.broadcom.com`) if you do not have one. Broadcom moved all
VMware downloads behind this portal; there is no anonymous download
link, which surprises people expecting the old vmware.com experience.

**Step 2.** In the portal, choose **VMware Cloud Foundation** as the
division, then navigate to **My Downloads → VMware Workstation Pro →
17.x** and select **17.6.3** for Windows. The file is named similarly
to:

```text
VMware-workstation-full-17.6.3-<build>.exe

```

**Step 3.** Verify the download before running it. Compare against the
checksum shown on the portal download page:

```powershell
Get-FileHash -Algorithm SHA256 .\VMware-workstation-full-17.6.3-*.exe

```

This is a habit worth keeping. You are about to install a kernel-mode
driver.

**Step 4.** Run the installer elevated:

```powershell
Start-Process -FilePath .\VMware-workstation-full-17.6.3-<build>.exe -Verb RunAs

```

**Step 5.** Work through the wizard:

- Accept the license agreement.
- **Enhanced Keyboard Driver** — check it. It improves key handling for
  guests, which matters when you are typing into a Linux console in a VM
  window.
- Install path — the default
  `C:\Program Files\VMware\VMware Workstation\` is fine.
- **Check for product updates on startup** — your choice.
- **Join the VMware Customer Experience Improvement Program** — uncheck
  if you prefer.
- Shortcuts — your choice.

**Step 6.** Reboot when prompted. The installer adds network drivers,
and skipping the reboot causes odd behavior in the Virtual Network
Editor.

**Step 7.** Launch Workstation. On the license screen, select **Use
Workstation Pro for free for commercial, educational, and personal use**
and click **Continue**. There is no key to enter.

**Step 8.** Confirm from the command line that the services are healthy:

```powershell
Get-Service -Name "VMware*" | Format-Table -AutoSize Name, Status, StartType

```

Expected — the core services running:

```text
Name                          Status  StartType
----                          ------  ---------
VMAuthdService                Running Automatic
VMnetDHCP                     Running Automatic
VMware NAT Service            Running Automatic
VMwareHostd                   Running Automatic
VMUSBArbService               Running Automatic

```

**Step 9.** Set a sensible default VM location so you do not scatter 130
GB across your profile. **Edit → Preferences → Workspace → Default
location for virtual machines.** Set it to something like
`D:\VMs\ColorTokens-Lab\` on your fastest drive with the most space.

**Expected result.** Workstation Pro 17.6.3 launches, reports itself
licensed for free use, and all five VMware services are running.

**Negative test.** Try to power on any 64-bit VM with VT-x disabled in
firmware. Workstation raises *“This host supports Intel VT-x, but Intel
VT-x is disabled”* or *“Virtualized Intel VT-x/EPT is not supported on
this platform.”* Recognizing this message saves you a support ticket; it
always means firmware, not Workstation.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Lab 2.1 complete, including its negative test.
- [ ] Lab 2.2 complete, including its negative test.
- [ ] Lab 2.3 complete, including its negative test.
