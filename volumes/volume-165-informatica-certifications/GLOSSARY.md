# Volume CLXV — Glossary

| Term | Definition |
|:---|:---|
| **CLAIRE** | Informatica's AI/ML metadata-intelligence engine — the "Intelligent" in IDMC. It reasons over the metadata fabric to recommend and automate data-management work: suggesting mappings, discovering and classifying sensitive data, recommending quality rules, matching records, and auto-curating the catalog. |
| **Cloud Application Integration (CAI)** | The IDMC module for real-time application/API integration — processes that orchestrate service connectors in response to API calls or events, the request/response counterpart to CDI's batch mappings. |
| **Cloud Data Governance & Catalog (CDGC)** | The IDMC module that scans, catalogs, and governs the data estate — catalog (searchable inventory), lineage (source-to-report paths), business glossary, ownership/stewardship, and policy/classification. |
| **Cloud Data Integration (CDI)** | The core IDMC module for batch/bulk ETL/ELT — the cloud successor to PowerCenter. Data flows from a source through transformations to a target in a visual mapping. |
| **Cloud Data Quality** | The IDMC module that makes data trustworthy — profiling to discover the actual state, cleansing and standardization to fix it, and validation/scorecards/monitoring to prove and track it. |
| **Cloud Mapping Designer** | The browser canvas in CDI where you build a mapping — dragging a source, adding transformation objects, wiring them, and ending at a target. |
| **Certified Practitioner** | Informatica's implementation-focused credential tier — aimed at delivering real customer projects, with a two-year validity period; includes modernization specializations such as PC→CDI. |
| **Certified Professional** | Informatica's mainstream, role-based credential tier — validates product knowledge and task competency; exams are 70% to pass, 90 minutes, course-backed, and release-dated. |
| **Golden record** | The single, trusted, authoritative record for a real-world entity (a customer, product, supplier), built by MDM from matched source records using survivorship rules — the single source of truth. |
| **IDMC (Intelligent Data Management Cloud)** | Informatica's unified cloud data-management platform — one environment of separately-licensed but integrated modules (integration, quality, MDM, governance/catalog) sharing one metadata fabric and CLAIRE. |
| **Lineage** | The end-to-end path of data through systems — upstream (where a value came from) and downstream (where it flows) — used for impact analysis, root-cause analysis, and compliance; captured automatically across IDMC modules. |
| **Mapping** | The central CDI abstraction — a visual data-flow from source through transformations (filter, expression, joiner, aggregator, lookup) to target; wrapped in a task to run and in a taskflow to orchestrate. |
| **Master Data Management (MDM)** | The IDMC discipline of reconciling records across systems into golden records — matching (deterministic/probabilistic), merge with survivorship, hierarchies, and stewardship; certified as Developer, Administrator, and SaaS. |
| **Metadata fabric** | IDMC's shared metadata layer — one place recording what data exists, its structure, and relationships. Because all modules read and write it, quality rules apply inside mappings and lineage crosses modules; it is what CLAIRE reasons over. |
| **PowerCenter** | Informatica's legacy on-premises ETL flagship — mapping → session → workflow objects stored in a repository, run by an Integration Service. Being modernized to CDI via CDI-PC ("PC to CDI"). |
| **Process (CAI)** | A real-time orchestration in Cloud Application Integration — triggered by an API call, event, or schedule; it calls service connectors, transforms and routes data, and returns a response (synchronous) or fires-and-forgets (asynchronous). |
| **Profiling** | The first step of data quality — automatically analyzing a dataset to discover its actual state: completeness, uniqueness, validity/patterns, and value distribution — so you know where to focus cleansing. |
| **Secure Agent** | A lightweight IDMC runtime engine deployed near the data (in your VPC or data center) that does the actual data processing, while the cloud control plane designs, schedules, and monitors — design in the cloud, execute near the data. |
| **Service connector** | A CAI definition of an external REST/SOAP service (URL, method, request/response shape, auth) that a process can invoke as a step — turning an external API into a callable action inside an integration. |
| **Survivorship** | The MDM rules that decide, field by field, which source value wins when merging matched records into a golden record — most-trusted source, most recent, or most complete. |
| **Standardization** | A data-quality rule that brings values to a canonical form — consistent case, trimmed whitespace, canonical codes (NY ↔ New York) — so data is comparable and dedupe/matching works. |
| **Stewardship** | The human governance of data — data stewards review uncertain matches, resolve conflicts, and manage hierarchies in MDM, and own/curate assets in governance. |
| **Taskflow** | A CDI orchestration of multiple tasks with order, branching, and error handling — run the customer load, then orders, then notify; the counterpart to a PowerCenter workflow. |
