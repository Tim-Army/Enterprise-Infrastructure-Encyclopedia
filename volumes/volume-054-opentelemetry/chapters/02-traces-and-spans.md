# Chapter 02: Traces and Spans

## Learning Objectives

- Explain traces, spans, and the span hierarchy.
- Create spans with the SDK and add attributes/events.
- Propagate context across function and service boundaries.
- Set span status and record exceptions.
- Complete a walkthrough for each tracing concept.

## Theory and Architecture

A **trace** represents one request's journey; it is a tree of **spans**, each a timed
operation with a name, **span kind** (server/client/internal/producer/consumer),
**attributes**, **events**, **status**, and links. Spans share a **trace ID** and nest
via **parent span IDs**. **Context propagation** carries the active span across function
calls (in-process) and across services (via headers like `traceparent`, the W3C Trace
Context standard) so a distributed request forms a single trace.

## Design Considerations

Name spans by **operation** (not by unique values), attach **attributes** using semantic
conventions, record **events** for notable points, and set **status** to Error on
failures. Keep cardinality sane — attributes on spans, not high-cardinality data in span
names.

## Implementation and Automation

The labs use the Python SDK to create spans, nest them, add attributes/events, and
propagate context.

## Validation and Troubleshooting

Confirm the model:

```text
Trace (trace_id) = tree of Spans (parent span_id). Span: name, kind, attributes,
events, status, links. Propagation: W3C traceparent header across services.
```

Common pitfalls: unique values in **span names** (cardinality blowup); and lost
**context** (spans appear as separate traces).

## Security and Best Practices

Use **semantic-convention** attribute names, keep span names low-cardinality, set
**Error status** and **record exceptions**, and ensure **context propagates** so
distributed requests stay one trace. Avoid putting secrets in attributes.

## Hands-On Lab

Tracing walkthroughs. **Shared prerequisites** — Python with `pip install
opentelemetry-sdk opentelemetry-exporter-otlp`; a running Collector (Chapter 01).
**Cost:** none.

### Lab 2.1 — Create a span

**Objective:** Emit a single span with the SDK.

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
tracer = trace.get_tracer("demo")
with tracer.start_as_current_span("checkout"):
    pass
```

**Expected result:** a **"checkout" span** printed to the console — a trace with one
span.

**Negative test:** name the span `checkout-order-98213` (unique id); use a **stable
operation name** and put the id in an attribute.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Nest spans

**Objective:** Create a parent/child span hierarchy.

```python
with tracer.start_as_current_span("checkout"):
    with tracer.start_as_current_span("charge-card"):
        with tracer.start_as_current_span("call-gateway"):
            pass
```

**Expected result:** three spans sharing a **trace ID**, nested by parent — the span
tree.

**Negative test:** start child spans without the parent as current; they become
**siblings/roots** — nest within the active context.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Attributes, events, and status

**Objective:** Enrich a span and mark an error.

```python
from opentelemetry.trace import Status, StatusCode
with tracer.start_as_current_span("charge-card") as span:
    span.set_attribute("payment.amount", 42.0)
    span.add_event("gateway.request.sent")
    try:
        raise RuntimeError("declined")
    except Exception as e:
        span.record_exception(e); span.set_status(Status(StatusCode.ERROR))
```

**Expected result:** a span carrying an **attribute, event, recorded exception, and
Error status** — a diagnostic-rich span.

**Negative test:** swallow the exception silently; **record it + set Error status** so
the trace shows the failure.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Propagate context across a boundary

**Objective:** Inject and extract W3C trace context.

```python
from opentelemetry.propagate import inject, extract
carrier = {}
with tracer.start_as_current_span("client"):
    inject(carrier)                    # adds 'traceparent' to carrier
print("traceparent:", carrier.get("traceparent"))
ctx = extract(carrier)                 # server side reconstructs context
```

**Expected result:** a **`traceparent`** header carrying the trace context — the basis
of distributed tracing.

**Negative test:** call a downstream service without injecting context; its spans start a
**new trace** — propagate the header.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A trace is a tree of spans sharing a trace ID, enriched with attributes/events/status and
linked across services by W3C context propagation. This chapter created, nested,
enriched, and propagated spans with the SDK.

- [ ] I can create and nest spans.
- [ ] I can add attributes, events, and error status.
- [ ] I can record exceptions on spans.
- [ ] I can inject/extract W3C trace context.
- [ ] I completed Labs 2.1–2.4 including each negative test.
