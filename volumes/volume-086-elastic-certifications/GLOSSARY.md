# Volume LXXXVI Glossary

Definitions for terms introduced in **Volume LXXXVI — Elastic Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **APM (Application Performance Monitoring)** — Elastic's tracing of service transactions, spans, errors, and dependencies.
- **Data stream** — an abstraction over a series of auto-rolled-over backing indices for time-series data.
- **Data tier** — hot/warm/cold/frozen storage classes that ILM uses to place indices by age and access.
- **Detection rule** — an Elastic Security rule (query, threshold, indicator-match, EQL, or ML) that generates alerts.
- **ECS (Elastic Common Schema)** — the common field schema that normalizes data across sources.
- **Elastic Agent** — a single, Fleet-managed agent that runs integrations to collect logs, metrics, and security data.
- **ES|QL** — the Elasticsearch Query Language, a piped, SQL-like query and aggregation language (new in the 9.3 blueprint).
- **Fleet** — Kibana's central management for Elastic Agents and integrations.
- **Heartbeat** — the Beat that checks service uptime over ICMP, TCP, or HTTP.
- **ILM (Index Lifecycle Management)** — policies that roll over, tier, and delete indices automatically.
- **Ingest pipeline** — a set of processors (grok, dissect, date, geoip, and more) that transform documents before indexing.
- **KQL (Kibana Query Language)** — Kibana's filtering language for Discover and dashboards.
- **Kibana** — the Elastic Stack UI for search, visualization (Lens, dashboards), observability, and security.
- **Lens** — Kibana's drag-and-drop visualization builder.
- **Machine learning anomaly job** — an Elastic ML job that learns a baseline and flags deviations.
- **Query DSL** — Elasticsearch's JSON query language (leaf queries plus the bool query).
- **Runtime field** — a field computed at query time (via Painless) without reindexing.
- **Shard** — a horizontal partition of an index (primary or replica) distributed across nodes.
- **Snapshot / SLM** — a backup of indices and cluster state to a repository; Snapshot Lifecycle Management automates it.
- **Timeline** — Elastic Security's investigation workspace for reconstructing an incident event by event.
