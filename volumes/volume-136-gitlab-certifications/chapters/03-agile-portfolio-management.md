# Chapter 03: Agile Portfolio Management

## Learning Objectives

- Structure work with issues, labels, milestones, epics, and iterations.
- Build boards that reflect a real workflow rather than a wish.
- Manage dependencies and blocking relationships between issues.
- Track velocity honestly, and know what it cannot tell you.

## The planning hierarchy

This is the **Certified Agile Portfolio Management Associate** material. GitLab's planning objects nest from the concrete upward:

| Object | Scope | Lives at |
|:---|:---|:---|
| **Task** | A checklist item or child work item | Within an issue |
| **Issue** | One unit of work — bug, feature, chore | Project |
| **Epic** | A body of work spanning issues, possibly across projects | Group |
| **Milestone** | A time-boxed or release-boxed collection | Project or group |
| **Iteration** | A recurring, fixed-length cadence (a sprint) | Group |
| **Roadmap** | Epics visualized over time | Group |

The split matters: **issues are per-project, epics are per-group**. Work that spans several repositories is exactly what epics exist for, and that is why the certification is a *group*-level topic rather than a project one.

## Labels and boards

**Labels** classify issues; **scoped labels** (`workflow::in-progress`, using the `::` syntax) are mutually exclusive within their scope, so applying `workflow::review` automatically removes `workflow::in-progress`. This single feature is what makes label-driven boards work — without exclusivity an issue drifts into several columns at once.

**Boards** visualize issues as columns, typically by scoped label. A board is only as honest as the workflow it encodes: columns that match how work *actually* moves reveal bottlenecks, while columns invented to look tidy hide them.

## Dependencies

GitLab expresses relationships between issues: **blocks / is blocked by**, and **relates to**. Blocking relationships are the useful ones for planning, because they make the critical path explicit — and, if you have created a cycle, they make that visible too.

## Velocity, honestly

**Velocity** is work completed per iteration, used to forecast. It is genuinely useful and routinely misused:

- It is **descriptive, not a target.** The moment velocity becomes a goal, estimates inflate and the metric stops measuring anything.
- It is **team-specific.** Comparing velocity between teams is meaningless — different estimation scales, different work.
- It needs **several iterations** before it means anything, and it should be read as a range rather than a number.

## Hands-On Lab

Python models planning. **Cost:** none.

### Lab 3.1 — Scoped labels and board columns

**Objective:** Show why exclusivity is what makes boards coherent.

```bash
python3 - <<'EOF'
def apply_label(labels, new):
    if "::" in new:
        scope = new.split("::")[0] + "::"
        labels = {l for l in labels if not l.startswith(scope)}   # scoped: mutually exclusive
    return labels | {new}

print("=== scoped labels (workflow::) ===")
labels = set()
for step in ["workflow::todo", "priority::high", "workflow::in-progress", "workflow::review"]:
    labels = apply_label(labels, step)
    print(f"apply {step:22} -> {sorted(labels)}")

print("\n=== unscoped labels (no exclusivity) ===")
plain = set()
for step in ["todo", "in-progress", "review"]:
    plain = plain | {step}
    print(f"apply {step:22} -> {sorted(plain)}")
print("\nThe issue now carries todo AND in-progress AND review — it appears in three board")
print("columns at once, and the board no longer tells you where the work actually is.")
EOF
```

**Expected result:** Scoped labels replace one another within `workflow::` while `priority::high` survives (different scope); unscoped labels accumulate until the issue sits in three columns simultaneously. That accumulation is precisely the failure scoped labels exist to prevent, and it is why board design starts with choosing a scope.

**Negative test:** Building a workflow board on plain labels and relying on people to remove the old one — they forget under pressure, and within a fortnight the board is a lie.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Dependencies and the critical path

**Objective:** Resolve blocking relationships and detect cycles.

```bash
python3 - <<'EOF'
issues = {
  "#1 schema migration":   {"blocks": ["#2 API endpoint"], "estimate": 3},
  "#2 API endpoint":       {"blocks": ["#3 UI form", "#4 SDK update"], "estimate": 5},
  "#3 UI form":            {"blocks": [], "estimate": 2},
  "#4 SDK update":         {"blocks": ["#5 docs"], "estimate": 2},
  "#5 docs":               {"blocks": [], "estimate": 1},
}
blocked_by = {k: [] for k in issues}
for i, meta in issues.items():
    for b in meta["blocks"]:
        blocked_by[b].append(i)

def longest_path(issue, seen=None):
    seen = seen or set()
    if issue in seen: return float("inf"), ["CYCLE"]
    seen = seen | {issue}
    best, path = issues[issue]["estimate"], [issue]
    for nxt in issues[issue]["blocks"]:
        d, p = longest_path(nxt, seen)
        if issues[issue]["estimate"] + d > best:
            best, path = issues[issue]["estimate"] + d, [issue] + p
    return best, path

starts = [i for i in issues if not blocked_by[i]]
print("ready to start now (nothing blocking them):", starts)
for s in starts:
    d, p = longest_path(s)
    print(f"\ncritical path from {s}: {d} points")
    for step in p: print(f"   -> {step}")
print("\nTotal estimate is 13 points, but the CRITICAL PATH is 11 — that is the schedule floor,")
print("no matter how many people you add. #3 and #4 can run in parallel once #2 lands.")
EOF
```

**Expected result:** Only `#1` can start; the critical path runs #1 → #2 → #4 → #5 at 11 points against a 13-point total. The distinction is the planning lesson: **total effort and elapsed time are different numbers**, and parallelism only helps on work that is not on the critical path. Adding people to #3 does not make the release ship sooner.

**Negative test:** Planning by summing estimates and dividing by team size — it ignores blocking entirely and produces a date the dependency chain makes impossible.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Velocity as a range, not a target

**Objective:** Forecast honestly from historical iterations.

```bash
python3 - <<'EOF'
import statistics
iterations = {"Sprint 1": 18, "Sprint 2": 23, "Sprint 3": 20, "Sprint 4": 26, "Sprint 5": 21}
vals = list(iterations.values())
mean, lo, hi = statistics.mean(vals), min(vals), max(vals)
for name, v in iterations.items():
    print(f"{name}: {'#'*v} {v}")
print(f"\nmean {mean:.1f}  range {lo}-{hi}  stdev {statistics.pstdev(vals):.1f}")

backlog = 100
print(f"\nForecast for a {backlog}-point backlog:")
print(f"   optimistic (best sprint) : {backlog/hi:5.1f} sprints")
print(f"   likely     (mean)        : {backlog/mean:5.1f} sprints")
print(f"   pessimistic(worst sprint): {backlog/lo:5.1f} sprints")
print(f"\nHonest answer: '{backlog/hi:.0f} to {backlog/lo:.0f} sprints', not '{backlog/mean:.1f}'.")
print("Velocity is DESCRIPTIVE. Make it a target and estimates inflate until it measures nothing.")
EOF
```

**Expected result:** A forecast of roughly 3.8 to 5.6 sprints rather than a false-precision 4.6. Presenting the range is the honest output, because the historical data genuinely does not support a single number. The closing warning is the one that matters organizationally: velocity used as a performance target is trivially gamed by inflating estimates, after which it tracks nothing at all.

**Negative test:** Forecasting from a single sprint's velocity — the sample is one, the variance is invisible, and the resulting date is presented with a confidence the data cannot support.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Planning hierarchy mapped, with issues per-project and epics per-group.
- [ ] Scoped labels used to make boards coherent.
- [ ] Blocking dependencies resolved, with the critical path distinguished from total effort.
- [ ] Velocity forecast as a range, and understood as descriptive rather than a target.
