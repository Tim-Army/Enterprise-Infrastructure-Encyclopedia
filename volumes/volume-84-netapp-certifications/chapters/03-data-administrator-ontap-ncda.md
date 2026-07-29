# Chapter 03: Data Administrator ONTAP (NCDA)

## Learning Objectives

- Create and manage a storage virtual machine (SVM/vserver).
- Provision FlexVol volumes and reason about FlexGroup.
- Apply storage efficiency (deduplication, compression, compaction).
- Manage qtrees and quotas.
- Complete a walkthrough for each NCDA core-administration topic.

## Theory and Architecture

The **Data Administrator ONTAP (NCDA, exam NS0-163)** is NetApp's flagship credential and the anchor of
almost every path. Its blueprint spans eight domains — Storage Platforms, Core ONTAP, ONTAP Storage,
Networking, Storage Protocols and Connectivity, Data Protection, Security, and Performance. This chapter
takes the **Core ONTAP** and **ONTAP Storage** heart of it. ONTAP is **multi-tenant**: each tenant is a
**storage virtual machine (SVM**, historically **vserver)** with its own volumes, LIFs, and namespace.
Inside an SVM you provision **FlexVol** volumes (thin-provisioned, resizable containers carved from an
aggregate) — or a **FlexGroup** (a single namespace spread across many constituents for massive scale).
ONTAP's **storage efficiency** — inline and background **deduplication**, **compression**, and
**compaction** — reduces the physical footprint of every volume. **Qtrees** partition a volume, and
**quotas** cap usage per qtree, user, or group. This chapter teaches the NCDA core with hands-on ONTAP
walkthroughs on an SVM.

## Design Considerations

Give each tenant or workload its own **SVM** for isolation and delegated administration. Use **FlexVol**
for general workloads and **FlexGroup** where a single huge namespace with even distribution is needed.
Leave **storage efficiency** on (it is default on AFF) — it is nearly free on SSD. Use **qtrees +
quotas** to keep one project from consuming a shared volume. Thin-provision, but monitor aggregate
fullness.

## Implementation and Automation

The labs create an SVM, provision a FlexVol, enable and verify storage efficiency, and set a qtree quota
— the day-to-day administration the NCDA validates.

## Validation and Troubleshooting

Confirm the NCDA core:

```text
SVM (vserver) = tenant: own volumes + LIFs + namespace
FlexVol = thin, resizable volume from an aggregate; FlexGroup = one namespace across constituents
Efficiency: dedup + compression + compaction (default on AFF) shrink the footprint
qtree partitions a volume; quota caps usage (qtree/user/group)
```

Common pitfalls: provisioning volumes in the wrong **SVM** (breaks tenant isolation); and forgetting
that **quotas** must be **resized/reinitialized** to take effect.

## Security and Best Practices

Isolate tenants with **SVMs**, cap consumption with **quotas**, and keep **efficiency** on to save
capacity. Delegate SVM administration with scoped roles rather than sharing the cluster admin. All work
is authorized administration.

## Hands-On Lab

NCDA core walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster with an aggregate
(`aggr1_data`), and `python3`. **Cost:** none.

### Lab 3.1 — Create a storage virtual machine

**Objective:** Provision a tenant SVM.

```text
cluster1::> vserver create -vserver svm_app -aggregate aggr1_data -rootvolume-security-style unix
[Job 61] Job succeeded: Vserver creation completed.

cluster1::> vserver show -vserver svm_app -fields state,allowed-protocols
vserver  state   allowed-protocols
-------- ------- -----------------------
svm_app  running nfs,cifs,fcp,iscsi,nvme,s3
```

**Expected result:** a running SVM `svm_app` — an isolated tenant namespace.

**Negative test:** provision application volumes directly in the cluster admin SVM; that breaks tenant
isolation — create a data SVM instead.

**Cleanup:**

```text
cluster1::> vserver delete -vserver svm_app
```

### Lab 3.2 — Provision a FlexVol volume

**Objective:** Carve a thin volume for a workload.

```text
cluster1::> volume create -vserver svm_app -volume vol_finance -aggregate aggr1_data \
  -size 100GB -space-guarantee none -junction-path /finance
[Job 62] Job succeeded: Successful

cluster1::> volume show -vserver svm_app -volume vol_finance -fields size,space-guarantee,junction-path
vserver  volume       size   space-guarantee junction-path
-------- ------------ ------ --------------- -------------
svm_app  vol_finance  100GB  none            /finance
```

**Expected result:** a 100GB thin-provisioned (`space-guarantee none`) volume mounted at `/finance`.

**Negative test:** set `-space-guarantee volume` on every volume in a nearly full aggregate; you exhaust
capacity — thin-provision and monitor instead.

**Cleanup:**

```text
cluster1::> volume unmount -vserver svm_app -volume vol_finance
cluster1::> volume offline -vserver svm_app -volume vol_finance
cluster1::> volume delete -vserver svm_app -volume vol_finance
```

### Lab 3.3 — Enable and verify storage efficiency

**Objective:** Reduce the physical footprint.

```text
cluster1::> volume efficiency on -vserver svm_app -volume vol_finance
Efficiency for volume "vol_finance" of Vserver "svm_app" is enabled.

cluster1::> volume efficiency show -vserver svm_app -volume vol_finance \
  -fields state,compression,inline-compression,inline-dedupe
vserver  volume       state    compression inline-compression inline-dedupe
-------- ------------ -------- ----------- ------------------ -------------
svm_app  vol_finance  Enabled  true        true               true
```

**Expected result:** efficiency **enabled** with inline compression and dedup — a smaller footprint.

**Negative test:** disable efficiency on an all-flash volume to "save CPU"; on AFF it is nearly free and
you lose large savings — leave it on.

**Cleanup:** none (removed with the volume in Lab 3.2).

### Lab 3.4 — Set a qtree quota

**Objective:** Cap usage within a volume.

```text
cluster1::> volume qtree create -vserver svm_app -volume vol_finance -qtree reports
cluster1::> quota policy rule create -vserver svm_app -policy-name default -volume vol_finance \
  -type tree -target reports -disk-limit 20GB
cluster1::> quota on -vserver svm_app -volume vol_finance
[Job 63] Job succeeded: Quota resize successful.

cluster1::> quota report -vserver svm_app -volume vol_finance
Vserver  Volume     Tree    Type  Disk-Used Disk-Limit
-------- ---------- ------- ----- --------- ----------
svm_app  vol_finance reports tree      0B      20GB
```

**Expected result:** the `reports` qtree capped at a 20GB disk limit.

**Negative test:** add a quota rule but skip `quota on`/resize; the limit never applies — enable and
resize quotas after any rule change.

**Cleanup:**

```text
cluster1::> quota off -vserver svm_app -volume vol_finance
cluster1::> volume qtree delete -vserver svm_app -volume vol_finance -qtree reports -force
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCDA core is ONTAP's multi-tenant administration: storage virtual machines for isolation, FlexVol
(and FlexGroup) volumes carved from aggregates, storage efficiency (dedup/compression/compaction) to
shrink the footprint, and qtrees with quotas to cap consumption.

- [ ] I can create and manage an SVM.
- [ ] I can provision a FlexVol and reason about FlexGroup.
- [ ] I can enable and verify storage efficiency.
- [ ] I can set a qtree quota.
- [ ] I completed Labs 3.1–3.4 including each negative test.
