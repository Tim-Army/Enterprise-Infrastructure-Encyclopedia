# Chapter 08: Dashboards, Reporting, and Capacity Planning

## Learning Objectives

- Design dashboards for a specific audience and question.
- Produce SLA and availability reports that withstand scrutiny.
- Forecast capacity from trend data and act before exhaustion.
- Distinguish percentile from average when reporting performance.

## Dashboards answer questions

The commonest dashboard mistake is building one that displays everything available rather than answering a question someone actually has. A dashboard should have an **audience** and a **decision** attached:

| Audience | Question | Content |
|:---|:---|:---|
| **NOC / on-call** | What is broken right now? | Active alerts, current outages, top talkers — nothing historical |
| **Engineer** | Why is this broken? | Deep metrics, correlated timelines, per-component detail |
| **IT management** | Are we meeting our commitments? | SLA attainment, trends, incident counts |
| **Executive** | Is the service healthy and adequately funded? | A handful of business-relevant indicators, capacity runway |

The NOC view and the executive view are genuinely different artifacts, and trying to serve both from one screen produces something that serves neither.

## Averages lie; percentiles do not

An average response time hides the tail where the pain lives. If 95% of requests complete in 100 ms and 5% take 10 seconds, the average is a comfortable 595 ms — and one user in twenty is having an unusable experience.

Report **percentiles**: p50 (the typical experience), p95 and p99 (the tail). SLAs should be written against percentiles too — "95% of transactions under 2 seconds" is measurable and meaningful; "average under 2 seconds" can be met while a fifth of users suffer.

## Capacity planning

Capacity planning is arithmetic on trend data: measure the growth rate, extrapolate to the limit, and subtract the lead time for doing something about it.

**Runway = (capacity − current) ÷ growth rate.** The number to compare it against is not zero but your **procurement and change lead time**. A disk with 60 days of runway and a 90-day procurement cycle is already late.

## Hands-On Lab

Python models reporting and forecasting. **Cost:** none.

### Lab 8.1 — Percentiles versus averages

**Objective:** Show what an average conceals.

```bash
python3 - <<'EOF'
import statistics
# 100 requests: 95 fast, 5 pathological
latencies = [100]*95 + [10000]*5

def pct(data, p):
    s = sorted(data)
    return s[min(int(len(s)*p/100), len(s)-1)]

print(f"requests: {len(latencies)}")
print(f"average : {statistics.mean(latencies):8.0f} ms   <- looks acceptable")
print(f"p50     : {pct(latencies,50):8.0f} ms")
print(f"p95     : {pct(latencies,95):8.0f} ms   <- the tail appears")
print(f"p99     : {pct(latencies,99):8.0f} ms")
sla_ms = 2000
meets_avg = statistics.mean(latencies) <= sla_ms
meets_p95 = pct(latencies,95) <= sla_ms
print(f"\nSLA '{sla_ms} ms': by AVERAGE -> {'MET' if meets_avg else 'BREACHED'}; "
      f"by p95 -> {'MET' if meets_p95 else 'BREACHED'}")
print("5 users in 100 wait 10 seconds. The average says everything is fine.")
EOF
```

**Expected result:** The average lands at 595 ms and passes a 2-second SLA, while p95 sits at 10,000 ms and breaches it badly. Same data, opposite conclusions — and the percentile view is the one that matches what users experience. This is why performance SLAs should always be written against a percentile.

**Negative test:** Reporting average response time to management — the graph looks healthy while the support queue fills with complaints, and the disagreement between the data and reality erodes trust in the monitoring.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — SLA reporting that survives scrutiny

**Objective:** Produce a defensible availability report.

```bash
python3 - <<'EOF'
PERIOD_MIN = 30*24*60
services = [
  {"name":"payments-api","target":99.95,"outage_min":18,"maintenance_min":120,"excl_maint":True},
  {"name":"intranet",    "target":99.5, "outage_min":300,"maintenance_min":60, "excl_maint":True},
  {"name":"reporting",   "target":99.0, "outage_min":600,"maintenance_min":0,  "excl_maint":False},
]
for s in services:
    measured = PERIOD_MIN - (s["maintenance_min"] if s["excl_maint"] else 0)
    avail = (measured - s["outage_min"]) / measured * 100
    budget = measured * (1 - s["target"]/100)
    remaining = budget - s["outage_min"]
    print(f"{s['name']:14} target {s['target']:>6}%  measured {avail:7.3f}%  "
          f"{'MET' if avail >= s['target'] else 'BREACHED'}")
    print(f"{'':14} outage {s['outage_min']:>4} min of {budget:6.1f} min budget "
          f"({remaining:+.1f} min remaining)"
          f"{'  [scheduled maintenance excluded]' if s['excl_maint'] else '  [maintenance counted]'}")
print("\nAlways state the exclusion rule: whether planned maintenance counts changes the number,")
print("and an SLA report that hides its methodology will not survive an audit.")
EOF
```

**Expected result:** payments-api meets 99.95% with a little budget left; intranet breaches; reporting meets 99% comfortably. The methodological point is in the closing lines — whether **scheduled maintenance is excluded** materially changes the availability figure, so a credible report states its exclusion rule up front rather than quietly choosing the flattering one.

**Negative test:** Reporting availability without defining downtime, the measurement interval, or maintenance exclusions — the number is unfalsifiable, and the first person who disagrees with it has no way to reconcile.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Capacity forecasting with lead time

**Objective:** Forecast exhaustion and compare against procurement reality.

```bash
python3 - <<'EOF'
resources = [
  {"name":"db-storage",   "used_pct":72,"growth_pct_per_month":4.5,"lead_time_days":90},
  {"name":"wan-link-eu",  "used_pct":68,"growth_pct_per_month":2.0,"lead_time_days":120},
  {"name":"vm-cluster-ram","used_pct":85,"growth_pct_per_month":1.5,"lead_time_days":45},
  {"name":"log-volume",   "used_pct":40,"growth_pct_per_month":9.0,"lead_time_days":30},
]
for r in resources:
    headroom = 100 - r["used_pct"]
    months = headroom / r["growth_pct_per_month"]
    days = months * 30
    lead = r["lead_time_days"]
    if days <= lead:
        verdict = f"ACT NOW — {days:.0f}d runway vs {lead}d lead time (ALREADY LATE)"
    elif days <= lead * 1.5:
        verdict = f"ORDER THIS MONTH — {days:.0f}d runway, {lead}d lead time"
    else:
        verdict = f"monitor — {days:.0f}d runway vs {lead}d lead time"
    print(f"{r['name']:16} {r['used_pct']:>3}% used  +{r['growth_pct_per_month']}%/mo  -> {verdict}")
print("\nRunway matters only relative to LEAD TIME. 186 days of headroom on a 120-day")
print("procurement cycle leaves 66 days of actual slack, not 186.")
EOF
```

**Expected result:** `vm-cluster-ram` (85% used, 300 days runway against a 45-day lead time) is comfortable, while `db-storage` at 72% with 4.5% monthly growth has ~187 days against a 90-day lead — order this quarter. The framing that matters: **runway is only meaningful net of lead time**, so the resource with the highest utilization is not automatically the most urgent.

**Negative test:** Triggering capacity work at a fixed utilization threshold like 80% — a slow-growing resource crosses 80% and sits there harmlessly for two years, while a fast-growing one goes from 60% to full inside a procurement cycle.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Dashboards designed per audience and per question, with NOC and executive views separated.
- [ ] Percentiles used in place of averages, and SLAs written against them.
- [ ] SLA reports produced with explicit methodology and maintenance-exclusion rules.
- [ ] Capacity forecast as runway measured against procurement lead time.
