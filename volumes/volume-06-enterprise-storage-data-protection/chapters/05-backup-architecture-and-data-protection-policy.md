# Chapter 5: Backup Architecture and Data Protection Policy

![Lab flow for this chapter: a restic repository is initialized with a password and two source files; the first backup creates one snapshot, and after one file is modified, a second backup adds a second snapshot whose repository growth matches only the changed file's size — direct evidence of block-level deduplication. Restoring the latest snapshot to a separate directory produces a file identical to the current source. As a negative test, listing snapshots with an intentionally wrong repository password fails with a decryption/authentication error rather than returning any data, confirming the repository's encryption actually protects its contents.](../../../diagrams/volume-06-enterprise-storage-data-protection/chapter-05-restic-dedup-encryption-flow.svg)

*Figure 5-1. Flow used throughout this chapter's Hands-On Lab: a restic backup repository proven to deduplicate, restore correctly, and enforce its encryption against a wrong-password negative test.*

## Learning Objectives

- Define Recovery Point Objective (RPO) and Recovery Time Objective (RTO)
  precisely and explain how each drives a different set of architectural
  decisions.
- Apply the 3-2-1 backup rule (and its 3-2-1-1-0 extension) and explain the
  specific failure mode each copy and medium addresses.
- Compare full, incremental, differential, incremental-forever, and
  synthetic-full backup types on backup window, restore complexity, and
  storage consumption.
- Describe backup software architecture: sources (agent-based, agentless,
  snapshot-integrated), proxies/media servers, the catalog, and target
  types.
- Design a retention policy using the Grandfather-Father-Son (GFS) model
  aligned to business and compliance requirements.
- Build and validate a working backup repository with incremental backups,
  a restore test, and an encryption-enforcement negative test.
- Diagnose common backup failure modes: window overrun, catalog drift, and
  target capacity exhaustion.

## Theory and Architecture

Backup architecture is the discipline of guaranteeing that a defined amount
of data loss and a defined amount of downtime are the *worst* outcomes of a
failure, not an open-ended unknown. [Chapter 1](01-enterprise-storage-architecture-and-service-design.md) introduced RPO and RTO by
name in the service catalog; this chapter defines them formally and builds
the architecture that delivers them.

### RPO and RTO, precisely

- **Recovery Point Objective (RPO)** is the maximum acceptable amount of
  data loss, expressed as a duration. An RPO of 4 hours means that after a
  failure, the organization accepts losing up to (but not more than) the
  last 4 hours of writes. RPO is a statement about **backup frequency and
  method** — it is satisfied by how often a recoverable copy of data is
  created, not by how fast that copy can be restored.
- **Recovery Time Objective (RTO)** is the maximum acceptable duration from
  the start of an outage to the restoration of a working service. An RTO of
  2 hours means the business accepts up to 2 hours of downtime, but no
  more. RTO is a statement about **restore speed and process** — it is
  satisfied by how quickly a backup (or a replica, covered in [Chapter 6](06-snapshots-replication-and-continuous-data-protection.md))
  can be brought back into production use.

These are independent numbers. A nightly full backup to tape can deliver an
RPO of 24 hours but an RTO measured in many hours once a large restore and
tape retrieval are counted. A synchronous storage-array replica ([Chapter 6](06-snapshots-replication-and-continuous-data-protection.md))
can deliver a near-zero RPO but still require a lengthy RTO if the failover
process itself is manual and undocumented. Backup architecture and disaster
recovery engineering ([Chapter 7](07-recovery-engineering-and-disaster-recovery-validation.md)) are two different disciplines that both
answer to the same RPO/RTO targets from opposite ends: backup design
minimizes data loss, recovery engineering minimizes downtime.

### The 3-2-1 rule and its extension

The 3-2-1 rule is the baseline architectural pattern for surviving the
largest realistic range of failure modes with the fewest assumptions:

- **3 copies** of data — the production copy plus at least two backups.
  One copy is never a backup; it is a single point of failure with a
  different name.
- **2 different media or platforms** — protects against a media- or
  platform-specific failure mode (a firmware bug, a storage-array-wide
  outage, a single vendor's vulnerability) taking out every copy at once.
- **1 copy offsite** — protects against a site-level event (fire, flood,
  regional outage, physical theft) that a purely local set of copies cannot
  survive regardless of how many local copies exist.

Current practice extends this to **3-2-1-1-0**:

- **1 copy immutable or air-gapped** — a copy that cannot be altered or
  deleted within its retention window, even by a compromised backup
  administrator account, directly addressing ransomware and insider-threat
  scenarios covered in depth in [Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md).
- **0 errors** — every backup is verified restorable, not merely verified
  as "the job completed." A backup that has never been test-restored is an
  unverified assumption, not a data protection control.

### Backup types

| Type | What is captured | Restore complexity | Storage cost | Backup window impact |
| --- | --- | --- | --- | --- |
| Full | Entire dataset, every job | Simple — one restore point, one job | Highest (full copy every run) | Longest per job |
| Incremental | Only data changed since the *last backup of any type* | Complex — requires the last full plus every incremental since | Lowest per job | Shortest per job |
| Differential | Only data changed since the *last full* | Moderate — requires the last full plus one differential | Grows between fulls | Grows between fulls |
| Incremental-forever | One initial full, then indefinite incrementals; the backup software maintains a synthesized current view | Simple from the operator's perspective (software resolves the chain) | Low, ongoing | Consistently short after the initial full |
| Synthetic full | A new "full" restore point built by merging a prior full and subsequent incrementals at the backup target, without re-reading the entire source dataset | Simple, same as a full | Similar to full at the target, but does not re-burden the source or network | No source-side full-backup window after the first |

Traditional full/incremental/differential scheduling (for example, a weekly
full with daily incrementals) trades a longer weekly window and a
multi-step restore chain for simplicity of the day-to-day job. Incremental-
forever and synthetic-full approaches — now the default model in most
modern backup platforms — eliminate the recurring full-backup window
entirely by synthesizing new full restore points from previously
transferred data, which is why they dominate current backup architecture
for any dataset large enough that a recurring full backup would not
otherwise fit in the available window.

### Backup software architecture

A backup platform, regardless of vendor, is built from the same functional
components:

- **Source integration** — how data is read from the protected system.
  **Agent-based** backup runs software on the protected host with
  filesystem- or application-aware knowledge (open-file handling,
  database-consistent capture). **Agentless** backup typically integrates
  at the hypervisor or storage-array layer (for example, reading a
  hypervisor snapshot or an array-side snapshot directly, covered in
  [Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)) without installing software inside the guest. **Application-
  consistent** capture (coordinating with the application or OS quiescing
  mechanism, such as Windows VSS or a database's own hot-backup mode)
  produces a restore point the application can start cleanly from;
  **crash-consistent** capture (a point-in-time copy with no application
  coordination) is faster and simpler but restores to the same state as if
  the system had lost power — acceptable for some workloads, not for
  transactional databases without their own crash-recovery log replay.
- **Backup proxy / media server** — the component that moves data between
  source and target, offloading that work from the protected host itself
  and centralizing target connectivity, deduplication, and encryption.
- **Catalog** — the metadata database recording what was backed up, when,
  where each restore point's data physically lives, and the chain
  dependencies between full/incremental/differential jobs. The catalog is
  itself a critical piece of infrastructure: a backup platform with
  intact backup data but a corrupted or lost catalog can be effectively
  unrestorable, because nothing else records what exists or how to
  reassemble it. The catalog needs its own backup and disaster recovery
  plan, not an implicit assumption that it is always available.
- **Backup target** — disk (often a deduplication-capable backup
  repository), tape (still the standard for very long-term, air-gapped
  retention — see [Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md)), and object/cloud storage ([Chapter 3](03-enterprise-file-and-object-storage.md)),
  increasingly the default target for both on-premises and cloud-native
  workloads due to its built-in durability, lifecycle tiering, and
  immutability features.

### Deduplication and its effect on capacity planning

Backup deduplication eliminates redundant data blocks, either at the
**source** (before transfer, reducing network load) or at the **target**
(after transfer, reducing storage consumption but not network load), and
either **inline** (during ingest) or **post-process** (after a full write,
trading a temporary capacity spike for less impact on backup-window
performance). Deduplication ratios are highly workload-dependent — a set of
full backups of largely static file data can dedup at very high ratios,
while already-compressed or encrypted source data dedups poorly — and
should never be assumed from a vendor's marketed average ratio; measure it
against the organization's actual data before it becomes a capacity-
planning input.

### Backup window and change-rate math

Backup window planning is a direct extension of the throughput vocabulary
from [Chapter 1](01-enterprise-storage-architecture-and-service-design.md):

```text
Required throughput = Data to transfer within the window / Window duration

Example: 8 TB incremental change set, 6-hour overnight window
Required throughput = 8,000 GB / (6 x 3600 s) ≈ 370 MB/s sustained
```

A backup design that cannot sustain 370 MB/s end to end — source read
speed, proxy throughput, network bandwidth, and target ingest speed, all
of them, not just the fastest link — will overrun its window regardless of
how the job is scheduled. Change-rate growth over time is the single most
common cause of a backup architecture that "used to fit" no longer fitting;
re-baseline change rate against window capacity on the same cadence used
for the capacity-monitoring practices in [Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md).

## Design Considerations

- **Tier RPO/RTO to the service catalog from [Chapter 1](01-enterprise-storage-architecture-and-service-design.md).** Not every
  workload needs the same backup frequency; align backup job frequency and
  retention to the tier (Platinum/Gold/Bronze) a workload was provisioned
  against, and treat a request for a tighter RPO than the workload's tier
  provides as a service-catalog change, not a one-off exception.
- **Retention policy design (GFS).** The Grandfather-Father-Son model
  retains daily backups for a short window, weekly backups for a longer
  window, and monthly (or yearly) backups for the longest window, giving
  a small number of restore points that still cover a long retention
  period without retaining every daily backup indefinitely. Retention
  design must also account for legal hold and regulatory retention minimums
  ([Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md)) that can override the operational GFS schedule for specific
  data.
- **Agent vs. agentless trade-offs.** Agent-based backup gives the finest
  application awareness (transaction log truncation, item-level restore)
  at the cost of software to deploy, patch, and license per host.
  Agentless/snapshot-integrated backup scales more easily across large
  virtualized estates but depends on the underlying snapshot mechanism
  ([Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)) and its own consistency guarantees.
- **Bandwidth and window sizing must use worst-case change rate**, not
  average change rate — a backup design sized to the average day fails on
  the day it is needed most (post-patch-cycle, post-batch-job, or during a
  legitimate but unusually large data load).
- **Immutability and air-gapping are architectural decisions made at
  design time**, not features bolted on after an incident; [Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md)
  develops this fully, but the target platform and retention-lock model
  should be chosen during initial backup architecture design, since
  changing target platforms later is disruptive.
- **The catalog's own resiliency** deserves the same design rigor as the
  backup data itself — catalog backup frequency, and ideally a documented,
  tested catalog-rebuild or catalog-restore procedure, belong in the
  design from day one.

## Implementation and Automation

### Expressing backup policy as data

Following the same pattern as the service catalog in [Chapter 1](01-enterprise-storage-architecture-and-service-design.md), express
backup policy as a version-controlled artifact so intent and actual job
configuration cannot silently drift apart:

```yaml
# backup-policy.yaml
policies:
  - name: platinum-database
    service_tier: platinum
    rpo_minutes: 15
    rto_hours: 1
    method: application_consistent
    schedule:
      type: incremental_forever
      frequency: continuous_snapshot_plus_hourly_log_backup
    retention:
      daily: 14
      weekly: 8
      monthly: 12
      yearly: 0
    copies:
      - target: primary_disk_repository
        immutable: false
      - target: object_storage_secondary_site
        immutable: true
        retention_lock_days: 30
  - name: bronze-fileshare
    service_tier: bronze
    rpo_minutes: 1440
    rto_hours: 24
    method: crash_consistent
    schedule:
      type: synthetic_full
      frequency: daily
    retention:
      daily: 7
      weekly: 4
      monthly: 6
      yearly: 1
    copies:
      - target: primary_disk_repository
        immutable: false
      - target: tape_offsite
        immutable: true
        retention_lock_days: 365
```

This file is the reference a technical-review or audit checks actual job
configuration against, and the input an automation pipeline ([Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md))
uses to provision new backup jobs consistently as new workloads are
onboarded.

### Building a backup repository with `restic`

`restic` is a vendor-neutral, open-source backup tool that implements
source-side deduplication, encryption, and snapshot/retention management
against a variety of repository targets (local disk, SFTP, and S3-
compatible object storage among others), making it a practical way to
demonstrate real backup mechanics without dedicated backup-server
infrastructure.

```bash
# Install
sudo dnf install -y restic     # or: apt-get install -y restic

# Initialize a repository (a local disk target for this example)
export RESTIC_REPOSITORY=/srv/backup-repo
export RESTIC_PASSWORD='ChangeThisRepositoryPassword!'
restic init

# Run a backup
restic backup /srv/protected-data --tag daily

# List snapshots (restore points) in the repository
restic snapshots

# Apply a GFS-style retention policy and remove data no longer covered
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
```

Each `restic backup` run is effectively incremental-forever: only new or
changed data blocks are transferred and stored, while every snapshot still
presents a complete, independently restorable view of the source directory
— the operational simplicity of a full backup with the storage and window
efficiency of an incremental.

### Restoring and verifying

```bash
# Restore the latest snapshot to a separate directory
restic restore latest --target /srv/restore-test

# Verify repository integrity (data and metadata consistency)
restic check
```

## Validation and Troubleshooting

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Backup job consistently exceeds its window | Change rate growth outpacing bandwidth/throughput capacity | Re-baseline change rate against the window math above; consider synthetic-full or incremental-forever if not already in use |
| Catalog shows a job as successful but restore fails | Catalog/target drift (target data deleted or corrupted outside the backup platform's awareness) | Run the platform's catalog-consistency or verification job; compare catalog entries against actual target contents |
| Deduplication ratio far below expected | Source data already compressed/encrypted before backup, or dedup running post-source-encryption | Confirm where encryption is applied in the pipeline; adjust job order (dedup before encrypt) where the platform allows it |
| Backup target reports capacity exhaustion despite recent cleanup | Retention policy not actually pruning, or immutable/retention-locked data not yet eligible for deletion | Verify retention policy execution logs; distinguish "eligible but not yet run" from "misconfigured and never pruning" |
| Restore test produces application that will not start | Crash-consistent backup used for an application requiring application-consistent capture | Confirm the backup method matches the application's consistency requirement; switch to application-consistent capture |
| `restic check` (or equivalent) reports integrity errors | Underlying storage corruption, interrupted write, or unauthorized modification | Isolate the affected snapshot/pack files; restore from an earlier verified snapshot; investigate the underlying storage or access-control cause |

Never treat "job status: success" as proof of a usable backup by itself.
The only real evidence a backup is usable is a completed restore test
against that specific restore point — this is the "0 errors" component of
3-2-1-1-0, and [Chapter 7](07-recovery-engineering-and-disaster-recovery-validation.md) builds the formal recovery-validation practice
this chapter's restore test previews.

## Security and Best Practices

- Encrypt backup data both in transit and at rest; treat the backup
  repository password/key with the same custody discipline as any other
  cryptographic key material ([Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md) develops key management fully).
- Use backup service accounts with the minimum privilege required to read
  source data and write to the target — never reuse a general
  administrative or domain account for backup agent authentication, since
  that account becoming compromised would expose both production systems
  and every backup copy it can reach.
- Isolate backup administration credentials from the general identity
  provider where practical, and require separate, auditable authentication
  for any action that can delete a backup or shorten a retention policy —
  this is the human-process half of ransomware resilience developed fully
  in [Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md).
- Maintain at least one immutable or air-gapped copy per the 3-2-1-1-0
  model; a fully online, fully mutable set of backup copies is vulnerable
  to the same compromise that took down production.
- Log and alert on retention-policy changes, job deletions, and target
  deletions as high-sensitivity administrative actions.
- Schedule and actually execute periodic restore tests against a
  representative sample of protected systems, not only the systems judged
  most critical; an untested tier tends to be exactly the tier whose backup
  quietly stops working first.

## References and Knowledge Checks

**References**

- [SNIA Data Protection and Backup terminology references.](https://www.snia.org/education/dictionary/about-dictionary)
- [NIST SP 800-34 (Contingency Planning Guide), the source of the RPO/RTO
  vocabulary used throughout this volume.](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final)
- [`restic` official documentation (restic.net) for repository, snapshot,
  and retention command reference.](https://restic.readthedocs.io/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated Linux baseline (RHEL 10 / Ubuntu Server
  26.04 LTS) used for this chapter's CLI examples.

**Knowledge Checks**

1. An application has an RPO of 15 minutes and an RTO of 4 hours. Explain,
   in terms of what each objective actually measures, why these two
   numbers require different architectural investments to satisfy.
2. Explain the difference between an incremental backup and a differential
   backup in terms of what a restore actually requires, and why
   incremental-forever architectures have largely displaced the classic
   weekly-full/daily-incremental schedule.
3. Why is "1 copy immutable" a necessary addition to the original 3-2-1
   rule rather than a redundant restatement of "2 different media"?
4. A backup job reports success every night, but a disaster-recovery test
   reveals the restored application will not start. What is the most
   likely root cause given this chapter's distinction between crash-
   consistent and application-consistent backup?
5. Why does the backup catalog require its own resiliency plan, separate
   from the backup data itself?

## Hands-On Lab

### Lab: Build a Deduplicated Backup Repository, Validate Restore, and Confirm Encryption Enforcement

This lab builds a working `restic` backup repository, performs an initial
and incremental backup, validates a full restore, and includes a negative
test proving the repository's encryption is actually enforced rather than
cosmetic.

**Prerequisites**

- A Linux host (RHEL 10 or Ubuntu Server 26.04 LTS baseline) with root or
  sudo access and `restic` installed:

  ```bash
  sudo dnf install -y restic   # or: apt-get install -y restic
  ```

- At least 500 MB of free disk space for the lab's source data and
  repository.

**Procedure**

1. Create a source data directory and initial test files:

   ```bash
   mkdir -p ~/backup-lab/source
   echo "version one" > ~/backup-lab/source/file1.txt
   echo "static data" > ~/backup-lab/source/file2.txt
   ```

2. Initialize a repository and set the required environment variables:

   ```bash
   mkdir -p ~/backup-lab/repo
   export RESTIC_REPOSITORY=~/backup-lab/repo
   export RESTIC_PASSWORD='LabRepoPassword2026!'
   restic init
   ```

3. Run the first backup:

   ```bash
   restic backup ~/backup-lab/source --tag daily
   restic snapshots
   ```

   **Expected result:** one snapshot is listed, with the tag `daily` and a
   timestamp.

4. Modify one file (simulating a day's change) and take a second backup:

   ```bash
   echo "version two - modified" > ~/backup-lab/source/file1.txt
   restic backup ~/backup-lab/source --tag daily
   restic snapshots
   ```

   **Expected result:** two snapshots are now listed. Run
   `restic stats --mode raw-data` to observe that the repository's stored
   size grew by roughly the size of the single changed file, not by a full
   second copy of the source directory — direct evidence of block-level
   deduplication.

5. Restore the latest snapshot to a separate directory and verify content:

   ```bash
   restic restore latest --target ~/backup-lab/restore-test
   RESTORED_FILE=$(find ~/backup-lab/restore-test -name file1.txt)
   diff ~/backup-lab/source/file1.txt "$RESTORED_FILE"
   ```

   **Expected result:** `diff` produces no output, confirming the restored
   file matches the current source exactly. (`restic` restores under the
   source's original absolute path by default, so the restored file lands
   in a nested subdirectory of the target — `find` locates it regardless of
   that path depth.)

**Negative test**

6. Attempt to list snapshots using an incorrect repository password:

   ```bash
   RESTIC_PASSWORD='WrongPassword' restic snapshots
   ```

   **Expected result:** the command fails with a decryption/authentication
   error rather than returning any snapshot data. This confirms the
   repository's encryption is actually protecting the data — anyone who
   obtained a copy of the repository's files without the password cannot
   read the catalog or the backed-up data, satisfying this chapter's
   encryption-at-rest guidance.

7. Confirm normal access still works with the correct password:

   ```bash
   export RESTIC_PASSWORD='LabRepoPassword2026!'
   restic snapshots
   ```

**Cleanup**

8. Remove the lab's repository, source, and restore directories, and unset
   the environment variables:

   ```bash
   unset RESTIC_REPOSITORY RESTIC_PASSWORD
   rm -rf ~/backup-lab
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter formally defined RPO and RTO, established the 3-2-1-1-0
backup architecture pattern, compared backup types and their restore-chain
trade-offs, and walked through backup software architecture — sources,
proxies, the catalog, and targets — along with deduplication and backup-
window capacity math. It then built a real deduplicated, encrypted backup
repository, validated a restore, and proved encryption enforcement with a
wrong-password negative test.

**Completion checklist**

- [ ] Can state the precise definitions of RPO and RTO and explain why they
      require different architectural investments.
- [ ] Can compare full, incremental, differential, incremental-forever, and
      synthetic-full backup types on restore complexity and window impact.
- [ ] Can explain each element of the 3-2-1-1-0 rule and the failure mode
      it addresses.
- [ ] Has built a version-controlled backup policy definition covering at
      least two service tiers.
- [ ] Has built a working deduplicated backup repository with multiple
      snapshots and a validated restore.
- [ ] Has confirmed, via a negative test, that backup repository encryption
      is actually enforced.
