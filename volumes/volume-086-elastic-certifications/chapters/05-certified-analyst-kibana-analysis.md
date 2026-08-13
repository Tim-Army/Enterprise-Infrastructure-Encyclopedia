# Chapter 05: Certified Analyst — Kibana Analysis and Visualization

## Learning Objectives

- Explore data in Discover with KQL.
- Build visualizations with Lens.
- Assemble a dashboard.
- Define a runtime field for on-the-fly values.
- Complete a walkthrough for each analysis-and-visualization topic.

## Theory and Architecture

The **Elastic Certified Analyst** validates Kibana mastery — turning indexed data into insight. It
starts in **Discover**, where you explore raw documents filtered with **KQL (Kibana Query Language)** and
a **data view** (the index pattern Kibana reads). Visualization is built in **Lens** — a drag-and-drop
builder for bar, line, area, pie, metric, and table visualizations backed by aggregations — and older
tools like TSVB for time series. Visualizations are assembled into **dashboards** with filters and time
ranges for interactive analysis. **Runtime fields** compute values at query time (from a Painless script
or a simpler expression) without reindexing — useful for deriving fields you did not index. This is a
**performance-based** exam: you build real analyses in Kibana. This chapter teaches Kibana analysis with
hands-on walkthroughs (Discover/KQL and the underlying aggregations via the API, plus Lens/dashboard
reasoning).

## Design Considerations

Filter in **Discover** with **KQL** to find the right documents fast. Build the simplest visualization
that answers the question in **Lens**; reserve TSVB/Vega for special cases. Compose **dashboards** with
shared filters and a sensible default time range. Use **runtime fields** to derive values without a
costly reindex — but index frequently queried fields for performance.

## Implementation and Automation

The labs filter data with KQL, model a Lens visualization from an aggregation, assemble a dashboard, and
define a runtime field — the analysis the Analyst exam validates.

## Validation and Troubleshooting

Confirm Kibana analysis:

```text
Discover: explore documents via a data view, filtered with KQL
Lens: drag-and-drop visualizations (bar/line/pie/metric/table) over aggregations
Dashboard: visualizations + filters + time range = interactive analysis
Runtime field: value computed at query time (Painless) — no reindex
```

Common pitfalls: writing KQL against the wrong **data view** (no results); and creating a **runtime
field** for a field you query constantly (slower than indexing it).

## Security and Best Practices

Give analysts read-only, space-scoped Kibana access; share dashboards rather than raw cluster
credentials. Analysis is authorized use of your own data. All work is authorized.

## Hands-On Lab

Analysis-and-visualization walkthroughs. **Shared prerequisites** — Kibana on an Elastic Stack with
sample data (e.g., the Kibana sample web logs), plus `curl` for the underlying API. **Cost:** none.

### Lab 5.1 — Filter data with KQL

**Objective:** Find the right documents in Discover.

```text
Kibana > Discover > data view: kibana_sample_data_logs
KQL:  response >= 500 and url : "*checkout*"
Time: Last 7 days
Result: only server-error requests to checkout URLs are shown
```

**Expected result:** Discover filtered to 5xx checkout requests — the subset you want to analyze.

**Negative test:** run the KQL against a data view that does not include the `response` field; it returns
nothing — select the correct data view.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Model a Lens visualization

**Objective:** Turn an aggregation into a chart.

```bash
curl -s -k -u elastic:$PW -X GET "https://localhost:9200/kibana_sample_data_logs/_search" -H 'Content-Type: application/json' -d'
{ "size": 0, "aggs": {
    "by_response": { "terms": { "field": "response.keyword" },
      "aggs": { "bytes": { "avg": { "field": "bytes" } } } } } }'
```

```json
{ "aggregations": { "by_response": { "buckets": [
  { "key": "200", "doc_count": 12000, "bytes": { "value": 5600.0 } },
  { "key": "404", "doc_count": 900,  "bytes": { "value": 3100.0 } } ] } } }
```

**Expected result:** the aggregation behind a Lens bar chart of average bytes by response code — a
visualization's data.

**Negative test:** build a Lens chart on a high-cardinality `text` field; aggregate on its `keyword`
sub-field instead.

**Rollback:** none (read-only).

### Lab 5.3 — Assemble a dashboard

**Objective:** Combine visualizations for analysis.

```text
Kibana > Dashboard > Create
  + Lens: "Requests by response code" (bar)
  + Lens: "Traffic over time" (line, date_histogram)
  + Metric: "Total bytes"
  Add a filter: geo.src : "US"; time range: Last 24 hours
Result: an interactive dashboard; the filter/time range apply to every panel
```

**Expected result:** a dashboard whose shared filter and time range drive all panels — interactive
analysis.

**Negative test:** build one giant visualization instead of a filtered dashboard; a **dashboard** lets
viewers slice all panels at once.

**Rollback:** delete the practice dashboard if not needed.

### Lab 5.4 — Define a runtime field

**Objective:** Derive a value without reindexing.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/kibana_sample_data_logs/_mapping" -H 'Content-Type: application/json' -d'
{ "runtime": { "is_error": {
    "type": "boolean",
    "script": { "source": "emit(doc[\"response.keyword\"].value.startsWith(\"5\"))" } } } }'
```

```json
{ "acknowledged": true }
```

**Expected result:** a runtime `is_error` field computed at query time from the response code — no
reindex needed.

**Negative test:** reindex the whole dataset just to add a derived flag; a **runtime field** computes it
on the fly.

**Rollback:**

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/kibana_sample_data_logs/_mapping" -H 'Content-Type: application/json' -d'{ "runtime": { "is_error": null } }'
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Certified Analyst turns data into insight in Kibana: exploring documents in Discover with KQL,
building visualizations in Lens over aggregations, assembling interactive dashboards with shared filters
and time ranges, and deriving values with runtime fields without reindexing.

- [ ] I can filter data with KQL in Discover.
- [ ] I can model a Lens visualization from an aggregation.
- [ ] I can assemble a dashboard.
- [ ] I can define a runtime field.
- [ ] I completed Labs 5.1–5.4 including each negative test.
