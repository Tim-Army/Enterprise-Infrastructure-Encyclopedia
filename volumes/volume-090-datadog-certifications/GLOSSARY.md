# Volume XC Glossary

Definitions for terms introduced in **Volume XC — Datadog Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Agent** — the Datadog software installed on hosts (or run as a container) that collects metrics, traces, and logs and forwards them to Datadog.
- **Cloud SIEM** — Datadog's security analytics that applies detection rules to logs to raise security signals for defensive triage.
- **Database Monitoring (DBM)** — Datadog's query-level database observability (normalized query metrics, explain plans, samples).
- **Distribution** — a metric type providing globally accurate percentiles across many hosts.
- **DogStatsD** — the StatsD-compatible endpoint the Agent exposes for custom application metrics.
- **Downtime** — a scheduled mute of alerts during planned maintenance.
- **Facet** — an indexed log attribute that can be searched and aggregated in the Log Explorer.
- **Grok parser** — a log pipeline processor that extracts structured fields from unstructured text.
- **Host map** — a fleet visualization coloring hosts by a metric to spot outliers.
- **Monitor** — an object that evaluates a query against thresholds (or a learned baseline) and alerts.
- **Normalized query metrics** — DBM's aggregation of a query shape regardless of literal values.
- **Pipeline** — an ordered set of log processors that structure and enrich logs on ingestion.
- **Screenboard** — a free-form Datadog dashboard for status/NOC displays.
- **SLO** — a Service Level Objective tracking a reliability target against an error budget.
- **Span** — one unit of work within a trace, with a duration, tags, and parent/child links.
- **Timeboard** — a time-synchronized Datadog dashboard for troubleshooting and correlation.
- **Trace** — the full record of a request as a tree of spans across services.
- **Unified service tagging** — the `env`, `service`, and `version` tags that correlate a service's metrics, traces, and logs.
