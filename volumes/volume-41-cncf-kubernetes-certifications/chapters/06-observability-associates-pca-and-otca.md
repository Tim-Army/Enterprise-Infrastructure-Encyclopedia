# Chapter 06: Observability Associates — PCA and OTCA

## Learning Objectives

- Explain the two observability associate credentials: PCA (Prometheus) and OTCA (OpenTelemetry).
- List the PCA and OTCA domains and their exam weights.
- Describe the multiple-choice format and the projects each certifies.
- Apply core skills: PromQL, exporters, alerting; and OpenTelemetry signals, SDK, and the Collector.
- Complete a per-domain walkthrough for every PCA and OTCA domain.

## Theory and Architecture

Observability — the ability to ask new questions of a system from its telemetry —
is certified through two CNCF associate exams:

- **Prometheus Certified Associate (PCA)** — the metrics and monitoring
  credential, centered on **PromQL**. Multiple-choice, 90 minutes. Five domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Observability Concepts | 18% |
  | 2 | Prometheus Fundamentals | 20% |
  | 3 | PromQL | 28% |
  | 4 | Instrumentation and Exporters | 16% |
  | 5 | Alerting & Dashboarding | 18% |

- **OpenTelemetry Certified Associate (OTCA)** — the vendor-neutral telemetry
  (traces, metrics, logs) credential. Multiple-choice. Four domains:

  | # | Domain | Weight |
  |---|--------|--------|
  | 1 | Fundamentals of Observability | 18% |
  | 2 | The OpenTelemetry API and SDK | 46% |
  | 3 | The OpenTelemetry Collector | 26% |
  | 4 | Maintaining and Debugging Observability Pipelines | 10% |

**PromQL (28%)** dominates PCA; **the API and SDK (46%)** dominates OTCA.

## Design Considerations

The two are complementary: **OpenTelemetry** *produces and ships* telemetry
(instrumentation, the SDK, the Collector), and **Prometheus** *stores and
queries* metrics. A modern stack often instruments with OpenTelemetry and exports
metrics to Prometheus. For PCA, invest in **PromQL** (selectors, `rate()`,
aggregation, histograms); for OTCA, invest in the **signals, SDK pipeline, and
Collector** (receivers → processors → exporters).

## Implementation and Automation

The labs below use `promtool` and PromQL expressions (PCA) and OpenTelemetry
Collector configuration and signal reasoning (OTCA) — portable demonstrations
that need no running backend to study.

## Validation and Troubleshooting

Confirm both blueprints before studying:

```text
training.linuxfoundation.org > PCA and OTCA > curricula:
  - PCA: five domains (18/20/28/16/18), multiple-choice, PromQL-heavy
  - OTCA: four domains (18/46/26/10), multiple-choice, SDK-heavy
```

Common pitfalls: treating PromQL as an afterthought (it is 28%); confusing a
**counter** (monotonic, use `rate()`) with a **gauge**; and conflating the
OpenTelemetry **API** (instrumentation surface) with the **SDK** (the
implementation that samples, batches, and exports).

## Security and Best Practices

Instrument with **semantic conventions** so telemetry is portable; use the
**Collector** to centralize processing (redaction, batching, routing) rather than
per-service exporters; and alert on **symptoms** (SLO burn) not just causes.
Protect telemetry endpoints — metrics and traces can leak sensitive data.

## References and Knowledge Checks

- training.linuxfoundation.org: *PCA* and *OTCA* curricula; prometheus.io; opentelemetry.io.

**Knowledge checks**

1. Which PCA domain is heaviest, and why?
2. What is the difference between the OpenTelemetry API and SDK?
3. How do Prometheus and OpenTelemetry fit together in a stack?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted PCA and OTCA domain**.

**Shared prerequisites** — a Linux shell with `python3`; `promtool` optional
(concepts shown regardless). **Cost:** none.

### PCA — Prometheus Certified Associate

### Lab 6.1 — PCA: Observability Concepts (18%)

**Objective:** Distinguish the pillars and the pull model.

```bash
python3 - <<'PY'
pillars = {"Metrics":"numeric time series (Prometheus)",
           "Logs":"discrete events","Traces":"request paths across services"}
for k,v in pillars.items(): print(f"{k:8}: {v}")
print("Prometheus is PULL-based: it scrapes /metrics from targets it discovers.")
PY
```

**Expected result:** the three telemetry pillars and Prometheus's pull/scrape
model — the observability concepts PCA Domain 1 tests.

**Negative test:** assume Prometheus pushes; it **pulls** (scrapes) targets —
push is the exception (Pushgateway) for short-lived jobs.

**Cleanup:** none.

### Lab 6.2 — PCA: Prometheus Fundamentals (20%)

**Objective:** Read the exposition format and the data model (labels).

```bash
cat <<'EOF'
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="get",code="200"} 1027
http_requests_total{method="get",code="500"} 3
EOF
echo "Series identity = metric name + label set; {method,code} are dimensions."
```

**Expected result:** a counter metric with `{method,code}` labels — the
exposition format and dimensional data model of PCA Domain 2.

**Negative test:** treat two series with different labels as the same series; the
**label set** is part of the identity — they are distinct time series.

**Cleanup:** none.

### Lab 6.3 — PCA: PromQL (28%)

**Objective:** Write the canonical rate-of-a-counter query.

```bash
cat <<'EOF'
# per-second request rate over 5m, aggregated by code:
sum by (code) (rate(http_requests_total[5m]))

# error ratio:
sum(rate(http_requests_total{code="500"}[5m]))
  / sum(rate(http_requests_total[5m]))
EOF
echo "rate() needs a range vector [5m]; always rate() a counter before aggregating."
```

**Expected result:** a `sum by (code) (rate(...[5m]))` query and an error-ratio
expression — the PromQL fluency that is PCA's heaviest domain.

**Negative test:** `sum(http_requests_total)` a raw counter; counters only
increase — you must `rate()` over a range first.

**Cleanup:** none.

### Lab 6.4 — PCA: Instrumentation and Exporters (16%)

**Objective:** Choose metric types and naming for instrumentation.

```bash
python3 - <<'PY'
choices = {"requests served":"Counter (monotonic) -> http_requests_total",
           "current memory":"Gauge (up/down) -> process_resident_memory_bytes",
           "request latency":"Histogram -> http_request_duration_seconds_bucket"}
for what,how in choices.items(): print(f"{what:18} -> {how}")
print("Exporters expose third-party systems' metrics (node_exporter, blackbox_exporter).")
PY
```

**Expected result:** each measurement mapped to the correct metric type and a
conventional name, plus the role of exporters — PCA Domain 4.

**Negative test:** use a Gauge for a total count; use a **Counter** so `rate()`
works and resets are handled correctly.

**Cleanup:** none.

### Lab 6.5 — PCA: Alerting & Dashboarding (18%)

**Objective:** Write an alerting rule and describe Alertmanager routing.

```bash
cat <<'EOF'
groups:
- name: availability
  rules:
  - alert: HighErrorRate
    expr: sum(rate(http_requests_total{code="500"}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
    for: 10m
    labels: {severity: page}
EOF
echo "Alertmanager: dedups, groups, silences, and routes alerts to receivers."
```

**Expected result:** a `HighErrorRate` rule (>5% for 10m) and the Alertmanager
role — the alerting-and-dashboarding domain of PCA.

**Negative test:** alert without a `for:` duration; a momentary spike pages
someone — require the condition to hold before firing.

**Cleanup:** none.

### OTCA — OpenTelemetry Certified Associate

### Lab 6.6 — OTCA: Fundamentals of Observability (18%)

**Objective:** Relate the three OTel signals and semantic conventions.

```bash
python3 - <<'PY'
signals = {"traces":"causal request paths (spans)","metrics":"aggregated numbers",
           "logs":"timestamped records"}
for s,d in signals.items(): print(f"{s:7}: {d}")
print("Semantic conventions standardize attribute names (http.method, service.name) across tools.")
PY
```

**Expected result:** the three signals plus the role of semantic conventions —
the vendor-neutral fundamentals OTCA Domain 1 tests.

**Negative test:** invent custom attribute names; **semantic conventions** make
telemetry portable across backends — follow them.

**Cleanup:** none.

### Lab 6.7 — OTCA: The OpenTelemetry API and SDK (46%)

**Objective:** Distinguish the API from the SDK in the pipeline.

```bash
python3 - <<'PY'
print("API : the instrumentation surface (create spans/metrics) — stable, no-op if no SDK")
print("SDK : the implementation — samplers, processors, exporters, context propagation")
print("Pipeline: Instrument (API) -> Process/Batch (SDK) -> Export (OTLP) -> Collector/Backend")
PY
```

**Expected result:** the API-vs-SDK split and the export pipeline — OTCA's
heaviest domain (nearly half the exam).

**Negative test:** assume instrumenting with the API alone emits data; without an
**SDK** configured, the API is a no-op — you must wire the SDK.

**Cleanup:** none.

### Lab 6.8 — OTCA: The OpenTelemetry Collector (26%)

**Objective:** Configure a Collector pipeline (receivers → processors →
exporters).

```bash
cat <<'EOF'
receivers:   {otlp: {protocols: {grpc: {}, http: {}}}}
processors:  {batch: {}, memory_limiter: {check_interval: 1s, limit_mib: 400}}
exporters:   {debug: {}, prometheus: {endpoint: "0.0.0.0:8889"}}
service:
  pipelines:
    metrics: {receivers: [otlp], processors: [memory_limiter, batch], exporters: [prometheus]}
EOF
echo "The Collector decouples apps from backends: receive -> process -> export."
```

**Expected result:** a valid Collector pipeline routing OTLP metrics to a
Prometheus exporter — the Collector architecture of OTCA Domain 3.

**Negative test:** export directly from every app to every backend; the
**Collector** centralizes processing and routing — use it as the hub.

**Cleanup:** none.

### Lab 6.9 — OTCA: Maintaining and Debugging Observability Pipelines (10%)

**Objective:** Debug a pipeline with the debug exporter and context propagation.

```bash
python3 - <<'PY'
checks = ["Add a `debug` exporter to see data reaching the Collector",
          "Verify context propagation (traceparent header) across services",
          "Watch Collector's own metrics for dropped/refused spans",
          "Check exporter queue/retry on backend errors"]
for c in checks: print("-", c)
PY
```

**Expected result:** a pipeline-debugging checklist (debug exporter, propagation,
Collector self-metrics, exporter retries) — OTCA Domain 4.

**Negative test:** assume missing traces mean the app is broken; often the
**context (traceparent) isn't propagated** or the exporter is dropping — debug
the pipeline end to end.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The observability associates certify the two halves of a telemetry stack: **PCA**
(five domains 18/20/28/16/18, PromQL-heavy) for storing and querying metrics, and
**OTCA** (four domains 18/46/26/10, SDK-heavy) for producing and shipping traces,
metrics, and logs. Together they cover instrumentation, the Collector, PromQL,
and alerting.

- [ ] I can list the PCA and OTCA domains and their weights.
- [ ] I can write a `rate()`-based PromQL query and an alerting rule.
- [ ] I can distinguish the OTel API from the SDK and configure a Collector pipeline.
- [ ] I can debug a telemetry pipeline end to end.
- [ ] I completed Labs 6.1–6.9 including each negative test.
