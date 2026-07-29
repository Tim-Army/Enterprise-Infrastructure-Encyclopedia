# Volume LXXXVIII Glossary

Definitions for terms introduced in **Volume LXXXVIII — MongoDB Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Aggregation pipeline** — MongoDB's staged framework for transforming and computing over documents ($match, $group, $project, $lookup, $unwind).
- **Atlas** — MongoDB's fully managed cloud database service on AWS, Azure, and Google Cloud.
- **Atlas Search** — Lucene-based full-text search integrated with data in Atlas, queried via the `$search` stage.
- **BSON** — Binary JSON, the typed binary serialization MongoDB uses for documents.
- **Collection** — a schema-flexible grouping of documents, analogous to a table.
- **Compound index** — an index on multiple fields, where field order matters (see ESR rule).
- **Covered query** — a query answered entirely from an index, with no document fetch.
- **CRUD** — create, read, update, delete (insertOne/find/updateOne/deleteOne and their variants).
- **Document** — a field-and-value record (BSON) with a unique `_id`, the unit of storage in MongoDB.
- **Embedding vs referencing** — storing related data within one document (embedding) versus in separate documents linked by `_id` (referencing).
- **ESR rule** — the compound-index field order: Equality, then Sort, then Range.
- **explain** — a command returning the query plan (index use, documents examined, winning plan).
- **mongos** — the query router that directs operations across shards using config-server metadata.
- **mongosh** — the MongoDB Shell, the interactive JavaScript interface to a MongoDB deployment.
- **Read preference** — the rule for which replica-set members serve reads (primary, secondaryPreferred, etc.).
- **Replica set** — a group of mongod nodes with one primary and secondaries replicating the oplog for high availability.
- **SCRAM** — MongoDB's default username/password authentication mechanism.
- **Shard key** — the field(s) MongoDB uses to partition a sharded collection into chunks across shards.
- **Sharding** — horizontal partitioning of a collection across shards for scale.
- **Write concern** — the number of nodes that must acknowledge a write (e.g., `w:"majority"`) before it returns.
