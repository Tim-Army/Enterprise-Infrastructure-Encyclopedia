#!/usr/bin/env python3
"""Volume CXXXIX (Grafana Observability Platform and GROT Academy) map.

Chapter 1: the LGTM stack and its surrounding components, the three
delivery models (OSS / Cloud / Enterprise), and the GROT Academy badge
program — six free badges in three tiers, two assessment-gated and four
path-only, issued via Credly with a quarterly cadence.

Run from scripts/diagrams:  python3 gen_volume139.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-139-grafana-observability"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Platform & Program Map: Grafana and GROT Academy",
        subtitle="LGTM stack · queries data where it lives · 6 FREE badges in 3 tiers · Credly · new badges each quarter",
        svg_title="Chapter 1 map: the Grafana observability platform and the GROT Academy badge program",
        svg_desc="Grafana's defining architectural choice is that it queries data where it lives rather than "
                 "owning a store, so a single dashboard can span many backends. The open-source LGTM stack is "
                 "Loki for logs, Grafana for visualization, Tempo for traces, and Mimir for long-term metrics, "
                 "with Pyroscope for continuous profiling. Surrounding components include Alloy, the "
                 "OpenTelemetry-native collector, Beyla for eBPF auto-instrumentation, Faro for frontend "
                 "observability, k6 for load testing, and OnCall or IRM for incident response. The platform is "
                 "delivered three ways: Grafana OSS, which you run yourself; Grafana Cloud, the managed service "
                 "with a free tier; and the Enterprise Stack, which is self-managed with commercial support and "
                 "additional data source plugins. The credential program is GROT Academy at learn dot grafana "
                 "dot com, and it currently awards free digital badges rather than paid certifications. There "
                 "are six badges in three tiers. Trailblazer is awarded for the introductory Technical "
                 "Practitioner 101 learning path and Explorer for the intermediate-level Technical Practitioner "
                 "201 path; both require a completed learning path AND a passed aligned assessment. Four "
                 "Navigator badges cover PromQL Zero to Hero, LogQL Zero to Hero, Observability Signals "
                 "Foundations, and Dashboard Design and Visual Storytelling; these require only path completion, "
                 "with no assessment. All GROT Academy learning content is currently available at no cost, "
                 "badges issue through Credly and can be made private in Credly's own settings, and Grafana "
                 "states that new badges are expected to launch each quarter. The Technical Practitioner 101 "
                 "path contains nineteen items: seven modules, ten hands-on labs, the assessment, and the badge, "
                 "with lessons to be completed in order. No paid Certified Grafana Associate exam appears in "
                 "Grafana's own catalog, so third-party courses advertising one should be treated with caution.")

    c.node_box(180, 42, 600, 44, "mgmt", [
        Line("GRAFANA — queries data WHERE IT LIVES (it does not own a store)", 10.5, 700, "#111827"),
        Line("one dashboard spans metrics + logs + traces + profiles + ordinary SQL", 8.5, 400, "#374151"),
    ])

    # LGTM stack
    c.node_box(40, 124, 200, 66, "data", [
        Line("METRICS", 9.5, 700, "#111827"),
        Line("Mimir — long-term store", 8, 400, "#374151"),
        Line("Prometheus-compatible", 7.5, 400, "#374151"),
        Line("query: PromQL  (ch04)", 7.5, 700, "#166534"),
    ])
    c.node_box(250, 124, 200, 66, "data", [
        Line("LOGS", 9.5, 700, "#111827"),
        Line("Loki — LABELS-ONLY index", 8, 400, "#374151"),
        Line("cheap ingest, needs a selector", 7, 400, "#374151"),
        Line("query: LogQL  (ch05)", 7.5, 700, "#166534"),
    ])
    c.node_box(460, 124, 200, 66, "data", [
        Line("TRACES", 9.5, 700, "#111827"),
        Line("Tempo — one request's path", 8, 400, "#374151"),
        Line("read by SELF TIME, not total", 7, 400, "#374151"),
        Line("correlate: exemplars  (ch06)", 7.5, 700, "#166534"),
    ])
    c.node_box(670, 124, 250, 66, "neutral", [
        Line("PROFILES", 9.5, 700, "#111827"),
        Line("Pyroscope — inside a process", 8, 400, "#374151"),
        Line("Alloy collects · Beyla (eBPF)", 7.5, 400, "#374151"),
        Line("Faro (frontend) · k6 · OnCall", 7.5, 400, "#374151"),
    ])

    # delivery models
    c.node_box(40, 212, 880, 40, "mgmt", [
        Line("Delivery: GRAFANA OSS (self-run, free) · GRAFANA CLOUD (managed, free tier) · ENTERPRISE STACK (self-managed + support and extra plugins)", 8.5, 400, "#374151"),
    ])

    # academy
    c.node_box(40, 276, 880, 34, "alt", [
        Line("GROT ACADEMY (learn.grafana.com) — FREE digital BADGES, not paid certifications · issued via Credly · new badges expected EACH QUARTER", 9, 700, "#111827"),
    ])

    c.node_box(40, 330, 285, 70, "alt", [
        Line("TRAILBLAZER  ·  introductory", 9.5, 700, "#111827"),
        Line("Technical Practitioner 101", 8.5, 400, "#374151"),
        Line("learning path + PASSED ASSESSMENT", 8, 700, "#166534"),
        Line("19 items = 7 modules + 10 LABS + assessment", 7, 400, "#374151"),
    ])
    c.node_box(335, 330, 285, 70, "alt", [
        Line("EXPLORER  ·  intermediate-level", 9.5, 700, "#111827"),
        Line("Technical Practitioner 201", 8.5, 400, "#374151"),
        Line("learning path + PASSED ASSESSMENT", 8, 700, "#166534"),
        Line("blurbs nearly identical to 101 — compare curricula", 6.5, 400, "#374151"),
    ])
    c.node_box(630, 330, 290, 70, "neutral", [
        Line("NAVIGATOR  ·  four targeted badges", 9.5, 700, "#111827"),
        Line("PromQL Zero to Hero · LogQL Zero to Hero", 7.5, 400, "#374151"),
        Line("Observability Signals Foundations", 7.5, 400, "#374151"),
        Line("Dashboard Design — PATH ONLY, NO ASSESSMENT", 7.5, 700, "#166534"),
    ])
    c.connector(325, 365, 335, 365, "alt", label="", label_pos=(0, 0))

    c.raw('<text x="40" y="432" font-size="9.5" font-weight="700" fill="#166534">'
          'Everything is free, so sequencing is about what you need, not what you can afford — and the Navigator badges close gaps with no assessment risk.</text>')
    c.raw('<text x="40" y="451" font-size="9.5" font-weight="400" fill="#374151">'
          '"Introductory" describes the Grafana Cloud content, NOT the prerequisites: 101 assumes you can operate Kubernetes and are not frightened by a query language.</text>')
    c.raw('<text x="40" y="470" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'No paid "Certified Grafana Associate" exam appears in Grafana\'s catalog — treat third-party courses selling one with caution.</text>')

    c.legend(40, 500, [
        ("data", "Signal backends"),
        ("neutral", "Adjacent tools / path-only"),
        ("alt", "Academy & gated badges"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-platform-and-academy.svg")


if __name__ == "__main__":
    ch01()
