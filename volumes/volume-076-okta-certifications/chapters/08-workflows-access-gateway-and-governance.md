# Chapter 08: Workflows, Access Gateway, and Identity Governance

## Learning Objectives

- Automate identity tasks with Okta Workflows (no-code).
- Extend SSO to on-prem apps with Access Gateway.
- Govern access with Okta Identity Governance (OIG).
- Run access requests and certifications.
- Complete a walkthrough for each specialty topic.

## Theory and Architecture

Three specialties extend the core platform. **Okta Workflows** is a **no-code automation** engine —
event-driven flows (triggers, logic, and connector cards) that automate identity tasks without
custom code (e.g., "when a user joins the Contractors group, set an expiry date and notify their
manager"). **Access Gateway (OAG)** extends Okta SSO and policy to **on-prem, header-based, and
legacy web applications** that can't use modern federation, acting as a reverse proxy that injects
identity. **Okta Identity Governance (OIG)** adds **governance**: **access requests** (self-service
with approval workflows), **access certifications** (periodic reviews where managers attest to who
should keep access), and **separation-of-duties** policies — answering the audit questions *who has
access, why, and should they still*. Together they automate, extend, and govern identity beyond
day-one SSO. This chapter teaches each with a hands-on defensive walkthrough (a Workflow, an OAG
policy, and a certification campaign).

## Design Considerations

Automate repetitive identity tasks with **Workflows** (least code, most auditability). Use **Access
Gateway** for apps that can't federate, not as a default. Run **access certifications** on a cadence
and **least-privilege access requests** with approvals. Enforce **separation of duties**. Keep
governance evidence for audit.

## Implementation and Automation

The labs build a Workflow, gate an on-prem app, and run a certification.

## Validation and Troubleshooting

Confirm the specialty map:

```text
Workflows = no-code event-driven automation (triggers + logic + connectors). Access Gateway = SSO/policy for on-prem/header/legacy apps (reverse proxy).
Okta Identity Governance (OIG) = access requests (self-service + approval), access certifications (periodic review), separation of duties.
```

Common pitfalls: scripting what **Workflows** does natively (harder to audit); and **never reviewing**
access (privilege creep).

## Security and Best Practices

Automate with **Workflows**, extend legacy apps via **Access Gateway**, and govern with **OIG**
(requests, certifications, SoD) on a cadence. Keep audit evidence. All work is defensive.

## Hands-On Lab

Specialty walkthroughs. **Shared prerequisites** — `python3`, a developer org. **Cost:** none.

### Lab 8.1 — Build an automation Workflow

**Objective:** No-code lifecycle automation.

```python
python3 - <<'PY'
def workflow(event):
    # trigger: user added to "Contractors"
    if event["group"]=="Contractors":
        return {"set_attribute":{"accountExpires":"+90d"},"notify":event["manager"]}
    return {}
print(workflow({"group":"Contractors","manager":"ben@ex.com"}))
print("Workflows: event -> logic -> actions (set expiry + notify), no custom code")
PY
```

**Expected result:** the flow sets a **90-day expiry** and notifies the manager — Workflows
automation.

**Negative test:** onboard contractors with no expiry; accounts linger forever — automate an
**expiry** with Workflows.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Gate an on-prem app with Access Gateway

**Objective:** SSO for a legacy app.

```python
python3 - <<'PY'
request={"app":"legacy-hr (header-based)","user":"amy@ex.com","okta_session":True,"group":"HR"}
def oag(req):
    if not req["okta_session"]: return "redirect to Okta login"
    if req["group"]!="HR": return "403 (not authorized)"
    return f"inject headers (user={req['user']}) -> app grants access"
print(oag(request))
print("Access Gateway: enforce Okta auth + policy, then inject identity headers to the legacy app")
PY
```

**Expected result:** an authenticated HR user gets **identity headers injected** into the legacy app
— Access Gateway SSO.

**Negative test:** expose the legacy app directly without OAG; it has no modern auth — front it with
**Access Gateway**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Run an access certification (OIG)

**Objective:** Review who should keep access.

```python
python3 - <<'PY'
access=[{"user":"amy@ex.com","app":"NetSuite","last_used":"2d ago"},
        {"user":"dan@ex.com","app":"NetSuite","last_used":"400d ago"}]
for a in access:
    decision="REVOKE (stale)" if "400d" in a["last_used"] else "CERTIFY (in use)"
    print(f"{a['user']:14} {a['app']:10} last_used {a['last_used']:9} -> {decision}")
print("OIG certification: managers attest; revoke stale access (least privilege over time)")
PY
```

**Expected result:** stale access **revoked** and active access **certified** — an OIG certification
campaign.

**Negative test:** never review access; users accumulate entitlements (privilege creep) — run
**periodic certifications**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Enforce separation of duties

**Objective:** Prevent toxic combinations.

```python
python3 - <<'PY'
sod=[("Create Vendor","Approve Payment")]   # one person must not hold both
user_entitlements={"Create Vendor","Submit Invoice"}
requested="Approve Payment"
conflict=any(a in user_entitlements and b==requested or b in user_entitlements and a==requested for a,b in sod)
print("request:",requested,"-> ", "DENY (SoD conflict)" if conflict else "allow")
PY
```

**Expected result:** granting **Approve Payment** to someone who can **Create Vendor** is **denied** —
separation-of-duties enforcement.

**Negative test:** ignore SoD; one user can create and pay a fake vendor (fraud) — enforce **SoD**
policies.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The specialties extend the platform: Workflows automate identity tasks no-code, Access Gateway brings
SSO to on-prem/legacy apps, and Identity Governance adds access requests, certifications, and
separation of duties — automate, extend, and govern.

- [ ] I can build an automation Workflow.
- [ ] I can gate an on-prem app with Access Gateway.
- [ ] I can run an access certification (OIG).
- [ ] I can enforce separation of duties.
- [ ] I completed Labs 8.1–8.4 including each negative test.
