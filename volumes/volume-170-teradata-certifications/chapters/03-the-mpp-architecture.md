# Chapter 03: The MPP Architecture

## Learning Objectives

- Explain massively parallel processing (MPP) and the shared-nothing design.
- Describe the components — Parsing Engine, AMPs, and the BYNET.
- Understand how parallelism delivers scalable analytics.
- Recognize why architecture is foundational to Teradata certification.

*Cert relevance: MPP architecture is core to the Associate exam and all Teradata knowledge.*

## Massively parallel processing

Teradata's defining characteristic is **MPP — massively parallel processing** — the architecture that lets it run analytics on **enormous data** fast. The idea: instead of one big computer processing all the data serially, **divide the data across many independent processing units** that each work on **their slice in parallel**, then combine the results. A query that would take hours on one machine finishes in minutes when dozens or hundreds of units attack it simultaneously.

This is a **shared-nothing** architecture: each processing unit has **its own** slice of data, memory, and CPU, and does **not** share them with others. Shared-nothing scales **linearly** — add more units and you get proportionally more capacity and throughput, with no shared bottleneck. This architecture is **why Teradata scales** to the largest data warehouses, and understanding it is foundational to every Teradata certification. The lab models parallel processing across units.

## The components

Teradata's MPP is built from a few key components:

- **Parsing Engine (PE)** — the "front end" that receives a SQL request, **parses** it, **checks** security and syntax, and — crucially — **optimizes** it into an efficient execution plan, then dispatches the work to the AMPs. The PE is the brain that decides **how** to run the query.
- **AMPs (Access Module Processors)** — the parallel **workers**. Each AMP **owns a portion of the data** (its rows) and does the actual work — reading, filtering, joining, aggregating **its slice** — independently and in parallel with the others. More AMPs = more parallelism.
- **BYNET** — the **interconnect** (message-passing layer) that lets the PE and AMPs **communicate** and coordinate — distributing work and merging results across the AMPs.

So a query flows: **PE parses and optimizes → dispatches to AMPs over BYNET → each AMP works its data in parallel → results merge back**. Knowing these components and their roles is bedrock Teradata knowledge. The lab models the PE/AMP/BYNET flow.

## Parallelism in action

The **payoff** of the architecture is parallel query execution. When a query runs:

- Every AMP that holds relevant data works on it **simultaneously** — so scanning a billion-row table means each of, say, 100 AMPs scans ~10 million rows **at the same time**, not one machine scanning a billion serially.
- Operations like **filtering, aggregation, and joins** are executed **in parallel across AMPs**, with the BYNET redistributing data between AMPs when needed (e.g. to join on a non-distribution key).
- The result is **scalable performance**: throughput grows with the number of AMPs.

The administrator's and designer's job is to **keep the AMPs evenly busy** — even data distribution ([Ch 4](04-data-distribution-and-primary-index.md)) so no AMP does more than its share. Parallelism only pays off when the work is **balanced**. The lab shows parallel speedup and the cost of imbalance.

## Architecture as the foundation

Every other Teradata topic — data distribution ([Ch 4](04-data-distribution-and-primary-index.md)), SQL and the optimizer ([Ch 5](05-sql-and-querying.md)), physical design ([Ch 6](06-physical-database-design.md)), workload management ([Ch 7](07-workload-management-and-administration.md)) — is **shaped by the MPP architecture**. You choose a primary index to distribute rows **across AMPs**; you design tables and indexes to let the **parallel engine** run efficiently; you manage workloads to share the **parallel resources** fairly. This is why the Associate exam and all Teradata learning **start with architecture**: it is the lens through which everything else makes sense. The lab ties architecture to the rest. *(Shared-nothing MPP is the same scaling principle behind other distributed analytics engines like [Databricks XLVIII](../../volume-048-databricks-certifications/README.md).)*

## Hands-On Lab

Python models MPP parallelism — PE, AMPs, BYNET, and the effect of balance. **Cost:** none.

### Lab 3.1 — Model parallel query across AMPs

**Objective:** Distribute rows across AMPs, run a query in parallel, and see the cost of imbalance.

```bash
python3 - <<'EOF'
# MPP: Parsing Engine optimizes; AMPs process their slice in parallel; BYNET coordinates
class Teradata:
    def __init__(self, n_amps):
        self.n_amps = n_amps
        self.amps = {i: [] for i in range(n_amps)}   # each AMP owns a slice of rows
    def distribute(self, rows, key_fn):              # rows -> AMPs by hashing a key
        for r in rows:
            amp = hash(key_fn(r)) % self.n_amps
            self.amps[amp].append(r)
    def parallel_scan(self):                          # each AMP scans its rows in parallel
        # "time" = max rows on any single AMP (they run simultaneously)
        per_amp = [len(v) for v in self.amps.values()]
        return {"total_rows": sum(per_amp), "per_amp": per_amp, "parallel_time": max(per_amp)}

rows = [{"id": i, "cust": i % 400} for i in range(4000)]   # 4000 rows

# EVEN distribution (good key -> balanced AMPs)
td = Teradata(n_amps=8); td.distribute(rows, lambda r: r["cust"])
res = td.parallel_scan()
print("MPP PARALLEL SCAN — 4000 rows across 8 AMPs (Parsing Engine -> AMPs via BYNET):")
print(f"   even distribution: per-AMP={res['per_amp']}  parallel_time={res['parallel_time']} (vs {res['total_rows']} serial)")
print(f"   speedup ~ {res['total_rows']/res['parallel_time']:.1f}x (all AMPs work simultaneously)")

# SKEWED distribution (bad key -> one AMP overloaded)
td2 = Teradata(n_amps=8); td2.distribute(rows, lambda r: 0 if r["id"] < 3000 else r["id"])  # 3000 land on AMP 0
res2 = td2.parallel_scan()
print(f"\n   SKEWED distribution: per-AMP={res2['per_amp']}  parallel_time={res2['parallel_time']}")
print(f"   speedup collapses to ~ {res2['total_rows']/res2['parallel_time']:.1f}x — one hot AMP bottlenecks everyone")
print()
print("MPP divides data across AMPs (shared-nothing); each AMP scans ITS slice in PARALLEL, so")
print("8 balanced AMPs finish ~8x faster than serial. But SKEW (one AMP with most rows) collapses")
print("the speedup — the query waits for the slowest AMP. Even distribution keeps AMPs balanced;")
print("that's why the Primary Index (next chapter) matters. Architecture is the Teradata foundation.")
EOF
```

**Expected result:** 4000 rows distributed evenly across 8 AMPs giving a large parallel speedup, versus a skewed distribution where one overloaded AMP collapses the speedup. The lesson is MPP: the Parsing Engine optimizes and dispatches to AMPs over the BYNET, each AMP processes its slice in parallel for scalable speed, but the speedup depends on even data distribution — skew makes the query wait for the slowest AMP.

**Negative test:** Assuming performance scales just by adding AMPs regardless of distribution. A skewed table leaves most AMPs idle while one is overloaded, so more AMPs do not help; balanced distribution is what makes MPP parallelism deliver.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] MPP understood — dividing data across parallel, shared-nothing processing units for scalable analytics.
- [ ] The components understood — Parsing Engine (parse/optimize/dispatch), AMPs (parallel workers), BYNET (interconnect).
- [ ] Parallelism understood — AMPs process their slices simultaneously; throughput grows with AMPs.
- [ ] Architecture as foundation understood — data distribution, SQL, design, and workload all shaped by MPP.

## See also

- [Chapter 04 — Data Distribution and the Primary Index](04-data-distribution-and-primary-index.md) — how rows spread across AMPs.
- [Chapter 05 — SQL and Querying at Scale](05-sql-and-querying.md) — the Parsing Engine's optimizer.
- [Chapter 02 — Teradata Vantage and VantageCloud](02-vantage-and-vantagecloud.md) — the platform this engine powers.
