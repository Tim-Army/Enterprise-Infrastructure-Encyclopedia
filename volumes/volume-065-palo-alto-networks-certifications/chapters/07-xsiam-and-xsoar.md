# Chapter 07: XSIAM and XSOAR

## Learning Objectives

- Explain the XSIAM Analyst/Engineer and XSOAR Engineer credentials.
- Describe the Cortex XSIAM data model and AI-driven SOC.
- Analyze and correlate data in XSIAM with XQL.
- Automate response with XSOAR playbooks.
- Complete a walkthrough for each XSIAM and XSOAR topic (defensive).

## Theory and Architecture

**Cortex XSIAM** (Extended Security Intelligence and Automation Management) is Palo Alto's
AI-driven **SOC platform** — a next-generation SIEM that ingests all security data into a unified
**data model**, applies machine-learning analytics and stitching to reduce alerts to a small
number of incidents, and drives automated response. The **XSIAM Analyst** investigates and
hunts; the **XSIAM Engineer** onboards data, builds correlation and parsing, and manages the
platform (querying with **XQL**). **Cortex XSOAR** (Security Orchestration, Automation, and
Response) is the automation engine: **playbooks** (visual/YAML workflows) enrich, decide, and
act across hundreds of integrations, turning manual runbooks into automated response with a
**war room** for collaboration. The **XSOAR Engineer** builds playbooks, integrations, and
automations. All of this is **defensive**: detection, correlation, and automated incident
response.

## Design Considerations

Onboard data to the **XSIAM data model** with good parsing so analytics work. Let XSIAM
**reduce alerts to incidents** rather than drowning analysts. Automate the repetitive parts of
response with **XSOAR playbooks**, keeping a human decision point for consequential actions.
Version-control playbooks and integrations.

## Implementation and Automation

The labs query the XSIAM data model, review AI-reduced incidents, and build an XSOAR playbook —
**authorized detection and response automation**.

## Validation and Troubleshooting

Confirm the XSIAM/XSOAR model:

```text
XSIAM: ingest all security data -> unified data model -> ML analytics + stitching -> few incidents.
  Analyst investigates/hunts (XQL); Engineer onboards/parses/correlates.
XSOAR: playbooks (YAML/visual) + integrations -> automated enrich/decide/act; war room.
```

Common pitfalls: ingesting data with **no parsing/mapping** (analytics fail); and automating a
**consequential** action with no human checkpoint.

## Security and Best Practices

Keep operations **defensive** — detect, correlate, respond. Map data to the model correctly so
detections fire. Put a **human approval** on high-impact playbook actions. Restrict and audit
platform and API access. Automate to speed response, safely.

## Hands-On Lab

XSIAM/XSOAR walkthroughs (defensive). **Shared prerequisites** — a Cortex XSIAM/XSOAR tenant (or
the XQL/playbook patterns), in an **authorized** environment. **Cost:** none with a tenant/trial.

### Lab 7.1 — Query the XSIAM data model

**Objective:** Correlate authentication data.

```sql
dataset = xdr_data
| filter event_type = ENUM.STORY or event_type = ENUM.AUTHENTICATION
| comp count() as attempts by actor_effective_username, action_country
| filter attempts > 100
| sort desc attempts
```

**Expected result:** high-volume authentication by user and country surfaced for **analysis** —
the XSIAM analyst view.

**Negative test:** inspect one raw log source at a time; **XSIAM** unifies the model — query
across it.

**Rollback:** none (read-only).

### Lab 7.2 — Review AI-reduced incidents

**Objective:** Understand alert-to-incident reduction.

```text
# XSIAM applies ML + stitching so thousands of alerts collapse into a handful of incidents,
#   each scored and prioritized -> analysts work incidents, not raw alerts.
"XSIAM: thousands of alerts -> ML/stitching -> a few scored incidents"
```

**Expected result:** the **alert-to-incident** reduction model — analysts focus on what matters.

**Negative test:** triage every raw alert manually; **XSIAM** reduces them — work incidents.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Build an XSOAR playbook

**Objective:** Automate phishing triage (with a human checkpoint).

```yaml
# XSOAR playbook (excerpt): enrich a reported phishing email, then gate containment on approval.
tasks:
  "1": {type: regular, task: {scriptName: "Extract Indicators From Email"}}
  "2": {type: regular, task: {scriptName: "Enrich Indicators (WildFire/TIM)"}}
  "3": {type: condition, conditions: [{label: "malicious"}]}
  "4": {type: regular, task: {scriptName: "Analyst Approval"}}   # human checkpoint
  "5": {type: regular, task: {scriptName: "Block Sender + Quarantine"}}  # after approval
```

**Expected result:** a playbook that **enriches, decides, requests approval, then contains** —
automated response with a human gate.

**Negative test:** auto-quarantine on any match with no approval; keep a **human checkpoint** on
consequential actions.

**Rollback:** disable/delete the test playbook.

### Lab 7.4 — Automate via the XSOAR API

**Objective:** Create an incident programmatically.

```bash
curl -sk -X POST "https://<xsoar>/incident" -H "Authorization: $XSOAR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Automated triage test","type":"Phishing","severity":2}' 2>/dev/null \
  | python3 -c "import sys,json;print('incident created' if 'id' in sys.stdin.read() else 'use the XSOAR REST API to create/manage incidents')" 2>/dev/null \
  || echo "XSOAR REST API: POST /incident -> create incidents to drive playbooks"
```

**Expected result:** an incident created via the **XSOAR API** — programmatic SOAR integration.

**Negative test:** open incidents by hand for automated sources; the **API** integrates them —
use it.

**Rollback:** close/delete the test incident.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The XSIAM Analyst/Engineer and XSOAR Engineer credentials cover Cortex XSIAM (AI-driven SOC,
unified data model, XQL, alert-to-incident reduction) and Cortex XSOAR (playbook automation with
integrations and a war room). Parse data well, let XSIAM reduce alerts, and automate response
with human checkpoints on consequential actions. Defensive only.

- [ ] I can query the XSIAM data model with XQL.
- [ ] I can explain alert-to-incident reduction.
- [ ] I can build an XSOAR playbook with a human checkpoint.
- [ ] I can drive XSOAR via its API.
- [ ] I completed Labs 7.1–7.4 including each negative test.
