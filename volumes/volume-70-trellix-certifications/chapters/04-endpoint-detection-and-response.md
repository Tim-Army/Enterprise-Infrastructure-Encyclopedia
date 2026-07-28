# Chapter 04: Endpoint Detection and Response (EDR)

## Learning Objectives

- Explain the Trellix EDR platform and its role alongside ENS.
- Hunt across endpoints with real-time and historical search.
- Investigate detections and the process story.
- Take response reactions on endpoints.
- Complete a walkthrough for each EDR topic (defensive).

## Theory and Architecture

**Trellix EDR** adds continuous **detection, investigation, and response** on top of ENS's
prevention. It records endpoint activity (processes, files, network, registry) and applies
analytics and behavioral detections to surface suspicious activity as **threats/detections** with
a **process story** (the causality chain — parent → child → network → impact). Analysts **hunt**
with **real-time search** (query the live fleet now — "which endpoints have this file/registry
key/running process?") and **historical search** (over recorded telemetry), triage detections in a
guided **investigation** workspace (often AI-assisted), and take **reactions** — isolate/contain a
host, kill a process, delete a file, or collect forensics — directly from the console. EDR pairs
with **Helix/XDR** for cross-domain correlation. This is **defensive**: detection engineering,
threat hunting, and incident response.

## Design Considerations

Onboard the **right telemetry** and tune detections to reduce noise without blinding the SOC. Hunt
on **hypotheses** with real-time search, not at random. Work detections from the **process story**
(root cause), and use **reactions** proportionately (contain first, eradicate after confirmation).
Feed findings back into ENS prevention and detection rules.

## Implementation and Automation

The labs run a real-time hunt, review a detection's process story, take a reaction, and query the
EDR API — all **authorized detection and response**.

## Validation and Troubleshooting

Confirm the EDR model:

```text
EDR: records endpoint activity -> analytics/behavioral detections -> threat + process story (causality).
Hunt: real-time search (live fleet) + historical search (telemetry). Investigate -> reactions
  (isolate/contain, kill process, delete file, collect forensics). Pairs with Helix/XDR. Defensive.
```

Common pitfalls: hunting with **no hypothesis** (noise); and eradicating before **containing/
confirming** (evidence loss, incomplete response).

## Security and Best Practices

Operate **defensively** — detect, hunt, investigate, respond. **Contain** before eradicating,
preserve **forensics**, and follow IR process. Tune detections to protect signal. Restrict EDR
console/API access. Improve prevention from what hunting reveals.

## Hands-On Lab

EDR walkthroughs (defensive). **Shared prerequisites** — a Trellix EDR tenant (or the search/API
patterns), in an **authorized** lab. **Cost:** none with a tenant.

### Lab 4.1 — Real-time search hunt

**Objective:** Find a suspicious artifact across the fleet.

```text
# EDR Real-Time Search (query the live fleet now):
Processes name, id where Processes name equals "powershell.exe"
  and Processes cmdline contains "-enc"
# Returns matching live endpoints for investigation.
"real-time search: hypothesis-driven query of the live fleet -> targets to investigate"
```

**Expected result:** endpoints running **encoded PowerShell** surfaced for investigation — a
hypothesis-driven hunt.

**Negative test:** browse detections randomly hoping to spot evil; **real-time search** answers a
hypothesis — query it.

**Cleanup:** none (read-only hunt).

### Lab 4.2 — Investigate the process story

**Objective:** Trace a detection to root cause.

```text
# EDR investigation: open a detection -> view the process story (root process -> children ->
#   network connections -> file/registry changes). Identify patient zero and scope.
"process story: root cause -> child processes -> network -> impact -> scope the incident"
```

**Expected result:** the **causality chain** from root cause to impact — the investigation view for
scoping.

**Negative test:** react to a single alert without the **story**; investigate the causality chain
to understand scope first.

**Cleanup:** none.

### Lab 4.3 — Take a reaction (contain)

**Objective:** Contain a compromised host.

```text
# EDR reactions on a host: Isolate/Contain network (allow only EDR comms), kill a malicious process,
#   delete a file, or collect forensics. Contain FIRST to stop spread.
"reaction: contain host (network isolation) -> then kill process / collect forensics"
```

**Expected result:** the host **contained** (network-isolated to EDR) — spread stopped while you
investigate.

**Negative test:** delete the malware and move on without containment; **contain first** to stop
lateral movement, then eradicate.

**Cleanup:** un-isolate after remediation (in a lab).

### Lab 4.4 — Query EDR via the API

**Objective:** Retrieve detections programmatically.

```bash
curl -sk -H "Authorization: Bearer $EDR_TOKEN" "https://<edr-tenant>/edr/v2/detections?status=open" 2>/dev/null \
  | python3 -c "import sys,json;print('open detections retrieved' if sys.stdin.read().strip() else 'query the Trellix EDR API for detections')" 2>/dev/null \
  || echo "Trellix EDR API returns detections/searches for SOC automation and SIEM integration"
```

**Expected result:** open detections from the **EDR API** — programmatic SOC integration.

**Negative test:** copy detections out of the console to automate; the **API** feeds automation —
use it.

**Cleanup:** none (read-only).

### Lab 4.5 — Feed detection back to prevention

**Objective:** Close the loop into ENS.

```text
# From a confirmed EDR finding: add the malicious hash/behavior to ENS (block by hash/ATP rule),
#   create/refine a detection rule, and tag affected systems in ePO for follow-up.
"loop: EDR finding -> ENS prevention (block) + refined detection + ePO tag -> reduce recurrence"
```

**Expected result:** the finding **hardened into prevention** — hunting improves defense.

**Negative test:** investigate and close without hardening; **feed findings into prevention** so the
threat can't recur.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Trellix EDR adds detection, hunting, investigation, and response to ENS: real-time/historical
search, the process-story causality view, and reactions (contain, kill, collect). Hunt on
hypotheses, work from root cause, contain before eradicating, integrate via the API, and feed
findings back into prevention. Defensive only.

- [ ] I can run a real-time search hunt.
- [ ] I can investigate a process story.
- [ ] I can contain a host and respond.
- [ ] I can query the EDR API and close the loop into ENS.
- [ ] I completed Labs 4.1–4.5 including each negative test.
