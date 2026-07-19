# Chapter 05: Distributed Tracing, Profiling, and Dependency Analysis

## Learning Objectives

- Describe the structural model of a distributed trace: spans, span
  kinds, parent-child relationships, and how a trace tree is assembled
  from independently emitted spans.
- Configure tail-based sampling policies that retain high-value traces
  (errors, latency outliers) while controlling storage cost at scale.
- Use exemplars to pivot from a metric's latency spike directly to a
  representative trace.
- Explain continuous profiling and how it complements tracing by
  answering "where in the code" rather than "which service call."
- Build and interpret a service dependency map from trace data, and use
  it to identify the critical path of a slow request.
- Diagnose common tracing failures: broken context propagation, clock
  skew between hosts, and sampling bias that hides a real problem.

## Theory and Architecture

### The structural model of a trace

A **trace** represents the end-to-end journey of one request through a
distributed system. It is composed of **spans**, where each span
represents a single unit of work — an inbound HTTP request, an outbound
database query, a function call explicitly instrumented as
business-meaningful ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)). Every span carries:

- A `trace_id`, shared by every span in the same trace.
- A `span_id`, unique to that span.
- A `parent_span_id`, linking it to the span that caused it (absent only
  for the trace's root span).
- A start time and duration.
- A `span kind` — `SERVER`, `CLIENT`, `PRODUCER`, `CONSUMER`, or
  `INTERNAL` — describing the span's role in the call, which downstream
  tooling uses to correctly render request/response pairs instead of
  duplicate-counting the same logical hop.
- Attributes (following semantic conventions, [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)), events (
  timestamped annotations within the span, such as a retry), and a
  status (`OK`, `ERROR`, with an optional description).

Because spans are emitted independently by each service — a client span
from the calling service, a server span from the called service — a
trace backend reconstructs the tree by joining spans on `trace_id` and
`parent_span_id` after ingestion, not at emission time. This is why
context propagation ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)'s W3C Trace Context) is structurally
necessary rather than a nice-to-have: any hop that fails to propagate
`traceparent` produces spans that share no `trace_id` with what came
before, and the backend cannot join them into one tree no matter how
complete each fragment's own data is.

```text
Trace tree for one checkout request:

SERVER  checkout-api /checkout               [0ms   -------------------- 420ms]
  CLIENT  -> inventory-service /reserve       [ 10ms  ---- 90ms]
    SERVER  inventory-service /reserve        [ 15ms  --- 85ms]
      INTERNAL  db.query reserve_stock        [ 20ms  -- 70ms]
  CLIENT  -> payment-gateway-adapter /charge  [ 95ms  -------------- 400ms]
    SERVER  payment-gateway-adapter /charge   [100ms  ------------ 395ms]
      CLIENT  -> external payment processor   [110ms  ---------- 380ms]
```

The **critical path** of a trace is the sequence of spans that, if each
were made faster, would actually reduce the total request latency —
distinct from simply the slowest span. In the example above, the
external payment processor call dominates total latency; optimizing the
inventory reservation's database query would not shorten the overall
request, because that work happens concurrently with, and finishes well
before, the payment call's critical path. Trace visualization tools
compute and highlight the critical path automatically; reading a flame
graph or waterfall view without that distinction leads investigators to
optimize spans that do not actually matter.

### Sampling strategy in depth

[Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md) introduced head-based and tail-based sampling at a pipeline
level; this section covers the decision logic in depth, since tracing is
where sampling strategy has the largest effect on both diagnostic value
and cost.

**Head-based sampling** decides at the trace's root span, before
anything downstream is known, typically with a fixed probability (for
example, sample 5% of all traces) or a rate-limiting sampler (sample up
to N traces per second per service). It is cheap — no buffering, no
cross-span coordination required — but structurally blind: a rare,
severe error trace is sampled in or out with the same probability as a
routine successful trace, so at low sampling rates the traces an
incident investigation most needs are frequently the ones that were
discarded.

**Tail-based sampling** defers the keep/discard decision until the full
trace (or a bounded waiting window) has been observed at the gateway
Collector, and applies policy based on what actually happened:

```yaml
# gateway otel-config.yaml (excerpt) — tail sampling policy
processors:
  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    policies:
      - name: keep-all-errors
        type: status_code
        status_code:
          status_codes: [ERROR]
      - name: keep-slow-traces
        type: latency
        latency:
          threshold_ms: 1000
      - name: keep-tier0-services-always
        type: string_attribute
        string_attribute:
          key: service.tier
          values: [tier-0]
      - name: baseline-sample-the-rest
        type: probabilistic
        probabilistic:
          sampling_percentage: 5
```

This policy set keeps 100% of error traces and traces over 1 second
regardless of overall sampling rate, keeps 100% of any trace touching a
Tier 0 service, and applies only a 5% baseline sample to routine,
fast, non-Tier-0 traffic — concentrating storage spend on the traces
most likely to matter for an investigation. The trade-off, noted in
[Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md), is that tail sampling requires every span belonging to a
given trace to reach the same Collector instance for the decision to see
the complete picture; this is typically achieved by consistently
routing on `trace_id` (a load balancer configured for trace-ID-aware
routing, or an OTel Collector `loadbalancing` exporter) ahead of the
tail-sampling gateway tier.

### Exemplars: linking metrics to traces

An **exemplar** is a sampled trace ID attached to a specific metric data
point at the time it was recorded — typically a histogram bucket
observation carries the `trace_id` of one representative request that
fell into that bucket. This closes a common investigation gap:
a latency dashboard shows p99 has spiked, but a metric alone cannot show
*which* request was slow or why. With exemplars, the dashboard panel
renders a clickable point on the spike that jumps directly to a
concrete, representative trace for that exact time and latency bucket.

```text
# Prometheus exposition format with an OpenMetrics exemplar
http_server_request_duration_seconds_bucket{le="0.5"} 12450 # {trace_id="5b8aa5a2d2c872e8321cf37308d69df2"} 0.482 1700000000.114
```

Exemplars require the metrics SDK to have access to the active trace
context at the moment a measurement is recorded (the same underlying
mechanism that enables log-trace correlation, [Chapter 04](04-enterprise-logging-event-management-and-retention.md)) and require
the metrics backend and visualization layer to support exemplar storage
and rendering (Prometheus 3.x and Grafana both do, natively).

### Continuous profiling

Tracing answers "which service call, and how long did it take."
**Continuous profiling** answers the next question down: "where in the
code, at the CPU-instruction or allocation level, did that time or
memory actually go," sampled continuously in production rather than only
during an on-demand profiling session. Modern continuous profilers
(Grafana Pyroscope, Parca) use either language-runtime-level sampling
(periodic stack sampling, similar in principle to `pprof`) or eBPF-based
whole-system sampling that requires no per-language instrumentation and
can profile a process without any code changes or restarts.

Profiling data is visualized as a **flame graph**: each horizontal bar
represents a stack frame, width proportional to the fraction of samples
in which that frame was on the call stack, and stacked vertically by
call depth. A wide bar high in the stack immediately identifies the
function consuming the most CPU time (or, for a memory profile, the most
allocated bytes) across the sampled window — a level of resolution
tracing does not reach, since a single "INTERNAL" span around a slow
function tells you *that* it was slow but not *which line or allocation*
inside it was responsible.

The combination is deliberately layered: a burn-rate alert ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md))
identifies *that* a service is degraded; a trace identifies *which*
downstream call or code path is slow; a profile identifies *where in the
code*, down to the function, that time is being spent. Correlating all
three — increasingly via shared `service.name` and time-window linking
in a single observability UI — is what lets an investigation go from
"latency SLO is burning" to "this specific function's regex compilation
is the cause" without a re-deploy-and-wait profiling cycle.

### Service dependency maps

A trace backend that has ingested a representative sample of traces can
derive a **service dependency map**: which services call which other
services, at what request rate, and with what error rate and latency per
edge — computed automatically from `SERVER`/`CLIENT` span pairs rather
than maintained as a manually updated architecture diagram, which drifts
from reality within weeks in an actively developed system. This map
answers questions a static architecture diagram cannot: which downstream
dependency is a proposed change's actual blast radius, which service has
accumulated the most inbound dependents since a diagram was last drawn,
and which edge's error rate spiked first during a cascading incident —
frequently the fastest way to identify a root-cause service among many
that are simultaneously showing symptoms.

## Design Considerations

- **Sampling policy ownership and review cadence.** Tail-sampling policy
  is a platform-level control with fleet-wide cost and diagnostic-
  coverage impact; changes should go through the same change review as
  other shared pipeline configuration ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)), and the policy
  should be reviewed periodically against actual incident-investigation
  outcomes — a policy that misses the traces investigators actually
  needed during a recent incident is a signal to adjust it, not just a
  one-time design decision.
- **Gateway sizing for tail sampling.** Buffering full traces for the
  `decision_wait` interval (10 seconds in the example above) means
  gateway memory scales with concurrent in-flight trace volume during
  that window, not just steady-state throughput. Size the gateway tier
  for peak concurrent trace volume, and monitor the tail-sampling
  processor's own internal queue and dropped-trace metrics the same way
  [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md) monitors Collector self-telemetry generally.
- **Consistent trace-ID routing overhead.** Ensuring every span of a
  trace reaches the same gateway instance requires an additional routing
  layer (consistent hashing on `trace_id`) ahead of the tail-sampling
  tier, adding one more network hop and one more component that can
  become a bottleneck or single point of degradation; weigh this
  operational cost against the diagnostic value tail sampling provides,
  which is substantial for Tier 0/1 services and may not justify the
  complexity for lower-tier, best-effort services.
- **Continuous profiling overhead and always-on versus on-demand.**
  eBPF-based profilers typically add low, roughly 1-2 percent CPU
  overhead and are safe to run always-on fleet-wide; language-runtime
  sampling profilers vary more by language and configuration. Default to
  always-on for Tier 0/1 services (the profiling data is most valuable
  exactly when captured continuously, before anyone knew an investigation
  would be needed) and evaluate overhead empirically before fleet-wide
  rollout to lower tiers.
- **Cardinality in dependency maps.** A service mesh or heavily
  versioned deployment (many concurrent canary or feature-flag variants)
  can produce a dependency map with far more edges than there are
  logical service relationships, since each version or variant may
  appear as a distinct node. Aggregate by logical service name for the
  primary map view, with version/variant as a drill-down dimension, not
  the default rendering.
- **Storage cost curve by signal.** Full-fidelity trace storage is
  typically the most expensive observability signal per byte retained,
  because a trace carries the union of many attributes across many
  spans. Tail sampling is the primary cost lever; a secondary lever is
  aggressive attribute trimming on routine (non-error, non-slow) spans
  before long-term storage, keeping full attribute fidelity only for the
  traces tail sampling already decided to retain.

## Implementation and Automation

Manual span creation around a critical, non-framework-covered code path,
with events marking retries and an explicit error status — extending
the auto-instrumentation baseline from [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md):

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer("payment-gateway-adapter")

def charge_with_retry(cart, gateway_client, max_attempts=3):
    with tracer.start_as_current_span("charge_with_retry") as span:
        span.set_attribute("payment.attempt_limit", max_attempts)
        for attempt in range(1, max_attempts + 1):
            span.add_event("attempt_started", {"attempt": attempt})
            try:
                result = gateway_client.charge(cart.total_minor_units)
                span.set_attribute("payment.attempts_used", attempt)
                span.set_status(Status(StatusCode.OK))
                return result
            except GatewayTimeout as exc:
                span.add_event("attempt_failed", {"attempt": attempt, "reason": "timeout"})
                if attempt == max_attempts:
                    span.record_exception(exc)
                    span.set_status(Status(StatusCode.ERROR, "gateway exhausted retries"))
                    raise
```

Recording the exception and setting an explicit `ERROR` status is what
allows the tail-sampling `status_code` policy above to reliably retain
this trace — a caught-and-retried exception that never sets span status
is invisible to that policy even though it represents a real, if
recovered, degradation worth investigating in aggregate.

Query a trace backend's derived service dependency data (illustrated
against Tempo's `traceql`-adjacent metrics-generator output, which
produces standard Prometheus-compatible span metrics from ingested
traces) to alert on a specific edge's error rate rather than only the
service's own aggregate:

```promql
# Error rate on the checkout-api -> payment-gateway-adapter edge specifically
sum(rate(traces_service_graph_request_failed_total{
  client="checkout-api", server="payment-gateway-adapter"
}[5m]))
/
sum(rate(traces_service_graph_request_total{
  client="checkout-api", server="payment-gateway-adapter"
}[5m]))
```

Edge-level alerting isolates which specific dependency relationship
degraded, which is materially faster to act on during a multi-service
incident than an aggregate service-level error rate that does not say
which downstream call is responsible.

Deploy an eBPF continuous profiler as a DaemonSet, requiring no
application code changes:

```yaml
# pyroscope-agent-daemonset.yaml (excerpt)
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: pyroscope-ebpf-agent
  namespace: observability
spec:
  selector:
    matchLabels: { app: pyroscope-ebpf-agent }
  template:
    metadata:
      labels: { app: pyroscope-ebpf-agent }
    spec:
      hostPID: true
      containers:
        - name: agent
          image: grafana/pyroscope-ebpf:1.9.0
          securityContext:
            privileged: true
          args:
            - "--server.address=http://pyroscope-gateway.observability.svc:4040"
            - "--collect-user-profile=true"
            - "--collect-kernel-profile=true"
      tolerations:
        - operator: Exists
```

## Validation and Troubleshooting

- **Confirm trace-metric-log correlation end to end.** Take one recent
  trace ID from the tracing backend, confirm the exemplar linking works
  from a corresponding metrics dashboard panel, and confirm the same
  `trace_id` returns matching log lines from the log store ([Chapter 04](04-enterprise-logging-event-management-and-retention.md)'s
  lab pattern). A gap in any leg of this triangle indicates a
  context-propagation or SDK-configuration defect that will surface
  again, worse, during a real incident.
- **Symptom: trace tree is fragmented into disconnected sub-trees.**
  Confirm `traceparent` propagation at every hop ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)'s
  diagnostic approach) and additionally check for clock skew between
  hosts — a trace backend that renders spans out of causal order or
  drops apparently-orphaned spans due to a parent span with a later
  timestamp than its child is frequently a symptom of unsynchronized
  host clocks (verify with `chrony` or the platform's NTP status) rather
  than a propagation defect.
- **Symptom: tail sampling keeps almost nothing, or keeps far more than
  expected.** Check the `decision_wait` value against actual trace
  duration for slow requests — a trace that takes 15 seconds to complete
  cannot be correctly classified by a `latency` policy if
  `decision_wait` is only 10 seconds, since the gateway makes its
  keep/discard decision before the trace finished. Increase
  `decision_wait` to comfortably exceed the slowest traces you intend to
  catch, and monitor the tail-sampling processor's
  `otelcol_processor_tail_sampling_sampling_trace_dropped_too_early`
  metric for confirmation.
- **Symptom: profiling flame graph looks flat or unrepresentative.**
  Confirm the sampling frequency is sufficient for the workload's
  duration — a profiler sampling at a low default rate against a very
  short-lived process may capture too few samples for a statistically
  meaningful flame graph. Cross-check against a longer observation
  window before concluding a genuinely flat CPU profile.
- **Sampling bias masking a real problem.** If head-based sampling
  alone is in use and an investigation cannot find any trace exhibiting
  a known symptom, check whether the sampling rate itself is the reason
  — a rare failure mode occurring in 0.1% of requests will rarely appear
  in a 5% head-based sample. This is precisely the failure mode
  tail-based sampling's error/latency-based retention policies exist to
  prevent, and its absence is a strong argument for adopting tail
  sampling for Tier 0/1 services if not already in place.

## Security and Best Practices

- Treat span attributes with the same sensitivity discipline as log
  fields and metric labels (Chapters 02 and 04): do not attach raw
  request bodies, authorization headers, or unmasked personal data to
  span attributes, since trace backends are frequently granted broader
  read access across teams than any single service's own logs, widening
  the blast radius of an accidental sensitive-attribute leak.
- Restrict who can modify tail-sampling policy and profiling agent
  configuration in production; a policy change that silently starts
  discarding error traces (a `probabilistic` policy accidentally
  replacing a `status_code` policy) degrades incident-investigation
  capability without an obvious symptom until the next incident.
- Scope eBPF-based profiling agents' host privileges narrowly even
  though they require elevated (often privileged) container security
  context to attach kernel probes; run them under a dedicated
  service account with no other cluster permissions, audited
  separately from general workload service accounts.
- Apply retention limits to trace and profile storage consistent with
  the same regulatory and data-minimization considerations covered for
  logs in [Chapter 04](04-enterprise-logging-event-management-and-retention.md) — a full-fidelity trace can incidentally carry as
  much sensitive operational detail as a log line, and profiling data
  can reveal proprietary algorithm characteristics that warrant its own
  access scoping.
- Rate-limit and authenticate the OTLP ingestion endpoint for traces and
  profiles the same as for metrics and logs ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)); an
  unauthenticated ingestion endpoint is a viable injection point for
  fabricated telemetry intended to mislead an investigation or exhaust
  storage capacity.

## References and Knowledge Checks

**References**

- [OpenTelemetry Tracing specification, `opentelemetry.io/docs/specs/otel/trace/`,
  for span structure, span kinds, and status semantics.](https://opentelemetry.io/docs/specs/otel/trace/)
- [Grafana Tempo documentation, `grafana.com/docs/tempo/latest/`, for
  tail sampling and the service-graph metrics generator referenced in
  this chapter's PromQL example.](https://grafana.com/docs/tempo/latest/)
- [Grafana Pyroscope documentation, `grafana.com/docs/pyroscope/latest/`,
  for eBPF and language-runtime continuous profiling.](https://grafana.com/docs/pyroscope/latest/)
- [Sigelman et al., "Dapper, a Large-Scale Distributed Systems Tracing
  Infrastructure" (Google technical report), for the foundational trace
  data model most modern tracing systems still follow.](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/)

**Knowledge Checks**

1. Explain why a trace backend must reconstruct the trace tree after
   ingestion rather than receiving it pre-assembled, and what that
   implies about context propagation.
2. Contrast head-based and tail-based sampling and describe a specific
   incident-investigation scenario in which head-based sampling would
   likely fail to retain the needed trace.
3. What does an exemplar attach to a metric data point, and what
   investigation gap does it close?
4. Why can a trace identify that a function is slow but not identify
   which line or allocation inside it is responsible, and what signal
   fills that gap?
5. A service dependency map shows far more edges than the team's actual
   architecture. What is the most likely cause, and how should the map
   be adjusted?

## Hands-On Lab

**Objective:** Run a local trace pipeline with tail-based sampling
policies, generate both routine and error/slow traces, and verify that
sampling policy correctly retains high-value traces while discarding
routine ones at the configured baseline rate.

### Prerequisites

- Docker Engine and Docker Compose v2.
- `curl` and a POSIX shell.
- Approximately 1.5 GB of free memory for the lab stack.

### Procedure

1. Create the lab directory and a Collector configuration implementing
   tail sampling: retain all errors and all traces over 800ms, sample
   10% of everything else:

   ```bash
   mkdir -p ~/trace-lab && cd ~/trace-lab
   cat > otel-config.yaml <<'EOF'
   receivers:
     otlp:
       protocols:
         grpc:
           endpoint: 0.0.0.0:4317
         http:
           endpoint: 0.0.0.0:4318
   processors:
     tail_sampling:
       decision_wait: 5s
       num_traces: 10000
       policies:
         - name: keep-errors
           type: status_code
           status_code:
             status_codes: [ERROR]
         - name: keep-slow
           type: latency
           latency:
             threshold_ms: 800
         - name: baseline-sample
           type: probabilistic
           probabilistic:
             sampling_percentage: 10
     batch:
       timeout: 2s
   exporters:
     otlp/jaeger:
       endpoint: jaeger:4317
       tls:
         insecure: true
     debug:
       verbosity: basic
   service:
     pipelines:
       traces:
         receivers: [otlp]
         processors: [tail_sampling, batch]
         exporters: [otlp/jaeger, debug]
     telemetry:
       metrics:
         level: detailed
         address: 0.0.0.0:8888
   EOF
   ```

2. Create the Compose file with the Collector and Jaeger:

   ```bash
   cat > docker-compose.yaml <<'EOF'
   services:
     otel-collector:
       image: otel/opentelemetry-collector-contrib:0.116.0
       command: ["--config=/etc/otel/config.yaml"]
       volumes:
         - ./otel-config.yaml:/etc/otel/config.yaml
       ports:
         - "4317:4317"
         - "4318:4318"
         - "8888:8888"
     jaeger:
       image: jaegertracing/all-in-one:1.63.0
       environment:
         - COLLECTOR_OTLP_ENABLED=true
       ports:
         - "16686:16686"
         - "4319:4317"
   EOF
   docker compose up -d
   ```

3. Create a script that sends 100 synthetic traces: 90 fast/successful,
   5 slow (over the 800ms threshold), and 5 errors, so the expected
   retention count can be verified precisely:

   ```bash
   cat > send-traces.py <<'EOF'
   import json
   import random
   import time
   import urllib.request

   def send(trace_id, duration_ms, status_code):
       start = 1_700_000_000_000_000_000
       end = start + duration_ms * 1_000_000
       span = {
           "resourceSpans": [{
               "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": "lab-app"}}]},
               "scopeSpans": [{"spans": [{
                   "traceId": trace_id, "spanId": trace_id[:16], "name": "lab-op",
                   "kind": 2, "startTimeUnixNano": str(start), "endTimeUnixNano": str(end),
                   "status": {"code": status_code},
               }]}],
           }]
       }
       req = urllib.request.Request(
           "http://localhost:4318/v1/traces",
           data=json.dumps(span).encode(),
           headers={"Content-Type": "application/json"},
       )
       urllib.request.urlopen(req).read()

   for i in range(90):
       send(f"{i:032x}", 50, 0)       # fast, OK
   for i in range(5):
       send(f"{900+i:032x}", 1200, 0)  # slow, OK -> kept by latency policy
   for i in range(5):
       send(f"{950+i:032x}", 50, 2)    # fast, ERROR -> kept by status_code policy
       time.sleep(0.01)
   EOF
   python3 send-traces.py
   sleep 8  # allow decision_wait plus export
   ```

### Expected Results

Open `http://localhost:16686`, select service `lab-app`, set the lookback
window to the last 15 minutes, and search with no additional filters.
Confirm the total number of retained traces is approximately 19-20: all
5 slow traces, all 5 error traces, and roughly 9 (10% of 90, allowing for
sampling variance) fast/successful traces. Confirm searching with
`Tags: error=true` returns exactly the 5 error traces, and confirm at
least one returned trace has a duration over 800ms.

### Negative Test

Confirm the baseline sampling is actually discarding most routine
traffic, not accidentally retaining everything (a common tail-sampling
misconfiguration where the probabilistic policy is unreachable because
an earlier policy's logic is inverted). Count the fast/successful traces
specifically:

```bash
curl -s "http://localhost:16686/api/traces?service=lab-app&limit=200" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
fast_ok = [t for t in data['data'] if all(
    not any(tag['key']=='error' for tag in s.get('tags', []))
    for s in t['spans']
)]
print(f'fast/successful traces retained: {len(fast_ok)}')
"
```

Confirm the count is well under 90 (roughly 5-15, consistent with a 10%
sample of 90), not close to 90 — a count near 90 would indicate the
`baseline-sample` policy is not actually being applied and every trace
is being retained regardless of sampling percentage, defeating the cost
control this chapter's Design Considerations section describes.

### Cleanup

```bash
cd ~/trace-lab
docker compose down -v
cd ~
rm -rf ~/trace-lab
```

## Summary and Completion Checklist

A trace is a tree of independently emitted spans joined by shared trace
and parent-span identifiers, and reconstructing it depends entirely on
context propagation working at every hop. Tail-based sampling retains
the traces an investigation actually needs — errors, outliers, and
Tier 0 traffic — while controlling cost on the routine majority.
Exemplars connect metrics to representative traces, and continuous
profiling adds a code-level resolution neither tracing nor metrics
reach. Together with the automatically derived service dependency map,
these signals let an investigation move from "the SLO is burning"
([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)) to the specific function responsible without guesswork.
[Chapter 06](06-actionable-alerting-on-call-and-operations-centers.md) builds actionable alerting and on-call process on top of all
the signals introduced so far.

**Completion checklist**

- [ ] Can describe a trace's structure (spans, span kinds, parent-child
      relationships) and why the backend assembles it after ingestion.
- [ ] Can design a tail-sampling policy that retains errors and outliers
      while controlling baseline cost.
- [ ] Can explain what an exemplar links and the investigation gap it
      closes.
- [ ] Can explain how continuous profiling complements tracing at the
      code level.
- [ ] Deployed a local tail-sampling pipeline and verified retention
      counts matched the configured policy for errors, slow traces, and
      baseline-sampled routine traffic.
