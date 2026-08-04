# Chapter 69: Appendix — Confluent Certifications and Course Access

The **Confluent** certification program — certifications, free accreditations, learning paths, and exam
logistics. Verified on **4 August 2026** from **confluent.io/certification/** and
**confluent.io/training/**, the sources that anchor [Volume CXXXV — Confluent Certification
Tracks](../../volume-135-confluent-certifications/README.md).

> **Sourcing and ethics note.** Search results for these certifications are dominated by "practice exam"
> and question-dump products. All were excluded. Confluent requires every candidate to accept the
> **Confluent Certification Program Agreement** at registration *and* again at the start of each exam;
> that agreement governs exam content, so using harvested questions is a contract violation that can
> invalidate a credential — not merely weak preparation.

**How access works.** The program is a **free on-ramp plus three proctored certifications**. The free
**Fundamentals Accreditations** are self-paced, cost nothing, and earn a shareable digital badge;
Confluent positions them explicitly for candidates "not quite ready for Certification." Above them sit
the three paid certifications, each with an official **Exam Guide** covering topics, format, and study
recommendations. Training is **recommended but not required**.

> **Currency.** The **Fundamentals Accreditation for Apache Flink is new**, and Confluent Cloud offers
> managed Flink — stream *processing* is now as central to the platform as stream *transport*, so expect
> the catalog to keep evolving. Note also that **Confluent Certification is not affiliated with the
> Apache Software Foundation**: exams cover Apache Kafka *and* Confluent's commercial additions (Schema
> Registry, Cluster Linking, Stream Governance). Promotional discounts appear on the training page from
> time to time; check current offers rather than relying on any code quoted elsewhere.

## Free and low-cost resources and entry points

- **[Confluent Certification](https://www.confluent.io/certification/)** — the authoritative page: certifications, exam guides, scheduling, and the full FAQ
- **[Confluent Training](https://www.confluent.io/training/)** — learning paths, free fundamentals, and paid courses
- **Free [Fundamentals Accreditation for Apache Kafka](https://www.confluent.io/training/)** — self-paced, badge on completion
- **Free Fundamentals Accreditation for Apache Flink (NEW)** — self-paced, badge on completion
- **Official Exam Guides** — one each for CCDAK, CCAAK, and CCAC
- **Apache Kafka itself is free and open source** — a local cluster costs nothing to run
- **Free study lab:** any host with `python3` models the exam concepts — the partitioned log and per-partition ordering, `acks`/idempotence/transactions, consumer-group assignment and lag, schema compatibility, Connect pipelines with dead-letter queues, windowed processing with event time, and cluster sizing and ACLs (see the volume's labs)

## Fees, delivery, and renewal

- **Fees:** the Fundamentals Accreditations are **free**; the three certifications are paid (confirm current pricing on the certification page).
- **Delivery:** **90-minute proctored** exams administered remotely worldwide by **Honorlock**. Question types are **multiple-choice, matching, and list order**. Requires a webcam, microphone and speakers, **Google Chrome**, a strong internet connection, and a **government ID**. Install the **Honorlock Chrome Extension** and run a **System Check** in advance — an inadequate connection **may forfeit the attempt**. Reference materials and mobile phones are prohibited. **Results appear immediately** on the testing screen.
- **Prerequisites:** none formal; training is recommended, not required.
- **Validity/renewal:** certifications **expire after two years**; recertification is required.
- **Retake:** wait **7 days** before repurchasing and retaking the same exam.
- **Cancel/reschedule:** **5 or more calendar days** before the appointment. Inside five days, rescheduling is unavailable, cancelling requires reapplying, and a no-show forfeits the fee.
- **Accommodations:** contact `certification@confluent.io` at least **21 days** before the test date.

## The certifications

Verified against confluent.io/certification on 4 August 2026.

| Certification | Code | Focus |
| --- | --- | --- |
| Confluent Certified Developer for Apache Kafka | **CCDAK** | Developers and solution architects building applications with Kafka — core APIs, streaming applications, Kafka Streams, testing |
| Confluent Certified Administrator for Apache Kafka | **CCAAK** | Managing and maintaining cluster environments — configure, deploy, monitor, support |
| Confluent Cloud Certified Operator | **CCAC** | Confluent Cloud — multi-cloud and global architectures using Cluster Linking, Stream Governance, fully managed connectors, and stream processing |

## Free accreditations

| Accreditation | Focus |
| --- | --- |
| Confluent Fundamentals Accreditation for Apache Kafka | Core Kafka concepts; the standard on-ramp |
| Fundamentals Accreditation for Apache Flink **(new)** | Stream processing with Flink |

## Learning paths

| Path | Sequence |
| --- | --- |
| **Confluent Platform — Operator** | Kafka Fundamentals (free) → Apache Kafka Administration (paid) → **CCAAK** |
| **Confluent Platform — Developer** | Kafka Fundamentals (free) → Confluent Developer Skills for Apache Kafka (paid) → Stream Processing using Kafka Streams (paid) → **CCDAK** |
| **Confluent Cloud — Operator / Developer** | Free fundamentals → paid intermediate and advanced courses → certification |

## Notes

- **Take the free accreditations first, whatever your target.** They are free, badge-bearing, and cover
  exactly the foundations the paid exams assume — and they tell you at no cost whether you are ready.
- **Plan the Honorlock system check days ahead.** A failed connection or browser setup on exam day can
  forfeit the attempt, and inside the five-day window you cannot reschedule.
- **Record the two-year expiry the day you pass** — the same discipline as
  [SailPoint CXXXII](../../volume-132-sailpoint-certifications/README.md)'s recertification cycle.
- **Position in the encyclopedia:** Confluent is the **data-in-motion** program, complementing
  [Snowflake XLIX](../../volume-049-snowflake-certifications/README.md) and
  [Databricks XLVIII](../../volume-048-databricks-certifications/README.md) (data at rest),
  [MongoDB LXXXVIII](../../volume-088-mongodb-certifications/README.md) (operational data), and
  [Elastic LXXXVI](../../volume-086-elastic-certifications/README.md) /
  [Splunk XLV](../../volume-045-splunk-certifications/README.md) (search and logs).
