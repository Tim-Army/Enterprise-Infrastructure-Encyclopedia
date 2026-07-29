# Volume LV — Prometheus

> The CNCF metrics system and TSDB, end to end — the pull model, the data model and
> metric types, scraping and service discovery, PromQL (fundamentals and advanced),
> exporters and instrumentation, recording and alerting rules, Alertmanager, and
> storage/scaling — with hands-on PromQL, `promtool`, and API labs against a Docker
> Prometheus, pinned to Prometheus 3.13.x.

## Overview

Volume LV is a hands-on guide to **Prometheus**, the open-source (CNCF) **monitoring
system and time-series database**. It sits with the encyclopedia's **observability**
volumes (Observability XI, LibreNMS LIII, OpenTelemetry LIV) — Prometheus is the
metrics backbone many of them export to.

Like the other tool volumes, this is a **product/skills** volume — it teaches the tool,
organized by capability, with a **walkthrough lab for every major functional area**. It
targets the **3.x** series (**v3.13.x**, verified on github.com/prometheus/prometheus on
27 July 2026) and runs Prometheus, exporters, and Alertmanager via Docker, so every lab
is reproducible for free.

Chapters are organized by capability:

- **Chapter 01** introduces Prometheus, the pull model, and the architecture.
- **Chapter 02** covers the **data model and metric types**.
- **Chapter 03** covers **scraping and service discovery**.
- **Chapters 04–05** cover **PromQL** — fundamentals then advanced.
- **Chapter 06** covers **exporters and instrumentation**.
- **Chapter 07** covers **recording and alerting rules**.
- **Chapter 08** covers **Alertmanager**.
- **Chapter 09** covers **storage, scaling, and keeping current**.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Introduction and Architecture](chapters/01-introduction-and-architecture.md) — the pull model, TSDB, and running Prometheus.
2. [The Data Model and Metric Types](chapters/02-data-model-and-metric-types.md) — series, labels, the four types, cardinality.
3. [Scraping and Service Discovery](chapters/03-scraping-and-service-discovery.md) — scrape_configs, relabeling, promtool.
4. [PromQL Fundamentals](chapters/04-promql-fundamentals.md) — selectors, rate, aggregation, filters.
5. [PromQL Advanced](chapters/05-promql-advanced.md) — histograms, subqueries, vector matching, forecasting.
6. [Exporters and Instrumentation](chapters/06-exporters-and-instrumentation.md) — node_exporter, client libraries, Pushgateway, blackbox.
7. [Recording and Alerting Rules](chapters/07-recording-and-alerting-rules.md) — rules, `for`, labels/annotations, unit tests.
8. [Alertmanager](chapters/08-alertmanager.md) — routing, grouping, inhibition, silences.
9. [Storage, Scaling, and Keeping Current](chapters/09-storage-scaling-and-keeping-current.md) — TSDB, remote write, snapshots, releases.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **walkthrough lab for every major functional area** — **35 labs** across the
nine chapters. Because Prometheus is query- and config-driven, the walkthroughs use the
real tooling — **PromQL** over the HTTP API (`curl`), **`promtool`** and **`amtool`**,
the **exporters**, and **Alertmanager** — all runnable via Docker. Each lab states an
objective, commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **prometheus.io** and **github.com/prometheus** (the project and
docs), the **`prom/prometheus`**, **`prom/node-exporter`**, **`prom/pushgateway`**, and
**`prom/alertmanager`** images, and **Prometheus 3.13.x**. Prometheus releases
frequently, so confirm the running version (`/api/v1/status/buildinfo`) — the latest
release was verified on 27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-055-prometheus
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
