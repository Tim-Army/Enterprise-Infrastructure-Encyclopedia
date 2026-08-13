# Chapter 04: NCP-MCA — Multicloud Automation

## Learning Objectives

- Explain what the NCP-MCA certifies and its target role.
- Summarize the three blueprint sections.
- Apply automation concepts with Nutanix Self-Service and X-Play.
- Build and validate blueprints, runbooks, and playbooks.
- Complete a per-section walkthrough for each NCP-MCA domain.

## Theory and Architecture

The **Nutanix Certified Professional — Multicloud Automation (NCP-MCA)** validates
automating on Nutanix — the automation credential (**75 questions / 120 minutes**).
Its blueprint has **three sections**: **Describe and Differentiate Automation Concepts
and Principles**; **Deploy and Configure Self Service and Related Components**; and
**Validate Blueprints, Runbooks, Playbooks, and Automation Settings**. Automation uses
**Nutanix Self-Service** (formerly Calm) and **X-Play** (Playbooks).

## Design Considerations

The automation engineer distinguishes **imperative vs declarative** automation, models
apps as **blueprints** deployed via **Self-Service** (Projects, categories, roles),
orchestrates with **runbooks**, and event-automates with **X-Play playbooks**
(triggers + actions). Categories and Projects scope who can deploy what.

## Implementation and Automation

The labs use Self-Service/X-Play concepts and the Prism API for each section —
automation principles, Self-Service deployment, and validation.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nutanix.com > NCP-MCA blueprint (75 Q / 120 min):
  1 Describe and Differentiate Automation Concepts and Principles
  2 Deploy and Configure Self Service and Related Components
  3 Validate Blueprints, Runbooks, Playbooks, and Automation Settings
```

Common pitfalls: hard-coding values instead of **macros/variables**; and blueprints
with no failure handling.

## Security and Best Practices

Prefer **declarative blueprints**, parameterize with **macros/variables**, scope with
**Projects/categories/roles**, automate operations with **X-Play**, and **validate**
before publishing. Version blueprints and store secrets in credentials, not plaintext.

## References and Knowledge Checks

- nutanix.com: NCP-MCA blueprint guide; Nutanix Self-Service and X-Play docs.

**Knowledge checks**

1. What is the difference between a blueprint and a runbook?
2. What do Projects and categories control?
3. How does X-Play automate operational responses?

## Hands-On Lab

Per-section walkthroughs — NCP-MCA. **Shared prerequisites** — Prism Central with
Self-Service (Calm) enabled. Concepts shown with API/spec snippets. **Cost:** none on
Community Edition where available.

### Lab 4.1 — Automation concepts and principles

**Objective:** Distinguish declarative from imperative automation.

```text
# Declarative blueprint (desired state): Self-Service reconciles to it.
# Imperative runbook (ordered steps): task1 -> task2 -> task3.
"blueprint = desired state; runbook = ordered tasks; playbook = trigger+actions"
```

**Expected result:** the correct mapping of blueprint/runbook/playbook — the concepts
section.

**Negative test:** script everything imperatively; **declarative blueprints** are
repeatable and self-documenting — prefer them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Deploy and configure Self-Service

**Objective:** Model a single-VM blueprint with a variable.

```text
# Self-Service blueprint (concept): a service with a variable and a provision action
service: WebServer
  substrate: AHV VM (2 vCPU, 4G), image=@@{os_image}@@   # macro/variable
  action Create: provision VM -> install package -> start service
```

**Expected result:** a parameterized blueprint deployable through **Self-Service** —
the deployment section.

**Negative test:** hard-code the image name; use a **macro/variable** so one blueprint
serves many environments.

**Rollback:** delete the blueprint/app if it was for the lab.

### Lab 4.3 — Validate blueprints, runbooks, and playbooks

**Objective:** Validate an X-Play playbook trigger/action.

```text
# X-Play playbook: WHEN alert "VM CPU > 90% for 10m" THEN scale-out / notify.
# Validate: dry-run the playbook; confirm trigger fires and action config resolves.
"validated: trigger=alert(CPU>90%) action=notify+runbook resolves"
```

**Expected result:** a validated playbook (trigger + action resolve) — the validation
section.

**Negative test:** publish without a dry-run; **validate** so a bad macro/credential
doesn't fail at runtime.

**Rollback:** disable the playbook if it was for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCP-MCA certifies automation on Nutanix across three sections: automation
concepts/principles, Self-Service deployment (blueprints, Projects, categories), and
validation of blueprints/runbooks/playbooks (X-Play).

- [ ] I can differentiate blueprints, runbooks, and playbooks.
- [ ] I can model a parameterized Self-Service blueprint.
- [ ] I can validate an X-Play playbook.
- [ ] I can scope automation with Projects/categories.
- [ ] I completed Labs 4.1–4.3 including each negative test.
