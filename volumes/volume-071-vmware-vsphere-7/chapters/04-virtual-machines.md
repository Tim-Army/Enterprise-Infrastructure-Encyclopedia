# Chapter 04: Virtual Machines

## Learning Objectives

- Create and configure virtual machines on vSphere 7.
- Understand VM hardware versions, VMware Tools, and virtual devices.
- Use templates and the Content Library for standardized deployment.
- Manage snapshots correctly.
- Complete a walkthrough for each virtual-machine topic.

## Theory and Architecture

A **virtual machine** is a set of files (the `.vmx` configuration, `.vmdk` virtual disks, and
others) on a datastore, presenting virtual **CPU, memory, disk, and network** to a guest OS. The
**VM hardware version** (also "compatibility") determines available features and the maximum
hosts/versions that can run it — vSphere 7 introduced **hardware version 17** (7.0) and **18**
(7.0 U2). **VMware Tools** (drivers and services in the guest) enables graceful shutdown, time sync,
better performance, and quiescing. Virtual disks can be **thin** (allocated on demand) or **thick**;
network adapters are typically **VMXNET3**. **Templates** are golden, non-runnable VM images for
consistent deployment, and the **Content Library** stores and shares templates, ISOs, and OVF/OVA
across vCenters. **Snapshots** capture a point-in-time state for short-term rollback — they are
**not backups** and must be managed (consolidated/deleted) to avoid disk growth and performance
loss. VMs are the unit of work the whole platform exists to run.

## Design Considerations

Set the **hardware version** to the lowest that supports needed features and your host fleet (for
portability). Always install **VMware Tools**. Use **thin** disks with monitoring, or thick where
guaranteed space matters. Standardize with **templates** in the **Content Library**. Treat
**snapshots** as short-lived — never as backups.

## Implementation and Automation

The labs create a VM, deploy from a template/Content Library, and manage a snapshot with PowerCLI.

## Validation and Troubleshooting

Confirm the VM model:

```text
VM = files on datastore (.vmx + .vmdk). Hardware version (v17=7.0, v18=7.0U2) gates features/portability.
VMware Tools = guest drivers/services. Disks: thin/thick. NIC: VMXNET3. Templates + Content Library for standard deploy.
Snapshots = short-term rollback, NOT backups; consolidate/delete to avoid growth.
```

Common pitfalls: leaving **snapshots** for weeks (disk bloat, performance); and not installing
**VMware Tools**.

## Security and Best Practices

Install **VMware Tools**, keep the **hardware version** appropriate, standardize with **templates**,
and **delete snapshots** promptly. Right-size CPU/memory (over-provisioning hurts consolidation).
Encrypt sensitive VMs where required. Back up with real backup tools, not snapshots.

## Hands-On Lab

VM walkthroughs. **Shared prerequisites** — vCenter 7 with a host and datastore, PowerCLI, in a lab.
**Cost:** none.

### Lab 4.1 — Create a VM

**Objective:** Provision a new virtual machine.

```powershell
New-VM -Name "web01" -VMHost (Get-VMHost)[0] -Datastore (Get-Datastore)[0] `
  -NumCpu 2 -MemoryGB 4 -DiskGB 40 -DiskStorageFormat Thin -NetworkName "VM Network"
Get-VM web01 | Select Name, NumCpu, MemoryGB, @{N='HW';E={$_.HardwareVersion}}
```

**Expected result:** a VM **web01** with 2 vCPU, 4 GB RAM, a **thin** 40 GB disk — a new virtual
machine.

**Negative test:** create every VM with a **thick** disk on a small datastore; **thin** (monitored)
conserves space — choose per need.

**Cleanup:** `Remove-VM web01 -DeletePermanently -Confirm:$false`.

### Lab 4.2 — Convert to a template and deploy

**Objective:** Standardize deployment.

```powershell
Get-VM web01 | Set-VM -ToTemplate -Confirm:$false
New-VM -Name "web02" -Template (Get-Template web01) -VMHost (Get-VMHost)[0] -Datastore (Get-Datastore)[0]
Get-VM web02
```

**Expected result:** a **template** created and a new VM **deployed from it** — consistent,
repeatable provisioning.

**Negative test:** build each VM from scratch; **templates** guarantee consistency — deploy from
them.

**Cleanup:** remove web02 and the template.

### Lab 4.3 — Content Library

**Objective:** Share templates/ISOs across vCenter.

```powershell
New-ContentLibrary -Name "Lib1" -Datastore (Get-Datastore)[0] -Published
Get-ContentLibrary
# Add OVF/ISO items and deploy from the library across vCenters.
```

**Expected result:** a published **Content Library** for sharing templates/ISOs — centralized,
consistent content.

**Negative test:** copy ISOs/templates to each host/datastore manually; the **Content Library**
centralizes and syncs them.

**Cleanup:** `Remove-ContentLibrary Lib1 -Confirm:$false`.

### Lab 4.4 — Take and delete a snapshot

**Objective:** Manage a snapshot correctly.

```powershell
$vm = Get-VM web02
New-Snapshot -VM $vm -Name "pre-change" -Description "before patch"
# ... make the change, verify ...
Get-Snapshot -VM $vm | Remove-Snapshot -Confirm:$false   # delete promptly
Get-Snapshot -VM $vm
```

**Expected result:** a snapshot taken **and deleted** after the change — short-term rollback without
lingering disk growth.

**Negative test:** keep the snapshot indefinitely as a "backup"; snapshots **grow and slow the VM** —
delete promptly and back up properly.

**Cleanup:** ensure no snapshots remain.

### Lab 4.5 — Verify VMware Tools

**Objective:** Confirm guest integration.

```powershell
Get-VM | Select Name, @{N='Tools';E={$_.ExtensionData.Guest.ToolsStatus}}
```

**Expected result:** **VMware Tools** status per VM (toolsOk) — guest integration for graceful
operations.

**Negative test:** run production VMs with **Tools not installed**; graceful shutdown, time sync,
and quiescing need Tools — install them.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Virtual machines are files presenting virtual hardware, gated by the hardware version, integrated by
VMware Tools, standardized via templates and the Content Library, and rolled back short-term with
snapshots. Right-size VMs, install Tools, deploy from templates, and delete snapshots promptly.

- [ ] I can create a VM with PowerCLI.
- [ ] I can template and deploy from it.
- [ ] I can use a Content Library.
- [ ] I can manage snapshots correctly and verify Tools.
- [ ] I completed Labs 4.1–4.5 including each negative test.
