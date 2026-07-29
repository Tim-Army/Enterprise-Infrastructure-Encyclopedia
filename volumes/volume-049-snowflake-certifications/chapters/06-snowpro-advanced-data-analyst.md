# Chapter 06: SnowPro Advanced — Data Analyst

## Learning Objectives

- Explain what the SnowPro Advanced: Data Analyst certifies and its prerequisite.
- Summarize the exam-guide domains.
- Apply advanced analytic SQL, semi-structured data, and window functions.
- Understand data quality and consumption/visualization.
- Complete a per-topic walkthrough for each Data Analyst domain.

## Theory and Architecture

The **SnowPro Advanced: Data Analyst (DAA-C01)** validates analyzing data on
Snowflake. It **requires SnowPro Core**. Its exam guide covers **advanced analytic
SQL** (window functions, aggregation), working with **semi-structured data** (JSON/
VARIANT), **data quality and preparation**, and **consumption/visualization**
(Snowsight, sharing results). Cortex AI functions increasingly feature.

## Design Considerations

The analyst writes advanced SQL over structured and **semi-structured** data
(`VARIANT`, `FLATTEN`), applies window functions and statistical aggregates,
ensures **data quality**, and delivers via Snowsight dashboards and sharing. Master
JSON handling and window analysis.

## Implementation and Automation

The labs below use Snowflake SQL for each domain — analytic SQL, semi-structured
data, data quality, and consumption.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
learn.snowflake.com/certifications > SnowPro Advanced: Data Analyst (DAA-C01):
  - advanced analytic SQL, semi-structured data, data quality/prep, consumption
  - requires SnowPro Core
```

Common pitfalls: parsing JSON with string functions instead of **`VARIANT`/
`FLATTEN`**; and mis-using window frames.

## Security and Best Practices

Query semi-structured data natively with **`VARIANT`** and **`LATERAL FLATTEN`**;
use **window functions** for ranking/running totals; validate **data quality**
(nulls, duplicates, ranges); and deliver via governed **Snowsight** dashboards and
secure sharing. Use **Cortex** functions for AI-assisted analysis where available.

## References and Knowledge Checks

- learn.snowflake.com: SnowPro Advanced: Data Analyst exam guide; semi-structured data and Snowsight docs.

**Knowledge checks**

1. How do you query JSON stored in a VARIANT column?
2. What is a window frame, and when do you use it?
3. What data-quality checks precede analysis?

## Hands-On Lab

Per-topic walkthroughs — Data Analyst domains. Run on a free trial.

**Shared prerequisites** — a free Snowflake trial; a warehouse. **Cost:** none.

### Lab 6.1 — Advanced analytic SQL: window functions

**Objective:** Compute a running total.

```sql
SELECT order_date, amount,
       SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM demo_db.sales.orders ORDER BY order_date;
```

**Expected result:** a running total via a window frame — the advanced analytic SQL
the exam tests.

**Negative test:** self-join to compute running totals; a **window function** is
clearer and faster.

**Cleanup:** none.

### Lab 6.2 — Semi-structured data (VARIANT / FLATTEN)

**Objective:** Query JSON stored in a VARIANT column.

```sql
CREATE TABLE demo_db.raw.events_json (v VARIANT);
INSERT INTO demo_db.raw.events_json SELECT PARSE_JSON('{"user":"ann","tags":["a","b"]}');
SELECT v:user::STRING AS user, t.value::STRING AS tag
FROM demo_db.raw.events_json, LATERAL FLATTEN(input => v:tags) t;
```

**Expected result:** the user and each tag extracted from JSON via `VARIANT` +
`LATERAL FLATTEN` — the semi-structured domain.

**Negative test:** regex-parse JSON as text; Snowflake's **VARIANT/FLATTEN** handle
it natively — use them.

**Cleanup:** `DROP TABLE IF EXISTS demo_db.raw.events_json;`

### Lab 6.3 — Data quality and preparation

**Objective:** Profile and clean data.

```sql
SELECT COUNT(*) total, COUNT(amount) non_null, COUNT(DISTINCT id) distinct_ids,
       SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) AS negatives
FROM demo_db.sales.orders;
```

**Expected result:** null/duplicate/range profiling — the data-quality checks that
precede analysis.

**Negative test:** analyze without profiling; **check quality first** or your
analysis inherits the data's flaws.

**Cleanup:** none.

### Lab 6.4 — Consumption and Cortex AI

**Objective:** Describe delivery and AI-assisted analysis.

```sql
-- Snowsight dashboards over query results; secure sharing to consumers.
SELECT SNOWFLAKE.CORTEX.SENTIMENT('The service was excellent') AS sentiment;   -- Cortex AI function
```

**Expected result:** a Cortex sentiment score (and the Snowsight/sharing concept) —
the consumption domain plus native AI.

**Negative test:** export data to an external tool for simple sentiment; **Cortex**
functions run in-platform — use them where they fit.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SnowPro Advanced: Data Analyst (requires Core) certifies analysis on Snowflake:
advanced analytic SQL (window functions), semi-structured data (VARIANT/FLATTEN),
data quality/preparation, and consumption via Snowsight and Cortex AI functions.

- [ ] I can write window-function analytics and running totals.
- [ ] I can query semi-structured data with VARIANT/FLATTEN.
- [ ] I can profile data quality before analysis.
- [ ] I can deliver via Snowsight and use Cortex functions.
- [ ] I completed Labs 6.1–6.4 including each negative test.
