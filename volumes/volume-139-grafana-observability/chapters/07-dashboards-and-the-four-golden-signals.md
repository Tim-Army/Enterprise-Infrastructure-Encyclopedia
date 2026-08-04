# Chapter 07: Dashboards and the Four Golden Signals

## Learning Objectives

- Apply the Four Golden Signals — latency, traffic, errors, saturation.
- Compare them with the RED and USE methods, and know when each fits.
- Design dashboards that answer a question rather than display everything available.
- Choose visualizations and thresholds that communicate honestly.

## The Four Golden Signals

The GROT Academy curriculum builds its dashboard module on the **Four Golden Signals**, a framing from Google's site-reliability practice. The point is that four measures cover most of what you need to know about a user-facing service:

| Signal | What it measures | Typical query shape |
|:---|:---|:---|
| **Latency** | How long requests take — **split successful from failed** | `histogram_quantile` over request duration |
| **Traffic** | How much demand — requests/second, transactions/minute | `sum(rate(requests_total[5m]))` |
| **Errors** | Rate of failing requests, explicit and implicit | `sum(rate(requests_total{code=~"5.."}[5m]))` |
| **Saturation** | How full the system is — the constrained resource | CPU, memory, queue depth, connection pool |

The latency subtlety is the one people miss: **failed requests are often fast**. A service returning instant 500s looks *better* on an undifferentiated latency graph than a healthy one, because the errors drag the average down. Always separate success latency from error latency.

Saturation is the forward-looking signal — it tells you what will break next, whereas the other three tell you what is happening now.

## RED and USE

Two related framings, each suited to a different subject:

| Method | Measures | Applies to |
|:---|:---|:---|
| **RED** | Rate / Errors / Duration | **Services** — the request-handling view |
| **USE** | Utilization / Saturation / Errors | **Resources** — CPU, disk, network, pools |

RED is essentially the Golden Signals minus saturation, applied per service. USE is the resource-side complement. Use RED for the services your users call and USE for the infrastructure beneath them; between them they cover both "are requests being served?" and "what is running out?"

## Dashboard design

A dashboard that shows everything communicates nothing. The discipline is the same as for reports and alerts: **decide the audience and the question first.**

| Audience | Question | Design |
|:---|:---|:---|
| **On-call, mid-incident** | Is it broken, and where? | Few panels, large, above the fold; the Four Golden Signals for the top services |
| **Service owner** | How is my service behaving? | RED per endpoint, dependencies, saturation trends |
| **Capacity planning** | What runs out, and when? | Long time ranges, trends, headroom |
| **Executive** | Are we meeting commitments? | SLO attainment and error budget, nothing else |

Practical rules that follow:

- **Most important panel top-left** — that is where eyes land first.
- **Consistent time range** across panels, or you are comparing different moments.
- **Units and axes labeled**; a number without a unit invites misreading.
- **Thresholds that mean something** — red should mean "act," not "above an arbitrary line."
- **Y-axis starting at zero for rates and counts**, or a trivial fluctuation looks like a cliff.

That last one is the commonest way a dashboard misleads honest people.

## Hands-On Lab

Python models dashboard design. **Cost:** none.

### Lab 7.1 — The Four Golden Signals, with latency split

**Objective:** Show why undifferentiated latency hides an outage.

```bash
python3 - <<'EOF'
# During the incident the service returns fast 500s
windows = [
  {"t":"09:00","ok":980,"err":20,  "ok_p99":420,"err_p99":410},
  {"t":"09:05","ok":975,"err":25,  "ok_p99":435,"err_p99":405},
  {"t":"09:10","ok":300,"err":700, "ok_p99":2100,"err_p99":12},   # <-- incident
]
print(f"{'time':>6}{'traffic/s':>11}{'error %':>10}{'p99 ALL':>10}{'p99 OK':>9}{'p99 ERR':>9}")
for w in windows:
    total = w["ok"] + w["err"]
    err_pct = w["err"]/total*100
    blended = (w["ok"]*w["ok_p99"] + w["err"]*w["err_p99"]) / total     # naive mixed latency
    print(f"{w['t']:>6}{total/60:>11.1f}{err_pct:>9.1f}%{blended:>10.0f}{w['ok_p99']:>9}{w['err_p99']:>9}")

print("\nAt 09:10 the blended p99 is ~640ms — only ~50% worse than normal, easy to dismiss.")
print("Split apart: successful requests degraded to 2100ms (5x) and 70% of traffic is FAILING.")
print("\nFast failures make an undifferentiated latency graph look BETTER than reality.")
print("Always split latency by outcome — and read errors and traffic alongside it, never alone.")
EOF
```

**Expected result:** The blended p99 rises modestly to about 640 ms while successful-request latency has quintupled and 70% of traffic is failing. This is the concrete case for the Golden Signals being read *together*: any one of them in isolation understates the incident, and blended latency actively conceals it.

**Negative test:** Alerting on overall p99 latency alone — a service failing fast can hold latency flat or even improve it while serving errors to most users.

**Cleanup:** None.

### Lab 7.2 — Design for the audience

**Objective:** Build the right dashboard for the question.

```bash
python3 - <<'EOF'
CATALOG = {
  "golden signals (top services)":{"noc":5,"owner":4,"capacity":1,"exec":1},
  "RED per endpoint":             {"noc":2,"owner":5,"capacity":1,"exec":0},
  "dependency health":            {"noc":4,"owner":4,"capacity":1,"exec":0},
  "saturation trend (30d)":       {"noc":1,"owner":3,"capacity":5,"exec":1},
  "capacity headroom forecast":   {"noc":0,"owner":2,"capacity":5,"exec":2},
  "SLO attainment + error budget":{"noc":3,"owner":4,"capacity":1,"exec":5},
  "per-pod CPU (200 pods)":       {"noc":1,"owner":2,"capacity":2,"exec":0},
  "deployment annotations":       {"noc":4,"owner":4,"capacity":0,"exec":0},
}
LIMIT = {"noc":6, "owner":8, "capacity":6, "exec":3}
for aud, cap in LIMIT.items():
    ranked = sorted(CATALOG.items(), key=lambda kv: -kv[1][aud])
    chosen = [name for name, s in ranked if s[aud] >= 3][:cap]
    dropped = [name for name, s in ranked if s[aud] < 3]
    print(f"\n{aud.upper()} dashboard ({len(chosen)} panels, limit {cap}):")
    for c in chosen: print(f"   + {c}")
    print(f"   omitted: {len(dropped)} panel(s) that do not serve this question")
print("\nThe executive dashboard is THREE panels. That is not laziness — every extra panel")
print("dilutes the one number that audience needs to act on.")
print("\n'per-pod CPU (200 pods)' serves almost nobody: 200 series on one panel is unreadable.")
print("Aggregate it, or show only the top N by usage.")
EOF
```

**Expected result:** Each audience gets a small, targeted panel set, with the executive view down to three. The per-pod CPU observation generalizes usefully: a panel with 200 series is decorative rather than informative, and the fix is aggregation or a top-N selection — the same "aggregate at the source" instinct from Chapter 03.

**Negative test:** Building one dashboard for everyone — it is too detailed for executives, too shallow for owners, and too cluttered for on-call at 3 a.m.

**Cleanup:** None.

### Lab 7.3 — Axes and thresholds that do not mislead

**Objective:** Show how presentation choices distort the same data.

```bash
python3 - <<'EOF'
values = [982, 985, 979, 991, 986, 988, 984]     # requests/sec — essentially flat
lo, hi = min(values), max(values)

def render(y_min, y_max, label):
    print(f"\n{label}  (y-axis {y_min}..{y_max})")
    for v in values:
        pos = int((v - y_min) / (y_max - y_min) * 40)
        print(f"   {v:>4} |{' ' * pos}#")

render(lo - 1, hi + 1, "TRUNCATED axis (auto-scaled to the data)")
print("   -> looks like violent, alarming swings")
render(0, hi * 1.1, "ZERO-BASED axis")
print("   -> looks like what it is: a flat line varying by ~1%")

print(f"\nSame numbers. Range is {hi-lo} req/s on a base of ~985 — about {(hi-lo)/985*100:.1f}% variation.")
print("Auto-scaling is the DEFAULT in most tools, which is why so many dashboards look dramatic.")
print("For rates and counts, start the axis at ZERO.")

print("\n--- thresholds ---")
for name, warn, crit, why in [
  ("CPU %",            70, 90, "meaningful: sustained >90% means saturation"),
  ("p99 latency (ms)", 500, 1000, "meaningful IF tied to your SLO — otherwise arbitrary"),
  ("error rate %",     1, 5, "meaningful: tie to the error budget, not a round number"),
  ("memory %",         70, 80, "MISLEADING for JVM/Go: high heap use is NORMAL, not a problem"),
]:
    print(f"   {name:18} warn>{warn:<5} crit>{crit:<5} {why}")
print("\nRed should mean ACT. A threshold that goes red during normal operation trains people")
print("to ignore the color — the dashboard equivalent of alert fatigue.")
EOF
```

**Expected result:** A 1.2% variation looks like violent swings on an auto-scaled axis and correctly flat on a zero-based one. Since auto-scaling is the default in most tools, this is a distortion people ship accidentally. The threshold table then makes the parallel point — a red that appears during healthy operation teaches viewers to disregard the color entirely.

**Negative test:** Leaving auto-scaling on a traffic panel and treating every visual dip as an incident — you will investigate noise repeatedly and eventually stop trusting the panel.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Four Golden Signals applied, with latency split by outcome.
- [ ] RED and USE matched to services and resources respectively.
- [ ] Dashboards designed per audience and question, with panel counts kept small.
- [ ] Zero-based axes used for rates, and thresholds tied to meaning rather than round numbers.
