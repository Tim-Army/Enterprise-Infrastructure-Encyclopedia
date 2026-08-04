# Volume CXXX — Rubrik Certification Tracks

> The certification map for **Rubrik** — the **Cyber Resilience Platform for Data and Identity** —
> verified on training.rubrik.com (Rubrik University), 4 August 2026. The program is deliberately
> focused on one active certification, **RCSA (Rubrik Certified System Administrator)**, which validates
> operational administration of **Rubrik Security Cloud (RSC)** and is earned through a **free**
> self-paced learning path (eLearning + unlimited practice exams) or a **paid** 4-day hands-on RSC
> Administration bootcamp, with a **Credly** badge (the older **RCE** is **retired**; Rubrik University
> access needs Rubrik Support credentials). The volume teaches the cyber-resilience model RCSA
> covers — **assume breach, protect immutably, recover fast and clean** — across the RSC domains:
> policy-driven **data protection** (SLA Domains), **immutability and logical air-gap** (backups
> ransomware cannot alter), **ransomware/cyber recovery** (anomaly detection, Data Threat Analytics,
> last-clean-snapshot selection), **Data Security Posture Management** (sensitive-data
> discovery/classification/risk), **recovery orchestration** (RTO/RPO, mass recovery, validation),
> broad **workload** protection (VM/DB/cloud/SaaS), and platform **security + identity resilience**
> (RBAC/MFA, recovering a clean AD/Entra). A **defensive** volume — every technique keeps a clean
> recovery point safe and available — with each drilled by a walkthrough lab modeled in **free Python**
> (an immutable/append-only store, backup-delta anomaly detection, data classification, recovery
> orchestration, RBAC) — no Rubrik software or license required.

## Overview

Volume CXXX is a **certification-tracks volume** for a focused program: one active certification (RCSA)
on a fast-evolving platform. It is organized around the Rubrik Security Cloud domains — architecture and
data protection (Chapter 02, the RCSA operational core), then the cyber-resilience pillars that make the
platform a security control (immutability 03, ransomware recovery 04, DSPM 05, recovery orchestration
06), workloads (07), and platform security + identity resilience (08), closing with study routes and
currency (09). It is a **defensive** volume: the backup is the last line of defense, and every chapter
is about keeping that line immutable, analyzable, and recoverable.

Its standing disciplines are the assume-breach premise, the "an untested recovery is a hope" rule, and
honest currency (one active cert, RCE retired, a platform that ships new security features often).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Rubrik Program and Cyber Resilience](chapters/01-the-rubrik-program-and-cyber-resilience.md) | 1.1–1.2 |
| 02 | [Rubrik Security Cloud Architecture and Data Protection (RCSA Core)](chapters/02-rsc-architecture-data-protection.md) | 2.1–2.3 |
| 03 | [Immutability and Air-Gap](chapters/03-immutability-and-air-gap.md) | 3.1–3.3 |
| 04 | [Ransomware and Cyber Recovery](chapters/04-ransomware-cyber-recovery.md) | 4.1–4.3 |
| 05 | [Data Security Posture Management (DSPM)](chapters/05-dspm.md) | 5.1–5.3 |
| 06 | [Recovery Orchestration and Testing](chapters/06-recovery-orchestration.md) | 6.1–6.3 |
| 07 | [Protecting Workloads — Cloud-Native, Database, and SaaS](chapters/07-workloads.md) | 7.1–7.3 |
| 08 | [Security Best Practices, RBAC, and Identity Resilience](chapters/08-security-rbac-identity-resilience.md) | 8.1–8.3 |
| 09 | [Choosing a Path, Currency, and Career](chapters/09-choosing-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the Rubrik program (RCSA active, RCE retired) and its free/paid study routes.
- Explain and model policy-driven protection (SLA Domains), immutability, and the logical air-gap.
- Reason about ransomware detection in backups, last-clean-snapshot recovery, and DSPM.
- Design recovery to RTO/RPO with orchestrated, validated mass recovery.
- Protect diverse workloads and secure the platform, including identity resilience.

## Prerequisites

- Data-protection and security fundamentals; [Volume X](../volume-010-enterprise-cybersecurity/README.md) for context.
- A Linux host with `python3` for the free labs.

## See also

- [Volume LXXXV — Veeam](../volume-085-veeam-certifications/README.md), [Volume LXXXIV — NetApp](../volume-084-netapp-certifications/README.md) — neighboring data-protection/storage programs.
- [Volume L — CrowdStrike](../volume-050-crowdstrike-certifications/README.md), [Volume X — Enterprise Cybersecurity](../volume-010-enterprise-cybersecurity/README.md) — the security side of cyber resilience.
- [Master Appendices — Rubrik appendix](../volume-997-master-appendices/chapters/64-appendix-rubrik-certifications-and-course-access.md) — the certification, learning paths, and access.
