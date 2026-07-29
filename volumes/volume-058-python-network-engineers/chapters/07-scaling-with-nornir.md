# Chapter 07: Scaling with Nornir

## Learning Objectives

- Explain what Nornir provides over ad-hoc scripts.
- Define an inventory of hosts and groups.
- Write and run tasks across devices in parallel.
- Use plugins (Netmiko, NAPALM) within Nornir.
- Complete a walkthrough for each Nornir skill.

## Theory and Architecture

**Nornir** is a pure-Python automation **framework**: instead of a DSL (like Ansible's
YAML), you write Python **tasks** and Nornir handles the **inventory**, **parallel
execution**, **filtering**, and **result aggregation**. Its **inventory** (hosts, groups,
defaults — often in YAML or from NetBox) carries connection data and variables; **tasks**
are functions run against a filtered set of hosts, in parallel by default; and
**plugins** (`nornir_netmiko`, `nornir_napalm`, `nornir_jinja2`) integrate the libraries
from earlier chapters. It scales the single-device patterns to a fleet with proper
concurrency and reporting.

## Design Considerations

Use Nornir when you outgrow loops — it gives **inventory management**, **parallelism**,
**host filtering** (by group/role/platform), and structured **results**. Source the
inventory from **NetBox** where possible. Keep tasks small and composable.

## Implementation and Automation

The labs define an inventory, write a task, filter hosts, and use plugins.

## Validation and Troubleshooting

Confirm the model:

```text
InitNornir(inventory=...) -> nr.filter(...) -> nr.run(task=fn) -> AggregatedResult.
Inventory: hosts/groups/defaults (YAML or NetBox). Plugins: nornir_netmiko/napalm/jinja2.
```

Common pitfalls: hand-rolling concurrency/inventory instead of using Nornir; and not
**filtering** (running against everything).

## Security and Best Practices

Let Nornir manage **inventory + parallelism**, **filter** to the target set, source
inventory from a **source of truth**, and keep credentials in the inventory's secure
store/env. Review aggregated **results** for per-host failures.

## Hands-On Lab

Nornir walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install nornir
nornir-netmiko nornir-utils`); a lab inventory (or the patterns shown). **Cost:** none.

### Lab 7.1 — Define an inventory

**Objective:** Create a simple YAML inventory.

```yaml
# hosts.yaml
r1: { hostname: 10.0.0.11, platform: ios, groups: [core] }
r2: { hostname: 10.0.0.12, platform: ios, groups: [core] }
# groups.yaml
core: { username: admin, password: admin }
```

**Expected result:** an inventory of two hosts in the **core** group — Nornir's data
model.

**Negative test:** put credentials on each host; use **groups/defaults** to avoid
repetition.

**Cleanup:** none.

### Lab 7.2 — Initialize and filter

**Objective:** Load the inventory and select hosts.

```python
from nornir import InitNornir
nr = InitNornir(inventory={"plugin":"SimpleInventory",
    "options":{"host_file":"hosts.yaml","group_file":"groups.yaml"}})
core = nr.filter(groups="core")
print(sorted(core.inventory.hosts))   # ['r1', 'r2']
```

**Expected result:** **`['r1', 'r2']`** — filtered target hosts.

**Negative test:** run tasks against **all** hosts unfiltered; **filter** to the intended
set to limit blast radius.

**Cleanup:** none.

### Lab 7.3 — Run a task in parallel

**Objective:** Execute a function across hosts.

```python
from nornir_netmiko.tasks import netmiko_send_command
result = core.run(task=netmiko_send_command, command_string="show clock")
for host, r in result.items():
    print(host, "->", "failed" if r.failed else "ok")
```

**Expected result:** per-host results (ok/failed), run **in parallel** — fleet execution.

**Negative test:** loop devices serially in Python; **Nornir** parallelizes and aggregates
results — use it at scale.

**Cleanup:** none.

### Lab 7.4 — Combine plugins (render + push)

**Objective:** Chain templating and deployment.

```python
# nornir_jinja2 renders config from host data; nornir_netmiko/napalm pushes it.
# def deploy(task): 
#     cfg = task.run(task=template_file, template="base.j2", path="templates").result
#     task.run(task=netmiko_send_config, config_commands=cfg.splitlines())
print("pattern: render (jinja2) -> push (netmiko/napalm) as chained Nornir tasks")
```

**Expected result:** a task chaining **render → push** across the fleet — end-to-end
automation.

**Negative test:** render and push in separate ad-hoc scripts; **chain** them in one
Nornir task for consistency.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Nornir scales single-device patterns to a fleet: a managed inventory (ideally from a
source of truth), host filtering, parallel task execution, and plugins integrating
Netmiko/NAPALM/Jinja2 — with aggregated results. This chapter built an inventory,
filtered, ran tasks, and chained plugins.

- [ ] I can define a Nornir inventory.
- [ ] I can initialize and filter hosts.
- [ ] I can run tasks in parallel.
- [ ] I can combine plugins to render and push.
- [ ] I completed Labs 7.1–7.4 including each negative test.
