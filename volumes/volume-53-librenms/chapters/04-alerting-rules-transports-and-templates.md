# Chapter 04: Alerting — Rules, Transports, and Templates

## Learning Objectives

- Write alert rules with the rule builder / query language.
- Configure transports to deliver notifications.
- Customize alert templates.
- Use acknowledgements and maintenance windows.
- Complete a walkthrough for each alerting building block.

## Theory and Architecture

LibreNMS **alerting** evaluates **alert rules** (SQL-like conditions over device/port/
sensor state) on a schedule; when a rule matches, it fires through **transports**
(email, Slack, webhook, PagerDuty, etc.) rendered by **templates** (the message body).
Operators **acknowledge** alerts and set **maintenance windows** (scheduled downtime) to
suppress noise during planned work. Rules have severity, delay, and max-alert limits.

## Design Considerations

Write **specific** rules (scope by device group), set **delays** to avoid flapping,
route by **severity** to the right transport, and template messages with the context
responders need. Use **maintenance windows** during changes so you don't alert-storm.

## Implementation and Automation

The labs use the API/CLI to create a rule, add a transport, template it, and set a
maintenance window.

## Validation and Troubleshooting

Confirm the model:

```text
Alert rule (condition + severity + delay) -> matches -> transport (email/Slack/webhook)
rendered by a template. Ack silences an active alert; maintenance suppresses during a window.
```

Common pitfalls: overly broad rules (alert storms); and no **maintenance window** during
planned work.

## Security and Best Practices

Scope rules to **device groups**, add **delays** to kill flaps, route by **severity**,
secure transport credentials, and always schedule **maintenance windows** for planned
changes. Review alert history to tune noisy rules.

## Hands-On Lab

Alerting walkthroughs. **Shared prerequisites** — a running LibreNMS with a device;
`$LNMS`/`$TOKEN`. **Cost:** none.

### Lab 4.1 — Create an alert rule

**Objective:** Alert when a device goes down.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -X POST "$LNMS/api/v0/rules" \
  -d '{"name":"device-down","severity":"critical","disabled":0,"count":-1,"delay":"5m",
       "builder":"{\"condition\":\"AND\",\"rules\":[{\"field\":\"devices.status\",\"operator\":\"equal\",\"value\":\"0\"}]}"}'
```

**Expected result:** a **critical "device-down"** rule with a 5-minute delay — the
alerting condition.

**Negative test:** alert on the first missed poll (no delay); a **delay** prevents
transient-blip flapping.

**Cleanup:** delete the rule.

### Lab 4.2 — Configure a transport

**Objective:** Add a webhook transport.

```bash
# Settings > Alerts > Transports (or API): create a webhook transport
curl -sS -H "X-Auth-Token: $TOKEN" "$LNMS/api/v0/alerts" \
  | python3 -c "import sys,json;print('active alerts:',json.load(sys.stdin).get('count',0))"
# transport: webhook -> https://receiver.example/alert
```

**Expected result:** a transport configured to deliver alerts (and the active-alert
count) — the delivery path.

**Negative test:** write rules with **no transport**; alerts fire but nobody is notified
— configure delivery.

**Cleanup:** remove the transport.

### Lab 4.3 — Customize a template

**Objective:** Describe a template with useful context.

```text
# Alert template (Jinja-like): include device, rule, and value context.
{{ alert.title }} on {{ alert.hostname }} — severity {{ alert.severity }}
Rule: {{ alert.name }}  Timestamp: {{ alert.timestamp }}
```

**Expected result:** a template rendering **device + rule + severity** context —
actionable notifications.

**Negative test:** send bare "alert fired" messages; **template** in the context
responders need to triage.

**Cleanup:** revert the template if changed.

### Lab 4.4 — Set a maintenance window

**Objective:** Suppress alerts during planned work.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -X POST "$LNMS/api/v0/devices/127.0.0.1/maintenance" \
  -d '{"duration":"02:00","title":"planned upgrade","notes":"firmware"}'
```

**Expected result:** a **2-hour maintenance window** on the device — alerts suppressed
during the change.

**Negative test:** upgrade without a maintenance window; you generate a **false-alarm
storm** — schedule maintenance.

**Cleanup:** let the window expire or remove it.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alerting is rules (conditions with severity/delay) firing through transports rendered by
templates, with acknowledgements and maintenance windows to control noise. This chapter
built a rule, a transport, a template, and a maintenance window.

- [ ] I can write a scoped, delayed alert rule.
- [ ] I can configure a delivery transport.
- [ ] I can template notifications with context.
- [ ] I can set maintenance windows for planned work.
- [ ] I completed Labs 4.1–4.4 including each negative test.
