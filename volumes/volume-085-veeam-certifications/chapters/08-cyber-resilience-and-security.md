# Chapter 08: Cyber Resilience and Security (VMCSE)

## Learning Objectives

- Explain the VMCSE and Zero Trust Data Resilience (ZTDR).
- Enforce backup immutability with a hardened repository or object lock.
- Detect malware and ransomware with inline scanning and the Threat Center.
- Run the Security and Compliance Analyzer and reason about four-eyes authorization.
- Complete a walkthrough for each cyber-resilience topic.

## Theory and Architecture

The new **VMCSE (Veeam Certified Security Expert)**, arriving Q2 2026, requires a valid **VMCE+** plus
the **Veeam Data Platform: Enterprise Data Security** training. It is entirely **defensive** — protecting
and recovering **your own** data against attack. Its pillars, all built into the Veeam Data Platform:

- **Immutability** — a **hardened Linux repository** (immutable flags, single-use credentials, no root)
  or **object-lock/immutable Vault** so backups cannot be altered or deleted before retention expires.
- **Zero Trust Data Resilience (ZTDR)** — Veeam's model applying zero-trust principles to backup:
  segmenting backup software from storage, least privilege, and immutable, verified copies.
- **Malware and ransomware detection** — **inline entropy/anomaly scanning** during backup, guest
  indexing signatures, and **YARA** rule scanning to find known threats and suspicious change.
- **Veeam Threat Center** — a dashboard scoring backup health, immutability coverage, and threats.
- **Security and Compliance Analyzer (SCA)** — checks the environment against security best practices
  and highlights misconfigurations.
- **Four-eyes authorization**, **MFA**, and **RBAC** — requiring a second approver for destructive
  actions and hardening administrative access.

This chapter teaches cyber resilience with hands-on walkthroughs — all defensive.

## Design Considerations

Make at least one copy **immutable** (hardened repo or object lock/Vault) and follow **ZTDR** by
separating backup roles and applying least privilege. Turn on **inline malware detection** and schedule
**YARA**/SCA scans. Watch the **Threat Center** for immutability gaps and anomalies. Require **four-eyes**
approval for delete/retention changes, and enforce **MFA** on the console. These protect recoverability
even when production is compromised.

## Implementation and Automation

The labs reason about ZTDR, verify repository immutability, model malware detection and the Threat
Center, and run the Security and Compliance Analyzer — the defensive controls VMCSE validates.

## Validation and Troubleshooting

Confirm cyber resilience:

```text
Immutability: hardened Linux repo (immutable flags, single-use creds) / object lock / Vault
ZTDR: separate backup software from storage + least privilege + immutable verified copies
Detection: inline entropy/anomaly scan + guest signatures + YARA rules -> Threat Center
Hardening: Security & Compliance Analyzer + four-eyes authorization + MFA + RBAC
```

Common pitfalls: backups with **no immutable copy** (ransomware deletes them); and admin accounts with
no **MFA/four-eyes** (a compromised admin can delete backups).

## Security and Best Practices

Everything here is **defensive**: immutability, ransomware **detection**, compliance analysis, and
four-eyes control protect and recover **your own** data. There is no offensive content. Keep an
immutable offsite copy, require multiple approvers for destructive actions, and monitor the Threat
Center. All work is authorized.

## Hands-On Lab

Cyber-resilience walkthroughs. **Shared prerequisites** — a Veeam Backup & Replication Community/Premium
environment (concepts modeled in `python3` where GUI-only); the Veeam PowerShell module. **Cost:** none.

### Lab 8.1 — Reason about Zero Trust Data Resilience

**Objective:** Apply zero trust to backup.

```python
python3 - <<'PY'
ztdr = [
  "Segment backup software from backup storage (separate trust zones)",
  "Least privilege: single-use repo credentials; no shared admin",
  "Immutable, verified backups (object lock / hardened repo)",
  "Assume breach: an attacker with prod access must NOT reach backups",
]
for i, principle in enumerate(ztdr, 1):
    print(f"ZTDR {i}: {principle}")
print("Goal: backups survive and stay recoverable even if production is compromised")
PY
```

**Expected result:** the ZTDR principles — segmentation, least privilege, immutability, assume-breach.

**Negative test:** run backups on the same domain/admin as production; a domain compromise reaches the
backups — segment and apply least privilege.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Verify repository immutability

**Objective:** Confirm backups cannot be deleted early.

```powershell
PS> Get-VBRBackupRepository -Name "Hardened-01" | Select-Object Name, Type, IsImmutabilityEnabled, ImmutabilityPeriod

Name         Type       IsImmutabilityEnabled ImmutabilityPeriod
----         ----       --------------------- ------------------
Hardened-01  LinuxLocal True                  14
```

**Expected result:** a hardened repository with immutability enabled for 14 days — early deletion is
blocked.

**Negative test:** store the only backup on a mutable share an admin can delete; ransomware or an
insider erases it — use a **hardened/immutable** repository.

**Rollback:** none (immutability is the protected state).

### Lab 8.3 — Detect malware and read the Threat Center

**Objective:** Catch ransomware early.

```python
python3 - <<'PY'
scan = {
  "inline_entropy": "high on app-vm01 last night (possible encryption)",
  "yara_match":     "rule 'ransom_note' hit in restore point 2026-07-28 22:10",
  "suspicious_change": "98% of files changed in 1 hour (mass encryption pattern)",
}
for signal, detail in scan.items():
    print(f"{signal:18}: {detail}")
print("Threat Center: flag app-vm01, quarantine the point, recover from the last CLEAN restore point")
PY
```

**Expected result:** entropy, YARA, and mass-change signals flagged — the Threat Center points recovery
at the last clean point.

**Negative test:** restore blindly from the newest backup after an attack; it may be encrypted —
recover from the last **clean** point the detection identifies.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Run the Security and Compliance Analyzer

**Objective:** Harden the configuration.

```python
python3 - <<'PY'
checks = {
  "Immutable backups configured":  "PASS",
  "MFA enabled on console":        "PASS",
  "Four-eyes authorization on delete": "FAIL -> enable second-approver",
  "Backup traffic encrypted":      "PASS",
  "Hardened repo (no root SSH)":   "PASS",
}
for check, result in checks.items():
    print(f"{check:36}: {result}")
print("SCA: remediate FAIL items (enable four-eyes) to harden against insider/attacker deletion")
PY
```

**Expected result:** an SCA report with a failed **four-eyes** check to remediate — configuration
hardened.

**Negative test:** allow a single admin to delete backups unchecked; enable **four-eyes authorization**
so destructive actions need a second approver.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The VMCSE is defensive cyber resilience across the Veeam Data Platform: immutable backups (hardened
repository, object lock, Vault) under Zero Trust Data Resilience, inline malware and ransomware detection
with YARA and the Threat Center, the Security and Compliance Analyzer, and four-eyes/MFA/RBAC hardening —
all protecting and recovering your own data.

- [ ] I can explain the VMCSE and Zero Trust Data Resilience.
- [ ] I can verify repository immutability.
- [ ] I can detect malware and read the Threat Center.
- [ ] I can run the Security and Compliance Analyzer.
- [ ] I completed Labs 8.1–8.4 including each negative test.
