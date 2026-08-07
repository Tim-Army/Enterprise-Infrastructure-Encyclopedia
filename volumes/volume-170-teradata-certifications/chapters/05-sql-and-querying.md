# Chapter 05: SQL and Querying at Scale

## Learning Objectives

- Write Teradata SQL — ANSI SQL plus Teradata extensions.
- Understand the optimizer and how it plans parallel queries.
- Explain joins in an MPP world — co-located versus redistributed.
- Recognize the role of statistics in query performance.

*Cert relevance: SQL and query processing are core to the Associate and developer exams.*

## Teradata SQL

Teradata is queried with **SQL** — it is **ANSI-standard SQL** plus **Teradata extensions**, so anyone who knows SQL is productive quickly. You write familiar `SELECT ... FROM ... WHERE ... GROUP BY ... JOIN` statements, and Teradata runs them **in parallel across the AMPs** ([Ch 3](03-the-mpp-architecture.md)). Teradata adds extensions for analytics — **OLAP/window functions** (rankings, running totals, moving averages), rich date/time handling, and set operations — that make complex analytical queries expressible in SQL.

Because Teradata was built for **analytics**, its SQL and engine handle **large aggregations and joins** across billions of rows as a core competency, not an afterthought. Writing correct, efficient SQL — and understanding that it runs in parallel — is the foundation of using Teradata. The lab writes analytical SQL. *(SQL as the analytics interface is common across the data platforms in [Snowflake XLIX](../../volume-049-snowflake-certifications/README.md) and [Databricks XLVIII](../../volume-048-databricks-certifications/README.md).)*

## The optimizer

You write **what** you want; the **Parsing Engine's optimizer** decides **how** to execute it. Teradata's is a **cost-based optimizer**: it considers possible **execution plans** (which join order, which join method, whether to redistribute data) and picks the one it estimates is **cheapest**, then dispatches the parallel work to the AMPs.

The optimizer's decisions depend on **statistics** (below) about the data. A good plan runs a query in seconds; a bad plan (from stale statistics or poor design) can run for hours. You do not write the plan, but you **enable** the optimizer to choose well — by keeping statistics current and designing tables sensibly ([Ch 6](06-physical-database-design.md)). Understanding that the optimizer plans **parallel** execution, and depends on statistics, is key. The lab shows the optimizer choosing a plan.

## Joins in an MPP world

**Joins** are where MPP architecture most shapes SQL performance, because a join needs the matching rows **on the same AMP**:

- **Co-located join** — if both tables are distributed on the **join column** (their primary index, [Ch 4](04-data-distribution-and-primary-index.md)), matching rows **already sit on the same AMP**, so the join is **local and fast** — no data movement.
- **Redistribution** — if the tables are **not** distributed on the join column, Teradata must **redistribute** one or both tables across the BYNET so matching rows meet on the same AMP. This works but **costs data movement** (network and time).
- **Duplication** — for a small table joined to a large one, the optimizer may **duplicate** the small table to every AMP instead of redistributing the large one.

So join performance depends heavily on **how tables are distributed** relative to the join. Designing primary indexes so that **frequently-joined tables co-locate** is a major performance lever — one that only makes sense once you understand MPP. The lab compares a co-located join with a redistributed one.

## Statistics

The optimizer is only as good as its **statistics** — collected metadata about the **data distribution** in columns (how many distinct values, how skewed, value ranges). With accurate statistics, the optimizer estimates **how many rows** each step will produce and chooses the best plan (which table to redistribute, which join method). With **stale or missing** statistics, it guesses badly — choosing a slow plan.

So **collecting and maintaining statistics** (on primary indexes, join columns, and filter columns) is a core administration/design task that directly drives performance. "The query is slow" is very often "the statistics are stale." Understanding this cause-and-effect is important Teradata knowledge and a common exam theme. The lab shows the effect of statistics on the plan. *(Cost-based optimization on statistics is a shared principle of all mature query engines.)*

## Hands-On Lab

Python models analytical SQL, the optimizer, co-located vs redistributed joins, and statistics. **Cost:** none.

### Lab 5.1 — Query at scale

**Objective:** Run an aggregation, choose a join strategy by distribution, and see statistics drive the plan.

```bash
python3 - <<'EOF'
# analytical SQL: aggregate sales by region (runs in parallel across AMPs)
SALES = [{"region":"E","amount":120},{"region":"W","amount":80},{"region":"E","amount":200},{"region":"W","amount":60}]
def group_by(rows, key, agg):
    out = {}
    for r in rows: out.setdefault(r[key],0); out[r[key]] += r[agg]
    return out
print("SQL (SELECT region, SUM(amount) GROUP BY region) — parallel aggregation:")
for region, total in group_by(SALES, "region", "amount").items(): print(f"   {region}: {total}")

# JOIN strategy depends on distribution relative to the join column
def join_strategy(orders_pi, items_pi, join_col):
    if orders_pi == join_col and items_pi == join_col:
        return "CO-LOCATED join (both PI = join col) -> local on each AMP, NO data movement (fast)"
    return "REDISTRIBUTE (PI != join col) -> move rows over BYNET so matches meet (costs data movement)"
print("\nJOIN orders JOIN order_items ON order_id:")
print(f"   both PI=order_id: {join_strategy('order_id','order_id','order_id')}")
print(f"   items PI=item_id: {join_strategy('order_id','item_id','order_id')}")

# STATISTICS drive the optimizer's plan
def optimizer_plan(stats_fresh, table_a_rows, table_b_rows):
    if not stats_fresh:
        return "stale stats -> optimizer GUESSES row counts -> may redistribute the WRONG (large) table -> SLOW"
    smaller = "B" if table_b_rows < table_a_rows else "A"
    return f"fresh stats -> optimizer knows B={table_b_rows}, A={table_a_rows} -> duplicate smaller table ({smaller}) -> FAST"
print("\nOPTIMIZER + STATISTICS:")
print(f"   {optimizer_plan(True, 1_000_000, 500)}")
print(f"   {optimizer_plan(False, 1_000_000, 500)}")
print()
print("Teradata runs ANSI SQL (+ extensions like window functions) in PARALLEL across AMPs. The")
print("cost-based OPTIMIZER plans execution — and JOINS are CO-LOCATED (fast, no movement) when")
print("tables share the join column as PI, else REDISTRIBUTED (costs BYNET movement). The optimizer")
print("depends on STATISTICS: fresh stats -> good plan; stale stats -> slow plan. Design + stats = performance.")
EOF
```

**Expected result:** A parallel GROUP BY aggregation, a join that is co-located when both tables share the join column as primary index versus redistributed otherwise, and the optimizer choosing a good plan with fresh statistics versus a bad one with stale statistics. The lesson is querying at scale in Teradata: SQL runs in parallel, joins are fast when tables co-locate on the join column (else redistributed over the BYNET), and the cost-based optimizer depends on current statistics to choose a good plan.

**Negative test:** Never collecting statistics and joining tables not distributed on the join column. The optimizer guesses and redistributes the wrong table while every join moves data over the BYNET; co-locating joins by design and keeping statistics fresh is what makes queries fast at scale.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Teradata SQL understood — ANSI SQL plus analytical extensions (window functions), run in parallel.
- [ ] The optimizer understood — cost-based, plans parallel execution, depends on statistics.
- [ ] MPP joins understood — co-located (fast) when tables share the join column as PI, else redistributed.
- [ ] Statistics understood — accurate stats drive good plans; stale stats cause slow queries.

## See also

- [Chapter 04 — Data Distribution and the Primary Index](04-data-distribution-and-primary-index.md) — why join co-location depends on the PI.
- [Chapter 06 — Physical Database Design](06-physical-database-design.md) — indexes, partitioning, and collecting statistics.
- [Chapter 03 — The MPP Architecture](03-the-mpp-architecture.md) — the parallel engine SQL runs on.
