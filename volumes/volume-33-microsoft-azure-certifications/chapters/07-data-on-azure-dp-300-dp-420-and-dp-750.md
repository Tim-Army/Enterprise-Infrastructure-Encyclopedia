# Chapter 07: Data on Azure — DP-300, DP-420, and DP-750

## Learning Objectives

- Map the Azure data certification track from DP-900 through the
  associate and specialty credentials that build on it
- Distinguish the Azure Database Administrator (DP-300), Cosmos DB
  Developer (DP-420), and Databricks Data Engineer (DP-750) roles
- Explain what the retirement of Azure Data Scientist (DP-100) leaves
  uncertified, and where the remaining data credentials sit
- Choose between relational and non-relational Azure data services from
  stated access patterns and consistency requirements
- Verify database configuration and performance from the CLI rather than
  by assumption

## Theory and Architecture

### The data track

| Certification | Exam | Level | Status |
| --- | --- | --- | --- |
| Azure Data Fundamentals | DP-900 | Fundamentals | Current |
| Azure Database Administrator | DP-300 | Associate | Current |
| Azure Databricks Data Engineer | DP-750 | Associate | Current (new) |
| Azure Cosmos DB Developer | DP-420 | Specialty | Current |
| Azure Data Scientist | DP-100 | Associate | **Retired** |

Verified against Microsoft Learn on **23 July 2026**. DP-900 is covered in
[Chapter 02](02-fundamentals-az-900-ai-901-and-dp-900.md); this chapter
takes the track from there.

### DP-300: the database administrator

The Azure Database Administrator role covers implementing and managing
operational aspects of cloud-native and hybrid data platforms built on
SQL Server and Azure SQL — provisioning and configuring, securing,
monitoring and optimizing performance, automating routine tasks, and
planning high availability and disaster recovery.

It is the closest data analogue to AZ-104: the operational,
keep-it-running credential. If your job title contains "DBA" and your
platform is Azure SQL, this is the certification that maps to it.

### DP-420: Cosmos DB developer

A **specialty** certification for designing and implementing applications
on Azure Cosmos DB — data modeling and partitioning for a distributed
NoSQL store, the consistency levels, request-unit provisioning and cost,
indexing policy, and the change feed.

Its defining subject is **partitioning**. Cosmos DB's performance and cost
behavior follow from partition-key choice more than from any other
decision, and a poor key cannot be fixed later without moving the data.
That single design decision is what the certification is really about.

### DP-750: Databricks data engineer

The newest data credential, covering implementing data-engineering
solutions **using Azure Databricks** — pipelines, transformation at scale,
and the lakehouse pattern.

Its arrival alongside the retirement of DP-100 is informative: Microsoft
is certifying **data engineering** — building the pipelines and platforms
that carry data — while stepping back from certifying **data science** —
building the models. That is a defensible read of where durable, teachable
skills sit.

### What DP-100's retirement leaves uncertified

The Azure Data Scientist certification is retired, along with its renewal
assessment. Model development, experiment tracking, and the MLOps surface
it covered now have no direct Azure-branded credential. Readers whose work
is model-building should note that:

- The **AI-centric associate tier** ([Chapter 06](06-the-ai-centric-associate-tier-ai-103-ai-200-and-ab-620.md))
  certifies building *applications and agents* on models, not training
  them.
- **DP-750** certifies the data engineering underneath.
- The gap between those two — data science proper — is currently
  uncertified in the Azure line.

That is worth stating plainly rather than papering over: not every
valuable skill has a current certification, and this is one of them.

### Relational or not: choosing by access pattern

The judgment DP-900 introduces and the associate exams test:

- **Azure SQL / SQL Managed Instance** — relational, strong consistency,
  rich querying and joins, transactional integrity. Choose when the data
  is relational and queries are varied and unpredictable.
- **Cosmos DB** — non-relational, globally distributable, single-digit
  millisecond reads at scale, tunable consistency. Choose when access
  patterns are known and narrow, scale is global, and latency is the
  binding constraint.

The trap is selecting Cosmos DB for scale while retaining relational
query expectations, then discovering that cross-partition queries are
expensive. Access pattern first, service second.

## Design Considerations

- **DP-300 for operations, DP-420 for a specific product, DP-750 for
  pipelines.** These are not a ladder; they are different jobs. Pick the
  one matching yours.
- **Treat partition-key design as the DP-420 exam.** If you can reason
  about partition keys, request units, and consistency trade-offs, most of
  the rest follows.
- **Do not look for a DP-100 replacement.** There is not one. Decide
  whether the uncertified data-science gap matters for your goals, and if
  it does, weigh non-Microsoft credentials or a portfolio instead.
- **Let consistency requirements drive the Cosmos DB decision.** Its five
  consistency levels trade latency and availability against staleness
  guarantees; a design that names "strong" everywhere has usually not read
  the cost.
- **DP-900 first if the data domain is new to you.** It is cheap, does not
  expire, and establishes whether the track suits you.

## Implementation and Automation

### Provisioning and inspecting an Azure SQL database

```bash
az group create --name rg-dp300-lab --location eastus
az sql server create -g rg-dp300-lab -n sqlsrv-dp300-$RANDOM \
  --admin-user labadmin --admin-password "$(openssl rand -base64 18)Aa1!"
```

```bash
# Verify the tier actually provisioned, rather than the tier intended
az sql db list -g rg-dp300-lab --server <SERVER_NAME> \
  --query '[].{name:name, tier:sku.tier, capacity:sku.capacity, status:status}' -o table
```

### Cosmos DB: create with an explicit partition key

```bash
az cosmosdb create -g rg-dp300-lab -n cosmos-dp420-$RANDOM --kind GlobalDocumentDB
```

```bash
# The partition key is the design decision — state it explicitly
az cosmosdb sql container create -g rg-dp300-lab \
  --account-name <ACCOUNT> --database-name labdb --name orders \
  --partition-key-path "/customerId" --throughput 400
```

### Reading the consistency level in force

```bash
az cosmosdb show -g rg-dp300-lab -n <ACCOUNT> \
  --query '{default:consistencyPolicy.defaultConsistencyLevel, maxLagSec:consistencyPolicy.maxIntervalInSeconds}' -o table
```

## Validation and Troubleshooting

- **Read the tier from the resource.** `sku.tier` states what is running
  and being billed; a deployment template states what was requested. When
  cost surprises appear, this is the first check.
- **Diagnose Cosmos DB cost through request units, not queries alone.** A
  query that reads across partitions consumes RUs disproportionately;
  RU consumption per operation is the signal that a partition key is
  wrong.
- **Confirm the consistency level explicitly.** Applications frequently
  assume the default without checking. The command above states it.
- **For DP-300, prove the recovery path.** A backup configuration that has
  never been restored from is unverified. Restore to a new database name
  and query it — that is the operationally meaningful test.
- **Distinguish throttling from failure.** Azure SQL and Cosmos DB both
  throttle rather than fail under load; an application seeing errors under
  pressure is often hitting a provisioned limit, not a fault.

## Security and Best Practices

- Never embed database credentials in application code or notebooks. Use
  Microsoft Entra ID authentication where the service supports it, and
  Key Vault otherwise.
- The generated admin password in the Implementation section is a lab
  convenience; production admin accounts should use Entra ID
  authentication with conditional access rather than SQL logins.
- Restrict data-plane access at the network layer — Private Endpoint
  (Chapter 04) for database services carrying sensitive data, rather than
  firewall rules on a public endpoint.
- Enable auditing and threat detection on Azure SQL in any environment
  holding real data; both are examinable and both are baseline practice.
- Delete lab databases promptly. Provisioned throughput on Cosmos DB bills
  continuously whether or not the container is queried — the single most
  common surprise cost in this chapter's subject area.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure Database Administrator Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-database-administrator-associate/) (DP-300)
- [Microsoft Certified: Azure Cosmos DB Developer Specialty](https://learn.microsoft.com/en-us/credentials/certifications/azure-cosmos-db-developer-specialty/) (DP-420)
- [Microsoft Certified: Azure Databricks Data Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/implementing-data-engineering-solutions-using-azure-databricks/) (DP-750)
- [Microsoft Certified: Azure Data Scientist Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-scientist/) (DP-100 — retired)
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 02](02-fundamentals-az-900-ai-901-and-dp-900.md) for DP-900.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name the current Azure data certifications and the role each serves.
2. What single design decision dominates DP-420, and why can it not be
   corrected later without moving data?
3. What does the retirement of DP-100 leave uncertified, and what does
   Microsoft still certify around that gap?
4. Give an access pattern that favors Cosmos DB and one that favors Azure
   SQL.
5. An application throttles under load. What do you check before
   concluding there is a fault?

## Hands-On Lab

These labs cover the exam-guide domains for the data track: **DP-300**
(Azure Database Administrator) and **DP-420** (Cosmos DB Developer) domain
by domain, and the newer **DP-750** (Databricks Data Engineer) at section
level. Each is a walkthrough with the runnable command and the expected
result. Mapping is in the
[volume README](../README.md#lab-coverage--data-on-azure).

**Cost note:** an Azure SQL Database (Basic tier) and a Cosmos DB
serverless account are the billable items — both minimal. Lab 7.16 deletes
everything.

**Prerequisites**

```bash
az group create --name rg-data-lab --location eastus
az configure --defaults group=rg-data-lab location=eastus
```

**Expected result:** `"provisioningState": "Succeeded"`.

### DP-300 Domain 1 — Plan and implement data platform resources (15–20%)

### Lab 7.1 — Deploy an Azure SQL Database and choose a tier

```bash
PW="$(openssl rand -base64 18)Aa1!"
az sql server create --name sqlsrv-dp300-$RANDOM --admin-user dbadmin --admin-password "$PW"
SRV=$(az sql server list --query "[0].name" -o tsv)
az sql db create --server "$SRV" --name db-dp300 --edition Basic
az sql db show --server "$SRV" --name db-dp300 --query "{name:name, tier:currentServiceObjectiveName, status:status}" -o table
```

**Expected result:** `db-dp300 Basic Online`. Basic is chosen for a lab;
GeneralPurpose/BusinessCritical/Hyperscale are selected by a stated
performance and HA requirement.

### Lab 7.2 — Configure a deployment and evaluate service tiers

```bash
az sql db list-editions --location eastus \
  --query "[?name=='BusinessCritical'].supportedServiceLevelObjectives[0].name" -o tsv | head -1
```

**Expected result:** a BusinessCritical SLO name. BusinessCritical adds
local SSD and built-in HA (always-on) — the tier for low-latency,
high-availability OLTP.

### DP-300 Domain 2 — Implement a secure environment (20–25%)

### Lab 7.3 — Configure the server firewall and authentication

```bash
az sql server firewall-rule create --server "$SRV" --name allow-azure \
  --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0
az sql server firewall-rule list --server "$SRV" --query "[].name" -o tsv
```

**Expected result:** `allow-azure` (0.0.0.0 = allow Azure services). Then
prefer Microsoft Entra authentication over SQL logins:

```bash
az sql server ad-admin list --server "$SRV" --query "[].login" -o tsv || echo "no Entra admin set"
```

**Expected result:** the Entra admin, or the note — Entra auth with
conditional access is the recommended posture.

### Lab 7.4 — Configure encryption and auditing

```bash
az sql db tde show --server "$SRV" --database db-dp300 --query "state" -o tsv
```

**Expected result:** `Enabled` — Transparent Data Encryption is on by
default. Auditing and Microsoft Defender for SQL are the detective
controls this domain adds.

### DP-300 Domain 3 — Monitor, configure, and optimize (20–25%)

### Lab 7.5 — Monitor database resources

```bash
az monitor metrics list --resource "$(az sql db show --server "$SRV" --name db-dp300 --query id -o tsv)" \
  --metric "dtu_consumption_percent" --query "value[0].timeseries[0].data[-1]" -o json 2>/dev/null | head -5 \
  || echo "metrics populate after activity"
```

**Expected result:** a DTU-consumption data point (or the note on a fresh
DB). DTU/vCore consumption is the signal for right-sizing — the
optimization skill.

### Lab 7.6 — Interpret performance and optimize

```bash
az sql db show --server "$SRV" --name db-dp300 \
  --query "{maxSize:maxSizeBytes, zoneRedundant:zoneRedundant}" -o table
```

**Expected result:** the size and zone-redundancy setting. Optimization is
reading these against the workload — an over-provisioned tier is a cost
finding, an under-provisioned one a throttling finding.

### DP-300 Domain 4 — Automation of tasks (15–20%)

### Lab 7.7 — Automate with elastic pools / policies

```bash
az sql elastic-pool create --server "$SRV" --name pool-dp300 --edition Basic 2>&1 | tail -2
az sql elastic-pool list --server "$SRV" --query "[].name" -o tsv
```

**Expected result:** `pool-dp300`. Elastic pools share capacity across
databases — the automation-and-cost lever for many small databases.

### DP-420 — Cosmos DB (data models 35–40%, optimize 15–20%, maintain 25–30%)

### Lab 7.8 — Create a Cosmos DB account and database *(integrate)*

```bash
COS="cosmos-dp420-$RANDOM"
az cosmosdb create --name "$COS" --kind GlobalDocumentDB --enable-free-tier false \
  --capabilities EnableServerless
az cosmosdb sql database create --account-name "$COS" --name appdb
az cosmosdb show --name "$COS" --query "{name:name, consistency:consistencyPolicy.defaultConsistencyLevel}" -o table
```

**Expected result:** the account with its default consistency level
(`Session`). Serverless suits spiky/dev workloads; provisioned throughput
suits steady load.

### Lab 7.9 — Design and implement a data model with a partition key *(data models, 35–40%)*

```bash
az cosmosdb sql container create --account-name "$COS" --database-name appdb \
  --name orders --partition-key-path "/customerId"
az cosmosdb sql container show --account-name "$COS" --database-name appdb \
  --name orders --query "resource.partitionKey.paths[0]" -o tsv
```

**Expected result:** `/customerId`. Partition-key choice is the single
dominant DP-420 decision — it governs performance and cost and cannot be
changed without moving data.

### Lab 7.10 — Data distribution and consistency *(distribution 5–10%)*

```bash
az cosmosdb show --name "$COS" \
  --query "{consistency:consistencyPolicy.defaultConsistencyLevel, maxLagSec:consistencyPolicy.maxIntervalInSeconds}" -o table
```

**Expected result:** the consistency level and any bounded-staleness lag.
The five levels trade latency/availability against staleness; global
distribution adds regions with per-region write options.

### Lab 7.11 — Optimize a Cosmos DB solution *(optimize 15–20%)*

```bash
az cosmosdb sql container show --account-name "$COS" --database-name appdb \
  --name orders --query "resource.indexingPolicy.indexingMode" -o tsv
```

**Expected result:** `consistent`. Indexing policy and request-unit (RU)
provisioning are the optimization levers — a cross-partition query burns
RUs disproportionately, which is the signal a partition key is wrong.

### Lab 7.12 — Maintain a Cosmos DB solution *(maintain 25–30%)*

```bash
az cosmosdb sql container update --account-name "$COS" --database-name appdb \
  --name orders --ttl 2592000
az cosmosdb sql container show --account-name "$COS" --database-name appdb \
  --name orders --query "resource.defaultTtl" -o tsv
```

**Expected result:** `2592000` (30 days). TTL, backup policy, and RU
scaling are the maintenance tasks; backup/restore is the durability
guarantee.

### DP-750 — Databricks Data Engineer (section level)

### Lab 7.13 — Databricks workspace and the lakehouse pattern

```bash
az provider show --namespace Microsoft.Databricks --query "registrationState" -o tsv 2>/dev/null \
  || echo "register Microsoft.Databricks"
```

**Expected result:** `Registered` or the note. DP-750 covers building
pipelines and the lakehouse (bronze/silver/gold) on Azure Databricks;
confirm the current guide, as this certification is new.

### Lab 7.14 — Storage foundation for the lakehouse

```bash
SA="stlake$RANDOM"
az storage account create --name "$SA" --sku Standard_LRS --kind StorageV2 \
  --enable-hierarchical-namespace true
az storage account show --name "$SA" --query "isHnsEnabled" -o tsv
```

**Expected result:** `true` — ADLS Gen2 (hierarchical namespace) is the
lakehouse storage layer Databricks reads and writes.

### Lab 7.15 — Negative test: prove TDE is enforced / firewall blocks

```bash
az sql db show --server "$SRV" --name db-dp300 --query "{tde:earliestRestoreDate}" -o tsv >/dev/null
az sql server firewall-rule delete --server "$SRV" --name allow-azure
az sql db show --server "$SRV" --name db-dp300 --query "status" -o tsv
```

**Expected result:** the DB is still `Online`, but with the firewall rule
gone, a client connection from Azure services is now refused at the network
layer — proving the firewall, not the database, controls reachability.
(Re-add the rule if you want to connect.)

### Lab 7.16 — Cleanup

```bash
az group delete --name rg-data-lab --yes --no-wait
az group exists --name rg-data-lab
```

**Expected result:** `false` shortly after — the SQL server, Cosmos
account, and storage accounts removed together. Cosmos provisioned
throughput and SQL databases bill continuously, so confirm deletion.

## Lab Verification

Complete this sign-off once both containers have been created, the
hot-partition reasoning verified, and the resource group deleted. Until
then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Azure data track runs from DP-900 through **DP-300** (database
administration — the operational, keep-it-running credential), **DP-420**
(Cosmos DB development, where partition-key design is effectively the
whole exam), and the new **DP-750** (Databricks data engineering). **DP-100
is retired**, which leaves data science proper uncertified in the Azure
line — Microsoft now certifies the engineering underneath models and the
applications built on them, but not model development itself. Choose
relational or non-relational from access patterns and consistency
requirements rather than from scale ambitions, and verify tiers,
request-unit consumption, and consistency levels from the resources
themselves.

- [ ] Can name the current data certifications and their roles.
- [ ] Can explain why partition-key choice dominates DP-420.
- [ ] Knows what DP-100's retirement leaves uncertified.
- [ ] Can choose between Cosmos DB and Azure SQL from an access pattern.
- [ ] Has demonstrated hot-partition reasoning against real metrics.
- [ ] Completed the hands-on lab, including cleanup and a cost check.
