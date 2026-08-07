# Chapter 06: Physical Database Design

## Learning Objectives

- Design tables and choose column types for a Teradata warehouse.
- Use secondary indexes and join indexes to accelerate access.
- Apply partitioning (PPI) to prune data scanned.
- Understand how physical design serves the parallel engine.

*Cert relevance: physical database design is core to the developer/design and Associate exams.*

## Tables and columns

Physical design starts with **tables** — defining columns, data types, and the **primary index** ([Ch 4](04-data-distribution-and-primary-index.md)) that distributes the rows. Good choices matter:

- **Data types** — pick the **smallest correct** type (INTEGER vs BIGINT, DATE vs TIMESTAMP, appropriate CHAR/VARCHAR lengths). Smaller rows mean **less I/O** and more rows per block — real performance at warehouse scale.
- **Primary index** — the distribution decision, chosen for even distribution and common access/joins.
- **Constraints** — primary/foreign keys and checks that document and enforce data integrity.

At the scale Teradata operates, **small design decisions multiply** across billions of rows — an oversized column or a poor primary index has outsized cost. Careful table design is foundational. The lab defines a table with sensible types.

## Secondary and join indexes

Beyond the primary index, Teradata offers indexes to **accelerate specific access patterns**:

- **Secondary Index (SI)** — an index on a **non-primary-index column** to speed queries that filter on it (a **Unique SI** for fast unique lookups, a **Non-Unique SI** for selective filters). Unlike the primary index, a secondary index does **not** change distribution — it is a true side lookup structure, at the cost of extra storage and maintenance.
- **Join Index (JI)** — a **pre-computed, stored** result (like a materialized view) — for example a **frequently-run join or aggregation** stored so the optimizer can use it directly instead of recomputing. Powerful for repeated heavy queries, at the cost of storage and update overhead.

The trade-off is always **query speed versus storage and maintenance**: each index helps some queries but costs space and slows writes. Choosing the **right** indexes for the **actual** query patterns — not indexing everything — is the design skill. The lab adds a secondary index and a join index.

## Partitioning (PPI)

**Partitioned Primary Index (PPI)** adds a **second level of organization** on top of distribution: within each AMP, rows are **partitioned** (typically by a **date range** — e.g. by month). The payoff is **partition elimination**: a query filtered to a date range **scans only the relevant partitions**, skipping the rest.

- Without partitioning, a query for "last month" scans the **whole** table (all AMPs, all rows).
- With PPI by month, the same query scans **only last month's partition** on each AMP — a huge I/O reduction on large time-series tables.

Partitioning is one of the most effective performance tools for the **date-ranged** queries common in data warehousing (most analytics filter by time). Combining a good primary index (distribution) with PPI (partition elimination) is a hallmark of good design. The lab shows partition elimination.

## Design serves the parallel engine

The through-line of physical design is that **every choice serves the parallel engine**:

- **Primary index** → even distribution across AMPs (parallel balance).
- **Column types** → smaller rows → less I/O per parallel scan.
- **Secondary/join indexes** → faster targeted access without disturbing distribution.
- **Partitioning** → less data scanned by pruning partitions.

Good Teradata design is not generic database design — it is design **for MPP**: distribute evenly, minimize I/O, prune what you can, and let the AMPs run balanced and fast. This MPP-aware design thinking is exactly what the design-oriented certifications test. The lab ties the choices to the engine. *(Partition pruning and columnar/type efficiency are performance principles shared across analytics engines.)*

## Hands-On Lab

Python models table design, secondary/join indexes, and PPI partition elimination. **Cost:** none.

### Lab 6.1 — Design for performance

**Objective:** Choose types, add indexes, and use PPI for partition elimination.

```bash
python3 - <<'EOF'
# table design: smaller correct types = less I/O at scale
COLUMNS = {"order_id":"INTEGER","order_date":"DATE","amount":"DECIMAL(10,2)","region":"CHAR(2)"}
print("TABLE DESIGN (smallest correct types -> less I/O across billions of rows):")
for c, t in COLUMNS.items(): print(f"   {c:12} {t}")

# indexes accelerate specific access (trade speed vs storage/maintenance)
INDEXES = {
  "Primary Index (order_id)": "distribution + single-AMP access + join co-location",
  "Secondary Index (region)": "speeds WHERE region=... (side lookup; does NOT change distribution)",
  "Join Index (region,SUM(amount))": "pre-computed aggregate -> optimizer uses it directly (materialized)",
}
print("\nINDEXES (right ones for actual query patterns):")
for idx, benefit in INDEXES.items(): print(f"   {idx:34} {benefit}")

# PPI: partition by month -> partition elimination for date-ranged queries
rows = [{"order_id": i, "month": (i % 12) + 1} for i in range(1200)]   # 100 rows/month
def scan(rows, want_month=None):
    scanned = [r for r in rows if (want_month is None or r["month"]==want_month)]
    return len(scanned)
print("\nPARTITIONING (PPI by month) — partition elimination:")
print(f"   no PPI, query month=8: scans ALL {scan(rows)} rows (full table)")
print(f"   PPI by month, query month=8: scans ONLY {scan(rows, 8)} rows (1 partition) -> {scan(rows)//scan(rows,8)}x less I/O")
print()
print("PHYSICAL DESIGN serves the parallel engine: SMALL correct TYPES cut I/O; the PRIMARY INDEX")
print("distributes; SECONDARY/JOIN indexes speed targeted access (vs storage/maintenance cost); and")
print("PPI PARTITIONING prunes — a month query scans one partition, not the whole table (12x less I/O).")
print("Design FOR MPP: distribute evenly, minimize I/O, prune. That's the Teradata design competency.")
EOF
```

**Expected result:** A table with small correct column types, a set of indexes (primary/secondary/join) each accelerating a pattern at a storage cost, and PPI partitioning by month giving partition elimination (scanning one partition instead of the whole table). The lesson is Teradata physical design for MPP: choose small correct types to cut I/O, add the right indexes for actual query patterns, and partition (PPI) to prune data scanned — every choice serving the parallel engine.

**Negative test:** Using oversized types, indexing every column, and never partitioning a huge time-series table. Rows are bloated, writes are slow from too many indexes, and every date query scans the whole table; type discipline, targeted indexes, and PPI partitioning are what make the design perform.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Table design understood — small correct column types and the distributing primary index at scale.
- [ ] Secondary and join indexes understood — targeted access acceleration, traded against storage/maintenance.
- [ ] Partitioning (PPI) understood — partition elimination that prunes data scanned for date-ranged queries.
- [ ] Design-for-MPP understood — every choice serves even distribution, low I/O, and pruning for the parallel engine.

## See also

- [Chapter 04 — Data Distribution and the Primary Index](04-data-distribution-and-primary-index.md) — the primary index at the center of design.
- [Chapter 05 — SQL and Querying at Scale](05-sql-and-querying.md) — how design and statistics drive the optimizer.
- [Chapter 07 — Workload Management and Administration](07-workload-management-and-administration.md) — operating the designed warehouse.
