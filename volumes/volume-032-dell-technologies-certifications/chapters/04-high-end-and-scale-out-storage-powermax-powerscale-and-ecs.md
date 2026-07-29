# Chapter 04: High-End and Scale-Out Storage — PowerMax, PowerScale, and ECS

## Learning Objectives

- Operate PowerMax at certification depth: SRDF replication families,
  service levels, and the mainframe-adjacent feature set
- Administer PowerScale (OneFS): the single-namespace scale-out model,
  protection levels, and multi-protocol access
- Position ECS object storage and the legacy-but-certified platforms
  (XtremIO, VPLEX, metro node, SRM, DLm)
- Map the ladders: PowerMax OE/DS/IN/MN (D-PVM-OE-01, D-PVM-DS-01,
  D-PM-IN-23, D-PM-MN-23), PowerScale DY/DS/MN (D-PSC-DY-23,
  D-PSC-DS-01, D-PSC-MN-01), ECS OE/DY/DS (D-ECS-OE-23, D-ECS-DY-23,
  D-ECS-DS-23), and the achievement exams for XtremIO, VPLEX, metro
  node, SRM, and DLm

## Theory and Architecture

### Three architectures, one chapter

**PowerMax** is the tier-0 array: end-to-end NVMe, service-level
provisioning, and **SRDF** — the synchronous/asynchronous/Metro
replication family whose topologies (S, A, Metro, STAR-style
composites) are the professional-level differentiator. **PowerScale**
is the opposite shape: OneFS fuses nodes into one filesystem and one
namespace, with per-path protection (N+M erasure) and SMB/NFS/S3/HDFS
on the same data. **ECS** is Dell's object platform: geo-distributed
erasure-coded buckets behind S3-compatible APIs for the archive,
analytics, and backup-target roles.

### The exams follow operations reality

PowerMax Operate lives in storage groups, service levels, SRDF pair
management, and snapshots (SnapVX); Install and Maintain are field
functions; Design is topology and sizing across SRDF and migration.
PowerScale Deploy certifies cluster build and joins, access zones,
authentication providers, and SmartConnect; Design turns node pools,
protection levels, and tiering (SmartPools/CloudPools) into sized
answers; Maintain is field service. ECS's OE/DY/DS split mirrors the
same grammar for object.

### The achievement tier keeps the installed base honest

XtremIO (OE/MN), VPLEX (OE/DY), metro node OE, Storage Resource
Manager, and Disk Library for mainframe carry `-A-` codes: focused
credentials for platforms that still run production estates. Know
what each is; deep study only where your estate demands it.

## Design Considerations

- SRDF/Metro versus VPLEX/metro node: array-native active-active
  against fabric-level federation — choose by platform estate and
  failure-domain doctrine, and draw the witness/quorum before either
- OneFS protection level is per-pool policy, not RAID: +2d:1n-class
  choices trade capacity against rebuild math at node scale
- ECS geo: replication group topology decides both durability and
  read locality; design buckets to the application's consistency
  tolerance
- SRM belongs wherever more than two of these platforms coexist —
  fleet reporting is a design deliverable, not an afterthought

## Implementation and Automation

```text
# PowerMax (Unisphere/CLI mindset the OE exam expects)
symsg -sid 001 create sg-app1; symsg -sg sg-app1 add dev 0A1B
symconfigure -sid 001 -cmd "set sg sg-app1 slo Diamond;" commit
symrdf -sid 001 -sg sg-app1 -rdfg 12 establish   # SRDF pair up
symsnapvx -sid 001 -sg sg-app1 establish -name hourly

# PowerScale (OneFS)
isi status; isi storagepool nodepools list
isi zone zones create zone-app --path /ifs/app
isi smb shares create app --path /ifs/app --zone zone-app
isi sync policies create app-dr sync /ifs/app tgt-cluster /ifs/app
```

## Validation and Troubleshooting

- PowerMax: `symrdf query` states are the truth of DR posture;
  service-level compliance views before performance folklore
- OneFS: `isi status` and events first; protection/rebuild state
  (`isi job status`) before capacity or client complaints;
  SmartConnect resolution tested from clients, not the cluster
- ECS: replication group health and bucket-level metrics; S3 API
  errors read from the client with request IDs
- All three: management-plane telemetry into CloudIQ/SRM — Chapter
  06 of Volume XI's discipline applied to storage fleets

## Security and Best Practices

- Directory-integrated RBAC everywhere; array service accounts
  vaulted; management interfaces off user VLANs
- D@RE on PowerMax/PowerScale verified; ECS object lock where
  compliance or ransomware posture requires WORM
- Replication links are attack surface: authenticate and encrypt
  inter-site traffic per platform capability

## References and Knowledge Checks

- Exam descriptions for the twelve codes in this chapter's map
  (Dell Learning catalog)
- PowerMax SRDF and SnapVX guides; OneFS admin guide; ECS admin guide

Knowledge checks:

1. Contrast SRDF/Metro and VPLEX Metro in one sentence each: where
   does the active-active intelligence live?
2. Why is OneFS protection "per policy" superior to per-array RAID at
   100-node scale?
3. Which questions move from the OE to the DS exam on PowerMax, and
   why does Install exist separately at this tier?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab spanning the **high-end and
scale-out storage exams — PowerMax (D-PVM-*, D-PM-*), PowerScale (D-PSC-*), ECS
(D-ECS-*), XtremIO (D-XTR-*), VPLEX/Metro Node (D-VPX-*, D-MN-OE-23), Storage
Resource Manager (D-SRM-A-01), and DLm (D-DLM-A-01)** — mapped in the volume
README's coverage tables. Labs use Solutions Enabler (`symcli`), PowerScale
`isi`, and the ECS/XtremIO/VPLEX CLIs. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 4.1–4.10** — a PowerMax with Solutions Enabler/
Unisphere, a PowerScale (OneFS) cluster, an ECS system, and management access to the
other platforms. **Cost:** none beyond lab resources.

### Lab 4.1 — PowerMax provisioning (PowerMax Operate)

**Objective:** Create a storage group and provision to a host.

```text
symcfg list
symsg -sid 001 create LAB-SG
symdev -sid 001 create -tdev -cap 100 -captype gb -N 1
symaccess -sid 001 -name LAB-SG -type storage add devs <devid>
symcfg list -sg LAB-SG
```

**Expected result:** the storage group with a thin device — **PowerMax** provisions
through **auto-provisioning groups** (storage/port/initiator groups tied by a masking
view); Solutions Enabler (`sym*`) is the scriptable CLI, with Unisphere for the UI.

**Negative test:** create a masking view missing the initiator group; the host sees
no devices — all three groups plus the masking view are required for access.

**Cleanup:** `symsg -sid 001 delete LAB-SG -force` and delete the device.

### Lab 4.2 — PowerMax SRDF replication (PowerMax Operate)

**Objective:** Read an SRDF (remote replication) pair state.

```text
symrdf -sid 001 -sg LAB-SG query
symrdf list
```

**Expected result:** the SRDF pairs and mode (Synchronous/Asynchronous/Metro) —
**SRDF** replicates PowerMax volumes to a remote array: **SRDF/S** (zero RPO, metro),
**SRDF/A** (async, distance), and **SRDF/Metro** (active/active) underpin
enterprise DR and continuous availability.

**Negative test:** put SRDF/S over a long-distance high-latency link; host write
latency spikes — synchronous mode requires metro distance, async for longer.

**Cleanup:** none (read-only).

### Lab 4.3 — PowerMax TimeFinder SnapVX (PowerMax Operate)

**Objective:** Create a local SnapVX snapshot and link a target.

```text
symsnapvx -sid 001 -sg LAB-SG establish -name LAB-SNAP
symsnapvx -sid 001 -sg LAB-SG list
```

**Expected result:** the SnapVX snapshot established — **TimeFinder SnapVX** takes
space-efficient, redirect-on-write local snapshots (targetless by default, linkable to
host-accessible targets) for backup, test/dev, and instant restore.

**Negative test:** link a SnapVX target smaller than the source; the link fails —
the linked target must match the source device size.

**Cleanup:** `symsnapvx -sid 001 -sg LAB-SG -name LAB-SNAP terminate`.

### Lab 4.4 — PowerScale cluster and SmartPools (PowerScale Deploy)

**Objective:** Read the OneFS cluster and tiering policy.

```text
isi status
isi storagepool nodepools list
isi filepool policy list
```

**Expected result:** the cluster nodes, node pools, and file-pool policies —
**PowerScale (OneFS)** is a scale-out NAS: nodes form a single file system/namespace,
and **SmartPools** tiers data across node pools (all-flash to archive) by policy,
scaling to petabytes.

**Negative test:** a file-pool policy targeting a tier with no capacity leaves data on
the default pool — the target node pool must have space.

**Cleanup:** none (read-only).

### Lab 4.5 — PowerScale SMB/NFS exports (PowerScale Deploy)

**Objective:** Create an SMB share and an NFS export on OneFS.

```text
isi smb shares create --name=LAB --path=/ifs/lab
isi nfs exports create --paths=/ifs/lab
isi smb shares list
isi nfs exports list
```

**Expected result:** the SMB share and NFS export on the same `/ifs` path —
PowerScale serves multiprotocol (SMB, NFS, S3, HDFS) from one namespace with a single
security model, so the same data is accessible to Windows, Unix, and analytics.

**Negative test:** access an SMB share with no permitted user/ACL; access is denied —
the share plus file-system ACLs govern access.

**Cleanup:** `isi smb shares delete LAB` and `isi nfs exports delete <id>`.

### Lab 4.6 — PowerScale SyncIQ replication (PowerScale Maintenance)

**Objective:** Read a SyncIQ replication policy and its state.

```text
isi sync policies list
isi sync jobs list
isi sync reports list | head
```

**Expected result:** the SyncIQ policy and job state — **SyncIQ** replicates OneFS
data to a remote cluster (async, with failover/failback) for DR, at file-system or
directory granularity with configurable RPO.

**Negative test:** a SyncIQ policy whose target directory is not writable/prepared
fails the job — the target cluster must be ready to receive.

**Cleanup:** none (read-only).

### Lab 4.7 — ECS object storage (ECS Deploy)

**Objective:** Create an ECS bucket via S3 and read the namespace.

```bash
aws --endpoint-url https://$ECS:9021 s3 mb s3://lab-ecs-bucket
aws --endpoint-url https://$ECS:9021 s3api put-bucket-versioning --bucket lab-ecs-bucket --versioning-configuration Status=Enabled
aws --endpoint-url https://$ECS:9021 s3 ls
```

**Expected result:** the versioned bucket in the ECS namespace — **ECS** is Dell's
scale-out object platform (S3/Swift/Atmos, plus HDFS/NFS): buckets live in a
namespace/tenant, with versioning, retention, and geo-replication across sites for
active/active object access.

**Negative test:** write to a bucket in a namespace the credential is not entitled to;
ECS returns access-denied — namespace/bucket policy governs access.

**Cleanup:** `aws --endpoint-url ... s3 rb s3://lab-ecs-bucket --force`.

### Lab 4.8 — XtremIO provisioning (XtremIO Operate)

**Objective:** Create an XtremIO volume and read data-reduction.

```text
show-clusters
add-volume vol-name="LAB-VOL" vol-size="100g"
show-volumes
show-data-reduction-ratio
```

**Expected result:** the volume and the array's data-reduction ratio — **XtremIO** is
an all-flash array with always-on inline dedup and compression and instant,
space-efficient snapshots (XVC), tuned for high-IOPS, low-latency workloads like VDI
and databases.

**Negative test:** expect high dedup on unique/encrypted data; XtremIO's ratio drops —
inline dedup depends on data redundancy.

**Cleanup:** `remove-volume vol-name="LAB-VOL"`.

### Lab 4.9 — VPLEX / Metro Node virtual volumes (VPLEX Operate)

**Objective:** Read a distributed virtual volume across two sites.

```text
ll /clusters/*/virtual-volumes
ll /distributed-storage/distributed-devices
cluster status
```

**Expected result:** distributed virtual volumes spanning two clusters — **VPLEX /
Metro Node** virtualizes back-end storage and presents **distributed (active/active)
virtual volumes** across two sites, enabling AccessAnywhere, non-disruptive mobility,
and metro continuous availability.

**Negative test:** a distributed device with a failed inter-cluster (WAN-COM) link
suspends the losing side per the detach rule — the witness/detach policy decides which
site continues.

**Cleanup:** none (read-only).

### Lab 4.10 — Storage Resource Manager reporting (Storage Resource Manager)

**Objective:** Read capacity/performance reporting across the estate.

```bash
curl -sk -u admin:$PW "https://$SRM/rest/v1/report-templates" 2>/dev/null | jq -r '.[]?.name' | head
```

**Expected result:** the SRM report templates — **Storage Resource Manager (SRM)**
gives multi-array, multi-vendor visibility: capacity trending, performance, chargeback,
and topology across PowerMax/PowerStore/PowerScale/VPLEX and third-party arrays, for
planning and compliance.

**Negative test:** expect reporting on an array SRM has not discovered/collected;
it is absent — SRM reports only on collected systems.

**Cleanup:** none (read-only).

## Lab Verification

Verification means each runbook names real commands and objects with
plausible outputs cross-checked to the guides, includes one induced
failure with its signature, and states its rollback; where any real
system was available, its evidence replaces the paper outputs.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] SRDF families and SnapVX articulated with pair-state fluency
- [ ] OneFS scale-out model, zones, and SyncIQ exercised
- [ ] ECS object/geo model positioned with security posture
- [ ] All twelve chapter codes recorded from the verified table
