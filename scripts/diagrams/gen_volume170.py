#!/usr/bin/env python3
"""Volume CLXX (Teradata) program map.

Chapter 1: the Teradata Vantage certification program (current VantageCloud Lake
Associate vs legacy Vantage 2 track) over the shared-nothing MPP engine — Parsing
Engine, AMPs, BYNET, Primary Index distribution, parallel SQL, and ClearScape Analytics.

Run from scripts/diagrams:  python3 gen_volume170.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-170-teradata-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Teradata Certification Tracks",
        subtitle="Teradata Vantage Certifications — current VantageCloud Lake Associate ($149/75min) vs legacy Vantage 2 · Pearson VUE · no expiration",
        svg_title="Chapter 1 program map: the Teradata certification tracks over the shared-nothing MPP data-warehouse engine",
        svg_desc="Teradata is the pioneer and leader of the enterprise data warehouse, built on massively parallel "
                 "processing, a shared-nothing engine that distributes data across Access Module Processors and "
                 "queries it in parallel. Today it is cloud, as Teradata Vantage and VantageCloud, with a Lake "
                 "edition that is cloud-native, elastic, and lakehouse-oriented, and an Enterprise edition that is "
                 "the full data warehouse. Certifications are transitioning from the legacy Vantage 2 track, whose "
                 "Analytics, Data Science, and Architecture exams retired in July 2024, to the current "
                 "VantageCloud Lake track, whose flagship is the Associate VantageCloud Lake 2.0 exam at one "
                 "hundred forty-nine dollars for seventy-five minutes, delivered through Pearson VUE with a "
                 "digital badge, no prerequisites, and no expiration. The engine beneath has a Parsing Engine that "
                 "parses and optimizes SQL, AMPs that process data in parallel, and a BYNET interconnect. The "
                 "Primary Index hashes rows to AMPs and is the distribution mechanism, where even distribution "
                 "avoids skew. Topics span the MPP architecture, primary-index distribution, parallel SQL and the "
                 "optimizer, physical design with indexes and partitioning, workload management and "
                 "administration, and ClearScape Analytics in-database machine learning. The lifecycle is "
                 "distribute, design, query, operate, and analyze.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("TERADATA — enterprise DATA WAREHOUSE leader on shared-nothing MPP: Vantage / VantageCloud (multi-cloud + on-prem)", 8.3, 700, "#111827"),
        Line("Parsing Engine (parse/optimize) → AMPs (parallel workers, own their data slice) → BYNET (interconnect) · VantageCloud LAKE (cloud-native/elastic/lakehouse) vs ENTERPRISE", 6.2, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("TERADATA VANTAGE CERTIFICATIONS — transitioning current ← legacy", 8.3, 700, "#111827"),
        Line("VANTAGECLOUD LAKE (current): Associate VantageCloud Lake 2.0 ($149/75min)   |   VANTAGE 2 (legacy): Associate 2.4 · Data Engineering · Admin (Analytics/Data Sci/Arch RETIRED Jul 2024)   |   Pearson VUE · badges · no expiration", 5.6, 400, "#374151"),
    ])

    c.node_box(40, 176, 288, 46, "data", [
        Line("MPP ARCHITECTURE", 7.8, 700, "#111827"),
        Line("shared-nothing · PE + AMPs + BYNET · parallel = scalable", 5.9, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("★ PRIMARY INDEX (distribution)", 7.4, 700, "#111827"),
        Line("hash rows → AMPs · even vs SKEW · single-AMP access · join co-location", 5.4, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("SQL + OPTIMIZER at scale", 7.6, 700, "#111827"),
        Line("ANSI SQL + window fns · cost-based optimizer · co-located vs redistributed joins · stats", 5.1, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 46, "alt", [
        Line("PHYSICAL DESIGN", 7.8, 700, "#111827"),
        Line("types · secondary/join indexes · PPI partition elimination", 5.8, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 46, "alt", [
        Line("WORKLOAD MGMT + ADMIN", 7.6, 700, "#111827"),
        Line("TASM priorities · users/roles · space (spool) · governance", 5.8, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 46, "alt", [
        Line("CLEARSCAPE + MODERN PLATFORM", 7.2, 700, "#111827"),
        Line("in-database analytics/ML · QueryGrid fabric · lakehouse/open/Python", 5.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="308" font-size="9.5" font-weight="700" fill="#166534">'
          'DISTRIBUTE (Primary Index) + DESIGN (indexes/PPI) + QUERY (parallel SQL + optimizer) + OPERATE (workload/space) + ANALYZE (ClearScape in-database) — enterprise analytics on a shared-nothing MPP engine.</text>')
    c.raw('<text x="40" y="330" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: current/legacy tracks + mechanics · Vantage Lake-vs-Enterprise · MPP parallel scan + skew cost · Primary Index distribution/access/join · SQL aggregation + join strategy + stats ·</text>')
    c.raw('<text x="40" y="347" font-size="9.5" font-weight="400" fill="#374151">'
          'design types/indexes + PPI partition elimination · workload priority + spool + governance · ClearScape in-database scoring + QueryGrid · capstone lifecycle. Peers: Snowflake (XLIX), Databricks (XLVIII), Cloudera (CLVIII).</text>')

    c.legend(40, 376, [
        ("data", "Architecture / distribute / query"),
        ("alt", "Design / operate / analyze"),
        ("neutral", "Cert tracks"),
        ("mgmt", "MPP data warehouse"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
