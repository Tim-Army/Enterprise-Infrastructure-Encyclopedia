#!/usr/bin/env python3
"""Volume CLXIV (Pega) program map.

Chapter 1: the Pega Academy tracks (System Architect ladder CSA->CSSA->CLSA [2-part],
Business Architect, Decisioning, Robotics; Infinity '25) over the low-code, model-
driven Pega Platform — case management, situational layer cake, Next-Best-Action.

Run from scripts/diagrams:  python3 gen_volume164.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-164-pega-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Pega Certification Tracks",
        subtitle="Pega Academy — System Architect ladder (CSA→CSSA→CLSA) + Business Architect + Decisioning + Robotics · low-code",
        svg_title="Chapter 1 program map: the Pega certification tracks over the low-code Pega Platform",
        svg_desc="Pega offers certifications across several tracks on Pega Infinity 25. The System Architect "
                 "ladder is the flagship: Certified System Architect for foundational app-building in App Studio "
                 "and Dev Studio; Certified Senior System Architect, requiring the System Architect credential, "
                 "for designing reusability across business lines; and Certified Lead System Architect, "
                 "requiring the Senior credential, an expert tier earned through a two-part written Architecture "
                 "Exam plus a hands-on Application Exam that designs and builds a real app. Other tracks: "
                 "Business Architect for capturing requirements via Directly Capture Objectives, Decisioning "
                 "with Data Scientist, Decisioning Consultant, and Lead Decisioning Architect, and Robotics. "
                 "The platform beneath is the low-code, model-driven Pega Platform where everything is a rule "
                 "and guardrails enforce best practice, spanning dynamic case management, the situational layer "
                 "cake for reuse, model-driven UI, Next-Best-Action decisioning in the Customer Decision Hub, "
                 "robotics, and Pega GenAI. Pega is a low-code enterprise BPM, CRM, and decisioning leader.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("PEGA — LOW-CODE, MODEL-DRIVEN enterprise platform: BPM / case management + CRM + AI decisioning", 9.5, 700, "#111827"),
        Line("model the app (Pega generates it) · everything is a RULE · guardrails = 'build for change' · Pega Infinity '25", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("PEGA ACADEMY — certifications by track (Pega Infinity '25)", 8.3, 700, "#111827"),
        Line("SYSTEM ARCHITECT ladder: CSA → CSSA (needs CSA, reuse) → CLSA (needs CSSA; ★ 2-part: written Architecture + hands-on BUILD)   |   BUSINESS ARCHITECT (CPBA)   |   DECISIONING (Data Scientist · CPDC · Lead)   |   ROBOTICS", 6.5, 400, "#374151"),
    ])

    # platform capabilities
    c.node_box(40, 176, 288, 46, "data", [
        Line("CASE MANAGEMENT (the core)", 8.0, 700, "#111827"),
        Line("dynamic cases: stages→steps (human+auto), adapt at runtime", 6.2, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("★ SITUATIONAL LAYER CAKE (reuse)", 7.4, 700, "#111827"),
        Line("build common ONCE, specialize by layer (BU/region/channel) — no forking", 5.9, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("MODEL-DRIVEN UI + data model", 7.6, 700, "#111827"),
        Line("responsive UI auto-rendered · data pages · integrations", 6.1, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 46, "alt", [
        Line("★ NEXT-BEST-ACTION (decisioning)", 7.4, 700, "#111827"),
        Line("Customer Decision Hub: real-time 1:1 AI — relevance x value, gated", 5.8, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 46, "alt", [
        Line("ROBOTICS (RPA) + GenAI", 8.0, 700, "#111827"),
        Line("attended/unattended bots (Robot Studio) · Pega GenAI Blueprint", 6.0, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 46, "alt", [
        Line("DCO (Directly Capture Objectives)", 7.4, 700, "#111827"),
        Line("business+IT capture requirements DIRECTLY as executable app (no stale docs)", 5.7, 400, "#374151"),
    ])

    c.raw('<text x="40" y="308" font-size="9.5" font-weight="700" fill="#166534">'
          'MODEL (low-code, rules) + ORCHESTRATE (dynamic cases) + REUSE (layer cake) + DECIDE (Next-Best-Action) + AUTOMATE (robotics + GenAI). App Studio (business) + Dev Studio (developer) on ONE app.</text>')
    c.raw('<text x="40" y="330" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: tracks + prerequisite ladder + 2-part CLSA · rules/studios/guardrail-score · dynamic case lifecycle · build app (data/UI/decision/integration) · layer-cake per-situation assembly ·</text>')
    c.raw('<text x="40" y="347" font-size="9.5" font-weight="400" fill="#374151">'
          'Next-Best-Action arbitration · RPA modes + hyperautomation + GenAI Blueprint · DCO executable requirements. Peers: ServiceNow (LXXX) platform, Salesforce (LXXXIII) CRM, UiPath (CXLIX) RPA, MuleSoft (CLX) integration.</text>')

    c.legend(40, 376, [
        ("data", "Build (case/reuse/UI)"),
        ("alt", "Decide / automate / DCO"),
        ("neutral", "Cert tracks"),
        ("mgmt", "Low-code platform"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
