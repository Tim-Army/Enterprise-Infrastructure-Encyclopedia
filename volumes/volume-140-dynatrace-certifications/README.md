# Volume CXL — Dynatrace Certification Tracks

> The Dynatrace observability and application-security platform and its credential program —
> verified 4 August 2026 against the **Dynatrace Credly issuer catalog** (34 badges) and
> `docs.dynatrace.com`. **Dynatrace University is sign-in gated, so exam mechanics — fee,
> duration, question count, passing score, and validity — are not publicly published, and this
> volume does not assert them.** What *is* published: the credential names, Dynatrace's own
> **level labels**, cost flags, time-to-earn bands, and per-badge **skill lists**, which serve as
> the blueprint. Two facts change how you read the program: the **Associate is labeled
> *Intermediate***, not foundational — Beginner and Essentials are the entry rungs — and
> **Essentials explicitly does not measure hands-on ability**. Of the 34 badges, only about
> eleven are practitioner certifications; the rest are partner, services-delivery, or internal
> Dynatrace programs. Every lab runs free in Python; the security chapter is defensive
> throughout.

## Overview

Dynatrace's defining bet is **automation over assembly**. One agent per host discovers what is
running, builds a live dependency model, and applies **deterministic, causation-based** analysis
to it — the opposite end of the axis from [Grafana's](../volume-139-grafana-observability/README.md)
query-data-where-it-lives composability.

Chapter 02 covers **OneAgent and ActiveGate**, including auto-instrumentation's silent gaps.
Chapter 03 covers **Grail, DQL, and DPL** — a schema-on-read lakehouse where the cost of
flexibility arrives at query time. Chapter 04 covers **entities, Smartscape topology, and
management zones**, and why topology completeness is a precondition for trusting root cause.
Chapter 05 covers **Digital Experience Monitoring**. Chapter 06 covers **Davis AI, problems, and
root cause**. Chapter 07 covers **Application Security**, defensively. Chapter 08 covers **SLOs,
workflows, and Site Reliability Guardian**. Chapter 09 closes on choosing a credential.

A theme runs through it: **the platform's confident answers are only as good as its inputs.**
Auto-instrumentation gaps raise no error, an incomplete topology yields a confident wrong root
cause, a baseline normalizes a chronically bad service, and blocking a false positive is an
outage. Each chapter names the input that has to be right.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Dynatrace Certification Program](chapters/01-the-dynatrace-certification-program.md) | 1.1–1.2 |
| 02 | [OneAgent, ActiveGate, and Deployment](chapters/02-oneagent-activegate-and-deployment.md) | 2.1–2.3 |
| 03 | [Grail, DQL, and DPL](chapters/03-grail-dql-and-dpl.md) | 3.1–3.3 |
| 04 | [Entities, Topology, and Management Zones](chapters/04-entities-topology-and-management-zones.md) | 4.1–4.3 |
| 05 | [Digital Experience Monitoring](chapters/05-digital-experience-monitoring.md) | 5.1–5.3 |
| 06 | [Davis AI, Problems, and Root Cause](chapters/06-davis-ai-problems-and-root-cause.md) | 6.1–6.3 |
| 07 | [Application Security](chapters/07-application-security.md) | 7.1–7.3 |
| 08 | [SLOs, Workflows, and Site Reliability Guardian](chapters/08-slos-workflows-and-site-reliability-guardian.md) | 8.1–8.3 |
| 09 | [Choosing a Certification, Currency, and Career](chapters/09-choosing-a-certification-currency-career.md) | 9.1–9.2 |

## The credential ladder

| Tier | Credential | Dynatrace's level label |
| --- | --- | --- |
| Entry | Dynatrace Beginner · **Dynatrace Essentials** (knowledge only) | — |
| Core | **Dynatrace Associate** · Associate for Managed | **Intermediate** |
| Core | **Dynatrace Professional** · Administration Professional · Implementation Professional | **Advanced** |
| Top | **Dynatrace Master** (live product usage exams) | **Advanced** |
| Beside | **Advanced Observability** · **DEM & Business Analytics** · **Advanced Security** · **Advanced Automation** · Application Development Specialists | **Intermediate** |

## What you will be able to do

- Read the credential catalog accurately, separating practitioner from partner and internal badges.
- Deploy OneAgent and ActiveGate, and reconcile detected services against a real inventory.
- Write DQL pipelines that are cheap as well as correct, and extract structure with DPL.
- Build rule-based tags and management zones that are access control, not view filtering.
- Run RUM and synthetics for their complementary blind spots, with mask-all Session Replay.
- Explain causal root cause — and the conditions under which it can be trusted.
- Prioritize vulnerabilities by runtime context, and enable blocking only after measuring precision.
- Define SLOs, gate releases with Site Reliability Guardian, and grade automation by risk.

## Prerequisites

- Working familiarity with distributed applications, containers, and cloud infrastructure.
- A Linux or macOS host with `python3` for the labs. A free Dynatrace trial tenant is
  recommended for practice — and effectively required for the Master tier.

## See also

- [Volume CXXXIX — Grafana](../volume-139-grafana-observability/README.md) — the composable opposite; [Volume XC — Datadog](../volume-090-datadog-certifications/README.md) — the other major SaaS platform.
- [Volume LV — Prometheus](../volume-055-prometheus/README.md), [Volume LIV — OpenTelemetry](../volume-054-opentelemetry/README.md) — open metrics and vendor-neutral instrumentation.
- [Volume LXXXVI — Elastic](../volume-086-elastic-certifications/README.md), [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md) — index-on-write, the counterpart to Grail's schema-on-read.
- [Volume CXXXVII — Rapid7](../volume-137-rapid7-certifications/README.md), [Volume LXXVIII — Tenable](../volume-078-tenable-certifications/README.md) — context-aware vulnerability prioritization from the scanner side.
- [Volume XI — Observability and Enterprise Operations](../volume-011-observability-enterprise-operations/README.md) — the vendor-neutral discipline.
