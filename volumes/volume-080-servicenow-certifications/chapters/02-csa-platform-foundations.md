# Chapter 02: CSA — Platform Foundations

## Learning Objectives

- Explain the Now Platform data model (tables, records, fields).
- Work with forms, lists, and the UI.
- Manage users, groups, and roles.
- Understand table inheritance and the CMDB basis.
- Complete a walkthrough for each CSA foundation topic.

## Theory and Architecture

The **Certified System Administrator (CSA)** begins with the Now Platform's **data model**. Everything
in ServiceNow is a **record** in a **table**; tables have **fields** (columns), and records are the
rows. Tables can **extend** other tables (inheritance) — for example `incident` extends `task`, so it
inherits Task's fields plus its own. Users interact through **forms** (a single record) and **lists**
(many records), with the UI configured by administrators. **Access** is governed by **users**,
**groups** (collections of users), and **roles** (permissions assigned to groups/users) — the basis
for who can see and do what. The **Configuration Management Database (CMDB)** is a special set of
tables (`cmdb_ci` and its children) modeling infrastructure. Understanding tables, inheritance, the
form/list UI, and the user/group/role model is the foundation every ServiceNow task builds on. This
chapter teaches each with a hands-on walkthrough (data-model reasoning on a free PDI, modeled in
`python3` where it clarifies logic).

## Design Considerations

Model data with **table inheritance** (extend `task` for work items). Assign access through
**roles → groups → users**, never per-user permissions. Configure **forms/lists** for usability.
Keep the **CMDB** accurate — it underpins ITSM/ITOM. Use the **base system** where possible before
customizing.

## Implementation and Automation

The labs reason about tables/inheritance, the role model, and list/form configuration.

## Validation and Troubleshooting

Confirm the foundation:

```text
Everything = a record in a table; tables have fields; tables extend other tables (incident extends task). UI = forms (one record) + lists (many).
Access: users -> groups -> roles (permissions). CMDB = cmdb_ci tables modeling infrastructure. Base system before customization.
```

Common pitfalls: assigning **roles to individual users** (unmanageable); and heavy **customization**
before using the base configuration.

## Security and Best Practices

Use **table inheritance**, assign access via **roles/groups**, configure the UI thoughtfully, and keep
the **CMDB** accurate. Prefer base configuration. Practice on a **PDI**. All work is authorized
administration.

## Hands-On Lab

Foundation walkthroughs. **Shared prerequisites** — `python3`, and a free PDI. **Cost:** none.

### Lab 2.1 — Reason about table inheritance

**Objective:** Understand the data model.

```python
python3 - <<'PY'
tables={"task":["number","short_description","assigned_to","state"],
        "incident (extends task)":["+ caller_id","+ severity","+ category"],
        "change_request (extends task)":["+ risk","+ implementation_plan"]}
for t,fields in tables.items(): print(f"{t}: {fields}")
print("CSA: incident/change extend task -> inherit task fields + add their own")
PY
```

**Expected result:** `incident`/`change` **extending** `task` with inherited plus own fields — the
data model.

**Negative test:** build a standalone incident table duplicating task fields; **extend task** instead
— use inheritance.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Model the role-based access

**Objective:** Assign access correctly.

```python
python3 - <<'PY'
groups={"Service Desk":["itil"],"Change Managers":["itil","change_manager"]}
users={"amy":"Service Desk","ben":"Change Managers"}
def roles_of(user):
    return groups[users[user]]
print("amy roles:", roles_of("amy"))
print("ben roles:", roles_of("ben"))
print("CSA: roles -> groups -> users (never assign roles directly to individuals)")
PY
```

**Expected result:** users' roles derived via **group membership** — the role model.

**Negative test:** grant `itil` directly to each user; onboarding/offboarding breaks — assign via
**groups**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Configure a list view

**Objective:** Make records usable.

```python
python3 - <<'PY'
list_config={"table":"incident","columns":["number","short_description","priority","assigned_to","state"],
             "filter":"active=true AND assigned_to.groupIN(Service Desk)","sort":"priority ASC"}
for k,v in list_config.items(): print(f"{k:8}: {v}")
print("CSA: list views (columns + filter + sort) shape how admins/agents see records")
PY
```

**Expected result:** a **list view** (columns, filter, sort) — usable record presentation.

**Negative test:** show every field in the default list; it's unreadable — **configure** columns and
filters.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Trace a CMDB relationship

**Objective:** Understand the CMDB basis.

```python
python3 - <<'PY'
ci={"name":"APP-PAYMENTS","class":"cmdb_ci_appl","runs_on":"SRV-DB01","depends_on":["SRV-WEB01"]}
print("CI:", ci)
print("CSA/CMDB: CIs (cmdb_ci_*) + relationships (runs_on/depends_on) model the service topology")
PY
```

**Expected result:** a **configuration item** with relationships — the CMDB foundation for ITSM/ITOM.

**Negative test:** treat the CMDB as a flat asset list; **relationships** power impact analysis — model
them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CSA foundation covers the Now Platform data model (tables, inheritance, records/fields), the
form/list UI, the user/group/role access model, and the CMDB basis — the platform grounding every
other credential builds on.

- [ ] I can reason about table inheritance.
- [ ] I can model role-based access.
- [ ] I can configure a list view.
- [ ] I can trace a CMDB relationship.
- [ ] I completed Labs 2.1–2.4 including each negative test.
