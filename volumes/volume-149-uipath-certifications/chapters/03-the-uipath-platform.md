# Chapter 03: The UiPath Platform

## Learning Objectives

- Describe the three core platform pieces: Studio, Orchestrator, Robots.
- Distinguish designing an automation from deploying and running it.
- Understand the Center of Excellence operating model.
- Place the broader product family around the core.

*Cert relevance: the platform architecture is foundational to every UiPath certification — you build in Studio, deploy through Orchestrator, run on Robots.*

## The three core pieces

Every UiPath automation moves through three components, and understanding their division of labor is the foundation of the whole platform:

| Component | Is | Who uses it |
|:---|:---|:---|
| **Studio** | The **design** environment — build automations as visual workflows | Developers |
| **Orchestrator** | The **management** server — deploy, schedule, monitor, and govern robots | Admins / CoE |
| **Robots** | The **execution** engines — actually run the automations | (headless or on a user's desk) |

The flow is: a developer **builds** an automation in **Studio**, publishes it to **Orchestrator**, which **deploys and schedules** it onto **Robots** that **execute** it. Design, manage, run — three distinct concerns, three tools. This separation is what lets one developer's automation run reliably on hundreds of robots under central governance.

## Studio: design

**Studio** is where automations are built — a **visual, low-code** environment where you assemble **activities** (click, type, read, loop, if/else) into **workflows** that describe the process. It is low-code so that automation is accessible beyond hard-core programmers (a business analyst can build simple automations), but it is a genuine development tool with variables, arguments, error handling, and version control — [Chapter 4](04-building-automations-studio-and-workflows.md) covers building in depth.

## Orchestrator: manage

**Orchestrator** is the control center — the web application that turns a *built* automation into a *running, governed* operation. It handles **deployment** (push automations to robots), **scheduling** (run at 2 a.m., or on a trigger), **queues** (distribute work items across robots), **monitoring** (are jobs succeeding?), **assets** (shared config and credentials), and **governance** (who can run what, audit logs). Orchestrator is what makes automation *enterprise-grade* rather than a script on someone's laptop — [Chapter 5](05-attended-vs-unattended-and-orchestrator.md) covers it.

## Robots: execute

**Robots** are the workers that actually perform the automation. They come in two kinds — **attended** (run on a person's desktop, triggered by them) and **unattended** (run headless on servers, fully automatic) — which is a central design decision covered in [Chapter 5](05-attended-vs-unattended-and-orchestrator.md).

## The Center of Excellence

UiPath deployments are typically run by a **Center of Excellence (CoE)** — a central team that governs automation across the organization: setting standards, running Orchestrator, curating the automation pipeline, and enabling business units to automate safely. The CoE is why the certification program is *role-based* (Chapter 1): a CoE needs developers, business analysts, architects, and now agent-governance skills. The lab models the platform flow and the CoE's role.

## Hands-On Lab

Python models the platform architecture. **Cost:** none.

### Lab 3.1 — Trace an automation through the platform

**Objective:** Follow an automation from build to execution across the three components.

```bash
python3 - <<'EOF'
# the lifecycle of an automation across Studio -> Orchestrator -> Robots
STAGES = [
  ("Studio",       "developer builds 'process invoices' as a visual workflow",  "DESIGN"),
  ("Studio",       "publishes the package to Orchestrator",                      "DESIGN"),
  ("Orchestrator", "stores the package, sets a schedule (daily 2am)",            "MANAGE"),
  ("Orchestrator", "assigns the job to a pool of unattended robots",             "MANAGE"),
  ("Orchestrator", "feeds work items via a QUEUE, supplies credentials as ASSETS","MANAGE"),
  ("Robot",        "executes the workflow on each item, headless",               "EXECUTE"),
  ("Orchestrator", "monitors results, logs, retries failures, alerts on errors", "MANAGE"),
]
print("One automation, three components, three concerns:\n")
concern = None
for comp, action, c in STAGES:
    if c != concern:
        print(f"  [{c}]")
        concern = c
    print(f"     {comp:13} {action}")
print("\nThe separation of concerns:")
print("  STUDIO  = DESIGN  — the developer builds the workflow (visual, low-code)")
print("  ORCHESTRATOR = MANAGE — deploy, schedule, queue work, supply credentials,")
print("            monitor, retry, audit. The enterprise control plane.")
print("  ROBOTS  = EXECUTE — actually run the steps, attended or unattended")
print("\nThis is why UiPath scales past 'a script on a laptop': ONE automation built")
print("once in Studio runs on MANY robots, centrally governed by Orchestrator. Change")
print("the schedule, rotate a credential, add robots — all in Orchestrator, without")
print("touching the automation. Build once, manage centrally, run everywhere.")
EOF
```

**Expected result:** An automation traced from Studio (design) through Orchestrator (manage: deploy, schedule, queue, credentials, monitor) to Robots (execute), showing the three separated concerns. The platform lesson is that this separation is what makes automation enterprise-grade — one automation built once runs on many robots under central Orchestrator governance, not a script on a laptop.

**Negative test:** Running an automation as a standalone script on a developer's machine. It has no central scheduling, credential management, monitoring, or governance — Orchestrator is what turns a built automation into a reliable, governed enterprise operation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Studio, Orchestrator, and Robots understood as design, manage, and execute — three separated concerns.
- [ ] Studio placed as the visual low-code design environment for developers.
- [ ] Orchestrator understood as the enterprise control plane (deploy, schedule, queues, assets, monitoring, governance).
- [ ] The Center of Excellence recognized as the operating model that makes the role-based program make sense.
