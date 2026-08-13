# Chapter 03: Data Engineer Associate

## Learning Objectives

- Explain what the Data Engineer Associate certifies and its exam format.
- Summarize the exam-guide sections.
- Apply ELT with Spark SQL and Python on the lakehouse.
- Apply incremental processing (Delta, Structured Streaming, Auto Loader) and pipelines.
- Complete a per-topic walkthrough for each Data Engineer Associate area.

## Theory and Architecture

The **Databricks Certified Data Engineer Associate** validates building data
pipelines on the lakehouse. Its exam guide covers five areas: the **Databricks
Lakehouse Platform**; **ELT with Spark SQL and Python**; **incremental data
processing** (Delta Lake, **Structured Streaming**, **Auto Loader**); **production
pipelines** (**Jobs**, **Delta Live Tables / Lakeflow Declarative Pipelines**); and
**data governance** (Unity Catalog). The organizing pattern is the **medallion
architecture** — bronze (raw) → silver (cleaned) → gold (curated).

## Design Considerations

The associate engineer builds **ELT** with Spark SQL/PySpark, lands raw data with
**Auto Loader**, processes incrementally with **Delta** and **Structured
Streaming**, and productionizes with **Jobs** or **DLT**. Master Delta operations
(**MERGE**, time travel, **OPTIMIZE**), the medallion layers, and Unity Catalog
governance. This is the foundation for the Professional exam.

## Implementation and Automation

The labs below use **PySpark/Spark SQL + Delta** you can run on Free/Community
Edition — ELT, Delta MERGE, incremental ingest, pipelines, and governance.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
databricks.com/learn/certification > Data Engineer Associate > exam guide:
  - Lakehouse Platform; ELT (Spark SQL/Python); incremental (Delta/Streaming/Auto Loader);
    production pipelines (Jobs/DLT); data governance (Unity Catalog)
```

Common pitfalls: overwriting instead of **MERGE** for upserts; batch-reading a
stream source (use **Auto Loader**/Structured Streaming for incremental); and
skipping the **medallion** layering.

## Security and Best Practices

Use **Delta Lake** for ACID tables and **MERGE** for upserts; ingest incrementally
with **Auto Loader**; layer data **bronze→silver→gold**; productionize with
**Jobs/DLT** (retries, alerts); and govern with **Unity Catalog**. Run **OPTIMIZE**/
`VACUUM` to maintain tables.

## References and Knowledge Checks

- databricks.com: Data Engineer Associate exam guide; Delta Lake, Structured Streaming, Auto Loader, and DLT docs.

**Knowledge checks**

1. What are the medallion architecture layers?
2. When do you use MERGE versus overwrite?
3. What does Auto Loader do for incremental ingestion?

## Hands-On Lab

Per-topic walkthroughs — **one lab per exam-guide area**. Run on Free/Community
Edition.

**Shared prerequisites** — a Databricks workspace; PySpark/Spark SQL. **Cost:**
none (Free Edition).

### Lab 3.1 — Lakehouse Platform: create a Delta table

**Objective:** Create and inspect a Delta table (the lakehouse foundation).

```python
spark.sql("""CREATE TABLE IF NOT EXISTS bronze_events
             (id INT, event STRING, ts TIMESTAMP) USING DELTA""")
spark.sql("DESCRIBE DETAIL bronze_events").select("format","location").show(truncate=False)
```

**Expected result:** a Delta-format table with a storage location — the Lakehouse
Platform foundation.

**Negative test:** create a plain Parquet table and expect ACID/time-travel; use
**Delta**.

**Rollback:** `spark.sql("DROP TABLE IF EXISTS bronze_events")`

### Lab 3.2 — ELT with Spark SQL and Python

**Objective:** Transform bronze → silver with Spark.

```python
from pyspark.sql import functions as F
bronze = spark.createDataFrame([(1," Login "),(2,"logout")], ["id","event"])
silver = bronze.withColumn("event", F.trim(F.lower("event")))
silver.show()
```

**Expected result:** cleaned events (trimmed, lowercased) — the ELT
transformation (bronze→silver) the exam tests.

**Negative test:** load straight to gold without cleaning; the **silver** layer is
where you standardize — don't skip it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Incremental processing: Delta MERGE (upsert)

**Objective:** Upsert with `MERGE`.

```sql
MERGE INTO silver_users t
USING updates s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.name = s.name
WHEN NOT MATCHED THEN INSERT (id, name) VALUES (s.id, s.name);
```

**Expected result:** matched rows updated and new rows inserted in one atomic
operation — the incremental-upsert pattern central to the exam.

**Negative test:** delete-then-insert for upserts; **MERGE** is atomic and
efficient — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Incremental ingestion: Auto Loader / Structured Streaming

**Objective:** Describe incremental file ingestion.

```python
(spark.readStream.format("cloudFiles")
   .option("cloudFiles.format","json")
   .load("/Volumes/main/raw/events")
   .writeStream.option("checkpointLocation","/tmp/ckpt")
   .toTable("bronze_events"))
```

**Expected result:** an Auto Loader stream ingesting new JSON files incrementally
with a checkpoint — the incremental-ingestion area.

**Negative test:** re-read the whole directory each run; **Auto Loader** tracks new
files via the checkpoint — process only new data.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.5 — Production pipelines: Jobs / DLT

**Objective:** Describe a production pipeline.

```python
# Delta Live Tables (Lakeflow Declarative Pipelines): declare tables + expectations
# @dlt.table def silver(): return dlt.read_stream("bronze").filter("id IS NOT NULL")
# Jobs: schedule tasks with dependencies, retries, alerts.
```

**Expected result:** a declarative DLT table with an expectation (and the Jobs
alternative) — the production-pipeline area.

**Negative test:** run notebooks manually in production; use **Jobs/DLT** for
scheduling, retries, and data-quality expectations.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.6 — Data governance: Unity Catalog

**Objective:** Grant governed access to a table.

```sql
GRANT SELECT ON TABLE main.sales.orders TO `analysts`;
SHOW GRANTS ON TABLE main.sales.orders;
```

**Expected result:** a least-privilege grant on a `catalog.schema.table` — the
Unity Catalog governance area of the exam.

**Negative test:** grant broad access at the catalog level for one table; grant at
the **table** level (least privilege).

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Data Engineer Associate certifies building lakehouse pipelines: the Lakehouse
Platform, ELT with Spark SQL/Python, incremental processing (Delta MERGE, Auto
Loader, Structured Streaming), production pipelines (Jobs/DLT), and Unity Catalog
governance — organized by the medallion architecture. It is the foundation for the
Professional exam.

- [ ] I can list the five Data Engineer Associate exam areas.
- [ ] I can build ELT and upsert with Delta MERGE.
- [ ] I can ingest incrementally with Auto Loader and productionize with Jobs/DLT.
- [ ] I can grant governed access via Unity Catalog.
- [ ] I completed Labs 3.1–3.6 including each negative test.
