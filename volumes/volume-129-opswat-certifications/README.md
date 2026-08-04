# Volume CXXIX — OPSWAT Certification Tracks

> The certification map for **OPSWAT** — the **Critical Infrastructure Protection (CIP)** vendor —
> verified on opswatacademy.com, 4 August 2026. The **OPSWAT Academy** runs a distinctive **free-first**
> program (foundational and Associate certifications are free, explicitly to close the CIP skills gap)
> across four tracks — **CIP Essentials**, **CyberOps**, **OPSWAT Product Training**, and **End-User
> Guides**. The Associate ladder — **ICIP** (Introduction to CIP), **OCFA** (Cybersecurity Fundamentals),
> **OFSA** (File Security), **OECA** (Endpoint Compliance), **ONSA** (Network Security), **OSSA** (Secure
> Storage) — builds the vendor-neutral CIP foundation into the paid **MetaDefender** product
> **Professional** certifications (Core, ICAP, Kiosk, MFT) and the **OPSWAT OT Security Expert**
> designation; badges issue on **Credly** with **ISC2 CPE** credit, and some carry a validity window. The
> volume teaches OPSWAT's signature defenses — **Deep CDR** (Content Disarm and Reconstruction),
> **Multiscanning** (many engines in parallel), Proactive DLP, endpoint posture/NAC, and secure data
> transfer across trust boundaries (**Kiosk** media scanning into air-gapped OT, **Vault** secure
> storage) — and drills each with a **defensive** walkthrough lab. Because the certifications are
> concept-and-product, every lab **models** the techniques (a working CDR that strips active content, a
> multiscanning aggregator, posture/NAC decisions, a scan-before-cross boundary) with **free Python** —
> no OPSWAT software or license required.

## Overview

Volume CXXIX is a **certification-tracks volume** organized around OPSWAT's CIP boundaries: the file
boundary (Chapters 03–04, OFSA), the device and network boundaries (05–06, OECA/ONSA), and the OT
data-transfer boundary (07, OSSA), then the MetaDefender Professional/Expert tier (08) and the CyberOps
track (09), all grounded in CIP fundamentals (02). It is a **defensive** volume — every technique is
about keeping weaponized files and untrusted devices out of critical infrastructure — and it pairs
directly with [Volume CXXVIII (ISA/IEC 62443)](../volume-128-isa-iec-62443-certifications/README.md):
62443 gives the standard and lifecycle, OPSWAT gives the boundary technology that implements it.

Its standing disciplines are the "trust no file, no device" premise, defense-in-depth (no single control
suffices), and honest currency (the free-first model shifts and some certs expire — re-verify).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The OPSWAT Academy and Critical Infrastructure Protection](chapters/01-the-opswat-academy-and-cip.md) | 1.1–1.2 |
| 02 | [CIP Fundamentals (ICIP / OCFA)](chapters/02-cip-fundamentals.md) | 2.1–2.3 |
| 03 | [File Security (OFSA) — Content Disarm and Reconstruction](chapters/03-file-security-cdr.md) | 3.1–3.3 |
| 04 | [File Security (OFSA) — Multiscanning, DLP, and Analysis](chapters/04-file-security-multiscanning.md) | 4.1–4.3 |
| 05 | [Endpoint Compliance (OECA)](chapters/05-endpoint-compliance.md) | 5.1–5.3 |
| 06 | [Network Security (ONSA)](chapters/06-network-security.md) | 6.1–6.3 |
| 07 | [Secure Data Flow into OT (OSSA, Kiosk, Vault)](chapters/07-secure-data-flow-ot.md) | 7.1–7.3 |
| 08 | [MetaDefender Professional and OT Security Expert](chapters/08-metadefender-professional-ot-expert.md) | 8.1–8.3 |
| 09 | [The CyberOps Track, Choosing a Path, and Currency](chapters/09-cyberops-choosing-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the OPSWAT Academy program (free-first Associates, MetaDefender Professionals, OT Security Expert).
- Explain and model Deep CDR, multiscanning, and Proactive DLP at the file boundary.
- Reason about endpoint posture/NAC and secure data flow into air-gapped OT.
- Place the MetaDefender products (Core, ICAP, Kiosk, MFT, Vault) in a CIP architecture.
- Build a free-first, role-aligned certification plan and keep it current.

## Prerequisites

- Security fundamentals; [Volume X](../volume-010-enterprise-cybersecurity/README.md) for context and [Volume CXXVIII](../volume-128-isa-iec-62443-certifications/README.md) for the OT standard.
- A Linux host with `python3` (and `nftables`/`iproute2` for the network labs) for the free labs.

## See also

- [Volume CXXVIII — ISA/IEC 62443](../volume-128-isa-iec-62443-certifications/README.md) — the standard OPSWAT's boundary controls implement.
- [Volume CXIII — Claroty](../volume-113-claroty-xdome-lab/README.md), [Volume CXIV — Nozomi](../volume-114-nozomi-networks-lab/README.md), [Volume CXV — TXOne](../volume-115-txone-networks-lab/README.md) — OT monitoring inside the network.
- [Master Appendices — OPSWAT appendix](../volume-997-master-appendices/chapters/63-appendix-opswat-certifications-and-course-access.md) — the certifications, the free-first model, and course access.
