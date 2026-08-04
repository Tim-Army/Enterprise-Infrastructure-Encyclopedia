# Chapter 08: SLOs, Workflows, and Site Reliability Guardian

## Learning Objectives

- Define SLOs in Dynatrace and connect them to error budgets.
- Build workflows in AutomationEngine to act on events rather than notify about them.
- Use Site Reliability Guardian as an automated release quality gate.
- Manage configuration as code so environments stay reproducible.

*Exam relevance: the whole **Advanced Automation Specialist** skill list — workflows, Site Reliability Guardian, service-level objectives, configuration-as-code, CI/CD integrations, Dynatrace API basics, automating routine tasks.*

## SLOs

An SLO states a target on a service-level indicator: "99.9% of checkout requests succeed over 28 days." Its complement is the **error budget** — the permitted failure.

Chapter 06 established why this matters here specifically: **baselines describe what is; SLOs encode what should be.** A service that has always been slow has a baseline that reflects that and an SLO that indicts it. Running only baselines means chronic underperformance never surfaces.

Dynatrace SLOs are defined over DQL or metric expressions, evaluated continuously, and surfaced as budget consumed and remaining.

## Workflows and AutomationEngine

**Workflows** are event-driven automations: a trigger (a problem opens, an SLO burns, a schedule fires, an API call arrives), then tasks — run JavaScript, call an API, post to a channel, open a ticket, execute a remediation.

The shift they represent is from **notification to action**. A monitoring platform that tells a human to restart a service is doing the diagnostic work and delegating the boring part. A workflow does the boring part and tells the human it happened.

That shift has a hard limit, and it is worth stating before anyone automates a restart:

> **Automate the remediation only when the diagnosis is reliable.** An action triggered by a misdiagnosis executes at machine speed on the wrong target.

The graded path is: notify → notify with a suggested action → automate with an approval step → automate fully for the narrow cases with a proven track record.

## Site Reliability Guardian

Dynatrace describes Site Reliability Guardian as **"a Dynatrace app that automates change impact analysis to validate service availability, performance, and capacity objectives."**

Its structure, per the documentation:

- **Objectives** are "means for measuring the performance, availability, capacity, and security of your services," measured by indicators. **A guardian can contain up to 50 objectives.**
- **Validation** runs manually from the UI or automatically from workflows, events, or API calls.
- Results carry a severity: **Pass (4)** — "the value is within the target range, the objective is met"; **Warning (3)** — "the value is in the warning range; the objective is met, but close to failure"; **Fail (2)** — "the value violates the failure threshold; the objective is not met".
- The overall result is **"the most severe of individual validations."**

That last rule is the one to design around: **one failing objective fails the guardian.** A guardian with fifty objectives is fifty chances to block a release, so the objectives you include should be ones you would genuinely stop a deployment for.

The **Warning** band is the feature people overlook most. It gives a signal that a release is drifting toward failure while still allowing it through — an early warning that costs nothing.

## Configuration as code

Dashboards, SLOs, alerting profiles, management zones, and guardians can be defined as code and applied through the API, which makes environments reproducible and reviewable. The failure mode it prevents is the familiar one: a staging environment that no longer resembles production because eighteen months of console clicks were never written down.

## Hands-On Lab

Python models SLOs and automation. **Cost:** none.

### Lab 8.1 — Error budgets and burn

**Objective:** Turn an SLO into a decision.

```bash
python3 - <<'EOF'
SLO_TARGET, WINDOW_DAYS = 0.999, 28
budget_min = WINDOW_DAYS*24*60*(1-SLO_TARGET)
print(f"SLO {SLO_TARGET*100}% over {WINDOW_DAYS}d -> error budget {budget_min:.1f} minutes\n")

WEEKS = [
  ("week 1", 0.9995,  "normal"),
  ("week 2", 0.9991,  "one brief incident"),
  ("week 3", 0.9975,  "database failover"),
  ("week 4", 0.9998,  "quiet"),
]
spent_total = 0
print(f"{'period':10}{'achieved':>11}{'spent(min)':>12}{'cum spent':>11}{'remaining':>11}   posture")
for name, achieved, note in WEEKS:
    spent = 7*24*60*(1-achieved)
    spent_total += spent
    rem = budget_min - spent_total
    pct = spent_total/budget_min*100
    if   pct > 100: posture = "EXHAUSTED — freeze feature releases, fix reliability"
    elif pct > 75:  posture = "at risk — slow down, no risky changes"
    elif pct > 50:  posture = "watch"
    else:           posture = "healthy — budget available for planned risk"
    print(f"{name:10}{achieved*100:>10.2f}%{spent:>12.1f}{spent_total:>11.1f}{rem:>11.1f}   {posture}")

print(f"\nThe database failover in week 3 consumed {7*24*60*(1-0.9975):.0f} of {budget_min:.0f} budget minutes")
print("in a single event — more than the other three weeks combined.")
print("\nWhat the budget buys you is a NEGOTIATION on evidence rather than opinion.")
print("'Can we ship the risky migration this week?' stops being a matter of nerve and")
print("becomes arithmetic: budget remaining says yes or no, and both answers are defensible.")
EOF
```

**Expected result:** A 40.3-minute budget over 28 days. Week 3's failover spends 25.2 minutes — more than the other three weeks combined — dropping the posture to "at risk," and then week 4 exhausts the budget despite being the *quietest* week of the four at 99.98%. That ending is the useful one: once the budget is gone, a good week does not restore it, and the freeze is triggered by arithmetic rather than by anyone's judgment of how bad things feel. The value framed at the end is organizational — the error budget converts a recurring argument about risk appetite into a number both sides already agreed to.

**Negative test:** Setting an SLO and never checking budget burn. An SLO nobody checks is a documentation exercise.

**Cleanup:** None.

### Lab 8.2 — Site Reliability Guardian as a release gate

**Objective:** Model the severity rules exactly as documented.

```bash
python3 - <<'EOF'
# Severity per Dynatrace docs: pass=4, warning=3, fail=2; overall = MOST SEVERE
SEV = {"pass": 4, "warning": 3, "fail": 2}
NAME = {4: "PASS", 3: "WARNING", 2: "FAIL"}

def evaluate(objectives):
    results = []
    for name, value, target, warn in objectives:
        if value <= target:   r = "pass"
        elif value <= warn:   r = "warning"
        else:                 r = "fail"
        results.append((name, value, target, warn, r))
    overall = min(SEV[r] for *_, r in results)      # most severe = lowest number
    return results, overall

RELEASES = {
  "release 1.4.0": [
    ("p95 latency (ms)",        280, 300, 400),
    ("error rate (%)",         0.12, 0.5, 1.0),
    ("CPU saturation (%)",       62,  70,  85),
    ("failed logins (count)",     3,  10,  25),
  ],
  "release 1.5.0": [
    ("p95 latency (ms)",        380, 300, 400),   # warning band
    ("error rate (%)",         0.31, 0.5, 1.0),
    ("CPU saturation (%)",       68,  70,  85),
    ("failed logins (count)",     7,  10,  25),
  ],
  "release 1.6.0": [
    ("p95 latency (ms)",        355, 300, 400),   # warning
    ("error rate (%)",         1.40, 0.5, 1.0),   # FAIL
    ("CPU saturation (%)",       91,  70,  85),   # FAIL
    ("failed logins (count)",     4,  10,  25),
  ],
}
for rel, objectives in RELEASES.items():
    results, overall = evaluate(objectives)
    print(f"\n=== {rel} ===")
    for n, v, t, w, r in results:
        print(f"   {n:26} value {v:>7}  target {t:>5}  warn {w:>5}   {r.upper()}")
    print(f"   -> guardian result: {NAME[overall]} (severity {overall}) — 'the most severe of individual validations'")
    if overall == 4:   print("      release proceeds")
    elif overall == 3: print("      release proceeds, but it is drifting — investigate before the next one")
    else:              print("      RELEASE BLOCKED")

print("\n\nTwo design consequences of 'most severe wins':")
print("  1. ONE failing objective fails the guardian. A guardian may hold up to 50")
print("     objectives — that is 50 chances to block. Include only objectives you")
print("     would genuinely stop a deployment for.")
print("  2. The WARNING band is free early warning. Release 1.5.0 shipped, and its")
print("     latency drift was visible BEFORE 1.6.0 failed outright. A pass/fail-only")
print("     gate would have shown green, then red, with no signal in between.")
EOF
```

**Expected result:** 1.4.0 passes, 1.5.0 warns and still ships, 1.6.0 is blocked by two failing objectives. The warning band's value shows up across the sequence — the latency drift that eventually contributed to 1.6.0's failure was already visible in 1.5.0, which a binary gate would have reported as simply green.

**Negative test:** Loading a guardian with all fifty objectives because they are available. Every marginal objective is another chance to block a good release on something nobody would actually stop for.

**Cleanup:** None.

### Lab 8.3 — Graded automation

**Objective:** Decide how far to automate each response.

```bash
python3 - <<'EOF'
SCENARIOS = [
  # trigger,                        diag_confidence, blast_radius, reversible, action
  ("disk >90% on log volume",              0.98, "one host",   True,  "rotate + compress logs"),
  ("pod OOMKilled, known memory leak",     0.95, "one pod",    True,  "restart pod"),
  ("SLO burn rate >14 on checkout",        0.70, "service",    False, "roll back release"),
  ("DB connection pool exhausted",         0.85, "service",    True,  "raise pool + alert DBA"),
  ("cert expires in 7 days",               0.99, "one service",True,  "renew via ACME"),
  ("elevated 5xx, cause unclear",          0.40, "unknown",    False, "scale out"),
]
print(f"{'trigger':38}{'conf':>6}{'blast':>12}{'rev':>5}   automation level")
for trig, conf, blast, rev, action in SCENARIOS:
    if conf >= 0.95 and rev and blast in ("one host","one pod","one service"):
        lvl = f"FULL AUTO — {action}"
    elif conf >= 0.85 and rev:
        lvl = f"AUTO + notify — {action}"
    elif conf >= 0.70:
        lvl = f"APPROVAL GATE — propose '{action}', human confirms"
    else:
        lvl = "NOTIFY ONLY — diagnosis too weak to act on"
    print(f"{trig:38}{conf:>6.2f}{blast:>12}{'yes' if rev else 'NO':>5}   {lvl}")

print("\nThree factors decide the level, and all three must hold for full automation:")
print("   CONFIDENCE  — how reliable is the diagnosis?")
print("   BLAST RADIUS— how much breaks if the action is wrong?")
print("   REVERSIBLE  — can it be undone?")
print("\n'roll back release' has 0.70 confidence and is NOT reversible in the")
print("meaningful sense — you cannot un-roll-back cleanly once traffic has moved and")
print("migrations have run. It gets an approval gate despite being the obvious fix.")
print("\n'elevated 5xx, cause unclear' automates NOTHING. Scaling out an unknown fault")
print("multiplies a broken thing — and at machine speed, before anyone looks.")
EOF
```

**Expected result:** Two scenarios reach full automation, two get notification or approval gates. The rollback case is the instructive one: it looks like the most obviously automatable response, and it fails the test on both confidence and true reversibility, which is why the graded ladder exists instead of a simple confidence threshold.

**Negative test:** Automating remediation for anything Davis raises a problem for. Chapter 04 showed root-cause attribution degrades into a *confident* wrong answer when topology is incomplete — automation then executes that wrong answer immediately.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] SLOs and error budgets used to make release-risk decisions on evidence.
- [ ] Site Reliability Guardian modeled with pass/warning/fail and most-severe-wins.
- [ ] The warning band used as free early warning.
- [ ] Automation graded by confidence, blast radius, and reversibility.
- [ ] Configuration held as code so environments stay reproducible.
