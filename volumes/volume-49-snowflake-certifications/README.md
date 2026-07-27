# Volume XLIX — Snowflake Certification Tracks

> The whole Snowflake certification program in one volume — SnowPro Associate,
> SnowPro Core, and the five SnowPro Advanced tracks (Architect, Data Engineer,
> Data Analyst, Data Scientist, Administrator) — with hands-on Snowflake SQL labs
> mapped to every exam-guide domain, verified against learn.snowflake.com.

## Overview

Volume XLIX maps the **Snowflake** certification program — the credentials for
building and operating on the **AI Data Cloud** (elastic warehouses, separation of
storage and compute, Snowpark, Cortex, and native governance). It sits alongside
the encyclopedia's other **data and analytics** volumes — Databricks (XLVIII) and
Splunk (XLV) — and complements the cloud volumes where Snowflake runs.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–
XLVIII): it maps the program — which credentials exist, their **exam-guide
domains** and weights, and levels — and teaches each with a hands-on walkthrough.
Every credential was **verified against learn.snowflake.com on 27 July 2026**,
which matters because the program moves with the platform: **SnowPro Core refreshed
from COF-C02 to COF-C03** (16 February 2026), a **SnowPro Associate: Platform**
entry tier was added, and **Cortex** AI content now features across the exams.

Chapters are organized by credential:

- **Chapter 01** frames the program — the AI Data Cloud, the credential tiers, and
  the exam experience.
- **Chapter 02** takes the **SnowPro Associate: Platform** on-ramp.
- **Chapter 03** takes the required **SnowPro Core (COF-C03)** — the foundation for
  every Advanced exam.
- **Chapters 04–08** take the five **SnowPro Advanced** tracks: Architect, Data
  Engineer, Data Analyst, Data Scientist, and Administrator.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic
hands-on labs and knowledge checks.

## Chapters

1. [The Snowflake Certification Program](chapters/01-the-snowflake-certification-program.md) — the AI Data Cloud, the credential tiers, and exam guides.
2. [SnowPro Associate: Platform](chapters/02-snowpro-associate-platform.md) — the entry-tier fundamentals of the platform.
3. [SnowPro Core (COF-C03)](chapters/03-snowpro-core.md) — the required foundation: architecture, loading, RBAC, performance, and semi-structured data.
4. [SnowPro Advanced: Architect](chapters/04-snowpro-advanced-architect.md) — account/data architecture, sharing, security, and continuity.
5. [SnowPro Advanced: Data Engineer](chapters/05-snowpro-advanced-data-engineer.md) — ingestion, transformation (Snowpark/UDFs), pipelines, optimization, and security.
6. [SnowPro Advanced: Data Analyst](chapters/06-snowpro-advanced-data-analyst.md) — analytic SQL, semi-structured data, data quality, and consumption.
7. [SnowPro Advanced: Data Scientist](chapters/07-snowpro-advanced-data-scientist.md) — feature engineering, Snowpark ML, deployment, and Cortex.
8. [SnowPro Advanced: Administrator](chapters/08-snowpro-advanced-administrator.md) — account/security, cost, governance, monitoring, and replication.
9. [Keeping the Snowflake Program Current and Career Paths](chapters/09-keeping-the-snowflake-program-current-and-career-paths.md) — renewal, the COF-C03 refresh, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Snowflake, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with credentials, exam-guide domains, and the free training/practice model is in the
[Snowflake certification appendix](../volume-97-master-appendices/chapters/23-appendix-snowflake-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Related practice lives in the Databricks (XLVIII),
data/observability (XLV), and cloud volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every
exam-guide domain** of each Snowflake credential — **38 topic-area labs** across the
program, including the program and currency labs in Chapters 01 and 09. Because
Snowflake is a hands-on data platform, the walkthroughs use real **Snowflake SQL** —
warehouses, RBAC, `COPY INTO`/stages, streams/tasks, time travel/cloning,
`VARIANT`/`FLATTEN`, resource monitors, and **Cortex** functions — as code you can
run on a **Snowflake free trial**. Each lab states an objective, commands, expected
results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **learn.snowflake.com/certifications** (catalog and exam
guides), the **Snowflake AI Data Cloud**, a **free trial** for practice, and
Pearson VUE exam delivery. Credentials and exam guides were verified against
learn.snowflake.com on 27 July 2026; Snowflake revises its guides as the platform
evolves, so confirm the current guide (Core is **COF-C03**) before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-49-snowflake-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
