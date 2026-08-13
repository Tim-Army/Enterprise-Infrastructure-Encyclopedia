# Chapter 03: Cloud Data Integration — The Core

## Learning Objectives

- Describe Cloud Data Integration (CDI) as the platform's ETL/ELT module.
- Explain the mapping model — source, transformations, target.
- Recognize the common transformations (filter, expression, joiner, aggregator, lookup).
- Understand mappings, mapping tasks, and the Cloud Mapping Designer.

*Cert relevance: CDI is the Cloud Data Integration Developer, Professional exam — the most widely held Informatica credential.*

## The core module

**Cloud Data Integration (CDI)** is the **workhorse** of IDMC — the module that **moves and transforms data at scale**. It is the cloud successor to **PowerCenter** ([Ch 4](04-powercenter-to-cloud.md)) and the foundation most Informatica customers start with. CDI does **ETL and ELT**: it **extracts** data from sources (databases, files, applications, SaaS APIs), **transforms** it (filtering, joining, aggregating, cleansing, reshaping), and **loads** it into targets (data warehouses, lakes, databases). If the job is "get data from these hundred sources into our Snowflake warehouse, cleaned and conformed, every night," CDI is the tool.

The **Cloud Data Integration Developer, Professional** certification is the most widely held Informatica credential because CDI is where most data engineering happens. It validates that you can build **mappings** and **integration tasks** that reliably do this work. The lab builds a mapping.

## The mapping model

The central abstraction in CDI is the **mapping** — a **visual data-flow** from **source** to **target** through **transformations**:

```text
SOURCE  ->  [ transformation ]  ->  [ transformation ]  ->  TARGET
(extract)     (filter, join, ...)     (aggregate, ...)      (load)
```

You build a mapping in the **Cloud Mapping Designer** — a browser canvas where you drag a **Source**, add **transformation** objects, wire them together, and end at a **Target**. Data **flows left to right**: rows enter from the source, pass through each transformation in order, and land in the target. A mapping is **declarative** — you describe the flow and CDI's engine (running on a **Secure Agent**, [Ch 2](02-idmc-platform.md)) executes it efficiently, often **pushing down** work to the source or target database (that pushdown is the "ELT" mode). The lab models the source→transform→target flow.

## The common transformations

A handful of **transformations** cover most integration work:

- **Source / Target** — read from and write to a connection (database, file, app, warehouse).
- **Filter** — keep only rows that match a condition (drop the rest).
- **Expression** — compute new fields per row (concatenate names, convert types, derive flags).
- **Joiner** — combine two inputs on a key (like a SQL join across sources).
- **Aggregator** — group rows and compute aggregates (sum, count, average per group).
- **Lookup** — enrich a row by looking up a value in another dataset (add a region name from a code).
- **Sorter, Router, Union, Normalizer** — order, split, combine, and reshape as needed.

Learning **which transformation solves which problem** — and how to sequence them efficiently — is the heart of CDI development. The lab implements a filter → expression → aggregate → lookup pipeline.

## Mappings, tasks, and taskflows

A **mapping** is the **design**; to **run** it you wrap it in a **task**:

- A **Mapping Task** turns a mapping into a **runnable, schedulable** job with its own connections, parameters, and runtime settings — the same mapping can run against dev and prod by swapping parameters.
- A **Synchronization Task** is a simpler point-to-point copy for straightforward source-to-target loads.
- A **Taskflow** orchestrates **multiple tasks** into a sequence with **dependencies, branching, and error handling** — run the customer load, then the orders load, then notify on success; stop and alert on failure.

So the progression is **mapping (what to do) → task (how to run it) → taskflow (orchestrate many)**. This is exactly the structure the Developer Professional exam expects you to know. The lab builds and runs a mapping as a task.

## Hands-On Lab

Python simulates a CDI mapping — source, transformations, target — then wraps it in a task. **Cost:** none.

### Lab 3.1 — Build a mapping: source → transform → target

**Objective:** Model an ETL mapping with the common transformations, then run it as a task.

```bash
python3 - <<'EOF'
# a CDI mapping: SOURCE -> filter -> expression -> aggregator (+lookup) -> TARGET
SOURCE = [  # raw orders extracted from a source system
  {"order_id": 1, "cust": "C1", "region_code": "NA", "amount": 120, "status": "paid"},
  {"order_id": 2, "cust": "C1", "region_code": "NA", "amount":  80, "status": "paid"},
  {"order_id": 3, "cust": "C2", "region_code": "EU", "amount": 200, "status": "cancelled"},
  {"order_id": 4, "cust": "C2", "region_code": "EU", "amount":  50, "status": "paid"},
  {"order_id": 5, "cust": "C3", "region_code": "AP", "amount": 300, "status": "paid"},
]
REGION_LOOKUP = {"NA": "North America", "EU": "Europe", "AP": "Asia Pacific"}

def t_filter(rows):      # keep only paid orders
    return [r for r in rows if r["status"] == "paid"]
def t_expression(rows):  # derive a new field (amount with 8% tax)
    return [{**r, "amount_taxed": round(r["amount"] * 1.08, 2)} for r in rows]
def t_aggregator(rows):  # group by customer -> total spend
    agg = {}
    for r in rows:
        agg.setdefault(r["cust"], {"cust": r["cust"], "region_code": r["region_code"], "total": 0.0})
        agg[r["cust"]]["total"] += r["amount_taxed"]
    return list(agg.values())
def t_lookup(rows):      # enrich region_code -> region_name
    return [{**r, "region": REGION_LOOKUP.get(r["region_code"], "?")} for r in rows]

# the mapping = ordered transformations from source to target
pipeline = [t_filter, t_expression, t_aggregator, t_lookup]
data = SOURCE
print("CDI MAPPING — SOURCE -> filter -> expression -> aggregator -> lookup -> TARGET:\n")
print(f"   SOURCE: {len(SOURCE)} rows extracted")
for step in pipeline:
    data = step(data)
    print(f"   after {step.__name__:14}: {len(data)} rows")
print("\n   TARGET (customer spend, paid only, taxed, region-enriched):")
for r in data:
    print(f"      {r['cust']}  {r['region']:14} total={r['total']:.2f}")
print()
# wrap the mapping in a TASK to run it
task = {"name": "mt_customer_spend", "mapping": "m_customer_spend", "schedule": "daily 02:00", "runtime": "SecureAgent-us-east"}
print(f"   MAPPING TASK: {task}")
print()
print("A MAPPING is the visual data-flow (source -> transformations -> target) built in the")
print("Cloud Mapping Designer. Filter drops non-paid rows; Expression derives taxed amount;")
print("Aggregator groups per customer; Lookup enriches the region. Wrap the mapping in a")
print("MAPPING TASK to schedule and run it (on a Secure Agent). This mapping/task model is")
print("the core of the CDI Developer, Professional certification.")
EOF
```

**Expected result:** A mapping that extracts five orders, filters to paid orders, derives a taxed amount, aggregates spend per customer, and enriches the region name — landing three customer rows in the target — then wraps the mapping in a schedulable mapping task. The lesson is the CDI model: a mapping is a source→transformations→target data-flow built in the Cloud Mapping Designer, and a task makes it runnable and schedulable — the core skill of the Developer Professional exam.

**Negative test:** Hand-coding each nightly load as a bespoke script. It works once but has no shared connections, no visual lineage, no reusable transformations, and no orchestration; CDI's mapping/task/taskflow model makes the flow declarative, parameterized, schedulable, and maintainable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] CDI understood — the core ETL/ELT module and cloud successor to PowerCenter.
- [ ] The mapping model understood — source → transformations → target, built in the Cloud Mapping Designer.
- [ ] The common transformations recognized — filter, expression, joiner, aggregator, lookup, and more.
- [ ] Mapping → task → taskflow understood — design, run, and orchestrate.

## See also

- [Chapter 04 — From PowerCenter to the Cloud](04-powercenter-to-cloud.md) — CDI's on-premises predecessor and the modernization path.
- [Chapter 06 — Cloud Data Quality](06-data-quality.md) — quality rules applied inside integration mappings.
- [Volume XLIX — Snowflake](../../volume-049-snowflake-certifications/README.md) — a common CDI load target.
