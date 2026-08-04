# Volume CXL — Glossary

| Term | Definition |
|:---|:---|
| **ActiveGate** | Dynatrace's gateway component: routes OneAgent traffic, performs remote monitoring of things with no agent, runs private synthetic monitors, and provides controlled egress in segmented networks. Environment and Cluster variants. |
| **Alerting profile** | A rule set deciding which problems reach which recipients, filtered by severity, impact, management zone, and tags — the second noise-reduction layer after problem consolidation. |
| **AppEngine** | The Dynatrace platform layer for building custom apps; the subject of the Application Development Specialist certification. |
| **AutomationEngine** | The engine behind workflows — event-driven automation that acts on telemetry rather than only notifying about it. |
| **Baseline** | Learned normal behavior per entity. Baselines are **descriptive**: they answer "is this different?" and cannot answer "is this good enough?" — that is what an SLO is for. |
| **Business event** | A record carrying business meaning (order placed, value, payment method) into Grail for analysis alongside technical telemetry; also the main pathway by which sensitive fields enter the platform. |
| **Davis AI** | Dynatrace's **deterministic, causation-based** analysis engine. It identifies root cause using topology and dependency context, correlating code changes, deployments, and configuration updates rather than statistical coincidence. |
| **DPL** | Dynatrace Pattern Language — named matchers (`INT`, `WORD`, `IPADDR`, `LD`) bound to field names, used by DQL's `parse` to extract structure from unstructured records. |
| **DQL** | Dynatrace Query Language — a pipeline language over Grail (`fetch` → `filter` → `parse` → `summarize` → `sort` → `limit`). Cheap stages belong first: filter before parse before summarize. |
| **Dynatrace Essentials** | A knowledge-based credential whose own description states it **does not measure hands-on** ability. An entry rung, not a competence claim. |
| **Entity** | A monitored object — host, process, service, application, container, cloud resource — carrying a stable ID (`HOST-1A2B3C`) that survives restarts and re-IPs. |
| **Grail** | "The Dynatrace data lakehouse designed explicitly for observability data": logs, metrics, traces, and events in one store organized as **buckets, tables, and views**, requiring **no up-front schema**. |
| **Management zone** | A rule-defined slice of the environment used for both scoping and access control. Distinct from a UI filter, which is cosmetic and can be cleared by the person it appears to restrict. |
| **OneAgent** | The single per-host agent that auto-discovers processes and injects instrumentation. Its coverage gaps are **silent** — an uninstrumented service is absent, not errored. |
| **Problem** | A consolidated grouping of related anomalies with a claimed root cause, affected-entity set, and impact level — one problem where threshold alerting would produce dozens of alerts. |
| **Schema-on-read** | Grail's model: accept data without deciding its shape, and structure it at query time. Moves cost from ingest to query, which is why DQL stage ordering is the cost model rather than a micro-optimization. |
| **Session Replay** | Reconstruction of what a user saw. Masking is **not retroactive**, so the defensible starting point is mask-all with deliberate unmasking; "mask user input" misses sensitive data that is *displayed* rather than typed. |
| **Site Reliability Guardian** | "A Dynatrace app that automates change impact analysis to validate service availability, performance, and capacity objectives." Up to **50 objectives** per guardian; results are Pass (4), Warning (3), Fail (2), and the overall result is **the most severe of individual validations**. |
| **Smartscape** | The live dependency graph, built from observed calls rather than declared configuration. Its completeness is a precondition for trustworthy root cause. |
| **SLO** | A target on a service-level indicator, whose complement is the error budget. Encodes intent, where a baseline encodes history. |
| **User action naming rule** | A rule collapsing per-record action names (`/orders/88213/detail`) into aggregatable ones (`/orders/{id}/detail`), keeping the identifier as a property. The same cardinality discipline as Prometheus labels and Loki streams. |
| **Workflow** | An event-triggered automation — problem opens, SLO burns, schedule fires — running tasks such as API calls, notifications, or remediation. Safe to automate only where the diagnosis is reliable, the blast radius is small, and the action is reversible. |
