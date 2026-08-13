# Chapter 06: vSphere Storage

## Learning Objectives

- Explain vSphere storage: datastores, VMFS, and NFS.
- Configure and manage datastores and multipathing.
- Understand vSAN 7 (hyperconverged storage).
- Apply Storage Policy Based Management (SPBM).
- Complete a walkthrough for each storage topic.

## Theory and Architecture

vSphere presents storage to VMs as **datastores**. **VMFS** is VMware's clustered filesystem on
block storage (FC, iSCSI, local) — multiple hosts share a VMFS datastore, enabling vMotion and HA.
**NFS** datastores use file storage from a NAS. **Multipathing** (PSA/NMP with path selection
policies like Round Robin) provides redundant paths to block storage. **vSAN 7** is VMware's
**hyperconverged** software-defined storage: it pools the **local disks** of cluster hosts (cache +
capacity tiers) into a single shared datastore, with data and availability defined by policy — no
external SAN needed. The unifying model is **Storage Policy Based Management (SPBM)**: instead of
placing VMs on specific datastores, you attach a **storage policy** (e.g., "tolerate one host
failure, thick provision") and vSphere places/protects the VM to satisfy it. Storage is where VM
data lives and where availability and performance are ultimately decided.

## Design Considerations

Use **VMFS** on shared block storage or **vSAN** for hyperconverged. Configure **Round Robin**
multipathing for block storage redundancy. Define **storage policies (SPBM)** and let vSphere place
VMs to meet them, rather than hand-placing on datastores. Size vSAN cache/capacity and fault domains
for the required availability. Monitor datastore free space.

## Implementation and Automation

The labs list datastores, configure multipathing, apply a storage policy, and perform storage
vMotion — with esxcli/PowerCLI.

## Validation and Troubleshooting

Confirm the storage model:

```text
Datastores: VMFS (block: FC/iSCSI/local, clustered) | NFS (NAS). Multipathing: PSA/NMP (Round Robin).
vSAN 7: pool local disks (cache+capacity) -> shared HCI datastore, policy-defined availability.
SPBM: attach a storage policy -> vSphere places/protects the VM to satisfy it.
```

Common pitfalls: **hand-placing** VMs on datastores instead of using **SPBM**; and **single-path**
block storage (no redundancy).

## Security and Best Practices

Use **SPBM** so availability/performance are policy-driven and auditable, configure **multipathing**
for block redundancy, and size **vSAN** fault domains for the failure tolerance you need. Monitor
free space; encrypt datastores/VMs where required. Storage decisions determine resilience.

## Hands-On Lab

Storage walkthroughs. **Shared prerequisites** — vCenter 7 with hosts and storage, PowerCLI/esxcli,
in a lab. **Cost:** none.

### Lab 6.1 — List datastores and free space

**Objective:** Review the storage inventory.

```powershell
Get-Datastore | Select Name, Type, @{N='CapacityGB';E={[math]::Round($_.CapacityGB)}}, `
  @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB)}}
```

**Expected result:** each datastore's **type and free space** — the storage inventory to plan
against.

**Negative test:** provision VMs without checking **free space**; a full datastore stuns VMs —
monitor it.

**Rollback:** none (read-only).

### Lab 6.2 — Configure Round Robin multipathing

**Objective:** Ensure redundant block-storage paths.

```bash
esxcli storage nmp device list | head
# Set Round Robin on a device for path redundancy/load balancing:
esxcli storage nmp device set --device <naa.id> --psp VMW_PSP_RR
esxcli storage nmp device list -d <naa.id>
```

**Expected result:** the device using **Round Robin (VMW_PSP_RR)** — redundant, balanced paths.

**Negative test:** leave a fixed single path on multipathed storage; use **Round Robin** for
redundancy and throughput.

**Rollback:** revert PSP if needed (in a lab).

### Lab 6.3 — Apply a storage policy (SPBM)

**Objective:** Drive placement/protection by policy.

```powershell
# Assign an existing storage policy (e.g., vSAN "FTT=1") to a VM:
Get-VM web02 | Set-SpbmEntityConfiguration -StoragePolicy (Get-SpbmStoragePolicy -Name "vSAN Default Storage Policy")
Get-SpbmEntityConfiguration (Get-VM web02)
```

**Expected result:** the VM bound to a **storage policy** (e.g., tolerate one failure) — policy-
driven storage.

**Negative test:** place a VM on a specific datastore hoping for the right protection; **SPBM**
enforces it — attach a policy.

**Rollback:** reset to the default policy.

### Lab 6.4 — Storage vMotion

**Objective:** Move a VM's storage live.

```powershell
Move-VM -VM web02 -Datastore (Get-Datastore | Sort FreeSpaceGB -Descending)[0]
```

**Expected result:** the VM's disks **migrated live** to another datastore with no downtime —
storage flexibility.

**Negative test:** power off a VM to move its storage; **Storage vMotion** does it live — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.5 — vSAN health concept

**Objective:** Understand vSAN's policy-based availability.

```text
# vSAN pools host local disks into one datastore; a storage policy like "FTT=1" keeps a mirror copy
#   so one host/disk failure loses no data. vSAN health monitors disks, network, and objects.
"vSAN: local disks -> HCI datastore; FTT policy = failures tolerated; health monitors it"
```

**Expected result:** the **vSAN** availability model (FTT) — hyperconverged, policy-protected
storage.

**Negative test:** run vSAN with **FTT=0** for important VMs; a single failure loses data — set an
appropriate FTT.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere storage presents VMFS/NFS datastores (and vSAN hyperconverged storage), protected by
multipathing and governed by Storage Policy Based Management, with live Storage vMotion. Use SPBM
for policy-driven placement, multipath block storage, size vSAN for the required FTT, and monitor
capacity.

- [ ] I can inspect datastores and free space.
- [ ] I can configure Round Robin multipathing.
- [ ] I can apply a storage policy (SPBM).
- [ ] I can perform Storage vMotion and explain vSAN FTT.
- [ ] I completed Labs 6.1–6.5 including each negative test.
