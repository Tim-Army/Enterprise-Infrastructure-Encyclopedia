# Chapter 03: CC Admin - Stream — Sources, Routes, and Pipelines

## Learning Objectives

- Explain what the CC Admin - Stream certifies and its prerequisite.
- Configure sources and destinations.
- Route data to pipelines with filters.
- Build pipelines that process events.
- Complete a walkthrough for each Stream-admin topic (part 1).

## Theory and Architecture

The **Cribl Certified Admin - Stream (CC Admin - Stream)** validates implementing,
managing, and optimizing **Cribl Stream** — it requires **CC User**. This chapter covers
the data-path building blocks: **Sources** (inputs — Splunk, syslog, HTTP, S3, Kafka,
OpenTelemetry) and **Destinations** (outputs), **Routes** (an ordered list that matches
events with a **filter expression** and sends them to a **Pipeline** and a **Destination**;
routes are evaluated top-down and can be **final** or fall through), and **Pipelines**
(ordered **Functions** that transform events — Chapter 04). Data preview lets you test
before deploying.

## Design Considerations

Order **Routes** carefully (first match wins unless non-final), write precise **filter
expressions**, and keep **Pipelines** focused. Use **data preview** on sample events before
committing, and commit/deploy through the distributed model (Chapter 08).

## Implementation and Automation

The labs use the Stream API/config for sources, routes, and pipelines.

## Validation and Troubleshooting

Confirm the model:

```text
Source (input) -> Route (filter expr -> Pipeline + Destination; ordered, final/fall-through) -> Pipeline (Functions) -> Destination.
Preview sample events before deploy.
```

Common pitfalls: a broad Route placed above a specific one (shadowing); and no data
**preview** before deploy.

## Security and Best Practices

Secure **sources/destinations** (TLS, auth/tokens), order **Routes** specific-first, write
tight **filters**, **preview** on samples, and deploy through commit/deploy. Monitor for
dropped/blocked data.

## Hands-On Lab

Stream-admin walkthroughs (part 1). **Shared prerequisites** — a Cribl Stream instance;
`$CRIBL`/`$CRIBL_TOKEN`. **Cost:** none.

### Lab 3.1 — Add a source

**Objective:** Describe configuring an input.

```json
{ "type": "http", "id": "http_in", "port": 10080, "authTokens": ["<token>"] }
```

**Expected result:** an **HTTP source** definition listening on 10080 — a data entry point.

**Negative test:** expect events with no matching Source type for the sender; match the
**Source** to the sender's protocol (HTTP/syslog/TCP/S3/…).

**Rollback:** delete the source if it was for the lab.

### Lab 3.2 — Create a route with a filter

**Objective:** Match events to a pipeline.

```json
{ "id": "errors_route", "filter": "sourcetype=='app' && level=='error'",
  "pipeline": "errors_pipeline", "output": "s3_errors", "final": true }
```

**Expected result:** a Route sending **app error** events to a pipeline + destination — the
routing decision.

**Negative test:** put a catch-all `filter: true` route first; it **shadows** everything
below — order specific routes first.

**Rollback:** delete the route.

### Lab 3.3 — Build a pipeline

**Objective:** Define a processing pipeline.

```json
{ "id": "errors_pipeline", "conf": { "functions": [
  { "id": "eval", "conf": { "add": [{ "name": "severity", "value": "'high'" }] } }
] } }
```

**Expected result:** a pipeline with an **Eval** function adding a field — event
transformation.

**Negative test:** transform events inside a Route; **Pipelines** hold the Functions —
Routes only direct.

**Rollback:** delete the pipeline.

### Lab 3.4 — Preview on sample data

**Objective:** Test the pipeline before deploy.

```text
# In the UI/API: attach a sample capture to the pipeline, run preview,
#   confirm the OUT events show the added 'severity' field before committing.
"preview: sample IN -> pipeline -> OUT shows severity=high"
```

**Expected result:** previewed OUT events showing the change — validated before deploy.

**Negative test:** deploy a pipeline untested; **preview** on samples catches mistakes
first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.5 — Add a destination

**Objective:** Configure an output.

```json
{ "type": "s3", "id": "s3_errors", "bucket": "obs-errors", "region": "us-east-1" }
```

**Expected result:** an **S3 destination** for processed data — where events exit.

**Negative test:** process without a Destination; data has nowhere to go — configure the
output.

**Rollback:** delete the destination.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CC Admin - Stream (part 1) covers the data path: Sources and Destinations, Routes that
match events with filters and send them to Pipelines, and Pipelines of Functions —
validated with data preview. This chapter configured each.

- [ ] I can configure sources and destinations.
- [ ] I can route data with ordered filters.
- [ ] I can build a processing pipeline.
- [ ] I can preview on sample data before deploy.
- [ ] I completed Labs 3.1–3.5 including each negative test.
