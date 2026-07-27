# Chapter 07: Cribl Search and Lake

## Learning Objectives

- Explain Cribl Search's query-in-place model.
- Write basic Search queries.
- Explain Cribl Lake storage and datasets.
- Connect Search, Lake, and Stream.
- Complete a walkthrough for each Search/Lake topic.

## Theory and Architecture

**Cribl Search** queries data **where it lives** — object storage (S3/Blob/GCS), Cribl
Lake, or live sources — without first ingesting it into an expensive analytics platform,
using a **pipe-based query language** (dataset selection, filtering, aggregation). **Cribl
Lake** is managed, low-cost object storage organized into **datasets** with retention and
open formats, designed as the cheap **full-fidelity** tier that Stream writes to and Search
reads from, with **replay** back through Stream. Together they let you keep everything
affordably and query it on demand — the storage-and-query complement to Stream's
processing. These are covered by CC User (basics) and CC Engineer (design).

## Design Considerations

Use **Search** for ad-hoc investigation over data in place (avoid re-ingesting into premium
tools), write **Lake** datasets with appropriate retention, and design **Stream → Lake →
Search/replay** as the low-cost fidelity path. Query the right dataset with precise filters.

## Implementation and Automation

The labs write a Search query, describe Lake datasets, and connect the pieces.

## Validation and Troubleshooting

Confirm the model:

```text
Search: query-in-place over object storage/Lake/live; pipe language (dataset | where | summarize).
Lake: managed cheap object storage in datasets (retention, open formats). Stream writes; Search reads; replay back.
```

Common pitfalls: ingesting into a SIEM just to query (cost) when **Search** would do; and
Lake datasets with no retention policy.

## Security and Best Practices

Query **in place** with Search, store full fidelity cheaply in **Lake** with retention,
design the **Stream → Lake → Search/replay** path, and secure dataset access (RBAC).
Prefer Search for ad-hoc over premium-tool ingest.

## Hands-On Lab

Search/Lake walkthroughs. **Shared prerequisites** — a Cribl Search/Lake environment (or
the query patterns). **Cost:** none.

### Lab 7.1 — Basic Search query

**Objective:** Filter and aggregate in place.

```text
dataset="cribl_lake:app_logs"
| where level=="error"
| summarize count() by service
```

**Expected result:** error counts by service **queried in place** — no re-ingest.

**Negative test:** copy the dataset into a SIEM to run this; **Search** queries it where it
lives — save the ingest.

**Cleanup:** none.

### Lab 7.2 — Understand Lake datasets

**Objective:** Describe a Lake dataset.

```text
# A Lake dataset: named, retention-bounded, open-format object storage that Stream writes to.
# e.g., dataset 'app_logs' (30-day retention) written by a Stream S3/Lake destination.
"lake dataset: app_logs, 30d retention, open format"
```

**Expected result:** a Lake **dataset** with retention — the cheap fidelity tier.

**Negative test:** store full data in the SIEM's premium storage; **Lake** holds it cheaply
— write there.

**Cleanup:** none.

### Lab 7.3 — Stream writes to Lake

**Objective:** Route full-fidelity data to Lake.

```json
{ "type": "cribl_lake", "id": "to_lake", "dataset": "app_logs" }
```

**Expected result:** a Stream **Lake destination** writing the full copy — the fidelity
path.

**Negative test:** drop full data because it's "too much"; **write it to Lake** cheaply and
reduce only what goes to premium tools.

**Cleanup:** remove the destination.

### Lab 7.4 — Search plus replay

**Objective:** Investigate then rehydrate.

```text
# Investigate in Lake with Search; if you need it in the SIEM, replay the window through Stream.
# Search finds the incident; replay Lake -> Stream -> SIEM for the affected time range.
"search (find) -> replay (rehydrate the window to the SIEM)"
```

**Expected result:** the **search-then-replay** workflow — full access without keeping
everything hot.

**Negative test:** keep all data hot in the SIEM for rare investigations; **search + replay**
delivers it on demand cheaply.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cribl Search queries data in place (no re-ingest) and Cribl Lake stores full fidelity
cheaply in datasets, forming the Stream → Lake → Search/replay low-cost path. This chapter
queried in place, described Lake datasets, wrote to Lake, and used search-plus-replay.

- [ ] I can explain query-in-place Search.
- [ ] I can write a basic Search query.
- [ ] I can describe Lake datasets and retention.
- [ ] I can connect Stream, Lake, Search, and replay.
- [ ] I completed Labs 7.1–7.4 including each negative test.
