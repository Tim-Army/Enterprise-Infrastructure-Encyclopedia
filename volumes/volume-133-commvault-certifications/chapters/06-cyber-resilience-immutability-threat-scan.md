# Chapter 06: Cyber Resilience — Immutability, Air Gap, and Threat Scan

## Learning Objectives

- Implement immutability and air gap so backups survive an attack.
- Detect ransomware and corruption through anomaly detection and Threat Scan.
- Harden the backup platform itself against being the attacker's first target.
- Identify the last known-clean recovery point.

## The backup platform is a target

Cyber resilience is a full pillar of the Readiverse program and an exam component even at the Practitioner tier, for a straightforward reason: **modern ransomware attacks the backups first.** An attacker who encrypts production but leaves backups intact has not won; an attacker who deletes or encrypts the backups has removed the alternative to paying.

That changes the design goal. Backup is no longer "a copy in case of hardware failure" but a control that must survive an adversary who has administrative access to your environment and specifically wants it gone.

## Immutability

**Immutable** storage cannot be modified or deleted until its retention expires — enforced by the storage layer (object-lock/WORM), not by the backup application's own permissions. That distinction is the whole point: if immutability were enforced only by the application, an attacker with application admin rights could turn it off.

| Control | What it stops |
|:---|:---|
| **Object lock / WORM retention** | Deletion or encryption of existing backup copies |
| **Air gap** (logical or physical) | An attacker reaching the copy at all |
| **Separate credentials/identity domain** | Compromised production admin rights extending to backups |
| **MFA + RBAC on the backup console** | Console-driven mass deletion |

An **air gap** may be physical (offline tape) or **logical** (a copy in a separate account/tenant, reachable only during a narrow replication window, with independent credentials). Logical air gaps are what most cloud deployments actually use.

## Anomaly detection and Threat Scan

Immutability protects the copy; **detection** tells you the copy contains something bad. Two complementary signals:

- **Backup-behavior anomalies** — a sudden spike in change rate, a collapse in deduplication ratio (encrypted data does not deduplicate — Chapter 04), unusual deletion activity, or backup size changes that have no business explanation. Mass encryption looks exactly like this.
- **Content inspection** — Commvault's **Threat Scan** examines the protected data itself for indicators of corruption, encryption, or malware, so you learn whether a recovery point is *clean* rather than merely *present*.

Together they answer the question that matters during an incident: **what is the last known-clean recovery point?** Restoring from an infected backup reinfects, and without detection you find that out by doing it.

## Hands-On Lab

Python models the resilience controls. **Cost:** none.

### Lab 6.1 — Immutable storage that resists an admin attacker

**Objective:** Enforce retention at the storage layer.

```bash
python3 - <<'EOF'
import time
class ImmutableStore:
    def __init__(self): self.objects = {}
    def write(self, key, data, lock_days):
        if key in self.objects: return f"DENIED overwrite of {key} (WORM)"
        self.objects[key] = {"data":data, "locked_until": time.time() + lock_days*86400}
        return f"WROTE {key} (locked {lock_days}d)"
    def delete(self, key, requester_is_admin=False):
        o = self.objects.get(key)
        if not o: return f"{key} not found"
        if time.time() < o["locked_until"]:
            return (f"DENIED delete of {key} — object lock active "
                    f"({'even for admin/root' if requester_is_admin else 'retention not expired'})")
        del self.objects[key]; return f"DELETED {key} (retention expired)"

s = ImmutableStore()
print(s.write("backup-2026-08-04-full", b"...", lock_days=30))
print(s.write("backup-2026-08-04-full", b"ransomware", lock_days=30))     # overwrite attempt
print(s.delete("backup-2026-08-04-full", requester_is_admin=True))        # admin delete attempt
print("\nEnforcement is in the STORAGE layer: compromising the backup application does not lift the lock.")
EOF
```

**Expected result:** The overwrite is denied, and so is deletion **even by an administrator**, because the lock lives in the storage layer. That is precisely the threat model — the attacker is assumed to have admin credentials. Immutability implemented as an application setting fails this test, which is why the exams emphasize storage-enforced object lock.

**Negative test:** "Immutability" configured only as a retention rule in the backup software — an attacker with console admin simply shortens retention and then deletes, and the control evaporates exactly when needed.

**Cleanup:** None.

### Lab 6.2 — Detect ransomware from backup behavior

**Objective:** Spot mass encryption in the backup telemetry.

```bash
python3 - <<'EOF'
history = [
  {"day":"Mon","changed_gb":50, "dedup_ratio":8.2,"deleted_files":120},
  {"day":"Tue","changed_gb":48, "dedup_ratio":8.1,"deleted_files":95},
  {"day":"Wed","changed_gb":52, "dedup_ratio":8.3,"deleted_files":110},
  {"day":"Thu","changed_gb":870,"dedup_ratio":1.1,"deleted_files":48000},   # <-- attack
]
base_change = sum(d["changed_gb"] for d in history[:3])/3
base_dedup  = sum(d["dedup_ratio"] for d in history[:3])/3
for d in history:
    signals = []
    if d["changed_gb"] > base_change*3:   signals.append(f"change rate {d['changed_gb']/base_change:.0f}x baseline")
    if d["dedup_ratio"] < base_dedup*0.4: signals.append(f"dedup COLLAPSED {base_dedup:.1f}->{d['dedup_ratio']:.1f} (data now random = encrypted)")
    if d["deleted_files"] > 10000:        signals.append(f"mass deletion ({d['deleted_files']} files)")
    print(f"{d['day']}: {'ALERT — ' + '; '.join(signals) if signals else 'normal'}")
print("\nLast known-clean recovery point: WEDNESDAY. Restoring Thursday would restore the encryption.")
EOF
```

**Expected result:** Thursday triggers three simultaneous signals, and the **deduplication collapse is the most diagnostic** — ransomware-encrypted data is statistically random and therefore does not deduplicate, so the ratio falls off a cliff. The closing line is the operational payoff: the telemetry identifies Wednesday as the last clean point, which is the single most valuable fact during a ransomware response.

**Negative test:** Alerting only on job failures — the Thursday backup **succeeded**. It faithfully protected encrypted garbage, and a success-only monitoring posture sees nothing wrong at all.

**Cleanup:** None.

### Lab 6.3 — Threat Scan and clean recovery-point selection

**Objective:** Choose a recovery point verified as clean.

```bash
python3 - <<'EOF'
recovery_points = [
  {"date":"2026-07-28","threat_scan":"clean",     "anomaly":False},
  {"date":"2026-07-29","threat_scan":"clean",     "anomaly":False},
  {"date":"2026-07-30","threat_scan":"suspicious","anomaly":False},   # dormant payload present
  {"date":"2026-07-31","threat_scan":"infected",  "anomaly":True},
  {"date":"2026-08-01","threat_scan":"infected",  "anomaly":True},
]
clean = [rp for rp in recovery_points if rp["threat_scan"] == "clean"]
for rp in recovery_points:
    mark = {"clean":"OK      ","suspicious":"WARN    ","infected":"INFECTED"}[rp["threat_scan"]]
    print(f"{rp['date']}  scan={mark} anomaly={rp['anomaly']}")
best = clean[-1]
print(f"\nLatest CLEAN recovery point: {best['date']}")
print("Note 30 Jul is 'suspicious' though no behavioral anomaly fired — the payload was present but")
print("not yet detonated. Content inspection catches what behavior analysis alone would miss.")
EOF
```

**Expected result:** The latest clean point is 29 July, not 30 July — and the reasoning matters. On 30 July the behavioral signals were still normal because the ransomware had not yet encrypted anything, but **content inspection found the dormant payload**. Recovering to 30 July would restore the malware and re-trigger the incident. This is the argument for Threat Scan alongside anomaly detection: they catch different phases of the same attack.

**Negative test:** Choosing the most recent backup that "completed successfully and showed no anomaly" — that is 30 July, and it reinfects you.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Immutability enforced at the storage layer, tested against an admin-level attacker.
- [ ] Air gap (physical and logical) and credential separation understood.
- [ ] Ransomware detected from change rate, dedup collapse, and mass deletion.
- [ ] Threat Scan used to select a genuinely clean recovery point.
