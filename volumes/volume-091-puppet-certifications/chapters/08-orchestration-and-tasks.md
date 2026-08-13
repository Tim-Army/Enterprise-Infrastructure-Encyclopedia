# Chapter 08: Orchestration and Tasks

## Learning Objectives

- Explain Bolt and agentless orchestration.
- Run an ad-hoc command and a task.
- Reason about plans that combine tasks and Puppet code.
- Reason about the Puppet Orchestrator in PE.
- Complete a walkthrough for each orchestration-and-tasks topic.

## Theory and Architecture

The **Orchestration & Tasks** domain covers imperative, on-demand actions that complement Puppet's
continuous declarative enforcement. **Bolt** is Puppet's **agentless** orchestration tool: it runs
commands, scripts, and **tasks** over **SSH/WinRM** without requiring the Puppet agent, driven by an
**inventory** of targets. A **task** is a single action packaged in a module (a script in any language
plus metadata declaring its parameters) — e.g., "restart a service," "run a backup." A **plan** is a
workflow written in the Puppet language (or YAML) that orchestrates multiple tasks, commands, and even
Puppet `apply` blocks with logic (run this task, check the result, then that one) — for multi-step
operations like a coordinated deployment. In **Puppet Enterprise**, the **Orchestrator** runs Puppet
across the fleet on demand (trigger agent runs, respect dependencies, run tasks/plans at scale) through
the console or `puppet job`. Orchestration handles the "do this now, in order" that continuous
enforcement does not. This chapter teaches orchestration and tasks with hands-on Bolt walkthroughs.

## Design Considerations

Use **Puppet** (declarative) for continuous desired state and **Bolt/tasks** (imperative) for one-off or
ordered actions (deploys, reboots, break-glass). Package repeatable actions as **tasks** (parameterized,
in a module) rather than ad-hoc scripts. Compose multi-step operations as **plans** with error handling.
Use **Bolt** where nodes have no agent; use the **Orchestrator** to run at scale in PE. Keep tasks
idempotent where possible and least-privilege.

## Implementation and Automation

The labs run an ad-hoc Bolt command, run a task, and reason about a plan and the Orchestrator — the
orchestration the domain validates.

## Validation and Troubleshooting

Confirm orchestration and tasks:

```text
Bolt: agentless (SSH/WinRM) runs commands/scripts/tasks over an inventory; no agent needed
Task: one packaged action (script + metadata params) in a module
Plan: a workflow (Puppet language/YAML) orchestrating tasks/commands/apply with logic + error handling
PE Orchestrator: run Puppet + tasks/plans across the fleet on demand (console / puppet job)
Puppet (declarative continuous) vs Bolt/tasks (imperative on-demand)
```

Common pitfalls: scripting a multi-step deploy ad-hoc instead of a repeatable **plan**; and requiring the
agent for a one-off action on an agentless node — use **Bolt**.

## Security and Best Practices

Least-privilege credentials for Bolt/SSH, package actions as reviewed **tasks**, and prefer idempotent
operations. Orchestration acts on your own fleet with authorization. All work is authorized.

## Hands-On Lab

Orchestration-and-tasks walkthroughs. **Shared prerequisites** — **Bolt** installed and an inventory (or
a reachable target); `python3`. **Cost:** none (Bolt is free).

### Lab 8.1 — Run an ad-hoc command with Bolt

**Objective:** Act on targets without an agent.

```bash
bolt command run 'uptime' --targets web1.example.com --user deploy
```

```text
Started on web1.example.com...
Finished on web1.example.com:
  STDOUT: 12:00:00 up 3 days, load average: 0.10, 0.08, 0.05
Successful on 1 target
```

**Expected result:** the command run over SSH with no Puppet agent required — agentless orchestration.

**Negative test:** SSH to each host by hand to run the same command; use **Bolt** with an inventory to
run once across many.

**Rollback:** none (read-only command).

### Lab 8.2 — Run a task

**Objective:** Run a packaged, parameterized action.

```bash
# a module task: mymod/tasks/restart_service.sh with metadata declaring $service
bolt task run mymod::restart_service service=nginx --targets web1.example.com
```

```text
Started on web1.example.com...
Finished on web1.example.com:
  { "status": "restarted", "service": "nginx" }
Successful on 1 target
```

**Expected result:** the packaged task restarting a service with a parameter — a repeatable action.

**Negative test:** paste a one-off restart script each time; package it as a **task** with parameters.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Reason about a plan

**Objective:** Orchestrate a multi-step workflow.

```python
python3 - <<'PY'
plan = [
  "1. task: drain web1 from the load balancer",
  "2. apply: deploy new app version (Puppet)",
  "3. task: health-check web1; if fail -> stop + alert",
  "4. task: re-enable web1 in the load balancer",
]
for step in plan: print(step)
print("A Bolt plan chains tasks + apply with logic/error handling -> coordinated deploy")
PY
```

**Expected result:** a plan sequencing drain → deploy → health-check → re-enable with error handling — a
coordinated operation.

**Negative test:** run the four steps by hand across a fleet; a **plan** makes it repeatable and safe.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Reason about the PE Orchestrator

**Objective:** Run Puppet on demand at scale.

```python
python3 - <<'PY'
print("puppet job run --nodes web1,web2,web3   # trigger Puppet runs now, respecting dependencies")
print("PE Orchestrator: on-demand Puppet + tasks/plans across the fleet (console or CLI)")
print("Use when you must apply NOW rather than wait for the 30-min interval")
PY
```

**Expected result:** the Orchestrator triggering on-demand runs across nodes — immediate, dependency-aware
enforcement.

**Negative test:** wait 30 minutes for the next scheduled run during an incident; use the **Orchestrator**
to run now.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Orchestration complements Puppet's continuous enforcement with on-demand action: Bolt runs commands,
scripts, and packaged tasks agentlessly over SSH/WinRM; plans orchestrate multi-step workflows (tasks,
commands, and apply) with logic; and the Puppet Enterprise Orchestrator triggers Puppet and tasks/plans
across the fleet on demand — imperative "do this now" alongside declarative desired state.

- [ ] I can run an ad-hoc command with Bolt.
- [ ] I can run a packaged task.
- [ ] I can reason about a plan.
- [ ] I can reason about the PE Orchestrator.
- [ ] I completed Labs 8.1–8.4 including each negative test.
