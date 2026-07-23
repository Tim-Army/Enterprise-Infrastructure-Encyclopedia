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

Simulator/paper-lab (these platforms rarely offer free virtual
editions): write the full runbook for one scenario per platform —
PowerMax: SG + Diamond SLO + SRDF/A pair with a failover/failback
narrative; PowerScale: three-node join, access zone, SMB share,
SyncIQ policy; ECS: replication group + S3 bucket with object lock —
each with exact commands, expected outputs, and rollback steps,
validated line-by-line against the official guides.

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
