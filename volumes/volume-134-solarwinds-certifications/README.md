# Volume CXXXIV — SolarWinds Certification Tracks

> The certification map for **SolarWinds**, whose **SolarWinds Certified Professional (SCP)** program is
> product-specific rather than tiered — verified on the official program page, 4 August 2026. The
> portfolio has been **rebranded around SolarWinds Observability**, split into **SaaS** and **Self-Hosted**
> (the on-premises Orion lineage), and the eleven current exams follow that split: **Observability SaaS
> Fundamentals**; Self-Hosted **Fundamentals**, **Network Monitoring**, **Network Management**,
> **Architecture & Design**, **Diagnostics & Troubleshooting**, and **Federal Fundamentals**; plus
> **Server and Application Monitor**, **Database Performance Analyzer**, **Database Management**, and
> **Service Desk**. The process is three steps — sign up, study, schedule — with exams delivered by
> **PSI Services remote proctoring** and a fee of **US$200**, or **60,000 THWACK community points**
> exchanged for an SCP voucher, which makes the exam effectively free for active community members. The
> volume teaches the underlying monitoring and observability disciplines and models them free in Python:
> polling and collection, availability arithmetic and error budgets, interface errors versus utilization,
> configuration drift and compliance, application health rollup, database wait-time analysis,
> dependency-aware alerting, percentiles, and capacity runway. No SolarWinds license required.

## Overview

Volume CXXXIV is a **certification-tracks volume** organized by the disciplines the exams test rather than
by product screens. Chapter 02 covers platform architecture and collection (polling engines, SNMPv3,
agents, Self-Hosted versus SaaS); Chapters 03–04 cover the network pair — monitoring (availability,
utilization versus errors, topology-aware root cause) and management (drift, compliance, controlled
change); Chapter 05 covers server and application monitoring and the "process running ≠ service working"
distinction; Chapter 06 covers database performance through **wait-time analysis**; Chapter 07 covers
alerting, thresholds, and the alert-fatigue problem that determines whether monitoring works at all; and
Chapter 08 covers dashboards, SLA reporting, percentiles, and capacity forecasting against procurement
lead time. Chapter 09 closes on exam selection, preparation, and currency.

Its place on the encyclopedia's monitoring shelf is **breadth across traditional enterprise IT** with a
deep on-premises heritage, alongside [Datadog XC](../volume-090-datadog-certifications/README.md)
(cloud-native SaaS), [Splunk XLV](../volume-045-splunk-certifications/README.md) (logs and security),
[Prometheus LV](../volume-055-prometheus/README.md) and
[OpenTelemetry LIV](../volume-054-opentelemetry/README.md) (open standards), and
[LibreNMS LIII](../volume-053-librenms/README.md) (the open-source network counterpart).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The SolarWinds Program and the SCP Credential](chapters/01-the-solarwinds-program-and-scp.md) | 1.1–1.2 |
| 02 | [Monitoring Fundamentals and the Observability Platform](chapters/02-monitoring-fundamentals-and-the-platform.md) | 2.1–2.3 |
| 03 | [Network Monitoring](chapters/03-network-monitoring.md) | 3.1–3.3 |
| 04 | [Network Configuration and Change Management](chapters/04-network-configuration-management.md) | 4.1–4.3 |
| 05 | [Server and Application Monitoring](chapters/05-server-and-application-monitoring.md) | 5.1–5.3 |
| 06 | [Database Performance](chapters/06-database-performance.md) | 6.1–6.3 |
| 07 | [Alerting, Thresholds, and Noise](chapters/07-alerting-thresholds-and-noise.md) | 7.1–7.3 |
| 08 | [Dashboards, Reporting, and Capacity Planning](chapters/08-dashboards-reporting-capacity.md) | 8.1–8.3 |
| 09 | [Choosing an Exam, Currency, and Career](chapters/09-choosing-an-exam-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the eleven SCP exams and choose the one matching the product you operate.
- Size polling engines for capacity *and* reachability, and pick the right collection method per target.
- Calculate availability against SLA targets with error budgets, and distinguish errors from utilization.
- Detect configuration drift, assess compliance at scale, and gate change through backup and rollback.
- Build application templates whose checks test behavior rather than process existence.
- Use wait-time analysis to find what a database is really waiting on, and rank queries by total impact.
- Design alerting that survives contact with on-call: baselines, suppression, severity, measured signal ratio.
- Report percentiles rather than averages, and forecast capacity against procurement lead time.

## Prerequisites

- Networking and systems fundamentals ([Volume II](../volume-002-network-engineering-foundations/README.md), [Volume IV](../volume-004-enterprise-systems-administration/README.md)); [Volume XI](../volume-011-observability-enterprise-operations/README.md) for the vendor-neutral discipline.
- A Linux or macOS host with `python3` — every lab runs on the standard library, with no SolarWinds software.

## See also

- [Volume XC — Datadog](../volume-090-datadog-certifications/README.md), [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md), [Volume LV — Prometheus](../volume-055-prometheus/README.md), [Volume LIV — OpenTelemetry](../volume-054-opentelemetry/README.md), [Volume LIII — LibreNMS](../volume-053-librenms/README.md) — the neighboring monitoring programs.
- [Volume XI — Observability and Enterprise Operations](../volume-011-observability-enterprise-operations/README.md) — vendor-neutral foundations.
- [Volume LXIII — Public Sector Data Governance](../volume-063-public-sector-data-governance/README.md) — context for the Federal Fundamentals exam.
- [Master Appendices — SolarWinds appendix](../volume-997-master-appendices/chapters/68-appendix-solarwinds-certifications-and-course-access.md) — exams, resources, and access.
