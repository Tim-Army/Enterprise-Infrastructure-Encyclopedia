# Chapter 08: Identity and Secure Cloud Access

## Learning Objectives

- Describe CyberArk Identity (workforce and customer).
- Apply SSO, adaptive MFA, and identity lifecycle in an Identity Security context.
- Understand Secure Cloud Access and zero standing privileges.
- Apply just-in-time access to cloud entitlements.
- Complete a walkthrough for each Identity/cloud topic.

## Theory and Architecture

Beyond the Vault, CyberArk's **Identity Security** vision unifies human and machine access. **CyberArk
Identity** provides **workforce and customer identity** — single sign-on, **adaptive MFA**, and
**identity lifecycle** — as the front door that authenticates users before they reach privileged
resources, tightly integrated with PAM (an admin authenticates via Identity, then accesses privileged
targets via the Vault/PSM). **Secure Cloud Access** targets a modern problem: **standing cloud
entitlements** — permanent IAM roles and permissions in AWS/Azure/GCP that attackers love. It applies
**just-in-time (JIT)** access and **zero standing privileges (ZSP)**: users have **no** standing
access to cloud resources, requesting **time-boxed elevation** only when needed, which is granted and
then revoked automatically. This shrinks the cloud attack surface from "always privileged" to
"privileged only during an approved task." Together, Identity and Secure Cloud Access extend PAM's
principles — strong authentication and least standing privilege — across users and cloud. This chapter
teaches each with a hands-on defensive walkthrough (adaptive access, JIT cloud elevation, and ZSP).

## Design Considerations

Front privileged access with **strong authentication** (adaptive MFA) via Identity. Integrate Identity
with **PAM** so the same user is governed end to end. Eliminate **standing cloud entitlements** with
**JIT/ZSP**. Time-box and audit every cloud elevation. Apply least privilege to cloud roles.

## Implementation and Automation

The labs apply adaptive access, grant JIT cloud access, and enforce ZSP.

## Validation and Troubleshooting

Confirm the Identity/cloud model:

```text
CyberArk Identity = workforce/customer SSO + adaptive MFA + lifecycle (front door to privileged access, integrated with PAM).
Secure Cloud Access = JIT + zero standing privileges (ZSP) for cloud entitlements: no standing access, time-boxed elevation, auto-revoke.
```

Common pitfalls: **standing** cloud admin roles (permanent targets); and Identity and PAM as
**disconnected** silos.

## Security and Best Practices

Authenticate with **adaptive MFA**, integrate Identity with **PAM**, and eliminate standing cloud
access via **JIT/ZSP** with time-boxing and audit. Least privilege on cloud roles. All work is
defensive.

## Hands-On Lab

Identity/cloud walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 8.1 — Apply adaptive access before privilege

**Objective:** Strong authentication as the front door.

```python
python3 - <<'PY'
def gate(ctx):
    if ctx["target"]=="privileged":
        if ctx["risk"]=="high": return "require FIDO2 + manager approval"
        return "require MFA"
    return "password + session"
print(gate({"target":"privileged","risk":"high"}))
print(gate({"target":"privileged","risk":"low"}))
print("Identity: adaptive MFA gates access BEFORE the Vault/PSM grants the credential")
PY
```

**Expected result:** privileged access gated by **adaptive MFA** (stronger when risky) — Identity as
the front door.

**Negative test:** let privileged access rely on password alone; credential theft = full compromise —
require **adaptive MFA**.

**Cleanup:** none.

### Lab 8.2 — Grant just-in-time cloud access

**Objective:** Time-boxed cloud elevation.

```python
python3 - <<'PY'
grant={"user":"cloudops","role":"AWS/PowerUser","reason":"deploy fix","ttl_min":30,"approved":True}
print("JIT cloud grant:", grant)
print("-> role assumed for 30 min, then AUTO-REVOKED (no standing access)")
PY
```

**Expected result:** a **time-boxed** cloud role grant that auto-revokes — Secure Cloud Access JIT.

**Negative test:** assign the PowerUser role permanently; it's a standing target — grant **JIT** and
revoke.

**Cleanup:** none.

### Lab 8.3 — Enforce zero standing privileges

**Objective:** No permanent cloud access.

```python
python3 - <<'PY'
users=[{"name":"cloudops","standing_roles":[],"jit_capable":True},
       {"name":"legacy-admin","standing_roles":["AWS/Administrator"],"jit_capable":False}]
for u in users:
    status="ZSP compliant" if not u["standing_roles"] else f"VIOLATION: standing {u['standing_roles']}"
    print(f"{u['name']:14}: {status}")
print("ZSP: convert standing roles to JIT so no one holds permanent cloud privilege")
PY
```

**Expected result:** the JIT user **ZSP-compliant** and the standing-admin flagged as a **violation** —
zero standing privileges.

**Negative test:** keep a break-glass account with permanent Administrator; secure and monitor it, but
**default to ZSP** for everyone else.

**Cleanup:** none.

### Lab 8.4 — Audit a cloud elevation

**Objective:** Evidence for every grant.

```python
python3 - <<'PY'
audit=[{"user":"cloudops","role":"AWS/PowerUser","granted":"10:00","revoked":"10:30","reason":"deploy fix"}]
for a in audit: print(a)
print("Secure Cloud Access: every JIT grant is logged (who/what/when/why) for audit")
PY
```

**Expected result:** a full **audit record** of the JIT grant — accountability for cloud access.

**Negative test:** grant cloud access with no reason or record; audits fail — **log** who/what/when/why.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CyberArk Identity provides adaptive-MFA authentication integrated with PAM, and Secure Cloud Access
eliminates standing cloud entitlements through just-in-time, zero-standing-privilege access with
time-boxing and audit — extending PAM principles across users and cloud.

- [ ] I can apply adaptive access before privilege.
- [ ] I can grant just-in-time cloud access.
- [ ] I can enforce zero standing privileges.
- [ ] I can audit a cloud elevation.
- [ ] I completed Labs 8.1–8.4 including each negative test.
