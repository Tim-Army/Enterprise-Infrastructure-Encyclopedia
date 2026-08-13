# Chapter 04: Data Engineer Professional

## Learning Objectives

- Explain what the Data Engineer Professional certifies and how it extends the Associate.
- Summarize the exam-guide sections.
- Apply advanced data modeling, processing, and optimization.
- Apply security/governance, monitoring, testing, and deployment for pipelines.
- Complete a per-topic walkthrough for each Data Engineer Professional area.

## Theory and Architecture

The **Databricks Certified Data Engineer Professional** validates advanced,
production-grade data engineering on the lakehouse. Its exam guide covers:
**Databricks tooling** (advanced Spark, Delta internals), **data processing**
(batch/incremental at scale, optimization), **data modeling** (medallion, **CDC**,
**slowly changing dimensions**), **security and governance** (Unity Catalog,
dynamic views, secrets), **monitoring and logging**, and **testing and
deployment** (CI/CD, DABs — Databricks Asset Bundles). It assumes the Associate
foundation.

## Design Considerations

The professional engineer optimizes and hardens pipelines: Delta performance
(**OPTIMIZE**, **Z-ORDER**/liquid clustering, file sizing), **CDC** and **SCD Type
2**, streaming at scale, fine-grained governance (dynamic views, row/column
masking), and **deployment** via CI/CD and **Databricks Asset Bundles**. Master
observability of jobs and data quality, and testing.

## Implementation and Automation

The labs below use advanced Spark/Delta and pipeline patterns for each area —
optimization, CDC/SCD, governance, monitoring, and deployment.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
databricks.com/learn/certification > Data Engineer Professional > exam guide:
  - tooling, data processing/optimization, data modeling (CDC/SCD), security/governance,
    monitoring/logging, testing/deployment
```

Common pitfalls: not maintaining tables (**OPTIMIZE**/clustering); implementing SCD
Type 2 incorrectly; and deploying without **CI/CD / Asset Bundles**.

## Security and Best Practices

Optimize Delta (file sizing, **liquid clustering**/Z-ORDER, `OPTIMIZE`/`VACUUM`);
model change with **CDC** and **SCD Type 2**; secure with **dynamic views** and
column/row masking in Unity Catalog; monitor jobs and **data quality**; and deploy
with **Databricks Asset Bundles** and CI/CD.

## References and Knowledge Checks

- databricks.com: Data Engineer Professional exam guide; Delta optimization, Unity Catalog, and Asset Bundles docs.

**Knowledge checks**

1. How do you optimize Delta table layout for query performance?
2. What is SCD Type 2, and when do you use it?
3. How do Databricks Asset Bundles support deployment?

## Hands-On Lab

Per-topic walkthroughs — **one lab per exam-guide area**. Run on Free/Community
Edition where possible.

**Shared prerequisites** — a Databricks workspace; PySpark/Spark SQL. **Cost:**
none (Free Edition).

### Lab 4.1 — Tooling: Delta internals and time travel

**Objective:** Inspect Delta history and query a past version.

```sql
DESCRIBE HISTORY silver_orders;                 -- versioned transaction log
SELECT * FROM silver_orders VERSION AS OF 3;    -- time travel
```

**Expected result:** the Delta transaction history and a point-in-time read — Delta
internals/time-travel the Professional exam tests.

**Negative test:** rely on manual backups for point-in-time reads; **Delta time
travel** is built in — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Data processing: optimization

**Objective:** Optimize a Delta table's layout.

```sql
OPTIMIZE silver_orders ZORDER BY (customer_id);   -- or liquid clustering
VACUUM silver_orders RETAIN 168 HOURS;
```

**Expected result:** compacted files clustered by `customer_id` and old files
vacuumed — the optimization skills of the Professional exam.

**Negative test:** never `OPTIMIZE`; many small files slow queries — compact and
cluster regularly.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Data modeling: SCD Type 2 (CDC)

**Objective:** Implement SCD Type 2 with MERGE.

```sql
MERGE INTO dim_customer t
USING staged s ON t.id = s.id AND t.is_current = true
WHEN MATCHED AND t.attributes <> s.attributes THEN
  UPDATE SET t.is_current = false, t.end_date = current_date()
-- (followed by an INSERT of the new current row)
```

**Expected result:** history preserved by closing the old row and inserting a new
current one — SCD Type 2 / CDC modeling.

**Negative test:** overwrite the dimension in place; **SCD Type 2** preserves
history — don't lose it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Security and governance: dynamic views

**Objective:** Mask data with a Unity Catalog dynamic view.

```sql
CREATE VIEW sales.masked_customers AS
SELECT id,
       CASE WHEN is_account_group_member('pii_readers') THEN email
            ELSE '***' END AS email
FROM sales.customers;
```

**Expected result:** a view that reveals email only to `pii_readers` — dynamic,
role-aware masking (Professional governance).

**Negative test:** grant raw table access to all analysts; use a **dynamic view**
to enforce column-level masking.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — Monitoring and logging

**Objective:** Add a data-quality expectation and monitor a job.

```python
# DLT expectation (drops/quarantines bad rows) + job metrics
# @dlt.expect_or_drop("valid_id", "id IS NOT NULL")
# Monitor: Jobs UI run history, alerts on failure, and query the event log.
```

**Expected result:** a data-quality expectation and job monitoring — the
monitoring/logging area of the Professional exam.

**Negative test:** ship a pipeline with no quality checks; **expectations** catch
bad data early — add them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.6 — Testing and deployment (Asset Bundles / CI/CD)

**Objective:** Describe deploying with Databricks Asset Bundles.

```yaml
# databricks.yml (Databricks Asset Bundle)
bundle: {name: sales-pipeline}
resources:
  jobs:
    etl: {name: etl, tasks: [{task_key: run, notebook_task: {notebook_path: ./etl}}]}
targets: {dev: {mode: development}, prod: {mode: production}}
```

**Expected result:** an Asset Bundle defining a job across dev/prod targets — the
CI/CD deployment approach the Professional exam covers.

**Negative test:** click-deploy jobs to production; use **Asset Bundles + CI/CD**
for versioned, repeatable deployment.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Data Engineer Professional certifies advanced lakehouse engineering: Delta
internals and optimization, CDC/SCD data modeling, fine-grained governance
(dynamic views/masking), monitoring and data quality, and testing/deployment with
Asset Bundles and CI/CD. It hardens and scales what the Associate builds.

- [ ] I can summarize the Professional exam-guide areas.
- [ ] I can use Delta time travel and optimize table layout.
- [ ] I can implement SCD Type 2 and dynamic-view masking.
- [ ] I can add data-quality expectations and deploy with Asset Bundles.
- [ ] I completed Labs 4.1–4.6 including each negative test.
