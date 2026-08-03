# Chapter 06: Data and Analytics Certifications

## Learning Objectives

- Enumerate the current DP-family certifications and exam codes.
- Explain the shift to Microsoft Fabric (DP-700, DP-600) and where DP-203 went.
- Distinguish the data engineer, analyst, scientist, and database roles.
- Recognize the newer DP additions — Databricks (DP-750) and AI-enabled databases (DP-800).
- Build a study path for a data engineer or analyst role.

## Theory and Architecture

The **DP** family certifies data roles across **Microsoft Fabric**, **Azure
databases**, and **Power BI**. The big recent shift is **Microsoft Fabric**,
the unified analytics platform that absorbed much of what used to be separate
Azure Synapse and Data Factory certification scope. As verified on Microsoft
Learn (26 July 2026):

- **Microsoft Certified: Azure Data Fundamentals** — exam **DP-900**
  (Fundamentals). Core data concepts and Azure/Fabric data services.
- **Microsoft Certified: Fabric Data Engineer Associate** — exam **DP-700**
  (Associate). Ingest, transform, and serve data in Microsoft Fabric. This is
  the successor to the retired **DP-203** (Azure Data Engineer).
- **Microsoft Certified: Fabric Analytics Engineer Associate** — exam
  **DP-600** (Associate). Design and build analytics solutions in Fabric,
  including semantic models and Power BI.
- **Microsoft Certified: Azure Database Administrator Associate** — exam
  **DP-300** (Associate). Manage SQL Server and Azure SQL databases.
- **Microsoft Certified: Azure Cosmos DB Developer Specialty** — exam
  **DP-420** (Specialty). Build applications on Azure Cosmos DB.
- **Microsoft Certified: Azure Data Scientist Associate** — exam **DP-100**
  (Associate). Machine learning with Azure Machine Learning.
- **Microsoft Certified: Azure Databricks Data Engineer Associate** — exam
  **DP-750** (Associate). Data engineering on Azure Databricks — a newer
  credential reflecting the Databricks partnership.
- A newer **AI-enabled database solutions** credential — exam **DP-800** —
  bridging databases and generative AI.

**Power BI Data Analyst (PL-300)** lives in the Power Platform family
(Chapter 04) but belongs to any data professional's toolkit.

## Design Considerations

Lead with **DP-900** for the vocabulary, then choose by role. **Data
engineers** target **DP-700** (Fabric) — and note that if a study plan cites
**DP-203**, it is out of date; Fabric's DP-700 replaced it. **Analytics
engineers** take **DP-600** and typically **PL-300** for Power BI depth.
**Database administrators** take **DP-300**; **Cosmos DB** developers take the
**DP-420** specialty; and **data scientists** take **DP-100**. The newer
**DP-750** (Databricks) and **DP-800** (AI-enabled databases) reflect where
the platform is heading — lakehouse engineering and database-plus-GenAI.

Because Fabric, Power BI, and AI overlap, plan across families: an analytics
engineer might hold **DP-600 + PL-300**, and a data-plus-AI engineer might add
**DP-800** or the AI family's data-science credentials (Chapter 07).

## Implementation and Automation

Verify the Fabric shift and newer additions from Microsoft Learn:

```bash
for slug in azure-data-fundamentals fabric-data-engineer-associate fabric-analytics-engineer-associate \
            azure-database-administrator-associate azure-cosmos-db-developer-specialty azure-data-scientist \
            implementing-data-engineering-solutions-using-azure-databricks; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bDP-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# fabric-data-engineer-associate -> DP-700 (replaced DP-203)
# ...-azure-databricks -> DP-750
```

## Validation and Troubleshooting

Map credentials to roles:

| Credential | Exam | Tier | Role |
| --- | --- | --- | --- |
| Azure Data Fundamentals | DP-900 | Fundamentals | Gateway |
| Fabric Data Engineer | DP-700 | Associate | Data engineer (ex-DP-203) |
| Fabric Analytics Engineer | DP-600 | Associate | Analytics engineer |
| Azure Database Administrator | DP-300 | Associate | DBA |
| Azure Cosmos DB Developer | DP-420 | Specialty | NoSQL developer |
| Azure Data Scientist | DP-100 | Associate | Data scientist |
| Azure Databricks Data Engineer | DP-750 | Associate | Lakehouse engineer |
| AI-enabled database solutions | DP-800 | Associate | Data + GenAI |

Common pitfalls: studying **DP-203** (retired — Fabric's **DP-700** is
current); confusing **DP-600** (analytics engineering) with **DP-700** (data
engineering) — they are distinct Fabric roles; and missing the newer
**DP-750** and **DP-800**. As always, confirm on Learn — the data family has
moved fastest of all into Fabric and AI.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
practice in a **Microsoft Fabric trial** and **Azure** free account. Verify
the **Fabric transition** (DP-700 over DP-203) and the newer **DP-750/DP-800**
before planning. Pair analytics credentials with **PL-300** (Power BI) and
data-science credentials with the **AI** family (Chapter 07). Renew annually
through the free assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for DP-900, DP-700, DP-600, DP-300, DP-420, DP-100, DP-750, DP-800.
- Cross-reference: [Chapter 07 — AI and Copilot](07-ai-and-copilot-certifications.md); [Volume XXXIII](../../volume-033-microsoft-azure-certifications/README.md).

**Knowledge checks**

1. Which Fabric exam replaced the retired DP-203, and what role does it certify?
2. How do DP-600 and DP-700 differ?
3. What do the newer DP-750 and DP-800 reflect about the platform?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted "skills measured" domain**
of the Data and Analytics family (DP-900, DP-700, DP-600, DP-300, DP-420,
DP-100, DP-750, DP-800).

**Shared prerequisites** — an **Azure subscription** with the **Azure CLI**
(`az login`), plus a **Microsoft Fabric** capacity for the DP-700/DP-600 labs
and an **Azure Machine Learning** workspace for DP-100. SQL/KQL/Spark/Python are
shown as illustrative snippets. **Cost:** small — use free tiers/trial capacity
and delete resources after each lab.

### Lab 6.1 — DP-900: Describe core data concepts (25–30%)

**Objective:** Distinguish structured, semi-structured, and unstructured data.

```text
Structured  -> tables (SQL)         e.g., Azure SQL
Semi        -> JSON/Parquet         e.g., Cosmos DB, Data Lake
Unstructured-> files/blobs/media    e.g., Blob Storage
```

**Expected result:** the three data categories mapped to Azure stores — the core
data concepts DP-900 covers.

**Negative test:** force unstructured media into relational rows; use object
storage and metadata instead.

**Cleanup:** none.

### Lab 6.2 — DP-900: Identify considerations for relational data on Azure (20–25%)

**Objective:** List Azure SQL relational offerings.

```bash
az sql server list --query "[].{name:name,location:location}" -o table
```

**Expected result:** Azure SQL logical servers (or an empty list) — the
relational PaaS options (SQL Database, Managed Instance).

**Negative test:** run a lift-and-shift app needing SQL Agent on single SQL
Database; use Managed Instance for instance-level features.

**Cleanup:** none.

### Lab 6.3 — DP-900: Describe considerations for working with non-relational data on Azure (15–20%)

**Objective:** List non-relational stores.

```bash
az cosmosdb list --query "[].{name:name,kind:kind}" -o table
```

**Expected result:** Cosmos DB accounts (or empty) — the non-relational/NoSQL
option and its APIs (NoSQL, MongoDB, Cassandra, Gremlin, Table).

**Negative test:** model highly relational data in Cosmos DB with cross-partition
joins; denormalize for the access pattern instead.

**Cleanup:** none.

### Lab 6.4 — DP-900: Describe an analytics workload (25–30%)

**Objective:** Map the modern analytics flow.

```text
Ingest -> Store (Lakehouse/OneLake) -> Transform (Spark/SQL) -> Model -> Serve (Power BI)
Batch vs streaming; Microsoft Fabric unifies these
```

**Expected result:** the ingest-to-serve analytics pipeline — the workload
DP-900 describes.

**Negative test:** query the raw lake for every dashboard; serve from a modeled
semantic layer.

**Cleanup:** none.

### Lab 6.5 — DP-700: Implement and manage an analytics solution (30–35%)

**Objective:** Identify Fabric workspace/lakehouse items.

```text
Fabric workspace -> Lakehouse (OneLake) | Warehouse | KQL Database | Data pipelines
Manage via workspace roles; capacity assigned to the workspace
```

**Expected result:** the Fabric item types and workspace/capacity model — the
solution DP-700 implements.

**Negative test:** assign no capacity to a workspace; Fabric items need a
capacity to run.

**Cleanup:** none.

### Lab 6.6 — DP-700: Ingest and transform data (30–35%)

**Objective:** Transform data with a Spark snippet in a Lakehouse notebook.

```python
df = spark.read.format("csv").option("header", True).load("Files/raw/sales.csv")
df = df.dropna().withColumn("amount", df["amount"].cast("double"))
df.write.mode("overwrite").format("delta").saveAsTable("sales_clean")
```

**Expected result:** a cleaned Delta table `sales_clean` in the Lakehouse — ingest
and transform.

**Negative test:** write CSV instead of Delta for the curated layer; Delta gives
ACID and time travel.

**Cleanup:** drop the table.

### Lab 6.7 — DP-700: Monitor and optimize an analytics solution (30–35%)

**Objective:** Use the monitoring hub / capacity metrics concept.

```text
Monitoring hub: pipeline/notebook run history, durations, failures
Optimize: V-Order, partitioning, table maintenance (OPTIMIZE/VACUUM)
```

**Expected result:** the run-history and optimization levers — monitoring and
tuning a Fabric solution.

**Negative test:** never run OPTIMIZE/VACUUM on a growing Delta table; small
files degrade query performance.

**Cleanup:** none.

### Lab 6.8 — DP-600: Maintain a data analytics solution (25–30%)

**Objective:** Manage workspace source control and deployment (ALM).

```text
Fabric Git integration (workspace <-> Azure DevOps/GitHub)
Deployment pipelines: Dev -> Test -> Prod stages
```

**Expected result:** Git integration and deployment stages — maintaining an
analytics solution.

**Negative test:** edit prod artifacts directly; promote through the deployment
pipeline.

**Cleanup:** none.

### Lab 6.9 — DP-600: Prepare data (45–50%)

**Objective:** Prepare data with SQL in a Fabric Warehouse (the top domain).

```sql
CREATE TABLE dbo.sales_clean AS
SELECT CustomerId, CAST(Amount AS decimal(18,2)) AS Amount
FROM dbo.sales_raw
WHERE Amount IS NOT NULL;
```

**Expected result:** a typed, filtered table — the data-preparation core of
DP-600.

**Negative test:** analyze `sales_raw` directly; nulls/wrong types corrupt
measures.

**Cleanup:** `DROP TABLE dbo.sales_clean;`.

### Lab 6.10 — DP-600: Implement and manage semantic models (25–30%)

**Objective:** Define a semantic-model measure (DAX) on the warehouse.

```text
Total Sales = SUM('sales_clean'[Amount])
Model: relationships (star schema), row-level security roles
```

**Expected result:** a semantic-model measure and star-schema note — the
serving layer DP-600 manages.

**Negative test:** build a snowflake with many-to-many everywhere; a star schema
performs and models better.

**Cleanup:** none.

### Lab 6.11 — DP-300: Plan and implement data platform resources (15–20%)

**Objective:** Provision an Azure SQL logical server + database.

```bash
az sql server create -n labsql$RANDOM -g rg-lab -l eastus -u sqladmin -p 'P@ssw0rd2026!'
az sql db create -g rg-lab -s <server> -n labdb --service-objective S0
```

**Expected result:** a logical server and an S0 database — deploying data
platform resources.

**Negative test:** open the SQL firewall to 0.0.0.0/0; restrict to known IPs or
use Private Link.

**Cleanup:** `az sql db delete -g rg-lab -s <server> -n labdb -y`.

### Lab 6.12 — DP-300: Implement a secure environment (20–25%)

**Objective:** Enable Entra-only authentication and auditing (illustrative).

```bash
az sql server ad-only-auth enable -g rg-lab -n <server>
az sql db audit-policy update -g rg-lab -s <server> -n labdb --state Enabled
```

**Expected result:** Entra-only auth and auditing enabled — securing the SQL
environment.

**Negative test:** rely on SQL logins alone; prefer Entra authentication and
disable local admins where possible.

**Cleanup:** revert as needed.

### Lab 6.13 — DP-300: Monitor, configure, and optimize database resources (20–25%)

**Objective:** Read query performance insight / DTU usage.

```sql
SELECT TOP 5 query_id, avg_duration
FROM sys.query_store_runtime_stats ORDER BY avg_duration DESC;
```

**Expected result:** the slowest queries by average duration — the tuning input
DP-300 optimizes.

**Negative test:** scale up compute to fix a missing index; tune the query/index
first.

**Cleanup:** none.

### Lab 6.14 — DP-300: Configure and manage automation of tasks (15–20%)

**Objective:** Schedule maintenance via Elastic Jobs / automation.

```text
Elastic Jobs (Azure SQL) or SQL Agent (Managed Instance) for scheduled tasks
Automate index/statistics maintenance and backups (built-in for PaaS)
```

**Expected result:** the automation options — scheduling maintenance in Azure
SQL.

**Negative test:** script manual nightly maintenance on single SQL Database
(no Agent); use Elastic Jobs.

**Cleanup:** none.

### Lab 6.15 — DP-300: Plan and configure a high availability and disaster recovery (HA/DR) environment (20–25%)

**Objective:** Configure a geo-replication/failover group.

```bash
az sql failover-group create -n labfg -g rg-lab -s <primary-server> --partner-server <secondary-server> --add-db labdb
```

**Expected result:** an auto-failover group across regions — HA/DR for Azure SQL.

**Negative test:** rely on local redundancy for regional outages; geo-replication
protects against region failure.

**Cleanup:** `az sql failover-group delete -n labfg -g rg-lab -s <primary-server>`.

### Lab 6.16 — DP-420: Design and implement data models (35–40%)

**Objective:** Choose a partition key for a Cosmos DB container (the top domain).

```bash
az cosmosdb sql container create -a <acct> -g rg-lab -d appdb -n orders --partition-key-path "/customerId" --throughput 400
```

**Expected result:** a container partitioned by `/customerId` — the model design
that drives Cosmos DB scale.

**Negative test:** pick a low-cardinality partition key (e.g., country); it
creates hot partitions.

**Cleanup:** `az cosmosdb sql container delete -a <acct> -g rg-lab -d appdb -n orders -y`.

### Lab 6.17 — DP-420: Design and implement data distribution (5–10%)

**Objective:** Add a read region for global distribution.

```bash
az cosmosdb update -n <acct> -g rg-lab --locations regionName=eastus failoverPriority=0 --locations regionName=westus failoverPriority=1
```

**Expected result:** a multi-region account — global data distribution.

**Negative test:** enable multi-region writes and ignore conflict resolution;
define a conflict-resolution policy.

**Cleanup:** revert to a single region.

### Lab 6.18 — DP-420: Integrate an Azure Cosmos DB solution (5–10%)

**Objective:** Enable the change feed for event-driven integration.

```text
Change feed -> Azure Functions Cosmos DB trigger -> downstream processing
Analytical store + Synapse Link for HTAP analytics
```

**Expected result:** the change-feed integration pattern — connecting Cosmos DB
to compute/analytics.

**Negative test:** poll the container for changes; use the change feed instead.

**Cleanup:** none.

### Lab 6.19 — DP-420: Optimize an Azure Cosmos DB solution (15–20%)

**Objective:** Read the request-unit (RU) cost of a query.

```text
Query metrics -> RU charge per operation; indexing policy tuning
Optimize: point reads (id + partition key) are cheapest (~1 RU)
```

**Expected result:** the RU-cost view — optimizing throughput and cost.

**Negative test:** cross-partition fan-out queries at scale; design for
single-partition access.

**Cleanup:** none.

### Lab 6.20 — DP-420: Maintain an Azure Cosmos DB solution (25–30%)

**Objective:** Configure backup/restore and TTL.

```bash
az cosmosdb sql container update -a <acct> -g rg-lab -d appdb -n orders --ttl 2592000
```

**Expected result:** a 30-day TTL on items — data-lifecycle maintenance.

**Negative test:** rely on default periodic backup for point-in-time needs;
enable continuous backup for PITR.

**Cleanup:** remove the TTL.

### Lab 6.21 — DP-100: Design and prepare a machine learning solution (20–25%)

**Objective:** Provision/inspect an Azure ML workspace and compute.

```bash
az ml workspace show -n <workspace> -g rg-lab --query "{name:name,location:location}"
az ml compute list -w <workspace> -g rg-lab -o table
```

**Expected result:** the workspace and its compute targets — the ML environment
DP-100 designs.

**Negative test:** train on a tiny local VM for a large job; provision scalable
compute clusters.

**Cleanup:** none.

### Lab 6.22 — DP-100: Explore data, and run experiments (20–25%)

**Objective:** Explore a dataset with pandas (experimentation).

```python
import pandas as pd
df = pd.read_csv("titanic.csv")
print(df.describe(include="all").T.head())
```

**Expected result:** summary statistics per column — the data exploration that
precedes modeling.

**Negative test:** train before exploring; unseen skew/missingness wrecks the
model.

**Cleanup:** none.

### Lab 6.23 — DP-100: Train and deploy models (25–30%)

**Objective:** Submit a training job with the Azure ML CLI (v2).

```bash
az ml job create -f train-job.yml -w <workspace> -g rg-lab
az ml online-endpoint create -n lab-ep -w <workspace> -g rg-lab
```

**Expected result:** a submitted training job and an online endpoint — train and
deploy.

**Negative test:** deploy a model with no signature/environment pinned;
reproducibility requires a versioned environment.

**Cleanup:** `az ml online-endpoint delete -n lab-ep -w <workspace> -g rg-lab -y`.

### Lab 6.24 — DP-100: Optimize language models for AI applications (25–30%)

**Objective:** Optimize an LLM via prompt flow / fine-tuning concepts.

```text
Prompt flow: prompt -> grounding (RAG) -> evaluation metrics (groundedness, relevance)
Fine-tune only when prompting/RAG is insufficient; track with MLflow
```

**Expected result:** the RAG-then-fine-tune decision path with evaluation — the
newest DP-100 domain.

**Negative test:** fine-tune first for knowledge freshness; use RAG for changing
facts.

**Cleanup:** none.

### Lab 6.25 — DP-750: Set up and configure an Azure Databricks environment (15–20%)

**Objective:** Create a Databricks workspace/cluster.

```bash
az databricks workspace create -n lab-adb -g rg-lab -l eastus --sku premium
```

**Expected result:** a premium Databricks workspace — the environment DP-750 sets
up (clusters, pools, policies).

**Negative test:** use the Standard SKU expecting Unity Catalog/RBAC; those need
Premium.

**Cleanup:** `az databricks workspace delete -n lab-adb -g rg-lab -y`.

### Lab 6.26 — DP-750: Secure and govern Unity Catalog objects (15–20%)

**Objective:** Grant on a Unity Catalog object (governance).

```sql
GRANT SELECT ON TABLE main.sales.orders TO `data-analysts`;
```

**Expected result:** a table grant to a group — Unity Catalog governance
(catalog → schema → table).

**Negative test:** manage access per-workspace instead of via Unity Catalog;
governance is centralized in UC.

**Cleanup:** `REVOKE SELECT ON TABLE main.sales.orders FROM \`data-analysts\`;`.

### Lab 6.27 — DP-750: Prepare and process data (30–35%)

**Objective:** Process data with PySpark (the largest domain).

```python
df = spark.read.table("main.sales.orders")
agg = df.groupBy("region").sum("amount")
agg.write.mode("overwrite").saveAsTable("main.sales.by_region")
```

**Expected result:** an aggregated Delta table — prepare/process at scale.

**Negative test:** collect a huge DataFrame to the driver; aggregate in Spark and
write back.

**Cleanup:** drop the table.

### Lab 6.28 — DP-750: Deploy and maintain data pipelines and workloads (30–35%)

**Objective:** Define a Databricks Job / DLT pipeline (orchestration).

```text
Workflows (Jobs): tasks + dependencies + schedule/trigger
Delta Live Tables (DLT): declarative pipelines with expectations (data quality)
```

**Expected result:** the Jobs/DLT orchestration model — deploying and maintaining
pipelines.

**Negative test:** chain notebooks by hand; use Workflows for dependencies and
retries.

**Cleanup:** none.

### Lab 6.29 — DP-800: Design and develop database solutions (35–40%)

**Objective:** Design a schema with constraints (the top domain).

```sql
CREATE TABLE dbo.Orders (
  Id int IDENTITY PRIMARY KEY,
  CustomerId int NOT NULL,
  Total decimal(18,2) CHECK (Total >= 0)
);
```

**Expected result:** a constrained relational schema — designing the database
solution.

**Negative test:** omit constraints to "speed development"; constraints protect
integrity.

**Cleanup:** `DROP TABLE dbo.Orders;`.

### Lab 6.30 — DP-800: Secure, optimize, and deploy database solutions (35–40%)

**Objective:** Add an index and check the plan (optimize/secure).

```sql
CREATE INDEX ix_orders_customer ON dbo.Orders(CustomerId);
-- Then review the estimated plan for a CustomerId filter
```

**Expected result:** an index supporting a filter — optimizing the solution;
pair with least-privilege grants for security.

**Negative test:** index every column; write amplification hurts inserts —
index to the workload.

**Cleanup:** `DROP INDEX ix_orders_customer ON dbo.Orders;`.

### Lab 6.31 — DP-800: Implement AI capabilities in database solutions (25–30%)

**Objective:** Add a vector column for AI similarity search.

```sql
-- SQL Server 2025 / Azure SQL vector support
ALTER TABLE dbo.Docs ADD Embedding vector(1536);
-- Query: ORDER BY vector_distance('cosine', Embedding, @query)
```

**Expected result:** a vector column and a cosine-distance query — the new
AI-in-database domain (embeddings/RAG in SQL).

**Negative test:** store embeddings as JSON strings and compute distance in the
app; use native vector types/indexes.

**Cleanup:** `ALTER TABLE dbo.Docs DROP COLUMN Embedding;`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The DP family runs DP-900 (Fundamentals), the Fabric pair DP-700 (Data
Engineer, replacing DP-203) and DP-600 (Analytics Engineer), DP-300 (DBA),
DP-420 (Cosmos DB Specialty), DP-100 (Data Scientist), and the newer DP-750
(Databricks) and DP-800 (AI-enabled databases). Power BI depth comes from
PL-300. The family has moved decisively into Fabric and AI.

- [ ] I can list the DP credentials and exam codes.
- [ ] I know DP-700 replaced DP-203 and how DP-600 differs.
- [ ] I recognize the newer DP-750 and DP-800.
- [ ] I can build a data-engineering study path on Fabric.
- [ ] I completed Labs 6.1–6.2 including each negative test.
