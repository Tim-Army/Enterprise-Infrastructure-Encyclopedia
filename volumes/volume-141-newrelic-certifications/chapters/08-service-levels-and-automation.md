# Chapter 08: Service Levels and Automation

## Learning Objectives

- Define SLIs and SLOs in New Relic and read service level attainment.
- Draw service boundaries so SLOs measure what users experience.
- Prioritize which services get SLOs at all.
- Manage observability as code with Terraform and NerdGraph.

*Exam relevance: REP Section 2 in full — "understanding SLIs, SLOs, and service level attainment, service boundaries and prioritizing SLOs, managing service levels in New Relic" — and REP Section 4: "create observability fixtures like instrumentation configs, dashboards, synthetics, alert conditions, service levels and more using New Relic APIs and Terraform providers."*

## SLIs, SLOs, attainment

The vocabulary, in New Relic's frame:

- An **SLI** is the measurement — a ratio of good events to total events, defined by NRQL. "Requests under 500 ms and not erroring, over all requests."
- An **SLO** is the target on that measurement over a window. "99.5% over 28 days."
- **Attainment** is the score so far: what percentage of the window's events were good, read against the target.

Because the SLI is NRQL, Lab 3.3's warning completes its tour: dashboard, alert, and SLO can all inherit the same wrong clause. An SLO built on an under-counting SLI reports compliance that no user experiences — reviewed once when written, it lies quietly forever after.

Error budgets and burn-rate alerting were built in [Volume CXXXIX](../../volume-139-grafana-observability/chapters/08-recording-rules-alerting-and-slos.md) and [Volume CXL](../../volume-140-dynatrace-certifications/chapters/08-slos-workflows-and-site-reliability-guardian.md); the mechanics transfer unchanged. What REP adds — and what this chapter's labs work — is the **boundary and prioritization** questions that come *before* the arithmetic.

## Service boundaries

REP's phrase "service boundaries and prioritizing SLOs" names the design decision most SLO rollouts get wrong first: **where to measure.**

An SLO measured at each internal microservice tells you how components behave. The user does not call components. A checkout that traverses seven services can have seven green SLOs and still fail its users — each service 99.5% good compounds to roughly 96.6% end-to-end if failures are independent. The defensible pattern:

| Measure at | Answers | Owner |
|:---|:---|:---|
| **User-facing boundary** (the request the customer made) | Did we keep our promise? | Product / the whole team |
| **Selected internal dependencies** | Which component is eating the budget? | The owning team |

Boundary SLOs are the commitment; internal SLOs are the diagnosis. Publishing only internal ones is how a team reports 99.5% while support tickets say otherwise.

## Prioritizing: not everything gets an SLO

An SLO is a standing commitment with an on-call cost attached. Giving every service one dilutes all of them. The prioritization REP expects is unromantic: user-facing and revenue-bearing flows first, hard dependencies of those flows second, and internal tooling only where its failure bleeds into the first two. A batch job that can rerun tomorrow needs an alert, not an SLO.

## Observability as code

REP Section 4's list — "instrumentation configs, dashboards, synthetics, alert conditions, service levels" — are what it calls **observability fixtures**, and the exam expects them managed through the **NerdGraph** API (New Relic's GraphQL interface) and the official **Terraform provider**.

The argument is the standard infrastructure-as-code one, applied to monitoring: click-built fixtures drift, cannot be reviewed, and cannot be reproduced for the next environment or the next team. Fixtures-as-code get review, versioning, and — the lab's subject — **drift detection**, which is where the practice pays for itself.

## Hands-On Lab

Python models service levels and fixtures. **Cost:** none.

### Lab 8.1 — Attainment, and where you measure it

**Objective:** Compute attainment at two boundaries and watch them disagree.

```bash
python3 - <<'EOF'
import random
random.seed(8)
SERVICES = ["gateway", "auth", "cart", "pricing", "payment", "inventory", "email"]
GOOD_P   = {s: 0.995 for s in SERVICES}
GOOD_P["email"] = 0.999          # and email is async — a failure does not fail checkout

N = 100_000
component_good = {s: 0 for s in SERVICES}
journey_good = 0
for _ in range(N):
    ok = True
    for s in SERVICES:
        good = random.random() < GOOD_P[s]
        component_good[s] += good
        if not good and s != "email":
            ok = False
    journey_good += ok

print(f"{'component':12}{'attainment':>12}{'SLO 99.5%':>11}")
for s in SERVICES:
    a = component_good[s]/N*100
    print(f"{s:12}{a:>11.2f}%{'   met' if a >= 99.5 else '   MISSED':>11}")
ja = journey_good/N*100
print(f"\nend-to-end checkout attainment: {ja:.2f}%  <- what the USER experienced")
print(f"against a 99.5% boundary SLO: {'met' if ja >= 99.5 else 'MISSED'}")
print("\nEvery component met its SLO. The journey did not — six sequential 99.5%")
print("components compound to ~97% even before anything goes unusually wrong.")
print("\nTwo lessons the REP syllabus packs into 'service boundaries':")
print("  1. The COMMITMENT belongs at the user-facing boundary; component SLOs are")
print("     diagnosis, not promises.")
print("  2. Async/non-blocking dependencies (email) belong OUTSIDE the journey SLI —")
print("     including them fails checkout for a failure the user never saw.")
EOF
```

**Expected result:** All seven components meet 99.5% while end-to-end attainment lands near 97%, and the email service illustrates the exclusion rule for non-blocking dependencies. The compounding arithmetic is the argument nobody can wave away — green components and a missed promise are not merely compatible but *expected* once enough services stand in sequence.

**Negative test:** Publishing the component SLOs as the team's reliability report. Every number is true, and the sum of true numbers misstates what users got.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Which services get an SLO

**Objective:** Apply the prioritization rubric.

```bash
python3 - <<'EOF'
CANDIDATES = [
  # service,           user_facing, revenue, hard_dep_of_revenue, can_rerun
  ("checkout flow",         True,  True,  False, False),
  ("search",                True,  False, False, False),
  ("payment-svc",           False, True,  True,  False),
  ("recommendations",       True,  False, False, True),
  ("nightly-reconciliation",False, False, False, True),
  ("internal admin portal", False, False, False, False),
  ("auth",                  False, False, True,  False),
]
print(f"{'service':24}{'decision':>12}   reasoning")
for name, uf, rev, dep, rerun in CANDIDATES:
    if uf and rev:            d, why = "SLO (tier 1)", "user-facing AND revenue — the promise itself"
    elif dep:                 d, why = "SLO (tier 2)", "hard dependency of a revenue flow — diagnosis layer"
    elif uf and not rerun:    d, why = "SLO (tier 2)", "user-facing; failures are experienced, not replayed"
    elif rerun:               d, why = "alert only", "can be rerun — failure is an annoyance with a retry button"
    else:                     d, why = "alert only", "internal; measure, do not promise"
    print(f"{name:24}{d:>12}   {why}")

slos = sum(1 for c in CANDIDATES if not (c[4] or (not c[1] and not c[2] and not c[3])))
print(f"\n{slos} of {len(CANDIDATES)} candidates get SLOs. That restraint is the point:")
print("an SLO is a standing commitment with an on-call cost. Recommendations is")
print("user-facing and still gets none — a stale recommendation is a shrug, and a")
print("shrug does not deserve an error budget. The rubric spends commitments where")
print("breach means a user was failed or money was lost, and alerts everywhere else.")
EOF
```

**Expected result:** Four of seven candidates get SLOs, with recommendations — user-facing but tolerably degradable — deliberately excluded. The rubric's value is what it says no to: alerts are cheap and reversible, SLOs are commitments, and REP's "prioritizing SLOs" phrase is asking whether you know the difference.

**Negative test:** An SLO per microservice because the platform makes it easy. Sixty commitments, none of which anyone can name, is the same as none — with more dashboards.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Fixtures as code, and drift detection

**Objective:** Diff intended configuration against the live estate.

```bash
python3 - <<'EOF'
# What the Terraform/NerdGraph definitions say SHOULD exist
INTENDED = {
  "alert:checkout error rate":   {"threshold": "2%/3min", "workflow": "tier1-page"},
  "alert:payment external errs": {"threshold": "5%/5min", "workflow": "tier1-page"},
  "slo:checkout availability":   {"target": "99.5/28d",   "sli": "rev-2024-11"},
  "synthetic:checkout journey":  {"freq": "5min",         "locations": 3},
  "dashboard:golden-signals":    {"panels": 8},
}
# What the live account actually contains
LIVE = {
  "alert:checkout error rate":   {"threshold": "4%/10min","workflow": "tier1-page"},   # hand-edited during an incident
  "alert:payment external errs": {"threshold": "5%/5min", "workflow": "tier1-page"},
  "slo:checkout availability":   {"target": "99.5/28d",   "sli": "rev-2024-11"},
  "synthetic:checkout journey":  {"freq": "15min",        "locations": 1},             # "temporarily" reduced
  "dashboard:golden-signals":    {"panels": 8},
  "alert:cpu-test-DELETE-ME":    {"threshold": "50%/1min","workflow": "tier1-page"},   # someone's experiment
}
print("drift report (intended vs live):\n")
drifts = 0
for k in sorted(set(INTENDED) | set(LIVE)):
    i, l = INTENDED.get(k), LIVE.get(k)
    if i == l: continue
    drifts += 1
    if i is None:   print(f"  UNMANAGED  {k}\n             exists live, defined nowhere — {l}")
    elif l is None: print(f"  MISSING    {k}\n             defined in code, absent live")
    else:
        for f in i:
            if i[f] != l[f]:
                print(f"  DRIFTED    {k}\n             {f}: intended {i[f]!r}, live {l[f]!r}")
print(f"\n{drifts} finding(s). Each has a story:")
print("  the alert was LOOSENED mid-incident and never restored — the on-call is")
print("    now protected by a threshold nobody agreed to")
print("  the synthetic was cut to 1 location/15min during a cost push — checkout's")
print("    earliest-warning signal (Lab 7.3!) now has 1/3 the coverage")
print("  the test alert pages TIER 1 — an experiment wired to the loudest channel")
print("\nNone of these announce themselves. Drift detection is the ONLY way")
print("hand-edits surface, which is why fixtures-as-code is REP syllabus material")
print("and not just engineering hygiene: apply the code, and all three heal.")
EOF
```

**Expected result:** Three findings — a loosened alert, a degraded synthetic, and an unmanaged experiment paging tier 1 — each traceable to a reasonable-at-the-time hand edit. The report's punchline is that applying the code fixes all three at once; without the code there is nothing to diff against and every finding requires someone to *remember*.

**Negative test:** Managing fixtures as code but never running the diff. The code becomes documentation of intentions, drifting exactly as fast as the console-clicked reality it no longer describes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SLIs, SLOs, and attainment defined, with the SLI's NRQL treated as review-worthy.
- [ ] Commitments placed at user-facing boundaries; component SLOs kept as diagnosis.
- [ ] SLO candidates filtered by the rubric — commitments are spent, not sprinkled.
- [ ] Observability fixtures managed via Terraform/NerdGraph with drift detection actually run.
