# Volume XL — ISC2 Certification Tracks

> The whole ISC2 certification program in one volume — CC, SSCP, CISSP and its
> ISSAP/ISSEP/ISSMP concentrations, CCSP, CGRC, and CSSLP — with a walkthrough
> lab for every weighted exam domain, verified against the official ISC2 exam
> outlines.

## Overview

Volume XL maps the **ISC2** program — the vendor-neutral **governance,
architecture, engineering, and management** tier of the security profession.
Where CompTIA (Volume XXXIX) validates foundational, hands-on skill domains and
the vendor tracks (Cisco, Palo Alto, Fortinet, Zscaler, the cloud providers)
validate implementation on specific products, ISC2 credentials — led by the
**CISSP** — validate the design and management of whole security programs. That
places this volume **above** the other certification tracks in the encyclopedia's
stack.

This is a **certification-tracks** volume, like CompTIA (XXXIX), Microsoft beyond
Azure (XXXVIII), Azure (XXXIII), Google Cloud (XXXIV), Juniper (XXXI), and Dell
(XXXII): its job is to map the program — which credentials exist, their place on
the **experience-gated ladder**, their **weighted exam domains**, mechanics,
prerequisites, endorsement, and renewal — and to teach each domain with a
hands-on walkthrough. Every domain and weight in this volume was **verified
against the official ISC2 exam outlines on 26 July 2026**, which matters because
ISC2 refreshes its outlines briskly: the **CISSP** changed in April 2024, **SSCP**
and **CGRC** in 2024, the **ISSAP/ISSEP/ISSMP** concentrations were all re-issued
**1 August 2025**, and **CCSP** and **CC** refreshes land in 2026.

Chapters are organized by credential, ascending the ladder:

- **Chapter 01** frames the whole program — the ladder, experience gates,
  endorsement, the Associate of ISC2, CAT exams, the Code of Ethics, and CPE/AMF
  renewal.
- **Chapters 02–08** each take a credential (or credential family): CC; SSCP;
  CISSP; the ISSAP/ISSEP/ISSMP concentrations; CCSP; CGRC; and CSSLP.
- **Chapter 09** covers keeping current — CPE and AMF, the Code of Ethics,
  outline refreshes and betas, the new AI Security certification, and career
  paths with DoD 8140/8570 mapping.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-domain
hands-on labs and knowledge checks.

## Chapters

1. [The ISC2 Certification Program](chapters/01-the-isc2-certification-program.md) — the credential ladder, experience gates, endorsement, the Associate of ISC2, CAT exams, the Code of Ethics, and CPE/AMF renewal.
2. [Certified in Cybersecurity (CC)](chapters/02-certified-in-cybersecurity-cc.md) — ISC2's free, no-experience entry credential; five domains, with a new outline effective 1 September 2026.
3. [Systems Security Certified Practitioner (SSCP)](chapters/03-systems-security-certified-practitioner-sscp.md) — hands-on security operations; seven evenly weighted domains on a CAT exam.
4. [Certified Information Systems Security Professional (CISSP)](chapters/04-certified-information-systems-security-professional-cissp.md) — the flagship; the eight-domain Common Body of Knowledge (2024 refresh).
5. [CISSP Concentrations — ISSAP, ISSEP, ISSMP](chapters/05-cissp-concentrations-issap-issep-issmp.md) — architecture, engineering, and management specializations (new outlines, 1 August 2025).
6. [Certified Cloud Security Professional (CCSP)](chapters/06-certified-cloud-security-professional-ccsp.md) — cloud-security architecture and operations, co-created with the Cloud Security Alliance (new outline 1 August 2026).
7. [Certified in Governance, Risk and Compliance (CGRC)](chapters/07-certified-in-governance-risk-and-compliance-cgrc.md) — the RMF and authorization credential, formerly CAP; seven domains.
8. [Certified Secure Software Lifecycle Professional (CSSLP)](chapters/08-certified-secure-software-lifecycle-professional-csslp.md) — secure software across the SDLC; eight domains including software supply chain.
9. [Keeping the ISC2 Program Current and Career Paths](chapters/09-keeping-the-isc2-program-current-and-career-paths.md) — CPE/AMF, the Code of Ethics, outline refreshes, the AI Security certification, and DoD 8140 mapping.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for ISC2, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full
catalog with the ladder, exam mechanics, experience requirements, endorsement,
the Code of Ethics, and CPE/AMF renewal is in the
[ISC2 certification appendix](../volume-997-master-appendices/chapters/14-appendix-isc2-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Foundational hands-on security practice for
these credentials lives across the encyclopedia — the cybersecurity (X), cloud
(XVII/XXXIII/XXXIV), and automation (IX) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for
every weighted exam domain of every ISC2 credential** — **56 domain labs** in
all — plus the program and currency labs in Chapters 01 and 09. The weight for
each domain comes from that credential's official ISC2 exam outline: CC (5:
26/10/22/24/18), SSCP (7: 16/15/15/14/9/16/15), CISSP (8:
16/10/13/13/13/12/13/10), the concentrations ISSAP (4), ISSEP (5), ISSMP (6),
CCSP (6: 17/20/17/17/16/13), CGRC (7: 16/10/14/17/16/14/13), and CSSLP (8:
12/11/13/15/14/14/11/10). Because ISC2 credentials are vendor-neutral, the
walkthroughs use portable security tooling — `openssl`, `python3`, `ss`/`ip`,
`journalctl`, POSIX ACLs, and illustrative cloud-CLI and secure-SDLC patterns —
as concrete demonstrations of each domain's concepts. Each lab states an
objective, commands, expected results, a negative test, and cleanup, and ends
with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references the official **ISC2** site (`isc2.org`), the **Pearson
VUE** exam-delivery platform, **Computer Adaptive Testing (CAT)**, and the ISC2
**exam outlines** that serve as each credential's blueprint. Domains, weights,
and exam mechanics were verified against isc2.org on 26 July 2026; ISC2 refreshes
its outlines on a Job Task Analysis cycle, so confirm the current outline and its
effective date before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-40-isc2-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
