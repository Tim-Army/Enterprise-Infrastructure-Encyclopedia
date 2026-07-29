# Chapter 06: Privilege Cloud and Endpoint Privilege Manager

## Learning Objectives

- Describe Privilege Cloud (SaaS PAM) and its architecture.
- Deploy connectors for cloud-managed privileged access.
- Enforce endpoint least privilege with EPM.
- Apply application control and privilege elevation policies.
- Complete a walkthrough for each Privilege Cloud/EPM topic.

## Theory and Architecture

Two products extend PAM beyond the self-hosted Vault. **Privilege Cloud** is CyberArk's **SaaS PAM** —
the Vault, CPM, PVWA, and PSM capabilities delivered and operated as a service, with lightweight
**connectors** installed in the customer environment to reach targets. It reduces operational burden
while providing the same vaulting, rotation, isolation, and monitoring. **Endpoint Privilege Manager
(EPM)** addresses a different risk: **local administrator rights** on endpoints. Instead of users
running as local admin (a huge attack surface), EPM **removes standing admin rights** and grants
**just-in-time privilege elevation** for specific approved applications or actions, backed by
**application control** (allow/block/restrict) and **credential-theft protection**. Together they
deliver **cloud-delivered PAM** and **endpoint least privilege** — closing two of the most common
privilege-abuse paths. This chapter teaches each with a hands-on defensive walkthrough (connector
model, elevation policy, and application control).

## Design Considerations

Use **Privilege Cloud** to offload PAM operations while keeping targets reachable via **connectors**.
Remove **local admin** rights and grant **elevation per application/action** with EPM. Prefer
**allow-listing** for application control. Log elevations for audit. Balance security with user
productivity (approved elevations, not blanket admin).

## Implementation and Automation

The labs model the connector, build an elevation policy, and apply application control.

## Validation and Troubleshooting

Confirm the Privilege Cloud/EPM model:

```text
Privilege Cloud = SaaS PAM (Vault/CPM/PVWA/PSM as a service) + connectors to reach targets. EPM = remove local admin + JIT privilege elevation per app/action + application control (allow/block/restrict) + credential-theft protection.
```

Common pitfalls: leaving users as **local admin** "for convenience" (huge surface); and **block-listing**
instead of allow-listing applications.

## Security and Best Practices

Offload with **Privilege Cloud** connectors, **remove local admin** and elevate per app/action with
EPM, prefer **allow-listing**, and log elevations. Keep users productive with approved elevations. All
work is defensive.

## Hands-On Lab

Privilege Cloud/EPM walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 6.1 — Model the Privilege Cloud connector

**Objective:** Understand SaaS PAM reach.

```python
python3 - <<'PY'
model={"vault/cpm/pvwa/psm":"operated by CyberArk (SaaS)","connector":"lightweight, in customer network",
       "reaches":"on-prem + cloud targets via the connector","benefit":"less ops overhead, same controls"}
for k,v in model.items(): print(f"{k:22}: {v}")
PY
```

**Expected result:** the SaaS-plus-**connector** model — how Privilege Cloud reaches targets.

**Negative test:** expect Privilege Cloud to reach internal targets with no **connector**; it can't —
deploy connectors.

**Cleanup:** none.

### Lab 6.2 — Build an EPM elevation policy

**Objective:** Remove admin, elevate per app.

```python
python3 - <<'PY'
user={"local_admin":False}   # standing admin removed
elevation_rules={"install approved software (signed by IT)":"elevate (JIT)",
                 "run diagnostic tool":"elevate (JIT)","modify security settings":"deny"}
for action,decision in elevation_rules.items(): print(f"{action:34}: {decision}")
print("EPM: no standing admin; elevate only specific approved actions")
PY
```

**Expected result:** standing admin removed with **per-action JIT elevation** — endpoint least
privilege.

**Negative test:** leave users as local admin so "everything works"; malware inherits admin — **remove**
it and elevate selectively.

**Cleanup:** none.

### Lab 6.3 — Apply application control (allow-list)

**Objective:** Control what can run.

```python
python3 - <<'PY'
def decide(app):
    allow={"signed corporate app","approved browser","IT diagnostic tool"}
    block={"unknown.exe","macro-enabled downloader"}
    if app in allow: return "allow"
    if app in block: return "block"
    return "restrict (run with reduced rights / prompt)"
for app in ["signed corporate app","unknown.exe","new-tool.exe"]:
    print(f"{app:24} -> {decide(app)}")
PY
```

**Expected result:** known-good allowed, known-bad blocked, unknown **restricted** — EPM application
control.

**Negative test:** rely only on a **block-list**; new malware isn't on it — prefer **allow-listing**
with restrict-by-default.

**Cleanup:** none.

### Lab 6.4 — Audit privilege elevations

**Objective:** Keep evidence.

```python
python3 - <<'PY'
elevations=[{"user":"amy","app":"IT diagnostic tool","result":"elevated","ts":"10:02"},
            {"user":"ben","app":"unknown.exe","result":"blocked","ts":"10:05"}]
for e in elevations: print(f"{e['ts']} {e['user']:4} {e['app']:20} -> {e['result']}")
print("EPM: log every elevation/block for audit and hunting")
PY
```

**Expected result:** an **audit trail** of elevations and blocks — EPM accountability.

**Negative test:** elevate with no logging; you can't investigate abuse — **log** every elevation.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Privilege Cloud delivers PAM as a service via connectors, and EPM removes standing local admin in
favor of just-in-time, per-application elevation with allow-list application control and audited
elevations — cloud-delivered PAM and endpoint least privilege.

- [ ] I can model the Privilege Cloud connector.
- [ ] I can build an EPM elevation policy.
- [ ] I can apply application control.
- [ ] I can audit privilege elevations.
- [ ] I completed Labs 6.1–6.4 including each negative test.
