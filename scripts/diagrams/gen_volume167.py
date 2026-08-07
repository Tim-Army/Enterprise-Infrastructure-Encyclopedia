#!/usr/bin/env python3
"""Volume CLXVII (Automation Anywhere) program map.

Chapter 1: the Automation Anywhere University certification program (Essentials free →
Advanced → AI Automation Engineer) over the cloud-native Automation Success Platform
(Automation 360), an RPA pioneer pivoting to Agentic Process Automation — Control Room,
bots, Automation Co-Pilot, Document Automation, and AI Agent Studio.

Run from scripts/diagrams:  python3 gen_volume167.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-167-automation-anywhere-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Automation Anywhere Certification Tracks",
        subtitle="University: Essentials (free) → Advanced (60Q/2h/80%) → AI Automation Engineer · RPA → Agentic Process Automation",
        svg_title="Chapter 1 program map: the Automation Anywhere certification tiers over the cloud-native Automation Success Platform",
        svg_desc="Automation Anywhere is an RPA pioneer pivoting to Agentic Process Automation, combining "
                 "robotic process automation with AI agents and generative AI. Certifications run through "
                 "Automation Anywhere University in three tiers: the Essentials Certification, which is free and "
                 "foundational; the Advanced Certification, the Certified Advanced Automation Professional on "
                 "Automation 360, a sixty-question, two-hour, eighty-percent-to-pass exam with a fifty-dollar "
                 "renewal; and the AI Automation Engineer Certification, the AI and agentic flagship covering "
                 "Document Automation, AI Agent Studio, and Automation Co-Pilot. Training is free. The platform "
                 "beneath is the Automation Success Platform on Automation 360, cloud-native and fully web-based, "
                 "orchestrated from a central Control Room that stores bots, deploys them to Bot Runners, holds "
                 "secrets in a Credential Vault, enforces role-based access control, and audits everything. It "
                 "spans building Task Bots, attended and unattended automation, Automation Co-Pilot, Document "
                 "Automation for intelligent document processing, Agentic Process Automation with AI agents that "
                 "reason under guardrails, and Process Discovery, Bot Insight, and a Center of Excellence. The "
                 "arc runs from scripting deterministic bots to engineering AI-driven automation.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("AUTOMATION SUCCESS PLATFORM (Automation 360) — cloud-native, WEB-BASED · RPA → AGENTIC PROCESS AUTOMATION", 8.6, 700, "#111827"),
        Line("Control Room (deploy/govern/vault/RBAC/audit) · Bot Creators build · Bot Runners execute · AI layered across (Co-Pilot / Document Automation / AI Agent Studio)", 6.8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("AUTOMATION ANYWHERE UNIVERSITY — certification tiers (training FREE)", 8.3, 700, "#111827"),
        Line("ESSENTIALS (free, foundational)  →  ADVANCED (Certified Advanced Automation Professional; 60Q · 2h · 80% · 2 attempts · $50 renewal)  →  AI AUTOMATION ENGINEER (AI/agentic flagship)", 6.3, 400, "#374151"),
    ])

    c.node_box(40, 176, 288, 46, "data", [
        Line("BUILD BOTS (Bot Creator)", 7.8, 700, "#111827"),
        Line("Task Bots: actions over variables · recorders · control flow · reuse", 5.9, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("CONTROL ROOM (govern)", 7.8, 700, "#111827"),
        Line("deploy/schedule · work queues · Credential Vault · RBAC · audit", 5.9, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("ATTENDED / UNATTENDED + CO-PILOT", 7.2, 700, "#111827"),
        Line("front-office assist vs lights-out · human-in-the-loop · AI Co-Pilot", 5.7, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 46, "alt", [
        Line("DOCUMENT AUTOMATION (IDP)", 7.6, 700, "#111827"),
        Line("classify + extract across layouts · confidence · validate · route", 5.8, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 46, "alt", [
        Line("AGENTIC PA + AI AGENT STUDIO", 7.4, 700, "#111827"),
        Line("agents reason to a goal + call bots · GenAI · guardrails + oversight", 5.7, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 46, "alt", [
        Line("DISCOVERY · BOT INSIGHT · CoE", 7.4, 700, "#111827"),
        Line("find opportunities · measure ROI · scale as a governed program", 5.8, 400, "#374151"),
    ])

    c.raw('<text x="40" y="308" font-size="9.5" font-weight="700" fill="#166534">'
          'BUILD (bots) + GOVERN (Control Room) + ASSIST (Co-Pilot) + READ (Document Automation) + REASON (agents) + SCALE (Discovery + CoE) — from scripting bots to engineering AI-driven automation.</text>')
    c.raw('<text x="40" y="330" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: tiers + RPA-vs-APA routing · Automation 360 architecture · Task Bot (actions/loop/if/try-catch/subtask) · Control Room work queue + vault + RBAC + audit · attended/unattended + human-in-loop + Co-Pilot ·</text>')
    c.raw('<text x="40" y="347" font-size="9.5" font-weight="400" fill="#374151">'
          'IDP classify/extract/confidence/route · agent reason→call-bot under guardrails · Discovery scoring + Bot Insight ROI + CoE pipeline · capstone agentic accounts-payable. Peers: UiPath (CXLIX), Pega (CLXIV), Boomi (CLXVI).</text>')

    c.legend(40, 376, [
        ("data", "Build / govern / assist"),
        ("alt", "Read / reason / scale (AI)"),
        ("neutral", "Cert tiers"),
        ("mgmt", "Cloud-native platform"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
