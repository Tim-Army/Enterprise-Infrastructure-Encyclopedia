# Chapter 08: Operationalizing Wiz

## Learning Objectives

- Explain Posture Issues — grouping findings into actionable outcomes.
- Understand democratization — putting security in developers' hands.
- Describe policies, guardrails, and ownership routing.
- Recognize the operating model that makes a CNAPP actually reduce risk.

*Cert relevance: operationalizing — turning findings into fixed issues at scale — is what separates a tool that *reports* risk from one that *reduces* it, and it runs through the higher exams.*

## From findings to Posture Issues

A raw CNAPP can generate an overwhelming number of findings — thousands of vulnerabilities, secrets, and data issues. **Posture Issues** (a Wiz capability) group related findings into a single **actionable outcome**: instead of 400 separate "vulnerable log4j" findings across 400 containers, one Posture Issue — "log4j RCE across the payment service, here are the 400 instances, here is the one base image to fix." Grouping converts a *backlog* into a *to-do list*.

This is the operational face of the whole graph philosophy: the graph already knows these 400 findings share a cause (one base image) and a blast radius (the payment service), so it presents them as one unit of work with one owner and one fix. The lab models grouping and its effect on the queue.

## Democratization

The second operational idea is **democratization** — putting security findings directly in front of the **developers and teams who own the resources**, rather than funneling everything through a central security team that becomes a bottleneck. Because the graph knows *who owns* each resource (from tags, accounts, and code ownership), Wiz can **route** each Posture Issue to the team that can actually fix it, in the tools they already use (Jira, Slack, the PR).

The shift is from "security is a gate the security team enforces" to "security is context the owning team acts on." A central team of ten cannot review every deployment for a thousand developers; but if every developer sees the security implications of *their own* change, in *their own* workflow, security scales with the organization. This is the same **self-service** principle the [Jamf Self Service (CXLVI)](../../volume-146-jamf-certifications/chapters/05-scripts-self-service-and-app-deployment.md) and [Atlassian (CXLV)](../../volume-145-atlassian-certifications/README.md) volumes teach: publish the context, let owners act, keep the central team for governance not gatekeeping. The lab models the bottleneck math.

## Policies and guardrails

The governance layer is **policies** — the rules that define what "secure" means for your org (which configurations are forbidden, which vulnerabilities block a deploy, which data must be encrypted) — enforced as **guardrails** across the pipeline: a policy can *warn* in the IDE, *fail* a pull request (Wiz Code), *flag* in the cloud (Wiz Cloud), and *alert* at runtime (Wiz Defend) — the same rule at every stage. The central team's job becomes writing and tuning policy; the enforcement and remediation are distributed. The lab is covered within the two below.

## Hands-On Lab

Python models the operating model. **Cost:** none.

### Lab 8.1 — Group findings into Posture Issues

**Objective:** Convert a flat backlog into a small set of owned, actionable units.

```bash
python3 - <<'EOF'
import random
random.seed(20)
# 600 raw findings, but they share a small number of root causes
ROOT_CAUSES = [
  ("log4j RCE",        "base-image: java-app:1.0", "payments-team",   180),
  ("hardcoded API key","secret in repo web-svc",   "web-team",         12),
  ("public bucket",    "modules/storage/main.tf:42","platform-team",   140),
  ("over-privileged role","modules/iam/admin.tf:9", "platform-team",   210),
  ("outdated openssl", "base-image: base-os:2.3",   "platform-team",    58),
]
total = sum(c[3] for c in ROOT_CAUSES)
print(f"RAW: {total} individual findings across the estate. A wall of alerts.\n")
print("GROUPED into Posture Issues (by shared root cause):")
print(f"   {'issue':22}{'instances':>10}{'owner':>16}   one fix")
for name, cause, owner, count in sorted(ROOT_CAUSES, key=lambda x: -x[3]):
    print(f"   {name:22}{count:>10}{owner:>16}   {cause}")
print(f"\n   {total} findings  ->  {len(ROOT_CAUSES)} Posture Issues")
print(f"   reduction: {total} alerts collapse to {len(ROOT_CAUSES)} units of work")
# routing
from collections import Counter
by_owner = Counter()
for name, cause, owner, count in ROOT_CAUSES: by_owner[owner] += 1
print("\n   routed to owners:")
for owner, n in by_owner.items():
    print(f"      {owner:16} {n} issue(s) to fix")
print("\nGrouping converts a BACKLOG into a TO-DO LIST. 600 scattered findings are")
print("paralyzing; 5 Posture Issues — each with a single root cause, a single owner,")
print("and one fix that clears all its instances — are a sprint. The graph already")
print("knows the 180 log4j findings share ONE base image and ONE team, so it presents")
print("them as ONE issue. Fix the base image once, 180 findings clear. That's the")
print("difference between a tool that REPORTS risk and one that REDUCES it.")
EOF
```

**Expected result:** Hundreds of raw findings collapsing into a handful of Posture Issues, each with one root cause, one owner, and one fix that clears all its instances, routed to the owning team. The grouping lesson is that the graph knows which findings share a cause and blast radius, turning a paralyzing backlog into a short, owned to-do list — the operational difference between reporting risk and reducing it.

**Negative test:** Working findings individually. Fixing 180 log4j instances one container at a time is hopeless and misses that they share one base image — grouping fixes the cause once and clears all 180.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Democratization beats the central bottleneck

**Objective:** Show why routing to owners scales where a central team cannot.

```bash
python3 - <<'EOF'
DEVELOPERS = 1000
DEPLOYS_PER_DAY = 400
SEC_TEAM = 10
REVIEW_MIN = 20   # minutes for a security person to review one deploy

# Central-gate model: security team reviews every deploy
sec_capacity_per_day = SEC_TEAM * 6 * 60 / REVIEW_MIN   # 6 productive hours each
print("CENTRAL-GATE model (security team reviews every deploy):")
print(f"   {DEPLOYS_PER_DAY} deploys/day need review; team can do {sec_capacity_per_day:.0f}/day")
backlog = DEPLOYS_PER_DAY - sec_capacity_per_day
print(f"   -> capacity {sec_capacity_per_day:.0f} vs demand {DEPLOYS_PER_DAY}: "
      f"{'BOTTLENECK, backlog grows by %.0f/day' % backlog if backlog>0 else 'ok'}")
print("   security becomes the thing everyone waits for; devs route around it.\n")

# Democratized model: owners see their own issues; central team writes policy
print("DEMOCRATIZED model (Wiz routes each issue to the owning team):")
print(f"   each of {DEVELOPERS} devs sees the security context of THEIR OWN change,")
print("   in THEIR OWN workflow (PR/Slack/Jira). No central queue to wait on.")
print(f"   the {SEC_TEAM}-person team writes/tunes POLICY (guardrails) instead of")
print("   reviewing every deploy — enforcement is distributed, governance is central.")
print("   -> throughput scales with the DEV org, not the security headcount.")
print("\nA central team of 10 cannot gate 400 deploys/day for 1000 developers — the")
print("math doesn't work, and 'security reviews everything' becomes 'security blocks")
print("everything.' Democratization flips it: the graph knows who OWNS each resource,")
print("so it routes each Posture Issue to the team that can fix it, with the context")
print("to act. The central team moves from GATEKEEPER to policy author. That's how")
print("security scales in the cloud — and why Wiz emphasizes putting it in dev hands.")
EOF
```

**Expected result:** A central security team's review capacity falling far short of daily deploy volume (a growing bottleneck), versus a democratized model where each owner handles their own issues and the central team writes policy — throughput scaling with the dev org rather than security headcount. The democratization lesson is that central gating cannot scale to cloud deploy velocity, so routing issues to owners with context is the operating model that actually reduces risk.

**Negative test:** Scaling security by making the central team the mandatory reviewer of every deploy. At 400 deploys/day against 10 reviewers, the queue only grows — security becomes the bottleneck teams route around, the opposite of the goal.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Posture Issues understood as grouping related findings into single, owned, actionable outcomes.
- [ ] Democratization understood as routing issues to owning teams in their own workflow, with the central team writing policy.
- [ ] Policies and guardrails understood as one rule enforced at every pipeline stage (IDE, PR, cloud, runtime).
- [ ] The operating model recognized as what turns a CNAPP from a report generator into a risk reducer.
