#!/usr/bin/env python3
"""Volume CLXV (Informatica) program map.

Chapter 1: the Informatica Certified Professional Program (Professional + Practitioner
tiers; 70%/90min, course-backed, release-dated) over IDMC — the Intelligent Data
Management Cloud — a modular platform (CDI, CAI, Data Quality, MDM, CDGC) plus legacy
PowerCenter, sharing one metadata fabric reasoned over by CLAIRE, the AI engine.

Run from scripts/diagrams:  python3 gen_volume165.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-165-informatica-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Informatica Certification Tracks",
        subtitle="Certified Professional + Practitioner over IDMC — CDI · CAI · Data Quality · MDM · CDGC + PowerCenter · CLAIRE AI",
        svg_title="Chapter 1 program map: the Informatica certification tracks over the IDMC data-management platform",
        svg_desc="Informatica is the enterprise data-management leader. Certifications come in two tiers: "
                 "Certified Professional, the mainstream role-based credential validating product knowledge "
                 "(exams are seventy percent to pass, ninety minutes, backed by a matching training course, and "
                 "release-dated), and Certified Practitioner, an implementation-focused credential with a two-year "
                 "validity for delivering customer projects, including the PowerCenter-to-CDI modernization "
                 "specialization. The credentials map to the modules of IDMC, the Intelligent Data Management "
                 "Cloud: Cloud Data Integration for batch ETL and ELT mappings, Cloud Application Integration for "
                 "real-time API and process integration, Cloud Data Quality for profiling, cleansing and "
                 "standardization, Master Data Management for golden records, and Cloud Data Governance and Catalog "
                 "for metadata, lineage and governance. The legacy on-premises engine is PowerCenter, modernized "
                 "to Cloud Data Integration. All modules share one metadata fabric that CLAIRE, Informatica's AI "
                 "engine, reasons over to automate data-management work. The life cycle is integrate, trust, "
                 "master, and govern — turning scattered source data into trustworthy governed data.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("INFORMATICA — enterprise DATA-MANAGEMENT leader: integrate · trust · master · govern · catalog", 9.5, 700, "#111827"),
        Line("IDMC (Intelligent Data Management Cloud): modular platform · ONE metadata fabric · CLAIRE AI engine · legacy PowerCenter on-prem", 7.6, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("INFORMATICA CERTIFIED PROFESSIONAL PROGRAM — two tiers, by module", 8.3, 700, "#111827"),
        Line("CERTIFIED PROFESSIONAL (role-based; 70% to pass · 90 min · course-backed · release-dated)   |   CERTIFIED PRACTITIONER (implementation; 2-year validity; incl. PC→CDI modernization)", 6.4, 400, "#374151"),
    ])

    # platform modules
    c.node_box(40, 176, 288, 46, "data", [
        Line("CLOUD DATA INTEGRATION (CDI) — core", 7.6, 700, "#111827"),
        Line("batch ETL/ELT: source→transforms→target · Cloud Mapping Designer", 6.0, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("CLOUD APPLICATION INTEGRATION (CAI)", 7.4, 700, "#111827"),
        Line("real-time / API / process orchestration · service connectors · events", 5.9, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("CLOUD DATA QUALITY", 7.8, 700, "#111827"),
        Line("profile → cleanse → standardize → validate → score → monitor", 6.0, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 46, "alt", [
        Line("MASTER DATA MANAGEMENT (MDM)", 7.6, 700, "#111827"),
        Line("match → merge (survivorship) → golden record · Dev/Admin/SaaS", 5.9, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 46, "alt", [
        Line("DATA GOVERNANCE & CATALOG (CDGC)", 7.4, 700, "#111827"),
        Line("catalog · lineage · glossary · CLAIRE auto-classifies PII", 6.0, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 46, "alt", [
        Line("POWERCENTER → CLOUD (modernization)", 7.2, 700, "#111827"),
        Line("legacy on-prem ETL (mapping/session/workflow) → CDI-PC 'PC to CDI'", 5.7, 400, "#374151"),
    ])

    c.raw('<text x="40" y="308" font-size="9.5" font-weight="700" fill="#166534">'
          'INTEGRATE (CDI/CAI) + TRUST (Data Quality) + MASTER (MDM golden record) + GOVERN (catalog/lineage/CLAIRE) — one platform over one metadata fabric.</text>')
    c.raw('<text x="40" y="330" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: tiers + module map · IDMC modules + control-plane/Secure-Agent split · CDI mapping (source→transforms→target) as a task · PC→CDI object correspondence + wave migration ·</text>')
    c.raw('<text x="40" y="347" font-size="9.5" font-weight="400" fill="#374151">'
          'CAI real-time process + service connectors · profile/cleanse/validate/score · match+survivorship golden record · catalog/lineage/CLAIRE PII. Peers: Snowflake (XLIX), Databricks (XLVIII), MuleSoft (CLX).</text>')

    c.legend(40, 376, [
        ("data", "Integrate / quality"),
        ("alt", "Master / govern / modernize"),
        ("neutral", "Cert tiers"),
        ("mgmt", "IDMC + CLAIRE"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
