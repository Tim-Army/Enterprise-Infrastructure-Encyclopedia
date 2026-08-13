# Chapter 04: Defender — Session Management and Threat Detection

## Learning Objectives

- Configure privileged session isolation and recording (PSM).
- Apply just-in-time and session-control policies.
- Detect anomalous privileged activity (PTA).
- Respond to privileged threats automatically.
- Complete a walkthrough for each session/threat topic.

## Theory and Architecture

The second **Defender** domain covers **session management** and **threat detection**. The
**Privileged Session Manager (PSM)** proxies privileged connections so the credential is **injected
server-side** (never exposed to the user or endpoint), the session is **isolated** (a jump point
between user and target), and it is **recorded** for audit and investigation. Session policies can
**restrict** what commands or actions are allowed and require **just-in-time** access (elevate only
when needed, for a limited time). **Privileged Threat Analytics (PTA)** watches privileged behavior —
logins at unusual times, from unusual locations, bypass attempts, or credential theft indicators —
and can **respond automatically** (alert, suspend a session, rotate a compromised credential). Together
they ensure privileged sessions are **controlled, recorded, and monitored**, turning the Vault from a
password store into an active defense. This chapter teaches each with a hands-on defensive walkthrough
(isolation logic, session policy, and threat response).

## Design Considerations

Force privileged access through **PSM** (isolation + recording). Prefer **just-in-time**, time-boxed
access over standing privilege. **Record** sessions for high-risk targets. Tune **PTA** to real
anomalies and define **automatic responses** (suspend/rotate) for high-confidence threats. Protect the
recordings.

## Implementation and Automation

The labs isolate a session, apply JIT, and respond to a PTA detection.

## Validation and Troubleshooting

Confirm the session/threat model:

```text
PSM: proxy privileged sessions -> credential injected server-side (never on endpoint) + isolation + recording. Session policies restrict actions.
JIT: elevate only when needed, time-boxed. PTA: detect anomalies (time/location/bypass/theft) -> respond (alert/suspend/rotate).
```

Common pitfalls: allowing **direct** privileged connections that bypass PSM; and collecting PTA
alerts with **no automated response**.

## Security and Best Practices

Route privileged access through **PSM**, prefer **just-in-time**, **record** high-risk sessions, and
give **PTA** automatic responses for high-confidence threats. Protect recordings. All work is
defensive.

## Hands-On Lab

Session/threat walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 4.1 — Isolate and record a session

**Objective:** Keep credentials off the endpoint.

```python
python3 - <<'PY'
session={"user":"ops1","target":"win-sql01","via":"PSM"}
result={"credential_exposure":"none (injected by PSM server-side)","recording":"enabled",
        "isolation":"user never touches the target credential"}
for k,v in result.items(): print(f"{k:20}: {v}")
print("PSM: isolated + recorded privileged session")
PY
```

**Expected result:** an **isolated, recorded** session with no credential exposure — PSM in action.

**Negative test:** let the user retrieve the password and connect directly; no isolation or recording
— route through **PSM**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Apply just-in-time access

**Objective:** Eliminate standing privilege.

```python
python3 - <<'PY'
import datetime
grant={"user":"ops1","target":"win-sql01","granted_at":"14:00","ttl_minutes":60}
now="14:45"
def active(grant,now):
    g=datetime.datetime.strptime(grant["granted_at"],"%H:%M"); n=datetime.datetime.strptime(now,"%H:%M")
    return (n-g).seconds/60 <= grant["ttl_minutes"]
print(f"access at {now}:", "ACTIVE" if active(grant,now) else "EXPIRED")
print("JIT: access auto-expires after the TTL -> no standing privilege")
PY
```

**Expected result:** the JIT grant **active within the TTL** and auto-expiring after — just-in-time
access.

**Negative test:** grant standing (permanent) admin instead; it's a persistent target — use
**time-boxed JIT**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Detect and respond to a threat (PTA)

**Objective:** Act on anomalous privileged use.

```python
python3 - <<'PY'
event={"user":"svc-backup","action":"interactive login","time":"03:12","location":"new country","baseline":"batch only, business hours"}
risk = event["action"]=="interactive login" and event["time"]<"06:00"
print("PTA event:", event)
print("verdict:", "HIGH RISK -> alert + suspend session + rotate credential" if risk else "normal")
PY
```

**Expected result:** the off-hours interactive login by a batch account flagged **HIGH RISK** with
automatic response — PTA detection.

**Negative test:** log the anomaly with no response; the attacker continues — configure **automatic
response** (suspend/rotate).

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Restrict privileged actions

**Objective:** Limit what a session can do.

```python
python3 - <<'PY'
policy={"allow":["restart service","view logs"],"deny":["disable auditing","add domain admin"]}
for action in ["restart service","add domain admin"]:
    print(f"{action:18} ->", "allow" if action in policy["allow"] else "DENY (session policy)")
PY
```

**Expected result:** the benign action allowed and the dangerous one **denied** — session-level action
control.

**Negative test:** allow any command in a privileged session; a compromised session does maximum
damage — **restrict** actions.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Defender session/threat domain isolates and records privileged sessions with PSM, enforces
just-in-time time-boxed access, restricts privileged actions, and uses PTA to detect and
automatically respond to anomalous privileged behavior.

- [ ] I can isolate and record a session (PSM).
- [ ] I can apply just-in-time access.
- [ ] I can detect and respond to a threat (PTA).
- [ ] I can restrict privileged actions.
- [ ] I completed Labs 4.1–4.4 including each negative test.
