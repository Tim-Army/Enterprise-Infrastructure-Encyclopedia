# Volume LI — Nutanix Certification Tracks

> The whole Nutanix University certification program in one volume — the Associate
> (NCA), the Professional tracks (NCP-MCI, NCP-MCA, NCP-DB, NCP-US, NCP-CI-AWS,
> NCP-CI-Azure), the Master (NCM-MCI), and the Expert design credential (NCX-MCI) —
> with hands-on `ncli`/`acli`/Prism-API labs mapped to every blueprint section,
> verified against nutanix.com.

## Overview

Volume LI maps the **Nutanix** certification program — the credentials for operating
and designing the **Nutanix Cloud Platform** (NCI/AHV/AOS/Prism, unified storage,
database services, automation, and NC2 cloud clusters). It sits with the
encyclopedia's **virtualization and HCI** volumes (VMware, V; Proxmox, XXVI) and the
**cloud** volumes where NC2 runs (AWS, XVII; Azure, XXXIII).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–L):
it maps the program — which credentials exist, their **blueprint sections**, and
levels — and teaches each with a hands-on walkthrough. Every credential was
**verified against nutanix.com on 27 July 2026**, which matters because the program
moves with the platform: since **1 August 2025 all certifications are valid three
years** (up from two), and version **7.5** exams launched for **NCA** and
**NCP-MCI** in 2026.

Chapters are organized by credential and level:

- **Chapter 01** frames the program — the platform, the four levels, Pearson VUE
  delivery, three-year validity, and Community Edition.
- **Chapter 02** takes the Associate **NCA**.
- **Chapters 03–07** take the Professional tracks: **NCP-MCI** (Infrastructure),
  **NCP-MCA** (Automation), **NCP-DB** (Database), **NCP-US** (Unified Storage), and
  **NCP-CI** (Cloud Integration — NC2 on AWS and Azure).
- **Chapter 08** takes the Master **NCM-MCI**.
- **Chapter 09** takes the Expert **NCX-MCI** as design exercises.
- **Chapter 10** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-section
hands-on labs (or design exercises) and knowledge checks.

## Chapters

1. [The Nutanix Certification Program](chapters/01-the-nutanix-certification-program.md) — the platform, the four levels, and blueprint guides.
2. [NCA — Nutanix Certified Associate](chapters/02-nca-nutanix-certified-associate.md) — solutions/tools, administration, cluster maintenance, health.
3. [NCP-MCI — Multicloud Infrastructure](chapters/03-ncp-mci-multicloud-infrastructure.md) — clusters, storage, networking/Flow, performance, alerts, VMs.
4. [NCP-MCA — Multicloud Automation](chapters/04-ncp-mca-multicloud-automation.md) — Self-Service (Calm), blueprints, runbooks, X-Play playbooks.
5. [NCP-DB — Database Automation](chapters/05-ncp-db-database-automation.md) — Nutanix Database Service (NDB), Time Machine, clones.
6. [NCP-US — Unified Storage](chapters/06-ncp-us-unified-storage.md) — Files, Objects, Volumes, Data Lens.
7. [NCP-CI — Cloud Integration (NC2 on AWS and Azure)](chapters/07-ncp-ci-cloud-integration-nc2-aws-and-azure.md) — plan, deploy, configure, manage NC2.
8. [NCM-MCI — Master Multicloud Infrastructure](chapters/08-ncm-mci-master-multicloud-infrastructure.md) — advanced admin, data protection, security, workloads.
9. [NCX-MCI — Expert Design](chapters/09-ncx-mci-expert-design.md) — customer consultation, logical design, physical design.
10. [Keeping the Nutanix Program Current and Career Paths](chapters/10-keeping-the-nutanix-program-current-and-career-paths.md) — renewal, versions, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all ten chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Nutanix, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with credentials, blueprint sections, and the Nutanix University training model is in
the
[Nutanix certification appendix](../volume-997-master-appendices/chapters/25-appendix-nutanix-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the VMware (V), Proxmox
(XXVI), and cloud volumes.

## Lab coverage

The credential chapters go **per section**: there is **one walkthrough lab for every
blueprint section** of each Nutanix credential — **40 section labs** plus **3 design
exercises** for the expert credential and the program/currency labs, for **43
hands-on items** in all. Because Nutanix is a hands-on platform, the walkthroughs use
real tooling — the **Nutanix CLI (`ncli`)**, the **Acropolis CLI (`acli`)**, the
**Prism REST API (v3/v4)**, the **NDB API**, and cloud CLIs for NC2 — runnable on
**Community Edition** where possible. The expert chapter (NCX-MCI) uses **design
exercises** in the style of the CCDE volume (XXX). Each lab states an objective,
commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **nutanix.com/support-services/training-certification**
(catalog and blueprint guides), the **Nutanix Cloud Platform** (NCI/AHV/AOS/Prism),
**Community Edition** for practice, and **Pearson VUE** exam delivery. Credentials and
blueprints were verified against nutanix.com on 27 July 2026; Nutanix revises exams by
version (NCA/NCP-MCI 7.5 are current), so confirm the current blueprint before
scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-51-nutanix-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
