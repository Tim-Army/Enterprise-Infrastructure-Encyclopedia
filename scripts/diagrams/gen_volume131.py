#!/usr/bin/env python3
"""Volume CXXXI (Practical Offensive & Defensive Certification Tracks) program map.

Chapter 1: the three practical, hands-on providers — Hack The Box (HTB
Academy), TCM Security, and INE Security (formerly eLearnSecurity) — whose
common model is a real exam lab plus a professional report, not
multiple-choice. Each spans offensive, defensive/blue-team, and the newest
AI/LLM tracks. The volume is defensive: offensive technique is presented to
be understood, detected, prevented, and reported, in an authorized,
in-scope, educational context only.

Run from scripts/diagrams:  python3 gen_volume131.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-131-practical-offensive-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: Practical Certifications (HTB · TCM · INE)",
        subtitle="Three providers, one model — a real exam lab plus a professional report; each spans offensive, defensive/blue, and AI tracks; authorization governs everything",
        svg_title="Chapter 1 program map: the practical certification providers HTB, TCM, and INE",
        svg_desc="This volume maps three practical, hands-on security certification providers whose shared model is "
                 "certification by working a real exam lab, a network, web application, Active Directory domain, or "
                 "SOC scenario, and writing a professional report, rather than answering multiple-choice questions. "
                 "Hack The Box, through HTB Academy, offers offensive certifications such as CPTS, CWES, CWEE, CAPE, "
                 "and CJCA, the defensive CDSA, and the AI-focused COAE co-developed with Google. TCM Security offers "
                 "the offensive PJPT, PNPT, PWPx, PORP, PMRP, PIPA, and PMPA, the blue-team PSAA, PSAP, and PHDA, and "
                 "the AI-focused PAPA. INE Security, formerly eLearnSecurity, offers the offensive eJPT, eCPPT, eWPT, "
                 "eWPTX, and eMAPT, the defensive eSOC, eCIR, eCTHP, eEDA, eIAMA, and eCDFP, and the AI-focused eAIS. "
                 "The volume is written defensively: every offensive technique is presented to be understood, "
                 "detected, prevented, and reported, always in an authorized, in-scope, educational context only. "
                 "Authorization governs everything: the same skill set is a respected profession or a crime, and the "
                 "only difference is signed, in-scope permission. Labs model methodology, detection, and fixes free "
                 "in Python.")

    c.node_box(230, 42, 500, 44, "mgmt", [
        Line("Practical, hands-on certification — prove it by doing", 10.5, 700, "#111827"),
        Line("a real exam lab (network / web / AD / SOC) + a professional report, not multiple-choice", 8.5, 400, "#374151"),
    ])

    # three providers
    c.node_box(40, 130, 280, 46, "data", [
        Line("Hack The Box (HTB Academy)", 10, 700, "#111827"),
        Line("module-rich, job-role mapped", 8.5, 400, "#374151"),
    ])
    c.node_box(340, 130, 280, 46, "data", [
        Line("TCM Security", 10, 700, "#111827"),
        Line("affordable, scenario-realistic", 8.5, 400, "#374151"),
    ])
    c.node_box(640, 130, 280, 46, "data", [
        Line("INE Security (eLearnSecurity)", 10, 700, "#111827"),
        Line("subscription + hand-graded exams", 8.5, 400, "#374151"),
    ])
    c.connector(480, 86, 180, 130, "data", label="", label_pos=(0, 0))
    c.connector(480, 86, 480, 130, "data", label="", label_pos=(0, 0))
    c.connector(480, 86, 780, 130, "data", label="", label_pos=(0, 0))

    # offensive row
    c.node_box(40, 220, 880, 44, "alt", [
        Line("OFFENSIVE (understood to defend): HTB CPTS/CWES/CWEE/CAPE/CJCA · TCM PJPT/PNPT/PWPx/PORP/PIPA/PMPA · INE eJPT/eCPPT/eWPT/eWPTX/eMAPT", 8.5, 700, "#111827"),
        Line("reconnaissance -> methodology -> network/AD -> web app — always authorized, in-scope, lab-only", 8, 400, "#374151"),
    ])
    # defensive row
    c.node_box(40, 280, 880, 44, "neutral", [
        Line("DEFENSIVE / BLUE TEAM: HTB CDSA · TCM PSAA/PSAP/PHDA · INE eSOC/eCIR/eCTHP/eEDA/eIAMA/eCDFP", 8.5, 700, "#111827"),
        Line("SOC detection -> incident response -> threat hunting -> forensics", 8, 400, "#374151"),
    ])
    # AI row
    c.node_box(40, 340, 880, 44, "mgmt", [
        Line("AI / LLM SECURITY (newest, both sides): HTB COAE (with Google) · TCM PAPA · INE eAIS", 8.5, 700, "#111827"),
        Line("prompt injection · output handling · agentic guardrails — OWASP LLM Top 10 as a defender's checklist", 8, 400, "#374151"),
    ])

    c.raw('<text x="40" y="428" font-size="10" font-weight="700" fill="#991b1b">'
          'Authorization governs everything: the same skill set is a profession or a crime — the only difference is signed, in-scope permission.</text>')
    c.raw('<text x="40" y="448" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: attack-path graphs to defend · detection rules · IR timelines · secure coding · report structure — never operational tooling against real targets.</text>')

    c.legend(40, 476, [
        ("data", "Providers"),
        ("alt", "Offensive (to defend)"),
        ("neutral", "Defensive / blue"),
        ("mgmt", "AI/LLM security"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
