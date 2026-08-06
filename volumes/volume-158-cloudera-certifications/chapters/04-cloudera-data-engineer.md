# Chapter 04: Cloudera Data Engineer

## Learning Objectives

- Explain the Data Engineer role — building data pipelines on CDP.
- Describe Spark processing and Airflow orchestration.
- Understand batch and the shift toward Iceberg tables.
- Recognize performance tuning as a core engineering skill.

*Cert relevance: the Cloudera Data Engineer certification validates building and operating data pipelines.*

## The data engineer role

The **Cloudera Data Engineer** builds the **data pipelines** that move and transform data through the platform — ingesting raw data, cleaning and enriching it, and producing the curated datasets that analysts and ML models consume. On CDP, this centers on the **Data Engineering** service, using **Apache Spark** for large-scale processing and **Apache Airflow** for orchestration, increasingly writing to **Apache Iceberg** tables. Data engineering is the plumbing of the data platform — without reliable pipelines, there is no trustworthy data to analyze. The lab models a pipeline.

## Spark processing

**Apache Spark** is the workhorse — a distributed processing engine that transforms large datasets in parallel across a cluster. The data engineer writes Spark jobs (in Python/PySpark, SQL, or Scala) to **extract, transform, and load (ETL)** data: reading from sources, applying transformations (filtering, joining, aggregating, cleaning), and writing curated output. Spark's power is **scale** — it processes data far larger than any single machine by distributing the work. On CDP, Spark runs on the Data Engineering service (including **Spark on Kubernetes**), managed and secured by the platform. The lab models a Spark transformation.

## Airflow orchestration

Real pipelines are **multi-step** and **scheduled** — ingest, then transform, then aggregate, then publish, on a schedule and with dependencies. **Apache Airflow** orchestrates this: the engineer defines a **DAG** (directed acyclic graph) of tasks with dependencies, and Airflow runs them in order, on schedule, with **retries** and **monitoring**. Orchestration turns individual Spark jobs into a reliable, repeatable, observable **pipeline** — the difference between a one-off script and a production data pipeline. The lab models a DAG.

## Iceberg, batch, and performance tuning

Modern Cloudera data engineering writes to **Apache Iceberg** tables — an open table format bringing **ACID transactions, schema evolution, and time travel** to data-lake storage ([the lakehouse, Chapter 8](08-genai-lakehouse-generalist.md)). And a defining engineering skill is **performance tuning** — pipelines process huge data, and inefficient jobs are slow and expensive. The engineer tunes: partitioning, file sizes, join strategies, caching, and resource allocation, so pipelines run fast and cost-effectively. Performance tuning is where a data engineer's expertise shows most. The lab models tuning impact.

## Hands-On Lab

Python models a pipeline and tuning. **Cost:** none.

### Lab 4.1 — A Spark/Airflow pipeline and the impact of tuning

**Objective:** Model a DAG pipeline and a performance-tuning decision.

```bash
python3 - <<'EOF'
# an Airflow DAG of Spark tasks with dependencies
DAG = {
  "ingest":     {"deps": [],                    "engine": "Spark read (source -> raw)"},
  "clean":      {"deps": ["ingest"],            "engine": "Spark transform (dedupe/validate)"},
  "enrich":     {"deps": ["clean"],             "engine": "Spark join (+ reference data)"},
  "aggregate":  {"deps": ["enrich"],            "engine": "Spark groupBy -> metrics"},
  "publish":    {"deps": ["aggregate"],         "engine": "write Iceberg table (ACID)"},
}
# topological order (Airflow runs deps first)
done, order = set(), []
while len(order) < len(DAG):
    for t, meta in DAG.items():
        if t not in done and all(d in done for d in meta["deps"]):
            order.append(t); done.add(t)
print("Airflow DAG (Spark tasks), executed in dependency order:\n")
for i, t in enumerate(order, 1):
    print(f"   {i}. {t:10} <- deps {DAG[t]['deps'] or '(none)'}   [{DAG[t]['engine']}]")
print()
# performance tuning: partitioning a big join
rows = 2_000_000_000
print("Performance tuning — a 2B-row join:")
untuned_s = rows / 2_000_000     # naive: full shuffle, small files
tuned_s   = rows / 20_000_000    # tuned: good partitioning + file sizes + broadcast join
print(f"   untuned (bad partitioning, tiny files): ~{untuned_s:.0f}s")
print(f"   tuned (partition + right file size + broadcast small side): ~{tuned_s:.0f}s")
print(f"   -> ~{untuned_s/tuned_s:.0f}x faster (and proportionally cheaper)\n")
print("The Data Engineer builds PIPELINES: SPARK (distributed transform at scale) orchestrated")
print("by AIRFLOW (a DAG of scheduled, dependency-ordered, retryable tasks), writing ICEBERG")
print("tables (ACID, schema evolution, time travel). And TUNES them — partitioning, file")
print("sizes, join strategy, resources — because at billions of rows, tuning is the difference")
print("between fast+cheap and slow+expensive. Reliable pipelines = the trustworthy data")
print("everything downstream (analysts, ML) depends on.")
EOF
```

**Expected result:** An Airflow DAG of Spark tasks executed in dependency order (ingest → clean → enrich → aggregate → publish to Iceberg), and a 2-billion-row join running ~10× faster after tuning. The data-engineer lesson is that pipelines are Spark transformations orchestrated by Airflow DAGs writing to Iceberg tables, and performance tuning (partitioning, file sizes, join strategy) is the core skill that makes them fast and cost-effective at scale — producing the trustworthy data everything downstream depends on.

**Negative test:** Running one-off Spark scripts by hand with no orchestration or tuning. You lose scheduling, dependencies, retries, and observability, and untuned jobs are slow and expensive; Airflow DAGs plus performance tuning make pipelines production-grade.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The data-engineer role understood — building the pipelines that transform data on CDP.
- [ ] Spark processing understood — distributed ETL at scale.
- [ ] Airflow orchestration understood — DAGs of scheduled, dependency-ordered, retryable tasks.
- [ ] Iceberg tables and performance tuning recognized as core modern data-engineering skills.
