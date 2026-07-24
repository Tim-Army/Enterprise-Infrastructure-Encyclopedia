# Chapter 11: Cortex XSIAM and XDR — Analyst and Engineer

## Learning Objectives

- Operate Cortex XDR/XSIAM as a SOC analyst: incident triage,
  causality analysis, investigation, and response (XDR Analyst, XSIAM
  Analyst)
- Engineer Cortex XDR/XSIAM: agent and data-source deployment,
  integration configuration, and detection engineering (XDR Engineer,
  XSIAM Engineer)
- Write and tune detection content and use XQL for investigation and
  correlation
- Distinguish the XDR and XSIAM certification scopes and choose between
  them

## Theory and Architecture

### Two products, one causality model

Cortex XDR pioneered **causality-based detection**: rather than
alerting on isolated events, it stitches process, network, and file
activity into a **causality chain** rooted at a causality group owner
(the initiating process), so an analyst reads an incident as a story,
not a pile of alerts. XSIAM generalizes this across all telemetry —
endpoint, network, cloud, identity — with the same investigation model
and adds SIEM-scale data management and native automation. The Analyst
certs test reading and acting on these chains; the Engineer certs test
building the pipeline that produces them.

### The Analyst's platform

Analyst work is incident-centric: the incident view, the causality
chain, affected endpoints and users, artifact reputation (WildFire
verdicts), and the response verbs — isolate endpoint, terminate
process, block hash, initiate a playbook. XSIAM Analysts add
data-model fluency (the normalized schema queries run against) and
cross-source correlation. The exams live in exactly this operator
surface, and in the discipline of not closing what you have not
explained.

### The Engineer's platform

Engineer work is pipeline-centric: agent profiles and policy
(exploit/malware protection, host firewall), **data-source
onboarding** and parsing/normalization, integration configuration
(the connectors that feed detection and enable response), and
**detection engineering** — authoring correlation rules and BIOCs
(behavioral indicators of compromise) with measured precision. XSIAM
Engineers additionally own the data-management and multi-tenant
architecture that Analysts consume.

## Design Considerations

- Agent policy is a trade between protection and false positives;
  stage profiles by ring and measure before fleet rollout — the
  Engineer exam's judgment core
- Data-source onboarding order follows detection value: identity and
  EDR before low-signal firehoses; parsing correctness gates
  everything downstream
- Detection content is code: BIOCs and correlation rules versioned,
  peer-reviewed, and regression-tested against labeled data
- Analyst and Engineer certs are complementary, not a ladder — many
  SOCs want both skill sets on the same person for small teams

## Implementation and Automation

```text
# XQL — the investigation and detection language both roles use
dataset = xdr_data
| filter event_type = ENUM.PROCESS and action_process_image_name in ("powershell.exe","wscript.exe")
| filter action_process_image_command_line contains "-enc"
| comp count() by agent_hostname, actor_effective_username
| sort desc count_

# Response, driven by API (Analyst actions, Engineer automation)
POST /public_api/v1/endpoints/isolate      { "endpoint_id": "..." }
POST /public_api/v1/scripts/run_script      # remediation at scale
POST /public_api/v1/incidents/update        # status, assignment, severity

# Detection-as-code: BIOC / correlation rules exported and version-controlled
```

## Validation and Troubleshooting

- Analyst: if the causality chain looks wrong, check agent data
  completeness before doubting the detection — gaps read as innocence
- Engineer: parsing/normalization first — a data source that ingests
  but does not normalize produces silent detection blind spots;
  validate the data model, not just the byte count
- Detection tuning: track precision/recall per rule; a noisy rule is
  an incident-response tax the whole SOC pays
- Integration failures surface as absent response actions — test each
  connector's auth and scopes in isolation

## Security and Best Practices

- Analyst roles: response permissions scoped; destructive actions
  (isolate, terminate) gated by approval where policy requires
- Engineer roles: separate content-authoring from production-promotion
  rights; no direct edits to live detection without review
- WildFire and threat-intel verdicts inform but do not replace
  analyst judgment on high-impact actions
- Tenant API keys least-privileged; agent tamper protection enabled

## References and Knowledge Checks

- Palo Alto Networks certification pages: XDR Analyst, XDR Engineer,
  XSIAM Analyst, XSIAM Engineer (objectives and delivery authority)
- Cortex XDR and XSIAM administrator and XQL documentation
- Volume X (detection/response doctrine) and XI (telemetry)

Knowledge checks:

1. What is a causality group owner, and why does it change how an
   analyst reads an incident?
2. An onboarded data source shows healthy ingestion but produces no
   detections. Name the Engineer-side cause you check first and why.
3. Give one scenario each where XDR is the right certification and
   where XSIAM is.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for the **XSIAM Analyst**
(investigate/respond) and **XSIAM Engineer** (ingest/detect/tune) capability
areas the two certifications assume — mapped in the volume README's coverage
table. The Cortex datasheets sit behind a dynamic portal, so these labs map
to each certification's documented capability areas (re-check on the next
currency cycle). Each uses the Cortex XSIAM/XDR REST API and ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 11.1–11.6** — a Cortex XSIAM/XDR tenant with
`$XSIAM_KEY`, `$XSIAM_ID`, base URL `$XS` (else a runbook against product
docs). **Cost:** none; response actions target a lab endpoint only.

### Lab 11.1 — Investigate an incident (Analyst)

**Objective:** Pull an incident's alerts and key artifacts.

```bash
curl -sk -X POST "$XS/public_api/v1/incidents/get_incident_extra_data/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" \
  -d '{"request_data":{"incident_id":"<id>","alerts_limit":50}}' \
  | jq -r '.reply.alerts.data[] | "\(.severity)\t\(.name)"' | head
```

**Expected result:** the incident's constituent alerts by severity — the
starting point of an analyst investigation.

**Negative test:** triaging by the incident title alone misses a low-severity
alert that is the true entry point; the alert breakdown is the investigation.

**Cleanup:** none (read-only).

### Lab 11.2 — Read an alert's causality chain (Analyst)

**Objective:** Trace the process causality behind an endpoint alert.

```bash
curl -sk -X POST "$XS/public_api/v1/alerts/get_alerts_multi_events/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" \
  -d '{"request_data":{"filters":[{"field":"alert_id_list","operator":"in","value":["<alert-id>"]}]}}' \
  | jq -r '.reply.events[] | "\(.action_process_image_name) -> \(.action_process_signature_status)"' | head
```

**Expected result:** the causality group (parent→child process tree) with
signature status — XDR's analytics show *why* an alert fired, not just that
it did.

**Negative test:** an alert with no causality context forces manual host
forensics; the causality chain is what makes triage fast.

**Cleanup:** none (read-only).

### Lab 11.3 — Take an endpoint response action (Analyst)

**Objective:** Isolate a compromised endpoint from the network.

```bash
curl -sk -X POST "$XS/public_api/v1/endpoints/isolate/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" \
  -d '{"request_data":{"endpoint_id":"<lab-endpoint-id>"}}' | jq -r '.reply.action_id'
```

**Expected result:** an `action_id` and the endpoint moving to `isolated` —
network containment while forensics proceed.

**Negative test:** powering off the host instead destroys volatile memory
evidence; isolation contains while preserving forensic state.

**Cleanup:** `unisolate` the endpoint after the exercise.

### Lab 11.4 — Configure a data source and parser (Engineer)

**Objective:** Confirm a data source is parsed to the data model.

```bash
curl -sk -X POST "$XS/public_api/v1/data_sources/get_data_sources/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" -d '{"request_data":{}}' \
  | jq -r '.reply[] | select(.status!="active") | "\(.name)\t\(.status)"'
```

**Expected result:** any source not `active` (the engineer's onboarding
backlog) — an engineer's job is complete, parsed ingestion.

**Negative test:** an ingested-but-unparsed source is invisible to detection
rules that reference model fields; ingestion without parsing is not coverage.

**Cleanup:** none (read-only).

### Lab 11.5 — Build a correlation/BIOC detection rule (Engineer)

**Objective:** Read (and template) a custom correlation rule.

```bash
curl -sk -X POST "$XS/public_api/v1/correlations/get_correlations/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" -d '{"request_data":{}}' \
  | jq -r '.reply[] | select(.is_custom==true) | "\(.name)\t\(.xql_query|.[0:40])"' | head
```

**Expected result:** custom correlation rules with their XQL logic — the
engineer authors detections as XQL that promote events to alerts.

**Negative test:** a rule with too-broad XQL floods analysts with false
positives; detection engineering is tuning precision, not just writing logic.

**Cleanup:** none (read-only).

### Lab 11.6 — Tune alert exclusions (Engineer)

**Objective:** Read alert-exclusion/suppression policy that cuts noise.

```bash
curl -sk -X POST "$XS/public_api/v1/alerts/get_alerts/" \
  -H "Authorization: $XSIAM_KEY" -H "x-xdr-auth-id: $XSIAM_ID" \
  -d '{"request_data":{"filters":[{"field":"alert_source","operator":"eq","value":"Correlation"}],"sort":{"field":"severity","keyword":"desc"}}}' \
  | jq -r '.reply.alerts | length'
```

**Expected result:** the correlation-alert volume the engineer tunes down
with exclusions/suppression — the ongoing noise-reduction work.

**Negative test:** an exclusion that is too broad suppresses a real attack;
tuning trades noise against coverage, and must be reviewed.

**Cleanup:** none (read-only).

### Lab 11.7 — Analyst investigation and engineer detection (integrative)

In a Cortex evaluation tenant or the free digital-learning labs (else
a documented runbook against product docs): as Analyst, investigate a
seeded incident end to end — causality chain, scope, one response
action — and write the case narrative; as Engineer, onboard one data
source, validate its normalization with an XQL query, and author one
BIOC/correlation rule with a stated precision target and a test that
exercises it.

## Lab Verification

Verification means the analyst case narrative explains the whole
causality chain and justifies its response, the engineer's data
source normalizes correctly (proven by query), and the authored
detection fires on its test case without firing on a negative control.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Causality-based investigation performed and narrated (Analyst)
- [ ] Data source onboarded and normalization validated (Engineer)
- [ ] One detection authored with a precision target and test
- [ ] XDR vs. XSIAM cert scopes distinguished and a choice defended
