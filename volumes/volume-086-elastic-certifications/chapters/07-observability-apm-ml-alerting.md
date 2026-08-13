# Chapter 07: Observability Engineer — APM, ML, and Alerting

## Learning Objectives

- Analyze application performance with the APM app.
- Analyze real-user-monitoring (RUM) data.
- Define a machine-learning anomaly job on observability data.
- Define a Kibana alert.
- Complete a walkthrough for each APM-ML-alerting topic.

## Theory and Architecture

The **Observability Engineer** exam's second half covers application performance, anomaly detection, and
reacting to events. **APM (Application Performance Monitoring)** instruments services (with APM agents or
OpenTelemetry) to capture transactions, spans, errors, and dependencies, analyzed in the **APM app** —
service maps, latency distributions, and error rates. **RUM (Real User Monitoring)**, via the **Real
Experience app**, captures the performance real browsers experience. **Machine learning** anomaly jobs
learn the normal baseline of a metric, log rate, or latency and flag deviations — either the **predefined
jobs** or ones you **define** in Kibana. **Kibana Alerts** fire rules (threshold, anomaly, uptime,
error-rate) and send actions to connectors (email, Slack, PagerDuty, webhook) so teams react
automatically. This chapter teaches APM, ML, and alerting with hands-on walkthroughs.

## Design Considerations

Instrument services with **APM** (or OpenTelemetry) to see transactions and dependencies, and add **RUM**
for the real browser experience. Use **ML anomaly jobs** where static thresholds fail (seasonal or
noisy signals), starting with the **predefined** jobs. Define **alerts** on the signals you will act on
(SLO burn, error spikes, anomalies) and route them to the right connector. Avoid alert noise with
sensible thresholds and de-duplication.

## Implementation and Automation

The labs reason about APM/RUM analysis, define an ML anomaly job, and define a Kibana alert — the
performance analysis and reaction the exam validates.

## Validation and Troubleshooting

Confirm APM, ML, and alerting:

```text
APM: transactions/spans/errors/dependencies -> APM app (service map, latency, errors)
RUM: real browser performance -> Real Experience app
ML: anomaly jobs learn a baseline -> flag deviations (predefined or custom)
Alerts: rules (threshold/anomaly/uptime) -> connectors (email/Slack/PagerDuty/webhook)
```

Common pitfalls: static thresholds on seasonal metrics (constant false alarms) — use an **ML anomaly
job**; and alerts with no **connector** (nobody is notified).

## Security and Best Practices

Protect APM tokens, scope alert connectors, and review ML jobs for drift. Observability and alerting
defend your own systems. All work is authorized.

## Hands-On Lab

APM-ML-alerting walkthroughs. **Shared prerequisites** — an Elastic Stack with APM and ML (or the
concepts, modeled in `python3`), `curl`. **Cost:** none.

### Lab 7.1 — Reason about APM and RUM

**Objective:** Map application performance signals.

```python
python3 - <<'PY'
apm = {
  "Transactions": "request latency + throughput per service",
  "Spans":        "downstream calls (DB, HTTP) within a transaction",
  "Errors":       "exceptions with stack traces",
  "Service map":  "dependencies between services",
  "RUM":          "Real Experience app — actual browser load times",
}
for k, v in apm.items():
    print(f"{k:12}: {v}")
print("APM = server-side performance; RUM = client-side real-user performance")
PY
```

**Expected result:** the APM signals and RUM mapped — full-stack performance visibility.

**Negative test:** judge user experience from server latency alone; add **RUM** for what the browser
actually experiences.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Define a machine-learning anomaly job

**Objective:** Detect deviations from the baseline.

```bash
curl -s -k -u elastic:$PW -X PUT "https://localhost:9200/_ml/anomaly_detectors/high_latency" -H 'Content-Type: application/json' -d'
{ "analysis_config": {
    "bucket_span": "15m",
    "detectors": [ { "function": "high_mean", "field_name": "transaction.duration.us" } ] },
  "data_description": { "time_field": "@timestamp" } }'
```

```json
{ "job_id": "high_latency", "job_type": "anomaly_detector", "state": "closed" }
```

**Expected result:** an ML job that learns normal transaction latency and flags high-mean anomalies.

**Negative test:** set a fixed latency threshold on a service with daily peaks; it alarms every peak —
use an **anomaly job** that learns the pattern.

**Rollback:**

```bash
curl -s -k -u elastic:$PW -X DELETE "https://localhost:9200/_ml/anomaly_detectors/high_latency"
```

### Lab 7.3 — Define a Kibana alert

**Objective:** React automatically to a condition.

```text
Kibana > Observability > Alerts > Create rule
  Rule type: APM latency threshold
  Condition: transaction.duration p95 > 500ms over 5m for service "checkout"
  Connector: email -> sre-oncall@lab.local (+ Slack)
Result: sustained high checkout latency raises an alert and notifies on-call
```

**Expected result:** a rule that fires on sustained high latency and notifies the on-call team —
automatic reaction.

**Negative test:** create a rule with no **connector**; it fires silently and nobody responds — attach a
connector.

**Rollback:** disable the practice rule if not needed.

### Lab 7.4 — Correlate an anomaly to an alert

**Objective:** Close the detect-to-react loop.

```python
python3 - <<'PY'
event = {
  "10:02": "ML anomaly: transaction.duration high on checkout (score 92)",
  "10:03": "Alert rule fires: p95 latency > 500ms for 5m",
  "10:03b":"Connector notifies SRE on-call (email + Slack)",
  "10:15": "SRE finds slow DB span in APM service map -> mitigates",
}
for t, e in event.items():
    print(f"{t:6}: {e}")
print("Loop: ML detects -> alert notifies -> APM pinpoints -> mitigate")
PY
```

**Expected result:** the detect→notify→diagnose→mitigate loop — observability driving action.

**Negative test:** collect data but never alert or investigate; observability is only useful when it
**drives reaction**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Observability Engineer analyzes application performance with the APM app (transactions, spans, errors,
service maps) and RUM, detects deviations with machine-learning anomaly jobs, and reacts through Kibana
alerts routed to connectors — closing the detect-to-react loop.

- [ ] I can analyze application performance with APM and RUM.
- [ ] I can define a machine-learning anomaly job.
- [ ] I can define a Kibana alert.
- [ ] I can correlate an anomaly to an alert and action.
- [ ] I completed Labs 7.1–7.4 including each negative test.
