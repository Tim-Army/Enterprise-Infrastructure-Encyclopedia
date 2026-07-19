# Chapter 1: Enterprise Storage Architecture and Service Design

## Learning Objectives

- Classify enterprise storage into block, file, and object access models and
  explain when each model is the correct fit for a workload.
- Describe the storage media hierarchy (HDD, SATA/SAS SSD, NVMe, and storage
  class memory) and how tiering uses that hierarchy to balance cost and
  performance.
- Explain RAID and erasure coding fundamentals well enough to calculate usable
  capacity and fault tolerance for a proposed array.
- Translate business requirements into a storage service catalog with
  measurable performance, availability, and recovery tiers.
- Identify the storage metrics (IOPS, throughput, latency, queue depth) that
  drive capacity and performance planning, and the tools used to measure them.
- Apply a structured design process — workload profiling, tiering,
  data-service selection, and SLA definition — to a net-new storage design.

## Theory and Architecture

Enterprise storage exists to make data durable, available, and fast enough for
the applications that depend on it. Every storage design decision is a
trade-off among three axes: **capacity** (how much usable space is delivered),
**performance** (IOPS, throughput, and latency), and **resiliency** (how much
component failure the system tolerates without data loss or an outage). A
storage architect's job is choosing where a given workload sits on those three
axes and building a service that meets it — deliberately, not by accident.

### Access models: block, file, and object

Storage is consumed through one of three access models, and the model
dictates the protocol, the client integration, and the operational pattern.

| Model | Unit of access | Typical protocols | Typical workloads |
| --- | --- | --- | --- |
| Block | Fixed-size blocks on a raw volume (LUN) | Fibre Channel, iSCSI, NVMe-oF | Databases, hypervisor datastores, boot volumes |
| File | Files and directories in a shared namespace | NFS, SMB | Home directories, application shares, general-purpose NAS |
| Object | Immutable objects addressed by key, with metadata | HTTP/S3-compatible REST APIs | Backup targets, archives, unstructured data, cloud-native apps |

Block storage gives a host exclusive (or path-managed) access to a raw device;
the host's own filesystem or volume manager owns the data structure on top of
it. This is the lowest-latency model because there is no intervening
namespace service, but it is also the least shareable — concurrent access by
multiple hosts to the same block device requires a cluster-aware filesystem or
strict ownership rules. File storage moves the namespace into the storage
platform itself: the array or filer manages directories, permissions, and
locking, and many clients can share the same namespace concurrently. Object
storage discards the hierarchical namespace entirely in favor of a flat
(or logically flat) keyspace, rich metadata, and HTTP-based APIs; it trades
POSIX semantics and low millisecond latency for near-infinite horizontal
scalability and built-in durability mechanisms such as erasure coding across
failure domains. Chapters 2 and 3 cover block and file/object implementation
in depth; this chapter establishes the architectural vocabulary shared by all
three.

### Media hierarchy and the economics of tiering

Storage media sit on a well-understood cost/performance curve:

| Media | Typical random read latency | Relative cost per usable TB | Common role |
| --- | --- | --- | --- |
| 7.2K RPM HDD | 5–10 ms | Lowest | Capacity/archive tier, backup targets |
| 10K/15K RPM HDD | 2–4 ms | Low-medium | Legacy general-purpose tier (largely displaced by SSD) |
| SATA/SAS SSD | 100–200 µs | Medium | General-purpose primary tier |
| NVMe SSD | 20–100 µs | Medium-high | High-performance primary tier, databases |
| Storage Class Memory (e.g., persistent memory tiers) | Sub-10 µs | Highest | Ultra-low-latency caching and journal tiers |

No production platform is built from a single media type end to end. Instead,
architectures use **tiering** — automated or policy-driven placement of data
onto the media class that matches its access pattern — to avoid paying
flash/NVMe prices for cold data or accepting HDD latency for hot data.
Tiering operates at different granularities: sub-LUN block tiering inside an
array, storage-policy-based tiering in software-defined platforms, and
lifecycle-policy tiering in object storage (hot → warm → cold → archive
storage classes). The design question is never "flash or disk" but "what
percentage of this workload's active working set needs the top tier, and how
quickly does data go cold."

### RAID and erasure coding fundamentals

RAID (Redundant Array of Independent Disks) and erasure coding both convert a
set of physical drives into a logical unit that tolerates the loss of one or
more members without losing data. The mechanism differs, but the underlying
trade-off is identical: redundancy consumes usable capacity and write
performance in exchange for fault tolerance.

| Level | Minimum drives | Usable capacity | Fault tolerance | Write penalty | Notes |
| --- | --- | --- | --- | --- | --- |
| RAID 0 | 2 | 100% (N × smallest member) | None | 1× | Striping only; no redundancy, used only where resiliency is handled elsewhere |
| RAID 1 | 2 | 50% | 1 drive per mirrored pair | 2× | Mirroring; simplest, best small-write performance among redundant levels |
| RAID 5 | 3 | (N−1)/N | 1 drive | 4× (read-modify-write) | Single parity; rebuild risk grows with large-capacity drives |
| RAID 6 | 4 | (N−2)/N | 2 drives | 6× | Dual parity; standard choice for large-capacity HDD arrays |
| RAID 10 | 4 | 50% | 1 drive per mirrored pair (up to N/2) | 2× | Striped mirrors; best performance-and-resiliency balance for write-heavy workloads |
| Erasure coding (e.g., 10+2, 6+3) | Varies (data + parity fragments) | k/(k+m) | m fragments | Higher CPU cost, amortized across nodes | Common in scale-out file and object platforms; fault domain is typically a node or rack, not a single drive |

The write penalty column matters more than it appears: a RAID 5 array
absorbs a small random write as a read-modify-write cycle (read old data,
read old parity, write new data, write new parity — four I/O operations for
one logical write), which is why RAID 5/6 on spinning disk performs poorly
under heavy random-write database workloads even though it is capacity
efficient. RAID 10 avoids the penalty by mirroring instead of computing
parity, at the cost of losing half of raw capacity. Erasure coding generalizes
parity RAID across many more members and across nodes rather than drives
within one enclosure, which is why it dominates scale-out file and object
platforms: it tolerates the loss of an entire node, not just a disk, at a
capacity efficiency far better than node-level mirroring would allow.

### Storage controllers, caching, and data services

A storage array or software-defined storage cluster wraps the physical media
in a **controller** layer that provides:

- **Front-end connectivity** — the Fibre Channel, iSCSI, NVMe-oF, NFS, SMB, or
  S3-compatible ports that clients connect to.
- **Cache** — DRAM (and sometimes NVDIMM or SCM) that absorbs writes and
  serves hot reads; write cache is typically mirrored between redundant
  controllers and protected by battery or supercapacitor-backed destage so an
  acknowledged write survives a power loss.
- **Data services** — features layered on top of raw capacity: thin
  provisioning (allocate on write rather than on volume creation),
  deduplication and compression (reduce the physical footprint of stored
  data), snapshots and clones (point-in-time copies, covered in depth in
  [Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)), and quality-of-service controls (per-volume IOPS/throughput
  limits to prevent noisy-neighbor contention).
- **Back-end connectivity** — the internal fabric connecting controllers to
  drive shelves or, in scale-out designs, the cluster interconnect between
  storage nodes.

Thin provisioning and deduplication both create a gap between **provisioned**
capacity (what has been presented to hosts) and **physical** capacity (what is
actually consumed on media). That gap is a planning tool, not a free lunch:
over-provisioning without capacity monitoring is one of the most common causes
of an emergency, unplanned outage when a thin pool fills without warning.
[Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md) covers the observability practices that keep that gap under control.

### Performance vocabulary

Four metrics recur throughout this volume and should be treated as a fixed
vocabulary:

- **IOPS** (I/O operations per second) — the count of discrete read/write
  operations a system services. Dominated by random small-block workloads
  (databases, virtualization).
- **Throughput** (MB/s or GB/s) — the volume of data moved per second.
  Dominated by sequential large-block workloads (backup streams, media,
  analytics scans).
- **Latency** — the time to complete a single I/O, usually reported as an
  average and as tail percentiles (p95, p99). Latency is the metric
  applications actually feel; a system can have excellent IOPS and terrible
  latency under contention.
- **Queue depth** — the number of outstanding I/O requests a device or path
  will accept concurrently. Queue depth interacts with latency and IOPS
  through Little's Law: higher queue depth increases achievable IOPS up to a
  saturation point, beyond which latency rises sharply.

## Design Considerations

### Workload profiling before media selection

Every storage design should begin with a workload profile, not a media
catalog. At minimum, capture:

1. **Access pattern** — random vs. sequential, read/write mix, block size.
2. **Capacity** — current size, growth rate, and retention requirement.
3. **Performance target** — IOPS and latency at a stated queue depth, and
   throughput for streaming operations.
4. **Availability requirement** — acceptable downtime and the fault domains
   the design must survive (drive, controller, node, rack, site).
5. **Data protection requirement** — RPO/RTO ([Chapter 5](05-backup-architecture-and-data-protection-policy.md) and 7 define these
   formally), retention, and immutability needs.

A design built from a vendor spec sheet instead of a workload profile
routinely over-provisions performance it does not need while under-provisioning
the resiliency or capacity growth it does need.

### Choosing a RAID or erasure coding scheme

- Favor RAID 10 (or an equivalent mirrored scheme) for random-write-heavy,
  latency-sensitive workloads such as OLTP databases and hypervisor
  datastores, accepting the 50% capacity overhead as the cost of predictable
  performance and fast rebuilds.
- Favor RAID 6 or dual-parity erasure coding for large-capacity,
  read-dominant, or sequential workloads (archives, backup repositories,
  media) where capacity efficiency matters more than write latency, and where
  drive sizes are large enough that a single-parity scheme's rebuild window
  creates unacceptable exposure to a second failure.
- For scale-out file and object platforms, erasure coding schemes are
  expressed as data:parity fragment ratios (for example, 10+2). Wider stripes
  improve capacity efficiency but increase the number of nodes that must
  participate in every read and rebuild, and increase the blast radius of a
  correlated failure (a rack or power-domain outage). Align the fragment
  placement policy to real fault domains, not just node count.

### Tiering and service catalog design

Translate the media hierarchy into a small number of named service tiers with
explicit, measurable characteristics rather than exposing raw media choices to
consumers. A typical three-tier catalog:

| Tier | Media | Target latency | Target IOPS/TB | Availability | Backup RPO | Example workloads |
| --- | --- | --- | --- | --- | --- | --- |
| Platinum | NVMe, RAID 10 / mirrored | < 1 ms | 20,000+ | 99.99% (dual-controller, no single point of failure) | 15 minutes (CDP/frequent snapshot) | Tier-1 databases, latency-sensitive OLTP |
| Gold | SAS/SATA SSD, RAID 10 or RAID 6 | < 5 ms | 5,000–10,000 | 99.95% | 4 hours | General-purpose virtualization, application tiers |
| Bronze | HDD or erasure-coded capacity nodes | < 20 ms | 500–1,000 | 99.9% | 24 hours | File shares, archives, backup targets |

A service catalog like this does two things a media list cannot: it gives
application owners a vocabulary to request storage without needing to
understand RAID math, and it gives the storage team a small, auditable set of
configurations to operate, monitor, and capacity-plan against.

### Multi-tenancy, chargeback, and showback

Shared platforms need isolation and accountability mechanisms: per-tenant
quotas, QoS limits to prevent noisy-neighbor impact, and either chargeback
(billing tenants for consumption) or showback (reporting consumption without
billing) to keep demand honest. Design these in from the start — retrofitting
metering onto a platform that has already been provisioned without it is
substantially more disruptive than building it into the initial service
catalog.

## Implementation and Automation

### Modeling usable capacity

Capacity planning starts with the RAID/erasure-coding formula applied to real
drive counts. For a RAID 6 array of twelve 8 TB drives:

```text
Usable capacity = (N - 2) x drive_size
                = (12 - 2) x 8 TB
                = 80 TB raw-usable (before filesystem/thin-provisioning overhead)
```

For a 10+2 erasure-coded pool spread across twelve nodes with 8 TB per node:

```text
Usable capacity = (k / (k + m)) x total_raw_capacity
                = (10 / 12) x (12 x 8 TB)
                = 80 TB
```

Both schemes tolerate two failures and land at the same usable capacity in
this example, but the RAID 6 array's fault domain is a single enclosure's
twelve drives, while the erasure-coded pool's fault domain is spread across
twelve independent nodes — a materially different resiliency posture against
a correlated failure such as a shelf power loss.

### Expressing the service catalog as data

Treat the storage service catalog as a version-controlled artifact so
provisioning tooling and the design documentation never drift apart:

```yaml
# storage-service-catalog.yaml
service_tiers:
  - name: platinum
    media: nvme
    raid_scheme: raid10
    target_latency_ms: 1
    target_iops_per_tb: 20000
    availability_target: "99.99"
    backup_rpo_minutes: 15
    replication: synchronous
  - name: gold
    media: ssd
    raid_scheme: raid6
    target_latency_ms: 5
    target_iops_per_tb: 7500
    availability_target: "99.95"
    backup_rpo_minutes: 240
    replication: asynchronous
  - name: bronze
    media: hdd
    raid_scheme: erasure_coded_10_2
    target_latency_ms: 20
    target_iops_per_tb: 750
    availability_target: "99.9"
    backup_rpo_minutes: 1440
    replication: none
```

This file becomes the source of truth an automation pipeline ([Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md))
reads when provisioning a volume, and the reference a capacity report
validates actual consumption against.

### Baseline performance measurement

Before a platform goes into production, capture a performance baseline with a
synthetic I/O generator so future troubleshooting has a known-good reference
point. `fio` (Flexible I/O Tester) is the standard, vendor-neutral tool for
this:

```bash
# Random 4K read/write mix at queue depth 32, representative of OLTP
fio --name=oltp_profile --filename=/dev/sdX --direct=1 \
    --rw=randrw --rwmixread=70 --bs=4k --iodepth=32 \
    --numjobs=4 --runtime=300 --time_based --group_reporting

# Sequential 1M throughput test, representative of backup streaming
fio --name=seq_throughput --filename=/dev/sdX --direct=1 \
    --rw=write --bs=1M --iodepth=8 --numjobs=1 \
    --runtime=120 --time_based --group_reporting
```

Record the resulting IOPS, throughput, and p99 latency in the design
documentation alongside the service tier the device was provisioned against.

## Validation and Troubleshooting

- **Confirm the design matches the profile.** Re-run the `fio` baseline
  against the delivered service tier and compare against the catalog's
  target latency and IOPS/TB; a shortfall usually traces to an
  under-configured cache, an oversubscribed back-end fabric, or a RAID
  rebuild in progress.
- **Watch queue depth saturation.** `iostat -x 1` exposes `avgqu-sz` (or
  `aqu-sz` on newer util-linux) and `%util`; a device pinned at 100 percent
  utilization with climbing average wait time indicates the queue depth
  presented by the host exceeds what the back end can service — a common
  symptom of under-sized multipath queue depth settings ([Chapter 4](04-host-storage-integration-and-multipathing.md)) or an
  under-provisioned back-end fabric.
- **Distinguish capacity exhaustion from performance degradation.** A thin
  pool approaching full commonly degrades write latency well before it
  reports as full; monitor physical (not just provisioned) capacity headroom
  as a first-class alert, not an afterthought.
- **Rebuild impact.** After a drive failure, RAID or erasure-coding rebuild
  consumes back-end bandwidth and can visibly raise latency on the affected
  pool; this is expected and should be sized for in the service tier's
  performance target, not treated as an anomaly.
- **Common misdiagnosis:** attributing application-level latency complaints
  to "the storage" without first correlating host-side queue depth, path
  count, and network/fabric utilization; most reported "storage is slow"
  tickets resolve to a host or fabric bottleneck upstream of the array.

## Security and Best Practices

- Encrypt data at rest using array- or platform-level encryption with keys
  managed by a dedicated key management service (KMIP-compatible where
  possible); do not rely solely on self-encrypting drives without centralized
  key custody, since drive-only encryption does not protect against
  authenticated access through the storage stack.
- Apply least-privilege administrative roles on the storage management plane;
  separate the roles that can provision capacity from the roles that can
  delete volumes or modify data-protection policy.
- Treat the storage service catalog and its automation as configuration that
  goes through the same change-control process as any other production
  infrastructure — an unreviewed RAID or replication policy change can
  silently remove the resiliency a workload depends on.
- Log and retain all administrative actions on storage controllers and
  management planes; these logs are frequently the only forensic trail after
  a data-integrity incident (see [Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md)).
- Document the fault domain each service tier actually tolerates (single
  drive, controller, node, rack, site) and validate it periodically — fault
  domain claims drift as hardware is added without re-validating placement
  policy.

## References and Knowledge Checks

**References**

- [SNIA (Storage Networking Industry Association) Dictionary and CDMI/SDS
  reference architectures](https://www.snia.org/education/dictionary/about-dictionary) — vendor-neutral storage terminology and models.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated Linux baseline (RHEL 10 / Ubuntu Server
  26.04 LTS) used for CLI examples throughout this volume.
- [`fio(1)` and `iostat(1)` manual pages for the host toolchain used in this
  chapter's benchmarking examples.](https://fio.readthedocs.io/en/latest/fio_doc.html)

**Knowledge Checks**

1. A workload needs 50,000 random 4K IOPS at sub-millisecond latency and can
   tolerate the loss of exactly one drive per RAID group. Which RAID scheme
   from this chapter best fits, and why is RAID 6 a poor choice here?
2. A twelve-node erasure-coded object pool uses a 10+2 scheme. What is the
   usable capacity as a percentage of raw capacity, and how many node
   failures can occur simultaneously without data loss?
3. Explain the difference between provisioned capacity and physical capacity
   in a thin-provisioned pool, and describe one monitoring practice that
   prevents an unplanned outage from pool exhaustion.
4. Why does a scale-out erasure-coded platform tolerate a correlated
   rack-level failure better than a single RAID 6 array, even when both
   schemes report the same usable-capacity percentage?
5. List the four core performance metrics introduced in this chapter and
   identify which one most directly reflects what an end user experiences as
   "the application feels slow."

## Hands-On Lab

### Lab: Model a Storage Service Catalog and Baseline Performance

This lab builds a small, version-controlled storage service catalog and
validates it against a measured performance baseline on a Linux host. It does
not require shared storage hardware — a local disk, loop device, or virtual
machine disk is sufficient.

**Prerequisites**

- A Linux host (RHEL 10 or Ubuntu Server 26.04 LTS baseline) with root or
  sudo access.
- `fio` and `sysstat` (for `iostat`) installed:

  ```bash
  # RHEL 10
  sudo dnf install -y fio sysstat

  # Ubuntu Server 26.04 LTS
  sudo apt-get update && sudo apt-get install -y fio sysstat
  ```

- A spare block device, loop device, or dedicated test file at least 4 GB in
  size that you are authorized to write to and can safely destroy.

**Procedure**

1. Create a loopback test target if you do not have a spare block device:

   ```bash
   sudo fallocate -l 4G /tmp/storage-lab.img
   sudo losetup -fP /tmp/storage-lab.img
   losetup -a | grep storage-lab
   # Note the assigned device, e.g. /dev/loop10
   ```

2. Create the service catalog file:

   ```bash
   mkdir -p ~/storage-lab && cd ~/storage-lab
   cat > storage-service-catalog.yaml <<'EOF'
   service_tiers:
     - name: gold
       media: ssd
       raid_scheme: raid10
       target_latency_ms: 5
       target_iops_per_tb: 7500
       availability_target: "99.95"
   EOF
   ```

3. Run the baseline random read/write test against the loop device (replace
   `/dev/loopN` with the device from step 1):

   ```bash
   sudo fio --name=oltp_profile --filename=/dev/loopN --direct=1 \
       --rw=randrw --rwmixread=70 --bs=4k --iodepth=32 \
       --numjobs=2 --runtime=60 --time_based --group_reporting \
       --output=fio-baseline.txt
   cat fio-baseline.txt
   ```

4. Extract the measured IOPS and p99 latency from `fio-baseline.txt` and
   record them next to the `gold` tier's targets in the catalog file (as a
   comment or a companion `results:` block).

5. **Expected result:** `fio` reports a combined read+write IOPS figure and a
   completion latency distribution. On typical loopback-over-tmpfs or a local
   SSD, IOPS will exceed the modest `gold` tier target used in this lab;
   record the actual number rather than assuming the target was met.

**Negative test**

6. Re-run the same `fio` job with `--iodepth=1` and compare the resulting
   IOPS to the `--iodepth=32` run:

   ```bash
   sudo fio --name=oltp_profile_qd1 --filename=/dev/loopN --direct=1 \
       --rw=randrw --rwmixread=70 --bs=4k --iodepth=1 \
       --numjobs=1 --runtime=60 --time_based --group_reporting
   ```

   **Expected result:** IOPS drops sharply compared to the queue-depth-32 run
   even though latency per operation may look similar — this demonstrates why
   queue depth, not just raw device speed, determines achievable IOPS, and
   why a host misconfigured with a shallow queue depth ([Chapter 4](04-host-storage-integration-and-multipathing.md)) will
   under-perform its provisioned storage tier regardless of the array's
   capability.

**Cleanup**

7. Remove the loopback device and backing file:

   ```bash
   sudo losetup -d /dev/loopN
   rm -f /tmp/storage-lab.img
   ```

8. Retain `storage-service-catalog.yaml` and `fio-baseline.txt` if you intend
   to reuse them as a template; otherwise remove the `~/storage-lab`
   directory.

## Summary and Completion Checklist

This chapter established the shared vocabulary for the rest of the volume:
the three storage access models (block, file, object), the media hierarchy
that tiering is built on, RAID and erasure-coding fundamentals and their
capacity/resiliency/performance trade-offs, and the performance metrics
(IOPS, throughput, latency, queue depth) used to specify and validate a
design. It also introduced the storage service catalog as the mechanism that
turns those concepts into a small, operable, auditable set of offerings.

**Completion checklist**

- [ ] Can classify a given workload as block, file, or object and justify the
      choice.
- [ ] Can calculate usable capacity and fault tolerance for RAID 0/1/5/6/10
      and a stated erasure-coding scheme.
- [ ] Can explain the write penalty of parity RAID and why it affects
      random-write-heavy workloads more than sequential workloads.
- [ ] Has built and version-controlled a sample storage service catalog with
      at least two tiers.
- [ ] Has run an `fio` baseline and correlated queue depth with achieved
      IOPS.
- [ ] Understands the difference between provisioned and physical capacity in
      a thin-provisioned pool.
