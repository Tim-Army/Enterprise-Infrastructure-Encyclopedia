# Chapter 02: Data Analyst Associate

## Learning Objectives

- Explain what the Data Analyst Associate certifies and its exam format.
- Summarize the exam-guide sections.
- Apply Databricks SQL: queries, visualizations, dashboards, and the SQL warehouse.
- Understand analytics on the lakehouse with Unity Catalog.
- Complete a per-topic walkthrough for each Data Analyst area.

## Theory and Architecture

The **Databricks Certified Data Analyst Associate** validates using **Databricks
SQL** to analyze data on the lakehouse — writing SQL, building **visualizations
and dashboards**, and running queries on a **SQL warehouse** against governed
(**Unity Catalog**) data. It is the entry analytics credential. Its exam guide
covers areas such as the Databricks SQL service and warehouses, SQL for analysis
(joins, aggregation, windows), visualizations and dashboards, and data management/
governance basics.

## Design Considerations

The analyst works in **Databricks SQL** — the serverless SQL warehouse and the SQL
editor/dashboards — over lakehouse tables. Master analytic SQL (aggregation,
window functions, CTEs), how to build and share **dashboards** with parameters and
alerts, and the governance context (querying `catalog.schema.table` under Unity
Catalog). This is the SQL-first entry point before the engineering and ML certs.

## Implementation and Automation

The labs below use **Spark SQL / Databricks SQL** you can run on Free/Community
Edition — analytic queries, window functions, and dashboard/alert concepts.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
databricks.com/learn/certification > Data Analyst Associate > exam guide:
  - Databricks SQL & warehouses, SQL for analysis, visualizations/dashboards, governance
  - associate level; SQL-focused
```

Common pitfalls: confusing a **SQL warehouse** (Databricks SQL compute) with an
all-purpose cluster; and forgetting the **`catalog.schema.table`** namespace under
Unity Catalog.

## Security and Best Practices

Query governed data via **Unity Catalog**, use **SQL warehouses** (right-sized,
auto-stop) for cost control, parameterize dashboards, and set **alerts** on key
metrics. Prefer views/gold tables for analyst consumption.

## References and Knowledge Checks

- databricks.com: Data Analyst Associate exam guide; Databricks SQL documentation.

**Knowledge checks**

1. What compute does an analyst use in Databricks SQL?
2. How do you reference a table under Unity Catalog?
3. What is a window function used for in analysis?

## Hands-On Lab

Per-topic walkthroughs — Data Analyst areas. Run the SQL on Free/Community Edition.

**Shared prerequisites** — a Databricks workspace with a SQL warehouse or cluster;
sample data (or create it). **Cost:** none (Free Edition).

### Lab 2.1 — Databricks SQL: query the lakehouse

**Objective:** Run an analytic query over a governed table.

```sql
SELECT department, COUNT(*) AS headcount, ROUND(AVG(salary),2) AS avg_salary
FROM   samples.hr.employees
GROUP  BY department
ORDER  BY headcount DESC;
```

**Expected result:** per-department headcount and average salary — core analytic
SQL on a `catalog.schema.table` (Databricks SQL).

**Negative test:** query `employees` without the catalog/schema under Unity
Catalog; qualify it fully to avoid ambiguity.

**Cleanup:** none.

### Lab 2.2 — SQL for analysis: window functions

**Objective:** Rank rows within groups with a window function.

```sql
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
FROM   samples.hr.employees
QUALIFY rnk <= 3;
```

**Expected result:** the top-3 salaries per department via `RANK() OVER (...)` and
`QUALIFY` — window analysis the Data Analyst exam tests.

**Negative test:** self-join to compute per-group ranking; a **window function** is
clearer and faster — use it.

**Cleanup:** none.

### Lab 2.3 — Visualizations and dashboards

**Objective:** Describe building a parameterized dashboard.

```text
Databricks SQL dashboard:
  - query -> visualization (bar/line/pie/table)
  - parameter (e.g., :department) -> filter across widgets
  - schedule refresh + set an alert on a query result threshold
```

**Expected result:** a parameterized, scheduled dashboard with an alert — the
visualization/dashboard area of the exam.

**Negative test:** email static screenshots; a **live dashboard** with parameters
and refresh stays current — build it in Databricks SQL.

**Cleanup:** none.

### Lab 2.4 — Governance and data management for analysts

**Objective:** Use Unity Catalog objects an analyst relies on.

```sql
SHOW CATALOGS;
SHOW SCHEMAS IN samples;
DESCRIBE TABLE samples.hr.employees;   -- columns, types, comments
```

**Expected result:** the catalog/schema/table hierarchy and table metadata — the
governance context an analyst works within.

**Negative test:** assume access to any table; **Unity Catalog** grants are
per-object — you see only what you're granted.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Data Analyst Associate certifies analytics on the lakehouse with Databricks
SQL: analytic SQL (aggregation, window functions), visualizations and dashboards
on SQL warehouses, and the Unity Catalog governance context. It is the SQL-first
entry point to the Databricks program.

- [ ] I can summarize the Data Analyst exam-guide areas.
- [ ] I can write analytic SQL including window functions.
- [ ] I can build a parameterized dashboard with alerts.
- [ ] I can navigate Unity Catalog objects and metadata.
- [ ] I completed Labs 2.1–2.4 including each negative test.
