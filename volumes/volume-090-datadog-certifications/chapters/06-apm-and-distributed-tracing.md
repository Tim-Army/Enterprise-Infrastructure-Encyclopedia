# Chapter 06: APM and Distributed Tracing

## Learning Objectives

- Instrument an application for APM.
- Explain traces, spans, and the service map.
- Search and analyze traces.
- Troubleshoot a slow request with APM.
- Complete a walkthrough for each APM topic.

## Theory and Architecture

The **APM & Distributed Tracing Fundamentals** exam covers Datadog **Application Performance Monitoring**.
An application is **instrumented** with a Datadog tracing library (**`dd-trace`** for Node/Python/Java/Go/
Ruby/.NET/PHP, or **OpenTelemetry**), which captures a **trace** for each request — a tree of **spans**,
where each span is one unit of work (an HTTP handler, a database query, an outbound call) with a
duration, tags, and parent/child links. Traces are sent through the Agent to Datadog. The **service map**
draws services and their dependencies automatically from trace data; **trace search and analytics** lets
you filter traces by service, resource, status, latency, and tags to find slow or erroring requests; the
**service catalog** and per-service pages show latency (p50/p95/p99), throughput, and error rate. Unified
service tagging (`env`/`service`/`version`, Chapter 02) ties traces to metrics and logs. APM's job is to
show **where** time and errors go inside a request. This chapter teaches APM with hands-on walkthroughs.

## Design Considerations

**Instrument** every service (auto-instrumentation covers common frameworks; add custom spans for key
logic). Set **unified service tags** so traces correlate with metrics and logs. Use the **service map**
to see dependencies and the **trace search** to find slow/erroring requests. Track per-service **latency
percentiles** and **error rate**. Sample intelligently at scale (keep enough traces to diagnose without
overwhelming cost).

## Implementation and Automation

The labs reason about instrumentation, add a custom span, and analyze a slow trace — the APM skills the
exam validates.

## Validation and Troubleshooting

Confirm APM:

```text
Instrument: dd-trace lib (or OpenTelemetry) -> trace per request = tree of spans (unit of work)
Span: duration + tags + parent/child; sent via Agent to Datadog
Service map: services + dependencies from traces; trace search: filter by service/resource/latency/status
Per-service: p50/p95/p99 latency, throughput, error rate; unified tags correlate with metrics/logs
```

Common pitfalls: uninstrumented services appearing as **black holes** in the map; and no **unified service
tags**, so traces do not line up with metrics/logs.

## Security and Best Practices

Scrub sensitive data from spans (obfuscate query params/PII), scope APM keys, and sample to control cost.
APM observes your own applications. All work is authorized.

## Hands-On Lab

APM walkthroughs. **Shared prerequisites** — an app with `dd-trace` and the Agent (or the concepts,
modeled), `python3`. **Cost:** none.

### Lab 6.1 — Instrument an application

**Objective:** Turn on tracing.

```python
# Python: auto-instrument by running under ddtrace-run, with unified tags
# DD_ENV=prod DD_SERVICE=checkout DD_VERSION=1.4.2 ddtrace-run python app.py
from ddtrace import tracer

@tracer.wrap(service="checkout", resource="place_order")
def place_order(cart):
    # a traced unit of work; nested calls become child spans
    return charge(cart)
```

```text
# traces for 'checkout' now appear in APM with resource 'place_order'
```

**Expected result:** the service instrumented so each request produces a trace tagged `env/service/
version`.

**Negative test:** leave a downstream service uninstrumented; it becomes a **black hole** in the service
map — instrument it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Add a custom span

**Objective:** Time a specific operation.

```python
from ddtrace import tracer

def compute_pricing(cart):
    with tracer.trace("pricing.compute", service="checkout") as span:
        span.set_tag("cart.items", len(cart))
        result = expensive_pricing(cart)
        span.set_tag("pricing.result", result)
        return result
```

```text
# a 'pricing.compute' span nested under the request trace, with tags
```

**Expected result:** a custom span timing the pricing logic with useful tags — visibility into a specific
operation.

**Negative test:** guess which internal step is slow with no custom spans; add a **span** around the
suspect logic.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Analyze a slow trace

**Objective:** Find where time goes.

```python
python3 - <<'PY'
spans = [
  ("web.request", 820),
  ("  auth.check", 15),
  ("  pricing.compute", 40),
  ("  db.query orders", 700),   # dominates
  ("  render", 65),
]
for name, ms in spans: print(f"{name:22} {ms:>4} ms")
print("Bottleneck: db.query orders (700/820 ms) -> optimize the query / add an index")
PY
```

**Expected result:** the span breakdown identifying the database query as the bottleneck — APM pinpoints
the slow step.

**Negative test:** conclude "the app is slow" from a single latency number; the **trace** shows the slow
**span**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Search traces by criteria

**Objective:** Find erroring/slow requests.

```python
python3 - <<'PY'
query = 'service:checkout status:error duration:>1s'
print("Trace search query:", query)
print("Returns: error traces on checkout slower than 1s -> triage the common resource/endpoint")
PY
```

**Expected result:** a trace-search query isolating slow error traces on the service — targeted triage.

**Negative test:** scroll all traces hoping to spot problems; **search** by service/status/duration/tags.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Datadog APM instruments applications (dd-trace or OpenTelemetry) to capture traces — trees of spans —
that build a service map of dependencies, expose per-service latency percentiles and error rate, and are
searchable by service, status, latency, and tags to pinpoint the slow or erroring span, all correlated
with metrics and logs through unified service tagging.

- [ ] I can instrument an application for APM.
- [ ] I can add a custom span.
- [ ] I can analyze a slow trace.
- [ ] I can search traces by criteria.
- [ ] I completed Labs 6.1–6.4 including each negative test.
