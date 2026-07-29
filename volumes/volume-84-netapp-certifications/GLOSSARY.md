# Volume LXXXIV Glossary

Definitions for terms introduced in **Volume LXXXIV — NetApp Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Aggregate** — a pool of RAID-protected disks from which ONTAP volumes are carved.
- **Autonomous Ransomware Protection (ARP)** — on-box ONTAP machine learning that detects ransomware-like volume I/O, alerts, and takes an automatic protective Snapshot.
- **AutoSupport (ASUP)** — ONTAP's phone-home telemetry that opens support cases and feeds Active IQ proactive health.
- **Credly** — the platform that hosts NetApp digital certification badges.
- **FabricPool** — ONTAP tiering that moves cold blocks from an SSD aggregate to an object store while hot data stays on flash.
- **FlexGroup** — a single ONTAP namespace spread across many constituent volumes for massive scale.
- **FlexPod** — the Cisco-and-NetApp converged-infrastructure architecture (UCS compute, Nexus/MDS networking, ONTAP storage) validated as Cisco Validated Designs.
- **FlexVol** — a thin-provisioned, resizable ONTAP volume carved from an aggregate.
- **igroup (initiator group)** — the set of host initiators (IQNs/WWPNs) a SAN LUN is mapped to.
- **LIF (logical interface)** — a virtual network interface owned by an SVM and movable across ports and nodes.
- **MetroCluster** — synchronous mirroring between two sites for zero-RPO continuous availability with automatic switchover.
- **NCDA** — NetApp Certified Data Administrator, ONTAP (Professional, exam NS0-163) — the program's flagship credential.
- **NCIE** — NetApp Certified Implementation Engineer, the Specialist tier (SAN NS0-521; Data Protection NS0-528).
- **NVE / NAE** — NetApp Volume Encryption (per volume) and NetApp Aggregate Encryption (per aggregate) for data at rest.
- **ONTAP** — NetApp's storage operating system, serving unified NAS, SAN, and object storage.
- **ONTAP AI (AIPod)** — NetApp's validated AI data-infrastructure design pairing NVIDIA DGX compute with NetApp AFF all-flash storage.
- **RAID-DP / RAID-TEC** — ONTAP's double-parity and triple-parity RAID, surviving two (or three) disk failures per RAID group.
- **SnapLock** — WORM (write-once, read-many) retention; Compliance mode is immutable even to admins, Enterprise mode lets a trusted admin manage retention.
- **SnapMirror** — asynchronous or synchronous replication of Snapshots to another cluster for disaster recovery.
- **Snapshot** — an instant, space-efficient, read-only point-in-time image of a volume.
- **SnapVault** — a SnapMirror vault-policy relationship that keeps long-retention Snapshot backups on a secondary.
- **StorageGRID** — NetApp's S3-compatible, geo-distributed object-storage platform with ILM policies.
- **SVM (storage virtual machine / vserver)** — an ONTAP tenant with its own volumes, LIFs, and namespace.
- **WAFL** — the Write Anywhere File Layout, the file system underpinning ONTAP volumes and Snapshots.
