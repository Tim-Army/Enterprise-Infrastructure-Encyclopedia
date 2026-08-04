#!/usr/bin/env python3
"""Volume CXXXIII (Commvault Certification Tracks) program map.

Chapter 1: Readiverse Academy's "four tiers, one path" program (rebuilt
June 2026) — Practitioner, Specialist, Professional, Expert — all resting
on three learning pillars (platform skills, cyber resilience, workload
expertise), earned through coursework + hands-on labs + validated
assessments, with ISC2 CPE credit.

Run from scripts/diagrams:  python3 gen_volume133.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-133-commvault-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: Commvault Certification (Readiverse Academy)",
        subtitle="Four tiers, one path — Practitioner to Expert — on three pillars: platform skills, cyber resilience, workload expertise; coursework + labs + assessments; ISC2 CPE credit",
        svg_title="Chapter 1 program map: the Commvault Readiverse Academy certification program",
        svg_desc="Commvault's certification program runs in Readiverse Academy and was rebuilt in June 2026 around "
                 "four tiers on one path. Commvault Cloud Practitioner covers foundational platform and cyber "
                 "resilience knowledge and is earned through the Commvault Cloud Administrator course of about four "
                 "hours, the Cyber Resilience course of about four hours, one workload course of about thirty "
                 "minutes, exams for both the Administrator and Cyber Resilience components, and claiming a digital "
                 "badge. Commvault Cloud Specialist adds expanded operational, workload, and security depth. "
                 "Commvault Cloud Professional adds advanced recovery and workload expertise including Cloud Rewind "
                 "or Cleanroom Recovery coursework. Commvault Cloud Expert covers cloud engineering and resilience "
                 "leadership with Cloud Engineer coursework, advanced feature courses, Cloud Rewind, and Cleanroom "
                 "Recovery. All four tiers rest on the same three learning pillars: foundational platform skills, "
                 "cyber resilience, and workload and feature expertise. Named certifications include Commvault Cloud "
                 "Administrator, the Cyber Resilience Certification, and SaaS certifications for Threat Scan, "
                 "Cleanroom Recovery, and Cloud Rewind. Workload courses cover Microsoft 365, Active Directory and "
                 "Entra ID, file server protection, VMware, and Oracle. Credentials are vendor-validated through "
                 "coursework, hands-on lab activities, and validated assessments, and Commvault is an ISC2 CPE "
                 "Authorized Submitter so the training also earns continuing education credit. The volume models "
                 "these disciplines free in Python.")

    c.node_box(230, 42, 500, 44, "mgmt", [
        Line("Readiverse Academy — FOUR TIERS, ONE PATH", 10.5, 700, "#111827"),
        Line("vendor-validated: coursework + hands-on labs + validated assessments", 8.5, 400, "#374151"),
    ])

    # the four tiers as a ladder
    c.node_box(40, 128, 210, 78, "neutral", [
        Line("PRACTITIONER", 9.5, 700, "#111827"),
        Line("platform + resilience", 8, 400, "#374151"),
        Line("Administrator course 4h", 7.5, 400, "#374151"),
        Line("Cyber Resilience 4h", 7.5, 400, "#374151"),
        Line("+1 workload · 2 exams", 7.5, 400, "#374151"),
    ])
    c.node_box(268, 128, 210, 78, "data", [
        Line("SPECIALIST", 9.5, 700, "#111827"),
        Line("expanded operational,", 8, 400, "#374151"),
        Line("workload & security", 8, 400, "#374151"),
        Line("depth", 8, 400, "#374151"),
    ])
    c.node_box(496, 128, 210, 78, "data", [
        Line("PROFESSIONAL", 9.5, 700, "#111827"),
        Line("advanced recovery +", 8, 400, "#374151"),
        Line("workload expertise", 8, 400, "#374151"),
        Line("Cloud Rewind / Cleanroom", 7.5, 400, "#374151"),
    ])
    c.node_box(724, 128, 196, 78, "alt", [
        Line("EXPERT", 9.5, 700, "#111827"),
        Line("cloud engineering +", 8, 400, "#374151"),
        Line("resilience leadership", 8, 400, "#374151"),
        Line("Cloud Engineer + both", 7.5, 400, "#374151"),
    ])
    c.connector(250, 167, 268, 167, "data", label="", label_pos=(0, 0))
    c.connector(478, 167, 496, 167, "data", label="", label_pos=(0, 0))
    c.connector(706, 167, 724, 167, "alt", label="", label_pos=(0, 0))

    # three pillars
    c.node_box(40, 236, 280, 60, "mgmt", [
        Line("PILLAR 1 — Platform skills", 9, 700, "#111827"),
        Line("CommCell architecture · plans & retention", 8, 400, "#374151"),
        Line("deduplication/DDB · backup & recovery ops", 8, 400, "#374151"),
    ])
    c.node_box(340, 236, 280, 60, "mgmt", [
        Line("PILLAR 2 — Cyber resilience", 9, 700, "#111827"),
        Line("immutability/WORM · air gap · anomaly detect", 8, 400, "#374151"),
        Line("Threat Scan · Cleanroom · Cloud Rewind", 8, 400, "#374151"),
    ])
    c.node_box(640, 236, 280, 60, "mgmt", [
        Line("PILLAR 3 — Workload expertise", 9, 700, "#111827"),
        Line("M365 · Active Directory & Entra ID", 8, 400, "#374151"),
        Line("VMware · Oracle · file servers", 8, 400, "#374151"),
    ])

    # named certs band
    c.node_box(40, 320, 880, 40, "neutral", [
        Line("Named certifications: Commvault Cloud Administrator · Cyber Resilience · SaaS Threat Scan · SaaS Cleanroom Recovery · SaaS Cloud Rewind", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="400" font-size="9.5" font-weight="700" fill="#166534">'
          'Backup is a SECURITY control: resilience is examined from the Practitioner tier up, not bolted on at the top</text>')
    c.raw('<text x="40" y="419" font-size="9.5" font-weight="400" fill="#374151">'
          'Commvault is an ISC2 CPE Authorized Submitter — coursework also earns CPEs. Modeled free in Python: retention/cycles · dedup · RPO/RTO · immutability · cleanroom.</text>')

    c.legend(40, 450, [
        ("neutral", "Entry tier / certs"),
        ("data", "Mid tiers"),
        ("alt", "Expert tier"),
        ("mgmt", "Learning pillars"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
