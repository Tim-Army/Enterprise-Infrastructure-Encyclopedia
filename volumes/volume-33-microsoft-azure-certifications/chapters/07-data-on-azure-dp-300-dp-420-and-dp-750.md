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

**Objective:** Provision both a relational and a non-relational data
service, then demonstrate that partition-key choice — not service choice —
governs Cosmos DB behavior.

**Cost note:** Azure SQL and Cosmos DB both bill while provisioned. Use the
smallest tiers, and complete step 6 in the same session. Provisioned
throughput is charged even when idle.

**Prerequisites**

- The sandbox subscription and budget alert from Chapter 01.
- Azure CLI authenticated.

**Steps**

1. **Provision (20 minutes).** Create the resource group, a SQL server and
   database at the smallest tier, and a Cosmos DB account.

   **Expected result:** both exist; `az sql db list` reports the tier
   actually provisioned.

2. **Create a well-partitioned container (10 minutes).** Create the
   `orders` container with `/customerId` as the partition key.

   **Expected result:** the container exists with the stated key.

3. **Create a badly partitioned container (10 minutes).** Create a second
   container using a low-cardinality key — for example `/country` — with
   the same throughput.

   **Expected result:** both containers exist and look identical in the
   portal, which is the point: the difference is invisible until load.

4. **Negative test (15 minutes).** Reason through, in writing, what
   happens to each container as one country or one customer dominates
   traffic. Then confirm your reasoning against the request-unit and
   partition metrics Azure exposes for the account.

   **Expected result:** a correct account of hot-partition behavior — the
   low-cardinality key concentrates load on one physical partition and
   throttles while the account as a whole appears under-utilized.

5. **Verify consistency (5 minutes).** Read the account's consistency
   level with the command above and state what staleness it permits.

   **Expected result:** the level named and its guarantee stated in your
   own words.

6. **Cleanup:**

   ```bash
   az group delete --name rg-dp300-lab --yes --no-wait
   ```

   Confirm the group is gone and check the budget — provisioned throughput
   is the item to watch.

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
