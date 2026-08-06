# Volume CLVIII — Cloudera Certification Tracks

> The Cloudera Certification Program — verified 5 August 2026 on
> `cloudera.com/services-and-support/training/certification.html`. Cloudera recently launched a **new
> role-based Certification Program**, replacing the legacy **CCA** and **CCP** exams (the older **CDH** and
> **HDP** certifications are discontinued). Exams are **question-based** and **proctored securely online** via
> **Questionmark** (with a **Zoom** webcam proctor), **online only**, and awarded as **digital badges**. Nine
> role-based certifications span the platform — **Generalist**, **Administrator on premises**, **Administrator
> Cloud**, **Data Engineer**, **Data Operator**, **Data Analyst**, **Machine Learning Engineer**, **Generative
> AI Engineer**, and **Data Lakehouse Engineer**. The platform beneath is the hybrid **Cloudera Data Platform
> (CDP)**. Every lab runs **free** in Python. A data-platform volume — analytics, engineering, and AI on data.

## Overview

Cloudera is a **hybrid data platform** company — the **Cloudera Data Platform (CDP)** runs the full data
lifecycle (collect, enrich, report, serve, predict) across **on-premises and public cloud**, with deep
**open-source roots** (Spark, Hive, Impala, NiFi, Kafka, Iceberg). It sits alongside the other big data
platforms this shelf covers, [Databricks (XLVIII)](../volume-048-databricks-certifications/README.md) and
[Snowflake (XLIX)](../volume-049-snowflake-certifications/README.md); **Cloudera versus Databricks** is a key
comparison, with Cloudera's differentiator being **hybrid** (strong on-prem) and **open** (Iceberg, no lock-in).

Chapter 02 covers **the CDP platform** — hybrid architecture, open-source roots, and **SDX** (unified security
and governance via Ranger and Atlas). Chapters 03–08 take the roles: **Administrator** (on-prem and cloud),
**Data Engineer** (Spark/Airflow pipelines), **Data Operator** (NiFi/Kafka data flow), **Data Analyst** (Data
Warehouse and visualization), **Machine Learning Engineer** (MLOps on Cloudera AI), and the frontier —
**Generative AI Engineer**, **Data Lakehouse Engineer**, and **Generalist**. Chapter 09 closes on choosing a path.

A theme runs through it: **one hybrid, open platform across the whole data lifecycle**, with SDX providing one
security and governance model under every role.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Cloudera Certification Program](chapters/01-the-cloudera-program.md) | 1.1–1.2 |
| 02 | [The Cloudera Data Platform (CDP)](chapters/02-the-cloudera-data-platform.md) | 2.1 |
| 03 | [Cloudera Administrator (On-Premises and Cloud)](chapters/03-cloudera-administrator.md) | 3.1 |
| 04 | [Cloudera Data Engineer](chapters/04-cloudera-data-engineer.md) | 4.1 |
| 05 | [Cloudera Data Operator](chapters/05-cloudera-data-operator.md) | 5.1 |
| 06 | [Cloudera Data Analyst](chapters/06-cloudera-data-analyst.md) | 6.1 |
| 07 | [Cloudera Machine Learning Engineer](chapters/07-cloudera-machine-learning-engineer.md) | 7.1 |
| 08 | [Generative AI, Lakehouse, and Generalist](chapters/08-genai-lakehouse-generalist.md) | 8.1 |
| 09 | [Choosing Your Cloudera Path](chapters/09-choosing-your-cloudera-path.md) | 9.1–9.2 |

## The certifications

Nine **role-based** certifications, all question-based, proctored online, digital badges:

| Role | Focus |
| --- | --- |
| **Generalist** | Broad, multi-role platform knowledge (entry) |
| **Administrator on premises** | Install, operate, secure CDP on-prem (Cloudera Manager) |
| **Administrator Cloud** | Manage CDP in the public cloud |
| **Data Engineer** | Spark/Airflow pipelines, Iceberg, performance tuning |
| **Data Operator** | NiFi and Kafka data flow (DataOps) |
| **Data Analyst** | Data Warehouse (Hive/Impala), Data Visualization |
| **Machine Learning Engineer** | MLOps on Cloudera AI |
| **Generative AI Engineer** | RAG, multi-agent workflows, model serving |
| **Data Lakehouse Engineer** | Apache Iceberg open storage |

Legacy **CCA/CCP** (and CDH/HDP) are retired; the program is now all-CDP and role-based.

## What you will be able to do

- Read the role-based program, its online-proctored model, and the retirement of legacy CCA/CCP.
- Explain CDP as a hybrid, open data platform, and SDX as unified security (Ranger) and governance (Atlas).
- Administer CDP on-premises (clusters, Cloudera Manager) and in the cloud (auto-scaling, cost).
- Build data pipelines with Spark and Airflow, writing to Iceberg, and tune them for performance.
- Flow data in real time with NiFi and Kafka in event-driven workflows.
- Query and visualize governed data with the Data Warehouse (Hive/Impala) and Data Visualization.
- Operationalize ML with MLOps on Cloudera AI, including drift monitoring and retraining.
- Build enterprise generative AI with RAG and open lakehouse storage with Apache Iceberg.

## Prerequisites

- Familiarity with data, SQL, and distributed systems helps.
- A Linux or macOS host with `python3`. The **Cloudera certifications** are proctored online exams via Questionmark.

## See also

- [Volume XLVIII — Databricks](../volume-048-databricks-certifications/README.md) and [Volume XLIX — Snowflake](../volume-049-snowflake-certifications/README.md) — the data-platform/lakehouse peers; Cloudera vs Databricks is *the* comparison.
- [Volume CXXXV — Confluent](../volume-135-confluent-certifications/README.md) — Kafka streaming, adjacent to the Data Operator role.
- [Volume CLIV — Tableau](../volume-154-tableau-certifications/README.md) — BI/visualization, adjacent to the Data Analyst role.
- [Volume XLVI — NVIDIA](../volume-046-nvidia-certifications/README.md) — AI infrastructure, adjacent to the ML/GenAI roles.
