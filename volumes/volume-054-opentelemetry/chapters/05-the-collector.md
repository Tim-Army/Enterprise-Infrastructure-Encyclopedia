# Chapter 05: The Collector

## Learning Objectives

- Explain the Collector's pipeline model.
- Configure receivers, processors, exporters, and connectors.
- Build multi-signal pipelines.
- Distinguish the core and contrib distributions.
- Complete a walkthrough for each Collector component.

## Theory and Architecture

The **OpenTelemetry Collector** is a standalone service that **receives**, **processes**,
and **exports** telemetry. Its config is built from components wired into **pipelines**
(one per signal): **receivers** (ingest — OTLP, filelog, hostmetrics, prometheus),
**processors** (transform — batch, memory_limiter, attributes, filter, redaction),
**exporters** (send — OTLP, prometheus, backends), and **connectors** (link pipelines —
e.g., spanmetrics turns traces into metrics). The **contrib** distribution bundles many
community components; **core** is minimal.

## Design Considerations

Always include **memory_limiter** and **batch** processors. Use **processors** for
central concerns (redaction, sampling, attribute normalization) so apps stay simple.
Use **connectors** to derive signals (spanmetrics, servicegraph). Pick **contrib** when
you need a component not in core.

## Implementation and Automation

The labs build pipelines with receivers, processors, exporters, and a connector.

## Validation and Troubleshooting

Confirm the model:

```text
Pipeline (per signal) = receivers -> processors -> exporters.
Connectors bridge pipelines (traces -> metrics via spanmetrics).
Always add memory_limiter + batch. contrib bundles extra components.
```

Common pitfalls: no **memory_limiter** (OOM under load); and processor **order** wrong
(batch before memory_limiter).

## Security and Best Practices

Add **memory_limiter** first and **batch** last, **redact** sensitive attributes in a
processor, secure receivers/exporters with TLS+auth, and validate config before rollout.
Keep the Collector's own health monitored.

## Hands-On Lab

Collector walkthroughs. **Shared prerequisites** — Docker; the contrib Collector image.
**Cost:** none.

### Lab 5.1 — Validate a config

**Objective:** Check a Collector config is valid.

```bash
cat > col.yaml <<'YAML'
receivers: { otlp: { protocols: { http: {}, grpc: {} } } }
processors: { memory_limiter: { check_interval: 1s, limit_mib: 256 }, batch: {} }
exporters: { debug: {} }
service:
  pipelines:
    traces: { receivers: [otlp], processors: [memory_limiter, batch], exporters: [debug] }
YAML
docker run --rm -v "$PWD/col.yaml:/c.yaml" \
  otel/opentelemetry-collector-contrib:latest validate --config /c.yaml && echo VALID
```

**Expected result:** **VALID** — the config parses and components resolve.

**Negative test:** reference a receiver you didn't define in a pipeline; `validate`
**errors** — fix references before deploy.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Add an attributes processor (redaction)

**Objective:** Redact a sensitive attribute centrally.

```yaml
processors:
  attributes/redact:
    actions: [ { key: "user.email", action: delete } ]
# add attributes/redact to the pipeline's processors list
```

**Expected result:** `user.email` **removed** from telemetry in the Collector — central
redaction.

**Negative test:** redact in every app; do it **once in the Collector** so all apps are
covered.

**Rollback:** remove the processor.

### Lab 5.3 — Add an exporter

**Objective:** Export to a second destination.

```yaml
exporters:
  otlp/backend: { endpoint: backend:4317, tls: { insecure: true } }
# add otlp/backend to the pipeline's exporters list (fan-out to debug + backend)
```

**Expected result:** telemetry **fanned out** to both debug and the OTLP backend — the
export path.

**Negative test:** export straight from apps to the backend; the **Collector exporter**
decouples apps from backends — route through it.

**Rollback:** remove the exporter.

### Lab 5.4 — Use the spanmetrics connector

**Objective:** Derive metrics from traces.

```yaml
connectors: { spanmetrics: {} }
service:
  pipelines:
    traces: { receivers: [otlp], exporters: [spanmetrics] }
    metrics: { receivers: [spanmetrics], exporters: [debug] }
```

**Expected result:** **RED metrics** (rate/errors/duration) generated from spans — a
connector bridging pipelines.

**Negative test:** instrument separate metrics for request rate/latency you already
trace; **spanmetrics** derives them from spans — reuse.

**Rollback:** remove the connector.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Collector wires receivers → processors → exporters into per-signal pipelines, with
connectors bridging pipelines. This chapter validated a config, added redaction and an
exporter, and derived metrics from traces with spanmetrics.

- [ ] I can validate a Collector config.
- [ ] I can redact attributes with a processor.
- [ ] I can fan out to multiple exporters.
- [ ] I can derive metrics from traces via a connector.
- [ ] I completed Labs 5.1–5.4 including each negative test.
