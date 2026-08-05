# Chapter 04: APM — Transactions, Apdex, and Databases

## Learning Objectives

- Read APM's core views: transactions, errors, distributed traces, databases.
- Compute and interpret Apdex, including what its threshold choice hides.
- Triage a slow service from summary to transaction trace to root cause.
- Rank database work by total impact rather than per-query slowness.

*Exam relevance: the whole APA syllabus — "APM fundamentals," "managing agent data," "visualizing insights," and "full stack observability practices with APM: troubleshooting performance… monitoring and management of applications and databases" — plus PEP Section 2 (Backend Application Performance: "APM setup, microservices, and database performance").*

## Transactions

A **transaction** is APM's unit of work: one request handled by one instrumented service, with duration, outcome, and attributes, recorded as a queryable event. Everything else in APM is a view over transactions — throughput, error rate, latency percentiles, and the breakdown of where time went (application code, database calls, external services).

The triage path the APA exam expects is a funnel:

1. **Summary** — is the service off its normal? Which signal moved: latency, throughput, errors?
2. **Transactions view** — *which* transaction moved? Sort by what matters (Chapter 3's lesson: total impact, not per-request slowness).
3. **Transaction trace** — one slow instance, segment by segment. Where did *this* request spend its time?
4. **Cross-cutting views** — distributed traces when the answer is another service; database view when it is a query; logs in context when it is neither.

## Apdex

**Apdex** scores user satisfaction from response times against a threshold **T**:

- **Satisfied**: response ≤ T
- **Tolerating**: T < response ≤ 4T
- **Frustrated**: response > 4T

`Apdex = (satisfied + tolerating/2) / total`, giving 0–1.

Apdex is on the APA syllabus and worth understanding precisely *because* it compresses so much. Two cautions that the lab makes concrete:

- **The score is only as meaningful as T.** T is a configuration choice per application. A generous T manufactures a good score; nobody chose it maliciously — it was the default, and the default does not know your users.
- **Compression hides shape.** An Apdex of 0.93 cannot distinguish "everyone slightly slow" from "most users fine, 7% having a terrible time." Percentiles split by outcome (the discipline from [Volume CXXXIX's Golden Signals chapter](../../volume-139-grafana-observability/chapters/07-dashboards-and-the-four-golden-signals.md)) remain necessary beside it.

## Databases from the application's side

APM's database view attributes query time to the transactions that spent it, which enables the ranking that matters operationally: **total time = calls × average time**. The slowest query in the estate is usually not the biggest problem; the biggest problem is usually a fast query called absurdly often. This is the same wait-time-times-frequency argument as [SolarWinds DPA](../../volume-134-solarwinds-certifications/README.md) makes from the database's side — meeting it from the application's side here is what PEP Section 2 means by "database performance."

## Hands-On Lab

Python models APM analysis. **Cost:** none.

### Lab 4.1 — Apdex: compute it, then distrust it properly

**Objective:** See what the score shows and what it compresses away.

```bash
python3 - <<'EOF'
import random
random.seed(4)
def apdex(durations, T):
    s = sum(1 for d in durations if d <= T)
    t = sum(1 for d in durations if T < d <= 4*T)
    return (s + t/2) / len(durations)

# Two very different services engineered to the same score
uniform_slow  = [random.uniform(0.40, 0.516) for _ in range(2000)]        # everyone mildly slow
bimodal       = [random.uniform(0.05, 0.3) for _ in range(1856)] + \
                [random.uniform(2.5, 6.0)  for _ in range(144)]           # 7% having a terrible time
T = 0.5
a1, a2 = apdex(uniform_slow, T), apdex(bimodal, T)
print(f"T = {T}s")
print(f"service A (everyone mildly slow) : Apdex {a1:.3f}")
print(f"service B (93% fast, 7% awful)   : Apdex {a2:.3f}")
print(f"-> nearly identical scores, completely different user experiences.")
p95a = sorted(uniform_slow)[int(len(uniform_slow)*.95)]
p95b = sorted(bimodal)[int(len(bimodal)*.95)]
print(f"   p95: A = {p95a:.2f}s   B = {p95b:.2f}s   ({p95b/p95a:.0f}x apart) <- the percentile separates them instantly\n")

# And the T lever
svc = bimodal
print(f"{'T (s)':>7}{'Apdex':>9}   reading")
for t_choice in (0.1, 0.5, 1.0, 2.0):
    a = apdex(svc, t_choice)
    note = "  <- same service, 'excellent', because T is generous" if t_choice == 2.0 else ""
    print(f"{t_choice:>7}{a:>9.3f}{note}")
print("\nTwo findings:")
print("  1. Apdex COMPRESSES: A and B tie despite B's 7% disaster. Keep percentiles")
print("     split by outcome next to any Apdex number.")
print("  2. T is a CHOICE: the same service scores 0.5 or 0.9 depending on T.")
print("     An unexamined default T is a score about nothing. Here T=2.0 rates a")
print("     service with a 7% disaster tail as 0.96 — near-perfect.")
EOF
```

**Expected result:** Services A and B land within a few thousandths of the same Apdex (0.926 vs 0.928) while their p95s sit 7x apart, and sweeping T moves the same service from 0.56 to 0.96. Neither finding says Apdex is useless — it says the score answers "how satisfied, given T" and must not be read as "what shape is the latency."

**Negative test:** Tuning until Apdex is green by raising T. The metric improves; the 7% keep suffering; the dashboard now actively hides them.

**Cleanup:** None.

### Lab 4.2 — Triage: summary → transaction → trace

**Objective:** Walk the APA troubleshooting funnel.

```bash
python3 - <<'EOF'
SUMMARY = {"latency_p95_ms": (310, 940), "throughput_rpm": (5200, 5150), "error_pct": (0.7, 0.8)}
print("STEP 1 — SUMMARY (before -> during):")
for k, (b, d) in SUMMARY.items():
    moved = "  <-- MOVED" if abs(d-b)/b > 0.3 else ""
    print(f"   {k:18} {b:>7} -> {d:<7}{moved}")
print("   latency moved; throughput and errors did not. This is a SLOWDOWN, not an outage.\n")

SAMPLED = [
  ("WebTransaction/checkout/place_order",  180, 2900),
  ("WebTransaction/browse/list",          3600,  140),
  ("WebTransaction/search/query",         1100,  135),
  ("WebTransaction/cart/update",           400,  150),
]
print("STEP 2 — TRANSACTIONS (rpm, p95 ms) — sort by TOTAL impact (rpm x p95):")
for name, rpm, p95 in sorted(SAMPLED, key=lambda t: -t[1]*t[2]):
    print(f"   {name:40} {rpm:>5} rpm  p95 {p95:>5} ms   impact {rpm*p95/1000:>7,.0f}")
print("   place_order is 20x slower than normal AND carries the impact. Zoom in.\n")

TRACE = [
  ("Java/app.controller.place_order",             28),
  ("Datastore/orders.find_by_customer",           45),
  ("External/inventory-svc/reserve",            2710),
  ("Datastore/orders.insert",                     60),
]
print("STEP 3 — TRANSACTION TRACE of one slow place_order (2,900 ms):")
for seg, ms in TRACE:
    bar = "#" * max(1, ms // 100)
    print(f"   {seg:42} {ms:>6} ms {bar}")
print("\nSTEP 4 — the time is in an EXTERNAL segment: inventory-svc.")
print("   -> pivot to the DISTRIBUTED trace; the fault is one service over.")
print("   The funnel ends by handing off correctly, not by staring harder at this app.")
EOF
```

**Expected result:** The summary isolates latency as the moved signal, the impact sort surfaces `place_order`, and the trace attributes 2.7 of 2.9 seconds to an external call — ending with a pivot, not a local fix. That ending is deliberate: the most common APM triage failure is tuning the service that *reported* the slowness instead of the one that caused it.

**Negative test:** Sorting transactions by p95 alone in step 2 — `browse/list` would never surface, and in a different incident the high-volume moderately-slow transaction is exactly the one that matters.

**Cleanup:** None.

### Lab 4.3 — Databases: total time, not slowest query

**Objective:** Rank database work the way the platform does.

```bash
python3 - <<'EOF'
QUERIES = [
  # query,                          calls/hr, avg_ms
  ("SELECT plan FROM subscriptions WHERE user_id=?",  920_000,   3.1),
  ("SELECT * FROM orders WHERE id=?",                 310_000,   2.2),
  ("UPDATE carts SET ... WHERE session=?",            140_000,   4.0),
  ("SELECT ... FROM reports r JOIN ... (analytics)",       40, 8200.0),
  ("INSERT INTO audit_log ...",                       610_000,   1.1),
]
rows = [(q, c, a, c*a/3_600_000) for q, c, a in QUERIES]   # seconds of DB time per second
print(f"{'query':52}{'calls/hr':>10}{'avg ms':>9}{'db-sec/sec':>12}")
for q, c, a, load in sorted(rows, key=lambda r: -r[3]):
    print(f"{q:52}{c:>10,}{a:>9.1f}{load:>12.2f}")
slowest = max(rows, key=lambda r: r[2]); heaviest = max(rows, key=lambda r: r[3])
print(f"\nSLOWEST query : {slowest[2]:>7.0f} ms avg — the analytics join, 40 calls/hr")
print(f"HEAVIEST query: {heaviest[3]:.2f} db-seconds per second — a {heaviest[2]} ms lookup")
ratio = heaviest[3] / max(r[3] for r in rows if r[2] > 1000)
print(f"\nThe 3 ms subscription lookup consumes ~{ratio:.0f}x the database time of the")
print("8-second analytics join, because it runs 920,000 times an hour. Cache it or")
print("batch it and the database exhales; tune the scary-looking join and almost")
print("nothing changes. Total time = calls x average — sort by THAT.")
print("\n(Meeting this from the DB side is Vol CXXXIV's wait-time analysis; APM")
print("gives you the same ranking from the application side, attributed to the")
print("transactions that spent the time.)")
EOF
```

**Expected result:** The 3.1 ms lookup tops the load ranking at 0.79 db-seconds per second — about 9x the analytics join's load — while the 8.2-second join sits at the bottom. The inversion is the entire lesson, and it recurs on both PEP and the DB-side volumes: per-query slowness is what catches the eye, total time is what loads the database.

**Negative test:** Spending the sprint on the analytics join because 8200 ms looks worst. It runs forty times an hour; the win is a rounding error.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Transactions understood as APM's unit, with the four-step triage funnel practiced.
- [ ] Apdex computed, and its two blind spots — T choice and compression — demonstrated.
- [ ] Slowdowns pivoted to distributed traces when the time is in an external segment.
- [ ] Database work ranked by calls × average, not by per-query slowness.
