# Chapter 01: The Proven Professional Program and Storage Foundations

## Learning Objectives

- Map Dell's certification framework: portfolios, the
  function-based exam naming (Foundations, Operate, Deploy, Design,
  Install, Maintain), and the D-code format
- Explain modern data center building blocks through the ISM lens:
  storage architectures, RAID, SAN/NAS/object, and cloud models
- Choose an entry certification — ISM Foundations (D-ISM-FN-01), Cloud
  Infrastructure and Services Foundations (D-CIS-FN-01), or a
  portfolio Foundations exam — by role
- Read any Dell exam code on sight and locate its authority page

## Theory and Architecture

### The program in one sentence

Dell Technologies certifications are organized by **portfolio**
(servers, storage platforms, data protection, networking, HCI/cloud,
AI, security, client) and **function** — the exam code says both:
`D-<product>-<function>-<version>`, where the function is FN
(Foundations), OE (Operate), DY (Deploy), DS (Design), IN (Install),
or MN (Maintain), and `-A-` marks an achievement-style credential.
Seventy-seven exams were live when this volume's tables were verified
against Dell Learning's certification pages on **22 July 2026** — the
README carries the complete grouped list; each exam's authority page
is its entry at Dell Learning's certification catalog.

### ISM: the vendor's vendor-neutral spine

**Information Storage and Management Foundations (D-ISM-FN-01)** is the
program's conceptual backbone: intelligent storage systems, RAID and
erasure coding, FC SAN / IP SAN / NAS / object protocols, replication
and archive, and software-defined storage — taught platform-neutrally
before any Power-branded product applies them. Pair it with **CIS
Foundations (D-CIS-FN-01)** where the role leans cloud: service
models, orchestration, and the consumption economics APEX later
productizes.

### Functions define depth, not products

Operate exams certify administration of a running platform; Deploy
adds installation and integration; Design tests sizing and
architecture; Install/Maintain certify field service. The same product
ladder repeats across the portfolio, so mastering one platform's
ladder teaches you to read every other track in the program.

## Design Considerations

- Enter through the Foundations exam nearest your role, not the most
  famous product; the OE exam of the platform you actually run is the
  correct second step
- Dell exams are delivered by Pearson VUE; training lives on Dell
  Learning (subscription Learning Hub, ILT, and on-demand) — plan
  budget accordingly, and mine the free exam-description documents
  hard: they carry the objectives and weights
- This encyclopedia's Volumes XXII (OpenManage), XXIII (iDRAC), and
  XXVI (the R640 lab) are the hands-on companions to this track

## Implementation and Automation

```text
# Reading a D-code, worked examples from the verified table
D-PST-OE-23   -> PowerStore, Operate, 2023 series
D-PDD-DY-01   -> PowerProtect Data Domain, Deploy, -01 series
D-PSC-MN-01   -> PowerScale, Maintain, -01 series
D-AX-RH-A-00  -> APEX Cloud Platform for Red Hat OpenShift, achievement
D-ISM-FN-01   -> Information Storage and Management, Foundations
```

Lab base for the whole volume: the Volume XXVI R640/Proxmox estate
hosts the simulators and virtual editions used throughout — Dell's
hands-on story is appliance-centric, so labs emphasize the management
planes (OME, iDRAC) and virtual/community editions where they exist.

## Validation and Troubleshooting

- Verify any code before study or booking: Dell Learning's
  certification catalog is the authority; the -23 to -01 to -A-00
  series rolls are frequent and silent
- The exam description PDF for each exam lists objectives, weights,
  and recommended training — treat it the way Cisco volumes treat
  exam-topics pages
- CertTracker/Credly records the earned badge; employers verify there

## Security and Best Practices

- Buy exams and courseware only through Dell Learning and Pearson VUE;
  the braindump economy is an integrity trap
- Keep one primary study identity: Dell Learning account, Pearson
  profile, and badge wallet aligned to the same email

## References and Knowledge Checks

- Dell Learning certification overview and available-exams catalog —
  the primary source for every code in this volume
- ISM participant guide (Dell's flagship storage text)

Knowledge checks:

1. Decode D-PCR-DY-01 and D-XTR-MN-A-24 completely.
2. Which two Foundations exams anchor the program, and which roles
   choose each?
3. Where do objectives and weights for a Dell exam live, and why does
   this volume not restate them?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each topic area of the
Information Storage and Management Foundations (D-ISM-FN-01) exam** — the storage
baseline of the Dell Proven Professional program — mapped in the volume README's
coverage tables. Labs use representative Dell storage CLIs and host tools to make
each concept concrete. Each ends **`**Lab verified by:** *pending*`** until a human
runs it.

**Shared prerequisites for Labs 1.1–1.10** — a Dell storage array (PowerStore/Unity
or a simulator), a Linux host with `multipath`, `iscsiadm`, and FC tooling, and
management access. **Cost:** none beyond lab resources.

### Lab 1.1 — Intelligent storage system architecture (Topic: Storage Systems)

**Objective:** Read the block/file/object personalities an array presents.

```text
show storage-arrays
show volumes
show file-systems
```

**Expected result:** the array with block volumes, file systems, and (where
present) object buckets — a modern intelligent storage system serves **block**
(LUNs/volumes over FC/iSCSI/NVMe), **file** (NAS: SMB/NFS), and **object** (S3) from
a controller pair over a pooled back end, the foundation ISM defines.

**Negative test:** expect file access from a block-only volume; a raw LUN has no
file system until a host (or the array's NAS) formats/exports it — the personality
determines the access method.

**Cleanup:** none (read-only).

### Lab 1.2 — RAID and data protection (Topic: Storage Systems — RAID)

**Objective:** Read the RAID/protection level of a pool.

```text
show pools
show disk-groups
show drives
```

**Expected result:** the pool's RAID type (e.g., dynamic/distributed RAID 5/6) and
its drives — RAID protects against drive failure by striping with parity (RAID 5/6)
or mirroring (RAID 1/10); distributed/dynamic RAID spreads spare capacity for faster
rebuilds, the modern default.

**Negative test:** size a RAID 5 pool of large drives and assess rebuild exposure; a
second failure during a long rebuild loses data — RAID 6 (dual parity) or
distributed sparing addresses the rebuild-window risk.

**Cleanup:** none (read-only).

### Lab 1.3 — Provisioning: thin volumes (Topic: Storage Systems — Provisioning)

**Objective:** Create a thin volume and read its allocation.

```text
create volume name LAB-VOL size 100GB pool Pool0 thin-provisioned true
show volumes name LAB-VOL detail
show pools name Pool0 | match "subscribed|used|free"
```

**Expected result:** a 100 GB volume consuming near-zero until written — **thin
provisioning** allocates capacity on write, so the pool can be over-subscribed;
monitoring `subscribed` vs `used` is essential to avoid an out-of-space condition.

**Negative test:** over-subscribe a pool and fill the thin volumes; when physical
`used` reaches capacity, writes fail array-wide — thin provisioning requires
capacity monitoring and alerts.

**Cleanup:** `delete volume LAB-VOL`.

### Lab 1.4 — Fibre Channel SAN (Topic: Storage Networking — FC SAN)

**Objective:** Verify FC host connectivity (zoning, WWPN login).

```bash
systool -c fc_host -v | grep -E "port_name|port_state"
multipath -ll | head
```

```text
show host-initiators
```

**Expected result:** the host WWPNs logged in and multipathed to the array — an FC
SAN connects hosts to storage over a dedicated lossless fabric; **zoning** (by WWPN)
controls which initiators see which targets, and multipathing gives redundancy
across two fabrics (A/B).

**Negative test:** a host whose WWPN is not zoned to the array sees no LUNs even
though the cable is up — zoning, not link state, admits the initiator.

**Cleanup:** none (read-only).

### Lab 1.5 — IP SAN and NVMe over Fabrics (Topic: Storage Networking — IP SAN)

**Objective:** Discover and log in to an iSCSI (or NVMe-oF) target.

```bash
iscsiadm -m discovery -t st -p 10.0.0.60:3260
iscsiadm -m node -T iqn.dell:lab-target -l
nvme discover -t tcp -a 10.0.0.61 -s 4420 2>/dev/null | head
```

**Expected result:** the iSCSI target discovered and logged in (and NVMe/TCP
subsystems listed) — **IP SAN** carries block storage over Ethernet: iSCSI over
TCP/3260, and **NVMe-oF** (TCP/RoCE) for lower latency, the modern high-performance
IP block transport.

**Negative test:** discover an iSCSI portal with no LUN masked to the initiator's
IQN; login succeeds but no block device appears — host-to-LUN masking is required.

**Cleanup:** `iscsiadm -m node -T iqn.dell:lab-target -u`.

### Lab 1.6 — NAS and file storage (Topic: Storage Networking — NAS)

**Objective:** Mount an SMB and an NFS export.

```bash
showmount -e 10.0.0.62
mount -t nfs 10.0.0.62:/lab_share /mnt/nfs
smbclient -L //10.0.0.62 -U labuser 2>/dev/null | head
```

**Expected result:** the NFS export mounted and SMB shares listed — **NAS** serves
files over NFS (Unix) and SMB (Windows) from the array's file personality, with the
storage handling the file system, permissions, and protocol.

**Negative test:** mount an NFS export not permitted for the client's IP; the mount
is refused — export access rules (host/subnet) gate NAS access.

**Cleanup:** `umount /mnt/nfs`.

### Lab 1.7 — Object and cloud storage (Topic: Storage Systems — Object)

**Objective:** Create an S3 bucket and put an object.

```bash
aws --endpoint-url https://10.0.0.63:9021 s3 mb s3://lab-bucket
aws --endpoint-url https://10.0.0.63:9021 s3 cp /etc/hostname s3://lab-bucket/
aws --endpoint-url https://10.0.0.63:9021 s3 ls s3://lab-bucket/
```

**Expected result:** the bucket created and the object stored/listed — **object
storage** (Dell ECS) stores data as objects with metadata in a flat namespace,
accessed by S3/Swift APIs over HTTP, scaling to billions of objects for
cloud/archive workloads.

**Negative test:** PUT to a bucket without the right IAM/bucket policy; the API
returns `AccessDenied` — object access is governed by keys and policies, not host
mounts.

**Cleanup:** `aws --endpoint-url ... s3 rb s3://lab-bucket --force`.

### Lab 1.8 — Backup, archive, and deduplication (Topic: Business Continuity — Backup)

**Objective:** Read a backup target's deduplication efficiency.

```text
show mtree list
show compression daily detail
show filesys space
```

**Expected result:** the backup MTrees and the dedup/compression ratio — business
continuity's **backup/archive** protects against data loss; **deduplication** (as on
Dell PowerProtect Data Domain) stores only unique segments, so the effective:used
ratio is often 10–50×, making disk-based backup and replication economical.

**Negative test:** back up already-encrypted or pre-compressed data to a dedup
appliance; the dedup ratio collapses toward 1× — dedup works on redundancy, which
encryption/compression removes.

**Cleanup:** none (read-only).

### Lab 1.9 — Replication: local and remote (Topic: Business Continuity — Replication)

**Objective:** Read a snapshot (local) and a remote replication session.

```text
create snapshot volume LAB-VOL name LAB-SNAP
show snapshots volume LAB-VOL
show replication-sessions
```

**Expected result:** the local snapshot and any remote replication session with its
RPO — **local replication** (snapshots/clones) enables fast local recovery and
test/dev; **remote replication** (synchronous for zero RPO, asynchronous for
distance) protects against site loss, the core of a DR strategy.

**Negative test:** rely on synchronous replication over a high-latency long-distance
link; application write latency spikes — synchronous suits metro distance; async (or
Dell's active/active metro) suits longer distance.

**Cleanup:** `delete snapshot LAB-SNAP`.

### Lab 1.10 — Storage security and management (Topic: Security and Management)

**Objective:** Read the array's security posture and management/monitoring.

```text
show security-settings
show encryption
show alerts list
show performance-metrics summary
```

**Expected result:** RBAC, data-at-rest encryption, alerts, and performance metrics
— storage security spans access control (RBAC, secure management), **data-at-rest
encryption** (self-encrypting drives/controller), and audit; management/monitoring
(CloudIQ, alerts, capacity/performance trending) keeps the infrastructure healthy.

**Negative test:** leave data-at-rest encryption disabled on drives that leave the
data center for RMA; the data is readable off-array — encryption protects retired/
stolen media, which access control alone does not.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the plan's every exam code matched the live
catalog on the stated date, each ladder step has its description
document archived, and the role-to-entry-exam choice is defended in
two sentences.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] D-code grammar internalized (portfolio x function x series)
- [ ] ISM/CIS foundations positioned and chosen by role
- [ ] Exam-description documents located for one full ladder
- [ ] Program map produced with same-day code verification
