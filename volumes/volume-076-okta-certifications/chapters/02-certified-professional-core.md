# Chapter 02: Certified Professional — Core Okta

## Learning Objectives

- Navigate the Okta org and admin console.
- Manage users and groups in Universal Directory.
- Configure a basic single sign-on integration.
- Apply core security settings.
- Complete a walkthrough for each Certified Professional topic.

## Theory and Architecture

The **Okta Certified Professional** validates core platform skills — the foundation for every other
credential. It centers on the **Okta org** (a tenant), managed through the **Admin Console**, and the
**Universal Directory** — Okta's cloud identity store holding **users** (people) and **groups**
(collections used to assign access). Core tasks: creating and activating users, organizing them into
groups, assigning applications, configuring a basic **single sign-on (SSO)** integration from the
**OIN (Okta Integration Network)** app catalog, and applying baseline security (password policy,
basic MFA enrollment). The mental model is: **directory (who) → groups (how access is grouped) →
applications (what) → policies (rules)**. This chapter teaches each with a hands-on defensive
walkthrough, using Okta concepts and the API where it clarifies (all against a free developer org).

## Design Considerations

Model access with **groups**, not per-user assignments, for scale and auditability. Keep the
**directory** authoritative and clean. Assign apps to **groups**. Apply a baseline **password and MFA
policy** from day one. Use the **OIN** catalog for known apps rather than hand-building integrations.

## Implementation and Automation

The labs model users/groups, assign an app, and apply baseline security.

## Validation and Troubleshooting

Confirm the core model:

```text
Org (tenant) -> Admin Console. Universal Directory = users + groups. Assign apps to groups. OIN = app catalog.
Model: directory (who) -> groups (access grouping) -> apps (what) -> policies (rules). Baseline: password + MFA.
```

Common pitfalls: assigning apps **per user** (unmanageable at scale); and skipping a baseline **MFA**
policy.

## Security and Best Practices

Group-based access, a clean authoritative **directory**, **baseline MFA/password** policy, and OIN
integrations. Least privilege on admin roles. Practice on a **developer org**. All work is defensive.

## Hands-On Lab

Core walkthroughs. **Shared prerequisites** — `python3` and a free Okta developer org, in a lab.
**Cost:** none.

### Lab 2.1 — Model users and groups

**Objective:** Group-based access.

```python
python3 - <<'PY'
users=[{"login":"amy@ex.com","dept":"Finance"},{"login":"ben@ex.com","dept":"Sales"},
       {"login":"cara@ex.com","dept":"Finance"}]
groups={}
for u in users: groups.setdefault(u["dept"],[]).append(u["login"])
for g,members in groups.items(): print(f"group {g}: {members}")
print("Okta: assign apps to GROUPS (Finance/Sales), not individuals")
PY
```

**Expected result:** users organized into **department groups** — the group-based access model.

**Negative test:** assign an app to each user directly; onboarding/offboarding becomes manual —
assign to **groups**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Assign an application to a group

**Objective:** Connect access to groups.

```python
python3 - <<'PY'
assignment={"app":"Salesforce (OIN SAML)","assigned_to_group":"Sales","sso":"SAML 2.0"}
for k,v in assignment.items(): print(f"{k:20}: {v}")
print("New Sales hires added to the group -> instant app access; leavers removed -> access revoked")
PY
```

**Expected result:** an app assigned to the **Sales group** via SSO — access that follows group
membership.

**Negative test:** grant the app to individuals; a new hire has no access until manually added — use
**group assignment**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Apply a baseline MFA enrollment policy

**Objective:** Require a second factor.

```python
python3 - <<'PY'
policy={"name":"Baseline MFA","applies_to":"Everyone","require_factor":"Okta Verify or FIDO2",
        "enroll":"on first sign-in"}
for k,v in policy.items(): print(f"{k:14}: {v}")
print("Certified Professional: baseline MFA enrollment protects every account")
PY
```

**Expected result:** a baseline **MFA** enrollment policy for everyone — core security.

**Negative test:** rely on passwords alone; credential theft = account takeover — require **MFA**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Verify a user's effective access

**Objective:** Trace who can reach what.

```python
python3 - <<'PY'
user="amy@ex.com"; user_groups=["Finance"]
app_assignments={"NetSuite":"Finance","Salesforce":"Sales","Okta Dashboard":"Everyone"}
effective=[app for app,grp in app_assignments.items() if grp in user_groups or grp=="Everyone"]
print(f"{user} effective apps:", effective)
print("Trace access via group membership -> app assignment (auditability)")
PY
```

**Expected result:** the user's **effective apps** derived from group membership — access
traceability.

**Negative test:** guess access from memory; **group→app** mapping is the source of truth — trace it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Certified Professional core covers the Okta org, Universal Directory (users/groups), group-based
app assignment via the OIN, and baseline MFA — the directory→groups→apps→policies model every later
credential builds on.

- [ ] I can model users and groups.
- [ ] I can assign an app to a group.
- [ ] I can apply a baseline MFA policy.
- [ ] I can trace a user's effective access.
- [ ] I completed Labs 2.1–2.4 including each negative test.
