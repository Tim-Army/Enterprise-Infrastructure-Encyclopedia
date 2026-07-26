# Volume XXXVIII — Microsoft Certifications Beyond Azure

> The whole of Microsoft's role-based certification program *outside* Azure
> in one volume: Microsoft 365, Security, Power Platform, Dynamics 365, Data
> and Analytics (Fabric), AI and Copilot, and GitHub — every tier, every
> exam code, verified against Microsoft Learn.

## Overview

Volume XXXVIII catalogs Microsoft's **role-based certification program
beyond Azure**. Azure itself is covered in
[Volume XXXIII — Microsoft Azure Certification Tracks](../volume-33-microsoft-azure-certifications/README.md);
this volume covers everything else Microsoft certifies: **Microsoft 365**,
**Security, Compliance, and Identity (SC)**, **Power Platform (PL)**,
**Dynamics 365 (MB)**, **Data and Analytics (DP, including Microsoft
Fabric)**, **AI and Copilot (AI)**, and **GitHub (GH)**. It is the third of
the encyclopedia's three Microsoft volumes, completing the set alongside the
hands-on [Volume XXXVI — Windows Server 2025 and Active Directory](../volume-36-windows-server-2025-active-directory/README.md)
and [Volume XXXVII — Microsoft 365 and Modern Work](../volume-37-microsoft-365-modern-work/README.md).

This is a **certification-tracks** volume, like Juniper (XXXI), Dell (XXXII),
Azure (XXXIII), and Google Cloud (XXXIV): its job is to map the program —
which credentials exist, their **tiers** (Fundamentals, Associate, Expert,
Specialty), their **exam codes** and blueprint domains, prerequisites,
renewal, and the study path to each — and to point at the hands-on volumes
(XXXVI, XXXVII) and Microsoft Learn for practice. Every exam code in this
volume was **verified against the Microsoft Learn catalog and individual
certification pages on 26 July 2026**, which is worth doing because
Microsoft's program changes constantly: the AI and agent family expanded
sharply, GitHub certifications now use **GH-** codes, and several security
exams were renumbered (SC-401 replacing SC-400, the new SC-500).

Chapters are organized by product family:

- **Chapter 01** frames the whole program — the role-based model, the four
  tiers, the Fundamentals gateway, Microsoft Learn, the exam experience, and
  renewal.
- **Chapters 02–08** each take a family: Microsoft 365; Security, Compliance,
  and Identity; Power Platform; Dynamics 365; Data and Analytics; AI and
  Copilot; and GitHub.
- **Chapter 09** covers keeping current — the annual renewal model, betas and
  retirements, the exam sandbox, and reading the program for change.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including a hands-on
exam-preparation lab and knowledge checks.

## Chapters

1. [The Microsoft Certification Program Beyond Azure](chapters/01-the-microsoft-certification-program-beyond-azure.md) — the role-based model, the four tiers, the Fundamentals gateway, Microsoft Learn, the exam experience, and free annual renewal.
2. [Microsoft 365 Certifications](chapters/02-microsoft-365-certifications.md) — MS-900, MS-102, MD-102, MS-700, and MS-721 across the Fundamentals, Administrator Expert, and specialist tiers.
3. [Security, Compliance, and Identity Certifications](chapters/03-security-compliance-and-identity-certifications.md) — SC-900, SC-300, SC-200, SC-401, SC-100, and the new SC-500.
4. [Power Platform Certifications](chapters/04-power-platform-certifications.md) — PL-900, PL-200, PL-300, PL-400, PL-500, and PL-600.
5. [Dynamics 365 Certifications](chapters/05-dynamics-365-certifications.md) — the Customer Engagement and Finance and Operations tracks, and Business Central.
6. [Data and Analytics Certifications](chapters/06-data-and-analytics-certifications.md) — DP-900, Microsoft Fabric (DP-700, DP-600), DP-300, DP-420, DP-100, and DP-750.
7. [AI and Copilot Certifications](chapters/07-ai-and-copilot-certifications.md) — AI-900/AI-901, AI-102, the AI apps/agents wave (AI-103, AI-500), and Copilot and agent administration.
8. [GitHub Certifications](chapters/08-github-certifications.md) — GitHub Foundations, Actions, Administration, Advanced Security, Copilot, and the new Agentic AI Developer.
9. [Keeping the Microsoft Program Current](chapters/09-keeping-the-microsoft-program-current.md) — renewal, betas and retirements, the exam sandbox, and reading the program for change.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Microsoft beyond Azure, recorded
in [CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The
full catalog with tiers, exam codes, retirements, the Microsoft Learn free
training model, and free annual renewal is in the
[Microsoft (beyond Azure) certification appendix](../volume-97-master-appendices/chapters/12-appendix-microsoft-beyond-azure-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Hands-on practice for these credentials
lives in Volumes XXXVI (Windows Server/AD) and XXXVII (Microsoft 365), and in
Volume XXXIII for the shared Azure and data/AI foundations.

## Lab coverage

The family chapters go **per topic**: there is **one walkthrough lab for every
weighted "skills measured" domain of every certification** — 199 domain labs in
all — plus the program and currency labs in Chapters 01 and 09. The weight for
each domain comes from that exam's Microsoft Learn study guide: M365 (21 labs
across MS-900/MS-102/MD-102/MS-700/MS-721), Security/Compliance/Identity (22:
SC-900/300/200/401/100/500), Power Platform (24: PL-900/200/300/400/500/600),
Dynamics 365 (52 across the MB exams that publish a study guide), Data and
Analytics (31: DP-900/700/600/300/420/100/750/800), AI and Copilot (20:
AI-901/102/103/500), and GitHub (29: GH-900/100/300/500/600). Because these are
Microsoft-platform skills, the walkthroughs use the appropriate tooling —
**Microsoft Graph PowerShell**, **Teams PowerShell**, **Azure CLI (`az`)**, the
**Power Platform CLI (`pac`)**, Dataverse Web API, X++/AL for Dynamics, and the
**GitHub CLI (`gh`)** — as illustrative commands against a developer tenant.
Each lab states an objective, commands, expected results, a negative test, and
cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **Microsoft Learn** (`learn.microsoft.com/credentials`),
the **Microsoft Learn Catalog API**, the **Pearson VUE** exam-delivery
platform, and **Credly** digital badges. Exam codes, blueprint domains, and
program structure were verified against Microsoft Learn on 26 July 2026;
Microsoft's program is continuously updated, so confirm current exam names,
numbers, and status on Microsoft Learn before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-38-microsoft-certifications-beyond-azure
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
