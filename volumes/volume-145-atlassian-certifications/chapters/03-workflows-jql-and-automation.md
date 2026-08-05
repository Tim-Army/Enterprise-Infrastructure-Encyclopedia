# Chapter 03: Workflows, JQL, and Automation

## Learning Objectives

- Design Jira workflows — statuses, transitions, conditions, validators, post-functions.
- Query the instance with JQL, and understand what makes a query fast or slow.
- Build automation rules that reduce manual work without creating loops.
- Recognize the over-engineering failure mode in each.

*Cert relevance: workflows, JQL, and automation are heavily weighted in **Jira Administration for Cloud** (ACP) and appear in the ACA project-management certification.*

## Workflows

A Jira **workflow** is the lifecycle an issue moves through — **statuses** (To Do, In Progress, Done) connected by **transitions**. What makes workflows an administration skill rather than a drawing exercise is what hangs off the transitions:

| Element | Does | Example |
|:---|:---|:---|
| **Condition** | Controls *who can even see* a transition | Only assignee can move to In Progress |
| **Validator** | Checks the transition is *allowed to complete* | Resolution required before Done |
| **Post-function** | Acts *after* a successful transition | Auto-assign, set a field, fire a webhook |

The design discipline is **model the real process, then stop.** The commonest workflow mistake is over-engineering: fifteen statuses, mandatory fields at every transition, conditions nobody understands — a workflow so elaborate that teams route around it (marking things Done that are not, because the "correct" path is too painful). A workflow that people fight is worse than a simple one they follow, the same lesson as [SAP's fit-to-standard](../../volume-144-sap-certifications/chapters/03-sap-activate-and-project-methodology.md): match the tool to how work actually happens, not to an idealized process.

## JQL

**Jira Query Language** is how you ask the instance questions — `project = PLAT AND status = "In Progress" AND assignee = currentUser() ORDER BY priority DESC`. It powers filters, boards, dashboards, and reports, which makes it the connective tissue of Jira the way [NRQL is for New Relic](../../volume-141-newrelic-certifications/chapters/03-nrql.md) or [DQL for Dynatrace](../../volume-140-dynatrace-certifications/chapters/03-grail-dql-and-dpl.md).

The performance discipline is the same one those languages teach: **narrow first.** A JQL query that filters on an indexed field (project, status, assignee) before an expensive one (text search, custom-field scans) returns fast; one that scans all issues before narrowing is slow, and a slow query behind a dashboard everyone loads is slow *repeatedly*. The lab quantifies it.

## Automation

Jira's **automation rules** — trigger, conditions, actions — remove manual toil: auto-transition when a linked issue closes, notify on SLA breach, sync fields across issues. The value is real; the danger is two-fold and both appear in the lab:

1. **Loops.** Rule A edits an issue, which triggers Rule B, which edits it back, triggering Rule A. Automation platforms guard against infinite loops, but a rule that fires far more than intended is a subtler, real cost.
2. **Invisible logic.** Automation that "just happens" becomes undocumented behavior nobody can explain — "why did this ticket auto-close?" with no obvious cause. Automation is code; it needs the same ownership, naming, and review as any other configuration (the [fixture-drift discipline](../../volume-142-cloudflare-certifications/chapters/08-operating-cloudflare-api-terraform-and-logs.md)).

## Hands-On Lab

Python models Jira configuration. **Cost:** none.

### Lab 3.1 — Model the process, then stop

**Objective:** Show why an over-engineered workflow gets bypassed.

```bash
python3 - <<'EOF'
WORKFLOWS = {
  "minimal (3 status)":      {"statuses": 3,  "mandatory_fields": 1, "conditions": 1},
  "reasonable (5 status)":   {"statuses": 5,  "mandatory_fields": 3, "conditions": 3},
  "over-engineered (14)":    {"statuses": 14, "mandatory_fields": 11,"conditions": 12},
}
def friction(w):
    # friction rises with every gate a user must satisfy per issue
    return w["statuses"]*0.3 + w["mandatory_fields"]*1.2 + w["conditions"]*0.8
def bypass_rate(f):
    # the more friction, the more people route around the workflow
    return min(0.85, f/25)
print(f"{'workflow':26}{'friction':>10}{'bypass rate':>13}   outcome")
for name, w in WORKFLOWS.items():
    f = friction(w)
    b = bypass_rate(f)
    outcome = "followed — data is trustworthy" if b < 0.15 else \
              "gamed — 'Done' doesn't mean done" if b > 0.4 else "some corner-cutting"
    print(f"{name:26}{f:>10.1f}{b*100:>12.0f}%   {outcome}")
print("\nThe over-engineered workflow has a HIGH bypass rate: 11 mandatory fields and")
print("12 conditions per issue is so painful that people mark things Done to escape")
print("it — and now 'Done' is a lie. The workflow meant to ENSURE data quality")
print("DESTROYED it, because a process people fight is a process people fake.")
print("\nThe minimal workflow is FOLLOWED, so its (less) data is TRUE. Less data you")
print("can trust beats more data you cannot.")
print("\nDesign rule: model the REAL process, add gates only where they earn their")
print("friction (a resolution field on Done: yes; 11 mandatory fields: no), then")
print("STOP. The ACP exam tests this restraint — anyone can add statuses; knowing")
print("when NOT to is the admin skill.")
EOF
```

**Expected result:** The over-engineered workflow driving a high bypass rate that corrupts its own data, while the minimal workflow is followed and trustworthy. The "process people fight is a process people fake" framing is the design lesson — gates that exceed their value get routed around, destroying the data quality they were meant to ensure.

**Negative test:** Adding mandatory fields and conditions to "improve data quality." Past a threshold, users escape the friction by faking transitions, and the data quality drops.

**Cleanup:** None.

### Lab 3.2 — JQL performance: narrow first

**Objective:** Quantify indexed-field filtering.

```bash
python3 - <<'EOF'
TOTAL_ISSUES = 2_000_000
# A dashboard query, two ways to write it
QUERIES = [
  ("text ~ 'timeout' AND project = PLAT AND status = Open",
   "text search FIRST (scans everything), then narrow"),
  ("project = PLAT AND status = Open AND text ~ 'timeout'",
   "indexed fields FIRST (project+status), then text search the remainder"),
]
# project=PLAT is ~2% of issues; status=Open is ~15% of those
after_project = int(TOTAL_ISSUES * 0.02)
after_status = int(after_project * 0.15)
print(f"instance: {TOTAL_ISSUES:,} issues\n")
print("BAD ordering (text search first):")
print(f"   text ~ 'timeout' scans ALL {TOTAL_ISSUES:,} issues (unindexed full-text)")
print(f"   -> then filters to PLAT+Open. Cost dominated by the {TOTAL_ISSUES:,}-issue scan.\n")
print("GOOD ordering (indexed fields first):")
print(f"   project = PLAT      -> {after_project:,} issues (indexed, instant)")
print(f"   status = Open       -> {after_status:,} issues (indexed)")
print(f"   text ~ 'timeout'    -> full-text search over just {after_status:,}, not {TOTAL_ISSUES:,}")
print(f"\nthe text search runs over {TOTAL_ISSUES//after_status}x fewer issues when you narrow first.")
print("\nJira's query planner helps, but the lesson is the same as NRQL/DQL/LogQL")
print("everywhere on this shelf: put the CHEAP, INDEXED, SELECTIVE filters first")
print("(project, status, assignee), the EXPENSIVE ones (text ~, custom-field scans)")
print("last. And remember WHERE this query lives — a slow filter behind a dashboard")
print("that 200 people load each morning is slow 200 times a day, every day.")
EOF
```

**Expected result:** The indexed-first ordering running the expensive text search over roughly 150,000 issues instead of 2 million — a ~13x reduction. The where-it-lives note is the operational payoff — a JQL filter behind a shared dashboard pays its cost on every load, so query efficiency compounds with usage.

**Negative test:** Leading a JQL filter with a text search or custom-field scan. It works on a small instance and crawls on a large one, especially behind a frequently-loaded dashboard.

**Cleanup:** None.

### Lab 3.3 — Automation without loops or mystery

**Objective:** Audit automation rules for the two failure modes.

```bash
python3 - <<'EOF'
RULES = [
  # name,                        trigger,              action,                  documented, owner
  ("close-parent-on-children",  "child issue closed",  "close parent if all done", True,  "platform-team"),
  ("sync-priority-to-linked",   "priority changed",    "set linked issue priority", False, "(unknown)"),
  ("reopen-on-comment",         "comment added",       "reopen if closed",          True,  "support-team"),
  ("mirror-back-priority",      "priority changed",    "set THIS from linked",      False, "(unknown)"),  # <- loops with sync-priority
  ("auto-assign-round-robin",   "issue created",       "assign to next in team",    True,  "team-lead"),
]
print("Automation audit:\n")
# loop detection: two rules whose trigger+action form a cycle
loop_pairs = []
for i, r1 in enumerate(RULES):
    for r2 in RULES[i+1:]:
        if "priority" in r1[1] and "priority" in r2[2] and "priority" in r2[1] and "priority" in r1[2]:
            loop_pairs.append((r1[0], r2[0]))
undocumented = [r[0] for r in RULES if not r[3]]
ownerless = [r[0] for r in RULES if r[4].startswith("(")]
print(f"{'rule':28}{'documented':>12}{'owner':>16}")
for name, trig, act, doc, owner in RULES:
    print(f"{name:28}{'yes' if doc else 'NO':>12}{owner:>16}")
print(f"\nFINDINGS:")
print(f"  LOOP RISK: {loop_pairs} — 'sync-priority' sets the linked issue's priority,")
print(f"     'mirror-back' sets THIS issue's from the linked. A change ping-pongs")
print(f"     between them until the platform's loop-guard stops it — after firing")
print(f"     far more than intended, on every priority edit.")
print(f"  {len(undocumented)} UNDOCUMENTED rules: {', '.join(undocumented)} — 'why did this happen?'")
print(f"     has no answer. Automation is invisible logic until it is written down.")
print(f"  {len(ownerless)} OWNERLESS rules — nobody to ask, nobody to fix it when it misfires.")
print("\nAutomation is CODE. It needs the same discipline as any config on this shelf:")
print("  - an OWNER (a team, not a departed person)")
print("  - DOCUMENTATION (what it does and why — or it becomes unexplainable behavior)")
print("  - LOOP awareness (two rules that each edit what the other watches = a cycle)")
print("The value is real; ungoverned, it becomes the instance's haunted house.")
EOF
```

**Expected result:** A loop between two priority-sync rules and several undocumented, ownerless rules flagged. The automation-is-code framing is the discipline — the same owner/documentation/review requirements as any configuration, plus loop awareness, because two rules each editing what the other watches form a cycle that fires far more than intended.

**Negative test:** Building automation rules ad hoc without ownership or documentation. Six months later "why did this ticket auto-close?" is unanswerable, and two rules are quietly ping-ponging on every edit.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Workflows designed to model the real process, with gates only where they earn their friction.
- [ ] JQL written indexed-fields-first, mindful of where the query is loaded.
- [ ] Automation rules owned, documented, and audited for loops.
- [ ] Over-engineering recognized as the shared failure mode of all three.
