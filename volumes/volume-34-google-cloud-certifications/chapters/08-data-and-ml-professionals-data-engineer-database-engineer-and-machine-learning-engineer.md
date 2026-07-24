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

These labs cover the exam-guide topics for all three certifications in
this chapter. **Professional Data Engineer** is covered topic by topic
(its guide publishes 19 sub-topics); **Cloud Database Engineer** and
**Machine Learning Engineer** are covered at section level with their
published weights. Mapping is in the
[volume README](../README.md#lab-coverage--data-and-ml-professionals).

**Cost note:** BigQuery dry runs are free and used throughout. The public
datasets cost nothing to query at these sizes. Lab 8.20 deletes
everything created.

**Prerequisites**

```bash
export PROJECT_ID="$(gcloud config get-value project)"
bq mk --dataset --location=us-central1 "${PROJECT_ID}:de_lab" 2>/dev/null
bq ls --format=pretty "${PROJECT_ID}:" | grep de_lab
```

**Expected result:** `de_lab` listed.

### Lab 8.1 — Designing for security and compliance *(DE 1.1)*

```bash
bq show --format=prettyjson "${PROJECT_ID}:de_lab" | grep -E '"location"|"access"' | head -5
```

**Expected result:** `"location": "us-central1"` and an access block.
Dataset location is a compliance control fixed at creation — it cannot be
changed later, only recreated elsewhere.

### Lab 8.2 — Designing for reliability and fidelity *(DE 1.2)*

```bash
bq query --use_legacy_sql=false --dry_run \
 'SELECT COUNT(*) c, COUNTIF(word IS NULL) nulls
  FROM `bigquery-public-data.samples.shakespeare`'
```

**Expected result:** a bytes estimate and no execution. Fidelity checks
belong in the pipeline as queries like this — count plus null count is the
minimum contract on any ingested table.

### Lab 8.3 — Designing for flexibility and portability *(DE 1.3)*

```bash
bq show --schema --format=prettyjson bigquery-public-data:samples.shakespeare
```

**Expected result:** a JSON schema array. A schema exported this way is
the portable artifact — it recreates the table shape on another platform
without moving data.

### Lab 8.4 — Designing data migrations *(DE 1.4)*

```bash
gcloud services list --available --filter="name:datamigration OR name:datastream" \
  --format='value(name)'
```

**Expected result:** `datamigration.googleapis.com` and
`datastream.googleapis.com` available. Migration is a service selection
before it is a data movement — record which one a stated cutover window
would force.

### Lab 8.5 — Planning the data pipelines *(DE 2.1)*

```bash
bq mk --table --time_partitioning_field=event_date --time_partitioning_type=DAY \
  --clustering_fields=customer_id \
  "${PROJECT_ID}:de_lab.events" \
  event_date:DATE,customer_id:STRING,amount:NUMERIC
bq show --format=prettyjson "${PROJECT_ID}:de_lab.events" | grep -A3 timePartitioning
```

**Expected result:** a `timePartitioning` block naming `event_date`.
Partition and cluster keys are pipeline design decisions, fixed before the
first row lands.

### Lab 8.6 — Building the pipelines *(DE 2.2)*

```bash
bq query --use_legacy_sql=false \
 'INSERT INTO `'"${PROJECT_ID}"'.de_lab.events` (event_date, customer_id, amount)
  VALUES (DATE "2026-07-01","c1",10.5), (DATE "2026-07-02","c2",20.0)'
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `'"${PROJECT_ID}"'.de_lab.events`'
```

**Expected result:** `2`. A pipeline is not built until rows are readable
at the far end — the count is the proof.

### Lab 8.7 — Deploying and operationalizing pipelines *(DE 2.3)*

```bash
bq ls -j --max_results=3 --format='table(jobId, state, statistics.query.totalBytesProcessed)'
```

**Expected result:** your recent jobs with state `DONE` and bytes
processed. Job history is the operational surface — it answers "did it
run, and what did it cost?"

### Lab 8.8 — Selecting storage systems *(DE 3.1)*

```bash
gcloud storage buckets create "gs://de-lab-${PROJECT_ID}" \
  --location=us-central1 --uniform-bucket-level-access
gcloud storage buckets describe "gs://de-lab-${PROJECT_ID}" \
  --format='value(storageClass, location)'
```

**Expected result:** `STANDARD US-CENTRAL1`. Object storage and BigQuery
are different answers — state the access pattern that selects each.

### Lab 8.9 — Planning for a data warehouse *(DE 3.2)*

```bash
bq query --use_legacy_sql=false --dry_run \
 'SELECT customer_id, SUM(amount) FROM `'"${PROJECT_ID}"'.de_lab.events`
  WHERE event_date = "2026-07-01" GROUP BY customer_id'
```

**Expected result:** a small bytes figure — the partition filter pruned
the scan. Warehouse planning *is* this arithmetic.

### Lab 8.10 — Using a data lake *(DE 3.3)*

```bash
echo '{"customer_id":"c3","amount":30.0,"event_date":"2026-07-03"}' > /tmp/e.json
gcloud storage cp /tmp/e.json "gs://de-lab-${PROJECT_ID}/raw/"
gcloud storage ls "gs://de-lab-${PROJECT_ID}/raw/"
```

**Expected result:** the object listed. Raw landing in object storage
ahead of load is the lake pattern — the file stays authoritative.

### Lab 8.11 — Designing for a data platform *(DE 3.4)*

```bash
bq query --use_legacy_sql=false \
 'CREATE OR REPLACE VIEW `'"${PROJECT_ID}"'.de_lab.v_daily` AS
  SELECT event_date, SUM(amount) total FROM `'"${PROJECT_ID}"'.de_lab.events`
  GROUP BY event_date'
bq show --format=prettyjson "${PROJECT_ID}:de_lab.v_daily" | grep '"query"' | head -1
```

**Expected result:** the view definition echoed back. A view is the
platform's contract with consumers — they depend on it, not the table.

### Lab 8.12 — Preparing data for visualization *(DE 4.1)*

```bash
bq query --use_legacy_sql=false --format=csv \
 'SELECT * FROM `'"${PROJECT_ID}"'.de_lab.v_daily` ORDER BY event_date'
```

**Expected result:** CSV rows with a header — the shape a BI tool
consumes.

### Lab 8.13 — Preparing data for AI and ML *(DE 4.2)*

```bash
bq query --use_legacy_sql=false --dry_run \
 'SELECT customer_id, AVG(amount) AS avg_amount
  FROM `'"${PROJECT_ID}"'.de_lab.events` GROUP BY customer_id'
```

**Expected result:** a bytes estimate. Feature preparation is a query
before it is a model — this aggregate is a feature.

### Lab 8.14 — Sharing data *(DE 4.3)*

```bash
bq show --format=prettyjson "${PROJECT_ID}:de_lab" | grep -A6 '"access"' | head -10
```

**Expected result:** the dataset access list. Sharing via an **authorized
view** grants the view, not the base table — that distinction is the
examinable one.

### Lab 8.15 — Optimizing resources *(DE 5.1)*

```bash
bq query --use_legacy_sql=false --dry_run \
 'SELECT * FROM `'"${PROJECT_ID}"'.de_lab.events`'
```

**Expected result:** a larger bytes figure than Lab 8.9's. `SELECT *`
against columnar storage is a cost decision, and the two numbers prove it.

### Lab 8.16 — Designing automation and repeatability *(DE 5.2)*

```bash
bq mk --transfer_config --data_source=scheduled_query \
  --target_dataset=de_lab --display_name=daily_rollup \
  --schedule='every 24 hours' \
  --params='{"query":"SELECT 1","destination_table_name_template":"rollup","write_disposition":"WRITE_TRUNCATE"}' \
  2>&1 | head -3
```

**Expected result:** either a transfer config ID, or a message that the
Data Transfer API must be enabled — both are informative. Scheduling is
where a query becomes a workload.

### Lab 8.17 — Organizing workloads and monitoring *(DE 5.3, 5.4)*

```bash
bq ls -j --max_results=5 \
  --format='table(jobId, state, statistics.query.totalSlotMs)'
```

**Expected result:** slot-milliseconds per job — the unit that shows which
workload actually consumes capacity.

### Lab 8.18 — Awareness of failures and mitigation *(DE 5.5)*

```bash
bq query --use_legacy_sql=false \
 'SELECT * FROM `'"${PROJECT_ID}"'.de_lab.no_such_table`' 2>&1 | head -3
```

**Expected result:** `Not found: Table ... no_such_table`. Knowing the
exact failure string is what lets an alert distinguish a missing table
from a permissions error.

### Lab 8.19 — Database and ML sections *(DBE 1–4, MLE 1–6)*

Database Engineer — capacity, HA/DR, connectivity, and service selection
(section 1, ~32%):

```bash
gcloud sql tiers list --format='table(tier, RAM, DiskQuota)' | head -6
```

**Expected result:** available Cloud SQL machine tiers — the sizing
catalogue section 1.1 asks you to select from. Then record, for a stated
RPO/RTO: zonal, regional, or multi-regional, and why the other two fail.

Machine Learning Engineer — serving and monitoring (sections 4 and 6):

```bash
gcloud ai models list --region=us-central1 --format='table(displayName)' 2>&1 | head -3
gcloud ai endpoints list --region=us-central1 --format='table(displayName)' 2>&1 | head -3
```

**Expected result:** empty lists (or a "must enable API" message) on a
fresh project — which is the correct starting state. The examinable point
is that a *model* and an *endpoint* are separate objects: training
produces the first, serving requires the second, and drift monitoring
attaches to the endpoint.

### Lab 8.20 — Negative test and cleanup

Prove partitioning is what prunes, not the `WHERE` clause:

```bash
bq mk --table "${PROJECT_ID}:de_lab.events_flat" \
  event_date:DATE,customer_id:STRING,amount:NUMERIC
bq query --use_legacy_sql=false --dry_run \
 'SELECT SUM(amount) FROM `'"${PROJECT_ID}"'.de_lab.events_flat` WHERE event_date = "2026-07-01"'
```

**Expected result:** the same bytes figure as an unfiltered scan of that
table — the filter did **not** prune, because the table is not partitioned
on `event_date`. Compare against Lab 8.9. This is the misconception the
lab exists to break.

```bash
gcloud projects delete "$PROJECT_ID" --quiet
gcloud projects describe "$PROJECT_ID" --format='value(lifecycleState)'
```

**Expected result:** `DELETE_REQUESTED`, removing the datasets, bucket,
and any transfer config together.

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
