# Chapter 03: Scraping and Service Discovery

## Learning Objectives

- Configure scrape jobs and static targets.
- Use service discovery to find targets dynamically.
- Apply relabeling to shape targets and labels.
- Validate configuration with promtool.
- Complete a walkthrough for each scraping concept.

## Theory and Architecture

Prometheus discovers what to scrape through **`scrape_configs`**: each job defines
**targets** (statically, or via **service discovery** — Kubernetes, file, DNS, cloud)
and a scrape **interval**. **Relabeling** transforms the target/label set before
(`relabel_configs`) and after (`metric_relabel_configs`) scraping — to drop targets,
rewrite labels, or filter metrics. **`promtool`** validates config and rules before you
reload. The reload endpoint (`/-/reload`) applies changes without a restart.

## Design Considerations

Use **service discovery** in dynamic environments (Kubernetes) rather than static lists.
Use **relabeling** to keep only relevant targets/metrics and to add meaningful labels
(env, team). Always **`promtool check`** before reloading.

## Implementation and Automation

The labs write a scrape config, add a target, relabel, and validate with promtool.

## Validation and Troubleshooting

Confirm the model:

```text
scrape_configs: jobs -> targets (static or SD) + interval.
relabel_configs: shape targets/labels pre-scrape; metric_relabel_configs post-scrape.
promtool check config <file>; reload via POST /-/reload (needs --web.enable-lifecycle).
```

Common pitfalls: editing config without **promtool** (bad reload); and scraping too
frequently (load) or too rarely (gaps).

## Security and Best Practices

Prefer **service discovery**, **relabel** to keep only what you need, set sensible
**intervals**, and **validate** every config change with promtool before reloading.
Restrict the lifecycle/reload endpoint.

## Hands-On Lab

Scraping walkthroughs. **Shared prerequisites** — Docker; a `prometheus.yml` you can
mount. **Cost:** none.

### Lab 3.1 — Define a scrape job

**Objective:** Add a static scrape target.

```yaml
# prometheus.yml
global: { scrape_interval: 15s }
scrape_configs:
  - job_name: self
    static_configs: [ { targets: ["localhost:9090"] } ]
  - job_name: node
    static_configs: [ { targets: ["node-exporter:9100"], labels: { env: lab } } ]
```

**Expected result:** two jobs — `self` and `node` (with an `env=lab` label) — the scrape
configuration.

**Negative test:** point a job at an endpoint that isn't exposing `/metrics`; the target
goes **down** — targets must expose Prometheus metrics.

**Cleanup:** none.

### Lab 3.2 — Validate the config with promtool

**Objective:** Check the config before reload.

```bash
docker run --rm -v "$PWD/prometheus.yml:/p.yml" prom/prometheus:latest \
  promtool check config /p.yml
```

**Expected result:** **SUCCESS: /p.yml is valid prometheus config** — a safe-to-load
file.

**Negative test:** reload a config with a YAML typo; Prometheus **rejects the reload** —
`promtool check` catches it first.

**Cleanup:** none.

### Lab 3.3 — Relabel to drop a target

**Objective:** Keep only targets matching a rule.

```yaml
scrape_configs:
  - job_name: node
    static_configs: [ { targets: ["a:9100","b:9100"] } ]
    relabel_configs:
      - source_labels: [__address__]
        regex: "a:9100"
        action: keep      # keep only 'a'
```

**Expected result:** only target **`a:9100`** scraped — relabeling filtering targets.

**Negative test:** scrape everything then filter in queries; **relabel at scrape time**
to avoid ingesting unwanted targets.

**Cleanup:** none.

### Lab 3.4 — Reload without restart

**Objective:** Apply config changes live.

```bash
# run Prometheus with --web.enable-lifecycle, then:
curl -sS -X POST "http://localhost:9090/-/reload" -w "HTTP %{http_code}\n"
```

**Expected result:** **HTTP 200** — the new config applied without a restart.

**Negative test:** POST `/-/reload` without `--web.enable-lifecycle`; it returns
**403** — enable the lifecycle endpoint.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Prometheus scrapes targets defined by scrape_configs (static or service discovery),
shaped by relabeling, validated by promtool, and applied via hot reload. This chapter
configured jobs, relabeled, validated, and reloaded.

- [ ] I can define scrape jobs and static targets.
- [ ] I can validate config with promtool.
- [ ] I can relabel to filter targets/labels.
- [ ] I can reload config without a restart.
- [ ] I completed Labs 3.1–3.4 including each negative test.
