#!/usr/bin/env python3
"""Volume CXXX (Rubrik Certification Tracks) program map.

Chapter 1: the Rubrik program — one active certification (RCSA, Rubrik
Certified System Administrator) earned via Rubrik University's free
self-paced path or a paid hands-on RSC Administration bootcamp (RCE
retired), all on Rubrik Security Cloud, the Cyber Resilience Platform for
Data and Identity: policy-driven protection, immutability/air-gap,
ransomware recovery + Data Threat Analytics, DSPM, and identity resilience.

Run from scripts/diagrams:  python3 gen_volume130.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-130-rubrik-certifications"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Program Map: Rubrik Certification (Cyber Resilience for Data & Identity)",
        subtitle="One active cert — RCSA — via a free self-paced path or a paid hands-on RSC Administration bootcamp (RCE retired); all on Rubrik Security Cloud",
        svg_title="Chapter 1 program map: the Rubrik certification program",
        svg_desc="The Rubrik certification program is focused on one active certification, RCSA, Rubrik Certified "
                 "System Administrator, which validates operational administration of Rubrik Security Cloud. It is "
                 "earned through Rubrik University via a free self-paced learning path with eLearning and unlimited "
                 "practice exams, or a paid four-day hands-on Rubrik Security Cloud Administration bootcamp. Badges "
                 "issue on Credly and Rubrik University access requires Rubrik Support credentials. The older RCE, "
                 "Rubrik Certified Engineer, is retired. Everything is grounded in Rubrik Security Cloud, the Cyber "
                 "Resilience Platform for Data and Identity, whose domains are policy-driven data protection via SLA "
                 "Domains, immutability and logical air-gap, ransomware and cyber recovery with anomaly detection "
                 "and Data Threat Analytics, Data Security Posture Management, recovery orchestration and testing, "
                 "broad workload protection, and identity resilience. The premise is assume breach, protect "
                 "immutably, recover fast and clean. The volume models these free in Python.")

    c.node_box(280, 42, 400, 42, "mgmt", [
        Line("Rubrik Security Cloud — Cyber Resilience for Data & Identity", 10, 700, "#111827"),
        Line("premise: assume breach — protect immutably, recover fast & clean", 8.5, 400, "#374151"),
    ])

    # the one cert + two routes
    c.node_box(330, 120, 300, 52, "data", [
        Line("RCSA — Rubrik Certified System Administrator", 9.5, 700, "#111827"),
        Line("operate Rubrik Security Cloud (RCE retired)", 8.5, 400, "#374151"),
    ])
    c.node_box(60, 210, 380, 46, "neutral", [
        Line("FREE learning path", 10, 700, "#111827"),
        Line("eLearning + unlimited practice exams -> final", 8.5, 400, "#374151"),
    ])
    c.node_box(520, 210, 380, 46, "alt", [
        Line("PAID bootcamp (4-day, ~60% labs)", 10, 700, "#111827"),
        Line("RSC Administration; exam Qs from bootcamp", 8.5, 400, "#374151"),
    ])
    c.connector(300, 146, 250, 210, "neutral", label="", label_pos=(0, 0))
    c.connector(660, 146, 710, 210, "alt", label="", label_pos=(0, 0))

    # domains band
    c.node_box(60, 290, 840, 40, "neutral", [
        Line("RSC domains: data protection (SLA) · immutability/air-gap · ransomware recovery + Data Threat Analytics · DSPM · orchestrated recovery · identity resilience", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="60" y="375" font-size="9.5" font-weight="700" fill="#166534">'
          'The backup is the last line of defense: immutable (ransomware can\'t alter it), analyzable (detect + hunt), recoverable (tested)</text>')
    c.raw('<text x="60" y="394" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: append-only immutable store · backup-delta anomaly detection · classification · recovery orchestration · RBAC</text>')

    c.legend(60, 420, [
        ("data", "The active certification (RCSA)"),
        ("neutral", "Free study route"),
        ("alt", "Paid bootcamp route"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
