# Chapter 03: Cyber Defense — Blue Team

## Learning Objectives

- Analyze intrusions and network traffic (GCIA).
- Build continuous monitoring and detection (GMON, GCDA).
- Design a defensible security architecture (GDSA).
- Defend against advanced threats (GDAT).
- Complete a walkthrough for each Cyber Defense domain.

## Theory and Architecture

The **Cyber Defense** focus area — GIAC's largest — validates the blue team. **GCIA (Certified
Intrusion Analyst)** covers traffic analysis and IDS: reading packets, writing and tuning signatures,
and recognizing attack patterns. **GMON (Continuous Monitoring)** and **GCDA (Certified Detection
Analyst)** cover security operations: continuous monitoring, log and network telemetry, and building
**detections** (SIEM rules, Sigma, analytics) with low false positives. **GDSA (Defensible Security
Architect)** covers designing networks and controls that are inherently defensible — segmentation,
zero trust, and layered controls. **GDAT (Defending Advanced Threats)** covers defeating advanced
adversaries by mapping detections and mitigations to the **MITRE ATT&CK** framework across the
kill chain. Many of these use **CyberLive** — real packet captures, real logs, real tooling. This
chapter teaches each with a hands-on defensive walkthrough using open tools (tcpdump/tshark, Zeek/
Suricata concepts, jq, Sigma/ATT&CK).

## Design Considerations

Build detections from **telemetry you actually collect**; tune for signal, not noise (GCDA/GMON).
Map coverage to **MITRE ATT&CK** to find gaps (GDAT). Design for **segmentation and least privilege**
so a breach is contained (GDSA). Analyze traffic with the **right layer** — packets for GCIA, flows/
logs for monitoring. Automate repetitive triage.

## Implementation and Automation

The labs analyze a capture, build a detection, map to ATT&CK, and reason about architecture.

## Validation and Troubleshooting

Confirm the Cyber Defense map:

```text
GCIA = intrusion/traffic analysis + IDS signatures. GMON/GCDA = continuous monitoring + detections (SIEM/Sigma).
GDSA = defensible architecture (segmentation/zero trust). GDAT = defend vs advanced threats via MITRE ATT&CK.
```

Common pitfalls: alerting on everything (no tuning → alert fatigue); and buying tools without
**ATT&CK-mapped** coverage (blind spots).

## Security and Best Practices

Collect the right telemetry, **tune detections**, map coverage to **ATT&CK**, and design
**defensible, segmented** architectures. Validate detections against real captures/logs. Everything
here is defensive.

## Hands-On Lab

Cyber Defense walkthroughs. **Shared prerequisites** — Linux with `tshark`/`tcpdump`, `python3`,
`jq`, in a lab. **Cost:** none.

### Lab 3.1 — GCIA: analyze a capture

**Objective:** Read traffic like an intrusion analyst.

```bash
# Capture a little authorized local traffic, then analyze protocols/conversations:
tcpdump -w /tmp/lab.pcap -c 40 -i lo 2>/dev/null &  ping -c 5 127.0.0.1 >/dev/null; wait
tshark -r /tmp/lab.pcap -q -z io,phs 2>/dev/null | head -20     # protocol hierarchy
tshark -r /tmp/lab.pcap -q -z conv,ip 2>/dev/null | head        # IP conversations
```

**Expected result:** a **protocol hierarchy** and **conversation** summary — the GCIA analyst's view
of a capture.

**Negative test:** judge traffic from packet counts alone; the **protocol hierarchy** and
conversations reveal what's actually happening — analyze, don't guess.

**Rollback:** `rm -f /tmp/lab.pcap`.

### Lab 3.2 — GCDA: build a detection rule

**Objective:** Turn a pattern into a tuned detection.

```python
python3 - <<'PY'
# Toy log; detection = failed logins by source over threshold (brute-force pattern)
logs=[{"src":"10.0.0.9","event":"login_fail"} for _ in range(6)]+[{"src":"10.0.0.5","event":"login_ok"}]
from collections import Counter
fails=Counter(l["src"] for l in logs if l["event"]=="login_fail")
alerts=[s for s,n in fails.items() if n>=5]
print("detection: >=5 login_fail from one src ->", alerts)
print("tune threshold to reduce false positives (GCDA)")
PY
```

**Expected result:** an alert for the brute-force source (>=5 failures) — a tuned **detection**.

**Negative test:** set the threshold to 1 failure; every fat-fingered password alerts — **tune** the
threshold.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — GDAT: map a detection to MITRE ATT&CK

**Objective:** Measure coverage against the framework.

```python
python3 - <<'PY'
coverage={"T1110 Brute Force":"detection: failed-login threshold (have)",
          "T1059 Command & Scripting":"process-cmdline analytics (have)",
          "T1071 App-Layer C2":"beacon/JA3 detection (GAP)",
          "T1486 Data Encrypted for Impact":"mass-file-change alert (GAP)"}
for tech,status in coverage.items(): print(f"{tech:32}: {status}")
print("GDAT: ATT&CK map surfaces coverage gaps to prioritize")
PY
```

**Expected result:** an **ATT&CK** coverage map showing which techniques are covered vs gaps — the
GDAT method.

**Negative test:** claim "we have EDR, so we're covered"; the **ATT&CK map** shows specific gaps —
measure coverage per technique.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — GMON: continuous monitoring health

**Objective:** Verify telemetry is flowing.

```python
python3 - <<'PY'
sources={"firewall":True,"dns":True,"edr":False,"proxy":True}  # is telemetry arriving?
gaps=[s for s,ok in sources.items() if not ok]
print("monitoring gaps (no telemetry):", gaps or "none")
print("GMON: a blind source = an unmonitored attack path; fix before tuning detections")
PY
```

**Expected result:** the list of **blind sources** — continuous-monitoring health (GMON).

**Negative test:** build detections on a source that isn't sending data; they silently never fire —
verify **telemetry flow** first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.5 — GDSA: reason about defensible architecture

**Objective:** Apply segmentation and least privilege.

```python
python3 - <<'PY'
zones={"internet":"untrusted","dmz":"web only","app":"from dmz only","data":"from app only"}
def allowed(src,dst):  # simple segmentation policy
    order=["internet","dmz","app","data"]; return order.index(dst)-order.index(src)==1
for pair in [("internet","dmz"),("dmz","app"),("internet","data")]:
    print(pair, "ALLOW" if allowed(*pair) else "DENY (not adjacent zone)")
PY
```

**Expected result:** internet→dmz and dmz→app **allowed**, internet→data **denied** — a defensible,
segmented design (GDSA).

**Negative test:** flatten the network (internet can reach data); one breach reaches the crown jewels
— **segment** into zones.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cyber Defense spans intrusion/traffic analysis (GCIA), monitoring and detection (GMON/GCDA),
defensible architecture (GDSA), and defending advanced threats via MITRE ATT&CK (GDAT) — the blue
team's core, validated hands-on with CyberLive.

- [ ] I can analyze a capture (GCIA).
- [ ] I can build and tune a detection (GCDA).
- [ ] I can map coverage to ATT&CK (GDAT).
- [ ] I can verify monitoring health and reason about segmentation (GMON/GDSA).
- [ ] I completed Labs 3.1–3.5 including each negative test.
