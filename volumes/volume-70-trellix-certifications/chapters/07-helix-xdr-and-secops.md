# Chapter 07: Helix, XDR, and SecOps

## Learning Objectives

- Explain Trellix Helix and the XDR platform.
- Correlate cross-domain telemetry into incidents.
- Search and write detection rules in Helix.
- Automate response with playbooks/SOAR.
- Complete a walkthrough for each SecOps topic (defensive).

## Theory and Architecture

**Trellix Helix** (from FireEye) is the **SecOps / SIEM** platform, and the hub of the Trellix
**XDR** story. It **ingests** telemetry and alerts from across the estate — endpoint (ENS/EDR),
network (IPS/ATD), email, cloud, and third-party sources — **normalizes** it, applies **correlation
rules** and analytics to reduce alerts into prioritized **incidents**, and enriches with **threat
intelligence**. Analysts **search** the data (Helix has its own search/query language), triage
incidents in a case-management workflow, and drive **automated response** through **playbooks/SOAR**
(orchestrating actions across integrated tools). **XDR** is the outcome: instead of siloed endpoint
and network consoles, one platform correlates signals across domains so an attack that touches
endpoint *and* network *and* email is seen as **one incident**. All of this is **defensive** —
detection engineering, correlation, and orchestrated response.

## Design Considerations

Onboard the **right sources** with correct parsing so correlation works. Let Helix **reduce alerts
to incidents** rather than drowning analysts. Write **correlation rules** for multi-signal attacks.
Automate the **repetitive** response steps with playbooks, keeping a human decision point for
consequential actions. Enrich with **threat intelligence**.

## Implementation and Automation

The labs search Helix, write a correlation rule, and build a response playbook — all **defensive**.

## Validation and Troubleshooting

Confirm the Helix/XDR model:

```text
Helix (SecOps/SIEM/XDR hub): ingest (endpoint/network/email/cloud/3rd-party) -> normalize ->
  correlate + analytics -> prioritized incidents + threat intel. Search/query language; case mgmt; playbooks/SOAR.
XDR: cross-domain correlation -> one incident from endpoint+network+email signals.
```

Common pitfalls: ingesting sources with **no parsing/mapping** (correlation fails); and automating a
**consequential** action with no human checkpoint.

## Security and Best Practices

Map sources correctly, let Helix **correlate to incidents**, and automate response with **human
approval** on high-impact actions. Enrich with threat intel. Restrict and audit platform access.
Defensive SecOps throughout.

## Hands-On Lab

Helix/XDR walkthroughs (defensive). **Shared prerequisites for Labs 7.1–7.4** — a Helix tenant (or
the query/playbook patterns), in an **authorized** lab. **Cost:** none with a tenant.

### Lab 7.1 — Search Helix

**Objective:** Query correlated data.

```text
# Helix search (query language): find failed logons followed by success from the same source.
class=authentication action=failure | groupby src_ip | where count > 20
"helix search: query normalized cross-source data -> surface suspicious patterns"
```

**Expected result:** high-volume failed-auth sources surfaced by **Helix search** — the analyst
view across sources.

**Negative test:** query one raw source at a time; **Helix** normalizes and correlates across
sources — search there.

**Cleanup:** none (read-only).

### Lab 7.2 — Correlation rule

**Objective:** Detect a multi-signal attack.

```text
# Rule: EDR detection on a host AND (within 10 min) an IPS C2 alert from the same host -> raise a
#   HIGH incident (endpoint + network correlation).
"correlation: EDR host detection + IPS C2 from same host -> one high-priority XDR incident"
```

**Expected result:** a **correlation rule** raising one incident from endpoint+network signals —
the XDR advantage.

**Negative test:** treat the EDR and IPS alerts as separate; **correlation** ties them into one
incident — write the rule.

**Cleanup:** none.

### Lab 7.3 — Response playbook

**Objective:** Automate triage with a human gate.

```yaml
# Helix/SOAR playbook (excerpt): enrich, decide, gate containment on approval.
steps:
  - enrich: {indicators: [host, hash], sources: [threat-intel, EDR]}
  - condition: {if: "reputation == malicious"}
  - approval: {task: "Analyst approve containment"}   # human checkpoint
  - action: {do: "EDR isolate host + block hash (ENS)"}  # after approval
```

**Expected result:** a playbook that **enriches, decides, requests approval, then contains** —
automated response with a human gate.

**Negative test:** auto-isolate hosts on any match with no approval; keep a **human checkpoint** on
consequential actions.

**Cleanup:** disable/delete the test playbook.

### Lab 7.4 — XDR incident view

**Objective:** See one incident across domains.

```python
python3 - <<'PY'
signals=["EDR: suspicious process on host-42","IPS: C2 beacon from host-42","Email: phishing to user on host-42"]
print("XDR incident (host-42):")
for s in signals: print("  -",s)
print("=> one correlated incident, not three siloed alerts")
PY
```

**Expected result:** endpoint, network, and email signals shown as **one XDR incident** — unified
detection and response.

**Negative test:** chase three siloed alerts in three consoles; **XDR** correlates them into one —
work the incident.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Trellix Helix is the SecOps/SIEM hub of the XDR platform: it ingests and normalizes cross-domain
telemetry, correlates alerts into prioritized incidents, and drives playbook/SOAR response. Map
sources well, correlate multi-signal attacks, automate with human checkpoints, and work one XDR
incident instead of siloed alerts. Defensive only.

- [ ] I can search Helix across sources.
- [ ] I can write a cross-domain correlation rule.
- [ ] I can build a response playbook with a human gate.
- [ ] I can explain the XDR single-incident view.
- [ ] I completed Labs 7.1–7.4 including each negative test.
