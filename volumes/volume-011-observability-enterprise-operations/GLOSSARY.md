# Volume XI Glossary

Definitions for terms introduced in **Volume XI — Observability and
Enterprise Operations**, alphabetized. See also the
[volume index](INDEX.md) for pointers back to the chapter section each
term is drawn from, and the [master glossary](../../GLOSSARY.md) for
cross-volume terminology.

**Alertmanager** — The Prometheus ecosystem component that receives
fired alerts and applies routing, grouping, inhibition, and silencing
before dispatching notifications to a receiver. Introduced in
Chapter 06.

**Anomaly detection** — Statistical or machine-learning models that
learn a telemetry signal's normal range and flag deviations, used as a
secondary signal alongside threshold-based alerting rather than a
replacement for it. Introduced in Chapter 09.

**Auto-remediation (closed-loop)** — An automated response that detects
a condition and remediates it without human intervention, appropriate
only for low-risk, reversible, well-understood actions protected by rate
limiting and an audit trail. Introduced in Chapter 09.

**Baggage** — A W3C specification for propagating arbitrary key-value
context (a tenant ID or feature-flag variant) alongside a distributed
trace, separate from the Trace Context specification. Introduced in
Chapter 02.

**Blameless postmortem** — A retrospective document treating human error
as a symptom of systemic conditions rather than a root cause, producing
a timeline, contributing factors, and tracked action items rather than
individual blame. Introduced in Chapter 07.

**Burn rate** — The ratio of an SLI's current bad-event rate to the rate
that would exactly exhaust an error budget at the end of its measurement
window; a burn rate of 1 is sustainable, higher values indicate faster
budget consumption. Introduced in Chapter 03.

**Cardinality budget** — An explicit limit on the number of unique
label or attribute value combinations a service may emit on a metric or
log stream, enforced at the pipeline layer to prevent backend overload
and cost inflation. Introduced in Chapter 02.

**ChatOps** — Runbook automation triggered and observed through a chat
interface, keeping a human as the trigger while adding shared
situational awareness to the team watching the channel. Introduced in
Chapter 09.

**Change risk category** — The standard/normal/emergency classification
that routes a production change through the appropriate approval path
based on its risk. Introduced in Chapter 07 (originating in Volume I,
Chapter 08).

**Circuit breaker (remediation)** — A guardrail that halts a closed-loop
automated action once it has fired a defined number of times within a
window, escalating to a human instead of retrying indefinitely against
an unresolved condition. Introduced in Chapter 09.

**Collector (OpenTelemetry)** — A standalone binary that receives,
processes, and exports telemetry, decoupling application processes from
backend choice and availability. Introduced in Chapter 02.

**Continual improvement loop** — The ITIL 4 practice of feeding
operational signals (postmortem action items, capacity forecasts, alert
fatigue trends, cost trends) into a recurring, prioritized platform
investment decision. Introduced in Chapter 09.

**Continuous profiling** — Production sampling of CPU or memory usage at
the code level, visualized as a flame graph, that identifies where in
the code time or memory is spent rather than which service call was
slow. Introduced in Chapter 05.

**Contributing-factors model** — A root cause analysis approach
capturing multiple independent conditions that combined to produce
incident impact, more complete than a single linear Five Whys chain.
Introduced in Chapter 07.

**Counter** — A Prometheus metric type whose value only increases
(or resets on restart), always queried through `rate()` or `increase()`
rather than read directly. Introduced in Chapter 03.

**Critical path (trace)** — The sequence of spans in a trace that, if
individually made faster, would actually reduce total request latency,
distinct from simply the slowest span. Introduced in Chapter 05.

**Error budget** — The amount of unreliability a Service Level
Objective permits over a measurement window, expressed as an allowance a
team can deliberately spend rather than minimize to zero. Introduced in
Chapter 03 (first referenced in Volume I, Chapter 06).

**Escalation policy** — The defined sequence of who is paged next, and
when, if the primary on-call responder does not acknowledge an alert
within a target window. Introduced in Chapter 06.

**Exemplar** — A sampled trace ID attached to a specific metric data
point at the time it was recorded, letting a dashboard pivot from a
latency spike directly to a representative trace. Introduced in
Chapter 05.

**FinOps** — The discipline of making cloud and infrastructure cost a
shared, continuously managed engineering responsibility through
showback, chargeback, and unit economics. Introduced in Chapter 08.

**Five Whys** — A root cause analysis technique that repeatedly asks
"why" against each answer until reaching a root cause, useful for
single-cause narratives but limited for multi-factor incidents.
Introduced in Chapter 07.

**Flame graph** — A visualization of profiling data where each
horizontal bar represents a stack frame, width proportional to sampled
time or allocation, stacked by call depth. Introduced in Chapter 05.

**Gauge** — A Prometheus metric type whose value can go up or down,
read directly or aggregated with `avg()`, `max()`, or `min()`.
Introduced in Chapter 03.

**Head-based sampling** — A trace sampling decision made at the trace's
root span before any downstream outcome is known, typically
probabilistic and cheap but blind to which traces turn out to matter.
Introduced in Chapter 02.

**Histogram** — A Prometheus metric type recording a distribution of
observed values in cumulative buckets, supporting server-side percentile
calculation and cross-instance aggregation. Introduced in Chapter 03.

**Incident Commander (IC)** — The role that owns a major incident end
to end: directing response, making mitigation decisions, and declaring
resolution, deliberately separated from hands-on technical execution.
Introduced in Chapter 07.

**Known Error Database (KEDB)** — An ITIL 4 record of a diagnosed root
cause and its accepted workaround for a problem not yet permanently
fixed, letting a recurrence be recognized immediately rather than
re-investigated. Introduced in Chapter 07.

**Label-indexed storage** — A log storage model (exemplified by Grafana
Loki) that indexes only a small set of labels and stores log content as
compressed, unindexed chunks, trading full-text search for lower cost at
volume. Introduced in Chapter 04.

**LogQL** — Loki's query language, combining a label-based stream
selector with a pipeline of content-filtering operators evaluated at
query time. Introduced in Chapter 04.

**Major incident** — An incident whose impact or ambiguity exceeds what
a single on-call responder should resolve alone, activating a dedicated
command structure. Introduced in Chapter 07.

**MELT** — Metrics, Events, Logs, Traces: the commonly cited signal
types of observability, most valuable when correlated by shared
identifiers rather than treated as independent pillars. Introduced in
Chapter 01.

**MTTA (Mean Time To Acknowledge)** — The average time between an alert
firing and a human acknowledging it, tracked as a trend to detect alert
fatigue or coverage gaps early. Introduced in Chapter 09.

**MTTR (Mean Time To Resolve)** — The average time from incident
declaration to resolution, decomposable into detection, engagement,
diagnosis, and mitigation phases for targeted improvement. Introduced in
Chapter 09.

**Multi-window, multi-burn-rate alerting** — An SLO alerting method
requiring a short window and a longer confirmation window to agree on
elevated burn rate before paging, catching fast severe outages while
suppressing brief noise. Introduced in Chapter 03.

**Observability** — The property of a system that lets an operator ask
questions not anticipated at design time, using existing telemetry,
without shipping new code. Introduced in Chapter 01.

**On-call rotation** — The scheduled assignment of paging accountability
to a specific person for a defined time window, with a defined primary
and secondary to avoid a single point of failure. Introduced in
Chapter 06.

**OTLP (OpenTelemetry Protocol)** — The gRPC or HTTP/protobuf wire
format with defined schemas for metrics, traces, and logs, serving as
the common transport across OpenTelemetry-instrumented systems.
Introduced in Chapter 02.

**Paved road** — A centrally maintained, self-service set of
instrumentation libraries, pipelines, and dashboard/alert templates that
product teams consume rather than each building independently.
Introduced in Chapter 01.

**Problem management** — The ITIL 4 practice that determines why an
incident happened and produces a permanent fix or documented accepted
risk, operating after service is already restored. Introduced in
Chapter 07.

**PromQL** — Prometheus's functional query language over time series,
used to compute rates, ratios, and percentiles from raw counter and
histogram data. Introduced in Chapter 03.

**Saturation point** — The load level at which a system's latency or
error rate begins degrading non-linearly, the primary output of a stress
test. Introduced in Chapter 08.

**Semantic conventions** — OpenTelemetry's standardized attribute names
(`service.name`, `http.request.method`) that let dashboards and queries
written against one service's telemetry work against any conforming
service. Introduced in Chapter 02.

**Service catalog** — The single source of truth for which team owns
which service, its tier, dependencies, and escalation path, consumed by
onboarding and paging automation. Introduced in Chapter 01.

**Service dependency map** — A service-to-service call graph, with
per-edge rate, error rate, and latency, derived automatically from
ingested trace data rather than manually maintained. Introduced in
Chapter 05.

**Service Level Indicator (SLI)** — A precisely defined ratio of good
events to valid events over a window, the measured input to a Service
Level Objective. Introduced in Chapter 03 (first referenced in
Volume I, Chapter 06).

**Service Level Objective (SLO)** — An internal reliability target for
an SLI, set stricter than any externally published SLA to provide
operational lead time. Introduced in Chapter 03 (first referenced in
Volume I, Chapter 06).

**Service tiering** — A classification (commonly Tier 0 through Tier 3)
of a service's business criticality, driving SLO strictness, alert
routing, and on-call rigor. Introduced in Chapter 01.

**Showback** — Reporting infrastructure cost attribution per team or
service without an actual internal billing transfer, making cost visible
as a decision input. Introduced in Chapter 08.

**Span** — A single unit of work within a distributed trace, carrying a
trace ID, span ID, parent span ID, duration, attributes, and a span
kind. Introduced in Chapter 05.

**Structured logging** — Emitting log lines in a defined, machine-
parseable schema (commonly JSON) rather than free text, enabling
reliable field-based querying. Introduced in Chapter 04.

**Summary (metric type)** — A Prometheus metric type calculating
quantiles client-side before export, unable to be meaningfully
aggregated across instances, generally a poorer default than a
histogram. Introduced in Chapter 03.

**Symptom-based alerting** — Alerting on a directly user-visible signal
(such as SLO burn rate) rather than an internal proxy signal, preferred
as the primary paging mechanism because it correlates reliably with
actual user impact. Introduced in Chapter 06.

**Tail-based sampling** — A trace sampling decision made after a trace
completes (or a bounded wait), retaining traces based on what actually
happened — errors, latency outliers — rather than a fixed probability.
Introduced in Chapter 02.

**Toil** — Operational work that is manual, repetitive, automatable,
tactical, devoid of enduring value, and scales linearly with service
growth; a defined category that identifies strong automation candidates.
Introduced in Chapter 09.

**Trace** — The end-to-end record of one request's journey through a
distributed system, assembled from independently emitted spans joined
by a shared trace ID. Introduced in Chapter 05.

**Trace Context** — The W3C specification defining the `traceparent` and
`tracestate` HTTP headers that propagate a trace's identity across
process and service boundaries. Introduced in Chapter 02.

**Unit economics** — Infrastructure cost normalized against a
business-meaningful unit (cost per 1,000 requests, cost per active
user), a more actionable FinOps signal than raw spend for a growing
service. Introduced in Chapter 08.
