# Volume VI Glossary

Definitions for terms introduced in **Volume VI — Enterprise Storage and
Data Protection**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Access-Based Enumeration (ABE)** — An SMB feature that hides files and
folders a user has no permission to access, rather than showing them as
access-denied. Introduced in Chapter 03.

**ALUA (Asymmetric Logical Unit Access)** — The SCSI standard mechanism
dual-controller arrays use to advertise which paths to a LUN are
Active/Optimized (owning controller) versus Active/Non-Optimized (peer
controller, higher latency), enabling host multipathing to prefer the
faster path. Introduced in Chapter 04.

**ANA (Asymmetric Namespace Access)** — The NVMe analog of ALUA, exposing
per-controller path state (optimized, non-optimized, inaccessible) for
native NVMe multipathing. Introduced in Chapter 04.

**Application-consistent capture** — A snapshot or backup taken after
coordinating with the application or OS quiesce mechanism (Windows VSS,
`fsfreeze`, a database's hot-backup mode) so the resulting restore point is
safe for the application to start from directly. Introduced in Chapter 05
and developed further in Chapter 06.

**Asynchronous replication** — Replication in which a write is
acknowledged to the application immediately and transmitted to the
secondary site afterward, producing a non-zero RPO but without the
distance limitation of synchronous replication. Introduced in Chapter 06.

**Backup catalog** — The metadata database recording what was backed up,
when, where the data physically lives, and the dependency chain between
full/incremental/differential jobs; its own resiliency is a first-class
design concern, not an implicit assumption. Introduced in Chapter 05.

**Backup window** — The available time during which a backup job must
complete, used together with the change rate to compute the required
sustained throughput for a backup design. Introduced in Chapter 05.

**CHAP (Challenge-Handshake Authentication Protocol)** — The
authentication mechanism used to secure an iSCSI session between initiator
and target, optionally mutual (both sides authenticate each other).
Introduced in Chapter 02.

**Compliance mode (object lock)** — An immutability mode in which a locked
object cannot be deleted or modified by anyone, including the account that
created the lock, until the retention period expires. Introduced in
Chapter 08.

**Consistency group** — A set of volumes snapshotted or replicated
atomically as a single operation, required whenever an application depends
on more than one volume (for example, database data and log volumes) to
avoid a cross-volume inconsistent restore point. Introduced in Chapter 06.

**Continuous data protection (CDP)** — Journal-based data protection that
captures a continuous stream of writes, allowing recovery to any point in
time within the journal's retention window rather than only to discrete
snapshot intervals. Introduced in Chapter 06.

**Copy-on-write (COW) snapshot** — A snapshot mechanism that copies the
original block to a reserved snapshot area before the first write to it
after the snapshot is taken, incurring an extra read/write penalty on that
first write. Introduced in Chapter 06.

**Core-edge topology** — A SAN fabric design in which edge switches
aggregate host and storage connections and a higher-bandwidth core switch
interconnects the edges via Inter-Switch Links. Introduced in Chapter 02.

**Crash-consistent capture** — A point-in-time copy taken with no
application or OS coordination, equivalent to the state after a sudden
power loss; sufficient only for workloads with their own crash-recovery
mechanism. Introduced in Chapter 06.

**Data governance** — The set of policies and controls determining how
data is classified, retained, and handled based on sensitivity and
regulatory obligation, including legal hold and data sovereignty.
Introduced in Chapter 08.

**Data sovereignty** — The obligation that certain data remain within a
specific jurisdiction's boundaries, constraining where replication
targets, backup copies, and DR sites may reside. Introduced in Chapter 08.

**Deduplication** — The elimination of redundant data blocks, performed at
the source or target and inline or post-process, reducing network load or
storage consumption depending on where it is applied. Introduced in
Chapter 01 and applied to backup design in Chapter 05.

**DM-Multipath** — The Linux native device-mapper multipathing stack
(`multipathd`) that discovers multiple paths to the same LUN and
coalesces them into a single stable device. Introduced in Chapter 04.

**Erasure coding** — A data protection scheme that spreads data and parity
fragments across many members (commonly nodes rather than drives),
expressed as a data:parity ratio (for example, 10+2), tolerating the loss
of up to the parity fragment count. Introduced in Chapter 01.

**Failback** — The process of returning production operation to the
original primary site after a disaster, requiring explicit reconciliation
of any data written at the DR site during the outage window. Introduced in
Chapter 07.

**Failover** — The act of promoting a secondary or replica environment to
primary and redirecting production traffic to it. Introduced in Chapter
07.

**FCoE (Fibre Channel over Ethernet)** — A converged-fabric transport that
encapsulates FC frames on Data Center Bridging-enabled lossless Ethernet.
Introduced in Chapter 02.

**Fibre Channel (FC)** — A purpose-built, lossless SAN transport using
dedicated switches and HBAs with buffer-to-buffer credit flow control.
Introduced in Chapter 02.

**GFS (Grandfather-Father-Son) retention** — A backup retention model that
retains daily backups for a short window, weekly for a longer window, and
monthly/yearly for the longest window, covering a long retention period
without keeping every daily backup indefinitely. Introduced in Chapter 05.

**Governance mode (object lock)** — An immutability mode in which a locked
object is protected from deletion or modification but a narrowly
privileged, separately audited role can override the lock early.
Introduced in Chapter 08.

**Hot site** — A DR site model with infrastructure fully provisioned and
data kept current via continuous replication, delivering an RTO measured
in minutes to low hours. Introduced in Chapter 07.

**Immutability / WORM (Write Once, Read Many)** — A storage-platform-
enforced guarantee that data cannot be deleted or modified for a defined
retention period, resisting even a compromised administrative account.
Introduced in Chapter 08.

**Incremental-forever backup** — A backup schedule using one initial full
backup followed by indefinite incrementals, with the backup software
synthesizing a current full view without a recurring full-backup window.
Introduced in Chapter 05.

**ISL (Inter-Switch Link) oversubscription** — The ratio of edge-facing to
core-facing bandwidth in a core-edge fabric; an under-provisioned ISL
becomes a fabric-wide bottleneck invisible to any single host. Introduced
in Chapter 02.

**iSCSI** — A block storage transport that carries SCSI commands over
standard Ethernet/TCP-IP networks. Introduced in Chapter 02.

**KMIP (Key Management Interoperability Protocol)** — A standard protocol
for centralized encryption key management, allowing key custody, rotation,
and revocation to be managed independently of the storage platform.
Introduced in Chapter 08.

**Legal hold** — A suspension of normal data retention and deletion
schedules for data subject to litigation, investigation, or audit,
overriding the operational GFS retention policy until released. Introduced
in Chapter 08.

**LUN (Logical Unit Number)** — A raw, addressable block volume presented
by a storage array to a host over a SAN. Introduced in Chapter 01.

**LUN masking** — Array-level access control restricting which specific
LUNs a zoned-and-visible initiator is actually permitted to address.
Introduced in Chapter 02.

**no_path_retry** — A DM-Multipath setting controlling whether I/O queues
indefinitely or fails after a bounded number of retries when all paths to
a device are lost, a decision that must account for cluster fencing
behavior. Introduced in Chapter 04.

**NVMe-oF (NVMe over Fabrics)** — A family of transports (FC-NVMe,
NVMe/TCP, NVMe/RoCE) that extend the NVMe command set's deep queuing model
across a SAN fabric. Introduced in Chapter 02.

**Object lock** — A storage-platform mechanism enforcing WORM/immutability
on individual objects, implemented as governance mode or compliance mode.
Introduced in Chapter 03 and developed fully in Chapter 08.

**Path selection policy** — The multipath configuration setting
determining how I/O is distributed across paths within an active path
group (round-robin, queue-length, or service-time). Introduced in Chapter
04.

**Queue depth** — The number of outstanding I/O requests a device or path
will accept concurrently; higher queue depth increases achievable IOPS up
to a saturation point, beyond which latency rises sharply. Introduced in
Chapter 01.

**RAID (Redundant Array of Independent Disks)** — A set of schemes
(RAID 0/1/5/6/10) that convert physical drives into a logical unit
tolerating one or more member failures, trading usable capacity and write
performance for fault tolerance. Introduced in Chapter 01.

**Ransomware resilience model** — The three-layer model of prevention,
detection, and guaranteed-clean recovery, in which recovery is the layer
that must not fail once prevention and detection have both been defeated.
Introduced in Chapter 08.

**Recovery Point Objective (RPO)** — The maximum acceptable amount of data
loss, expressed as a duration, satisfied by backup and replication
frequency rather than restore speed. Introduced in Chapter 05.

**Recovery runbook** — The authoritative, version-controlled, tested
procedure for executing a recovery, including trigger criteria, roles,
step-by-step commands, validation checkpoints, and a separate failback
procedure. Introduced in Chapter 07.

**Recovery Time Objective (RTO)** — The maximum acceptable duration from
the start of an outage to restoration of a working service, decomposed
into detection, decision, and execution phases. Introduced in Chapter 05
and decomposed in Chapter 07.

**Redirect-on-write (ROW) snapshot** — A snapshot mechanism that always
directs new writes to newly allocated blocks and retains a pointer to the
original blocks for the snapshot, avoiding the copy-on-write penalty.
Introduced in Chapter 06.

**root_squash** — The default NFS export behavior mapping a remote root
user to an unprivileged local account, preventing a client's root user
from gaining root privilege over the exported filesystem. Introduced in
Chapter 03.

**Scale-out file system** — A distributed file system that spreads
namespace metadata and data across a cluster of nodes, scaling capacity
and performance roughly linearly while confining a single node failure's
impact. Introduced in Chapter 03.

**Self-encrypting drive (SED)** — A drive that transparently encrypts data
at the hardware layer; protects against physical media theft but not
against an authenticated user or compromised account reading data through
the normal access path, which is why it must be paired with centralized
key management. Introduced in Chapter 08.

**Snapshot** — A read-only, point-in-time view of a volume, distinct from
a clone, which is a writable copy. Introduced in Chapter 06.

**Split-brain** — A failure mode in bidirectional/active-active
replication where a network partition allows both sites to independently
accept writes to the same data, producing divergent copies that require a
predefined conflict-resolution policy to reconcile. Introduced in Chapter
06.

**Storage service catalog** — A small set of named service tiers with
explicit, measurable latency, IOPS, availability, and RPO characteristics,
translating the media hierarchy into offerings application owners can
request without needing to understand RAID math. Introduced in Chapter 01.

**Synchronous replication** — Replication in which a write is acknowledged
to the application only after the secondary site confirms it has also
committed the write, delivering near-zero RPO at the cost of round-trip
latency that bounds practical distance. Introduced in Chapter 06.

**Synthetic full backup** — A new full restore point built by merging a
prior full and subsequent incrementals at the backup target, without
re-reading the entire source dataset. Introduced in Chapter 05.

**Thin provisioning** — Allocating storage capacity on write rather than
at volume creation, creating a gap between provisioned and physical
capacity that must be actively monitored to avoid unplanned pool
exhaustion. Introduced in Chapter 01.

**Trend-based capacity forecasting** — Extrapolating observed capacity
growth rate forward to project time-to-exhaustion, catching risk that a
static threshold alert misses because it does not account for rate of
change. Introduced in Chapter 09.

**WWID (World Wide Identifier)** — The stable identifier used to recognize
that multiple raw paths represent the same underlying LUN, forming the
basis for persistent multipath device naming. Introduced in Chapter 04.

**Zoning** — Fabric switch-level access control restricting which WWNs or
ports can communicate; standard practice uses single-initiator,
single-target (1:1) zones to minimize RSCN blast radius. Introduced in
Chapter 02.

**3-2-1-1-0 rule** — The extended backup architecture pattern requiring
three copies of data, on two different media, with one copy offsite, one
copy immutable or air-gapped, and zero errors (every backup verified
restorable). Introduced in Chapter 05.
