# Chapter 04: CC Admin - Stream — Functions, Packs, and Optimization

## Learning Objectives

- Use functions to reduce, enrich, and transform events.
- Mask sensitive data and enrich with lookups.
- Package reusable content as Packs.
- Optimize for cost and performance.
- Complete a walkthrough for each Stream-admin topic (part 2).

## Theory and Architecture

The heart of Stream is the **Function** — a step in a pipeline that operates on events.
Key functions: **Eval** (add/modify fields), **Drop**/**Sampling**/**Suppress** (reduce
volume), **Aggregations** (roll up to metrics), **Mask** (redact sensitive data),
**Parser** (extract structure), and **Lookup** (enrich from a table). Reusable pipelines,
routes, samples, and lookups bundle into **Packs** (shareable via the Cribl Packs
dispatcher). The whole point is **optimization**: reduce and shape data so downstream tools
ingest less (and cost less) while keeping fidelity. This is the core of CC Admin - Stream.

## Design Considerations

**Reduce** at the source of truth: drop null/duplicate fields, sample high-volume/low-value
data, and aggregate logs to metrics where possible. **Enrich** with lookups, **mask** PII
before it leaves, and package repeatable logic as **Packs**. Measure the reduction
(bytes in vs out).

## Implementation and Automation

The labs use functions (eval, drop, mask, lookup), a Pack, and a reduction check.

## Validation and Troubleshooting

Confirm the tools:

```text
Functions: Eval, Drop/Sampling/Suppress, Aggregations, Mask, Parser, Lookup.
Packs: reusable pipelines/routes/lookups/samples. Optimize: reduce volume (bytes in vs out).
```

Common pitfalls: reducing data you later need (over-aggressive drop); and unmasked PII
reaching destinations.

## Security and Best Practices

**Reduce** low-value data, **enrich** with lookups, **mask PII** before egress, package
reusable logic in **Packs**, and continuously measure the **reduction ratio**. Keep raw
copies (to Lake) where compliance requires.

## Hands-On Lab

Stream-admin walkthroughs (part 2). **Shared prerequisites** — a Cribl Stream instance with
a pipeline. **Cost:** none.

### Lab 4.1 — Drop to reduce volume

**Objective:** Drop low-value events.

```json
{ "id": "drop", "conf": { "filter": "level=='debug'" } }
```

**Expected result:** a **Drop** function removing debug events — volume reduction.

**Negative test:** forward every debug line to an expensive SIEM; **drop/sample** low-value
data to cut cost.

**Rollback:** remove the function.

### Lab 4.2 — Mask sensitive data

**Objective:** Redact PII in-flight.

```json
{ "id": "mask", "conf": { "rules": [
  { "matchRegex": "/(\\d{3}-\\d{2})-\\d{4}/", "replaceExpr": "`${g1}-XXXX`" }
] } }
```

**Expected result:** SSNs partially **masked** before egress — data protection in the
pipeline.

**Negative test:** mask at the destination; **mask in Stream** so PII never leaves in the
clear.

**Rollback:** remove the function.

### Lab 4.3 — Enrich with a lookup

**Objective:** Add context from a lookup table.

```json
{ "id": "lookup", "conf": { "matchMode": "exact", "matchType": "first",
  "file": "hosts.csv", "inFields": [{ "eventField": "host" }],
  "outFields": [{ "lookupField": "owner", "eventField": "owner" }] } }
```

**Expected result:** an **`owner`** field added from the lookup — enrichment.

**Negative test:** hard-code owner mappings in an Eval; a **lookup table** is maintainable
and reusable.

**Rollback:** remove the function.

### Lab 4.4 — Package a Pack

**Objective:** Bundle reusable content.

```text
# A Pack bundles pipelines, routes, lookups, and samples into a versioned, shareable unit.
# Export the pipeline + lookup above as a Pack; import it into another worker group.
"pack: reusable pipelines/lookups shared across environments"
```

**Expected result:** a **Pack** of reusable content — portability across environments.

**Negative test:** rebuild the same pipelines per environment; a **Pack** packages them
once — reuse.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — Measure the reduction

**Objective:** Confirm bytes-in vs bytes-out.

```bash
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" "$CRIBL/api/v1/system/metrics?filterExp=..." 2>/dev/null \
  | python3 -c "import sys;print('compare inBytes vs outBytes for the route/pipeline')" 
# Cribl Monitoring shows in/out volume and the reduction ratio per pipeline/route.
```

**Expected result:** the **in-vs-out** volume (reduction ratio) — the optimization metric.

**Negative test:** claim reduction without measuring; **track in/out bytes** to prove it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CC Admin - Stream (part 2) is the value of Cribl: functions to reduce (drop/sample/
aggregate), mask, and enrich (lookup), packaged as reusable Packs, with optimization
measured by the reduction ratio. This chapter applied each.

- [ ] I can reduce volume with drop/sampling.
- [ ] I can mask sensitive data in-flight.
- [ ] I can enrich with lookups.
- [ ] I can package Packs and measure reduction.
- [ ] I completed Labs 4.1–4.5 including each negative test.
