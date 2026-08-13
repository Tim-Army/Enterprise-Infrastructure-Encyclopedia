# Chapter 08: Portworx and Cloud-Native Storage

## Learning Objectives

- Explain why stateful workloads on Kubernetes need more than ephemeral storage.
- Describe PersistentVolumes, PersistentVolumeClaims, and StorageClasses.
- Use replication and failover to survive node loss.
- Apply snapshots and data protection to containerized applications.

## Containers were designed stateless

Kubernetes assumes pods are disposable: it kills and reschedules them freely, and a container's local filesystem dies with it. That model works beautifully for stateless services and collides with reality the moment you run a database, a message queue, or anything that remembers.

**Portworx** — the **Portworx Enterprise** Professional certification's subject — provides storage that survives pod rescheduling and node failure, presented through Kubernetes' native storage abstractions.

## The Kubernetes storage model

| Object | Role |
|:---|:---|
| **PersistentVolume (PV)** | A piece of storage in the cluster |
| **PersistentVolumeClaim (PVC)** | A pod's *request* for storage — size, access mode, class |
| **StorageClass** | A named template describing *how* to provision (replication, IOPS, encryption) |
| **CSI driver** | The interface between Kubernetes and the storage provider |

The flow is deliberately indirect: a pod references a **PVC**, the PVC names a **StorageClass**, and the class provisions a **PV** dynamically. That indirection is what lets the same manifest run on a laptop and in production against entirely different storage.

### Access modes

| Mode | Meaning |
|:---|:---|
| **ReadWriteOnce (RWO)** | Mounted read-write by one **node** |
| **ReadOnlyMany (ROX)** | Mounted read-only by many nodes |
| **ReadWriteMany (RWX)** | Mounted read-write by many nodes |

The trap mirrors Chapter 03's mapping rule: **RWX with a non-cluster-aware filesystem corrupts data.** Many storage backends do not support RWX at all, and a PVC requesting an unsupported mode simply stays **Pending** — a pod stuck in `ContainerCreating` with no obvious error is very often exactly this.

## Replication and failover

Portworx replicates volumes across nodes, so if a node fails the pod reschedules elsewhere and its data is already present. The replication factor is the key setting:

- **Replication factor 1** — no copies. Node failure means data loss.
- **Replication factor 2** — survives one node failure.
- **Replication factor 3** — survives two, at three times the capacity cost.

The scheduling benefit is subtle and important: with replicas on multiple nodes, Kubernetes can restart the pod on a node that **already holds the data**, so recovery does not wait for a volume to move.

## Hands-On Lab

Python models Kubernetes storage. **Cost:** none.

### Lab 8.1 — PVC binding and the Pending trap

**Objective:** Resolve claims against classes, and diagnose the silent failure.

```bash
python3 - <<'EOF'
storage_classes = {
  "px-db":     {"repl":3, "modes":{"RWO"},        "encrypted":True},
  "px-shared": {"repl":2, "modes":{"RWO","RWX"},  "encrypted":False},
  "px-scratch":{"repl":1, "modes":{"RWO"},        "encrypted":False},
}
claims = [
  {"pvc":"postgres-data","class":"px-db",     "mode":"RWO","size_gb":100},
  {"pvc":"web-uploads",  "class":"px-shared", "mode":"RWX","size_gb":50},
  {"pvc":"cache",        "class":"px-scratch","mode":"RWO","size_gb":20},
  {"pvc":"reports",      "class":"px-db",     "mode":"RWX","size_gb":30},
]
for c in claims:
    sc = storage_classes[c["class"]]
    if c["mode"] in sc["modes"]:
        print(f"{c['pvc']:14} -> BOUND   class={c['class']:11} {c['mode']} {c['size_gb']}GB "
              f"repl={sc['repl']} encrypted={sc['encrypted']}")
    else:
        print(f"{c['pvc']:14} -> PENDING class={c['class']:11} requests {c['mode']}, "
              f"class supports {sorted(sc['modes'])}")
        print(f"{'':17} The PVC stays Pending FOREVER and the pod sits in ContainerCreating.")
        print(f"{'':17} No error is raised on the pod — check the PVC, not the pod.")
print("\nAlso note px-scratch has repl=1: fine for a cache, DATA LOSS for anything that matters.")
EOF
```

**Expected result:** Three claims bind and `reports` stays **Pending** because it asks for RWX from a class that only supports RWO. The diagnostic note is the practically valuable part — the pod's events say nothing useful, so the habit of describing the *PVC* rather than the pod is what shortens this from an hour to a minute.

**Negative test:** Debugging the pod when a PVC will not bind — the pod is a victim; the mode or class mismatch is visible only on the claim.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Replication factor and node failure

**Objective:** Model survival and recovery speed.

```bash
python3 - <<'EOF'
def outcome(repl, nodes_failed):
    if nodes_failed >= repl:
        return "DATA LOSS", f"all {repl} replica(s) were on failed nodes"
    return "SURVIVES", f"{repl - nodes_failed} replica(s) remain; pod reschedules onto a node that HAS the data"

print(f"{'repl':>5}{'nodes failed':>14}   result")
for repl in (1, 2, 3):
    for failed in (1, 2):
        res, why = outcome(repl, failed)
        print(f"{repl:>5}{failed:>14}   {res:11} — {why}")
    print()
print("Capacity cost: repl=3 stores 3x. Choose per workload, not globally:")
print("   cache / scratch      -> repl 1 (can be rebuilt; do not pay 3x for it)")
print("   general applications -> repl 2")
print("   production databases -> repl 3")
print("\nThe scheduling win matters as much as the durability: with replicas on several nodes,")
print("Kubernetes restarts the pod where the data ALREADY IS, instead of waiting on a volume move.")
EOF
```

**Expected result:** Replication factor 1 loses data on any node failure; 2 survives one; 3 survives two — at proportional capacity cost. The per-workload guidance is the point: a uniform replication factor either over-pays for scratch data or under-protects databases, and the right setting is a property of the workload rather than of the cluster.

**Negative test:** Setting replication factor 1 cluster-wide to save capacity — the first node failure destroys every stateful workload simultaneously.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Protecting stateful applications

**Objective:** Apply consistent snapshots to multi-volume applications on Kubernetes.

```bash
python3 - <<'EOF'
app = {
  "name":"orders-service",
  "volumes":[
    {"pvc":"orders-postgres-data","role":"database data"},
    {"pvc":"orders-postgres-wal", "role":"write-ahead log"},
    {"pvc":"orders-uploads",      "role":"user uploads"},
  ],
}
def snapshot(mode):
    print(f"\n--- {mode} ---")
    if mode == "per-PVC (independent)":
        for i, v in enumerate(app["volumes"]):
            print(f"   {v['pvc']:26} snapped at t+{i*6}s")
        print("   -> data and WAL are from DIFFERENT moments; the database may not restore cleanly")
    else:
        for v in app["volumes"]:
            print(f"   {v['pvc']:26} snapped at t+0s  (group-consistent)")
        print("   -> one consistent set across the whole application")
snapshot("per-PVC (independent)")
snapshot("application group snapshot")
print("\nSame rule as Chapter 03's protection groups, now at the Kubernetes layer: an application")
print("spanning several PVCs must be snapshotted as ONE GROUP.")
print("And the same caveat applies — a group snapshot is CRASH-consistent. For a database,")
print("quiesce it first (or use its native backup) for APPLICATION consistency.")
EOF
```

**Expected result:** Independent PVC snapshots land seconds apart while a group snapshot captures one instant. This is Chapter 03's protection-group lesson restated at the orchestration layer, with the same escalation to application consistency — the storage layer can give you a consistent *set*, and only the database can give you a consistent *database*.

**Negative test:** Snapshotting each PVC on its own schedule — the data and write-ahead-log volumes drift apart, and recovery may fail in ways that only appear when you attempt it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Kubernetes storage model learned: PV, PVC, StorageClass, CSI.
- [ ] Access modes applied, with the RWX corruption risk and the Pending-PVC diagnosis understood.
- [ ] Replication factor chosen per workload for durability and scheduling speed.
- [ ] Multi-PVC applications snapshotted as a group, with application consistency distinguished.
