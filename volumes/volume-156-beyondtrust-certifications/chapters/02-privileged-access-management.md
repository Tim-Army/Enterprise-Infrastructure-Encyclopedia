# Chapter 02: Privileged Access Management — The Discipline

## Learning Objectives

- Explain what privileged access is and why it is the primary attack path.
- Describe the core PAM controls — vaulting, least privilege, session management, JIT.
- Understand least privilege and just-in-time access as the goal.
- Place PAM in the identity-security landscape.

*Cert relevance: PAM is the discipline every BeyondTrust product implements — the frame for the whole program.*

## Why privileged access is the attack path

A **privileged account** — a domain administrator, a root user, a cloud admin role, a service account — can do things ordinary users cannot: change configurations, access all data, create accounts, disable security controls. That power makes privileged accounts the **primary target** in a breach. The attack pattern is consistent:

1. **Compromise** an initial account (phishing, a vulnerability).
2. **Escalate** to a privileged account (steal admin credentials, exploit a misconfiguration).
3. **Move laterally** using that privilege, reaching more systems.
4. **Act** — exfiltrate data, deploy ransomware, establish persistence.

Nearly every major breach involves **privileged credential abuse** somewhere in the chain. PAM exists to break it — to make privileged credentials hard to steal, privileged sessions hard to hijack, and standing privilege rare. The lab models the attack path and where PAM controls sit.

## The core PAM controls

PAM is a set of interlocking controls, each of which a BeyondTrust product implements:

| Control | What it does | Product |
|:---|:---|:---|
| **Credential vaulting** | Store privileged credentials in a vault; never expose them to users | [Password Safe (Ch 3)](03-password-safe.md) |
| **Rotation** | Change credentials automatically and often, so a stolen one is short-lived | Password Safe |
| **Session management** | Broker, isolate, record, and monitor privileged sessions | Password Safe, [PRA (Ch 5)](05-privileged-remote-access.md) |
| **Least privilege** | Remove standing admin rights; grant only what's needed, when needed | [EPM (Ch 4)](04-endpoint-privilege-management.md) |
| **Just-in-time (JIT)** | Grant privilege only for the moment it's needed, then revoke | [Entitle (Ch 8)](08-entitle.md) |

The unifying idea is to **eliminate standing privilege** — the always-on admin rights and shared passwords that attackers rely on — and replace it with **brokered, monitored, time-bounded** access.

## Least privilege and JIT: the goal

The north star is **least privilege**: every identity has exactly the access it needs to do its job, and no more. Its dynamic form is **just-in-time (JIT)** access: rather than granting standing privilege that sits idle (and exploitable) most of the time, grant it **only when needed**, for **only as long as needed**, then revoke. Standing privilege is attack surface with no benefit when unused — the same insight the [runtime-entitlement chapters of Sysdig (CLV)](../../volume-155-sysdig-certifications/chapters/07-posture-permissions-and-compliance.md) and [Wiz (CXLVII)](../../volume-147-wiz-certifications/README.md) apply to cloud permissions. PAM applies it to the most dangerous access of all. The lab models least privilege.

## PAM in the identity landscape

PAM is one pillar of **identity security**, alongside:

- **Access management / SSO / MFA** — [Ping (CL)](../../volume-150-ping-identity-certifications/README.md), [Okta (LXXVI)](../../volume-076-okta-certifications/README.md) — *who* can log in.
- **Identity governance (IGA)** — [SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md) — *what* access identities *should* have, reviewed and certified.
- **PAM** — BeyondTrust, [CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md) — securing the *privileged* subset, the highest-risk access.

Identity is the modern security perimeter, and privileged identity is its most sensitive core. The lab situates PAM.

## Hands-On Lab

Python models the privilege attack path and PAM controls. **Cost:** none.

### Lab 2.1 — Where PAM breaks the attack chain

**Objective:** See how PAM controls interrupt privileged-credential abuse.

```bash
python3 - <<'EOF'
# the classic breach chain, and the PAM control that breaks each step
CHAIN = [
  ("1. Initial compromise", "phishing steals a standard user's login",
      "(identity: MFA/SSO — Ping/Okta — reduces this)"),
  ("2. Privilege escalation", "attacker grabs cached ADMIN credentials on the host",
      "EPM removes local admin rights -> no admin creds to steal"),
  ("3. Credential theft", "attacker finds a shared admin password in a script",
      "Password Safe VAULTS creds + ROTATES them -> the found one is dead"),
  ("4. Lateral movement", "attacker reuses admin creds to hop to other servers",
      "PRA brokers access + INJECTS creds (user never sees them) -> nothing to reuse"),
  ("5. Standing privilege", "a dormant admin role sat available for months",
      "JIT (Entitle) grants privilege only when needed, then REVOKES"),
]
print("The privileged-credential attack chain, and where PAM breaks it:\n")
for step, attack, control in CHAIN:
    print(f"   {step}")
    print(f"      attacker: {attack}")
    print(f"      PAM:      {control}\n")
print("The thesis: nearly every breach RUNS ON privileged credential abuse — escalate,")
print("steal, reuse, move. PAM breaks EACH link: remove standing admin (EPM), vault +")
print("rotate secrets (Password Safe), inject creds so users never hold them (PRA), and")
print("grant privilege just-in-time (Entitle). No single control is enough; TOGETHER they")
print("eliminate the standing, stealable, reusable privilege attackers depend on.")
EOF
```

**Expected result:** The five-step breach chain (compromise → escalate → steal → move → standing privilege) mapped to the PAM control that breaks each — EPM removing local admin, Password Safe vaulting and rotating, PRA injecting credentials, JIT revoking standing access. The PAM lesson is that privileged-credential abuse runs through nearly every breach and no single control suffices; the controls together eliminate the standing, stealable, reusable privilege attackers rely on.

**Negative test:** Relying on a strong perimeter and password complexity alone. Once an attacker is inside, standing privileged credentials are the vehicle; only vaulting, rotation, least privilege, and JIT remove that vehicle.

**Cleanup:** None.

### Lab 2.2 — Least privilege and just-in-time

**Objective:** Contrast standing privilege with JIT.

```bash
python3 - <<'EOF'
# an engineer needs admin on a server for a 30-minute maintenance window, once a month
HOURS_MONTH = 730
JIT_HOURS = 0.5   # granted only for the task
print("Engineer needs server-admin for ONE 30-min maintenance task per month.\n")
print("STANDING privilege (traditional):")
print(f"   admin granted 24/7 = {HOURS_MONTH} hours/month of exploitable privilege")
print(f"   actually USED: {JIT_HOURS} hours -> {HOURS_MONTH-JIT_HOURS:.1f} hours of PURE attack surface\n")
print("JUST-IN-TIME privilege (PAM):")
print(f"   admin granted only for the task = {JIT_HOURS} hours/month")
exposure_cut = 100*(HOURS_MONTH-JIT_HOURS)/HOURS_MONTH
print(f"   exposure window cut by {exposure_cut:.2f}%")
print(f"   the rest of the month: the engineer has NO standing admin to steal or abuse\n")
print("Least privilege = exactly the access needed, no more. Its dynamic form, JIT, adds")
print("'...and only WHEN needed.' Standing privilege sits idle ~99.9% of the time as pure")
print("attack surface; JIT collapses the window to the task itself. Same 'remove what's")
print("granted-but-unused' logic as cloud CIEM (Sysdig CLV / Wiz CXLVII) — applied to the")
print("most dangerous access there is. Eliminating STANDING privilege is the PAM endgame.")
EOF
```

**Expected result:** A standing-admin exposure of 730 hours/month collapsing to 0.5 hours under JIT — a >99.9% cut in the exploitable window. The least-privilege lesson is that standing privilege is attack surface that sits idle almost all the time, and JIT collapses the exposure window to the task itself, applying the same remove-the-unused logic as cloud CIEM to the most dangerous access there is.

**Negative test:** Granting standing admin because "the engineer needs it sometimes." Sometimes is not always; JIT grants it for the task and revokes it after, removing the idle exposure that standing privilege leaves open.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Privileged access understood as the primary attack path — escalate, steal, move, act.
- [ ] The core PAM controls understood — vaulting, rotation, session management, least privilege, JIT.
- [ ] Least privilege and just-in-time understood as the goal — eliminating standing privilege.
- [ ] PAM placed in identity security alongside access management (Ping/Okta) and governance (SailPoint).
