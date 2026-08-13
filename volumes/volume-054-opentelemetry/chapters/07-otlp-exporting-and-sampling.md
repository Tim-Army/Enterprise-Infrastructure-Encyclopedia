# Chapter 07: OTLP, Exporting, and Sampling

## Learning Objectives

- Explain OTLP transports and endpoints.
- Configure exporters from the SDK.
- Apply head sampling in the SDK.
- Apply tail sampling in the Collector.
- Complete a walkthrough for each concept.

## Theory and Architecture

**OTLP** (OpenTelemetry Protocol) is the native wire format, over **gRPC** (port 4317)
or **HTTP/protobuf** (port 4318). SDK **exporters** send signals over OTLP to a Collector
or backend; batching and retry live in the SDK/Collector. **Sampling** controls volume:
**head sampling** decides at span start (in the SDK) — e.g., `ParentBased(TraceIdRatio)`
keeps a fixed fraction and honors upstream decisions; **tail sampling** decides after a
trace completes (in the Collector) — e.g., keep all error traces and slow traces, sample
the rest. Head is cheap but blind to outcome; tail is outcome-aware but needs the whole
trace buffered.

## Design Considerations

Use **gRPC** OTLP for efficiency, **HTTP** where gRPC is awkward (browsers, some
proxies). For sampling, use **head** (ParentBased ratio) for simple cost control, and
**tail sampling in the Collector** when you must keep errors/slow traces regardless of
rate.

## Implementation and Automation

The labs configure OTLP exporters and both sampling strategies.

## Validation and Troubleshooting

Confirm the model:

```text
OTLP: gRPC :4317 / HTTP :4318 (protobuf). Exporter: SDK/Collector sends over OTLP.
Head sampling (SDK): decide at start (ParentBased + TraceIdRatio).
Tail sampling (Collector): decide after trace completes (keep errors/slow).
```

Common pitfalls: head-sampling away all error traces; and tail sampling without enough
buffer memory.

## Security and Best Practices

Prefer **gRPC OTLP** with **TLS + auth**, use **ParentBased** head sampling to keep
traces consistent across services, and add **tail sampling** in the Collector to always
retain errors/slow traces. Size the tail-sampling buffer for peak trace rate.

## Hands-On Lab

Export/sampling walkthroughs. **Shared prerequisites** — Python SDK; a running Collector.
**Cost:** none.

### Lab 7.1 — Configure an OTLP exporter

**Objective:** Export spans over OTLP/HTTP.

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
tp = TracerProvider()
tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")))
```

**Expected result:** the SDK exporting spans to the Collector over **OTLP/HTTP** — the
export path.

**Negative test:** point the gRPC exporter at the HTTP port (4318); use the **matching
transport/port** (gRPC→4317).

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Head sampling (ratio)

**Objective:** Keep a fixed fraction of traces at the source.

```python
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
tp = TracerProvider(sampler=ParentBased(root=TraceIdRatioBased(0.10)))  # ~10%
```

**Expected result:** roughly **10%** of root traces sampled, with children honoring the
parent — head sampling.

**Negative test:** use a bare ratio (not ParentBased); child services make **inconsistent**
decisions — use ParentBased.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Tail sampling (Collector)

**Objective:** Keep all error/slow traces, sample the rest.

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - { name: errors, type: status_code, status_code: { status_codes: [ERROR] } }
      - { name: slow, type: latency, latency: { threshold_ms: 500 } }
      - { name: sample-rest, type: probabilistic, probabilistic: { sampling_percentage: 10 } }
```

**Expected result:** **100% of errors and slow traces** kept, ~10% of the rest —
outcome-aware sampling.

**Negative test:** head-sample at 10% only; you **lose 90% of errors** — add tail
sampling for the ones that matter.

**Rollback:** remove the processor.

### Lab 7.4 — Export to a backend

**Objective:** Add a backend OTLP exporter in the Collector.

```yaml
exporters:
  otlp/vendor: { endpoint: "otel-backend:4317", tls: { insecure: false }, headers: { "api-key": "${env:API_KEY}" } }
# add otlp/vendor to the traces pipeline exporters
```

**Expected result:** traces delivered to the backend over **authenticated OTLP** — the
production export.

**Negative test:** hard-code the API key in config; use **`${env:...}`** so secrets stay
out of the file.

**Rollback:** remove the exporter.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OTLP carries signals over gRPC/HTTP to Collectors and backends; sampling controls volume
via head sampling (SDK, ParentBased ratio) and tail sampling (Collector, keep errors/slow).
This chapter configured exporters and both sampling strategies.

- [ ] I can configure OTLP exporters with the right transport.
- [ ] I can apply ParentBased head sampling.
- [ ] I can configure tail sampling to keep errors/slow traces.
- [ ] I can export to a backend with secrets from env.
- [ ] I completed Labs 7.1–7.4 including each negative test.
