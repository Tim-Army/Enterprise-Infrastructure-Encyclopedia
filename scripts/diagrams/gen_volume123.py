#!/usr/bin/env python3
"""Volume CXXIII (IBM Certification Tracks) program map.

Chapter 1: the IBM Professional Certification Program — 62 current
certifications across seven portfolios, Pearson VUE/OnVUE delivery,
Credly badges, six PLUS combinations bundling Red Hat exams, and five
credentials flagged Retiring soon.

Run from scripts/diagrams:  python3 gen_volume123.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-123-ibm-certifications"


def ch01():
    c = Canvas(960, 520,
        title="Chapter 1 Program Map: The IBM Professional Certification Program",
        subtitle="62 current certifications in seven portfolios — Pearson VUE/OnVUE delivery, Credly badges, six PLUS combos bundling Red Hat OpenShift exams, five flagged Retiring soon",
        svg_title="Chapter 1 program map: the IBM Professional Certification Program",
        svg_desc="The IBM Professional Certification Program has 62 current certifications across seven "
                 "portfolios: AI, watsonx and quantum including Qiskit; security centered on the QRadar SIEM "
                 "V7.5 ladder plus Guardium and Verify Access; data platforms covering Db2 for z/OS, Db2 LUW "
                 "and Informix; analytics with Cognos, Planning Analytics and Cloud Pak for Data; integration "
                 "and messaging with MQ, App Connect, API Connect, DataPower and Sterling; automation, "
                 "observability and AIOps with Cloud Pak for Business Automation, Business Automation "
                 "Workflow, FileNet, Turbonomic, Instana and Cloud Pak for AIOps; and systems and asset "
                 "management with z/OS, AIX, IBM i, WebSphere, Maximo and TRIRIGA. Exams are delivered by "
                 "Pearson VUE in test centers or online with OnVUE, badges issue on Credly, six PLUS "
                 "combination certifications bundle a Red Hat Certified Specialist OpenShift exam, and five "
                 "credentials are flagged Retiring soon. IBM certifications are distinct from TechXchange "
                 "badges and Coursera IBM Professional Certificates.")

    c.node_box(280, 42, 400, 42, "mgmt", [
        Line("IBM Training credentials catalog — 62 certifications", 10.5, 700, "#111827"),
        Line("Pearson VUE / OnVUE delivery · Credly badges · version-pinned", 9, 400, "#374151"),
    ])

    def port(x, y, title, sub):
        c.node_box(x, y, 280, 54, "neutral", [
            Line(title, 10, 700, "#111827"),
            Line(sub, 8.5, 400, "#374151"),
        ])

    port(35, 130, "AI / watsonx / quantum (8)", "GenAI · Assistant · Orchestrate · Qiskit")
    port(340, 130, "Security (8)", "QRadar V7.5 ladder · Guardium · Verify")
    port(645, 130, "Data platforms (6)", "Db2 z/OS + LUW · Informix")
    port(35, 215, "Analytics (5)", "Cognos · Planning Analytics · CP4D")
    port(340, 215, "Integration (6)", "MQ · ACE · API Connect · DataPower")
    port(645, 215, "Automation / AIOps (8)", "CP4BA · BAW · Turbonomic · Instana")
    port(35, 300, "Systems + assets (12)", "z/OS · AIX · IBM i · WebSphere · Maximo")

    c.node_box(340, 300, 280, 54, "alt", [
        Line("PLUS combinations (6)", 10, 700, "#111827"),
        Line("IBM Cloud Pak exam + Red Hat OpenShift exam", 8.5, 400, "#166534"),
    ])
    c.node_box(645, 300, 280, 54, "warn", [
        Line("Retiring soon (5)", 10, 700, "#111827"),
        Line("Datacap · DOORS Next · ETM · CP4BA v21 · MMA", 8.5, 400, "#7f1d1d"),
    ])

    c.raw('<text x="35" y="395" font-size="9.5" font-weight="700" fill="#1d4ed8">'
          'Three credential kinds: proctored certifications (this volume) vs TechXchange badges vs Coursera certificates</text>')
    c.raw('<text x="35" y="415" font-size="9.5" font-weight="400" fill="#374151">'
          'Free runnable lab engines: Qiskit (pip) · Db2 Community Edition (container) · MQ Advanced for Developers (container)</text>')

    c.legend(35, 445, [
        ("neutral", "Certification portfolio (count)"),
        ("alt", "PLUS: bundles a Red Hat exam"),
        ("warn", "Retiring soon — do not target"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
