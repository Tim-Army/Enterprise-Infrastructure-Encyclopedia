# Chapter 03: CSA — Data and Security

## Learning Objectives

- Secure records and fields with Access Control Lists (ACLs).
- Import data with Import Sets and Transform Maps.
- Migrate changes with Update Sets.
- Build a Service Catalog item.
- Complete a walkthrough for each CSA data/security topic.

## Theory and Architecture

The second CSA domain covers **data and security**. **Access Control Lists (ACLs)** are ServiceNow's
security model: each ACL protects an **operation** (read, write, create, delete) on a **table or
field**, and grants access based on **roles** and optional **conditions/scripts** — ACLs are evaluated
so a user must pass the applicable rule to act. **Import Sets** bring external data in: data lands in a
staging table, then a **Transform Map** maps and copies it into a target table (with coalescing to
update vs insert). **Update Sets** capture configuration changes (new fields, business rules, UI
changes) so they can be **migrated** from a development instance to test and production — the platform's
change-promotion mechanism (distinct from data). The **Service Catalog** presents requestable items
(hardware, access, services) as **catalog items** backed by workflows. Together these cover securing
data, loading data, moving configuration safely, and delivering services — core administrator skills.
This chapter teaches each with a hands-on walkthrough (ACL evaluation, transform logic, and catalog
design).

## Design Considerations

Secure with **ACLs** (role + condition), least privilege, field-level where needed. Import via
**Import Set + Transform Map** with **coalesce** to avoid duplicates. Capture config in **Update Sets**
and promote dev → test → prod (never edit prod directly). Build **catalog items** with clear
workflows. Keep data and configuration changes separate.

## Implementation and Automation

The labs evaluate an ACL, transform imported data, plan an Update Set, and design a catalog item.

## Validation and Troubleshooting

Confirm the data/security model:

```text
ACLs: protect operation (read/write/create/delete) on table/field via role + condition/script; user must pass. Import Sets -> staging -> Transform Map (coalesce) -> target table.
Update Sets: capture config changes -> promote dev->test->prod. Service Catalog: catalog items + workflows. Data != configuration.
```

Common pitfalls: **editing production** directly instead of using Update Sets; and imports with no
**coalesce** (duplicate records).

## Security and Best Practices

Secure with least-privilege **ACLs**, import with **coalesce**, promote configuration via **Update
Sets** (dev→test→prod), and build clear **catalog items**. Never edit prod directly. All work is
authorized administration.

## Hands-On Lab

Data/security walkthroughs. **Shared prerequisites** — `python3`, a free PDI. **Cost:** none.

### Lab 3.1 — Evaluate an ACL

**Objective:** Enforce record security.

```python
python3 - <<'PY'
def acl_pass(user_roles, required_role, condition_ok):
    return required_role in user_roles and condition_ok
# ACL: write on incident.priority requires 'itil' AND record is active
print("agent writes active incident:", acl_pass(["itil"], "itil", True))
print("agent writes closed incident:", acl_pass(["itil"], "itil", False))
print("no-role user writes:", acl_pass(["ess"], "itil", True))
print("CSA: ACL = required role + condition; user must pass to perform the operation")
PY
```

**Expected result:** access **granted** only when role and condition both pass — ACL enforcement.

**Negative test:** rely on hiding a field in the UI for security; **ACLs** enforce it server-side —
use them.

**Cleanup:** none.

### Lab 3.2 — Transform imported data

**Objective:** Load data cleanly.

```python
python3 - <<'PY'
staging=[{"emp_id":"E1","full_name":"Amy Ng","dept":"Finance"},
         {"emp_id":"E1","full_name":"Amy Ng","dept":"Finance"}]  # duplicate
seen={}; 
for row in staging:
    # coalesce on emp_id -> update if exists, else insert
    action="update" if row["emp_id"] in seen else "insert"
    seen[row["emp_id"]]=row
    print(f"{row['emp_id']} -> {action}")
print("Transform Map: coalesce on a key -> update existing, insert new (no duplicates)")
PY
```

**Expected result:** the duplicate **updates** rather than inserting — coalesce-based transform.

**Negative test:** import without a **coalesce** field; every run creates duplicates — coalesce on a
key.

**Cleanup:** none.

### Lab 3.3 — Plan an Update Set promotion

**Objective:** Move configuration safely.

```python
python3 - <<'PY'
update_set={"name":"INC-form-tweaks","captures":["new field: incident.impact_notes","modified business rule"],
            "path":"dev -> test -> prod","note":"config only (not data)"}
for k,v in update_set.items(): print(f"{k:9}: {v}")
print("CSA: Update Sets promote CONFIG changes dev->test->prod; data uses import, not update sets")
PY
```

**Expected result:** a config change captured in an **Update Set** for promotion — safe change
management.

**Negative test:** make the change directly in **production**; it's unversioned and risky — use an
**Update Set** from dev.

**Cleanup:** none.

### Lab 3.4 — Design a Service Catalog item

**Objective:** Deliver a requestable service.

```python
python3 - <<'PY'
catalog_item={"name":"Request new laptop","variables":["model","justification"],
              "workflow":"manager approval -> fulfillment task -> asset assignment","fulfillment_group":"IT Hardware"}
for k,v in catalog_item.items(): print(f"{k:16}: {v}")
print("CSA: catalog item = variables + workflow (approval + fulfillment)")
PY
```

**Expected result:** a **catalog item** with variables and an approval/fulfillment workflow — service
delivery.

**Negative test:** let users email IT for laptops; a **catalog item** standardizes approval and
fulfillment — build one.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CSA data/security domain secures records with ACLs, imports data via Import Sets and Transform
Maps with coalesce, promotes configuration with Update Sets (dev→test→prod), and delivers services via
the Service Catalog — the administrator's core data and change skills.

- [ ] I can evaluate an ACL.
- [ ] I can transform imported data with coalesce.
- [ ] I can plan an Update Set promotion.
- [ ] I can design a Service Catalog item.
- [ ] I completed Labs 3.1–3.4 including each negative test.
