# Chapter 06: Calculations — Calculated Fields, LOD, and Table Calcs

## Learning Objectives

- Create calculated fields for derived values.
- Understand Level-of-Detail (LOD) expressions — FIXED, INCLUDE, EXCLUDE.
- Apply table calculations for running totals, percent-of-total, and rank.
- Recognize calculations as the analytical depth beyond drag-and-drop.

*Cert relevance: calculations — especially **LOD expressions** — are the deepest **Data Analyst** topic and a common point of difficulty.*

## Calculated fields

Beyond the fields in your data, you often need **derived values** — a **calculated field** written in Tableau's formula language: `Profit Ratio = SUM(Profit) / SUM(Sales)`, `[Order Date]` bucketed into a category, a string cleaned, a conditional flag. Calculated fields extend the data with the specific metrics your analysis needs, and range from simple arithmetic to complex logic. They are the first level of analytical depth beyond dragging existing fields. The lab is covered within the LOD exercise.

## Level-of-Detail (LOD) expressions

The signature advanced concept — and the one that most challenges learners — is **Level-of-Detail (LOD) expressions**. Normally a measure aggregates at the level of the [dimensions in the view (Chapter 4)](04-dimensions-measures-and-the-grammar.md). But sometimes you need a value computed at a *different* level than the view — and LOD expressions let you **specify the aggregation level explicitly**, independent of the view:

| LOD | Computes at | Example use |
|:---|:---|:---|
| **FIXED** | A *specified* set of dimensions, ignoring the view | Total sales per customer, shown alongside per-order rows |
| **INCLUDE** | The view's dimensions *plus* extra ones | Average of a finer-grained aggregate |
| **EXCLUDE** | The view's dimensions *minus* some | Percent of a total that ignores a view dimension |

The classic case: you want each customer's **lifetime total** displayed on a view that is broken down by individual order. The view is at the order level, but you need a *customer-level* number — `{FIXED [Customer]: SUM([Sales])}` computes it at the customer level regardless of the view. LOD expressions are what let analysis mix aggregation levels, and understanding *when* the view level differs from the *needed* level is the key insight. The lab models FIXED.

## Table calculations

**Table calculations** compute on the **already-aggregated data in the view** (the visible table of results), rather than the underlying rows. They power common analytical patterns: **running total** (cumulative sum), **percent of total** (each value's share), **rank**, **moving average**, **difference from previous**. Because they operate on the view's result table, they depend on how the table is **partitioned and ordered** (the "compute using" direction) — a running total *along* months versus *down* categories gives different results. Table calcs add time-series and ranking analysis on top of the aggregated view. The lab is covered within the calculation exercises.

## Hands-On Lab

Python models calculations. **Cost:** none.

### Lab 6.1 — LOD FIXED: mixing aggregation levels

**Objective:** Show a customer-level total on an order-level view.

```bash
python3 - <<'EOF'
# orders (the view is at the ORDER level); we want each customer's LIFETIME total too
ORDERS = [
  {"customer": "Alice", "order": 1, "sales": 100},
  {"customer": "Alice", "order": 2, "sales": 150},
  {"customer": "Alice", "order": 3, "sales": 50},
  {"customer": "Bob",   "order": 4, "sales": 200},
  {"customer": "Bob",   "order": 5, "sales": 300},
]
# FIXED [Customer]: SUM([Sales]) -> compute total per customer, IGNORING the order-level view
from collections import defaultdict
customer_total = defaultdict(float)
for o in ORDERS:
    customer_total[o["customer"]] += o["sales"]

print("View is at the ORDER level (one row per order). We also want each customer's")
print("LIFETIME total — a CUSTOMER-level number on an ORDER-level view.\n")
print(f"   {'customer':10}{'order':>6}{'order sales':>12}{'FIXED cust total':>18}")
for o in ORDERS:
    ct = customer_total[o["customer"]]
    print(f"   {o['customer']:10}{o['order']:>6}{o['sales']:>12}{ct:>18.0f}")
print("\n   the last column = {FIXED [Customer]: SUM([Sales])} — Alice's 300 and Bob's")
print("   500 appear on EVERY one of their order rows, computed at the CUSTOMER level")
print("   REGARDLESS of the order-level view.\n")
# now use it: what % of the customer's lifetime value is each order?
print("Now a derived metric — each order as a % of the customer's lifetime value:")
for o in ORDERS:
    ct = customer_total[o["customer"]]
    print(f"   {o['customer']} order {o['order']}: {o['sales']}/{ct:.0f} = {100*o['sales']/ct:.0f}% of lifetime")
print("\nThe LOD insight: normally a measure aggregates at the VIEW's level (per order")
print("here). But sometimes you need a value at a DIFFERENT level — a customer lifetime")
print("total on an order-level view. FIXED lets you SPECIFY the aggregation level")
print("(per Customer) independent of the view, so you can mix levels: show per-order")
print("rows AND the customer total, and compute 'order as % of lifetime.' Knowing WHEN")
print("the view level differs from the NEEDED level is the key LOD skill the Data")
print("Analyst cert tests — and the #1 thing learners find hard.")
EOF
```

**Expected result:** A FIXED LOD expression computing each customer's lifetime total at the customer level and displaying it on every order-level row, enabling a per-order-as-percent-of-lifetime metric. The LOD lesson is that measures normally aggregate at the view's level, but FIXED specifies a different level explicitly, letting analysis mix aggregation levels — the key advanced skill and the most common difficulty.

**Negative test:** Trying to compute a customer lifetime total on an order-level view with a plain aggregation. It would sum only the current order's level; a FIXED LOD expression computes at the customer level regardless of the view, which is what mixing levels requires.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Table calculation: running total and percent of total

**Objective:** Compute on the aggregated view, respecting partition and order.

```bash
python3 - <<'EOF'
# monthly sales already aggregated in the view; table calcs operate on THIS result table
MONTHLY = [("Jan", 100), ("Feb", 130), ("Mar", 90), ("Apr", 160), ("May", 120)]
total = sum(v for _, v in MONTHLY)

print("Aggregated view: SUM(Sales) by month. Table calcs compute on THIS result:\n")
print(f"   {'month':6}{'sales':>7}{'running total':>15}{'% of total':>12}")
running = 0
for m, v in MONTHLY:
    running += v                       # RUNNING TOTAL: cumulative along the table
    pct = 100 * v / total              # PERCENT OF TOTAL: share of the grand total
    print(f"   {m:6}{v:>7}{running:>15}{pct:>11.0f}%")
print("\n   RUNNING TOTAL accumulates DOWN the table (Jan, +Feb, +Mar...) -> ends at the")
print(f"      grand total ({total}). Great for cumulative-to-date charts.")
print("   PERCENT OF TOTAL divides each value by the grand total -> each month's share.")
print("\nTable calculations compute on the ALREADY-AGGREGATED data in the view (not the")
print("raw rows). They power running totals, % of total, rank, moving average, and")
print("difference-from-previous. Crucially they depend on PARTITION + ORDER ('compute")
print("using'): a running total ALONG months differs from one DOWN categories. Same")
print("calc, different direction, different result — a common cert gotcha. Table calcs")
print("add time-series + ranking analysis on top of the aggregated view.")
EOF
```

**Expected result:** A running total accumulating down the monthly view to the grand total and a percent-of-total giving each month's share, both computed on the aggregated result and dependent on partition and order. The table-calculation lesson is that these operate on the already-aggregated view (not raw rows) and depend on the compute-using direction, powering running totals, percent-of-total, rank, and moving averages.

**Negative test:** Assuming a table calculation gives the same result regardless of direction. A running total along months differs from one down categories — table calcs depend on the partition and order (compute using), a common source of error.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Calculated fields understood as derived values extending the data with the metrics analysis needs.
- [ ] LOD expressions (FIXED, INCLUDE, EXCLUDE) understood as specifying aggregation level independent of the view.
- [ ] Table calculations understood as computing on the aggregated view, dependent on partition and order.
- [ ] Calculations recognized as the analytical depth beyond drag-and-drop, with LOD the key advanced skill.
