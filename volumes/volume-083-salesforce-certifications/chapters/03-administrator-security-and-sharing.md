# Chapter 03: Administrator — Security and Sharing

## Learning Objectives

- Control object and field access with profiles and permission sets.
- Design the record-sharing model (OWD, role hierarchy, sharing rules).
- Apply the principle of least privilege.
- Troubleshoot access issues.
- Complete a walkthrough for each security/sharing topic.

## Theory and Architecture

Salesforce security operates at two levels: **object/field access** (can a user see/edit this object
or field at all?) and **record access** (which specific records can they see?). Object and field
access come from **profiles** (a baseline set of permissions per user, one per user) and **permission
sets** (additive grants layered on top, so you can give extra access without changing profiles) — the
modern best practice is **lean profiles + permission sets**. Record access is governed by the
**sharing model**, evaluated in layers: **Org-Wide Defaults (OWD)** set the baseline (Private,
Public Read Only, Public Read/Write) — the most restrictive starting point; the **role hierarchy**
grants managers access to their subordinates' records (records roll **up**); **sharing rules** open
access laterally (e.g., share West-region records with the West team); and **manual/team sharing**
handles exceptions. The model is **restrictive by default, then selectively opened** — the opposite of
open-by-default. Understanding this layered model is central to the Administrator exam and to securing
data. This chapter teaches each with a hands-on walkthrough (permission logic and sharing evaluation).

## Design Considerations

Use **lean profiles + permission sets** (additive) for least privilege. Set **OWD to the most
restrictive** appropriate baseline, then open with **role hierarchy** and **sharing rules**. Avoid
broad "Modify All". Use **field-level security** for sensitive fields. Document the sharing model.
Troubleshoot access top-down (object → field → record).

## Implementation and Automation

The labs model profile/permission-set access and evaluate the sharing model.

## Validation and Troubleshooting

Confirm the security model:

```text
Object/field access: profiles (baseline, one per user) + permission sets (additive) + field-level security. Record access (sharing): OWD baseline (Private/Public RO/RW) -> role hierarchy (managers see subordinates' records) -> sharing rules (lateral) -> manual/team.
Model: restrictive by default, selectively opened. Best practice: lean profiles + permission sets.
```

Common pitfalls: fat **profiles** with everything (unmanageable — use **permission sets**); and setting
**OWD to Public Read/Write** then trying to restrict (start **restrictive**).

## Security and Best Practices

Least privilege with **lean profiles + permission sets**, **restrictive OWD** opened selectively, and
**field-level security** for sensitive data. Avoid "Modify All". Document and troubleshoot the sharing
model. All work is authorized administration.

## Hands-On Lab

Security/sharing walkthroughs. **Shared prerequisites** — `python3`, a free Dev org. **Cost:** none.

### Lab 3.1 — Model profiles and permission sets

**Objective:** Additive least privilege.

```python
python3 - <<'PY'
profile={"Standard User":{"Account":"read/edit","Report":"run"}}
perm_set={"Data Exporter":{"extra":"export reports"}}
def effective(user_profile, user_perm_sets):
    perms=dict(profile[user_profile])
    for ps in user_perm_sets: perms.update(perm_set[ps])
    return perms
print("amy (Standard User + Data Exporter):", effective("Standard User", ["Data Exporter"]))
print("Admin: lean profile + permission sets (additive) -> least privilege, easy to manage")
PY
```

**Expected result:** effective access = **profile baseline + permission-set grants** — additive least
privilege.

**Negative test:** clone the profile and add the export permission directly; profiles proliferate — use
a **permission set**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Evaluate the sharing model

**Objective:** Determine record access.

```python
python3 - <<'PY'
def can_see(owd, is_manager_of_owner, matched_sharing_rule):
    if owd in ("Public Read Only","Public Read/Write"): return True
    if is_manager_of_owner: return True          # role hierarchy
    if matched_sharing_rule: return True          # sharing rule
    return False                                  # Private + no grant
print("Private, not manager, no rule:", can_see("Private", False, False))
print("Private, manager of owner:", can_see("Private", True, False))
print("Private, matching sharing rule:", can_see("Private", False, True))
PY
```

**Expected result:** access granted only via **hierarchy or sharing rule** on top of a Private OWD —
the layered model.

**Negative test:** set OWD Private and expect a peer to see records with no rule; access is **denied**
— add a **sharing rule**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Open access with a sharing rule

**Objective:** Lateral access.

```python
python3 - <<'PY'
sharing_rule={"name":"West records to West team","criteria":"Region__c = 'West'",
              "share_with":"Role: Sales - West","access":"Read/Write"}
for k,v in sharing_rule.items(): print(f"{k:12}: {v}")
print("Sharing rule: opens Private records laterally to a group/role (beyond the hierarchy)")
PY
```

**Expected result:** a **sharing rule** granting a team lateral access — selective opening.

**Negative test:** lower **OWD to Public** to give the West team access; that over-shares to everyone —
use a targeted **sharing rule**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Troubleshoot an access issue

**Objective:** Diagnose top-down.

```python
python3 - <<'PY'
def diagnose(has_object_access, has_field_access, has_record_access):
    if not has_object_access: return "fix: object permission (profile/permission set)"
    if not has_field_access: return "fix: field-level security"
    if not has_record_access: return "fix: sharing (OWD/role/sharing rule)"
    return "access OK"
print(diagnose(False,True,True))
print(diagnose(True,True,False))
PY
```

**Expected result:** the access problem localized to **object → field → record** — systematic
troubleshooting.

**Negative test:** change the sharing model when the real issue is a missing **field-level** permission
— diagnose **top-down** first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Salesforce security combines object/field access (lean profiles + additive permission sets) with a
layered record-sharing model (restrictive OWD opened by role hierarchy and sharing rules) — least
privilege, restrictive by default, selectively opened.

- [ ] I can model profiles and permission sets.
- [ ] I can evaluate the sharing model.
- [ ] I can open access with a sharing rule.
- [ ] I can troubleshoot an access issue top-down.
- [ ] I completed Labs 3.1–3.4 including each negative test.
