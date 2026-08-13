# Chapter 04: VMDR — Detection and TruRisk Prioritization

## Learning Objectives

- Detect vulnerabilities with agents and scanners.
- Understand the Qualys TruRisk score.
- Prioritize by threat intelligence and asset criticality.
- Focus remediation on real risk.
- Complete a walkthrough for each detection/prioritization topic.

## Theory and Architecture

The **detection** stage of VMDR identifies vulnerabilities across the inventory — each detection is a
**QID (Qualys ID)**, Qualys's identifier for a specific vulnerability check (analogous to a plugin).
As with any scanner, the volume of findings vastly exceeds remediation capacity, so **prioritization**
is the value. Qualys's answer is the **TruRisk score** — a risk-based score that goes beyond static
CVSS by incorporating **real-world threat intelligence** (is there a known exploit, active
exploitation, ransomware association, malware, exploit maturity?) and **asset criticality** (how
important is the affected asset to the business). This produces a score reflecting **actual risk**, so
teams fix the exploitable vulnerabilities on important assets first rather than chasing every "high
CVSS" finding. Qualys also surfaces indicators like **exploitable**, **actively attacked**, and
**high lateral movement**. Prioritizing by **TruRisk** focuses limited effort where it reduces the
most risk. This chapter teaches each with a hands-on defensive walkthrough (detection, TruRisk
reasoning, and prioritization).

## Design Considerations

Detect continuously with **agents** and periodically with **scanners**. Prioritize by **TruRisk**
(threat intel + criticality), not raw CVSS. Focus on **exploitable/actively-attacked** vulnerabilities
first. Weight by **asset criticality**. Set risk-based **SLAs**. Re-detect to confirm fixes.

## Implementation and Automation

The labs detect vulns, compute a TruRisk-style score, and prioritize.

## Validation and Troubleshooting

Confirm the detection/prioritization model:

```text
Detection: each vuln = a QID (Qualys ID). Prioritization: TruRisk score = CVSS + real-world threat intel (exploit/active attack/ransomware/malware) + asset criticality.
Indicators: exploitable, actively attacked, lateral movement. Prioritize exploitable on critical assets first.
```

Common pitfalls: patching by **CVSS** alone (wastes effort on non-exploited issues); and ignoring
**asset criticality**.

## Security and Best Practices

Prioritize by **TruRisk**, focus on **exploitable/actively-attacked** vulnerabilities, weight by
**criticality**, set risk-based **SLAs**, and **re-detect** to verify. All work is defensive.

## Hands-On Lab

Detection/prioritization walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 4.1 — Interpret a detection (QID)

**Objective:** Read a Qualys vulnerability.

```python
python3 - <<'PY'
detections=[{"qid":91234,"title":"Missing critical OS patch","severity":5,"exploitable":True},
            {"qid":38657,"title":"Weak TLS cipher","severity":3,"exploitable":False}]
for d in detections: print(f"QID {d['qid']} sev{d['severity']} exploitable={d['exploitable']} - {d['title']}")
print("Qualys: each detection is a QID; severity + exploitability guide attention")
PY
```

**Expected result:** detections as **QIDs** with severity and exploitability — how Qualys reports
vulnerabilities.

**Negative test:** treat all severity-5 QIDs equally; **exploitability** differentiates them —
consider it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Compute a TruRisk-style score

**Objective:** Combine threat intel and criticality.

```python
python3 - <<'PY'
def trurisk(cvss, threat_factor, asset_criticality):  # illustrative
    # threat_factor: 1.0 none, 1.5 exploit exists, 2.0 actively exploited/ransomware
    return round(min(1000, cvss*10 * threat_factor * (asset_criticality/5)), 0)
cases=[{"cvss":9.8,"threat":1.0,"acr":2,"note":"high CVSS, no exploit, low-value asset"},
       {"cvss":7.2,"threat":2.0,"acr":5,"note":"actively exploited, critical asset"}]
for c in cases: print(f"TruRisk {trurisk(c['cvss'],c['threat'],c['acr']):>4} - {c['note']}")
print("TruRisk: active exploitation on a critical asset outranks a higher raw CVSS")
PY
```

**Expected result:** the actively-exploited vuln on a critical asset scores higher **TruRisk** despite
lower CVSS — risk-based scoring.

**Negative test:** rank by **CVSS** only; you fix the theoretical 9.8 before the exploited 7.2 — use
**TruRisk**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Prioritize the remediation queue

**Objective:** Fix the highest risk first.

```python
python3 - <<'PY'
queue=[{"host":"crown-db","trurisk":880,"exploited":True},{"host":"lab-vm","trurisk":300,"exploited":False},
       {"host":"dmz-web","trurisk":760,"exploited":True}]
for item in sorted(queue,key=lambda x:-x["trurisk"]):
    print(f"TruRisk {item['trurisk']:>3}  {item['host']:9} exploited={item['exploited']}")
print("Remediation: order by TruRisk -> most risk reduced first")
PY
```

**Expected result:** the queue ordered by **TruRisk** — risk-based remediation.

**Negative test:** work by host name; risk isn't reduced efficiently — order by **TruRisk**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Filter to actively-attacked vulnerabilities

**Objective:** Focus on what attackers use now.

```python
python3 - <<'PY'
vulns=[{"qid":91234,"actively_attacked":True,"ransomware":True},
       {"qid":38657,"actively_attacked":False,"ransomware":False}]
urgent=[v["qid"] for v in vulns if v["actively_attacked"] or v["ransomware"]]
print("fix immediately (active/ransomware):", urgent)
print("VMDR: threat-intel filters surface the vulnerabilities under active exploitation")
PY
```

**Expected result:** the **actively-attacked/ransomware** vuln surfaced for immediate action — threat-
intel prioritization.

**Negative test:** ignore threat intel and work purely by severity; you may miss the one being
exploited **now** — filter by active attack.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VMDR detects vulnerabilities as QIDs and prioritizes with the TruRisk score — combining threat
intelligence and asset criticality so teams fix the exploitable, actively-attacked vulnerabilities on
critical assets first.

- [ ] I can interpret a detection (QID).
- [ ] I can compute a TruRisk-style score.
- [ ] I can prioritize the remediation queue.
- [ ] I can filter to actively-attacked vulnerabilities.
- [ ] I completed Labs 4.1–4.4 including each negative test.
