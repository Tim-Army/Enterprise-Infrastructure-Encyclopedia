# Chapter 03: Connecting and Preparing Data

## Learning Objectives

- Distinguish live connections from extracts and their trade-offs.
- Understand the data model — joins, blends, and relationships.
- Place Tableau Prep for shaping and cleaning data.
- Recognize that good analysis starts with well-prepared data.

*Cert relevance: connecting and preparing data is the foundation of **Desktop Specialist** and a major **Data Analyst** topic.*

## Live versus extract

Tableau connects to data two ways, and choosing correctly is a core skill:

| | **Live connection** | **Extract (.hyper)** |
|:---|:---|:---|
| Queries | The source database directly, in real time | A snapshot pulled into Tableau's fast engine |
| Freshness | Always current | As of the last refresh |
| Performance | Depends on the source | Fast (Tableau's optimized columnar engine) |
| Use when | Data changes constantly and must be live | Source is slow, remote, or you need speed |

A **live** connection always shows current data but is only as fast as the underlying database (a slow warehouse makes a slow dashboard). An **extract** takes a **snapshot** into Tableau's high-performance **Hyper** engine — much faster for interaction, but the data is only as fresh as the last refresh. The trade-off is **freshness versus speed**, and the certifications test knowing which fits a scenario. The lab models it.

## The data model: joins, blends, relationships

Real analysis usually needs data from **multiple tables** (orders + customers + products), and Tableau offers three ways to combine them:

- **Joins** — row-level combination (like SQL joins) into one flat table; the classic approach, but can duplicate data if the granularity differs.
- **Blends** — combining data from *different sources* at an aggregated level (a primary and secondary source linked on a common field).
- **Relationships** — the *modern* default: you define how tables *relate* (the "noodle" model) without flattening them, and Tableau chooses the right join *automatically per visualization* based on the fields used — avoiding the duplication traps of manual joins.

**Relationships** are the current best practice because they keep each table at its native granularity and let Tableau handle the join logic contextually, which the newer certifications emphasize. Understanding *why relationships avoid the duplication that naive joins cause* is a key concept. The lab models the duplication trap.

## Tableau Prep

Sometimes data needs real **cleaning and reshaping** before analysis — pivoting, splitting fields, removing duplicates, joining, aggregating — and doing this in the visualization tool is awkward. **Tableau Prep** is the dedicated visual **data-preparation** tool: you build a **flow** of cleaning/shaping steps (a visual ETL pipeline) that you can inspect at each stage and re-run. It handles the "get the data into the right shape first" work that good analysis depends on. The lab is covered within the preparation exercise.

## Hands-On Lab

Python models data connection and modeling. **Cost:** none.

### Lab 3.1 — Live versus extract trade-off

**Objective:** Choose the connection type for a scenario.

```bash
python3 - <<'EOF'
SCENARIOS = [
  # scenario,                                        best,       why
  ("live stock-trading dashboard (must be current)", "LIVE",     "freshness is critical; seconds matter"),
  ("monthly sales report off a slow warehouse",      "EXTRACT",  "speed > freshness; refresh nightly"),
  ("exploring a 500M-row dataset interactively",     "EXTRACT",  "Hyper engine makes interaction fast"),
  ("operational monitoring of a live system",        "LIVE",     "must reflect current state"),
  ("dashboard on a remote DB with slow queries",     "EXTRACT",  "avoid hitting the slow source per interaction"),
]
print(f"{'scenario':50}{'choice':>9}   why")
for scen, choice, why in SCENARIOS:
    print(f"{scen:50}{choice:>9}   {why}")
print("\nThe trade-off is FRESHNESS vs SPEED:")
print("  LIVE — always current, but only as fast as the source DB. Use when the data")
print("     CHANGES constantly and must be up-to-the-second (trading, ops monitoring).")
print("  EXTRACT — a snapshot in Tableau's fast Hyper engine: interaction is quick even")
print("     on huge/slow/remote sources, but data is only as fresh as the last refresh.")
print("     Use when SPEED matters more than real-time (reports, big-data exploration).")
print("\nGetting this right is a core Desktop Specialist skill: a live dashboard on a slow")
print("warehouse is a SLOW dashboard (every filter re-queries the source); an extract")
print("makes it snappy but you must schedule refreshes. Match the connection to whether")
print("the scenario needs REAL-TIME data or FAST interaction.")
EOF
```

**Expected result:** Live connections chosen for real-time-critical scenarios (trading, ops monitoring) and extracts for speed-critical ones (reports, big-data exploration, slow sources). The connection lesson is the freshness-versus-speed trade-off — live is always current but source-bound, extracts are fast via the Hyper engine but only as fresh as the last refresh.

**Negative test:** Using a live connection to a slow warehouse for an interactive dashboard. Every filter re-queries the slow source, making the dashboard sluggish; an extract into the Hyper engine makes interaction fast.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Why relationships avoid the join-duplication trap

**Objective:** See how naive joins duplicate data that relationships avoid.

```bash
python3 - <<'EOF'
# orders and a one-to-many "order_lines" — a naive join duplicates the order total
ORDERS = [{"order_id": 1, "order_total": 100}, {"order_id": 2, "order_total": 50}]
ORDER_LINES = [
  {"order_id": 1, "line": "A", "qty": 2},
  {"order_id": 1, "line": "B", "qty": 3},   # order 1 has 2 lines
  {"order_id": 2, "line": "C", "qty": 1},
]
print("NAIVE JOIN (flatten orders + order_lines into one table):")
joined = []
for line in ORDER_LINES:
    o = next(o for o in ORDERS if o["order_id"] == line["order_id"])
    joined.append({**line, "order_total": o["order_total"]})
for r in joined:
    print(f"   order {r['order_id']} line {r['line']}: order_total={r['order_total']}")
naive_sum = sum(r["order_total"] for r in joined)
print(f"   SUM(order_total) over the joined table = {naive_sum}")
true_total = sum(o["order_total"] for o in ORDERS)
print(f"   -> WRONG! True total is {true_total}, but the join DOUBLE-COUNTED order 1's")
print(f"      $100 (it appears on BOTH its lines). Inflated by {naive_sum - true_total}.\n")

print("RELATIONSHIPS (keep tables at native granularity, join per-viz):")
print("   orders stays 1 row per order; order_lines stays 1 row per line.")
print(f"   SUM(order_total) -> computed at the ORDER level = {true_total}  (correct)")
print(f"   SUM(qty)         -> computed at the LINE level = {sum(l['qty'] for l in ORDER_LINES)}  (correct)")
print("\nThe trap: a naive JOIN flattens one-to-many data, so the 'one' side's values")
print("(order_total) REPEAT on every 'many' row and get DOUBLE-COUNTED when aggregated.")
print("RELATIONSHIPS (Tableau's modern model) keep each table at its own granularity and")
print("let Tableau choose the correct join/aggregation PER VISUALIZATION — so order_total")
print("sums at the order level and qty at the line level, both correct. That's why")
print("relationships are the best-practice default: they avoid the duplication that")
print("silently inflates numbers in manual joins. Understanding this is a key cert concept.")
EOF
```

**Expected result:** A naive join double-counting an order total across its multiple line items (inflating the sum), while relationships keep each table at native granularity and aggregate each measure at the correct level. The relationships lesson is that flattening one-to-many data with a manual join duplicates the "one" side's values, silently inflating aggregates, which relationships avoid by joining contextually per visualization.

**Negative test:** Flattening one-to-many tables with a manual join and summing the parent-level measure. The parent value repeats on every child row and is double-counted; relationships keep granularity separate and aggregate each measure at its correct level.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Live versus extract understood as the freshness-versus-speed trade-off, with the Hyper engine behind extracts.
- [ ] The data model understood — joins, blends, and relationships — with relationships the modern default.
- [ ] The join-duplication trap understood, and why relationships avoid it by preserving granularity.
- [ ] Tableau Prep placed as the dedicated visual data-preparation tool for cleaning and reshaping.
