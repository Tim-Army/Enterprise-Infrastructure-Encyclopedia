# Chapter 01: Introduction and Architecture

## Learning Objectives

- Explain what OpenTelemetry is and the problem it solves.
- Identify the signals: traces, metrics, logs, and profiles.
- Describe the architecture: API/SDK, the Collector, and OTLP.
- Run a Collector and send it telemetry.
- Verify component versions.

## Theory and Architecture

**OpenTelemetry (OTel)** is the **CNCF** vendor-neutral framework and standard for
generating, collecting, and exporting **telemetry** — a single set of APIs, SDKs, and
tools so you instrument once and send data to any backend. It solves vendor lock-in and
fragmentation across observability tools. OTel defines **signals**: **traces** (request
flow), **metrics** (aggregated measurements), **logs** (events), and the newer
**profiles** (continuous profiling).

The pieces fit together as: the **API** (what your code calls), the **SDK** (the
implementation that samples, batches, and exports, per language), the **OTLP** protocol
(OpenTelemetry Protocol — the wire format over gRPC/HTTP), and the **Collector** (a
standalone service that receives, processes, and exports telemetry). Cross-cutting
concerns are **context propagation** (linking spans across services) and **semantic
conventions** (standard attribute names). Components version independently — the
Collector is at **v0.157.0**, the spec at **v1.59.0**.

## Design Considerations

Instrument with the **API** (stable, decoupled from any vendor), let the **SDK** handle
export, and prefer sending through a **Collector** rather than exporting directly from
apps — the Collector centralizes processing (batching, filtering, redaction) and
decouples apps from backends.

## Implementation and Automation

Run a Collector with Docker and send it telemetry:

```bash
docker run --rm -p 4317:4317 -p 4318:4318 \
  -v "$PWD/otelcol.yaml:/etc/otelcol/config.yaml" \
  otel/opentelemetry-collector-contrib:latest
```

## Validation and Troubleshooting

Confirm the framework facts:

```text
OpenTelemetry (CNCF):
  - signals: traces, metrics, logs, profiles
  - API (call site) + SDK (implementation) + OTLP (wire) + Collector (service)
  - OTLP ports: 4317 (gRPC), 4318 (HTTP)
  - semantic conventions standardize attribute names
```

Common pitfalls: exporting directly from every app (no central processing); and mixing
**API** and **SDK** versions incorrectly.

## Security and Best Practices

Instrument to the **API**, route through a **Collector** for central control, secure
**OTLP** with TLS and auth, and follow **semantic conventions** so data is portable.
Redact sensitive attributes in the Collector, not the app.

## References and Knowledge Checks

- opentelemetry.io/docs: the specification, signals, SDKs, and the Collector.

**Knowledge checks**

1. What problem does OpenTelemetry solve?
2. Name the four signals.
3. Why route telemetry through a Collector?

## Hands-On Lab

Setup and orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — Docker;
`curl`, `python3`. **Cost:** none.

### Lab 1.1 — Run a Collector

**Objective:** Start a Collector with a minimal pipeline.

```bash
cat > otelcol.yaml <<'YAML'
receivers: { otlp: { protocols: { http: { endpoint: 0.0.0.0:4318 }, grpc: { endpoint: 0.0.0.0:4317 } } } }
exporters: { debug: { verbosity: detailed } }
service: { pipelines: { traces: { receivers: [otlp], exporters: [debug] } } }
YAML
docker run -d --name otelcol -p 4317:4317 -p 4318:4318 \
  -v "$PWD/otelcol.yaml:/etc/otelcol-contrib/config.yaml" \
  otel/opentelemetry-collector-contrib:latest
docker ps --filter name=otelcol --format '{{.Status}}'
```

**Expected result:** a **running Collector** listening on 4317/4318 — the telemetry
pipeline.

**Negative test:** send OTLP to a Collector that isn't running; the exporter gets
**connection refused** — start it first.

**Cleanup:** `docker rm -f otelcol`.

### Lab 1.2 — Send a trace over OTLP/HTTP

**Objective:** Post a span to the Collector.

```bash
curl -sS -X POST http://localhost:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans":[{"scopeSpans":[{"spans":[{"traceId":"5b8aa5a2d2c872e8321cf37308d69df2","spanId":"051581bf3cb55c13","name":"hello","kind":1,"startTimeUnixNano":"1","endTimeUnixNano":"2"}]}]}]}' \
  -w "\nHTTP %{http_code}\n"
```

**Expected result:** **HTTP 200** and the span printed in the Collector's debug log —
end-to-end OTLP ingestion.

**Negative test:** POST to `/v1/traces` with malformed protobuf/JSON; the Collector
rejects it (**4xx**) — match the OTLP schema.

**Cleanup:** none.

### Lab 1.3 — Verify component versions

**Objective:** Confirm the Collector version.

```bash
docker run --rm otel/opentelemetry-collector-contrib:latest --version
```

**Expected result:** a Collector **version string** (e.g., 0.157.x) — the running
component version.

**Negative test:** assume signals/features exist regardless of version; **check the
version** — OTel components evolve independently.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OpenTelemetry is the CNCF standard for telemetry — signals (traces, metrics, logs,
profiles) generated via the API/SDK, carried by OTLP, and processed by the Collector.
This chapter ran a Collector and sent it a trace over OTLP.

- [ ] I can explain OTel and the four signals.
- [ ] I can describe API vs SDK vs Collector vs OTLP.
- [ ] I can run a Collector with a pipeline.
- [ ] I can send telemetry over OTLP and verify the version.
- [ ] I completed Labs 1.1–1.3 including each negative test.
