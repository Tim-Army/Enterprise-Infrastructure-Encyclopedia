# Chapter 12: XSOAR Automation and the Cloud Security Engineer

## Learning Objectives

- Engineer Cortex XSOAR: playbooks, integrations, incident layouts,
  and threat-intel management (XSOAR Engineer)
- Apply SOAR discipline — automate the repeatable, gate the
  consequential — connecting Volume IX's automation-trust ladder to
  the SOC
- Complete the Cloud Security track: the Cloud Security Engineer
  certification alongside the Cloud Security Professional of Chapter 09
- Close Volume XVI's certification portfolio across all three Palo Alto
  Networks tracks

## Theory and Architecture

### XSOAR: orchestration as code

Cortex XSOAR turns incident response into **playbooks** — visual,
versioned workflows of tasks that call **integrations** (hundreds of
third-party connectors), branch on conditions, loop over indicators,
and pause for **analyst input** at the decisions that must stay human.
Around them sit **incident types and layouts** (the case UI analysts
work), **indicator/threat-intel management** (TIM: dedup, scoring,
sharing), and a scripting layer (Python/JS automations) for anything a
task cannot express. The XSOAR Engineer certification validates
building this: playbook design, integration configuration, custom
automations, and content-pack lifecycle.

### The automation-trust ladder, in the SOC

XSOAR is where Volume IX's doctrine meets security operations:
enrichment and containment of well-understood incidents automate
fully; consequential actions (mass isolation, account disablement)
run behind analyst-gated tasks; everything logs for audit. The
engineering skill the exam rewards is knowing which tasks belong on
which rung — a playbook that auto-executes a destructive action on a
false positive is worse than no playbook.

### Closing the Cloud Security track

Chapter 09 covered the **Cloud Security Professional** and the Cortex
Cloud / Prisma Cloud CNAPP model (CSPM, CWPP, CIEM, IaC/API security).
The **Cloud Security Engineer** certification is its build-side
counterpart: deploying and configuring cloud-security coverage,
onboarding cloud accounts, tuning posture and runtime policy, and
integrating findings into the SOC — the same Professional/Engineer
split this volume's Cortex chapters use, applied to the cloud track.
Together they complete Palo Alto Networks' third track inside this
volume.

## Design Considerations

- Automate enrichment and triage first (highest volume, lowest risk);
  reserve automated response for incidents with unambiguous signatures
- Playbooks are products: version them, test them against replayed
  incidents, and review changes — the Volume IX pipeline applies
  unchanged
- Cloud Security Engineer work is account-onboarding-first: coverage
  gaps are silent risk; prove every account is monitored before
  tuning any policy
- One SOC content strategy: XSIAM/XDR detections and XSOAR playbooks
  and cloud-security policies belong in one governed content
  lifecycle, not three

## Implementation and Automation

```python
# XSOAR automation (the Engineer exam's building block)
def enrich_and_gate(indicator):
    verdict = demisto.executeCommand("wildfire-get-verdict",
                                     {"hash": indicator})[0]["Contents"]
    if verdict == "malicious":
        # low-risk, auto: block at the firewall (Network Security track)
        demisto.executeCommand("panorama-block-ip", {"ip": indicator})
        # high-risk, gate: isolation waits for an analyst task
        demisto.executeCommand("setIncident",
                               {"customFields": {"awaitingapproval": "true"}})
    return verdict
```

```text
# Cloud Security Engineer: onboard, then verify coverage
# 1. Onboard cloud account (CSPM/CWPP agentless + agent)
# 2. Confirm asset inventory is complete before trusting any finding
# 3. Tune posture policy to the org's compliance baseline
# 4. Route findings into XSOAR / the SOC queue (one content lifecycle)
```

## Validation and Troubleshooting

- Playbook failures: read the task graph — a red task names its input,
  integration, or condition fault directly; test integrations'
  auth/scopes in isolation
- Never trust an automation you have not replayed against a real past
  incident; dry-run mode before production enablement
- Cloud Security: coverage gaps masquerade as clean posture — verify
  account/asset inventory completeness first, findings second
- Measure automation value: incidents auto-resolved, analyst-hours
  saved, and — critically — automated actions later reversed (the
  false-positive tax)

## Security and Best Practices

- Separate playbook-authoring from production-promotion rights; no
  live edits to running playbooks without review
- XSOAR integration credentials are keys to every connected system —
  vault them, scope them, rotate them
- Analyst-gated tasks for any irreversible action; the human rung is a
  feature, not a limitation
- Cloud onboarding uses least-privilege roles; the security platform
  does not need broad write access to the estate it watches

## References and Knowledge Checks

- Palo Alto Networks certification pages: XSOAR Engineer, Cloud
  Security Professional, Cloud Security Engineer (objectives authority)
- Cortex XSOAR and Cortex Cloud / Prisma Cloud documentation
- Volumes VII (cloud), IX (automation), X (security) of this
  encyclopedia

Knowledge checks:

1. Which SOC actions belong on the "auto-execute" rung and which on
   the "analyst-gated" rung, and what principle decides?
2. Why does a Cloud Security Engineer verify asset inventory before
   trusting posture findings?
3. Argue for one governed content lifecycle across detections,
   playbooks, and cloud policy rather than three separate ones.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for the **XSOAR Engineer**
(playbooks, integrations, automation) and **Cloud Security Engineer**
(cloud remediation, policy-as-code) capability areas the two certifications
assume — mapped in the volume README's coverage table. The Cortex datasheets
sit behind a dynamic portal, so these labs map to each certification's
documented capability areas (re-check on the next currency cycle). Each uses
the XSOAR / Cortex Cloud REST API and ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 12.1–12.5** — an XSOAR/XSIAM tenant with an
API key in `$XSOAR_KEY` and base URL `$SOAR`, plus the Cortex Cloud tenant
from Chapter 09 (`$CORTEX_TOKEN`, `$CC`) for the Cloud Security Engineer
labs. **Cost:** none; automation targets lab resources only.

### Lab 12.1 — Trigger and read a playbook run (XSOAR)

**Objective:** Kick off an incident and read its playbook execution.

```bash
IID=$(curl -sk -X POST "$SOAR/incident" -H "Authorization: $XSOAR_KEY" \
  -H 'Content-Type: application/json' -d '{"name":"lab-enrich","type":"Unclassified"}' | jq -r '.id')
curl -sk "$SOAR/inv-playbook/$IID" -H "Authorization: $XSOAR_KEY" | jq -r '.state, .tasks | length'
```

**Expected result:** the incident's playbook in a running/completed state
with its task count — automation orchestrating the response.

**Negative test:** an incident with no playbook assigned sits untouched;
the playbook binding is what triggers automation.

**Cleanup:** delete the lab incident.

### Lab 12.2 — Configure an integration instance (XSOAR)

**Objective:** Confirm an enabled integration the playbooks call.

```bash
curl -sk "$SOAR/settings/integration/search" -H "Authorization: $XSOAR_KEY" \
  -H 'Content-Type: application/json' -d '{"size":50}' \
  | jq -r '.instances[] | select(.enabled=="true") | "\(.brand)\t\(.name)"' | head
```

**Expected result:** enabled integration instances (firewall, XDR, threat
intel) — the connectors a playbook uses to enrich and act.

**Negative test:** a playbook that calls a disabled integration errors at the
task; the instance must be enabled and healthy first.

**Cleanup:** none (read-only).

### Lab 12.3 — Read a playbook task result / war room (XSOAR)

**Objective:** Read an automation task's output from the incident war room.

```bash
curl -sk "$SOAR/investigation/$IID" -H "Authorization: $XSOAR_KEY" \
  -H 'Content-Type: application/json' -d '{"pageSize":20}' \
  | jq -r '.entries[] | select(.type==1) | .contents' 2>/dev/null | head
```

**Expected result:** task entries (enrichment output, indicator verdicts) in
the war room — the auditable record of what the automation did.

**Negative test:** an auto-containment action taken with no war-room entry is
untraceable; every automated action should log to the war room for audit.

**Cleanup:** none (read-only).

### Lab 12.4 — Automate cloud remediation (Cloud Security Engineer)

**Objective:** Read the remediation available for a cloud finding.

```bash
curl -sk -H "Authorization: $CORTEX_TOKEN" \
  "$CC/cspm/v1/findings?severity=high&remediable=true" \
  | jq -r '.findings[0] | "\(.policy)\t\(.remediation.type)"'
```

**Expected result:** a high-severity finding with an available remediation
(auto or guided) — the engineer wires findings to automated fixes.

**Negative test:** auto-remediating without a guardrail can break a
legitimate resource; remediation automation needs scoping and approval for
destructive fixes.

**Cleanup:** none (read-only).

### Lab 12.5 — Enforce a policy-as-code guardrail (Cloud Security Engineer)

**Objective:** Read the code-security policy that blocks bad IaC pre-merge.

```bash
curl -sk -H "Authorization: $CORTEX_TOKEN" "$CC/code-security/v1/policies?enabled=true" \
  | jq -r '.policies[] | "\(.name)\t\(.severity)\t\(.enforcement)"' | head
```

**Expected result:** enabled code-security policies with an enforcement mode
(`block`/`monitor`) — guardrails that stop misconfiguration in the pipeline.

**Negative test:** a policy in `monitor` mode logs but does not block; a
guardrail must be in `block` mode to actually prevent the merge.

**Cleanup:** none (read-only).

### Lab 12.6 — Enrich, contain, and remediate playbook (integrative)

XSOAR (evaluation/free digital-learning labs, else runbook): build one
playbook that enriches an indicator, auto-contains on an unambiguous
malicious verdict, and gates isolation behind an analyst task; test it
against a replayed incident and a false-positive control. Cloud
Security Engineer: onboard one cloud account in an eval Prisma/Cortex
Cloud tenant (or runbook), verify inventory completeness, tune one
posture policy, and route a finding into the SOC queue.

## Lab Verification

Verification means the playbook auto-contained the true positive,
held on the false-positive control at the analyst gate, and logged
both; and the cloud onboarding proved complete asset inventory before
any policy tuning, with one finding delivered to the SOC.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] XSOAR playbook built with auto and analyst-gated rungs
- [ ] Automation replayed against a real incident and a control
- [ ] Cloud Security Engineer onboarding and coverage verification done
- [ ] All three Palo Alto Networks tracks' certs mapped across Volume XVI
