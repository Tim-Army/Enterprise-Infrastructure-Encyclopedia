# Volume XLIX Glossary

Definitions for terms used in **Volume XLIX — Snowflake Certification Tracks**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**AI Data Cloud** — Snowflake's branding for its platform: elastic storage and
compute plus native AI (Cortex). Used in Chapter 01.

**Cloning (zero-copy)** — Creating an instant, storage-free copy of a table,
schema, or database that shares micro-partitions until changed. Used in Chapters
03 and 04.

**COPY INTO** — The Snowflake command that bulk-loads staged files into a table
(and unloads results back to a stage). Used in Chapter 03.

**Cortex** — Snowflake's native AI: SQL functions for LLM completion, sentiment,
forecasting, anomaly detection, and classification. Used in Chapters 06 and 07.

**Micro-partition** — The immutable, columnar storage unit Snowflake automatically
divides tables into; the basis for pruning and cloning. Used in Chapter 03.

**Resource monitor** — An account object that tracks warehouse credit usage and
triggers notify/suspend actions at defined thresholds. Used in Chapter 08.

**Snowpark** — Snowflake's developer framework (Python/Java/Scala) whose DataFrame
operations are pushed down to Snowflake compute. Used in Chapters 05 and 07.

**Snowpipe** — Snowflake's continuous, serverless data-ingestion service that loads
new files as they arrive. Used in Chapter 05.

**SnowPro Advanced** — The role-based expert tier (Architect, Data Engineer, Data
Analyst, Data Scientist, Administrator); each requires SnowPro Core. Used in
Chapters 04–08.

**SnowPro Core (COF-C03)** — The foundational Snowflake certification required
before any Advanced exam. Used in Chapter 03.

**Stage** — A named location (internal or external cloud storage) where files sit
for loading/unloading with `COPY INTO`. Used in Chapter 03.

**Stream** — A Snowflake object that records change data (inserts/updates/deletes)
on a table for incremental processing. Used in Chapter 05.

**Task** — A scheduled or dependency-chained unit of SQL execution used to build
pipelines (task graphs/DAGs). Used in Chapter 05.

**Time Travel** — Querying or restoring historical data as of a past point within
the retention window. Used in Chapters 03 and 04.

**VARIANT** — Snowflake's semi-structured data type (JSON/Avro/etc.), queried with
path notation and `LATERAL FLATTEN`. Used in Chapters 03 and 06.

**Virtual warehouse** — Snowflake's elastic compute cluster, sized and scaled
independently of storage. Used in Chapters 01 and 03.

**Window function** — A SQL function computing values across a partition of rows
(e.g., running totals, `RANK() OVER (...)`). Used in Chapter 06.
