#!/usr/bin/env python3
"""Volume CLVIII (Cloudera) program map.

Chapter 1: the new role-based Cloudera Certification Program (9 role exams,
proctored online via Questionmark, digital badges; legacy CCA/CCP retired) over
the hybrid Cloudera Data Platform (CDP) with SDX security/governance.

Run from scripts/diagrams:  python3 gen_volume158.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-158-cloudera-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Cloudera Certification Tracks",
        subtitle="NEW role-based program (9 role exams) · proctored online (Questionmark) · digital badges · hybrid Cloudera Data Platform + SDX",
        svg_title="Chapter 1 program map: the Cloudera role-based certifications over the hybrid Data Platform",
        svg_desc="Cloudera recently launched a new role-based Certification Program, replacing the legacy CCA "
                 "and CCP exams; the older CDH and HDP certifications are discontinued. Exams are question-based "
                 "and proctored securely online through Questionmark with a Zoom webcam proctor, online only, "
                 "awarded as digital badges. Nine role-based certifications span the platform: Generalist for "
                 "broad multi-role knowledge, Administrator on premises and Administrator Cloud for managing "
                 "clusters, Data Engineer for Spark and Airflow pipelines, Data Operator for NiFi and Kafka "
                 "data flow, Data Analyst for the Data Warehouse and Data Visualization with Hive and Impala, "
                 "Machine Learning Engineer for MLOps on Cloudera AI, Generative AI Engineer for RAG and "
                 "multi-agent systems, and Data Lakehouse Engineer for Apache Iceberg open storage. The "
                 "platform beneath is the Cloudera Data Platform, a hybrid platform spanning on-premises and "
                 "public cloud, rooted in open source (Spark, Hive, Impala, NiFi, Kafka, Iceberg), with the "
                 "Shared Data Experience providing unified security through Apache Ranger and governance "
                 "through Apache Atlas across every data service. Cloudera is a peer of Databricks and "
                 "Snowflake, with hybrid and open being its differentiators.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("CLOUDERA — hybrid DATA PLATFORM (CDP): full lifecycle on-prem + cloud, open-source rooted", 10, 700, "#111827"),
        Line("collect -> enrich -> report -> serve -> predict · peer of Databricks (XLVIII) / Snowflake (XLIX); edge = HYBRID + OPEN (Iceberg)", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("NEW ROLE-BASED CERTIFICATION PROGRAM (replaces legacy CCA/CCP; CDH/HDP discontinued) · question-based, proctored ONLINE via Questionmark + Zoom · digital badges", 7.6, 700, "#111827"),
        Line("9 role exams: GENERALIST (entry) · ADMIN on-prem · ADMIN cloud · DATA ENGINEER · DATA OPERATOR · DATA ANALYST · ML ENGINEER · GENERATIVE AI ENGINEER · DATA LAKEHOUSE ENGINEER", 7.0, 400, "#374151"),
    ])

    # role/service tiles
    c.node_box(40, 176, 288, 50, "data", [
        Line("ADMINISTRATOR (on-prem + cloud)", 8.0, 700, "#111827"),
        Line("Cloudera Manager · install/operate clusters ·", 7.0, 400, "#374151"),
        Line("capacity, maintenance, users (2 certs)", 7.0, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 50, "data", [
        Line("DATA ENGINEER", 8.3, 700, "#111827"),
        Line("Spark + Airflow pipelines · Iceberg ·", 7.0, 400, "#374151"),
        Line("performance tuning", 7.0, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 50, "data", [
        Line("DATA OPERATOR (DataOps)", 8.0, 700, "#111827"),
        Line("Apache NiFi (flow) + Apache Kafka (stream) ·", 7.0, 400, "#374151"),
        Line("event-driven end-to-end workflows", 7.0, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 50, "alt", [
        Line("DATA ANALYST", 8.3, 700, "#111827"),
        Line("Data Warehouse (Hive/Impala SQL) +", 7.0, 400, "#374151"),
        Line("Data Visualization · Ranger/Atlas", 7.0, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 50, "alt", [
        Line("ML ENGINEER", 8.3, 700, "#111827"),
        Line("Cloudera AI (fka CML) · MLOps ·", 7.0, 400, "#374151"),
        Line("deploy/serve/monitor (drift) models", 7.0, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 50, "alt", [
        Line("GENAI + LAKEHOUSE ENGINEER (frontier)", 7.4, 700, "#111827"),
        Line("RAG + multi-agent (Cloudera AI) ·", 7.0, 400, "#374151"),
        Line("Apache ICEBERG open ACID lakehouse", 7.0, 400, "#374151"),
    ])

    c.node_box(40, 296, 880, 30, "mgmt", [
        Line("★ FOUNDATION under every role: SDX (Shared Data Experience) — one SECURITY + GOVERNANCE model across ALL services · Ranger (access) + Atlas (lineage/classification) · hybrid on-prem + cloud", 7.4, 700, "#111827"),
    ])

    c.raw('<text x="40" y="352" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: role-based program + online-proctored model · SDX one-model governance · on-prem fixed vs cloud auto-scale capacity · Spark/Airflow DAG + tuning · NiFi->Kafka->consumers ·</text>')
    c.raw('<text x="40" y="369" font-size="9.5" font-weight="400" fill="#374151">'
          'governed SQL + right chart · MLOps deploy/monitor/drift/retrain · RAG grounding + Iceberg schema-evolution/rollback. Data cluster: Databricks (XLVIII)/Snowflake (XLIX) peers, Confluent (CXXXV) streaming, Tableau (CLIV) BI, NVIDIA (XLVI) AI infra.</text>')

    c.legend(40, 398, [
        ("data", "Admin / engineer / operator"),
        ("alt", "Analyst / ML / frontier"),
        ("neutral", "Role-based program"),
        ("mgmt", "CDP platform + SDX"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
