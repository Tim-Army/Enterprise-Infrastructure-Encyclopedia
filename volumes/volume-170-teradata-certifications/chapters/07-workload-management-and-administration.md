# Chapter 07: Workload Management and Administration

## Learning Objectives

- Explain workload management and mixed-workload prioritization.
- Describe the DBA's tasks — users, space, sessions, and security.
- Understand monitoring and resource governance.
- Recognize the administration role in the certification program.

*Cert relevance: this is the administration track — DBA and workload-management competency.*

## Workload management

A production Teradata warehouse runs a **mix of workloads** at once: quick tactical lookups, long analytical queries, batch loads, and dashboards — all competing for the **parallel resources** (AMPs, CPU, I/O). **Workload management** ensures they **coexist fairly and predictably** rather than a runaway report starving everyone else. Teradata's workload management (historically **TASM — Teradata Active System Management**, and its VantageCloud equivalents) lets you:

- **Classify** requests into **workloads** by who/what they are (user, application, query type).
- **Prioritize** — give business-critical or tactical queries **more resources** than low-priority batch work.
- **Set rules** — throttles (limit concurrent heavy queries), filters (block a bad query), and exceptions (abort a query that runs too long).

The goal is **service-level management**: important work gets the resources it needs, and no single query monopolizes the shared parallel engine. This is essential on a busy multi-tenant warehouse and a distinct administration skill. The lab prioritizes a mixed workload.

## The DBA's tasks

A Teradata **DBA (database administrator)** keeps the platform healthy and secure:

- **Users and roles** — create users, grant privileges via **roles**, and manage authentication — controlling who can access what (least privilege).
- **Space management** — Teradata allocates **space** (perm, spool, temp) to databases/users; the DBA monitors and manages it so no user runs out of **spool** (working space) and no database fills its **perm** space (a common cause of failures).
- **Sessions** — monitor active **sessions**, identify and manage problem queries, and control concurrency.
- **Security** — access controls, row/column-level security where needed, encryption, and auditing for governance and compliance.

Space (especially **spool**) and user/role management are frequent, practical DBA concerns — "the query failed: no more spool" is a classic. These operational tasks are exactly what the administration certification validates. The lab manages users and space.

## Monitoring and governance

Running the warehouse well requires **visibility and control**:

- **Monitoring** — track system health, resource usage, query performance, and workload behavior (via Teradata Viewpoint / VantageCloud monitoring). Spot the query consuming all the CPU, the skewed table, the filling space.
- **Resource governance** — enforce the workload-management rules continuously, adjusting priorities and throttles as demand changes.
- **Capacity and cost** — on **VantageCloud** especially, monitor consumption and cost (compute is elastic and metered), rightsizing to balance performance and spend.

Governance turns raw capacity into **reliable service**: the warehouse stays responsive under load, costs stay controlled, and problems are caught early. On the cloud (VantageCloud), **cost governance** joins performance as a first-class concern. The lab monitors and governs resources. *(Resource governance and cost management echo the FinOps/observability themes across the encyclopedia's cloud volumes.)*

## Administration in the certification program

Administration is a **distinct track** in the Teradata program (the legacy Vantage 2 **Administration** exam, with VantageCloud administration content in the current direction). It validates the **operational** competency — workload management, space, users, security, monitoring — that keeps a warehouse running, as opposed to the **development/design** competency of building and querying it. Some professionals specialize as DBAs; others (developers, architects) need enough administration knowledge to design and operate responsibly. Understanding that the program certifies **both building and running** the warehouse helps you choose a path ([Ch 9](09-choosing-your-teradata-path.md)). The lab reflects the operational focus.

## Hands-On Lab

Python models workload prioritization, space management, and resource governance. **Cost:** none.

### Lab 7.1 — Manage workloads, users, and space

**Objective:** Prioritize a mixed workload, manage spool space, and govern a runaway query.

```bash
python3 - <<'EOF'
# WORKLOAD MANAGEMENT: classify + prioritize a mixed workload sharing the parallel engine
WORKLOADS = {"tactical":{"priority":"high","share":50},"dashboard":{"priority":"medium","share":30},"batch":{"priority":"low","share":20}}
print("WORKLOAD MANAGEMENT (TASM) — allocate the shared parallel engine by priority:")
for w, d in WORKLOADS.items(): print(f"   {w:10} priority={d['priority']:6} resource share={d['share']}%")

# SPACE management: users have spool (working) space; a query needing more than allowed fails
def run_query(user_spool_gb, query_needs_gb):
    return "OK" if query_needs_gb <= user_spool_gb else f"FAIL: 'No more spool space' (needs {query_needs_gb}GB > {user_spool_gb}GB limit)"
print("\nSPACE MANAGEMENT (spool):")
print(f"   query needing 50GB, user spool 100GB: {run_query(100, 50)}")
print(f"   runaway query needing 500GB, user spool 100GB: {run_query(100, 500)}")

# GOVERNANCE: a rule aborts a query that exceeds a runtime threshold (protect the system)
def governor(runtime_s, limit_s=3600):
    return f"ABORT (ran {runtime_s}s > {limit_s}s limit) — protect the shared system" if runtime_s > limit_s else "allow"
print("\nRESOURCE GOVERNANCE (exception rule):")
print(f"   query running 5000s: {governor(5000)}")
print()
print("WORKLOAD MANAGEMENT classifies + prioritizes a MIXED workload so tactical queries get more")
print("of the shared parallel engine than low-priority batch. The DBA manages SPACE (a query over its")
print("SPOOL limit fails with 'no more spool') and USERS/roles, and GOVERNANCE rules abort runaway")
print("queries to protect the system. Operating the warehouse (vs building it) is the Administration cert.")
EOF
```

**Expected result:** A mixed workload prioritized (tactical high, batch low), spool-space management where a query within the limit succeeds and a runaway one fails with "no more spool," and a governance rule aborting a query over the runtime limit. The lesson is Teradata administration: workload management prioritizes mixed workloads on the shared parallel engine, the DBA manages users/roles and space (especially spool), and resource governance protects the system from runaway queries — the operational competency of the administration track.

**Negative test:** Running all workloads at equal priority with no space limits or governance. A single batch query or runaway report consumes the engine and exhausts spool, and everyone's queries fail; workload prioritization, space management, and governance rules are what keep a busy warehouse reliable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Workload management understood — classifying and prioritizing mixed workloads on the shared parallel engine (TASM).
- [ ] The DBA's tasks understood — users/roles, space (perm/spool), sessions, and security.
- [ ] Monitoring and governance understood — visibility, resource rules, and (on cloud) cost governance.
- [ ] The administration track placed — operating the warehouse, distinct from building/querying it.

## See also

- [Chapter 06 — Physical Database Design](06-physical-database-design.md) — the design that administration operates.
- [Chapter 02 — Teradata Vantage and VantageCloud](02-vantage-and-vantagecloud.md) — cloud consumption and cost governance.
- [Chapter 09 — Choosing Your Teradata Path](09-choosing-your-teradata-path.md) — the DBA path among the roles.
