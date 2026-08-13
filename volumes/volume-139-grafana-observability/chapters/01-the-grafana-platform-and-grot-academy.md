# Chapter 01: The Grafana Platform and GROT Academy

![The Grafana observability platform and its GROT Academy credential program. The platform spans open-source components — Grafana for visualization, Loki for logs, Mimir for metrics, Tempo for traces, Pyroscope for profiles, Alloy for collection, Beyla for eBPF auto-instrumentation, Faro for frontend observability, k6 for load testing, and OnCall — alongside Grafana Cloud and the Enterprise Stack. GROT Academy awards six free digital badges in three tiers: Trailblazer for the Technical Practitioner 101 learning path, Explorer for Technical Practitioner 201, both requiring a completed learning path and a passed aligned assessment, and four Navigator badges for PromQL Zero to Hero, LogQL Zero to Hero, Observability Signals Foundations, and Dashboard Design and Visual Storytelling, each requiring only the learning path to be completed. All GROT Academy learning content is currently available at no cost, badges issue through Credly, and new badges are expected to launch each quarter.](../../../diagrams/volume-139-grafana-observability/chapter-01-platform-and-academy.svg)

*Figure 1-1. The Grafana platform's components and the GROT Academy badge tiers built on top of them.*

## Learning Objectives

- Describe the Grafana platform: the open-source components, Grafana Cloud, and the Enterprise Stack.
- Explain the GROT Academy badge program, its three tiers, and how badges are earned.
- Distinguish what Grafana Labs actually offers from what third parties claim it offers.
- Set up a free study environment for the labs in this volume.

## What Grafana is

Grafana began as a visualization layer — dashboards over someone else's data — and grew into a full observability platform. Its defining architectural choice remains that first one: **Grafana queries data where it lives** rather than requiring you to send everything into a single proprietary store. A dashboard can pull metrics from Prometheus, logs from Loki, traces from Tempo, and rows from PostgreSQL, side by side.

### The open-source components

| Component | Signal / role |
|:---|:---|
| **Grafana** | Visualization, dashboards, alerting, exploration |
| **Loki** | Log aggregation, queried with **LogQL** |
| **Mimir** | Scalable long-term metrics storage (Prometheus-compatible) |
| **Tempo** | Distributed tracing backend |
| **Pyroscope** | Continuous profiling |
| **Alloy** | Telemetry collector — the pipeline that gathers and forwards |
| **Beyla** | eBPF auto-instrumentation, without touching application code |
| **Faro** | Frontend/browser observability |
| **k6** | Load and performance testing |
| **OnCall** | On-call scheduling and escalation |

The "**LGTM stack**" — Loki, Grafana, Tempo, Mimir — is the common shorthand for the core four.

### Open source, Cloud, and Enterprise

| Edition | What it is |
|:---|:---|
| **Open source** | Free, self-hosted, genuinely capable — this is not a crippled edition |
| **Grafana Cloud** | Managed SaaS: hosted Loki/Mimir/Tempo/Pyroscope plus Cloud-only features (Asserts, IRM, SLO, Synthetic Monitoring, Application and Frontend Observability) |
| **Grafana Enterprise Stack** | Self-managed with enterprise features and support |

This matters for study: **GROT Academy's learning paths are built around Grafana Cloud**, so some material assumes the managed backends rather than a self-hosted stack.

## GROT Academy: badges, not (yet) certifications

Grafana Labs' credential program runs through **GROT Academy**, and it is important to describe it accurately because the wider internet does not.

**Grafana Labs currently awards digital badges.** The program's own page is titled "Badges & Certifications," lists **six badges**, and its FAQ asks *"When will new badges and certifications be available?"* — answering that **new badges are expected to launch each quarter**. The certification tier, in other words, is still being built out.

### The six badges, in three tiers

| Tier | Badge | Earned by |
|:---|:---|:---|
| **Trailblazer** | Technical Practitioner **101** | Learning path completed **and aligned assessment passed** |
| **Explorer** | Technical Practitioner **201** | Learning path completed **and aligned assessment passed** |
| **Navigator** | **PromQL Zero to Hero** | Learning path completed |
| **Navigator** | **LogQL Zero to Hero** | Learning path completed |
| **Navigator** | **Observability Signals Foundations: Metrics, Logs & Traces** | Learning path completed |
| **Navigator** | **Dashboard Design & Visual Storytelling** | Learning path completed |

Note the distinction: the **101 and 201 badges require passing an assessment**, while the four Navigator badges require only completing their learning path.

### The program's terms

- **"All GROT Academy learning content is currently available at no cost."** The program is free; enrollment goes through a registration flow, but there is no exam fee.
- Credentials issue through **Credly**, which sends an email after your first badge. Badges can be made private in Credly's settings.
- Eligibility is broad: **customers, partners, and community members** — anyone completing the programs, which are designed for Grafana Cloud users.

### A caution about third-party material

Search for Grafana certification and you will find courses and practice tests for a "**Certified Grafana Associate**," complete with confident exam-domain weightings. **No such exam appears in Grafana Labs' own catalog.** Whatever those products are testing, it is not a credential you can currently earn from Grafana. Check GROT Academy directly before paying anyone for exam preparation — the official program is free, which makes paid third-party preparation for it a strange purchase in any case.

## How hard is the 101 path, really?

Grafana's ladder is coherent across the two badges: **101 is described as the "introductory" curriculum** and **201 as the "intermediate-level"** one. The odd one out is the **101 learning-path page**, which markets the same material as "**advanced** tools and techniques" for those going "**beyond the basics**," aimed at "engineers, developers, and **power users**."

Take the badge descriptions as the intended ladder and the path page's language as enthusiasm. But do not read "introductory" as "no prerequisites" either — the 101 syllabus covers PromQL, LogQL, recording rules in Mimir and Loki, alerting tied to SLOs, and deploying Alloy on Kubernetes through a Helm chart. That is introductory *to Grafana Cloud*, while assuming you are already comfortable with Kubernetes and with the idea of a time-series query language.

One further honesty note about the badges: **101 and 201 state nearly identical competencies** — navigating and configuring Grafana Cloud, interpreting metrics/logs/traces with core visualization tools, applying observability best practices, and using dashboards, alerts, and queries for data-informed decisions. The 201 wording adds "real-world" and "operational insight," which is a difference of emphasis rather than of substance. **Choose between them by comparing the learning-path curricula, not the badge descriptions.**

## This volume

Chapters 02–08 follow the **Technical Practitioner 101** curriculum, because it is Grafana's own statement of what a practitioner should know:

| Chapter | GROT Academy module |
|:---|:---|
| [02](02-collection-with-alloy.md) Collection with Alloy | Collection of Metrics, Logs & Traces |
| [03](03-data-sources-queries-transformations.md) Data sources and transformations | (platform foundations) |
| [04](04-promql-for-metrics.md) PromQL | Building Efficient Queries: PromQL |
| [05](05-loki-and-logql.md) Loki and LogQL | Building Efficient Queries: LogQL |
| [06](06-traces-and-correlation.md) Traces and correlation | Using Logs, Metrics, and Traces Together |
| [07](07-dashboards-and-the-four-golden-signals.md) Dashboards | Building Effective Dashboards with the Four Golden Signals |
| [08](08-recording-rules-alerting-and-slos.md) Recording rules, alerting, SLOs | Recording Rules + Alerting Essentials |

## Free study environment

**Grafana is open source and free to run**, so unlike most volumes here you genuinely can stand up the real thing. The labs below nonetheless model the *concepts* — query evaluation, transformation pipelines, cardinality arithmetic, alert state machines, burn-rate math — in plain Python, so they run in seconds and isolate the reasoning the badges assess.

## Hands-On Lab

### Lab 1.1 — Set up the study environment

**Objective:** Confirm the free toolchain.

```bash
python3 --version
mkdir -p ~/grafana-study && cd ~/grafana-study
python3 - <<'EOF'
print("Observability study environment ready.")
print("Labs model: telemetry pipelines, PromQL/LogQL evaluation, transformations,")
print("trace correlation, cardinality, recording rules, alert states, SLO burn rate.")
print("Grafana OSS is free to run too — docker run -p 3000:3000 grafana/grafana")
EOF
```

**Expected result:** Python reports a version and the message prints. Unusually for this encyclopedia, the real product is also free — running Grafana alongside these labs is genuinely worthwhile.

**Negative test:** Assuming a Grafana Cloud subscription is required to learn the platform — the open-source stack covers most of the curriculum, though Cloud-only features (Asserts, IRM, Synthetic Monitoring) are exactly that.

**Rollback:** `rm -rf ~/grafana-study` when finished.

### Lab 1.2 — Plan a badge path

**Objective:** Choose a route through the badges and set expectations honestly.

```bash
python3 - <<'EOF'
BADGES = {
  "Trailblazer: Technical Practitioner 101": {"tier":"Trailblazer","assessment":True,
      "covers":["Alloy collection on k8s","PromQL","LogQL","Four Golden Signals dashboards",
                "recording rules","alerting + SLOs","correlating signals"]},
  "Explorer: Technical Practitioner 201":    {"tier":"Explorer","assessment":True,  "covers":["builds on 101"]},
  "Navigator: PromQL Zero to Hero":          {"tier":"Navigator","assessment":False,"covers":["PromQL depth"]},
  "Navigator: LogQL Zero to Hero":           {"tier":"Navigator","assessment":False,"covers":["LogQL depth"]},
  "Navigator: Observability Signals Foundations":{"tier":"Navigator","assessment":False,"covers":["metrics, logs, traces"]},
  "Navigator: Dashboard Design & Visual Storytelling":{"tier":"Navigator","assessment":False,"covers":["dashboard design"]},
}
for name, b in BADGES.items():
    gate = "learning path + PASSED ASSESSMENT" if b["assessment"] else "learning path completed"
    print(f"{b['tier']:12} {name.split(': ',1)[1]:42} <- {gate}")

print("\nCost: $0 — all GROT Academy learning content is currently free. Badges via Credly.")
print("Cadence: new badges expected each quarter, so re-check the catalog.")

print("\n--- honest effort estimate for 101 ---")
prereqs = {"comfortable with Kubernetes":True, "seen a time-series query language":False,
           "have a Grafana Cloud account":True}
for p, have in prereqs.items():
    print(f"   [{'yes' if have else 'NO '}] {p}")
missing = [p for p, have in prereqs.items() if not have]
if missing:
    print(f"\n   Grafana's badge page calls 101 'introductory'; its path page calls it 'advanced'.")
    print(f"   The syllabus (PromQL, LogQL, recording rules, SLO alerting, Alloy on k8s) is INTERMEDIATE.")
    print(f"   Missing {missing} — budget extra time; do not trust the word 'introductory'.")
EOF
```

**Expected result:** The badge ladder prints with its gating, the zero cost and quarterly cadence are recorded, and the readiness check flags the gap. The closing lines are the practically useful part — Grafana's own two descriptions of this path contradict each other, and the syllabus settles it as intermediate.

**Negative test:** Buying a third-party "Certified Grafana Associate" course — that credential does not appear in Grafana's catalog, and the official learning content is free.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Grafana platform's components identified, and the LGTM stack named.
- [ ] Open source, Grafana Cloud, and Enterprise Stack distinguished.
- [ ] The six GROT Academy badges and three tiers mapped, with their differing gates.
- [ ] The program's free, Credly-issued, quarterly-expanding nature recorded.
- [ ] Third-party "Certified Grafana Associate" claims checked against the official catalog.
- [ ] The 101 path calibrated as intermediate rather than introductory.
