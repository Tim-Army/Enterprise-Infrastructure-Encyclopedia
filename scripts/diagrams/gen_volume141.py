#!/usr/bin/env python3
"""Volume CXLI (New Relic) certification program + platform map.

Chapter 1: the four-certification ladder (NVF free/unproctored -> APA ->
the sibling Professionals PEP and REP), full published mechanics, Webassessor
delivery, four languages -- over the platform spine of MELT telemetry into
NRDB, queried everywhere by NRQL, organized by entities/tags/workloads, and
automated via NerdGraph + Terraform.

Run from scripts/diagrams:  python3 gen_volume141.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-141-newrelic-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: New Relic Certification Tracks",
        subtitle="4 certifications, one ladder · mechanics PUBLIC · NVF free + unproctored · Webassessor · EN/ES/PT/JA",
        svg_title="Chapter 1 program map: the New Relic certification program and the platform beneath it",
        svg_desc="New Relic's certification program is small, public, and cleanly laddered: four "
                 "certifications. The New Relic Verified Foundation, NVF, is free, forty-five minutes, "
                 "multiple choice, online and unproctored, with no prerequisites, recommended for zero to "
                 "six months of experience, and is taken on learn.newrelic.com itself. The Certified APM "
                 "Practitioner Associate, APA, costs one hundred twenty-five dollars, runs fifty minutes, "
                 "is online proctored, and recommends six or more months of experience. Two sibling "
                 "Professional certifications cost one hundred seventy-five dollars each, run sixty "
                 "minutes, are online proctored, and recommend two or more years of experience: the "
                 "Certified Performance Engineer, PEP, covering platform capabilities and data, backend "
                 "application performance, client-side performance, and infrastructure and cloud "
                 "performance; and the Certified Reliability Engineer, REP, covering alerts and incident "
                 "management including alert quality management, service level management with SLIs, SLOs "
                 "and service boundaries, infrastructure, cloud integration and networking, and automation "
                 "of observability fixtures using New Relic APIs and Terraform providers. There is no "
                 "Expert tier, and PEP and REP are siblings rather than a sequence. All exams are multiple "
                 "choice and offered in English, Spanish, Portuguese, and Japanese; the paid exams are "
                 "delivered through Webassessor. Every exam publishes its section-level topics on public "
                 "pages, which serve as the blueprints; question count and passing score sit in per-exam "
                 "Exam Guides behind a free sign-in, and no validity policy appears publicly. The platform "
                 "beneath is the single-store model: agents send metrics, events, logs, and traces, the "
                 "MELT four, into NRDB, and one language, NRQL, queries all of it — dashboards, alert "
                 "conditions, and service levels are all NRQL. Entities, tags, and workloads organize the "
                 "estate, and NerdGraph plus the Terraform provider manage observability as code.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("NEW RELIC — single store (NRDB), one language (NRQL) everywhere", 10.5, 700, "#111827"),
        Line("dashboards, alert conditions, and service levels are ALL NRQL — leverage and risk in one clause", 8, 400, "#374151"),
    ])

    # ladder
    c.node_box(40, 122, 210, 66, "alt", [
        Line("NVF — FOUNDATION", 9.5, 700, "#111827"),
        Line("FREE · 45 min · UNPROCTORED", 7.5, 700, "#166534"),
        Line("no prerequisites · 0-6 months", 7.5, 400, "#374151"),
        Line("taken on learn.newrelic.com", 7, 400, "#374151"),
    ])
    c.node_box(262, 122, 210, 66, "data", [
        Line("APA — ASSOCIATE", 9.5, 700, "#111827"),
        Line("APM Practitioner", 8, 400, "#374151"),
        Line("$125 · 50 min · proctored", 7.5, 400, "#374151"),
        Line("6+ months experience", 7.5, 400, "#374151"),
    ])
    c.node_box(484, 122, 212, 66, "data", [
        Line("PEP — PROFESSIONAL", 9.5, 700, "#111827"),
        Line("Performance Engineer", 8, 400, "#374151"),
        Line("$175 · 60 min · proctored · 2+ yrs", 7, 400, "#374151"),
        Line("backend · client-side · infra perf", 7, 400, "#374151"),
    ])
    c.node_box(708, 122, 212, 66, "data", [
        Line("REP — PROFESSIONAL", 9.5, 700, "#111827"),
        Line("Reliability Engineer", 8, 400, "#374151"),
        Line("$175 · 60 min · proctored · 2+ yrs", 7, 400, "#374151"),
        Line("alerts · SLOs · automation", 7, 400, "#374151"),
    ])
    c.connector(250, 155, 262, 155, "data", label="", label_pos=(0, 0))
    c.connector(472, 155, 484, 155, "data", label="", label_pos=(0, 0))
    c.connector(696, 155, 708, 155, "data", label="", label_pos=(0, 0))

    c.node_box(40, 208, 880, 34, "neutral", [
        Line("PEP and REP are SIBLINGS, not a sequence — same level, same price; choose by calendar shape · NO EXPERT TIER exists", 8.5, 700, "#111827"),
    ])

    # mechanics band
    c.node_box(40, 262, 880, 40, "alt", [
        Line("PUBLISHED OPENLY: cost · duration · format (multiple choice) · proctoring · languages (EN/ES/PT/JA) · experience bands · SECTION-LEVEL EXAM TOPICS", 8, 700, "#111827"),
        Line("behind FREE sign-in (Exam Guides): question count · passing score  ·  NOT found publicly: validity/expiration · retake policy — this volume asserts neither", 7.5, 400, "#b91c1c"),
    ])

    # platform spine
    c.node_box(40, 322, 880, 56, "mgmt", [
        Line("PLATFORM SPINE", 8.5, 700, "#111827"),
        Line("agents (APM per-language · infrastructure + on-host integrations · browser · mobile) + OpenTelemetry ingest → MELT into NRDB", 7.5, 400, "#374151"),
        Line("NRQL (SELECT/FROM/WHERE/FACET/SINCE/TIMESERIES) · entities + tags + workloads · alerts (policy→condition→incident→workflow) · SLIs/SLOs · NerdGraph + Terraform", 7, 400, "#374151"),
    ])

    c.raw('<text x="40" y="408" font-size="9.5" font-weight="700" fill="#166534">'
          'The disclosure mirror image of Dynatrace (Vol CXL): 4 public certifications with a mechanics table, vs 34 badges behind a University sign-in.</text>')
    c.raw('<text x="40" y="427" font-size="9.5" font-weight="400" fill="#374151">'
          'Registration: paid exams via webassessor.com/newrelic · the free NVF moved onto learn.newrelic.com itself · official prep courses and program guide are free.</text>')
    c.raw('<text x="40" y="446" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: MELT routing · workloads-as-verdicts · NRQL clause cost + the shared-WHERE risk · Apdex blind spots · db total-time ranking · Core Web Vitals at p75 ·</text>')
    c.raw('<text x="40" y="463" font-size="9.5" font-weight="400" fill="#374151">'
          'journey synthetics · agent-tuning ledger · K8s workload aggregation · network-app MTTR correlation · alert-quality audit · boundary SLOs + compounding · fixture drift detection.</text>')

    c.legend(40, 496, [
        ("alt", "Free tier / published facts"),
        ("data", "Paid certifications"),
        ("neutral", "Program structure"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
