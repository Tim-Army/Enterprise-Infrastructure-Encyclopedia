# Chapter 04: FlashBlade and Unstructured Data

## Learning Objectives

- Distinguish file, object, and block storage, and choose between them.
- Describe FlashBlade's scale-out architecture and where it fits.
- Explain what FlashBlade//EXA adds for AI and high-performance computing.
- Size capacity and performance for unstructured workloads.

## Three storage types

The **FlashBlade Storage** certification is about unstructured data, so the first thing to get right is what "unstructured" means and which access method suits it.

| Type | Access unit | Protocols | Fits |
|:---|:---|:---|:---|
| **Block** (FlashArray) | Fixed-size blocks; the host puts a filesystem on top | FC, iSCSI, NVMe-oF | Databases, virtualization, anything wanting a raw device |
| **File** (FlashBlade) | Files in a directory hierarchy, shared | NFS, SMB | Home directories, shared project data, media, analytics |
| **Object** (FlashBlade) | Immutable objects with metadata in a flat namespace | S3 | Backups, archives, data lakes, cloud-native applications |

The decision rule that resolves most cases:

- Does an application need a **raw device** it formats itself? → **block**.
- Do multiple clients need to **share and modify** the same files concurrently? → **file**.
- Are you writing **whole objects** that are read later and rarely modified in place? → **object**.

Object storage's defining constraint is worth stating plainly: **objects are replaced, not edited**. You cannot seek into an object and change a byte the way you can in a file, which is exactly why it scales — no locking, no shared-state coordination.

## Scale-out

FlashBlade is **scale-out**: capacity and performance grow by adding blades, and the system presents one namespace regardless of size. That differs from scale-up designs where a controller pair is the ceiling.

The property that matters for planning: in a scale-out system, **performance grows with capacity**, so a large dataset is not automatically a slow one. In scale-up designs, adding capacity behind a fixed controller pair dilutes performance per terabyte.

## FlashBlade//EXA

**FlashBlade//EXA** targets **AI and HPC** data pipelines, where the workload is many clients reading a shared dataset at extreme aggregate throughput — GPU training clusters being the current driver. The distinguishing requirement is not IOPS on small random reads but **sustained parallel bandwidth** to many readers at once, which is an architecturally different problem.

## Hands-On Lab

Python models unstructured storage decisions. **Cost:** none.

### Lab 4.1 — Choose file, object, or block

**Objective:** Apply the decision rule to real workloads.

```bash
python3 - <<'EOF'
workloads = [
  {"name":"Oracle database",       "raw_device":True,  "shared_concurrent_edit":False,"whole_object_writes":False},
  {"name":"Team project share",    "raw_device":False, "shared_concurrent_edit":True, "whole_object_writes":False},
  {"name":"Backup repository",     "raw_device":False, "shared_concurrent_edit":False,"whole_object_writes":True},
  {"name":"ML training dataset",   "raw_device":False, "shared_concurrent_edit":False,"whole_object_writes":True},
  {"name":"VMware datastore",      "raw_device":True,  "shared_concurrent_edit":False,"whole_object_writes":False},
  {"name":"Home directories",      "raw_device":False, "shared_concurrent_edit":True, "whole_object_writes":False},
]
for w in workloads:
    if w["raw_device"]:
        choice, why = "BLOCK (FlashArray)", "the application formats and owns a raw device"
    elif w["shared_concurrent_edit"]:
        choice, why = "FILE (FlashBlade NFS/SMB)", "multiple clients read AND modify the same files"
    elif w["whole_object_writes"]:
        choice, why = "OBJECT (FlashBlade S3)", "written whole, read later, rarely edited in place"
    else:
        choice, why = "FILE", "default for shared access"
    print(f"{w['name']:24} -> {choice:26} ({why})")
print("\nKey constraint: objects are REPLACED, never edited in place. That restriction is exactly")
print("what lets object storage scale — no byte-range locking, no shared-state coordination.")
print("Put a database on object storage and you will fight that constraint every day.")
EOF
```

**Expected result:** Databases and the VMware datastore route to block, shared editable data to file, and backups and training datasets to object. The closing note explains *why* the categories exist rather than treating them as arbitrary: object storage's scalability is purchased with an immutability constraint, and workloads that need in-place modification are fighting the design.

**Negative test:** Choosing object storage for a workload that rewrites small portions of large files — every change becomes a full-object rewrite, and both cost and latency multiply.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Scale-out versus scale-up performance

**Objective:** Show how performance-per-terabyte diverges as capacity grows.

```bash
python3 - <<'EOF'
def scale_up(capacity_tb, controller_max_gbs=20):
    return {"throughput_gbs": controller_max_gbs, "per_tb": controller_max_gbs / capacity_tb}
def scale_out(capacity_tb, gbs_per_blade=2.5, tb_per_blade=50):
    blades = max(1, -(-capacity_tb // tb_per_blade))
    throughput = blades * gbs_per_blade
    return {"blades": blades, "throughput_gbs": throughput, "per_tb": throughput / capacity_tb}

print(f"{'capacity':>10}{'scale-up GB/s':>16}{'per TB':>10}   |{'scale-out GB/s':>16}{'per TB':>10}{'blades':>8}")
for cap in (50, 200, 500, 1000):
    su, so = scale_up(cap), scale_out(cap)
    print(f"{cap:>8} TB{su['throughput_gbs']:>16.1f}{su['per_tb']:>10.3f}   |"
          f"{so['throughput_gbs']:>16.1f}{so['per_tb']:>10.3f}{so['blades']:>8}")
print("\nScale-up: throughput is FIXED by the controller pair, so performance per TB falls as you")
print("add capacity — a 1 PB dataset gets the same 20 GB/s a 50 TB one did.")
print("Scale-out: adding blades adds capacity AND throughput, so per-TB performance stays flat.")
print("This is why 'large dataset' does not have to mean 'slow dataset'.")
EOF
```

**Expected result:** Scale-up throughput stays at 20 GB/s while per-terabyte performance falls by a factor of twenty from 50 TB to 1 PB; scale-out holds per-terabyte performance constant. That divergence is the architectural argument for scale-out on unstructured data, where datasets grow by orders of magnitude and the access pattern is many clients at once.

**Negative test:** Planning a petabyte analytics dataset on a scale-up array sized by capacity alone — the capacity fits and the throughput does not, and that only becomes apparent when the workload arrives.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Size for AI training throughput

**Objective:** Check that storage can feed the compute.

```bash
python3 - <<'EOF'
def feed_check(gpus, gbs_per_gpu_needed, storage_gbs):
    demand = gpus * gbs_per_gpu_needed
    if demand > storage_gbs:
        util = storage_gbs / demand * 100
        return (f"STORAGE-BOUND — GPUs demand {demand:.0f} GB/s, storage delivers {storage_gbs:.0f}. "
                f"GPUs run at ~{util:.0f}% utilization; you are paying for idle accelerators")
    return f"balanced — demand {demand:.0f} GB/s within {storage_gbs:.0f} GB/s available"

print("AI training cluster feeding checks:\n")
for gpus, per_gpu, storage in [(8, 1.0, 20), (64, 1.0, 20), (64, 1.0, 160), (256, 0.8, 160)]:
    print(f"{gpus:>4} GPUs x {per_gpu} GB/s -> {feed_check(gpus, per_gpu, storage)}")
print("\nAI/HPC storage is a BANDWIDTH problem, not an IOPS problem: many readers pulling a shared")
print("dataset in parallel. FlashBlade//EXA targets exactly this — sustained parallel throughput.")
print("\nThe economics are brutal: idle GPUs are the most expensive idle resource in the building,")
print("so under-sizing storage to save money wastes far more than it saves.")
EOF
```

**Expected result:** Eight GPUs are fed comfortably, 64 GPUs against the same storage run at roughly 31% utilization, and scaling storage restores balance. The economic argument in the closing lines is the one that matters for design decisions: storage under-provisioning in an AI cluster manifests as **expensive accelerators waiting**, which dwarfs the storage saving.

**Negative test:** Sizing AI storage by capacity alone — the dataset fits, the GPUs starve, and the symptom presents as "the training job is slow" rather than as a storage problem.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Block, file, and object distinguished, with the objects-are-replaced constraint understood.
- [ ] Scale-out architecture explained, and per-terabyte performance compared against scale-up.
- [ ] FlashBlade//EXA placed as the AI/HPC parallel-bandwidth variant.
- [ ] AI training storage sized on bandwidth so accelerators are not left waiting.
