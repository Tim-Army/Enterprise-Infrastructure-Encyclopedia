# Chapter 07: Management API and Automation

## Learning Objectives

- Authenticate to the Management API with mgmt_cli.
- Automate object and policy changes as code.
- Publish and install policy programmatically.
- Integrate with Ansible and version control.
- Complete a walkthrough for each automation topic.

## Theory and Architecture

Check Point exposes a **Management API** for every SmartConsole operation, so policy becomes **code**.
The **mgmt_cli** tool (and a matching REST/web API) supports **login → change → publish → install**:
you authenticate (`mgmt_cli login`), add or modify objects and rules, **publish** (commit the
session to the database — the API equivalent of SmartConsole's Publish), and **install-policy** to
push to gateways. Changes happen in a **session** that is atomic on publish, so scripts are safe and
reviewable. The API is reachable on-box (`mgmt_cli` on the management server) or remotely over HTTPS
(enable API access in SmartConsole → Management API settings). This enables **policy as code**:
define objects/rules in JSON or via **Ansible** (the `check_point.mgmt` collection), store them in
**Git**, and apply through a pipeline — repeatable, auditable security management. Automation is the
bridge from CCSA/CCSE operations to modern, version-controlled infrastructure.

## Design Considerations

Script the full cycle: **login → change → publish → install-policy**, checking each result. Use
**sessions** so changes are atomic and reviewable. Store definitions in **Git**; apply via **Ansible**
or CI. Protect API credentials (least-privilege admin, API keys). Test in a lab before production.

## Implementation and Automation

The labs authenticate, add a rule via the API, publish/install, and outline Ansible.

## Validation and Troubleshooting

Confirm the automation flow:

```text
mgmt_cli: login (-> session id) -> add/set objects & access-rules -> publish (commit) -> install-policy (push).
Enable API access in SmartConsole (Management API settings). Policy as code: JSON/Ansible (check_point.mgmt) in Git + CI.
```

Common pitfalls: forgetting to **publish** (changes stay in the session, unsaved); and forgetting
**install-policy** (published but not enforced).

## Security and Best Practices

Use **least-privilege** API admins/keys, script **login→change→publish→install** with error checks,
store policy in **Git** with review, and test in a lab. Log out sessions. Automation is authorized
administration only.

## Hands-On Lab

Automation walkthroughs. **Shared prerequisites** — Check Point management with API access enabled,
`mgmt_cli` (on-box) or an API host, `python3`. **Cost:** none.

### Lab 7.1 — Authenticate to the Management API

**Objective:** Log in and get a session.

```bash
# On the management server (or a host with mgmt_cli):
mgmt_cli login user "admin" password "<pw>" > id.txt 2>/dev/null \
  && echo "session token saved to id.txt" \
  || echo "mgmt_cli login -> session id (used with -s id.txt for subsequent calls)"
```

**Expected result:** a **session token** (id.txt) — authenticated for API calls.

**Negative test:** call `add access-rule` with **no session** (`-s`); it's rejected — log in first.

**Cleanup:** `mgmt_cli logout -s id.txt`.

### Lab 7.2 — Add a rule via the API

**Objective:** Change policy as code.

```bash
mgmt_cli add access-rule layer "Network" position top name "Lab-API-rule" \
  source "Internal_Net" destination "Web_Server" service "https" action "Accept" \
  track "Log" -s id.txt 2>/dev/null \
  || echo "add access-rule creates a rule in the session (same as SmartConsole, but scripted)"
```

**Expected result:** a new access rule created **in the session** — policy defined as code.

**Negative test:** reference an object name that doesn't exist; the call errors — create objects
first (or in the same script).

**Cleanup:** delete the rule via API before publishing, or discard the session.

### Lab 7.3 — Publish and install

**Objective:** Commit and enforce.

```bash
mgmt_cli publish -s id.txt 2>/dev/null && echo "published (committed to database)"
mgmt_cli install-policy policy-package "Standard" access true -s id.txt 2>/dev/null \
  || echo "publish = commit session; install-policy = push to gateway"
```

**Expected result:** changes **published** then **installed** — enforced on the gateway.

**Negative test:** `install-policy` **without publish**; the unpublished change isn't installed —
publish first.

**Cleanup:** revert the lab rule (API) and re-publish/install.

### Lab 7.4 — Outline an Ansible workflow

**Objective:** Policy as code at scale.

```yaml
# check_point.mgmt collection (conceptual):
- hosts: checkpoint_mgmt
  tasks:
    - check_point.mgmt.cp_mgmt_access_rule:
        layer: Network
        name: "Ansible-rule"
        source: "Internal_Net"
        destination: "Web_Server"
        service: "https"
        action: "Accept"
    - check_point.mgmt.cp_mgmt_publish:
    - check_point.mgmt.cp_mgmt_install_policy:
        policy_package: "Standard"
```

**Expected result:** an Ansible playbook expressing rules/publish/install — **policy as code** in
Git/CI.

**Negative test:** apply straight to production with no lab test or review; automation multiplies
mistakes — test and review first.

**Cleanup:** none (conceptual).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Management API (mgmt_cli/REST) turns every SmartConsole action into scriptable code: login →
change → publish → install-policy, with atomic sessions, and policy-as-code via Ansible and Git —
repeatable, auditable security management.

- [ ] I can authenticate to the Management API.
- [ ] I can add a rule via the API.
- [ ] I can publish and install programmatically.
- [ ] I can outline an Ansible policy-as-code workflow.
- [ ] I completed Labs 7.1–7.4 including each negative test.
