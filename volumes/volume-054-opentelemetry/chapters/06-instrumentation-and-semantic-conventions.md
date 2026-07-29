# Chapter 06: Instrumentation and Semantic Conventions

## Learning Objectives

- Distinguish automatic (zero-code) from manual instrumentation.
- Apply zero-code instrumentation to an app.
- Follow semantic conventions for attribute names.
- Enrich telemetry with resource detection.
- Complete a walkthrough for each instrumentation approach.

## Theory and Architecture

**Instrumentation** is how telemetry gets generated. **Zero-code (automatic)**
instrumentation attaches to popular libraries/frameworks without changing source — via a
language agent (Java agent, Python `opentelemetry-instrument`, the Kubernetes Operator's
auto-injection). **Manual** instrumentation uses the SDK directly for custom spans/
metrics. **Semantic conventions** define standard attribute names (`http.request.method`,
`db.system`, `service.name`) so telemetry is portable across backends. **Resource
detection** auto-discovers environment attributes (host, container, cloud, process).

## Design Considerations

Start with **zero-code** for breadth (framework spans, HTTP/DB calls for free), then add
**manual** spans for business-specific operations. Always emit **semantic-convention**
attributes and enable **resource detectors** so telemetry self-identifies.

## Implementation and Automation

The labs use zero-code Python instrumentation, manual enrichment, and semantic-convention
checks.

## Validation and Troubleshooting

Confirm the approaches:

```text
Zero-code: agent/operator instruments libraries with no source changes.
Manual: SDK spans/metrics for custom logic. Combine both.
Semantic conventions: standard attribute names. Resource detectors: env attributes.
```

Common pitfalls: custom attribute names where a **convention** exists; and missing
`service.name` (telemetry unattributable).

## Security and Best Practices

Use **zero-code** for coverage and **manual** for business context, always follow
**semantic conventions**, enable **resource detection**, and keep instrumentation
versions aligned with the SDK. Don't reinvent attribute names.

## Hands-On Lab

Instrumentation walkthroughs. **Shared prerequisites** — Python; a running Collector.
**Cost:** none.

### Lab 6.1 — Zero-code instrumentation

**Objective:** Auto-instrument a Python app without code changes.

```bash
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install
OTEL_SERVICE_NAME=checkout OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 \
  opentelemetry-instrument python app.py
```

**Expected result:** framework/HTTP/DB spans emitted **without editing `app.py`** — the
zero-code approach.

**Negative test:** hand-instrument every library call; **zero-code** covers popular
libraries automatically — start there.

**Cleanup:** none.

### Lab 6.2 — Add manual spans for business logic

**Objective:** Supplement auto-instrumentation with a custom span.

```python
from opentelemetry import trace
tracer = trace.get_tracer("app")
with tracer.start_as_current_span("apply-discount") as s:
    s.set_attribute("discount.code", "SUMMER")   # business-specific span
```

**Expected result:** a custom **"apply-discount"** span nested under auto-instrumented
spans — breadth plus business context.

**Negative test:** rely only on auto-instrumentation; **manual spans** capture
business operations the libraries can't see.

**Cleanup:** none.

### Lab 6.3 — Use semantic-convention attributes

**Objective:** Name attributes to the standard.

```python
with tracer.start_as_current_span("GET /orders", kind=trace.SpanKind.SERVER) as s:
    s.set_attribute("http.request.method", "GET")
    s.set_attribute("url.path", "/orders")
    s.set_attribute("http.response.status_code", 200)
```

**Expected result:** a span using **semantic-convention** HTTP attributes — portable,
backend-agnostic telemetry.

**Negative test:** invent `method`/`status`; backends expect **`http.request.method`**
etc. — follow the conventions.

**Cleanup:** none.

### Lab 6.4 — Enable resource detection

**Objective:** Auto-add environment attributes.

```bash
OTEL_RESOURCE_ATTRIBUTES="service.name=checkout,service.version=1.4.0" \
OTEL_EXPERIMENTAL_RESOURCE_DETECTORS="process,os,host" \
  opentelemetry-instrument python app.py
```

**Expected result:** telemetry carrying **host/os/process** resource attributes plus
service identity — self-describing signals.

**Negative test:** hard-code environment attributes; **resource detectors** discover them
per host — enable them.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Instrumentation combines zero-code (broad, no source changes) with manual SDK spans (for
business logic), all using semantic-convention attribute names and resource detection so
telemetry self-identifies. This chapter auto-instrumented, added manual context, and
applied conventions.

- [ ] I can apply zero-code instrumentation.
- [ ] I can add manual spans for business logic.
- [ ] I can use semantic-convention attributes.
- [ ] I can enable resource detection.
- [ ] I completed Labs 6.1–6.4 including each negative test.
