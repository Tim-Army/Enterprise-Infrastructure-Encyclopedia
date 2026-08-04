# Volume CXXXI — Practical Offensive and Defensive Certification Tracks (HTB, TCM, INE)

> The certification map for the three leading **practical, hands-on** security certification providers —
> **Hack The Box (HTB Academy)**, **TCM Security**, and **INE Security** (formerly eLearnSecurity) —
> verified on their sites, 4 August 2026. What unites them is a **prove-it-by-doing** model: you are
> certified by working a **real exam lab** (a network, web app, Active Directory domain, or SOC
> scenario) and writing a **professional report**, not by answering multiple-choice questions. The
> volume spans their offensive tracks (HTB **CPTS/CWES/CAPE/CWPE/COAE**, TCM **PJPT/PNPT/PWPx/PORP/PMRP/
> PIPA/PAPA/PMPA**, INE **eJPT/eCPPT/eWPT/eWPTX/eMAPT/eAIS**) and — distinctively — their **defensive /
> blue-team** tracks (HTB **CDSA**, TCM **PSAA/PSAP/PHDA**, INE **eSOC/eIAMA/eEDA/eCIR/eCTHP/eCDFP**),
> plus the newest **AI/LLM security** certifications across all three (HTB COAE, co-developed with
> Google; TCM PAPA; INE eAIS). It is written as a **defensive, authorized-methodology** volume: every
> offensive technique is presented to be **understood, detected, prevented, and reported** — always in
> an **authorized, in-scope, educational** context only — and every lab is a free-Python model of the
> *methodology, detection, or fix* (attack-path graphs to defend, detection rules, IR timelines, secure
> coding, report structure), never operational tooling against real targets. **Authorization governs
> everything.**

## Overview

Volume CXXXI is a **certification-tracks volume** for the practical-assessment school of security
certification. Its thesis — hands-on exam labs plus a report prove job capability in a way
multiple-choice cannot — organizes the chapters by discipline rather than by provider: reconnaissance
(02), engagement methodology and reporting (03), network/Active Directory *defended* (04), web
application security (05), the blue-team half (SOC detection 06; IR/hunting/forensics 07), the emerging
AI/LLM frontier (08), and choosing a path with the ethics that govern it (09). Because the same
knowledge serves attack and defense, the volume treats offensive understanding as the route to better
defense throughout, and it repeats the non-negotiable frame: **only ever test what you own or have
signed, in-scope authorization to test.**

It sits alongside the encyclopedia's other security-certification volumes ([OffSec
XLIII](../volume-043-offensive-security-certifications/README.md), [GIAC
LXXIV](../volume-074-giac-certifications/README.md), [EC-Council
LXXV](../volume-075-ec-council-certifications/README.md), [ISC2
XL](../volume-040-isc2-certifications/README.md)), contributing the practical, prove-it-by-doing model
and the red-and-blue span.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Practical Certification Landscape (HTB, TCM, INE)](chapters/01-the-practical-cert-landscape.md) | 1.1–1.2 |
| 02 | [Reconnaissance and OSINT](chapters/02-reconnaissance-and-osint.md) | 2.1–2.3 |
| 03 | [The Penetration Test Methodology and Reporting](chapters/03-methodology-and-reporting.md) | 3.1–3.3 |
| 04 | [Network and Active Directory Attack Paths — Defended](chapters/04-network-and-active-directory.md) | 4.1–4.3 |
| 05 | [Web Application Security](chapters/05-web-application-security.md) | 5.1–5.3 |
| 06 | [Blue Team — SOC Analysis and Detection](chapters/06-blue-team-soc-detection.md) | 6.1–6.3 |
| 07 | [Blue Team — Incident Response, Threat Hunting, and Forensics](chapters/07-incident-response-hunting-forensics.md) | 7.1–7.3 |
| 08 | [AI and LLM Security — Red and Blue](chapters/08-ai-llm-security.md) | 8.1–8.3 |
| 09 | [Choosing a Path, Ethics and Authorization, and Career](chapters/09-choosing-ethics-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the three providers' practical certifications (offensive, defensive, and AI) and choose a path.
- Explain the engagement methodology and write a professional, actionable report.
- Understand network/AD and web attack paths well enough to detect, harden, and remediate them.
- Operate the blue-team disciplines: detection engineering, triage, correlation, IR, hunting, forensics.
- Reason about AI/LLM security from both sides, and internalize the authorization ethic that governs the field.

## Prerequisites

- Networking, Linux/Windows, and web fundamentals; [Volume X](../volume-010-enterprise-cybersecurity/README.md) for the defensive program.
- A Linux host with `python3` for the defensive-methodology labs; the providers' **sanctioned exam ranges** (or your own isolated lab VMs) for any hands-on offensive practice.

## See also

- [Volume XLIII — Offensive Security (OffSec)](../volume-043-offensive-security-certifications/README.md), [Volume LXXIV — GIAC (SANS)](../volume-074-giac-certifications/README.md), [Volume LXXV — EC-Council](../volume-075-ec-council-certifications/README.md) — peer offensive/authorized-testing programs.
- [Volume XL — ISC2](../volume-040-isc2-certifications/README.md), [Volume XXXIX — CompTIA](../volume-039-comptia-certification-tracks/README.md), [Volume X — Enterprise Cybersecurity](../volume-010-enterprise-cybersecurity/README.md) — governance and the broader defensive program.
- [Master Appendices — HTB/TCM/INE appendix](../volume-997-master-appendices/chapters/65-appendix-practical-offensive-certifications-and-course-access.md) — the certifications, training, and access.
