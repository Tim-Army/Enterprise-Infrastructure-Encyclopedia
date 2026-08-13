# Chapter 08: Security Best Practices, RBAC, and Identity Resilience

## Learning Objectives

- Cover Rubrik's own security posture: RBAC, MFA, and least privilege for the platform.
- Understand identity resilience — protecting and recovering the identity systems attackers target.
- Model role-based access and an identity-recovery scenario.

## Securing the last line of defense

If the backup is the last line of defense, **the backup platform itself is a top target** — an attacker who controls it can delete recovery points or exfiltrate the data it holds. Rubrik's security best practices harden the platform: **role-based access control (RBAC)** with least privilege, **multi-factor authentication**, and separation of duties (so no single stolen credential can both disable protection and delete backups — reinforced by the immutability/retention-lock of [Chapter 03](03-immutability-and-air-gap.md)).

Rubrik also protects **identity itself** — the newer "**and Identity**" in "Cyber Resilience Platform for Data and Identity": Active Directory and Entra ID are the crown jewels attackers compromise to move laterally, and recovering a clean directory after an attack is its own discipline.

## Hands-On Lab

Python models RBAC and identity recovery. **Cost:** none.

### Lab 8.1 — Role-based access with least privilege

**Objective:** Scope platform access so no one role can do everything.

```bash
python3 - <<'EOF'
# Separation of duties on the backup platform itself
roles = {
  "backup-operator":   {"take_snapshot", "view_compliance", "run_recovery"},
  "security-analyst":  {"view_threat_analytics", "hunt", "view_dspm"},
  "admin":             {"manage_sla", "manage_users", "take_snapshot", "view_compliance"},
  # NOTE: no single role can BOTH manage retention AND delete backups; deletion is retention-locked (Ch 03)
}
def can(role, action):
    return "ALLOW" if action in roles.get(role, set()) else "DENY (not in role)"
print("backup-operator run_recovery:", can("backup-operator", "run_recovery"))
print("backup-operator manage_users:", can("backup-operator", "manage_users"))
print("security-analyst delete_snapshot:", can("security-analyst", "delete_snapshot"))
print("\nLeast privilege + separation of duties: a stolen operator credential can't reconfigure or delete.")
EOF
```

**Expected result:** Each role is scoped — the operator can recover but not manage users, the analyst can hunt but not delete snapshots, and **no role can early-delete backups** (retention-locked). RBAC with least privilege and separation of duties means a single compromised credential can't both disable protection and destroy recovery points. Securing the platform is part of RCSA-level operation.

**Negative test:** One all-powerful admin account used by everyone — its theft hands the attacker the ability to delete every backup; RBAC + separation of duties + immutable retention is the defense in depth that prevents it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — MFA and access hardening

**Objective:** Model the access controls that protect the backup platform.

```bash
python3 - <<'EOF'
def access(user_authed, mfa, from_network, privileged_action):
    if not user_authed: return "DENY (auth)"
    if privileged_action and not mfa: return "DENY (privileged action requires MFA)"
    if from_network == "untrusted" and not mfa: return "DENY (MFA required off-network)"
    return "ALLOW"
print("recover, MFA on:      ", access(True, True,  "corp",      True))
print("delete-config, no MFA:", access(True, False, "corp",      True))
print("login from internet:  ", access(True, False, "untrusted", False))
EOF
```

**Expected result:** MFA is enforced for privileged actions and off-network access — the access hardening that keeps stolen passwords from reaching the backup platform's dangerous operations. Combined with RBAC and immutability, this is the layered protection of the recovery data itself.

**Negative test:** Password-only access to the backup console — credential theft (phishing) then grants platform control; MFA on privileged/off-network access is a baseline the security best practices require.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Identity resilience: recover a clean directory

**Objective:** Model recovering identity (AD/Entra) after compromise — the "and Identity" pillar.

```bash
python3 - <<'EOF'
# After an attacker adds backdoor accounts / group memberships, recover a KNOWN-CLEAN directory state
clean_snapshot = {"admins": {"alice"}, "accounts": {"alice","bob","carol"}}
compromised    = {"admins": {"alice","attacker_svc"}, "accounts": {"alice","bob","carol","attacker_svc","backdoor1"}}
# Diff shows what the attacker changed:
added_admins   = compromised["admins"]   - clean_snapshot["admins"]
added_accounts = compromised["accounts"] - clean_snapshot["accounts"]
print(f"attacker-added admins:   {added_admins}")
print(f"attacker-added accounts: {added_accounts}")
print("Identity recovery: restore the clean directory state (or surgically remove the additions),")
print("re-establishing a trustworthy identity fabric so lateral movement is cut off.")
EOF
```

**Expected result:** The diff reveals the attacker's backdoor admin and accounts; identity recovery restores the **clean directory state**, cutting off the persistence and lateral-movement paths an attacker built. Recovering data without recovering identity leaves the attacker's foothold in AD/Entra intact — which is why Rubrik added identity resilience: **you must recover the identity fabric, not just the file server.**

**Negative test:** Restoring only the application/file data after a breach while leaving compromised AD untouched — the attacker's backdoor accounts persist and re-compromise the restored systems; identity recovery is the missing half of a complete cyber recovery.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] RBAC with least privilege and separation of duties on the platform drilled.
- [ ] MFA/access hardening for the backup console modeled.
- [ ] Identity resilience (recover a clean AD/Entra state) understood as the "and Identity" pillar.
