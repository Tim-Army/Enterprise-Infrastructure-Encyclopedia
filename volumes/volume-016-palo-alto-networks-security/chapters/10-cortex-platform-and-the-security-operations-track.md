# Chapter 10: The Cortex Platform and the Security Operations Track

## Learning Objectives

- Map Palo Alto Networks' Security Operations certification track:
  Security Operations Professional, Security Operations Architect, and
  the role-based XSIAM/XDR/XSOAR credentials beneath them
- Explain the Cortex platform — XSIAM, XDR, XSOAR, and Xpanse — and how
  the modern SOC consolidates onto it
- Position this track against the Network Security track (Chapters
  01–08) and the Cloud Security track (Chapters 09, 12)
- Choose a SecOps certification by role and sequence the study path

## Theory and Architecture

### The track in one sentence

Palo Alto Networks retired its exam-coded certifications (PCDRA and
peers) into a **role-based program** across three tracks — Network
Security, Security Operations, and Cloud Security. The Security
Operations track certifies the Cortex-powered SOC: **Security
Operations Professional** is the track's applied generalist (covering
XDR, XSOAR, and XSIAM; digital-learning delivered, launched 30 May
2025), **Security Operations Architect** is its design apex, and
beneath them sit the platform-specific role certs — **XSIAM Analyst,
XSIAM Engineer, XDR Analyst, XDR Engineer, XSOAR Engineer** (the XDR
pair launched 29 April 2025, superseding PCDRA). All were verified
against Palo Alto Networks' certification pages on **22 July 2026**;
those pages are the authority on objectives and delivery.

### Cortex: four products, one SOC

**Cortex XSIAM** (Extended Security Intelligence and Automation
Management) is the AI-driven SOC platform — a SIEM successor that
ingests everything, correlates with machine learning, and drives
automated response. **Cortex XDR** is the endpoint-and-beyond
detection/response engine (agents, behavioral analytics, causality
chains). **Cortex XSOAR** is the orchestration-and-automation layer —
playbooks, case management, threat-intel management. **Cortex Xpanse**
is attack-surface management — the outside-in view of what the
internet can see. The track's certifications slice this platform by
role: analysts operate it, engineers deploy and tune it, architects
design it.

### Analyst versus Engineer versus Architect

The role split is the exam's organizing principle. **Analyst** certs
(XSIAM, XDR) validate the SOC operator: triage, investigation,
incident response, using the platform. **Engineer** certs (XSIAM,
XDR, XSOAR) validate the builder: installation, data-source
onboarding, integration configuration, playbook creation, and
detection engineering. **Architect** (SecOps) validates the designer:
sizing, data strategy, multi-tenant and integration architecture. The
same product, three depths — exactly the ladder this encyclopedia's
other vendor volumes teach.

## Design Considerations

- **Analyst or Engineer first?** SOC operators take the Analyst path
  (XDR or XSIAM Analyst) and add SecOps Professional for breadth;
  detection/automation engineers take the Engineer path
- **XDR or XSIAM?** XDR for endpoint-centric estates and the installed
  base; XSIAM where the SOC is consolidating SIEM + SOAR + XDR onto
  one platform — the strategic direction, so weight new study toward
  XSIAM
- **SecOps Architect is a capstone**, not an entry point: take it
  after an Engineer cert and real deployment experience
- Volume XI (observability) and Volume X (cybersecurity) are the
  systems substrate; this track is their SOC-product specialization

## Implementation and Automation

```text
# The Cortex platform, mapped to the SOC workflow the certs test
Ingest      -> XSIAM data sources / XDR agents / third-party feeds
Detect      -> analytics, correlation rules, behavioral models
Investigate -> causality chains, incident timelines (Analyst skills)
Respond     -> XSOAR playbooks, automated + analyst-gated actions
Manage      -> multi-tenant tenants, RBAC, content packs (Engineer)
Expose      -> Xpanse attack-surface findings feeding the queue

# Everything is API-addressable — the automation this repo's Volume IX
# generalizes, applied to the SOC:
GET  /public_api/v1/incidents        # XDR/XSIAM incident retrieval
POST /public_api/v1/xql_query        # XQL: the platform's query language
POST /xsoar/incident/{id}/investigate  # drive a playbook programmatically
```

## Validation and Troubleshooting

- Ingestion first: no data, no detection — verify data sources and
  parsing before tuning any rule (the Engineer exam's first instinct)
- Analyst triage order: incident → causality chain → affected assets
  → response, reading the platform's own timeline as truth
- Detection tuning is measured, not felt: false-positive/negative
  rates against a labeled set, the way Volume XI measures SLOs
- XSOAR playbook failures triage in the task graph — inputs, integration
  auth, conditional branches — before blaming content

## Security and Best Practices

- Least-privilege RBAC per tenant; SOC analyst roles cannot alter
  detection content or integrations
- API keys scoped and rotated; the platform that watches everything is
  itself a high-value target
- Content as code where possible: detection rules and playbooks under
  version control, promoted through environments (Volume IX doctrine)

## References and Knowledge Checks

- Palo Alto Networks certification pages for the Security Operations
  track (the authority on objectives and delivery)
- Cortex XSIAM, XDR, XSOAR, and Xpanse product documentation
- Volumes X and XI of this encyclopedia

Knowledge checks:

1. Place XSIAM, XDR, XSOAR, and Xpanse in the SOC workflow and name
   the certification role that operates each.
2. A candidate runs a small endpoint-focused SOC today but is
   consolidating tooling next year. Which analyst cert now, and why
   which engineer cert next?
3. Why is Security Operations Architect a capstone rather than an
   entry certification?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for the core **Cortex
platform / Security Operations** capabilities the XSIAM and XSOAR
certifications assume — data sources, ingestion, XQL query, correlation, and
incident management — mapped in the volume README's coverage table. The
Cortex datasheets sit behind a dynamic portal, so these labs map to the
platform's documented capability areas (re-check on the next currency
cycle). Each uses the Cortex REST API and ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 10.1–10.5** — a Cortex XSIAM/XDR tenant with
`$XSIAM_KEY`, `$XSIAM_ID`, and base URL `$XS` (else run against product
docs). All read-only. **Cost:** none.

### Lab 10.1 — Read platform data sources

**Objective:** List the data sources feeding the platform.

```bash
curl -sk -X POST "$XS/public_api/v1/data_sources/get_data_sources/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" -d '{"request_data":{}}' \
  | jq -r '.reply[] | "\(.name)\t\(.status)"' 2>/dev/null | head
```

**Expected result:** connected sources (firewall logs, EDR, cloud, identity)
with status — the platform correlates across all of them.

**Negative test:** a SOC fed by one source (network only) misses
endpoint/identity signal; cross-source correlation needs breadth of
ingestion.

**Cleanup:** none (read-only).

### Lab 10.2 — Confirm data ingestion and normalization

**Objective:** Verify events are ingested and mapped to the Cortex Data
Model.

```bash
curl -sk -X POST "$XS/public_api/v1/xql/start_xql_query/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" \
  -d '{"request_data":{"query":"dataset = xdr_data | fields _time, event_type | limit 5"}}' | jq -r '.reply'
```

**Expected result:** a query execution ID whose results show recent
normalized events — ingestion plus parsing into the data model.

**Negative test:** a custom log source with no parser lands as raw text and
is not queryable by field; normalization is what makes it analyzable.

**Cleanup:** none (read-only).

### Lab 10.3 — Query telemetry with XQL

**Objective:** Run an XQL query and read results.

```bash
QID=$(curl -sk -X POST "$XS/public_api/v1/xql/start_xql_query/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" \
  -d '{"request_data":{"query":"dataset = xdr_data | filter action_local_ip != null | comp count() by action_local_ip | sort desc count | limit 10"}}' | jq -r '.reply')
curl -sk -X POST "$XS/public_api/v1/xql/get_query_results/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" \
  -d "{\"request_data\":{\"query_id\":\"$QID\"}}" | jq -r '.reply.status'
```

**Expected result:** a `SUCCESS` status with top talkers by IP — XQL is the
platform's investigation and detection query language.

**Negative test:** querying a field that the source did not populate returns
nulls; know the data model each source maps to.

**Cleanup:** none (read-only).

### Lab 10.4 — Read correlation/detection rules

**Objective:** List the correlation rules that turn events into alerts.

```bash
curl -sk -X POST "$XS/public_api/v1/correlations/get_correlations/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" -d '{"request_data":{}}' \
  | jq -r '.reply[] | "\(.name)\t\(.enabled)"' 2>/dev/null | head
```

**Expected result:** correlation rules (built-in and custom) with enabled
state — the logic that promotes raw telemetry to alerts.

**Negative test:** a disabled correlation rule generates no alerts even as
matching events stream in; enablement, not authorship, activates detection.

**Cleanup:** none (read-only).

### Lab 10.5 — Manage an incident lifecycle

**Objective:** Read an incident and its aggregated alerts.

```bash
curl -sk -X POST "$XS/public_api/v1/incidents/get_incidents/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" -d '{"request_data":{"filters":[]}}' \
  | jq -r '.reply.incidents[0] | "\(.incident_id)\t\(.status)\t\(.alert_count) alerts"'
```

**Expected result:** an incident grouping multiple alerts with a status — the
platform reduces alert volume by aggregating related alerts into incidents.

**Negative test:** working individual alerts instead of incidents multiplies
analyst effort; incident grouping is the volume-reduction the platform
provides.

**Cleanup:** none (read-only).

### Lab 10.6 — SOC track-map planning (integrative)

Build the track map for your SOC role: pick analyst or engineer, pull
the objectives for the XDR/XSIAM cert that fits, and produce a
one-page study plan (cert order, Cortex products involved, digital-
learning modules, capstone). Where a Cortex evaluation tenant or the
free digital-learning labs are available, complete one guided XQL
investigation and document the causality chain; otherwise runbook the
investigation workflow against the product docs.

## Lab Verification

Verification means the study plan names the correct role certs in a
defensible order, every cert was confirmed live on Palo Alto's pages
the same day, and one investigation (real or runbooked) shows the
ingest → detect → investigate → respond path with evidence.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Security Operations track structure mapped by role
- [ ] Cortex XSIAM/XDR/XSOAR/Xpanse positioned in the SOC workflow
- [ ] Analyst/Engineer/Architect depths distinguished
- [ ] Role-appropriate cert chosen with a dated, live-verified plan
