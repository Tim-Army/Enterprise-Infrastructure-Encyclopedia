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

### Lab coverage — AZ-104 (Azure Administrator)

Labs are mapped to the certification's published **"Skills measured"**
outline (harvested from Microsoft Learn's study guide), domain by domain
at Microsoft's own weights. Every domain has walkthrough labs in
[Chapter 03](chapters/03-azure-administrator-az-104.md).

| Skills-measured domain (weight) | Labs |
| --- | --- |
| Manage Azure identities and governance (20–25%) | 3.1–3.6 |
| Implement and manage storage (15–20%) | 3.7–3.10 |
| Deploy and manage Azure compute resources (20–25%) | 3.11–3.15 |
| Implement and manage virtual networking (15–20%) | 3.16–3.19 |
| Monitor and maintain Azure resources (10–15%) | 3.20–3.22 |

Lab 3.23 is the negative test (Policy denies a privileged principal) and
3.24 is cleanup. Every lab is a **walkthrough**: the runnable `az` command
plus the expected result.

**All certifications in this volume now carry topic-level walkthrough
labs**, mapped to each exam's published "Skills measured" outline (Chapters
02–08). The design exam AZ-305 additionally carries a `## Design Exercise`
section. Chapter 01 (program planning) and Chapter 09 (currency check) keep
process labs, since their subject is the program itself.

### Lab coverage — AZ-305 (Solutions Architect)

Mapped to the AZ-305 "Skills measured" outline at Microsoft's weights.
AZ-305 is a design exam, so labs read the evidence a design rests on and
record the decision with its rejected alternative. Labs are in
[Chapter 08](chapters/08-the-expert-tier-az-305-and-az-400.md).

| Skills-measured domain (weight) | Labs |
| --- | --- |
| Design identity, governance, and monitoring (25–30%) | 8.1–8.4 |
| Design data storage solutions (20–25%) | 8.5–8.8 |
| Design business continuity solutions (15–20%) | 8.9–8.10 |
| Design infrastructure solutions (30–35%) | 8.11–8.17 |

Lab 8.18 is the negative test (a compliance guardrail enforces) and 8.19
is cleanup. Lab 8.14 also exercises the AZ-400 automated-deployment
surface.

### Lab coverage — Fundamentals

Mapped to the "Skills measured" domains of AZ-900, AI-901, and DP-900.
Labs are in [Chapter 02](chapters/02-fundamentals-az-900-ai-901-and-dp-900.md).

| Certification / domain | Labs |
| --- | --- |
| AZ-900 cloud concepts / architecture / governance | 2.1–2.3 |
| AI-901 AI workloads, ML, vision, NLP and generative AI | 2.4–2.7 |
| DP-900 core data, relational, non-relational, analytics | 2.8–2.11 |

Lab 2.12 is the negative test.

### Lab coverage — AZ-700 (Network Engineer)

Mapped to the AZ-700 "Skills measured" outline at Microsoft's weights.
Labs are in [Chapter 04](chapters/04-azure-network-engineer-az-700.md).

| Skills-measured domain (weight) | Labs |
| --- | --- |
| Core networking infrastructure (25–30%) | 4.1–4.3 |
| Connectivity services (20–25%) | 4.4–4.5 |
| Private access to Azure services (10–15%) | 4.6–4.7 |
| Network security services (15–20%) | 4.8–4.9 |
| Application delivery services (15–20%) | 4.10–4.12 |

Lab 4.13 is the negative test (peering non-transitivity) and 4.14 is cleanup.

### Lab coverage — The Retiring Associate Tier (AZ-204, AZ-500)

Mapped to both exam guides' domains. Both retire in 2026, but the subject
matter is current — the labs are professional development past the
credential dates. Labs are in
[Chapter 05](chapters/05-the-retiring-associate-tier-az-204-and-az-500.md).

| Certification / domain | Labs |
| --- | --- |
| AZ-500 identity and access | 5.1–5.2 |
| AZ-500 secure networking | 5.3 |
| AZ-500 secure compute/storage/databases | 5.4–5.5 |
| AZ-500 Defender for Cloud and Sentinel | 5.6–5.7 |
| AZ-204 develop compute solutions | 5.8–5.9 |
| AZ-204 develop for storage | 5.10 |
| AZ-204 implement security | 5.11 |
| AZ-204 connect to and consume services | 5.12 |
| AZ-204 monitor and troubleshoot | 5.13 |

Lab 5.14 is the negative test (Key Vault management vs. data-plane) and 5.15 is cleanup.

### Lab coverage — The AI-Centric Associate Tier (AI-103, AI-200, AB-620)

These certifications are new and their published skills outlines are still
thin, so labs cover the stated scope (Azure AI surface, Microsoft Foundry,
agent building) against what is verifiable today — **re-check each exam
guide**. Labs are in
[Chapter 06](chapters/06-the-ai-centric-associate-tier-ai-103-ai-200-and-ab-620.md).

| Scope | Labs |
| --- | --- |
| Azure AI service surface (AI-103 / AI-200) | 6.1–6.3 |
| Microsoft Foundry and model deployment (AI-103) | 6.4–6.5 |
| Agent building (AB-620) | 6.6 |
| Responsible AI / content safety (all) | 6.7 |

Lab 6.8 is the negative test (endpoint auth) and 6.9 is cleanup.

### Lab coverage — Data on Azure (DP-300, DP-420, DP-750)

DP-300 and DP-420 mapped domain by domain; DP-750 (new) at section level.
Labs are in [Chapter 07](chapters/07-data-on-azure-dp-300-dp-420-and-dp-750.md).

| Certification / domain | Labs |
| --- | --- |
| DP-300 plan/implement data platform | 7.1–7.2 |
| DP-300 secure environment | 7.3–7.4 |
| DP-300 monitor and optimize | 7.5–7.6 |
| DP-300 automation | 7.7 |
| DP-420 Cosmos DB (models, distribution, optimize, maintain) | 7.8–7.12 |
| DP-750 Databricks lakehouse | 7.13–7.14 |

Lab 7.15 is the negative test (firewall vs. database) and 7.16 is cleanup.

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
