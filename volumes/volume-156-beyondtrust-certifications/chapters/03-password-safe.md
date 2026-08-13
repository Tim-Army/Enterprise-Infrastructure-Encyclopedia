# Chapter 03: Password Safe — Vaulting, Rotation, and Sessions

## Learning Objectives

- Explain credential vaulting and why credentials must never be exposed.
- Describe automatic rotation and check-in/check-out.
- Understand privileged session management — isolation, recording, monitoring.
- Recognize Password Safe as the credential-security core of PAM.

*Cert relevance: Password Safe is a Certified Administrator product — the credential vault and session manager at the heart of BeyondTrust PAM.*

## Credential vaulting

**Password Safe** is BeyondTrust's **privileged credential vault** and **session manager**. Its first job is **vaulting**: privileged credentials (admin passwords, SSH keys, service-account secrets, API keys) are stored **encrypted in the vault**, never scattered in scripts, spreadsheets, or config files, and — crucially — **never exposed to the user.** When an administrator needs privileged access, Password Safe **retrieves the credential and uses it on the user's behalf** (or injects it into the session), so the human never sees or holds the actual password. You cannot steal, phish, or reuse a credential you never possessed. The lab models vaulting.

## Rotation and check-in/check-out

Vaulting is paired with **automatic rotation**: Password Safe **changes privileged passwords automatically** — on a schedule, and after each use. Combined with **check-out / check-in**, a credential is checked out for a task, used, then **rotated on check-in** so its value is immediately dead. This means a credential's useful lifetime to an attacker is **near zero**: even if one leaked, it would already be rotated. Shared static admin passwords — the ones that live for years and appear in a dozen scripts — are exactly what rotation eliminates. The lab models rotation.

## Privileged session management

Password Safe also provides **privileged session management (PSM)**: when a privileged session runs, it is **brokered** through Password Safe, which can **isolate** the session (the target is never directly exposed to the user's machine), **record** it (a full audit trail of what the administrator did), and **monitor** it live (with the ability to terminate a suspicious session). This turns privileged access from an untracked, trust-based activity into a **controlled, recorded, accountable** one — essential for both security and compliance (who did what, when, on which system). The lab models session management.

## Password Safe as the PAM core

Vaulting + rotation + session management together are the **credential-security core** of PAM: secrets are hidden from users, short-lived, and every privileged session is accountable. This is the discipline [CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md) also centers on — the two PAM leaders both anchor on the vault. The lab synthesizes.

## Hands-On Lab

Python models vaulting, rotation, and session control. **Cost:** none.

### Lab 3.1 — Vaulting and rotation shrink the credential lifetime

**Objective:** See how vaulting + rotation make a stolen credential worthless.

```bash
python3 - <<'EOF'
import hashlib, time
# a privileged credential managed by Password Safe: vaulted, injected, rotated on check-in
class PasswordSafe:
    def __init__(self):
        self._secret = self._rotate()          # current vaulted value (never shown to users)
        self.checked_out = False
    def _rotate(self):
        return "PW-" + hashlib.sha1(str(time.time_ns()).encode()).hexdigest()[:12]
    def checkout_and_use(self):
        self.checked_out = True
        # user NEVER receives the secret; Password Safe injects it into the session
        used = self._secret
        return f"session opened (credential injected, user never saw it)"
    def checkin(self):
        stolen = self._secret                  # pretend an attacker grabbed it during use
        self._secret = self._rotate()          # rotate on check-in
        self.checked_out = False
        return stolen
ps = PasswordSafe()
print("Password Safe: vault + inject + rotate-on-check-in\n")
print("  ", ps.checkout_and_use())
stolen = ps.checkin()
print(f"   attacker somehow captured the in-use credential: {stolen}")
print(f"   current vaulted credential after check-in:        {ps._secret}")
print(f"   stolen == current? {stolen == ps._secret}  -> the stolen one is ALREADY DEAD\n")
print("Two properties make the theft worthless:")
print("  1. VAULTING + INJECTION: the user never HOLDS the credential -> nothing to phish,")
print("     paste in a script, or reuse. It's used on their behalf.")
print("  2. ROTATION on check-in: even a captured value is changed immediately, so its")
print("     useful lifetime is ~zero. Static shared admin passwords (living for years in")
print("     a dozen scripts) are exactly what this eliminates.")
EOF
```

**Expected result:** A credential injected into a session (never held by the user) and rotated on check-in, so a value captured during use no longer matches the current vaulted credential — it is already dead. The Password Safe lesson is that vaulting plus injection means the user never holds the secret (nothing to phish or reuse) and rotation collapses a credential's useful lifetime to near zero, eliminating the static shared admin passwords that live for years.

**Negative test:** Storing privileged passwords in a shared spreadsheet or script, even encrypted at rest. If a human ever holds the plaintext, it can be phished, pasted, and reused; vaulting with injection plus rotation is what removes the exposure.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Session management makes privileged access accountable

**Objective:** See isolation, recording, and monitoring.

```bash
python3 - <<'EOF'
# a brokered privileged session through Password Safe PSM
session = {
    "user": "alice", "target": "db-prod-01", "credential": "(injected, hidden)",
    "isolated": True,      # target never directly exposed to alice's laptop
    "recorded": True,      # full keystroke/screen audit trail
    "monitored": True,     # live, can be terminated
}
commands = ["SELECT count(*) FROM orders", "SHOW TABLES",
            "DROP TABLE audit_log   <-- suspicious!"]
print(f"Privileged session: {session['user']} -> {session['target']}")
print(f"   isolated={session['isolated']}  recorded={session['recorded']}  monitored={session['monitored']}\n")
print("   session audit trail:")
for c in commands:
    flag = "  *** ALERT: destructive on audit table — monitor can TERMINATE"  if "DROP TABLE audit" in c else ""
    print(f"      {c}{flag}")
print("\nPrivileged Session Management turns admin access from untracked trust into a")
print("CONTROLLED, RECORDED, ACCOUNTABLE activity:")
print("  ISOLATION  — the target is brokered; alice's laptop never touches it directly,")
print("               so malware on her endpoint can't ride the session.")
print("  RECORDING  — a full audit trail: who did what, when, on which system.")
print("  MONITORING — live oversight; a suspicious command (dropping the audit log!) can")
print("               be caught and the session terminated in real time.")
print("This is the accountability half of PAM — essential for security AND compliance.")
EOF
```

**Expected result:** A brokered session that is isolated (target never directly exposed), recorded (full audit trail), and monitored (a destructive command flagged for live termination). The session-management lesson is that PSM turns privileged access from untracked trust into a controlled, recorded, accountable activity — isolation stops endpoint malware riding the session, recording answers who-did-what, and monitoring catches abuse in real time.

**Negative test:** Letting administrators connect directly to production with a vaulted password and no session brokering. You lose isolation, the audit trail, and live oversight — the accountability that PAM (and every auditor) requires.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Vaulting understood — credentials stored encrypted and never exposed to users.
- [ ] Rotation and check-in/check-out understood — a stolen credential is short-lived to worthless.
- [ ] Privileged session management understood — isolation, recording, live monitoring.
- [ ] Password Safe recognized as the credential-security core of PAM, the peer of CyberArk's vault.
