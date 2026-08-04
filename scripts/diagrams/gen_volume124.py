#!/usr/bin/env python3
"""Volume CXXIV (Linux Foundation + LPI Certification Tracks) program map.

Chapter 1: the two vendor-neutral Linux programs. LPI's Essentials tier +
LPIC-1/2/3 ladder + Open Technology track (weighted public objectives,
5-year professional validity), and the Linux Foundation's LFCA + the
performance-based LFCS (2-year), with LFCT inactive.

Run from scripts/diagrams:  python3 gen_volume124.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-124-linux-certifications"


def ch01():
    c = Canvas(960, 520,
        title="Chapter 1 Program Map: Vendor-Neutral Linux Certifications (LPI + Linux Foundation)",
        subtitle="LPI's Essentials + LPIC-1/2/3 ladder + Open Technology track (weighted public objectives, 5-yr) and the Linux Foundation's LFCA + performance-based LFCS (2-yr); LFCT inactive",
        svg_title="Chapter 1 program map: the two vendor-neutral Linux certification programs",
        svg_desc="Two vendor-neutral Linux certification programs. LPI, the Linux Professional Institute, has an "
                 "Essentials tier with lifetime validity: Linux Essentials exam 010, Security Essentials 020, Web "
                 "Development Essentials 030, and Open Source Essentials 050. Its professional ladder, five-year "
                 "validity, runs LPIC-1 with exams 101-500 and 102-500, then LPIC-2 with exams 201-450 and 202-450 "
                 "requiring an active LPIC-1, then four LPIC-3 specialties requiring an active LPIC-2: 300 Mixed "
                 "Environments, 303 Security, 305 Virtualization and Containerization, and 306 High Availability "
                 "and Storage Clusters. The Open Technology track has DevOps Tools Engineer exam 701 and BSD "
                 "Specialist exam 702. The Linux Foundation has the multiple-choice LFCA Certified IT Associate and "
                 "the performance-based LFCS Certified System Administrator, with five weighted domains, two-year "
                 "validity; the LFCT Cloud Technician certification is inactive. Every lab in the volume is runnable "
                 "on free standard Linux.")

    # LPI column
    c.node_box(35, 60, 560, 34, "mgmt", [Line("LPI (Linux Professional Institute) — public weighted objectives", 10, 700, "#111827")])
    c.node_box(35, 108, 560, 40, "neutral", [
        Line("Essentials (lifetime): Linux 010 · Security 020 · Web Dev 030 · Open Source 050", 9, 400, "#374151"),
    ])
    c.node_box(35, 162, 175, 46, "alt", [Line("LPIC-1", 11, 700, "#111827"), Line("101-500 + 102-500 (v5.0)", 8, 400, "#374151")])
    c.node_box(230, 162, 175, 46, "alt", [Line("LPIC-2", 11, 700, "#111827"), Line("201-450 + 202-450 (v4.5)", 8, 400, "#374151")])
    c.node_box(425, 162, 170, 46, "alt", [Line("LPIC-3 (x4)", 11, 700, "#111827"), Line("300·303·305·306", 8, 400, "#374151")])
    c.connector(210, 185, 230, 185, "alt", label="", label_pos=(0, 0))
    c.connector(405, 185, 425, 185, "alt", label="", label_pos=(0, 0))
    c.node_box(35, 222, 560, 34, "data", [Line("Open Technology (5-yr): DevOps Tools Engineer 701 · BSD Specialist 702", 9, 700, "#111827")])

    # Linux Foundation column
    c.node_box(630, 60, 295, 34, "mgmt", [Line("Linux Foundation", 10, 700, "#111827")])
    c.node_box(630, 108, 295, 40, "neutral", [
        Line("LFCA — Certified IT Associate", 10, 700, "#111827"),
        Line("60 MCQ · pre-professional breadth", 8, 400, "#374151"),
    ])
    c.node_box(630, 162, 295, 60, "data", [
        Line("LFCS — Certified System Administrator", 9.5, 700, "#111827"),
        Line("performance-based · 2 hrs · 2-yr validity", 8, 400, "#374151"),
        Line("Ops 25 · Net 25 · Storage 20 · Cmds 20 · Users 10", 7.5, 400, "#166534"),
    ])
    c.node_box(630, 236, 295, 20, "warn", [Line("LFCT (Cloud Technician) — INACTIVE", 8.5, 700, "#7f1d1d")])

    c.raw('<text x="35" y="300" font-size="9.5" font-weight="700" fill="#1d4ed8">'
          'Two philosophies: LPI tests knowledge from weighted public objectives; LFCS tests doing, in a live terminal</text>')
    c.raw('<text x="35" y="320" font-size="9.5" font-weight="400" fill="#374151">'
          'Chaining: LPIC-2 needs active LPIC-1, LPIC-3 needs active LPIC-2 · every lab runs free on any Linux machine</text>')

    c.legend(35, 345, [
        ("alt", "LPI professional ladder (5-yr)"),
        ("data", "Top credentials / performance-based"),
        ("warn", "Inactive — do not target"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
