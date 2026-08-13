# Chapter 08: Recording Rules, Alerting, and SLOs

## Learning Objectives

- Use recording rules in Mimir and Loki to precompute expensive queries.
- Build alert rules with the right evaluation interval, `for` duration, and labels.
- Route notifications with notification policies, and silence deliberately.
- Define SLOs and alert on **error-budget burn rate** rather than raw thresholds.

## Recording rules

A **recording rule** evaluates a query on a schedule and stores the result as a new time series. The GROT Academy module frames the purpose exactly right: **boost performance, reduce system load, and streamline dashboard and alert workflows.**

The case for them is arithmetic. An expensive aggregation across thousands of series, run by fifteen dashboard panels and five alert rules every thirty seconds, is the same computation performed twenty times a minute. A recording rule performs it **once** per interval; everything else reads a single precomputed series.

| Use a recording rule when | Example |
|:---|:---|
| A query is expensive **and** used repeatedly | `sum(rate(...)) by (service)` across 50,000 series |
| An alert query must evaluate fast and predictably | Anything backing a paging alert |
| A dashboard is slow on wide time ranges | Multi-week trends |
| You want a stable name for a business concept | `job:request_errors:rate5m` |

The conventional naming — `level:metric:operation`, as in `service:http_requests:rate5m` — pays off once you have more than a handful, because the name states what it is without opening the rule.

Loki supports recording rules too, materializing log-derived metrics (Chapter 05) so alerts stop re-scanning raw logs on every evaluation.

## Alert rules

A Grafana alert rule has a query, a condition, an evaluation interval, and a **`for`** duration — and that last one is what separates a usable alert from a noisy one.

| Setting | Meaning | Getting it wrong |
|:---|:---|:---|
| **Evaluation interval** | How often the rule runs | Too frequent wastes resources; too rare delays detection |
| **`for` duration** | How long the condition must hold before firing | Too short fires on transient spikes; too long delays real incidents |
| **Labels** | Attached to the alert; used for routing | Missing labels mean the alert cannot be routed sensibly |
| **Annotations** | Human-facing text — summary, runbook link | An alert with no runbook wastes the responder's first ten minutes |

Alert states run **Normal → Pending → Alerting → Resolved**, where **Pending** is the `for` window doing its job: the condition is true but has not persisted long enough to be worth waking anyone.

## Notification policies

Routing is a tree matched on labels: an alert enters the tree, matches the most specific branch, and inherits that branch's contact point, grouping, and timing.

**Grouping** is the feature that prevents a hundred simultaneous alerts becoming a hundred notifications — alerts sharing group labels are batched into one message. **Silences** suppress notifications during known work; the discipline is that a silence must have an **expiry and a reason**, or you will discover months later that a critical alert has been quietly muted since a maintenance window in March.

## SLOs and burn-rate alerting

A **Service Level Objective** states a target — "99.9% of requests succeed over 30 days" — and its complement is the **error budget**: the 0.1% you are permitted to fail. For 30 days, that is about 43 minutes of total failure.

Alerting on the SLO directly is unsatisfying: a threshold alert on error rate either fires on brief harmless blips or misses a slow burn that consumes the budget over days. **Burn-rate alerting** fixes this by asking *how fast the budget is being consumed*:

- Burn rate 1 = you will exactly exhaust the budget by period end.
- Burn rate 14.4 sustained over 1 hour = 2% of a 30-day budget gone in an hour — page now.
- Burn rate 6 over 6 hours = 5% consumed — page.
- Burn rate 1 over 3 days = a slow leak — a ticket, not a page.

Pairing a **fast window with a slow window** (both must be burning) suppresses the false pages that a single short window produces.

## Hands-On Lab

Python models rules, alerts, and SLOs. **Cost:** none.

### Lab 8.1 — What a recording rule saves

**Objective:** Quantify repeated expensive evaluation.

```bash
python3 - <<'EOF'
SERIES_SCANNED = 50_000
COST_PER_1K = 0.8            # arbitrary cost units per 1000 series scanned
panels, alerts, eval_per_min = 15, 5, 2

adhoc_evals = (panels + alerts) * eval_per_min
rule_evals = 1 * eval_per_min

def cost(evals, series): return evals * series / 1000 * COST_PER_1K

print(f"expensive query: sum(rate(...)) by (service) over {SERIES_SCANNED:,} series")
print(f"consumers: {panels} panels + {alerts} alert rules, evaluated {eval_per_min}x/min\n")
print(f"WITHOUT recording rule: {adhoc_evals:>3} evaluations/min -> cost {cost(adhoc_evals, SERIES_SCANNED):>9,.0f}/min")
print(f"WITH    recording rule: {rule_evals:>3} evaluations/min -> cost {cost(rule_evals, SERIES_SCANNED):>9,.0f}/min")
print(f"   + consumers read a single precomputed series (~{cost(adhoc_evals, 1):.1f}/min, negligible)")
red = (1 - rule_evals/adhoc_evals) * 100
print(f"\nreduction: {red:.0f}% — the same computation was being done {adhoc_evals//rule_evals}x over.")
print("\nNaming convention: level:metric:operation, e.g. service:http_requests:rate5m")
print("Also: alerts backed by a recording rule evaluate FAST and PREDICTABLY, which matters")
print("more than the cost saving — a paging alert should never time out on a slow query.")
EOF
```

**Expected result:** A 95% reduction in evaluation cost, from 40 evaluations per minute to 2. The closing point is the one that matters most operationally: an alert whose query is slow can time out or evaluate late, and an alert that fails to evaluate is indistinguishable from a system that is healthy.

**Negative test:** Creating recording rules for every query — rules cost storage and evaluation too, so a rule used by one panel on a cheap query is pure overhead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — The `for` duration and alert states

**Objective:** Tune `for` to suppress transients without delaying real incidents.

```bash
python3 - <<'EOF'
# CPU samples at 30s intervals; a brief spike, then a sustained problem
samples = [40,42,95,41,43,40,  92,94,96,93,95,97,94,96]
THRESHOLD = 90

def simulate(for_minutes):
    need = int(for_minutes * 60 / 30)       # samples required at 30s interval
    state, pending, fired_at = "Normal", 0, None
    log = []
    for i, v in enumerate(samples):
        if v > THRESHOLD:
            pending += 1
            state = "Alerting" if pending >= need else "Pending"
            if state == "Alerting" and fired_at is None: fired_at = i
        else:
            pending, state = 0, "Normal"
        log.append(state[0])
    return "".join(log), fired_at

for f in (0, 1, 2, 5):
    trace, fired = simulate(f)
    when = f"fired at sample {fired} (t+{fired*30}s)" if fired is not None else "never fired"
    note = ""
    if f == 0:   note = "  <-- FALSE ALARM on the single transient spike at sample 2"
    if f == 5:   note = "  <-- too slow: 5 minutes of a real incident before anyone is told"
    print(f"for={f}m  {trace}  {when}{note}")
print("\nN=Normal  P=Pending  A=Alerting")
print("\nfor=0 pages on a 30-second blip. for=5m ignores the blip but delays the real incident.")
print("for=1-2m is the usual sweet spot: long enough to ride out transients, short enough to matter.")
print("Pending is the feature — the condition is true but has not EARNED a page yet.")
EOF
```

**Expected result:** `for=0` fires on the isolated spike, `for=5m` delays the genuine incident substantially, and 1–2 minutes balances both. The framing of **Pending as a feature** rather than a delay is the conceptual point: it encodes the judgment that a condition must persist to be worth interrupting someone.

**Negative test:** Setting `for=0` to "catch everything" — you catch every transient too, and the resulting noise is exactly how teams learn to ignore alerts.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Error budgets and burn-rate alerting

**Objective:** Alert on budget consumption rather than a raw error threshold.

```bash
python3 - <<'EOF'
SLO = 0.999                      # 99.9% success over 30 days
PERIOD_MIN = 30*24*60
budget_min = PERIOD_MIN * (1 - SLO)
print(f"SLO {SLO*100}% over 30 days -> error budget = {budget_min:.1f} minutes of total failure\n")

def burn_rate(error_ratio): return error_ratio / (1 - SLO)

# each scenario gives the error ratio measured over a FAST window and a SLOW window
scenarios = [                    # name                fast(5m)  slow(1h)
  ("normal",                                             0.0005, 0.0005),
  ("brief 5% spike (1 min, then gone)",                  0.05,   0.0012),
  ("sustained 1.5% elevation",                           0.015,  0.015),
  ("slow leak 0.3% for days",                            0.003,  0.003),
  ("major outage 50%",                                   0.50,   0.30),
]
print(f"{'scenario':38}{'burn 5m':>9}{'burn 1h':>9}   decision")
for name, fast_err, slow_err in scenarios:
    fast, slow = burn_rate(fast_err), burn_rate(slow_err)
    if fast >= 14.4 and slow >= 14.4:
        decision = "PAGE — 2% of the 30-day budget going in an hour"
    elif fast >= 6 and slow >= 6:
        decision = "PAGE — 5% consumed over 6 hours"
    elif fast >= 14.4 and slow < 14.4:
        decision = "SUPPRESSED — fast window burning, slow window is not"
    elif slow >= 1:
        decision = "TICKET — slow burn, will exhaust the budget"
    else:
        decision = "ok — within budget"
    print(f"{name:38}{fast:>9.1f}{slow:>9.1f}   {decision}")

print("\nThe pairing does real work here: the brief spike hits burn rate 50 on the FAST window")
print("and would page on its own — but the slow window never confirms it, so nobody is woken.")
print("The major outage burns on BOTH windows and pages immediately.")
print("\nWhy burn rate beats a fixed threshold:")
print("  a 5% error threshold MISSES the 0.3% slow leak that quietly eats the budget over days")
print("  a 0.1% threshold FIRES CONSTANTLY on harmless noise")
print("  burn rate asks the only question that matters: are we going to run out, and how fast?")
EOF
```

**Expected result:** A 43.2-minute error budget. The major outage and the sustained elevation page; the slow leak raises a ticket; and the brief spike is **suppressed** despite a fast-window burn rate of 50, because the slow window never confirms it. That suppression is the whole point of the pairing — the same spike alerting on one short window would page for a problem that had already resolved. The closing comparison is the argument for the technique: a single fixed threshold cannot simultaneously catch a slow leak and stay quiet during normal noise, whereas burn rate reframes the question as time-to-exhaustion.

**Negative test:** Alerting on the fast window alone — the brief spike then pages at burn rate 50 for a condition lasting one minute, and enough of those teach the on-call to mute the alert.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Recording rules used to precompute expensive, repeatedly-evaluated queries, with a naming convention.
- [ ] Alert rules tuned with an appropriate `for` duration, and Pending understood as a feature.
- [ ] Notification policies, grouping, and expiring silences applied.
- [ ] SLOs expressed as error budgets, with multi-window burn-rate alerting.
