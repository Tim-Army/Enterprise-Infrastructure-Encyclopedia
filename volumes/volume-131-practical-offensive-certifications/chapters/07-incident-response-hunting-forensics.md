# Chapter 07: Blue Team — Incident Response, Threat Hunting, and Forensics

## Learning Objectives

- Cover the response-side certifications (INE eCIR/eCTHP/eCDFP; TCM PSAP/PMRP).
- Understand the incident-response lifecycle, proactive threat hunting, and digital forensics.
- Model an IR timeline, a hunt hypothesis, and forensic evidence handling.

## After detection: respond, hunt, investigate

Detection ([Chapter 06](06-blue-team-soc-detection.md)) surfaces an incident; then comes the response. INE **eCIR** (Incident Responder), **eCTHP** (Threat Hunting), and **eCDFP** (Digital Forensics), plus TCM **PSAP** and **PMRP** (Malware Research), certify the response disciplines. These are hands-on: you investigate a realistic compromise and produce a professional report.

| Discipline | Question it answers |
|:---|:---|
| **Incident Response (IR)** | Contain, eradicate, recover — and how did they get in, what did they touch? |
| **Threat Hunting** | Are there compromises our detections *missed*? (proactive, hypothesis-driven) |
| **Digital Forensics** | What exactly happened, provably? (evidence, timeline, attribution) |
| **Malware Analysis** | What does this sample do? (behavior, IOCs, capabilities) |

## Hands-On Lab

Python models IR, hunting, and forensics. **Cost:** none.

### Lab 7.1 — The incident-response lifecycle

**Objective:** Walk the IR phases (the eCIR / PSAP core) on the Chapter 06 incident.

```bash
python3 - <<'EOF'
# IR lifecycle (NIST-style): Prepare -> Detect/Analyze -> Contain -> Eradicate -> Recover -> Lessons
incident = "domain compromise (phish -> DA, from Ch06)"
phases = [
  ("Preparation",      "have the plan, tools, and access ready BEFORE the incident"),
  ("Detection/Analysis","confirm scope: which accounts/systems, dwell time, entry vector"),
  ("Containment",      "isolate affected hosts; disable compromised accounts; preserve evidence"),
  ("Eradication",      "remove backdoors, malware, attacker persistence (incl. rogue DA — cf. identity recovery)"),
  ("Recovery",         "restore from KNOWN-CLEAN backups; rebuild DCs if needed; monitor for return"),
  ("Lessons Learned",  "fix the root cause (phishing controls, tiering); update detections"),
]
print(f"IR for: {incident}\n")
for name, action in phases: print(f"  {name:<20}{action}")
print("\nContainment BEFORE eradication; recover from clean backups; close the root cause, not just the symptom.")
EOF
```

**Expected result:** The six IR phases applied to the domain-compromise incident — with the key ordering that **containment precedes eradication** (stop the bleeding, preserve evidence, then remove the attacker), recovery uses **known-clean backups** (ties to [Volume CXXX](../../volume-130-rubrik-certifications/README.md)), and lessons-learned fixes the **root cause**. eCIR/PSAP test executing this lifecycle under realistic conditions.

**Negative test:** Eradicating (wiping the box) before containing and preserving evidence — you destroy the forensic trail and may miss persistence elsewhere; the phase order exists for a reason, and rushing it is a classic IR error.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — A threat-hunting hypothesis

**Objective:** Hunt proactively for what detections missed (the eCTHP skill).

```bash
python3 - <<'EOF'
# Threat hunting is hypothesis-driven: assume a technique, look for its traces, refine.
hypothesis = "An attacker used scheduled tasks for persistence (ATT&CK T1053) that our alerts didn't catch."
# Hunt: enumerate scheduled tasks across hosts, flag the anomalous ones
tasks = [
  {"host":"ws-01", "task":"GoogleUpdate", "signed":True,  "created":"install-time"},
  {"host":"ws-07", "task":"SysUpdate",    "signed":False, "created":"3am, day of the incident"},  # suspicious
  {"host":"srv-03","task":"BackupJob",    "signed":True,  "created":"install-time"},
]
print(f"Hypothesis: {hypothesis}\n")
for t in tasks:
    suspicious = not t["signed"] and "incident" in t["created"]
    print(f"{t['host']} '{t['task']}' signed={t['signed']} created={t['created']}"
          + ("  <-- HUNT HIT: unsigned task created during the incident window" if suspicious else ""))
print("\nHunting finds the persistence the alerts missed; feed the finding back into a new detection.")
EOF
```

**Expected result:** The unsigned `SysUpdate` scheduled task created at 3am during the incident is a hunt hit — persistence the detections missed. Threat hunting is **proactive and hypothesis-driven** (eCTHP): assume a technique (scheduled-task persistence, ATT&CK T1053), search for its traces, and when you find one, turn it into a new detection. It closes the gap between what you detect and what's actually there.

**Negative test:** Waiting for an alert instead of hunting — undetected persistence lets the attacker return after you "recover"; hunting proactively finds what the alerts, by definition, didn't.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Forensic evidence handling

**Objective:** Model the chain-of-custody rigor eCDFP requires.

```bash
python3 - <<'EOF'
import hashlib
# Forensics = provable facts: acquire, hash, preserve chain of custody, analyze COPIES
evidence = b"disk-image-of-compromised-host"
acquired_hash = hashlib.sha256(evidence).hexdigest()[:16]
# Later, verify the working copy hasn't changed:
working_copy = evidence  # analysis is done on a copy, never the original
verify_hash = hashlib.sha256(working_copy).hexdigest()[:16]
print(f"acquisition hash: {acquired_hash}")
print(f"verify hash:      {verify_hash}")
print(f"integrity: {'INTACT — evidence unaltered (admissible)' if acquired_hash == verify_hash else 'BROKEN — chain of custody compromised'}")
print("\nRules: hash on acquisition, analyze copies, log every handoff (chain of custody) -> findings hold up.")
EOF
```

**Expected result:** The acquisition and verification hashes match — evidence integrity intact, chain of custody preserved. Digital forensics (eCDFP) is about **provable facts**: hash evidence on acquisition, analyze *copies* not originals, and log every handoff, so the findings withstand scrutiny (legal, HR, or a post-incident review). Rigor is the difference between a finding that holds up and one that's dismissed.

**Negative test:** Analyzing the original evidence directly (altering timestamps) or skipping the hash — the evidence is now tainted and inadmissible; forensic discipline exists to keep findings provable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The IR lifecycle (contain before eradicate; recover clean; fix root cause) drilled.
- [ ] Hypothesis-driven threat hunting (find what detections missed) modeled.
- [ ] Forensic evidence handling (hash, copies, chain of custody) internalized.
