# Chapter 02: Jira Administration — Projects and Schemes

## Learning Objectives

- Distinguish company-managed from team-managed projects — the defining Jira admin decision.
- Explain the scheme model: how workflows, permissions, and fields are shared across projects.
- Understand why shared configuration is Jira's power and its danger.
- Design a Jira instance that scales without becoming unmaintainable.

*Cert relevance: the core of **Jira Administration for Cloud** (ACP) — projects, schemes, workflows, permissions.*

## The defining decision: company-managed vs team-managed

The first and most consequential choice a Jira admin makes about any project is its type, and it is the concept the ACP exam most wants you to understand:

| | **Company-managed** | **Team-managed** |
|:---|:---|:---|
| Configured by | Jira administrators, centrally | The team itself, independently |
| Configuration | **Shared** via schemes across many projects | **Self-contained** in the one project |
| Consistency | Enforced org-wide | Per-team, varies |
| Best for | Scale, standardization, cross-project reporting | Team autonomy, speed, simple needs |
| The trade | Central control, slower change | Autonomy, configuration sprawl |

This is the same **standardization-versus-autonomy** axis [SAP's fit-to-standard](../../volume-144-sap-certifications/chapters/03-sap-activate-and-project-methodology.md) and [S/4HANA's cloud editions](../../volume-144-sap-certifications/chapters/02-s4hana-and-the-rise-context.md) drew, here at project scale. Company-managed projects share configuration through **schemes** — change a workflow once, every project using it updates — which is powerful for consistency and dangerous if you do not know which projects share what. Team-managed projects wall their configuration off — each team moves fast and independently, at the cost of no org-wide consistency and harder cross-project reporting.

An admin who defaults everything to team-managed gets speed and sprawl; one who defaults everything to company-managed gets consistency and a bottleneck. The skill is knowing which each project needs.

## The scheme model

Company-managed Jira's power is the **scheme** — a reusable configuration object shared across projects:

| Scheme | Controls |
|:---|:---|
| **Workflow scheme** | Which workflows apply to which issue types |
| **Permission scheme** | Who can do what in the project |
| **Notification scheme** | Who gets emailed on which events |
| **Issue type scheme** | Which issue types the project uses |
| **Field configuration scheme** | Which fields are required, hidden, or shown |

The critical property: **one scheme is shared by many projects.** A single permission scheme might govern fifty projects. This is the feature — configure once, apply everywhere, stay consistent — and the trap: **editing a shared scheme changes every project that uses it**, including the forty-nine you were not thinking about.

The lab models the discipline: **know a scheme's blast radius before you edit it**, the exact same lesson as [Akamai's shared-scheme edits](../../volume-143-akamai-certifications/README.md) and [Cloudflare's WAF rule order](../../volume-142-cloudflare-certifications/chapters/03-waf-rules-and-rate-limiting.md), in Jira's vocabulary.

## Scaling without sprawl

The failure mode of a large Jira instance is **scheme sprawl**: hundreds of nearly-identical workflows, permission schemes, and field configurations, each created because someone needed a tiny variation and cloned an existing one rather than reusing it. The result is an instance nobody can reason about, where changing anything risks breaking something unknown.

The discipline is **consolidation**: a small number of well-designed shared schemes that most projects reuse, with genuine variations kept few and documented. This is the same tidiness-as-maintainability argument as everywhere on this shelf — and it is what separates a Jira admin who keeps an instance healthy from one who presides over its decay.

## Hands-On Lab

Python models Jira administration. **Cost:** none. (The free Cloud tier makes it real.)

### Lab 2.1 — Company-managed vs team-managed, by need

**Objective:** Match project type to what the team actually requires.

```bash
python3 - <<'EOF'
PROJECTS = [
  # project,                     needs_cross_project_reporting, needs_org_consistency, wants_autonomy, complexity
  ("Finance (audited workflows)",  True,  True,  False, "high"),
  ("Marketing campaigns",          False, False, True,  "low"),
  ("Platform engineering",         True,  True,  False, "high"),
  ("A 3-person side project",      False, False, True,  "low"),
  ("Customer support (SLA-bound)", True,  True,  False, "high"),
]
print(f"{'project':32}{'x-proj rpt':>11}{'consistency':>12}{'autonomy':>10}   -> type")
for proj, cross_report, consist, auto, cx in PROJECTS:
    if consist or cross_report:
        t = "COMPANY-managed (shared schemes, central control)"
    else:
        t = "TEAM-managed (self-contained, fast)"
    print(f"{proj:32}{'yes' if cross_report else 'no':>11}{'yes' if consist else 'no':>12}{'yes' if auto else 'no':>10}")
    print(f"{'':65}-> {t}")
print("\nThe decision hinges on TWO questions:")
print("  need CROSS-PROJECT reporting or ORG CONSISTENCY? -> company-managed")
print("  want team AUTONOMY and speed, self-contained?    -> team-managed")
print("\nFinance and Support MUST be company-managed: audited workflows and SLAs")
print("require enforced, consistent, centrally-owned configuration. The 3-person")
print("side project should be team-managed — central schemes would be bureaucracy")
print("it does not need.")
print("\nThe admin anti-patterns, both real:")
print("  ALL company-managed -> every team waits on the admin for a field change")
print("  ALL team-managed    -> 200 projects, 200 workflows, zero consistency, no")
print("                         org-wide reporting possible. Choose per project.")
EOF
```

**Expected result:** Projects split between company-managed (audited/SLA-bound/cross-reporting) and team-managed (autonomous/simple), by the two deciding questions. The dual anti-pattern is the admin lesson — defaulting everything one way produces either a bottleneck or sprawl, and the skill is the per-project judgment.

**Negative test:** Making everything team-managed "so teams are happy." Cross-project reporting becomes impossible and the audited finance workflow has no enforced consistency — a compliance problem.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — A scheme's blast radius

**Objective:** Know what an edit touches before making it.

```bash
python3 - <<'EOF'
# One permission scheme shared across many projects
SCHEME_USAGE = {
  "Default Software Scheme":  ["PLAT", "MOBILE", "WEB", "API", "DATA", "INFRA"],
  "Finance Restricted":       ["FIN", "AUDIT"],
  "Open Collaboration":       ["MKT", "DESIGN", "DOCS"],
}
EDIT = ("Default Software Scheme", "add 'anyone can delete issues' permission")
scheme, change = EDIT
affected = SCHEME_USAGE[scheme]
print(f"Requested edit: {scheme}")
print(f"  change: {change}\n")
print(f"This scheme is shared by {len(affected)} projects:")
for p in affected: print(f"   {p}")
print(f"\nThe edit applies to ALL {len(affected)}, not just the one project whose")
print("admin requested it. 'anyone can delete issues' on PLAT also lands on")
print("INFRA and DATA — where deleted issues might be audit records.")
print("\nBefore ANY scheme edit, the admin's question is: WHICH PROJECTS SHARE THIS?")
print("The answer here is 6, and two of them (DATA, INFRA) probably should not get")
print("this permission at all. The correct move is likely a SEPARATE scheme for the")
print("one project that needs the change — not editing the shared one.")
print("\nThis is Jira's version of the shared-configuration trap that recurs across")
print("this whole shelf (Akamai schemes, Cloudflare rules, SAP transport): the")
print("power of 'configure once, apply everywhere' IS the danger of 'edit once,")
print("break everywhere.' Blast radius first, edit second.")
EOF
```

**Expected result:** A permission edit intended for one project landing on all six that share the scheme, including two where it is dangerous. The blast-radius-first discipline is the transferable lesson — shared configuration means an edit's scope is every consumer of the scheme, and the fix for a one-project need is often a new scheme, not a shared edit.

**Negative test:** Editing the shared scheme to satisfy one project's request. The other five inherit the change, and the audit-record projects just became deletable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Scheme sprawl and consolidation

**Objective:** Quantify the cost of clone-instead-of-reuse.

```bash
python3 - <<'EOF'
import random
random.seed(29)
# 80 projects, each got a workflow either reused or cloned-with-tweaks
projects = []
base_workflows = ["Software Dev", "Simple Task", "Bug Triage"]
for i in range(80):
    if random.random() < 0.55:      # cloned "just for a small tweak"
        projects.append(f"cloned-workflow-{i}")
    else:
        projects.append(random.choice(base_workflows))
from collections import Counter
counts = Counter(projects)
unique = len(counts)
cloned = sum(1 for w in counts if w.startswith("cloned"))
print(f"80 projects, {unique} distinct workflows in the instance.")
print(f"  {len(base_workflows)} well-designed shared workflows, reused by many projects")
print(f"  {cloned} one-off cloned workflows, each used by ~1 project\n")
reused_projects = sum(c for w, c in counts.items() if not w.startswith("cloned"))
print(f"{reused_projects} projects share {len(base_workflows)} workflows (healthy).")
print(f"{cloned} projects each have their OWN workflow (sprawl).")
print("\nThe sprawl cost is not storage — it is COMPREHENSIBILITY. An admin facing")
print(f"{unique} workflows cannot reason about the instance: 'if I change the bug")
print("process, which projects are affected?' has no knowable answer when every")
print("project cloned its own.")
print("\nConsolidation target: a SMALL set of shared workflows most projects reuse,")
print("with genuine exceptions kept few and documented. The 44 clones above are")
print("almost all 'I needed one extra status' — solvable by adding that status to")
print("a shared workflow (behind a condition) rather than cloning the whole thing.")
print("\nThis is the difference between a Jira instance that stays healthy for years")
print("and one that becomes the system nobody dares touch. The ACP exam tests the")
print("design judgment; the instance tests whether you applied it.")
EOF
```

**Expected result:** 80 projects fragmenting into dozens of workflows because most were cloned for minor tweaks, versus a healthy handful of shared ones. The comprehensibility cost is the point — sprawl's damage is not storage but the loss of the ability to reason about change impact, which is exactly what makes a large instance unmaintainable.

**Negative test:** Cloning a workflow every time a project wants one small variation. Within a year the instance has a workflow per project and no admin can predict what any change affects.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Company-managed and team-managed projects distinguished by the standardization/autonomy trade.
- [ ] The scheme model understood: shared configuration is Jira's power and its blast-radius danger.
- [ ] Scheme edits preceded by a blast-radius check; one-project needs met with new schemes.
- [ ] Scheme sprawl recognized as a comprehensibility cost, with consolidation as the discipline.
