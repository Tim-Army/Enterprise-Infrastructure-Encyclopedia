# Chapter 02: Hitachi Storage and the VSP Platform

## Learning Objectives

- Describe the VSP (Virtual Storage Platform) block-storage family.
- Explain enterprise storage concepts — controllers, cache, RAID, and the SVOS operating system.
- Distinguish block, file, and object storage in the Hitachi portfolio.
- Understand storage virtualization — Hitachi's signature capability.

*Cert relevance: the VSP platform underlies the block-storage tracks; this chapter is the shared foundation.*

## The VSP family

The **VSP — Virtual Storage Platform** is Hitachi Vantara's **block-storage** product line, and the platform most Hitachi storage certifications center on. It is enterprise storage built for **reliability, performance, and availability** — the kind that runs mission-critical databases and applications where downtime and data loss are unacceptable. The family spans:

- **VSP 5000 series** — the **high-end**, highest-performance, highest-availability arrays.
- **VSP Midrange** — mid-tier arrays balancing performance and cost.
- **VSP One Block** — the modern block platform.
- **VSP 360** — the current management/administration experience (the focus of HQT-6742, [Ch 3](03-block-storage-administration.md)).

All run Hitachi's storage operating system and share a common architecture and management model, so skills transfer across the family. Enterprise storage is about **guarantees** — that data is there, correct, and fast — and the VSP line is engineered for that. The lab models the VSP family.

## Enterprise storage concepts

To administer VSP you need the **enterprise storage** fundamentals:

- **Controllers** — the redundant "brains" that process I/O; enterprise arrays have **dual (or more) controllers** so one can fail without downtime.
- **Cache** — fast memory that absorbs writes and speeds reads; mirrored across controllers for protection.
- **RAID and drives** — data is spread across drives with **RAID** (redundant array) so a drive failure loses no data; VSP supports flash/SSD and other media.
- **SVOS (Storage Virtualization Operating System)** — the software running the array, providing provisioning, data services, and virtualization.
- **LDEVs / LUNs** — logical volumes carved from pools and presented to hosts ([Ch 3](03-block-storage-administration.md)).

These fundamentals — redundancy at every layer, cache, RAID — are why enterprise storage is trusted for critical data, and they underpin every storage certification. The lab models controllers, cache, and RAID protection.

## Block, file, and object

Hitachi Vantara's portfolio spans the **three storage types**, and knowing which fits which workload is core knowledge:

- **Block storage** (VSP) — presents raw **volumes (LUNs)** to hosts over SAN (Fibre Channel, iSCSI); the choice for **databases and VMs** that need low-latency block access.
- **File storage** (VSP One File / NAS) — presents **shared file systems** over NFS/SMB; the choice for **user shares and file workloads** ([Ch 4](04-file-and-object-storage.md)).
- **Object storage** (Content Platform / HCP) — stores **objects** with rich metadata over HTTP/S3; the choice for **archives, backups, and cloud-native/unstructured data at massive scale** ([Ch 4](04-file-and-object-storage.md)).

The right type depends on the workload's **access pattern**: block for transactional, file for shared documents, object for scale and archive. Certifications specialize by type. The lab routes workloads to storage types.

## Storage virtualization

Hitachi's **signature capability** is **storage virtualization** — the ability of a VSP to **virtualize other storage arrays** (including third-party) **behind it**, presenting them as one pool it manages. This lets an enterprise:

- **Consolidate** heterogeneous storage under one management and data-services layer.
- **Extend the life** of existing arrays by placing them behind a VSP.
- **Apply VSP data services** (replication, tiering, thin provisioning) **across** virtualized storage.

This is where the "**Virtual**" in Virtual Storage Platform comes from, and it is a differentiator Hitachi emphasizes. Understanding that a VSP can be a **virtualization controller** for a whole storage estate, not just its own drives, is important platform knowledge. The lab models virtualizing an external array. *(This consolidation-under-one-control idea parallels how other platforms unify heterogeneous resources.)*

## Hands-On Lab

Python models the VSP family, enterprise-storage redundancy, storage types, and virtualization. **Cost:** none.

### Lab 2.1 — Model the VSP platform

**Objective:** See the VSP family, controller/cache/RAID redundancy, storage-type routing, and virtualization.

```bash
python3 - <<'EOF'
# VSP family
VSP = {"VSP 5000":"high-end","VSP Midrange":"mid-tier","VSP One Block":"modern block","VSP 360":"current admin experience"}
print("VSP FAMILY (block storage):")
for m,t in VSP.items(): print(f"   {m:14} {t}")

# enterprise redundancy: dual controllers, mirrored cache, RAID
class VSPArray:
    def __init__(self): self.controllers = ["ctrl-1","ctrl-2"]; self.raid = "RAID-6 (2 parity)"
    def survive_failure(self, failed):
        alive = [c for c in self.controllers if c != failed]
        return f"controller {failed} failed -> {alive[0]} keeps serving I/O (no downtime); {self.raid} survives 2 drive failures"
arr = VSPArray()
print(f"\nENTERPRISE REDUNDANCY: {arr.survive_failure('ctrl-1')}")

# route workloads to block/file/object by access pattern
def storage_type(workload):
    return {"database":"BLOCK (VSP LUN)","VM datastore":"BLOCK (VSP LUN)",
            "user file share":"FILE (VSP One File, NFS/SMB)","archive/backup":"OBJECT (Content Platform, S3)"}.get(workload,"?")
print("\nSTORAGE TYPE by workload:")
for w in ["database","user file share","archive/backup"]:
    print(f"   {w:16} -> {storage_type(w)}")

# storage virtualization: a VSP virtualizes an external array behind it
print("\nSTORAGE VIRTUALIZATION (the 'Virtual' in VSP):")
external = "3rd-party array (legacy)"
print(f"   VSP virtualizes '{external}' -> presents it as one pool + applies VSP data services (replication/tiering)")
print()
print("The VSP family (5000/Midrange/One Block/360) is enterprise BLOCK storage: DUAL controllers,")
print("mirrored CACHE, and RAID mean a controller or drive can fail with NO data loss or downtime.")
print("Block (LUN) for databases/VMs, FILE for shares, OBJECT for archive. And VSP can VIRTUALIZE")
print("other arrays behind it — consolidating a storage estate under one control. This is the cert foundation.")
EOF
```

**Expected result:** The VSP family, an array surviving a controller failure (dual controllers) and drive failures (RAID), workloads routed to block/file/object by access pattern, and a VSP virtualizing an external array. The lesson is the Hitachi storage foundation: VSP is redundant enterprise block storage (dual controllers, mirrored cache, RAID), the portfolio spans block/file/object for different access patterns, and VSP's signature is virtualizing other storage behind it.

**Negative test:** Running a transactional database on object storage, or a single-controller array for a mission-critical app. The database suffers with object semantics/latency, and a single controller means an outage on failure; matching storage type to workload and using redundant enterprise arrays is what storage administration is about.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The VSP family understood — VSP 5000/Midrange/One Block/360 enterprise block storage.
- [ ] Enterprise storage concepts understood — dual controllers, mirrored cache, RAID, SVOS, LDEVs.
- [ ] Block/file/object understood — matching storage type to workload access pattern.
- [ ] Storage virtualization understood — VSP virtualizing other arrays behind it, the "Virtual" in VSP.

## See also

- [Chapter 03 — Block Storage Administration](03-block-storage-administration.md) — provisioning and managing VSP block storage.
- [Chapter 04 — File and Object Storage](04-file-and-object-storage.md) — the other two storage types.
- [Volume LXXXIV — NetApp](../../volume-084-netapp-certifications/README.md) — enterprise storage on another platform.
