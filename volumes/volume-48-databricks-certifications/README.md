# Volume XLVIII — Databricks Certification Tracks

> The whole Databricks certification program in one volume — Data Analyst, Data
> Engineer, Machine Learning, the new Generative AI and Context Engineer, and
> Apache Spark Developer — with hands-on Spark/SQL/MLflow labs mapped to every
> exam-guide section, verified against databricks.com.

## Overview

Volume XLVIII maps the **Databricks** certification program — the credentials for
building and operating on the **lakehouse Data Intelligence Platform** (Delta Lake,
Unity Catalog, Spark, MLflow, Mosaic AI). It sits between the encyclopedia's
**data/observability** (Splunk, XLV) and **AI-infrastructure** (NVIDIA, XLVI)
volumes and complements the cloud volumes where Databricks runs.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–
XLVII): it maps the program — which credentials exist, their **exam-guide
sections**, and levels — and teaches each with a hands-on walkthrough. Every
credential was **verified against databricks.com on 26 July 2026**, which matters
because the program is expanding toward AI: the **Generative AI Engineer** and
**Context Engineer** certifications are recent additions, and the **Hadoop
Migration Architect** certification was retired (1 August 2024).

Chapters are organized by credential:

- **Chapter 01** frames the program — the lakehouse, certifications vs
  accreditations, and the exam experience.
- **Chapters 02–06** take the core role-based certs: Data Analyst; Data Engineer
  Associate and Professional; Machine Learning Associate and Professional.
- **Chapter 07** takes the new AI certs: Generative AI Engineer and Context
  Engineer.
- **Chapter 08** takes the Apache Spark Developer Associate and the Platform
  accreditations.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic
hands-on labs and knowledge checks.

## Chapters

1. [The Databricks Certification Program](chapters/01-the-databricks-certification-program.md) — the lakehouse, certifications vs accreditations, and exam guides.
2. [Data Analyst Associate](chapters/02-data-analyst-associate.md) — Databricks SQL, analytics, and dashboards.
3. [Data Engineer Associate](chapters/03-data-engineer-associate.md) — ELT, incremental processing, pipelines, and governance.
4. [Data Engineer Professional](chapters/04-data-engineer-professional.md) — advanced modeling, optimization, security, and deployment.
5. [Machine Learning Associate](chapters/05-machine-learning-associate.md) — the ML workflow, MLflow, AutoML, and Feature Store.
6. [Machine Learning Professional](chapters/06-machine-learning-professional.md) — MLOps: lifecycle, deployment, and monitoring.
7. [Generative AI Engineer and Context Engineer](chapters/07-generative-ai-engineer-and-context-engineer.md) — RAG, Mosaic AI, evaluation, and agent context.
8. [Apache Spark Developer and Platform Accreditations](chapters/08-apache-spark-developer-and-platform-accreditations.md) — the Spark DataFrame API and platform administration.
9. [Keeping the Databricks Program Current and Career Paths](chapters/09-keeping-the-databricks-program-current-and-career-paths.md) — renewal, the AI additions, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Databricks, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with certifications, accreditations, exam-guide sections, and the free
training/practice model is in the
[Databricks certification appendix](../volume-97-master-appendices/chapters/22-appendix-databricks-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Related practice lives in the data (XLV),
AI-infrastructure (XLVI), automation (IX), and cloud volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every
exam-guide section** of each Databricks credential — roughly **55 topic-area labs**
across the program — plus the program and currency labs in Chapters 01 and 09.
Because Databricks is a hands-on data-and-AI platform, the walkthroughs use the real
tooling — **Spark** (PySpark/Spark SQL), **Delta Lake**, **Unity Catalog**,
**MLflow**, **AutoML**, the **Feature Store**, and **Mosaic AI** (Vector Search,
Model Serving) — as code you can run on **Databricks Free/Community Edition**. Each
lab states an objective, commands, expected results, a negative test, and cleanup,
and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **databricks.com/learn/certification** (catalog and exam
guides), the **Databricks Data Intelligence Platform**, **Free/Community Edition**
for practice, and Kryterion/Webassessor exam delivery. Certifications and exam
guides were verified against databricks.com on 26 July 2026; Databricks revises its
guides as the platform evolves, so confirm the current guide before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-48-databricks-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
