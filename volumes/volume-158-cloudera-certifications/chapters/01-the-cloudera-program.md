# Chapter 01: The Cloudera Certification Program

![The Cloudera Certification Program and the Cloudera Data Platform beneath it. Cloudera recently launched a new role-based Certification Program, replacing the legacy CCA and CCP exams; the older CDH and HDP certifications are discontinued. Exams are question-based and proctored securely online through Questionmark with a Zoom webcam proctor, available online only with no test centers, and earned credentials are awarded as digital badges. Nine role-based certifications span the platform: Generalist for broad multi-role knowledge, Administrator on premises and Administrator Cloud for managing clusters, Data Engineer for pipelines, Data Operator for NiFi and Kafka data flow, Data Analyst for the data warehouse and visualization, Machine Learning Engineer for MLOps, Generative AI Engineer for RAG and multi-agent systems, and Data Lakehouse Engineer for Apache Iceberg open storage. The platform beneath is the Cloudera Data Platform, a hybrid data platform spanning on-premises and public cloud, rooted in open source, with the Shared Data Experience providing unified security and governance through Apache Ranger and Apache Atlas.](../../../diagrams/volume-158-cloudera-certifications/chapter-01-program.svg)

*Figure 1-1. The nine role-based certifications and the hybrid Cloudera Data Platform they validate.*

## Learning Objectives

- Describe the new Cloudera Certification Program — role-based, proctored online, digital badges.
- Place the nine role-based certifications.
- Understand the retirement of the legacy CCA/CCP (and CDH/HDP) certifications.
- Recognize Cloudera's position as a hybrid data platform.

## What Cloudera is

Cloudera is a **hybrid data platform** company — its product, the **Cloudera Data Platform (CDP)**, runs the full data lifecycle (collect, enrich, report, serve, and predict on data) across **on-premises and public cloud**. Cloudera has deep **open-source roots** (Hadoop, Spark, Hive, Impala, NiFi, Kafka, Iceberg) and is distinctive for its **hybrid** strength — running the same platform in your data center *and* in the cloud. It sits alongside the other big data platforms this shelf covers, [Databricks (XLVIII)](../../volume-048-databricks-certifications/README.md) and [Snowflake (XLIX)](../../volume-049-snowflake-certifications/README.md); **Cloudera versus Databricks** (both Spark/lakehouse) is a key comparison, with Cloudera's differentiator being **hybrid, open, on-prem-capable** data management.

## The new role-based program

Cloudera recently **launched a new Certification Program** that is **role-based** — each exam maps to a **job role** working with the platform. This **replaces the legacy CCA (Cloudera Certified Associate) and CCP (Cloudera Certified Professional)** exams, and the even older **CDH and HDP** certifications are **discontinued** — Cloudera's certification strategy is now entirely on **CDP** and organized by role. For anyone with older Cloudera credentials, the important fact is that the program has been **rebuilt around roles and the current platform**. The lab models the program.

## Exam mechanics

The program's exams share a delivery model:

| Element | Value |
|:---|:---|
| **Format** | **Question-based**, role-based |
| **Delivery** | **Proctored securely online** via **Questionmark** (with a **Zoom** webcam proctor) |
| **Location** | **Online only** — no test centers |
| **Credential** | **Digital badge**, shareable on professional forums |
| **Prerequisites** | None required (training recommended) |

The online-proctored, question-based format (a remote proctor watches by webcam and enforces exam rules) validates **role knowledge** of the Cloudera platform. The lab models the rule set.

## The nine role-based certifications

| Certification | Role / focus |
|:---|:---|
| **Generalist** | Broad, multi-role platform knowledge (entry) |
| **Administrator on premises** | Install, operate, and secure CDP on-prem ([Ch 3](03-cloudera-administrator.md)) |
| **Administrator Cloud** | Manage CDP in the public cloud ([Ch 3](03-cloudera-administrator.md)) |
| **Data Engineer** | Pipelines — Spark, Airflow, Iceberg ([Ch 4](04-cloudera-data-engineer.md)) |
| **Data Operator** | Data flow — NiFi, Kafka ([Ch 5](05-cloudera-data-operator.md)) |
| **Data Analyst** | Data Warehouse, visualization — Hive, Impala ([Ch 6](06-cloudera-data-analyst.md)) |
| **Machine Learning Engineer** | ML models, MLOps ([Ch 7](07-cloudera-machine-learning-engineer.md)) |
| **Generative AI Engineer** | RAG, multi-agent, model serving ([Ch 8](08-genai-lakehouse-generalist.md)) |
| **Data Lakehouse Engineer** | Apache Iceberg open storage ([Ch 8](08-genai-lakehouse-generalist.md)) |

The roles span the whole platform — administration, engineering, operations, analysis, and the AI/ML and lakehouse frontier. [Chapter 2](02-the-cloudera-data-platform.md) covers the CDP platform itself; the middle chapters take the roles; [Chapter 9](09-choosing-your-cloudera-path.md) sequences a path. The lab models the role map.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the role-based certifications

**Objective:** Represent the nine role-based certifications.

```bash
python3 - <<'EOF'
CERTS = {
  "Generalist": "broad, multi-role platform knowledge (entry)",
  "Administrator on premises": "install/operate/secure CDP on-prem",
  "Administrator Cloud": "manage CDP in public cloud",
  "Data Engineer": "pipelines — Spark, Airflow, Iceberg",
  "Data Operator": "data flow — NiFi, Kafka (DataOps)",
  "Data Analyst": "Data Warehouse + visualization — Hive, Impala",
  "Machine Learning Engineer": "ML models, MLOps (Cloudera AI)",
  "Generative AI Engineer": "RAG, multi-agent, model serving",
  "Data Lakehouse Engineer": "Apache Iceberg open storage",
}
print("Cloudera Certification Program — NEW role-based exams:\n")
for i, (cert, focus) in enumerate(CERTS.items(), 1):
    print(f"   {i}. {cert:28} {focus}")
print(f"\n   {len(CERTS)} role-based certifications\n")
print("Key facts:")
print("  - NEW role-based program REPLACES legacy CCA (Associate) + CCP (Professional);")
print("    older CDH/HDP certs are DISCONTINUED — strategy is now all-CDP, by ROLE.")
print("  - each exam maps to a JOB ROLE on the platform (admin -> engineer -> operator ->")
print("    analyst -> ML/AI/lakehouse) — you certify for the role you work.")
print("  - QUESTION-BASED, proctored securely ONLINE via Questionmark + Zoom webcam,")
print("    online-only (no test centers); credentials = shareable DIGITAL BADGES.")
EOF
```

**Expected result:** The nine role-based certifications (Generalist, two Administrators, Data Engineer, Data Operator, Data Analyst, ML Engineer, GenAI Engineer, Data Lakehouse Engineer). The program lesson is that Cloudera's new program is role-based and all-CDP — replacing the legacy CCA/CCP and discontinuing CDH/HDP — with question-based exams proctored online via Questionmark and awarded as digital badges.

**Negative test:** Studying for the old CCA/CCP or CDH/HDP exams. Those are retired; the current program is role-based on CDP, so target the role certification that matches your job.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — The online-proctored model

**Objective:** Reason about the question-based, online-proctored format.

```bash
python3 - <<'EOF'
MODEL = {
  "format": "question-based, role-based",
  "delivery": "proctored online via Questionmark",
  "proctor": "live human via Zoom webcam (enforces rules, knows no Hadoop)",
  "location": "online only — no test centers",
  "rules": "alone, desk clear, face visible, no notes/phones/headphones, no leaving view",
  "credential": "digital badge (shareable)",
}
print("Cloudera exam delivery model:\n")
for k, v in MODEL.items():
    print(f"   {k:11}: {v}")
print("\nReading it: an ONLINE, live-proctored, question-based exam. A remote proctor watches")
print("by webcam ONLY to enforce integrity (verify identity, ensure you're alone, no notes)")
print("— they know nothing of the content. This makes the credential portable (take it from")
print("anywhere) while keeping it proctored + trustworthy. It validates ROLE KNOWLEDGE of")
print("the Cloudera platform, awarded as a shareable digital badge. Match the exam to the")
print("role you perform, and prepare with Cloudera training + hands-on platform time.")
EOF
```

**Expected result:** The delivery model — question-based, proctored online via Questionmark with a Zoom webcam proctor enforcing exam rules, online-only, digital badge. The lesson is that the online-proctored format keeps the credential portable yet trustworthy, validating role knowledge of the Cloudera platform and awarded as a shareable digital badge.

**Negative test:** Expecting a hands-on lab exam or a test-center appointment. The current program is question-based and online-only via Questionmark; prepare for role-knowledge questions taken under remote webcam proctoring.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The new Cloudera Certification Program understood — role-based, proctored online, digital badges.
- [ ] The nine role-based certifications placed against the roles they validate.
- [ ] The retirement of legacy CCA/CCP and CDH/HDP understood — the program is now all-CDP by role.
- [ ] Cloudera recognized as a hybrid data platform, the peer of Databricks (XLVIII) and Snowflake (XLIX).
