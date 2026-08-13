# Chapter 02: SnowPro Associate — Platform

## Learning Objectives

- Explain what the SnowPro Associate: Platform certifies and its level.
- Summarize the exam-guide domains.
- Apply foundational Snowflake: warehouses, databases, loading, and querying.
- Understand basic security and cost concepts.
- Complete a per-topic walkthrough for each Associate area.

## Theory and Architecture

The **SnowPro Associate: Platform** is Snowflake's **entry-level** credential,
validating foundational understanding of the AI Data Cloud — core architecture,
navigating Snowsight, running queries, loading data, basic access control, and
cost/consumption basics. It requires no prerequisites and sets up **SnowPro Core**.

## Design Considerations

The Associate is **breadth at a foundational level**. Learn the object hierarchy
(**account → database → schema → objects**), how **warehouses** provide compute,
basic **loading** (stages, `COPY INTO`), querying, the **role** model, and how
consumption/credits work. It is the conceptual on-ramp before Core's
implementation depth.

## Implementation and Automation

The labs below use **Snowflake SQL** on a free trial to make each foundational
area concrete — objects, warehouses, loading, querying, and roles.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
learn.snowflake.com/certifications > SnowPro Associate: Platform > exam guide:
  - platform architecture, navigation, querying, loading, access, cost basics
  - associate level, no prerequisites
```

Common pitfalls: confusing **database** (storage) and **warehouse** (compute); and
loading data without a **stage**.

## Security and Best Practices

Use least-privilege **roles**, right-size and **auto-suspend** warehouses to
control credits, and load via **stages** with `COPY INTO`. Understand that
**storage and compute bill separately**.

## References and Knowledge Checks

- learn.snowflake.com: SnowPro Associate: Platform exam guide; Snowflake documentation.

**Knowledge checks**

1. What is the Snowflake object hierarchy?
2. What provides compute in Snowflake, and how is it billed?
3. What is a stage used for?

## Hands-On Lab

Per-topic walkthroughs — Associate areas. Run the SQL on a free trial.

**Shared prerequisites** — a free Snowflake trial; a role that can create objects.
**Cost:** none (trial).

### Lab 2.1 — Platform architecture: object hierarchy

**Objective:** Create the account → database → schema → table hierarchy.

```sql
CREATE DATABASE IF NOT EXISTS demo_db;
CREATE SCHEMA IF NOT EXISTS demo_db.sales;
CREATE TABLE demo_db.sales.orders (id INT, amount NUMBER(12,2));
SHOW TABLES IN SCHEMA demo_db.sales;
```

**Expected result:** the nested object hierarchy with an `orders` table — the
foundational structure the Associate tests.

**Negative test:** create a table with no database/schema context; qualify names
(`db.schema.table`) — objects live in the hierarchy.

**Rollback:** `DROP DATABASE IF EXISTS demo_db;`

### Lab 2.2 — Compute: warehouses

**Objective:** Create and size a warehouse.

```sql
CREATE WAREHOUSE demo_wh WAREHOUSE_SIZE='XSMALL' AUTO_SUSPEND=60 AUTO_RESUME=TRUE;
USE WAREHOUSE demo_wh;
SELECT 1;   -- runs on demo_wh
```

**Expected result:** an auto-suspending XSMALL warehouse running a query — compute
provisioning and cost control.

**Negative test:** leave `AUTO_SUSPEND` off; an idle warehouse burns credits — set
auto-suspend.

**Rollback:** `DROP WAREHOUSE IF EXISTS demo_wh;`

### Lab 2.3 — Loading: stages and COPY INTO

**Objective:** Describe loading via a stage.

```sql
CREATE STAGE demo_stage;
-- PUT file://orders.csv @demo_stage;   (from SnowSQL client)
COPY INTO demo_db.sales.orders
FROM @demo_stage FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1);
```

**Expected result:** the stage → `COPY INTO` load path — the loading foundation of
the Associate exam.

**Negative test:** `INSERT` millions of rows one by one; use **`COPY INTO`** from a
stage for bulk loading.

**Rollback:** `DROP STAGE IF EXISTS demo_stage;`

### Lab 2.4 — Querying and access

**Objective:** Query data and read role context.

```sql
SELECT COUNT(*) FROM demo_db.sales.orders;
SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE();
```

**Expected result:** a row count and the current role/warehouse/database — querying
and the access context the Associate covers.

**Negative test:** query with no warehouse set; a query needs a **running
warehouse** — set one first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SnowPro Associate: Platform certifies foundational Snowflake: the object
hierarchy, warehouses (compute) vs databases (storage), loading via stages and
`COPY INTO`, querying, and basic roles and cost. It is the conceptual on-ramp to
SnowPro Core.

- [ ] I can summarize the Associate exam-guide areas.
- [ ] I can create the object hierarchy and a warehouse.
- [ ] I can load via a stage with `COPY INTO` and query.
- [ ] I can read role/warehouse/database context.
- [ ] I completed Labs 2.1–2.4 including each negative test.
