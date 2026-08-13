# Chapter 02: Technology Solutions and Storage Foundations

## Learning Objectives

- Explain the ONTAP cluster model (nodes, HA pairs, cluster network).
- Manage feature licensing on a cluster.
- Create and inspect aggregates from disks.
- Explain RAID-DP and RAID-TEC resiliency.
- Complete a walkthrough for each storage-foundation topic.

## Theory and Architecture

The **Technology Solutions** Professional and the **Associate** accreditations ground the NetApp
portfolio: **ONTAP** software, the storage systems (**AFF**, **ASA**, **FAS**), and the hybrid-cloud
services around them. Physically, an ONTAP deployment is a **cluster** of **nodes** paired into **HA
pairs** (each node can take over its partner) joined by a private **cluster network**. Storage begins
with **disks** (SSD/HDD) grouped into **RAID groups** and assembled into **aggregates** — the pools from
which volumes are carved. NetApp's default RAID is **RAID-DP** (double-parity: survives two disk
failures per RAID group); very large SSD RAID groups can use **RAID-TEC** (triple-parity). Everything
ONTAP does is written through **WAFL** (the Write Anywhere File Layout) onto those aggregates. Cluster
features are enabled by **licenses** (increasingly delivered as a single **NetApp License File**). This
chapter teaches the foundation — cluster, licensing, aggregates, and RAID resiliency — with hands-on
ONTAP walkthroughs.

## Design Considerations

Size **aggregates** for the workload and keep enough spare disks for RAID reconstruction. Choose
**RAID-DP** for general use and **RAID-TEC** for large-capacity SSD RAID groups where a triple-failure
window matters. Keep **HA pairs** balanced so a takeover does not overload the surviving node. Apply the
correct **license** entitlements before enabling a feature (SnapMirror, FabricPool, and so on).

## Implementation and Automation

The labs inspect the cluster and HA state, list licensed features, create an aggregate from spare disks,
and read the RAID layout — the physical grounding the NCDA and every path build on.

## Validation and Troubleshooting

Confirm the storage foundation:

```text
Cluster: nodes -> HA pairs (partner takeover) -> cluster network
Disks -> RAID groups (RAID-DP double parity / RAID-TEC triple) -> aggregates -> (volumes)
WAFL writes everything; licenses (NetApp License File) enable features
```

Common pitfalls: building an aggregate with no spare disks (no room to reconstruct after a failure); and
enabling a feature before its **license** is installed.

## Security and Best Practices

Reserve adequate **RAID spares**, keep **HA** healthy so failover is non-disruptive, and install only
the **licenses** you are entitled to. Protect the cluster-management LIF. All work is authorized
administration of your own cluster.

## Hands-On Lab

Storage-foundation walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster (`admin@cluster1`)
with spare disks, and `python3`. **Cost:** none.

### Lab 2.1 — Inspect nodes and HA pairs

**Objective:** Read the cluster and HA topology.

```text
cluster1::> storage failover show
                              Takeover
Node           Partner        Possible State Description
-------------- -------------- -------- -------------------------------------
cluster1-01    cluster1-02    true     Connected to cluster1-02
cluster1-02    cluster1-01    true     Connected to cluster1-02
2 entries were displayed.
```

**Expected result:** each node paired with its partner and `Takeover Possible true` — a healthy HA pair.

**Negative test:** find `Takeover Possible false`; HA is degraded and an upgrade or reboot would be
disruptive — resolve interconnect or version mismatches first.

**Rollback:** none (read-only).

### Lab 2.2 — List feature licenses

**Objective:** Confirm which features are entitled.

```text
cluster1::> system license show -package SnapMirror
Package           Type        Description           Expiration
----------------- ----------- --------------------- ----------
SnapMirror        license     SnapMirror            -

cluster1::> system license show-status
Status      License          Scope       Detailed Status
----------- ---------------- ----------- ------------------
valid       SnapMirror       cluster     -
```

**Expected result:** the SnapMirror feature shown as a `valid` cluster-scoped license.

**Negative test:** try to create a SnapMirror relationship with the license absent; ONTAP refuses —
install the NetApp License File first.

**Rollback:** none (read-only).

### Lab 2.3 — Create an aggregate

**Objective:** Assemble spare disks into a storage pool.

```text
cluster1::> storage aggregate create -aggregate aggr1_data -node cluster1-01 -diskcount 5
[Job 51] Job succeeded: DONE

cluster1::> storage aggregate show -aggregate aggr1_data -fields size,raidtype,state
aggregate  size    raidtype  state
---------- ------- --------- ------
aggr1_data 3.60TB  raid_dp   online
```

**Expected result:** an online aggregate `aggr1_data` protected by `raid_dp`.

**Negative test:** request more disks than are spare (`-diskcount 99`); the job fails for lack of
disks — add shelves or lower the count.

**Rollback:**

```text
cluster1::> storage aggregate delete -aggregate aggr1_data
```

### Lab 2.4 — Read the RAID layout

**Objective:** Confirm double-parity protection.

```text
cluster1::> storage aggregate show-status -aggregate aggr1_data
Owner Node: cluster1-01
 Aggregate: aggr1_data (online, raid_dp)
  Plex: /aggr1_data/plex0 (online, normal, active)
   RAID Group /aggr1_data/plex0/rg0 (normal, block checksums)
     Position Disk        Type    Usable Size
     -------- ----------- ------- -----------
     dparity  1.0.0       SSD        900GB
     parity   1.0.1       SSD        900GB
     data     1.0.2       SSD        900GB
     data     1.0.3       SSD        900GB
     data     1.0.4       SSD        900GB
```

**Expected result:** a `raid_dp` RAID group with `dparity` and `parity` disks — survives two disk
failures.

**Negative test:** plan a single-parity layout for a large SSD aggregate; a second failure during
rebuild loses data — use **RAID-DP** (or **RAID-TEC** for very large SSD groups).

**Rollback:** none (the aggregate was removed in Lab 2.3 cleanup).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Technology Solutions foundation is the ONTAP cluster (nodes, HA pairs, cluster network), feature
licensing, aggregates built from RAID groups, and RAID-DP/RAID-TEC resiliency written through WAFL — the
physical grounding every NetApp path assumes.

- [ ] I can explain the cluster and HA model.
- [ ] I can list and reason about feature licenses.
- [ ] I can create an aggregate and read its RAID layout.
- [ ] I completed Labs 2.1–2.4 including each negative test.
