# Volume LXIII — Public Sector Data Governance (PSDGP)

> The ICCP Public Sector Data Governance Professional (PSDGP) credential in one volume — its
> four content areas (Mission Drivers, Deliverables, Roles and Responsibilities, and the Legal
> and Regulatory Environment), the DGSP core body of knowledge, and the exam — with hands-on
> governance walkthroughs, verified against ther2c.com and iccp.org.

## Overview

Volume LXIII maps the **Public Sector Data Governance Professional (PSDGP)** certification —
the **ICCP** credential, taught by **R2C (TheR2C)** and **Buchanan & Edwards**, for standing up
and running a data governance program in a **government** context. It joins the encyclopedia's
governance, risk, and compliance volumes (ISC2 XL, ISACA XLIV, Enterprise Cybersecurity X) and
the data-platform volumes (NetBox LII) that its practices apply to.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXII): it maps
the program — the credential, its content areas, and its exam — and teaches each with a
hands-on walkthrough. PSDGP is **process- and policy-oriented**, so the walkthroughs produce
real governance **artifacts** (charters, policies, catalogs, RACI matrices, retention
schedules, quality scorecards) rather than device configs. Every fact was **verified against
ther2c.com and iccp.org on 28 July 2026**.

Chapters follow the exam blueprint:

- **Chapter 01** frames the program — ICCP/R2C, the exam, prerequisites, and CPD recert.
- **Chapters 02–05** take the **four content areas**: Mission Drivers; Deliverables; Roles and
  Responsibilities; and the Legal and Regulatory Environment.
- **Chapter 06** covers the **DGSP core body of knowledge** that underpins PSDGP.
- **Chapter 07** covers **exam preparation** (the 100-question, 90-minute exam).
- **Chapter 08** is a **capstone** program blueprint.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

## Chapters

1. [The PSDGP Program](chapters/01-the-psdgp-program.md) — ICCP/R2C, exam, prerequisites, CPD.
2. [Public Sector Data Governance Mission Drivers](chapters/02-mission-drivers.md) — the "why".
3. [Public Sector Data Governance Deliverables](chapters/03-deliverables.md) — charter, policy, catalog, quality.
4. [Data Governance Roles and Responsibilities](chapters/04-roles-and-responsibilities.md) — bodies, roles, RACI.
5. [The Legal and Regulatory Environment](chapters/05-legal-and-regulatory-environment.md) — FOIA, Privacy Act, NARA, FISMA.
6. [The DGSP Core Body of Knowledge](chapters/06-dgsp-core-body-of-knowledge.md) — quality, metadata, MDM, lifecycle, security.
7. [Exam Preparation](chapters/07-exam-preparation.md) — the 100-question, 90-minute exam.
8. [Capstone — A Program Blueprint](chapters/08-capstone-program-blueprint.md) — maturity, roadmap, end-to-end trace.
9. [Keeping the Program Current and Career Paths](chapters/09-keeping-current-and-career-paths.md) — CPD recert and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for PSDGP, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with the
ICCP levels, the DGSP core relationship, and the R2C training model is in the
[PSDGP certification appendix](../volume-997-master-appendices/chapters/29-appendix-psdgp-public-sector-data-governance-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the ISC2 (XL), ISACA (XLIV),
Enterprise Cybersecurity (X), and NetBox (LII) volumes.

## Lab coverage

The chapters go **per topic**: there is **one walkthrough lab for every sub-topic** of the four
content areas plus the core body of knowledge, exam prep, and capstone — **35 labs** across the
program. Because PSDGP is a governance credential, the walkthroughs produce **real artifacts** —
a charter, a classification policy, a metadata catalog entry, a data-quality scorecard (SQL/
Python), a RACI matrix, a NARA-style retention schedule, a NIST/FedRAMP control mapping, and an
executive one-pager. Each lab states an objective, steps, expected result, a negative test, and
cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **ther2c.com** and **iccp.org** (the PSDGP course and ICCP
certification) and **datagovernance.education** (Buchanan & Edwards). The labs run with only a
shell, `python3`, and `sqlite3` — no proprietary tooling — so the governance patterns are
reproducible anywhere. The program was verified against ther2c.com and iccp.org on 28 July 2026;
because it rests on statute, confirm the current content areas and the legal landscape before
you study.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-063-public-sector-data-governance
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
