# Chapter 06: Certified Cybersecurity Defense Analyst

## Learning Objectives

- Explain what the Cybersecurity Defense Analyst certifies.
- Summarize the blueprint areas: the cybersecurity landscape, threats/attacks, and SOC operations.
- Apply SPL and Splunk Enterprise Security to detection and investigation.
- Map detections to MITRE ATT&CK and use risk-based alerting.
- Complete a per-topic walkthrough for each Analyst area.

## Theory and Architecture

The **Certified Cybersecurity Defense Analyst** validates using Splunk — including
**Splunk Enterprise Security (ES)** — to **detect, analyze, and respond** to
threats as a SOC analyst. Its blueprint covers **the cybersecurity landscape**,
**understanding threats and attacks**, and **security operations and the defense
analyst** — the analyst's daily work of triaging notables, investigating with SPL,
and correlating against threat intelligence. It builds on the Core SPL skills and
the **CIM**-normalized data model.

## Design Considerations

The analyst's leverage is **SPL detection over normalized data**. Learn to search
CIM data models for security events, triage **notable events** and **risk-based
alerting (RBA)** in ES, map activity to **MITRE ATT&CK**, and enrich with **threat
intelligence**. This chapter pairs with the OffSec defensive track (OSDA/OSIR/OSTH,
Volume XLIII) and the ISACA CCOA analyst credential (Volume XLIV).

## Implementation and Automation

The labs below use **SPL** against normalized (CIM) data and describe ES workflows
— landscape/context, threat detection, notable triage, ATT&CK mapping, RBA, and
investigation.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
splunk.com > Certified Cybersecurity Defense Analyst > test blueprint:
  - the cybersecurity landscape; understanding threats and attacks;
    security operations and the defense analyst
  - uses Splunk Enterprise Security + CIM
```

Common pitfalls: writing detections against raw sourcetypes instead of the
**CIM**; alerting on indicators only (map **TTPs**); and chasing every notable
without **risk-based** prioritization.

## Security and Best Practices

Detect over **CIM** data models so one search works across sources; prioritize
with **risk-based alerting**; map detections to **MITRE ATT&CK**; enrich with
**threat intel**; and document investigations. Feed confirmed detections back into
correlation searches.

## References and Knowledge Checks

- splunk.com: *Cybersecurity Defense Analyst* blueprint; Splunk Enterprise Security docs; the CIM; MITRE ATT&CK.

**Knowledge checks**

1. Why detect over CIM data models rather than raw sourcetypes?
2. What is risk-based alerting, and why does it help triage?
3. How does ATT&CK mapping improve detections?

## Hands-On Lab

Per-topic walkthroughs — **one lab per Analyst area**. SPL runs on a Splunk
instance (ES optional).

**Shared prerequisites** — a Splunk instance; CIM-normalized data (or `_internal`
for SPL practice). **Cost:** none (trial).

### Lab 6.1 — The cybersecurity landscape (context)

**Objective:** Frame the analyst's data sources and the kill chain.

```text
| tstats count where index=* by index | sort -count | head 10
```

**Expected result:** the busiest data sources — the analyst maps these to the kill
chain (endpoint, network, auth, cloud) to know what visibility exists.

**Negative test:** assume full visibility; identify **coverage gaps** (missing
data sources) — you cannot detect what you do not collect.

**Cleanup:** none.

### Lab 6.2 — Understanding threats and attacks (detection over CIM)

**Objective:** Detect brute-force authentication over the CIM.

```text
| tstats count from datamodel=Authentication where Authentication.action=failure
  by Authentication.src, Authentication.user
  | where count > 10
```

**Expected result:** sources/users with many failed authentications — a
CIM-normalized brute-force detection (works across auth sources).

**Negative test:** write this against one raw sourcetype; the **CIM** normalizes
`action`/`src`/`user` across sources — detect once.

**Cleanup:** none.

### Lab 6.3 — Security operations: notable triage

**Objective:** Triage notable events (ES) by urgency.

```text
`notable` | stats count by rule_name, urgency | sort -urgency, -count
```

**Expected result:** notable events grouped by rule and urgency — the SOC triage
queue ES produces for the analyst.

**Negative test:** work notables in arrival order; triage by **urgency/risk**, not
time — prioritize impact.

**Cleanup:** none.

### Lab 6.4 — MITRE ATT&CK mapping

**Objective:** Enrich detections with ATT&CK technique context.

```text
`notable` | stats count by rule_name, annotations.mitre_attack.mitre_technique_id
  | sort -count
```

**Expected result:** notables grouped by ATT&CK technique ID — TTP context that
tells the analyst *what* the adversary is attempting.

**Negative test:** track only indicators (hashes/IPs); **ATT&CK** techniques catch
variants — map to TTPs.

**Cleanup:** none.

### Lab 6.5 — Risk-based alerting (RBA)

**Objective:** Aggregate risk to surface high-risk objects.

```text
| tstats sum(All_Risk.calculated_risk_score) as risk from datamodel=Risk
  by All_Risk.risk_object | where risk > 100 | sort -risk
```

**Expected result:** risk objects exceeding a threshold — RBA elevating entities
with accumulated risk instead of firing on every event.

**Negative test:** alert on every single risk event; **RBA** aggregates risk so
analysts focus on the highest-risk objects — reduce noise.

**Cleanup:** none.

### Lab 6.6 — Investigation and response

**Objective:** Pivot from an alert to the full event timeline.

```text
index=* (user="alice" OR src="10.1.1.5") earliest=-24h
  | sort _time | table _time, index, sourcetype, action, src, dest, user
```

**Expected result:** a chronological, cross-source timeline for the entity — the
investigation pivot the analyst performs after a notable.

**Negative test:** investigate a single sourcetype; pivot across **all** relevant
data for the entity to reconstruct the incident.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Cybersecurity Defense Analyst certifies SOC detection and investigation with
Splunk and Enterprise Security: the cybersecurity landscape, understanding threats
and attacks, and security operations — using SPL over CIM data, notable triage,
ATT&CK mapping, risk-based alerting, and cross-source investigation.

- [ ] I can summarize the Analyst blueprint areas.
- [ ] I can detect over CIM data models and triage notables.
- [ ] I can map detections to MITRE ATT&CK and use RBA.
- [ ] I can pivot from an alert to a cross-source timeline.
- [ ] I completed Labs 6.1–6.6 including each negative test.
