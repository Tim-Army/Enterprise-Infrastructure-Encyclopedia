# Chapter 03: Infrastructure Monitoring

## Learning Objectives

- Enable an integration to collect a service's metrics.
- Explore metrics in the Metrics Explorer.
- Reason about the host map and infrastructure list.
- Monitor containers and processes.
- Complete a walkthrough for each infrastructure-monitoring topic.

## Theory and Architecture

**Infrastructure monitoring** is Datadog's foundation and a core **Fundamentals** domain. Datadog ships
**700+ integrations** — Agent checks configured under **`conf.d/<integration>.d/conf.yaml`** — that
collect metrics from databases, web servers, message queues, cloud services, and more. Collected metrics
are explored in the **Metrics Explorer** (graph any metric, grouped and filtered by **tags**), and the
**Metrics Summary** lists metadata. The **host map** visualizes the whole fleet colored by any metric to
spot outliers at a glance, while the **infrastructure list** tabulates hosts, their status, and tags.
For containers, **live containers** and **live processes** views show per-container/per-process resource
use in real time (via the Agent's container/process collection). Understanding how integrations feed
metrics that you then explore, map, and drill into is the heart of infrastructure monitoring. This
chapter teaches it with hands-on walkthroughs.

## Design Considerations

Enable the **integration** for each service rather than hand-rolling metrics. Use **tags** consistently so
the **Metrics Explorer** and **host map** can group meaningfully. Use the **host map** to spot outliers
across a large fleet and the **infrastructure list** for status/tag audits. Enable **container/process**
collection where you run containers. Watch metric **cardinality** (too many unique tag combinations costs
money).

## Implementation and Automation

The labs enable an integration, query a metric via the API (the Metrics Explorer's backend), and reason
about the host map and containers — the infrastructure monitoring the Fundamentals exam validates.

## Validation and Troubleshooting

Confirm infrastructure monitoring:

```text
Integrations (700+): conf.d/<integration>.d/conf.yaml -> Agent collects service metrics
Metrics Explorer: graph any metric grouped/filtered by tags; Metrics Summary = metadata
Host map: fleet colored by a metric (spot outliers); infrastructure list: hosts + status + tags
Containers/processes: live views of per-container/process resource use
```

Common pitfalls: writing custom scripts to scrape a service that has an **integration**; and exploding
metric **cardinality** with high-uniqueness tags.

## Security and Best Practices

Use official integrations, scope Agent permissions, and watch cardinality/cost. Consistent tags make the
whole platform usable. All work is authorized monitoring of your own infrastructure.

## Hands-On Lab

Infrastructure-monitoring walkthroughs. **Shared prerequisites** — a Datadog Agent, an API/app key, and
`curl`. **Cost:** none.

### Lab 3.1 — Enable an integration

**Objective:** Collect a service's metrics.

```yaml
# /etc/datadog-agent/conf.d/nginx.d/conf.yaml
instances:
  - nginx_status_url: http://localhost:81/nginx_status
    tags:
      - service:web
```

```bash
sudo systemctl restart datadog-agent
datadog-agent status | grep -A2 "nginx"
```

```text
nginx (5.3.0)
  Instance ID: nginx:... [OK]
  Total Runs: 3
```

**Expected result:** the NGINX integration collecting metrics with an `[OK]` check — service metrics
flowing.

**Negative test:** scrape NGINX status with a cron job into a custom metric; enable the **integration**
instead.

**Rollback:** remove the conf file if not needed.

### Lab 3.2 — Query a metric (Metrics Explorer backend)

**Objective:** Graph a metric via the API.

```bash
NOW=$(date +%s); FROM=$((NOW-3600))
curl -s -G "https://api.datadoghq.com/api/v1/query" \
  -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  --data-urlencode "from=${FROM}" --data-urlencode "to=${NOW}" \
  --data-urlencode "query=avg:system.cpu.user{env:prod} by {host}" \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);print("series:",len(d.get("series",[])))'
```

```text
series: 3
```

**Expected result:** a timeseries per host for CPU — the query the Metrics Explorer runs under the hood.

**Negative test:** query a metric with no `by {}` grouping when you need per-host detail; group by a
**tag** to see outliers.

**Rollback:** none (read-only).

### Lab 3.3 — Reason about the host map

**Objective:** Spot outliers across the fleet.

```python
python3 - <<'PY'
hosts = {"web-1": 0.30, "web-2": 0.35, "web-3": 0.92, "web-4": 0.28}  # cpu fraction
hottest = max(hosts, key=hosts.get)
print("Host map colored by cpu:")
for h, v in hosts.items(): print(f"  {h}: {'#'*int(v*20)} {v:.0%}")
print(f"Outlier: {hottest} at {hosts[hottest]:.0%} -> investigate")
PY
```

**Expected result:** a fleet view highlighting the hot host — the host map's outlier-spotting value.

**Negative test:** scan a long table of hosts by hand; the **host map** colors the fleet so the outlier
pops.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Monitor containers

**Objective:** See per-container resource use.

```bash
# Agent container collection (Docker/K8s) surfaces live containers
datadog-agent status | grep -A2 "Docker\|Containerd" || echo "enable container collection"
```

```text
Docker
  Successfully connected; 12 containers reported
```

**Expected result:** the Agent reporting live containers — per-container CPU/memory visibility.

**Negative test:** monitor only host-level metrics in a container platform; enable **container**
collection to see per-container use.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Datadog infrastructure monitoring collects metrics through 700+ integrations (Agent checks under
`conf.d/`), explored and graphed in the Metrics Explorer by tag, visualized across the fleet in the host
map to spot outliers, and drilled into per-container and per-process with live views — all resting on a
consistent tag strategy.

- [ ] I can enable an integration.
- [ ] I can query and graph a metric.
- [ ] I can reason about the host map.
- [ ] I can monitor containers.
- [ ] I completed Labs 3.1–3.4 including each negative test.
