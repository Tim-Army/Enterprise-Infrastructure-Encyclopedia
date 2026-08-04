# Volume CXXXIX — Grafana Observability Platform and GROT Academy

> The Grafana observability platform and its credential program — verified on GROT Academy
> (learn.grafana.com) and grafana.com, 4 August 2026. Grafana's defining choice is that it **queries data
> where it lives** rather than owning a store, so one dashboard spans Prometheus/Mimir metrics, Loki logs,
> Tempo traces, Pyroscope profiles, and ordinary SQL. **Grafana Labs currently awards free digital
> badges, not paid certifications:** six badges in three tiers through **GROT Academy** — **Trailblazer**
> (Technical Practitioner 101) and **Explorer** (201), each requiring a completed learning path **and a
> passed assessment**, plus four **Navigator** badges (PromQL Zero to Hero, LogQL Zero to Hero,
> Observability Signals Foundations, Dashboard Design & Visual Storytelling) requiring only path
> completion. All content is **free**, badges issue via **Credly**, and new badges are expected each
> quarter. Chapters 02–08 follow Grafana's own **Technical Practitioner 101** curriculum. Every lab runs
> free in Python — and unusually for this encyclopedia, the real product is free to run too.

## Overview

Volume CXXXIX is a **product and skills volume** whose spine is Grafana's own practitioner curriculum.
Chapter 02 covers collection with **Alloy** on Kubernetes — explicitly *collection*, not instrumentation,
which is [OpenTelemetry's](../volume-054-opentelemetry/README.md) territory. Chapter 03 covers data
sources, cross-source joins, and variables. Chapters 04 and 05 cover the two query languages, **PromQL**
and **LogQL**, each with the cardinality discipline that keeps them affordable. Chapter 06 covers
**traces** and the metric → trace → log correlation workflow. Chapter 07 covers dashboards through the
**Four Golden Signals**, including how axis choices mislead. Chapter 08 covers **recording rules**,
alerting, and **error-budget burn-rate** SLO alerting. Chapter 09 closes on badge paths and honest effort
estimates.

A recurring theme, drawn from the material itself: **the default is usually wrong at scale.** Auto-scaled
axes dramatize noise, head sampling discards the traces you need, unbounded labels explode cardinality,
`rate` outside `sum` invents outages, and a healthy-looking collector proves nothing about ingestion.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Grafana Platform and GROT Academy](chapters/01-the-grafana-platform-and-grot-academy.md) | 1.1–1.2 |
| 02 | [Collection with Alloy](chapters/02-collection-with-alloy.md) | 2.1–2.3 |
| 03 | [Data Sources, Queries, and Transformations](chapters/03-data-sources-queries-transformations.md) | 3.1–3.3 |
| 04 | [PromQL for Metrics](chapters/04-promql-for-metrics.md) | 4.1–4.3 |
| 05 | [Loki and LogQL](chapters/05-loki-and-logql.md) | 5.1–5.3 |
| 06 | [Traces and Correlating the Three Signals](chapters/06-traces-and-correlation.md) | 6.1–6.3 |
| 07 | [Dashboards and the Four Golden Signals](chapters/07-dashboards-and-the-four-golden-signals.md) | 7.1–7.3 |
| 08 | [Recording Rules, Alerting, and SLOs](chapters/08-recording-rules-alerting-and-slos.md) | 8.1–8.3 |
| 09 | [Badge Paths, Currency, and Career](chapters/09-badge-paths-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Describe the Grafana platform and the GROT Academy badge program accurately — including what it is not.
- Build collection pipelines with Alloy, control cardinality at the process stage, and prove ingestion works.
- Join data across sources to derive insight neither backend holds.
- Write PromQL that survives restarts, and LogQL that scans only what it must.
- Read traces by self time, and walk metric → trace → log from symptom to cause.
- Design dashboards per audience, with latency split by outcome and axes that do not mislead.
- Precompute with recording rules, tune `for` durations, and alert on error-budget burn rate.

## Prerequisites

- Familiarity with Kubernetes and with the idea of a time-series query language — the 101 curriculum assumes both, despite being labeled introductory.
- A Linux or macOS host with `python3`. Grafana OSS is also free: `docker run -p 3000:3000 grafana/grafana`.

## See also

- [Volume LV — Prometheus](../volume-055-prometheus/README.md) — the metrics backend behind PromQL; [Volume LIV — OpenTelemetry](../volume-054-opentelemetry/README.md) — instrumentation, where this volume's Chapter 02 begins.
- [Volume XC — Datadog](../volume-090-datadog-certifications/README.md) — the owns-its-data alternative; [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md) and [Volume LXXXVI — Elastic](../volume-086-elastic-certifications/README.md) — full-text indexing, the architectural opposite of Loki.
- [Volume LIII — LibreNMS](../volume-053-librenms/README.md), [Volume CXXXIV — SolarWinds](../volume-134-solarwinds-certifications/README.md) — network and IT-operations monitoring.
- [Volume XI — Observability and Enterprise Operations](../volume-011-observability-enterprise-operations/README.md) — the vendor-neutral discipline.
