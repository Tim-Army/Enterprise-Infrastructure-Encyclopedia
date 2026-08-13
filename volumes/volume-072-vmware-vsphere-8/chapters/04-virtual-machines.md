# Chapter 04: Virtual Machines

## Learning Objectives

- Configure vSphere 8 virtual machines and hardware versions (v20/v21).
- Use device groups for coordinated hardware assignment.
- Assign vGPU and passthrough devices.
- Standardize with templates and the Content Library.
- Complete a walkthrough for each virtual-machine topic.

## Theory and Architecture

Virtual machines in vSphere 8 work as in 7 — files on a datastore presenting virtual hardware — with
newer **VM hardware versions (v20 in 8.0, v21 in 8.0 U2/U3)** that unlock the latest features and
guest support. Two capabilities stand out. **Device groups** let a VM consume **coordinated
hardware** — for example, a NIC and a GPU that must share a PCIe complex, or **vendor device
groups** that a hardware vendor defines — so vSphere places and migrates the VM with its device
dependencies intact. **vGPU** (NVIDIA GRID and successors) and **DirectPath I/O passthrough** give
VMs accelerated or direct hardware access for AI/ML, VDI, and high-performance workloads; vSphere 8
improves live operations (e.g., vMotion) for some of these. As always, **VMware Tools** provides
guest integration, **templates** and the **Content Library** standardize deployment, and
**snapshots** are short-term rollback (not backups). The VM is still the unit of work; vSphere 8
extends what hardware it can consume.

## Design Considerations

Set the **hardware version** to the newest your host fleet supports (for features) balanced against
portability. Use **device groups** when a VM needs coordinated hardware. Assign **vGPU** for
accelerated workloads and size profiles to the GPU. Standardize with **templates/Content Library**,
and keep **snapshots** short-lived. Install **VMware Tools** everywhere.

## Implementation and Automation

The labs create a VM at a modern hardware version, reason about device groups and vGPU, and deploy
from the Content Library.

## Validation and Troubleshooting

Confirm the VM model:

```text
Hardware versions: v20 (8.0), v21 (8.0 U2/U3). Device groups: coordinated hardware (NIC+GPU, vendor-defined).
vGPU (NVIDIA) + DirectPath passthrough for acceleration; improved live ops in 8. Templates + Content Library. Tools. Snapshots = short-term.
```

Common pitfalls: setting **v21** on hosts that don't support it (portability/compat); and manual
device assignment where a **device group** keeps dependencies coherent.

## Security and Best Practices

Choose the **hardware version** deliberately, use **device groups** for coordinated hardware,
right-size **vGPU** profiles, standardize with **templates**, and delete **snapshots** promptly.
Install **VMware Tools**. Encrypt sensitive VMs. Back up with real tools.

## Hands-On Lab

VM walkthroughs. **Shared prerequisites** — vCenter 8 with a host and datastore, PowerCLI, in a lab.
**Cost:** none.

### Lab 4.1 — Create a VM at a modern hardware version

**Objective:** Provision a VM and set compatibility.

```powershell
$vm = New-VM -Name "app01" -VMHost (Get-VMHost)[0] -Datastore (Get-Datastore)[0] `
  -NumCpu 4 -MemoryGB 8 -DiskGB 60 -DiskStorageFormat Thin -NetworkName "VM Network"
# Set VM hardware compatibility (version) as supported by the host:
Set-VM -VM $vm -HardwareVersion "vmx-20" -Confirm:$false
Get-VM app01 | Select Name, NumCpu, MemoryGB, HardwareVersion
```

**Expected result:** a VM at **hardware version 20** — a vSphere 8 VM with current features.

**Negative test:** set **vmx-21** on a host that only supports v20; match the hardware version to
the **host capability** — check first.

**Rollback:** `Remove-VM app01 -DeletePermanently -Confirm:$false`.

### Lab 4.2 — Device groups concept

**Objective:** Understand coordinated hardware.

```text
# A device group binds hardware that must stay together (e.g., a NIC + GPU on the same PCIe complex,
#   or a vendor-defined group). vSphere places/migrates the VM keeping the device dependency intact.
"device group: coordinated hardware (NIC+GPU / vendor-defined) -> VM keeps its device dependencies"
```

**Expected result:** the **device group** model — coordinated hardware assignment for the VM.

**Negative test:** assign interdependent devices separately; a **device group** keeps them coherent
for placement/migration — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — vGPU assignment concept

**Objective:** Accelerate a workload with a GPU.

```text
# Add a shared PCI device (NVIDIA vGPU) with a profile sized to the workload (e.g., grid_a100-8c).
#   vSphere 8 improves live operations for GPU-backed VMs. Used for AI/ML and VDI.
"vGPU: shared GPU profile on the VM -> accelerated AI/ML/VDI; size the profile to the GPU"
```

**Expected result:** a **vGPU** profile on the VM — hardware-accelerated compute.

**Negative test:** run AI/ML on CPU-only VMs; assign **vGPU** for acceleration where the workload
needs it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Deploy from the Content Library

**Objective:** Standardize deployment.

```powershell
New-ContentLibrary -Name "Lib8" -Datastore (Get-Datastore)[0] -Published
# Add an OVF/template item, then deploy a VM from it (consistent across vCenters).
Get-ContentLibrary Lib8
```

**Expected result:** a **Content Library** for consistent, shareable templates/ISOs — standardized
provisioning (same as 7).

**Negative test:** copy templates per host manually; the **Content Library** centralizes them.

**Rollback:** `Remove-ContentLibrary Lib8 -Confirm:$false`.

### Lab 4.5 — Manage a snapshot

**Objective:** Use snapshots correctly.

```powershell
$vm = Get-VM app01
New-Snapshot -VM $vm -Name "pre-upgrade"
# ... change, verify ...
Get-Snapshot -VM $vm | Remove-Snapshot -Confirm:$false
```

**Expected result:** a snapshot taken **and deleted** promptly — short-term rollback without disk
bloat.

**Negative test:** keep the snapshot as a backup; snapshots **grow and slow** the VM — delete them
and back up properly.

**Rollback:** ensure no snapshots remain.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 8 VMs add newer hardware versions (v20/v21), device groups for coordinated hardware, and
improved vGPU/passthrough for acceleration, while keeping templates, the Content Library, Tools, and
short-lived snapshots. Choose the hardware version deliberately, use device groups, size vGPU
profiles, and manage snapshots correctly.

- [ ] I can create a VM at a modern hardware version.
- [ ] I can explain device groups.
- [ ] I can explain vGPU assignment.
- [ ] I can deploy from the Content Library and manage snapshots.
- [ ] I completed Labs 4.1–4.5 including each negative test.
