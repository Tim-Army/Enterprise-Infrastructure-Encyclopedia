#!/usr/bin/env python3
"""Volume CXLIX (UiPath) certification-program map.

Chapter 1: the role-based UiPath Certified Professional program (Associate /
Professional across developer, business analyst, architect, AI, testing,
agentic) over the automation platform (Studio / Orchestrator / Robots), amid the
RPA-to-agentic shift. Credentials since Feb 2026 valid 3 years; legacy
UiRPA/UiARD expire 15 Oct 2026.

Run from scripts/diagrams:  python3 gen_volume149.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-149-uipath-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: UiPath Certification Tracks",
        subtitle="role-based (Associate / Professional) · RPA -> AGENTIC · 3-yr validity (since Feb 2026) · UiRPA/UiARD expire 15 Oct 2026",
        svg_title="Chapter 1 program map: the role-based UiPath Certified Professional program over the automation platform",
        svg_desc="The UiPath Certified Professional program is role-based, aligned to real automation-team "
                 "roles across two levels, Associate and Professional, rather than a single ladder. "
                 "Certifications include Agentic Automation Associate and Professional for collaborating with "
                 "and governing AI agents, Automation Developer Associate and Professional for building "
                 "automations, Specialized AI Professional for Document Understanding and Communications "
                 "Mining, Automation Solution Architect Professional for enterprise architecture, Automation "
                 "Business Analyst Professional for process discovery and requirements, and a testing track "
                 "moving from the retiring Software Testing Engineer Professional to the new Test Cloud "
                 "Architect Professional. The Automation Developer Associate exam is sixty multiple-choice "
                 "and multi-select questions and is the common entry point. Credentials issued since "
                 "February 2026 are valid for three years. Preparation is free through UiPath Academy; exams "
                 "are proctored and paid via vouchers; holding multiple certifications earns the Automation "
                 "Catalysts badge. The legacy UiPath RPA Associate and Advanced RPA Developer certifications, "
                 "retired in 2023, expire on October 15, 2026, and were relaunched as the Automation "
                 "Developer Associate and Professional. The whole program reflects the industry shift from "
                 "robotic process automation, deterministic software robots automating rule-based tasks, to "
                 "agentic automation that combines AI agents that reason and act, robots, and humans. The "
                 "platform beneath is Studio for building automations, Orchestrator for deploying, "
                 "scheduling, and governing robots, attended and unattended Robots for execution, and AI and "
                 "discovery products including Document Understanding, Communications Mining, Process Mining, "
                 "Task Mining, and Autopilot, run by a Center of Excellence.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("UiPATH — business process automation: from RPA to AGENTIC automation", 10.5, 700, "#111827"),
        Line("robots (deterministic) + AI agents (reason & act) + humans (accountability), orchestrated", 8, 400, "#374151"),
    ])

    # role-based certs — two rows by level
    c.node_box(40, 120, 880, 26, "neutral", [
        Line("ROLE-BASED program — pick the CERT for your JOB, climb the LEVEL (Associate -> Professional). Not one ladder.", 8.5, 700, "#111827"),
    ])
    c.node_box(40, 152, 215, 52, "alt", [
        Line("Automation Developer", 8.5, 700, "#111827"),
        Line("Associate -> Professional", 7, 400, "#374151"),
        Line("build (ADA: 60 MC+multi)", 7, 400, "#166534"),
    ])
    c.node_box(263, 152, 215, 52, "data", [
        Line("Agentic Automation", 8.5, 700, "#111827"),
        Line("Associate -> Professional", 7, 400, "#374151"),
        Line("★ work with / govern agents", 7, 400, "#166534"),
    ])
    c.node_box(486, 152, 210, 52, "data", [
        Line("Business Analyst Pro", 8.5, 700, "#111827"),
        Line("discovery + requirements", 7, 400, "#374151"),
        Line("Specialized AI Pro (IDP)", 7, 400, "#374151"),
    ])
    c.node_box(704, 152, 216, 52, "data", [
        Line("Solution Architect Pro", 8.5, 700, "#111827"),
        Line("enterprise architecture", 7, 400, "#374151"),
        Line("Test Cloud Architect Pro (new)", 7, 400, "#374151"),
    ])

    c.node_box(40, 220, 880, 30, "alt", [
        Line("proctored · vouchers · prep FREE via UiPath ACADEMY · Automation CATALYSTS badge for multiple certs · credentials since Feb 2026 valid 3 YEARS", 8, 700, "#111827"),
    ])

    # RPA -> agentic band
    c.node_box(40, 262, 880, 46, "mgmt", [
        Line("★ THE SHIFT: classic RPA = DETERMINISTIC robots (rule-based, structured) -> AGENTIC automation adds AI AGENTS (reason over ambiguity)", 8.5, 700, "#111827"),
        Line("robots do the deterministic bulk · agents handle judgment/unstructured · humans own accountability — orchestrated together (Chapter 2)", 7.5, 400, "#374151"),
    ])

    # platform
    c.node_box(40, 320, 880, 46, "mgmt", [
        Line("PLATFORM (run by a Center of Excellence)", 8.5, 700, "#111827"),
        Line("STUDIO (build — visual workflows/activities/selectors) · ORCHESTRATOR (deploy/schedule/QUEUES/assets+credentials/monitor/govern) · ROBOTS (attended vs unattended)", 7.3, 400, "#374151"),
        Line("Document Understanding + Communications Mining (Specialized AI) · Process/Task Mining + Automation Hub (discover) · Test Suite/Cloud · Autopilot/Agent Builder (agentic)", 7.3, 400, "#374151"),
    ])

    c.raw('<text x="40" y="392" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'LEGACY: UiRPA (RPA Associate) + UiARD (Advanced RPA Developer), retired 2023, EXPIRE 15 Oct 2026 -> migrate to Automation Developer Associate / Professional.</text>')
    c.raw('<text x="40" y="411" font-size="9.5" font-weight="400" fill="#166534">'
          'Automation Developer Associate exam is PUBLIC (60 multiple-choice + multi-select questions); other exam mechanics point at the exam descriptions / UiPath Academy.</text>')
    c.raw('<text x="40" y="430" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: role/level reading · legacy migration · RPA-vs-agent · robot/agent/human orchestration · platform flow · robust selectors · retry-vs-route ·</text>')
    c.raw('<text x="40" y="447" font-size="9.5" font-weight="400" fill="#374151">'
          'attended-vs-unattended · queue throughput · IDP confidence + straight-through processing · ROI-based process prioritization · robot least-privilege · regression testing.</text>')

    c.legend(40, 478, [
        ("alt", "Developer / structure"),
        ("data", "Role certifications"),
        ("neutral", "Program shape"),
        ("mgmt", "Platform / shift"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
