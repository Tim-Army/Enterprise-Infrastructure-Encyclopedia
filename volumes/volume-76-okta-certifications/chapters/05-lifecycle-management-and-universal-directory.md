# Chapter 05: Lifecycle Management and Universal Directory

## Learning Objectives

- Model profiles and attributes in Universal Directory.
- Integrate directories (AD/LDAP) and sources of truth.
- Automate provisioning and deprovisioning with Lifecycle Management.
- Use SCIM for downstream app provisioning.
- Complete a walkthrough for each LCM/UD topic.

## Theory and Architecture

**Universal Directory (UD)** is Okta's flexible profile store: each user has a **profile** with
**attributes**, and Okta maps attributes between **profile sources** (an authoritative directory or
HR system), the **Okta user profile**, and **application profiles**. Enterprises integrate on-prem
**Active Directory / LDAP** via the Okta **agent**, and increasingly use an **HR system as the source
of truth** (joiner-mover-leaver events flow into Okta). **Lifecycle Management (LCM)** automates the
identity lifecycle: when a user is **created/activated** they are provisioned into the right apps;
when their attributes **change** (department move) their access updates; when they are
**deactivated** they are **deprovisioned** everywhere — closing the biggest access-risk gap
(orphaned accounts). Downstream provisioning uses **SCIM** (System for Cross-domain Identity
Management), the standard API apps expose to receive create/update/deactivate events. This chapter
teaches each with a hands-on defensive walkthrough (attribute mapping, source-of-truth logic,
lifecycle automation, and SCIM events).

## Design Considerations

Pick one **source of truth** (HR or AD) and map attributes **from** it. Automate **deprovisioning** —
it's the top audit finding. Use **SCIM** for downstream apps where available. Map the **minimum**
attributes each app needs. Handle **mover** events (transfers) as carefully as joiners/leavers.

## Implementation and Automation

The labs map attributes, model source-of-truth, automate lifecycle, and emit SCIM events.

## Validation and Troubleshooting

Confirm the LCM/UD model:

```text
Universal Directory: profile sources -> Okta user profile -> app profiles (attribute mapping). AD/LDAP via agent; HR as source of truth.
Lifecycle Management: create->provision, change->update, deactivate->deprovision (kills orphaned accounts). Downstream = SCIM.
```

Common pitfalls: manual **deprovisioning** (orphaned accounts persist); and two systems both claiming
to be the **source of truth** (attribute fights).

## Security and Best Practices

One **source of truth**, automated **deprovisioning**, **SCIM** for downstream apps, and least
attribute mapping. Audit for orphaned accounts. Handle transfers correctly. All work is defensive.

## Hands-On Lab

LCM/UD walkthroughs. **Shared prerequisites** — `python3`, a developer org. **Cost:** none.

### Lab 5.1 — Map attributes from a source of truth

**Objective:** Establish authoritative attributes.

```python
python3 - <<'PY'
hr={"email":"amy@ex.com","department":"Finance","manager":"ben@ex.com","status":"active"}
# UD mapping: HR (source) -> Okta profile
okta_profile={"login":hr["email"],"department":hr["department"],"manager":hr["manager"]}
print("Okta profile (mapped from HR source of truth):", okta_profile)
print("UD: attributes flow FROM the source of truth, not edited ad hoc in Okta")
PY
```

**Expected result:** an Okta profile **mapped from HR** — a single authoritative source (UD).

**Negative test:** hand-edit department in Okta while HR also sets it; the next sync **overwrites**
your edit — change it at the **source**.

**Cleanup:** none.

### Lab 5.2 — Automate provisioning on create

**Objective:** Grant access automatically.

```python
python3 - <<'PY'
def onboard(user):
    groups=["Everyone"]
    if user["department"]=="Finance": groups.append("Finance")
    apps={"Finance":["NetSuite","Concur"],"Everyone":["Okta Dashboard","Email"]}
    provisioned=[a for g in groups for a in apps.get(g,[])]
    return groups,provisioned
g,p=onboard({"email":"amy@ex.com","department":"Finance"})
print("groups:",g,"\nprovisioned apps:",p)
print("LCM: create -> group rules -> automatic app provisioning")
PY
```

**Expected result:** a new Finance user **auto-provisioned** into the right groups and apps — LCM
onboarding.

**Negative test:** provision access manually per hire; it's slow and error-prone — **automate** via
group rules.

**Cleanup:** none.

### Lab 5.3 — Deprovision on deactivate

**Objective:** Close the access gap.

```python
python3 - <<'PY'
user={"email":"amy@ex.com","status":"deactivated","apps":["NetSuite","Concur","Okta Dashboard"]}
if user["status"]=="deactivated":
    revoked=user["apps"]; user["apps"]=[]
    print(f"deprovisioned {user['email']} from:", revoked)
print("LCM: deactivate -> revoke ALL app access + sessions (no orphaned accounts)")
PY
```

**Expected result:** a deactivated user **deprovisioned everywhere** — the biggest access-risk gap
closed.

**Negative test:** deactivate in Okta but leave downstream app accounts; those **orphans** remain
exploitable — deprovision **downstream** too (SCIM).

**Cleanup:** none.

### Lab 5.4 — Emit a SCIM event

**Objective:** Propagate lifecycle downstream.

```python
python3 - <<'PY'
import json
scim_deactivate={"schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
                 "id":"00u123","active":False}   # SCIM PATCH/PUT to the downstream app
print(json.dumps(scim_deactivate,indent=2))
print("SCIM: standard API so the downstream app deactivates the account automatically")
PY
```

**Expected result:** a **SCIM** deactivation payload (`active:false`) — standard downstream
provisioning.

**Negative test:** rely on the app admin to manually disable leavers; it lags and gets missed — use
**SCIM** automation.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Universal Directory maps attributes from an authoritative source, and Lifecycle Management automates
provisioning, updates, and — critically — deprovisioning via SCIM, closing the orphaned-account gap.

- [ ] I can map attributes from a source of truth (UD).
- [ ] I can automate provisioning on create (LCM).
- [ ] I can deprovision on deactivate.
- [ ] I can emit a SCIM event downstream.
- [ ] I completed Labs 5.1–5.4 including each negative test.
