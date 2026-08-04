# Volume CXXXIX — Glossary

| Term | Definition |
|:---|:---|
| **Alloy** | Grafana's OpenTelemetry-native collector: components for discovery, scraping, processing, and export, wired into a pipeline. Collects telemetry; does not instrument applications. |
| **Beyla** | eBPF-based auto-instrumentation that produces telemetry without changing application code. |
| **Burn rate** | How fast an error budget is being consumed relative to the rate that would exhaust it exactly at period end. Burn rate 1 means on-track to exhaust; 14.4 over an hour is a page. |
| **Cardinality** | The number of distinct time series or log streams produced by a metric or label set — the product of every label's distinct values. The dominant cost driver in both Prometheus and Loki. |
| **Context propagation** | Passing trace and span IDs across service boundaries in request headers. Without it, a distributed trace fragments into disconnected pieces. |
| **Credly** | The third-party platform that issues and verifies GROT Academy badges; badge visibility is controlled in Credly's own settings. |
| **Error budget** | The complement of an SLO — the permitted failure. A 99.9% target over 30 days allows roughly 43 minutes of total failure. |
| **Exemplar** | A trace ID attached to a metric sample, allowing a click from a latency spike straight to a representative slow trace. |
| **Explorer** | The GROT Academy badge for the intermediate-level Technical Practitioner 201 path; requires path completion **and** a passed assessment. |
| **`for` duration** | How long an alert condition must hold before firing. During this window the alert is **Pending** — true, but not yet worth waking anyone. |
| **Four Golden Signals** | Latency, traffic, errors, saturation. Latency must be split by outcome, because failed requests are often fast and flatter the graph. |
| **GROT Academy** | Grafana's free learning platform at learn.grafana.com, offering learning paths and the digital badges that are Grafana's current credential program. |
| **Head sampling** | Deciding whether to keep a trace at its start, before the outcome is known — cheap, but discards the errors and slow requests you most want. |
| **LGTM stack** | Loki (logs), Grafana (visualization), Tempo (traces), Mimir (metrics) — Grafana Labs' open-source observability suite. |
| **LogQL** | Loki's query language: stream selector, then line filter, then parser, then label filter — in that order, because filtering before parsing is what keeps queries cheap. |
| **Loki** | Grafana's log backend. It indexes **labels only**, not log content — cheap to ingest, but demanding a good stream selector at query time. |
| **Mimir** | Grafana's horizontally scalable long-term metrics store, Prometheus-compatible and PromQL-queryable. |
| **Navigator** | The GROT Academy badge tier awarded for completing a targeted learning path (PromQL, LogQL, Observability Signals, Dashboard Design) — **no assessment required**. |
| **Notification policy** | A label-matched routing tree deciding which contact point receives an alert, with grouping and timing inherited from the matched branch. |
| **PromQL** | Prometheus' query language for metrics. `sum(rate(counter[5m]))` — `rate` innermost, so counter resets are handled per series before aggregation. |
| **Pyroscope** | Grafana's continuous-profiling backend — resource attribution to code paths *inside* a process. |
| **RED method** | Rate, Errors, Duration — the request-side view, applied per service. |
| **Recording rule** | A query evaluated on a schedule whose result is stored as a new series, so dashboards and alerts read one precomputed value instead of recomputing an expensive aggregation. |
| **Self time** | A span's duration minus the time its children accounted for. High self time marks where work actually happened; total duration merely marks what contained it. |
| **Stream selector** | The mandatory label matcher opening every LogQL query (`{app="checkout"}`); it determines how much data is scanned before any filtering. |
| **Tail sampling** | Deciding whether to keep a trace after it completes, using its outcome — retains errors and outliers at the cost of buffering. |
| **Tempo** | Grafana's trace backend, designed to be cheap enough to store traces at high volume. |
| **Trailblazer** | The GROT Academy badge for the introductory Technical Practitioner 101 path; requires path completion **and** a passed assessment. Its path holds 19 items, ten of them hands-on labs. |
| **Transformation** | A Grafana-side operation on query results — join, merge, rename, calculate — that produces a view neither data source could return alone. |
| **USE method** | Utilization, Saturation, Errors — the resource-side complement to RED. |
