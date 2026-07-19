# Chapter 08: Observability, Operations, and Major-Incident Lab

![Lab flow for this chapter: the observability stack scrapes every host, network device, and Kubernetes component with complete target health; the sample web workload's SLO and multi-window burn-rate alert rules are defined, and a synthetic test alert confirms the paging webhook reaches the simulated pager before the real test runs. As a negative test, a resource-exhaustion workload is injected on one Kubernetes worker; the workload's SLI drops below its SLO and the fast-burn alert fires within the fast-burn window, logging a page. A major incident is declared; cordoning and draining the affected node lets the scheduler move the workload elsewhere, and the SLI recovers to at least 99.5% within a few minutes, clearing the alert. The postmortem is reconstructed entirely from dashboards, the paging log, and captured evidence — not from memory.](../../../diagrams/volume-13-integrated-enterprise-labs/chapter-08-slo-major-incident-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: complete environment instrumentation and an SLO burn-rate alert exercised through a full major-incident cycle against an injected resource-exhaustion failure.*

## Learning Objectives

- Deploy a metrics, tracing, and alerting stack that instruments every
  layer built in this volume — hosts, network devices, the Kubernetes
  platform, and the `meridian-web` application.
- Define a Service Level Objective for `meridian-web` with an explicit
  error budget, not just a dashboard someone occasionally looks at.
- Configure burn-rate alerting that pages before the error budget is
  fully spent, not after.
- Run a full major-incident process — declaration, bridge, resolution,
  postmortem — against a real, injected failure.
- Reconstruct an accurate incident timeline from telemetry and evidence
  captured during the incident, rather than from memory afterward.

## Theory and Architecture

This chapter instruments what Chapters 02 through 07 built, following
[Volume XI](../../volume-11-observability-enterprise-operations/README.md) (Observability and Enterprise Operations): [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) (Telemetry
Architecture, Instrumentation, and Pipelines) for how metrics, logs, and
traces reach a central store, [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) (Metrics, Service-Level
Objectives, and Error Budgets) for defining and measuring the SLO this
chapter sets for `meridian-web`, [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md) (Distributed Tracing,
Profiling, and Dependency Analysis) for tracing the hybrid-scheduled
workload from [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md), [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) (Actionable Alerting, On-Call, and
Operations Centers) for the burn-rate alert and paging simulation, and
[Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) (Service Management, Incident, Problem, and Change Operations)
for the major-incident process this chapter's lab runs end to end.

The relationship between this chapter and [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) is deliberate:
[Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) built detection for security events; this chapter builds
detection for reliability events. Both feed the same underlying
discipline — a system that fails silently is worse than one that fails
loudly, whether the failure is an intrusion or a resource exhaustion
event. `siem01` from [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) continues to receive security-relevant
logs; `obs01`, introduced here, owns metrics, dashboards, tracing, and
alerting.

An SLO without an error budget is just a target nobody is accountable to;
[Volume XI, Chapter 03](../../volume-11-observability-enterprise-operations/chapters/03-metrics-service-level-objectives-and-error-budgets.md) treats the error budget as the resource this
chapter's major-incident exercise deliberately spends down, so the reader
experiences what a burn-rate alert firing under real pressure actually
feels like, not just how to configure one.

### Systems introduced in this chapter

| Hostname | Role | Address |
| --- | --- | --- |
| `obs01` | Metrics, dashboards, tracing, and alerting stack | `10.13.99.12` |

`obs01` scrapes or receives telemetry from every host, network device, and
Kubernetes component built in Chapters 02–07; no other new hosts are
required.

## Design Considerations

- **Pull-based metrics for infrastructure, push-based for short-lived
  work.** Hosts, network devices, and long-running services are scraped
  on an interval (the Prometheus model); anything with a shorter lifetime
  than the scrape interval pushes instead — a distinction [Volume XI](../../volume-11-observability-enterprise-operations/README.md),
  [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) treats as a first design decision, not an implementation
  detail.
- **The SLO is defined before the alert, and the alert is defined before
  the incident.** Sequencing matters: an alert with no SLO behind it
  measures nothing meaningful, and an incident process with no alert to
  trigger it depends entirely on someone noticing by accident.
- **Multi-window, multi-burn-rate alerting, not a static threshold.** A
  single "error rate > 5%" alert either fires too late for a fast, severe
  burn or too often for normal noise. This chapter configures a fast
  (1-hour) and slow (6-hour) burn-rate window, the pattern [Volume XI](../../volume-11-observability-enterprise-operations/README.md),
  [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) recommends, so the alert is sensitive to both a sudden severe
  outage and a slow, sustained degradation.
- **Paging is simulated, not connected to a real phone.** The lab's
  on-call simulation posts to a local webhook that logs a page with a
  timestamp, rather than an actual paging service — the incident process
  this chapter teaches applies identically whether the page reaches a
  phone or a log file, and a lab has no business generating a real 2 a.m.
  alert.
- **The postmortem is blameless and evidence-driven.** The timeline in
  this chapter's postmortem is reconstructed entirely from `obs01`
  dashboards, `siem01` logs, and `evidence.sh` captures — not from
  participants' recollection — which is both a better record and the
  standard [Volume XI, Chapter 07](../../volume-11-observability-enterprise-operations/chapters/07-service-management-incident-problem-and-change-operations.md) expects of a real postmortem.

## Implementation and Automation

Instrument `meridian-web` with a metrics endpoint and deploy the
Kubernetes-native exporters needed to observe the platform underneath it:

```yaml
# ServiceMonitor-equivalent scrape config on obs01
scrape_configs:
  - job_name: meridian-web
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: meridian-web
        action: keep
  - job_name: node-exporter
    static_configs:
      - targets:
          - dc01:9100
          - dc02:9100
          - ctrl01:9100
          - k8s-cp01:9100
          - k8s-wk01:9100
          - k8s-wk02:9100
  - job_name: network-devices
    static_configs:
      - targets: [sw-core01:9116, sw-core02:9116, rtr-hq01:9116]
```

Define the `meridian-web` SLO and its error budget:

```yaml
# obs01 SLO definition
slo: meridian-web-availability
objective: 99.5
window: 30d
sli: >
  sum(rate(http_requests_total{app="meridian-web",code!~"5.."}[5m]))
  /
  sum(rate(http_requests_total{app="meridian-web"}[5m]))
```

Configure multi-window, multi-burn-rate alerting against that SLO:

```yaml
groups:
  - name: meridian-web-slo-burn
    rules:
      - alert: MeridianWebFastBurn
        expr: >
          (1 - slo:meridian-web-availability:ratio_rate1h) > (14.4 * 0.005)
          and
          (1 - slo:meridian-web-availability:ratio_rate5m) > (14.4 * 0.005)
        for: 2m
        labels: {severity: page}
      - alert: MeridianWebSlowBurn
        expr: >
          (1 - slo:meridian-web-availability:ratio_rate6h) > (6 * 0.005)
          and
          (1 - slo:meridian-web-availability:ratio_rate30m) > (6 * 0.005)
        for: 15m
        labels: {severity: ticket}
```

Wire the paging simulation:

```bash
#!/usr/bin/env bash
# on-call-webhook.sh — logs a simulated page with timestamp
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) PAGE severity=$1 alert=$2" \
  >> /var/log/oncall-pages.log
```

## Validation and Troubleshooting

- **Telemetry completeness.** Before trusting any dashboard, confirm
  `obs01`'s target list shows every host and device as `up`:

  ```bash
  curl -s http://obs01:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health!="up")'
  ```

  This should return nothing; any unhealthy target is a blind spot the
  major-incident exercise would otherwise mask as "nothing happened
  there."
- **SLO math sanity check.** Manually compute the 30-day availability
  from raw request counts at least once and compare it to the dashboard's
  reported value — a transposed numerator/denominator in the SLI query is
  a common and easy-to-miss error that silently inverts the entire metric.
- **Common failure: alert fires on deploy, not on degradation.** If the
  fast-burn alert fires every time `meridian-web` is redeployed, the
  `for:` duration is too short relative to normal rolling-update
  disruption; lengthen it slightly rather than disabling the alert.
- **Common failure: burn-rate windows too close together.** If both the
  fast- and slow-burn alerts fire simultaneously for every incident, the
  windows are not actually differentiating severity — revisit the
  multiplier constants against [Volume XI, Chapter 03](../../volume-11-observability-enterprise-operations/chapters/03-metrics-service-level-objectives-and-error-budgets.md)'s guidance before
  the on-call rotation starts treating every page as equally urgent.
- **Postmortem timeline gaps.** If the reconstructed timeline in this
  chapter's lab has a gap longer than the scrape/log interval, check
  whether `obs01` or `siem01` had a retention or ingestion problem during
  that window rather than assuming nothing happened.

## Security and Best Practices

- Restrict `obs01`'s dashboards and raw metrics API to authenticated
  users from `corp.meridian.example`; infrastructure metrics reveal
  topology and capacity information useful to an attacker.
- Avoid embedding secrets or personally identifiable data in metric
  labels — labels are typically retained far longer and are far more
  widely queryable than the log line they might have come from.
- Set an explicit retention policy on `obs01` and `siem01` and document
  it; unbounded retention is both a cost problem and a data-minimization
  problem.
- Treat the on-call escalation path itself as a tested control: the
  paging simulation in this chapter's lab should be validated with a
  known-good alert before it is trusted during the negative test, the
  same "test the safety net before you need it" principle [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)
  applied to snapshot/rollback.
- Feed alerting and major-incident metadata (declared, resolved,
  postmortem completed) into the same evidence trail used elsewhere in
  this volume, so [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md)'s capstone can reference operational history
  alongside infrastructure state.

## References and Knowledge Checks

**References**

- [Volume XI](../../volume-11-observability-enterprise-operations/README.md), Chapters 02–03, 05–07 — telemetry architecture, metrics/SLOs,
  distributed tracing, alerting/on-call, and incident/problem/change
  operations.
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — *Alerting on SLOs* (multi-window, multi-burn-rate
  alerting).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — platform
  baseline for the Kubernetes and host components instrumented in this
  chapter.

**Knowledge checks**

1. Why does a single static error-rate threshold perform worse than a
   multi-window, multi-burn-rate alert for both a sudden outage and a
   slow degradation?
2. What does defining the SLO before the alert prevent, compared to
   defining the alert first?
3. Why is a postmortem timeline reconstructed from telemetry considered
   more reliable than one reconstructed from participant recollection?
4. What blind spot would an unhealthy (not `up`) Prometheus target create
   during this chapter's major-incident exercise?

## Hands-On Lab

**Objective:** Instrument the full environment with metrics and tracing,
define and alert on a real SLO for `meridian-web`, then run a complete
major-incident cycle against an injected resource-exhaustion failure.

**Prerequisites**

- [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) complete, with `siem01` and the zero-trust segmentation
  model in place.
- The Kubernetes cluster and `meridian-web` deployment from [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md)
  healthy and reachable.
- Familiarity with PromQL-style query syntax is helpful but not required;
  the queries in this chapter are provided in full.

**Steps**

1. Restore or confirm the `ch07-baseline` state.

2. Deploy `obs01` and configure the scrape targets from Implementation and
   Automation, covering every host, network device, and Kubernetes
   component built so far.

3. **Expected result — telemetry completeness.**

   ```bash
   ./evidence.sh "curl -s http://obs01:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health!=\"up\")'"
   ```

   Must return an empty result.

4. Instrument `meridian-web` with a `/metrics` endpoint and redeploy it.

5. Define the `meridian-web-availability` SLO and the multi-window
   burn-rate alert rules from Implementation and Automation.

6. Deploy the on-call paging simulation webhook and connect it to the
   `severity: page` alert route.

7. **Expected result — alert path validated.** Trigger a synthetic test
   alert (not the real SLO condition) and confirm it reaches the
   simulated pager:

   ```bash
   ./evidence.sh "curl -X POST obs01:9093/api/v1/alerts -d '[{\"labels\":{\"alertname\":\"TestPage\",\"severity\":\"page\"}}]'"
   ./evidence.sh "tail -n 5 /var/log/oncall-pages.log"
   ```

   The test page must appear in the log before proceeding — do not rely
   on an unvalidated alert path during the negative test.

8. Take a snapshot/export of `obs01`'s dashboards, SLO definitions, and
   alert rules, labeled `ch08-baseline`.

9. **Negative test:** Inject a resource-exhaustion failure on `k8s-wk01`
   to drive `meridian-web` below its SLO:

   ```bash
   ./evidence.sh "kubectl debug node/k8s-wk01 -it --image=busybox -- \
     sh -c 'stress-ng --cpu 4 --vm 2 --vm-bytes 90% --timeout 600s'"
   ```

   **Expected result — burn-rate alert fires.** Within the fast-burn
   window, `MeridianWebFastBurn` fires and a page is logged:

   ```bash
   ./evidence.sh "tail -n 5 /var/log/oncall-pages.log"
   ```

10. **Declare and run the major incident.** Following [Volume XI](../../volume-11-observability-enterprise-operations/README.md), Chapter
    07's process, declare a major incident, open a bridge (a shared
    document or channel is sufficient for the lab), and assign an
    incident commander. Record the declaration timestamp with
    `evidence.sh`.

11. **Resolve:** Cordon and drain the affected node so the scheduler moves
    `meridian-web` pods elsewhere:

    ```bash
    ./evidence.sh "kubectl cordon k8s-wk01 && kubectl drain k8s-wk01 --ignore-daemonsets --delete-emptydir-data"
    ```

    **Expected result:** `meridian-web`'s SLI recovers above the 99.5%
    objective within a few minutes, and the burn-rate alert clears.

12. **Recovery verification.**

    ```bash
    ./evidence.sh "curl -s 'http://obs01:9090/api/v1/query?query=slo:meridian-web-availability:ratio_rate5m'"
    ```

    Must show a value at or above `0.995` before the incident is closed.

13. Uncordon `k8s-wk01` once the stress workload has been removed and
    confirm it returns to `Ready` and schedulable.

14. **Postmortem:** Reconstruct the incident timeline entirely from
    `obs01` dashboards, the paging log, and `evidence.sh` output — not
    from memory — and record: detection time, declaration time,
    resolution time, and root cause. This is the deliverable for this
    exercise.

15. **Cleanup:** Confirm no residual stress workload remains on any node,
    and retain `obs01` and the SLO/alert configuration for [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md).
    Commit the final state:

    ```bash
    cd ~/vol13-lab
    git add topology.yml
    git commit -m "Chapter 08: observability, operations, and major-incident lab"
    ```

## Summary and Completion Checklist

This chapter instrumented every system built across the volume, defined a
real SLO with a multi-window burn-rate alert instead of a static
threshold, and ran a complete major-incident cycle — including a validated
paging path, a documented bridge and resolution, and a telemetry-driven
postmortem — against a real injected failure rather than a tabletop
exercise.

- [ ] Deployed `obs01` with complete telemetry coverage across hosts,
      network devices, and the Kubernetes platform.
- [ ] Defined the `meridian-web` SLO and multi-window burn-rate alerting.
- [ ] Validated the on-call paging path before relying on it.
- [ ] Declared, ran, and resolved a major incident against an injected
      resource-exhaustion failure.
- [ ] Produced a telemetry-reconstructed postmortem timeline.
