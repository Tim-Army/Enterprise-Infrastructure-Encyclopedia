#!/usr/bin/env python3
"""Volume CLIV (Tableau) certification-program map.

Chapter 1: the three-step Tableau certification track (Desktop Specialist ->
Salesforce Certified Data Analyst -> Certified Architect) over the
connect-prepare-visualize-share platform. Salesforce-owned. Desktop Specialist
45Q/60min/750/$75; Data Analyst 40-45Q + hands-on labs/120min.

Run from scripts/diagrams:  python3 gen_volume154.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-154-tableau-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Tableau Certification Tracks",
        subtitle="3-step track (Desktop Specialist -> Data Analyst -> Architect) · Salesforce-owned · connect-prepare-visualize-share",
        svg_title="Chapter 1 program map: the three-step Tableau certification track over the platform",
        svg_desc="Tableau, owned by Salesforce, offers a three-step certification track. The Tableau Desktop "
                 "Specialist, also called Desktop Foundations, is the entry-level credential: a proctored "
                 "exam of forty-five questions in sixty minutes with a passing score of seven hundred fifty, "
                 "priced around seventy-five dollars, validating connecting to and preparing data and "
                 "building basic visualizations. The Salesforce Certified Tableau Data Analyst is the "
                 "mid-level, most recognized credential: forty to forty-five questions plus eight to ten "
                 "hands-on labs in one hundred twenty minutes, validating data visualization and analysis "
                 "proficiency. The Salesforce Certified Tableau Architect is the advanced credential for "
                 "enterprise deployment, Server and Cloud architecture, and governance. The recommended "
                 "progression runs Desktop Specialist to Certified Data Analyst to Certified Architect. The "
                 "platform beneath follows a connect, prepare, visualize, share workflow: connect to data "
                 "live or by extract; prepare and model with joins, relationships, and Tableau Prep; build "
                 "visualizations with the VizQL engine, choosing the right chart for the question and adding "
                 "calculated fields, level-of-detail expressions, and table calculations; assemble "
                 "interactive dashboards and stories with actions; and publish to Tableau Server or Cloud "
                 "with permissions and certified data sources as a single source of truth, increasingly "
                 "augmented by AI through Tableau Pulse. Tableau is the visualization and analytics layer on "
                 "top of the data platforms, where data becomes decisions.")

    c.node_box(160, 42, 640, 44, "mgmt", [
        Line("TABLEAU (Salesforce) — data VISUALIZATION + BI: 'see and understand your data'", 10.5, 700, "#111827"),
        Line("the human-facing analytics layer on the data platforms (Snowflake XLIX, Databricks XLVIII) — where data becomes DECISIONS", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 26, "neutral", [
        Line("3-STEP TRACK — USING -> ANALYZING -> ARCHITECTING · Salesforce-owned (2019) · mechanics PUBLISHED", 8.5, 700, "#111827"),
    ])

    # certs
    c.node_box(40, 152, 280, 58, "data", [
        Line("Desktop SPECIALIST", 8.8, 700, "#111827"),
        Line("entry — connect + prepare + basic viz", 7.2, 400, "#374151"),
        Line("45Q / 60min / 750 / ~$75 / proctored", 7.2, 700, "#166534"),
    ])
    c.node_box(340, 152, 280, 58, "data", [
        Line("Certified DATA ANALYST", 8.8, 700, "#111827"),
        Line("mid — viz + analysis (most recognized)", 7.2, 400, "#374151"),
        Line("40-45Q + 8-10 HANDS-ON LABS / 120min", 7.2, 700, "#166534"),
    ])
    c.node_box(640, 152, 280, 58, "alt", [
        Line("Certified ARCHITECT", 8.8, 700, "#111827"),
        Line("advanced — enterprise deploy,", 7.2, 400, "#374151"),
        Line("Server/Cloud, governance", 7.2, 400, "#374151"),
    ])
    c.connector(320, 181, 340, 181, "data", label="", label_pos=(0, 0))
    c.connector(620, 181, 640, 181, "data", label="", label_pos=(0, 0))

    # workflow
    c.node_box(40, 224, 880, 56, "mgmt", [
        Line("PLATFORM WORKFLOW: CONNECT -> PREPARE -> VISUALIZE -> SHARE", 8.5, 700, "#111827"),
        Line("CONNECT (live vs EXTRACT/.hyper) · PREPARE (joins/blends/RELATIONSHIPS, Tableau Prep) · VISUALIZE (VizQL; dimensions vs measures; discrete BLUE vs continuous GREEN; right chart)", 7.1, 400, "#374151"),
        Line("CALCULATIONS (calculated fields, ★ LOD FIXED/INCLUDE/EXCLUDE, table calcs) · DASHBOARDS + actions + stories · SHARE (Server/Cloud, permissions, CERTIFIED data sources) · AI (Pulse)", 7.1, 400, "#374151"),
    ])

    c.raw('<text x="40" y="306" font-size="9.5" font-weight="700" fill="#166534">'
          'Core grammar: a viz = MEASURES aggregated BY DIMENSIONS. Blue = discrete (headers), Green = continuous (axis) — independent of dimension/measure (the most-confused, most-tested concept).</text>')
    c.raw('<text x="40" y="325" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Governance: without CERTIFIED data sources, "revenue" means 3 things in 3 dashboards. A certified source defines metrics ONCE = the single source of truth (the Architect\'s job).</text>')
    c.raw('<text x="40" y="344" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: track reading · Tableau-in-the-stack · numbers-hide-vs-picture-reveals · perceptual accuracy · live-vs-extract · relationships-avoid-join-duplication · measures-aggregate-by-dimensions ·</text>')
    c.raw('<text x="40" y="361" font-size="9.5" font-weight="400" fill="#374151">'
          'discrete-vs-continuous · chart-for-the-question · LOD FIXED · table calcs (running total/% of total) · dashboard filter action · certified data sources. Completes the data cluster (Snowflake XLIX, Databricks XLVIII, Confluent CXXXV).</text>')

    c.legend(40, 392, [
        ("data", "Specialist / Data Analyst"),
        ("alt", "Architect"),
        ("neutral", "Track shape"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
