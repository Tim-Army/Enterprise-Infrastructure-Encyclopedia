# Chapter 03: FlashArray Fundamentals

## Learning Objectives

- Provision block storage: volumes, hosts, host groups, and connectivity.
- Use protection groups and snapshot schedules correctly.
- Choose between iSCSI, Fibre Channel, and NVMe-oF.
- Diagnose the common mapping mistakes that cause data corruption.

## The object model

**FlashArray** is block storage, and its model is small enough to hold in your head — which is the point of the product:

| Object | What it is |
|:---|:---|
| **Volume** | A block device presented to hosts |
| **Host** | An initiator (a server), identified by its WWNs or IQNs |
| **Host group** | A set of hosts that share volumes — a cluster |
| **Connection** | The mapping of a volume to a host or host group |
| **Protection group (pgroup)** | A set of volumes/hosts protected together on a shared snapshot and replication schedule |
| **Snapshot** | A point-in-time image, space-efficient and near-instant |

The absence of RAID groups, aggregates, and tiering policies is deliberate: capacity is a single pool, and provisioning is choosing a size and a name.

## The mapping rule that prevents corruption

The single most consequential operational rule in block storage:

> **A volume containing a non-clustered filesystem must be mapped to exactly one host.**

Two hosts writing to the same block device without a **cluster-aware filesystem** (or a clustering layer like VMware VMFS, which coordinates access) will corrupt it — each host caches metadata that the other invalidates without its knowledge. Nothing warns you at mapping time; the corruption appears later, under load.

This is what **host groups** exist for: a genuine cluster (VMware, Oracle RAC, a Windows failover cluster) is defined as a host group, and volumes are mapped to the group so that every member sees consistent connectivity.

## Connectivity

| Protocol | Notes |
|:---|:---|
| **Fibre Channel** | Dedicated storage fabric; predictable, requires HBAs and FC switches |
| **iSCSI** | Block over TCP/IP; uses existing Ethernet, needs careful network design |
| **NVMe-oF** (FC, TCP, RoCE) | Lower protocol overhead, designed for flash latency |

Whatever the protocol, **multipathing** is mandatory: multiple paths from host to array, with a supported multipath policy. A single-path host loses access when any component in that path is serviced — including during the non-disruptive controller upgrades of Chapter 02, which is precisely when you would rather find out you had redundancy.

## Protection groups

A **protection group** applies a snapshot and replication schedule to a set of volumes **atomically** — a crucial property when an application spans several volumes. Snapshotting a database's data and log volumes independently produces images from slightly different moments, which may not restore consistently. Placing them in one protection group produces a consistent set.

## Hands-On Lab

Python models FlashArray provisioning. **Cost:** none.

### Lab 3.1 — Volume-to-host mapping and the corruption trap

**Objective:** Validate mappings the way an experienced administrator would.

```bash
python3 - <<'EOF'
hosts = {
  "esxi-01": {"group":"vmware-cluster"},
  "esxi-02": {"group":"vmware-cluster"},
  "sql-01":  {"group":None},
  "sql-02":  {"group":None},
}
volumes = [
  {"name":"vmfs-datastore-1","fs":"VMFS (cluster-aware)","mapped_to":["vmware-cluster"],"is_group":True},
  {"name":"sql-data",        "fs":"NTFS (not cluster-aware)","mapped_to":["sql-01"],"is_group":False},
  {"name":"sql-scratch",     "fs":"NTFS (not cluster-aware)","mapped_to":["sql-01","sql-02"],"is_group":False},
]
for v in volumes:
    cluster_aware = "cluster-aware" in v["fs"]
    n = len(v["mapped_to"])
    if v["is_group"] and cluster_aware:
        verdict = "OK — cluster-aware filesystem mapped to a HOST GROUP; all members see it consistently"
    elif n == 1:
        verdict = "OK — single host, exclusive access"
    else:
        verdict = ("*** DANGER *** non-cluster-aware filesystem mapped to MULTIPLE hosts. "
                   "Both will cache metadata the other invalidates -> CORRUPTION under load. "
                   "Nothing warns you at mapping time.")
    print(f"{v['name']:18} fs={v['fs']:26} -> {v['mapped_to']}")
    print(f"{'':18} {verdict}\n")
print("Rule: non-clustered filesystem = exactly ONE host. Real clusters = a HOST GROUP.")
EOF
```

**Expected result:** The VMFS datastore mapped to a host group is correct, the single-host NTFS volume is correct, and `sql-scratch` mapped to two standalone hosts is flagged as a corruption risk. The detail that makes this dangerous in practice is that **the array performs the mapping without complaint** — the filesystem's assumptions are invisible to the storage layer, so the damage surfaces later and looks like a filesystem bug.

**Negative test:** Mapping a volume to a second host "temporarily, just to copy some files off" — that is the exact scenario, and the corruption typically appears after the temporary mapping is removed.

**Cleanup:** None.

### Lab 3.2 — Protection groups and crash-consistent sets

**Objective:** Show why multi-volume applications need grouping.

```bash
python3 - <<'EOF'
import datetime
base = datetime.datetime(2026, 8, 4, 2, 0, 0)

print("=== INDEPENDENT volume snapshots (no protection group) ===")
independent = [("sql-data", 0), ("sql-logs", 9), ("sql-temp", 17)]
for vol, offset in independent:
    print(f"   {vol:10} snapped at {(base + datetime.timedelta(seconds=offset)).strftime('%H:%M:%S')}")
print("   -> images are up to 17 seconds APART. Transactions committed in that gap exist in the")
print("      log snapshot but not the data snapshot (or vice versa). Restore may not be consistent.\n")

print("=== PROTECTION GROUP snapshot ===")
for vol in ("sql-data","sql-logs","sql-temp"):
    print(f"   {vol:10} snapped at {base.strftime('%H:%M:%S')}  (same instant, atomic set)")
print("   -> one consistent point in time across every volume the application uses.")
print("\nRule: if an application spans multiple volumes, they belong in ONE protection group.")
print("Application-consistent snapshots go further still (quiesce the app first) — see Vol CXXXIII ch08.")
EOF
```

**Expected result:** Independent snapshots land up to 17 seconds apart while the protection group captures one instant. The 17-second spread is the whole problem: a database's data and log files must represent the same moment, or recovery may be impossible or silently wrong. The pointer to application-consistent snapshots is the next level up — crash-consistent grouping is necessary but not always sufficient.

**Negative test:** Scheduling per-volume snapshots at the same clock time and assuming they are atomic — they start together and complete at different moments under load, which is precisely when consistency matters.

**Cleanup:** None.

### Lab 3.3 — Multipathing and the single-path trap

**Objective:** Check path redundancy against a controller upgrade.

```bash
python3 - <<'EOF'
hosts = [
  {"host":"esxi-01","paths":[("ctrl-A","fc-switch-1"),("ctrl-B","fc-switch-2"),
                             ("ctrl-A","fc-switch-2"),("ctrl-B","fc-switch-1")]},
  {"host":"sql-01", "paths":[("ctrl-A","fc-switch-1"),("ctrl-A","fc-switch-2")]},
  {"host":"app-03", "paths":[("ctrl-A","fc-switch-1")]},
]
for h in hosts:
    ctrls = {c for c, _ in h["paths"]}
    switches = {s for _, s in h["paths"]}
    issues = []
    if len(ctrls) < 2:    issues.append("ALL paths via ONE controller — a controller upgrade CUTS ACCESS")
    if len(switches) < 2: issues.append("ALL paths via ONE switch — switch maintenance cuts access")
    if len(h["paths"]) < 2: issues.append("SINGLE PATH — no redundancy at all")
    print(f"{h['host']:9} {len(h['paths'])} path(s), controllers={sorted(ctrls)}, switches={sorted(switches)}")
    for i in issues: print(f"{'':9}   {i}")
    if not issues: print(f"{'':9}   fully redundant — survives controller upgrade AND switch maintenance")
    print()
print("The non-disruptive upgrade of Chapter 02 is only non-disruptive FOR HOSTS WITH PATHS TO")
print("BOTH CONTROLLERS. sql-01 and app-03 would lose access during a routine, planned upgrade.")
EOF
```

**Expected result:** Only `esxi-01` is fully redundant; `sql-01` has two paths but both to controller A, and `app-03` has one path. The closing point ties the chapter back to Chapter 02: the array's non-disruptive upgrade guarantee is **conditional on host-side path configuration**, so an array-side feature silently fails for badly-configured hosts, and the failure shows up during planned maintenance.

**Negative test:** Counting paths without checking which controller they reach — two paths to the same controller looks redundant in a path count and provides no protection against the most common maintenance event.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The FlashArray object model learned: volumes, hosts, host groups, connections, protection groups.
- [ ] The one-host mapping rule applied, and host groups used for genuine clusters.
- [ ] Protection groups used to snapshot multi-volume applications atomically.
- [ ] Multipathing verified across both controllers and both fabrics.
