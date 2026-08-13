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

**Step 2.** In an elevated PowerShell on the Windows 11 host, confirm virtualization is enabled and check whether a Microsoft hypervisor is already running:

```powershell
Get-ComputerInfo -Property "HyperV*","*Virtualization*" |
    Format-List
systeminfo | Select-String "Hyper-V", "Virtualization"
```

**Expected result.** `HyperVRequirementVirtualizationFirmwareEnabled : True`. If `systeminfo` reports *"A hypervisor has been detected. Features required for Hyper-V will not be displayed,"* the Microsoft hypervisor is running and will contend with Workstation for VT-x — resolve it in Lab 2.3.

**Negative test.** Leave VT-x disabled in firmware and try to power on a 64-bit guest later; Workstation refuses with *"This host supports Intel VT-x, but Intel VT-x is disabled."* The fix is always firmware, not Workstation.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Install VMware Workstation Pro

**Objective.** Install Workstation Pro 17.6.3 and verify the Virtual Network Editor is present (you need it in Chapter 03).

**Walkthrough**

**Step 1.** Sign in to the Broadcom Support Portal, download **VMware Workstation Pro 17.6.3 for Windows**, and run the installer as Administrator. Accept the defaults. No license key is required.

**Step 2.** Launch Workstation once so it registers its virtual network services. Then confirm the services are running:

```powershell
Get-Service -Name "VMware*" |
    Where-Object { $_.Status -eq "Running" } |
    Format-Table Name, DisplayName, Status
```

**Expected result.** `VMwareHostd`, `VMnetDHCP`, and `VMware NAT Service` appear as Running. **Edit → Virtual Network Editor** opens without error.

**Negative test.** If the Virtual Network Editor menu item is missing or greyed out, the install did not complete elevated; repair the installation from **Apps → VMware Workstation → Modify** and reboot.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Resolve the Hyper-V / VBS conflict

**Objective.** Ensure Workstation runs with full hardware acceleration rather than falling back to the slow **User Level Monitor (ULM)** it uses when the Microsoft hypervisor holds VT-x.

**Background.** Windows 11 enables **Virtualization-Based Security (VBS)** and **Memory Integrity (HVCI)** by default on many machines. These run the Microsoft hypervisor beneath Windows, which then owns VT-x. Workstation 17 can still run under the Windows Hypervisor Platform, but in a reduced-performance ULM mode. For a five-VM lab you want the native monitor.

**Walkthrough**

**Step 1.** Check whether VBS is running:

```powershell
Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard |
    Select-Object VirtualizationBasedSecurityStatus, SecurityServicesRunning
```

`VirtualizationBasedSecurityStatus : 2` means VBS is running.

**Step 2 (optional, for maximum performance).** If you are willing to disable VBS on a lab machine, turn off Memory Integrity in **Settings → Privacy & security → Windows Security → Device security → Core isolation**, then disable the remaining pieces from an elevated prompt and reboot:

```powershell
bcdedit /set hypervisorlaunchtype off
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -NoRestart
```

**Expected result.** After reboot, `systeminfo` again shows the four firmware virtualization lines (no "hypervisor detected" banner), and Workstation powers on guests with the native monitor.

**Negative test.** Skip this lab on a machine with VBS on and build the estate anyway. It works, but nested guests run visibly slower and the Windows Server install in Chapter 04 can take twice as long. That is the ULM tax; you now know its cause.

**Rollback.** If this is a shared or corporate machine and you disabled VBS, re-enable Memory Integrity when you finish the lab (`bcdedit /set hypervisorlaunchtype auto` and turn Core isolation back on).

### Lab 2.4 — Create the lab directory structure

**Objective.** Give every VM and snapshot a predictable home.

**Walkthrough**

```powershell
$root = "D:\labs\illumio"
"il-gw","il-app01","il-db01","il-win01","il-ot01" | ForEach-Object {
    New-Item -ItemType Directory -Force -Path (Join-Path $root $_) | Out-Null
}
New-Item -ItemType Directory -Force -Path (Join-Path $root "iso") | Out-Null
Get-ChildItem $root
```

**Expected result.** Five VM folders plus an `iso` folder. Place the Ubuntu and Windows Server ISOs in `D:\labs\illumio\iso`.

**Negative test.** Put the VMs on a nearly full system drive; Workstation refuses to power on when free space drops below the guest's provisioned size. Keep 250 GB free.

**Rollback.** None — this is your working tree for the rest of the lab.

## Summary and Completion Checklist

- [ ] VT-x/AMD-V (and VT-d) enabled in firmware.
- [ ] Workstation Pro installed; virtual network services running.
- [ ] Hyper-V/VBS contention understood and, if desired, resolved.
- [ ] Lab directory tree and ISO folder created.
