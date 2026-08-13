# Chapter 06: Big Data

## Learning Objectives

- Process large datasets with MaxCompute.
- Orchestrate data pipelines with DataWorks.
- Understand batch vs real-time processing.
- Apply data governance and cost control.
- Complete a walkthrough for each big-data topic.

## Theory and Architecture

Alibaba Cloud's big-data platform centers on **MaxCompute** — a fully-managed, serverless **data
warehouse** for petabyte-scale batch analytics, queried with a SQL-like language and billed by
compute used (no cluster to manage). Around it, **DataWorks** is the **orchestration and development**
environment: it builds **data pipelines** (ingest → transform → load), schedules jobs with
dependencies, manages data quality, and provides a governance catalog. For **real-time** needs,
**Realtime Compute (Flink)** processes streaming data with low latency (fraud detection, live
dashboards) — the complement to MaxCompute's batch. The pattern mirrors big-data platforms elsewhere:
a scalable **warehouse** (MaxCompute), an **orchestration** layer (DataWorks), and a **streaming**
engine (Flink), with **governance** and **cost control** (partitioning, lifecycle, quota) throughout.
Understanding when to use batch vs streaming and how to build governed, cost-effective pipelines is the
core of the Big Data certifications. This chapter teaches each with a hands-on walkthrough (SQL/job
logic, pipeline design, and batch-vs-stream reasoning).

## Design Considerations

Use **MaxCompute** for large-scale **batch** analytics (serverless, pay per query). Orchestrate with
**DataWorks** (dependencies, quality, catalog). Use **Realtime Compute (Flink)** for **streaming**.
**Partition** tables and set **lifecycle** to control cost. Govern data (lineage, quality, access).
Match batch vs streaming to latency needs.

## Implementation and Automation

The labs write a MaxCompute query, design a pipeline, and choose batch vs streaming.

## Validation and Troubleshooting

Confirm the big-data model:

```text
MaxCompute = serverless petabyte data warehouse (SQL-like, pay per compute). DataWorks = orchestration/dev (pipelines, scheduling, quality, catalog). Realtime Compute (Flink) = streaming/low-latency.
Cost/governance: partitioning + lifecycle + quota + lineage. Batch (MaxCompute) vs streaming (Flink) by latency.
```

Common pitfalls: full-table scans on **unpartitioned** MaxCompute tables (slow/costly); and using
**batch** for a real-time need (use **Flink**).

## Security and Best Practices

Use **MaxCompute** for batch and **Flink** for streaming, orchestrate with **DataWorks**, **partition**
and set **lifecycle** for cost, and **govern** data. All work is authorized data engineering.

## Hands-On Lab

Big-data walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none (modeled).

### Lab 6.1 — Write a partitioned MaxCompute query

**Objective:** Query efficiently.

```sql
-- MaxCompute SQL (partitioned by ds = date):
SELECT region, COUNT(*) AS orders
FROM sales
WHERE ds = '20260728'        -- partition pruning: scan one day, not the whole table
GROUP BY region
ORDER BY orders DESC;
```

**Expected result:** a query that **prunes to one partition** (`ds`) — efficient MaxCompute analytics.

**Negative test:** query `sales` with no `ds` filter; it scans **all** partitions (slow, costly) —
filter on the **partition** column.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Design a DataWorks pipeline

**Objective:** Orchestrate a data flow.

```python
python3 - <<'PY'
pipeline=["extract: sync OSS/RDS raw data into MaxCompute (ingest)","transform: SQL cleaning + aggregation (with dependency)",
          "quality: row-count + null checks (gate)","load: publish to a reporting table","schedule: daily 02:00 with upstream deps"]
for i,s in enumerate(pipeline,1): print(f"{i}. {s}")
print("DataWorks: ingest -> transform -> quality gate -> load, scheduled with dependencies")
PY
```

**Expected result:** a **DataWorks** pipeline (ingest → transform → quality → load, scheduled) —
orchestrated data engineering.

**Negative test:** run transforms manually with no scheduling/dependencies; they break and drift —
orchestrate with **DataWorks**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Choose batch vs streaming

**Objective:** Match the engine to latency.

```python
python3 - <<'PY'
needs={"daily sales report":"MaxCompute (batch)","fraud detection on transactions":"Realtime Compute/Flink (streaming)",
       "monthly data-warehouse aggregation":"MaxCompute (batch)","live operations dashboard":"Flink (streaming)"}
for need,engine in needs.items(): print(f"{need:36}: {engine}")
PY
```

**Expected result:** each need matched to **batch (MaxCompute) or streaming (Flink)** — correct engine
choice.

**Negative test:** compute fraud alerts in a **nightly batch**; it's hours too late — use **streaming**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Control big-data cost

**Objective:** Keep analytics affordable.

```python
python3 - <<'PY'
controls={"partitioning":"query only needed partitions","lifecycle":"drop/archive old partitions automatically",
          "quota":"set compute quota per project","materialized/summary tables":"precompute common aggregations"}
for k,v in controls.items(): print(f"{k:24}: {v}")
print("MaxCompute cost: partition + lifecycle + quota + precomputed summaries")
PY
```

**Expected result:** big-data **cost controls** (partition/lifecycle/quota/summaries) — affordable
analytics.

**Negative test:** keep all raw data forever and full-scan it; costs balloon — apply **lifecycle** and
**partitioning**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alibaba Cloud big data uses MaxCompute for serverless batch analytics, DataWorks for pipeline
orchestration, and Realtime Compute (Flink) for streaming — with partitioning, lifecycle, and
governance for cost-effective, governed data engineering.

- [ ] I can write a partitioned MaxCompute query.
- [ ] I can design a DataWorks pipeline.
- [ ] I can choose batch vs streaming.
- [ ] I can control big-data cost.
- [ ] I completed Labs 6.1–6.4 including each negative test.
