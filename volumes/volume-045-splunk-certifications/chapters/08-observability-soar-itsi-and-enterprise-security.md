# Chapter 08: Observability, SOAR, ITSI, and Enterprise Security

## Learning Objectives

- Explain the specialist credentials: O11y Metrics User, SOAR Automation Developer, ITSI Admin, and ES Certified Admin.
- Describe observability (OpenTelemetry, metrics, detectors) and IT service intelligence.
- Apply SOAR playbook development and ES/ITSI administration.
- Relate these to the encyclopedia's observability and security volumes.
- Complete a per-topic walkthrough for each specialist area.

## Theory and Architecture

Beyond the Core, Admin, and Security tracks, Splunk certifies several specialist
platforms:

- **Splunk O11y Cloud Certified Metrics User** — **observability**: deploying the
  **OpenTelemetry Collector**, sending and exploring **metrics**, and building
  **detectors** (alerts) and dashboards in Splunk Observability Cloud.
- **Splunk SOAR Certified Automation Developer** — **automation and
  orchestration**: building **playbooks** and integrating apps to automate SOC
  response.
- **Splunk IT Service Intelligence (ITSI) Certified Admin** — **service
  monitoring**: modeling **services**, **KPIs**, and **glass tables** for
  IT/business service health.
- **Splunk Enterprise Security (ES) Certified Admin** — administering **ES**:
  installation, data-model/CIM configuration, and **correlation searches**.

These extend Splunk into observability (pairing with Volume XI) and deeper
security operations (pairing with the Cybersecurity Defense track).

## Design Considerations

Choose by platform: **O11y** for SRE/observability roles (metrics, OpenTelemetry,
detectors); **SOAR** for automation engineers (playbooks); **ITSI** for
service-monitoring/AIOps roles (services, KPIs, health scores); and **ES Admin**
for security-platform administrators. Each assumes Splunk fundamentals and adds a
product-specific skill set.

## Implementation and Automation

The labs below cover one skill per specialist area — OpenTelemetry/metrics and
detectors (O11y), a SOAR playbook, ITSI services/KPIs, and ES correlation-search
administration.

## Validation and Troubleshooting

Confirm the credentials before studying:

```text
splunk.com > O11y Metrics User / SOAR Automation Developer / ITSI Admin / ES Admin:
  - each has its own blueprint and product focus
  - all assume Splunk fundamentals (SPL/admin)
```

Common pitfalls: confusing **metrics** (O11y) with **events** (Core Splunk);
automating in SOAR without tested detections; and administering ES without a
**CIM/data-model** foundation.

## Security and Best Practices

Instrument with **OpenTelemetry** (vendor-neutral) for observability; gate SOAR
automation with approvals for high-impact actions; model ITSI **services** to
business impact (not just infrastructure); and keep ES built on **accelerated CIM
data models**. Right-size metric resolution and detector sensitivity to avoid
noise and cost.

## References and Knowledge Checks

- splunk.com: *O11y Metrics User*, *SOAR Automation Developer*, *ITSI Admin*, *ES Admin* blueprints; Observability Cloud, SOAR, ITSI, and ES docs; opentelemetry.io.

**Knowledge checks**

1. What does the O11y Metrics User deploy to collect metrics?
2. When should a SOAR playbook pause for human approval?
3. What does ITSI model that Core Splunk does not?

## Hands-On Lab

Per-topic walkthroughs — one lab per specialist area.

**Shared prerequisites** — a Splunk instance (and the relevant product/trial:
Observability Cloud, SOAR, ITSI, ES). **Cost:** none (trial).

### Lab 8.1 — O11y: deploy the OpenTelemetry Collector

**Objective:** Configure the Collector to send metrics to Observability Cloud.

```yaml
receivers: {hostmetrics: {collection_interval: 10s, scrapers: {cpu: {}, memory: {}}}}
exporters: {signalfx: {access_token: "${TOKEN}", realm: "${REALM}"}}
service:
  pipelines: {metrics: {receivers: [hostmetrics], exporters: [signalfx]}}
```

**Expected result:** a Collector pipeline scraping host metrics and exporting to
Splunk Observability Cloud — the O11y Metrics User's core deployment skill.

**Negative test:** hand-push metrics from scripts; the **OpenTelemetry Collector**
is the standard, scalable collection path — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — O11y: explore metrics and build a detector

**Objective:** Alert on a metric threshold (a detector).

```text
Detector: CPU utilization
  Signal: cpu.utilization (avg by host)
  Condition: > 90% for 5 minutes
  Alert: notify on trigger; clear when it recovers
```

**Expected result:** a detector firing on sustained high CPU — the metrics
alerting O11y certifies.

**Negative test:** alert on a single spike; require the condition to **persist**
(duration) to avoid noise.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — SOAR: build a playbook

**Objective:** Outline an automated response playbook.

```text
Playbook: Suspicious Login
  1. Trigger: notable from ES
  2. Enrich: geo/IP reputation, user risk
  3. Decision: risky? -> (approval) disable account; (auto) require MFA re-auth
  4. Respond: open ticket, notify SOC, record actions
```

**Expected result:** a SOAR playbook with enrichment, a decision, and an approval
gate — the automation the SOAR Automation Developer builds.

**Negative test:** auto-disable accounts on any alert; gate **high-impact**
actions behind approval — avoid harmful automation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — ITSI: model a service and KPIs

**Objective:** Define a service with KPIs and a health score.

```text
Service: Checkout
  KPIs: request latency (<300ms), error rate (<1%), throughput
  Health score: weighted KPI thresholds -> 0-100 service health
  Glass table: visualize Checkout dependencies and health
```

**Expected result:** a service modeled with KPIs and a health score — the
service-intelligence modeling ITSI certifies.

**Negative test:** monitor only infrastructure metrics; ITSI models **service**
health (business impact), not just hosts.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.5 — ES Admin: manage a correlation search

**Objective:** Administer an ES correlation search over CIM data.

```text
Correlation search: Excessive Failed Logins
  Search: | tstats count from datamodel=Authentication where Authentication.action=failure
           by Authentication.user | where count > 25
  Action: create notable (urgency=high), add risk to the user
  Governance: enable, schedule, and tune suppression
```

**Expected result:** an ES correlation search producing a notable and risk — the
ES administration (data models + correlation searches) the ES Admin performs.

**Negative test:** run correlation searches on raw data; ES relies on **accelerated
CIM data models** — build on them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Splunk's specialist credentials extend the platform: the **O11y Metrics User**
(OpenTelemetry, metrics, detectors), the **SOAR Automation Developer** (playbooks),
the **ITSI Admin** (services, KPIs, health), and the **ES Certified Admin** (ES on
CIM data models and correlation searches). Each assumes Splunk fundamentals and
adds a product-specific skill set.

- [ ] I can name the four specialist credentials and their focus.
- [ ] I can deploy the OpenTelemetry Collector and build a detector.
- [ ] I can outline a SOAR playbook with an approval gate.
- [ ] I can model an ITSI service and administer an ES correlation search.
- [ ] I completed Labs 8.1–8.5 including each negative test.
