# Volume CXXXV — Confluent Certification Tracks

> The certification map for **Confluent**, the commercial platform built around **Apache Kafka** by
> Kafka's original creators — verified on confluent.io, 4 August 2026. The program pairs **two free,
> self-paced Fundamentals Accreditations** (Apache Kafka, and a **new one for Apache Flink**), each
> earning a shareable digital badge and explicitly positioned as the on-ramp for those "not quite ready
> for Certification," with **three proctored certifications**: **CCDAK** (Certified Developer for Apache
> Kafka), **CCAAK** (Certified Administrator for Apache Kafka), and **CCAC** (Confluent Cloud Certified
> Operator). All three are **90-minute Honorlock-proctored** exams taken remotely in Google Chrome with a
> webcam and government ID, using multiple-choice, matching, and list-order questions, with **results
> immediately on screen**, **two-year validity**, a **7-day retake wait**, and a **5-day cancellation
> window**. The volume teaches the underlying streaming disciplines and models them free in Python — the
> partitioned log and per-partition ordering, delivery semantics and exactly-once, consumer groups and
> lag, schema compatibility, Connect pipelines, windowed stream processing with event time, and cluster
> sizing, monitoring, and ACLs. No Kafka installation required.

## Overview

Volume CXXXV is a **certification-tracks volume** organized by the concepts the exams test. Chapter 02
builds the partitioned, append-only log and the replication model (ISR, `min.insync.replicas`, and the
deliberate choice of durability over availability). Chapter 03 covers producers and the three delivery
semantics, including why at-least-once *must* duplicate and how idempotence and transactions fix it.
Chapter 04 covers consumer groups, the parallelism cap, commit strategies, and reading lag by trend.
Chapter 05 covers Schema Registry and compatibility modes — including why Kafka's **replayable** log
makes transitive compatibility matter more than elsewhere. Chapter 06 covers Kafka Connect, and Chapter
07 stream processing with **Kafka Streams and Flink**, event time versus processing time, and grace
periods. Chapter 08 carries the administrator and cloud-operator material: sizing with the replication
multiplier, the metrics that predict trouble, ACLs, and Confluent Cloud's Cluster Linking and multi-cloud
features. Chapter 09 closes on choosing an exam and staying current.

Confluent's place among the encyclopedia's data-platform volumes is **data in motion**, complementing
[Snowflake XLIX](../volume-049-snowflake-certifications/README.md) and
[Databricks XLVIII](../volume-048-databricks-certifications/README.md) (data at rest),
[MongoDB LXXXVIII](../volume-088-mongodb-certifications/README.md) (operational data), and
[Elastic LXXXVI](../volume-086-elastic-certifications/README.md) /
[Splunk XLV](../volume-045-splunk-certifications/README.md) (search and logs).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Confluent Program and Apache Kafka](chapters/01-the-confluent-program-and-kafka.md) | 1.1–1.2 |
| 02 | [Kafka Architecture and the Partitioned Log](chapters/02-kafka-architecture-and-the-log.md) | 2.1–2.3 |
| 03 | [Producers and Delivery Semantics](chapters/03-producers-and-delivery-semantics.md) | 3.1–3.3 |
| 04 | [Consumers and Consumer Groups](chapters/04-consumers-and-consumer-groups.md) | 4.1–4.3 |
| 05 | [Schemas and Stream Governance](chapters/05-schemas-and-stream-governance.md) | 5.1–5.3 |
| 06 | [Kafka Connect and Connectors](chapters/06-kafka-connect-and-connectors.md) | 6.1–6.3 |
| 07 | [Stream Processing — Kafka Streams and Flink](chapters/07-stream-processing-kafka-streams-and-flink.md) | 7.1–7.3 |
| 08 | [Operating Clusters and Confluent Cloud](chapters/08-operating-clusters-and-confluent-cloud.md) | 8.1–8.3 |
| 09 | [Choosing a Certification, Currency, and Career](chapters/09-choosing-a-certification-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the three certifications and two free accreditations, and sequence them sensibly.
- Explain per-partition ordering, key-based partitioning, and the cost of changing partition count.
- Configure `acks`, idempotence, and transactions for the delivery semantics you actually need.
- Size consumer groups against partition count, choose a commit strategy, and read lag by trend.
- Evolve schemas safely with the right compatibility mode, including transitive for replayable logs.
- Build Connect pipelines with transforms and monitored dead-letter queues.
- Write windowed stream processing that uses event time and tolerates late data.
- Size, monitor, and secure clusters, and describe Confluent Cloud's Cluster Linking and governance.

## Prerequisites

- General distributed-systems and application-development familiarity; [Volume VIII](../volume-008-containers-platform-engineering/README.md) for platform context.
- A Linux or macOS host with `python3` — every lab runs on the standard library. Apache Kafka is free if you want a real cluster alongside.

## See also

- [Volume XLIX — Snowflake](../volume-049-snowflake-certifications/README.md), [Volume XLVIII — Databricks](../volume-048-databricks-certifications/README.md), [Volume LXXXVIII — MongoDB](../volume-088-mongodb-certifications/README.md), [Volume LXXXVI — Elastic](../volume-086-elastic-certifications/README.md), [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md) — the neighboring data-platform programs.
- [Volume LIV — OpenTelemetry](../volume-054-opentelemetry/README.md) — telemetry pipelines that commonly produce into Kafka.
- [Master Appendices — Confluent appendix](../volume-997-master-appendices/chapters/69-appendix-confluent-certifications-and-course-access.md) — certifications, accreditations, and access.
