# Volume XLVIII Glossary

Definitions for terms used in **Volume XLVIII — Databricks Certification Tracks**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Accreditation** — A free Databricks badge/assessment (Fundamentals, Platform
Architect/Administrator), distinct from a proctored certification. Used in Chapter
01.

**Auto Loader** — Databricks' incremental file-ingestion mechanism (`cloudFiles`)
that tracks new files via a checkpoint. Used in Chapter 03.

**Context Engineer** — A Databricks credential for designing the context
(retrieval, tools, memory) that AI agent systems act on. Used in Chapter 07.

**Databricks Asset Bundle (DAB)** — A declarative, versioned way to define and
deploy Databricks jobs/pipelines across environments (CI/CD). Used in Chapter 04.

**Delta Lake** — The ACID table format underpinning the lakehouse (MERGE, time
travel, OPTIMIZE). Used in Chapters 03 and 04.

**Feature Store / Feature Engineering** — Governed feature tables reused across
training and serving to prevent skew. Used in Chapter 05.

**Lakehouse** — Databricks' unified architecture combining a data lake and
warehouse; the Data Intelligence Platform. Used in Chapter 01.

**Medallion architecture** — The bronze (raw) → silver (cleaned) → gold (curated)
data-layering pattern. Used in Chapter 03.

**MLflow** — The open-source platform for experiment tracking, the model registry,
and model lifecycle on Databricks. Used in Chapters 05 and 06.

**Model Serving** — Databricks' managed real-time inference endpoints for
registered models. Used in Chapter 06.

**Mosaic AI** — Databricks' AI suite, including Vector Search, the Agent Framework,
and Model Serving for GenAI. Used in Chapter 07.

**RAG (Retrieval-Augmented Generation)** — Grounding LLM answers with retrieved
context (via Mosaic AI Vector Search on Databricks). Used in Chapter 07.

**SCD Type 2** — A slowly-changing-dimension pattern that preserves history by
closing old rows and inserting new current ones. Used in Chapter 04.

**SQL warehouse** — Databricks SQL compute for analytics and dashboards. Used in
Chapter 02.

**Unity Catalog** — Databricks' governance layer with the `catalog.schema.table`
namespace, grants, and dynamic views. Used in Chapters 01, 03, and 04.

**Window function** — A SQL function computing values across a partition of rows
(e.g., `RANK() OVER (...)`). Used in Chapter 02.
