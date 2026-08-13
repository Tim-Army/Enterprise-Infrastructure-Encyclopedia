# Chapter 06: Exporters and Instrumentation

## Learning Objectives

- Use exporters to expose third-party system metrics.
- Instrument an application with a client library.
- Push batch-job metrics via Pushgateway.
- Probe endpoints with the blackbox exporter.
- Complete a walkthrough for each instrumentation path.

## Theory and Architecture

Prometheus gets metrics two ways: **exporters** (sidecar processes that translate a
system's stats into the Prometheus format — **node_exporter** for hosts,
**blackbox_exporter** for probing endpoints, plus database/hardware exporters) and
**direct instrumentation** with a **client library** (Go, Python, Java, …) that exposes
`/metrics` from your app. **Pushgateway** is a special case: short-lived **batch jobs**
push metrics to it, and Prometheus scrapes the gateway — never use it for long-running
services.

## Design Considerations

Prefer **direct instrumentation** for your own apps and **exporters** for systems you
don't control. Use **node_exporter** for host metrics and **blackbox_exporter** for
synthetic probes. Reserve **Pushgateway** for batch jobs — it breaks the pull model's
liveness signal for services.

## Implementation and Automation

The labs run node_exporter, instrument a Python app, use Pushgateway, and describe
blackbox probing.

## Validation and Troubleshooting

Confirm the paths:

```text
Exporter: sidecar exposing /metrics (node_exporter :9100, blackbox :9115).
Client library: app exposes /metrics directly.
Pushgateway: batch jobs push; Prometheus scrapes the gateway (batch only).
```

Common pitfalls: Pushgateway for services (stale metrics, no liveness); and reinventing
an exporter that already exists.

## Security and Best Practices

Instrument your apps **directly**, use **existing exporters** for third-party systems,
keep **Pushgateway** for batch jobs, and secure exporter endpoints. Follow metric naming
conventions (`_total`, `_seconds`, `_bytes`).

## Hands-On Lab

Instrumentation walkthroughs. **Shared prerequisites** — Docker; Python with
`pip install prometheus-client`. **Cost:** none.

### Lab 6.1 — Run node_exporter

**Objective:** Expose host metrics.

```bash
docker run -d --name node -p 9100:9100 prom/node-exporter:latest
curl -sS "http://localhost:9100/metrics" | grep -m1 "^node_cpu_seconds_total"
```

**Expected result:** a **`node_cpu_seconds_total`** sample — host metrics via the
exporter.

**Negative test:** write a custom script to read `/proc`; **node_exporter** already
exposes host metrics correctly — reuse it.

**Rollback:** `docker rm -f node`.

### Lab 6.2 — Instrument an app (client library)

**Objective:** Expose a custom metric from Python.

```python
from prometheus_client import start_http_server, Counter
import time
REQS = Counter("app_requests_total", "requests", ["route"])
start_http_server(8000)
REQS.labels(route="/checkout").inc()
time.sleep(2)   # curl http://localhost:8000/metrics to see app_requests_total
```

**Expected result:** **`app_requests_total{route="/checkout"}`** at `/metrics` — direct
instrumentation.

**Negative test:** log request counts to a file and parse them; **instrument directly**
so Prometheus scrapes structured metrics.

**Rollback:** stop the script.

### Lab 6.3 — Push batch metrics via Pushgateway

**Objective:** Push a metric from a batch job.

```bash
docker run -d --name pgw -p 9091:9091 prom/pushgateway:latest
echo 'batch_job_last_success_seconds '"$(date +%s)" \
  | curl -sS --data-binary @- "http://localhost:9091/metrics/job/nightly_backup"
curl -sS "http://localhost:9091/metrics" | grep batch_job_last_success_seconds
```

**Expected result:** the pushed **`batch_job_last_success_seconds`** held by the gateway
— the batch-job pattern.

**Negative test:** push metrics for a long-running web service; the gateway holds
**stale** values with no liveness — instrument the service directly instead.

**Rollback:** `docker rm -f pgw`.

### Lab 6.4 — Probe an endpoint (blackbox)

**Objective:** Describe synthetic probing.

```text
# blackbox_exporter probes targets (HTTP/TCP/ICMP/DNS) and exposes probe_success etc.
# Prometheus scrapes /probe?target=https://example.com&module=http_2xx
"probe_success{instance='https://example.com'} = 1 when the endpoint is healthy"
```

**Expected result:** a **`probe_success`** signal for an external endpoint — synthetic
monitoring via blackbox.

**Negative test:** infer external availability from internal metrics; a **blackbox probe**
tests it from outside — use it for endpoint SLOs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Prometheus ingests metrics via exporters (node_exporter, blackbox for systems you don't
control), direct instrumentation with client libraries (your apps), and Pushgateway
(batch jobs only). This chapter ran an exporter, instrumented an app, pushed batch
metrics, and described blackbox probing.

- [ ] I can run node_exporter for host metrics.
- [ ] I can instrument an app with a client library.
- [ ] I can push batch metrics via Pushgateway.
- [ ] I can describe blackbox probing for endpoints.
- [ ] I completed Labs 6.1–6.4 including each negative test.
