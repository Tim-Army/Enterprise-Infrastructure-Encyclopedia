# Chapter 01: The Databricks Certification Program

## Learning Objectives

- Explain what Databricks certifies and its place in the data-and-AI stack.
- Describe the credential map: role-based certifications and free accreditations.
- Explain the exam experience, exam guides, and how certifications differ from accreditations.
- Understand recent additions (Generative AI Engineer, Context Engineer) and the Lakehouse platform.
- Verify a current exam guide from the authoritative source.

## Theory and Architecture

**Databricks** builds the **Data Intelligence Platform** — the **lakehouse** that
unifies data engineering, analytics, machine learning, and generative AI on one
governed platform (**Delta Lake**, **Unity Catalog**, **Spark**, **MLflow**,
**Mosaic AI**). Its certifications validate the ability to build and operate on
that platform. This volume sits between the encyclopedia's **data/observability**
(Splunk, XLV) and **AI-infrastructure** (NVIDIA, XLVI) volumes, and complements the
cloud volumes where Databricks runs (AWS, Azure, GCP).

The program has two kinds of credential:

- **Role-based certifications** (proctored exams): **Data Analyst Associate**;
  **Data Engineer Associate** and **Professional**; **Machine Learning Associate**
  and **Professional**; the new **Generative AI Engineer Associate** and **Context
  Engineer Associate**; and the **Apache Spark Developer Associate**.
- **Accreditations** (free badges/assessments): **Databricks Fundamentals**,
  **Generative AI Fundamentals**, **AI Agent Fundamentals**, **Platform Architect**
  (AWS/Azure/GCP), and **Platform Administrator**.

The **Generative AI Engineer** and **Context Engineer** certifications are recent
additions reflecting the platform's AI-agent focus; the **Hadoop Migration
Architect** certification was retired (1 August 2024).

## Design Considerations

Plan a path by **role**. Analysts start with **Data Analyst Associate**; data
engineers take **Data Engineer Associate → Professional**; ML practitioners take
**Machine Learning Associate → Professional**; and AI builders take the **GenAI
Engineer** and **Context Engineer** certs. The **Apache Spark Developer Associate**
validates the Spark DataFrame API that underpins the platform. Start with the free
**Fundamentals** accreditations to learn the lakehouse before an exam.

## Implementation and Automation

Every Databricks exam has a published **exam guide** with weighted sections — the
authoritative study scope. Confirm the current guide before studying, and practice
on **Databricks Free Edition / Community Edition**. The core tools are **Spark**
(PySpark/Spark SQL), **Delta Lake**, **Unity Catalog**, and **MLflow**:

```python
# The Databricks working surface: Spark + SQL + Delta, governed by Unity Catalog
spark.sql("SELECT current_catalog(), current_schema()").show()
```

## Validation and Troubleshooting

Confirm a credential's guide, level, and format:

```text
databricks.com/learn/certification > open the certification:
  - the exam guide (weighted sections)
  - level (Associate/Professional) and duration
  - whether it is a proctored certification or a free accreditation
```

Common pitfalls: confusing a free **accreditation** with a proctored
**certification**; studying an **old exam guide** (the program adds/revises exams,
e.g., the new GenAI and Context Engineer certs); and conflating **Delta Lake** (the
storage format) with **Databricks SQL** (the analytics warehouse).

## Security and Best Practices

Verify facts on **databricks.com**, never a dump site. Practice on **Free/Community
Edition**. Govern data with **Unity Catalog** (a recurring exam theme), track ML
with **MLflow**, and prefer **Delta Lake** for reliable, ACID lakehouse tables.
Learn the **medallion architecture** (bronze/silver/gold) — it frames much of the
data-engineering content.

## References and Knowledge Checks

- databricks.com/learn/certification: the certification catalog and per-exam guides; Databricks Academy; the Databricks documentation.

**Knowledge checks**

1. What is the lakehouse, and how does Databricks unify data and AI on it?
2. How does a Databricks accreditation differ from a certification?
3. Which certifications are recent AI-focused additions?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and preparing to practice.

**Shared prerequisites for Labs 1.1–1.3** — a shell with `curl`; a Databricks Free
Edition / Community workspace to run the Spark/SQL. **Cost:** none.

### Lab 1.1 — Enumerate the certification catalog (Topic: Read the program)

**Objective:** List the current certifications from the authoritative source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.databricks.com/learn/certification" \
  | grep -oiE '(Data Analyst|Data Engineer|Machine Learning|Generative AI Engineer|Context Engineer|Apache Spark Developer)[^<]{0,20}(Associate|Professional)?' \
  | sort -u | head
```

**Expected result:** the role-based certifications across Data Analyst, Data
Engineer, Machine Learning, the new GenAI/Context Engineer, and Apache Spark
Developer — the program in one view.

**Negative test:** rely on an old list; it misses the **Generative AI Engineer**
and **Context Engineer** certs — use the live catalog.

**Cleanup:** none.

### Lab 1.2 — Explore the lakehouse platform (Topic: Foundation)

**Objective:** Confirm the Spark + SQL + Delta surface.

```python
spark.range(5).write.format("delta").mode("overwrite").saveAsTable("demo_delta")
spark.sql("SELECT count(*) AS n FROM demo_delta").show()
```

**Expected result:** a Delta table created and counted (`n = 5`) — the Spark +
Delta Lake foundation every Databricks cert builds on.

**Negative test:** write as CSV and expect ACID/time-travel; use **Delta** for
reliable lakehouse tables.

**Cleanup:** `spark.sql("DROP TABLE IF EXISTS demo_delta")`

### Lab 1.3 — Read Unity Catalog context (Topic: Governance)

**Objective:** See the three-level namespace Unity Catalog governs.

```python
spark.sql("SELECT current_catalog() AS cat, current_schema() AS sch").show()
# Unity Catalog namespace: catalog.schema.table
```

**Expected result:** the current catalog and schema — the `catalog.schema.table`
governance model Unity Catalog enforces (a recurring exam theme).

**Negative test:** reference tables by `schema.table` only under Unity Catalog; use
the full **`catalog.schema.table`** name to avoid ambiguity.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Databricks certifies building and operating on the lakehouse Data Intelligence
Platform, through role-based certifications (Data Analyst, Data Engineer, Machine
Learning, the new GenAI/Context Engineer, and Apache Spark Developer) and free
accreditations (Fundamentals, Platform Architect/Administrator). Spark, Delta Lake,
Unity Catalog, and MLflow underpin the whole program.

- [ ] I can map the Databricks certifications and accreditations.
- [ ] I can explain the lakehouse and Unity Catalog governance.
- [ ] I can create a Delta table and read catalog context.
- [ ] I know the recent GenAI/Context Engineer additions.
- [ ] I completed Labs 1.1–1.3 including each negative test.
