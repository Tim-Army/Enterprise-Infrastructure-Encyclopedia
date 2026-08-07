# Chapter 08: ClearScape Analytics and the Modern Platform

## Learning Objectives

- Describe ClearScape Analytics — in-database analytics and machine learning.
- Explain QueryGrid — the data fabric connecting systems.
- Understand the lakehouse, open formats, and language integration.
- Recognize Teradata's positioning for modern analytics and AI.

*Cert relevance: ClearScape Analytics and the modern platform features shape the current VantageCloud certifications.*

## ClearScape Analytics

Teradata is not just a query engine — it runs **analytics and machine learning in the database** through **ClearScape Analytics**. The idea of **in-database analytics** is to bring the **computation to the data** instead of extracting data to a separate tool: run the model **where the data lives**, on the **parallel MPP engine** ([Ch 3](03-the-mpp-architecture.md)), at scale.

ClearScape Analytics provides:

- **In-database functions** — a large library of analytic and ML functions (data prep, statistics, feature engineering, model training and scoring) callable in SQL, executed in parallel across AMPs.
- **Scale** — analytics run on the full data set on the parallel engine, avoiding the sampling or data-movement that separate tools force.
- **Operationalization** — models can be **deployed and scored in-database**, so predictions run at warehouse scale in production.

The payoff is **analytics at data scale without moving the data** — a strong fit for enterprises with huge datasets. This modern-analytics capability is central to how the current platform (and certifications) are positioned. The lab runs in-database scoring.

## QueryGrid

Data lives in **many systems**, and Teradata's **QueryGrid** is a **data fabric** that lets Vantage **query across** them — reaching data in other Teradata systems, data lakes, object storage, and other engines **without physically moving it first**. A query can join Teradata data with data in an external system, with QueryGrid orchestrating the cross-system access.

This addresses the reality that no single platform holds all the data: rather than copying everything into one place, QueryGrid lets you **analyze data where it sits** and combine it. For a modern data architecture spanning warehouses, lakes, and clouds, this **connected** capability is key — and it reflects Teradata's "connected multi-cloud data platform" ([Ch 2](02-vantage-and-vantagecloud.md)) positioning. The lab models a cross-system query. *(Cross-system query fabrics parallel data-virtualization approaches across the data ecosystem.)*

## Lakehouse, open formats, and languages

The modern VantageCloud platform embraces the broader **data ecosystem**:

- **Open table formats** — read/write **open formats** (like Parquet and open table formats) on object storage, so Teradata participates in the **lakehouse** rather than locking data in a proprietary store ([Ch 2](02-vantage-and-vantagecloud.md)).
- **Object storage** — VantageCloud Lake stores data on cheap, scalable **cloud object storage**, separating compute from storage for elasticity.
- **Language integration** — beyond SQL, work with Teradata from **Python and R** (via connectors and packages like `teradataml`), so data scientists use their preferred tools against the parallel engine.

This openness is a deliberate shift: Teradata's engine and reliability, made **interoperable** with the open, cloud-native data world. It is why the current certifications center on **VantageCloud Lake** — the platform meeting modern data architecture. The lab uses a Python-style client and open data.

## Positioning for analytics and AI

Putting it together, Teradata's modern positioning is a **high-performance analytics and AI platform** that:

- runs **complex analytics and ML at scale** in-database (ClearScape),
- **connects** to data wherever it lives (QueryGrid, multi-cloud),
- is **open** (lakehouse, open formats, Python/R), and
- keeps the **enterprise-grade** performance, reliability, and governance Teradata is known for.

For an enterprise investing in **AI and large-scale analytics**, this is Teradata's pitch: the trusted, scalable engine, now cloud-native and open. Understanding this direction — and that certification has moved to VantageCloud/Lake to match it — completes the modern picture and frames the path choice ([Ch 9](09-choosing-your-teradata-path.md)). The lab synthesizes the modern platform. *(Analytics-and-AI-at-scale is the shared frontier of [Databricks XLVIII](../../volume-048-databricks-certifications/README.md), [Snowflake XLIX](../../volume-049-snowflake-certifications/README.md), and [SAS CLXVIII](../../volume-168-sas-certifications/README.md).)*

## Hands-On Lab

Python models in-database analytics, QueryGrid cross-system query, and open/Python access. **Cost:** none.

### Lab 8.1 — Modern analytics on Vantage

**Objective:** Score a model in-database, query across systems via QueryGrid, and use a Python client.

```bash
python3 - <<'EOF'
# ClearScape: IN-DATABASE scoring (compute goes to the data, parallel across AMPs)
customers = [{"id":1,"tenure":2,"spend":50},{"id":2,"tenure":20,"spend":500},{"id":3,"tenure":1,"spend":20}]
def in_db_score(rows):   # model runs WHERE THE DATA IS, no extraction
    for r in rows:
        r["churn_risk"] = round(max(0, 1 - (r["tenure"]/12) ) * (1 if r["spend"]<100 else 0.5), 2)
    return rows
print("CLEARSCAPE ANALYTICS — in-database scoring (no data movement, parallel on AMPs):")
for r in in_db_score(customers): print(f"   customer {r['id']}: churn_risk={r['churn_risk']}")

# QueryGrid: query ACROSS systems without moving data first
def querygrid(local_table, remote_system, remote_table):
    return f"JOIN {local_table} (Teradata) WITH {remote_table} (@{remote_system}) via QueryGrid — data stays put"
print("\nQUERYGRID (data fabric across systems):")
print(f"   {querygrid('sales', 'data-lake (S3)', 'web_clicks')}")

# Open + Python: access Vantage from Python (teradataml-style) on open data
print("\nOPEN + PYTHON (VantageCloud Lake, lakehouse):")
print("   df = teradataml.DataFrame('sales')   # query the parallel engine from Python")
print("   read/write Parquet + open table formats on cloud object storage (compute/storage separated)")
print()
print("CLEARSCAPE runs analytics/ML IN-DATABASE — compute goes to the data, parallel across AMPs,")
print("no extraction. QUERYGRID queries ACROSS systems (Teradata + data lake) without moving data.")
print("The modern platform is OPEN — Parquet/open formats on object storage, accessed from SQL AND")
print("Python/R. Enterprise-grade engine, now cloud-native + open — the VantageCloud Lake direction.")
EOF
```

**Expected result:** In-database churn scoring running where the data lives, a QueryGrid cross-system join keeping data in place, and Python/open-format access to VantageCloud Lake. The lesson is Teradata's modern platform: ClearScape Analytics runs analytics and ML in-database on the parallel engine (no data movement), QueryGrid queries across systems as a data fabric, and the platform is open (lakehouse, open formats, Python/R) — the direction the current VantageCloud certifications reflect.

**Negative test:** Extracting all the data to a separate tool for every analysis, and copying data between systems for every cross-system query. It is slow, moves huge volumes, and does not scale; in-database analytics (ClearScape) and cross-system query (QueryGrid) keep computation at the data.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] ClearScape Analytics understood — in-database analytics/ML on the parallel engine, no data movement.
- [ ] QueryGrid understood — a data fabric querying across systems without moving data first.
- [ ] Lakehouse/open/languages understood — open formats on object storage, and Python/R access.
- [ ] Modern positioning understood — an open, cloud-native, enterprise-grade analytics and AI platform.

## See also

- [Chapter 02 — Teradata Vantage and VantageCloud](02-vantage-and-vantagecloud.md) — the cloud/lakehouse platform this runs on.
- [Chapter 03 — The MPP Architecture](03-the-mpp-architecture.md) — the parallel engine in-database analytics use.
- [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md) and [Volume CLXVIII — SAS](../../volume-168-sas-certifications/README.md) — analytics/ML-at-scale peers.
