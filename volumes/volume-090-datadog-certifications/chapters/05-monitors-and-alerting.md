# Chapter 05: Monitors and Alerting

## Learning Objectives

- Create a metric monitor with warning and alert thresholds.
- Route notifications to the right responders.
- Reason about anomaly and composite monitors.
- Define an SLO and a downtime.
- Complete a walkthrough for each monitor-and-alerting topic.

## Theory and Architecture

**Monitors** turn telemetry into action. A **metric monitor** evaluates a query against **thresholds**
(a **warning** level and an **alert** level) over a window and changes state (OK → Warn → Alert). Beyond
static thresholds, **anomaly** monitors learn a baseline and alert on deviations, **forecast** monitors
alert before a metric will cross a bound, and **composite** monitors combine several monitors with
logic. Alerts send **notifications** via message templates that `@`-mention destinations (**@slack-…**,
**@pagerduty-…**, email, webhook). **Service Level Objectives (SLOs)** track a target (e.g., 99.9%
availability) against an error budget, built on metrics or monitors. **Downtimes** mute alerts during
planned maintenance, and monitors can be **muted** to avoid noise. Good alerting is actionable, routed,
and free of noise. This chapter teaches monitors and alerting with hands-on walkthroughs (monitor JSON
via the API).

## Design Considerations

Alert on **symptoms** users feel (latency, errors, saturation), with a **warning** before the **alert**
level. Route notifications to the **owning team** with clear, templated messages (what, where, runbook
link). Use **anomaly/forecast** monitors where static thresholds fail. Track reliability with **SLOs**
and error budgets. Schedule **downtimes** for maintenance so you do not page on planned work. Reduce
noise — group, require sustained breaches, and mute known conditions.

## Implementation and Automation

The labs create a threshold monitor with notifications, and reason about anomaly monitors, SLOs, and
downtimes — the alerting the Fundamentals exam validates.

## Validation and Troubleshooting

Confirm monitors and alerting:

```text
Metric monitor: query vs thresholds (warning < alert) over a window -> OK/Warn/Alert
Types: metric | anomaly (learned baseline) | forecast | composite (logic across monitors)
Notifications: templated message @slack/@pagerduty/email/webhook (what/where/runbook)
SLO: target + error budget (on metrics/monitors); Downtime: mute during maintenance
```

Common pitfalls: paging on a **cause** metric (CPU) instead of a **symptom** (latency/errors); and no
**downtime** during maintenance, paging on planned work.

## Security and Best Practices

Route alerts to owners, keep messages actionable, and mute planned work with downtimes. Alerting protects
your own services' reliability. All work is authorized.

## Hands-On Lab

Monitor-and-alerting walkthroughs. **Shared prerequisites** — a Datadog account with an API/app key and
`curl`; `python3`. **Cost:** none.

### Lab 5.1 — Create a threshold monitor

**Objective:** Alert on high latency with a warning first.

```bash
curl -s -X POST "https://api.datadoghq.com/api/v1/monitor" \
  -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -H "Content-Type: application/json" -d '{
    "name": "High p95 latency - checkout",
    "type": "metric alert",
    "query": "avg(last_5m):p95:trace.http.request{service:checkout} > 0.5",
    "message": "p95 latency high on checkout. Runbook: ... @slack-sre",
    "options": { "thresholds": { "warning": 0.3, "critical": 0.5 } } }' \
  | python3 -c 'import sys,json;print("monitor id:",json.load(sys.stdin)["id"])'
```

```text
monitor id: 12345678
```

**Expected result:** a monitor that warns at 300ms and alerts at 500ms p95 latency, notifying SRE.

**Negative test:** set only a critical threshold with no warning; add a **warning** so you can act before
it's critical.

**Rollback:**

```bash
curl -s -X DELETE "https://api.datadoghq.com/api/v1/monitor/12345678" \
  -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}"
```

### Lab 5.2 — Route the notification

**Objective:** Page the right team.

```python
python3 - <<'PY'
msg = ("{{#is_alert}}CRITICAL{{/is_alert}} p95 latency high on {{service.name}}\n"
       "Dashboard: https://app.datadoghq.com/... \nRunbook: https://wiki/...\n"
       "@slack-sre-payments @pagerduty-payments")
print(msg)
print("Routed to the owning team with what/where/runbook -> actionable")
PY
```

**Expected result:** a templated, routed message with context and a runbook link — actionable alerting.

**Negative test:** send `"something is wrong"` to a shared channel; template the message with
**what/where/runbook** and route to the **owner**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Reason about anomaly monitors and SLOs

**Objective:** Handle seasonal metrics and track reliability.

```python
python3 - <<'PY'
print("Anomaly monitor: learns daily/weekly baseline -> alerts on deviation (not a fixed threshold)")
# SLO: 99.9% availability over 30 days
target, days = 0.999, 30
budget_min = round((1 - target) * days * 24 * 60, 1)
print(f"SLO 99.9%/30d -> error budget = {budget_min} minutes of downtime allowed")
PY
```

```text
Anomaly monitor: learns daily/weekly baseline -> alerts on deviation (not a fixed threshold)
SLO 99.9%/30d -> error budget = 43.2 minutes of downtime allowed
```

**Expected result:** an anomaly monitor for seasonal data and an SLO with a computed error budget.

**Negative test:** put a fixed threshold on a metric with daily peaks; use an **anomaly** monitor.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Schedule a downtime

**Objective:** Mute alerts during maintenance.

```bash
NOW=$(date +%s); END=$((NOW+3600))
curl -s -X POST "https://api.datadoghq.com/api/v1/downtime" \
  -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -H "Content-Type: application/json" -d "{
    \"scope\": [\"service:checkout\"], \"start\": ${NOW}, \"end\": ${END},
    \"message\": \"Planned deploy window\" }" \
  | python3 -c 'import sys,json;print("downtime id:",json.load(sys.stdin)["id"])'
```

```text
downtime id: 98765
```

**Expected result:** a one-hour downtime muting `checkout` alerts during the deploy — no paging on planned
work.

**Negative test:** deploy without a downtime and page the on-call for expected blips; schedule a
**downtime**.

**Rollback:**

```bash
curl -s -X DELETE "https://api.datadoghq.com/api/v1/downtime/98765" \
  -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}"
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Datadog monitors evaluate queries against warning and alert thresholds (or learned anomaly baselines,
forecasts, and composites), send templated, routed notifications to owning teams, track reliability with
SLOs and error budgets, and mute planned work with downtimes — alerting on user-facing symptoms, kept
actionable and noise-free.

- [ ] I can create a threshold monitor with warning and alert levels.
- [ ] I can route an actionable notification.
- [ ] I can reason about anomaly monitors and SLOs.
- [ ] I can schedule a downtime.
- [ ] I completed Labs 5.1–5.4 including each negative test.
