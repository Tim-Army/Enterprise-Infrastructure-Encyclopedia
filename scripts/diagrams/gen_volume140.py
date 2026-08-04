#!/usr/bin/env python3
"""Volume CXL (Dynatrace) certification program + platform map.

Chapter 1: the 34-badge Credly catalog split into the practitioner ladder
(Beginner/Essentials -> Associate -> Professional tier -> Master), the four
Intermediate Specialist certifications, and the much larger partner/services
and internal groups -- over the platform spine of OneAgent, ActiveGate, Grail,
DQL/DPL, and Davis AI. Exam mechanics are NOT published: Dynatrace University
requires a sign-in.

Run from scripts/diagrams:  python3 gen_volume140.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-140-dynatrace-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Dynatrace Certification Tracks",
        subtitle="34 Credly badges - only ~11 are practitioner certs · exam mechanics NOT published (University is sign-in gated)",
        svg_title="Chapter 1 program map: the Dynatrace certification catalog and the platform beneath it",
        svg_desc="Dynatrace publishes thirty-four badges through Credly, but only about eleven are "
                 "practitioner certifications. The practitioner ladder begins with two entry credentials: "
                 "Dynatrace Beginner, a course completion, and Dynatrace Essentials, a knowledge-based "
                 "certificate whose own description states it does not measure hands-on ability. Above them "
                 "sits the Dynatrace Associate and the Associate for Managed variant, both labeled "
                 "Intermediate by Dynatrace, covering six domains: capabilities and monitoring, components "
                 "and architecture, digital experience management, installation and configuration, problems "
                 "and resolution, and reporting and analysis. The Professional tier is labeled Advanced and "
                 "holds three credentials: Dynatrace Professional, which adds product extensions to the "
                 "Associate six; Administration Professional, the only credential with a time to earn "
                 "measured in weeks; and Implementation Professional. At the top is Dynatrace Master, also "
                 "Advanced, whose skill list includes live product usage exams, making it partly practical. "
                 "Beside the ladder sit five Specialist certifications at Intermediate level: Advanced "
                 "Observability, DEM and Business Analytics, Advanced Security, Advanced Automation, and "
                 "Application Development. A separate and larger group covers partner and services badges "
                 "including Partner Sales, the free Partner Sales Engineer, ACE Services, three Services "
                 "Delivery certifications, and the Endorsed Services Partner accreditation; a further group "
                 "covers internal Dynatrace leadership programs that customers cannot earn. The platform "
                 "beneath consists of OneAgent for automatic instrumentation, ActiveGate for routing and "
                 "remote monitoring, Grail as a schema-on-read data lakehouse organized in buckets, tables, "
                 "and views, queried with DQL and DPL, and Davis AI performing deterministic causation-based "
                 "root cause analysis over the topology. Exam fee, duration, question count, passing score, "
                 "and validity period are not published publicly because Dynatrace University requires a "
                 "sign-in; the per-badge skill lists serve as the blueprint instead.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("DYNATRACE — automation over assembly: one agent discovers, models, and diagnoses", 10.5, 700, "#111827"),
        Line("the opposite end of the axis from Grafana's query-data-where-it-lives composability (Vol CXXXIX)", 8, 400, "#374151"),
    ])

    # ladder
    c.node_box(40, 122, 180, 60, "neutral", [
        Line("ENTRY", 9.5, 700, "#111827"),
        Line("Beginner (course)", 8, 400, "#374151"),
        Line("Essentials", 8, 400, "#374151"),
        Line("NOT hands-on", 7.5, 700, "#b91c1c"),
    ])
    c.node_box(232, 122, 200, 60, "data", [
        Line("ASSOCIATE", 9.5, 700, "#111827"),
        Line("+ Associate for Managed", 7.5, 400, "#374151"),
        Line("6 domains", 7.5, 400, "#374151"),
        Line("label: INTERMEDIATE", 8, 700, "#b91c1c"),
    ])
    c.node_box(444, 122, 240, 60, "data", [
        Line("PROFESSIONAL   label: ADVANCED", 9, 700, "#111827"),
        Line("Professional (6 + Product Extensions)", 7, 400, "#374151"),
        Line("Administration Prof. — time: WEEKS", 7, 400, "#374151"),
        Line("Implementation Professional", 7, 400, "#374151"),
    ])
    c.node_box(696, 122, 224, 60, "alt", [
        Line("MASTER   label: ADVANCED", 9, 700, "#111827"),
        Line("entire platform: design,", 7.5, 400, "#374151"),
        Line("execution, troubleshooting", 7.5, 400, "#374151"),
        Line("LIVE PRODUCT USAGE EXAMS", 7.5, 700, "#166534"),
    ])
    c.connector(220, 152, 232, 152, "data", label="", label_pos=(0, 0))
    c.connector(432, 152, 444, 152, "data", label="", label_pos=(0, 0))
    c.connector(684, 152, 696, 152, "alt", label="", label_pos=(0, 0))

    # specialists
    c.node_box(40, 202, 880, 54, "data", [
        Line("SPECIALIST CERTIFICATIONS — all label: INTERMEDIATE · beside the ladder, not above it · best value for most working engineers", 8.5, 700, "#111827"),
        Line("Advanced Observability (OneAgent · Grail · DQL/DPL)   ·   DEM & Business Analytics (RUM · Session Replay · USQL)", 7.5, 400, "#374151"),
        Line("Advanced Security (runtime vulns · attack detection)   ·   Advanced Automation (workflows · SRG · SLOs)   ·   Application Development (AppEngine)", 7.5, 400, "#374151"),
    ])

    # non-practitioner
    c.node_box(40, 272, 430, 46, "neutral", [
        Line("PARTNER / SERVICES  (~15 badges — partner org only)", 8.5, 700, "#111827"),
        Line("Partner Sales · Sales Specialist · Sales Engineer (FREE)", 7, 400, "#374151"),
        Line("ACE Services · 3× Services Delivery · Endorsed Services Partner", 7, 400, "#374151"),
    ])
    c.node_box(490, 272, 430, 46, "neutral", [
        Line("INTERNAL DYNATRACE  (~4 badges — NOT earnable)", 8.5, 700, "#111827"),
        Line("RD / RVP / Future Leaders Excellence · Customer Success", 7, 400, "#374151"),
        Line("a search for \"Dynatrace certification\" returns all 34 at once", 7, 400, "#b91c1c"),
    ])

    # platform spine
    c.node_box(40, 336, 880, 56, "mgmt", [
        Line("PLATFORM SPINE", 8.5, 700, "#111827"),
        Line("OneAgent (auto-instrumentation — gaps are SILENT)  ·  ActiveGate (routing · remote monitoring · private synthetics · segmented egress)", 7.5, 400, "#374151"),
        Line("Grail (SCHEMA-ON-READ lakehouse: buckets/tables/views) → DQL + DPL  ·  Davis AI (DETERMINISTIC, CAUSATION-BASED over topology)", 7.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="422" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'NOT PUBLISHED: exam fee · duration · question count · passing score · validity — Dynatrace University requires a sign-in. This volume does not assert them.</text>')
    c.raw('<text x="40" y="441" font-size="9.5" font-weight="700" fill="#166534">'
          'PUBLISHED (Credly issuer catalog): credential names · level labels · Paid/Free · time-to-earn · per-badge SKILL LISTS — which serve as the blueprint.</text>')
    c.raw('<text x="40" y="460" font-size="9.5" font-weight="400" fill="#374151">'
          'Read the LEVEL LABEL, not the credential name: "Associate" is Intermediate. Same trap as Grafana\'s "introductory" 101 (Vol CXXXIX).</text>')
    c.raw('<text x="40" y="479" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: inventory reconciliation · ActiveGate sizing · DQL stage-order cost · topology gaps vs root cause · RUM/synthetic blind spots · masking · runtime-vs-CVSS risk · SRG severity.</text>')

    c.legend(40, 512, [
        ("neutral", "Entry / non-practitioner"),
        ("data", "Associate / Prof / Specialist"),
        ("alt", "Master"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
