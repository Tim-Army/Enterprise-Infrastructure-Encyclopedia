#!/usr/bin/env python3
"""Volume CLXVIII (SAS) program map.

Chapter 1: the SAS Global Certification program (Specialist / Professional / composite
Data Scientist) across categories — programming, statistics, AI/ML, data curation,
visual BI, administration — over the SAS language (DATA step + PROC) and SAS Viya
(the in-memory CAS engine, Model Studio, Visual Analytics).

Run from scripts/diagrams:  python3 gen_volume168.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-168-sas-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: SAS Certification Tracks",
        subtitle="SAS Global Certification — Specialist / Professional / composite Data Scientist · Pearson VUE · ~$180 · 5-yr · A00-xxx",
        svg_title="Chapter 1 program map: the SAS certification scopes and categories over the SAS language and SAS Viya",
        svg_desc="SAS is the analytics, statistics, and data-management leader — the SAS language, built from the "
                 "DATA step and PROC steps, and SAS Viya, its cloud-native, in-memory analytics and AI platform "
                 "powered by the CAS engine. SAS Global Certification comes in three scopes: SAS Certified "
                 "Specialist, earned by a single exam; SAS Certified Professional, earned by multiple exams; and "
                 "the composite SAS Certified Data Scientist, earned by combining credentials across the "
                 "discipline. Credentials are organized by category: programming, from Fundamentals to "
                 "Programming Specialist to Advanced Programming; advanced analytics and statistics, the "
                 "Statistical Business Analyst; AI and machine learning, the Machine Learning Specialist using "
                 "SAS Viya and Model Studio; data curation; visual business intelligence with SAS Visual "
                 "Analytics; and SAS Viya Administration. Exams are delivered through Pearson VUE, are about one "
                 "hundred eighty dollars, are valid five years, use A00 exam codes, and some are performance-based "
                 "and hands-on in SAS. The lifecycle is curate, describe, model, assess, and report or deploy, "
                 "with statistical rigor at each step.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("SAS — analytics · statistics · data management leader: the SAS LANGUAGE (DATA step + PROC) + SAS VIYA (cloud-native AI/analytics)", 8.0, 700, "#111827"),
        Line("SAS Viya: in-memory CAS engine · Model Studio (ML pipelines) · SAS Visual Analytics (BI) · SAS Studio (code) · SAS 9.4 = legacy", 6.9, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("SAS GLOBAL CERTIFICATION — three scopes", 8.3, 700, "#111827"),
        Line("SAS Certified SPECIALIST (single exam)  ·  SAS Certified PROFESSIONAL (multiple exams)  ·  composite SAS Certified DATA SCIENTIST   |   Pearson VUE · ~$180 · 5-yr · A00-xxx · some performance-based", 6.1, 400, "#374151"),
    ])

    c.node_box(40, 176, 288, 46, "data", [
        Line("PROGRAMMING", 7.8, 700, "#111827"),
        Line("Fundamentals → Specialist (A00-420, 71%) → Advanced · DATA step + PROC", 5.6, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("DATA CURATION", 7.8, 700, "#111827"),
        Line("merge · formats/informats · clean · validate · missing values", 5.9, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("STATISTICS (Stat Business Analyst)", 7.2, 700, "#111827"),
        Line("A00-240 · descriptive/inferential · regression · assessment", 5.8, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 46, "alt", [
        Line("AI & MACHINE LEARNING", 7.6, 700, "#111827"),
        Line("ML Specialist (Viya) · Model Studio pipelines · champion · deploy", 5.6, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 46, "alt", [
        Line("VISUAL / BI (Visual Business Analytics)", 7.0, 700, "#111827"),
        Line("A00-470 · SAS Visual Analytics · reports + forecasting", 5.9, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 46, "alt", [
        Line("ADMINISTRATION (Viya Admin)", 7.4, 700, "#111827"),
        Line("A00-451 · Kubernetes · users/security · data governance", 5.8, 400, "#374151"),
    ])

    c.raw('<text x="40" y="308" font-size="9.5" font-weight="700" fill="#166534">'
          'CURATE (data) + DESCRIBE (statistics) + MODEL (stats + ML) + ASSESS (rigorously) + REPORT/DEPLOY — the end-to-end analytics lifecycle, with statistical rigor at each step.</text>')
    c.raw('<text x="40" y="330" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: scopes + categories + mechanics · CAS in-memory + DATA step/PROC · read/DATA-step/summarize · match-merge + formats + clean/validate · descriptive + regression + R-squared ·</text>')
    c.raw('<text x="40" y="347" font-size="9.5" font-weight="400" fill="#374151">'
          'Model Studio pipeline + champion selection · Visual Analytics report + forecast · composite Data Scientist + Viya admin · capstone lifecycle end-to-end. Peers: Tableau (CLIV), Qlik (CLXI), Databricks (XLVIII).</text>')

    c.legend(40, 376, [
        ("data", "Program / curate / stats"),
        ("alt", "ML / BI / administer"),
        ("neutral", "Cert scopes"),
        ("mgmt", "SAS language + Viya"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
