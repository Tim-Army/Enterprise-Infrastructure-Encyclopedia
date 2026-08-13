# Chapter 05: SnowPro Advanced — Data Engineer

## Learning Objectives

- Explain what the SnowPro Advanced: Data Engineer certifies and its prerequisite.
- Summarize the exam-guide domains.
- Apply ingestion, transformation (Snowpark/UDFs/stored procedures), and pipeline optimization.
- Apply storage/data modeling and pipeline security.
- Complete a per-topic walkthrough for each Data Engineer domain.

## Theory and Architecture

The **SnowPro Advanced: Data Engineer (DEA-C02)** validates building production
data pipelines on Snowflake. It **requires SnowPro Core**. Its exam guide covers
**data movement/ingestion** (Snowpipe, streams, external tables), **transformation**
(SQL, **Snowpark**, UDFs/UDTFs, stored procedures), **performance and
optimization** of pipelines, **storage and data modeling**, and **security** for
data engineering.

## Design Considerations

The data engineer ingests continuously (**Snowpipe**, streams/tasks), transforms
with SQL and **Snowpark** (Python/Java/Scala), builds reusable logic (UDFs, stored
procedures), optimizes (clustering, warehouse strategy, pruning), and secures data
in motion and at rest. Master streams/tasks orchestration and Snowpark.

## Implementation and Automation

The labs below use Snowflake SQL/Snowpark patterns for each domain — ingestion,
transformation, pipelines, optimization, and security.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
learn.snowflake.com/certifications > SnowPro Advanced: Data Engineer (DEA-C02):
  - ingestion, transformation (Snowpark/UDFs/procs), optimization, storage/modeling, security
  - requires SnowPro Core
```

Common pitfalls: full reloads instead of **streams** for incremental; heavy
row-by-row UDFs where set-based SQL is faster; and unmonitored task chains.

## Security and Best Practices

Ingest incrementally (**Snowpipe/streams**), orchestrate with **task graphs**,
prefer **set-based SQL** and **Snowpark** vectorized ops over row UDFs, monitor task
history, and secure pipelines with least-privilege roles and masking.

## References and Knowledge Checks

- learn.snowflake.com: SnowPro Advanced: Data Engineer exam guide; Snowpark, Snowpipe, streams/tasks docs.

**Knowledge checks**

1. What does the Data Engineer exam require as a prerequisite?
2. When do you use Snowpark versus SQL?
3. How do streams enable incremental processing?

## Hands-On Lab

Per-topic walkthroughs — Data Engineer domains. Run on a free trial.

**Shared prerequisites** — a free Snowflake trial; a warehouse. **Cost:** none.

### Lab 5.1 — Ingestion: Snowpipe / streams

**Objective:** Set up continuous ingestion with a stream.

```sql
CREATE STREAM raw_stream ON TABLE demo_db.raw.events;   -- change capture
-- Snowpipe (auto-ingest): PIPE + cloud notification loads new files continuously
```

**Expected result:** a stream capturing changes (and the Snowpipe concept) — the
ingestion domain.

**Negative test:** schedule full reloads; **streams/Snowpipe** process only new
data — ingest incrementally.

**Rollback:** `DROP STREAM IF EXISTS raw_stream;`

### Lab 5.2 — Transformation: Snowpark and UDFs

**Objective:** Create a UDF and describe Snowpark.

```sql
CREATE FUNCTION to_cents(dollars NUMBER) RETURNS NUMBER
  AS $$ dollars * 100 $$;
SELECT to_cents(19.99);   -- 1999
-- Snowpark (Python): df.group_by("k").agg(...) runs pushed-down in Snowflake.
```

**Expected result:** a working SQL UDF (and the Snowpark concept) — the
transformation domain.

**Negative test:** pull data to a client to transform; **Snowpark/SQL** push
compute to Snowflake — keep it in-platform.

**Rollback:** `DROP FUNCTION IF EXISTS to_cents(NUMBER);`

### Lab 5.3 — Pipelines: task graphs

**Objective:** Orchestrate dependent tasks.

```sql
CREATE TASK t_load  WAREHOUSE=lab_wh SCHEDULE='1 MINUTE' AS INSERT INTO staged SELECT * FROM raw_stream;
CREATE TASK t_clean WAREHOUSE=lab_wh AFTER t_load AS INSERT INTO curated SELECT * FROM staged WHERE ok;
ALTER TASK t_load RESUME;   -- tasks are created suspended
```

**Expected result:** a dependent task graph (`t_clean AFTER t_load`) — the pipeline
orchestration the exam tests.

**Negative test:** forget to `RESUME` tasks; they are created **suspended** — resume
them (root last for DAGs).

**Rollback:** `ALTER TASK t_load SUSPEND; DROP TASK IF EXISTS t_clean; DROP TASK IF EXISTS t_load;`

### Lab 5.4 — Optimization

**Objective:** Optimize a pipeline query.

```sql
-- Cluster large tables on filter columns; size warehouses to workload;
-- use result/warehouse cache; avoid unnecessary re-computation with materialized views.
CREATE MATERIALIZED VIEW mv_daily AS
  SELECT order_date, SUM(amount) total FROM curated GROUP BY order_date;
```

**Expected result:** a materialized view precomputing daily totals — a pipeline
optimization technique.

**Negative test:** recompute expensive aggregates every query; a **materialized
view** maintains them incrementally — use it for hot aggregates.

**Rollback:** `DROP MATERIALIZED VIEW IF EXISTS mv_daily;`

### Lab 5.5 — Security for data engineering

**Objective:** Secure a pipeline with least privilege.

```sql
CREATE ROLE etl_role;
GRANT USAGE ON WAREHOUSE lab_wh TO ROLE etl_role;
GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA demo_db.curated TO ROLE etl_role;
-- run tasks as etl_role (not ACCOUNTADMIN)
```

**Expected result:** an ETL role scoped to the warehouse and curated schema — the
security domain of the Data Engineer exam.

**Negative test:** run pipelines as ACCOUNTADMIN; use a **least-privilege ETL
role**.

**Rollback:** `DROP ROLE IF EXISTS etl_role;`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SnowPro Advanced: Data Engineer (requires Core) certifies production data
engineering on Snowflake: incremental ingestion (Snowpipe/streams), transformation
(Snowpark/UDFs/procedures), pipeline orchestration (task graphs), optimization
(clustering, materialized views), and pipeline security.

- [ ] I can set up incremental ingestion with streams/Snowpipe.
- [ ] I can transform with UDFs and Snowpark.
- [ ] I can orchestrate a task graph and optimize with materialized views.
- [ ] I can secure a pipeline with a least-privilege role.
- [ ] I completed Labs 5.1–5.5 including each negative test.
