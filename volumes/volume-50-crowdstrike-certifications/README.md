# Volume L — CrowdStrike Certification Tracks

> The whole CrowdStrike Falcon certification program in one volume — the platform
> credentials (CCFA, CCFR, CCFH) and Next-Gen SIEM pair (CCSA, CCSE), plus the
> Identity (CCIS) and Cloud (CCCS) specialists — with hands-on FalconPy, CQL, and
> GraphQL labs mapped to every exam-guide domain, verified against crowdstrike.com.

## Overview

Volume L maps the **CrowdStrike Falcon** certification program — the credentials for
operating the **Falcon platform** across endpoint, Next-Gen SIEM, identity, and cloud
security. It sits with the encyclopedia's **security** volumes (Cybersecurity, X;
Zscaler, XXXV; Fortinet, XIX; Palo Alto, XVI) and the **data/observability** volumes
(Splunk, XLV) that neighbor Falcon's SIEM.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–
XLIX): it maps the program — which credentials exist, their **exam-guide domains**,
and roles — and teaches each with a hands-on walkthrough. Every credential was
**verified against crowdstrike.com on 27 July 2026**; the seven exam guides carry
recent revision dates (January–July 2026). CrowdStrike does **not** publish
percentage domain weights, so the volume provides **one walkthrough lab per
exam-guide domain**.

Chapters are organized by credential:

- **Chapter 01** frames the program — the Falcon platform, the seven-credential
  lineup, Pearson VUE delivery, and three-year validity.
- **Chapters 02–04** take the platform analyst path: **CCFA** (Administrator),
  **CCFR** (Responder), **CCFH** (Hunter).
- **Chapters 05–06** take the **Next-Gen SIEM** pair: **CCSA** (Analyst) and
  **CCSE** (Engineer).
- **Chapters 07–08** take the specialists: **CCIS** (Identity) and **CCCS** (Cloud).
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-domain
hands-on labs and knowledge checks. All content is **defensive** security:
authorized administration, detection, hunting, and response only.

## Chapters

1. [The CrowdStrike Falcon Certification Program](chapters/01-the-crowdstrike-falcon-certification-program.md) — the platform, the seven credentials, and exam guides.
2. [CCFA — Certified Falcon Administrator](chapters/02-ccfa-certified-falcon-administrator.md) — RBAC, sensors, host/group management, policy, rules, workflows.
3. [CCFR — Certified Falcon Responder](chapters/03-ccfr-certified-falcon-responder.md) — ATT&CK, detection analysis, event search/investigation, RTR.
4. [CCFH — Certified Falcon Hunter](chapters/04-ccfh-certified-falcon-hunter.md) — hypothesis-driven hunting with the CrowdStrike Query Language.
5. [CCSA — Certified SIEM Analyst](chapters/05-ccsa-certified-siem-analyst.md) — querying/analytics, detection logic, incident investigation, reporting.
6. [CCSE — Certified SIEM Engineer](chapters/06-ccse-certified-siem-engineer.md) — users, ingestion, parsing, content creation, automation.
7. [CCIS — Certified Identity Specialist](chapters/07-ccis-certified-identity-specialist.md) — Zero Trust identity, risk, policy rules, connectors, GraphQL.
8. [CCCS — Certified Cloud Specialist](chapters/08-cccs-certified-cloud-specialist.md) — CSPM/CWP/CIEM: registration, pre-runtime, runtime, remediation.
9. [Keeping the CrowdStrike Program Current and Career Paths](chapters/09-keeping-the-crowdstrike-program-current-and-career-paths.md) — renewal, program change, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for CrowdStrike, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with credentials, exam-guide domains, and the CrowdStrike University training model
is in the
[CrowdStrike certification appendix](../volume-997-master-appendices/chapters/24-appendix-crowdstrike-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the cybersecurity (X),
Zscaler (XXXV), Splunk (XLV), and cloud volumes.

## Lab coverage

The credential chapters go **per domain**: there is **one walkthrough lab for every
exam-guide domain** of each Falcon credential — **49 domain labs** across the program
(8 CCFA + 6 CCFR + 7 CCFH + 4 CCSA + 5 CCSE + 12 CCIS + 7 CCCS), plus the program and
currency labs in Chapters 01 and 09 for **54 labs total**. Because Falcon is a
hands-on platform, the walkthroughs use real tooling — the **`falconctl`** sensor
CLI, the **FalconPy** Python SDK, the **OAuth2 REST API**, the **CrowdStrike Query
Language (CQL)** for Next-Gen SIEM, and the **GraphQL API** for Identity Protection —
against a licensed Falcon tenant (with read-only patterns where no tenant is
available). Each lab states an objective, commands, expected results, a negative
test, and cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **crowdstrike.com/crowdstrike-university** (catalog and exam
guides), the **Falcon platform**, **FalconPy** (`crowdstrike-falconpy`), and **Pearson
VUE** exam delivery. Credentials and exam guides were verified against crowdstrike.com
on 27 July 2026; CrowdStrike revises its guides as the platform evolves, so confirm
the current guide before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-50-crowdstrike-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
