# Chapter 04: Ransomware Resilience

## Learning Objectives

- Explain immutable snapshots and why immutability defeats backup tampering.
- Describe DataLock (WORM) and air-gapping.
- Understand anomaly and threat detection over backup data.
- Recognize rapid recovery as the resilience payoff.

*Cert relevance: ransomware resilience is central to the Security Specialist (COH350) and the whole data-security thesis.*

## Immutable snapshots

The foundation of ransomware resilience is the **immutable snapshot**: a backup copy that, once written, **cannot be modified or deleted** for its retention period — not by an administrator, not by a compromised account, not by ransomware. Cohesity's backups are immutable by design: the snapshot is a read-only, unchangeable point-in-time copy. This directly defeats the modern ransomware playbook ([Chapter 2](02-modern-data-security-and-management.md)) of **deleting the backups first** — the attacker simply *cannot*, because immutability is enforced by the platform, not by permissions an attacker could steal. Immutability is the single most important ransomware-resilience control. The lab models it.

## DataLock (WORM) and air-gapping

Cohesity strengthens immutability with:

- **DataLock** — a **WORM** (write-once, read-many) capability that locks backups for a defined period under strict controls, so that **even a Cohesity administrator** cannot delete them before the lock expires (often requiring separate security-officer approval). This defends against **insider threat** and **compromised admin credentials**, not just external ransomware.
- **Air-gapping** — keeping an isolated copy **off the production network** (logically or physically), so even a total network compromise cannot reach it. Cohesity's [FortKnox (Chapter 6)](06-fortknox-cyber-vaulting.md) provides a cloud-based air-gapped vault.

Together these mean a clean copy survives **all** the ways backups are attacked: external ransomware, malicious insiders, stolen admin accounts, and network-wide compromise. The lab models DataLock.

## Anomaly and threat detection

Resilience is not only about surviving an attack but **detecting it early.** Cohesity analyzes backup data for **anomalies** that signal ransomware: a sudden spike in data-change rate, unusual encryption entropy, or mass file modifications between backups are strong indicators that data is being encrypted. Because Cohesity sees every backup, it has a **unique vantage point** to spot these patterns — and can alert before the damage is complete, and identify a **clean recovery point** (the last snapshot before the anomaly) to restore from. Detecting the attack and knowing *which* backup is clean is as important as having the backup. The lab models anomaly detection.

## Rapid recovery: the payoff

The payoff of all this — immutable, air-gapped, monitored backups — is **rapid, clean recovery.** When ransomware hits, resilience means: a clean copy **exists** (immutability), you **know which** copy is clean (anomaly detection), and you can **restore it fast at scale** ([instant mass restore, Chapter 3](03-dataprotect.md)). The goal is to make ransomware a **recoverable event** rather than a catastrophe — turning "pay the ransom or lose everything" into "restore from a clean immutable copy and move on." That resilience is the whole value proposition. The lab synthesizes.

## Hands-On Lab

Python models immutability and anomaly detection. **Cost:** none.

### Lab 4.1 — Immutability plus anomaly detection enable clean recovery

**Objective:** See how immutability and detection combine for resilience.

```bash
python3 - <<'EOF'
# a series of daily immutable snapshots; ransomware starts encrypting on day 4
snapshots = [
    {"day": 1, "change_rate_pct": 3,  "entropy": "normal"},
    {"day": 2, "change_rate_pct": 4,  "entropy": "normal"},
    {"day": 3, "change_rate_pct": 3,  "entropy": "normal"},
    {"day": 4, "change_rate_pct": 78, "entropy": "high"},    # ransomware encrypting!
    {"day": 5, "change_rate_pct": 85, "entropy": "high"},
]
IMMUTABLE = True   # attacker cannot delete/alter any of these

print("Daily immutable snapshots — Cohesity analyzes each for anomalies:\n")
clean_point = None
for s in snapshots:
    anomaly = s["change_rate_pct"] > 40 or s["entropy"] == "high"
    tag = "  *** ANOMALY: ransomware-like (mass change + high entropy)" if anomaly else "  ok"
    if not anomaly:
        clean_point = s["day"]
    print(f"   day {s['day']}: change={s['change_rate_pct']:>2}%  entropy={s['entropy']:<6}{tag}")
print()
print(f"   attacker tried to DELETE backups first: BLOCKED (immutable={IMMUTABLE})")
print(f"   last CLEAN recovery point: day {clean_point} (before the anomaly)")
print(f"   -> restore day {clean_point}'s immutable snapshot at scale = clean recovery\n")
print("Ransomware resilience = three things together:")
print("  1. IMMUTABILITY — a clean copy EXISTS (attacker can't delete/alter it: not via")
print("     ransomware, stolen admin creds (DataLock/WORM), or network compromise (air-gap)).")
print("  2. ANOMALY DETECTION — Cohesity sees every backup, spots the mass-change/high-entropy")
print("     signature, and identifies WHICH snapshot is clean (day 3, before day-4 encryption).")
print("  3. RAPID MASS RESTORE — bring the whole estate back fast from that clean point.")
print("Result: ransomware becomes a RECOVERABLE event, not 'pay or lose everything.'")
EOF
```

**Expected result:** Daily immutable snapshots where days 4–5 trip the anomaly detector (mass change rate and high entropy), the attacker's delete attempt is blocked by immutability, and day 3 is identified as the last clean recovery point. The resilience lesson is that immutability guarantees a clean copy exists, anomaly detection identifies which copy is clean (and catches the attack early), and rapid mass restore brings the estate back — turning ransomware into a recoverable event.

**Negative test:** Keeping backups that an admin (or a stolen admin credential) can delete, with no anomaly detection. Attackers delete such backups first, and without detection you cannot tell which copy predates the encryption; immutability plus anomaly detection is what makes recovery reliable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Immutable snapshots understood — backups that cannot be modified or deleted, defeating backup tampering.
- [ ] DataLock (WORM) and air-gapping understood as defenses against insiders, stolen admin credentials, and network compromise.
- [ ] Anomaly and threat detection over backup data understood — early detection and identifying the clean recovery point.
- [ ] Rapid recovery recognized as the payoff — making ransomware a recoverable event.
