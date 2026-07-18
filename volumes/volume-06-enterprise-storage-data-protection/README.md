# Volume VI — Enterprise Storage and Data Protection

> Vendor-neutral storage architecture and data protection engineering:
> block, file, and object storage; SAN fabrics and host multipathing;
> backup, snapshots, replication, and continuous data protection; disaster
> recovery validation; ransomware resilience and data governance; and the
> automation, observability, capacity, and lifecycle practices that keep a
> storage platform operable at scale.

## Overview

Volume VI builds a complete, vendor-neutral storage and data protection
curriculum from first principles to daily operations. It assumes the
engineering practices established in Volume I (repository architecture,
automation architecture, documentation pipelines) and is a named
dependency for later volumes that provision or protect storage, most
directly Volume V (VMware Virtualization), Volume VII (Cloud
Infrastructure), and Volume X (Enterprise Cybersecurity).

The volume is organized in three arcs:

- **Chapters 01–03** establish storage architecture fundamentals: the
  block/file/object access models, the media hierarchy and RAID/erasure
  coding, the storage service catalog, SAN fabric transports and access
  control, and enterprise file and object storage protocols.
- **Chapter 04** covers host-side storage integration — multipathing, ALUA
  and ANA path awareness, and the host I/O stack that turns fabric
  redundancy into application-visible resilience.
- **Chapters 05–09** cover data protection end to end: backup architecture
  and RPO/RTO-driven policy design, snapshots and replication and
  continuous data protection, recovery engineering and disaster recovery
  validation, storage security and ransomware resilience and data
  governance, and the automation, observability, capacity forecasting, and
  lifecycle operations that keep all of the above running correctly over
  time.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with stated
prerequisites, numbered steps, expected results, a negative test, and
cleanup instructions, built from real, vendor-neutral tooling (`targetcli`,
`iscsiadm`, `multipathd`, LVM, `restic`, and standard Linux utilities)
rather than proprietary vendor consoles.

## Chapters

1. [Enterprise Storage Architecture and Service Design](chapters/01-enterprise-storage-architecture-and-service-design.md) — block/file/object access models, the media hierarchy and tiering economics, RAID and erasure coding fundamentals, and the storage service catalog.
2. [Block Storage and Storage Area Networks](chapters/02-block-storage-and-storage-area-networks.md) — Fibre Channel, iSCSI, FCoE, and NVMe-oF transports, fabric topology, zoning and LUN masking, and array front-end/back-end architecture.
3. [Enterprise File and Object Storage](chapters/03-enterprise-file-and-object-storage.md) — NFS and SMB protocols, scale-out file systems, object storage's flat namespace and lifecycle model, and choosing between file and object.
4. [Host Storage Integration and Multipathing](chapters/04-host-storage-integration-and-multipathing.md) — DM-Multipath and NVMe native multipathing, ALUA/ANA path states, path selection policies, and the host-side queue depth chain.
5. [Backup Architecture and Data Protection Policy](chapters/05-backup-architecture-and-data-protection-policy.md) — RPO/RTO definitions, the 3-2-1-1-0 rule, backup types, backup software architecture, and retention policy design.
6. [Snapshots, Replication, and Continuous Data Protection](chapters/06-snapshots-replication-and-continuous-data-protection.md) — copy-on-write vs. redirect-on-write snapshots, consistency groups, synchronous/asynchronous replication topologies, and journal-based CDP.
7. [Recovery Engineering and Disaster Recovery Validation](chapters/07-recovery-engineering-and-disaster-recovery-validation.md) — DR site models, the detection/decision/execution RTO breakdown, recovery runbooks, failover/failback risk, and DR test types.
8. [Storage Security, Ransomware Resilience, and Data Governance](chapters/08-storage-security-ransomware-resilience-and-data-governance.md) — encryption and key management, storage RBAC, immutability and object lock, the layered ransomware resilience model, and data governance.
9. [Storage Automation, Observability, Capacity, and Lifecycle Operations](chapters/09-storage-automation-observability-capacity-and-lifecycle-operations.md) — infrastructure-as-code storage provisioning, the observability stack, trend-based capacity forecasting, and firmware/refresh/decommissioning lifecycle practices.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) — RHEL 10 and Ubuntu
Server 26.04 LTS for host-side CLI examples (`targetcli`, `iscsiadm`,
`multipathd`, LVM, `restic`, Python 3). Storage array, backup platform, and
fabric switch examples in this volume are intentionally vendor-neutral and
illustrative; update this file, not individual chapters, when the Linux
baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-06-enterprise-storage-data-protection

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-06-enterprise-storage-data-protection/chapters/05-backup-architecture-and-data-protection-policy.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
