# Volume CXXVIII — ISA/IEC 62443 Certification Tracks

> The certification map for **ISA/IEC 62443** — the consensus standard for **Industrial Automation and
> Control Systems (IACS)** cybersecurity — verified on isa.org, 4 August 2026. The **ISA/IEC 62443
> Cybersecurity Certificate Program** is a four-certificate ladder mapped to the IACS security
> lifecycle: **Certificate 1, Cybersecurity Fundamentals Specialist** (course **IC32**), is the
> mandatory gate; then **Certificate 2, Risk Assessment Specialist** (**IC33**, Assess), **Certificate
> 3, Design Specialist** (**IC34**, Design), and **Certificate 4, Maintenance Specialist** (**IC37**,
> Operate/Maintain) may be taken in any order. Earning all four **automatically** confers the **ISA/IEC
> 62443 Cybersecurity Expert** designation; the credentials **do not expire**. The volume teaches the
> standard's load-bearing mechanics — **zones and conduits**, **security levels (SL 0–4)** as a vector
> across the **seven foundational requirements (FR1–FR7)**, the Purdue reference model, and the
> availability/safety-first OT priority inversion — and walks the whole lifecycle: high-level and
> detailed **risk assessment** (SL-Target), **design** (Cybersecurity Requirements Specification,
> segmentation, compensating controls, SL-Achieved), and **maintenance** (OT patching, passive
> monitoring, change-driven SL decay). Because 62443 is a standards/design certification, every lab
> **models** its concepts with **free Linux primitives** (namespaces as zones, nftables as conduits,
> Python for SL and risk scoring) — no OT hardware or ISA software required.

## Overview

Volume CXXVIII is a **certification-tracks volume** and the **standards-and-lifecycle** layer above the
encyclopedia's OT product volumes. It is organized the way the program is: a Fundamentals gate
(Chapters 02–03) establishing zones/conduits/SL/FR, then the three lifecycle specialists — Risk
Assessment (04–05), Design (06–07), and Maintenance (08) — each a runnable model of its phase, closing
with the Expert path (09). Where the OT product volumes ([Claroty CXIII](../volume-113-claroty-xdome-lab/README.md),
[Nozomi CXIV](../volume-114-nozomi-networks-lab/README.md), [TXOne CXV](../volume-115-txone-networks-lab/README.md),
[Forescout XV](../volume-015-forescout-platform-certifications/README.md), [Xage CXII](../volume-112-xage-security-lab/README.md))
show *how* tools implement OT security, this volume gives the *standard and lifecycle* that decide *what*
protection is required and *why*.

Its standing disciplines are the OT priority inversion (availability/safety before confidentiality),
traceability (every control back to an FR/SL/standard part), and honest currency (the credentials do not
expire, but the standard evolves — re-read the current editions).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The ISA/IEC 62443 Program and the Standard](chapters/01-the-program-and-the-standard.md) | 1.1–1.2 |
| 02 | [Fundamentals (IC32) — Core Concepts and the Reference Model](chapters/02-fundamentals-concepts.md) | 2.1–2.3 |
| 03 | [Fundamentals (IC32) — Zones, Conduits, Security Levels, and Foundational Requirements](chapters/03-fundamentals-zones-and-security-levels.md) | 3.1–3.3 |
| 04 | [Risk Assessment (IC33) — High-Level Assessment](chapters/04-risk-assessment-high-level.md) | 4.1–4.3 |
| 05 | [Risk Assessment (IC33) — Detailed Assessment and Target Security Levels](chapters/05-risk-assessment-detailed.md) | 5.1–5.3 |
| 06 | [Design (IC34) — Cybersecurity Requirements and Zone/Conduit Design](chapters/06-design-requirements.md) | 6.1–6.3 |
| 07 | [Design (IC34) — Countermeasures and Verifying Security Levels](chapters/07-design-countermeasures.md) | 7.1–7.3 |
| 08 | [Maintenance (IC37) — Operations and Maintenance](chapters/08-maintenance-operations.md) | 8.1–8.3 |
| 09 | [The Expert Path, Currency, and Career](chapters/09-expert-path-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the four-certificate program and the automatic Expert designation.
- Explain zones, conduits, security levels (as an FR vector), and the OT priority inversion.
- Run a high-level and detailed IACS risk assessment and determine SL-Targets.
- Produce a traceable Cybersecurity Requirements Specification and a segmented zone/conduit design with compensating controls.
- Maintain SL-Achieved through OT patching, passive monitoring, and change verification.

## Prerequisites

- Networking and security fundamentals; [Volume X](../volume-010-enterprise-cybersecurity/README.md) for the defensive context and the OT product volumes for tooling.
- A Linux host with `nftables`, `iproute2`, `netcat`, and `python3` for the free labs.

## See also

- [Volume XV — Forescout](../volume-015-forescout-platform-certifications/README.md), [Volume CXII — Xage](../volume-112-xage-security-lab/README.md), [Volume CXIII — Claroty](../volume-113-claroty-xdome-lab/README.md), [Volume CXIV — Nozomi](../volume-114-nozomi-networks-lab/README.md), [Volume CXV — TXOne](../volume-115-txone-networks-lab/README.md) — the OT products that implement 62443's controls.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — zones and conduits realized as products.
- [Master Appendices — ISA/IEC 62443 appendix](../volume-997-master-appendices/chapters/62-appendix-isa-iec-62443-certifications-and-course-access.md) — the certificates, courses, and access.
