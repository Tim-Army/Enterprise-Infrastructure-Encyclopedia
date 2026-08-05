# Volume CXLIV — Glossary

| Term | Definition |
|:---|:---|
| **ABAP Cloud** | The upgrade-safe subset of SAP's ABAP language: it may use only officially released APIs, which is exactly what makes code built on it survive quarterly updates. Uses RAP; the C_ABAPD exam adds Joule-assisted development. |
| **ACDOCA** | S/4HANA's Universal Journal — a single line-item table from which financial totals are computed in memory, replacing the many redundant aggregate tables ECC maintained and reconciled. |
| **Associate** | The fundamental SAP certification level (mostly `C_` codes): validates knowledge applied "under the guidance of an experienced consultant." No experience gate; the bulk of the catalog. |
| **Autonomous Enterprise** | SAP's AI-era operating model — five Autonomous Domains as an integrated system, the Business AI Platform's three pillars, and Joule agents versus assistants. The C_BCSBS positioning certification. |
| **BTP (Business Technology Platform)** | SAP's PaaS layer for development, integration, data, and AI — the place side-by-side extensions live so the ERP core stays clean and upgradeable. |
| **Clean core** | The principle that custom logic belongs beside the core (on BTP), calling it through released APIs, never modified into it — the architectural answer to the fit-gap technical debt that made ECC upgrades painful. |
| **ECC** | ERP Central Component — the predecessor to S/4HANA, database-agnostic with a heavier aggregate-table data model. |
| **Employee Central (EC)** | SuccessFactors' core HR module and system of record for people and positions; the foundational SF certification other modules build on. |
| **Fit-to-standard** | The cloud-era implementation approach: adopt SAP's standard best-practice processes, customizing only genuine competitive differentiators. "Adopt, don't adapt." Contrast with the customization-heavy fit-gap. |
| **GROW with SAP** | The transformation offer for *new* customers adopting S/4HANA Cloud Public Edition. (RISE is the existing-customer, Private-Edition counterpart.) |
| **HANA** | SAP's in-memory columnar database; S/4HANA runs only on it, and its in-memory model is what lets aggregates be computed on the fly rather than stored and reconciled. |
| **Joule** | SAP's generative-AI assistant. An *assistant* responds reactively to prompts; an *agent* pursues a goal autonomously across steps — the distinction the Autonomous Enterprise certification tests. |
| **Practical exam** | The 2026 SAP exam format: system-based tasks or roleplay scenarios, timeboxed, **open-book with AI tools allowed**, not live-proctored. Tests application over recall; cannot be crammed from a question bank. |
| **Professional** | The advanced SAP level (`P_`, some `E_`): requires **proven, recent project experience** (e.g. RISE Methodology needs 24 months of ERP work in the past 36) — a different claim from Associate, not just a harder test. |
| **RAP** | The RESTful Application Programming Model — the standardized way to build services and Fiori apps in ABAP Cloud. |
| **RISE with SAP** | The bundled transformation offer moving *existing* customers to S/4HANA Cloud Private Edition. The C_RISME certification is experience-gated because it certifies running these transformations. |
| **S/4HANA** | SAP's current-generation ERP suite, successor to ECC — HANA-only, with a simplified data model and the Fiori UI. Available as Cloud Public, Cloud Private, or on-premise. |
| **SAP Activate** | SAP's certified implementation methodology: phases Discover → Prepare → Explore → Realize → Deploy → Run. Explore, where fit-to-standard sets scope, is where projects are won or lost. |
| **Segregation of duties (SoD)** | The control preventing one user from holding a fraud-enabling capability combination (create-vendor + pay-vendor). Conflicts hide in role *combinations*; GRC Access Control scans for them continuously. |
| **Solution area** | The top-level SAP specialization fork — S/4HANA, SuccessFactors, BTP, Ariba, Analytics, AI/data — chosen first, because module, projects, and roles all follow from it. |
| **Specialist** | A certification level added on top of an Associate for a focused role or integration component (e.g. S/4HANA Conversion and System Upgrade). |
| **Stay-certified assessment** | The standard renewal SAP requires of already-certified professionals at expiration — distinct from the practical exams, which are required for first-time takers only. |
