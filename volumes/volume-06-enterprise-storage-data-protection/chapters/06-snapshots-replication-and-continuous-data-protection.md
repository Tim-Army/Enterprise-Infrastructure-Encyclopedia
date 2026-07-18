# Chapter 6: Snapshots, Replication, and Continuous Data Protection

## Learning Objectives

- Compare copy-on-write and redirect-on-write snapshot mechanisms and
  explain the performance and capacity implications of each.
- Distinguish crash-consistent from application-consistent snapshots and
  explain why consistency groups exist.
- Compare synchronous and asynchronous replication on RPO, latency, and
  distance limitations.
- Describe common replication topologies and the operational trade-offs of
  each.
- Explain continuous data protection (CDP) and how journal-based recovery
  differs from discrete snapshot intervals.
- Create, roll back, and monitor space consumption of a working snapshot,
  including a snapshot-exhaustion negative test.
- Diagnose common snapshot and replication failure modes: space exhaustion,
  replication lag, and split-brain.

## Theory and Architecture

Snapshots and replication are the two mechanisms that turn a single copy of
data into a set of point-in-time or geographically separated copies without
requiring a full, from-scratch backup for every restore point. They are
closely related to backup (Chapter 5) but architecturally distinct: backup
is fundamentally about creating an independent copy on separate media for
long-term retention, while snapshots and replication are primarily about
low-overhead, frequent, storage-native point-in-time and site-to-site data
protection — often used as the *source* a backup job reads from, rather
than a replacement for backup.

### Snapshot mechanisms

| Mechanism | How it works | Write performance impact | Capacity behavior | Common in |
| --- | --- | --- | --- | --- |
| Copy-on-write (COW) | Before the first write to a block after a snapshot is taken, the original block is copied to a reserved snapshot area, then the write proceeds | First write to each block after the snapshot incurs an extra read+write ("COW penalty") | Snapshot consumes space proportional to *changed* blocks since it was taken | Traditional LVM snapshots, many legacy array snapshot implementations |
| Redirect-on-write (ROW) | New writes are always directed to newly allocated blocks; the snapshot simply retains a pointer to the original blocks, and the active volume's metadata is updated to point at the new blocks | No extra I/O penalty on the first write after a snapshot — writes are already "new" writes by design | Snapshot consumes space proportional to changed blocks, same as COW, but without the write-amplification penalty; can increase fragmentation over time | ZFS, most modern all-flash array snapshot implementations, thin-provisioned/log-structured platforms |

Redirect-on-write has become the dominant mechanism on modern platforms
specifically because it avoids the COW penalty, making snapshots
effectively free at creation time and cheap enough in ongoing overhead that
frequent (hourly or more granular) snapshot schedules are practical. A
platform's snapshot mechanism should be understood before committing to a
snapshot frequency in the design phase — a COW-based platform taking
snapshots every few minutes across many volumes can measurably affect write
latency in a way a ROW-based platform will not.

A **snapshot** is a read-only, point-in-time view. A **clone** is a
writable volume derived from a snapshot (or directly from the source), used
when a full read-write copy is needed — test/dev refresh, forensic
investigation of a point in time without touching production, or as a
target for validating a restore (previewed in Chapter 5, formalized in
Chapter 7).

### Consistency: crash-consistent vs. application-consistent

A **crash-consistent** snapshot captures exactly the state a system would
be in if power were cut at that instant — every block as it existed at
that moment, with no coordination from the application or operating
system. This is sufficient for workloads with their own crash-recovery
mechanism (journaling filesystems, databases with write-ahead logs that
replay on startup) but is not, by itself, a guarantee the application will
start cleanly.

An **application-consistent** snapshot coordinates with the application or
OS before the snapshot is taken — flushing in-memory buffers, briefly
quiescing writes, and (on Windows) invoking the Volume Shadow Copy Service
(VSS) writer for the specific application, or (on Linux) using a
filesystem freeze (`fsfreeze`) or a database's native hot-backup/quiesce
mode. The snapshot is taken at a moment the application itself considers
safe to resume from, which is what Chapter 5's application-consistent
backup method actually depends on.

**Consistency groups** extend this guarantee across multiple volumes that
must be captured at the *same* instant — for example, a database's data
volume and its transaction-log volume, or every volume backing a multi-disk
virtual machine. Snapshotting those volumes independently, even
microseconds apart, can produce a set of snapshots that are each internally
consistent but mutually inconsistent with each other (the log references a
transaction the data volume's snapshot does not yet contain, or vice
versa). A consistency group snapshots every member volume atomically as a
single operation specifically to prevent this.

### Replication: synchronous vs. asynchronous

Replication copies writes from a source (primary) volume to a target
(secondary) volume, typically at a different site, to protect against a
site-level failure that no amount of local snapshot retention can survive.

| Mode | Acknowledgment behavior | RPO | Distance/latency sensitivity | Typical use |
| --- | --- | --- | --- | --- |
| Synchronous | Write is acknowledged to the application only after the secondary site confirms it has also committed the write | Zero (or near-zero) — no committed write can be lost | Bound by round-trip latency between sites; typically limited to short/metro distances (commonly under ~100 km, network-dependent) because every write pays the round-trip cost | Tier-1 workloads with a zero-data-loss requirement and sites close enough to absorb the latency |
| Asynchronous | Write is acknowledged locally immediately; the update is transmitted to the secondary site on its own schedule or continuously but without blocking the local write | Non-zero — bounded by the replication interval or by how far behind the continuous stream has fallen under load | Not distance-limited in the same way; works across any WAN distance | Most cross-region and long-distance DR replication |

Synchronous replication's RPO advantage comes at a direct, unavoidable
latency cost on every write, because the application-visible write latency
now includes a full network round trip to the secondary site. This is a
fundamental trade-off, not an engineering shortfall to be tuned away —
which is exactly why it bounds the practical distance for synchronous
replication regardless of link bandwidth.

### Replication topologies

| Topology | Description | Typical use |
| --- | --- | --- |
| 1:1 | One source replicates to one target | Standard active/passive site-to-site DR |
| 1:many (fan-out) | One source replicates to multiple targets | Multiple DR copies, or one DR copy plus one test/dev copy kept current |
| many:1 (fan-in) | Multiple sources replicate into one target, commonly at a consolidated DR or backup site | Remote-office consolidation into a central DR facility |
| Cascading | Source replicates to an intermediate site, which replicates onward to a further site | Extending effective replication distance or reducing load on the primary site |
| Bidirectional / active-active | Both sites accept writes and replicate to each other | Active-active application architectures; requires an explicit conflict-resolution strategy for writes to the same data at both sites |

Bidirectional replication introduces a class of problem the other
topologies do not: **split-brain**, where a network partition allows both
sites to independently accept writes to the same data, producing divergent
copies that cannot be automatically reconciled without a defined conflict-
resolution policy (last-writer-wins, application-level merge, or manual
reconciliation). Any active-active design must decide this policy at
design time, not discover it during an actual partition event.

### Continuous data protection (CDP)

Snapshot-based protection captures state at discrete intervals — every
snapshot is a point-in-time restore point, but anything that happened
*between* two snapshots is unrecoverable except by rolling back to the
earlier one. **Continuous data protection** instead captures a continuous
journal of every write (or a near-continuous stream at very fine
granularity), allowing recovery to *any* point in time within the journal's
retention window, not just the moments a snapshot happened to be taken.
This is particularly valuable against logical corruption and ransomware
(developed fully in Chapter 8): a discrete snapshot schedule might only
offer restore points hours apart, each of which could already contain
corrupted or encrypted data, while a CDP journal can roll back to seconds
before the corrupting event began. The cost is journal storage overhead and
the compute/network cost of continuously shipping every write, which is
why CDP is typically applied selectively to the highest-value tier-1
workloads rather than uniformly across an entire estate.

### Snapshot capacity planning

For a COW or ROW snapshot, reserved capacity must accommodate the *changed*
data over the snapshot's retention period, not the full volume size:

```text
Snapshot space required ≈ change_rate_per_day x retention_days x safety_margin

Example: 50 GB/day change rate, 7-day snapshot retention, 30% safety margin
Snapshot space required ≈ 50 GB x 7 x 1.3 ≈ 455 GB
```

A snapshot reserve sized without a safety margin, or without ongoing
monitoring as change rate grows (Chapter 9), is one of the most common
causes of an unplanned snapshot-related outage: when reserved snapshot
space is exhausted, the platform's fallback behavior is either to
automatically delete the oldest snapshot (silently reducing the actual
retention the design promised) or, on some legacy COW implementations, to
invalidate the snapshot outright — this chapter's lab reproduces exactly
that failure mode as a negative test.

## Design Considerations

- **Snapshot frequency vs. platform mechanism.** A ROW platform can
  reasonably support very frequent (sub-hourly) snapshots; a COW platform's
  write-penalty behavior should be factored into how aggressive a snapshot
  schedule is chosen, especially for write-heavy volumes.
- **Consistency group boundaries must match application boundaries.** Group
  every volume a single application instance depends on for a consistent
  restore point (data, logs, and any dependent volumes), not an arbitrary
  administrative grouping.
- **Synchronous replication distance is a hard physics constraint, not a
  configuration setting** — do not commit to a zero-RPO design without
  first validating actual measured round-trip latency between the specific
  candidate sites.
- **Topology choice should match the actual recovery model**, not just
  what a platform supports by default: a fan-out topology used for both DR
  and test/dev refresh needs to guarantee the DR copy's currency is never
  degraded by test/dev workload demands on the shared replication link.
- **Bidirectional replication requires an explicit conflict-resolution
  policy chosen before deployment**, documented, and periodically tested —
  an undocumented default conflict policy discovered only during a real
  partition event is a design failure, not an edge case.
- **CDP is a targeted, not universal, control.** Apply it to the workloads
  whose RPO requirement or ransomware exposure genuinely justifies its
  overhead; a blanket CDP policy across an entire estate is usually both
  more expensive and operationally noisier than the RPO improvement
  justifies for lower tiers.
- **Snapshot retention is not backup retention.** Snapshots typically live
  on the same physical platform (or a directly attached replica) as the
  source data; they satisfy the "point-in-time recovery" need but do not,
  by themselves, satisfy the "2 different media, 1 offsite, 1 immutable"
  requirements from Chapter 5's 3-2-1-1-0 model.

## Implementation and Automation

### LVM snapshot creation and rollback (Linux, real and reproducible)

```bash
# Create a snapshot of an existing logical volume, reserving 5 GB for
# copy-on-write data
sudo lvcreate --size 5G --snapshot --name lv_data_snap /dev/vg_data/lv_data

# Inspect snapshot allocation and consumed percentage
sudo lvs -o lv_name,lv_size,data_percent vg_data

# Roll the origin volume back to the snapshot's point-in-time state
# (requires the origin to be unmounted first)
sudo umount /data
sudo lvconvert --merge /dev/vg_data/lv_data_snap
sudo mount /dev/vg_data/lv_data /data
```

`data_percent` in the `lvs` output is the field to monitor continuously
(Chapter 9): once it approaches 100%, the reserved snapshot space is
exhausted.

### Illustrative array-based asynchronous replication (generic pattern)

Real replication configuration syntax is array-specific, but the workflow
is consistent across platforms: define a replication relationship between
a source and target volume (or consistency group), set the replication
mode and schedule, and start the relationship.

```text
# Illustrative generic storage array CLI pattern
replication relationship create RR_DB01_DATA \
    --source-volume vol_db01_data --source-site site-a \
    --target-volume vol_db01_data_dr --target-site site-b \
    --mode asynchronous --rpo-target 15m

replication consistency-group create CG_DB01 \
    --members vol_db01_data,vol_db01_log \
    --relationship RR_DB01_DATA

replication relationship start RR_DB01_DATA
replication relationship show RR_DB01_DATA
```

The consistency-group binding is what guarantees the data and log volumes
above replicate as a single atomic unit, directly applying the consistency-
group principle from the theory section to a multi-volume database.

### Illustrative CDP journal configuration

```yaml
# cdp-policy.yaml — illustrative continuous data protection policy
policies:
  - name: tier1-database-cdp
    protected_volumes:
      - vol_db01_data
      - vol_db01_log
    journal_retention_hours: 72
    journal_target: dedicated_journal_pool
    recovery_granularity_seconds: 5
    alert_on_journal_capacity_percent: 80
```

A 72-hour journal retention window means any point within the last 72
hours can be recovered to; beyond that window, recovery falls back to the
discrete snapshot or backup restore points from Chapter 5.

## Validation and Troubleshooting

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Snapshot creation fails or an existing snapshot is silently dropped | Snapshot reserve/pool exhausted | Check `lvs data_percent` (or the array's snapshot pool utilization); increase reserve or reduce retention |
| Application will not start cleanly from a restored snapshot | Crash-consistent snapshot used where application-consistent capture was required | Reconfigure the snapshot job to invoke VSS/`fsfreeze`/database quiesce before capture |
| Replication relationship shows growing lag | Insufficient replication link bandwidth for current change rate, or a network path issue | Compare current change rate against link bandwidth math (Chapter 5); check for packet loss/latency spikes on the replication path |
| Two volumes in an application restore to mutually inconsistent states | Volumes were snapshotted independently rather than as a consistency group | Rebuild the snapshot/replication job to bind all dependent volumes into one consistency group |
| Active-active replication reports conflicting writes after a network partition | Split-brain: both sites accepted writes during the partition | Apply the predefined conflict-resolution policy; if none exists, this is a design gap to close before the next partition, not just an incident to resolve |
| CDP journal capacity alert firing repeatedly | Change rate exceeds journal retention sizing, or a stalled journal consumer | Check journal consumer/replication target health; re-size journal retention against current change rate |

## Security and Best Practices

- Treat snapshots as part of the ransomware attack surface, not purely a
  recovery tool: an attacker with sufficient privilege can delete
  snapshots along with production data unless snapshot deletion is
  separately protected (Chapter 8 develops immutable/locked snapshots in
  depth).
- Restrict who can delete a replication relationship or shorten a CDP
  journal retention window to a narrowly scoped administrative role,
  separate from general storage provisioning access.
- Encrypt replication traffic that crosses untrusted or shared network
  paths, especially inter-site links that may traverse third-party
  circuits.
- Monitor and alert on snapshot reserve and journal capacity proactively
  (Chapter 9) rather than discovering exhaustion when a snapshot operation
  fails.
- Document and periodically test the actual conflict-resolution behavior
  of any bidirectional replication relationship — do not assume the
  documented default is what the platform will do under a real partition.
- Validate that consistency-group membership still matches an
  application's actual volume footprint after any storage reconfiguration;
  a volume added to an application without being added to its consistency
  group silently reintroduces the cross-volume inconsistency risk.

## References and Knowledge Checks

**References**

- SNIA snapshot and replication terminology references.
- Microsoft Volume Shadow Copy Service (VSS) architecture documentation,
  for application-consistent snapshot coordination on Windows.
- `lvcreate(8)`, `lvconvert(8)`, `lvs(8)` manual pages, RHEL 10 / Ubuntu
  Server 26.04 LTS baseline per SOFTWARE_VERSIONS.md.

**Knowledge Checks**

1. Explain why redirect-on-write snapshots avoid the "COW penalty" that
   copy-on-write snapshots incur on the first write to a block after a
   snapshot is taken.
2. A database's data volume and log volume were snapshotted 30 seconds
   apart instead of as a consistency group. Describe the specific
   inconsistency risk this creates.
3. Why is synchronous replication distance fundamentally limited by
   physics rather than by configuration, and what RPO does asynchronous
   replication trade for removing that limitation?
4. What specific problem does continuous data protection solve that a
   4-hour snapshot schedule cannot, even with unlimited retention?
5. Describe the failure mode that occurs when a COW snapshot's reserved
   space is exhausted, and the monitoring practice that prevents it from
   happening unexpectedly.

## Hands-On Lab

### Lab: Create, Roll Back, and Exhaust an LVM Snapshot

This lab creates a working LVM snapshot, modifies the origin volume,
verifies the snapshot preserves the earlier point-in-time state, and
includes a negative test that deliberately exhausts a small snapshot's
reserved space to observe the resulting failure mode.

**Prerequisites**

- A Linux host (RHEL 10 or Ubuntu Server 26.04 LTS baseline) with root or
  sudo access and LVM tools installed (`lvm2` package, present by default
  on most server installations).
- A spare block device, or two loopback-backed files, to build a test
  volume group (this lab does not require dedicated storage hardware).

**Procedure**

1. Create two loopback devices — one for the origin volume, one to keep
   the volume group large enough for both the origin and a snapshot:

   ```bash
   sudo fallocate -l 2G /tmp/lvm-lab-disk.img
   sudo losetup -fP /tmp/lvm-lab-disk.img
   losetup -a | grep lvm-lab-disk
   # Note the assigned device, e.g. /dev/loop10
   ```

2. Build a volume group and a 1 GB origin logical volume, then format and
   mount it:

   ```bash
   sudo pvcreate /dev/loop10
   sudo vgcreate vg_lab /dev/loop10
   sudo lvcreate --size 1G --name lv_lab vg_lab
   sudo mkfs.xfs /dev/vg_lab/lv_lab
   sudo mkdir -p /mnt/lvm-lab
   sudo mount /dev/vg_lab/lv_lab /mnt/lvm-lab
   echo "original data - point in time A" | sudo tee /mnt/lvm-lab/data.txt
   ```

3. Create a snapshot with a deliberately small 100 MB reserve (small on
   purpose, to make the negative test in step 6 reproducible quickly):

   ```bash
   sudo lvcreate --size 100M --snapshot --name lv_lab_snap /dev/vg_lab/lv_lab
   sudo lvs -o lv_name,lv_size,data_percent vg_lab
   ```

   **Expected result:** `lv_lab_snap` appears with `data_percent` at or
   near 0%, since no changes have been made to the origin since the
   snapshot was taken.

4. Modify the origin volume's data:

   ```bash
   echo "modified data - point in time B" | sudo tee /mnt/lvm-lab/data.txt
   sudo lvs -o lv_name,lv_size,data_percent vg_lab
   ```

   **Expected result:** `data_percent` on `lv_lab_snap` rises above 0%,
   reflecting the copy-on-write data now held by the snapshot.

5. Mount the snapshot read-only (separately from the origin) and confirm
   it still shows the original point-in-time content:

   ```bash
   sudo mkdir -p /mnt/lvm-lab-snap
   sudo mount -o ro /dev/vg_lab/lv_lab_snap /mnt/lvm-lab-snap
   cat /mnt/lvm-lab-snap/data.txt
   cat /mnt/lvm-lab/data.txt
   ```

   **Expected result:** the snapshot mount shows `original data - point in
   time A` while the origin mount shows `modified data - point in time B`
   — direct proof the snapshot preserved the earlier state independent of
   subsequent origin changes.

**Negative test**

6. Unmount the snapshot, then generate enough change on the origin to
   exceed the snapshot's 100 MB reserve:

   ```bash
   sudo umount /mnt/lvm-lab-snap
   sudo dd if=/dev/urandom of=/mnt/lvm-lab/fill.bin bs=1M count=150 status=progress
   sudo lvs -o lv_name,lv_size,data_percent vg_lab
   ```

   **Expected result:** `data_percent` on `lv_lab_snap` reaches 100%, and
   the snapshot's status is reported as invalid (`lvs -o
   lv_attr,lv_name vg_lab` shows an invalidated state, typically surfaced
   with a capital `I`/`d` attribute flag). Attempting to mount the
   snapshot at this point fails or exposes an unusable, partial image —
   demonstrating exactly why proactive snapshot-reserve monitoring
   (Chapter 9) is required rather than optional.

**Cleanup**

7. Remove the snapshot (if still present), unmount and remove the origin,
   and tear down the volume group and loopback device:

   ```bash
   sudo lvremove -f vg_lab/lv_lab_snap 2>/dev/null || true
   sudo umount /mnt/lvm-lab
   sudo lvremove -f vg_lab/lv_lab
   sudo vgremove vg_lab
   sudo pvremove /dev/loop10
   sudo losetup -d /dev/loop10
   sudo rm -f /tmp/lvm-lab-disk.img
   sudo rmdir /mnt/lvm-lab /mnt/lvm-lab-snap
   ```

## Summary and Completion Checklist

This chapter covered snapshot mechanisms (copy-on-write vs. redirect-on-
write), the crash-consistent vs. application-consistent distinction and
consistency groups, synchronous vs. asynchronous replication, replication
topologies and split-brain risk, continuous data protection, and snapshot
capacity planning. It then built, validated, and deliberately exhausted a
working LVM snapshot to make the space-exhaustion failure mode directly
observable.

**Completion checklist**

- [ ] Can compare copy-on-write and redirect-on-write snapshot mechanisms
      and their performance implications.
- [ ] Can explain why consistency groups are required for multi-volume
      applications.
- [ ] Can compare synchronous and asynchronous replication on RPO and
      distance constraints.
- [ ] Can describe at least three replication topologies and their use
      cases.
- [ ] Can explain what continuous data protection adds beyond discrete
      snapshot intervals.
- [ ] Has created, verified, and rolled back an LVM snapshot.
- [ ] Has reproduced and diagnosed a snapshot-reserve exhaustion failure.
