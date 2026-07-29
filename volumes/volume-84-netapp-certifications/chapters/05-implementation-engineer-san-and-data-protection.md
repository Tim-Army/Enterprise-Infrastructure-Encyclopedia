# Chapter 05: Implementation Engineer — SAN, Data Protection, MetroCluster

## Learning Objectives

- Create a Snapshot and restore from it.
- Build a SnapMirror (DR) relationship and reason about SnapVault (backup).
- Protect a whole tenant with SVM-DR.
- Explain MetroCluster synchronous continuous availability.
- Complete a walkthrough for each Implementation Engineer specialist topic.

## Theory and Architecture

The **Certified Specialist** implementation credentials build on the NCDA. **Implementation Engineer —
Data Protection (NCIE-DP, exam NS0-528)** and **Implementation Engineer — SAN, ONTAP (NCIE-SAN, exam
NS0-521)** were both refreshed in April 2026. Data protection in ONTAP starts with **Snapshots** —
instant, space-efficient, read-only point-in-time images of a volume (WAFL makes them nearly free).
**SnapMirror** replicates Snapshots to another cluster for **disaster recovery** (an asynchronous or
synchronous mirror you can fail over to). **SnapVault** (a SnapMirror policy of type `vault`) keeps a
longer retention of Snapshots on a secondary for **backup**. **SVM-DR** mirrors an entire storage
virtual machine — its volumes and configuration — for tenant-level DR. For zero-RPO continuous
availability across two sites, **MetroCluster** synchronously mirrors between clusters with automatic
switchover. On the SAN side, the Implementation Engineer provisions **LUNs**, **igroups**, selective LUN
mapping, and multipathing. This chapter teaches the specialist topics with hands-on ONTAP walkthroughs.

## Design Considerations

Set a **Snapshot policy** matching the workload's RPO. Use **SnapMirror** (async or Sync) for DR to a
second site and **SnapVault** for long-retention backup. Use **SVM-DR** to fail over a whole tenant at
once. Reserve **MetroCluster** for the strict zero-RPO, automatic-switchover requirement. On SAN, plan
multipathing and selective LUN mapping so each host sees only its LUNs.

## Implementation and Automation

The labs take a Snapshot and restore, build a SnapMirror relationship and initialize it, and reason
about SnapVault retention and MetroCluster — the protection an NCIE implements.

## Validation and Troubleshooting

Confirm the protection model:

```text
Snapshot = instant read-only PIT image (near-free on WAFL); restore in place
SnapMirror (async/sync) = DR mirror to another cluster; failover target
SnapVault (vault policy) = long-retention backup on a secondary
SVM-DR = mirror a whole tenant; MetroCluster = synchronous zero-RPO, auto switchover
```

Common pitfalls: a SnapMirror relationship that is created but never **initialized** (no baseline
transferred); and relying on Snapshots alone for DR (they live on the same cluster) — mirror them off-box.

## Security and Best Practices

Keep DR copies on a **separate cluster/site**, protect the SnapMirror intercluster LIFs, and treat
secondary/vault copies as recovery sources you can trust. Immutable retention (SnapLock) is covered in
Chapter 09. All work is authorized protection of your own data.

## Hands-On Lab

Data-protection walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster with SVM `svm_app` and
volume `vol_finance`; a second SVM/cluster peer for SnapMirror (or a second SVM in the same cluster for
the lab). **Cost:** none.

### Lab 5.1 — Create and restore a Snapshot

**Objective:** Take a point-in-time image and roll back.

```text
cluster1::> volume snapshot create -vserver svm_app -volume vol_finance -snapshot before_change
cluster1::> volume snapshot show -vserver svm_app -volume vol_finance
Vserver  Volume       Snapshot        Size   Total%  Used%
-------- ------------ --------------- ------ ------- -----
svm_app  vol_finance  before_change   132KB     0%     0%

cluster1::> volume snapshot restore -vserver svm_app -volume vol_finance -snapshot before_change
Warning: promote the specified Snapshot copy? {y|n}: y
```

**Expected result:** a Snapshot created, then the volume restored to it — instant recovery.

**Negative test:** delete a volume that has only local Snapshots and expect to recover from them; local
Snapshots die with the volume — mirror off-box for DR.

**Cleanup:**

```text
cluster1::> volume snapshot delete -vserver svm_app -volume vol_finance -snapshot before_change
```

### Lab 5.2 — Build a SnapMirror DR relationship

**Objective:** Mirror a volume to a DR destination.

```text
cluster1::> volume create -vserver svm_dr -volume vol_finance_dr -aggregate aggr1_data -type DP
cluster1::> snapmirror create -source-path svm_app:vol_finance \
  -destination-path svm_dr:vol_finance_dr -policy MirrorAllSnapshots
cluster1::> snapmirror initialize -destination-path svm_dr:vol_finance_dr
[Job 71] Job succeeded: SnapMirror Initialize Succeeded

cluster1::> snapmirror show -destination-path svm_dr:vol_finance_dr -fields state,status,healthy
source-path        destination-path      state        status healthy
------------------ --------------------- ------------ ------ -------
svm_app:vol_finance svm_dr:vol_finance_dr Snapmirrored Idle   true
```

**Expected result:** a healthy `Snapmirrored/Idle` relationship — a DR copy you can fail over to.

**Negative test:** create the relationship but skip `snapmirror initialize`; the destination has no
baseline and cannot serve data — always initialize.

**Cleanup:**

```text
cluster1::> snapmirror delete -destination-path svm_dr:vol_finance_dr
cluster1::> volume delete -vserver svm_dr -volume vol_finance_dr
```

### Lab 5.3 — Reason about SnapVault retention

**Objective:** Separate DR from long-retention backup.

```python
python3 - <<'PY'
policies = {
  "MirrorAllSnapshots": "DR mirror (identical to source; failover target)",
  "XDPDefault (vault)":  "backup: keep daily x30, weekly x12 on secondary",
  "MirrorAndVault":      "unified: DR mirror + long retention",
}
for name, use in policies.items():
    print(f"{name:22}: {use}")
print("Rule: SnapMirror = DR (short, failover); SnapVault = backup (long retention)")
PY
```

**Expected result:** each policy matched to DR versus backup — the right relationship for each need.

**Negative test:** use a short DR mirror as your only backup; you cannot recover last month's file —
add a **vault** policy with long retention.

**Cleanup:** none.

### Lab 5.4 — Explain MetroCluster continuous availability

**Objective:** Reason about zero-RPO synchronous protection.

```python
python3 - <<'PY'
options = {
  "SnapMirror Async":  "RPO minutes-hours; manual/scripted failover",
  "SnapMirror Sync":   "RPO ~zero for volumes; manual failover",
  "MetroCluster":      "RPO zero, RTO seconds; automatic switchover across two sites",
}
for k, v in options.items():
    print(f"{k:18}: {v}")
print("Rule: strict zero-RPO + automatic switchover -> MetroCluster")
PY
```

**Expected result:** the protection tiers ranked by RPO/RTO with MetroCluster as the zero-RPO option.

**Negative test:** promise a zero-RPO SLA with nightly SnapVault only; a mid-day outage loses hours —
use MetroCluster (or SnapMirror Sync) for that SLA.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Implementation Engineer specialties build on the NCDA: Snapshots for instant local recovery,
SnapMirror for DR mirrors you fail over to, SnapVault for long-retention backup, SVM-DR for tenant-level
protection, and MetroCluster for synchronous zero-RPO continuous availability — plus SAN LUN and igroup
provisioning.

- [ ] I can create and restore a Snapshot.
- [ ] I can build and initialize a SnapMirror relationship.
- [ ] I can distinguish SnapMirror DR from SnapVault backup.
- [ ] I can explain MetroCluster zero-RPO protection.
- [ ] I completed Labs 5.1–5.4 including each negative test.
