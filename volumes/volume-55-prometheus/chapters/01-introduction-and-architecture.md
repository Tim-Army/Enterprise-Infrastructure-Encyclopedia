# Chapter 01: Introduction and Architecture

## Learning Objectives

- Explain what Prometheus is and its pull-based model.
- Describe the architecture: server, TSDB, scraping, and PromQL.
- Run Prometheus and scrape a target.
- Query the HTTP API.
- Verify the running version.

## Theory and Architecture

**Prometheus** is the open-source (CNCF) **monitoring system and time-series database
(TSDB)**. It is **pull-based**: the server periodically **scrapes** HTTP `/metrics`
endpoints exposed by instrumented targets, stores samples in its local **TSDB**, and
makes them queryable with **PromQL**. It graduated as the second CNCF project (after
Kubernetes) and is the de-facto standard for metrics in cloud-native systems. This
volume targets the **3.x** series (**v3.13.x**).

The core pieces: the **Prometheus server** (scrape + store + query + rule evaluation),
**exporters/instrumented apps** (expose `/metrics`), **service discovery** (finds
targets dynamically), **recording/alerting rules**, and **Alertmanager** (handles
alert routing/notification). For long-term/global storage it integrates with remote
systems (Thanos, Mimir) via **remote write/read**.

## Design Considerations

Prometheus is **metrics** (numeric time series), not logs or traces — pair it with
Loki/OTel for those. Its **pull** model means targets expose metrics and Prometheus
discovers/scrapes them, which suits dynamic (Kubernetes) environments. Keep label
**cardinality** bounded — every unique label set is a series.

## Implementation and Automation

Run Prometheus with Docker and scrape itself:

```bash
docker run -d --name prom -p 9090:9090 prom/prometheus:latest
```

## Validation and Troubleshooting

Confirm the platform facts:

```text
Prometheus (CNCF):
  - pull-based metrics + TSDB; PromQL query language
  - scrapes HTTP /metrics; service discovery finds targets
  - Alertmanager handles alert routing; remote write/read for long-term storage
  - current series 3.x (v3.13.x)
```

Common pitfalls: expecting a push model (it **pulls**; use Pushgateway only for batch
jobs); and unbounded label cardinality (series explosion).

## Security and Best Practices

Bound label **cardinality**, secure the server and `/metrics` endpoints (TLS/auth),
scope scrape targets, and offload long-term storage to remote systems. Use Pushgateway
sparingly (batch jobs only).

## References and Knowledge Checks

- prometheus.io/docs: architecture, configuration, PromQL, and the HTTP API.

**Knowledge checks**

1. Why is Prometheus pull-based, and when do you use Pushgateway?
2. What does Prometheus store — metrics, logs, or traces?
3. What handles alert notifications?

## Hands-On Lab

Setup and orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — Docker;
`curl`, `python3`. **Cost:** none.

### Lab 1.1 — Run Prometheus

**Objective:** Start Prometheus and confirm it is up.

```bash
docker run -d --name prom -p 9090:9090 prom/prometheus:latest
curl -sS "http://localhost:9090/-/ready" ; echo
```

**Expected result:** **Prometheus Server is Ready.** — a running server scraping itself.

**Negative test:** query before the server is ready; `/-/ready` returns **503** until
startup completes — wait for ready.

**Cleanup:** `docker rm -f prom`.

### Lab 1.2 — Confirm the self-scrape target

**Objective:** Verify the built-in `prometheus` target is up.

```bash
curl -sS "http://localhost:9090/api/v1/targets" \
  | python3 -c "import sys,json;d=json.load(sys.stdin)['data']['activeTargets'];print([t['health'] for t in d])"
```

**Expected result:** a target with health **up** — proof scraping works end to end.

**Negative test:** assume a target is scraped because it's configured; **check
`/targets`** — a down target has health `down` with an error.

**Cleanup:** none (read-only).

### Lab 1.3 — Query the API

**Objective:** Run a PromQL query over the HTTP API.

```bash
curl -sS "http://localhost:9090/api/v1/query?query=up" \
  | python3 -c "import sys,json;r=json.load(sys.stdin)['data']['result'];print('series:',len(r),'value:',r[0]['value'][1] if r else None)"
```

**Expected result:** the **`up`** metric returning `1` for the scraped target — the query
path.

**Negative test:** query a metric name that doesn't exist; the result is **empty** —
confirm the metric is exposed/scraped.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Prometheus is the CNCF pull-based metrics system and TSDB: it scrapes `/metrics`
targets, stores samples, and queries them with PromQL, with Alertmanager for
notifications and remote write/read for long-term storage. This chapter ran Prometheus
and queried the API.

- [ ] I can explain the pull model and when to use Pushgateway.
- [ ] I can describe server/TSDB/scraping/PromQL.
- [ ] I can run Prometheus and confirm it is ready.
- [ ] I can check targets and query the API.
- [ ] I completed Labs 1.1–1.3 including each negative test.
