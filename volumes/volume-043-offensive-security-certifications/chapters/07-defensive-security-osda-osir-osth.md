# Chapter 07: Defensive Security — OSDA, OSIR, and OSTH

## Learning Objectives

- Explain the defensive OffSec credentials: OSDA (SOC-200), OSIR (IR-200), and OSTH (TH-200).
- Distinguish detection (OSDA), incident response (OSIR), and threat hunting (OSTH).
- Practice detection, response, and hunting methodology on your own telemetry.
- Apply the same attacker knowledge from earlier chapters to defense.
- Complete per-topic walkthroughs for the OSDA, OSIR, and OSTH topic areas.

## Theory and Architecture

OffSec's **defensive** track applies offensive knowledge to detection and
response — the blue-team counterpart to the earlier chapters:

- **OSDA (OffSec Defense Analyst, SOC-200)** — **detection**: SOC operations,
  detecting attacks across the kill chain, log and SIEM analysis, and recognizing
  Active Directory and lateral-movement activity. Uses the **"+" renewal**.
- **OSIR (OffSec Incident Responder, IR-200)** — **incident response**: the IR
  lifecycle (preparation, identification, containment, eradication, recovery,
  lessons learned), forensics, and timeline reconstruction. Uses the **"+"
  renewal**.
- **OSTH (OffSec Threat Hunter, TH-200)** — **threat hunting**: hypothesis-driven
  hunting, working from **IOCs** and **TTPs** (aligned to MITRE ATT&CK), and
  finding adversary activity that evaded automated detection. Uses the **"+"
  renewal**.

Together they close the loop: the attacks studied in Chapters 03–06 are here
**detected, responded to, and hunted**.

## Design Considerations

Choose by **blue-team role**: **OSDA** for SOC analysts building and tuning
detections; **OSIR** for responders who must contain and recover from incidents;
**OSTH** for hunters who proactively search telemetry for what alerts missed. All
three are strongest when paired with the **offensive** understanding from earlier
chapters — you detect, respond to, and hunt what you understand how attackers do.

## Implementation and Automation

The labs below practice defensive methodology on **your own system's logs and
telemetry**: detection from logs (OSDA), the IR lifecycle and timeline
reconstruction (OSIR), and hypothesis-driven hunting against ATT&CK TTPs (OSTH).

## Validation and Troubleshooting

Confirm the courses on offsec.com:

```text
offsec.com/courses:
  - SOC-200 -> OSDA (detection, SIEM, kill-chain) — "+" renewal
  - IR-200  -> OSIR (incident response lifecycle, forensics) — "+" renewal
  - TH-200  -> OSTH (hypothesis-driven threat hunting, TTPs) — "+" renewal
```

Common pitfalls: alert-only thinking (detection without **response** or
**hunting** leaves gaps); and hunting without a **hypothesis** (aimless log
review is not hunting).

## Security and Best Practices

Build detections mapped to **MITRE ATT&CK**, rehearse the **IR lifecycle** before
an incident, preserve evidence (timeline, hashes) during response, and hunt on a
schedule with **testable hypotheses**. Feed findings back into detections — the
defensive loop only works if it improves over time.

## References and Knowledge Checks

- offsec.com: *SOC-200 (OSDA)*, *IR-200 (OSIR)*, *TH-200 (OSTH)* course pages; MITRE ATT&CK.

**Knowledge checks**

1. How do OSDA, OSIR, and OSTH divide detection, response, and hunting?
2. What are the phases of the incident-response lifecycle?
3. What makes a threat hunt different from routine log review?

## Hands-On Lab

Per-topic walkthroughs — **on your own system's logs and telemetry.**

**Shared prerequisites** — a Linux shell with `journalctl`/`last`, `python3`, and
`sha256sum`. **Cost:** none.

### OSDA — Detection

### Lab 7.1 — OSDA: detect a brute-force pattern in logs

**Objective:** Write a detection over authentication logs.

```bash
journalctl _COMM=sshd --no-pager 2>/dev/null | grep -c 'Failed password' \
  || echo "0"
echo "Detection rule: >10 failed logins from one source in 5 min -> alert (spraying/brute force)."
```

**Expected result:** a count of failed authentications and a threshold-based
detection rule — the log-analysis detection OSDA builds.

**Negative test:** alert on every single failure; tune thresholds so real attacks
stand out from noise.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — OSDA: map detections to the kill chain

**Objective:** Place detections along the attack kill chain.

```bash
python3 - <<'PY'
chain = {"Recon":"scan/enumeration spikes","Initial Access":"exploit/phish signatures",
         "Priv Esc":"new admin, SUID abuse","Lateral Movement":"remote-exec, unusual auth graph",
         "Exfil":"large egress, rare destinations"}
for phase,det in chain.items(): print(f"{phase:16} -> detect: {det}")
PY
```

**Expected result:** a detection per kill-chain phase — the coverage model OSDA
teaches (detect early and across the chain).

**Negative test:** detect only at exfiltration; earlier detection limits damage —
cover the whole chain.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### OSIR — Incident Response

### Lab 7.3 — OSIR: the incident-response lifecycle

**Objective:** Walk the IR phases and their goals.

```bash
python3 - <<'PY'
for i,p in enumerate(["Preparation","Identification","Containment","Eradication",
                      "Recovery","Lessons Learned"],1):
    print(f"{i}. {p}")
print("Goal: contain fast, preserve evidence, eradicate root cause, recover safely, improve.")
PY
```

**Expected result:** the six IR phases (PICERL) — the response lifecycle OSIR
certifies.

**Negative test:** wipe and rebuild before **identification/containment**; you
destroy evidence and may miss persistence — follow the lifecycle.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — OSIR: preserve evidence and build a timeline

**Objective:** Capture integrity-preserving evidence for a timeline.

```bash
last -n 10 > evidence_logins.txt 2>/dev/null || journalctl -n 10 > evidence_logins.txt
sha256sum evidence_logins.txt | tee evidence_logins.sha256
echo "Timeline: correlate auth, process, and file events by timestamp to reconstruct the incident."
```

**Expected result:** an evidence file with a SHA-256 to prove integrity — the
forensic-preservation and timeline habit OSIR requires.

**Negative test:** edit logs while investigating; hashing proves integrity —
preserve, don't alter, evidence.

**Rollback:** `rm -f evidence_logins.txt evidence_logins.sha256`

### OSTH — Threat Hunting

### Lab 7.5 — OSTH: hypothesis-driven hunting

**Objective:** Frame a hunt as a testable hypothesis.

```bash
python3 - <<'PY'
hunt = {"Hypothesis":"an attacker used a scheduled task for persistence",
        "Data":"task creation events + parent process + command line",
        "Test":"list non-baseline scheduled tasks; investigate anomalies",
        "Outcome":"confirm/deny; if new TTP found, write a detection"}
for k,v in hunt.items(): print(f"{k:11}: {v}")
PY
```

**Expected result:** a structured hunt (hypothesis → data → test → outcome) — the
method that distinguishes hunting from routine review.

**Negative test:** browse logs with no hypothesis; a hunt needs a **testable
question** to be productive.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.6 — OSTH: hunt on IOCs and TTPs (ATT&CK-aligned)

**Objective:** Turn a TTP into a hunt and a detection.

```bash
python3 - <<'PY'
ttp = {"Technique":"T1053 Scheduled Task/Job (ATT&CK)",
       "IOC hunt":"unexpected task names, unusual authors, encoded commands",
       "Detect":"alert on task creation by non-admin/unusual parent"}
for k,v in ttp.items(): print(f"{k:10}: {v}")
PY
```

**Expected result:** a MITRE ATT&CK technique turned into an IOC hunt and a
detection rule — the TTP-driven hunting OSTH teaches, feeding back into OSDA
detections.

**Negative test:** hunt only for known file hashes (IOCs); **TTP/behavior**
hunting catches variants that change hashes — hunt behaviors too.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OffSec's defensive track closes the loop on the offensive chapters: **OSDA**
(SOC-200) builds detections across the kill chain, **OSIR** (IR-200) runs the
incident-response lifecycle and forensics, and **OSTH** (TH-200) hunts adversary
TTPs — all three renewable under the "+" model. They apply the same attacker
knowledge from Chapters 03–06 to detection, response, and hunting.

- [ ] I can distinguish OSDA, OSIR, and OSTH.
- [ ] I can write a threshold detection and map detections to the kill chain.
- [ ] I can walk the IR lifecycle and preserve evidence with hashing.
- [ ] I can frame a hypothesis-driven, ATT&CK-aligned hunt.
- [ ] I completed Labs 7.1–7.6 including each negative test.
