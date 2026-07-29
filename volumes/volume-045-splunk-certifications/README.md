# Volume XLV — Splunk Certification Tracks

> The whole Splunk certification program in one volume — the Core (SPL) track,
> Administration, Architecture, the Cybersecurity Defense track, and Observability
> — with SPL and administration walkthrough labs mapped to every exam blueprint
> topic area, verified against splunk.com.

## Overview

Volume XLV maps the **Splunk** (now a **Cisco company**) certification program —
the credentials for turning machine data into searchable insight with the
**Search Processing Language (SPL)**, and for administering, securing, and
observing systems with Splunk. These credentials sit alongside the encyclopedia's
**observability (XI)**, **visibility (XVIII, XX)**, and security volumes.

This is a **certification-tracks** volume, like CompTIA (XXXIX), ISC2 (XL),
CNCF/Kubernetes (XLI), HashiCorp (XLII), OffSec (XLIII), and ISACA (XLIV): it maps
the program — which credentials exist, their **blueprint topic areas and weights**,
prerequisites, and delivery — and teaches each with a hands-on SPL or
administration walkthrough. Every track and blueprint was **verified against
splunk.com on 26 July 2026**, which matters because the program changed: Splunk was
acquired by **Cisco (2024)**, added the **Advanced Power User**, and built out a
full **Cybersecurity Defense** track (Analyst, Engineer, Architect).

Chapters are organized by track:

- **Chapter 01** frames the program — the tracks, SPL, test blueprints, Pearson VUE,
  and the Cisco era.
- **Chapters 02–03** take the Core (SPL) track: User/Power User and Advanced Power
  User.
- **Chapters 04–05** take Administration (Enterprise/Cloud Admin) and Architecture
  (Architect/Consultant).
- **Chapters 06–07** take the Cybersecurity Defense track: Analyst, then Engineer
  and Architect.
- **Chapter 08** covers the specialist platforms (Observability, SOAR, ITSI,
  Enterprise Security).
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic
hands-on labs and knowledge checks.

## Chapters

1. [The Splunk Certification Program](chapters/01-the-splunk-certification-program.md) — the tracks, SPL, test blueprints, Pearson VUE, and the Cisco era.
2. [Core Certified User and Power User](chapters/02-core-certified-user-and-power-user.md) — the SPL foundation; the ten Power User topic areas.
3. [Core Certified Advanced Power User](chapters/03-core-certified-advanced-power-user.md) — advanced SPL, acceleration, tuning, and dashboards.
4. [Enterprise Admin and Cloud Admin](chapters/04-enterprise-admin-and-cloud-admin.md) — configuration, indexes, users/auth, and forwarders.
5. [Enterprise Architect and Consultant](chapters/05-enterprise-architect-and-consultant.md) — distributed design, clustering, sizing, and troubleshooting.
6. [Certified Cybersecurity Defense Analyst](chapters/06-cybersecurity-defense-analyst.md) — SOC detection and investigation with SPL and Enterprise Security.
7. [Cybersecurity Defense Engineer and Architect](chapters/07-cybersecurity-defense-engineer-and-architect.md) — detection engineering, threat intel, SOAR, and security architecture.
8. [Observability, SOAR, ITSI, and Enterprise Security](chapters/08-observability-soar-itsi-and-enterprise-security.md) — the specialist platform credentials.
9. [Keeping the Splunk Program Current and Career Paths](chapters/09-keeping-the-splunk-program-current-and-career-paths.md) — renewal, the Cisco era, and career paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Splunk, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with tracks, blueprint topic areas, prerequisites, delivery, and renewal is in the
[Splunk certification appendix](../volume-997-master-appendices/chapters/19-appendix-splunk-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related observability and security practice
lives in Volume XI (Observability), Volume X (Cybersecurity), and the visibility
volumes (XVIII, XX).

## Lab coverage

The track chapters go **per topic**: there is **one walkthrough lab for every
exam-blueprint topic area** of each Splunk credential (consolidating the finest
sub-topics of the largest exams) — roughly **55 topic-area labs** across the
program — plus the program and currency labs in Chapters 01 and 09. Weights come
from each credential's Splunk test blueprint (for example, Power User: Correlating
Events 15%, Data Models and CIM 20% combined; Enterprise Admin: Indexes,
Distributed Search, and Forwarder Management 10% each). Because Splunk is an
SPL-driven platform, the walkthroughs use **illustrative SPL searches** and
**administration configuration** you can adapt to a Splunk trial or Splunk Cloud
instance. Each lab states an objective, commands, expected results, a negative
test, and cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **splunk.com** (Training & Certification and test
blueprints), the **SPL** search language, **Splunk Enterprise / Splunk Cloud**,
**Splunk Enterprise Security**, **SOAR**, **ITSI**, **Splunk Observability Cloud**
(OpenTelemetry), and **Pearson VUE** delivery. Tracks and blueprints were verified
against splunk.com on 26 July 2026; Splunk updates its blueprints and tracks, so
confirm the current blueprint before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-045-splunk-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
