# Chapter 01: Windows Server 2025 — Editions, Installation, Server Core, and Windows Admin Center

## Learning Objectives

- Distinguish the Windows Server 2025 editions and licensing models and choose the right one for a workload.
- Compare the installation options — Server Core, Desktop Experience, and Azure Edition — and justify Server Core as the default.
- Perform an unattended installation and complete first-boot configuration entirely from PowerShell.
- Explain the servicing model (Long-Term Servicing Channel and hotpatching) and keep a server current.
- Manage one server or many with Windows Admin Center and Server Manager without a local desktop.

## Theory and Architecture

Windows Server 2025 is the Long-Term Servicing Channel (LTSC) release that
succeeds Windows Server 2022. It ships as a conventional on-premises
operating system and as **Azure Edition**, a variant tuned for Azure and
Azure Stack HCI that adds features such as hotpatching and SMB over QUIC.
The kernel, driver model, and management surface are shared with the
client Windows line, but the server SKUs enable the **roles and features**
— AD DS, Hyper-V, Failover Clustering, DNS, and dozens more — that turn a
generic OS into infrastructure.

Two axes define any Windows Server deployment. The first is **edition**,
which sets licensing rights and a few feature ceilings: **Standard** and
**Datacenter** are the mainstream editions, licensed per physical core
with a 16-core minimum per server and Client Access Licenses (CALs) for
users or devices. The practical difference is virtualization rights and a
handful of Datacenter-only features. Standard grants two Operating System
Environments (OSEs, effectively two virtual machines) per fully licensed
host; Datacenter grants **unlimited** OSEs and adds Storage Spaces Direct,
Storage Replica without limits, software-defined networking, and shielded
VMs. A virtualization host that runs more than two Windows VMs is almost
always cheaper on Datacenter.

The second axis is **installation option**. **Server Core** installs the
OS with no Explorer shell, no Edge, and no desktop — management is
PowerShell, remote tools, and Windows Admin Center. **Desktop Experience**
adds the full GUI. **Azure Edition** is delivered through Azure or Azure
Stack HCI images. Microsoft's guidance, and this volume's default, is
Server Core: a smaller disk and memory footprint, a much smaller attack
surface, and fewer patches (and therefore fewer reboots) because the
graphical components that generate a large share of updates are absent.

Architecturally, everything an administrator does resolves to one of three
management planes: **local** (rare, and impossible headless), **remote MMC
and PowerShell** (Server Manager, RSAT, `Enter-PSSession`), and
**browser-based** (Windows Admin Center, and for Azure-connected servers,
the Azure portal). A modern estate leans on the second and third and
treats the console as a break-glass path.

## Design Considerations

Choosing an edition is a cost-and-capability decision. Count physical
cores, apply the 16-core minimum, and compare the Standard two-VM ceiling
against the number of Windows guests the host will run; cross three guests
and Datacenter usually wins on both price and features. Reserve Datacenter
deliberately for hosts that need Storage Spaces Direct, unlimited Storage
Replica, or SDN.

Choosing an installation option is a manageability decision. Server Core
is correct for domain controllers, Hyper-V hosts, file servers, and
clustered roles — anything managed at scale. Desktop Experience is
justified when an application vendor requires a GUI on the box, when a role
has no remote tooling, or for a jump host. Note that you cannot convert
between Server Core and Desktop Experience in place on modern releases; the
choice is made at install time, so decide before you deploy.

Plan servicing before first boot. LTSC releases get five years of
mainstream and five of extended support. Azure Edition supports
**hotpatching**, which applies most monthly security updates to running
processes in memory without a reboot, cutting reboots to a quarterly
baseline — a major availability win for hosts where a reboot is
expensive. On-premises hotpatch enrollment is delivered through Azure Arc,
which is one more reason to Arc-enable even on-premises servers
(Chapter 11).

## Implementation and Automation

An unattended installation is driven by an `autounattend.xml` answer file
on the installation media or a virtual floppy/USB. It sets the edition
index, disk partitioning, locale, administrator password, and the computer
name, so a server boots to a known state with no clicks. In a lab you can
also deploy from the Evaluation ISO and configure the rest from PowerShell.

First-boot configuration is entirely scriptable. The classic interactive
tool on Server Core is `sconfig`, but every setting it exposes has a
cmdlet:

```powershell
# Rename, set a static IP, set DNS, then join a domain — the first-boot core
Rename-Computer -NewName "FS01" -Restart:$false
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 10.10.0.20 `
  -PrefixLength 24 -DefaultGateway 10.10.0.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 10.10.0.10
Add-Computer -DomainName "corp.contoso.lab" -Restart
```

Roles and features are added with the `ServerManager` module. The same
command works locally on Server Core and remotely against any server:

```powershell
Install-WindowsFeature -Name Web-Server -IncludeManagementTools
Get-WindowsFeature -Name Web-Server
```

`Install-WindowsFeature` replaced the older `ocsetup`/`dism` role paths for
Windows features and is idempotent — re-running it when the feature is
present is a no-op, which makes it safe in configuration scripts and DSC
(Chapter 02).

## Validation and Troubleshooting

Confirm the edition and build so you know exactly what you are running:

```powershell
Get-ComputerInfo -Property WindowsProductName, OsHardwareAbstractionLayer, WindowsVersion
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').DisplayVersion
```

Expected output names the edition (for example `Windows Server 2025
Datacenter`) and a display version such as `24H2`. If `Install-WindowsFeature`
fails with a source error on Server Core, the feature's payload may have
been removed (Features on Demand); supply `-Source` pointing at a mounted
install image's `sources\sxs` folder. If a server is unreachable remotely
after install, the usual causes are the firewall (WinRM and the relevant
role ports), a missing DNS record, or the server not being domain-joined
so Kerberos and remote MMC fail — verify with `Test-NetConnection
-ComputerName FS01 -Port 5985` for WinRM.

## Security and Best Practices

Default to Server Core to shrink the attack surface. Keep the local
Administrator account renamed and its password in a vault (Windows LAPS,
Chapter 10). Enable the firewall and open only the ports a role needs.
Apply updates on a schedule and adopt hotpatching where the platform
supports it to reduce reboot-driven downtime. Never browse the internet or
read email from a server, and never install a full desktop "just in case"
— an unused GUI is pure attack surface and patch load. Manage from a
dedicated privileged access workstation using RSAT and Windows Admin
Center rather than logging on to the console.

## References and Knowledge Checks

- Microsoft Learn: *What's new in Windows Server 2025*; *Install Windows Server*; *Windows Admin Center*.
- Microsoft Learn: AZ-800 study guide — *Deploy and manage Windows Servers in a hybrid environment*.

**Knowledge checks**

1. A host will run five Windows VMs. Which edition is more cost-effective, and why?
2. Why can you not convert Server Core to Desktop Experience in place?
3. What does hotpatching change about the monthly reboot cadence, and how is it enrolled on-premises?

## Hands-On Lab

This chapter's lab is a topic-level walkthrough for each **installation and
first-configuration** task in AZ-800's "deploy and manage" skill area.
Every step is a runnable PowerShell command.

**Shared prerequisites for Labs 1.1–1.4** — a Windows Server 2025 instance
(Evaluation edition is fine), local Administrator rights, and a lab network
`10.10.0.0/24`. **Cost:** none (Evaluation edition is free for 180 days and
can be rearmed).

### Lab 1.1 — Identify the edition, version, and installed features (Topic: Inventory the server)

**Objective:** Establish exactly what the server is before changing it.

```powershell
Get-ComputerInfo -Property WindowsProductName, WindowsVersion, CsName
Get-WindowsFeature | Where-Object Installed | Select-Object Name, InstallState
```

**Expected result:** the product name (for example `Windows Server 2025
Standard Evaluation`), a version such as `24H2`, and a list of installed
features — a Server Core box shows only a short baseline list, confirming
the minimal footprint.

**Negative test:** run `Get-WindowsFeature -Name FS-Fake`; it returns
nothing and warns the feature name is not valid — feature names are exact,
and a typo silently installs nothing rather than erroring loudly.

**Cleanup:** none (read-only).

### Lab 1.2 — First-boot configuration from PowerShell (Topic: Configure a new server)

**Objective:** Rename the server and set static networking without `sconfig`.

```powershell
Rename-Computer -NewName "FS01"
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 10.10.0.20 `
  -PrefixLength 24 -DefaultGateway 10.10.0.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 10.10.0.10
Get-NetIPAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4 | Format-Table IPAddress, PrefixLength
```

**Expected result:** the address `10.10.0.20/24` is bound to the interface;
the rename takes effect after the next reboot. Every setting `sconfig`
offers has a cmdlet, so first-boot configuration is fully scriptable.

**Negative test:** set a second `New-NetIPAddress` with the same IP on
another interface; the command fails with a duplicate-address error —
Windows refuses overlapping static bindings.

**Cleanup:** `Remove-NetIPAddress -IPAddress 10.10.0.20 -Confirm:$false` if reverting.

### Lab 1.3 — Install and remove a role idempotently (Topic: Manage roles and features)

**Objective:** Add a role, confirm it, and prove re-adding is a no-op.

```powershell
Install-WindowsFeature -Name Web-Server -IncludeManagementTools
Install-WindowsFeature -Name Web-Server   # run again
Get-WindowsFeature -Name Web-Server | Select-Object Name, InstallState
```

**Expected result:** the first call installs IIS and reports
`Success = True, ExitCode = Success`; the second reports
`Success = True, ExitCode = NoChangeNeeded` — `Install-WindowsFeature` is
idempotent, which is what makes it safe in automation.

**Negative test:** run `Install-WindowsFeature -Name Web-Server` on Server
Core after removing the payload; it fails with a source error — supply
`-Source wim:<path>` from a mounted image to fix.

**Cleanup:** `Uninstall-WindowsFeature -Name Web-Server -IncludeManagementTools -Restart:$false`.

### Lab 1.4 — Add a server to Windows Admin Center's connection list (Topic: Manage servers remotely)

**Objective:** Register a target server for browser-based management.

```powershell
# On the management gateway (Windows Admin Center installed):
Import-Module "$env:ProgramFiles\Windows Admin Center\PowerShell\Modules\ConnectionTools"
Add-Connection -Name "FS01.corp.contoso.lab" -Type msft.sme.connection-type.server
Get-Connection | Format-Table Name, Type
```

**Expected result:** `FS01` appears in the Windows Admin Center connection
list and can be opened in the browser; WAC uses WinRM under the hood, so
the target needs WinRM reachable (TCP 5985/5986).

**Negative test:** add a server whose name does not resolve; WAC lists it
but the connection fails on open with a WinRM/DNS error — name resolution
and WinRM reachability, not the WAC entry, determine success.

**Cleanup:** `Remove-Connection -Name "FS01.corp.contoso.lab"`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Windows Server 2025 is chosen along two axes — edition (Standard versus
Datacenter, a cost-and-virtualization-rights decision) and installation
option (Server Core by default, Desktop Experience by exception, Azure
Edition for hotpatching and Azure integration). Every first-boot and
role-management task is scriptable in PowerShell, and a modern estate is
managed remotely through RSAT and Windows Admin Center rather than at the
console.

- [ ] I can choose an edition from core count and virtualization needs.
- [ ] I can justify Server Core and know why it cannot convert in place.
- [ ] I can configure a new server and manage roles entirely from PowerShell.
- [ ] I can explain hotpatching and how on-premises servers enroll.
- [ ] I completed Labs 1.1–1.4 including each negative test.
