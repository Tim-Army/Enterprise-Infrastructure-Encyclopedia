# Volume LIV — OpenTelemetry

> The CNCF standard for telemetry, end to end — traces, metrics, logs, and profiles;
> the API/SDK, the Collector, OTLP, instrumentation, semantic conventions, sampling,
> and Kubernetes deployment — with hands-on SDK, `curl`/OTLP, and Collector labs,
> pinned to the OpenTelemetry Collector 0.157.x / spec 1.59.x.

## Overview

Volume LIV is a hands-on guide to **OpenTelemetry (OTel)**, the vendor-neutral **CNCF**
framework and standard for generating, collecting, and exporting **telemetry**. It sits
with the encyclopedia's **observability** volumes (Observability XI, LibreNMS LIII) and
underpins modern application monitoring across the cloud and container volumes.

Like the other tool volumes, this is a **product/skills** volume — it teaches the
framework, organized by capability, with a **walkthrough lab for every major functional
area**. It targets the **Collector 0.157.x** and **specification 1.59.x** (verified on
github.com/open-telemetry on 27 July 2026) and runs the Collector and SDKs via Docker
and pip, so every lab is reproducible for free.

Chapters are organized by capability:

- **Chapter 01** introduces OTel, its signals, and the architecture.
- **Chapters 02–04** cover the signals: **traces**, **metrics**, and **logs**.
- **Chapter 05** covers **the Collector** (receivers, processors, exporters, connectors).
- **Chapter 06** covers **instrumentation** and semantic conventions.
- **Chapter 07** covers **OTLP, exporting, and sampling**.
- **Chapter 08** covers **deployment patterns and Kubernetes** (the Operator).
- **Chapter 09** covers **profiles and keeping current**.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Introduction and Architecture](chapters/01-introduction-and-architecture.md) — signals, API/SDK/Collector/OTLP, and running a Collector.
2. [Traces and Spans](chapters/02-traces-and-spans.md) — spans, attributes/events, and context propagation.
3. [Metrics and Instruments](chapters/03-metrics-and-instruments.md) — counters, gauges, histograms, and views.
4. [Logs and Correlation](chapters/04-logs-and-correlation.md) — the log bridge, trace correlation, and the filelog receiver.
5. [The Collector](chapters/05-the-collector.md) — receivers, processors, exporters, and connectors.
6. [Instrumentation and Semantic Conventions](chapters/06-instrumentation-and-semantic-conventions.md) — zero-code and manual instrumentation.
7. [OTLP, Exporting, and Sampling](chapters/07-otlp-exporting-and-sampling.md) — transports, exporters, and head/tail sampling.
8. [Deployment Patterns and Kubernetes](chapters/08-deployment-patterns-and-kubernetes.md) — agent/gateway and the Operator.
9. [Profiles and Keeping Current](chapters/09-profiles-and-keeping-current.md) — the profiles signal, stability, and releases.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **walkthrough lab for every major functional area** — **35 labs** across the
nine chapters. Because OTel is code- and config-driven, the walkthroughs use the real
tooling — the **Python SDK**, **OTLP** over `curl`, the **Collector** (config YAML), and
the **Kubernetes Operator** — all runnable via Docker/pip/kubectl. Each lab states an
objective, commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **opentelemetry.io** and **github.com/open-telemetry** (the
project and docs), the **`otel/opentelemetry-collector-contrib`** image, the language
SDKs, and the **Kubernetes Operator**. OTel components version independently, so confirm
the running versions — the Collector (0.157.x) and specification (1.59.x) were verified
on 27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-54-opentelemetry
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
