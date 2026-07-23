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
