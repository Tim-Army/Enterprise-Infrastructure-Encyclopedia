# Chapter 08: Solution Architecture, Testing, and Governance

## Learning Objectives

- Explain the solution architect's role in scaling automation.
- Understand testing automations — and why automations need testing too.
- Place governance, security, and the unattended-robot risk surface.
- Recognize the operating disciplines that keep an automation program healthy.

*Cert relevance: architecture is the **Solution Architect Professional**; testing is the **Test Cloud Architect Professional**; governance runs through both.*

## The architect's role

A single automation is a developer's job; **an automation program is an architect's**. The **Automation Solution Architect Professional** designs how automation fits the enterprise: how automations share reusable components, how they integrate with the ERP/CRM/APIs, how the robot fleet is sized and scaled, how environments (dev/test/prod) are structured, and how it all stays reliable under load. The architect thinks in **systems**, not scripts — the difference between "this automation works" and "our automation *platform* scales to 500 processes without collapsing."

A recurring architectural discipline is **reuse**: shared libraries of common components (a login sequence, a standard error handler) so 200 automations do not each reinvent them — and so a fix to the shared login fixes all 200 (the [fix-at-the-source multiplier](../../volume-147-wiz-certifications/chapters/06-wiz-code-shift-left.md) again). The lab touches this within the governance exercise.

## Testing automations

Automations are **software**, and software needs **testing** — a point often missed until an untested automation silently processes 10,000 records wrong overnight. UiPath's **Test Suite** (and the new **Test Cloud Architect Professional** certification) covers this: unit-testing workflows, regression-testing that a change did not break existing automations, and testing against the applications the automation drives.

Testing matters *doubly* for unattended automation because there is **no human watching** — a bug in an interactive tool gets noticed when the user sees something wrong; a bug in an unattended 2 a.m. robot runs unnoticed until the damage is done. And automations are **fragile to their dependencies**: the app they drive gets an update, a selector breaks, and the automation fails — regression testing catches this before production does. The lab models the untested-change risk.

## Governance and the risk surface

An automation program is a **governance** responsibility, and unattended robots are a real **security surface**:

- **Credentials & access** — robots log into systems with real permissions. A fleet of robots with broad access is a large attack surface; the discipline is **least privilege** (each robot gets only the access its process needs), **centralized credentials** (in Orchestrator's vault, never hardcoded), and **audit** (who ran what, when).
- **Change control** — automations that touch financial or customer data need review, testing, and approval before deployment, like any production software.
- **Monitoring** — an automation program needs to know its robots' health, success rates, and exceptions, or failures accumulate silently.

This is the same least-privilege and audit discipline the [security volumes](../../volume-147-wiz-certifications/chapters/05-ciem-and-dspm-identity-and-data.md) teach, applied to a robot workforce — and it is why the **Center of Excellence** exists: to govern automation centrally rather than letting ungoverned bots proliferate. The lab models the least-privilege discipline for robots.

## Hands-On Lab

Python models governance and testing disciplines. **Cost:** none.

### Lab 8.1 — Least privilege for an unattended robot fleet

**Objective:** Scope each robot's access to only what its process needs.

```bash
python3 - <<'EOF'
# unattended robots, each running one process; what access does each NEED?
ROBOTS = [
  # robot,            process,              needs,                             over-provisioned grant
  ("robot-invoice",   "invoice entry",      ["ERP:AP:write", "email:read"],    ["ERP:ADMIN", "HR:read"]),
  ("robot-report",    "month-end report",   ["ERP:GL:read", "fileshare:write"],["ERP:ADMIN"]),
  ("robot-onboard",   "onboarding entry",   ["HR:write", "AD:createuser"],     ["AD:DOMAIN_ADMIN"]),
]
print("Unattended robots each log in with REAL permissions. Least privilege:\n")
for robot, proc, needs, over in ROBOTS:
    print(f"   {robot} ('{proc}')")
    print(f"      NEEDS (grant): {needs}")
    print(f"      over-provisioned (DENY): {over}")
    risk = "CRITICAL" if any("ADMIN" in o or "DOMAIN_ADMIN" in o for o in over) else "high"
    print(f"      if over-granted -> {risk}: a compromised/ buggy robot could do far more\n")
print("The discipline: each robot gets ONLY the access ITS PROCESS needs.")
print("  robot-invoice needs ERP accounts-payable WRITE — NOT ERP ADMIN, NOT HR.")
print("  robot-onboard needs to create AD users — NOT DOMAIN ADMIN.")
print("\nWhy it matters: an unattended robot fleet is a workforce with system access,")
print("running headless. If a robot is over-privileged and something goes wrong (a bug,")
print("a compromise, a bad input steering it), the blast radius is everything it CAN")
print("touch. Least privilege caps that blast radius to one process's scope.")
print("\nPlus: credentials live in ORCHESTRATOR's vault (never hardcoded in the")
print("workflow), and every run is AUDITED. Same least-privilege + centralized-secrets")
print("+ audit discipline as human identity governance (Wiz CIEM, CXLVII) — applied to")
print("a ROBOT workforce. Governing this is exactly why a Center of Excellence exists.")
EOF
```

**Expected result:** Each robot scoped to only its process's access, with admin/domain-admin grants denied as over-provisioning that would widen the blast radius. The least-privilege lesson is that an unattended robot fleet is a workforce with system access, so each robot gets only what its process needs, with centralized credentials and audit — the same identity-governance discipline applied to robots.

**Negative test:** Granting robots broad admin access "so they don't hit permission errors." An over-privileged headless robot's blast radius on a bug or compromise is everything it can touch — least privilege caps it to one process's scope.

**Cleanup:** None.

### Lab 8.2 — Why automations need regression testing

**Objective:** See how an untested change silently breaks production.

```bash
python3 - <<'EOF'
# an automation drives an app; the app updates and a selector breaks
print("An unattended automation processes 5,000 invoices/night. A change ships")
print("(the target app got a UI update; one selector now fails silently).\n")

NIGHTLY = 5000
print("WITHOUT regression testing:")
print("   the change deploys Friday. Nobody runs a test.")
broken = NIGHTLY * 3   # Fri, Sat, Sun before anyone notices Monday
print(f"   Fri/Sat/Sun the robot runs headless — the broken selector mis-files EVERY")
print(f"   invoice. No human is watching (it's unattended). By Monday: {broken:,} invoices")
print(f"   processed WRONG before anyone notices. Now it's a cleanup project.\n")

print("WITH regression testing (Test Suite):")
print("   the change triggers the automated test suite BEFORE deploy.")
print("   the test drives the automation against the updated app -> the broken")
print("   selector FAILS the test -> deployment is BLOCKED -> a dev fixes the selector.")
print(f"   invoices processed wrong: 0.\n")
print("The doubled stakes for UNATTENDED automation: there's NO human watching, so a")
print("bug runs unnoticed until the damage is done — a weekend of wrong processing")
print("before Monday. Automations are SOFTWARE, and they're FRAGILE to their")
print("dependencies (the apps they drive get updated and break selectors).")
print("\nRegression testing catches 'did this change break an existing automation?'")
print("BEFORE production does. Skipping it doesn't save time — it defers the cost to a")
print("bigger cleanup. This is why testing automations (Test Suite / Test Cloud")
print("Architect) is its own certification: at scale, untested automation is a")
print("liability, not an asset.")
EOF
```

**Expected result:** An untested selector break silently mis-processing a weekend of unattended invoices before anyone notices, versus a regression test blocking the deploy and yielding zero wrong records. The testing lesson is that automations are software fragile to their dependencies, and the stakes double for unattended runs with no human watching — regression testing catches breakage before production does.

**Negative test:** Deploying an automation change without regression testing because "it's just a small change." The app it drives may have shifted a selector; unattended, it processes a weekend of records wrong before Monday — testing before deploy is what prevents the silent-failure cleanup.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The solution architect's role understood as designing automation to scale across the enterprise, with reuse as a discipline.
- [ ] Testing automations understood as necessary software practice, doubly so for unwatched unattended runs.
- [ ] Governance and the unattended-robot risk surface understood — least privilege, centralized credentials, audit, change control.
- [ ] The Center of Excellence recognized as the body that governs automation centrally to keep the program healthy.
