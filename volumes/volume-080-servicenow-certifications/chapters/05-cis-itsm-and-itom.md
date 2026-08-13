# Chapter 05: CIS — ITSM and ITOM

## Learning Objectives

- Implement Incident, Problem, and Change Management (ITSM).
- Maintain a healthy CMDB.
- Discover infrastructure with Discovery and the MID Server.
- Correlate alerts with Event Management (ITOM).
- Complete a walkthrough for each ITSM/ITOM domain.

## Theory and Architecture

The **CIS-ITSM** and IT Operations Management (ITOM) credentials cover ServiceNow's original home.
**ITSM** implements the service-management processes on the `task`-derived tables: **Incident
Management** (restore service — the `incident` table, with priority from impact × urgency),
**Problem Management** (find root cause), and **Change Management** (control changes — normal/standard/
emergency, with risk and approvals). These depend on a healthy **CMDB** — accurate Configuration
Items and relationships enable **impact analysis** (which services a change affects). **ITOM** keeps
the CMDB current and reduces noise: **Discovery** uses a **MID Server** (an on-prem agent) to probe
infrastructure and populate CIs automatically, while **Event Management** ingests monitoring alerts,
**deduplicates and correlates** them into actionable **alerts** and **incidents**, reducing alert
fatigue. Together, ITSM delivers the processes and ITOM feeds them accurate data — the operational
core of the platform. This chapter teaches each with a hands-on walkthrough (process logic, CMDB
health, and event correlation).

## Design Considerations

Compute incident **priority** from impact × urgency consistently. Enforce **change** risk/approval by
type. Keep the **CMDB** accurate (Discovery-populated, reconciled). Use **Discovery** (MID Server) for
automated CI population. Configure **Event Management** to deduplicate/correlate so alerts are
actionable. Link changes to CIs for **impact analysis**.

## Implementation and Automation

The labs compute priority, plan a change, discover CIs, and correlate events.

## Validation and Troubleshooting

Confirm the ITSM/ITOM model:

```text
ITSM: Incident (restore, priority=impact x urgency), Problem (root cause), Change (normal/standard/emergency + risk/approval) on task-derived tables. Depends on healthy CMDB (impact analysis).
ITOM: Discovery (MID Server probes -> populate CIs), Event Management (ingest alerts -> dedup/correlate -> actionable alerts/incidents).
```

Common pitfalls: a **stale CMDB** (broken impact analysis); and raw monitoring **alert floods** with
no correlation (fatigue).

## Security and Best Practices

Compute **priority** consistently, gate **changes** by risk, keep the **CMDB** accurate via
**Discovery**, and **correlate** events into actionable alerts. Link changes to CIs. All work is
authorized administration.

## Hands-On Lab

ITSM/ITOM walkthroughs. **Shared prerequisites** — `python3`, a free PDI. **Cost:** none.

### Lab 5.1 — Compute incident priority

**Objective:** Prioritize consistently.

```python
python3 - <<'PY'
matrix={(1,1):1,(1,2):2,(2,1):2,(2,2):3,(3,3):5}  # (impact,urgency)->priority (1=Critical)
for impact,urgency in [(1,1),(2,2),(3,3)]:
    print(f"impact {impact} x urgency {urgency} -> priority {matrix.get((impact,urgency),4)}")
print("ITSM: priority is derived from impact x urgency (consistent, not ad hoc)")
PY
```

**Expected result:** priority derived from the **impact × urgency** matrix — consistent incident
prioritization.

**Negative test:** let agents set priority by gut feel; it's inconsistent — derive from **impact ×
urgency**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Plan a change with risk and approval

**Objective:** Control change safely.

```python
python3 - <<'PY'
changes={"normal (patch DB)":{"risk":"high","approval":"CAB + manager"},
         "standard (add user)":{"risk":"low","approval":"pre-approved template"},
         "emergency (outage fix)":{"risk":"high","approval":"emergency CAB (expedited)"}}
for c,d in changes.items(): print(f"{c:22}: risk={d['risk']}, approval={d['approval']}")
print("Change Mgmt: type -> risk -> approval path (standard = pre-approved)")
PY
```

**Expected result:** each change type mapped to **risk and approval** — controlled change management.

**Negative test:** route a high-risk DB patch as a **standard** (pre-approved) change; it skips review
— classify by **risk**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Populate the CMDB with Discovery

**Objective:** Automate CI accuracy.

```python
python3 - <<'PY'
discovery={"mid_server":"on-prem agent (probes + sensors)","targets":"10.0.0.0/24",
           "populates":["cmdb_ci_server","cmdb_ci_appl","relationships (runs on/depends on)"],
           "schedule":"nightly"}
for k,v in discovery.items(): print(f"{k:11}: {v}")
print("ITOM Discovery: MID Server probes infrastructure -> auto-populates CIs + relationships")
PY
```

**Expected result:** **Discovery** via the MID Server auto-populating CIs — an accurate, current CMDB.

**Negative test:** maintain the CMDB by hand; it drifts immediately — automate with **Discovery**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Correlate events into an alert

**Objective:** Reduce alert noise.

```python
python3 - <<'PY'
events=[{"ci":"SRV-DB01","type":"high CPU","time":"10:00"},{"ci":"SRV-DB01","type":"high CPU","time":"10:01"},
        {"ci":"SRV-DB01","type":"disk full","time":"10:02"}]
from collections import defaultdict
alerts=defaultdict(list)
for e in events: alerts[e["ci"]].append(e["type"])
for ci,types in alerts.items():
    print(f"{ci}: {len(set(types))} distinct alert(s) from {len(types)} events -> {set(types)}")
print("Event Management: dedup + correlate raw events into actionable alerts (less fatigue)")
PY
```

**Expected result:** raw events **deduplicated/correlated** into fewer actionable alerts — Event
Management.

**Negative test:** open an incident for every raw monitoring event; agents drown — **correlate**
first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CIS-ITSM/ITOM implements Incident/Problem/Change management on a healthy CMDB, with Discovery (MID
Server) populating CIs and Event Management correlating alerts — the operational core of the platform.

- [ ] I can compute incident priority.
- [ ] I can plan a change with risk and approval.
- [ ] I can populate the CMDB with Discovery.
- [ ] I can correlate events into an alert.
- [ ] I completed Labs 5.1–5.4 including each negative test.
