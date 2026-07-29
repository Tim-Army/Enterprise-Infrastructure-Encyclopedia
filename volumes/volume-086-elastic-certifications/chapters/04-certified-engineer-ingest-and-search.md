# Chapter 04: Certified Engineer — Ingest and Search

## Learning Objectives

- Define and use an ingest pipeline with processors.
- Write and execute Query DSL searches (boolean, term/phrase).
- Write and execute metric and bucket aggregations.
- Write and execute an ES|QL query.
- Complete a walkthrough for each ingest-and-search topic.

## Theory and Architecture

The **Certified Engineer** exam's **Data Ingestion** and **Searching Data** domains cover how data is
transformed on the way in and queried on the way out. An **ingest pipeline** runs **processors** (grok,
dissect, date, geoip, convert, set, rename, remove, json, split, and more) to parse and enrich documents
before indexing. On the query side, **Query DSL** is Elasticsearch's JSON query language — leaf queries
(`term`, `match`, `range`) combined with the `bool` query (`must`, `should`, `filter`, `must_not`).
**Aggregations** summarize data: **metric** aggregations (`avg`, `sum`, `max`, cardinality) and
**bucket** aggregations (`terms`, `date_histogram`, `range`), which can nest. New in the 9.3 blueprint,
**ES|QL** (the Elasticsearch Query Language) is a piped, SQL-like language for querying and aggregating,
and **semantic search** uses vector embeddings for meaning-based retrieval. This chapter teaches ingest
and search with hands-on Elasticsearch API walkthroughs.

## Design Considerations

Parse and enrich at ingest with a **pipeline** so documents are clean and typed before indexing. Use the
**`bool` query** to combine conditions, and put non-scoring conditions in **`filter`** (cacheable, no
relevance cost). Choose the right **aggregation** — metric for numbers, bucket for grouping — and mind
cardinality. Reach for **ES|QL** for quick, composable analytics and **semantic search** for
meaning-based retrieval.

## Implementation and Automation

The labs create an ingest pipeline, run a boolean Query DSL search, run a bucketed aggregation, and run
an ES|QL query — the ingest and search the Engineer exam validates.

## Validation and Troubleshooting

Confirm ingest and search:

```text
Ingest pipeline: processors (grok/dissect/date/geoip/convert/set/rename/remove/json/split) enrich docs
Query DSL: leaf (term/match/range) + bool (must/should/filter/must_not); filter = cacheable, no scoring
Aggregations: metric (avg/sum/max/cardinality) + bucket (terms/date_histogram/range), nestable
ES|QL: piped SQL-like query+aggregate; semantic search = vector/meaning-based retrieval
```

Common pitfalls: putting exact-match conditions in **`must`** (pays a relevance cost) instead of
**`filter`**; and parsing logs at query time instead of enriching once at **ingest**.

## Security and Best Practices

Enrich at ingest, filter with cacheable clauses, and scope search with least-privilege API keys. Well
-structured queries are efficient and safe on shared clusters. All work is authorized.

## Hands-On Lab

Ingest-and-search walkthroughs. **Shared prerequisites** — an Elasticsearch cluster at
`https://localhost:9200` with sample data, `curl`. **Cost:** none.

### Lab 4.1 — Define an ingest pipeline

**Objective:** Parse and enrich on the way in.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/_ingest/pipeline/weblog" -H 'Content-Type: application/json' -d'
{ "processors": [
    { "grok": { "field": "message",
        "patterns": ["%{IP:client_ip} %{WORD:method} %{URIPATHPARAM:request}"] } },
    { "geoip": { "field": "client_ip", "target_field": "geo" } },
    { "date": { "field": "ts", "formats": ["ISO8601"] } } ] }'
```

```json
{ "acknowledged": true }
```

**Expected result:** a pipeline that greps the log line, adds geo from the IP, and parses the date —
enriched documents.

**Negative test:** index raw log strings and parse at search time; enrich once at **ingest** for
efficient, structured queries.

**Cleanup:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_ingest/pipeline/weblog"
```

### Lab 4.2 — Run a boolean Query DSL search

**Objective:** Combine conditions correctly.

```bash
curl -s -k -u elastic:$PW -X GET "https://localhost:9200/orders/_search" -H 'Content-Type: application/json' -d'
{ "query": { "bool": {
    "must":   [ { "match": { "customer": "acme" } } ],
    "filter": [ { "range": { "amount": { "gte": 100 } } } ] } } }'
```

```json
{ "hits": { "total": { "value": 12 }, "hits": [ { "_source": { "customer": "Acme Corp", "amount": 250 } } ] } }
```

**Expected result:** matches for the customer with the amount filter applied — a correct boolean query.

**Negative test:** put the `range` in `must`; it needlessly influences relevance scoring — use `filter`
for exact/range conditions.

**Cleanup:** none (read-only).

### Lab 4.3 — Run a bucket aggregation

**Objective:** Group and summarize data.

```bash
curl -s -k -u elastic:$PW -X GET "https://localhost:9200/orders/_search" -H 'Content-Type: application/json' -d'
{ "size": 0, "aggs": {
    "by_day": { "date_histogram": { "field": "ordered_at", "calendar_interval": "day" },
      "aggs": { "revenue": { "sum": { "field": "amount" } } } } } }'
```

```json
{ "aggregations": { "by_day": { "buckets": [
  { "key_as_string": "2026-07-28", "doc_count": 40, "revenue": { "value": 10250.0 } } ] } } }
```

**Expected result:** daily buckets with a summed-revenue metric nested inside — grouped analytics.

**Negative test:** request `size: 10000` hits when you only need aggregates; set `size: 0` so the query
returns aggregations without documents.

**Cleanup:** none (read-only).

### Lab 4.4 — Run an ES|QL query

**Objective:** Query and aggregate with ES|QL.

```bash
curl -s -k -u elastic:$PW -X POST "https://localhost:9200/_query?format=txt" -H 'Content-Type: application/json' -d'
{ "query": "FROM orders | STATS revenue = SUM(amount) BY customer | SORT revenue DESC | LIMIT 5" }'
```

```text
    revenue |   customer
------------+-----------
    10250.0 | Acme Corp
     8400.0 | Globex
```

**Expected result:** the top customers by revenue via a piped ES|QL query — the 9.3 blueprint's new
query language.

**Negative test:** ignore ES|QL and expect only Query DSL on the 9.3 exam; **ES|QL** is now a tested
topic — learn it.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Certified Engineer's ingest and search skills are ingest pipelines with enrichment processors,
Query DSL with the bool query and cacheable filters, metric and bucket aggregations, and the new
piped ES|QL language plus semantic search — the data-in and data-out of Elasticsearch.

- [ ] I can define and use an ingest pipeline.
- [ ] I can write a boolean Query DSL search.
- [ ] I can write a bucket aggregation.
- [ ] I can write an ES|QL query.
- [ ] I completed Labs 4.1–4.4 including each negative test.
