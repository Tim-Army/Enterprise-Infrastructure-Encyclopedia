# Volume XXXIII — Microsoft Azure Certification Tracks

> The complete Microsoft Azure certification program in one volume:
> fundamentals, the role-based associate tier, the expert tier, and the
> specialty certifications — with the exam codes, retirement dates, and
> the annual renewal model that governs them all.

## Overview

Volume XXXIII maps Microsoft's Azure certification program end to end and
teaches the platform knowledge each credential assesses. It exists because
the program is **role-based by construction**, which means Microsoft
reorganizes it whenever the underlying roles change — and it is in the
middle of exactly such a reorganization as this volume is written.

Every exam code, retirement date, and status in this volume was verified
against Microsoft Learn on **23 July 2026**, read from the certification
pages and the public catalog API rather than from any summary.

The volume is organized in four parts:

- **Chapter 01** maps the program: four levels, the `AZ`/`AI`/`DP`/`SC`/`AB`
  code families, and the annual free renewal model that distinguishes
  Microsoft from most vendors in this encyclopedia.
- **Chapters 02–04** cover the durable core: the three non-expiring
  fundamentals certifications, the Azure Administrator (AZ-104) that
  anchors the associate tier, and the Azure Network Engineer (AZ-700)
  depth beyond it.
- **Chapters 05–07** cover the tier in motion: the two associate
  certifications now retiring, the AI-centric certifications replacing
  them, and the data track.
- **Chapters 08–09** complete the volume with the expert tier and with
  specialty certifications plus the recurring currency check that keeps
  this map accurate.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab states its cost implications and ends in cleanup, because
every lab in this volume runs against a billable Azure subscription.

## Chapters

1. [The Azure Certification Program — Levels, Codes, and Renewal](chapters/01-the-azure-certification-program-levels-codes-and-renewal.md) — four levels, the exam-code families including the new `AB`, the full current lineup, and the annual free renewal assessment.
2. [Fundamentals — AZ-900, AI-901, and DP-900](chapters/02-fundamentals-az-900-ai-901-and-dp-900.md) — the three non-expiring fundamentals certifications, the AI-900 to AI-901 renumbering, and the subscription/resource-group/region scaffolding they all assume.
3. [Azure Administrator — AZ-104](chapters/03-azure-administrator-az-104.md) — the anchor associate certification: identity and governance, storage, compute, networking, monitoring, and the RBAC-versus-Policy distinction.
4. [Azure Network Engineer — AZ-700](chapters/04-azure-network-engineer-az-700.md) — hybrid connectivity, hub-and-spoke and the non-transitivity of peering, routing, private PaaS access, and the load-balancing portfolio.
5. [The Retiring Associate Tier — AZ-204 and AZ-500](chapters/05-the-retiring-associate-tier-az-204-and-az-500.md) — Azure Developer retires 31 July 2026 and Azure Security Engineer 31 August 2026, including renewal assessments; what that means and where the subject matter went.
6. [The AI-Centric Associate Tier — AI-103, AI-200, and AB-620](chapters/06-the-ai-centric-associate-tier-ai-103-ai-200-and-ab-620.md) — the three new AI certifications replacing the retired AI-102 and DP-100, and what a new code family signals.
7. [Data on Azure — DP-300, DP-420, and DP-750](chapters/07-data-on-azure-dp-300-dp-420-and-dp-750.md) — database administration, Cosmos DB partition design, the new Databricks data-engineering certification, and the gap DP-100's retirement leaves.
8. [The Expert Tier — AZ-305 and AZ-400](chapters/08-the-expert-tier-az-305-and-az-400.md) — solutions architecture and DevOps engineering, both updated in 2026, with RPO/RTO-driven continuity design.
9. [Specialty Certifications and Certification Operations](chapters/09-specialty-certifications-and-certification-operations.md) — the surviving and retired specialties, the adjacent `SC` and Windows Server families, and the four-step currency check.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume maps the whole Microsoft Azure certification program, recorded
in [CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The
table below is the state verified on 23 July 2026; confirm any code and
status on its Microsoft Learn page before registering, because this program
changes faster than this repository's release cycle.

| Level | Certification | Exam | Status |
| --- | --- | --- | --- |
| Fundamentals | Azure Fundamentals | AZ-900 | Current |
| Fundamentals | Azure AI Fundamentals | AI-901 | Current — replaced AI-900 (retired 30 Jun 2026) |
| Fundamentals | Azure Data Fundamentals | DP-900 | Current |
| Associate | Azure Administrator | AZ-104 | Current |
| Associate | Azure Network Engineer | AZ-700 | Current |
| Associate | Azure Database Administrator | DP-300 | Current |
| Associate | Azure Developer | AZ-204 | **Retires 31 July 2026** |
| Associate | Azure Security Engineer | AZ-500 | **Retires 31 August 2026** |
| Associate | Azure AI Engineer | AI-102 | **Retired** |
| Associate | Azure Data Scientist | DP-100 | **Retired** |
| Associate | Azure AI Apps and Agents Developer | AI-103 | Current (new) |
| Associate | Azure AI Cloud Developer | AI-200 | Current (new) |
| Associate | AI Agent Builder | AB-620 | Current (new `AB` family) |
| Associate | Azure Databricks Data Engineer | DP-750 | Current (new) |
| Expert | Azure Solutions Architect Expert | AZ-305 | Current — updated 17 Apr 2026 |
| Expert | DevOps Engineer Expert | AZ-400 | Current — updated 27 Jun 2026 |
| Specialty | Azure Virtual Desktop | AZ-140 | Current |
| Specialty | Azure Cosmos DB Developer | DP-420 | Current |
| Specialty | Azure for SAP Workloads | AZ-120 | Current |
| Specialty | Azure IoT Developer | AZ-220 | **Retired** |
| Specialty | Azure Support Engineer for Connectivity | AZ-720 | **Retired** |
| Specialty | Azure Stack Hub Operator | AZ-600 | **Retired** |

### Three facts to carry into any study plan

**No Azure certification is a prerequisite for another.** Microsoft
"strongly recommends" some sequences — AZ-104 before the SAP Workloads
specialty, for instance — but recommendation is not a gate.

**Renewal is annual, free, and unproctored.** Role-based certifications
last one year and are renewed by a free online assessment on Microsoft
Learn. Fundamentals certifications do not expire at all. This makes
holding a certification cheap, but a lapse is silent and a renewed
certification is quietly re-based onto current content each year.

**The associate tier is being rebuilt around AI.** Two certifications are
retiring, two are already retired, and four are new — one on an entirely
new code family. Chapters 05 and 06 cover this directly, and Chapter 09's
currency check exists because of it.

### Training access

Microsoft Learn provides **free training paths for every certification in
this volume**, which makes paid courses hard to justify at the
fundamentals level and optional above it. Practice assessments are
published free for many exams. Exams themselves are paid and booked
through Microsoft's scheduling flow. The
[course-catalog appendix](../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
records the training path and access model per certification.

## Software and platform baseline

Chapters in this volume reference the current GA Azure service surface and
the Azure CLI. Azure service behavior and portal paths evolve
continuously; treat the CLI examples as correct against the baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) and verify current
syntax against Microsoft's documentation before using them in production.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh
```

```bash
# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all --volume volume-33-microsoft-azure-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
