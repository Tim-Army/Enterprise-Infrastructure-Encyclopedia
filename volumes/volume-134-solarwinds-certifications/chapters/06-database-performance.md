# Chapter 06: Database Performance

## Learning Objectives

- Apply wait-time analysis to find what a database is actually waiting on.
- Rank queries by total impact rather than by single-execution duration.
- Distinguish a blocking chain from genuine resource contention.
- Explain what Database Performance Analyzer and Database Management each cover.

## Two database exams

SolarWinds certifies two adjacent but distinct areas:

| Exam | Question it answers |
|:---|:---|
| **Database Performance Analyzer (DPA)** | *Why is the database slow?* — wait-time analysis, query tuning |
| **Database Management** | *Is the database healthy and well-administered?* — administration, health, capacity |

DPA's distinctive contribution, and the reason it is worth a chapter, is **wait-time analysis**.

## Wait-time analysis

Traditional database monitoring reports resource utilization: CPU, memory, disk I/O, cache hit ratios. The trouble is that these describe the **server**, not the **user's experience**, and they routinely look fine while queries crawl.

Wait-time analysis inverts the question. Instead of asking "how busy is the server?", it asks: **when a query takes 8 seconds, where do those 8 seconds go?** Every session is sampled and its time attributed to what it was waiting on:

| Wait category | Meaning | Typical remedy |
|:---|:---|:---|
| **CPU** | Actually executing | Tune the query; reduce work |
| **I/O (disk read/write)** | Waiting for storage | Indexing, faster storage, more memory for cache |
| **Lock/blocking** | Waiting for another session's lock | Fix the blocker; shorten transactions |
| **Latch/buffer** | Internal memory-structure contention | Reduce hot-spotting; configuration |
| **Network** | Waiting on the client or the wire | Fetch size, chattiness, distance |
| **Commit/log** | Waiting for the log write | Faster log storage; batch commits |

The power of this framing is that it points directly at the remedy. "CPU is at 60%" tells you nothing actionable. "72% of this query's time is lock waits caused by session 412" tells you exactly what to fix.

## Ranking by total impact

The slowest single query is rarely the biggest problem. A query taking 5 seconds and running twice a day costs 10 seconds; a query taking 200 milliseconds and running 500,000 times a day costs over 27 hours. **Rank by total time, not per-execution time** — the frequent, moderately slow query is almost always the one worth tuning first.

## Blocking versus contention

Both present as "the database is slow," and they need different responses:

- **Blocking** — one session holds a lock others need, forming a chain. Fix the **head of the chain**: kill it, tune it, or shorten its transaction. Killing a mid-chain session accomplishes nothing.
- **Resource contention** — many sessions competing for the same I/O or memory. No single culprit; the answer is capacity or reducing total demand.

## Hands-On Lab

Python models database performance analysis. **Cost:** none.

### Lab 6.1 — Wait-time analysis

**Objective:** Attribute query time to wait categories and read the remedy.

```bash
python3 - <<'EOF'
query_time = {                     # seconds attributed per wait category
  "CPU":            0.9,
  "I/O read":       1.2,
  "lock/blocking":  5.4,
  "commit/log":     0.3,
  "network":        0.2,
}
total = sum(query_time.values())
print(f"Query total elapsed: {total:.1f}s\n")
for cat, secs in sorted(query_time.items(), key=lambda kv: -kv[1]):
    pct = secs/total*100
    bar = "#" * int(pct/3)
    print(f"{cat:15} {secs:5.1f}s {pct:5.1f}% {bar}")

top = max(query_time, key=query_time.get)
REMEDY = {
 "CPU":"tune the query — it is doing real work; reduce rows examined",
 "I/O read":"add/repair indexes, increase cache memory, or move to faster storage",
 "lock/blocking":"find the BLOCKING session and fix it — indexing/transaction length, not hardware",
 "commit/log":"faster log storage or batched commits",
 "network":"reduce round trips and fetch sizes",
}
print(f"\nDominant wait: {top} ({query_time[top]/total*100:.0f}%)")
print(f"Remedy: {REMEDY[top]}")
print("\nNote the server could show 60% CPU and 'healthy' storage the whole time —")
print("utilization metrics would never have found this.")
EOF
```

**Expected result:** Lock/blocking dominates at 68% of the query's 8 seconds, so the remedy is to fix the blocking session — **not** to buy faster disks, which the I/O figure might have tempted you into. The closing lines make the argument for wait-time analysis: a utilization dashboard would have shown a comfortable server throughout.

**Negative test:** Responding to "the database is slow" by adding CPU or storage — with 68% of the time in lock waits, faster hardware makes the blocked sessions wait at exactly the same speed.

**Cleanup:** None.

### Lab 6.2 — Rank queries by total impact

**Objective:** Find the query actually worth tuning.

```bash
python3 - <<'EOF'
queries = [
  {"id":"Q1","sql":"nightly report aggregate","avg_sec":5.0,   "execs_per_day":2},
  {"id":"Q2","sql":"session lookup by token",  "avg_sec":0.2,   "execs_per_day":500_000},
  {"id":"Q3","sql":"order detail fetch",       "avg_sec":0.8,   "execs_per_day":20_000},
  {"id":"Q4","sql":"admin audit export",       "avg_sec":45.0,  "execs_per_day":1},
]
for q in queries:
    q["total_hours"] = q["avg_sec"] * q["execs_per_day"] / 3600

print(f"{'id':4}{'avg':>8}{'execs/day':>12}{'TOTAL/day':>14}   query")
for q in sorted(queries, key=lambda x: -x["total_hours"]):
    print(f"{q['id']:4}{q['avg_sec']:>7.1f}s{q['execs_per_day']:>12,}{q['total_hours']:>12.1f}h   {q['sql']}")
print("\nQ4 is the SLOWEST single execution (45s) but costs 45 seconds per day in total.")
print("Q2 looks fast at 0.2s and costs 27.8 HOURS per day — tune Q2 first.")
print("Shaving Q2 to 0.1s saves ~14 h/day of database time; perfecting Q4 saves 45 s.")
EOF
```

**Expected result:** Q4 is the slowest per execution at 45 seconds, and Q2 — a "fast" 0.2-second query — consumes **27.8 hours of database time per day** through sheer frequency. The final line quantifies the choice: halving Q2 saves roughly 14 hours a day; perfecting Q4 saves 45 seconds. Sorting by average duration would have sent you to the wrong query.

**Negative test:** Tuning the query at the top of a "slowest queries" report — that report ranks by per-execution time, which systematically hides the high-frequency queries that dominate total load.

**Cleanup:** None.

### Lab 6.3 — Blocking chains versus resource contention

**Objective:** Diagnose which one you have, and act at the right place.

```bash
python3 - <<'EOF'
sessions = [
  {"id":412,"state":"running","blocked_by":None,"waiting_on":"CPU",  "held_locks":["orders"]},
  {"id":455,"state":"blocked","blocked_by":412, "waiting_on":"lock", "held_locks":["order_lines"]},
  {"id":460,"state":"blocked","blocked_by":455, "waiting_on":"lock", "held_locks":[]},
  {"id":471,"state":"blocked","blocked_by":455, "waiting_on":"lock", "held_locks":[]},
]
blocked = [s for s in sessions if s["state"] == "blocked"]
def head_of_chain(sess):
    cur = sess
    while cur["blocked_by"]:
        cur = next(s for s in sessions if s["id"] == cur["blocked_by"])
    return cur

heads = {head_of_chain(s)["id"] for s in blocked}
print(f"{len(blocked)} blocked session(s); head(s) of chain: {sorted(heads)}")
for s in sessions:
    role = "HEAD BLOCKER" if s["id"] in heads else ("blocked" if s["state"]=="blocked" else "running")
    print(f"  session {s['id']}: {role:12} waiting_on={s['waiting_on']:5} blocked_by={s['blocked_by']}")
print("\nAct on session 412 — the HEAD. Killing 455 frees 460/471 only until 455's work retries;")
print("killing 460 or 471 achieves nothing at all.")
print("\nContrast: if all four were waiting on 'I/O read' with no blocked_by, that is RESOURCE")
print("CONTENTION — no culprit session, so the answer is capacity or reduced demand.")
EOF
```

**Expected result:** Three blocked sessions resolve to a single head — session 412 — and the guidance is explicit that killing mid-chain sessions is useless. The contrast at the end is the diagnostic that matters: **blocked_by chains mean blocking (find the head); a crowd waiting on the same resource with no blocker means contention (add capacity or reduce demand).** Both look like "slow database" from the outside.

**Negative test:** Killing the session with the longest wait time — that is usually the session at the *end* of the chain, the biggest victim rather than the cause, and the blocking resumes immediately.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Wait-time analysis applied to attribute query time and select the remedy.
- [ ] Queries ranked by total daily impact rather than per-execution duration.
- [ ] Blocking chains traced to the head, and distinguished from resource contention.
- [ ] The DPA and Database Management exam scopes distinguished.
