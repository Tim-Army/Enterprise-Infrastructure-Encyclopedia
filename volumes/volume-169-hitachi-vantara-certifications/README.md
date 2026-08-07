# Volume CLXIX — Hitachi Vantara Certification Tracks

> The Hitachi Vantara Certified Professional (HVCP) program — verified 6 August 2026 on
> `hitachivantara.com/services/learning/certifications`. Hitachi Vantara is the **data-infrastructure** arm of
> Hitachi — enterprise **storage** (the **VSP** Virtual Storage Platform), data protection, **Hitachi Ops Center**
> management, and **Pentaho** data software. Certifications split into two categories — **Qualification** credentials
> (**HQT-** exams; **Associate**/**Professional**; medium-stakes, some open-book) and **Certification** credentials
> (**HCE-** exams; **Specialist**/**Expert**; high-stakes, **proctored**, hands-on) — across tracks: block/file/object
> storage, data protection, Ops Center, Pentaho, and converged/UCP. Exams like **HQT-6742** are **35 Q / 60 min /
> 65% / $100**; credentials are valid **2–3 years**. Every lab runs **free** in Python. An enterprise-storage /
> data-infrastructure volume.

## Overview

**Hitachi Vantara** is enterprise **data infrastructure** — the reliable **storage** that holds mission-critical
data, the **protection** that keeps it safe, the **management** (Ops Center) that operates it at scale, and the
**data software** (Pentaho) that turns it into insight. Its flagship is the **VSP (Virtual Storage Platform)**
block-storage line, famous for reliability and **storage virtualization**. Hitachi Vantara sits alongside the
storage and data vendors this shelf covers ([NetApp LXXXIV](../volume-084-netapp-certifications/README.md),
[Dell XXXII](../volume-032-dell-technologies-certifications/README.md),
[Everpure CXXXVIII](../volume-138-everpure-purestorage-certifications/README.md)).

Chapter 02 covers **Hitachi storage and the VSP platform**. Chapters 03–08 take the tracks: **block storage
administration** (VSP 360, HQT-6742), **file and object storage**, **data protection and replication**, **Hitachi
Ops Center**, **Pentaho** data integration and analytics, and **converged/hyperconverged and hybrid cloud**.
Chapter 09 closes on choosing a path, with a capstone across the whole data-infrastructure stack.

A theme runs through it: **hold** (storage), **protect** (replication), **manage** (Ops Center), **archive**
(object/cloud), and **analyze** (Pentaho) — the enterprise data-infrastructure lifecycle.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Hitachi Vantara Certification Program](chapters/01-the-hitachi-vantara-program.md) | 1.1–1.2 |
| 02 | [Hitachi Storage and the VSP Platform](chapters/02-hitachi-storage-and-vsp.md) | 2.1 |
| 03 | [Block Storage Administration](chapters/03-block-storage-administration.md) | 3.1 |
| 04 | [File and Object Storage](chapters/04-file-and-object-storage.md) | 4.1 |
| 05 | [Data Protection and Replication](chapters/05-data-protection-and-replication.md) | 5.1 |
| 06 | [Hitachi Ops Center](chapters/06-hitachi-ops-center.md) | 6.1 |
| 07 | [Pentaho — Data Integration and Analytics](chapters/07-pentaho-data-and-analytics.md) | 7.1 |
| 08 | [Converged, Hyperconverged, and Hybrid Cloud](chapters/08-converged-and-cloud.md) | 8.1 |
| 09 | [Choosing Your Hitachi Vantara Path](chapters/09-choosing-your-hitachi-vantara-path.md) | 9.1–9.2 |

## The certifications

Two categories across the tracks:

| Category / level | Exams | Tracks |
| --- | --- | --- |
| **Qualification** — Associate, Professional | **HQT-xxxx** (medium-stakes, some open-book) | Block/File/Object storage · Data Protection · Ops Center · Pentaho · UCP |
| **Certification** — Specialist, Expert | **HCE-xxxx** (high-stakes, proctored, hands-on) | deeper domain mastery |

**Mechanics** (e.g. HQT-6742 VSP 360 Storage Administration): 35 questions · 60 minutes · 65% to pass · $100.
Credentials valid **2–3 years** depending on track.

## What you will be able to do

- Read the HVCP program — Qualification (HQT) vs Certification (HCE), the four levels, and the tracks.
- Explain the VSP platform — enterprise block storage, controllers/cache/RAID, and storage virtualization.
- Administer block storage — pools, LDEVs, thin provisioning, tiering, and capacity monitoring (VSP 360).
- Use file and object storage — NFS/SMB shares and Content Platform objects with metadata and WORM retention.
- Protect data — local snapshots/clones and remote replication (TrueCopy sync, Universal Replicator async), RPO/RTO.
- Operate at scale with Hitachi Ops Center — Administrator, Automator, Protector, Analyzer.
- Build Pentaho pipelines and analytics — PDI transformations/jobs and Business Analytics.
- Design converged/hyperconverged (UCP) and hybrid-cloud data infrastructure.

## Prerequisites

- Familiarity with servers, storage, and data-center concepts helps.
- A Linux or macOS host with `python3`. **Hitachi Vantara certifications** are delivered via the HVCP program
  (HQT qualification and HCE certification exams; valid 2–3 years).

## See also

- [Volume LXXXIV — NetApp](../volume-084-netapp-certifications/README.md), [Volume XXXII — Dell](../volume-032-dell-technologies-certifications/README.md), and [Volume CXXXVIII — Everpure](../volume-138-everpure-purestorage-certifications/README.md) — enterprise-storage peers.
- [Volume CXXX — Rubrik](../volume-130-rubrik-certifications/README.md) and [Volume CLVII — Cohesity](../volume-157-cohesity-certifications/README.md) — data-protection peers.
- [Volume CLXV — Informatica](../volume-165-informatica-certifications/README.md) and [Volume CLIV — Tableau](../volume-154-tableau-certifications/README.md) — data-integration/analytics peers (Pentaho's space).
