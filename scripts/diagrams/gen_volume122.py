#!/usr/bin/env python3
"""Volume CXXII (Citrix Certification Tracks) program map.

Chapter 1: the current Citrix program under Cloud Software Group — the
Virtualization track (CCA-V -> CCP-V) and the App Delivery and Security
track (CCA-AppDS via either of two exams -> CCP-AppDS 1Y0-342), delivered
on Webassessor, with the Expert tier discontinued and an announced
program overhaul in progress.

Run from scripts/diagrams:  python3 gen_volume122.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-122-citrix-certifications"


def ch01():
    c = Canvas(960, 470,
        title="Chapter 1 Program Map: Citrix Certifications under Cloud Software Group",
        subtitle="Two tracks, five exams, no Expert tier — Webassessor delivery, ~10% performance-based items on AppDS forms, and an announced program overhaul in progress",
        svg_title="Chapter 1 program map: the current Citrix certification program",
        svg_desc="The Citrix certification program under Cloud Software Group has two tracks. The Virtualization "
                 "track: CCA-V, whose exam Citrix Virtual Apps and Desktops Administration replaced the retired "
                 "1Y0-204, leads to CCP-V, Citrix Virtual Apps and Desktops 7 Advanced Administration. The App "
                 "Delivery and Security track: CCA-AppDS is one credential with two exam options, NetScaler 14.x "
                 "Essentials and NetScaler Gateway, or Deploy and Manage Citrix ADC 14.x with Traffic Management; "
                 "either leads to CCP-AppDS, exam 1Y0-342 NetScaler Advanced Topics covering Web App Firewall, "
                 "nFactor authentication, and NetScaler Console. Exams are delivered on Webassessor by Kryterion. "
                 "The Expert tier, CCE-V and CCE-N, is discontinued, and the program is under an announced "
                 "comprehensive overhaul with additional certifications planned.")

    c.node_box(280, 42, 400, 42, "mgmt", [
        Line("Cloud Software Group — Webassessor (Kryterion) delivery", 10.5, 700, "#111827"),
        Line("program overhaul announced: re-verify before scheduling", 9, 400, "#374151"),
    ])

    # Virtualization track
    c.node_box(60, 130, 380, 40, "alt", [
        Line("Virtualization track (Citrix Virtual Apps and Desktops)", 10, 700, "#111827"),
    ])
    c.node_box(60, 195, 380, 56, "neutral", [
        Line("CCA-V — CVAD Administration", 10.5, 700, "#111827"),
        Line("replaces retired 1Y0-204 · ~60-65 Q · 90 min · ~65%", 8.5, 400, "#374151"),
    ])
    c.node_box(60, 285, 380, 56, "data", [
        Line("CCP-V — CVAD 7 Advanced Administration", 10.5, 700, "#111827"),
        Line("prerequisite: CCA-V · 60-70 Q · 64% pass", 8.5, 400, "#374151"),
    ])
    c.connector(250, 251, 250, 285, "neutral", label="", label_pos=(0, 0))

    # AppDS track
    c.node_box(520, 130, 380, 40, "alt", [
        Line("App Delivery and Security track (NetScaler 14.x)", 10, 700, "#111827"),
    ])
    c.node_box(520, 195, 380, 56, "neutral", [
        Line("CCA-AppDS — one credential, two exam options", 10.5, 700, "#111827"),
        Line("Gateway  · or ·  Traffic Management (CLI sims)", 8.5, 400, "#374151"),
    ])
    c.node_box(520, 285, 380, 56, "data", [
        Line("CCP-AppDS — 1Y0-342 NetScaler Advanced Topics", 10.5, 700, "#111827"),
        Line("WAF · nFactor · NetScaler Console · prereq: either CCA", 8.5, 400, "#374151"),
    ])
    c.connector(710, 251, 710, 285, "neutral", label="", label_pos=(0, 0))

    c.raw('<text x="60" y="380" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'Retired: Expert tier (CCE-V, CCE-N) · 1Y0-204 · the old exam-code system (1Y0-342 is the last)</text>')
    c.raw('<text x="60" y="400" font-size="9.5" font-weight="400" fill="#374151">'
          'AppDS forms: ~10% performance-based items — lab hours at the NetScaler CLI (free on CPX Express)</text>')

    c.legend(60, 425, [
        ("neutral", "Associate level"),
        ("data", "Professional level (top of ladder)"),
        ("mgmt", "Program / delivery platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
