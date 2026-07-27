# Chapter 05: PromQL Advanced

## Learning Objectives

- Compute quantiles from histograms.
- Use subqueries for range-over-range analysis.
- Join series with vector matching (`on`, `group_left`).
- Apply `increase`, `offset`, and `predict_linear`.
- Complete a walkthrough for each advanced technique.

## Theory and Architecture

Advanced PromQL turns raw series into SLO-grade signals. **`histogram_quantile()`**
computes a percentile (e.g., p99 latency) from a histogram's `_bucket` series.
**Subqueries** (`<expr>[5m:1m]`) evaluate an expression over a range, enabling
range-over-range (e.g., max of a rate). **Vector matching** joins two vectors:
one-to-one on shared labels (`on`/`ignoring`) and many-to-one with **`group_left`/
`group_right`** to enrich series with metadata (e.g., join metrics to an `info` series).
Time functions like **`increase`**, **`offset`**, and **`predict_linear`** support
totals, comparisons, and forecasting.

## Design Considerations

Use **`histogram_quantile`** on **rated** buckets (`rate(..._bucket[5m])`) for
percentiles. Use **`group_left`** to attach labels from an info metric. Use
**`predict_linear`** for capacity alerts (e.g., disk full in N hours).

## Implementation and Automation

The labs run advanced PromQL over the HTTP API.

## Validation and Troubleshooting

Confirm the techniques:

```text
Percentile: histogram_quantile(0.99, sum by (le) (rate(metric_bucket[5m]))).
Subquery: max_over_time(rate(m[5m])[1h:1m]). Matching: a * on(x) group_left(y) b.
increase(m[1h]); m offset 1d; predict_linear(m[1h], 4*3600).
```

Common pitfalls: `histogram_quantile` on raw (non-rated) buckets; and vector-matching
mismatches (labels don't align).

## Security and Best Practices

Percentiles from **rated buckets**, join metadata with **`group_left`**, forecast with
**`predict_linear`** for proactive capacity alerts, and align labels carefully in vector
matches. Keep advanced queries documented — they encode SLOs.

## Hands-On Lab

Advanced PromQL walkthroughs. **Shared prerequisites** — a running Prometheus; `curl`,
`python3`. **Cost:** none.

### Lab 5.1 — Compute a p99 from a histogram

**Objective:** Get the 99th-percentile latency.

```bash
curl -sSG "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum by (le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))' \
  | python3 -c "import sys,json;r=json.load(sys.stdin)['data']['result'];print('p99:',r[0]['value'][1] if r else None)"
```

**Expected result:** a **p99 latency** value in seconds — a percentile from histogram
buckets.

**Negative test:** run `histogram_quantile` on raw `_bucket` (no `rate`); you get wrong
values — **rate the buckets** first.

**Cleanup:** none.

### Lab 5.2 — Subquery (max of a rate)

**Objective:** Find the peak rate over the last hour.

```bash
curl -sSG "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=max_over_time(rate(prometheus_http_requests_total[5m])[1h:1m])' \
  | python3 -c "import sys,json;print('series:',len(json.load(sys.stdin)['data']['result']))"
```

**Expected result:** the **peak 5-minute rate** across the last hour — a subquery.

**Negative test:** try `max_over_time(rate(...[5m]))` without the subquery `[1h:1m]`; you
need the **subquery range** to evaluate over time.

**Cleanup:** none.

### Lab 5.3 — Vector matching with group_left

**Objective:** Enrich a metric with info-metric labels.

```text
# Join a metric to a build_info series to attach the 'version' label:
#   rate(app_requests_total[5m]) * on(instance) group_left(version) app_build_info
"result: request rate series enriched with the app version label"
```

**Expected result:** request-rate series carrying the **`version`** label from the info
metric — many-to-one vector matching.

**Negative test:** join on mismatched labels; the match **produces nothing** — align the
`on(...)` labels.

**Cleanup:** none.

### Lab 5.4 — Forecast with predict_linear

**Objective:** Predict a value into the future.

```bash
curl -sSG "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=predict_linear(go_memstats_alloc_bytes[30m], 4*3600)' \
  | python3 -c "import sys,json;r=json.load(sys.stdin)['data']['result'];print('predicted bytes in 4h:',r[0]['value'][1] if r else None)"
```

**Expected result:** a **predicted value** 4 hours ahead — linear forecasting for
capacity alerts.

**Negative test:** alert only when a resource is already full; **predict_linear** warns
before it happens — alert on the forecast.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Advanced PromQL computes percentiles from histograms, evaluates subqueries, joins series
with vector matching (`group_left`), and forecasts with `predict_linear` — turning raw
metrics into SLO and capacity signals. This chapter applied each technique.

- [ ] I can compute percentiles from rated histogram buckets.
- [ ] I can write subqueries for range-over-range analysis.
- [ ] I can join series with group_left.
- [ ] I can forecast with predict_linear.
- [ ] I completed Labs 5.1–5.4 including each negative test.
