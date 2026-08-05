# Chapter 07: Agile at Scale and the Marketplace

## Learning Objectives

- Explain how Jira supports agile: boards, sprints, backlogs, and reports.
- Understand agile-at-scale patterns and where Jira's native features end.
- Evaluate Atlassian Marketplace apps without creating dependency risk.
- Recognize the "there's an app for that" trap.

*Cert relevance: agile configuration underpins the ACA project-management certification and the Jira admin ACP; Marketplace app governance is an org-admin concern.*

## Jira and agile

Jira's origin is agile, and its agile features are what most teams touch daily:

| Feature | Is |
|:---|:---|
| **Board** | The visual work display — **Scrum** (sprint-based) or **Kanban** (continuous flow) |
| **Backlog** | The ordered list of work not yet in a sprint |
| **Sprint** | A timeboxed batch of work (Scrum) |
| **Reports** | Burndown, velocity, cumulative flow — the agile metrics |

The admin's contribution is configuring boards to reflect how a team *actually* works, and the honest counsel the certifications imply: **the tool serves the process, not the reverse.** A team doing genuine Kanban should not be forced onto a Scrum board because "that's how we set up Jira." The board is a view; fit it to the team.

The agile **reports** carry a caution this shelf keeps repeating: **velocity is a planning aid, not a performance metric.** Comparing teams by velocity, or pressuring a team to raise it, corrupts the estimates that make it useful — teams inflate story points and the number becomes meaningless, the same [gaming-the-metric failure](03-workflows-jql-and-automation.md) as an over-engineered workflow. The lab makes this concrete.

## Agile at scale

A single team on a single board is straightforward; **many teams on a shared product** is where it gets hard, and where Jira's native features meet their limits:

- **Native Jira** handles multiple boards, shared backlogs, epics spanning teams, and basic cross-project reporting.
- **Frameworks like SAFe** (Scaled Agile Framework) add program increments, portfolio planning, and dependency management that native Jira only partly covers — which is where **Jira's premium plans and Marketplace apps** (Advanced Roadmaps and others) enter.

The admin's judgment is knowing **where native features end and where you genuinely need more** — because the alternative is the Marketplace trap.

## The Marketplace, and its trap

The **Atlassian Marketplace** is a large ecosystem of third-party apps extending Jira and Confluence — time tracking, diagramming, advanced reporting, integrations. It is a genuine strength: capabilities Atlassian does not build natively are one install away.

It is also a genuine risk, and app governance is an org-admin skill:

1. **Every app is a dependency.** It must be maintained, it can break on a Jira update, it may not survive to the next version, and its vendor may vanish. An instance with forty apps has forty ways to break and forty things to keep current.
2. **Apps have data access.** A Marketplace app often reads (and sometimes writes) your Jira/Confluence data — a supply-chain and privacy consideration, not just a feature decision.
3. **"There's an app for that" defers, not solves.** The instinct to install an app for every gap accumulates the same technical debt as cloning a scheme for every variation (Chapter 02) — each is reasonable alone and unmaintainable in aggregate.

The discipline: **install apps deliberately**, with an owner, a real justification (does native Jira genuinely not do this?), and periodic review to remove the ones no longer used. The lab models the accumulation.

## Hands-On Lab

Python models agile and Marketplace decisions. **Cost:** none.

### Lab 7.1 — Velocity is a planning aid, not a scoreboard

**Objective:** Show how measuring velocity as performance destroys it.

```bash
python3 - <<'EOF'
import random
random.seed(37)
# Team's true throughput is stable; watch what happens when velocity becomes a target
def simulate(pressure_to_raise):
    true_throughput = 30   # actual work done per sprint, stable
    velocity = []
    inflation = 1.0
    for sprint in range(8):
        if pressure_to_raise:
            inflation *= 1.08          # team pads estimates to show "improvement"
        reported = true_throughput * inflation
        velocity.append(reported)
    return velocity, true_throughput

no_pressure, tt1 = simulate(False)
pressure, tt2 = simulate(True)
print(f"{'sprint':>7}{'no pressure':>14}{'velocity as target':>20}")
for i in range(8):
    print(f"{i+1:>7}{no_pressure[i]:>14.0f}{pressure[i]:>20.0f}")
print(f"\nactual throughput both cases: {tt1} points of REAL work per sprint\n")
print("Under no pressure, velocity ~30 and STABLE — a reliable planning input:")
print("'we do ~30/sprint, so this 90-point epic is ~3 sprints.'")
print("\nWhen velocity becomes a TARGET (management wants it to 'go up'), the team")
print(f"inflates estimates: reported velocity climbs to {pressure[-1]:.0f} while REAL")
print(f"throughput never moved off {tt2}. The number rose; nothing got faster.")
print("\nGoodhart's law in Jira: 'when a measure becomes a target, it ceases to be a")
print("good measure.' Velocity is a PLANNING aid (how much can we commit to?) and")
print("collapses the moment it is used to COMPARE teams or PRESSURE improvement.")
print("\nThe admin/coach discipline: velocity stays a team's PRIVATE planning tool,")
print("never a cross-team scoreboard. Same lesson as the over-engineered workflow")
print("(ch03): a metric people are pressured on becomes a metric people game.")
EOF
```

**Expected result:** Stable, useful velocity under no pressure versus inflating, meaningless velocity once it becomes a target — with real throughput unchanged. Goodhart's law is the lesson — velocity is a planning input that collapses when used to compare or pressure teams, the same gaming failure as the over-engineered workflow.

**Negative test:** Putting velocity on a dashboard that compares teams. Estimates inflate to compete, and the number stops predicting anything about delivery.

**Cleanup:** None.

### Lab 7.2 — Native Jira versus an app: where's the real gap?

**Objective:** Decide when a Marketplace app is genuinely justified.

```bash
python3 - <<'EOF'
NEEDS = [
  # need,                                native_jira, verdict
  ("scrum/kanban boards",                "yes (core)",        "USE NATIVE — apps here are redundant"),
  ("basic burndown/velocity reports",    "yes (core)",        "USE NATIVE"),
  ("cross-project epics/roadmap",        "premium (Adv Roadmaps)", "premium plan, not a third-party app"),
  ("simple time tracking",               "basic native",      "native usually enough; app only if you need billing-grade"),
  ("Gantt-chart dependency planning",    "partial",           "app JUSTIFIED if native roadmaps insufficient"),
  ("advanced SLA/CSAT for support",      "JSM has SLAs",      "native JSM first; app only for gaps"),
  ("diagramming inside pages",           "no",                "app JUSTIFIED — native gap"),
]
print(f"{'need':38}{'native Jira?':>24}   decision")
apps_needed = 0
for need, native, verdict in NEEDS:
    if "JUSTIFIED" in verdict: apps_needed += 1
    print(f"{need:38}{native:>24}")
    print(f"{'':38}   {verdict}")
print(f"\nOf {len(NEEDS)} needs, only {apps_needed} genuinely justify a third-party app.")
print("\nThe discipline before every install: 'does native Jira (or a PREMIUM PLAN)")
print("already do this?' Most 'we need an app' moments are actually:")
print("  - a native feature nobody knew existed (boards, basic reports, JSM SLAs)")
print("  - a premium-plan feature (Advanced Roadmaps) — same vendor, no supply-chain")
print("    risk, no separate app to break on updates")
print("The genuine gaps (diagramming, Gantt-grade dependency planning) ARE worth an")
print("app — installed deliberately, with an owner.")
print("\nThe anti-pattern: install an app at the first friction, accumulate 40, and")
print("now every Jira update is a 40-app compatibility gamble. Check native FIRST.")
EOF
```

**Expected result:** Only two of seven needs genuinely justifying a third-party app, the rest met by native or premium features. The check-native-first discipline is the governance lesson — most "we need an app" moments are unknown native features or premium-plan capabilities that carry no supply-chain risk.

**Negative test:** Installing a Marketplace app at the first sign of friction. Half the time native Jira or a premium plan already does it, and each unnecessary app is a future compatibility liability.

**Cleanup:** None.

### Lab 7.3 — App sprawl and supply-chain risk

**Objective:** Audit an app portfolio for dependency risk.

```bash
python3 - <<'EOF'
APPS = [
  # app,                     used_by_pct, vendor_health, data_access, last_reviewed_days
  ("time-tracking-pro",           85, "healthy",   "read",         90),
  ("legacy-gantt",                 4, "abandoned", "read+write",   800),   # <- risk
  ("diagram-tool",                60, "healthy",   "read",        120),
  ("old-reporting-addon",          2, "unknown",   "read+write",  900),    # <- risk
  ("sso-connector",              100, "healthy",   "read+write",   30),
  ("survey-widget",                8, "healthy",   "read",        400),
]
print(f"{'app':22}{'usage':>7}{'vendor':>11}{'access':>12}{'reviewed':>10}   flag")
findings = 0
for app, usage, vendor, access, reviewed in APPS:
    flags = []
    if usage < 10: flags.append("LOW USE — candidate to remove")
    if vendor in ("abandoned","unknown"): flags.append("VENDOR RISK")
    if access == "read+write" and reviewed > 365: flags.append("WRITE ACCESS, unreviewed >1yr")
    if flags: findings += 1
    print(f"{app:22}{usage:>6}%{vendor:>11}{access:>12}{reviewed:>9}d   {'; '.join(flags)}")
print(f"\n{findings} apps flagged. The worst offenders:")
print("  legacy-gantt: 4% usage, ABANDONED vendor, READ+WRITE access, unreviewed for")
print("     800 days. It can break the instance on the next Jira update, its vendor")
print("     won't fix it, and it can WRITE your data. Remove it — the 4% who use it")
print("     can move to native roadmaps or a maintained app.")
print("  old-reporting-addon: 2% usage, UNKNOWN vendor, write access. Same profile.")
print("\nThe audit dimensions, run periodically (the org admin's job):")
print("  USAGE   — low-use apps are pure risk with little benefit; remove them")
print("  VENDOR  — abandoned/unknown vendors won't fix breakage; migrate off")
print("  ACCESS  — read+write apps are the supply-chain exposure; justify each")
print("  REVIEWED— an app nobody has looked at in a year is an unowned dependency")
print("\nEvery app is a dependency AND a data-access grant. A 40-app instance nobody")
print("audits is 40 unmanaged risks; a curated dozen with owners is a healthy one.")
EOF
```

**Expected result:** Two abandoned/unknown-vendor apps with write access and negligible usage flagged for removal. The four audit dimensions — usage, vendor health, data access, review recency — are the governance framework, and the read+write-access risk is the supply-chain lens most app decisions omit.

**Negative test:** Leaving Marketplace apps installed indefinitely because "someone might use them." The abandoned-vendor, write-access app is a live risk whether or not anyone uses it, and it breaks the next update.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Jira's agile features configured to fit the team, with Scrum/Kanban chosen by how work flows.
- [ ] Velocity treated as a private planning aid, never a cross-team scoreboard.
- [ ] Marketplace apps justified against native and premium features before installing.
- [ ] The app portfolio audited by usage, vendor health, data access, and review recency.
