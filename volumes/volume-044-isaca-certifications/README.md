# Volume XLIV — ISACA Certification Tracks

> The whole ISACA certification program in one volume — CISA, CISM, CRISC,
> CGEIT, CDPSE, the hands-on CCOA, and the new Advanced in AI family (AAIA,
> AAISM, AAIR) — with a walkthrough lab for every weighted job-practice domain,
> verified against ISACA's exam content outlines.

## Overview

Volume XLIV maps the **ISACA** program — the vendor-neutral **audit, governance,
and risk** tier of the profession. Where ISC2 (Volume XL) certifies security
architecture, engineering, and management, ISACA owns the **audit and governance**
quadrant: **CISA** (audit), **CISM** (security management), **CRISC** (risk),
**CGEIT** (enterprise IT governance), and **CDPSE** (data-privacy engineering).
Together with ISC2 it completes the governance-and-management tier that sits
*above* the CompTIA and vendor tracks.

This is a **certification-tracks** volume, like CompTIA (XXXIX), ISC2 (XL),
CNCF/Kubernetes (XLI), HashiCorp (XLII), and OffSec (XLIII): it maps the program —
which credentials exist, their **weighted job-practice domains**, exam mechanics,
experience requirements, and CPE maintenance — and teaches each domain with a
hands-on walkthrough. Every domain and weight was **verified against ISACA's exam
content outlines on 26 July 2026**, which matters because the program changed
substantially: ISACA added the hands-on **CCOA** analyst certification and a whole
**Advanced in AI family** (AAIA, AAISM, AAIR), refreshed **CDPSE** from three to
four domains (June 2025), and updated **CRISC** (2025).

Chapters are organized by credential:

- **Chapter 01** frames the program — the classic certifications, CCOA, the AI
  family, the CMMC roles, job-practice domains, and CPE maintenance.
- **Chapters 02–06** take the classic certifications: CISA, CISM, CRISC, CGEIT,
  and CDPSE.
- **Chapter 07** covers the hands-on CCOA.
- **Chapter 08** covers the Advanced in AI family (AAIA, AAISM, AAIR).
- **Chapter 09** covers the CMMC roles, certificate programs, and keeping current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-domain
hands-on labs and knowledge checks.

## Chapters

1. [The ISACA Certification Program](chapters/01-the-isaca-certification-program.md) — the credential map, job-practice domains, experience verification, and CPE maintenance.
2. [Certified Information Systems Auditor (CISA)](chapters/02-certified-information-systems-auditor-cisa.md) — the benchmark IS-audit credential; five domains.
3. [Certified Information Security Manager (CISM)](chapters/03-certified-information-security-manager-cism.md) — security-program management; four domains.
4. [Certified in Risk and Information Systems Control (CRISC)](chapters/04-certified-in-risk-and-information-systems-control-crisc.md) — IT risk; four domains (2025 update).
5. [Certified in the Governance of Enterprise IT (CGEIT)](chapters/05-certified-in-the-governance-of-enterprise-it-cgeit.md) — enterprise IT governance; four domains.
6. [Certified Data Privacy Solutions Engineer (CDPSE)](chapters/06-certified-data-privacy-solutions-engineer-cdpse.md) — privacy-by-design engineering; four domains (June 2025 refresh).
7. [Certified Cybersecurity Operations Analyst (CCOA)](chapters/07-certified-cybersecurity-operations-analyst-ccoa.md) — the hands-on SOC-analyst credential; five domains, hybrid exam.
8. [Advanced in AI — AAIA, AAISM, and AAIR](chapters/08-advanced-in-ai-aaia-aaism-aair.md) — AI audit, AI security management, and AI risk.
9. [CMMC Roles, Certificates, and Keeping Current](chapters/09-cmmc-certificates-and-keeping-current.md) — the CMMC ecosystem, certificate programs, CPE, and career paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for ISACA, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with the credentials, weighted domains, exam mechanics, experience requirements,
CPE maintenance, and the CMMC/certificate programs is in the
[ISACA certification appendix](../volume-997-master-appendices/chapters/18-appendix-isaca-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related governance and security practice lives
in Volume XL (ISC2), Volume X (Cybersecurity), and Volume XXXIX (CompTIA).

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for
every weighted job-practice domain of every ISACA credential** — **35 domain
labs** in all — plus the program and currency labs in Chapters 01 and 09. The
weight for each domain comes from that credential's ISACA exam content outline:
CISA (5: 18/18/12/26/26), CISM (4: 17/20/33/30), CRISC (4: 26/22/32/20), CGEIT
(4: 40/15/26/19), CDPSE (4: 20/18/23/39), CCOA (5 domains, hands-on), and the
Advanced in AI family AAIA (3), AAISM (3: 31/31/38), and AAIR (3). Because ISACA
credentials are governance-and-audit disciplines, most walkthroughs **model the
artifacts and decisions** of the role — audit plans, risk registers, control
mappings, KRIs, privacy engineering, and AI-governance controls — in `python`,
while the hands-on CCOA chapter uses real shell analysis (`ss`, `journalctl`,
`curl`). Each lab states an objective, commands, expected results, a negative
test, and cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **isaca.org** (credentialing and exam content outlines),
the **COBIT** governance framework, and the **PSI** exam-delivery platform.
Domains, weights, and program structure were verified against ISACA on 26 July
2026; ISACA updates its job-practice outlines and adds credentials, so confirm the
current outline and its effective date before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-044-isaca-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
