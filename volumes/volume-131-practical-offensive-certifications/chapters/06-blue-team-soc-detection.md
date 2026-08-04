# Chapter 06: Blue Team — SOC Analysis and Detection

## Learning Objectives

- Cover the defensive/blue-team certifications (HTB CDSA; TCM PSAA/PSAP; INE eSOC).
- Understand SOC operations: monitoring, triage, detection engineering, and correlation.
- Model a detection rule and an alert-triage decision.

## The other half of the same knowledge

The offensive techniques of Chapters 02–05 exist, from the blue-team perspective, to be **detected and responded to**. HTB **CDSA**, TCM **PSAA**/**PSAP**, and INE **eSOC** certify exactly this: operating a Security Operations Center — monitoring, triage, detection engineering, and correlation. These are practical, hands-on certs too: you work a realistic compromise scenario and report on it, just from the defender's chair.

| SOC skill | What it is |
|:---|:---|
| **Monitoring** | Aggregate logs/telemetry (SIEM) across endpoints, network, identity, cloud |
| **Triage** | Separate true positives from noise; prioritize by impact |
| **Detection engineering** | Write rules that catch attacker techniques (mapped to MITRE ATT&CK) |
| **Correlation** | Connect disparate events into one incident story |
| **Reporting / escalation** | Document and hand off with the context responders need |

## Hands-On Lab

Python models detection and triage. **Cost:** none.

### Lab 6.1 — Write a detection from an attack signature

**Objective:** Convert the kerberoasting knowledge from [Chapter 04](04-network-and-active-directory.md) into a SOC detection.

```bash
python3 - <<'EOF'
# Detection engineering: a rule mapped to a technique (MITRE ATT&CK T1558.003 Kerberoasting)
def detect_kerberoasting(events):
    # rule: a single account requesting many TGS (Event 4769) with RC4 in a short window
    alerts = []
    for user, tgs_count, rc4_ratio in events:
        if tgs_count >= 15 and rc4_ratio > 0.8:
            alerts.append(f"ALERT [T1558.003 Kerberoasting]: {user} — {tgs_count} TGS, {rc4_ratio:.0%} RC4")
    return alerts
events = [("svc-scan", 3, 0.0), ("jdoe", 40, 0.95), ("backup", 12, 0.2)]
for a in detect_kerberoasting(events): print(a)
print("\nA good detection: mapped to ATT&CK, tuned to reduce false positives, with clear triage context.")
EOF
```

**Expected result:** `jdoe`'s 40 TGS requests at 95% RC4 fire the detection, mapped to MITRE ATT&CK T1558.003. Detection engineering is where offensive knowledge (how kerberoasting works, [Chapter 04](04-network-and-active-directory.md)) becomes a defensive control (a tuned SIEM rule). CDSA/eSOC teach building these — mapped to ATT&CK, tuned against false positives, with triage context baked in.

**Negative test:** A rule with no threshold (`tgs_count >= 1`) — it fires on every normal Kerberos request, drowning the SOC; tuning (thresholds, ratios) is what makes a detection usable, a core detection-engineering skill.

**Cleanup:** None.

### Lab 6.2 — Triage: true positive vs noise

**Objective:** Prioritize alerts the way a SOC analyst must.

```bash
python3 - <<'EOF'
# Triage: score alerts by fidelity + asset value + corroboration; escalate the real ones
def triage(alert, fidelity, asset_value, corroborated):
    score = fidelity*asset_value + (3 if corroborated else 0)
    if score >= 12: return f"ESCALATE (incident): {alert}"
    if score >= 6:  return f"INVESTIGATE: {alert}"
    return f"MONITOR/close: {alert}"
print(triage("kerberoasting on DC-adjacent acct", fidelity=4, asset_value=4, corroborated=True))
print(triage("single failed login", fidelity=1, asset_value=2, corroborated=False))
print(triage("EDR flag on exec laptop", fidelity=3, asset_value=3, corroborated=False))
EOF
```

**Expected result:** The kerberoasting alert on a high-value account with corroboration escalates to an incident; a single failed login is monitored/closed; a mid-fidelity EDR flag gets investigated. Triage is the SOC's core discipline — **most alerts are noise, and the skill is finding the few that matter** by fidelity, asset value, and corroboration. Alert fatigue is the enemy; disciplined triage is the answer.

**Negative test:** Treating every alert with equal urgency — analysts burn out and miss the real incident in the flood; triage prioritization is what makes a SOC effective, and the practical exams test it under realistic alert volume.

**Cleanup:** None.

### Lab 6.3 — Correlate events into an incident

**Objective:** Connect disparate signals into one story — the analysis these certs reward.

```bash
python3 - <<'EOF'
# Individually-minor events that together tell an intrusion story
events = [
  ("08:00", "jdoe", "phishing email clicked"),
  ("08:05", "jdoe-workstation", "unusual PowerShell spawned"),
  ("08:20", "jdoe", "kerberoasting detection (Ch06 Lab6.1)"),
  ("09:00", "svc-sql", "login to a server jdoe never uses"),
  ("09:30", "DC", "new domain admin added"),
]
print("Correlated timeline (one incident):")
for t, who, what in events: print(f"  {t}  {who:<16} {what}")
print("\nStory: phish -> code exec -> credential theft -> lateral move -> domain admin.")
print("Each event alone looks minor; correlated, it's a full domain-compromise incident -> ESCALATE + IR (Ch 07).")
EOF
```

**Expected result:** Five individually-minor events correlate into a complete intrusion story: phishing → code execution → kerberoasting → lateral movement → domain admin. **Correlation is the analyst skill that turns scattered alerts into an incident** — no single event is alarming, but the chain is a domain compromise. This is exactly what CDSA/PSAP grade: thinking across data sources to see the whole attack, then handing off to incident response ([Chapter 07](07-incident-response-hunting-forensics.md)).

**Negative test:** Analyzing each event in isolation — each closes as low-priority, and the compromise proceeds undetected; correlation across time and data sources is what reveals the intrusion the individual alerts hide.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Detection engineering (attack knowledge → tuned, ATT&CK-mapped rule) drilled.
- [ ] Triage (fidelity × asset value × corroboration) to beat alert fatigue internalized.
- [ ] Correlation of scattered events into one incident story modeled.
