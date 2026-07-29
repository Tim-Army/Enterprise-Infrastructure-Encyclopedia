# Chapter 09: High Availability and Disaster Recovery — Failover Clustering, Hyper-V Replica, and Backup

## Learning Objectives

- Build a failover cluster and explain quorum, witnesses, and dynamic quorum.
- Use Cluster Shared Volumes and clustered roles for highly available services.
- Distinguish high availability from disaster recovery and design for both.
- Configure Hyper-V Replica for cross-site VM recovery.
- Protect and restore data with Windows Server Backup and AD system-state recovery.

## Theory and Architecture

**High availability (HA)** keeps a service running through a component or
node failure; **disaster recovery (DR)** restores service after a site-level
loss. They are different problems: HA is measured in seconds of failover
within a site, DR in a recovery point and recovery time objective (RPO/RTO)
across sites. A resilient design uses both.

**Failover Clustering** provides HA. Two or more nodes present a **clustered
role** (a file server, a SQL instance, a Hyper-V VM) behind a virtual
network name and IP; if the owning node fails, another node brings the role
online. The cluster's integrity depends on **quorum** — a majority of votes
among nodes and an optional **witness** (disk, file share, or **cloud
witness** in Azure) — so the cluster can decide it still has authority and
avoid **split-brain**. **Dynamic quorum** and **dynamic witness** adjust
votes automatically as nodes come and go, keeping the cluster running down
to a last surviving node. **Cluster Shared Volumes (CSV)** let all nodes
access the same NTFS/ReFS volume simultaneously, which is what makes
clustered Hyper-V and Scale-Out File Server work.

**Hyper-V Replica** provides DR for VMs: a primary host asynchronously
replicates a VM's changes to a replica host (typically another site) on a
30-second, 5-minute, or 15-minute interval, keeping recovery points without
shared storage. On a disaster you **fail over** to the replica; a **test
failover** validates recovery non-disruptively. **Storage Replica** provides
block-level volume replication (synchronous for zero-RPO within metro
distance, asynchronous for longer distance).

**Backup** is the last line and the ransomware defense. **Windows Server
Backup** captures volumes, files, and **system state** (which for a DC
includes the AD database, SYSVOL, and registry). Restoring a deleted AD
object authoritatively, or recovering a whole DC, depends on a good system-
state backup. **Azure Backup** extends this off-site with immutable,
isolated recovery points.

## Design Considerations

Match the tool to the objective. For **in-site HA**, cluster the role and
choose a **witness** so an even node count still has a majority — a **cloud
witness** is ideal because it needs no third site. Use **CSV** on **ReFS or
NTFS** with S2D or shared storage for clustered Hyper-V. Size clusters so
the surviving nodes can carry the load after a failure (N+1). For **DR**,
choose **Hyper-V Replica** for VM-level, cross-site recovery with a
tolerable RPO, or **Storage Replica** where you need volume-level or
near-zero RPO. Keep the **replica interval** aligned to the business RPO.

Design **backup** for the 3-2-1 rule (three copies, two media, one off-site)
and make at least one copy **immutable** to survive ransomware. Back up
**system state** on multiple DCs and test **authoritative** and **non-
authoritative** restores before you need them. Document and rehearse the DR
runbook — an untested DR plan is a hope, not a plan.

## Implementation and Automation

Validate and create a cluster, then set a cloud witness:

```powershell
Install-WindowsFeature Failover-Clustering -IncludeManagementTools
Test-Cluster -Node "HV01","HV02"                      # must pass before creating
New-Cluster -Name "CL01" -Node "HV01","HV02" -StaticAddress 10.10.0.30
Set-ClusterQuorum -CloudWitness -AccountName "stgwitness" -AccessKey "<key>"
Add-ClusterSharedVolume -Name "Cluster Disk 1"
```

Enable Hyper-V Replica and replicate a VM:

```powershell
# On the replica host: enable it as a replica server (Kerberos/HTTP 80 or cert/HTTPS 443)
Set-VMReplicationServer -ReplicationEnabled $true -AllowedAuthenticationType Kerberos `
  -ReplicationAllowedFromAnyServer $true -DefaultStorageLocation "E:\Replica"
# On the primary host:
Enable-VMReplication -VMName "APP01" -ReplicaServerName "HV02" -ReplicaServerPort 80 -AuthenticationType Kerberos
Start-VMInitialReplication -VMName "APP01"
```

Back up system state on a domain controller:

```powershell
Install-WindowsFeature Windows-Server-Backup
wbadmin start systemstatebackup -backupTarget:E: -quiet
```

## Validation and Troubleshooting

Confirm cluster, replication, and restore readiness:

```powershell
Get-Cluster | Select-Object Name, QuorumType
Get-ClusterNode | Select-Object Name, State
Get-ClusterQuorum
Get-VMReplication | Select-Object VMName, State, Health, LastReplicationTime
wbadmin get versions
```

Healthy cluster nodes report `Up`; `Get-ClusterQuorum` shows the witness in
use. `Get-VMReplication` health should be `Normal` with a recent
`LastReplicationTime`. Common issues: cluster **validation** warnings
ignored (never run an unsupported cluster in production); **quorum loss**
when an even node count loses the witness (add or fix the witness);
**replication falling behind** because of bandwidth or a large change rate
(check `Measure-VMReplication`); and AD restores failing because the
system-state backup is older than the **tombstone lifetime**, making objects
un-restorable — keep recent backups. For authoritative AD restore, boot the
DC into **DSRM**, restore system state, then mark the object subtree
authoritative with `ntdsutil`.

## Security and Best Practices

Protect the cluster: least-privilege **Cluster Admin** membership, patch
nodes with **Cluster-Aware Updating** so updates roll node-by-node without
downtime, and secure the **witness** (a cloud witness key is a secret).
Encrypt replicated and backup data in transit and at rest — Hyper-V Replica
over **HTTPS with certificates** for cross-organization links, BitLocker on
backup volumes. Keep at least one backup **offline or immutable** so
ransomware cannot encrypt your recovery. Restrict and audit who can perform
restores, and separate the **backup account** from domain admin. Test
failover and restore on a schedule; verify that a **test failover** of a
replicated VM boots and the application works. For DCs, protect
**system-state** backups as Tier 0 assets.

## References and Knowledge Checks

- Microsoft Learn: *Failover Clustering*; *Cluster quorum*; *Cluster Shared Volumes*; *Hyper-V Replica*; *Storage Replica*; *Windows Server Backup*.
- Microsoft Learn: AZ-801 — *Implement and manage high availability; implement disaster recovery*.

**Knowledge checks**

1. What problem does a cluster witness solve, and why is a cloud witness convenient?
2. How do high availability and disaster recovery differ in what they protect against?
3. Why can an AD object be un-restorable, and how does backup frequency prevent it?

## Hands-On Lab

Topic-level walkthroughs for AZ-801's HA and DR skills.

**Shared prerequisites for Labs 9.1–9.4** — two Windows Server 2025 hosts
(`HV01`, `HV02`) in `corp.contoso.lab` for clustering/replica labs, a
storage account for a cloud witness (or a file-share witness), and
Administrator rights. **Cost:** none (a file-share witness avoids any Azure
cost).

### Lab 9.1 — Validate and create a failover cluster (Topic: Build a cluster)

**Objective:** Pass validation and form a two-node cluster.

```powershell
Install-WindowsFeature Failover-Clustering -IncludeManagementTools   # on both nodes
Test-Cluster -Node "HV01","HV02"
New-Cluster -Name "CL01" -Node "HV01","HV02" -StaticAddress 10.10.0.30
Get-ClusterNode | Select-Object Name, State
```

**Expected result:** validation passes and both nodes report `Up` in cluster
`CL01` — a supported cluster must pass `Test-Cluster` first.

**Negative test:** create the cluster while a validation test fails (for
example, inconsistent updates); the cluster is unsupported and may behave
unpredictably — fix validation warnings before proceeding.

**Cleanup:** `Remove-Cluster -Name "CL01" -Force -CleanupAD`.

### Lab 9.2 — Configure a witness for quorum (Topic: Cluster quorum)

**Objective:** Give an even-node cluster a majority.

```powershell
# File-share witness (no cloud cost):
New-Item \\FS01\Witness -ItemType Directory -Force
Set-ClusterQuorum -Cluster CL01 -FileShareWitness "\\FS01\Witness"
Get-ClusterQuorum -Cluster CL01
```

**Expected result:** the quorum configuration lists the file-share witness —
with two nodes plus a witness, losing one node still leaves a majority.

**Negative test:** remove the witness and stop one node; the cluster loses
quorum and shuts the role down to prevent split-brain — an even node count
needs a witness.

**Cleanup:** `Remove-Item \\FS01\Witness -Recurse -Force` after reconfiguring quorum.

### Lab 9.3 — Replicate a VM with Hyper-V Replica (Topic: Disaster recovery)

**Objective:** Establish cross-host VM replication and test failover.

```powershell
Set-VMReplicationServer -ReplicationEnabled $true -AllowedAuthenticationType Kerberos `
  -ReplicationAllowedFromAnyServer $true -DefaultStorageLocation "E:\Replica"   # on HV02
Enable-VMReplication -VMName "APP01" -ReplicaServerName "HV02" -ReplicaServerPort 80 -AuthenticationType Kerberos
Start-VMInitialReplication -VMName "APP01"
Get-VMReplication -VMName "APP01" | Select-Object State, Health, LastReplicationTime
```

**Expected result:** replication reaches `Health : Normal` with a recent
replication time; a **test failover** boots an isolated copy on `HV02` —
Replica gives cross-site recovery without shared storage.

**Negative test:** enable replication without enabling the replica server on
`HV02`; it fails with an authorization error — the replica host must accept
replication first.

**Cleanup:** `Remove-VMReplication -VMName "APP01"`.

### Lab 9.4 — Back up and inspect system state (Topic: Backup and restore)

**Objective:** Capture a DC's system state.

```powershell
Install-WindowsFeature Windows-Server-Backup
wbadmin start systemstatebackup -backupTarget:E: -quiet
wbadmin get versions
```

**Expected result:** a system-state backup completes and appears in
`wbadmin get versions` — for a DC this includes the AD database and SYSVOL,
the basis for authoritative restore.

**Negative test:** attempt an authoritative object restore from a backup
older than the tombstone lifetime; the object cannot be restored — keep
recent system-state backups.

**Cleanup:** remove the lab backup target contents if reclaiming space.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Failover Clustering delivers in-site HA through clustered roles, quorum with
a witness, and Cluster Shared Volumes; Hyper-V Replica and Storage Replica
deliver cross-site DR; and Windows Server Backup with system state is the
foundation for AD and whole-server recovery. HA and DR are distinct
objectives, and both must be designed, secured, and tested.

- [ ] I can build a validated cluster and configure quorum with a witness.
- [ ] I can distinguish HA from DR and pick the right tool.
- [ ] I can replicate a VM with Hyper-V Replica and test failover.
- [ ] I can back up and reason about restoring AD system state.
- [ ] I completed Labs 9.1–9.4 including each negative test.
