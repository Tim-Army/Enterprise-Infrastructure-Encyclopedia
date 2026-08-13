# Chapter 02: The Cloudera Data Platform (CDP)

## Learning Objectives

- Explain CDP as a hybrid data platform spanning on-premises and cloud.
- Describe the data lifecycle CDP covers and its open-source roots.
- Understand SDX — unified security and governance (Ranger, Atlas).
- Recognize the data services that make up the platform.

*Cert relevance: the CDP platform and SDX underpin every role certification — the shared foundation.*

## A hybrid data platform

The **Cloudera Data Platform (CDP)** is a **hybrid data platform** — it runs the same data management and analytics across **on-premises data centers and public clouds** (AWS, Azure, Google Cloud). This **hybrid** capability is Cloudera's signature: many data platforms are cloud-only, but Cloudera lets an organization run analytics **where the data lives**, including in its own data center (for data-gravity, sovereignty, latency, or cost reasons), and move workloads between on-prem and cloud with a **consistent platform**. CDP came from the **2019 merger of Cloudera and Hortonworks**, unifying their Hadoop-era platforms into one modern hybrid product. The lab models the hybrid model.

## The data lifecycle and open-source roots

CDP covers the **full data lifecycle** — **collect, enrich, report, serve, and predict** — on one platform, so data can flow from ingestion through analytics to machine learning without leaving it. It is built on **open-source** foundations: **Hadoop/HDFS** and **Ozone** (storage), **Spark** (processing), **Hive/Impala** (SQL), **NiFi** (data flow), **Kafka/Flink** (streaming), **Iceberg** (open table format), and **Ranger/Atlas** (security/governance). This open core means skills transfer — learning Cloudera teaches the open-source data stack the broader industry uses — and avoids lock-in to proprietary formats. The lab models the lifecycle.

## SDX: unified security and governance

A defining CDP feature is **SDX (Shared Data Experience)** — a **unified security and governance** layer that applies **consistently across all the data services**. Instead of each tool (warehouse, engineering, ML) having its own security model, SDX provides one:

- **Apache Ranger** — **access control**: fine-grained, policy-based authorization (who can read/write which tables, columns, rows) applied uniformly.
- **Apache Atlas** — **metadata and governance**: a catalog of data assets, **lineage** (where data came from and how it was transformed), and **classification** (tagging sensitive data).

SDX means you define security and governance **once** and it applies everywhere data is used — critical for compliance and for managing data at enterprise scale. This is a genuine differentiator: consistent governance across a hybrid, multi-service platform. The lab models SDX.

## The data services

On the CDP foundation run **data services**, each aligned to roles and chapters:

| Service | Purpose | Role |
|:---|:---|:---|
| **Cloudera Manager** | Cluster deployment, management, monitoring | [Administrator (Ch 3)](03-cloudera-administrator.md) |
| **Data Engineering** | Spark/Airflow pipelines | [Data Engineer (Ch 4)](04-cloudera-data-engineer.md) |
| **DataFlow / Stream Processing** | NiFi, Kafka, Flink | [Data Operator (Ch 5)](05-cloudera-data-operator.md) |
| **Data Warehouse** | Hive/Impala/Trino SQL analytics | [Data Analyst (Ch 6)](06-cloudera-data-analyst.md) |
| **Cloudera AI** (fka CML) | Notebooks, MLOps, model serving | [ML Engineer (Ch 7)](07-cloudera-machine-learning-engineer.md) |
| **Iceberg (lakehouse)** | Open transactional tables | [Lakehouse Engineer (Ch 8)](08-genai-lakehouse-generalist.md) |

One platform, one security model (SDX), many services — that is CDP. The lab synthesizes.

## Hands-On Lab

Python models SDX unified governance. **Cost:** none.

### Lab 2.1 — SDX applies one security model across all services

**Objective:** See consistent governance across the hybrid platform.

```bash
python3 - <<'EOF'
# SDX: one Ranger policy + Atlas lineage/classification applied across ALL data services
RANGER_POLICY = {"table": "customers", "column": "ssn",
                 "allow": {"role:compliance"}, "deny_default": True}
ATLAS = {"customers.ssn": {"classification": "PII", "lineage": "ingested from crm -> masked in warehouse"}}
SERVICES = ["Data Warehouse (Impala)", "Data Engineering (Spark)", "Cloudera AI (notebook)", "Data Analyst (Hive)"]

def can_access(service, user_roles):
    allowed = bool(RANGER_POLICY["allow"] & user_roles)
    return allowed

print("SDX = ONE security + governance model across ALL data services (hybrid on-prem+cloud):\n")
print(f"   Ranger policy: {RANGER_POLICY['table']}.{RANGER_POLICY['column']} -> allow {RANGER_POLICY['allow']}, else DENY")
print(f"   Atlas: {list(ATLAS.keys())[0]} classified {ATLAS['customers.ssn']['classification']},")
print(f"          lineage = {ATLAS['customers.ssn']['lineage']}\n")
print("   The SAME policy enforced no matter which service touches the data:")
for svc in SERVICES:
    analyst = can_access(svc, {"role:analyst"})
    compliance = can_access(svc, {"role:compliance"})
    print(f"      {svc:30} analyst={'ALLOW' if analyst else 'DENY '}  compliance={'ALLOW' if compliance else 'DENY'}")
print("\nThe SDX insight: define security + governance ONCE (Ranger access + Atlas lineage/")
print("classification) and it applies EVERYWHERE data is used — warehouse, engineering, ML,")
print("analysis, on-prem or cloud. Without it, each tool has its OWN security model = gaps +")
print("inconsistency + compliance nightmares. Consistent governance across a HYBRID,")
print("MULTI-SERVICE platform is a Cloudera differentiator, and the foundation under every role.")
EOF
```

**Expected result:** One Ranger policy and Atlas classification/lineage for `customers.ssn` enforced identically across the Data Warehouse, Data Engineering, Cloudera AI, and analyst services — the analyst denied, compliance allowed, everywhere. The SDX lesson is that Cloudera defines security and governance once and applies it across all data services and both on-prem and cloud, avoiding the gaps and inconsistency of per-tool security models — the platform foundation under every role certification.

**Negative test:** Securing each data tool separately with its own access model. Policies drift, gaps appear at the seams, and lineage is lost; SDX enforces one Ranger/Atlas model across every service and deployment.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] CDP understood as a hybrid data platform spanning on-premises and public cloud.
- [ ] The data lifecycle (collect → predict) and open-source roots (Spark, Iceberg, NiFi, Kafka) understood.
- [ ] SDX understood — unified security (Ranger) and governance (Atlas) across all data services.
- [ ] The data services (Manager, Data Engineering, DataFlow, Warehouse, Cloudera AI, Iceberg) placed against the roles.
