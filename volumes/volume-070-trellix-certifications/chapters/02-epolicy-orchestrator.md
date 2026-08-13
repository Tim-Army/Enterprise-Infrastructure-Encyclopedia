# Chapter 02: ePolicy Orchestrator (ePO)

## Learning Objectives

- Explain ePO's role as the Trellix central management console.
- Organize managed systems with the System Tree and tags.
- Assign policies and client tasks.
- Read state and automate with the ePO API.
- Complete a walkthrough for each ePO topic.

## Theory and Architecture

**ePolicy Orchestrator (ePO)** is the central nervous system of a Trellix endpoint deployment — a
single console to **deploy** agents and products, **configure policies**, **schedule tasks**,
**collect events**, and **report** on the whole estate. Its core structures are: the **System
Tree** (a hierarchy of managed systems, organized by group — geography, function, or synced from
Active Directory); **tags** (labels applied by criteria to group systems dynamically, e.g., "sales
laptops"); **policies** (per-product configuration assigned to groups/systems, with inheritance);
**client tasks** (scheduled actions like scans or updates); and **dashboards/queries** (reporting
over the event and system data). The **Trellix Agent** on each endpoint communicates with ePO to
receive policy and report events. ePO also exposes a **web API** for automation. Because most
Trellix endpoint products (ENS, EDR, DLP) manage **through ePO**, mastering it is the foundation
for the rest.

## Design Considerations

Structure the **System Tree** to match how you assign policy (by function/location), and use
**tags** for dynamic grouping rather than manual moves. Rely on **policy inheritance** — set broad
defaults high in the tree, override narrowly. Schedule **client tasks** off-peak. Use the **API**
for repeatable, auditable automation.

## Implementation and Automation

The labs organize the System Tree, apply a tag, assign a policy, and query ePO via the API — all
**authorized administration**.

## Validation and Troubleshooting

Confirm the ePO model:

```text
ePO: System Tree (groups, AD sync) + tags (dynamic grouping) + policies (per-product, inherited)
  + client tasks (scheduled) + dashboards/queries (reporting). Trellix Agent <-> ePO. Web API for automation.
Most endpoint products (ENS/EDR/DLP) manage THROUGH ePO.
```

Common pitfalls: **manually moving** systems where a **tag** would group them dynamically; and
flat policy with **no inheritance** (unmanageable at scale).

## Security and Best Practices

Use **least-privilege ePO roles**, structure the tree for clean **policy inheritance**, and
**tag** dynamically. Secure the ePO server and API (TLS, restricted accounts). Keep the agent and
products updated via client tasks. Defensive administration throughout.

## Hands-On Lab

ePO walkthroughs. **Shared prerequisites** — an ePO instance (or the console/API patterns), in an
**authorized** lab. **Cost:** none with a lab instance.

### Lab 2.1 — Organize the System Tree

**Objective:** Group managed systems for policy assignment.

```text
# ePO console: System Tree -> New Subgroups (e.g., "Corp/Laptops", "Corp/Servers").
# Optionally sync from Active Directory for automatic population.
"system tree: group by function/location -> assign policy at the group level (inherited)"
```

**Expected result:** a **System Tree** grouped for policy assignment — the management structure.

**Negative test:** put every system in the root with no grouping; policy assignment becomes
unmanageable — **group** them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Create a dynamic tag

**Objective:** Group systems by criteria automatically.

```text
# ePO: Tag Catalog -> New Tag "Sales-Laptops" with criteria (e.g., OS=Windows AND OU contains Sales).
# Tag runs on a schedule/criteria and applies automatically to matching systems.
"tag: criteria-based dynamic grouping -> policy follows the tag, not manual placement"
```

**Expected result:** a **tag** that auto-applies to matching systems — dynamic grouping.

**Negative test:** manually tag hundreds of systems; **criteria-based tags** apply automatically —
define the criteria.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Assign a policy

**Objective:** Configure a product for a group.

```text
# ePO: Policy Catalog -> pick a product policy (e.g., ENS Threat Prevention) -> assign to a
#   System Tree group. Child groups inherit unless overridden.
"policy: set at group -> inherited by children -> override narrowly where needed"
```

**Expected result:** a **policy assigned** with inheritance — consistent, scalable configuration.

**Negative test:** assign the same policy to every system individually; use **group assignment +
inheritance** — set once, inherit widely.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Query ePO via the API

**Objective:** Retrieve managed-system state programmatically.

```bash
curl -sk -u "$EPO_CRED" "https://<epo>:8443/remote/system.find?searchText=&:output=json" 2>/dev/null \
  | python3 -c "import sys,json;print('managed systems returned' if sys.stdin.read().strip() else 'query ePO via /remote/<command> web API')" 2>/dev/null \
  || echo "ePO web API: /remote/system.find, /remote/policy... return managed-estate data as JSON"
```

**Expected result:** the managed systems from the **ePO web API** — programmatic administration and
reporting.

**Negative test:** export reports from the console by hand for automation; the **API** feeds it —
use it.

**Rollback:** none (read-only).

### Lab 2.5 — Schedule a client task

**Objective:** Automate a recurring action.

```text
# ePO: Client Task Catalog -> New Task (e.g., "On-Demand Scan" or "Product Update") ->
#   assign to a group with a schedule (off-peak).
"client task: scheduled scan/update assigned to a group -> automated maintenance"
```

**Expected result:** a **scheduled client task** (scan/update) on a group — automated endpoint
maintenance.

**Negative test:** run scans manually per endpoint; **client tasks** schedule them fleet-wide —
automate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ePO is the Trellix central console: the System Tree and tags organize systems, policies (with
inheritance) and client tasks configure and maintain them, dashboards report, and the web API
automates. Structure the tree for policy, tag dynamically, rely on inheritance, and automate via
the API.

- [ ] I can organize the System Tree.
- [ ] I can create a dynamic tag.
- [ ] I can assign a policy with inheritance.
- [ ] I can query ePO via the API and schedule a client task.
- [ ] I completed Labs 2.1–2.5 including each negative test.
