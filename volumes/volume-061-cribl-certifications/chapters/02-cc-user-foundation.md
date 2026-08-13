# Chapter 02: CC User — Foundation

## Learning Objectives

- Explain what the CC User certifies and its scope.
- Describe deployment options and the four products.
- Configure a basic Stream source, pipeline, and destination.
- Run a basic Search query and understand Lake.
- Complete a walkthrough for each foundation topic.

## Theory and Architecture

The **Cribl Certified User (CC User)** is the foundation credential — it introduces the
whole platform. Its topics: **deployment options** (single-instance vs distributed;
Cribl.Cloud vs on-prem), the **components** of **Stream** (Sources → Routes → Pipelines →
Destinations), **Edge** (nodes/fleets collecting at the source), **Search** (query in
place), and **Lake** (storage), plus **basic configuration**, **queries**, and **pipeline
operation**. It is the prerequisite for the Admin certifications.

## Design Considerations

Understand the **data flow**: data enters via a **Source**, a **Route** matches it to a
**Pipeline**, the pipeline's **Functions** transform it, and it exits to a **Destination**.
Know when to use each **product** (Stream to process, Edge to collect, Search to query in
place, Lake to store). Start on **Cribl.Cloud free**.

## Implementation and Automation

The labs use Stream config and the API for each foundation topic.

## Validation and Troubleshooting

Confirm the topics:

```text
CC User: deployment options; Stream/Edge/Search/Lake components; basic config; queries; pipeline operation.
Stream flow: Source -> Route -> Pipeline (Functions) -> Destination.
```

Common pitfalls: confusing **Routes** (match/direct) with **Pipelines** (transform); and
single-instance thinking where distributed is needed.

## Security and Best Practices

Learn the **Source → Route → Pipeline → Destination** flow, pick the right **product** per
task, use **Cribl.Cloud free** to practice, and secure sources/destinations (TLS, auth,
tokens). Understand deployment topologies before scaling.

## Hands-On Lab

Foundation walkthroughs. **Shared prerequisites** — a Cribl Stream instance (free tier);
`$CRIBL`/`$CRIBL_TOKEN`. **Cost:** none.

### Lab 2.1 — List sources

**Objective:** Enumerate configured input sources.

```bash
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" "$CRIBL/api/v1/system/inputs" \
  | python3 -c "import sys,json;print('sources:',len(json.load(sys.stdin).get('items',[])))"
```

**Expected result:** the count of configured **Sources** — where data enters Stream.

**Negative test:** expect data to flow with no Source configured; a **Source** is the entry
point — configure one.

**Rollback:** none (read-only).

### Lab 2.2 — Understand the pipeline flow

**Objective:** State the Stream data flow.

```bash
python3 - <<'PY'
flow=["Source (in)","Route (match -> send to pipeline)","Pipeline (Functions transform)","Destination (out)"]
print(" -> ".join(flow))
PY
```

**Expected result:** **Source → Route → Pipeline → Destination** — the core Stream model.

**Negative test:** put transform logic in a Route; **Routes** match/direct, **Pipelines**
transform — separate the concerns.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — List destinations

**Objective:** Enumerate output destinations.

```bash
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" "$CRIBL/api/v1/system/outputs" \
  | python3 -c "import sys,json;print('destinations:',len(json.load(sys.stdin).get('items',[])))"
```

**Expected result:** the configured **Destinations** — where processed data exits.

**Negative test:** process data with no Destination; it has nowhere to go — configure an
output.

**Rollback:** none (read-only).

### Lab 2.4 — Basic Search query

**Objective:** Describe a query-in-place search.

```text
# Cribl Search (Kusto-like): query data where it lives (S3, Lake, live) without moving it.
dataset="cribl_search_sample" | limit 10
```

**Expected result:** a Search query returning sample rows — the query-in-place model.

**Negative test:** copy data to a warehouse just to query it; **Search** queries in place —
avoid the movement.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.5 — Deployment options

**Objective:** Distinguish single-instance from distributed.

```text
# Single-instance: one process (UI + worker). Distributed: a Leader + Worker Groups (scale).
# Cribl.Cloud (managed) vs on-prem (self-managed).
"foundation: know single vs distributed, Cloud vs on-prem"
```

**Expected result:** the deployment options — the foundation for sizing/scaling.

**Negative test:** run a single instance for a large fleet; a **distributed** Leader +
Workers scales — plan the topology.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CC User certifies foundation knowledge across Cribl: deployment options, the four
products, and the Stream flow (Source → Route → Pipeline → Destination) with basic config,
queries, and pipeline operation.

- [ ] I can describe deployment options and the products.
- [ ] I can explain the Stream data flow.
- [ ] I can list sources and destinations.
- [ ] I can describe Search (query-in-place) and Lake.
- [ ] I completed Labs 2.1–2.5 including each negative test.
