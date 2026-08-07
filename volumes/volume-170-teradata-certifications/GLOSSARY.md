# Volume CLXX — Glossary

| Term | Definition |
|:---|:---|
| **AMP (Access Module Processor)** | A parallel worker in Teradata's MPP architecture — each AMP owns a portion of the data (its rows) and processes it (read/filter/join/aggregate) independently and in parallel with the others. More AMPs = more parallelism. |
| **BYNET** | Teradata's interconnect (message-passing layer) — lets the Parsing Engine and AMPs communicate and coordinate, distributing work and merging results, and redistributing data between AMPs when a join requires it. |
| **ClearScape Analytics** | Teradata's in-database analytics and machine learning — a library of analytic/ML functions run where the data lives on the parallel engine (no extraction), with in-database model training and scoring at scale. |
| **MPP (massively parallel processing)** | Teradata's architecture — divide data across many independent, shared-nothing processing units (AMPs) that each work their slice in parallel, then combine results; scales linearly by adding units. |
| **Optimizer** | The Parsing Engine's cost-based query planner — considers execution plans (join order/method, redistribution) and picks the estimated cheapest, depending on accurate statistics to choose well. |
| **Parsing Engine (PE)** | The front end of Teradata's MPP — parses a SQL request, checks security/syntax, optimizes it into an execution plan, and dispatches the parallel work to the AMPs over the BYNET. |
| **Partitioned Primary Index (PPI)** | A second level of organization within each AMP — rows partitioned (often by date range) so a filtered query scans only relevant partitions (partition elimination), reducing I/O on large time-series tables. |
| **Primary Index (PI)** | The most important Teradata concept — the column(s) whose hash determines which AMP each row lives on. It IS the data-distribution mechanism (not a side lookup), and also enables single-AMP access and join co-location. A high-cardinality PI distributes evenly; a low-cardinality one causes skew. |
| **QueryGrid** | Teradata's data fabric — lets Vantage query across other systems (other Teradata, data lakes, object storage, other engines) without physically moving the data first, combining data where it sits. |
| **Shared-nothing** | An architecture where each processing unit (AMP) has its own data, memory, and CPU and shares none — the basis of Teradata's linear MPP scalability (no shared bottleneck). |
| **Skew** | Uneven data distribution across AMPs — when a low-cardinality primary index piles most rows onto a few AMPs; queries then wait for the slowest (overloaded) AMP, crippling the MPP advantage. |
| **Spool space** | The working (temporary) space Teradata allocates a user for query intermediate results — a query needing more than its spool limit fails with "no more spool space," a classic DBA/space concern. |
| **Statistics** | Collected metadata about column data distribution (distinct values, skew, ranges) — the optimizer uses them to estimate row counts and choose good plans; stale/missing statistics cause slow queries. |
| **TASM** | Teradata Active System Management (and VantageCloud equivalents) — workload management that classifies requests into workloads, prioritizes them, and applies throttles/filters/exceptions so mixed workloads coexist fairly on the shared engine. |
| **Teradata Vantage** | Teradata's connected, multi-cloud data platform — the modern evolution of the data warehouse across clouds and on-premises, keeping the MPP analytics engine and adding cloud delivery, open formats, and in-database analytics. |
| **VantageCloud Lake** | The cloud-native, elastic, lakehouse-oriented edition of VantageCloud — separation of compute and storage, elastic scaling, object-storage-backed data; the flagship of the current certification track. |
| **VantageCloud Enterprise** | The full enterprise data warehouse delivered in the cloud — the complete, mature Teradata feature set and performance for demanding workloads. |
| **Co-located join** | A join where both tables are distributed on the join column (their primary index), so matching rows already sit on the same AMP — a local, fast join with no data movement (vs a redistributed join over the BYNET). |
