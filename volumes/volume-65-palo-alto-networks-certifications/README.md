# Volume LXV — Palo Alto Networks Certification Tracks

> The whole Palo Alto Networks role-based certification framework in one volume — the
> Foundational, Professional, Specialist, and Architect levels across the Network Security,
> Security Operations, and Cloud Security tracks — on PAN-OS, Cortex (XDR/XSIAM/XSOAR), and
> Prisma/Cortex Cloud, with hands-on, defensive walkthrough labs, verified against
> paloaltonetworks.com.

## Overview

Volume LXV maps the **Palo Alto Networks** certification program — the credentials for securing,
operating, and defending with Palo Alto's platform. It is the **certification companion** to
[Volume XVI — Palo Alto Networks Security](../../volume-16-palo-alto-networks-security/README.md),
which covers the product platform in depth; this volume follows the **exam blueprints**, one
walkthrough lab per role and domain. It joins the encyclopedia's security volumes (Cisco
Security XXV, Fortinet XIX, Zscaler XXXV, CrowdStrike L, Enterprise Cybersecurity X, ISC2 XL).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXIV): it maps
the program — the levels, tracks, and credentials — and teaches each with a hands-on walkthrough.
Palo Alto **restructured the program in 2025** from the legacy code-based exams
(PCNSA/PCNSE/PCCSE and the rest) into a **role-based framework**; every credential was **verified
against paloaltonetworks.com on 28 July 2026**.

Chapters follow the framework:

- **Chapter 01** frames the program — the four levels, three tracks, and the 2025 restructure.
- **Chapter 02** takes the shared **Foundational** tier.
- **Chapters 03–05** take the **Network Security** track (Professional/Analyst; NGFW/SD-WAN
  Engineer; SSE Engineer/Architect).
- **Chapters 06–07** take the **Security Operations** track (XDR; XSIAM/XSOAR).
- **Chapter 08** takes the **Cloud Security** track.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** Palo Alto's firewall, Cortex XDR/XSIAM, and XSOAR are defensive platforms. Every
> lab is **authorized administration, detection, hunting, incident response, or automation** —
> never an operational attack technique.

## Chapters

1. [The Palo Alto Networks Certification Program](chapters/01-the-palo-alto-networks-certification-program.md) — levels, tracks, the 2025 restructure.
2. [The Foundational Tier](chapters/02-foundational-tier.md) — Cybersecurity Apprentice and Practitioner.
3. [Network Security — Professional and Analyst](chapters/03-network-security-professional-and-analyst.md) — PAN-OS, App-ID/User-ID/Content-ID.
4. [NGFW Engineer and SD-WAN Engineer](chapters/04-ngfw-and-sd-wan-engineer.md) — HA, Panorama, NAT/decryption, Prisma SD-WAN.
5. [SSE Engineer and Network Security Architect](chapters/05-sse-engineer-and-network-security-architect.md) — Prisma Access/SASE, design.
6. [Security Operations — Professional and XDR](chapters/06-secops-professional-and-xdr.md) — Cortex XDR, XQL, hunting.
7. [XSIAM and XSOAR](chapters/07-xsiam-and-xsoar.md) — AI-driven SOC and playbook automation.
8. [Cloud Security — Professional and Engineer](chapters/08-cloud-security-professional-and-engineer.md) — Prisma/Cortex Cloud CNAPP, RQL, IaC.
9. [Keeping the Program Current and Career Paths](chapters/09-keeping-current-and-career-paths.md) — recert, the 2025 restructure, paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Palo Alto Networks, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with levels,
tracks, and the training model is in the
[Palo Alto Networks certification-tracks appendix](../volume-997-master-appendices/chapters/31-appendix-palo-alto-networks-certification-tracks-and-course-access.md)
(Master Appendices, Volume CMXCVII). The complementary product volume is
[Volume XVI](../../volume-16-palo-alto-networks-security/README.md); related practice lives in
the Cisco Security (XXV), Fortinet (XIX), Zscaler (XXXV), CrowdStrike (L), and Enterprise
Cybersecurity (X) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every role and
domain** across the tracks — **34 labs** in all. Because Palo Alto is a hands-on platform, the
walkthroughs use real, **defensive** tooling — the **PAN-OS CLI** and **XML/REST API**, the
**pan-os-python** SDK, **XQL** (Cortex XDR/XSIAM), **XSOAR** playbooks, and **RQL** (Prisma/Cortex
Cloud) plus IaC scanning — practiced in an **authorized** lab (VM-Series/PAN-OS, Cortex and
Prisma trials). Each lab states an objective, commands, expected results, a negative test, and
cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **paloaltonetworks.com** (the role-based framework), **PAN-OS** and
Panorama, **Prisma SD-WAN** and **Prisma Access**, **Cortex XDR/XSIAM/XSOAR**, and
**Prisma/Cortex Cloud**, with the PAN-OS API/pan-os-python, XQL, and RQL for automation. The
program was verified against paloaltonetworks.com on 28 July 2026; Palo Alto revises the program
and platform quickly, so confirm the current framework and blueprints before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-65-palo-alto-networks-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
