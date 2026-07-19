# Chapter 03: Metrics, Service-Level Objectives, and Error Budgets

## Learning Objectives

- Differentiate the four Prometheus metric types (counter, gauge,
  histogram, summary) and select the correct type for a given signal.
- Write PromQL queries that compute rate, percentile latency, and
  availability ratios from raw metric data.
- Define a Service Level Indicator (SLI) as a ratio of good events to
  valid events and translate a business reliability goal into a Service
  Level Objective (SLO).
- Calculate an error budget from an SLO and a measurement window, and
  explain what spending the budget means operationally.
- Design multi-window, multi-burn-rate alerting that pages on budget
  exhaustion trajectory rather than on a single threshold breach.
- Diagnose common SLO-measurement failures: bucket boundary mismatch,
  bad-request pollution of the SLI, and window-alignment errors.

## Theory and Architecture

### The metrics data model

A metric is a numeric measurement recorded with a name, a timestamp, and a
set of key-value labels that identify its source and dimensions
(`service.name`, `http.route`, `deployment.environment.name`, per the
semantic conventions established in [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)). Prometheus, the de facto
enterprise standard for metrics storage and query, defines four metric
types, and choosing the wrong one is the most common mistake made by teams
new to metrics instrumentation:

- **Counter** — a value that only increases (or resets to zero on process
  restart): total requests served, total errors, total bytes sent. A
  counter is never queried directly for its raw value; it is always
  wrapped in `rate()` or `increase()` to produce a meaningful
  per-second or per-interval figure.
- **Gauge** — a value that can go up or down: current queue depth,
  in-flight requests, memory used, temperature. Gauges are read directly
  or aggregated with `avg()`, `max()`, or `min()`.
- **Histogram** — a distribution of observed values (typically latency or
  size) bucketed into configurable boundaries, exposed as a set of
  cumulative counters (`_bucket{le="0.1"}`, `_bucket{le="0.5"}`, and so
  on) plus `_sum` and `_count`. Histograms support server-side percentile
  calculation via `histogram_quantile()` and, critically, can be
  aggregated across instances — you can sum buckets from a thousand pods
  and compute one fleet-wide p99.
- **Summary** — similar to a histogram but calculates configured
  quantiles (for example, p50, p99) client-side, in-process, before
  export. Summaries cannot be aggregated across instances (you cannot
  average two pre-computed p99 values into a meaningful fleet p99), which
  makes them a poor default for any service running more than one
  replica. Prefer histograms unless a summary's specific quantile
  guarantees are required and cross-instance aggregation is genuinely not
  needed.

The OpenTelemetry Metrics SDK maps onto this model with Counter,
UpDownCounter (gauge-equivalent), and Histogram instruments, exported over
OTLP and typically converted to Prometheus's exposition format at the
Collector's `prometheus` exporter ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)) or scraped natively by
Prometheus 3.x's OTLP receiver.

### PromQL fundamentals

PromQL (Prometheus Query Language) is a functional query language over
time series. The instructions that follow assume familiarity with its
core operators, illustrated against a request counter:

```promql
# Raw counter value at each scrape (rarely useful directly)
http_server_request_duration_seconds_count{service="checkout-api"}

# Per-second request rate, averaged over a 5-minute sliding window
rate(http_server_request_duration_seconds_count{service="checkout-api"}[5m])

# Error rate as a ratio: errors / total requests, over 5 minutes
sum(rate(http_server_request_duration_seconds_count{service="checkout-api",http_response_status_code=~"5.."}[5m]))
/
sum(rate(http_server_request_duration_seconds_count{service="checkout-api"}[5m]))

# p99 latency from histogram buckets, over 5 minutes
histogram_quantile(0.99,
  sum(rate(http_server_request_duration_seconds_bucket{service="checkout-api"}[5m])) by (le)
)
```

`rate()` requires a counter and a range vector (the `[5m]` selector); it
computes the per-second average rate of increase across the window,
correctly handling counter resets from process restarts.
`histogram_quantile()` requires the bucket data grouped `by (le)` (the
"less than or equal" bucket boundary label) — omitting `by (le)` is the
single most common PromQL authoring error and produces a query that
returns no data or nonsensical results, because the function needs the
full set of bucket boundaries preserved as the grouping dimension while
every other label is summed away.

### From SLI to SLO to error budget

A **Service Level Indicator (SLI)** is a precisely defined ratio measuring
one aspect of service behavior, expressed as good events divided by valid
events over a window:

```text
SLI = (count of good events) / (count of valid events)
```

"Valid events" matters as much as "good events." A checkout API's
availability SLI should exclude requests that were never valid attempts —
health checks, requests rejected for client-side malformed input (HTTP
`4xx` that is not the service's fault), and synthetic load-test traffic —
because including them either inflates or deflates the SLI with noise
that does not reflect real user experience. Defining "valid" precisely,
in the query itself, is most of the engineering work in a good SLI.

A **Service Level Objective (SLO)** is a target value for the SLI over a
rolling window: "99.9% of valid checkout requests succeed, measured over
a rolling 30-day window." The SLO is internal and should be stricter than
any externally published Service Level Agreement (SLA), because the SLA
typically carries a financial or contractual penalty and the organization
wants operational warning before it is breached, not simultaneous
discovery.

The **error budget** is the complement of the SLO, expressed as an
allowance rather than a target: a 99.9% availability SLO permits 0.1%
unavailability, or 43.2 minutes of full downtime-equivalent over a 30-day
window (`30 days × 24 h × 60 min × 0.001 = 43.2 minutes`). Because the
budget is denominated in bad *events*, not necessarily contiguous
downtime, a service can spend it as many small elevated-error periods
instead of one outage and the arithmetic is identical. The table below
gives common SLO targets and their 30-day budgets:

| SLO target | Allowed bad-event ratio | Error budget per 30 days |
| --- | --- | --- |
| 99.0% | 1 in 100 | 7 hours 12 minutes |
| 99.9% | 1 in 1,000 | 43 minutes 12 seconds |
| 99.95% | 1 in 2,000 | 21 minutes 36 seconds |
| 99.99% | 1 in 10,000 | 4 minutes 19 seconds |
| 99.999% | 1 in 100,000 | 25.9 seconds |

The error budget's operational value is that it converts "is reliability
good enough" from a subjective argument into an objective, pre-negotiated
resource. When the budget remains, the team is authorized to take risk:
ship features, run migrations, deploy on Fridays. When the budget is
exhausted, a pre-agreed policy — not a debate — kicks in: freeze
risky changes, and reallocate engineering effort to reliability work
until the budget recovers. This is the mechanism that resolves the
structural tension between feature velocity and reliability without
relying on organizational politics each time it arises.

### Latency SLOs and multi-dimensional SLIs

Availability is not the only SLI type. A latency SLO defines "good" as a
request completing under a threshold: "95% of requests complete in under
300ms, measured over a rolling 30-day window." This is computed directly
from histogram buckets rather than from `histogram_quantile()`, because
the SLI needs a ratio (good/valid), not a percentile value:

```promql
# Latency SLI: fraction of requests under 300ms
sum(rate(http_server_request_duration_seconds_bucket{service="checkout-api",le="0.3"}[30d]))
/
sum(rate(http_server_request_duration_seconds_count{service="checkout-api"}[30d]))
```

This query only produces a correct answer if a histogram bucket boundary
exists at exactly the SLO threshold (`le="0.3"` for a 300ms objective).
Choosing histogram bucket boundaries is therefore not a purely
operational decision made after the SLO is defined — it must be made
alongside the SLO, or the SLI cannot be computed without interpolation
error. Set bucket boundaries at your SLO thresholds first, then add
additional boundaries for general-purpose percentile visibility.

### Multi-window, multi-burn-rate alerting

Alerting directly on "SLI below SLO right now" produces two failure
modes: it pages on brief noise that will not meaningfully consume the
30-day budget, and it is too slow to catch a fast, severe outage before
significant budget is gone. The Google SRE Workbook's multi-window,
multi-burn-rate method solves both by alerting on **burn rate** — how
fast the budget is being consumed relative to the rate that would exhaust
it exactly at the SLO — evaluated over both a short and a long window
simultaneously, requiring both to agree before paging:

```text
burn rate = (1 - SLI_over_window) / (1 - SLO)
```

A burn rate of `1` means the budget is being consumed exactly fast enough
to exhaust it at the end of the SLO window (expected, sustainable). A
burn rate of `14.4` sustained for one hour would exhaust a 30-day budget
in about 2 days. The standard four-condition table (adapted from the
Google SRE Workbook for a 99.9% SLO) pairs a fast/short window with a
slow/long confirmation window per severity:

| Severity | Burn rate threshold | Short window | Long window | Budget consumed if sustained |
| --- | --- | --- | --- | --- |
| Page (critical) | 14.4 | 5 minutes | 1 hour | 2% in 1 hour |
| Page (critical) | 6 | 30 minutes | 6 hours | 5% in 6 hours |
| Ticket (warning) | 3 | 2 hours | 24 hours | 10% in 24 hours |
| Ticket (warning) | 1 | 6 hours | 72 hours | 10% in 3 days |

Requiring agreement between a short window (fast detection) and a longer
window (confirms the burn is sustained, not a single scrape blip)
suppresses page-worthy noise from a 90-second network hiccup while still
catching a genuine fast-burning outage within minutes rather than waiting
for the full long window to elapse — the short window pages immediately
once both conditions are true, since both are evaluated continuously in
parallel. [Chapter 06](06-actionable-alerting-on-call-and-operations-centers.md) builds the alerting rule and routing on top of this
math.

## Design Considerations

- **SLO count per service.** Define the smallest number of SLOs that
  actually represent user-perceived health — typically one availability
  SLO and one or two latency SLOs (often split by request class, such as
  read versus write) per service. A service with fifteen SLOs dilutes
  attention and makes error-budget policy ambiguous when some are healthy
  and others are not; consolidate or drop SLOs that do not drive a
  decision.
- **Window length trade-off.** A 30-day rolling window is the common
  default: long enough to smooth weekly traffic patterns, short enough
  that a past incident's budget consumption eventually ages out and stops
  freezing releases indefinitely. A calendar-month window is simpler to
  reason about but creates a "budget reset" cliff on the first of the
  month that a rolling window avoids. Choose rolling windows for
  burn-rate alerting and consider calendar windows only for
  executive-facing quarterly reporting.
- **SLA versus SLO margin.** Set the internal SLO stricter than any
  externally committed SLA by a deliberate margin (commonly one order of
  magnitude on the allowed-failure ratio, such as an SLO permitting a
  quarter of the SLA's allowed downtime) so the organization has
  operational lead time to react before a contractual penalty is
  triggered, not simultaneous notice.
- **Bad-request exclusion policy.** Decide, in writing, and encode in the
  SLI query, which response codes and request types are excluded as
  "invalid" (client error `4xx` that is not the service's fault, canceled
  requests, synthetic traffic) versus counted as "bad" (server error
  `5xx`, timeouts). An SLI that counts every client typo as a service
  failure understates real reliability and erodes trust in the metric.
- **Histogram bucket selection cost.** Every additional histogram bucket
  boundary is additional cardinality on export and additional storage.
  Choose the minimum bucket set that covers your SLO thresholds plus a
  handful of general diagnostic points (for example, native histograms in
  Prometheus 3.x, which use exponential bucketing and largely remove this
  trade-off, are the preferred choice for new instrumentation over
  classic fixed-bucket histograms where the backend supports them).
- **Error budget policy ownership.** Decide, before the first budget
  exhaustion, who has authority to declare a freeze, what a freeze
  actually restricts (all deploys, or only risky ones), and what
  exception process exists for a security patch that must ship regardless
  of budget state. Writing this policy after the first contentious
  exhaustion event produces a worse policy under worse conditions.

## Implementation and Automation

Define the SLO as a version-controlled, machine-readable specification
rather than only as prose in a wiki, using the OpenSLO-style shape
adopted by common SLO tooling (Sloth, Pyrra, and commercial platforms
consume a similar structure):

```yaml
# slo/checkout-api-availability.yaml
apiVersion: sloth.slok.dev/v1
kind: PrometheusServiceLevel
metadata:
  name: checkout-api-availability
  labels:
    service: checkout-api
    tier: tier-0
spec:
  service: checkout-api
  labels:
    owner: payments-platform-team
  slos:
    - name: requests-availability
      objective: 99.9
      description: 99.9% of valid checkout requests succeed over 30 days.
      sli:
        events:
          errorQuery: |
            sum(rate(http_server_request_duration_seconds_count{
              service="checkout-api",
              http_response_status_code=~"5.."
            }[{{.window}}]))
          totalQuery: |
            sum(rate(http_server_request_duration_seconds_count{
              service="checkout-api",
              http_response_status_code!~"429"
            }[{{.window}}]))
      alerting:
        name: CheckoutAPIAvailabilitySLO
        pageAlert:
          labels:
            severity: page
        ticketAlert:
          labels:
            severity: ticket
```

A tool such as Sloth compiles this specification into raw Prometheus
recording and alerting rules, which is strongly preferable to
hand-writing multi-window burn-rate PromQL for every service — the
generated rules are consistent and the burn-rate math cannot drift
between services maintained by different teams. The generated recording
rule for the SLI itself looks like:

```yaml
# generated: slo-recording-rules.yaml (excerpt)
groups:
  - name: checkout-api-availability-slo-sli-recording
    rules:
      - record: slo:sli_error:ratio_rate5m
        expr: |
          sum(rate(http_server_request_duration_seconds_count{
            service="checkout-api", http_response_status_code=~"5.."
          }[5m]))
          /
          sum(rate(http_server_request_duration_seconds_count{
            service="checkout-api", http_response_status_code!~"429"
          }[5m]))
        labels:
          service: checkout-api
          slo: requests-availability
      - record: slo:sli_error:ratio_rate1h
        expr: |
          sum(rate(http_server_request_duration_seconds_count{
            service="checkout-api", http_response_status_code=~"5.."
          }[1h]))
          /
          sum(rate(http_server_request_duration_seconds_count{
            service="checkout-api", http_response_status_code!~"429"
          }[1h]))
        labels:
          service: checkout-api
          slo: requests-availability
```

Precomputing the ratio at each required window as a recording rule keeps
the burn-rate alert expressions themselves cheap and readable:

```yaml
# generated: slo-alerting-rules.yaml (excerpt, page-severity rule)
groups:
  - name: checkout-api-availability-slo-alerts
    rules:
      - alert: CheckoutAPIAvailabilitySLOPageBurn
        expr: |
          (
            slo:sli_error:ratio_rate5m{service="checkout-api", slo="requests-availability"} > (14.4 * 0.001)
            and
            slo:sli_error:ratio_rate1h{service="checkout-api", slo="requests-availability"} > (14.4 * 0.001)
          )
          or
          (
            slo:sli_error:ratio_rate30m{service="checkout-api", slo="requests-availability"} > (6 * 0.001)
            and
            slo:sli_error:ratio_rate6h{service="checkout-api", slo="requests-availability"} > (6 * 0.001)
          )
        for: 2m
        labels:
          severity: page
          service: checkout-api
        annotations:
          summary: "checkout-api is burning its 30-day availability error budget fast"
          runbook: "https://runbooks.internal/checkout-api/slo-burn"
```

Compute remaining error budget for a dashboard panel or a chatbot query
with a single PromQL expression:

```promql
# Remaining error budget, as a fraction of the total 30-day budget
1 - (
  (1 - slo:sli_error:ratio_rate30d{service="checkout-api", slo="requests-availability"})
  /
  (1 - 0.999)
)
```

## Validation and Troubleshooting

- **Confirm the SLI excludes what it should.** Query the raw numerator
  and denominator series independently and manually verify a sample of
  excluded requests (synthetic checks, known bad-client traffic) are
  actually absent from both, not just the ratio. A ratio can look correct
  by coincidence while the underlying filter is wrong.
- **Symptom: `histogram_quantile()` returns no data.** The most common
  cause is a missing `by (le)` clause in the inner aggregation, or a
  label rename between the raw metric and the recording rule that drops
  `le` entirely. Run the inner `sum(rate(...)) by (le)` query alone first
  and confirm it returns one series per bucket boundary before wrapping
  it in `histogram_quantile()`.
- **Symptom: burn-rate alert never fires even during a known incident.**
  Check the recording rule's window against the Prometheus scrape
  interval and evaluation interval — a `5m` rate window needs at least
  two scrapes within that window to compute a rate, so a 5-minute scrape
  interval with a `5m` rate window is unreliable near the edge. Use a
  rate window at least four times the scrape interval.
- **Symptom: SLO reports 100% availability during a known partial
  outage.** Confirm the "valid" denominator query is not itself
  affected by the outage in a way that hides it — for example, if the
  outage caused requests to fail at a load balancer before reaching the
  instrumented service, the service's own metrics show zero traffic, not
  errors, and the SLI computed only from application metrics will miss
  the incident entirely. Layer an externally observed synthetic-probe SLI
  alongside the application-metric SLI for exactly this blind spot.
- **Bucket boundary drift after a code change.** If a service's
  histogram bucket boundaries change (a library upgrade that changes
  default buckets, for example) without updating the SLO's threshold
  query, the SLI silently starts measuring against the wrong latency
  threshold. Pin bucket boundaries explicitly in instrumentation
  configuration rather than accepting library defaults, and alert on
  `absent()` for the specific `le` bucket the SLO depends on.

## Security and Best Practices

- Treat SLO definitions and error-budget policy as governance artifacts:
  store them in version control with required review, the same as
  infrastructure-as-code, because a silently loosened SLO ("adjusting"
  99.9% to 99.5% without review) is a real and easy way to make an
  unreliable service appear compliant.
- Restrict who can edit generated alerting-rule files directly (as
  opposed to the source SLO specification) — hand-edits to generated
  rules drift from the source of truth and are typically overwritten
  silently on the next regeneration, which itself is a change-control
  risk if regeneration is not gated.
- Do not include personally identifiable information in SLI label
  values; label cardinality control ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)) applies with particular
  force to SLO recording rules, which are commonly among the
  highest-query-volume rules in the entire metrics backend.
- Version and diff error-budget policy changes visibly (who can declare a
  freeze, what a freeze restricts) the same as any other operational
  policy, since a quietly changed freeze policy can be used to bypass
  deployment risk controls.
- Alert on the absence of expected SLI data (`absent()` over the
  recording rule series), not only on the SLI's value — a broken metrics
  pipeline that stops producing data reads as "100% good" under a naive
  ratio query and will hide a real, ongoing outage from the SLO
  dashboard.

## References and Knowledge Checks

**References**

- Google, *Site Reliability Engineering*, Chapter 4 ("Service Level
  Objectives") and *The Site Reliability Workbook*, Chapter 5
  ("Alerting on SLOs"), free online editions.
- Prometheus documentation, `prometheus.io/docs/prometheus/latest/querying/`,
  for PromQL functions and native histograms.
- OpenSLO specification, `openslo.com`, for the vendor-neutral SLO
  definition schema.
- Sloth documentation, `sloth.dev`, for generating multi-window,
  multi-burn-rate Prometheus rules from an SLO specification.

**Knowledge Checks**

1. A service has a 99.9% availability SLO over a rolling 30-day window.
   Calculate the total allowed downtime-equivalent budget in minutes.
2. Explain why a Prometheus summary metric type is a poor choice for a
   service running behind a load balancer with many replicas.
3. Why does multi-window, multi-burn-rate alerting require both a short
   and a long window to agree before paging, instead of alerting on the
   short window alone?
4. A latency SLO of "95% of requests under 300ms" cannot be computed
   accurately from histogram data unless what precondition is met at
   instrumentation time?
5. Describe a failure scenario in which an SLI computed purely from
   application-emitted metrics reports full availability during a real
   outage, and the design change that closes the gap.

## Hands-On Lab

**Objective:** Instrument a sample HTTP service with a Prometheus
histogram, run Prometheus locally, compute an availability and a latency
SLI with PromQL, and validate a multi-window burn-rate alert firing
condition, including a negative test against a healthy baseline.

### Prerequisites

- Docker Engine and Docker Compose v2.
- `curl` and a POSIX shell.
- Approximately 1 GB of free memory for the lab stack.

### Procedure

1. Create the lab directory and a minimal instrumented service using the
   Prometheus Python client's built-in test server (no application code
   beyond a few lines is required for this lab):

   ```bash
   mkdir -p ~/slo-lab && cd ~/slo-lab
   cat > app.py <<'EOF'
   import random
   import time
   from http.server import BaseHTTPRequestHandler, HTTPServer
   from prometheus_client import Counter, Histogram, start_http_server

   REQUESTS = Counter(
       "http_server_request_duration_seconds_count",
       "Total requests",
       ["service", "http_response_status_code"],
   )
   LATENCY = Histogram(
       "http_server_request_duration_seconds",
       "Request duration",
       ["service"],
       buckets=[0.05, 0.1, 0.3, 0.5, 1.0, 2.5],
   )

   class Handler(BaseHTTPRequestHandler):
       def do_GET(self):
           start = time.time()
           # Simulate occasional errors and occasional slow requests.
           status = 500 if random.random() < 0.02 else 200
           delay = 0.4 if random.random() < 0.05 else 0.05
           time.sleep(delay)
           LATENCY.labels(service="lab-app").observe(time.time() - start)
           REQUESTS.labels(service="lab-app", http_response_status_code=str(status)).inc()
           self.send_response(status)
           self.end_headers()
           self.wfile.write(b"ok")

       def log_message(self, fmt, *args):
           return

   if __name__ == "__main__":
       start_http_server(9500)  # /metrics on :9500
       HTTPServer(("0.0.0.0", 8090), Handler).serve_forever()
   EOF
   ```

2. Create a Dockerfile for the app and a Prometheus configuration:

   ```bash
   cat > Dockerfile <<'EOF'
   FROM python:3.13-slim
   RUN pip install prometheus_client==0.21.1
   COPY app.py /app.py
   EXPOSE 8090 9500
   CMD ["python", "/app.py"]
   EOF

   cat > prometheus.yaml <<'EOF'
   global:
     scrape_interval: 15s
     evaluation_interval: 15s
   scrape_configs:
     - job_name: lab-app
       static_configs:
         - targets: ["lab-app:9500"]
   rule_files:
     - /etc/prometheus/slo-rules.yaml
   EOF
   ```

3. Create a recording-and-alerting rule file implementing a simplified
   single-window burn-rate check (kept to one window for lab clarity; the
   Design section above covers the full multi-window pattern):

   ```bash
   cat > slo-rules.yaml <<'EOF'
   groups:
     - name: lab-app-availability-slo
       rules:
         - record: slo:sli_error:ratio_rate5m
           expr: |
             sum(rate(http_server_request_duration_seconds_count{service="lab-app",http_response_status_code="500"}[5m]))
             /
             sum(rate(http_server_request_duration_seconds_count{service="lab-app"}[5m]))
         - alert: LabAppAvailabilitySLOBurn
           expr: slo:sli_error:ratio_rate5m > (14.4 * 0.001)
           for: 1m
           labels:
             severity: page
           annotations:
             summary: "lab-app burning availability error budget fast"
   EOF
   ```

4. Create the Compose file and start the stack:

   ```bash
   cat > docker-compose.yaml <<'EOF'
   services:
     lab-app:
       build: .
       ports:
         - "8090:8090"
         - "9500:9500"
     prometheus:
       image: prom/prometheus:v3.0.1
       volumes:
         - ./prometheus.yaml:/etc/prometheus/prometheus.yaml
         - ./slo-rules.yaml:/etc/prometheus/slo-rules.yaml
       ports:
         - "9090:9090"
   EOF
   docker compose up -d --build
   ```

5. Generate load against the sample service for at least five minutes so
   the `rate()` windows have enough data:

   ```bash
   for i in $(seq 1 600); do curl -s -o /dev/null http://localhost:8090/; sleep 0.5; done &
   ```

### Expected Results

After roughly two minutes of sustained load, open
`http://localhost:9090/graph`, query `slo:sli_error:ratio_rate5m`, and
confirm it returns a value near `0.02` (matching the simulated 2% error
injection rate in `app.py`). Query
`histogram_quantile(0.99, sum(rate(http_server_request_duration_seconds_bucket{service="lab-app"}[5m])) by (le))`
and confirm it returns a value consistent with the simulated 5% slow-tail
injection (roughly 0.4-0.5 seconds). Open the Alerts tab and confirm
`LabAppAvailabilitySLOBurn` is in a `firing` state, since a 2% sustained
error rate exceeds the `14.4 × 0.1% = 1.44%` page threshold used in this
lab's simplified single-window rule.

### Negative Test

Stop the load generator, edit `app.py` to set the error probability to
`0.0005` (well under the 0.1% SLO threshold), rebuild, and restart:

```bash
kill %1 2>/dev/null || true
sed -i.bak 's/random.random() < 0.02/random.random() < 0.0005/' app.py
docker compose up -d --build lab-app
for i in $(seq 1 600); do curl -s -o /dev/null http://localhost:8090/; sleep 0.5; done &
```

Wait five minutes, then re-query `slo:sli_error:ratio_rate5m` in
Prometheus and confirm it now reports a value near `0.0005`, well under
the `0.0144` burn-rate threshold, and confirm `LabAppAvailabilitySLOBurn`
returns to `inactive`. This demonstrates the alert correctly
distinguishes a genuine fast-burn condition from normal, budget-compliant
operation rather than firing on any nonzero error rate.

### Cleanup

```bash
kill %1 2>/dev/null || true
cd ~/slo-lab
docker compose down -v
cd ~
rm -rf ~/slo-lab
```

## Summary and Completion Checklist

SLIs express reliability as a precise ratio of good to valid events; SLOs
set a target for that ratio; error budgets convert the gap between 100%
and the SLO into a spendable, objectively tracked resource that resolves
the velocity-versus-reliability tension without relying on ad hoc
negotiation. Multi-window, multi-burn-rate alerting pages on the
trajectory toward budget exhaustion, catching both fast severe outages
and slow sustained degradation while suppressing single-scrape noise.
[Chapter 04](04-enterprise-logging-event-management-and-retention.md) turns to logs as the complementary signal that explains why an
SLI moved; [Chapter 06](06-actionable-alerting-on-call-and-operations-centers.md) builds the paging and on-call layer on top of the
burn-rate alerts introduced here.

**Completion checklist**

- [ ] Can select the correct Prometheus metric type (counter, gauge,
      histogram, summary) for a given signal and explain why.
- [ ] Can write a PromQL query computing an error ratio and a percentile
      latency from raw counter and histogram data.
- [ ] Can calculate an error budget in absolute time from an SLO
      percentage and a window length.
- [ ] Can explain multi-window, multi-burn-rate alerting and why it
      requires agreement between a short and a long window.
- [ ] Deployed a working local SLI/SLO pipeline and validated both a
      firing burn-rate alert and a healthy, non-firing baseline.
