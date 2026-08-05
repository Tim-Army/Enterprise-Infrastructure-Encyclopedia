#!/usr/bin/env python3
"""Volume CXLIV (SAP) certification program map.

Chapter 1: a vast program mid-transformation -- the 2026 move to practical,
open-book, AI-allowed exams -- across three levels (Associate C_, Specialist,
Professional P_/E_) and the solution areas (S/4HANA, SuccessFactors, BTP,
Ariba, Analytics, Business AI), with published attempt-bundle pricing.

Run from scripts/diagrams:  python3 gen_volume144.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-144-sap-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: SAP Certification Tracks",
        subtitle="a vast program MID-TRANSFORMATION · practical exams roll out Q1 2026 · open-book + AI-allowed + no proctoring",
        svg_title="Chapter 1 program map: the SAP certification program and its 2026 practical-exam transition",
        svg_desc="SAP's certification program is vast and, as of 2026, mid-transformation. The defining "
                 "change is a move from multiple-choice to practical, performance-based exams: most exams "
                 "available by mid-January 2026 and all transitioned by end of March. The new format uses "
                 "system-based tasks or roleplay scenarios tailored to each certification, timeboxed around "
                 "real project expectations, with an open-book approach that allows the use of relevant "
                 "resources and AI-supported tools, and no live proctoring. The rationale is the AI era: "
                 "when AI handles recall, the exam tests application rather than memorization. The program "
                 "has three levels. Associate, mostly carrying C underscore exam codes, validates "
                 "fundamental consultant knowledge applied under supervision and forms the bulk of the "
                 "catalog. Specialist adds a focused role or integration component on top of an Associate. "
                 "Professional, carrying P underscore and some E underscore codes, is advanced and requires "
                 "proven recent project experience, for example twenty-four months of ERP project "
                 "involvement within the past thirty-six. Solution areas span S/4HANA, the ERP core with "
                 "modules for finance, controlling, sales, and procurement, available as Cloud Public "
                 "Edition via GROW with SAP, Cloud Private Edition via RISE with SAP, or on-premise; "
                 "SuccessFactors for human experience management; the Business Technology Platform for "
                 "administration, integration, and ABAP Cloud development; Ariba and Concur; analytics via "
                 "SAP Analytics Cloud, Datasphere, and Business Data Cloud; and the Business AI Platform "
                 "with Joule assistants and agents. Certification is purchased as attempt bundles of one, "
                 "two, or six attempts, or an SAP Learning Hub subscription with four attempts; the "
                 "two-attempt bundle costs two hundred seventy-six US dollars and includes ten hours of "
                 "hands-on practice-system access. Scoring is automatic or AI-reviewed, with video "
                 "submissions scored by experts within twenty business days. Practical format is required "
                 "for first-time takers only; already-certified professionals continue their renewal cycle.")

    c.node_box(150, 42, 660, 46, "alt", [
        Line("★ 2026 TRANSITION: multiple-choice → PRACTICAL, performance-based exams (all by end-March)", 10, 700, "#111827"),
        Line("system tasks/scenarios · TIMEBOXED · OPEN-BOOK + AI TOOLS ALLOWED · NO live proctoring — \"prove what you can DO\"", 8, 400, "#374151"),
    ])

    # three levels
    c.node_box(40, 128, 270, 62, "data", [
        Line("ASSOCIATE  (C_)", 9.5, 700, "#111827"),
        Line("fundamental, applied UNDER SUPERVISION", 7.5, 400, "#374151"),
        Line("no experience gate · the BULK of the catalog", 7.5, 400, "#374151"),
    ])
    c.node_box(340, 128, 240, 62, "data", [
        Line("SPECIALIST", 9.5, 700, "#111827"),
        Line("added ON TOP of an Associate", 7.5, 400, "#374151"),
        Line("focused role / integration component", 7.5, 400, "#374151"),
    ])
    c.node_box(610, 128, 310, 62, "alt", [
        Line("PROFESSIONAL  (P_ / some E_)", 9.5, 700, "#111827"),
        Line("advanced · requires PROVEN PROJECT EXPERIENCE", 7.5, 700, "#166534"),
        Line("e.g. 24 months ERP in past 36 (C_RISME) — cannot be crammed", 7, 400, "#374151"),
    ])
    c.connector(310, 159, 340, 159, "data", label="", label_pos=(0, 0))
    c.connector(580, 159, 610, 159, "alt", label="", label_pos=(0, 0))

    # solution areas
    c.node_box(40, 208, 880, 72, "mgmt", [
        Line("SOLUTION AREAS (choose FIRST — a business-function fork; module + level follow)", 8.5, 700, "#111827"),
        Line("S/4HANA (ERP core: FI · CO · SD · MM · PS) — Cloud PUBLIC (GROW) / PRIVATE (RISE) / on-prem · HANA in-memory · clean core", 7.5, 400, "#374151"),
        Line("SuccessFactors (HXM: Employee Central + specialties) · BTP (Administrator · Integration/CPI · ABAP Cloud/RAP+Joule) · Ariba · Concur", 7.5, 400, "#374151"),
        Line("Analytics (SAC · Datasphere · Business Data Cloud) · Business AI Platform (Joule ASSISTANTS vs AGENTS · Gen AI Developer)", 7.5, 400, "#374151"),
    ])

    # pricing
    c.node_box(40, 298, 880, 40, "neutral", [
        Line("PURCHASING (published): attempt bundles — ONE / TWO / SIX attempts, or SAP Learning Hub subscription (4 attempts)", 8.5, 700, "#111827"),
        Line("two-attempt bundle = USD 276/yr, INCLUDES 10 HOURS of hands-on practice systems (because a practical exam is prepared by DOING)", 8, 400, "#374151"),
    ])

    c.raw('<text x="40" y="360" font-size="9.5" font-weight="700" fill="#166534">'
          'The AI-era bet: when AI handles recall, the exam tests APPLICATION. Question dumps target the RETIRED format — worse than useless in 2026.</text>')
    c.raw('<text x="40" y="379" font-size="9.5" font-weight="400" fill="#374151">'
          'Transition rules: PRACTICAL format required for FIRST-TIME takers only · already-certified continue renewal · video components scored by experts within 20 BUSINESS DAYS.</text>')
    c.raw('<text x="40" y="398" font-size="9.5" font-weight="400" fill="#374151">'
          'There is no "SAP certification" — you certify in an AREA + MODULE + LEVEL. Specialize, don\'t generalize (like Vols CXXIII IBM, XLVII Oracle, LXXXIII Salesforce).</text>')
    c.raw('<text x="40" y="417" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: level/prefix reading · attempt-bundle choice · ECC→S/4HANA data-model change · edition choice · fit-to-standard liability math · Explore-sets-scope ·</text>')
    c.raw('<text x="40" y="434" font-size="9.5" font-weight="400" fill="#374151">'
          'OCM×technical adoption · clean-core extension vs modification · ABAP-Cloud restriction · integration seams · EC system-of-record · assistant-vs-agent · practical-exam prep · SoD scan.</text>')

    c.legend(40, 468, [
        ("data", "Associate / Specialist"),
        ("alt", "Professional / transition"),
        ("mgmt", "Solution areas"),
        ("neutral", "Purchasing"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
