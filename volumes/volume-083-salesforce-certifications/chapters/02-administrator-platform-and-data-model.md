# Chapter 02: Administrator — Platform and Data Model

## Learning Objectives

- Explain the Salesforce data model (objects, fields, records, relationships).
- Configure standard and custom objects.
- Design page layouts and record types.
- Set up the org and manage users.
- Complete a walkthrough for each Administrator foundation topic.

## Theory and Architecture

The **Administrator (ADM-201)** begins with the data model. Salesforce stores data in **objects** —
tables — of two kinds: **standard objects** (Account, Contact, Opportunity, Case) that come with the
CRM, and **custom objects** (suffixed `__c`) that admins create. Each object has **fields** (columns,
including custom `__c` fields of various types), and rows are **records**. Objects relate through
**relationships**: **lookup** (a loose reference) and **master-detail** (a tight parent-child where
the child depends on the parent and inherits sharing). The user interface is configured with **page
layouts** (which fields/related lists appear) and **record types** (variations of an object for
different business processes, each with its own layout and picklist values). Org setup covers
**company settings**, **users**, and **licenses**. Understanding the object/field/record model,
relationships, and declarative UI configuration is the foundation every Salesforce role builds on.
This chapter teaches each with a hands-on walkthrough (data-model reasoning; declarative config on a
free Dev org, modeled in `python3`).

## Design Considerations

Model data with the right **object relationships** (master-detail for tight ownership/rollups, lookup
for loose links). Add **custom fields/objects** only when standard ones don't fit. Use **record types**
for genuine process variations. Configure **page layouts** for usability. Manage **users and licenses**
carefully. Prefer **declarative** configuration over code.

## Implementation and Automation

The labs reason about the data model, relationships, and record types.

## Validation and Troubleshooting

Confirm the data-model foundation:

```text
Objects (tables): standard (Account/Contact/Opportunity/Case) + custom (__c). Fields (columns) + records (rows). Relationships: lookup (loose) vs master-detail (tight parent-child, inherits sharing + rollups).
UI: page layouts (fields/related lists) + record types (process variations). Org: company settings + users + licenses. Declarative-first.
```

Common pitfalls: using **master-detail** where a **lookup** is meant (creates unwanted dependency); and
custom objects duplicating **standard** ones.

## Security and Best Practices

Model with the right **relationships**, extend with **custom** only when needed, use **record types**
for real variations, and configure **layouts** and **users** thoughtfully. Declarative-first. All work
is authorized administration.

## Hands-On Lab

Data-model walkthroughs. **Shared prerequisites** — `python3`, and a free Developer Edition org.
**Cost:** none.

### Lab 2.1 — Reason about the data model

**Objective:** Objects, fields, records.

```python
python3 - <<'PY'
objects={"Account (standard)":["Name","Industry","AnnualRevenue"],
         "Contact (standard)":["Name","Email","AccountId (lookup)"],
         "Project__c (custom)":["Name","Status__c","Account__c (master-detail)"]}
for obj,fields in objects.items(): print(f"{obj}: {fields}")
print("Admin: standard + custom (__c) objects, each with fields; records are the rows")
PY
```

**Expected result:** standard and **custom** objects with fields and relationships — the data model.

**Negative test:** store project data in the Notes field of Account; create a **custom object** with
proper fields instead.

**Cleanup:** none.

### Lab 2.2 — Choose lookup vs master-detail

**Objective:** Model the right relationship.

```python
python3 - <<'PY'
cases={"Contact -> Account":"lookup (contact can exist, loosely linked)",
       "Line Item -> Order":"master-detail (line item can't exist without the order; rollup totals)",
       "Case -> Account":"lookup (loose)"}
for rel,choice in cases.items(): print(f"{rel:20}: {choice}")
print("Admin: master-detail = tight (dependency + rollup + inherited sharing); lookup = loose")
PY
```

**Expected result:** each relationship matched to **lookup or master-detail** — correct data modeling.

**Negative test:** use a **lookup** where you need rollup summary totals; only **master-detail**
supports rollups — choose it.

**Cleanup:** none.

### Lab 2.3 — Apply record types

**Objective:** Model process variations.

```python
python3 - <<'PY'
record_types={"Opportunity":["New Business (layout A, stages 1)","Renewal (layout B, stages 2)"],
              "Case":["Support (support layout)","Billing (billing layout)"]}
for obj,rts in record_types.items(): print(f"{obj}: {rts}")
print("Admin: record types = variations of one object (own layout + picklists) per business process")
PY
```

**Expected result:** **record types** giving one object multiple process variations — flexible
configuration.

**Negative test:** create separate **custom objects** for New Business vs Renewal opportunities; use
**record types** on one object instead.

**Cleanup:** none.

### Lab 2.4 — Set up users and licenses

**Objective:** Provision access correctly.

```python
python3 - <<'PY'
user={"name":"amy","license":"Salesforce (full CRM)","profile":"Standard User","role":"Sales - West","active":True}
for k,v in user.items(): print(f"{k:9}: {v}")
print("Admin: each user needs a license + profile + role; deactivate (not delete) on offboarding")
PY
```

**Expected result:** a user provisioned with **license, profile, and role** — correct access setup.

**Negative test:** delete a departing user's record; Salesforce **deactivates** users (records
reference them) — deactivate, don't delete.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Administrator foundation covers the Salesforce data model (standard/custom objects, fields,
records), lookup vs master-detail relationships, record types for process variations, page layouts,
and user/license setup — the declarative grounding for every role.

- [ ] I can reason about the data model.
- [ ] I can choose lookup vs master-detail.
- [ ] I can apply record types.
- [ ] I can set up users and licenses.
- [ ] I completed Labs 2.1–2.4 including each negative test.
