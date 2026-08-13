# Chapter 02: The Data Model and Metric Types

## Learning Objectives

- Explain the Prometheus data model: metrics, labels, samples.
- Distinguish the four metric types.
- Read the text exposition format.
- Reason about label cardinality.
- Complete a walkthrough for each concept.

## Theory and Architecture

A Prometheus **time series** is identified by a **metric name** plus a set of **labels**
(key/value pairs); each series is a stream of **samples** (timestamp + float value).
There are four **metric types**: **Counter** (monotonically increasing, e.g., total
requests), **Gauge** (goes up and down, e.g., memory in use), **Histogram** (samples
into cumulative buckets plus `_sum`/`_count`, e.g., latency), and **Summary** (client-
side quantiles plus `_sum`/`_count`). Targets expose these in a simple **text exposition
format** at `/metrics`. Every unique label combination is a separate series — the basis
of **cardinality**.

## Design Considerations

Choose the type by semantics (monotonic → Counter; distribution → Histogram). Prefer
**histograms** over summaries for aggregatable quantiles. Keep labels **low-cardinality**
(no user IDs, no unbounded values) — cardinality drives memory and query cost.

## Implementation and Automation

The labs read the exposition format and reason about types and cardinality.

## Validation and Troubleshooting

Confirm the model:

```text
Series = metric_name{label=value,...} -> samples (ts, value).
Types: Counter (monotonic), Gauge (up/down), Histogram (buckets+_sum/_count),
Summary (quantiles+_sum/_count). Exposition: text /metrics.
Cardinality = number of unique label combinations.
```

Common pitfalls: a Gauge where a Counter is right (or vice versa); and high-cardinality
labels.

## Security and Best Practices

Match the **metric type** to semantics, prefer **histograms** for latency, keep labels
**bounded**, and name metrics with units (`_seconds`, `_bytes`, `_total`). Avoid
embedding high-cardinality values in labels.

## Hands-On Lab

Data-model walkthroughs. **Shared prerequisites** — a running Prometheus (Chapter 01);
`curl`, `python3`. **Cost:** none.

### Lab 2.1 — Read the exposition format

**Objective:** Fetch raw metrics from a target.

```bash
curl -sS "http://localhost:9090/metrics" | grep -E "^# (HELP|TYPE) prometheus_http_requests_total" 
curl -sS "http://localhost:9090/metrics" | grep "^prometheus_http_requests_total" | head -3
```

**Expected result:** the **HELP/TYPE** metadata and sample lines for a counter — the text
exposition format.

**Negative test:** parse metrics with ad-hoc regex ignoring `# TYPE`; the **TYPE**
comment tells you how to interpret the series — read it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Identify a counter vs gauge

**Objective:** Contrast a counter and a gauge.

```bash
curl -sS "http://localhost:9090/metrics" | grep -E "^# TYPE (go_goroutines|prometheus_http_requests_total) "
```

**Expected result:** `go_goroutines` typed **gauge** and `prometheus_http_requests_total`
typed **counter** — the two most common types.

**Negative test:** graph a counter's raw value as a rate; counters need **`rate()`** —
raw counters only ever climb.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Inspect a histogram

**Objective:** See histogram buckets.

```bash
curl -sS "http://localhost:9090/metrics" | grep "prometheus_http_request_duration_seconds_bucket" | head -5
```

**Expected result:** cumulative **`_bucket{le="..."}`** series (plus `_sum`/`_count`) — a
histogram's structure.

**Negative test:** use a summary expecting to aggregate quantiles across instances;
**histograms** aggregate, summaries don't — prefer histograms.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Reason about cardinality

**Objective:** Measure series count.

```bash
curl -sS "http://localhost:9090/api/v1/query?query=count(count%20by(__name__)({__name__!=\"\"}))" \
  | python3 -c "import sys,json;print('distinct metric names:',json.load(sys.stdin)['data']['result'][0]['value'][1])"
```

**Expected result:** the count of distinct metric names — a proxy for the TSDB's series
scope.

**Negative test:** add a label like `request_id`; each value spawns a **new series** —
cardinality explodes, so keep labels bounded.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Prometheus series are metric names plus labels carrying timestamped samples, in four
types (counter, gauge, histogram, summary) exposed as text at `/metrics`, with
cardinality set by unique label combinations. This chapter read the exposition format
and reasoned about types and cardinality.

- [ ] I can explain series, labels, and samples.
- [ ] I can distinguish the four metric types.
- [ ] I can read the exposition format and histograms.
- [ ] I can reason about label cardinality.
- [ ] I completed Labs 2.1–2.4 including each negative test.
