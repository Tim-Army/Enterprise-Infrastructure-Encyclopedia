# Chapter 03: NRQL

## Learning Objectives

- Write NRQL queries: `SELECT` … `FROM` … `WHERE` … `FACET` … `SINCE` … `TIMESERIES`.
- Choose between event queries and metric queries for the same question.
- Control query cost with time windows, facet cardinality, and aggregation.
- Recognize NRQL as the platform's connective tissue — dashboards, alerts, and SLOs are all queries.

*Exam relevance: NRQL appears in the NVF topics twice ("write NRQL queries for different event types"), in PEP Section 1 (data visualization), and in REP Section 4 ("create queries for improved insights and monitoring"). It is the most cross-cutting skill in the program — the same position DQL holds in [Volume CXL](../../volume-140-dynatrace-certifications/chapters/03-grail-dql-and-dpl.md).*

## The shape of a query

NRQL reads like SQL aimed at telemetry:

```sql
SELECT percentile(duration, 95) FROM Transaction
WHERE appName = 'checkout-prod' AND error IS false
FACET request.uri
SINCE 1 hour ago COMPARE WITH 1 week ago
TIMESERIES
```

| Clause | Does | Notes |
|:---|:---|:---|
| `SELECT` | Aggregation or attribute selection | `count(*)`, `average()`, `percentile()`, `percentage()`, `latest()` |
| `FROM` | The event type | `Transaction`, `PageView`, `SystemSample`, `Log`, `Span`, `Metric` |
| `WHERE` | Filter | Attribute comparisons; do the narrowing here |
| `FACET` | Group by attribute | The cardinality lever — this is where cost hides |
| `SINCE` / `UNTIL` | Time window | The scan-size lever |
| `TIMESERIES` | Bucket over time | Turns a number into a chart |
| `COMPARE WITH` | Same query, offset window | Week-over-week in one clause |

Two clauses deserve most of your attention, because they are the cost model:

- **`SINCE` sets how much is scanned.** An event query over 90 days reads 90 days of per-occurrence records. The habit from DQL and LogQL transfers directly: narrow the window first.
- **`FACET` sets how many series come back.** `FACET request.uri` on a URL space with embedded IDs is the same cardinality explosion as Chapter 05 of [Volume CXL](../../volume-140-dynatrace-certifications/chapters/05-digital-experience-monitoring.md), arriving through a query instead of a naming rule.

## Events versus metrics for the same question

Most performance questions can be answered two ways, and the trade is the one this shelf keeps meeting:

| | Event query (`FROM Transaction`) | Metric query (`FROM Metric`) |
|:---|:---|:---|
| Precision | Exact — every record, every attribute | Pre-aggregated |
| Attribute filtering | Any attribute, decided at query time | Only dimensions kept at write time |
| Long windows | Expensive | Cheap |
| Retention | Shorter, costlier | Longer, cheaper |

The working rule: **explore on events, standardize on metrics.** The question you ask once a quarter with novel filters belongs on events; the panel every engineer loads daily belongs on a metric. This is Grail's schema-on-read trade and Prometheus's recording-rule trade wearing a third costume, and the exams in this program reward recognizing it.

## One language, every feature

The reason NRQL earns a full chapter is structural: **dashboards are NRQL, alert conditions are NRQL, service levels are NRQL.** Learn the language once and you have learned the configuration surface of Chapters 07 and 08. It also means a wrong query is not a cosmetic defect — the same mistaken `WHERE` clause that under-counts errors on a dashboard under-counts them in the alert built from it, in both cases silently.

## Hands-On Lab

Python models NRQL evaluation. **Cost:** none.

### Lab 3.1 — A minimal NRQL evaluator

**Objective:** Execute the clauses in the right order and see each one's effect.

```bash
python3 - <<'EOF'
import random
random.seed(3)
SAMPLED = []
for i in range(4000):
    uri = random.choice(["/checkout", "/browse", "/search", "/api/cart"])
    dur = random.lognormvariate(-1.5, 0.7) * (2.2 if uri == "/checkout" else 1.0)
    SAMPLED.append({"appName": "checkout-prod" if random.random() < .8 else "checkout-stg",
                 "request.uri": uri, "duration": round(dur, 3),
                 "error": random.random() < (0.03 if uri == "/checkout" else 0.006)})

def percentile(vals, p):
    s = sorted(vals); return s[min(len(s)-1, int(len(s)*p/100))]

print("SELECT percentile(duration, 95) FROM Transaction")
print("WHERE appName = 'checkout-prod' FACET request.uri\n")
stage = SAMPLED
print(f"FROM Transaction          -> {len(stage):,} events in window")
stage = [t for t in stage if t["appName"] == "checkout-prod"]
print(f"WHERE appName = ...       -> {len(stage):,} events")
facets = {}
for t in stage: facets.setdefault(t["request.uri"], []).append(t["duration"])
print(f"FACET request.uri         -> {len(facets)} groups\n")
print(f"{'facet':12}{'count':>8}{'p95 (s)':>10}")
for uri, durations_list in sorted(facets.items(), key=lambda kv: -percentile(kv[1], 95)):
    print(f"{uri:12}{len(durations_list):>8}{percentile(durations_list, 95):>10.3f}")

print("\nClause roles, in cost order:")
print("  SINCE  decides how many events are SCANNED (not shown: this window was fixed)")
print("  WHERE  decides how many survive to aggregation")
print("  FACET  decides how many series come back — bounded here (4 URIs), and only")
print("         because these URIs carry no embedded IDs. FACET on a raw URL space")
print("         with /orders/88213-style paths is the cardinality explosion again.")
EOF
```

**Expected result:** Four facets with `/checkout` slowest at p95, and the clause-by-clause narration showing where volume drops. The closing note is the transferable one — `FACET` is this platform's cardinality lever, and it is safe here only because the URI space is bounded.

**Negative test:** `FACET` on an attribute with unbounded values. The query returns, the chart is unreadable, and at alert-evaluation time the cost recurs every minute.

**Cleanup:** None.

### Lab 3.2 — Events versus metrics: the same question, two costs

**Objective:** Quantify explore-on-events, standardize-on-metrics.

```bash
python3 - <<'EOF'
EVENTS_PER_DAY   = 40_000_000      # Transaction events, busy estate
METRIC_POINTS_PER_DAY = 1440       # one aggregate per minute per series
SCAN_COST_PER_M  = 1.0             # arbitrary units per million records scanned

QUESTIONS = [
  ("p95 latency, daily panel, 24h window, loaded ~200x/day", "daily", 1,   True),
  ("p95 latency trend, 90-day capacity review, run once",    "rare",  90,  False),
  ("every txn >2s for ONE premium customer, last 6h, run once","rare", 0.25,False),
]
print(f"{'question':58}{'events cost':>13}{'metric cost':>13}   verdict")
for q, freq, days, repeated in QUESTIONS:
    ev = days * EVENTS_PER_DAY / 1e6 * SCAN_COST_PER_M
    mt = days * METRIC_POINTS_PER_DAY / 1e6 * SCAN_COST_PER_M
    runs = 200 if repeated else 1
    ev_total, mt_total = ev * runs, mt * runs
    if "ONE premium customer" in q:
        verdict = "EVENTS — needs an attribute metrics never kept"
    elif repeated:
        verdict = f"METRIC — {ev_total/max(mt_total,1e-9):,.0f}x cheaper at {runs} runs/day"
    else:
        verdict = "either; events fine for a one-off"
    print(f"{q:58}{ev_total:>13,.1f}{mt_total:>13,.4f}   {verdict}")

print("\nThe rule: EXPLORE on events, STANDARDIZE on metrics.")
print("The customer question is the reverse lesson — no metric can answer it,")
print("because 'which customer' was never a dimension. Events keep every attribute")
print("precisely so that questions nobody predicted stay answerable.")
EOF
```

**Expected result:** The daily panel is thousands of times cheaper as a metric query, while the single-customer question is only answerable from events at any price. Both halves matter: the cost argument pushes standard views onto metrics, and the capability argument is why events exist at all.

**Negative test:** Building the daily dashboard on `FROM Transaction` because it worked in testing. It keeps working — 200 times a day, against a full day's events, forever.

**Cleanup:** None.

### Lab 3.3 — One wrong WHERE, three broken features

**Objective:** Show why a shared query language concentrates risk.

```bash
python3 - <<'EOF'
import random
random.seed(21)
SAMPLED = [{"error": random.random() < 0.02,
         "http.statusCode": random.choice([200]*92 + [404]*3 + [500]*2 + [503]*3)}
        for _ in range(10_000)]

def true_error_rate(sampled):
    return sum(1 for t in sampled if t["error"] or t["http.statusCode"] >= 500) / len(sampled) * 100

def buggy_error_rate(sampled):     # WHERE http.statusCode = 500  (misses 503 and agent-caught errors)
    return sum(1 for t in sampled if t["http.statusCode"] == 500) / len(sampled) * 100

t, b = true_error_rate(SAMPLED), buggy_error_rate(SAMPLED)
print(f"true error rate  : {t:.2f}%   (error flag OR any 5xx)")
print(f"buggy WHERE      : {b:.2f}%   (statusCode = 500 only)")
print(f"under-count       : {(1-b/t)*100:.0f}% of real errors invisible\n")
print("Because the SAME query is reused, the bug ships three times at once:")
print(f"   dashboard panel    shows {b:.2f}% — looks fine")
print(f"   alert condition    fires when {b:.2f}% crosses 3% — it never does")
print(f"   service level SLI  reports {100-b:.2f}% success — SLO 'met'")
print("\nOne language everywhere is leverage in both directions: fix the query once")
print("and all three heal; get it wrong once and all three lie in perfect agreement.")
print("Agreement between your dashboard, your alert, and your SLO is NOT evidence of")
print("correctness when all three inherit the same WHERE clause.")
EOF
```

**Expected result:** The buggy predicate under-counts errors by about 70% — a 6.9% true rate reported as 2% — and dashboard, alert, and SLO all repeat the same wrong number, with the alert never crossing its 3% threshold. The closing sentence is the chapter's sharpest point — three features agreeing proves nothing when they share one clause, so the query itself is what deserves review.

**Negative test:** Validating an alert by checking it matches the dashboard. When both wrap the same NRQL, that check can only ever pass.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] NRQL clause roles understood, with `SINCE` and `FACET` as the cost levers.
- [ ] Events used for exploration and novel attributes; metrics for standardized views.
- [ ] Facet cardinality kept bounded.
- [ ] The shared-language risk understood: one wrong clause propagates to every feature built on it.
