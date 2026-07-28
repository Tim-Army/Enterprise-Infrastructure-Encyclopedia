# Chapter 06: Storage and vSAN 8 Express Storage Architecture

## Learning Objectives

- Explain vSphere 8 storage and the vSAN 8 Express Storage Architecture (ESA).
- Compare ESA with the Original Storage Architecture (OSA).
- Apply Storage Policy Based Management on vSAN ESA.
- Manage datastores, multipathing, and NVMe.
- Complete a walkthrough for each storage topic.

## Theory and Architecture

vSphere 8 storage keeps the familiar model — **VMFS/NFS datastores**, **multipathing** (Round
Robin), **SPBM**, and **Storage vMotion** — and introduces the **vSAN 8 Express Storage
Architecture (ESA)**. The classic vSAN (now called the **Original Storage Architecture, OSA**) uses
a two-tier design (a cache tier fronting a capacity tier) built for the SATA/SAS SSD era. **ESA** is
a **ground-up redesign for high-performance NVMe**: a **single tier** of NVMe devices, a new
log-structured filesystem and data path, and **RAID-5/6 erasure coding with the performance of
mirroring** — so you get space efficiency *and* speed, plus better compression, all defined by
**storage policy**. ESA runs on validated all-NVMe **ESA-ready** hardware; OSA remains supported for
existing/hybrid deployments. The unifying model is unchanged: attach a **storage policy** (FTT, RAID
level, space efficiency) and vSAN places and protects data to satisfy it. vSphere 8 also raises
storage maximums and improves NVMe/NVMe-oF support.

## Design Considerations

Use **vSAN ESA** on all-NVMe, ESA-ready hardware for the best performance and efficiency; keep
**OSA** for existing hybrid/SATA deployments. Define **storage policies** (FTT and RAID) and let
vSAN enforce them — ESA makes **RAID-5/6** viable for performance-sensitive workloads. Multipath
external block storage, and monitor capacity/health.

## Implementation and Automation

The labs list datastores, apply a storage policy, compare ESA vs OSA, and perform Storage vMotion.

## Validation and Troubleshooting

Confirm the storage model:

```text
Datastores: VMFS/NFS + multipathing (Round Robin) + SPBM + Storage vMotion (as in 7).
vSAN 8 ESA: single-tier all-NVMe, log-structured, RAID-5/6 with mirror-like performance + better compression.
  vs OSA (classic cache+capacity, SATA/SAS era; still supported). Policy-driven (FTT/RAID).
```

Common pitfalls: expecting **ESA** on non-NVMe/non-ESA-ready hardware; and avoiding **RAID-5/6** for
performance — on **ESA** it performs like mirroring.

## Security and Best Practices

Deploy **ESA** on validated all-NVMe hardware for efficiency and speed, drive protection with
**SPBM** (appropriate FTT/RAID), multipath external storage, and monitor **vSAN health** and
capacity. Encrypt where required. Storage decisions still determine resilience and performance.

## Hands-On Lab

Storage walkthroughs. **Shared prerequisites** — vCenter 8 with hosts and storage (vSAN cluster for
ESA labs), PowerCLI/esxcli, in a lab. **Cost:** none.

### Lab 6.1 — List datastores and free space

**Objective:** Review the storage inventory.

```powershell
Get-Datastore | Select Name, Type, @{N='CapacityGB';E={[math]::Round($_.CapacityGB)}}, `
  @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB)}}
```

**Expected result:** each datastore's **type and free space** — the storage inventory (same as 7).

**Negative test:** provision without checking **free space**; a full datastore stuns VMs — monitor
it.

**Cleanup:** none (read-only).

### Lab 6.2 — Compare ESA and OSA

**Objective:** Choose the vSAN architecture.

```python
python3 - <<'PY'
arch={"OSA (Original)":"cache tier + capacity tier; SATA/SAS era; mirroring preferred for perf",
      "ESA (Express)":"single all-NVMe tier; log-structured; RAID-5/6 with mirror-like performance + compression"}
for a,d in arch.items(): print(f"{a:16}: {d}")
print("choose ESA on all-NVMe ESA-ready hardware; OSA for existing/hybrid")
PY
```

**Expected result:** the **ESA vs OSA** comparison — ESA for all-NVMe performance and efficiency.

**Negative test:** deploy ESA on SATA SSDs; **ESA needs all-NVMe ESA-ready** hardware — use OSA
there.

**Cleanup:** none.

### Lab 6.3 — Apply a storage policy (RAID-5 on ESA)

**Objective:** Drive protection and efficiency by policy.

```powershell
# On vSAN ESA, a RAID-5/6 policy gives space efficiency with mirror-like performance.
Get-VM app01 | Set-SpbmEntityConfiguration -StoragePolicy (Get-SpbmStoragePolicy | Where {$_.Name -match "RAID-5|ESA"} | Select -First 1)
Get-SpbmEntityConfiguration (Get-VM app01)
```

**Expected result:** the VM bound to a **RAID-5/ESA** policy — efficient, performant, policy-driven
protection.

**Negative test:** avoid RAID-5/6 to "keep performance"; on **ESA** it performs like mirroring —
use it for efficiency.

**Cleanup:** reset to the default policy.

### Lab 6.4 — Round Robin multipathing

**Objective:** Ensure redundant block-storage paths.

```bash
esxcli storage nmp device list | head
esxcli storage nmp device set --device <naa.id> --psp VMW_PSP_RR
```

**Expected result:** external block storage on **Round Robin** — redundant, balanced paths (same as
7).

**Negative test:** leave a single fixed path; use **Round Robin** for redundancy/throughput.

**Cleanup:** revert PSP in a lab.

### Lab 6.5 — Storage vMotion

**Objective:** Move a VM's storage live.

```powershell
Move-VM -VM app01 -Datastore (Get-Datastore | Sort FreeSpaceGB -Descending)[0]
```

**Expected result:** the VM's disks **migrated live** to another datastore — no downtime.

**Negative test:** power off to move storage; **Storage vMotion** does it live — use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 8 storage keeps VMFS/NFS, multipathing, SPBM, and Storage vMotion, and adds vSAN 8 ESA — a
single-tier, all-NVMe, log-structured architecture giving RAID-5/6 with mirror-like performance and
better efficiency, alongside the classic OSA. Use ESA on all-NVMe hardware, drive protection with
SPBM, and adopt RAID-5/6 on ESA.

- [ ] I can inspect datastores and free space.
- [ ] I can compare vSAN ESA and OSA.
- [ ] I can apply a RAID-5/ESA storage policy.
- [ ] I can configure multipathing and Storage vMotion.
- [ ] I completed Labs 6.1–6.5 including each negative test.
