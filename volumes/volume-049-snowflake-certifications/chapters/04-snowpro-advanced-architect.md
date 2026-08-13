# Chapter 04: SnowPro Advanced — Architect

## Learning Objectives

- Explain what the SnowPro Advanced: Architect certifies and its prerequisite.
- Summarize the exam-guide domains.
- Design Snowflake account, data-model, security, and performance architecture.
- Design data sharing/collaboration and migration.
- Complete a per-topic walkthrough for each Architect domain.

## Theory and Architecture

The **SnowPro Advanced: Architect (ARA-C01)** validates **designing** Snowflake
solutions at scale. It **requires SnowPro Core**. Its exam guide covers Snowflake
architecture and account design, data modeling and storage, **security and data
governance**, **performance optimization** at scale, **data sharing and
collaboration** (shares, the Marketplace, data clean rooms), and **migration**.

## Design Considerations

The architect designs the whole environment: **account/organization** topology
(multiple accounts, replication), **data models** (schema design, clustering keys),
**governance** (RBAC hierarchy, masking, row access policies, tags), **performance**
(warehouse strategy, clustering, search optimization, query acceleration), and
**data collaboration** (secure shares, Marketplace, clean rooms). Ground designs in
requirements (cost, latency, compliance, DR).

## Implementation and Automation

The labs below use design reasoning and Snowflake SQL for each Architect domain —
account/data-model design, governance, performance, sharing, and migration.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
learn.snowflake.com/certifications > SnowPro Advanced: Architect (ARA-C01):
  - architecture/account design, data modeling, security/governance, performance,
    data sharing/collaboration, migration
  - requires SnowPro Core
```

Common pitfalls: single-account designs where **multi-account/replication** is
needed for DR/isolation; missing **clustering/search optimization** on large
tables; and copying data where **secure sharing** suffices.

## Security and Best Practices

Design a clear **RBAC hierarchy** (functional + access roles), enforce governance
with **masking/row-access policies and tags**, plan **replication/failover** for
DR, optimize large tables with **clustering keys/search optimization**, and share
via **Secure Data Sharing/Marketplace/clean rooms** instead of copies.

## References and Knowledge Checks

- learn.snowflake.com: SnowPro Advanced: Architect exam guide; Snowflake governance, replication, and data-sharing docs.

**Knowledge checks**

1. What does the Architect exam require as a prerequisite?
2. When do you use multiple accounts and replication?
3. How do clean rooms enable collaboration without exposing raw data?

## Hands-On Lab

Per-topic walkthroughs — Architect domains. Design + SQL on a free trial.

**Shared prerequisites** — a free Snowflake trial; ACCOUNTADMIN or a role with
governance grants. **Cost:** none (trial).

### Lab 4.1 — Account and data-model architecture

**Objective:** Design the object and account topology.

```sql
-- Data model: separate raw/staging/curated schemas; clustering on large tables
ALTER TABLE demo_db.sales.orders CLUSTER BY (order_date);
-- Account topology (concept): prod + dev accounts; replication for DR/regions.
```

**Expected result:** a clustered large table and the account-topology concept — the
architecture-design domain.

**Negative test:** cluster a small table; **clustering** helps only large tables
with selective predicates — reserve it for those.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Security and data governance

**Objective:** Apply a masking policy.

```sql
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN val ELSE '***MASKED***' END;
ALTER TABLE demo_db.sales.customers MODIFY COLUMN email SET MASKING POLICY email_mask;
```

**Expected result:** column-level masking revealing email only to `PII_READER` —
the governance design of the Architect exam.

**Negative test:** rely on views alone for masking; **masking policies** apply
consistently at the column across all access paths.

**Rollback:** `ALTER TABLE demo_db.sales.customers MODIFY COLUMN email UNSET MASKING POLICY; DROP MASKING POLICY IF EXISTS email_mask;`

### Lab 4.3 — Performance at scale

**Objective:** Apply search optimization / query acceleration.

```sql
ALTER TABLE demo_db.sales.orders ADD SEARCH OPTIMIZATION;   -- point-lookup speedup
-- Query Acceleration Service offloads scan-heavy portions to shared compute.
```

**Expected result:** search optimization added for fast point lookups — a
performance-at-scale technique the Architect designs.

**Negative test:** add search optimization to every table; it has cost — apply it
where **selective lookups** justify it.

**Rollback:** `ALTER TABLE demo_db.sales.orders DROP SEARCH OPTIMIZATION;`

### Lab 4.4 — Data sharing and collaboration

**Objective:** Create a secure share.

```sql
CREATE SHARE orders_share;
GRANT USAGE ON DATABASE demo_db TO SHARE orders_share;
GRANT SELECT ON demo_db.sales.orders TO SHARE orders_share;
-- Consumers query live data with no copy; Marketplace/clean rooms extend this.
```

**Expected result:** a secure share exposing a table to consumers without copying —
the collaboration domain.

**Negative test:** export data to send to a partner; **secure sharing** gives live,
governed access with no copy — use it.

**Rollback:** `DROP SHARE IF EXISTS orders_share;`

### Lab 4.5 — Migration

**Objective:** Plan a migration to Snowflake.

```sql
-- Migration approach: stage source extracts -> COPY INTO -> validate row counts/checksums
-- Convert DDL/types; re-implement pipelines as streams/tasks; validate + cut over.
SELECT COUNT(*) AS loaded FROM demo_db.sales.orders;
```

**Expected result:** a migration approach (stage → load → validate → cut over) —
the migration domain of the Architect exam.

**Negative test:** cut over without **row-count/checksum validation**; verify data
integrity before decommissioning the source.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SnowPro Advanced: Architect (requires Core) certifies designing Snowflake at
scale: account/data-model architecture, security and governance (masking, row
access, tags), performance (clustering, search optimization), data sharing/
collaboration (shares, Marketplace, clean rooms), and migration.

- [ ] I can design account topology and clustered data models.
- [ ] I can apply masking and governance policies.
- [ ] I can optimize with clustering/search optimization.
- [ ] I can create secure shares and plan a migration.
- [ ] I completed Labs 4.1–4.5 including each negative test.
