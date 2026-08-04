#!/usr/bin/env python3
"""Volume CXXVIII (ISA/IEC 62443 Certification Tracks) program map.

Chapter 1: the ISA/IEC 62443 Cybersecurity Certificate Program — a
mandatory Fundamentals Specialist gate (IC32), then Risk Assessment
(IC33), Design (IC34), and Maintenance (IC37) specialists in any order,
mapped to the IACS security lifecycle (Assess/Design/Maintain); all four
automatically confer the ISA/IEC 62443 Cybersecurity Expert designation.

Run from scripts/diagrams:  python3 gen_volume128.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-128-isa-iec-62443-certifications"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Program Map: ISA/IEC 62443 Cybersecurity Certificate Program",
        subtitle="Certificate 1 Fundamentals Specialist (IC32) is the mandatory gate; Risk Assessment (IC33), Design (IC34), and Maintenance (IC37) follow in any order; all four confer the Expert designation",
        svg_title="Chapter 1 program map: the ISA/IEC 62443 Cybersecurity Certificate Program",
        svg_desc="The ISA/IEC 62443 Cybersecurity Certificate Program has four certificates mapped to the "
                 "industrial automation and control systems security lifecycle. Certificate 1, Cybersecurity "
                 "Fundamentals Specialist, course IC32, is the mandatory gate covering zones and conduits, security "
                 "levels, and the seven foundational requirements. After it, in any order: Certificate 2 "
                 "Cybersecurity Risk Assessment Specialist, course IC33, the Assess phase; Certificate 3 "
                 "Cybersecurity Design Specialist, course IC34, the Design phase; and Certificate 4 Cybersecurity "
                 "Maintenance Specialist, course IC37, the Operate and Maintain phase. Earning all four "
                 "automatically confers the ISA/IEC 62443 Cybersecurity Expert designation, with no separate exam. "
                 "The credentials do not expire. Everything is grounded in the IEC 62443 standard family, and the "
                 "volume models zones, conduits, security levels, and risk scoring with free Linux primitives.")

    c.node_box(300, 42, 360, 42, "mgmt", [
        Line("IEC 62443 standard family (1-x / 2-x / 3-x / 4-x)", 10, 700, "#111827"),
        Line("credentials do not expire · standard evolves — re-read editions", 8.5, 400, "#374151"),
    ])

    # the mandatory gate
    c.node_box(340, 120, 280, 52, "neutral", [
        Line("Certificate 1 — Fundamentals Specialist", 10, 700, "#111827"),
        Line("course IC32 · MANDATORY GATE", 8.5, 700, "#166534"),
    ])

    # the three lifecycle specialists
    def spec(x, cert, course, phase):
        c.node_box(x, 220, 280, 52, "alt", [
            Line(cert, 9.5, 700, "#111827"),
            Line(f"course {course} · {phase}", 8.5, 400, "#374151"),
        ])
        c.connector(480, 172, x + 140, 220, "alt", label="", label_pos=(0, 0))

    spec(30,  "Cert 2 — Risk Assessment", "IC33", "Assess")
    spec(340, "Cert 3 — Design", "IC34", "Design")
    spec(650, "Cert 4 — Maintenance", "IC37", "Operate/Maintain")

    c.node_box(300, 320, 360, 44, "data", [
        Line("ISA/IEC 62443 Cybersecurity Expert", 10.5, 700, "#111827"),
        Line("automatic on all four certificates — no separate exam", 8.5, 400, "#374151"),
    ])
    c.connector(170, 272, 400, 320, "data", label="", label_pos=(0, 0))
    c.connector(480, 272, 480, 320, "data", label="", label_pos=(0, 0))
    c.connector(790, 272, 560, 320, "data", label="", label_pos=(0, 0))

    c.raw('<text x="30" y="405" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'OT priority inversion: availability &amp; safety outrank confidentiality (A-I-C) — every control decision follows from it</text>')
    c.raw('<text x="30" y="424" font-size="9.5" font-weight="400" fill="#374151">'
          'Core mechanics: zones + conduits, security levels (SL 0-4) as a vector over FR1-FR7 — modeled free on Linux (namespaces/nftables/python)</text>')

    c.legend(30, 450, [
        ("neutral", "Mandatory Fundamentals gate"),
        ("alt", "Lifecycle specialist (any order)"),
        ("data", "Expert (all four)"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
