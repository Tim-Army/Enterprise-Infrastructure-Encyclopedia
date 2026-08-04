# Chapter 04: PromQL for Metrics

## Learning Objectives

- Read and write PromQL: selectors, matchers, and the four metric types.
- Use `rate()` correctly on counters, and know why `sum` before `rate` is wrong.
- Aggregate with `by` and `without`, and join series with vector matching.
- Recognize and prevent cardinality explosion.

## The four metric types

PromQL is the query language for Prometheus and Mimir, and reading it starts with knowing what kind of metric you are looking at:

| Type | Behavior | Query with |
|:---|:---|:---|
| **Counter** | Only increases; resets to zero on restart | **Always** `rate()` or `increase()` — never the raw value |
| **Gauge** | Goes up and down | Read directly; aggregate with `avg`, `max`, `sum` |
| **Histogram** | Observations bucketed by size | `histogram_quantile()` over `rate()` of buckets |
| **Summary** | Pre-computed quantiles at the client | Read the quantile directly; **cannot** be aggregated across instances |

The counter rule is the single most common source of wrong dashboards. A counter's raw value is "how many since this process started," which is meaningless to plot — what you want is the rate of change.

## `rate()` and the order of operations

`rate(metric[5m])` computes the per-second average increase over a five-minute window, and it handles counter resets correctly — that is its whole purpose.

The rule that trips people up:

> **`rate()` must be applied before `sum()`, never after.**

`sum(rate(x[5m]))` is correct. `rate(sum(x)[5m])` is wrong, because summing across instances destroys the per-series information `rate` needs to detect resets: when one instance restarts, the summed series dips, and `rate` reads that dip as a legitimate decrease rather than a reset.

The window matters too. `rate()` needs at least two samples in its window, so the range must be **at least twice the scrape interval** — a `rate(x[1m])` against a 60-second scrape is unreliable, and the usual guidance is four times the interval.

## Aggregation

`by` keeps the listed labels; `without` drops them. They are complements, and choosing correctly is about what you want the result to be *per*:

- `sum(rate(http_requests_total[5m])) by (service)` — one series per service.
- `sum(rate(http_requests_total[5m])) without (instance, pod)` — everything except instance and pod, which keeps labels you did not have to enumerate.

`without` is the more maintainable choice when new labels appear over time, because it does not silently drop dimensions you forgot to list.

## Cardinality

**Cardinality** is the number of distinct time series, and it is the property that decides whether your metrics system stays fast and affordable. Every unique combination of label values is its own series.

The multiplication is unforgiving: 100 pods × 20 endpoints × 5 status codes × 3 methods = 30,000 series from **one** metric name. Add a label with unbounded values — a user ID, a request ID, a full URL path, a commit SHA — and the count grows without limit.

The remedies, in order of preference: do not create the label (Chapter 02's process stage), aggregate away from the high-cardinality dimension in recording rules (Chapter 08), and use exemplars or traces for the per-request detail you were trying to capture with labels.

## Hands-On Lab

Python models PromQL semantics. **Cost:** none.

### Lab 4.1 — Counters, `rate()`, and why order matters

**Objective:** Show what breaks when `rate` and `sum` are transposed.

```bash
python3 - <<'EOF'
# Two instances scraped every 15s; instance B RESTARTS between t=45 and t=60
a = [(0,1000),(15,1150),(30,1300),(45,1450),(60,1600)]
b = [(0,5000),(15,5200),(30,5400),(45,5600),(60,120)]   # <-- restart: counter resets

def rate_series(samples):
    out = []
    for (t0,v0),(t1,v1) in zip(samples, samples[1:]):
        delta = v1 - v0
        if delta < 0:                       # counter reset detected on THIS series
            delta = v1                      # treat post-reset value as the increase
        out.append((t1, delta/(t1-t0)))
    return out

print("CORRECT — sum(rate(x)):  rate per instance first, then add")
ra, rb = rate_series(a), rate_series(b)
for (t, va), (_, vb) in zip(ra, rb):
    print(f"   t={t:>3}s  A={va:6.2f}/s  B={vb:6.2f}/s  sum={va+vb:7.2f}/s")

print("\nWRONG — rate(sum(x)): add first, then rate")
summed = [(t, va+vb) for (t,va),(_,vb) in zip(a,b)]
for (t0,v0),(t1,v1) in zip(summed, summed[1:]):
    delta = v1 - v0
    flag = "  <-- NEGATIVE: the restart looks like a DECREASE" if delta < 0 else ""
    print(f"   t={t1:>3}s  summed rate={delta/(t1-t0):8.2f}/s{flag}")

print("\nSumming first destroys per-series reset detection. One instance restarting makes the")
print("aggregate dip, and rate() reads that as real traffic loss — a false outage on your dashboard.")
print("Rule: rate() ALWAYS goes inside sum(), never outside.")
EOF
```

**Expected result:** The correct form holds steady at about 23 requests/second across the restart, while the transposed form produces a large negative rate at t=60. That negative spike is what appears on a dashboard as a sudden traffic collapse that never happened — and because restarts are routine, the false alarm recurs.

**Negative test:** Writing `rate(sum(...))` because it reads more naturally left to right — it is syntactically valid, produces a plausible-looking graph most of the time, and lies whenever anything restarts.

**Cleanup:** None.

### Lab 4.2 — Aggregation with `by` and `without`

**Objective:** Choose the aggregation that survives new labels.

```bash
python3 - <<'EOF'
series = [
  {"labels":{"service":"api","instance":"i-1","pod":"api-a","code":"200"},"rate":40.0},
  {"labels":{"service":"api","instance":"i-2","pod":"api-b","code":"200"},"rate":35.0},
  {"labels":{"service":"api","instance":"i-1","pod":"api-a","code":"500"},"rate":2.0},
  {"labels":{"service":"web","instance":"i-3","pod":"web-a","code":"200"},"rate":90.0},
]
def aggregate(series, by=None, without=None):
    out = {}
    for s in series:
        if by is not None:      key = tuple(sorted((k, s["labels"][k]) for k in by if k in s["labels"]))
        else:                   key = tuple(sorted((k, v) for k, v in s["labels"].items() if k not in without))
        out[key] = out.get(key, 0) + s["rate"]
    return out

print("sum(...) by (service):")
for k, v in aggregate(series, by=["service"]).items():        print(f"   {dict(k)} = {v}")
print("\nsum(...) by (service, code):")
for k, v in aggregate(series, by=["service","code"]).items(): print(f"   {dict(k)} = {v}")
print("\nsum(...) without (instance, pod):")
for k, v in aggregate(series, without={"instance","pod"}).items(): print(f"   {dict(k)} = {v}")

print("\nNow a NEW label 'region' appears on every series (a deployment change):")
for s in series: s["labels"]["region"] = "eu-west"
print("   by (service, code)      -> region is SILENTLY DROPPED; you lose a dimension without noticing")
print("   without (instance, pod) -> region is KEPT automatically")
print("\n'without' is the more maintainable default: it survives labels you did not know about.")
EOF
```

**Expected result:** `by (service)` collapses to two series, `by (service, code)` separates the error rate, and `without` retains everything except the instance-level labels. The closing observation is the practical one — when a new label appears later, `by` silently discards it while `without` keeps it, so `without` degrades more gracefully as an estate evolves.

**Negative test:** Aggregating with `by (service)` on a dashboard meant to show errors — the 500s are summed into the total and the error signal disappears entirely.

**Cleanup:** None.

### Lab 4.3 — Cardinality arithmetic

**Objective:** Compute series counts and find the label that must go.

```bash
python3 - <<'EOF'
def cardinality(dimensions):
    total = 1
    for _, n in dimensions: total *= n
    return total

base = [("pod", 100), ("endpoint", 20), ("status", 5), ("method", 3)]
print("Baseline for ONE metric name:")
for name, n in base: print(f"   {name:12} {n:>7,} values")
print(f"   -> {cardinality(base):,} series\n")

for label, n, note in [("user_id", 50000, "unbounded — one per user"),
                       ("request_id", 1000000, "unbounded — one per REQUEST"),
                       ("commit_sha", 400, "grows with every deploy, forever")]:
    total = cardinality(base + [(label, n)])
    print(f"add {label:11} ({note})")
    print(f"   -> {total:,} series  ({total/cardinality(base):,.0f}x increase)\n")

print("Any label whose values are UNBOUNDED will eventually break the system:")
print("   user_id, request_id, session_id, full URL path, error message text, commit_sha")
print("\nFixes, in order of preference:")
print("   1. never create the label (drop it in the collector — ch02's process stage)")
print("   2. aggregate it away in a recording rule (ch08)")
print("   3. use EXEMPLARS or TRACES for per-request detail — that is what they are for")
print("\nLabels are for dimensions you GROUP BY. If you would never group by it, it is not a label.")
EOF
```

**Expected result:** A 30,000-series baseline becomes 1.5 billion with `user_id` and 30 billion with `request_id`. The closing test — *"if you would never group by it, it is not a label"* — is the most useful single heuristic for label design, and it correctly rejects every unbounded example.

**Negative test:** Adding a label "temporarily, to debug an issue" — the series it creates persist for the full retention period, and the cost and query slowdown outlive the debugging session by weeks.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The four metric types distinguished, with counters always read through `rate()`.
- [ ] `sum(rate(...))` ordering justified by counter-reset detection.
- [ ] Range windows sized against the scrape interval.
- [ ] `by` and `without` compared, with `without` preferred for maintainability.
- [ ] Cardinality computed, and the "would I group by it?" test applied to label design.
