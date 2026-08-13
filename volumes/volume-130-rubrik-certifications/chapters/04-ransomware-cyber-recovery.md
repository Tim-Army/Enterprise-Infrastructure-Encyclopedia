# Chapter 04: Ransomware and Cyber Recovery

## Learning Objectives

- Cover Rubrik's ransomware/cyber-recovery capabilities: anomaly detection and Data Threat Analytics.
- Understand how the backup stream becomes a detection sensor.
- Model anomaly detection on backup deltas and finding the last clean snapshot.

## The backup as a detection sensor

Because Rubrik snapshots data continuously, the **backup stream itself reveals an attack in progress**: ransomware encrypting files shows up as an anomalous surge in change rate, entropy, and add/modify/delete patterns. Rubrik's **Data Threat Analytics** watches for these anomalies, alerts, and — critically — helps you find the **last clean snapshot** before the encryption began, so recovery restores known-good data, not re-encrypted data.

| Capability | What it does |
|:---|:---|
| **Anomaly detection** | Flag unusual change rate / entropy / file-operation patterns across snapshots |
| **Data Threat Analytics** | Analyze the backup for signs of ransomware/malware and scope the impact |
| **Threat hunting** | Search backups for indicators of compromise (IOCs) — including in historical snapshots |
| **Threat monitoring** | Continuously scan new snapshots for known threats |
| **Recovery point selection** | Identify the last clean snapshot to avoid reinfecting on restore |

## Hands-On Lab

Python models anomaly detection on backup metadata. **Cost:** none.

### Lab 4.1 — Detect ransomware from backup deltas

**Objective:** Flag the snapshot where mass encryption began — the core cyber-recovery signal.

```bash
python3 - <<'EOF'
# Per-snapshot metrics; ransomware = sudden spike in files-modified + entropy
snapshots = [
  {"t":"Mon 00:00", "files_modified":120,  "avg_entropy":4.1},
  {"t":"Mon 04:00", "files_modified":140,  "avg_entropy":4.2},
  {"t":"Mon 08:00", "files_modified":135,  "avg_entropy":4.0},
  {"t":"Mon 12:00", "files_modified":9800, "avg_entropy":7.9},   # <-- ransomware (mass modify, high entropy)
  {"t":"Mon 16:00", "files_modified":9600, "avg_entropy":7.9},
]
baseline_mod = sum(s["files_modified"] for s in snapshots[:3]) / 3
for s in snapshots:
    spike = s["files_modified"] > baseline_mod * 5
    enc   = s["avg_entropy"] > 7.0   # near-random -> encrypted/compressed
    flag = "  <-- ANOMALY (mass modify + high entropy = likely ransomware)" if spike and enc else ""
    print(f"{s['t']:<10} modified={s['files_modified']:<6} entropy={s['avg_entropy']}{flag}")
EOF
```

**Expected result:** The `Mon 12:00` snapshot is flagged — a 70× surge in modified files with near-random entropy (7.9), the signature of mass encryption. The backup stream detected the attack **from the data itself**, without any endpoint agent. Data Threat Analytics automates this across the whole estate; RCSA/cyber-recovery material tests recognizing this pattern.

**Negative test:** Watching only production endpoints for ransomware — a stealthy strain may evade EDR, but it cannot hide the mass-encryption footprint in the backup deltas; the backup is an independent sensor.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Find the last clean snapshot

**Objective:** Select a recovery point *before* the encryption — avoid reinfection.

```bash
python3 - <<'EOF'
snapshots = [
  {"t":"Mon 00:00","clean":True},
  {"t":"Mon 04:00","clean":True},
  {"t":"Mon 08:00","clean":True},   # last clean
  {"t":"Mon 12:00","clean":False},  # ransomware
  {"t":"Mon 16:00","clean":False},
]
last_clean = None
for s in snapshots:
    if s["clean"]: last_clean = s["t"]
    else: break
print(f"Last clean snapshot: {last_clean}  -> recover from HERE (Mon 08:00), not the latest")
print("Recovering the latest snapshot would restore the encrypted data — reinfection.")
EOF
```

**Expected result:** `Mon 08:00` is the last clean snapshot; recovering the *latest* would restore the encrypted files. The cyber-recovery discipline: **don't restore the newest backup blindly** — restore the last known-clean point identified by anomaly analysis. Getting this wrong reintroduces the ransomware; getting it right is the whole value of detection integrated with recovery.

**Negative test:** "Just restore last night's backup" — if last night is already encrypted, you've recovered the ransomware; the last-clean-snapshot selection (informed by Data Threat Analytics) is what prevents that.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Threat hunting in backups

**Objective:** Search historical snapshots for an IOC — find when a threat first appeared.

```bash
python3 - <<'EOF'
# An IOC (malicious file hash / path) is discovered today; hunt backwards to scope the intrusion
ioc = "evil.dll"
snapshots = {
  "Jul 01": [], "Jul 15": [], "Jul 28": ["evil.dll"],   # first appearance
  "Aug 01": ["evil.dll"], "Aug 04": ["evil.dll"],
}
first_seen = next((t for t, files in snapshots.items() if ioc in files), None)
print(f"IOC '{ioc}' first appears in the {first_seen} snapshot")
print("-> dwell time established; scope which systems/snapshots are affected; recover pre-'Jul 28' where needed")
EOF
```

**Expected result:** The IOC first appears in the `Jul 28` snapshot — establishing **dwell time** and scope. Threat hunting *in the backups* answers "how long were they in, and what did they touch?" using historical snapshots as a forensic timeline. This is a distinctive Rubrik capability: the backup is not just recovery, but investigation.

**Negative test:** Only scanning live systems for the IOC — you learn it's present now but not *when it arrived* or *what else it reached*; the historical snapshots give the timeline live scanning can't.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Anomaly detection on backup deltas (change rate + entropy) drilled.
- [ ] Last-clean-snapshot selection (avoid reinfection) internalized.
- [ ] Threat hunting in historical snapshots (dwell time, scope) modeled.
