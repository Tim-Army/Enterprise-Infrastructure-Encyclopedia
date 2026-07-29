# Chapter 07: Recording and Alerting Rules

## Learning Objectives

- Write recording rules to precompute expressions.
- Write alerting rules with `for`, labels, and annotations.
- Validate and test rules with promtool.
- Understand alert states.
- Complete a walkthrough for each rule type.

## Theory and Architecture

**Rules** are PromQL evaluated on a schedule. **Recording rules** precompute expensive or
frequently-used expressions into new series (named by convention `level:metric:op`) so
dashboards/alerts query cheaply. **Alerting rules** evaluate a condition; when it holds
for the **`for`** duration, the alert transitions **pending → firing** and is sent to
Alertmanager. Alerts carry **labels** (for routing) and **annotations** (human context,
often templated). **`promtool`** checks rule files and can **unit-test** rules against
sample data.

## Design Considerations

Use **recording rules** for expensive queries reused across dashboards/alerts. Give
alerts a **`for`** to avoid flapping, meaningful **labels** (severity, team) for routing,
and **annotations** with actionable context. **Unit-test** rules so alert logic is
verified.

## Implementation and Automation

The labs write recording and alerting rules and validate/test them with promtool.

## Validation and Troubleshooting

Confirm the model:

```text
Recording rule: record: <name>, expr: <promql> -> new series.
Alerting rule: alert: <name>, expr, for: 10m, labels{}, annotations{}.
States: inactive -> pending (within 'for') -> firing. promtool check/test rules.
```

Common pitfalls: alerts with no **`for`** (flapping); and untested rule logic.

## Security and Best Practices

Precompute with **recording rules**, add **`for`** durations, label alerts for
**routing**, template **annotations** for context, and **unit-test** rules in CI.
Version rule files.

## Hands-On Lab

Rules walkthroughs. **Shared prerequisites** — Docker; the Prometheus image (promtool).
**Cost:** none.

### Lab 7.1 — Write a recording rule

**Objective:** Precompute a request rate.

```yaml
# rules.yml
groups:
  - name: recording
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(prometheus_http_requests_total[5m]))
```

**Expected result:** a new series **`job:http_requests:rate5m`** — a precomputed rate.

**Negative test:** recompute the same heavy query in every dashboard; a **recording
rule** computes it once — reuse it.

**Cleanup:** none.

### Lab 7.2 — Write an alerting rule

**Objective:** Alert on a target being down.

```yaml
groups:
  - name: alerts
    rules:
      - alert: TargetDown
        expr: up == 0
        for: 5m
        labels: { severity: critical }
        annotations: { summary: "{{ $labels.instance }} is down" }
```

**Expected result:** a **TargetDown** alert that fires after 5 minutes down — a
labeled, annotated alert.

**Negative test:** omit `for`; a single failed scrape **flaps** an alert — add a `for`
duration.

**Cleanup:** none.

### Lab 7.3 — Validate the rules

**Objective:** Check rule files with promtool.

```bash
docker run --rm -v "$PWD/rules.yml:/r.yml" prom/prometheus:latest \
  promtool check rules /r.yml
```

**Expected result:** **SUCCESS** with the rule count — syntactically valid rules.

**Negative test:** load rules with a PromQL error; Prometheus **won't evaluate** them —
`promtool check rules` catches it first.

**Cleanup:** none.

### Lab 7.4 — Unit-test an alert

**Objective:** Verify alert logic with a test file.

```yaml
# test.yml
rule_files: [ rules.yml ]
tests:
  - interval: 1m
    input_series: [ { series: 'up{instance="a"}', values: '0x10' } ]
    alert_rule_test:
      - eval_time: 6m
        alertname: TargetDown
        exp_alerts: [ { exp_labels: { severity: critical, instance: "a" } } ]
```

```bash
docker run --rm -v "$PWD:/w" -w /w prom/prometheus:latest promtool test rules test.yml
```

**Expected result:** **SUCCESS** — the alert fires as designed under test data.

**Negative test:** ship alert rules with no tests; **unit-test** them so logic changes
don't silently break alerting.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Rules are scheduled PromQL: recording rules precompute reused expressions, alerting rules
fire (after `for`) with routing labels and templated annotations, all validated and
unit-tested with promtool. This chapter wrote, validated, and tested rules.

- [ ] I can write recording rules.
- [ ] I can write alerting rules with `for`, labels, annotations.
- [ ] I can validate rules with promtool.
- [ ] I can unit-test alert logic.
- [ ] I completed Labs 7.1–7.4 including each negative test.
