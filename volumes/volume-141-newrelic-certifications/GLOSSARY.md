# Volume CXLI — Glossary

| Term | Definition |
|:---|:---|
| **Apdex** | A 0–1 satisfaction score from response times against threshold T: satisfied (≤ T), tolerating (≤ 4T), frustrated (> 4T), scored (satisfied + tolerating/2) / total. Only as meaningful as the chosen T, and blind to distribution shape — keep percentiles beside it. |
| **APA** | New Relic Certified APM Practitioner – Associate: $125, 50 minutes, multiple choice, online proctored, recommending 6+ months of experience. |
| **Attainment** | The percentage of a service level's window that met the SLI's "good" definition, read against the SLO target. |
| **Alert condition** | A NRQL query plus thresholds — the detecting object. Static thresholds for signals with known meaning; baseline conditions for "is this different?", which can never answer "is this acceptable?". |
| **Alert quality management** | REP syllabus material: measuring conditions by action rate, night-page cost, and coverage, then deleting or rerouting the noise. Fires are cost; *acted on* is value. |
| **Core Web Vitals** | LCP (largest contentful paint, good ≤ 2.5 s), INP (interaction to next paint, good ≤ 200 ms), CLS (cumulative layout shift, good ≤ 0.1) — assessed at the 75th percentile of real users, as three separate failure modes. |
| **Custom attribute** | A key-value added to transactions/events by agent configuration (`customer_tier`). Bounded values only, never sensitive data — it is retained, queryable telemetry. |
| **Entity** | Anything reporting to New Relic — app, host, monitor, dashboard — with a GUID and metadata, organized by tags and workloads. |
| **Incident / issue** | An incident opens when a condition's threshold is violated; incidents group into issues, which are what workflows route to humans. Detection and notification are separate decisions. |
| **Infrastructure agent** | The host agent for metrics, processes, and events, and the carrier for on-host integrations. Its tuning knobs trade ingest cost for diagnostic resolution — tune with a ledger, tiered by host criticality. |
| **MELT** | Metrics, events, logs, traces — the four telemetry types. The routing rule: aggregate questions → metrics; per-occurrence → events, traces (cross-service), or logs (one component). |
| **NerdGraph** | New Relic's GraphQL API — the programmatic surface for managing observability fixtures, alongside the Terraform provider. |
| **NRDB** | New Relic's single telemetry store; everything queries it through NRQL. |
| **NRQL** | The query language: `SELECT … FROM … WHERE … FACET … SINCE … TIMESERIES`. `SINCE` sets scan size, `FACET` sets cardinality — and dashboards, alerts, and SLIs are all NRQL, so one wrong clause lies from three places in perfect agreement. |
| **NVF** | New Relic Verified Foundation: free, 45 minutes, multiple choice, online **unproctored**, no prerequisites — taken on learn.newrelic.com rather than Webassessor. |
| **Observability fixtures** | REP's term for instrumentation configs, dashboards, synthetics, alert conditions, and service levels — managed as code via Terraform/NerdGraph, with drift detection actually run. |
| **PEP** | New Relic Certified Performance Engineer – Professional: $175, 60 minutes, proctored, 2+ years recommended. The *performance* sibling: backend, client-side, infrastructure. |
| **REP** | New Relic Certified Reliability Engineer – Professional: $175, 60 minutes, proctored, 2+ years recommended. The *reliability* sibling: alerts, service levels, automation. |
| **Service boundary** | Where an SLO measures. Commitments belong at the user-facing boundary — component SLOs compound (seven 99.5% services ≈ 96.6% end-to-end) and serve as diagnosis, not promises. |
| **SLI / SLO** | The measurement (a NRQL good/total ratio) and the target on it over a window. An SLO is a standing commitment with on-call cost — prioritized to revenue-bearing flows, not sprinkled. |
| **Synthetics** | Scheduled scripted checks: pings for uptime, journey scripts for the flows that make money. Journey scripts are code — updated in the same PR that changes the flow they walk. |
| **Transaction** | APM's unit of work: one request through one instrumented service, recorded as a queryable event. The triage funnel runs summary → transactions (by total impact) → transaction trace → pivot. |
| **Webassessor** | The testing platform delivering New Relic's paid, proctored exams (`webassessor.com/newrelic`). |
| **Workload** | A named group of entities with rolled-up health — returns a verdict ("checkout is degraded because payment-svc") where a tag filter returns a list. |
