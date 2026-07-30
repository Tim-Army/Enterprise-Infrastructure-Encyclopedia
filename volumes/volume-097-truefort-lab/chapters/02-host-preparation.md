# Chapter 02: Host Preparation

## Learning Objectives

- Enable hardware virtualization and confirm the host can run nested guests.
- Install VMware Workstation Pro 17.6.3 (or 26H1) cleanly.
- Recognize and resolve the Hyper-V / Virtualization-Based Security (VBS) contention that silently halves VM performance.
- Lay down a predictable directory structure for the five VMs and their snapshots.

## Hands-On Lab

### Lab 2.1 — Enable virtualization and verify host readiness

**Objective.** Confirm the host exposes hardware virtualization to VMware Workstation, and that no competing hypervisor is holding it.

**Walkthrough**

**Step 1.** Reboot into firmware (UEFI) setup and enable **Intel VT-x** (or **AMD-V**) and, if present, **VT-d / IOMMU**. Save and exit.

**Step 2.** In an elevated PowerShell, confirm virtualization is enabled and check for a running Microsoft hypervisor:

```powershell
Get-ComputerInfo -Property "HyperV*","*Virtualization*" | Format-List
systeminfo | Select-String "Hyper-V", "Virtualization"
```

**Expected result.** `HyperVRequirementVirtualizationFirmwareEnabled : True`. A "hypervisor has been detected" banner means the Microsoft hypervisor is running and will contend with Workstation — resolve it in Lab 2.3.

**Negative test.** Leave VT-x disabled and a 64-bit guest refuses to boot with "Intel VT-x is disabled." The fix is firmware, not Workstation.

**Cleanup.** None.

### Lab 2.2 — Install VMware Workstation Pro

**Objective.** Install Workstation Pro 17.6.3 and verify the Virtual Network Editor is present.

**Walkthrough**

**Step 1.** Download **VMware Workstation Pro 17.6.3** from the Broadcom Support Portal and install as Administrator. No license key is required.

**Step 2.** Launch it once, then confirm the network services:

```powershell
Get-Service -Name "VMware*" | Where-Object { $_.Status -eq "Running" } |
    Format-Table Name, DisplayName, Status
```

**Expected result.** `VMwareHostd`, `VMnetDHCP`, and `VMware NAT Service` are Running; **Edit → Virtual Network Editor** opens.

**Negative test.** A greyed-out Virtual Network Editor means the install was not elevated; repair via **Apps → VMware Workstation → Modify** and reboot.

**Cleanup.** None.

### Lab 2.3 — Resolve the Hyper-V / VBS conflict

**Objective.** Ensure Workstation runs with full hardware acceleration rather than the slow User Level Monitor fallback.

**Walkthrough**

**Step 1.** Check whether VBS is running:

```powershell
Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard |
    Select-Object VirtualizationBasedSecurityStatus, SecurityServicesRunning
```

`VirtualizationBasedSecurityStatus : 2` means VBS is on.

**Step 2 (optional, for maximum performance).** On a lab machine, disable Memory Integrity in **Settings → Privacy & security → Windows Security → Device security → Core isolation**, then:

```powershell
bcdedit /set hypervisorlaunchtype off
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -NoRestart
```

Reboot.

**Expected result.** After reboot, no "hypervisor detected" banner; Workstation uses the native monitor.

**Negative test.** Build the estate with VBS on and nested guests run visibly slower — the ULM tax.

**Cleanup.** Re-enable Memory Integrity when finished if this is a shared machine.

### Lab 2.4 — Create the lab directory structure

**Objective.** Give every VM and snapshot a predictable home.

**Walkthrough**

```powershell
$root = "D:\labs\truefort"
"tf-gw","tf-app01","tf-db01","tf-win01","tf-ot01" | ForEach-Object {
    New-Item -ItemType Directory -Force -Path (Join-Path $root $_) | Out-Null
}
New-Item -ItemType Directory -Force -Path (Join-Path $root "iso") | Out-Null
Get-ChildItem $root
```

**Expected result.** Five VM folders plus an `iso` folder holding the Ubuntu and Windows Server ISOs.

**Negative test.** Building on a nearly full system drive makes Workstation refuse to power on; keep 250 GB free.

**Cleanup.** None — this is your working tree.

## Summary and Completion Checklist

- [ ] VT-x/AMD-V (and VT-d) enabled in firmware.
- [ ] Workstation Pro installed; virtual network services running.
- [ ] Hyper-V/VBS contention understood and, if desired, resolved.
- [ ] Lab directory tree and ISO folder created.
