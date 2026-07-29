# Chapter 04: PromQL Fundamentals

## Learning Objectives

- Select series with instant and range vectors.
- Compute rates from counters.
- Aggregate across series with operators.
- Filter with comparison operators.
- Complete a walkthrough for each PromQL basic.

## Theory and Architecture

**PromQL** is Prometheus's query language. It operates on **instant vectors** (a value
per series at one instant) and **range vectors** (a range of samples per series, e.g.,
`[5m]`). Counters are queried with **`rate()`/`irate()`** over a range vector to get
per-second rates. **Aggregation operators** (`sum`, `avg`, `max`, `min`, `count`,
`topk`) collapse series, optionally grouped with `by`/`without`. **Comparison operators**
filter or produce booleans. The golden pattern for a counter is
`rate(metric_total[5m])` then `sum by (label) (...)`.

## Design Considerations

Always **`rate()`** counters before aggregating (never sum raw counters). Choose the
range window to cover a few scrape intervals. Aggregate with **`by`** to keep the labels
you need. Use `irate` for fast-moving graphs, `rate` for alerting stability.

## Implementation and Automation

The labs run PromQL over the HTTP API against the running Prometheus.

## Validation and Troubleshooting

Confirm the basics:

```text
Instant vector: metric{labels}. Range vector: metric[5m].
Counter rate: rate(metric_total[5m]) (per-second). Aggregate: sum by (label) (...).
Filter: metric > 0. topk(k, ...) for top-N.
```

Common pitfalls: `sum()` of raw counters (meaningless); and a range window smaller than
the scrape interval (empty/NaN rates).

## Security and Best Practices

**Rate before aggregate**, size range windows to cover scrape intervals, aggregate with
**`by`** to preserve meaningful labels, and prefer `rate` for alerts. Keep queries
readable and label-aware.

## Hands-On Lab

PromQL walkthroughs. **Shared prerequisites** — a running Prometheus; `curl`, `python3`.
Queries use `/api/v1/query`. **Cost:** none.

### Lab 4.1 — Instant vector selector

**Objective:** Select a metric with a label matcher.

```bash
curl -sSG "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=up{job="prometheus"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['result'][0]['value'])"
```

**Expected result:** the **`up`** value (`1`) for the prometheus job — an instant vector.

**Negative test:** match a label value that doesn't exist; you get an **empty result** —
check label values with `/api/v1/label/<name>/values`.

**Cleanup:** none.

### Lab 4.2 — Rate of a counter

**Objective:** Compute a per-second rate.

```bash
curl -sSG "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=rate(prometheus_http_requests_total[5m])' \
  | python3 -c "import sys,json;print('series:',len(json.load(sys.stdin)['data']['result']))"
```

**Expected result:** per-series **request rates** over 5 minutes — the counter idiom.

**Negative test:** query the raw counter for a graph; it only **climbs** — wrap it in
`rate()`.

**Cleanup:** none.

### Lab 4.3 — Aggregate with by

**Objective:** Sum rates grouped by a label.

```bash
curl -sSG "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=sum by (code) (rate(prometheus_http_requests_total[5m]))' \
  | python3 -c "import sys,json;print([r['metric'] for r in json.load(sys.stdin)['data']['result']])"
```

**Expected result:** request rate **grouped by HTTP `code`** — aggregation preserving one
label.

**Negative test:** `sum()` without `by`; you lose all labels — use **`by (code)`** to
keep the dimension you need.

**Cleanup:** none.

### Lab 4.4 — Filter with a comparison

**Objective:** Keep only series above a threshold.

```bash
curl -sSG "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=go_goroutines > 5' \
  | python3 -c "import sys,json;print('matching series:',len(json.load(sys.stdin)['data']['result']))"
```

**Expected result:** only series where goroutines **exceed 5** — comparison as a filter.

**Negative test:** eyeball all series to find high ones; a **comparison operator** filters
server-side — use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

PromQL selects instant/range vectors, rates counters, aggregates with operators grouped
by labels, and filters with comparisons — the golden pattern being
`sum by (label) (rate(metric_total[5m]))`. This chapter ran each basic against the API.

- [ ] I can select series with label matchers.
- [ ] I can rate a counter over a range.
- [ ] I can aggregate with `by`.
- [ ] I can filter with comparison operators.
- [ ] I completed Labs 4.1–4.4 including each negative test.
