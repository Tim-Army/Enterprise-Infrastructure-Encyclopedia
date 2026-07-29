# Volume LIV Glossary

Definitions for terms used in **Volume LIV — OpenTelemetry**, alphabetized.
See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Collector** — A standalone service that receives, processes, and exports telemetry via
configurable pipelines. Used in Chapter 05.

**Connector** — A Collector component that links two pipelines (e.g., spanmetrics turns
traces into metrics). Used in Chapter 05.

**Context propagation** — Carrying the active trace context across function/service
boundaries, e.g., the W3C `traceparent` header. Used in Chapter 02.

**Exporter** — A component (SDK or Collector) that sends telemetry over OTLP to a
Collector or backend. Used in Chapters 05 and 07.

**Head sampling** — A sampling decision made at span start in the SDK (e.g., ParentBased
with TraceIdRatio). Used in Chapter 07.

**Instrument** — A metrics API object: Counter, UpDownCounter, Gauge, or Histogram. Used
in Chapter 03.

**Instrumentation** — Code/agents that generate telemetry; zero-code (automatic) or
manual (SDK). Used in Chapter 06.

**OTLP** — OpenTelemetry Protocol; the native wire format over gRPC (:4317) or HTTP
(:4318). Used in Chapters 01 and 07.

**Processor** — A Collector component that transforms telemetry (batch, memory_limiter,
attributes, filter). Used in Chapter 05.

**Profiles** — The emerging fourth signal: continuous profiling correlated with other
telemetry. Used in Chapter 09.

**Receiver** — A Collector component that ingests telemetry (otlp, filelog, hostmetrics).
Used in Chapters 04 and 05.

**Resource** — A set of attributes identifying the telemetry source (`service.name`,
host, container). Used in Chapters 04 and 06.

**Semantic conventions** — Standard attribute names (e.g., `http.request.method`) for
portable telemetry. Used in Chapters 06 and 09.

**Signal** — A telemetry type: traces, metrics, logs, or profiles. Used in Chapter 01.

**Span** — A timed operation within a trace, with name, kind, attributes, events, and
status. Used in Chapter 02.

**Tail sampling** — A sampling decision made after a trace completes, in the Collector
(e.g., keep errors/slow). Used in Chapter 07.

**Trace** — The tree of spans representing one request's journey. Used in Chapter 02.

**View** — A metrics SDK configuration that customizes export, aggregation, and attribute
filtering. Used in Chapter 03.
