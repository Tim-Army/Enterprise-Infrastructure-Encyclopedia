# Volume CXXVII — Netskope Certification Tracks

> The certification map for **Netskope** — the SASE/SSE platform — verified on netskope.com, 3 August
> 2026. The program runs a **free, vendor-agnostic SASE Accreditation** (an on-demand SASE-architecture
> course with a 45-minute, 80%-to-pass exam and a LinkedIn badge) as the on-ramp, then the **NCCSA**
> (Netskope Certified Cloud Security Administrator — exam **NSK101**, replacing NSK100; Pearson VUE, ~70
> questions, ~2 hours, 70% pass, **valid 2 years**) on the **Netskope One Administrator** course, and the
> **NCCSI** (Netskope Certified Cloud Security Integrator) on the **Netskope One Professional** course.
> The volume teaches both the **SASE/SSE frameworks** (SASE = SD-WAN + SSE; SSE = **CASB + SWG + ZTNA**,
> plus **DLP** and threat protection) and the **Netskope One** platform that implements them — the
> **NewEdge** network, traffic **steering**, inline-vs-API protection, app-instance-aware CASB, SWG with
> SSL inspection, DLP with pattern/EDM detection, and ZTNA's no-inbound broker/publisher model — with a
> walkthrough lab per exam objective. Because the concepts model cleanly on **free primitives** (a
> forward proxy, real regex DLP, a reverse-broker for ZTNA), every lab runs at no cost; the Netskope
> tenant appears at design level.

## Overview

Volume CXXVII is a **certification-tracks volume** organized around the SSE pillars the exams test. The
free, **vendor-agnostic** SASE Accreditation is treated as a genuine architecture course (useful beyond
Netskope); the **NCCSA** is mapped pillar-by-pillar — steering, CASB, SWG, DLP, ZTNA — each as a
runnable model; and the **NCCSI** adds the enterprise-integration surfaces (SAML/SSO, REST API,
IaaS/SSPM posture, advanced analytics). It sits alongside the encyclopedia's other cloud-security-edge
volumes ([Zscaler XXXV](../volume-035-zscaler-zero-trust-exchange/README.md), [Palo Alto
LXV](../volume-065-palo-alto-networks-certifications/README.md), [Fortinet
XIX](../volume-019-fortinet-network-security/README.md)) as the Netskope entry in the SASE/SSE market.

Its standing disciplines are honest currency — exam codes churn (NSK100 → NSK101), the SASE
Accreditation's free window is time-limited, and the platform rebranded to **Netskope One** — so the
volume flags re-verification on netskope.com before booking.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Netskope Certification Program and SASE/SSE Foundations](chapters/01-the-netskope-program-and-sase.md) | 1.1–1.2 |
| 02 | [The SASE Accreditation — SASE Architecture](chapters/02-sase-accreditation-architecture.md) | 2.1–2.4 |
| 03 | [NCCSA — The Netskope One Platform and Traffic Steering](chapters/03-nccsa-platform-and-steering.md) | 3.1–3.4 |
| 04 | [NCCSA — CASB and Cloud App Control](chapters/04-nccsa-casb-cloud-app-control.md) | 4.1–4.4 |
| 05 | [NCCSA — Secure Web Gateway and Threat Protection](chapters/05-nccsa-swg-web-security.md) | 5.1–5.4 |
| 06 | [NCCSA — Data Loss Prevention](chapters/06-nccsa-dlp-data-protection.md) | 6.1–6.4 |
| 07 | [NCCSA — ZTNA and Private Access](chapters/07-nccsa-ztna-private-access.md) | 7.1–7.4 |
| 08 | [NCCSI — Integration and Operations](chapters/08-nccsi-integration-and-operations.md) | 8.1–8.4 |
| 09 | [Choosing a Path, Currency, and Career](chapters/09-choosing-currency-and-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the Netskope program (SASE Accreditation → NCCSA → NCCSI) and its exam logistics.
- Explain SASE and SSE and the Netskope One platform (NewEdge, steering, inline vs API).
- Reason about and model each SSE control: CASB, SWG, DLP, and ZTNA.
- Integrate Netskope into the enterprise: SAML/SSO, REST API, IaaS/SSPM posture, and analytics.
- Keep a certification plan current through exam-code churn and platform evolution.

## Prerequisites

- Security, networking, and cloud fundamentals; [Volume X](../volume-010-enterprise-cybersecurity/README.md) for the defensive context.
- A Linux host with `squid`/`nginx`, `nftables`, and `python3` for the free labs.

## See also

- [Volume XXXV — Zscaler Zero Trust Exchange](../volume-035-zscaler-zero-trust-exchange/README.md), [Volume LXV — Palo Alto Certification Tracks](../volume-065-palo-alto-networks-certifications/README.md), [Volume XIX — Fortinet Network Security](../volume-019-fortinet-network-security/README.md) — the neighboring SASE/SSE platforms and certifications.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the segmentation landscape ZTNA's private-access model connects to.
- [Master Appendices — Netskope appendix](../volume-997-master-appendices/chapters/61-appendix-netskope-certifications-and-course-access.md) — the certifications, the free SASE Accreditation, and course access.
