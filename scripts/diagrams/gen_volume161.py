#!/usr/bin/env python3
"""Volume CLXI (Qlik) program map.

Chapter 1: the two-tier Qlik program (fundamental Qualifications vs expert
Certifications QSBA/QSDA/QSSA 50Q/90min/62%) over the Qlik Sense / Qlik Cloud
platform and the Associative Engine (green/white/gray, the power of gray).

Run from scripts/diagrams:  python3 gen_volume161.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-161-qlik-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Qlik Certification Tracks",
        subtitle="Two tiers: fundamental QUALIFICATIONS + expert CERTIFICATIONS (QSBA/QSDA/QSSA 50Q/90min/62%) · Associative Engine",
        svg_title="Chapter 1 program map: the Qlik Qualifications and Certifications over the associative platform",
        svg_desc="Qlik offers a two-tier credential structure. Fundamental-level Qualifications include the Data "
                 "Literacy Qualification, a non-technical product-agnostic exam of thirty questions in one hour; "
                 "the Qlik Sense Business Analyst Qualification, which requires building a Qlik Sense app plus a "
                 "multiple-choice exam; and the Qlik Sense Data Architect Qualification. Expert-level "
                 "Certifications include the Qlik Sense Business Analyst and Data Architect, each fifty questions "
                 "in ninety minutes at sixty-two percent to pass and platform-neutral across client-managed and "
                 "Qlik Cloud, and the Qlik Sense System Administrator. The platform beneath is Qlik Sense and "
                 "Qlik Cloud, built on the Associative Engine: an in-memory associative model where one "
                 "selection instantly recolors every visualization green for selected, white for associated, "
                 "and gray for excluded, so users see not only what is related but what is not, the power of "
                 "gray, unlike query-based tools. The Data Architect builds the model in the Data Load Editor "
                 "avoiding synthetic keys; the Business Analyst builds visualizations and uses set analysis; "
                 "the System Administrator governs via the Qlik Management Console with streams and security "
                 "rules. Qlik is the associative-analytics peer of Tableau.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("QLIK — associative ANALYTICS / BI (Qlik Sense · Qlik Cloud) · the peer of Tableau (CLIV)", 10, 700, "#111827"),
        Line("★ ASSOCIATIVE ENGINE: explore data FREELY in any direction + see what's NOT related (the power of GRAY) — vs query-based tools", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 430, 68, "neutral", [
        Line("QUALIFICATIONS (fundamental — 'NOT expert-level')", 8.2, 700, "#111827"),
        Line("Data Literacy (30Q/1hr, product-agnostic)", 7.2, 400, "#374151"),
        Line("QS Business Analyst Qual (build app + MCQ)", 7.2, 400, "#374151"),
        Line("QS Data Architect Qual (build app + MCQ)", 7.2, 400, "#374151"),
    ])
    c.node_box(490, 120, 430, 68, "data", [
        Line("CERTIFICATIONS (EXPERT-level)", 8.2, 700, "#111827"),
        Line("QS Business Analyst (QSBA) — 50Q/90min/62%", 7.2, 400, "#374151"),
        Line("QS Data Architect (QSDA) — 50Q/90min/62%", 7.2, 400, "#374151"),
        Line("QS System Administrator (QSSA) · PLATFORM-NEUTRAL", 7.2, 400, "#374151"),
    ])

    # roles
    c.node_box(40, 202, 288, 46, "alt", [
        Line("DATA ARCHITECT (QSDA)", 8.0, 700, "#111827"),
        Line("Data Load Editor · associations by same-named", 6.9, 400, "#374151"),
    ])
    c.node_box(336, 202, 288, 46, "alt", [
        Line("BUSINESS ANALYST (QSBA)", 8.0, 700, "#111827"),
        Line("apps/sheets/viz · selections · stories", 6.9, 400, "#374151"),
    ])
    c.node_box(632, 202, 288, 46, "alt", [
        Line("SYSTEM ADMIN (QSSA)", 8.0, 700, "#111827"),
        Line("QMC · streams/spaces · security rules · reloads", 6.7, 400, "#374151"),
    ])
    c.raw('<text x="40" y="272" font-size="8.6" font-weight="700" fill="#166534">★ fields (avoid SYNTHETIC KEYS/loops) · QVD optimized load   |   ★ SET ANALYSIS {&lt;Year={2024}&gt;} = define a data set INDEPENDENT of selections (YoY, this-vs-all) — distinctive + heavily tested   |   master items = governed self-service</text>')

    c.node_box(40, 286, 880, 30, "mgmt", [
        Line("DATA LITERACY (the product-agnostic Qualification — read/analyze/communicate) + AI: Insight Advisor (augmented/NL) → AutoML (no-code ML) → Qlik Answers (GenAI) · Qlik Talend integration (Talend acq. 2023)", 7.2, 700, "#111827"),
    ])

    c.raw('<text x="40" y="342" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: two-tier program + platform-neutral roles · associative green/white/GRAY + the power of gray · app structure + master items · associations + synthetic-key pitfall + QVD · right-chart + selection-driven analysis ·</text>')
    c.raw('<text x="40" y="359" font-size="9.5" font-weight="400" fill="#374151">'
          'set analysis (selection-independent sets, YoY) · QMC streams/security-rules/reloads · data-literacy reading + descriptive→predictive→generative AI. Data cluster: Tableau (CLIV) peer, Snowflake (XLIX)/Databricks (XLVIII)/Cloudera (CLVIII) sources.</text>')

    c.legend(40, 388, [
        ("neutral", "Qualifications"),
        ("data", "Certifications"),
        ("alt", "Roles (BA/DA/SA)"),
        ("mgmt", "Associative platform + AI"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
