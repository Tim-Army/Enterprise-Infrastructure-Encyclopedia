# Chapter 08: Alertmanager

## Learning Objectives

- Explain Alertmanager's role and the routing tree.
- Configure grouping, receivers, and routes.
- Suppress noise with inhibition and silences.
- Validate config with amtool.
- Complete a walkthrough for each Alertmanager feature.

## Theory and Architecture

**Alertmanager** takes alerts fired by Prometheus and handles **deduplication**,
**grouping**, **routing**, **inhibition**, and **silencing** before dispatching
**notifications** to receivers (email, Slack, PagerDuty, webhook). A **routing tree**
matches alert labels to routes, each with a **receiver** and grouping/timing
(`group_by`, `group_wait`, `repeat_interval`). **Inhibition** suppresses lower-priority
alerts when a higher-priority one fires (e.g., mute node alerts when the cluster is
down). **Silences** temporarily mute matching alerts (planned maintenance). It runs as an
HA cluster to avoid duplicate notifications.

## Design Considerations

Route by **severity/team** labels, **group** related alerts to cut noise, use
**inhibition** to suppress downstream alerts, and **silence** during maintenance. Set
`repeat_interval` sensibly and run Alertmanager **highly available**.

## Implementation and Automation

The labs configure routing/grouping, inhibition, a silence, and validate with amtool.

## Validation and Troubleshooting

Confirm the model:

```text
Alertmanager: dedup + group + route + inhibit + silence -> receivers.
Routing tree: match labels -> receiver + group_by/group_wait/repeat_interval.
Inhibition: high-sev alert mutes matching low-sev alerts. Silence: temporary mute.
amtool check-config alertmanager.yml.
```

Common pitfalls: no **grouping** (one notification per alert = storm); and silences that
never expire.

## Security and Best Practices

**Group** related alerts, route by **labels**, use **inhibition** to suppress cascades,
**silence** only with an expiry during maintenance, secure receiver credentials, and run
**HA**. Validate config with amtool before reload.

## Hands-On Lab

Alertmanager walkthroughs. **Shared prerequisites** — Docker; the Alertmanager image
(amtool). **Cost:** none.

### Lab 8.1 — Configure routing and grouping

**Objective:** Route critical alerts and group them.

```yaml
# alertmanager.yml
route:
  receiver: default
  group_by: [alertname, cluster]
  group_wait: 30s
  repeat_interval: 4h
  routes:
    - matchers: [ severity="critical" ]
      receiver: pager
receivers:
  - name: default
  - name: pager
    webhook_configs: [ { url: "http://receiver.example/pager" } ]
```

**Expected result:** a route sending **critical** alerts to `pager`, grouped by
alertname/cluster — the routing tree.

**Negative test:** route everything to one receiver with no grouping; you get an alert
**storm** — group and route by labels.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Validate the config

**Objective:** Check the Alertmanager config.

```bash
docker run --rm -v "$PWD/alertmanager.yml:/a.yml" \
  prom/alertmanager:latest amtool check-config /a.yml
```

**Expected result:** **config validates** (routes/receivers OK) — safe to load.

**Negative test:** reference a receiver that isn't defined; `amtool check-config`
**errors** — catch it before reload.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Add an inhibition rule

**Objective:** Suppress downstream alerts.

```yaml
inhibit_rules:
  - source_matchers: [ severity="critical", alertname="ClusterDown" ]
    target_matchers: [ severity="warning" ]
    equal: [ cluster ]
```

**Expected result:** warnings in the same cluster are **muted** while ClusterDown fires
— inhibition suppressing cascades.

**Negative test:** page for every node alert during a full cluster outage; **inhibition**
mutes the noise — configure it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Create a silence

**Objective:** Mute alerts during maintenance.

```bash
docker run --rm --network host prom/alertmanager:latest \
  amtool silence add alertname="TargetDown" instance="a" \
  --comment "maintenance" --duration 2h --alertmanager.url http://localhost:9093
```

**Expected result:** a **2-hour silence** matching the alert — suppression during planned
work.

**Negative test:** create a silence with no expiry; it mutes alerts **indefinitely** —
always set a duration.

**Rollback:** expire/remove the silence with `amtool silence expire`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alertmanager deduplicates, groups, routes, inhibits, and silences alerts before
notifying receivers, configured by a label-matching routing tree and validated with
amtool. This chapter configured routing/grouping, inhibition, and a silence.

- [ ] I can configure routing and grouping.
- [ ] I can validate config with amtool.
- [ ] I can suppress cascades with inhibition.
- [ ] I can create an expiring silence.
- [ ] I completed Labs 8.1–8.4 including each negative test.
