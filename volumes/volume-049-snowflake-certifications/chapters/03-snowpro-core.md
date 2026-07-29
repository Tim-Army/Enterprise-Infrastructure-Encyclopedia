# Chapter 03: SnowPro Core (COF-C03)

## Learning Objectives

- Explain what SnowPro Core certifies and its exam format.
- List the six COF-C03 domains and their weights.
- Apply Snowflake architecture, security, performance, loading, protection, and pipelines.
- Understand the AI Data Cloud capabilities the current exam emphasizes.
- Complete a per-domain walkthrough for each Core domain.

## Theory and Architecture

The **SnowPro Core** is Snowflake's flagship credential — implementation-level
knowledge across the platform. The current exam, **COF-C03** (live 16 February
2026, replacing COF-C02), is **100 questions in 115 minutes**, **750/1000** to
pass, **$175**, with ~6 months' recommended experience. Six weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Snowflake AI Data Cloud Capabilities and Architecture | 25% |
| 2 | Account Access and Security | 20% |
| 3 | Performance Concepts | 15% |
| 4 | Data Loading and Transformation | 20% |
| 5 | Data Protection and Data Sharing | 10% |
| 6 | Data Pipelines | 10% |

The renamed **AI Data Cloud** domain (25%) is the largest, reflecting the platform's
architecture and its AI (**Cortex**) capabilities.

## Design Considerations

Core rewards knowing **how Snowflake works**: the three-layer architecture
(storage, multi-cluster compute, cloud services), **RBAC** and security,
**performance** (warehouse sizing, caching, clustering, pruning), **loading**
(stages, `COPY INTO`, Snowpipe), **protection** (time travel, fail-safe, cloning)
and **secure data sharing**, and **pipelines** (streams, tasks). Practice each on a
free trial.

## Implementation and Automation

The labs below use **Snowflake SQL** for each domain — architecture, security,
performance, loading, protection/sharing, and pipelines.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
learn.snowflake.com/certifications > SnowPro Core (COF-C03) > exam guide:
  - six domains (25/20/15/20/10/10), 100 Q / 115 min / 750-1000 / $175
  - verify COF-C03 (not the retired COF-C02)
```

Common pitfalls: studying **COF-C02** content; confusing **time travel** (recent,
user-accessible) with **fail-safe** (7-day Snowflake-only recovery); and oversizing
warehouses instead of using **multi-cluster** for concurrency.

## Security and Best Practices

Apply **least-privilege RBAC**; right-size warehouses and use **multi-cluster** for
concurrency and **result/warehouse caching** for performance; load with
**Snowpipe** for continuous ingest; protect with **time travel/cloning**; and share
data securely with **Secure Data Sharing** (no copies). Use **Cortex** for native
AI where it fits.

## References and Knowledge Checks

- learn.snowflake.com: SnowPro Core (COF-C03) exam guide; Snowflake architecture and Cortex docs.

**Knowledge checks**

1. Which Core domain is largest, and what does it cover?
2. What is the difference between time travel and fail-safe?
3. How does secure data sharing avoid copying data?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every COF-C03 domain**. Run on a free trial.

**Shared prerequisites** — a free Snowflake trial; a warehouse and role.
**Cost:** none (trial).

### Lab 3.1 — Domain 1: AI Data Cloud Capabilities and Architecture (25%)

**Objective:** Observe the three-layer architecture.

```sql
SELECT CURRENT_WAREHOUSE() AS compute_layer,       -- virtual warehouses (compute)
       CURRENT_DATABASE()  AS storage_layer;        -- databases (storage)
SHOW WAREHOUSES;                                     -- cloud services orchestrates these
```

**Expected result:** compute and storage referenced independently — Snowflake's
separated three-layer architecture, the largest Core domain.

**Negative test:** assume scaling storage scales compute; they are **independent** —
resize the warehouse for compute.

**Cleanup:** none.

### Lab 3.2 — Domain 2: Account Access and Security (20%)

**Objective:** Grant least-privilege access via a role.

```sql
CREATE ROLE analyst_role;
GRANT USAGE ON WAREHOUSE lab_wh TO ROLE analyst_role;
GRANT SELECT ON ALL TABLES IN SCHEMA demo_db.sales TO ROLE analyst_role;
GRANT ROLE analyst_role TO USER my_user;
```

**Expected result:** a role granted only usage + select, assigned to a user — the
RBAC security model (Domain 2).

**Negative test:** grant `ACCOUNTADMIN` for convenience; scope a **custom role** to
least privilege.

**Cleanup:** `DROP ROLE IF EXISTS analyst_role;`

### Lab 3.3 — Domain 3: Performance Concepts (15%)

**Objective:** Use multi-cluster and caching for performance.

```sql
ALTER WAREHOUSE lab_wh SET MIN_CLUSTER_COUNT=1 MAX_CLUSTER_COUNT=3;  -- multi-cluster (concurrency)
-- Result cache: re-running an identical query returns instantly from cache
SELECT COUNT(*) FROM demo_db.sales.orders;   -- run twice; 2nd hits the result cache
```

**Expected result:** a multi-cluster warehouse (scales out for concurrency) and
result caching — the performance domain.

**Negative test:** size up a single cluster to handle many concurrent users;
**multi-cluster** scales concurrency better than a bigger single cluster.

**Cleanup:** none.

### Lab 3.4 — Domain 4: Data Loading and Transformation (20%)

**Objective:** Load with COPY INTO and transform.

```sql
COPY INTO demo_db.sales.orders FROM @demo_stage FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1);
CREATE TABLE demo_db.sales.orders_clean AS
SELECT id, ABS(amount) AS amount FROM demo_db.sales.orders WHERE amount IS NOT NULL;
```

**Expected result:** a bulk load and a transform (clean table) — the loading/
transformation domain.

**Negative test:** row-by-row inserts for bulk data; use **`COPY INTO`** from a
stage — it's far faster.

**Cleanup:** `DROP TABLE IF EXISTS demo_db.sales.orders_clean;`

### Lab 3.5 — Domain 5: Data Protection and Data Sharing (10%)

**Objective:** Use time travel and clone; describe secure sharing.

```sql
SELECT * FROM demo_db.sales.orders AT(OFFSET => -60);   -- time travel: 60s ago
CREATE TABLE orders_bak CLONE demo_db.sales.orders;      -- zero-copy clone
-- Secure Data Sharing: CREATE SHARE + GRANT -> consumers query without copies.
```

**Expected result:** a time-travel query and a zero-copy clone, plus the sharing
concept — the protection/sharing domain.

**Negative test:** back up by exporting/copying data; **time travel + zero-copy
clone** protect data without duplication.

**Cleanup:** `DROP TABLE IF EXISTS orders_bak;`

### Lab 3.6 — Domain 6: Data Pipelines (10%)

**Objective:** Build a stream + task pipeline.

```sql
CREATE STREAM orders_stream ON TABLE demo_db.sales.orders;   -- CDC on the table
CREATE TASK load_task WAREHOUSE=lab_wh SCHEDULE='1 MINUTE' AS
  INSERT INTO demo_db.sales.orders_clean
  SELECT id, ABS(amount) FROM orders_stream WHERE METADATA$ACTION='INSERT';
```

**Expected result:** a **stream** (change capture) feeding a scheduled **task** —
the continuous-pipeline domain (with Snowpipe for ingest).

**Negative test:** poll the whole table on a schedule; a **stream** captures only
changes — process incrementally.

**Cleanup:** `DROP TASK IF EXISTS load_task; DROP STREAM IF EXISTS orders_stream;`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SnowPro Core (COF-C03) is Snowflake's flagship credential: six domains weighted
25/20/15/20/10/10, led by the AI Data Cloud architecture. It certifies
implementation-level knowledge of architecture, security (RBAC), performance
(multi-cluster/caching), loading (`COPY INTO`/Snowpipe), protection (time travel/
cloning), sharing, and pipelines (streams/tasks). Study COF-C03, not the retired
COF-C02.

- [ ] I can list the six COF-C03 domains and weights.
- [ ] I can apply RBAC and multi-cluster/caching performance.
- [ ] I can load with COPY INTO and use time travel/cloning.
- [ ] I can build a stream + task pipeline.
- [ ] I completed Labs 3.1–3.6 including each negative test.
