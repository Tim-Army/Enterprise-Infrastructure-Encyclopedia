# Chapter 09: Badge Paths, Currency, and Career

## Learning Objectives

- Choose a GROT Academy badge path and estimate the effort honestly.
- Place Grafana among the encyclopedia's other observability volumes.
- Keep current with a platform and a credential program that both move quarterly.
- Extend into the adjacent Grafana tools this volume does not cover.

## Choosing a badge path

| If you… | Take | Gate |
|:---|:---|:---|
| Are new to Grafana Cloud and want breadth | **Technical Practitioner 101** → Trailblazer | Path **+ assessment** |
| Have 101 and want the intermediate curriculum | **Technical Practitioner 201** → Explorer | Path **+ assessment** |
| Want depth in metrics querying | **PromQL Zero to Hero** → Navigator | Path only |
| Want depth in log querying | **LogQL Zero to Hero** → Navigator | Path only |
| Want the conceptual grounding in signals | **Observability Signals Foundations** → Navigator | Path only |
| Design dashboards for others | **Dashboard Design & Visual Storytelling** → Navigator | Path only |

Everything is **free**, so the only cost is time — which makes the sequencing question purely about what you need rather than what you can afford.

**A note on choosing between 101 and 201:** their badge descriptions state nearly identical competencies, differing mainly in that 201 says "real-world" and "operational insight" where 101 says "systems" and "data-informed decisions." The dependable signal is the level wording — 101 is the *introductory* curriculum, 201 the *intermediate-level* one — and beyond that, **compare the learning-path curricula directly** rather than the badge blurbs.

The Navigator badges have a single generic description shared between them, so their content is defined entirely by their path names. They also require **only path completion, no assessment**, which makes them the lower-friction option if you want a credential for a specific skill rather than broad coverage.

## Effort, honestly

The Technical Practitioner 101 path contains **19 items**: seven modules, ten hands-on labs, an assessment, and the badge. Module 1 alone carries four labs — installing Alloy via the Kubernetes Monitoring Helm chart, then collecting metrics, logs, and traces from a Kubernetes cluster — and its lessons must be completed **in order**.

Two calibration points:

1. **"Introductory" describes the Grafana Cloud content, not the prerequisites.** The syllabus assumes you can operate a Kubernetes cluster and are not frightened by a query language. If neither is true, budget considerably more time.
2. **The labs are the substance.** Ten of nineteen items are hands-on. A path skimmed as reading material will not prepare you for the assessment, and more importantly will not teach you the thing.

## Where Grafana sits in the encyclopedia

Grafana is the **visualization and correlation layer** that sits above the other observability volumes:

- [**Prometheus LV**](../../volume-055-prometheus/README.md) — the metrics backend and PromQL's origin. Chapter 04 here is applied PromQL; that volume is the system itself.
- [**OpenTelemetry LIV**](../../volume-054-opentelemetry/README.md) — **instrumentation**, which this volume explicitly does not cover. Chapter 02 begins where OpenTelemetry ends.
- [**LibreNMS LIII**](../../volume-053-librenms/README.md) — network-device monitoring, a different sampling model.
- [**Datadog XC**](../../volume-090-datadog-certifications/README.md) — the commercial SaaS alternative that owns its data, in contrast to Grafana's query-where-it-lives model.
- [**Splunk XLV**](../../volume-045-splunk-certifications/README.md) and [**Elastic LXXXVI**](../../volume-086-elastic-certifications/README.md) — full-text-indexed log platforms, the architectural opposite of Loki's labels-only index (Chapter 05).
- [**SolarWinds CXXXIV**](../../volume-134-solarwinds-certifications/README.md) — traditional IT-operations monitoring.
- [**Observability and Enterprise Operations XI**](../../volume-011-observability-enterprise-operations/README.md) — the vendor-neutral discipline.

The comparison worth carrying: **Loki and Elasticsearch make opposite bets.** Elasticsearch indexes content for fast arbitrary search at high ingestion cost; Loki indexes only labels for cheap ingestion at the cost of requiring a good stream selector. Neither is wrong — they suit different query patterns and budgets.

## What this volume does not cover

The platform is larger than the 101 curriculum. Adjacent tools worth knowing exist:

| Tool | Purpose |
|:---|:---|
| **Pyroscope** | Continuous profiling — resource attribution *inside* a process |
| **Beyla** | eBPF auto-instrumentation, no code changes |
| **Faro** | Frontend and browser observability |
| **k6** | Load and performance testing (also a workshop topic) |
| **OnCall / IRM** | On-call scheduling, escalation, incident response |
| **Asserts, SLO, Synthetic Monitoring** | Grafana Cloud features |

## Currency

- **The badge catalog expands quarterly.** Grafana states that new GROT Academy badges are expected each quarter, so re-check the catalog rather than assuming this list is complete.
- **A certification tier may be coming.** The program page is titled "Badges & Certifications" while listing only badges, and its own FAQ asks when certifications will be available. Treat any future certification announcement as new information, not as confirmation of today's third-party claims.
- **Ignore third-party "Certified Grafana Associate" material.** No such exam appears in Grafana's catalog. Paying for preparation for a free program is questionable in any case; paying for preparation for a credential that may not exist is worse.
- **The platform ships continuously.** Alloy, Loki, Mimir, and Tempo all move; treat version-specific details as perishable and the concepts as durable.
- **Verified 4 August 2026** from learn.grafana.com (GROT Academy) and grafana.com: the six badges and three tiers, the free-of-charge terms, Credly issuance, the quarterly cadence, and the Technical Practitioner 101 curriculum and its 19 items.

## Hands-On Lab

### Lab 9.1 — Build your GROT Academy plan

**Objective:** Choose a path and set realistic expectations.

```bash
cat > my-grafana-plan.md <<'EOF'
Where I am:     new to Grafana Cloud  /  using it daily  /  designing for others
FREE — all GROT Academy learning content is currently available at no cost.

Broad coverage:  [ ] Technical Practitioner 101  -> Trailblazer badge  (path + ASSESSMENT)
                 [ ] Technical Practitioner 201  -> Explorer badge     (path + ASSESSMENT)
Targeted depth:  [ ] PromQL Zero to Hero         -> Navigator (path only, no assessment)
                 [ ] LogQL Zero to Hero          -> Navigator (path only)
                 [ ] Observability Signals Foundations -> Navigator (path only)
                 [ ] Dashboard Design & Visual Storytelling -> Navigator (path only)

101 effort:      19 items = 7 modules + 10 LABS + assessment + badge
                 lessons must be completed IN ORDER; module 1 alone has 4 labs
Prerequisites:   "introductory" refers to the Grafana Cloud content, NOT to prerequisites.
                 Assumes comfort with Kubernetes and with a time-series query language.
Badges:          issued via Credly; can be made private in Credly settings
Re-check:        new badges expected EACH QUARTER
Do NOT buy:      third-party "Certified Grafana Associate" courses — no such exam in
                 Grafana's own catalog, and the official program is free
EOF
cat my-grafana-plan.md
```

**Expected result:** A plan that distinguishes the assessment-gated badges from the path-only ones, records the 19-item scope, and states the prerequisite reality. The "do not buy" line belongs in writing because the third-party material is well-optimized for search and looks official.

**Negative test:** Treating the 101 path as reading material to skim — ten of its nineteen items are hands-on labs, and the assessment is aligned to the work, not to the prose.

**Rollback:** Keep the plan.

### Lab 9.2 — Self-assess against the curriculum

**Objective:** Find the weak module before starting.

```bash
python3 - <<'EOF'
modules = {
  "Collection: Alloy on Kubernetes (ch02)":   2,
  "Data sources & transformations (ch03)":    3,
  "PromQL (ch04)":                            2,
  "LogQL (ch05)":                             1,
  "Traces & correlation (ch06)":              1,
  "Dashboards & Golden Signals (ch07)":       4,
  "Recording rules, alerting, SLOs (ch08)":   2,
}
print("Self-rated confidence (0-5):\n")
for m, s in sorted(modules.items(), key=lambda kv: kv[1]):
    print(f"{m:44} [{'#'*s}{'.'*(5-s)}] {'STUDY FIRST' if s <= 2 else ('review' if s < 4 else 'ready')}")

paths = {
  "Technical Practitioner 101": ["ch02","ch03","ch04","ch05","ch06","ch07","ch08"],
  "PromQL Zero to Hero":        ["ch04"],
  "LogQL Zero to Hero":         ["ch05"],
  "Observability Signals":      ["ch06"],
  "Dashboard Design":           ["ch07"],
}
print("\nChapter coverage per path:")
for p, chs in paths.items():
    print(f"  {p:28} {', '.join(chs)}")
print("\nThis profile is dashboard-strong and weak on LogQL and tracing.")
print("Two sensible routes:")
print("  - targeted: LogQL Zero to Hero, then Observability Signals — two Navigator badges,")
print("    no assessment, addressing exactly the gaps")
print("  - broad:    Technical Practitioner 101 — covers everything, but the assessment will")
print("    test the weak areas too, so do the targeted paths first")
EOF
```

**Expected result:** The profile shows dashboards strong and LogQL/tracing weak, with two defensible routes. The advice to take the targeted Navigator paths *before* the assessment-gated 101 is the useful sequencing insight — the Navigator badges have no assessment, so they are a low-risk way to close gaps that 101's assessment would otherwise expose.

**Negative test:** Starting 101 with two weak modules — the labs and assessment cover the full curriculum, so the weak areas simply arrive later with a deadline attached.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A badge path chosen, with assessment-gated and path-only badges distinguished.
- [ ] The 101 path's 19 items and lab-heavy composition understood.
- [ ] "Introductory" calibrated against the real prerequisites.
- [ ] Grafana placed against Prometheus, OpenTelemetry, Datadog, Splunk, Elastic, and LibreNMS.
- [ ] Quarterly badge cadence noted, and third-party certification claims rejected.
