# Chapter 08: Data and ML Professionals — Data Engineer, Database Engineer, and Machine Learning Engineer

## Learning Objectives

- Identify the three professional data and ML certifications and the
  distinct roles they serve
- Describe BigQuery's architecture and the cost model that governs every
  design decision made around it
- Distinguish Google Cloud's database services by access pattern,
  consistency, and scale
- Describe the machine learning engineer's surface, from Vertex AI through
  MLOps
- Recognize why this track is the most exposed to the Google Cloud
  Next '26 refresh

## Theory and Architecture

### Three certifications

| Certification | Role |
| --- | --- |
| Professional Data Engineer | Designs and operates data processing systems and analytics |
| Professional Cloud Database Engineer | Designs, manages, and migrates operational databases |
| Professional Machine Learning Engineer | Builds, deploys, and operates ML systems |

All three are **2 hours, $200, 50–60 multiple choice and multiple select
questions**, valid **two years**, no prerequisites (verified
23 July 2026). The associate **Data Practitioner**
([Chapter 04](04-associate-workspace-administrator-and-data-practitioner.md))
is the on-ramp to all three.

**This is the track most exposed to change.** Google's certification page
names **Google Cloud's data and analytics stack** as one of two areas
being refreshed after Google Cloud Next '26
([Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md)).
Read the exam guides before committing study time here — more than
anywhere else in this volume.

### BigQuery: the architecture the cost model follows from

BigQuery separates **storage** from **compute**, and understanding that
separation explains nearly every design recommendation:

- **Storage** is columnar and charged by bytes stored, with cheaper
  long-term storage for partitions untouched for 90 days.
- **Compute** is charged either **on-demand by bytes scanned** or through
  **capacity (slot) reservations** at a flat rate.
- Because storage is columnar, a query reads **only the columns it
  references**. `SELECT *` is not a stylistic complaint on BigQuery; it is
  a direct multiplier on cost.

Three design levers follow, and they are examined repeatedly:

- **Partitioning** — usually by ingestion time or a date column. A query
  filtering on the partition column prunes whole partitions and scans
  dramatically less.
- **Clustering** — sorts data within partitions by chosen columns,
  narrowing scans further on filtered and aggregated queries.
- **Materialized views and BI Engine** — precomputation and caching for
  repeated query patterns.

The habit that follows: **always dry-run**
([Chapter 04](04-associate-workspace-administrator-and-data-practitioner.md)).
A query that scans an unpartitioned table is a cost incident waiting to
happen, and the dry run exposes it for free.

### Choosing a database

The Database Engineer certification is fundamentally about matching a
service to an access pattern:

| Service | Model | Choose when |
| --- | --- | --- |
| Cloud SQL | Managed MySQL/PostgreSQL/SQL Server | Regional relational workloads, lift-and-shift migrations |
| AlloyDB | PostgreSQL-compatible, high performance | Demanding PostgreSQL workloads needing more than Cloud SQL |
| Spanner | Globally distributed, strongly consistent relational | Global scale **and** strong consistency **and** relational — its combination is the differentiator |
| Firestore | Document, serverless | Application data with known access patterns, mobile/web sync |
| Bigtable | Wide-column, low latency at scale | Very high throughput key-range access — time series, IoT |
| Memorystore | Managed Redis/Memcached | Caching |

**Spanner is the distinctive one.** Horizontal scale with strong
consistency and relational semantics is the combination other platforms
generally force you to trade away, and a requirement naming all three
points at it. It is also expensive, so a requirement lacking one of the
three usually points elsewhere — recognizing that is the exam skill.

### Machine Learning Engineer: Vertex AI and MLOps

The ML certification covers framing a problem, preparing data, building
and training models, deploying and serving, and — weighted heavily —
**operating** them. **Vertex AI** is the platform: training, pipelines,
feature store, model registry, endpoints, and monitoring.

The distinguishing emphasis is MLOps rather than modeling. Expect
scenarios about **training/serving skew**, **model and data drift**,
retraining triggers, and pipeline reproducibility. A model that trains
well and degrades silently in production is the failure this certification
is built around, and monitoring for drift is the answer it expects.

Generative AI on Vertex AI sits inside this surface too, and is precisely
the area the Next '26 refresh touches.

## Design Considerations

- **Read these exam guides first.** The data and analytics stack is named
  in the refresh notice; study material more than a few months old may
  omit examined products.
- **Design BigQuery around partition and cluster keys.** They are the
  levers that decide cost and performance, and like Cosmos DB's partition
  key they are painful to change after data lands.
- **Let all three requirements select Spanner.** Global scale, strong
  consistency, and relational semantics together justify it; any two of
  the three usually point at a cheaper service.
- **Weight MLOps over modeling.** The ML certification rewards knowing how
  a deployed model is monitored and retrained more than how it is built.
- **Use Data Practitioner as the entry decision.** It is the cheaper way to
  discover whether this track suits you before a $200, two-year
  commitment.

## Implementation and Automation

### Partitioned and clustered table

```bash
bq mk --table \
  --time_partitioning_field=event_date \
  --time_partitioning_type=DAY \
  --clustering_fields=customer_id \
  <PROJECT_ID>:<DATASET>.events \
  event_date:DATE,customer_id:STRING,amount:NUMERIC
```

### Proving partition pruning works

```bash
# Filtered on the partition column — scans one partition
bq query --use_legacy_sql=false --dry_run \
  'SELECT SUM(amount) FROM `<PROJECT_ID>.<DATASET>.events` WHERE event_date = "2026-07-01"'
```

```bash
# Same query without the partition filter — scans everything
bq query --use_legacy_sql=false --dry_run \
  'SELECT SUM(amount) FROM `<PROJECT_ID>.<DATASET>.events`'
```

### Inspecting a Vertex AI model's serving surface

```bash
gcloud ai models list --region=us-central1
gcloud ai endpoints list --region=us-central1 \
  --format='table(displayName, deployedModels.len())'
```

## Validation and Troubleshooting

- **Dry-run before every query.** The bytes-scanned figure is the cost.
  Comparing the two dry runs above is the clearest possible demonstration
  of why partitioning matters.
- **Read the query plan for skew.** A slow BigQuery query is usually
  skewed or scanning too much, not under-resourced; the execution details
  show which stage dominates.
- **Verify partitioning is actually in force**:

  ```bash
  bq show --format=prettyjson <PROJECT_ID>:<DATASET>.events | grep -A3 timePartitioning
  ```

- **For databases, confirm the replica topology matches the RPO.** A
  read replica is not a disaster-recovery plan unless failover is tested.
- **For ML, monitor for drift explicitly.** Training/serving skew is
  invisible in offline metrics; only production monitoring surfaces it,
  which is why the certification weights it.

## Security and Best Practices

- Use **authorized views** or column-level access rather than granting
  table access when sharing analytical data; least privilege in BigQuery
  is a data-governance control.
- Apply **Sensitive Data Protection** to discover and de-identify personal
  data before it spreads through a pipeline — remediation after the fact
  is far harder.
- Pair this track with **VPC Service Controls**
  ([Chapter 07](07-security-professionals-cloud-security-engineer-and-security-operations-engineer.md)):
  analytics data is exactly what exfiltration controls exist for.
- Never train on data you have not confirmed you may use; provenance and
  consent are governance requirements, not paperwork, and responsible-AI
  considerations are examinable.
- BigQuery costs scale with bytes scanned. Set **custom cost controls** on
  the project and use the sandbox budget alert from Chapter 01 — this is
  the track where study labs most easily become expensive.

## References and Knowledge Checks

**References**

- [Professional Data Engineer](https://cloud.google.com/certification/data-engineer)
- [Professional Cloud Database Engineer](https://cloud.google.com/certification/cloud-database-engineer)
- [Professional Machine Learning Engineer](https://cloud.google.com/certification/machine-learning-engineer)
- [BigQuery documentation](https://cloud.google.com/bigquery/docs)
- [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Chapter 04](04-associate-workspace-administrator-and-data-practitioner.md)
  for Data Practitioner, the on-ramp to this track.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. Explain how BigQuery's storage/compute separation produces its cost
   model, and why `SELECT *` is a cost decision.
2. Distinguish partitioning from clustering, and say which prunes whole
   blocks of data.
3. Name the three requirements that together justify Spanner, and say what
   happens if only two hold.
4. What is training/serving skew, and why can offline metrics not detect
   it?
5. Why is this track the most exposed to the Next '26 refresh?

## Hands-On Lab

**Objective:** Demonstrate, in bytes, that partitioning and column
selection govern BigQuery cost — the single most consequential habit in
this track.

**Cost note:** All dry runs are free. The one real query in step 4 is
tiny. Do **not** run the unfiltered query in step 3 without `--dry_run`.

**Prerequisites**

- The sandbox project and budget alert from Chapter 01.
- `bq` authenticated.

**Steps**

1. **Create a partitioned, clustered table (15 minutes).** Use the `bq mk`
   command from the Implementation section, then load a small sample or
   insert a handful of rows spanning several dates.

   **Expected result:** the table exists; `bq show` reports
   `timePartitioning`.

2. **Dry-run with a partition filter (5 minutes).** Run the filtered query.

   **Expected result:** a small bytes-scanned figure — one partition.

3. **Dry-run without the filter (5 minutes).** Run the unfiltered query.

   **Expected result:** a substantially larger figure. Record both
   numbers; the ratio is the value of partitioning, measured rather than
   asserted.

4. **Column selection (10 minutes).** Dry-run `SELECT *` against the same
   table, then `SELECT amount` only.

   **Expected result:** `SELECT *` scans more, because storage is
   columnar. Run only the narrow query for real.

5. **Negative test (10 minutes).** Create a second table **without**
   partitioning, load the same rows, and dry-run the date-filtered query
   against it.

   **Expected result:** the filter does **not** reduce bytes scanned —
   proving that a `WHERE` clause alone does not prune; the table must be
   partitioned on that column. This is the misconception the lab exists to
   break.

6. **Cleanup:**

   ```bash
   bq rm -f -t <PROJECT_ID>:<DATASET>.events
   bq rm -f -t <PROJECT_ID>:<DATASET>.events_unpartitioned
   ```

   Or delete the project. Confirm the budget shows only the small step-4
   query.

## Lab Verification

Complete this sign-off once the partitioned and unpartitioned scan figures
have been compared and recorded. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The data and ML track holds three professional certifications — Data
Engineer, Cloud Database Engineer, and Machine Learning Engineer — each
$200, two hours, and valid two years, with Data Practitioner as the
associate on-ramp. **BigQuery's separation of storage from compute**
produces its cost model: columnar storage means queries pay for the
columns and partitions they touch, so partitioning, clustering, and column
selection are cost decisions rather than style. **Spanner** is justified
only when global scale, strong consistency, and relational semantics are
all required. The ML certification weights **MLOps over modeling** —
training/serving skew and drift are the failures it is built around. This
is also the track most exposed to the Google Cloud Next '26 refresh, so
the exam guides deserve reading before any study material is bought.

- [ ] Can explain BigQuery's cost model from its architecture.
- [ ] Can distinguish partitioning from clustering.
- [ ] Knows the three requirements that together justify Spanner.
- [ ] Can explain training/serving skew and why monitoring catches it.
- [ ] Has measured the scan difference between partitioned and
      unpartitioned tables.
- [ ] Completed the hands-on lab, including the unpartitioned negative
      test and cleanup.
