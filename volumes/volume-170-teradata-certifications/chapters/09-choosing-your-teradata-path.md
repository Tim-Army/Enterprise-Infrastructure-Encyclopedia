# Chapter 09: Choosing Your Teradata Path

## Learning Objectives

- Map roles (developer, DBA, data engineer, architect, data scientist) to certifications.
- Sequence certifications — start with the VantageCloud Lake Associate.
- Understand the current-versus-legacy exam landscape when planning.
- Place Teradata in the data-platform ecosystem.

*Cert relevance: this chapter turns the program map ([Ch 1](01-the-teradata-program.md)) into a personal plan and ends with a capstone.*

## Match the credential to your role

Teradata certifications map to what you do:

| Your role | Start here | Then consider |
| --- | --- | --- |
| **Anyone new to Teradata** | Associate VantageCloud Lake ([Ch 1](01-the-teradata-program.md)) | a role-based path |
| **SQL developer / analyst** | Associate ([Ch 5](05-sql-and-querying.md)) | Data Engineering (legacy) / VantageCloud dev |
| **Data engineer** | Associate → Data Engineering ([Ch 4](04-data-distribution-and-primary-index.md), [Ch 6](06-physical-database-design.md)) | design + performance depth |
| **Database administrator** | Associate → Administration ([Ch 7](07-workload-management-and-administration.md)) | workload management depth |
| **Architect** | Associate + design/architecture ([Ch 3](03-the-mpp-architecture.md)) | platform architecture |
| **Data scientist** | Associate → analytics/ML ([Ch 8](08-clearscape-and-modern-platform.md)) | ClearScape/in-database ML |

The pattern: **everyone starts with the Associate** (foundational platform, architecture, SQL), then branches to the **role-based** depth their job needs. The lab builds a role-to-path planner.

## Sequence sensibly

A workable sequence for most people:

1. **Start with the Associate VantageCloud Lake.** It has **no prerequisites**, is a single accessible exam, and validates the **foundation** — the platform, MPP architecture, primary-index distribution, and SQL — that every other role builds on. This is the anchor of the current program.
2. **Add role-based depth** as your job requires — data engineering (design/performance), administration (workload/space/security), architecture, or analytics/ML.
3. **Mind the current-vs-legacy landscape** — target **VantageCloud Lake** certifications (the current direction); several legacy Vantage 2 role-based exams **retired in 2024**, so verify what is currently offered before planning ([Ch 1](01-the-teradata-program.md)).
4. **Stay current** — Teradata credentials **do not expire**, but the platform (especially the cloud/Lake direction) evolves, so keep learning even though the badge remains valid.

Because the Associate is the accessible, no-prerequisite entry and the platform is moving to VantageCloud, the natural path is **Associate VantageCloud Lake first, then specialize**. The lab sequences a plan.

## Current versus legacy when planning

A practical planning point unique to Teradata right now is the **transition** ([Ch 1](01-the-teradata-program.md)): the program is **actively moving** from the Vantage 2 track (with several role-based exams retired in mid-2024) to the **VantageCloud** direction. So when you plan:

- **Prefer VantageCloud Lake** certifications — they reflect the current platform and are where investment is going.
- **Check availability** — do not plan around a retired exam; confirm on the certification site.
- **Skills transfer** — the **fundamentals** (MPP, primary index, SQL, design) are stable across versions, so learning them is durable even as specific exams change.

Being aware of this landscape avoids studying for an exam that no longer exists and points you at the current, supported path. The lab reflects the transition. This currency-awareness is itself part of certifying wisely.

## Teradata in the ecosystem

Teradata competes in the enterprise data-warehouse and cloud-analytics space:

- **Cloud data-platform peers** — [Snowflake (XLIX)](../../volume-049-snowflake-certifications/README.md), [Databricks (XLVIII)](../../volume-048-databricks-certifications/README.md), and [Cloudera (CLVIII)](../../volume-158-cloudera-certifications/README.md): modern cloud data/analytics; Teradata's edge is **decades of MPP data-warehouse depth**, reliability at extreme scale, and now a cloud-native/open Lake.
- **Analytics peers** — [SAS (CLXVIII)](../../volume-168-sas-certifications/README.md): analytics and in-database ML.
- **Data integration** — [Informatica (CLXV)](../../volume-165-informatica-certifications/README.md): feeding the warehouse.

Learning Teradata is learning **enterprise-scale analytics on a shared-nothing MPP engine** — how to distribute data (the primary index), query it in parallel, design for the engine, operate it, and run modern analytics and AI on it. The capstone builds across it. The lab closes with it.

## Hands-On Lab

Python builds a role-to-path planner, then a capstone across the Teradata lifecycle. **Cost:** none.

### Lab 9.1 — Plan your Teradata path

**Objective:** Turn a role into a sequenced certification plan.

```bash
python3 - <<'EOF'
ROLE_PATHS = {
  "SQL developer/analyst": ["Associate VantageCloud Lake", "developer/data-engineering depth"],
  "Data engineer":         ["Associate VantageCloud Lake", "Data Engineering (design + performance)"],
  "Database administrator":["Associate VantageCloud Lake", "Administration (workload/space/security)"],
  "Data scientist":        ["Associate VantageCloud Lake", "ClearScape / in-database ML"],
}
def plan(role):
    steps = ROLE_PATHS[role]
    print(f"   ROLE: {role}")
    print(f"      1. START (foundation, no prereqs): {steps[0]}")
    for i, s in enumerate(steps[1:], 2):
        print(f"      {i}. THEN (role-based depth): {s}")
    print("      note: prefer VantageCloud Lake (current); some Vantage 2 exams retired 2024; certs don't expire")
print("TERADATA ROLE -> CERTIFICATION PATH:\n")
for role in ["SQL developer/analyst", "Data engineer", "Database administrator"]:
    plan(role); print()
print("EVERYONE starts with the Associate VantageCloud Lake (foundation: platform + MPP + PI + SQL),")
print("then branches to role-based depth. Prefer VantageCloud Lake (current direction); mind retired legacy exams.")
EOF
```

**Expected result:** A planner turning roles into sequenced paths — every role starts with the Associate VantageCloud Lake, then branches (data engineer → Data Engineering, DBA → Administration, data scientist → ClearScape/ML). The lesson is to start with the no-prerequisite Associate VantageCloud Lake foundation, then add role-based depth, preferring current VantageCloud Lake certifications over retired legacy exams.

**Cleanup:** None.

### Lab 9.2 — Capstone: the Teradata analytics lifecycle

**Objective:** Distribute data, query in parallel, design, administer, and run analytics — end to end.

```bash
python3 - <<'EOF'
# CAPSTONE: raw data -> the Teradata MPP lifecycle -> insight
N_AMPS = 4
rows = [{"order_id": i, "region": "E" if i%2 else "W", "amount": (i%5)*50, "month": (i%3)+1} for i in range(1, 401)]
log = []
# 1) DISTRIBUTE by Primary Index (order_id, high cardinality -> even)
amps = {i: [] for i in range(N_AMPS)}
for r in rows: amps[hash(r["order_id"]) % N_AMPS].append(r)
skew = max(len(v) for v in amps.values()) / (sum(len(v) for v in amps.values())/N_AMPS)
log.append(f"DISTRIBUTE: PI=order_id -> per-AMP={[len(v) for v in amps.values()]} (skew {skew:.2f}, even) -> balanced parallelism")
# 2) DESIGN: PPI by month -> partition elimination
log.append("DESIGN: PPI by month -> a month query scans 1 of 3 partitions (~3x less I/O)")
# 3) QUERY in parallel (aggregate) + optimizer with stats
agg = {}
for r in rows: agg[r["region"]] = agg.get(r["region"],0)+r["amount"]
log.append(f"QUERY (parallel GROUP BY region, optimizer + stats): {agg}")
# 4) ADMINISTER: workload priority + spool ok
log.append("ADMINISTER: tactical workload high-priority; query within spool limit -> OK")
# 5) ANALYZE: ClearScape in-database scoring (no data movement)
high_value = sum(1 for r in rows if r["amount"] >= 150)
log.append(f"ANALYZE (ClearScape in-database): scored {high_value} high-value orders where the data lives")

print("CAPSTONE — the Teradata analytics lifecycle end to end:\n")
for step in log: print(f"   {step}")
print()
print("Raw data is DISTRIBUTED evenly by the Primary Index (balanced AMPs), the table is DESIGNED")
print("with PPI (partition pruning), QUERIED in PARALLEL (optimizer + stats), ADMINISTERED (workload")
print("priority + spool), and ANALYZED IN-DATABASE (ClearScape, no data movement). Distribute -> design")
print("-> query -> operate -> analyze on a shared-nothing MPP engine IS Teradata — and what these certs prepare you for.")
EOF
```

**Expected result:** A capstone distributing data evenly by primary index, designing with PPI, querying in parallel with the optimizer, administering workload and space, and running in-database analytics. The lesson synthesizes the volume: Teradata is enterprise analytics on a shared-nothing MPP engine — distribute (primary index), design (indexes/PPI), query (parallel SQL + optimizer), operate (workload/space), and analyze (ClearScape in-database) — which the Associate-then-specialize certification path prepares you to do.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Roles mapped to certifications — developer, data engineer, DBA, architect, data scientist.
- [ ] A sensible sequence chosen — Associate VantageCloud Lake first, then role-based depth.
- [ ] The current-vs-legacy landscape understood — prefer VantageCloud Lake; verify retired legacy exams.
- [ ] Teradata placed in the ecosystem — enterprise MPP analytics, now cloud-native and open.

## See also

- [Chapter 01 — The Teradata Certification Program](01-the-teradata-program.md) — the tracks and mechanics this plan draws on.
- [Volume XLIX — Snowflake](../../volume-049-snowflake-certifications/README.md), [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md), and [Volume CLVIII — Cloudera](../../volume-158-cloudera-certifications/README.md) — cloud data-platform peers.
