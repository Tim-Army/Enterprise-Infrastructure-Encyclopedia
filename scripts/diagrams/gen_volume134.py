#!/usr/bin/env python3
"""Volume CXXXIV (SolarWinds Certification Tracks) program map.

Chapter 1: the SolarWinds Certified Professional (SCP) program — product-
specific rather than tiered. Eleven exams across the rebranded portfolio
(Observability SaaS vs Self-Hosted, the Orion lineage), three steps
(sign up, study, schedule), PSI Services remote proctoring, US$200 or
60,000 THWACK community points.

Run from scripts/diagrams:  python3 gen_volume134.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-134-solarwinds-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: SolarWinds Certified Professional (SCP)",
        subtitle="Product-specific, not tiered — 11 exams across Observability SaaS and Self-Hosted; PSI remote proctoring; US$200 or 60,000 THWACK points",
        svg_title="Chapter 1 program map: the SolarWinds Certified Professional certification program",
        svg_desc="The SolarWinds Certified Professional program awards one credential, SCP, earned by passing a "
                 "product-specific exam rather than by climbing a tiered ladder. The process has three steps: sign "
                 "up by registering with SolarWinds, study using that exam's preparation guide plus virtual and "
                 "on-demand training through the Customer Portal for customers with a product under active "
                 "maintenance, and schedule through PSI Services proprietary remote proctoring. The fee is 200 US "
                 "dollars, or 60,000 THWACK community points exchanged in the THWACK store for an SCP voucher "
                 "delivered by email within three business days. The portfolio has been rebranded around SolarWinds "
                 "Observability and split into SaaS and Self-Hosted editions, Self-Hosted being the on-premises "
                 "Orion lineage. Eleven exams are current: Observability SaaS Fundamentals; Observability "
                 "Self-Hosted Fundamentals, Network Monitoring, Network Management, Architecture and Design, "
                 "Diagnostics and Troubleshooting, and Federal Fundamentals; Server and Application Monitor; "
                 "Database Performance Analyzer; Database Management; and Service Desk. Supporting resources are "
                 "product documentation, virtual classrooms, eLearning videos, and the THWACK community forum; "
                 "SolarWinds notes that third-party training is not reviewed, monitored, or endorsed by them. The "
                 "volume teaches the underlying monitoring disciplines and models them free in Python.")

    c.node_box(230, 42, 500, 44, "mgmt", [
        Line("SolarWinds Certified Professional (SCP)", 10.5, 700, "#111827"),
        Line("one credential, earned per PRODUCT exam — no tiered ladder", 8.5, 400, "#374151"),
    ])

    # three steps
    c.node_box(40, 126, 270, 40, "neutral", [
        Line("1. SIGN UP", 9.5, 700, "#111827"),
        Line("register with SolarWinds", 8, 400, "#374151"),
    ])
    c.node_box(345, 126, 270, 40, "neutral", [
        Line("2. STUDY", 9.5, 700, "#111827"),
        Line("exam prep guide + Customer Portal training", 8, 400, "#374151"),
    ])
    c.node_box(650, 126, 270, 40, "neutral", [
        Line("3. SCHEDULE", 9.5, 700, "#111827"),
        Line("PSI Services — remote proctored", 8, 400, "#374151"),
    ])
    c.connector(310, 146, 345, 146, "neutral", label="", label_pos=(0, 0))
    c.connector(615, 146, 650, 146, "neutral", label="", label_pos=(0, 0))

    # the two product families
    c.node_box(40, 196, 430, 30, "alt", [
        Line("Observability SELF-HOSTED (Orion lineage)", 9, 700, "#111827"),
    ])
    c.node_box(40, 234, 430, 76, "data", [
        Line("Fundamentals · Network Monitoring · Network Management", 8.5, 400, "#374151"),
        Line("Architecture & Design · Diagnostics & Troubleshooting", 8.5, 400, "#374151"),
        Line("Federal Fundamentals (public sector)", 8.5, 400, "#374151"),
        Line("+ Server and Application Monitor", 8.5, 400, "#374151"),
    ])
    c.node_box(500, 196, 420, 30, "alt", [
        Line("Observability SaaS  ·  standalone products", 9, 700, "#111827"),
    ])
    c.node_box(500, 234, 420, 76, "data", [
        Line("Observability SaaS Fundamentals", 8.5, 400, "#374151"),
        Line("Database Performance Analyzer", 8.5, 400, "#374151"),
        Line("Database Management", 8.5, 400, "#374151"),
        Line("Service Desk", 8.5, 400, "#374151"),
    ])

    # cost band
    c.node_box(40, 326, 880, 40, "mgmt", [
        Line("Fee: US$200  —  OR  —  60,000 THWACK community points -> SCP Voucher (3 business days): the exam is effectively free for active contributors", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="404" font-size="9.5" font-weight="700" fill="#991b1b">'
          'Use the official prep guide: SolarWinds states third-party training is "not reviewed, monitored, or endorsed" — and the search results are full of braindumps for RETIRED exams</text>')
    c.raw('<text x="40" y="423" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: polling &amp; collection · availability + error budgets · errors vs utilization · config drift · wait-time analysis · alert suppression · percentiles · capacity runway</text>')

    c.legend(40, 454, [
        ("neutral", "The three steps"),
        ("alt", "Product family"),
        ("data", "Exams"),
        ("mgmt", "Program facts"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
