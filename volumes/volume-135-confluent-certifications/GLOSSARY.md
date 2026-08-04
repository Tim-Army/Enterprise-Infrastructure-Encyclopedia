# Volume CXXXV — Glossary

| Term | Definition |
|:---|:---|
| **acks** | Producer setting deciding when a write is acknowledged: 0 (fire and forget), 1 (leader only), or all (the in-sync replicas). |
| **CCAAK** | Confluent Certified Administrator for Apache Kafka — configuring, deploying, monitoring, and supporting clusters. |
| **CCAC** | Confluent Cloud Certified Operator — multi-cloud and global architectures using Cluster Linking, Stream Governance, managed connectors, and stream processing. |
| **CCDAK** | Confluent Certified Developer for Apache Kafka — building streaming applications with Kafka's core APIs. |
| **Changelog topic** | The Kafka topic backing a stream processor's state store, allowing state to be rebuilt after failure. |
| **Cluster Linking** | Confluent Cloud replication of topics between clusters, across regions or providers, preserving offsets. |
| **Compatibility mode** | Schema Registry rule governing evolution: BACKWARD (upgrade consumers first), FORWARD (producers first), FULL (either), NONE, and their TRANSITIVE variants checking all prior versions. |
| **Consumer group** | Consumers sharing a `group.id`; each partition is assigned to exactly one member, so parallelism is capped at the partition count. |
| **Dead-letter queue** | A topic receiving records Connect cannot process, with `errors.tolerance=all`; silent data loss if left unmonitored. |
| **Exactly-once semantics** | Neither loss nor duplication, achieved with the idempotent producer plus transactions spanning outputs and offset commits. |
| **Event time** | When an event actually occurred, per its own timestamp — required for correct windowing, unlike processing time. |
| **Grace period** | Extra time a window stays open for late-arriving records; longer grace trades retained state for correctness. |
| **Honorlock** | The remote proctoring service for Confluent exams; requires a Chrome extension, system check, webcam, and government ID. |
| **Idempotent producer** | Producer mode assigning sequence numbers so the broker deduplicates retries, eliminating duplicates per partition and session. |
| **ISR** | In-sync replicas — the replicas caught up with the leader; `min.insync.replicas` sets how many must acknowledge an `acks=all` write. |
| **Kafka Connect** | The framework for moving data between Kafka and external systems declaratively, via workers, connectors, tasks, and converters. |
| **Kafka Streams** | A Java library embedded in your application for stream processing, as opposed to Flink's separate cluster. |
| **Lag** | Latest partition offset minus committed offset; interpret by trend — growing lag never catches up on its own. |
| **Offset** | A record's monotonically increasing position within its partition; consumers track their own. |
| **Partition** | The unit of ordering, storage, and parallelism within a topic; ordering is guaranteed only within one. |
| **Schema Registry** | Confluent's versioned schema store; records carry a schema ID, making the registry a runtime dependency for deserialization. |
| **SMT** | Single Message Transform — stateless per-record modification in a Connect pipeline (mask, rename, route, cast). |
| **State store** | Local storage (RocksDB) for stateful stream operations, durably backed by a changelog topic. |
| **Stream Governance** | Confluent's Schema Registry, Stream Catalog, Stream Lineage, and data-quality rules together. |
| **Transactions** | Producer mechanism making output records and consumer offset commits atomic; consumers read with `isolation.level=read_committed`. |
| **Under-replicated partitions** | Partitions whose replicas have fallen behind the leader; should be zero, and the first cluster metric to alert on. |
