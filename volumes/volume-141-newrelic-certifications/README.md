# Volume CXLI — New Relic Certification Tracks

> The New Relic observability platform and its certification program — verified 4 August 2026 on
> `learn.newrelic.com` (New Relic University). The program is **small, public, and cleanly laddered**:
> four certifications. The **New Relic Verified Foundation (NVF)** is **free, 45 minutes, and
> unproctored**, with no prerequisites. The **Certified APM Practitioner – Associate (APA)** is $125,
> 50 minutes, online proctored, recommending 6+ months of experience. Two sibling Professionals are
> $175 and 60 minutes each, proctored, recommending 2+ years: the **Certified Performance Engineer
> (PEP)** — backend, client-side, and infrastructure performance — and the **Certified Reliability
> Engineer (REP)** — alerts, service levels, and automation. All exams are multiple choice, offered
> in **English, Spanish, Portuguese, and Japanese**; paid exams deliver via **Webassessor**, and every
> exam publishes its **section-level topics on public pages** — the blueprints this volume follows.
> Question count and passing score sit in per-exam Exam Guides behind a free sign-in, and **no
> validity policy appears publicly; this volume asserts neither.** Every lab runs free in Python.

## Overview

New Relic's architecture is the **single-store** model: agents send metrics, events, logs, and
traces (**MELT**) into **NRDB**, and one language — **NRQL** — queries all of it. That language is
also the platform's configuration surface: dashboards, alert conditions, and service levels are all
NRQL, which concentrates both leverage and risk (Chapter 03 demonstrates a single wrong `WHERE`
clause lying identically from all three).

Chapter 02 covers **telemetry types, agents, entities, tags, and workloads**. Chapter 03 covers
**NRQL** and its cost levers. Chapter 04 covers **APM** — transactions, Apdex and its blind spots,
and ranking database work by total time. Chapter 05 covers **browser, mobile, and synthetics**,
including Core Web Vitals at the 75th percentile. Chapter 06 covers **infrastructure, Kubernetes,
and network correlation**. Chapter 07 covers **alerts** — the policy/condition/incident/workflow
hierarchy and the alert-quality audit REP examines. Chapter 08 covers **service levels and
observability-as-code** via Terraform and NerdGraph. Chapter 09 closes on choosing between the
sibling Professional tracks.

A contrast runs through the volume: this program is the disclosure mirror image of
[Dynatrace's (CXL)](../volume-140-dynatrace-certifications/README.md) — four public certifications
with a mechanics table on an open page, versus thirty-four badges behind a University sign-in.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The New Relic Certification Program](chapters/01-the-new-relic-certification-program.md) | 1.1–1.2 |
| 02 | [Telemetry, Agents, Entities, and Workloads](chapters/02-telemetry-agents-entities-and-workloads.md) | 2.1–2.3 |
| 03 | [NRQL](chapters/03-nrql.md) | 3.1–3.3 |
| 04 | [APM — Transactions, Apdex, and Databases](chapters/04-apm-transactions-apdex-and-databases.md) | 4.1–4.3 |
| 05 | [Browser, Mobile, and Synthetics](chapters/05-browser-mobile-and-synthetics.md) | 5.1–5.3 |
| 06 | [Infrastructure, Cloud, and Kubernetes](chapters/06-infrastructure-cloud-and-kubernetes.md) | 6.1–6.3 |
| 07 | [Alerts and Incident Management](chapters/07-alerts-and-incident-management.md) | 7.1–7.3 |
| 08 | [Service Levels and Automation](chapters/08-service-levels-and-automation.md) | 8.1–8.3 |
| 09 | [Choosing a Certification, Currency, and Career](chapters/09-choosing-a-certification-currency-career.md) | 9.1–9.2 |

## The certification ladder

| Cert | Level | Cost | Duration | Delivery | Experience |
| --- | --- | --- | --- | --- | --- |
| **NVF** — Verified Foundation | Foundation | **Free** | 45 min | Online, **unproctored** | 0–6 months |
| **APA** — APM Practitioner | Associate | $125 | 50 min | Online proctored | 6+ months |
| **PEP** — Performance Engineer | Professional | $175 | 60 min | Online proctored | 2+ years |
| **REP** — Reliability Engineer | Professional | $175 | 60 min | Online proctored | 2+ years |

There is no Expert tier; PEP and REP are siblings, not a sequence.

## What you will be able to do

- Route questions to the right MELT telemetry type, and organize an estate with tags and workloads.
- Write NRQL that is cheap as well as correct, and recognize the shared-clause risk.
- Triage a slow service summary → transaction → trace, and rank database work by total time.
- Read Core Web Vitals at p75 and script journey synthetics for the paths that make money.
- Tune the infrastructure agent with a ledger, and monitor Kubernetes at the workload level.
- Audit alert quality by action rate, and run post-incident alert retrospectives.
- Put SLO commitments at user-facing boundaries and manage fixtures as code with drift detection.

## Prerequisites

- Working familiarity with web applications, databases, and cloud infrastructure.
- A Linux or macOS host with `python3`. A free New Relic account is recommended — every exam topic
  list assumes real platform time.

## See also

- [Volume CXL — Dynatrace](../volume-140-dynatrace-certifications/README.md) and [Volume XC — Datadog](../volume-090-datadog-certifications/README.md) — the other single-vendor platforms; [Volume CXXXIX — Grafana](../volume-139-grafana-observability/README.md) — the assemble-it-yourself opposite.
- [Volume LV — Prometheus](../volume-055-prometheus/README.md), [Volume LIV — OpenTelemetry](../volume-054-opentelemetry/README.md) — open foundations; New Relic ingests OTel natively.
- [Volume CXXXIV — SolarWinds](../volume-134-solarwinds-certifications/README.md) — the database wait-time analysis Chapter 04 meets from the application side.
- [Volume XI — Observability and Enterprise Operations](../volume-011-observability-enterprise-operations/README.md) — the vendor-neutral SRE discipline behind REP.
