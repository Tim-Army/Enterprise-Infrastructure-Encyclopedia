# Chapter 01: The Snowflake Certification Program

## Learning Objectives

- Explain what Snowflake certifies and its place in the data-platform stack.
- Describe the SnowPro credential map: Associate, Core, and Advanced.
- Explain the exam experience, study guides, and year/version currency.
- Understand the AI Data Cloud and the recent COF-C03 Core refresh.
- Verify a current exam guide from the authoritative source.

## Theory and Architecture

**Snowflake** is a leading cloud **data platform** — the **AI Data Cloud** —
providing an elastic, multi-cloud SQL warehouse with separation of storage and
compute, secure data sharing, and native AI (**Cortex**). Its **SnowPro**
certifications validate the ability to build on and administer it. This volume sits
beside the encyclopedia's other data-and-AI platform volumes (Databricks XLVIII,
Splunk XLV) and the cloud volumes Snowflake runs on (AWS, Azure, GCP).

The program has three tiers:

- **SnowPro Associate: Platform** — the entry credential covering foundational
  platform knowledge.
- **SnowPro Core** — the flagship: architecture, security, performance, data
  loading/transformation, protection/sharing, and pipelines. The current exam is
  **COF-C03** (live 16 February 2026, replacing COF-C02).
- **SnowPro Advanced** — role-based expert exams that **require Core**: **Architect**
  (ARA-C01), **Data Engineer** (DEA-C02), **Data Analyst** (DAA-C01), **Data
  Scientist** (DSA-C03), and **Administrator** (ADA-C01).

## Design Considerations

Plan a path by **role**. Newcomers may start with the **Associate**, but most
target **SnowPro Core** as the foundational credential, then a **SnowPro Advanced**
role exam. Core is SQL-and-architecture heavy — master warehouses (compute),
databases/schemas, **RBAC**, staging and **COPY INTO**, **Snowpipe/streams/tasks**,
**time travel/cloning**, and **secure data sharing**. Confirm the current exam
version (Core moved **COF-C02 → COF-C03**).

## Implementation and Automation

Snowflake publishes an **exam guide** per exam with weighted domains — the
authoritative study scope. Practice on a **free 30-day Snowflake trial**. The
primary tool is **Snowflake SQL**:

```sql
SELECT CURRENT_VERSION(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
```

## Validation and Troubleshooting

Confirm a credential's guide and version:

```text
learn.snowflake.com/certifications > open the certification:
  - the exam guide (weighted domains) and exam code (verify COF-C03 for Core)
  - questions, duration, and passing score (Core: 100 Q / 115 min / 750-1000)
  - Advanced exams require SnowPro Core
```

Common pitfalls: studying the retired **COF-C02** guide instead of **COF-C03**;
attempting an **Advanced** exam without **Core**; and confusing a **warehouse**
(compute) with a **database** (storage).

## Security and Best Practices

Verify facts on **snowflake.com / learn.snowflake.com**, never a dump site.
Practice on the **free trial**. Learn Snowflake's separation of **storage and
compute** (independent scaling), **RBAC** (roles/grants), and governance features
(masking, row access policies) — recurring across the exams. Right-size and
auto-suspend **warehouses** for cost.

## References and Knowledge Checks

- learn.snowflake.com/certifications: the certification catalog and per-exam guides; Snowflake documentation.

**Knowledge checks**

1. What are the three SnowPro tiers, and which requires Core?
2. What is the current SnowPro Core exam code?
3. How does Snowflake separate storage and compute?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and running first SQL.

**Shared prerequisites for Labs 1.1–1.3** — a shell with `curl`; a free Snowflake
trial for SQL. **Cost:** none (trial).

### Lab 1.1 — Enumerate the certifications (Topic: Read the program)

**Objective:** Identify the SnowPro tiers and a current exam code.

```bash
curl -sSL -A "Mozilla/5.0" "https://learn.snowflake.com/en/certifications/" \
  | grep -oiE 'SnowPro (Associate|Core|Advanced)[^<]{0,30}|COF-C0[0-9]' | sort -u | head
```

**Expected result:** the SnowPro Associate/Core/Advanced tiers and the current Core
code (**COF-C03**) — the program in one view.

**Negative test:** rely on a guide citing **COF-C02**; the current Core is
**COF-C03** — confirm the version.

**Cleanup:** none.

### Lab 1.2 — Explore the platform (Topic: Foundation)

**Objective:** Confirm the storage/compute separation.

```sql
CREATE WAREHOUSE IF NOT EXISTS lab_wh WAREHOUSE_SIZE='XSMALL' AUTO_SUSPEND=60;
CREATE DATABASE IF NOT EXISTS lab_db;
SELECT CURRENT_WAREHOUSE() AS compute, CURRENT_DATABASE() AS storage;
```

**Expected result:** a warehouse (compute) and a database (storage) created
independently — Snowflake's defining architecture.

**Negative test:** expect a database to provide compute; **warehouses** provide
compute, **databases** hold data — they scale separately.

**Cleanup:** `DROP WAREHOUSE IF EXISTS lab_wh; DROP DATABASE IF EXISTS lab_db;`

### Lab 1.3 — Role context (Topic: Security foundation)

**Objective:** Read the current role (RBAC foundation).

```sql
SELECT CURRENT_ROLE();
SHOW ROLES;
```

**Expected result:** your current role and the account roles — the RBAC model
Snowflake governs access with (a recurring exam theme).

**Negative test:** run privileged actions as a low role expecting success; Snowflake
enforces **RBAC** — use a role with the needed grants.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Snowflake's SnowPro program certifies building on and administering the AI Data
Cloud across three tiers — Associate, Core (now COF-C03), and role-based Advanced
exams (Architect, Data Engineer, Data Analyst, Data Scientist, Administrator). The
platform's separation of storage and compute, RBAC, and data sharing recur
throughout.

- [ ] I can map the SnowPro tiers and the Advanced-requires-Core rule.
- [ ] I can confirm the current Core exam code (COF-C03).
- [ ] I can create a warehouse and database and explain the separation.
- [ ] I can read role context (RBAC).
- [ ] I completed Labs 1.1–1.3 including each negative test.
