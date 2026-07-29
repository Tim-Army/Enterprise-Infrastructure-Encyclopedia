# Volume XLVII — Oracle Certification Tracks

> The whole Oracle certification program in one volume — Oracle Cloud
> Infrastructure (OCI), Oracle Database, MySQL, and Java — with hands-on SQL, CLI,
> and code labs mapped to every exam-topic area, verified against
> education.oracle.com.

## Overview

Volume XLVII maps the **Oracle** certification program across its four families —
**Oracle Cloud Infrastructure (OCI)**, **Oracle Database**, **MySQL**, and
**Java**. Oracle's footprint is enormous (its database and Java underpin countless
enterprises, and OCI is a major cloud), so this volume adds a large previously
uncovered vendor alongside the other cloud (AWS, Azure, Google Cloud) and data
volumes.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–
XLVI): it maps the program — which credentials exist, their **exam-topic areas**,
tiers, and the **year-versioned** code system — and teaches each with a hands-on
walkthrough. Every family and key credential was **verified against
education.oracle.com on 26 July 2026**, which matters because Oracle refreshes
exams annually (by year suffix) or by release: recent highlights include the **OCI
Generative AI Professional** and **Multicloud Architect** credentials, **Oracle
Database 23ai** (AI Vector Search), and **Java SE 21**.

Chapters are organized by family:

- **Chapter 01** frames the program — the four families, year-versioned codes, and
  CertView.
- **Chapters 02–06** take OCI: Foundations/AI Foundations; Architect; Developer/
  Operations/DevOps; Networking/Security/Multicloud; and Data Science/Generative AI.
- **Chapter 07** takes Oracle Database (SQL, DBA, 23ai, Autonomous).
- **Chapter 08** takes MySQL and Java.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic
hands-on labs and knowledge checks.

## Chapters

1. [The Oracle Certification Program](chapters/01-the-oracle-certification-program.md) — the four families, year-versioned codes, exam topics, and CertView.
2. [OCI Foundations and AI Foundations](chapters/02-oci-foundations-and-ai-foundations.md) — the OCI and AI associate baseline.
3. [OCI Architect (Associate and Professional)](chapters/03-oci-architect-associate-and-professional.md) — building and designing OCI solutions.
4. [OCI Developer, Operations, and DevOps](chapters/04-oci-developer-operations-and-devops.md) — cloud-native development, observability, and automation.
5. [OCI Networking, Security, and Multicloud](chapters/05-oci-networking-security-and-multicloud.md) — advanced networking, security services, and multicloud.
6. [OCI Data Science and Generative AI](chapters/06-oci-data-science-and-generative-ai.md) — the ML lifecycle and OCI Generative AI (RAG, 23ai vectors, agents).
7. [Oracle Database — SQL, DBA, and 23ai](chapters/07-oracle-database-sql-dba-and-23ai.md) — SQL, administration, multitenant, RMAN, 23ai, and Autonomous.
8. [MySQL and Java](chapters/08-mysql-and-java.md) — MySQL administration/development and Java SE 21.
9. [Keeping the Oracle Program Current and Career Paths](chapters/09-keeping-the-oracle-program-current-and-career-paths.md) — year-versioning, recertification, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Oracle, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with families, tiers, the year-versioned codes, and the free training/practice
model is in the
[Oracle certification appendix](../volume-997-master-appendices/chapters/21-appendix-oracle-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the cloud (XVII,
XXXIII, XXXIV), containers/Kubernetes (VIII, XLI), and automation (IX, XLII)
volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every
exam-topic area** of each Oracle credential (grouping the finest sub-topics) —
roughly **54 topic-area labs** across the program — plus the program and currency
labs in Chapters 01 and 09. Because Oracle credentials are hands-on, the
walkthroughs use the real tooling — **Oracle SQL** (runnable on Oracle Database
Free / Autonomous Database), the **OCI CLI** (`oci`), **MySQL**, and **Java SE
21** — with OCI service patterns shown illustratively where a tenancy is required.
Each lab states an objective, commands, expected results, a negative test, and
cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **education.oracle.com** (certifications and exam topics),
**Oracle CertView**, the **OCI CLI**, **Oracle Database 23ai** / **Autonomous
Database** / **Oracle Database Free**, **MySQL**, and **JDK 21**, with **Pearson
VUE** delivery. Families, credentials, and codes were verified against
education.oracle.com on 26 July 2026; Oracle year-versions its exams, so confirm
the current code (suffix/release) before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-047-oracle-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
