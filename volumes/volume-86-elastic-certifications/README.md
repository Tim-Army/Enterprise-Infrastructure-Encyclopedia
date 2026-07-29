# Volume LXXXVI — Elastic Certification Tracks

> The whole Elastic certification program in one volume — the Certified Engineer, Analyst, Observability
> Engineer, and SIEM Analyst — across the Elastic Stack (Elasticsearch, Kibana, Elastic Agent, and
> Elastic Security), with hands-on Elasticsearch/Kibana walkthroughs, verified against elastic.co.

## Overview

Volume LXXXVI maps the **Elastic** certification program — the credentials for building on the **Elastic
Stack** (Elasticsearch, Kibana, Elastic Agent/Fleet, Beats, Logstash) for search, data analysis,
observability, and security. Elastic offers four certifications: the hands-on **Elastic Certified
Engineer** (Elasticsearch cluster and search development), the **Elastic Certified Analyst** (Kibana
data visualization and analysis), the **Elastic Certified Observability Engineer** (metrics, logs, APM,
and uptime), and the **Elastic Certified SIEM Analyst** (Elastic Security). This volume continues the
encyclopedia's Data, storage & backup cluster and complements the observability volumes (XI, LIII–LV).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXXXV): it maps the
program — the credentials, the exam formats, and the Stack components — and teaches each with a hands-on
walkthrough. Every certification was **verified against elastic.co on 29 July 2026** (the certification
hub and the individual exam pages; third-party exam-dump sites were excluded as sources).

Chapters follow the certification ladder:

- **Chapter 01** frames the program — the four certifications, the performance-based versus cognitive exam formats, the 8.15→9.3 version transition, proctoring, and free training.
- **Chapter 02** takes the **Elastic Stack architecture** — Elasticsearch nodes, roles, shards, and data tiers; Kibana; Elastic Agent and Fleet; Beats and Logstash.
- **Chapter 03** takes the **Certified Engineer** data management — indices, mappings, dynamic templates, index templates, data streams, and ILM.
- **Chapter 04** takes the **Certified Engineer** ingest and search — ingest pipelines, Query DSL, ES|QL, and aggregations.
- **Chapter 05** takes the **Certified Analyst** — Kibana analysis and visualization with Discover, KQL, Lens, and dashboards.
- **Chapter 06** takes the **Observability Engineer** — metrics, logs, and uptime with Elastic Agent and the Kibana apps.
- **Chapter 07** takes the **Observability Engineer** — APM, machine learning, and alerting.
- **Chapter 08** takes the **Certified SIEM Analyst** — Elastic Security detection, investigation, and threat hunting.
- **Chapter 09** takes **cluster management, security, and career** — cluster health, RBAC, snapshots, and prep.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** Elasticsearch, Kibana, observability, and Elastic Security are authorized platform work —
> building on, analyzing, and defending your own clusters and data. The SIEM Analyst material (detection,
> investigation, threat hunting) is framed as **defensive** security operations on your own environment.

## Chapters

1. [The Elastic Certification Program](chapters/01-the-elastic-certification-program.md) — the four certifications, exam formats, 8.15→9.3, proctoring, training.
2. [The Elastic Stack Architecture](chapters/02-the-elastic-stack-architecture.md) — Elasticsearch nodes/roles/shards/data tiers, Kibana, Elastic Agent/Fleet, Beats, Logstash.
3. [Certified Engineer — Data Management](chapters/03-certified-engineer-data-management.md) — indices, mappings, dynamic/index templates, data streams, ILM, aliases.
4. [Certified Engineer — Ingest and Search](chapters/04-certified-engineer-ingest-and-search.md) — ingest pipelines, Query DSL, ES|QL, aggregations.
5. [Certified Analyst — Kibana Analysis and Visualization](chapters/05-certified-analyst-kibana-analysis.md) — Discover, KQL, Lens, dashboards, runtime fields.
6. [Observability Engineer — Metrics, Logs, and Uptime](chapters/06-observability-metrics-logs-uptime.md) — Elastic Agent, integrations, Metrics/Logs/Uptime apps, Heartbeat.
7. [Observability Engineer — APM, ML, and Alerting](chapters/07-observability-apm-ml-alerting.md) — APM/RUM apps, machine-learning anomaly jobs, Kibana Alerts, dashboards.
8. [Certified SIEM Analyst — Elastic Security](chapters/08-certified-siem-analyst-elastic-security.md) — detection rules, alerts, Timelines, threat hunting.
9. [Cluster Management, Security, and Career](chapters/09-cluster-management-security-and-career.md) — cluster health, RBAC, snapshots, cross-cluster, prep and career.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Elastic, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md) and the Master Appendices
course-catalog appendix. Every chapter carries one hands-on walkthrough lab per track domain, verified
against elastic.co on 29 July 2026.
