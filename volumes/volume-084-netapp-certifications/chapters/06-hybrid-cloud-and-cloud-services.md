# Chapter 06: Hybrid Cloud and Cloud Services

## Learning Objectives

- Tier cold data to object storage with FabricPool.
- Reason about StorageGRID object storage and buckets.
- Replicate on-premises data to the cloud (SnapMirror to Cloud Volumes ONTAP).
- Place the Hybrid Cloud Administrator, Implementation Engineer, and Architect in the ladder.
- Complete a walkthrough for each hybrid-cloud topic.

## Theory and Architecture

The **Hybrid Cloud** path runs from **Hybrid Cloud Administrator (Professional, exam NS0-304)** and
**StorageGRID Administration (Professional)** through **Hybrid Cloud Implementation Engineer
(Specialist)** to **Hybrid Cloud Architect (Expert, exam NS0-604)**; the parallel **Cloud Services**
path adds **Cloud and Storage Services Engineer (Professional)**. The technology that ties on-premises
ONTAP to the cloud is the **data fabric**: **FabricPool** automatically tiers cold blocks from an SSD
aggregate to an **object store** (StorageGRID, Amazon S3, Azure Blob, Google Cloud Storage) while hot
data stays on flash; **StorageGRID** is NetApp's own S3-compatible object platform for petabyte-scale,
geo-distributed object storage; and **SnapMirror** replicates volumes to **Cloud Volumes ONTAP (CVO)** —
ONTAP running in a hyperscaler — for cloud DR, bursting, and migration. **BlueXP** is the unified
control plane. This chapter teaches the hybrid-cloud building blocks with hands-on ONTAP walkthroughs.

## Design Considerations

Use **FabricPool** to shrink the flash footprint by tiering cold data to object — set the **tiering
policy** (`auto`, `snapshot-only`, `none`) per volume. Choose **StorageGRID** for on-prem/sovereign
object storage and a hyperscaler bucket for cloud-native tiering. Replicate to **CVO** for cloud DR or
migration. Design the **Architect** view: capacity, cost, data locality, and egress. Watch cloud
**egress** costs when reading tiered data back.

## Implementation and Automation

The labs attach an object store to an aggregate, set a volume tiering policy, and reason about
StorageGRID and SnapMirror-to-cloud — the hybrid data fabric the path validates.

## Validation and Troubleshooting

Confirm the fabric:

```text
FabricPool: hot blocks on SSD, cold blocks tiered to object (policy auto/snapshot-only/none)
StorageGRID: NetApp S3-compatible object platform (petabyte, geo-distributed)
SnapMirror -> Cloud Volumes ONTAP (CVO): cloud DR / burst / migrate; BlueXP control plane
Ladder: Hybrid Cloud Admin (NS0-304) -> Impl Engineer -> Architect (NS0-604)
```

Common pitfalls: tiering **hot** data (a too-aggressive policy) so reads pull back from object with
latency and egress cost; and forgetting that FabricPool tiers **cold blocks**, not whole files.

## Security and Best Practices

Encrypt data at rest on both tiers, scope object-store credentials, and keep cloud DR copies in a
separate account/region. Mind **egress** and data-sovereignty requirements. All work is authorized
administration of your own data across sites.

## Hands-On Lab

Hybrid-cloud walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster with `aggr1_data` and SVM
`svm_app`; an object-store endpoint (StorageGRID or a lab S3), and `python3`. **Cost:** none (uses lab
object storage).

### Lab 6.1 — Attach an object store for FabricPool

**Objective:** Register a capacity tier.

```text
cluster1::> storage aggregate object-store config create -object-store-name sg_bucket \
  -provider-type SGWS -server 192.168.20.10 -container-name fabricpool -access-key AKIALAB \
  -secret-password ******** -is-ssl-enabled true
cluster1::> storage aggregate object-store attach -aggregate aggr1_data -object-store-name sg_bucket

cluster1::> storage aggregate object-store show -fields aggregate,object-store-name,tier-type
aggregate  object-store-name tier-type
---------- ----------------- ---------
aggr1_data sg_bucket         object_store
```

**Expected result:** the object store attached to the aggregate — a FabricPool capacity tier is ready.

**Negative test:** attach an object store whose access key lacks write permission; tiering fails —
grant the bucket read/write to the FabricPool credential.

**Rollback:** none in the simulator (detach requires all cold data returned first).

### Lab 6.2 — Set a volume tiering policy

**Objective:** Tier only cold data.

```text
cluster1::> volume modify -vserver svm_app -volume vol_finance -tiering-policy auto
cluster1::> volume show -vserver svm_app -volume vol_finance -fields tiering-policy,tiering-minimum-cooling-days
vserver  volume       tiering-policy tiering-minimum-cooling-days
-------- ------------ -------------- ----------------------------
svm_app  vol_finance  auto           31
```

**Expected result:** the volume set to `auto` tiering with a 31-day cooling window — cold blocks tier,
hot blocks stay on SSD.

**Negative test:** set `-tiering-policy all` on a hot database volume; every block tiers to object and
reads become slow and costly — use `auto` or `snapshot-only`.

**Rollback:**

```text
cluster1::> volume modify -vserver svm_app -volume vol_finance -tiering-policy none
```

### Lab 6.3 — Reason about StorageGRID buckets

**Objective:** Map object needs to StorageGRID.

```python
python3 - <<'PY'
use_cases = {
  "FabricPool capacity tier": "cold ONTAP blocks -> StorageGRID bucket",
  "Backup target (SnapMirror to object)": "immutable object backup of volumes",
  "S3 data lake / apps":      "native S3 apps, ILM policies, geo-distribution",
}
for k, v in use_cases.items():
    print(f"{k:38}: {v}")
print("StorageGRID: NetApp S3 object platform; ILM policy places/protects objects across sites")
PY
```

**Expected result:** each object use case mapped to StorageGRID with its ILM-driven placement.

**Negative test:** store latency-sensitive primary workloads directly on object; object is for
capacity/backup/data-lake — keep primary on ONTAP flash.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Plan SnapMirror to the cloud

**Objective:** Extend DR to a hyperscaler.

```python
python3 - <<'PY'
plan = {
  "Source":      "on-prem svm_app:vol_finance",
  "Destination": "Cloud Volumes ONTAP (CVO) in cloud region",
  "Relationship":"SnapMirror async (MirrorAllSnapshots)",
  "Control":     "BlueXP orchestrates peering + relationship",
  "Use":         "cloud DR / burst / migrate; fail over to CVO",
}
for k, v in plan.items():
    print(f"{k:13}: {v}")
print("Rule: same SnapMirror engine reaches CVO; keep the DR copy in a separate account/region")
PY
```

**Expected result:** a SnapMirror-to-cloud plan targeting CVO via BlueXP — cloud DR for on-prem data.

**Negative test:** replicate to a CVO in the same region/account as production; a regional outage takes
both — target a separate region/account.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Hybrid Cloud and Cloud Services paths tie ONTAP to the cloud through the data fabric: FabricPool
tiers cold blocks to object, StorageGRID provides S3-compatible object storage, and SnapMirror extends
DR to Cloud Volumes ONTAP under the BlueXP control plane — from Hybrid Cloud Administrator (NS0-304) up
to Hybrid Cloud Architect (NS0-604).

- [ ] I can attach an object store and set a tiering policy.
- [ ] I can reason about StorageGRID object use cases.
- [ ] I can plan SnapMirror to Cloud Volumes ONTAP.
- [ ] I completed Labs 6.1–6.4 including each negative test.
