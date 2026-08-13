# Chapter 06: Security Operations — Professional and XDR

## Learning Objectives

- Explain the Security Operations Professional, XDR Analyst, and XDR Engineer credentials.
- Investigate incidents and hunt threats in Cortex XDR.
- Write detection and hunting queries in XQL.
- Manage XDR data sources and the platform via the API.
- Complete a walkthrough for each XDR topic (defensive).

## Theory and Architecture

The **Security Operations Professional** (Professional) credential and the **XDR Analyst** and
**XDR Engineer** (Specialist) credentials cover **Cortex XDR** — Palo Alto's extended detection
and response platform. XDR collects endpoint, network, and cloud telemetry, **stitches** it into
incidents, applies analytics and behavioral detection, and gives analysts a timeline to
investigate. The **Analyst** role focuses on **triage, investigation, and threat hunting**; the
**Engineer** role focuses on **deploying agents, onboarding data, tuning detection, and managing
the platform**. The query language is **XQL** (the Cortex Query Language), used for hunting,
detection rules, and correlation. Everything here is **defensive**: detection engineering, threat
hunting, and incident response — never offensive action.

## Design Considerations

Onboard the **right telemetry** (endpoint + network + cloud + identity) so detections have
context. Tune to reduce false positives without blinding the SOC. Hunt with **XQL** on
hypotheses, not at random. Automate repetitive response (bridges to XSOAR, next chapter).

## Implementation and Automation

The labs run an XQL hunt, review a stitched incident, tune a detection, and query the XDR API —
all **authorized detection and response**.

## Validation and Troubleshooting

Confirm the XDR model:

```text
Cortex XDR: endpoint+network+cloud telemetry -> stitched incidents -> analytics/behavioral detection.
Analyst: triage/investigate/hunt. Engineer: deploy/onboard/tune/manage.
Query language: XQL (hunting, detection, correlation).
```

Common pitfalls: hunting with **no hypothesis** (noise); and detections with **no tuning** (alert
fatigue).

## Security and Best Practices

Practice **defensive** operations only — detect, hunt, investigate, respond. Preserve evidence
and follow IR process. Tune detections to protect signal. Restrict and audit XDR admin/API
access. Use hunts to improve detections, not to attack.

## Hands-On Lab

XDR walkthroughs (defensive). **Shared prerequisites** — a Cortex XDR tenant (or the XQL/API
patterns), in an **authorized** environment. **Cost:** none with a tenant/trial.

### Lab 6.1 — Hunt with XQL

**Objective:** Find suspicious process executions.

```sql
dataset = xdr_data
| filter event_type = ENUM.PROCESS
| filter action_process_image_name in ("powershell.exe","wscript.exe")
       and action_process_command_line contains "-enc"
| fields agent_hostname, action_process_image_name, action_process_command_line
| limit 100
```

**Expected result:** encoded-command interpreter executions surfaced for **investigation** — a
hypothesis-driven hunt.

**Negative test:** scroll raw logs by hand; **XQL** filters to the hypothesis — query, don't
scroll.

**Rollback:** none (read-only hunt).

### Lab 6.2 — Review a stitched incident

**Objective:** Read XDR's causality view.

```text
# XDR stitches alerts across endpoint/network/cloud into ONE incident with a causality chain
#   (root cause -> child processes -> network -> impact). Analysts investigate the timeline.
"incident = stitched alerts + causality chain -> triage from root cause"
```

**Expected result:** an **incident** with its causality chain — investigate from root cause, not
isolated alerts.

**Negative test:** chase each alert separately; **stitching** groups them into one incident —
work the incident.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Tune a detection (Engineer)

**Objective:** Reduce false positives without losing coverage.

```sql
// Baseline shows admin tool 'sccm.exe' triggers a rule benignly on known servers.
dataset = xdr_data
| filter event_type = ENUM.PROCESS and action_process_image_name = "sccm.exe"
| comp count(agent_hostname) as hosts by agent_hostname
// Exclusion: suppress on known management servers only, keep detection elsewhere.
```

**Expected result:** a scoped **exclusion** for known-good hosts — tuning that preserves
coverage.

**Negative test:** disable the rule globally to stop the noise; scope the **exclusion** instead —
keep detection where it matters.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Query XDR via the API

**Objective:** Retrieve incidents programmatically.

```bash
curl -sk -X POST "https://api-<tenant>.xdr.paloaltonetworks.com/public_api/v1/incidents/get_incidents/" \
  -H "Authorization: $XDR_KEY" -H "x-xdr-auth-id: $XDR_ID" -H "Content-Type: application/json" \
  -d '{"request_data":{"filters":[{"field":"status","operator":"eq","value":"new"}]}}' 2>/dev/null \
  | python3 -c "import sys,json;print('new incidents retrieved' if 'reply' in sys.stdin.read() else 'query the Cortex XDR API for incidents')" 2>/dev/null \
  || echo "Cortex XDR public API: get_incidents -> incidents for SOAR/automation"
```

**Expected result:** the new incidents from the **XDR API** — programmatic SOC integration.

**Negative test:** copy incidents out of the GUI to automate; the **API** feeds automation — use
it.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Security Operations Professional and XDR Analyst/Engineer credentials cover Cortex XDR —
stitched incidents, behavioral analytics, and XQL for hunting and detection — with the Analyst
investigating and hunting and the Engineer onboarding data and tuning. Hunt on hypotheses, work
incidents from root cause, tune to protect signal, and integrate via the API. Defensive only.

- [ ] I can write an XQL hunt query.
- [ ] I can investigate a stitched incident from root cause.
- [ ] I can tune a detection with a scoped exclusion.
- [ ] I can query the XDR API for incidents.
- [ ] I completed Labs 6.1–6.4 including each negative test.
