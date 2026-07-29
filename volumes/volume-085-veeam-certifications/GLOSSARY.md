# Volume LXXXV Glossary

Definitions for terms introduced in **Volume LXXXV — Veeam Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **3-2-1-1-0 rule** — Veeam's data-protection rule: 3 copies of data, on 2 media, with 1 offsite, 1 offline/immutable, and 0 recovery errors after verification.
- **Application-aware processing** — quiescing applications (VSS, database log handling) during backup so restores are transactionally consistent.
- **Backup copy job** — a job that copies backups to a second (often offsite/immutable) repository for the 3-2-1-1-0 rule.
- **Backup proxy** — the Veeam component that moves and processes backup data (read, deduplicate, compress, encrypt).
- **Backup repository** — the storage target for backups (Windows/Linux server, hardened repository, dedup appliance, or object storage).
- **GFS (grandfather-father-son)** — a retention scheme that keeps weekly, monthly, and yearly full backups for long-term retention.
- **Hardened repository** — an immutable Linux backup repository with single-use credentials and immutable flags, resistant to deletion.
- **Immutability** — a property (via object lock or a hardened repository) preventing backups from being altered or deleted before their retention expires.
- **Instant Recovery** — running a workload directly from its backup file (mounted as storage) to meet an aggressive RTO while the full restore proceeds.
- **SOBR (scale-out backup repository)** — a logical repository aggregating storage into performance, capacity (object), and archive tiers.
- **SureBackup** — automated recovery verification that powers on backups in an isolated virtual lab to confirm they boot and applications respond.
- **Veeam Backup & Replication (VBR)** — Veeam's core backup and replication engine; version 13 anchors VMCE+.
- **Veeam Data Cloud Vault** — Veeam's managed, pre-secured, immutable cloud object storage.
- **Veeam ONE** — the Veeam Data Platform's monitoring, reporting, and analytics component.
- **Veeam Recovery Orchestrator (VRO)** — Veeam's orchestrated disaster-recovery product for recovery plans, automated testing, and documentation.
- **Veeam Threat Center** — a dashboard scoring backup health, immutability coverage, and detected threats.
- **Veeam University Pro** — the subscription that delivers the trainings required to sit VMCE+ and VMCSE.
- **VMCA** — Veeam Certified Architect, retired 30 November 2025.
- **VMCE** — Veeam Certified Engineer, the legacy flagship whose exam retires 31 March 2026.
- **VMCE+** — Veeam Certified Engineer Plus, the current v13-aligned flagship certification.
- **VMCSE** — Veeam Certified Security Expert, the security credential arriving Q2 2026 (requires VMCE+).
- **Zero Trust Data Resilience (ZTDR)** — Veeam's application of zero-trust principles to backup: segmentation, least privilege, and immutable verified copies.
