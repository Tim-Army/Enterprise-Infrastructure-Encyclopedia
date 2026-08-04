# Volume CXXXVIII — Everpure (formerly Pure Storage) Certification Tracks

> The certification map for **Everpure, Inc.** — the company formerly known as **Pure Storage** —
> verified on Everpure Academy and everpuredata.com, 4 August 2026. **The rebrand is recent and
> partial:** the company and its certifications are now "Everpure", while **FlashArray**,
> **FlashBlade**, **Portworx**, and **Evergreen** keep their names, the conference is still **Pure
> Accelerate**, and the academy — branded Everpure — is **still hosted at `academy.purestorage.com`**.
> The program offers **twelve IT Professional Certifications across four levels**: **Associate** Data
> Storage ($200); **Professional** FlashArray Storage, FlashBlade Storage, Portworx Enterprise, and
> Cyber Resilience ($300); **Specialist** FlashArray/FlashBlade Implementation, FlashArray/FlashBlade
> Support, Cloud, and Migration ($300); and **Expert** Platform Architect ($400). Exams are multiple
> choice, **online proctored with a webcam**, **closed book**, and training is not required because each
> is "designed to test your on-the-job experience." Certifications are **valid three years**, with two
> renewal paths worth planning around: the **Associate renews automatically** when any higher
> certification is earned, and **Continuing Everpure Education credits** apply to select FlashArray
> exams. The volume models the disciplines free in Python — no Everpure hardware required.

## Overview

Volume CXXXVIII is a **certification-tracks volume** organized by the disciplines the twelve exams test.
Chapter 02 covers purpose-built flash and the **Evergreen** non-disruptive upgrade model, including the
single-controller exposure windows an upgrade passes through. Chapter 03 covers FlashArray block storage
and the volume-to-host mapping rule that prevents corruption. Chapter 04 covers FlashBlade, file versus
object versus block, scale-out performance, and the AI/HPC bandwidth problem **FlashBlade//EXA** targets.
Chapter 05 separates data reduction from total efficiency and shows why ratios are workload properties.
Chapter 06 covers replication, deriving synchronous replication's metropolitan limit from the speed of
light, and the mediator that prevents split brain. Chapter 07 covers **cyber resilience**: immutability
that resists a compromised administrator, and retention sized against attacker dwell time. Chapter 08
covers **Portworx** and Kubernetes storage. Chapter 09 closes on certification choice and recertification.

Its place on the encyclopedia's storage shelf is alongside
[NetApp LXXXIV](../volume-084-netapp-certifications/README.md) and
[Dell XXXII](../volume-032-dell-technologies-certifications/README.md), with the cyber-resilience
material converging on [Rubrik CXXX](../volume-130-rubrik-certifications/README.md),
[Commvault CXXXIII](../volume-133-commvault-certifications/README.md), and
[Veeam LXXXV](../volume-085-veeam-certifications/README.md).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Everpure Program and the Rebrand](chapters/01-the-everpure-program-and-the-rebrand.md) | 1.1–1.2 |
| 02 | [All-Flash Architecture and the Evergreen Model](chapters/02-all-flash-architecture-and-evergreen.md) | 2.1–2.3 |
| 03 | [FlashArray Fundamentals](chapters/03-flasharray-fundamentals.md) | 3.1–3.3 |
| 04 | [FlashBlade and Unstructured Data](chapters/04-flashblade-and-unstructured-data.md) | 4.1–4.3 |
| 05 | [Data Reduction and Efficiency](chapters/05-data-reduction-and-efficiency.md) | 5.1–5.3 |
| 06 | [Data Protection and Replication](chapters/06-data-protection-and-replication.md) | 6.1–6.3 |
| 07 | [Cyber Resilience](chapters/07-cyber-resilience.md) | 7.1–7.3 |
| 08 | [Portworx and Cloud-Native Storage](chapters/08-portworx-and-cloud-native-storage.md) | 8.1–8.3 |
| 09 | [Choosing a Level, Recertification, and Career](chapters/09-choosing-a-level-recertification-career.md) | 9.1–9.2 |

## What you will be able to do

- Navigate the Pure Storage → Everpure rebrand, including which names and URLs did not change.
- Map the twelve certifications and sequence them so the Associate maintains itself.
- Sequence non-disruptive upgrades and size controllers so one can carry the whole workload.
- Provision block storage without creating the multi-host mapping that corrupts filesystems.
- Choose file, object, or block deliberately, and size scale-out storage to feed AI compute.
- Read data-reduction ratios honestly and forecast capacity per workload.
- Design replication to a stated RPO, and know why synchronous replication is metropolitan.
- Implement immutability that survives a compromised administrator, sized against dwell time.
- Run stateful Kubernetes workloads with the right access mode and replication factor.

## Prerequisites

- Storage and virtualization fundamentals; [Volume VI](../volume-006-enterprise-storage-data-protection/README.md) for the vendor-neutral basis.
- A Linux or macOS host with `python3` — every lab runs on the standard library, with no Everpure hardware.

## See also

- [Volume LXXXIV — NetApp](../volume-084-netapp-certifications/README.md), [Volume XXXII — Dell Technologies](../volume-032-dell-technologies-certifications/README.md) — the peer storage programs.
- [Volume CXXX — Rubrik](../volume-130-rubrik-certifications/README.md), [Volume CXXXIII — Commvault](../volume-133-commvault-certifications/README.md), [Volume LXXXV — Veeam](../volume-085-veeam-certifications/README.md) — where the cyber-resilience material converges.
- [Volume XLI — CNCF and Kubernetes](../volume-041-cncf-kubernetes-certifications/README.md) — context for Portworx; [Volume V — VMware](../volume-005-vmware-virtualization/README.md) for the virtualization workloads.
- [Master Appendices — Everpure appendix](../volume-997-master-appendices/chapters/72-appendix-everpure-purestorage-certifications-and-course-access.md) — certifications, levels, and access.
