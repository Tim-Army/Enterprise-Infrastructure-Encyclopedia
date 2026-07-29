# Chapter 03: CCFR — Certified Falcon Responder

## Learning Objectives

- Explain what the CCFR certifies and its target role.
- Summarize the six exam-guide domains.
- Analyze detections, search events, and investigate on Falcon.
- Use the search tools and Real Time Response (RTR).
- Complete a per-domain walkthrough for each CCFR domain.

## Theory and Architecture

The **CrowdStrike Certified Falcon Responder (CCFR)** validates responding to
detections — the front-line analyst credential. Its exam guide (90 minutes, 60
questions) covers **six domains**: **ATT&CK Frameworks**, **Detection Analysis**,
**Event Search**, **Event Investigation**, **Search Tools**, and **Real Time
Response (RTR)**. No domain weights are published.

## Design Considerations

The responder maps detections to **MITRE ATT&CK** tactics/techniques, triages the
**detection** (process tree, severity), pivots via **event search** across telemetry
(process, network, file events), reconstructs the incident with **investigation**
tools (host/process timelines), and remediates live with **RTR** — all under
least-privilege, audited access.

## Implementation and Automation

The labs use FalconPy for each domain — ATT&CK mapping, detection analysis, event
search, investigation, search tools, and RTR.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
crowdstrike.com > CCFR exam guide:
  1 ATT&CK Frameworks  2 Detection Analysis  3 Event Search
  4 Event Investigation  5 Search Tools  6 Real Time Response (RTR)
```

Common pitfalls: closing a detection without checking the **full process tree**;
and running RTR without scoping or auditing.

## Security and Best Practices

Triage with the **ATT&CK** lens, always review the **complete process tree**, pivot
on **indicators** across event search, use **host/process timelines** for scope, and
run **RTR** with least privilege and full audit. Document findings for handoff.

## References and Knowledge Checks

- crowdstrike.com: CCFR exam guide; Falcon detections, event search, and RTR docs.

**Knowledge checks**

1. Why map a detection to MITRE ATT&CK?
2. What does the process tree tell you during detection analysis?
3. How is RTR access controlled and audited?

## Hands-On Lab

Per-domain walkthroughs — CCFR. **Shared prerequisites** — a Falcon tenant, an API
client (Detections/RTR scopes), `crowdstrike-falconpy`, and exported credentials.
**Cost:** none beyond the tenant.

### Lab 3.1 — ATT&CK Frameworks

**Objective:** Read the ATT&CK tactic/technique on a detection.

```python
from falconpy import Alerts
a = Alerts(client_id=CID, client_secret=SEC)
ids = a.query_alerts_v2(filter="product:'epp'", limit=1)["body"]["resources"]
det = a.get_alerts_v2(composite_ids=ids)["body"]["resources"][0]
print("tactic:", det.get("tactic"), "technique:", det.get("technique"), det.get("technique_id"))
```

**Expected result:** the **tactic/technique (+ ATT&CK ID)** for a detection — the
ATT&CK Frameworks domain.

**Negative test:** triage on severity alone; the **ATT&CK mapping** tells you what
the adversary was doing — use it.

**Cleanup:** none (read-only).

### Lab 3.2 — Detection Analysis (process tree)

**Objective:** Inspect a detection's process detail.

```python
det = a.get_alerts_v2(composite_ids=ids)["body"]["resources"][0]
print("file:", det.get("filename"), "cmdline:", det.get("cmdline"))
print("parent:", det.get("parent_details",{}).get("filename"))
```

**Expected result:** the offending **process, command line, and parent** — the
Detection Analysis domain (the process tree).

**Negative test:** act on the leaf process only; check the **parent chain** — the
root cause is often upstream.

**Cleanup:** none (read-only).

### Lab 3.3 — Event Search

**Objective:** Search process-execution telemetry for a host.

```python
from falconpy import EventStreams  # or the Event Search / CQL API on Next-Gen SIEM
# Falcon event search (legacy: Falcon Data Replicator / Event Search):
# search: aid=<AID> event_simpleName=ProcessRollup2 | table timestamp, FileName, CommandLine
print("query: event_simpleName=ProcessRollup2 by aid -> process executions")
```

**Expected result:** a process-execution query returning executions for the host —
the Event Search domain (pivoting across telemetry).

**Negative test:** rely only on the detection; **event search** surfaces related
activity the detection didn't flag.

**Cleanup:** none (read-only).

### Lab 3.4 — Event Investigation (host timeline)

**Objective:** Pull a device's recent activity for timelining.

```python
from falconpy import Hosts
h = Hosts(client_id=CID, client_secret=SEC)
aid = ids[0].split(":")[-1] if ids else "<AID>"
dev = h.get_device_details(ids=[aid])["body"]["resources"]
print("host:", dev[0]["hostname"], "last seen:", dev[0]["last_seen"]) if dev else print("supply AID")
```

**Expected result:** host identity and **last-seen** context for building a
**timeline** — the Event Investigation domain.

**Negative test:** investigate a hostname in isolation; anchor on the **AID** —
hostnames are reused, AIDs are unique.

**Cleanup:** none (read-only).

### Lab 3.5 — Search Tools

**Objective:** Use IOC search to find an indicator's prevalence.

```python
from falconpy import IOC
ioc = IOC(client_id=CID, client_secret=SEC)
res = ioc.indicator_search(filter="type:'sha256'", limit=5)
print("indicators returned:", len(res["body"]["resources"]))
```

**Expected result:** matching **indicators** from the IOC search tool — the Search
Tools domain (hash/domain/IP lookups).

**Negative test:** grep raw logs for a hash; the **IOC/search tools** index
indicators across the estate — use them.

**Cleanup:** none (read-only).

### Lab 3.6 — Real Time Response (RTR)

**Objective:** Open an RTR session and run a read-only command.

```python
from falconpy import RealTimeResponse as RTR
rtr = RTR(client_id=CID, client_secret=SEC)
sess = rtr.init_session(body={"device_id": aid})
sid = sess["body"]["resources"][0]["session_id"]
out = rtr.execute_command(body={"base_command":"ps","command_string":"ps","session_id":sid})
print("ps issued, cloud_request_id:", out["body"]["resources"][0]["cloud_request_id"])
```

**Expected result:** an RTR session and a queued **`ps`** (list processes) command —
the Real Time Response domain (live investigation/remediation).

**Negative test:** run destructive RTR commands unscoped; start **read-only**
(`ps`, `ls`, `netstat`) and audit every action.

**Cleanup:** `rtr.delete_session(session_id=sid)`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCFR certifies responding to detections across six domains: ATT&CK mapping,
detection analysis (process tree), event search, event investigation (timelines),
search tools (IOC), and Real Time Response — using the console and FalconPy.

- [ ] I can map a detection to ATT&CK.
- [ ] I can analyze a detection's process tree.
- [ ] I can search events and build a host timeline.
- [ ] I can use IOC search and run RTR safely.
- [ ] I completed Labs 3.1–3.6 including each negative test.
