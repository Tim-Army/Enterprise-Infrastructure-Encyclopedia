# Chapter 06: Observability Engineer — Metrics, Logs, and Uptime

## Learning Objectives

- Collect metrics with Elastic Agent and integrations.
- Collect and tail logs with Elastic Agent.
- Monitor uptime with Heartbeat.
- Analyze data in the Metrics, Logs, and Uptime apps.
- Complete a walkthrough for each metrics-logs-uptime topic.

## Theory and Architecture

The **Elastic Certified Observability Engineer** exam covers ingesting and analyzing the three pillars of
observability. **Metrics** — install **Elastic Agent** and enable **integrations** to collect a service's
metrics, then analyze them in the **Metrics app** (including predefined machine-learning jobs).
**Logs** — install Elastic Agent, enable integrations, and configure **custom log** collection to tail a
given file, then analyze in the **Logs app** (also with ML jobs). **Uptime** — run **Heartbeat** to check
whether a service is reachable over **ICMP, TCP, or HTTP**, and monitor availability in the **Uptime
app**. All data lands in Elasticsearch as a single source and is analyzed in Kibana. This chapter teaches
the metrics, logs, and uptime pillars with hands-on walkthroughs (Elastic Agent/Heartbeat configuration
and the underlying data via the API).

## Design Considerations

Prefer **Elastic Agent + integrations** (Fleet-managed) for metrics and logs — one agent, central
config, curated integrations. Tail application logs with the **custom logs** integration and enrich at
ingest (Chapter 04). Run **Heartbeat** from the vantage point your users experience (external for public
services). Enable the **predefined ML jobs** to catch anomalies without hand-building models.

## Implementation and Automation

The labs configure Elastic Agent for metrics and logs, configure a Heartbeat monitor, and query the
resulting observability data — the ingestion and analysis the exam validates.

## Validation and Troubleshooting

Confirm the three pillars:

```text
Metrics: Elastic Agent + integration -> Metrics app (+ predefined ML jobs)
Logs:    Elastic Agent + integration / custom-log tail -> Logs app (+ ML)
Uptime:  Heartbeat (ICMP/TCP/HTTP) -> Uptime app
All land in Elasticsearch as one source; analyze in Kibana
```

Common pitfalls: running many standalone Beats when a Fleet-managed **Elastic Agent** would centralize
config; and monitoring uptime from inside the network for a service users reach from outside.

## Security and Best Practices

Use least-privilege Elastic Agent enrollment tokens, secure the Fleet server, and scope which
integrations run where. Observability protects your own systems. All work is authorized.

## Hands-On Lab

Metrics-logs-uptime walkthroughs. **Shared prerequisites** — an Elastic Stack with Fleet and Elastic
Agent (or the concepts, modeled), `curl`, and `python3`. **Cost:** none.

### Lab 6.1 — Collect metrics with Elastic Agent

**Objective:** Ingest a service's metrics.

```text
Kibana > Fleet > Agent policy "servers" > Add integration: System
  Collect: CPU, memory, disk, network metrics every 10s
Enroll host with the System integration -> metrics flow to metrics-system.* data streams
Verify:
```

```bash
curl -s -k -u elastic:$PW "https://localhost:9200/_cat/indices/metrics-system*?v&h=index,docs.count"
```

```text
index                              docs.count
.ds-metrics-system.cpu-default...  8640
```

**Expected result:** system metrics flowing into `metrics-system.*` data streams — visible in the
Metrics app.

**Negative test:** hand-write a custom metrics shipper when the **System integration** already collects
CPU/memory/disk; use the curated integration.

**Cleanup:** remove the test integration from the policy if not needed.

### Lab 6.2 — Collect and tail logs

**Objective:** Ingest application logs.

```text
Fleet > Agent policy "servers" > Add integration: Custom Logs
  Paths: /var/log/myapp/*.log
  Dataset: myapp.log ; (optional) ingest pipeline for parsing
Result: log lines flow to logs-myapp.log-* and appear in the Logs app
```

```bash
curl -s -k -u elastic:$PW "https://localhost:9200/logs-myapp.log-default/_count"
```

```json
{ "count": 1543 }
```

**Expected result:** application logs tailing into `logs-myapp.log-*` — searchable in the Logs app.

**Negative test:** copy log files around manually; configure the **Custom Logs integration** to tail
them continuously instead.

**Cleanup:** remove the integration if not needed.

### Lab 6.3 — Monitor uptime with Heartbeat

**Objective:** Check service reachability.

```yaml
# heartbeat.yml
heartbeat.monitors:
  - type: http
    id: web-home
    urls: ["https://www.example.com"]
    schedule: '@every 30s'
    check.response.status: [200]
  - type: icmp
    id: gw-ping
    hosts: ["10.0.0.1"]
    schedule: '@every 30s'
```

**Expected result:** Heartbeat checking an HTTP endpoint and an ICMP host every 30s — availability in the
Uptime app.

**Negative test:** monitor a public site only from inside the datacenter; run **Heartbeat** from where
users actually connect.

**Cleanup:** stop the Heartbeat monitor if not needed.

### Lab 6.4 — Query observability data

**Objective:** Confirm the single data source.

```bash
curl -s -k -u elastic:$PW -X GET "https://localhost:9200/metrics-system.cpu-default/_search" -H 'Content-Type: application/json' -d'
{ "size": 0, "aggs": { "avg_cpu": { "avg": { "field": "system.cpu.total.norm.pct" } } } }'
```

```json
{ "aggregations": { "avg_cpu": { "value": 0.34 } } }
```

**Expected result:** average CPU across the metrics data — the Metrics app's underlying query.

**Negative test:** keep metrics, logs, and uptime in three disconnected tools; Elastic unifies them in
**one** Elasticsearch source for correlation.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Observability Engineer ingests the three pillars into one Elasticsearch source: metrics and logs via
Elastic Agent integrations (analyzed in the Metrics and Logs apps with ML jobs) and uptime via Heartbeat
over ICMP/TCP/HTTP (analyzed in the Uptime app) — a single, correlatable observability platform.

- [ ] I can collect metrics with Elastic Agent.
- [ ] I can collect and tail logs.
- [ ] I can monitor uptime with Heartbeat.
- [ ] I can query the resulting observability data.
- [ ] I completed Labs 6.1–6.4 including each negative test.
