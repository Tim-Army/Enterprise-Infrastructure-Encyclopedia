# Chapter 03: Certified Engineer — Data Management

## Learning Objectives

- Define an index with explicit mappings.
- Create and use a dynamic template.
- Create an index template that provisions a data stream.
- Define an ILM policy for a time-series index.
- Complete a walkthrough for each data-management topic.

## Theory and Architecture

The **Elastic Certified Engineer** exam's **Data Management** domain is the heart of Elasticsearch
administration. An **index** stores JSON documents; its **mapping** defines each field's data type
(`keyword`, `text`, `date`, `long`, `geo_point`, and so on) — explicit mappings prevent surprises.
**Dynamic templates** apply mapping rules to new fields by name or type. For time-series data (logs,
metrics), you use an **index template** that provisions a **data stream** — an abstraction over a series
of hidden, auto-rolled-over backing indices — and an **Index Lifecycle Management (ILM)** policy that
rolls the write index over at a size/age and moves aging indices through hot → warm → cold → frozen
tiers and eventually deletes them. **Aliases** give a stable name that points at one or more indices for
zero-downtime reindexing. This chapter teaches data management with hands-on Elasticsearch API
walkthroughs.

## Design Considerations

Define **explicit mappings** for known fields and use **dynamic templates** for predictable new ones.
Model time-series data as **data streams** with an **index template** and an **ILM** policy sized to your
retention and cost targets. Use **aliases** for stable names and safe reindexing. Choose field types
deliberately — `keyword` for exact match/aggregation, `text` for full-text search.

## Implementation and Automation

The labs define an index with mappings, add a dynamic template, create a data-stream index template, and
attach an ILM policy — the data management the Engineer exam validates.

## Validation and Troubleshooting

Confirm data management:

```text
Index + mapping (keyword/text/date/long/geo_point); explicit > dynamic surprises
Dynamic template: rules for new fields by name/type
Data stream: index template -> hidden backing indices, auto rollover (time-series)
ILM: rollover + hot->warm->cold->frozen + delete; alias = stable name for reindex
```

Common pitfalls: letting Elasticsearch **dynamically map** a numeric ID as `text` (wrong type for
aggregation); and time-series data with no **ILM** (indices grow unbounded).

## Security and Best Practices

Explicit mappings and ILM keep data typed, sized, and retained per policy. Least-privilege API keys for
indexing (Chapter 09) protect the cluster. All work is authorized administration.

## Hands-On Lab

Data-management walkthroughs. **Shared prerequisites** — an Elasticsearch cluster at
`https://localhost:9200`, `curl`. **Cost:** none.

### Lab 3.1 — Define an index with mappings

**Objective:** Type the fields explicitly.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/orders" -H 'Content-Type: application/json' -d'
{ "mappings": { "properties": {
    "order_id":  { "type": "keyword" },
    "customer":  { "type": "text" },
    "amount":    { "type": "double" },
    "ordered_at":{ "type": "date" } } } }'
```

```json
{ "acknowledged": true, "shards_acknowledged": true, "index": "orders" }
```

**Expected result:** an `orders` index with typed fields — `keyword` for exact IDs, `text` for search.

**Negative test:** index `order_id` as `text` and try to aggregate on it; use `keyword` for exact-match
and aggregation fields.

**Cleanup:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/orders"
```

### Lab 3.2 — Add a dynamic template

**Objective:** Map new fields by rule.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/logs-dyn" -H 'Content-Type: application/json' -d'
{ "mappings": { "dynamic_templates": [
    { "strings_as_keyword": {
        "match_mapping_type": "string",
        "mapping": { "type": "keyword" } } } ] } }'
```

```json
{ "acknowledged": true, "index": "logs-dyn" }
```

**Expected result:** new string fields automatically mapped as `keyword` — predictable dynamic mapping.

**Negative test:** rely on default dynamic mapping (strings become `text` + `keyword` multi-field,
doubling storage); a **dynamic template** controls it.

**Cleanup:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/logs-dyn"
```

### Lab 3.3 — Create a data-stream index template

**Objective:** Provision time-series storage.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/_index_template/logs-app" -H 'Content-Type: application/json' -d'
{ "index_patterns": ["logs-app-*"],
  "data_stream": {},
  "template": { "mappings": { "properties": {
      "@timestamp": { "type": "date" },
      "message":    { "type": "text" } } } } }'
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/_data_stream/logs-app-default"
```

```json
{ "acknowledged": true }
```

**Expected result:** a data stream `logs-app-default` backed by auto-rolled-over indices — time-series
ready.

**Negative test:** write time-series logs to one ever-growing index; use a **data stream** so rollover
manages size.

**Cleanup:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_data_stream/logs-app-default"
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_index_template/logs-app"
```

### Lab 3.4 — Define an ILM policy

**Objective:** Automate the index lifecycle.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/_ilm/policy/logs-policy" -H 'Content-Type: application/json' -d'
{ "policy": { "phases": {
    "hot":    { "actions": { "rollover": { "max_age": "7d", "max_primary_shard_size": "50gb" } } },
    "warm":   { "min_age": "30d", "actions": { "forcemerge": { "max_num_segments": 1 } } },
    "delete": { "min_age": "90d", "actions": { "delete": {} } } } } }'
```

```json
{ "acknowledged": true }
```

**Expected result:** an ILM policy rolling over at 7 days/50GB, warming at 30 days, deleting at 90 —
lifecycle automated.

**Negative test:** keep every index on the hot tier indefinitely; storage and cost grow without bound —
attach an **ILM** policy.

**Cleanup:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_ilm/policy/logs-policy"
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Certified Engineer's data management is explicit index mappings and dynamic templates for field
typing, data streams provisioned by index templates for time-series data, and ILM policies that roll
over, tier, and delete indices — with aliases giving stable names for safe reindexing.

- [ ] I can define an index with explicit mappings.
- [ ] I can create and use a dynamic template.
- [ ] I can create a data-stream index template.
- [ ] I can define an ILM policy.
- [ ] I completed Labs 3.1–3.4 including each negative test.
