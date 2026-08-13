# Chapter 05: Server PAM — Server Privilege and AD Bridging

## Learning Objectives

- Explain Server PAM and privilege elevation on servers (PEDM).
- Describe Active Directory bridging for Linux/Unix.
- Understand MFA and identity-centric access at the server.
- Recognize the Centrify heritage's server/infrastructure focus.

*Cert relevance: Server PAM (Centrify heritage) extends the certifications to server and infrastructure privilege.*

## What Server PAM is

**Server PAM** (from the Centrify heritage; also delivered as Cloud Suite / Privileged Access Service) secures **privileged access on servers** — Linux, Unix, and Windows. Where [Privilege Manager (Ch 4)](04-privilege-manager.md) handles endpoint least privilege for users' workstations, Server PAM handles the **server/infrastructure** side: controlling who can log into servers, elevating privilege on them **granularly**, and bridging server identity to **Active Directory**. It reflects Centrify's **identity-centric** approach — tying server access to a central identity rather than scattered local accounts. The lab models server privilege.

## Privilege elevation on servers (PEDM)

Server PAM provides **PEDM (Privilege Elevation and Delegation Management)** on servers — the server equivalent of endpoint least privilege. Instead of giving administrators full **root** (or blanket `sudo`), Server PAM grants **fine-grained, policy-based elevation**: a user may run *specific* privileged commands (via a controlled mechanism such as `dzdo`, Centrify's audited `sudo` replacement), logged and constrained, without holding root. This means:

- No shared root passwords, no blanket sudo.
- Every privileged command is **attributable** to an individual and **logged**.
- Least privilege on servers: exactly the commands needed, nothing more.

Granular server privilege elevation is essential in Linux/Unix estates where root is otherwise all-or-nothing. The lab models PEDM.

## Active Directory bridging

A signature Centrify capability is **Active Directory bridging** — extending **AD** authentication and policy to **Linux and Unix** servers, so they authenticate users against their **existing AD identity** (via Kerberos) rather than local accounts. This is the same consolidation the [BeyondTrust AD Bridge (CLVI, Ch 7)](../../volume-156-beyondtrust-certifications/chapters/07-ad-bridge.md) provides, integrated here into Server PAM: **one identity** per person across Windows and Linux/Unix, centrally governed, so disabling an AD account ends server access everywhere. AD bridging turns a sprawl of local server accounts into one governed identity per user. The lab models the consolidation.

## MFA and identity-centric access

Server PAM adds **multi-factor authentication (MFA) at the server** — requiring a second factor to log in or to elevate privilege, so a stolen password alone cannot grant server access or root. This is **identity-centric** security applied to infrastructure: access decisions are based on **verified identity** (plus MFA and policy), not on possession of a shared credential or network location. Bringing MFA and identity to the server — historically a weak point, where shared root passwords and password-only SSH were common — materially raises the bar against server compromise. The lab models identity-centric elevation.

## Hands-On Lab

Python models server PEDM, AD bridging, and MFA. **Cost:** none.

### Lab 5.1 — Granular server elevation with AD identity and MFA

**Objective:** See least privilege on servers replace shared root.

```bash
python3 - <<'EOF'
# Server PAM: AD-bridged identity + MFA + granular PEDM (specific commands, not blanket root)
USER = {"ad_identity": "alice@corp", "mfa_verified": True}
# policy: which privileged commands alice may run (dzdo-style), instead of full root
ALLOWED_CMDS = {"systemctl restart app", "tail -f /var/log/app.log"}
REQUESTED = ["systemctl restart app", "cat /etc/shadow", "tail -f /var/log/app.log"]

print(f"Server login: {USER['ad_identity']} (AD-bridged identity, not a local account)")
print(f"   MFA verified: {USER['mfa_verified']}  -> a stolen password alone is NOT enough\n")
print("Granular PEDM (dzdo-style) — each privileged command checked against policy:")
for cmd in REQUESTED:
    allowed = cmd in ALLOWED_CMDS
    tag = "ALLOWED + logged (attributable to alice)" if allowed else "DENIED (not in alice's least-privilege policy)"
    print(f"   dzdo {cmd:28} -> {tag}")
print("\nServer PAM (Centrify heritage) secures SERVER privilege three ways:")
print("  AD BRIDGING  — Linux/Unix servers auth against alice's EXISTING AD identity (Kerberos),")
print("     not scattered local accounts -> one governed identity; disable AD = access ends everywhere.")
print("  MFA          — a second factor at login/elevation -> a stolen password alone can't get root.")
print("  PEDM         — grant SPECIFIC privileged commands (dzdo), not blanket root/sudo; every")
print("     command is attributable + logged. No shared root password, least privilege on servers.")
print("Identity-centric security applied to infrastructure — the historically weak point where")
print("shared root passwords and password-only SSH lived.")
EOF
```

**Expected result:** Alice authenticating with her AD-bridged identity and MFA, then granular PEDM allowing her two policy-permitted commands (logged and attributable) while denying `cat /etc/shadow` — no blanket root. The Server PAM lesson is that it secures server privilege through AD bridging (one governed identity, not local accounts), MFA (a stolen password alone can't grant access), and PEDM (specific commands not blanket root, each attributable) — identity-centric least privilege on the infrastructure that historically relied on shared root.

**Negative test:** Managing servers with shared root passwords and password-only SSH. Access is unattributable, a leaked password grants everything, and identities sprawl as local accounts; Server PAM's AD-bridged identity, MFA, and granular PEDM replace that with least privilege and accountability.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Server PAM understood as securing privileged access on Linux/Unix/Windows servers (Centrify heritage).
- [ ] PEDM understood — granular, policy-based command elevation instead of blanket root/sudo.
- [ ] Active Directory bridging understood — extending AD identity to Linux/Unix for one governed identity.
- [ ] MFA and identity-centric access at the server recognized as raising the bar against server compromise.
