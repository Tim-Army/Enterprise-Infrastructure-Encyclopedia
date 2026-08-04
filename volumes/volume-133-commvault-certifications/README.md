# Volume CXXXIII — Commvault Certification Tracks

> The certification map for **Commvault**, whose **Readiverse Academy** program was rebuilt in **June
> 2026** around **four tiers on one path** — **Commvault Cloud Practitioner**, **Specialist**,
> **Professional**, and **Expert** — verified on readiverse.com and Commvault's own announcements,
> 4 August 2026. Readiverse calls these "vendor-validated credentials, not just course completions":
> they are earned through **coursework, hands-on lab activities, and validated assessments**. Every tier
> rests on the same **three learning pillars — foundational platform skills, cyber resilience, and
> workload expertise** — so even the entry-level Practitioner requires the **Commvault Cloud
> Administrator** course *and* the **Cyber Resilience** course, each with an exam, plus a workload
> course. Named certifications include **Cloud Administrator**, **Cyber Resilience**, and the SaaS
> credentials for **Threat Scan**, **Cleanroom Recovery**, and **Cloud Rewind**. Commvault is an **ISC2
> CPE Authorized Submitter**, so the coursework also earns continuing-education credit toward CISSP and
> its siblings. The volume models all of it free in Python — retention and cycle pruning, deduplication
> and the DDB, RPO/RTO, immutability and anomaly detection, cleanroom orchestration, and workload
> protection. No Commvault license required.

## Overview

Volume CXXXIII is a **certification-tracks volume** organized by Readiverse's three pillars. Chapters
02–05 cover the **platform**: CommCell architecture and the control-plane/data-plane split, plans and
retention (including why cycle-based retention means space does not free), deduplication and the
deduplication database, and backup/recovery operations against RPO and RTO. Chapters 06–07 cover **cyber
resilience**, the pillar that distinguishes modern data protection: storage-enforced immutability that
survives an admin-level attacker, ransomware detection from backup telemetry, Threat Scan for selecting
a genuinely clean recovery point, and the **Cleanroom Recovery** and **Cloud Rewind** capabilities that
define the Professional tier. Chapter 08 covers **workloads** — Microsoft 365, Active Directory and Entra
ID, VMware, Oracle, and file servers — and Chapter 09 closes on tier selection, ISC2 CPEs, and currency.

Its contribution to the encyclopedia's data-protection shelf is **breadth**: the widest workload coverage
and the most explicit learning ladder, alongside [Veeam LXXXV](../volume-085-veeam-certifications/README.md),
[Rubrik CXXX](../volume-130-rubrik-certifications/README.md), and
[NetApp LXXXIV](../volume-084-netapp-certifications/README.md).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Commvault Program and Readiverse Academy](chapters/01-the-commvault-program-and-readiverse-academy.md) | 1.1–1.2 |
| 02 | [Commvault Cloud Architecture](chapters/02-commvault-cloud-architecture.md) | 2.1–2.3 |
| 03 | [Storage, Plans, and Retention Policies](chapters/03-storage-plans-and-policies.md) | 3.1–3.3 |
| 04 | [Deduplication and Storage Efficiency](chapters/04-deduplication-and-efficiency.md) | 4.1–4.3 |
| 05 | [Backup and Recovery Operations](chapters/05-backup-and-recovery-operations.md) | 5.1–5.3 |
| 06 | [Cyber Resilience — Immutability, Air Gap, and Threat Scan](chapters/06-cyber-resilience-immutability-threat-scan.md) | 6.1–6.3 |
| 07 | [Cleanroom Recovery and Cloud Rewind](chapters/07-cleanroom-recovery-and-cloud-rewind.md) | 7.1–7.3 |
| 08 | [Workload Protection](chapters/08-workload-protection.md) | 8.1–8.3 |
| 09 | [Choosing a Tier, Currency, and Career](chapters/09-choosing-tiers-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the four Readiverse tiers and three pillars, and choose where to start.
- Explain CommCell architecture and why the CommServe catalog is the critical dependency.
- Design plans and retention that satisfy the business, and predict what prunes and when.
- Calculate deduplication savings and order dedup, compression, and encryption correctly.
- Schedule against RPO, size against the backup window, and verify recoverability rather than assume it.
- Implement immutability that resists an admin attacker, and identify the last known-clean recovery point.
- Orchestrate cleanroom recovery and dependency-ordered cloud rebuilds.
- Protect M365, AD/Entra ID, VMware, Oracle, and file servers with the right consistency and granularity.

## Prerequisites

- Storage and virtualization fundamentals; [Volume VI](../volume-006-enterprise-storage-data-protection/README.md) for the vendor-neutral basis.
- A Linux or macOS host with `python3` — every lab runs on the standard library, with no Commvault software.

## See also

- [Volume LXXXV — Veeam](../volume-085-veeam-certifications/README.md), [Volume CXXX — Rubrik](../volume-130-rubrik-certifications/README.md), [Volume LXXXIV — NetApp](../volume-084-netapp-certifications/README.md) — the peer data-protection programs.
- [Volume VI — Enterprise Storage and Data Protection](../volume-006-enterprise-storage-data-protection/README.md) — vendor-neutral foundations.
- [Volume X — Enterprise Cybersecurity](../volume-010-enterprise-cybersecurity/README.md) and [Volume XL — ISC2](../volume-040-isc2-certifications/README.md) — the security framing and the CPE destination.
- [Master Appendices — Commvault appendix](../volume-997-master-appendices/chapters/67-appendix-commvault-certifications-and-course-access.md) — tiers, courses, and access.
