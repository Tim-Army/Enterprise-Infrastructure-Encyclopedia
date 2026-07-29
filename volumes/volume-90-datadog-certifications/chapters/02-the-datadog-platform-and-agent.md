# Chapter 02: The Datadog Platform and Agent

## Learning Objectives

- Configure the Datadog Agent.
- Explain metric types (gauge, count, rate, histogram, distribution).
- Apply tags and unified service tagging.
- Send a custom metric with DogStatsD.
- Complete a walkthrough for each platform-and-Agent topic.

## Theory and Architecture

The **Datadog Fundamentals** exam centers on the **Agent** and the metric/tag model. The **Datadog
Agent** is software installed on each host (or run as a container/DaemonSet) that collects **metrics**,
**traces**, and **logs** and forwards them to Datadog. It is configured through **`datadog.yaml`** (the
main config: API key, site, tags) and per-integration files under **`conf.d/`**. Datadog **metrics** come
in types: **gauge** (a value at a point in time, like memory used), **count** (events over an interval),
**rate** (count per second), **histogram** (statistical distribution — avg/median/max/p95), and
**distribution** (globally accurate percentiles across hosts). Everything is organized by **tags**
(`key:value`) that let you slice and aggregate; **unified service tagging** (`env`, `service`, `version`)
ties metrics, traces, and logs together for a service. Custom application metrics are sent with
**DogStatsD** (a StatsD-compatible endpoint the Agent exposes) or the HTTP API. This chapter teaches the
platform and Agent with hands-on walkthroughs.

## Design Considerations

Configure the **Agent** with a consistent **tag** strategy from the start — apply **unified service
tagging** (`env`/`service`/`version`) so metrics, traces, and logs correlate. Choose the right **metric
type** (gauge for levels, count for events, histogram/distribution for latencies). Prefer
**distribution** metrics for accurate cross-host percentiles. Keep API keys in config/secrets, not in
code. Run the Agent close to what it monitors.

## Implementation and Automation

The labs configure the Agent's tags, reason about metric types, and send a custom metric with DogStatsD —
the platform grounding the Fundamentals exam validates.

## Validation and Troubleshooting

Confirm the platform and Agent:

```text
Agent: datadog.yaml (API key/site/tags) + conf.d/ integrations; collects metrics/traces/logs
Metric types: gauge (level) | count (events) | rate (per-sec) | histogram | distribution (cross-host pXX)
Tags (key:value) slice/aggregate; unified service tagging (env/service/version) correlates m/t/l
Custom metrics: DogStatsD (StatsD-compatible) or HTTP API
```

Common pitfalls: inconsistent or missing **tags** (cannot slice or correlate); and using a **gauge** for
something that should be a **count**/histogram (wrong aggregation).

## Security and Best Practices

Protect the API key (config/secret, not code), apply consistent tags, and run the Agent with least
privilege. Good tagging is the basis of everything else. All work is authorized administration of your
own hosts.

## Hands-On Lab

Platform-and-Agent walkthroughs. **Shared prerequisites** — a host with the Datadog Agent, edit access to
`datadog.yaml`, and `python3`/a DogStatsD client. **Cost:** none.

### Lab 2.1 — Configure Agent tags

**Objective:** Tag a host consistently.

```yaml
# /etc/datadog-agent/datadog.yaml
api_key: "${DD_API_KEY}"
site: datadoghq.com
tags:
  - env:prod
  - team:payments
  - role:web
```

```bash
sudo datadog-agent configcheck >/dev/null && datadog-agent status | grep -A3 "Host tags"
```

```text
Host tags:
  env:prod
  team:payments
  role:web
```

**Expected result:** the host reporting `env`, `team`, and `role` tags — the basis for slicing metrics.

**Negative test:** run the Agent with no host tags; you cannot group by env/team — add a **tag** strategy.

**Cleanup:** none (tags are the desired state).

### Lab 2.2 — Reason about metric types

**Objective:** Pick the right type.

```python
python3 - <<'PY'
choices = {
  "memory_used_bytes":  "gauge (a level at a point in time)",
  "http_requests":      "count (events over the interval) -> rate for per-second",
  "request_latency_ms": "histogram / distribution (percentiles: p50/p95/p99)",
}
for metric, kind in choices.items(): print(f"{metric:20}: {kind}")
print("Use distribution for globally accurate percentiles across many hosts")
PY
```

**Expected result:** each metric matched to its correct type — levels vs events vs latencies.

**Negative test:** store latency as a **gauge** and average it; you lose percentiles — use a
**histogram/distribution**.

**Cleanup:** none.

### Lab 2.3 — Apply unified service tagging

**Objective:** Correlate metrics, traces, and logs.

```yaml
# environment for an instrumented app (unified service tagging)
DD_ENV: prod
DD_SERVICE: checkout
DD_VERSION: 1.4.2
```

```python
python3 - <<'PY'
tags = {"env": "prod", "service": "checkout", "version": "1.4.2"}
print("Unified service tags:", tags)
print("Result: metrics, traces, and logs for 'checkout' correlate by env/service/version")
PY
```

**Expected result:** `env`/`service`/`version` set so the service's telemetry correlates across products.

**Negative test:** tag metrics one way and traces another; use **unified service tagging** so they line
up.

**Cleanup:** none.

### Lab 2.4 — Send a custom metric with DogStatsD

**Objective:** Emit an application metric.

```python
python3 - <<'PY'
# datadog DogStatsD client (Agent exposes 8125/udp)
from datadog import initialize, statsd
initialize(statsd_host="127.0.0.1", statsd_port=8125)
statsd.increment("orders.placed", tags=["env:prod", "service:checkout"])
statsd.gauge("cart.items", 3, tags=["env:prod"])
print("sent orders.placed (count) and cart.items (gauge) via DogStatsD")
PY
```

```text
sent orders.placed (count) and cart.items (gauge) via DogStatsD
```

**Expected result:** a count and a gauge custom metric sent through DogStatsD — application telemetry in
Datadog.

**Negative test:** POST every event to the HTTP API synchronously in the request path; use **DogStatsD**
(fast, local, UDP) for high-frequency custom metrics.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Datadog platform centers on the Agent (configured via `datadog.yaml` and `conf.d/`) collecting
metrics, traces, and logs, organized by tags — with metric types (gauge, count, rate, histogram,
distribution) chosen to fit the data, unified service tagging (env/service/version) correlating
telemetry, and DogStatsD sending custom application metrics.

- [ ] I can configure the Agent and its tags.
- [ ] I can choose the right metric type.
- [ ] I can apply unified service tagging.
- [ ] I can send a custom metric with DogStatsD.
- [ ] I completed Labs 2.1–2.4 including each negative test.
