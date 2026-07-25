# Chapter 02: Telemetry Architecture, Instrumentation, and Pipelines

![Lab topology for this chapter: a synthetic trace sent to the Collector's OTLP receiver is exported to Jaeger and confirmed via search, and a Prometheus counter confirms the span was accepted end to end. As a negative test, the Jaeger container is stopped and another trace is sent; the Collector still returns HTTP 200 to the sender rather than erroring, and the Collector's own self-telemetry shows the exporter's queue size growing nonzero with each additional send — the buffering-under-backpressure behavior. Restarting Jaeger drains the queue back toward zero within the configured retry interval.](../../../diagrams/volume-11-observability-enterprise-operations/chapter-02-otel-collector-backpressure-topology.svg)

*Figure 2-1. Topology used throughout this chapter's Hands-On Lab: an OpenTelemetry Collector pipeline exporting to Prometheus and Jaeger, tested against a Jaeger outage.*

## Learning Objectives

- Describe the OpenTelemetry architecture: API, SDK, Collector,
  instrumentation libraries, and the OTLP wire protocol.
- Differentiate automatic and manual instrumentation and select the
  appropriate mix for a given service.
- Explain context propagation using W3C Trace Context and Baggage, and why
  it is the mechanism that makes cross-service correlation possible.
- Design a Collector deployment topology (agent plus gateway) that scales
  to enterprise telemetry volume with backpressure and failure isolation.
- Apply sampling, cardinality control, and PII scrubbing at the pipeline
  layer rather than relying on every service team to do it independently.
- Diagnose common telemetry pipeline failures: dropped spans, queue
  saturation, and exporter backpressure.

## Theory and Architecture

### The OpenTelemetry model

OpenTelemetry (OTel) is the CNCF-graduated, vendor-neutral standard for
generating and transporting telemetry. It separates four concerns that
earlier proprietary agents bundled together:

- **API** — the language-level interface application code calls
  (`tracer.StartSpan`, `meter.Counter`, `logger.Emit`). Instrumented code
  depends only on the API, not on any specific backend.
- **SDK** — the language-level implementation of the API: sampling
  decisions, batching, resource attribution, and export configuration.
  Swapping the SDK's exporter changes where data goes without touching
  application code.
- **Instrumentation libraries** — pre-built API calls wired into common
  frameworks and clients (HTTP servers, gRPC, database drivers, message
  queues) so most call-graph telemetry requires no application code
  changes at all.
- **Collector** — a standalone binary that receives, processes, and
  exports telemetry. It decouples application processes from backend
  choice and backend availability.

Telemetry travels over **OTLP** (OpenTelemetry Protocol), a gRPC or
HTTP/protobuf wire format with defined schemas for metrics, traces, and
logs. OTLP is the common language that lets a Java service's traces, a Go
service's metrics, and an Nginx access log converge on the same pipeline.

### Automatic versus manual instrumentation

Automatic instrumentation (language agents or auto-instrumentation
packages, such as `opentelemetry-instrument` for Python or the Java agent
`-javaagent` flag) intercepts common libraries at load time and emits spans
and metrics with no source changes. It covers HTTP inbound/outbound, common
database clients, and message queue clients — the call graph's skeleton.
Manual instrumentation adds spans, attributes, and events for
business-meaningful units of work the framework cannot infer: "validated
loyalty tier," "cache stampede guard triggered," or a custom span around a
specific algorithm.

The correct mix in an enterprise paved road is: automatic instrumentation
mandatory by default (delivered via the platform team's base container
image or sidecar so individual teams do not opt out silently), manual
instrumentation added by service owners for business-critical logic.
Auto-instrumentation alone typically covers 70-80 percent of what an
incident investigation needs; the remaining 20-30 percent — the "why," not
just the "what and when" — comes from manual spans and attributes that
require domain knowledge no agent has.

### Semantic conventions

OpenTelemetry defines semantic conventions: standardized attribute names
(`http.request.method`, `db.system.name`, `service.name`,
`deployment.environment.name`) so a dashboard or query written against one
service's telemetry works against any other service that follows the same
convention. Deviating from semantic conventions — using `svc` instead of
`service.name`, or `env` instead of `deployment.environment.name` — breaks
the paved road's shared dashboards and alert templates for every team that
deviates, silently, until an incident investigation discovers the gap.
Enforce semantic conventions at the Collector (reject or relabel
non-conforming attributes) rather than only in documentation.

### Context propagation

A trace spans multiple processes and, usually, multiple services. Context
propagation is the mechanism that carries a trace's identity across that
boundary. The W3C **Trace Context** specification defines the `traceparent`
HTTP header (`00-<trace-id>-<span-id>-<flags>`) and the optional
`tracestate` header for vendor-specific extensions. **Baggage** (a separate
W3C specification) propagates arbitrary key-value context — a tenant ID or
a feature-flag variant — alongside the trace, so downstream services can
read it without a separate lookup.

Context propagation is the single most fragile part of a telemetry
architecture: any hop that does not forward the incoming `traceparent`
header (an undocumented internal proxy, a message queue that does not
carry headers into the message body, a batch job that reads from a queue
asynchronously) breaks the trace into disconnected fragments. [Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md)
covers diagnosing and repairing broken propagation in depth.

### Pipeline topology: agent and gateway

At enterprise scale, application processes do not export telemetry
directly to a backend. Two Collector deployment patterns compose into the
standard topology:

- **Agent (node-level).** One Collector instance per host or per
  Kubernetes node (a DaemonSet), receiving telemetry from local processes
  over `localhost`. It performs cheap, local processing: batching,
  resource attribute enrichment (node name, availability zone), and
  immediate local buffering against transient backend unavailability.
- **Gateway (cluster- or region-level).** A smaller number of Collector
  instances, deployed as a scalable service (a Kubernetes Deployment behind
  a load balancer), that agents forward to. The gateway performs
  expensive, centralized processing: tail-based sampling ([Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md)),
  PII redaction, cardinality limiting, and fan-out to multiple backends
  (a metrics backend, a trace backend, and a long-term archive, for
  example).

```text
[ app process ] --OTLP/grpc--> [ node agent Collector ] --OTLP/grpc--> [ gateway Collector ] --> [ backends ]
                                       (DaemonSet)                        (Deployment, HPA-scaled)
```

This topology isolates failure domains: a gateway outage degrades to local
agent buffering (bounded by the agent's queue size) rather than blocking
application request paths, and centralized processing logic (redaction,
sampling policy) lives in one place instead of every service's SDK
configuration.

## Design Considerations

- **Push versus pull.** OTLP is push-based: the SDK or agent sends data to
  the next hop. Prometheus's native model is pull-based: the server scrapes
  a `/metrics` endpoint on an interval. Both are valid; an OTel Collector
  can bridge them (a `prometheus` receiver scrapes targets and converts to
  OTLP internally, and a `prometheus` exporter serves scraped-style output
  from OTLP data). Choose pull for infrastructure metrics where a stable
  scrape target exists and push for ephemeral or short-lived workloads
  (serverless functions, batch jobs) that may not live long enough to be
  scraped.
- **Cardinality budget.** Every unique combination of label/attribute
  values on a metric creates a new time series; every unique combination on
  span attributes inflates trace storage and query cost. Set an explicit
  per-service cardinality budget (for example, no unbounded values such as
  raw user ID or full URL with query string as a metric label) and enforce
  it at the Collector with a cardinality-limiting processor, because
  documentation-only limits get violated under deadline pressure.
  Cardinality mistakes are the leading cause of both a metrics backend
  falling over and an unexpected telemetry bill.
- **Sampling strategy.** Full-fidelity trace capture is rarely affordable
  at enterprise request volume. Head-based sampling (a decision made at
  trace start, typically probabilistic) is cheap but risks discarding the
  rare high-value trace (a slow outlier or an error). Tail-based sampling
  (a decision made after the full trace completes, retaining error traces
  and slow traces at a higher rate than routine ones) is more valuable but
  requires buffering the full trace at the gateway before deciding,
  increasing gateway memory and requiring all spans of a trace to reach the
  same gateway instance. [Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md) details tail-based sampling
  configuration.
- **Backpressure and buffering.** Decide, per signal type, what happens
  when the backend is unavailable or the pipeline is saturated: drop
  oldest, drop newest, or block the application. Blocking the application
  on telemetry export is rarely acceptable for a Tier 0 service — an
  observability outage should not become a product outage. Configure
  bounded queues with a drop policy and monitor the drop rate itself
  (self-telemetry, covered under Validation and Troubleshooting).
- **PII and sensitive data at the source.** Redact or exclude sensitive
  attributes (authorization headers, full request bodies, government
  identifiers) at the SDK or agent, not only at the gateway — data that
  crosses a network boundary before redaction has already left the trust
  boundary for compliance purposes in many regulatory regimes.
- **Vendor neutrality as a design goal, not just a preference.** Because
  OTLP is a wire-format standard, the choice of backend (self-hosted
  Prometheus/Tempo/Loki stack versus a commercial SaaS platform) becomes
  a Collector exporter configuration change, not an instrumentation
  rewrite. Preserve this by never adding vendor-proprietary SDKs directly
  into application code; route everything through the OTel API and let the
  Collector own backend selection.

### Tool versions referenced in this chapter

Observability tooling is not yet listed in the repository-wide
`SOFTWARE_VERSIONS.md` baseline. The examples in this volume were written
and validated against the dated baseline below; treat it the same way the
rest of the encyclopedia treats `SOFTWARE_VERSIONS.md` — as a snapshot, not
a timeless reference.

| Component | Version | Baseline Date |
| --- | --- | --- |
| OpenTelemetry Collector (Contrib distribution) | 0.116.x | 2026-07 |
| OpenTelemetry Semantic Conventions | 1.29.x | 2026-07 |
| Prometheus | 3.x | 2026-07 |
| Grafana Tempo | 2.6.x | 2026-07 |
| Grafana Loki | 3.2.x | 2026-07 |
| Grafana | 11.x | 2026-07 |

## Implementation and Automation

The following Collector configuration implements the agent role: it
receives OTLP from local application processes, enriches with resource
attributes, batches, and forwards to a gateway with a bounded retry queue.

```yaml
# otel-agent-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 512
  resourcedetection:
    detectors: [env, system]
    system:
      hostname_sources: [os]
  attributes/redact:
    actions:
      - key: http.request.header.authorization
        action: delete
      - key: user.email
        action: delete

exporters:
  otlp/gateway:
    endpoint: otel-gateway.observability.svc:4317
    tls:
      insecure: false
      ca_file: /etc/otel/certs/ca.pem
    sending_queue:
      enabled: true
      num_consumers: 4
      queue_size: 5000
    retry_on_failure:
      enabled: true
      initial_interval: 1s
      max_interval: 30s
      max_elapsed_time: 300s

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [resourcedetection, attributes/redact, batch]
      exporters: [otlp/gateway]
    metrics:
      receivers: [otlp]
      processors: [resourcedetection, batch]
      exporters: [otlp/gateway]
    logs:
      receivers: [otlp]
      processors: [resourcedetection, attributes/redact, batch]
      exporters: [otlp/gateway]
  telemetry:
    metrics:
      level: detailed
      address: 0.0.0.0:8888
```

Manual instrumentation example (Python, using the OTel SDK API directly
for a business-meaningful span and attribute):

```python
from opentelemetry import trace

tracer = trace.get_tracer("checkout-api")

def apply_loyalty_discount(cart, customer):
    with tracer.start_as_current_span("apply_loyalty_discount") as span:
        span.set_attribute("loyalty.tier", customer.tier)
        span.set_attribute("cart.item_count", len(cart.items))
        discount = compute_discount(cart, customer)
        span.set_attribute("discount.amount_minor_units", discount.amount)
        if discount.amount == 0 and customer.tier != "standard":
            span.add_event("loyalty_discount_not_applied_unexpectedly")
        return discount
```

Note `discount.amount_minor_units` (an integer count of cents, not raw
currency float) and `loyalty.tier` (a small enum, not a customer ID) —
both chosen deliberately to stay within the service's cardinality budget
and avoid emitting a value that could itself be sensitive.

Enforce semantic conventions and cardinality budgets centrally with a
gateway-side processor:

```yaml
# excerpt: gateway processors enforcing conventions and cardinality
processors:
  transform/enforce_conventions:
    metric_statements:
      - context: datapoint
        statements:
          - set(attributes["deployment.environment.name"], "unknown") where attributes["deployment.environment.name"] == nil
  filter/cardinality_guard:
    metrics:
      datapoint:
        - 'IsMatch(attributes["http.route"], ".*[0-9]{5,}.*")'  # drop unbounded ID-in-path labels
```

## Validation and Troubleshooting

- **Collector self-telemetry.** Every Collector exposes its own internal
  metrics on the `telemetry.metrics.address` (`:8888` above), including
  `otelcol_exporter_send_failed_spans`, `otelcol_exporter_queue_size`, and
  `otelcol_processor_dropped_spans`. Scrape these like any other service's
  metrics and alert on sustained queue growth or a nonzero sustained drop
  rate — a silent pipeline drop is worse than an obvious outage because
  dashboards keep rendering, just with gaps no one notices until an
  investigation needs the missing data.
- **Symptom: traces have gaps between services.** Confirm the
  `traceparent` header is present on the outbound call from the upstream
  service (inspect with `curl -v` or a packet capture) and present on the
  inbound call to the downstream service. The most common cause is an
  internal load balancer, API gateway, or message broker that does not
  forward custom headers by default and requires explicit allow-listing.
- **Symptom: metrics cardinality explosion / backend rejecting writes.**
  Query `otelcol_processor_batch_batch_send_size` alongside the backend's
  own active-series count. Identify the offending metric by label
  combination count, not just total series count, and check whether a
  recent deploy added a new label sourced from unbounded input (a raw path
  parameter, a session ID).
- **Symptom: application latency increased after adding instrumentation.**
  Check whether the SDK is configured for synchronous export (blocking the
  request thread) instead of the default batched, asynchronous export.
  Auto-instrumentation defaults are safe; a manual SDK configuration
  override that disables batching is the most common self-inflicted cause.
- **Backend availability test.** Deliberately point an agent Collector's
  gateway exporter at an unreachable endpoint (a `TEST` procedure, not
  production) and confirm the queue fills, retries occur per the configured
  backoff, and the application's own request latency is unaffected — this
  is the core backpressure-isolation guarantee the agent/gateway topology
  exists to provide, and it should be tested, not assumed.

## Security and Best Practices

- Enforce TLS (and mTLS where the network path crosses a trust boundary,
  such as agent-to-gateway across availability zones or a cloud
  interconnect) on every Collector receiver and exporter; telemetry
  frequently contains information sensitive enough to be a target in its
  own right (internal hostnames, request paths, error messages that may
  echo user input).
- Redact known-sensitive attribute keys (`authorization`, `cookie`,
  `set-cookie`, common PII field names) at the earliest possible hop — the
  SDK or the node agent — rather than only at the gateway, per the Design
  Considerations note above.
- Restrict who can modify Collector processor configuration in production;
  a redaction processor removed from a pipeline is a data-exposure
  incident, not a cosmetic configuration change, and should be change-
  controlled and reviewed like any other security control (see [Chapter 07](07-service-management-incident-problem-and-change-operations.md)
  for change-management process).
- Do not run Collector instances with broader network egress than
  required — the gateway needs a defined allow-list of backend
  destinations, not unrestricted outbound access, to limit the blast
  radius if a Collector is ever compromised.
- Rotate and scope credentials used for backend exporters (API keys,
  mTLS client certificates) per environment, and store them in a secrets
  manager referenced by the Collector configuration rather than committed
  alongside the YAML.

## References and Knowledge Checks

**References**

- [CNCF OpenTelemetry documentation and specification, `opentelemetry.io`.](https://opentelemetry.io/docs/)
- [W3C Trace Context Recommendation and W3C Baggage specification,
  `w3.org/TR/trace-context/` and the associated Baggage draft.](https://www.w3.org/TR/trace-context/)
- [OpenTelemetry Collector Contrib repository documentation for receiver,
  processor, and exporter reference configuration.](https://github.com/open-telemetry/opentelemetry-collector-contrib)
- [Prometheus documentation, `prometheus.io/docs`, for the pull-based
  scrape model referenced in Design Considerations.](https://prometheus.io/docs/)

**Knowledge Checks**

1. Explain the difference between the OTel API and the OTel SDK, and why
   application code should depend only on the API.
2. Why does tail-based sampling require buffering an entire trace at a
   single Collector instance, and what does that imply for gateway sizing?
3. A downstream service's spans never appear connected to the calling
   service's trace. List two likely root causes and how you would confirm
   each.
4. Why should PII redaction happen at the SDK or agent rather than only at
   the gateway?
5. What is the operational risk of configuring an application's telemetry
   export as synchronous/blocking rather than batched and asynchronous?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each telemetry-pipeline skill** — OpenTelemetry
instrumentation, the Collector pipeline, signal correlation, and sampling/cardinality control. Every
step is a runnable config/command. Each ends **`**Lab verified by:** *pending*`** until a human runs
it.

**Shared prerequisites for Labs 2.1–2.4** — a lab app to instrument (or the OpenTelemetry demo), the
OpenTelemetry Collector, and a metrics/trace backend (Prometheus + Tempo). **Cost:** none.

### Lab 2.1 — Instrument an application with OpenTelemetry (Topic: Instrumentation)

**Objective:** Emit a metric and a trace from application code.

```python
# Python example (otel SDK): a counter + a span
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
meter = metrics.get_meter("checkout")
orders = meter.create_counter("orders_total")
tracer = trace.get_tracer("checkout")
with tracer.start_as_current_span("place_order"):
    orders.add(1, {"result": "ok"})
# Run with: OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 python app.py
```

**Expected result:** the app exports an `orders_total` metric and a `place_order` span over OTLP to
the Collector — OpenTelemetry is the vendor-neutral instrumentation standard, so one SDK/API emits
metrics, traces, and logs to any compatible backend, avoiding per-vendor agents.

**Negative test:** hard-code a vendor-specific agent/SDK into the app; switching backends means
re-instrumenting everything — OTel's vendor-neutral API is what keeps instrumentation portable.

**Cleanup:** none.

### Lab 2.2 — The OpenTelemetry Collector pipeline (Topic: Pipelines)

**Objective:** Route telemetry through receivers, processors, and exporters.

```yaml
# otel-collector.yaml
receivers:
  otlp: { protocols: { grpc: { endpoint: 0.0.0.0:4317 } } }
processors:
  batch: {}
  memory_limiter: { check_interval: 1s, limit_percentage: 80 }
exporters:
  prometheus: { endpoint: 0.0.0.0:8889 }
  otlp/tempo: { endpoint: tempo:4317, tls: { insecure: true } }
service:
  pipelines:
    metrics: { receivers: [otlp], processors: [memory_limiter, batch], exporters: [prometheus] }
    traces:  { receivers: [otlp], processors: [memory_limiter, batch], exporters: [otlp/tempo] }
```

**Expected result:** metrics flow to Prometheus and traces to Tempo through one Collector, with
batching and memory limiting — the Collector decouples apps from backends (apps send to the
Collector, the Collector fans out), so you change backends/processing centrally without touching
apps.

**Negative test:** export directly from every app to every backend; changing a backend means
reconfiguring every app, and there is no central place to batch/filter/enrich — the Collector is the
control point that avoids that.

**Cleanup:** stop the lab Collector.

### Lab 2.3 — Correlate metrics, logs, and traces (Topic: Signal correlation)

**Objective:** Link the three signals by trace and exemplar.

```text
# Ensure the pipeline propagates correlation IDs:
#   - logs include trace_id/span_id (structured logging with the active span context)
#   - metrics carry exemplars (a sample metric point links to a trace_id)
#   - traces carry service.name and resource attributes matching metric/log labels
# In Grafana: click a spike on a metric exemplar -> jump to the trace -> jump to that trace's logs.
```

**Expected result:** a single trace_id ties a metric spike to its exact trace and that trace's logs,
so you pivot metric→trace→log in one click — correlation is what collapses "which of a thousand
requests was slow" into one, turning three separate data stores into one investigation.

**Negative test:** collect metrics, logs, and traces with no shared IDs; you cannot connect a metric
spike to the specific trace/log that caused it — correlation IDs (trace_id in logs, exemplars on
metrics) are the linkage that makes the pillars work together.

**Cleanup:** none.

### Lab 2.4 — Sampling and cardinality control (Topic: Data volume)

**Objective:** Control telemetry cost without losing signal.

```yaml
# Tail-based sampling (keep all errors + slow traces, sample the rest) in the Collector:
processors:
  tail_sampling:
    policies:
      - { name: errors, type: status_code, status_code: { status_codes: [ERROR] } }
      - { name: slow, type: latency, latency: { threshold_ms: 500 } }
      - { name: sample-rest, type: probabilistic, probabilistic: { sampling_percentage: 10 } }
```

**Expected result:** all error and slow traces are kept while normal traces are sampled to 10%, and
high-cardinality labels are dropped/aggregated — telemetry volume (and cost) is dominated by traces
and label cardinality, so tail-sampling and cardinality limits keep the signal (errors, slow paths)
while cutting the noise.

**Negative test:** keep 100% of traces and every high-cardinality label (user_id, request_id) as a
metric dimension; storage and cost explode and Prometheus struggles — sampling and cardinality
control are what make observability affordable at scale.

**Cleanup:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The OpenTelemetry API/SDK/Collector split, OTLP as a common wire format,
and W3C context propagation together make cross-service correlation
possible without vendor lock-in. An agent-plus-gateway pipeline topology
isolates application processes from backend availability and centralizes
expensive processing (sampling, redaction, cardinality control). The next
chapter builds on this pipeline to define metrics, SLIs, SLOs, and error
budgets; Chapters 04 and 05 build on it for logs and traces specifically.

**Completion checklist**

- [ ] Can explain the OTel API/SDK/Collector separation and why
      application code should depend only on the API.
- [ ] Can describe W3C Trace Context propagation and diagnose a broken
      propagation hop.
- [ ] Can design an agent/gateway Collector topology and justify the
      failure-isolation benefit.
- [ ] Deployed a working local telemetry pipeline and verified end-to-end
      trace and metric delivery.
- [ ] Demonstrated and explained backpressure/queue behavior during a
      simulated backend outage.
