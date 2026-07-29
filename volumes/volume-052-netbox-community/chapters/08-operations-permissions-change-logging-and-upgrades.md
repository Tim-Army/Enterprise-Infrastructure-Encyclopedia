# Chapter 08: Operations — Permissions, Change Logging, and Upgrades

## Learning Objectives

- Control access with users, groups, and object permissions.
- Audit changes with the change log.
- Record operational notes with journal entries.
- Back up and upgrade a NetBox deployment safely.
- Complete a walkthrough for each operational task.

## Theory and Architecture

NetBox operations center on **access, audit, and lifecycle**. **Object permissions**
grant actions (view/add/change/delete) on models — optionally constrained by a query
filter (e.g., only a tenant's objects) — to **users**/**groups**, layered on tokens.
Every create/update/delete is recorded in the **change log** (who, when, before/after).
**Journal entries** capture human operational notes on an object. Lifecycle is
**back up PostgreSQL → upgrade → run `upgrade.sh`/migrations**.

## Design Considerations

Grant **least privilege** with object permissions and constraints, rely on the
**change log** for audit (don't bolt on external tracking), use **journaling** for
context the change log can't capture ("replaced PSU"), and always **back up the
database** before an upgrade.

## Implementation and Automation

The labs use the API/CLI for a constrained permission, a change-log query, a journal
entry, and a backup.

## Validation and Troubleshooting

Confirm the operations model:

```text
Permissions: (user/group) x (model) x (actions) [+ constraint filter], plus API tokens.
Change log: automatic before/after record of every object change.
Journal: manual timestamped notes on an object.
Upgrade: back up PostgreSQL -> pull release -> upgrade.sh (migrations).
```

Common pitfalls: over-broad permissions; and upgrading with **no database backup**.

## Security and Best Practices

Use **constrained object permissions** (least privilege), review the **change log**
for audit, journal operational context, take a **PostgreSQL dump** before every
upgrade, and read the release notes for breaking changes.

## Hands-On Lab

Operations walkthroughs. **Shared prerequisites** — a running NetBox (`netbox-docker`);
`$NB`/`$TOKEN`; `pynetbox`; shell access to the containers. **Cost:** none.

### Lab 8.1 — Create a constrained object permission

**Objective:** Grant view on devices limited to one tenant.

```python
import pynetbox
nb = pynetbox.api("http://localhost:8000", token="TOKEN")
perm = nb.users.permissions.create(
  name="view-acme-devices", enabled=True, object_types=["dcim.device"],
  actions=["view"], constraints={"tenant__slug":"acme-corp"})
print("permission:", perm.name, "actions:", perm.actions)
```

**Expected result:** a permission granting **view** only on Acme's devices — least
privilege with a constraint.

**Negative test:** grant unconstrained `dcim.device` view to everyone; **constrain** to
the tenant's objects instead.

**Cleanup:** `perm.delete()`.

### Lab 8.2 — Read the change log

**Objective:** Confirm changes are audited.

```bash
curl -sS -H "Authorization: Token $TOKEN" \
  "$NB/api/extras/object-changes/?limit=3" \
  | python3 -c "import sys,json;[print(c['action']['value'],c['changed_object_type']) for c in json.load(sys.stdin)['results']]"
```

**Expected result:** recent **change-log entries** (action + object type) — the audit
trail.

**Negative test:** add external audit logging for NetBox edits; the **built-in change
log** already records before/after — use it.

**Cleanup:** none (read-only).

### Lab 8.3 — Add a journal entry

**Objective:** Record an operational note on a device.

```python
dev = nb.dcim.devices.get(name="leaf01")
j = nb.extras.journal_entries.create(
  assigned_object_type="dcim.device", assigned_object_id=dev.id,
  kind="info", comments="Replaced faulty SFP in eth1.")
print("journal entry id:", j.id, "on", dev.name)
```

**Expected result:** a timestamped **journal entry** on leaf01 — human context the
change log can't infer.

**Negative test:** keep maintenance notes in a wiki; **journal on the object** so
context lives with the device.

**Cleanup:** `j.delete()`.

### Lab 8.4 — Back up the database

**Objective:** Take a PostgreSQL dump before an upgrade.

```bash
docker compose exec -T postgres pg_dump -U netbox netbox > netbox-backup.sql
ls -lh netbox-backup.sql | awk '{print $5, $9}'
```

**Expected result:** a non-empty **`netbox-backup.sql`** dump — a restore point before
upgrading.

**Negative test:** upgrade without a backup; migrations are hard to reverse — **dump
first**.

**Cleanup:** keep or remove the dump as policy dictates.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NetBox operations are access (constrained object permissions + tokens), audit (the
change log), context (journal entries), and lifecycle (back up PostgreSQL, then run the
upgrade). This chapter constrained a permission, read the change log, journaled, and
backed up.

- [ ] I can create least-privilege, constrained permissions.
- [ ] I can read the change log for audit.
- [ ] I can add journal entries for context.
- [ ] I can back up PostgreSQL before an upgrade.
- [ ] I completed Labs 8.1–8.4 including each negative test.
