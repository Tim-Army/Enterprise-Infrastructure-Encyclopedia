# Chapter 07: Alerting, Thresholds, and Noise

## Learning Objectives

- Set thresholds from baselines rather than round numbers.
- Suppress dependent alerts so one failure produces one alert.
- Design escalation and de-duplication that respect on-call attention.
- Measure and reduce alert fatigue.

## Alert fatigue is the failure mode

Every monitoring deployment eventually faces the same crisis: it generates more alerts than anyone can read, so people stop reading them, and the platform's value collapses to zero — worse than zero, because the organization believes it is monitored.

Alert design is therefore not a configuration detail but the discipline that determines whether monitoring works at all. Four techniques carry most of the benefit:

1. **Baseline-derived thresholds** instead of arbitrary round numbers.
2. **Dependency suppression** so one root failure yields one alert.
3. **Duration and hysteresis** so transient spikes do not page anyone.
4. **Severity and routing** so the right alerts reach the right people at the right hour.

## Thresholds

"Alert at 80% CPU" is the canonical bad threshold: it fires constantly on a batch server that legitimately runs at 90%, and never fires on an idle web server that has quietly doubled to 40%. Both outcomes are wrong.

**Baseline-derived thresholds** compare against the metric's own normal behavior — its mean and standard deviation, ideally for that hour and day of week, since almost every real workload is cyclical. A deviation from *its own* pattern is the signal; an absolute number is a guess about a machine you have not looked at.

Two refinements matter:

- **Duration** — require the condition to persist (5 minutes, 3 consecutive polls) so momentary spikes are ignored.
- **Hysteresis** — clear at a lower value than you trigger at (trigger 90%, clear 75%), or a metric hovering at the threshold flaps and generates alert storms.

## Dependency suppression

Chapter 03 built topology-aware root cause for reachability. The same logic generalizes: if a parent is down, its children's alerts are **consequences**, not incidents. Suppress them, and report one actionable alert.

## Severity and routing

Not every alert deserves a page at 3 a.m. A useful discipline:

| Severity | Meaning | Route |
|:---|:---|:---|
| **Critical** | Users affected now; act immediately | Page on-call, any hour |
| **Warning** | Trending toward a problem; act this shift | Ticket/queue, business hours |
| **Informational** | Worth recording, not acting on | Log/dashboard only |

The test for "critical": **would you want to be woken for this?** If not, it is not critical, and labeling it so trains people to ignore the label.

## Hands-On Lab

Python models alert design. **Cost:** none.

### Lab 7.1 — Baseline thresholds beat round numbers

**Objective:** Compare fixed and baseline-derived thresholds on real-shaped data.

```bash
python3 - <<'EOF'
import statistics
# CPU for two servers over 10 polls; both currently at 62%
batch_server = [88,90,91,89,92,90,88,91,89,62]     # normally ~90 (batch workload)
web_server   = [18,20,19,21,20,19,22,20,21,62]     # normally ~20 (web workload)

for name, series in (("batch-01", batch_server), ("web-01", web_server)):
    history, current = series[:-1], series[-1]
    mean = statistics.mean(history)
    sd = statistics.pstdev(history) or 1
    z = (current - mean) / sd
    fixed = "ALERT" if current > 80 else "ok"
    baseline = "ALERT" if abs(z) > 3 else "ok"
    print(f"{name}: current={current}%  baseline={mean:.0f}%±{sd:.1f}  z={z:+.1f}")
    print(f"    fixed threshold (>80%):    {fixed}")
    print(f"    baseline threshold (3σ):   {baseline}\n")
print("Fixed 80% threshold: silent on BOTH — yet web-01 has TRIPLED against its own normal.")
print("Baseline threshold: flags web-01 (real anomaly) and stays quiet on batch-01 (normal drop).")
EOF
```

**Expected result:** At an identical 62% CPU, the fixed threshold says nothing about either server, while the baseline threshold flags **web-01** — which has tripled against its own normal — and correctly ignores batch-01, where 62% is simply a quiet moment. The same absolute number is unremarkable on one server and a genuine anomaly on the other, which is precisely why round-number thresholds both miss incidents and generate noise.

**Negative test:** Applying one global CPU threshold across a mixed estate — you will tune it upward to silence the batch servers, and in doing so guarantee it never fires for the web tier.

**Cleanup:** None.

### Lab 7.2 — Dependency suppression and de-duplication

**Objective:** Turn an alert storm into one actionable alert.

```bash
python3 - <<'EOF'
parents = {"srv-1":"acc-1","srv-2":"acc-1","acc-1":"dist-a","acc-2":"dist-a","dist-a":"core-1","core-1":None}
raw_alerts = [
  {"node":"dist-a","msg":"node down"},
  {"node":"acc-1", "msg":"node unreachable"},
  {"node":"acc-2", "msg":"node unreachable"},
  {"node":"srv-1", "msg":"node unreachable"},
  {"node":"srv-2", "msg":"node unreachable"},
  {"node":"srv-1", "msg":"node unreachable"},          # duplicate
  {"node":"app-x", "msg":"HTTP check failed"},          # rides on srv-1
]
down = {a["node"] for a in raw_alerts}
def suppressed_by(node):
    p = parents.get(node)
    while p:
        if p in down: return p
        p = parents.get(p)
    return None

seen, emitted, suppressed = set(), [], []
for a in raw_alerts:
    key = (a["node"], a["msg"])
    if key in seen:
        suppressed.append((a["node"], "duplicate")); continue
    seen.add(key)
    parent = suppressed_by(a["node"])
    (suppressed.append((a["node"], f"downstream of {parent}")) if parent else emitted.append(a))

print(f"raw alerts: {len(raw_alerts)}")
for a in emitted:     print(f"  EMIT      {a['node']:7} {a['msg']}")
for n, why in suppressed: print(f"  suppress  {n:7} ({why})")
print(f"\n{len(raw_alerts)} raw -> {len(emitted)} actionable alert(s). On-call is paged once, for the right device.")
EOF
```

**Expected result:** Seven raw alerts collapse to **one** — `dist-a` node down — with the rest suppressed as downstream or duplicate. Note that `app-x`'s failed HTTP check is suppressed too, because its host is behind the failed switch: dependency suppression works across layers, not just within the network. One failure, one page, correct device.

**Negative test:** Emitting every alert and relying on the responder to correlate — during a real incident that correlation happens under time pressure, at 3 a.m., which is exactly when people make mistakes.

**Cleanup:** None.

### Lab 7.3 — Measure alert fatigue

**Objective:** Quantify whether your alerting is worth reading.

```bash
python3 - <<'EOF'
weeks = [
  {"week":"W1","alerts":840,"acted_on":42,"pages_out_of_hours":31},
  {"week":"W2","alerts":790,"acted_on":38,"pages_out_of_hours":28},
  {"week":"W3","alerts":120,"acted_on":38,"pages_out_of_hours":6},   # after tuning
]
for w in weeks:
    signal = w["acted_on"]/w["alerts"]*100
    verdict = ("SEVERE FATIGUE — >95% noise" if signal < 5 else
               "poor" if signal < 15 else
               "healthy — most alerts are acted on")
    print(f"{w['week']}: {w['alerts']:>4} alerts, {w['acted_on']:>3} acted on "
          f"({signal:4.1f}% signal), {w['pages_out_of_hours']:>2} out-of-hours pages -> {verdict}")
print("\nW1/W2: ~5% signal — responders are trained to ignore alerts, so real incidents are missed.")
print("W3: same 38 real issues found, 120 alerts instead of 840, out-of-hours pages 31 -> 6.")
print("Tuning did not reduce COVERAGE; it removed noise. Signal ratio is the metric to track.")
EOF
```

**Expected result:** Weeks 1 and 2 run at roughly 5% signal — 95% noise, the condition in which people stop reading alerts — while week 3, after tuning, surfaces the **same 38 real issues** from 120 alerts instead of 840, and cuts out-of-hours pages from 31 to 6. The critical detail is that coverage did not change: tuning removed noise, not detection. Tracking the **signal ratio** turns "our alerting is noisy" into a number you can manage.

**Negative test:** Reducing alert volume by disabling alert rules wholesale — the volume drops and so does the acted-on count, which is a coverage loss disguised as a tuning win. Always check both numbers together.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Thresholds derived from each metric's own baseline rather than global round numbers.
- [ ] Duration and hysteresis applied to prevent flapping.
- [ ] Dependency suppression and de-duplication reducing a storm to one actionable alert.
- [ ] Severity mapped to routing, with "would you be woken for this?" as the critical test.
- [ ] Alert fatigue measured by signal ratio, with coverage checked alongside volume.
