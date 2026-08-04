# Chapter 08: IdentityIQ On-Premises

## Learning Objectives

- Describe IdentityIQ's architecture, installation, and build/deploy model.
- Map IdentityIQ vocabulary to Identity Security Cloud equivalents.
- Onboard an application and use Lifecycle Manager.
- Debug and troubleshoot an IdentityIQ deployment.

## Why IdentityIQ still matters

**IdentityIQ (IIQ)** is SailPoint's on-premises product, and it carries two of the four Professional Certifications — the **Associate** and the **Engineer**. Many large regulated organizations run it because their governance data or their systems cannot leave the premises. If you work in one of those shops, this is your track.

The IdentityIQ Engineer exam covers **installation, build and deployment; Lifecycle Manager; Identity Governance; custom development; application onboarding; debugging and troubleshooting; and data and access modeling** — a noticeably more infrastructural blueprint than the ISC exams, because with on-premises software you own the deployment too.

The Associate exam is scoped differently: it serves as the final exam for the *IdentityIQ Introduction* and *IdentityIQ Essentials* courses, covering foundational concepts, applications, identity modeling, access modeling, governance, user-driven requests, and provisioning.

## Vocabulary mapping

The governance concepts are the same across both products; the names differ. Knowing both is genuinely useful, since job descriptions and colleagues mix them freely.

| IdentityIQ | Identity Security Cloud | Concept |
|:---|:---|:---|
| **Identity Cube** | Identity | The person and all their correlated accounts/attributes |
| **Application** | Source | A connected system |
| **Business role / IT role** | Role / access profile | The access model layers |
| **Certification** | Campaign | Access review |
| **Lifecycle Manager (LCM)** | Request Center / lifecycle | Requests, approvals, JML automation |
| **Task / Quartz schedule** | Scheduled operation | Aggregation, refresh, and other background work |
| **Rule (BeanShell)** | Rule / transform | Extension logic |

## Architecture

IdentityIQ is a Java web application you run yourself:

| Layer | What you provide |
|:---|:---|
| **Application server** | Tomcat (or another supported container) |
| **Database** | The IdentityIQ schema (SQL Server, Oracle, MySQL) |
| **JVM** | Supported Java runtime |
| **Connectors** | To your applications, direct from the IIQ host |

Because you own all of it, capacity, patching, backup, and high availability are yours as well — the trade you accept for keeping identity data on-premises.

## Build and deploy

IdentityIQ deployments are managed as versioned artifacts, not by clicking in the UI:

1. **Install** the base product and initialize the database schema.
2. **Configure** as XML objects (applications, rules, roles, workflows) held in **source control**.
3. **Build** a deployable artifact from that configuration.
4. **Deploy** by importing the objects into the target environment (dev → test → prod).
5. **Patch/upgrade** on SailPoint's release cadence, re-testing customizations.

The discipline this enforces — configuration as versioned, reviewable artifacts promoted through environments — is exactly what the Engineer exam's "installation, build and deployment" domain is checking.

## Hands-On Lab

Python models IdentityIQ operational concepts. **Cost:** none.

### Lab 8.1 — Map IdentityIQ to ISC vocabulary

**Objective:** Translate fluently between the two products.

```bash
python3 - <<'EOF'
mapping = {
  "Identity Cube":"Identity", "Application":"Source", "Business role":"Role",
  "IT role":"Access profile", "Certification":"Campaign", "Lifecycle Manager":"Request Center",
  "Task":"Scheduled operation", "Rule (BeanShell)":"Rule / transform",
}
print(f"{'IdentityIQ (on-prem)':24} {'Identity Security Cloud':24}")
print("-"*50)
for iiq, isc in mapping.items():
    print(f"{iiq:24} {isc:24}")
print("\nSame governance concepts, different product vocabulary — know both.")
EOF
```

**Expected result:** A clean two-column translation table. The value is practical: an IdentityIQ engineer moving to ISC already understands identity cubes, certifications, and business roles — the learning curve is vocabulary and platform mechanics (Chapter 06), not governance theory (Chapters 02–05).

**Negative test:** Assuming the products are unrelated and re-learning governance from scratch — the concepts transfer almost entirely, which is why SailPoint's own training paths mirror each other across both product lines.

**Cleanup:** None.

### Lab 8.2 — Model the build-and-deploy pipeline

**Objective:** Promote configuration through environments safely.

```bash
python3 - <<'EOF'
def promote(artifact, from_env, to_env, tested, in_source_control, approved):
    if not in_source_control:
        return f"BLOCKED: {artifact} is not in source control — untracked config cannot be promoted"
    if not tested:
        return f"BLOCKED: {artifact} not tested in {from_env}"
    if to_env == "prod" and not approved:
        return f"BLOCKED: {artifact} needs change approval for prod"
    return f"PROMOTED: {artifact} {from_env} -> {to_env}"

cases = [
  ("app-AD.xml",      "dev","test", True,  True,  False),
  ("role-model.xml",  "test","prod",True,  True,  True),
  ("hotfix-rule.xml", "dev","prod", False, True,  True),
  ("ui-config-tweak",  "dev","test", True,  False, False),
]
for c in cases: print(promote(*c))
print("\nUI-only changes are the trap: made directly in prod, they vanish at the next deploy.")
EOF
```

**Expected result:** Two promotions succeed; the untested hotfix and the untracked UI tweak are blocked. The closing line names the classic IdentityIQ operational failure — configuration changed directly in the production UI is not in the artifact, so the next deployment silently reverts it and nobody can explain why the behavior changed.

**Negative test:** Treating IdentityIQ as a UI-configured appliance — with no source control you cannot reproduce an environment, diff a change, or roll back a bad one.

**Cleanup:** None.

### Lab 8.3 — Debug a failing aggregation task

**Objective:** Work the IdentityIQ troubleshooting fault tree.

```bash
python3 - <<'EOF'
def debug(task_started, connector_ok, db_ok, rule_error, memory_ok):
    if not task_started: return "Task never started — check the Quartz scheduler and task definition"
    if not connector_ok: return "Connector failure — check application config, credentials, network path"
    if not db_ok:        return "Database error — check the IIQ datasource, connection pool, and DB health"
    if rule_error:       return "Rule exception — check the BeanShell rule and iiq.log stack trace"
    if not memory_ok:    return "JVM out of memory — increase heap or reduce aggregation batch size"
    return "Aggregation completed successfully"

cases = [
  ("nightly-AD-agg",   True,  True, True,  False, True),
  ("hr-full-agg",      True,  True, False, False, True),
  ("scheduled-refresh",False, True, True,  False, True),
  ("bulk-identity-refresh", True, True, True, False, False),
]
for name, *state in cases:
    print(f"{name:24} -> {debug(*state)}")
print("\nStart with iiq.log; the stack trace usually names the layer before you guess at it.")
EOF
```

**Expected result:** Each failure maps to a distinct layer — scheduler, connector, database, rule, JVM. On-premises operation adds failure modes ISC administrators never see (JVM heap, Quartz scheduling, datasource pools), which is why the Engineer blueprint calls out debugging and troubleshooting explicitly. The habit that matters: read `iiq.log` first; the stack trace names the layer.

**Negative test:** Re-running the failed task hoping it passes — a heap exhaustion or a bad rule reproduces every time, and you have spent an hour confirming the failure rather than reading the log.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] IdentityIQ architecture (Tomcat, database, JVM, connectors) described.
- [ ] IdentityIQ ↔ ISC vocabulary mapped in both directions.
- [ ] Build/deploy promotion modeled, with configuration under source control.
- [ ] Aggregation failures debugged by layer, starting from the log.
