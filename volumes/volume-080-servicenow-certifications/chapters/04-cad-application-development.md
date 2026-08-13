# Chapter 04: CAD — Application Development

## Learning Objectives

- Write server-side scripts with GlideRecord and GlideSystem.
- Build Business Rules and Client Scripts.
- Develop scoped applications.
- Integrate via REST APIs.
- Complete a walkthrough for each CAD development topic.

## Theory and Architecture

The **Certified Application Developer (CAD)** validates building on the Now Platform with code. The
core server-side API is **GlideRecord** — an object for querying and manipulating table records
(`new GlideRecord('incident')`, `addQuery`, `query`, `next`, `update`) — paired with **GlideSystem
(gs)** for logging, user context, and utilities. **Business Rules** run server-side on database
operations (before/after insert/update/delete, or async) to enforce logic and automation. **Client
Scripts** run in the browser on form events (onLoad, onChange, onSubmit) for UI behavior, and
**Script Includes** hold reusable server-side functions. Developers build **scoped applications** —
self-contained apps with their own namespace, tables, and security — the modern way to extend the
platform safely. **REST APIs** (inbound Scripted REST APIs and outbound RESTMessageV2) integrate with
external systems. Writing efficient, secure GlideRecord queries and knowing when logic belongs
server-side (Business Rule) vs client-side (Client Script) is the heart of CAD. This chapter teaches
each with a hands-on walkthrough (GlideRecord logic, rule design, and REST patterns).

## Design Considerations

Query efficiently with **GlideRecord** (specific `addQuery`, avoid dot-walking loops). Put data
integrity and automation in **Business Rules** (server), UI behavior in **Client Scripts**. Reuse via
**Script Includes**. Build in a **scoped app** for isolation and security. Integrate with **REST**,
handling errors and auth. Log with **gs.info/gs.error**.

## Implementation and Automation

The labs write a GlideRecord query, design a Business Rule vs Client Script, and outline REST.

## Validation and Troubleshooting

Confirm the development model:

```text
Server: GlideRecord (query/manipulate records) + GlideSystem (gs: log/user/utils) + Business Rules (before/after/async on DB ops) + Script Includes (reusable).
Client: Client Scripts (onLoad/onChange/onSubmit, UI). Build scoped apps (isolated namespace). Integrate via REST (Scripted REST inbound / RESTMessageV2 outbound).
```

Common pitfalls: heavy logic in **Client Scripts** that belongs server-side; and **inefficient
GlideRecord** queries (no `addQuery`, querying in loops).

## Security and Best Practices

Query efficiently, put integrity logic **server-side** (Business Rules), reuse via **Script Includes**,
build **scoped apps**, and secure **REST** integrations (auth + error handling). Log appropriately.
All development is authorized.

## Hands-On Lab

Development walkthroughs. **Shared prerequisites** — a free PDI (Script Background / Studio) and
`python3` for modeling logic. **Cost:** none.

### Lab 4.1 — Write a GlideRecord query

**Objective:** Query records server-side.

```javascript
// ServiceNow server-side script (Scripts - Background on a PDI):
var gr = new GlideRecord('incident');
gr.addQuery('active', true);
gr.addQuery('priority', 1);          // P1 incidents
gr.orderBy('sys_created_on');
gr.query();
while (gr.next()) {
    gs.info('P1 incident: ' + gr.number + ' - ' + gr.short_description);
}
```

**Expected result:** the script logs **active P1 incidents** via GlideRecord — the core server-side
query pattern.

**Negative test:** query all incidents then filter in JavaScript; that pulls everything — use
**addQuery** to filter at the database.

**Rollback:** none (read-only query).

### Lab 4.2 — Choose Business Rule vs Client Script

**Objective:** Put logic in the right place.

```python
python3 - <<'PY'
logic={"prevent closing incident without resolution notes":"Business Rule (before update, server — enforced always)",
       "hide a field when category=hardware":"Client Script / UI Policy (browser)",
       "auto-set assignment group from category":"Business Rule (server)",
       "validate email format as user types":"Client Script (onChange)"}
for req,place in logic.items(): print(f"- {req}\n    -> {place}")
PY
```

**Expected result:** each requirement mapped to **server (Business Rule)** or **client (Client
Script)** — correct placement.

**Negative test:** enforce data integrity only in a **Client Script**; an API call bypasses the
browser — enforce server-side.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Model a scoped app boundary

**Objective:** Isolate an application.

```python
python3 - <<'PY'
scoped_app={"scope":"x_acme_travel","tables":["x_acme_travel_request"],
            "isolation":"own namespace + protected from global changes","access":"scoped roles + cross-scope privileges controlled"}
for k,v in scoped_app.items(): print(f"{k:11}: {v}")
print("CAD: scoped apps isolate tables/scripts/security under x_<vendor>_<app>")
PY
```

**Expected result:** a **scoped application** with an isolated namespace — safe extension.

**Negative test:** build everything in the **global** scope; changes can collide with the base system
— use a **scoped app**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Outline a REST integration

**Objective:** Integrate with an external system.

```python
python3 - <<'PY'
outbound={"tool":"RESTMessageV2","method":"POST","endpoint":"https://api.example.com/tickets",
          "auth":"OAuth 2.0 (credential record)","error_handling":"check status, log gs.error on failure"}
inbound={"tool":"Scripted REST API","resource":"/api/x_acme/travel/approve","auth":"ACL + OAuth"}
print("outbound:",outbound); print("inbound:",inbound)
print("CAD: RESTMessageV2 (out) + Scripted REST API (in), always with auth + error handling")
PY
```

**Expected result:** inbound and outbound **REST** patterns with auth and error handling — CAD
integration.

**Negative test:** hardcode credentials in the script; use a **credential/connection record** and
handle errors — secure the integration.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CAD develops on the Now Platform: GlideRecord/GlideSystem server-side scripting, Business Rules vs
Client Scripts, reusable Script Includes, scoped applications, and secure REST integrations — building
efficient, secure platform logic.

- [ ] I can write a GlideRecord query.
- [ ] I can choose Business Rule vs Client Script.
- [ ] I can model a scoped app boundary.
- [ ] I can outline a REST integration.
- [ ] I completed Labs 4.1–4.4 including each negative test.
