# Chapter 03: Secret Server — The PAM Vault

## Learning Objectives

- Explain Secret Server as Delinea's credential vault.
- Describe secret policies, rule-based passwords, and rotation.
- Understand session monitoring, recording, and keystroke logging.
- Recognize Secret Server as the flagship of the portfolio.

*Cert relevance: Secret Server is the flagship product and the core of Associate and Engineer certifications.*

## What Secret Server is

**Secret Server** (from the Thycotic heritage) is Delinea's **privileged credential vault** — the flagship product and the core of the certifications. It stores privileged credentials ("secrets" — passwords, keys, service-account credentials, API keys) **encrypted in a vault**, controls who can access them, **rotates** them automatically, and **records** privileged sessions. Its reputation is for being **fast to deploy and easy to use** while covering the full vault feature set. As with every PAM vault, the first principle is that credentials are **never exposed** to users in a way they can steal or reuse — Secret Server retrieves and uses them on the user's behalf. The lab models vaulting.

## Secret policies and rule-based passwords

Secret Server manages credentials through **secret policies** and **rule-based passwords**:

- **Secret policies** define how a class of secrets behaves — how often to rotate, who may access, whether check-out is required, whether sessions are recorded — applied consistently to all secrets of that type rather than configured one by one.
- **Rule-based passwords** (password requirements/rules) generate strong, policy-compliant passwords automatically — length, complexity, character sets — so rotated credentials always meet security standards.
- **Email alerts** notify on relevant events (access, check-out, policy violations).

Policy-driven management is what makes a vault manageable at enterprise scale — thousands of secrets governed by a handful of policies. The lab models policies.

## Rotation and check-out

Secret Server **rotates** privileged passwords automatically — on a schedule and after use — and supports **check-out**: a user checks out a secret for a task, and it is **rotated on check-in**, so its value is immediately dead. Combined with vaulting, this collapses a credential's useful lifetime to an attacker toward **zero** and eliminates the static shared passwords that live for years in scripts and spreadsheets. This is the same rotation discipline PAM centers on across vendors ([BeyondTrust's Password Safe, CLVI](../../volume-156-beyondtrust-certifications/chapters/03-password-safe.md)). The lab models rotation.

## Session monitoring, recording, and keystroke logging

Secret Server provides **privileged session management**: privileged sessions launched through it can be **monitored** live, **recorded** (a full playback of what the administrator did), and subject to **keystroke logging** — every command captured. This turns privileged access into an **accountable, auditable** activity: you can prove who did what, when, on which system, and review a session after the fact for incident response or compliance. Session recording is essential both for security (detecting and investigating misuse) and for the audit requirements every regulated organization faces. The lab models session accountability.

## Hands-On Lab

Python models the vault, policies, and session recording. **Cost:** none.

### Lab 3.1 — Policy-driven vaulting, rotation, and session recording

**Objective:** See secret policies, rotation on check-in, and session accountability.

```bash
python3 - <<'EOF'
import hashlib, time
# a secret policy governing a class of credentials + rule-based password generation
POLICY = {"name": "domain-admins", "rotate_on_checkin": True, "require_checkout": True,
          "record_session": True, "pw_rules": "20 chars, upper+lower+digit+symbol"}
def rule_based_password():
    return "Rb!" + hashlib.sha1(str(time.time_ns()).encode()).hexdigest()[:17]  # policy-compliant, generated

class SecretServer:
    def __init__(self): self.secret = rule_based_password()
    def checkout_use_checkin(self):
        used = self.secret                    # injected on the user's behalf; user doesn't keep it
        if POLICY["rotate_on_checkin"]:
            self.secret = rule_based_password()  # rotate -> the used value is now dead
        return used

print(f"Secret policy '{POLICY['name']}':")
for k, v in POLICY.items():
    if k != "name": print(f"   {k:18}: {v}")
print()
ss = SecretServer()
used = ss.checkout_use_checkin()
print(f"   secret used during session : {used}")
print(f"   secret after check-in      : {ss.secret}")
print(f"   used value still valid?     {used == ss.secret}  -> rotated = DEAD\n")
print("   session (recorded per policy): keystroke log playback ->")
for cmd in ["sudo systemctl restart app", "cat /etc/hosts", "exit"]:
    print(f"      [rec] {cmd}")
print("\nSecret Server = the PAM VAULT: credentials stored encrypted + never held by users;")
print("SECRET POLICIES govern a whole class at once (rotation, check-out, recording); ★")
print("RULE-BASED PASSWORDS auto-generate strong policy-compliant values; ROTATION on check-in")
print("makes a used/stolen credential immediately dead; and SESSION RECORDING + KEYSTROKE")
print("LOGGING make every privileged session accountable + auditable. Policy-driven = manageable")
print("at scale (thousands of secrets, a few policies). The Thycotic-heritage flagship.")
EOF
```

**Expected result:** A `domain-admins` secret policy driving rule-based password generation, rotation on check-in (so the used value no longer matches — it is dead), and a recorded keystroke-logged session. The Secret Server lesson is that the vault governs credentials by policy (rotation, check-out, recording applied to a whole class), auto-generates strong rule-based passwords, collapses a credential's lifetime via rotation, and makes every privileged session accountable through recording and keystroke logging.

**Negative test:** Storing privileged passwords without policy, rotation, or session recording. Static shared secrets persist and are reusable, and privileged sessions are unaccountable; Secret Server's policies, rotation, and recording are what make the vault secure and auditable at scale.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Secret Server understood as Delinea's flagship credential vault (Thycotic heritage).
- [ ] Secret policies and rule-based passwords understood — policy-driven management at scale.
- [ ] Rotation and check-out understood — collapsing a credential's useful lifetime toward zero.
- [ ] Session monitoring, recording, and keystroke logging understood — accountable, auditable privileged access.
