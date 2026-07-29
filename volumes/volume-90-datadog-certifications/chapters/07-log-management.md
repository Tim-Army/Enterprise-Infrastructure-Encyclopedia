# Chapter 07: Log Management

## Learning Objectives

- Collect logs with the Datadog Agent.
- Parse and enrich logs with pipelines and processors.
- Reason about indexes, retention, and exclusion filters.
- Use facets to search and analyze logs.
- Complete a walkthrough for each log-management topic.

## Theory and Architecture

The **Log Management Fundamentals** exam covers collecting, processing, and analyzing logs. The **Agent**
tails log files (or receives logs via API/integrations) and ships them to Datadog. On ingestion, logs
flow through **pipelines** of **processors** that structure and enrich them: a **grok parser** extracts
fields from unstructured text, a **remapper** maps a field to a standard attribute (status, service,
trace_id), a **date remapper** sets the official timestamp, a **category processor** buckets values, and
more. Structured logs land in **indexes** with a **retention** period; **exclusion filters** drop or
sample high-volume, low-value logs to control cost (Datadog's **Logging without Limits** ingests
everything but you index selectively). **Facets** (indexed attributes) make fields searchable and
aggregatable in the Log Explorer, and you can pivot logs into metrics or archive them to object storage
(and **rehydrate** on demand). This chapter teaches log management with hands-on walkthroughs.

## Design Considerations

Collect logs with the **Agent** and correlate them to traces via `trace_id` and unified service tags.
**Parse** unstructured logs with a **grok** processor and **remap** to standard attributes so they are
searchable. Index the logs you query and use **exclusion filters** to drop/sample noise (control cost).
Create **facets** for the fields you filter on. Archive to object storage for cheap long-term retention
and **rehydrate** when needed.

## Implementation and Automation

The labs configure log collection, build a grok pipeline, and reason about indexes/exclusion filters and
facets — the log management the exam validates.

## Validation and Troubleshooting

Confirm log management:

```text
Collect: Agent tails files / API / integrations -> Datadog
Pipeline processors: grok parser (extract fields) + remapper (standard attrs) + date remapper + category
Indexes + retention; exclusion filters drop/sample noise (Logging without Limits = ingest all, index some)
Facets = indexed attributes (search/aggregate) in Log Explorer; archive + rehydrate for long-term
```

Common pitfalls: indexing **everything** (cost) — use **exclusion filters**; and leaving logs
**unparsed** so you cannot facet/search on fields — add a **grok** processor.

## Security and Best Practices

Scrub sensitive data from logs (PII), correlate to traces for context, and control cost with exclusion
filters and archives. Log management observes your own systems. All work is authorized.

## Hands-On Lab

Log-management walkthroughs. **Shared prerequisites** — a Datadog Agent with logs enabled, and a sample
log source; `python3`. **Cost:** none.

### Lab 7.1 — Collect logs with the Agent

**Objective:** Tail an application log.

```yaml
# /etc/datadog-agent/conf.d/myapp.d/conf.yaml
logs:
  - type: file
    path: /var/log/myapp/app.log
    service: checkout
    source: python
```

```bash
# enable logs globally in datadog.yaml: logs_enabled: true
sudo systemctl restart datadog-agent
datadog-agent status | grep -A2 "myapp"
```

```text
myapp
  - Type: file  Status: OK  (Bytes read: 10240)
```

**Expected result:** the Agent tailing `app.log` and shipping logs tagged `service:checkout`.

**Negative test:** ship logs with no `service`/`source`; set them so logs correlate and get the right
pipeline.

**Cleanup:** remove the conf if not needed.

### Lab 7.2 — Parse logs with a grok processor

**Objective:** Structure unstructured logs.

```python
python3 - <<'PY'
# a grok rule extracts fields from a log line (pipeline processor)
rule = r'%{ip:network.client.ip} %{word:http.method} %{notSpace:http.url} %{number:http.status_code}'
line = "203.0.113.7 GET /checkout 500"
# result of the grok parser:
parsed = {"network.client.ip": "203.0.113.7", "http.method": "GET",
          "http.url": "/checkout", "http.status_code": 500}
print("grok rule:", rule)
print("parsed:", parsed)
print("Now facetable/searchable by http.status_code, http.method, etc.")
PY
```

**Expected result:** the log line parsed into structured attributes — searchable and facetable fields.

**Negative test:** leave the log as raw text and try to alert on 5xx rate; **parse** `http.status_code`
first.

**Cleanup:** none.

### Lab 7.3 — Reason about indexes and exclusion filters

**Objective:** Control cost with selective indexing.

```python
python3 - <<'PY'
daily_logs = {"error": 50_000, "warn": 200_000, "info": 5_000_000, "debug": 20_000_000}
# index errors/warns fully; sample info; exclude debug
policy = {"error": "index 100%", "warn": "index 100%",
          "info": "index 10% (exclusion filter samples)", "debug": "exclude (drop)"}
for level, action in policy.items():
    print(f"{level:6} ({daily_logs[level]:>9,}/day): {action}")
print("Logging without Limits: ingest all, index selectively -> cost control")
PY
```

**Expected result:** a policy that indexes valuable logs fully, samples info, and drops debug — cost
control via exclusion filters.

**Negative test:** index all 25M logs/day including debug; use **exclusion filters** to sample/drop
low-value logs.

**Cleanup:** none.

### Lab 7.4 — Create a facet and search

**Objective:** Make a field searchable.

```python
python3 - <<'PY'
# create a facet on http.status_code, then search/aggregate
facet = "http.status_code"
query = f'service:checkout @{facet}:>=500'
print(f"Facet: @{facet} (indexed attribute)")
print(f"Log Explorer query: {query}")
print("Aggregate: count of 5xx by @http.url -> find the failing endpoint")
PY
```

**Expected result:** a facet on `http.status_code` enabling a 5xx search and aggregation by endpoint.

**Negative test:** grep raw messages for "500"; create a **facet** on the parsed field and search/aggregate
it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Datadog Log Management collects logs via the Agent, structures them through pipelines of processors (grok
parsing, remapping to standard attributes), indexes selected logs with retention while exclusion filters
control cost (Logging without Limits), and makes fields searchable and aggregatable as facets in the Log
Explorer — with archive-and-rehydrate for cheap long-term retention.

- [ ] I can collect logs with the Agent.
- [ ] I can parse logs with a grok processor.
- [ ] I can reason about indexes and exclusion filters.
- [ ] I can create a facet and search logs.
- [ ] I completed Labs 7.1–7.4 including each negative test.
