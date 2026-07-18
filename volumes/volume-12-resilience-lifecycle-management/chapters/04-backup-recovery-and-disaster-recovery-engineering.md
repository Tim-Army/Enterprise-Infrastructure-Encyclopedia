# Chapter 4: Backup, Recovery, and Disaster-Recovery Engineering

## Learning Objectives

- Distinguish backup types (full, incremental, differential, synthetic full) and select a scheme from a change-rate and recovery-time budget.
- Apply the 3-2-1-1-0 backup rule and justify each of its five elements against a real ransomware or site-loss scenario.
- Design a DR site strategy (pilot light, warm standby, hot site) from the RTO/RPO values established in Chapter 2 and the replication trade-offs from Chapter 3.
- Calculate backup window, replication bandwidth, and retention storage requirements from a stated change rate and retention policy.
- Build an automated, verified backup job and a corresponding restore procedure, not just a backup job alone.
- Explain why immutable, air-gapped backup copies are a required control against ransomware rather than an optional hardening step.

## Theory and Architecture

### Backup Is Not Disaster Recovery

Backup and disaster recovery are related but distinct: a backup is a point-in-time copy of data that supports recovery; disaster recovery (DR) is the complete capability — infrastructure, data, network, and procedure — to restore a service after a major disruption. A service can have excellent backups and still fail its DR objective if there is nowhere to restore them to within the RTO, or if nobody has verified the restore procedure actually works. This chapter treats backup engineering (Chapter 2's RPO made concrete) and DR engineering (Chapter 2's RTO made concrete, building on Chapter 3's replication and HA patterns) as two halves of the same recovery capability, connected by the requirement that both be tested, not merely built.

### Backup Types

| Type | Description | Restore Complexity | Storage Cost |
| --- | --- | --- | --- |
| Full | Complete copy of the protected data set | Lowest — single artifact to restore | Highest |
| Incremental | Only data changed since the last backup of any type | Highest — requires the last full plus every incremental since | Lowest |
| Differential | Only data changed since the last full backup | Moderate — requires the last full plus one differential | Moderate |
| Synthetic full | A new "full" constructed from a prior full plus incrementals, without re-reading the source data set | Same as full at restore time | Moderate, with reduced backup-window impact |

Incremental backups minimize backup-window duration and storage but maximize restore complexity and the number of artifacts that must all be intact for a successful restore — a single missing or corrupt incremental in the chain can break the entire restore. Synthetic full backups address this by periodically consolidating a full-plus-incrementals chain into a new full artifact on the backup target itself, without re-reading the (often much larger, and busier) production source system, combining the backup-window benefit of incrementals with the restore simplicity of a full.

### The 3-2-1-1-0 Rule

The classic 3-2-1 backup rule has been extended in most modern practice to 3-2-1-1-0, and each element defends against a specific failure mode:

- **3** copies of data (the production copy plus at least two backups).
- **2** different media or storage types (for example, disk-based backup storage and object storage, not two volumes on the same array).
- **1** copy off-site, protecting against a site-level event (fire, flood, regional outage) that a same-site backup does not survive.
- **1** copy offline or immutable, protecting specifically against ransomware and destructive insider or attacker actions that a purely online, mutable backup cannot survive — an attacker with write access to production frequently also has write (and delete) access to a backup target that is merely another mounted volume.
- **0** errors on backup verification — a backup that has not been verified to restore correctly is a hypothesis, not a control, echoing the same "declared redundancy is a hypothesis until tested" principle from Chapter 1.

The "1 immutable" element is the most commonly missing in practice, and its absence is the single most common reason an organization with "backups" still pays a ransom or loses data permanently: if every backup copy is reachable and writable from the same credential set as production, a sufficiently privileged compromise (or a sufficiently privileged mistake) can destroy backups and production together.

### DR Site Strategies

Chapter 2 introduced the RTO-to-strategy mapping at a business-planning level; this chapter details the infrastructure architecture behind each row:

- **Cold site** — infrastructure is provisioned only when a disaster is declared, and data is restored from backup. Lowest ongoing cost, longest RTO (hours to days), and the strategy most exposed to "the restore has never actually been tested" risk because nothing runs continuously.
- **Pilot light** — a minimal core (typically the data tier, kept continuously replicated) runs at the DR location at all times; compute and supporting services are provisioned and scaled up only during a declared disaster. Moderate cost, RTO typically measured in tens of minutes to a few hours — dominated by how long it takes to scale up compute and validate the environment.
- **Warm standby** — a scaled-down but fully functional copy of the production environment runs continuously at the DR location, ready to be scaled up to full capacity on failover. Higher ongoing cost than pilot light, RTO typically minutes.
- **Hot site / active-active** — the DR location runs at full production capacity continuously and serves live traffic (or is one keystroke from doing so), identical to the active-active pattern from Chapter 3 applied at the site or region level. Highest cost, RTO approaching zero.

The DR site tier chosen must match the RTO derived from the BIA in Chapter 2; over-provisioning (a hot site for a Tier 3 process) wastes budget that could harden a genuinely Tier 0 service, and under-provisioning (a cold site for a Tier 0 process) makes the stated RTO structurally impossible to meet regardless of procedural discipline.

### Replication Mechanisms for Data Recovery

Beneath any DR strategy above pilot light sits a data replication mechanism, distinct from (but related to) the synchronous/asynchronous HA replication covered in Chapter 3:

- **Storage-array or volume snapshots** — point-in-time, space-efficient copies at the block or volume layer; fast to create and restore but typically tied to the source array unless shipped elsewhere, and are not a substitute for an independent backup copy since a snapshot commonly shares the underlying storage fault domain with its source.
- **Log shipping** — a database's write-ahead or transaction log is continuously shipped to a standby, which replays it to stay current; recovery point is bounded by the shipping and replay lag, typically seconds to low minutes.
- **Change data capture (CDC)** — a stream of row-level changes is captured (often from the same transaction log) and delivered to downstream consumers, used both for DR replicas and for feeding analytics or search systems from the same change stream.
- **Application-level dual-write or event replay** — the application itself writes to two locations or replays an event log to reconstruct state; higher engineering cost but useful when the data store itself has no native cross-site replication.

## Design Considerations

### Retention Policy and the Grandfather-Father-Son Model

Retention policy balances recovery flexibility (being able to go back further in time) against storage cost, and is typically expressed with a tiered rotation scheme:

| Tier | Frequency | Typical Retention |
| --- | --- | --- |
| Son (daily) | Daily incremental or differential | 7–14 days |
| Father (weekly) | Weekly full or synthetic full | 4–5 weeks |
| Grandfather (monthly) | Monthly full | 12–13 months |
| Yearly | Annual full | 3–7 years, driven by regulatory retention requirements |

Retention requirements are frequently set by regulation or contract, not operational preference — financial, healthcare, and government workloads in particular often carry multi-year mandatory retention that has nothing to do with the RPO used for operational recovery. Treat regulatory retention and operational-recovery retention as two separate, potentially conflicting requirements, and size storage for the longer of the two rather than assuming operational RPO drives the entire retention schedule.

### Backup Window and Change-Rate Math

A backup job must complete within an available backup window, and the achievable window is a function of data volume, change rate, and available throughput:

```text
Full backup duration (hours) = Data Volume (GB) / Effective Throughput (GB/hr)

Example:
  Data volume:          8,000 GB
  Effective throughput: 500 GB/hr (constrained by source I/O, not just network)
  Full backup duration: 8,000 / 500 = 16 hours

If the backup window is only 8 hours, a nightly full backup does not fit.
Options: switch to incremental/differential with a less frequent full,
increase throughput (parallel streams, faster backup target), or extend
the window (accept backup I/O contention with production during business
hours, if the workload tolerates it).
```

Incremental backup duration scales with the change rate rather than total data volume, which is why a large, slowly changing data set is usually a good incremental candidate, while a smaller but rapidly changing data set (a busy transactional database) may not shrink the backup-window problem nearly as much as its raw size suggests.

### Replication Bandwidth for DR

Continuous replication to a DR site (log shipping, CDC, or storage replication) requires sustained bandwidth at least equal to the peak sustained change rate, with headroom for catch-up after any transient link interruption:

```text
Required bandwidth (Mbps) = (Peak change rate GB/hr x 8,000) / 3,600 x safety_factor

Example:
  Peak change rate: 45 GB/hr
  Safety factor:    1.5 (headroom for catch-up and peak variance)
  Required bandwidth = (45 x 8,000) / 3,600 x 1.5 = 150 Mbps (approx.)
```

Undersized replication links do not fail cleanly — they fall progressively further behind under peak load, silently expanding RPO beyond the design target until a failover event exposes the gap. Replication lag must be monitored continuously against the RPO budget, exactly as Chapter 3 specifies for synchronous/asynchronous HA replication.

### Data Residency and Cross-Region Replication

Replicating data to a DR site in another jurisdiction can create data residency or export-control obligations independent of the technical design. This is a design input, not an afterthought: the acceptable set of DR site locations must be filtered by legal and compliance constraints before an RTO/RPO-optimal location is selected, and this filtering should happen during the BIA/DR-strategy selection stage in Chapter 2's process, not after a DR site is already built.

## Implementation and Automation

### Backup Policy as Code

```yaml
# backup-policy.yaml
- dataset_id: orders-database
  tier: 0
  schedule:
    full: "weekly, Sunday 01:00"
    incremental: "daily, 01:00"
    log_shipping: "continuous"
  retention:
    daily: 14
    weekly: 5
    monthly: 13
  immutability:
    enabled: true
    lock_days: 35
  offsite_copy: true
  verification:
    restore_test_cadence: "monthly"
    checksum_on_write: true
  rpo_minutes: 5
```

Storing backup policy as structured, version-controlled data — following the same pattern as the criticality register in Chapter 1 — allows automated compliance checks: every Tier 0/1 dataset must have an entry, every entry's `rpo_minutes` must be consistent with the value declared in the corresponding BIA record from Chapter 2, and every entry must show a `restore_test_cadence` no less frequent than the tier requires.

### Example: Verified Backup Script

```bash
#!/usr/bin/env bash
# run-backup.sh: perform a backup, verify its integrity, and record
# the result — a backup job that does not verify is not a control.
set -euo pipefail

SOURCE_DIR="$1"
BACKUP_TARGET="$2"
MANIFEST="${BACKUP_TARGET}/manifest-$(date +%Y%m%dT%H%M%S).sha256"

echo "Starting backup of ${SOURCE_DIR}..."
tar -czf "${BACKUP_TARGET}/backup-$(date +%Y%m%dT%H%M%S).tar.gz" -C "${SOURCE_DIR}" .

echo "Generating checksums for verification..."
find "${BACKUP_TARGET}" -name "*.tar.gz" -newer "${MANIFEST%.*}" -exec sha256sum {} \; > "${MANIFEST}" || true
sha256sum "${BACKUP_TARGET}"/backup-*.tar.gz > "${MANIFEST}"

echo "Verifying archive integrity..."
LATEST=$(ls -t "${BACKUP_TARGET}"/backup-*.tar.gz | head -1)
if ! tar -tzf "${LATEST}" > /dev/null 2>&1; then
  echo "FAIL: archive ${LATEST} failed integrity check" >&2
  exit 1
fi

echo "PASS: backup created and verified: ${LATEST}"
```

The integrity check (`tar -tzf`) is the difference between a backup script and a verified backup script: writing an archive and confirming it is readable back are separate failure modes, and a truncated or corrupted archive that was never test-read can sit undetected until the moment it is needed for a real restore.

### Example: Restore Procedure as a Tested Artifact

```bash
#!/usr/bin/env bash
# restore-verify.sh: restore the most recent backup to an isolated
# scratch location and validate content, never directly over production.
set -euo pipefail

BACKUP_TARGET="$1"
RESTORE_SCRATCH="$2"

LATEST=$(ls -t "${BACKUP_TARGET}"/backup-*.tar.gz | head -1)
mkdir -p "${RESTORE_SCRATCH}"

echo "Restoring ${LATEST} to scratch location ${RESTORE_SCRATCH}..."
tar -xzf "${LATEST}" -C "${RESTORE_SCRATCH}"

RESTORED_FILE_COUNT=$(find "${RESTORE_SCRATCH}" -type f | wc -l)
if [ "${RESTORED_FILE_COUNT}" -eq 0 ]; then
  echo "FAIL: restore produced zero files" >&2
  exit 1
fi

echo "PASS: restore produced ${RESTORED_FILE_COUNT} files at ${RESTORE_SCRATCH}"
```

Restoring to an isolated scratch location, rather than directly overwriting a live target, is deliberate: a restore test that could itself cause an outage is not a safe validation step, and the DR runbook (below) is the place where a controlled, authorized production restore or failover is actually exercised.

### DR Failover Runbook Skeleton

```markdown
# DR Runbook: <service-id>

## Declaration Authority
- Who may declare a disaster and invoke this runbook.

## Pre-Failover Checks
1. Confirm replication lag is within RPO budget (query monitoring; abort if not, and use last-known-good checkpoint instead).
2. Confirm DR-site capacity matches the required scale-up target.

## Failover Steps
1. Numbered, specific technical steps (promote replica, redirect DNS/traffic, scale up compute).

## Validation Steps
1. Smoke-test critical transactions at the DR site before declaring recovery complete.

## Failback Steps
1. Numbered steps to return to the primary site once it is restored, including re-establishing replication in reverse before cutting back.

## Test History
| Date | Test Type (tabletop/parallel/full) | RTO Achieved | Follow-up Actions |
```

Keep this runbook in the same version-controlled repository as the backup policy, the criticality register, and the BIA records, so an RTO or RPO change in the BIA is reviewed alongside the runbook and infrastructure that must change to keep them consistent — the same traceability principle established in Chapter 2.

## Validation and Troubleshooting

### Validating Backup and DR Design

- Confirm at least one backup copy is genuinely immutable or offline — verify this by attempting (in a controlled test, with appropriate authorization) to delete or modify a backup using production credentials; if it succeeds, the "1" in 3-2-1-1-0 is not actually satisfied.
- Confirm restore tests are executed on the cadence declared in the backup policy, and that results are recorded, not just attempted.
- Confirm DR runbooks have been executed as at least a parallel test (bringing up the DR environment without cutting over production traffic) within the last review cycle for every Tier 0/1 service.

### Common Failure Modes

| Symptom | Likely Cause |
| --- | --- |
| Restore fails despite "successful" backup job logs | Backup job verified only that the job completed, not that the artifact restores; missing integrity check |
| Backup completes but RPO is silently missed | Backup schedule frequency does not match the declared RPO, or a backup job has been silently failing and alerting was not tied to job success/failure |
| Ransomware encrypts backups along with production | No immutable/offline copy; backup target reachable with the same compromised credentials as production |
| DR failover works in test but fails during a real event | Test used synthetic, low-volume data; production-scale data volume or concurrency was never exercised |
| Restore takes far longer than RTO allows | Backup type (full incremental chain) was optimized for backup window, not restore speed, without checking the restore-time consequence |

### Troubleshooting a Failed Restore Test

When a restore test fails, resist the instinct to simply re-run it — a failed restore test is valuable signal about a real gap. Work backward through the chain: confirm the backup artifact's checksum first (was it corrupted at write time, or corrupted at rest), then confirm the restore procedure itself (was a step missing or a tool version mismatched), then confirm the target environment (was there sufficient capacity or a missing dependency at the DR location). Document the root cause and the corrective action in the runbook's test history — a restore test that fails and is silently retried without a recorded root cause will fail the same way again under real pressure.

## Security and Best Practices

- Isolate backup system credentials from production identity entirely; a backup service account should not be a member of the same privileged group as production administrators, precisely so that a production compromise does not automatically grant an attacker access to delete backups.
- Encrypt backups both in transit and at rest, with key management independent of the backup target itself — an attacker who obtains both the encrypted backup and its key from the same compromised system has gained nothing from the encryption.
- Enforce immutability with a genuine technical control (write-once storage, retention locks that even administrative accounts cannot shorten) rather than a policy statement; a "policy" of not deleting backups does not survive a credential compromise or an insider threat.
- Test the negative case regularly: attempt to delete or tamper with a backup using normal operational credentials as part of a scheduled security control test, and confirm it fails, rather than assuming immutability configuration is correct because it was configured once.
- Treat backup and DR documentation with the same sensitivity as the criticality register and BIA from earlier chapters — it is a roadmap of exactly what an attacker would need to know to maximize damage or to know which systems are, or are not, well protected.

## References and Knowledge Checks

### References

- [Chapter 2](02-business-impact-analysis-and-continuity-planning.md) for the RTO/RPO values and DR strategy mapping this chapter implements.
- [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md) for the synchronous/asynchronous replication trade-offs that underpin DR data replication.
- NIST SP 800-34 Rev. 1, *Contingency Planning Guide for Federal Information Systems*.
- NIST SP 800-209, *Security Guidelines for Storage Infrastructure*, for immutable and write-once storage guidance.
- Volume VI, Enterprise Storage and Data Protection, for storage-layer snapshot and replication mechanics referenced here at a vendor-neutral level.

### Knowledge Checks

1. Explain each element of the 3-2-1-1-0 rule and name the specific failure mode each element defends against.
2. A Tier 0 service has an RPO of 5 minutes but its backup schedule only takes a nightly full backup. Identify the gap and correct the design.
3. Given an 8,000 GB dataset, 500 GB/hr effective throughput, and a 6-hour backup window, is a nightly full backup feasible? What alternative would you propose?
4. Why is a storage-array snapshot not, by itself, a substitute for an independent backup copy?
5. Explain why restoring to an isolated scratch location rather than production is the correct default for routine restore testing.

## Hands-On Lab

### Lab: Verified Backup, Restore Testing, and Corruption Detection

**Objective:** Build a backup job that verifies its own output, perform a restore test to an isolated location, and confirm the verification step correctly detects a corrupted backup.

**Prerequisites:**

- `bash`, `tar`, `sha256sum` (or `shasum -a 256` on macOS).
- A workstation with at least 50 MB of free scratch space.

**Procedure:**

1. Create a working directory with sample data to protect:

   ```bash
   mkdir -p ~/labs/resilience-ch4/source ~/labs/resilience-ch4/backups ~/labs/resilience-ch4/restore
   cd ~/labs/resilience-ch4
   for i in $(seq 1 20); do echo "sample record $i" > "source/record-$i.txt"; done
   ```

2. Save the `run-backup.sh` script from this chapter and run it:

   ```bash
   bash run-backup.sh source backups
   ```

   **Expected Result:** Output ends with `PASS: backup created and verified`, and `backups/` contains a `.tar.gz` archive and a `.sha256` manifest.

3. Save the `restore-verify.sh` script from this chapter and run it:

   ```bash
   bash restore-verify.sh backups restore
   ```

   **Expected Result:** Output ends with `PASS: restore produced 20 files`, and `restore/` contains the 20 sample record files, matching the source.

4. Confirm restored content matches source content:

   ```bash
   diff -r source restore && echo "Restored content matches source"
   ```

**Negative Test:** Deliberately corrupt the backup archive and confirm the integrity check catches it:

```bash
LATEST=$(ls -t backups/backup-*.tar.gz | head -1)
echo "corruption" >> "$LATEST"
bash -c 'set -e; tar -tzf "'"$LATEST"'" > /dev/null' || echo "Corruption correctly detected — integrity check failed as expected"
```

Confirm the corrupted archive fails the `tar -tzf` integrity check rather than silently appearing to succeed — this is the specific failure mode the verification step exists to catch before a real restore is attempted against it.

**Cleanup:**

```bash
cd ~ && rm -rf ~/labs/resilience-ch4
```

No shared or production systems were modified; all artifacts were local to the working directory.

## Summary and Completion Checklist

Backup engineering turns Chapter 2's RPO into a concrete schedule, retention policy, and immutability control; DR engineering turns its RTO into a site strategy, replication mechanism, and tested failover runbook. Neither is complete as a design on paper — the 3-2-1-1-0 rule's final "0" (zero verification errors) and this chapter's emphasis on restore testing exist because an unverified backup or an untested DR runbook is a liability disguised as a control. Chapter 5 extends this testing discipline from scheduled restore drills into a broader resilience-testing and chaos-engineering practice that exercises far more than the recovery path alone.

**Completion checklist:**

- [ ] Can select a backup type (full/incremental/differential/synthetic full) from a stated change rate and backup-window budget.
- [ ] Can apply all five elements of the 3-2-1-1-0 rule to a given scenario and name the failure mode each defends against.
- [ ] Can map an RTO to a DR site strategy (cold, pilot light, warm standby, hot site) and justify the choice.
- [ ] Calculated backup window and replication bandwidth requirements from stated data volume and change rate.
- [ ] Built and ran a backup job that verifies its own output, and a restore test to an isolated location.
- [ ] Demonstrated that a corrupted backup is correctly detected by the verification step before it would be relied upon for a real restore.
