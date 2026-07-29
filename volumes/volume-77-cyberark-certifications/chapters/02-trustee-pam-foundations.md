# Chapter 02: Trustee — PAM Foundations and Platform Components

## Learning Objectives

- Explain privileged access and why PAM matters.
- Describe the CyberArk PAM Self-Hosted components.
- Understand the Vault, CPM, PVWA, PSM, and PTA roles.
- Apply core PAM principles (least privilege, rotation, isolation).
- Complete a walkthrough for each Trustee foundation topic.

## Theory and Architecture

The **Trustee** level establishes the foundation. **Privileged access** is any access with elevated
rights — domain admins, root, service accounts, application secrets — the keys attackers seek because
they grant control. **Privileged Access Management (PAM)** reduces this risk by **vaulting**
credentials, **rotating** them automatically, **isolating and recording** privileged sessions, and
**detecting** anomalous use. CyberArk PAM Self-Hosted realizes this with components: the **Digital
Vault** (a hardened, encrypted store — the heart of the system), the **Central Policy Manager (CPM)**
(rotates and manages passwords per policy), the **Password Vault Web Access (PVWA)** (the web UI and
REST API), the **Privileged Session Manager (PSM)** (proxies privileged sessions so credentials never
reach the endpoint, and records them), and **Privileged Threat Analytics (PTA)** (detects and
responds to anomalous privileged activity). The core principles — **least privilege, credential
rotation, session isolation, and monitoring** — recur across every chapter. This chapter teaches each
with a hands-on defensive walkthrough (component roles and PAM logic).

## Design Considerations

Protect the **Vault** above all (it holds everything). Rotate credentials with the **CPM** on a
policy. Force privileged access through **PSM** so passwords never touch endpoints. Monitor with
**PTA**. Apply **least privilege** everywhere. Understand each component's role before deploying.

## Implementation and Automation

The labs map components, reason about rotation and isolation, and apply least privilege.

## Validation and Troubleshooting

Confirm the foundation:

```text
PAM protects privileged accounts (admin/root/service/secrets). Components: Vault (encrypted store), CPM (rotation),
PVWA (UI/API), PSM (session isolation + recording), PTA (threat analytics). Principles: least privilege, rotation, isolation, monitoring.
```

Common pitfalls: exposing privileged passwords to endpoints (use **PSM**); and never rotating shared
accounts (use **CPM**).

## Security and Best Practices

Vault the credentials, **rotate** with CPM, **isolate/record** with PSM, **monitor** with PTA, and
enforce **least privilege**. Never store privileged passwords in scripts or spreadsheets. All work is
defensive.

## Hands-On Lab

Foundation walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 2.1 — Map the PAM components

**Objective:** Learn each component's role.

```python
python3 - <<'PY'
components={"Vault":"hardened encrypted store of credentials/secrets",
            "CPM":"rotates & manages passwords per policy",
            "PVWA":"web UI + REST API for users/admins",
            "PSM":"proxies + records privileged sessions (credentials never reach endpoint)",
            "PTA":"detects/responds to anomalous privileged activity"}
for c,role in components.items(): print(f"{c:5}: {role}")
PY
```

**Expected result:** the **five core components** and their roles — the Trustee foundation.

**Negative test:** treat CyberArk as just a password vault; **CPM/PSM/PTA** add rotation, isolation,
and detection — it's a full PAM system.

**Cleanup:** none.

### Lab 2.2 — Reason about credential rotation

**Objective:** Understand why rotation matters.

```python
python3 - <<'PY'
import datetime
account={"name":"svc-sql","last_rotated":"2026-05-01","policy_days":30}
last=datetime.date.fromisoformat(account["last_rotated"]); today=datetime.date(2026,7,28)
overdue=(today-last).days > account["policy_days"]
print(f"{account['name']}: last rotated {account['last_rotated']}, policy {account['policy_days']}d -> {'ROTATE NOW (overdue)' if overdue else 'ok'}")
print("CPM: automatic rotation limits the value of a stolen credential")
PY
```

**Expected result:** the overdue service account flagged **ROTATE NOW** — the value of CPM rotation.

**Negative test:** keep a static service-account password for years; a leak stays valid indefinitely —
**rotate** on policy.

**Cleanup:** none.

### Lab 2.3 — Reason about session isolation

**Objective:** Keep credentials off endpoints.

```python
python3 - <<'PY'
def connect(via_psm):
    if via_psm:
        return "PSM proxies the session; credential injected server-side; session recorded"
    return "credential exposed on the admin's workstation (risk: keylogger/theft)"
print("via PSM:   ", connect(True))
print("direct:    ", connect(False))
PY
```

**Expected result:** the PSM path keeps the **credential off the endpoint** and records the session —
session isolation.

**Negative test:** let admins RDP directly with a vaulted password copied to the clipboard; it can be
stolen — connect **through PSM**.

**Cleanup:** none.

### Lab 2.4 — Apply least privilege

**Objective:** Grant only what's needed.

```python
python3 - <<'PY'
request={"user":"ops1","needs":"restart the web service","asked_for":"domain admin"}
right_grant="local service-restart permission (or JIT elevation), NOT domain admin"
print(f"{request['user']} needs to {request['needs']} but asked for {request['asked_for']}")
print("least privilege ->", right_grant)
PY
```

**Expected result:** the over-broad **domain admin** request reduced to a **scoped** grant — least
privilege.

**Negative test:** grant domain admin for a service restart; that's massive over-privilege — grant
the **minimum** (or just-in-time).

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Trustee foundation covers privileged access and the CyberArk PAM components — Vault, CPM, PVWA,
PSM, PTA — and the core principles of least privilege, rotation, isolation, and monitoring that every
later chapter applies.

- [ ] I can map the PAM components.
- [ ] I can explain credential rotation (CPM).
- [ ] I can explain session isolation (PSM).
- [ ] I can apply least privilege.
- [ ] I completed Labs 2.1–2.4 including each negative test.
