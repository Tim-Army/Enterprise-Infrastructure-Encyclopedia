# Chapter 04: The Control Room

## Learning Objectives

- Describe the Control Room as the central hub for deploying and governing bots.
- Deploy and schedule bots to Bot Runners, attended and unattended.
- Secure automations with the Credential Vault and role-based access control.
- Understand audit, versioning, and governance at scale.

*Cert relevance: Control Room deployment and governance are core to the Advanced certification.*

## The central hub

The **Control Room** is the web-based **command center** of Automation 360 ([Ch 2](02-automation-success-platform.md)). Developers build bots in Bot Creators, but everything else — **storing, deploying, scheduling, securing, monitoring, and governing** them — happens in the Control Room. If a bot is the automation, the Control Room is the **operating system** that runs a fleet of them across an enterprise: who can build, where bots run, which credentials they use, when they execute, and what happened.

At small scale you could run a bot by hand; at enterprise scale — hundreds of bots, dozens of runners, many teams — you need **central orchestration and governance**, and that is exactly what the Control Room provides. The Advanced certification expects you to operate it. The lab models Control Room orchestration.

## Deploying and scheduling

The Control Room turns a stored bot into **running work**:

- **Deploy** a bot to one or more **Bot Runners** (the licensed execution devices). The Control Room dispatches the bot and tracks its run.
- **Schedule** bots to run at set times (nightly at 02:00) or **trigger** them on events (a file arrives, an email lands, an API call, a queue item appears).
- **Work queues** — feed a bot a **queue of items** (invoices, records) and let the Control Room distribute the work across multiple runners for **parallel** processing, tracking each item's status.

This is orchestration: matching **work** to **runners**, on the right schedule or trigger, at the scale needed. Getting throughput right — enough runners, good queue design — is core operational skill. The lab dispatches a work queue across runners.

## The Credential Vault and RBAC

Automations handle **secrets** — passwords, API keys, tokens for the systems they drive. Hardcoding those in bots is a serious risk. The Control Room provides **secure governance**:

- **Credential Vault** — a central, encrypted store for secrets. Bots **reference** a credential by name; the Control Room **injects** the actual value at runtime, so the secret never lives in the bot. Rotate the password once in the vault and every bot picks up the change.
- **Role-Based Access Control (RBAC)** — roles and permissions decide who can **create** bots, who can **deploy** them, who can **run** them, and who can **administer** the platform. A developer builds; an operator deploys; an admin governs — least privilege throughout.
- **Lockers** — group credentials and control which roles/bots can use them.

Together these make automation **secure by default**: secrets are vaulted, access is least-privilege, and no bot carries a plaintext password. The lab uses the vault and RBAC.

## Audit, versioning, and governance at scale

At enterprise scale the Control Room provides the controls that make automation **auditable and safe to change**:

- **Audit log** — every action (who deployed what, when a bot ran, who changed a credential) is recorded for compliance and troubleshooting.
- **Version control** — bots are versioned; you can review changes, roll back, and promote through environments (Dev → Test → Prod).
- **Monitoring and alerts** — dashboards show running/failed automations, and alerts surface problems early.
- **Governance boundaries** — separate the fleet by business unit or environment so teams operate independently under central policy.

This is what separates a governed automation **program** from a pile of scripts: accountability, change control, and visibility. It is also the difference the Advanced certification tests. The lab records an audit trail. *(These governance concerns mirror those in every enterprise automation platform — e.g. [UiPath Orchestrator (CXLIX)](../../volume-149-uipath-certifications/README.md).)*

## Hands-On Lab

Python models the Control Room — deploy, work queues, the vault, RBAC, and audit. **Cost:** none.

### Lab 4.1 — Orchestrate and govern from the Control Room

**Objective:** Dispatch a work queue across runners, inject a vaulted credential under RBAC, and audit it.

```bash
python3 - <<'EOF'
# Control Room: work queue -> Bot Runners, with Credential Vault + RBAC + audit log
VAULT = {"erp_password": "s3cret-injected-at-runtime"}     # never stored in the bot
ROLES = {"dev": {"create"}, "operator": {"deploy", "run"}, "admin": {"create","deploy","run","govern"}}
audit = []

def can(role, action):
    ok = action in ROLES.get(role, set())
    audit.append(f"{role} {action}: {'ALLOW' if ok else 'DENY'}")
    return ok

def deploy_queue(role, bot, items, runners):
    if not can(role, "deploy"):
        return f"DENY: role '{role}' cannot deploy"
    # distribute queue items across runners (parallel), inject the vaulted credential
    cred = VAULT["erp_password"]
    assignments = {r: [] for r in runners}
    for i, item in enumerate(items):
        assignments[runners[i % len(runners)]].append(item)
    audit.append(f"deployed '{bot}' to {runners} with vaulted credential (injected, not stored)")
    return assignments

print("CONTROL ROOM — orchestrate + govern:\n")
print("1) RBAC check + deploy a work queue across 2 runners (as 'operator'):")
items = [f"invoice-{n}" for n in range(1, 6)]
result = deploy_queue("operator", "bot_invoice", items, ["runner-A", "runner-B"])
for r, its in result.items():
    print(f"      {r}: {its}")

print("\n2) RBAC denies an over-privileged action (dev tries to govern):")
print(f"      dev can govern? {can('dev', 'govern')}")

print("\n3) CREDENTIAL VAULT: bot references 'erp_password'; value injected at runtime, never in the bot.")

print("\n4) AUDIT LOG (every action recorded):")
for line in audit:
    print(f"      {line}")
print()
print("The CONTROL ROOM dispatches a WORK QUEUE across Bot RUNNERS for parallel processing,")
print("injects secrets from the CREDENTIAL VAULT at runtime (never stored in the bot), enforces")
print("RBAC (operator deploys/runs; only admin governs), and records every action in the AUDIT")
print("LOG. Central orchestration + governance is what makes automation enterprise-grade — and")
print("the core of the Advanced certification.")
EOF
```

**Expected result:** The Control Room deploys a five-item work queue split across two runners (as an authorized operator), denies a developer's attempt to govern (RBAC), injects a vaulted ERP credential at runtime, and records every action in the audit log. The lesson is Control Room orchestration and governance: distribute work across runners, vault secrets and inject them at runtime, enforce least-privilege RBAC, and audit everything — the enterprise-grade operation the Advanced certification validates.

**Negative test:** Hardcoding the ERP password in the bot and letting anyone deploy. The secret leaks into every copy and audit/version history, and there is no least-privilege control; the Credential Vault plus RBAC and the audit log are what make an automation fleet secure and governable.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Control Room understood — the central hub for storing, deploying, and governing bots.
- [ ] Deployment and scheduling understood — dispatching to Bot Runners, schedules, triggers, and work queues.
- [ ] The Credential Vault and RBAC understood — vaulted secrets injected at runtime, least-privilege roles.
- [ ] Audit, versioning, and governance understood — accountability and change control at scale.

## See also

- [Chapter 03 — Building Bots](03-building-bots.md) — the bots the Control Room deploys.
- [Chapter 05 — Attended, Unattended, and Automation Co-Pilot](05-attended-unattended-and-copilot.md) — how those deployments are triggered and assisted.
- [Chapter 08 — Process Discovery, Bot Insight, and the CoE](08-process-discovery-and-coe.md) — measuring and scaling the governed fleet.
