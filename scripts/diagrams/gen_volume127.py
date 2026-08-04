#!/usr/bin/env python3
"""Volume CXXVII (Netskope Certification Tracks) program map.

Chapter 1: the Netskope certification program — a free vendor-agnostic
SASE Accreditation on-ramp, then NCCSA (Netskope One Administrator; exam
NSK101) and NCCSI (Netskope One Professional), all teaching the Netskope
One SASE/SSE platform (CASB + SWG + ZTNA + DLP over the NewEdge network).

Run from scripts/diagrams:  python3 gen_volume127.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-127-netskope-certifications"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Program Map: Netskope Certifications (SASE / SSE)",
        subtitle="A free vendor-agnostic SASE Accreditation on-ramp, then NCCSA (NSK101, administer) and NCCSI (integrate) on the Netskope One platform — SSE = CASB + SWG + ZTNA + DLP over NewEdge",
        svg_title="Chapter 1 program map: the Netskope certification program",
        svg_desc="The Netskope certification program has a free vendor-agnostic SASE Accreditation, an on-demand "
                 "SASE-architecture course with a 45-minute exam at 80 percent to pass and a LinkedIn badge, as the "
                 "on-ramp. Then the NCCSA, Netskope Certified Cloud Security Administrator, exam NSK101 replacing "
                 "NSK100, delivered by Pearson VUE with about 70 questions in two hours, 70 percent to pass, valid "
                 "two years, on the Netskope One Administrator course; and the NCCSI, Netskope Certified Cloud "
                 "Security Integrator, on the Netskope One Professional course for integration depth. All teach the "
                 "Netskope One SASE platform, where SASE equals SD-WAN plus SSE, and SSE equals CASB for cloud apps, "
                 "SWG for web, ZTNA for private apps, and DLP for data, delivered over the NewEdge network with one "
                 "policy engine. The volume's labs model these on free primitives.")

    # SASE framework band
    c.node_box(45, 42, 870, 40, "mgmt", [
        Line("Netskope One (SASE) = SD-WAN + SSE  |  SSE = CASB (apps) + SWG (web) + ZTNA (private) + DLP (data), over NewEdge", 9, 700, "#111827"),
    ])

    # ladder
    c.node_box(45, 120, 270, 58, "neutral", [
        Line("SASE Accreditation  (FREE)", 10, 700, "#111827"),
        Line("vendor-agnostic SASE architecture", 8.5, 400, "#374151"),
        Line("45-min exam · 80% · LinkedIn badge", 8, 400, "#374151"),
    ])
    c.node_box(355, 120, 270, 58, "alt", [
        Line("NCCSA — Administrator", 10, 700, "#111827"),
        Line("exam NSK101 · Pearson VUE", 8.5, 400, "#374151"),
        Line("70 Q · ~2 hr · 70% · valid 2 yr", 8, 400, "#374151"),
    ])
    c.node_box(665, 120, 250, 58, "data", [
        Line("NCCSI — Integrator", 10, 700, "#111827"),
        Line("SAML · API · IaaS/SSPM", 8.5, 400, "#374151"),
        Line("advanced DLP · analytics", 8, 400, "#374151"),
    ])
    c.connector(315, 149, 355, 149, "alt", label="", label_pos=(0, 0))
    c.connector(625, 149, 665, 149, "data", label="", label_pos=(0, 0))

    # the four SSE surfaces
    for x, name, sub in [(45,"CASB","cloud apps"), (265,"SWG","web + SSL"), (485,"ZTNA","private apps"), (705,"DLP","data")]:
        c.node_box(x, 215, 210, 34, "neutral", [Line(f"{name} — {sub}", 9, 400, "#374151")])

    c.raw('<text x="45" y="300" font-size="9.5" font-weight="700" fill="#1d4ed8">'
          'One policy engine, four surfaces — same identity/posture/data logic across web, SaaS, private apps, and data</text>')
    c.raw('<text x="45" y="320" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Currency: exam codes churn (NSK100 -> NSK101); SASE Accreditation free window is limited — re-verify on netskope.com</text>')

    c.legend(45, 350, [
        ("neutral", "Free / vendor-agnostic on-ramp"),
        ("alt", "NCCSA (administer)"),
        ("data", "NCCSI (integrate)"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
