# Chapter 08: Hyper-V Virtualization and Windows Containers

## Learning Objectives

- Install Hyper-V and describe its architecture: partitions, the hypervisor, and integration services.
- Create and configure virtual machines, choosing generation, memory, and storage models.
- Build virtual switches and connect VMs to networks with VLANs and isolation.
- Use checkpoints and live migration, and protect VMs with resiliency features.
- Run Windows and Hyper-V-isolated containers and explain when each fits.

## Theory and Architecture

Hyper-V is a **Type 1 (bare-metal) hypervisor**: when the role is enabled,
the hypervisor loads beneath the operating system, which becomes the
**parent (root) partition** that owns hardware and management, while VMs run
in **child partitions** with virtualized access through the **VMBus** and
**integration services**. This is why enabling Hyper-V changes the host — the
"host OS" is now itself a privileged VM on the hypervisor.

**Virtual machines** come in two generations. **Generation 1** emulates
legacy BIOS hardware for maximum compatibility. **Generation 2** uses UEFI,
Secure Boot, and synthetic devices, boots faster, and is required for
**Shielded VMs** and modern guest features — the default for supported
guests. Memory can be **static** or **Dynamic Memory** (a min/startup/max
band the host balances across VMs). Storage uses **VHDX** virtual disks
(resilient, up to 64 TB, supporting online resize) in **fixed**, **dynamic**,
or **differencing** form.

**Virtual switches** connect VMs to networks in three types: **external**
(bound to a physical NIC, VMs reach the LAN), **internal** (host and VMs
only), and **private** (VMs only). VLAN tags, bandwidth limits, and port
ACLs refine connectivity. **Checkpoints** capture VM state (standard, or
**production** checkpoints that use VSS for application-consistent
snapshots). **Live migration** moves a running VM between hosts with no
downtime; **Storage Migration** moves its disks; **Hyper-V Replica**
asynchronously copies a VM to a second site for disaster recovery
(Chapter 09).

**Containers** virtualize the OS, not the machine. **Windows Server
containers** share the host kernel for density and speed; **Hyper-V-isolated
containers** run each container in a lightweight VM for kernel-level
isolation on shared or multi-tenant hosts. Both use the same images and
tooling and are covered more broadly in Volume VIII; here the focus is their
place on a Windows Server host.

## Design Considerations

Prefer **Generation 2** VMs for supported guests (UEFI, Secure Boot, faster
boot, shielding). Use **Dynamic Memory** for variable workloads to raise
density, but pin **static memory** for latency-sensitive or NUMA-bound VMs
(and note some guests, like certain database configurations, prefer static).
Use **dynamic VHDX** for general workloads and **fixed** where peak
performance and predictable capacity matter; keep VM disks on **ReFS**
(Chapter 07) for block cloning and integrity.

Design switches to match the physical network: one **external** switch per
uplink team, VLAN-tag VM traffic, and consider **SR-IOV** or **VMQ** for
throughput. Plan **live migration** networks (dedicated, secured with
Kerberos-constrained delegation or CredSSP) and enable **VM resiliency** so a
transient host issue pauses rather than crashes guests. For isolation
requirements — multi-tenant or untrusted workloads — choose **Hyper-V
isolation** for containers and **Shielded VMs** (Datacenter) for guests whose
disks must be protected from a compromised fabric admin.

## Implementation and Automation

Enable Hyper-V and create a switch and a Generation 2 VM:

```powershell
Install-WindowsFeature Hyper-V -IncludeManagementTools -Restart
New-VMSwitch -Name "vSwitch-Ext" -NetAdapterName "Ethernet" -AllowManagementOS $true
New-VM -Name "APP01" -Generation 2 -MemoryStartupBytes 4GB -Path "E:\VMs" `
  -NewVHDPath "E:\VMs\APP01\APP01.vhdx" -NewVHDSizeBytes 80GB -SwitchName "vSwitch-Ext"
Set-VM -Name "APP01" -DynamicMemory -MemoryMinimumBytes 2GB -MemoryMaximumBytes 8GB
Set-VMProcessor -VMName "APP01" -Count 2
```

Tag a VLAN, take a production checkpoint, and live-migrate:

```powershell
Set-VMNetworkAdapterVlan -VMName "APP01" -Access -VlanId 20
Set-VM -Name "APP01" -CheckpointType Production
Checkpoint-VM -Name "APP01" -SnapshotName "pre-change"
Move-VM -Name "APP01" -DestinationHost "HV02" -IncludeStorage -DestinationStoragePath "E:\VMs\APP01"
```

Run a Windows container (containers feature + a runtime, see Volume VIII):

```powershell
Install-WindowsFeature Containers -Restart
# with a container runtime installed:
ctr image pull mcr.microsoft.com/windows/servercore:ltsc2025
```

## Validation and Troubleshooting

Check VM state, integration services, and replication/migration readiness:

```powershell
Get-VM | Select-Object Name, State, Status, MemoryAssigned, Uptime
Get-VMIntegrationService -VMName "APP01" | Select-Object Name, Enabled, PrimaryStatusDescription
Get-VMSwitch | Select-Object Name, SwitchType, NetAdapterInterfaceDescription
```

`State : Running` with a healthy `Status` is the baseline. Common issues:
enabling Hyper-V on a host without virtualization extensions (enable
Intel VT-x/AMD-V and, for nested VMs, expose virtualization to the guest);
a VM with **no network** because it is on an internal/private switch or the
wrong VLAN; **live migration** failing on authentication (constrained
delegation or CredSSP not configured) or on processor incompatibility
(enable **processor compatibility mode** across dissimilar hosts); and a
**checkpoint chain** consuming disk because old checkpoints were never
merged — delete them so the AVHDX files merge back.

## Security and Best Practices

Treat the **Hyper-V host as Tier 0-adjacent** — a host compromise exposes
every guest. Run hosts on **Server Core**, keep them patched, and restrict
who is a **Hyper-V Administrator**. Use **Generation 2 + Secure Boot** and,
on Datacenter with a Host Guardian Service, **Shielded VMs** to protect
guest disks and state from fabric admins. Secure **live migration** traffic
and use dedicated networks. For containers, prefer **Hyper-V isolation** for
untrusted or multi-tenant workloads, keep base images current, and scan them
(Volume VIII). Encrypt VM storage at rest (BitLocker on the host volumes,
Chapter 10) and back VMs up with application-consistent (production)
checkpoints or a VSS-aware backup product.

## References and Knowledge Checks

- Microsoft Learn: *Hyper-V on Windows Server*; *Virtual switches*; *Live migration*; *Windows containers*.
- Microsoft Learn: AZ-800 — *Manage virtual machines and containers*.

**Knowledge checks**

1. What happens to the "host OS" when the Hyper-V role is enabled, and why?
2. When would you choose static memory over Dynamic Memory?
3. What isolation guarantee does a Hyper-V-isolated container add over a Windows Server container?

## Hands-On Lab

Topic-level walkthroughs for AZ-800's virtualization and container skills.

**Shared prerequisites for Labs 8.1–8.4** — a Windows Server 2025 host with
virtualization extensions enabled (or nested virtualization), a spare data
volume `E:`, and Administrator rights. **Cost:** none.

### Lab 8.1 — Enable Hyper-V and create a virtual switch (Topic: Configure Hyper-V)

**Objective:** Stand up the hypervisor and an external switch.

```powershell
Install-WindowsFeature Hyper-V -IncludeManagementTools -Restart
# after reboot:
New-VMSwitch -Name "vSwitch-Ext" -NetAdapterName "Ethernet" -AllowManagementOS $true
Get-VMSwitch | Select-Object Name, SwitchType
```

**Expected result:** an `External` switch bound to the physical NIC — VMs on
it reach the LAN while the host retains management connectivity.

**Negative test:** enable Hyper-V on hardware without VT-x/AMD-V; the role
installs but VMs will not start (`hypervisor not running`) — virtualization
extensions are required.

**Cleanup:** `Remove-VMSwitch "vSwitch-Ext" -Force`.

### Lab 8.2 — Create a Generation 2 VM with Dynamic Memory (Topic: Deploy VMs)

**Objective:** Build a modern VM and set its resources.

```powershell
New-VM -Name "APP01" -Generation 2 -MemoryStartupBytes 4GB -Path "E:\VMs" `
  -NewVHDPath "E:\VMs\APP01\APP01.vhdx" -NewVHDSizeBytes 60GB -SwitchName "vSwitch-Ext"
Set-VM -Name "APP01" -DynamicMemory -MemoryMinimumBytes 2GB -MemoryMaximumBytes 8GB
Set-VMProcessor "APP01" -Count 2
Get-VM APP01 | Select-Object Name, Generation, MemoryStartup, DynamicMemoryEnabled
```

**Expected result:** a Generation 2 VM with Dynamic Memory between 2–8 GB —
Gen 2 gives UEFI/Secure Boot and is required for shielding.

**Negative test:** attach a legacy network adapter to a Gen 2 VM; it is not
available — Gen 2 uses only synthetic devices.

**Cleanup:** `Remove-VM APP01 -Force; Remove-Item E:\VMs\APP01 -Recurse -Force`.

### Lab 8.3 — Take and merge a production checkpoint (Topic: Protect VM state)

**Objective:** Snapshot a VM application-consistently and clean up.

```powershell
Set-VM -Name "APP01" -CheckpointType Production
Checkpoint-VM -Name "APP01" -SnapshotName "pre-change"
Get-VMSnapshot -VMName "APP01" | Select-Object Name, SnapshotType, CreationTime
Remove-VMSnapshot -VMName "APP01" -Name "pre-change"   # triggers AVHDX merge
```

**Expected result:** a `Production` checkpoint is created (VSS-based,
application-consistent) and removing it merges the differencing disk back —
production checkpoints are safe for server workloads.

**Negative test:** leave several standard checkpoints in place and watch
`E:\VMs` grow; the AVHDX chain consumes disk until merged — never hoard
checkpoints on production VMs.

**Cleanup:** ensure no snapshots remain (`Get-VMSnapshot`).

### Lab 8.4 — Tag a VLAN on a VM adapter (Topic: VM networking)

**Objective:** Place a VM on a specific VLAN.

```powershell
Set-VMNetworkAdapterVlan -VMName "APP01" -Access -VlanId 20
Get-VMNetworkAdapterVlan -VMName "APP01" | Select-Object VMName, OperationMode, AccessVlanId
```

**Expected result:** the adapter is in `Access` mode on VLAN 20 — VM traffic
is tagged so the physical switch places it on the correct segment.

**Negative test:** set an access VLAN the physical switch trunk does not
carry; the VM loses connectivity — the uplink trunk must carry the VLAN.

**Cleanup:** `Set-VMNetworkAdapterVlan -VMName "APP01" -Untagged`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Hyper-V is a Type 1 hypervisor that turns the host OS into a privileged
parent partition. VMs (prefer Generation 2), Dynamic Memory, VHDX storage,
and typed virtual switches deliver compute and networking; checkpoints and
live migration protect and move workloads. Windows and Hyper-V-isolated
containers add OS-level virtualization with a choice of density or isolation.

- [ ] I can enable Hyper-V and build the right virtual switch.
- [ ] I can create a Gen 2 VM and choose a memory and storage model.
- [ ] I can use production checkpoints and manage the AVHDX chain.
- [ ] I can place VMs on VLANs and reason about isolation choices.
- [ ] I completed Labs 8.1–8.4 including each negative test.
