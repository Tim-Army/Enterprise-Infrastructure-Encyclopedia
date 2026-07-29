# Chapter 07: SOC, Incident Handling, and Threat Intelligence

## Learning Objectives

- Operate in a SOC as an analyst (CSA).
- Handle incidents through the response lifecycle (ECIH).
- Produce and apply threat intelligence (CTIA).
- Correlate telemetry into detections and cases.
- Complete a walkthrough for each SOC/IR/intel domain.

## Theory and Architecture

This chapter covers EC-Council's security-operations trio. The **Certified SOC Analyst (CSA)**
validates working the SOC — monitoring, triaging alerts, using a **SIEM**, and escalating — the
tier-1/2 analyst role. The **EC-Council Certified Incident Handler (ECIH)** validates the
**incident-response lifecycle** — preparation, detection/analysis, containment, eradication,
recovery, and post-incident activity — across malware, network, web, insider, and cloud incidents.
The **Certified Threat Intelligence Analyst (CTIA)** validates the **threat-intelligence lifecycle**
— planning, collection, processing, analysis, and dissemination — turning raw data into structured,
actionable intelligence (indicators, TTPs, ATT&CK mapping) that feeds detection and response.
Together they form the SOC's operating loop: **detect (CSA) → respond (ECIH) → learn and inform
(CTIA) → improve detection**. This chapter teaches each with a hands-on defensive walkthrough (alert
triage, IR lifecycle, and intelligence structuring).

## Design Considerations

Triage on **severity and context**, not volume (CSA). Follow the **IR lifecycle** end to end and
contain before eradicating (ECIH). Run the **intelligence cycle** so intel is requirements-driven and
**actionable** (CTIA). Close the loop: incidents and intel should **improve detections**. Measure
with **MTTD/MTTR**.

## Implementation and Automation

The labs triage an alert, walk the IR lifecycle, and structure intelligence.

## Validation and Troubleshooting

Confirm the SOC/IR/intel map:

```text
CSA = SOC analyst (monitor/triage/SIEM/escalate). ECIH = IR lifecycle (prep/detect/contain/eradicate/recover/post).
CTIA = intel cycle (plan/collect/process/analyze/disseminate) -> IOC/TTP/ATT&CK. Loop: detect -> respond -> inform -> improve.
```

Common pitfalls: triaging by **alert volume** instead of severity/context; and intel that is a raw
IOC dump with **no action**.

## Security and Best Practices

Triage by risk, follow the **IR lifecycle**, run a requirements-driven **intel cycle**, and feed
findings back into **detections**. Measure MTTD/MTTR. All work is defensive.

## Hands-On Lab

SOC/IR/intel walkthroughs. **Shared prerequisites** — Linux with `python3`, `jq`, in a lab.
**Cost:** none.

### Lab 7.1 — CSA: triage alerts by severity and context

**Objective:** Prioritize the queue.

```python
python3 - <<'PY'
alerts=[{"rule":"port scan","sev":"low","asset":"lab host"},
        {"rule":"ransomware behavior","sev":"critical","asset":"file server"},
        {"rule":"impossible travel login","sev":"high","asset":"exec account"}]
order={"critical":0,"high":1,"medium":2,"low":3}
for a in sorted(alerts,key=lambda x:order[x["sev"]]):
    print(f"[{a['sev']:8}] {a['rule']:22} on {a['asset']}")
print("CSA: work critical/high first, weighted by asset value")
PY
```

**Expected result:** the alert queue ordered by **severity and asset** — CSA triage.

**Negative test:** work alerts oldest-first regardless of severity; the ransomware alert waits —
prioritize by **risk**.

**Cleanup:** none.

### Lab 7.2 — ECIH: walk the incident-response lifecycle

**Objective:** Structure a response.

```python
python3 - <<'PY'
phases=["Preparation","Detection & Analysis","Containment","Eradication","Recovery","Post-Incident"]
for i,p in enumerate(phases,1): print(f"{i}. {p}")
print("ECIH: contain before eradicate; capture lessons in post-incident")
PY
```

**Expected result:** the **IR lifecycle** phases in order — the ECIH structure.

**Negative test:** eradicate before **containment**; the threat spreads while you clean one host —
contain first.

**Cleanup:** none.

### Lab 7.3 — CTIA: structure threat intelligence

**Objective:** Make intel actionable.

```python
python3 - <<'PY'
intel={"indicator":"evilhost.example","type":"C2 domain","ttp":"T1071 App-Layer C2",
       "source_confidence":"high","action":"block at DNS/proxy + hunt historical logs"}
for k,v in intel.items(): print(f"{k:18}: {v}")
print("CTIA: indicator + TTP/ATT&CK + confidence + action = intelligence")
PY
```

**Expected result:** an indicator with **TTP mapping, confidence, and action** — CTIA-structured
intelligence.

**Negative test:** disseminate a bare IOC list; without **TTP and action** it's just data — structure
it.

**Cleanup:** none.

### Lab 7.4 — Close the loop into a detection

**Objective:** Turn an incident into prevention.

```python
python3 - <<'PY'
lesson={"incident":"phishing -> C2 to evilhost.example",
        "new_detection":"alert on DNS to evilhost.example + newly-registered-domain heuristic",
        "control":"add domain to blocklist; user-report button"}
for k,v in lesson.items(): print(f"{k:14}: {v}")
print("Loop: ECIH incident + CTIA intel -> new CSA detection (continuous improvement)")
PY
```

**Expected result:** an incident/intel pair converted into a **new detection and control** — the SOC
improvement loop.

**Negative test:** close the incident without a **new detection**; the same attack recurs — always
feed back a control.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SOC trio — CSA (monitor/triage), ECIH (IR lifecycle), and CTIA (intelligence cycle) — forms the
operating loop that detects, responds, informs, and improves, all measured and defensive.

- [ ] I can triage alerts by severity and context (CSA).
- [ ] I can walk the IR lifecycle (ECIH).
- [ ] I can structure threat intelligence (CTIA).
- [ ] I can close the loop into a new detection.
- [ ] I completed Labs 7.1–7.4 including each negative test.
