# Chapter 08: Capacity, Performance, and Cost-Aware Operations

## Learning Objectives

- Forecast capacity demand from historical utilization trends and
  distinguish organic growth from event-driven spikes.
- Design and interpret a load test that produces an actionable
  saturation point rather than a vague "it seemed fine" result.
- Configure Kubernetes autoscaling (HPA and KEDA) driven by the same
  telemetry signals established earlier in this volume, and explain the
  trade-offs between reactive and predictive scaling.
- Apply FinOps principles — showback, chargeback, and unit economics —
  to make infrastructure cost a visible, owned engineering signal rather
  than a finance-only concern.
- Right-size compute and storage allocations using utilization data
  instead of static, one-time-guessed requests and limits.
- Diagnose common capacity failures: noisy-neighbor contention,
  autoscaler thrashing, and cost blind spots in the observability
  pipeline itself.

## Theory and Architecture

### Capacity planning as a forecasting discipline

Capacity planning answers "will we have enough" before the answer
becomes "we did not," using historical utilization data (the same
metrics pipeline from [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md), now queried for trend rather than
alerting) projected forward against expected demand. Three demand
patterns require different forecasting approaches:

- **Organic growth** — steady, roughly predictable increase tied to
  user or transaction growth, forecast well with simple trend
  extrapolation (linear or log-linear regression over 90-180 days of
  history) reviewed monthly or quarterly.
- **Seasonal and cyclical demand** — recurring peaks tied to a known
  calendar (end-of-quarter batch processing, retail peak season, a
  recurring marketing event), forecast by comparing the current trend
  against the same period in prior cycles rather than against recent
  weeks alone, which would understate an approaching seasonal peak.
- **Event-driven spikes** — a product launch, a marketing campaign, a
  migration cutover — not visible in historical trend at all and
  requiring an explicit capacity request from the team that knows the
  event is coming, fed into planning as a manual input rather than
  expected to be inferred from telemetry.

A capacity forecast is only useful if it is compared against actual
provisioned headroom and reviewed on a fixed cadence; a forecast
produced once and never revisited ages into irrelevance within one
growth cycle, and a review cadence tied to the same cadence as SLO and
error-budget review ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)) keeps reliability and capacity planning
from drifting apart despite being causally connected — capacity
exhaustion is a common and entirely preventable root cause of an SLO
burn event.

### Load testing for a real saturation point

A load test's purpose is to find the point at which a system's behavior
degrades non-linearly — the **saturation point** — not merely to confirm
it survives an arbitrary target load. Three load test types serve
different purposes:

- **Load test** — sustained traffic at an expected or slightly elevated
  volume, confirming the system meets its SLOs under realistic
  conditions.
- **Stress test** — traffic increased steadily past expected volume
  until the system degrades, identifying the actual saturation point and
  the failure mode at that point (does latency degrade gracefully, or
  does the system fall over abruptly with cascading failure).
- **Soak test** — sustained moderate load over an extended duration
  (hours, not minutes), surfacing failure modes that only appear over
  time: a memory leak, gradual connection pool exhaustion, log or
  temp-file disk fill.

A load test is only as good as its traffic model. Synthetic load that
does not reflect the real request mix (read/write ratio, payload size
distribution, cache hit rate) produces a saturation point that does not
correspond to the real one, which is a common way a load test passes
cleanly and the system still falls over in production under actual
traffic. Build the traffic model from real production request
distributions (sampled from trace or access-log data, Chapters 04-05)
rather than from an engineer's assumption of what traffic "probably"
looks like.

```text
Throughput vs. latency under increasing load:

latency
  |                                    x  <- saturation point:
  |                                x       latency begins increasing
  |                            x           faster than linearly
  |                        x
  |                x   x
  |    x   x   x
  +---------------------------------------------  throughput
       (linear region)      (degradation region)
```

### Autoscaling: reactive and predictive

Kubernetes' **Horizontal Pod Autoscaler (HPA)** scales replica count
reactively, based on a metric crossing a threshold, most commonly CPU or
memory utilization but, critically, extensible to any custom or external
metric via the Kubernetes custom metrics API:

```yaml
# hpa-checkout-api.yaml — scale on p99 latency headroom via a custom metric
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: checkout-api
  namespace: prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout-api
  minReplicas: 6
  maxReplicas: 60
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
  metrics:
    - type: Pods
      pods:
        metric:
          name: http_requests_in_flight_per_pod
        target:
          type: AverageValue
          averageValue: "40"
```

Scaling on request-in-flight or queue-depth signals, sourced directly
from the same OTel-instrumented metrics pipeline built in [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md),
typically produces more accurate scaling decisions than CPU utilization
alone, because CPU utilization can lag or diverge from actual request
saturation for I/O-bound services. **KEDA** (Kubernetes Event-driven
Autoscaling) extends this model to scale on external event sources — a
message queue's backlog depth, a stream-processing consumer's lag — and
critically, can scale a deployment to zero when idle, a capability the
native HPA lacks, valuable for genuinely bursty or infrequent workloads
where paying for a warm minimum replica count around the clock is
unjustified cost.

The `scaleUp`/`scaleDown` **behavior** stabilization windows in the
example above exist specifically to prevent **autoscaler thrashing** —
rapid scale-up-then-down cycling in response to noisy, short-lived
metric fluctuation, which wastes both compute (repeated cold starts) and
reliability margin (a scale-down that removes capacity moments before it
was needed again). Asymmetric windows (scale up fast, scale down slow)
are the standard defensive default: the cost of scaling up one replica
too many briefly is low; the cost of scaling down and then needing that
capacity back within the next minute is a real latency or error impact.

**Predictive scaling** — pre-provisioning ahead of an anticipated demand
pattern (a known daily peak, a scheduled batch window) using a
forecasting model rather than waiting for a reactive metric to cross
threshold — closes the gap reactive scaling cannot: the time between a
metric crossing threshold and new capacity actually becoming ready
(image pull, container start, application warm-up) during which the
system is under-provisioned regardless of how fast the autoscaler
reacts. A common hybrid: predictive/scheduled scaling establishes a
baseline replica floor ahead of a known peak, and reactive HPA/KEDA
scaling handles the unpredictable portion above that floor.

### FinOps: cost as an engineering signal

**FinOps** (a portmanteau of Finance and DevOps) is the discipline that
makes cloud and infrastructure cost a shared, continuously managed
engineering responsibility rather than a monthly finance surprise. Three
mechanisms make cost visible and actionable at the team level:

- **Showback** — reporting cost attribution per team or service without
  an actual billing transfer, making cost visible as a decision input
  without the organizational friction of true internal billing.
- **Chargeback** — showback plus an actual internal financial transfer,
  typically adopted only once cost attribution accuracy and
  organizational maturity support it, since inaccurate chargeback
  produces disputes that undermine trust in the entire cost model faster
  than no chargeback at all.
- **Unit economics** — cost normalized against a business-meaningful
  unit (cost per 1,000 requests, cost per active user, cost per
  transaction) rather than raw spend, since raw spend naturally grows
  with a healthy, growing business and is a poor efficiency signal on
  its own; unit cost trending upward while volume grows is the
  actionable signal, not total spend trending upward.

Cost attribution depends on the same resource-tagging and service-
ownership discipline established for the catalog in [Chapter 01](01-observability-operating-model-and-service-ownership.md) — a cloud
resource or Kubernetes namespace without an owner tag is invisible to
showback the same way an unowned service is invisible to on-call, and
both gaps share the same root cause: metadata discipline not enforced at
creation time.

### The observability platform's own cost surface

Telemetry volume (Chapters 02 and 04) is itself a capacity and cost
problem the platform team must manage using the same discipline applied
to any other infrastructure resource: track ingestion volume per
service against budget, forecast its growth alongside request volume
growth, and treat an unbounded log or metric cardinality increase
(Chapters 02 and 04) as a capacity incident in its own right, since it
can degrade the shared observability platform for every team, not only
the team that caused it.

## Design Considerations

- **Forecast horizon versus provisioning lead time.** Match the
  forecast horizon to the actual lead time required to add capacity — a
  cloud environment with near-instant elasticity needs only a short
  forecast horizon; an on-premises environment with a hardware
  procurement lead time of months needs a forecast horizon long enough
  to trigger a purchase order before the shortfall arrives, which is a
  materially different planning cadence than most cloud-native teams
  default to.
- **Autoscaling metric choice.** Choose the metric that most directly
  represents the resource actually constraining the service (in-flight
  requests or queue depth for most I/O-bound services, CPU for
  genuinely compute-bound workloads) rather than defaulting to CPU
  utilization out of habit; a CPU-driven HPA for an I/O-bound service
  under-scales during I/O-bound saturation and over-scales during
  CPU-heavy but low-traffic background work.
- **Scale-to-zero trade-off.** KEDA's scale-to-zero eliminates idle cost
  but reintroduces cold-start latency on the next request, which may
  violate a latency SLO ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)) for a user-facing service even if
  it is entirely appropriate for an internal batch or async workload.
  Reserve scale-to-zero for workloads whose SLO, if any, tolerates
  cold-start latency.
- **Showback granularity versus attribution accuracy.** Finer cost
  attribution (per-feature, per-customer) is more actionable but harder
  to attribute accurately, especially for shared infrastructure
  (a shared database cluster, a shared observability pipeline). Start
  showback at the service or team level, where attribution is
  reasonably direct, before attempting finer-grained attribution that
  may require cost-allocation modeling effort disproportionate to its
  decision value.
- **Right-sizing cadence versus workload volatility.** A workload with
  stable, predictable utilization can be right-sized (Kubernetes
  requests/limits, VM sizing) on a slow quarterly cadence; a workload
  with volatile or evolving utilization needs more frequent review or,
  better, an automated recommender (Kubernetes VPA in recommendation-
  only mode, or a cloud provider's native right-sizing tool) rather than
  a manual review cadence that cannot keep pace.
- **Noisy-neighbor isolation versus utilization efficiency.** Higher
  workload density (more services sharing a node or cluster) improves
  utilization efficiency and lowers cost per unit of work, but increases
  noisy-neighbor risk — one workload's resource spike degrading another
  co-located workload's performance. Resource requests/limits and
  Kubernetes QoS classes (Guaranteed, Burstable, BestEffort) are the
  primary technical control; decide the acceptable isolation-versus-
  efficiency trade-off explicitly per service tier rather than applying
  one density policy uniformly across Tier 0 and Tier 3 workloads alike.

## Implementation and Automation

A capacity forecast implemented as a scheduled query against the
existing metrics backend, projecting current utilization trend forward
against a defined ceiling and reporting time-to-exhaustion — turning
capacity planning into a continuously running check rather than an
occasional manual spreadsheet exercise:

```python
# forecast-capacity.py — run on a schedule (e.g., weekly) per resource
import requests
from datetime import datetime, timedelta
import numpy as np

PROMETHEUS_URL = "http://prometheus.observability.svc:9090"
QUERY = 'avg(node_memory_MemUsed_bytes) by (cluster) / avg(node_memory_MemTotal_bytes) by (cluster)'
LOOKBACK_DAYS = 90
CEILING = 0.80  # alert if projected to cross 80% utilization

def fetch_series():
    end = datetime.utcnow()
    start = end - timedelta(days=LOOKBACK_DAYS)
    resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params={
        "query": QUERY, "start": start.timestamp(), "end": end.timestamp(),
        "step": "1d",
    })
    result = resp.json()["data"]["result"][0]["values"]
    return np.array([float(v[0]) for v in result]), np.array([float(v[1]) for v in result])

def forecast_days_to_ceiling(timestamps, values):
    slope, intercept = np.polyfit(timestamps, values, 1)
    if slope <= 0:
        return None  # flat or declining trend; no exhaustion projected
    days_to_ceiling = (CEILING - intercept) / slope / 86400
    return max(0, days_to_ceiling - (datetime.utcnow().timestamp() - timestamps[0]) / 86400)

if __name__ == "__main__":
    ts, vals = fetch_series()
    days = forecast_days_to_ceiling(ts, vals)
    if days is not None and days < 60:
        print(f"CAPACITY ALERT: cluster projected to reach {CEILING:.0%} "
              f"memory utilization in {days:.0f} days at current growth rate")
    else:
        print("Capacity forecast within acceptable horizon.")
```

A cost-attribution query against Kubernetes resource-usage metrics,
labeled by the same ownership metadata used in the service catalog
([Chapter 01](01-observability-operating-model-and-service-ownership.md)), producing a showback figure without requiring a dedicated
FinOps platform for a first iteration:

```promql
# Approximate monthly compute cost per team, using a per-core-hour rate
# and label-joined ownership metadata exposed via kube-state-metrics
sum(
  avg_over_time(kube_pod_container_resource_requests{resource="cpu"}[30d])
  * on(namespace) group_left(team)
  kube_namespace_labels{label_team!=""}
) by (label_team) * 24 * 30 * 0.034  # illustrative $/core-hour rate
```

Enforce request/limit right-sizing as a pre-merge CI check comparing
declared resource requests against observed utilization, flagging
significant over-provisioning before it reaches production and
accumulates as wasted cost:

```bash
#!/usr/bin/env bash
# check-right-sizing.sh — compare declared CPU request to p95 observed usage
set -euo pipefail

DEPLOYMENT="$1"
NAMESPACE="$2"

requested=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.spec.template.spec.containers[0].resources.requests.cpu}')

# p95 CPU usage over the last 14 days, from the metrics backend
observed=$(curl -s -G "http://prometheus.observability.svc:9090/api/v1/query" \
  --data-urlencode "query=quantile_over_time(0.95, rate(container_cpu_usage_seconds_total{pod=~\"${DEPLOYMENT}-.*\",namespace=\"${NAMESPACE}\"}[5m])[14d:5m])" \
  | jq -r '.data.result[0].value[1]')

echo "Requested: ${requested}, Observed p95: ${observed} cores"

# Flag if requested is more than 3x observed p95 (significant over-provisioning)
python3 -c "
import sys
requested = '${requested}'.rstrip('m')
requested_cores = float(requested) / 1000 if 'm' in '${requested}' else float(requested)
observed = float('${observed}' or 0)
if observed > 0 and requested_cores > observed * 3:
    print(f'OVER-PROVISIONED: requested {requested_cores} cores vs p95 observed {observed:.3f} cores')
    sys.exit(1)
print('Right-sizing check passed.')
"
```

## Validation and Troubleshooting

- **Validate a load test's traffic model before trusting its result.**
  Compare the load test's request-type and payload-size distribution
  against a recent sample of real production traffic (from trace or
  access-log data); a load test whose traffic model diverges
  significantly from production traffic produces a saturation point
  that does not transfer to the real system.
  Re-baseline the traffic model quarterly or after a significant
  product change.
- **Symptom: autoscaler thrashing (rapid scale up/down cycling).**
  Check the HPA's `behavior` stabilization windows and the underlying
  metric's noise characteristics — a metric with high scrape-to-scrape
  variance and a short stabilization window is the most common cause.
  Widen the stabilization window or switch to a metric with less
  natural volatility (an averaged or smoothed signal) before assuming
  thrashing requires a more complex fix.
- **Symptom: HPA does not scale despite sustained high load.** Confirm
  the custom metrics API is actually returning fresh data for the
  target metric (`kubectl get --raw
  "/apis/custom.metrics.k8s.io/v1beta1/..."` against the specific
  metric) — a stale or absent custom metric is the most common root
  cause and fails silently, with the HPA simply not acting rather than
  erroring visibly.
- **Symptom: cost showback figures do not reconcile with the actual
  cloud bill.** Confirm every billed resource has the ownership label
  the showback query depends on (`kube_namespace_labels{label_team!=""}`
  in the example above); unlabeled resources are invisible to the
  showback query and their cost accumulates as unattributed spend,
  understating every team's true figure proportionally.
- **Symptom: right-sizing recommendation conflicts with a known burst
  pattern.** A service with legitimate, infrequent but severe bursts
  (an end-of-month batch trigger, for example) can appear over-
  provisioned by a naive p95-over-14-days check that does not weight the
  burst period appropriately. Extend the observation window to include
  at least one full burst cycle, or explicitly annotate the service to
  exclude it from the automated right-sizing check with a documented
  reason.

## Security and Best Practices

- Restrict who can modify autoscaler `maxReplicas` and scale-to-zero
  configuration in production; an unauthorized reduction in `maxReplicas`
  is a subtle, delayed-effect way to cap a service's genuine capacity and
  can manifest later as an availability incident that is hard to
  attribute back to a configuration change made well before symptoms
  appeared.
- Apply resource quotas at the namespace level as a backstop against a
  runaway autoscaler or a misconfigured KEDA scaler consuming
  disproportionate shared-cluster capacity, protecting other tenants'
  availability from one team's capacity or cost incident.
- Treat cost and capacity data with the same ownership-boundary access
  control as the service catalog ([Chapter 01](01-observability-operating-model-and-service-ownership.md)) — cost attribution data
  reveals which services and teams are growing or shrinking, which is
  organizationally sensitive information in some contexts, and access
  should be scoped accordingly rather than broadly open by default.
- Do not let observability pipeline cost optimization (Chapters 02 and
  04's sampling and retention controls) silently erode the telemetry
  fidelity a Tier 0 service's incident response actually depends on;
  review cost-driven telemetry reductions against the same tiering
  framework used for everything else in this volume, not as a
  cost-only decision made in isolation from reliability impact.
- Validate load-testing traffic against production authentication and
  authorization paths using dedicated, clearly identified test
  credentials and accounts, never real customer credentials or
  production payment processing endpoints, to avoid an inadvertent real
  financial transaction or data exposure during a stress test.

## References and Knowledge Checks

**References**

- [Google, *Site Reliability Engineering*, Chapter 17 ("Testing for
  Reliability") and Chapter 21 ("Managing Load"), free online edition.](https://sre.google/sre-book/table-of-contents/)
- [Kubernetes documentation, `kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/`,
  for HPA behavior configuration.](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [KEDA documentation, `keda.sh/docs/`, for event-driven and scale-to-
  zero scaling patterns.](https://keda.sh/docs/)
- [FinOps Foundation, *FinOps Framework*, `finops.org`, for showback,
  chargeback, and unit economics definitions used in this chapter.](https://www.finops.org/framework/)

**Knowledge Checks**

1. Explain why a load test's saturation point is unreliable if the
   test's traffic model diverges significantly from real production
   traffic.
2. Why do HPA `behavior` stabilization windows typically use an
   asymmetric configuration (fast scale-up, slow scale-down)?
3. Distinguish showback from chargeback, and explain why an organization
   might deliberately adopt the former without the latter.
4. Why is unit cost (cost per 1,000 requests, for example) a more
   actionable FinOps signal than total spend alone for a growing
   service?
5. Describe a scenario in which reducing observability telemetry volume
   for cost reasons directly increases the risk of a delayed incident
   response, and how service tiering should factor into that decision.

## Hands-On Lab

**Objective:** Run a local load test against a sample service using a
realistic traffic model, identify its saturation point from latency
degradation, and validate a right-sizing check against observed p95
resource usage, including a negative test for a mismatched traffic
model.

### Prerequisites

- Docker Engine and Docker Compose v2.
- Python 3.11+ with `pip` available locally (for the load generator).
- `curl` and a POSIX shell.

### Procedure

1. Create the lab directory and a sample service that becomes
   non-linearly slower as concurrency increases past a deliberate
   saturation point (simulating a bounded worker pool):

   ```bash
   mkdir -p ~/capacity-lab && cd ~/capacity-lab
   cat > app.py <<'EOF'
   import threading
   import time
   from http.server import BaseHTTPRequestHandler, HTTPServer

   MAX_WORKERS = 8
   semaphore = threading.Semaphore(MAX_WORKERS)
   in_flight = 0
   lock = threading.Lock()

   class Handler(BaseHTTPRequestHandler):
       def do_GET(self):
           global in_flight
           acquired = semaphore.acquire(timeout=2)
           with lock:
               in_flight += 1
           start = time.time()
           if acquired:
               time.sleep(0.05)  # base work
           else:
               time.sleep(0.05 * 6)  # queued/degraded path
           duration = time.time() - start
           with lock:
               in_flight -= 1
           if acquired:
               semaphore.release()
           self.send_response(200)
           self.send_header("X-Duration-Ms", str(int(duration * 1000)))
           self.end_headers()
           self.wfile.write(b"ok")

       def log_message(self, fmt, *args):
           return

   HTTPServer(("0.0.0.0", 8091), Handler).serve_forever()
   EOF
   python3 app.py &
   echo $! > app.pid
   sleep 1
   ```

2. Create a load generator that ramps concurrency in stages and records
   average latency per stage, producing the throughput-versus-latency
   curve described in the Theory section:

   ```bash
   cat > loadtest.py <<'EOF'
   import concurrent.futures
   import statistics
   import time
   import urllib.request

   def one_request():
       start = time.time()
       urllib.request.urlopen("http://localhost:8091/").read()
       return time.time() - start

   for concurrency in [2, 4, 8, 12, 16, 24]:
       latencies = []
       with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
           futures = [ex.submit(one_request) for _ in range(concurrency * 5)]
           for f in concurrent.futures.as_completed(futures):
               latencies.append(f.result())
       avg_ms = statistics.mean(latencies) * 1000
       print(f"concurrency={concurrency:3d}  avg_latency_ms={avg_ms:7.1f}")
   EOF
   python3 loadtest.py
   ```

### Expected Results

The output shows average latency staying close to roughly 50-70ms at
concurrency 2, 4, and 8 (within the `MAX_WORKERS=8` capacity), then
increasing sharply — to roughly 150-300ms or more — at concurrency 12,
16, and 24, as requests exceed the worker pool and fall into the
degraded path. This inflection point, between concurrency 8 and 12, is
the saturation point: confirm your output shows a clear non-linear jump
in that range rather than a smooth, gradual increase, demonstrating the
load test successfully located a real capacity boundary rather than
producing an inconclusive result.

### Negative Test

Re-run the load test with a traffic model that does not reflect the
service's actual bottleneck — extremely low concurrency that never
approaches the worker pool limit — and confirm it fails to reveal any
saturation point at all, demonstrating why a load test's traffic model
must actually exercise the resource under evaluation:

```bash
cat > loadtest-shallow.py <<'EOF'
import concurrent.futures, statistics, time, urllib.request

def one_request():
    start = time.time()
    urllib.request.urlopen("http://localhost:8091/").read()
    return time.time() - start

for concurrency in [1, 2, 3]:
    latencies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(one_request) for _ in range(concurrency * 5)]
        for f in concurrent.futures.as_completed(futures):
            latencies.append(f.result())
    avg_ms = statistics.mean(latencies) * 1000
    print(f"concurrency={concurrency:3d}  avg_latency_ms={avg_ms:7.1f}")
EOF
python3 loadtest-shallow.py
```

Confirm the output shows flat, roughly 50-70ms latency across all three
concurrency levels with no degradation — correctly demonstrating that
this shallow test never reached the service's real saturation point
(concurrency 8-12) and would produce a false-confidence "the service
handles load fine" conclusion if it were the only test run, which is
precisely the traffic-model risk described in the Validation and
Troubleshooting section.

### Cleanup

```bash
cd ~/capacity-lab
kill "$(cat app.pid)" 2>/dev/null || true
cd ~
rm -rf ~/capacity-lab
```

## Summary and Completion Checklist

Capacity planning forecasts organic, seasonal, and event-driven demand
against real utilization trend; load testing must use a realistic
traffic model to find a saturation point that actually transfers to
production. Reactive autoscaling (HPA, KEDA) driven by the right metric,
paired with predictive pre-provisioning ahead of known peaks, keeps
capacity matched to demand without manual intervention on every cycle.
FinOps practices — showback, chargeback, and unit economics — make cost
a visible, owned engineering signal rather than a monthly finance
surprise, and the observability pipeline's own telemetry volume is
itself part of that cost surface. [Chapter 09](09-operational-automation-analytics-and-continual-improvement.md) closes the volume by
turning all of this operational data — incidents, alerts, capacity
trends, cost — into a continual improvement loop through automation and
analytics.

**Completion checklist**

- [ ] Can distinguish organic, seasonal, and event-driven capacity
      demand and the forecasting approach appropriate to each.
- [ ] Can design a load test with a realistic traffic model that locates
      a genuine saturation point.
- [ ] Can configure Kubernetes autoscaling on a request-based metric and
      explain asymmetric stabilization windows.
- [ ] Can explain showback, chargeback, and unit economics and when each
      is appropriate.
- [ ] Ran a local load test, identified a saturation point from latency
      degradation, and validated a right-sizing check with a negative
      test demonstrating a flawed traffic model's blind spot.
