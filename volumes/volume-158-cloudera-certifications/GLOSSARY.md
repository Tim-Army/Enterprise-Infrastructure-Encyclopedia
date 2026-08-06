# Volume CLVIII — Glossary

| Term | Definition |
|:---|:---|
| **Apache Airflow** | The orchestration tool for Cloudera data pipelines — defines a DAG of tasks with dependencies, scheduling, retries, and monitoring, turning individual Spark jobs into a reliable production pipeline. |
| **Apache Atlas** | The governance component of SDX — a catalog of data assets with lineage (where data came from and how it was transformed) and classification (tagging sensitive data), applied across the platform. |
| **Apache Iceberg** | The open table format underpinning Cloudera's lakehouse — multi-engine (Spark/Trino/Hive) transactional tables with ACID compliance, schema and partition evolution without rewrites, and snapshot rollback (time travel). |
| **Apache Kafka** | A distributed event-streaming platform — durable, high-throughput topics that decouple producers from many independent consumers, the backbone of event-driven, real-time data workflows; central to the Data Operator role. |
| **Apache NiFi** | A flow-based data-movement tool — visual flows that route, transform, and deliver data between systems with back-pressure, prioritization, guaranteed delivery, and provenance; the Data Operator's ingestion tool. |
| **Apache Ranger** | The access-control component of SDX — fine-grained, policy-based authorization (which users/roles can read/write which tables, columns, rows), enforced uniformly across all data services. |
| **CCA / CCP** | The legacy Cloudera Certified Associate and Professional certifications, now replaced by the new role-based Certification Program; the older CDH and HDP certifications are discontinued. |
| **Cloudera AI** | Cloudera's machine-learning platform (formerly Cloudera Machine Learning / CML) — collaborative notebooks, scalable training, and model deployment/serving, running on CDP next to governed data; the ML/GenAI engineer's platform. |
| **Cloudera Data Platform (CDP)** | Cloudera's hybrid data platform spanning on-premises and public cloud, covering the full data lifecycle (collect → enrich → report → serve → predict), built on open-source foundations with SDX governance. |
| **Cloudera Manager** | The console for deploying, configuring, managing, and monitoring on-premises clusters — the administrator's primary tool, centralizing dozens of components into one management plane. |
| **Data Warehouse** | Cloudera's SQL analytics service — Apache Hive (batch) and Apache Impala (fast, interactive, massively parallel) engines over governed platform data; the Data Analyst's environment. |
| **Hybrid data platform** | Cloudera's signature — running the same data management and analytics across both on-premises data centers and public clouds, letting workloads run where the data lives and move between environments. |
| **MLOps** | Machine-learning operations — the lifecycle from model development to reliable production (version, deploy, monitor, retrain), closing the gap between a notebook model and a production service, including drift detection. |
| **RAG (Retrieval-Augmented Generation)** | Grounding a large language model in enterprise data by retrieving relevant documents and feeding them to the model, so answers are accurate and current rather than hallucinated; the dominant enterprise-GenAI pattern. |
| **Role-based program** | The structure of Cloudera's new Certification Program — each exam maps to a job role (admin, engineer, operator, analyst, ML, GenAI, lakehouse, generalist) on the CDP platform. |
| **SDX (Shared Data Experience)** | CDP's unified security and governance layer — one model (Ranger for access, Atlas for governance/lineage) applied consistently across all data services and both on-prem and cloud. |
| **Apache Spark** | The distributed processing engine for Cloudera data engineering — parallel ETL over datasets far larger than a single machine (PySpark/SQL/Scala), including Spark on Kubernetes; the Data Engineer's workhorse. |
| **Snapshot rollback** | Iceberg's point-in-time restoration — reverting a table to a previous snapshot ("time travel"), used to recover from a bad load without rebuilding the table. |
