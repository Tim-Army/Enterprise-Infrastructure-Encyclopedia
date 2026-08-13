# Chapter 08: Apache Spark Developer and Platform Accreditations

## Learning Objectives

- Explain the Apache Spark Developer Associate certification and the Platform accreditations.
- Summarize the Spark Developer exam-guide areas.
- Apply the Spark DataFrame API: transformations, actions, functions, and tuning.
- Understand the Platform Architect and Administrator accreditations.
- Complete a per-topic walkthrough for each area.

## Theory and Architecture

This chapter covers the Spark-developer credential and the platform-focused
accreditations:

- **Apache Spark Developer Associate** — the **Spark DataFrame API**: Spark
  architecture (driver/executors, jobs/stages/tasks), transformations vs actions,
  built-in functions, joins and aggregations, I/O, and performance (partitioning,
  caching, **Adaptive Query Execution**). It certifies the Spark skills that
  underpin the whole platform.
- **Platform Architect** (AWS / Azure / GCP) and **Platform Administrator** —
  **free accreditations** on deploying, securing, and administering Databricks on
  each cloud (workspace/account setup, networking, identity, Unity Catalog
  metastore, cost).

## Design Considerations

The **Spark Developer** credential is language-and-API focused — master the
DataFrame API and Spark's execution model (lazy transformations, wide vs narrow,
shuffles). The **Platform** accreditations are for architects/admins standing up
Databricks on a cloud — learn the account/workspace model, identity federation, the
Unity Catalog metastore, and networking/security. Together they round out the
program's developer and platform ends.

## Implementation and Automation

The labs below use the **PySpark DataFrame API** (runnable on Free/Community
Edition) for the Spark developer areas, and platform-admin concepts for the
accreditations.

## Validation and Troubleshooting

Confirm the guides before studying:

```text
databricks.com/learn/certification:
  - Apache Spark Developer Associate > exam guide (DataFrame API, architecture, tuning)
  - Platform Architect (AWS/Azure/GCP) + Platform Administrator accreditations (free)
```

Common pitfalls: confusing **transformations** (lazy) with **actions** (trigger
execution); ignoring **shuffles** (wide transformations) in tuning; and treating a
platform **accreditation** like a proctored certification.

## Security and Best Practices

Write efficient Spark: minimize **shuffles**, cache reused DataFrames judiciously,
leverage **Adaptive Query Execution**, and select only needed columns. For the
platform, follow the cloud-specific deployment guidance — least-privilege identity,
a governed **Unity Catalog metastore**, private networking, and cost controls.

## References and Knowledge Checks

- databricks.com: Apache Spark Developer Associate exam guide; Platform Architect/Administrator accreditations; Apache Spark documentation.

**Knowledge checks**

1. What is the difference between a transformation and an action in Spark?
2. What causes a shuffle, and why does it matter for performance?
3. What do the Platform Architect accreditations cover?

## Hands-On Lab

Per-topic walkthroughs — Spark Developer areas plus platform concepts. Run PySpark
on Free/Community Edition.

**Shared prerequisites** — a Databricks workspace or local Spark; PySpark.
**Cost:** none (Free Edition).

### Lab 8.1 — Spark architecture: transformations vs actions

**Objective:** See lazy evaluation.

```python
from pyspark.sql import functions as F
df = spark.range(1_000_000).filter("id % 2 = 0").withColumn("x", F.col("id") * 2)
# transformations (filter/withColumn) are LAZY — nothing runs yet
print(df.count())   # count() is an ACTION -> triggers the job
```

**Expected result:** `500000`, computed only when the `count()` action runs — lazy
transformations vs eager actions (a core Spark concept).

**Negative test:** expect `filter`/`withColumn` to execute immediately; they are
**lazy** — an action triggers execution.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — DataFrame API: select, filter, transform

**Objective:** Use the core DataFrame API.

```python
from pyspark.sql import functions as F
people = spark.createDataFrame([("Ann",34),("Bob",41),("Cy",29)], ["name","age"])
(people.filter(F.col("age") > 30)
       .withColumn("decade", (F.col("age")/10).cast("int")*10)
       .select("name","decade").show())
```

**Expected result:** filtered rows with a derived `decade` column — the DataFrame
API transformations the exam tests.

**Negative test:** use raw SQL strings everywhere; the **DataFrame API** (typed,
composable) is what this exam assesses — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Joins and aggregations

**Objective:** Join and aggregate DataFrames.

```python
orders = spark.createDataFrame([(1,"Ann",100),(2,"Bob",50),(3,"Ann",25)], ["id","name","amt"])
orders.groupBy("name").agg(F.sum("amt").alias("total"), F.count("*").alias("n")).show()
```

**Expected result:** per-name totals and counts — aggregation the Spark Developer
exam covers.

**Negative test:** collect and aggregate in Python; **Spark aggregations** run
distributed — keep it in Spark.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Performance: caching and partitioning

**Objective:** Cache a reused DataFrame and control partitions.

```python
df = spark.range(10_000_000).repartition(8)     # control parallelism
df.cache(); df.count()                          # materialize the cache
print("partitions:", df.rdd.getNumPartitions())
```

**Expected result:** 8 partitions and a cached DataFrame reused without
recomputation — the tuning concepts (partitioning, caching) the exam tests.

**Negative test:** cache a DataFrame used only once; caching has overhead — cache
only **reused** data.

**Rollback:** `df.unpersist()`

### Lab 8.5 — Adaptive Query Execution

**Objective:** Confirm AQE optimizes at runtime.

```python
print(spark.conf.get("spark.sql.adaptive.enabled"))   # 'true' by default
# AQE: coalesces shuffle partitions, switches join strategies, handles skew at runtime.
```

**Expected result:** AQE enabled and what it optimizes (partition coalescing, join
strategy, skew) — a performance topic on the exam.

**Negative test:** hand-tune shuffle partitions and disable AQE; **AQE** adapts at
runtime — leave it on unless you have a specific reason.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.6 — Platform accreditations: architecture and administration

**Objective:** Outline a Databricks platform deployment.

```text
Platform Architect/Administrator (per cloud):
  - Account + workspace model; identity federation (SSO/SCIM)
  - Unity Catalog metastore (one per region) + catalogs
  - Networking (private access), storage, and encryption
  - Cost controls (cluster policies, SQL warehouse sizing, budgets)
```

**Expected result:** the platform deployment/administration checklist — the
Platform Architect/Administrator accreditation scope.

**Negative test:** treat these as proctored certifications; they are free
**accreditations** — useful, but distinct from the role-based certs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Apache Spark Developer Associate certifies the Spark DataFrame API and
execution model (lazy transformations, actions, joins/aggregations, and tuning with
caching/partitioning/AQE), and the free Platform Architect/Administrator
accreditations cover deploying and administering Databricks on AWS/Azure/GCP.
Together they cover the developer and platform ends of the program.

- [ ] I can distinguish transformations from actions and explain shuffles.
- [ ] I can use the DataFrame API for select/filter/transform/join/aggregate.
- [ ] I can tune with caching, partitioning, and AQE.
- [ ] I can outline a Databricks platform deployment/administration.
- [ ] I completed Labs 8.1–8.6 including each negative test.
