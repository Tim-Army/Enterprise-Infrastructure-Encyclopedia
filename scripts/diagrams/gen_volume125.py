#!/usr/bin/env python3
"""Volume CXXV (Red Hat Certification Tracks) program map.

Chapter 1: Red Hat's 2026 restructure — five tracks (Enterprise Linux,
Ansible, OpenShift, Cloud-Native, AI) across five levels (Technologist,
Systems Administrator/Developer, Engineer, Specialist, Architect), all
performance-based. RHCSA EX200 (RHEL 10) is the shared foundation; RHCA
is now track-specific.

Run from scripts/diagrams:  python3 gen_volume125.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-125-red-hat-certifications"


def ch01():
    c = Canvas(960, 520,
        title="Chapter 1 Program Map: Red Hat Certifications (2026 five-track restructure)",
        subtitle="Five tracks x five levels, all 100% performance-based; RHCSA EX200 (RHEL 10) is the shared foundation and RHCA is now track-specific",
        svg_title="Chapter 1 program map: the Red Hat certification program restructured for 2026",
        svg_desc="Red Hat's 2026 certification program has five tracks — Enterprise Linux, Ansible, OpenShift, "
                 "Cloud-Native Applications, and a new provisional AI track — across five progressive levels: "
                 "Technologist, Systems Administrator or Developer, Engineer, Specialist electives, and Architect. "
                 "Every exam is 100 percent performance-based on live systems. RHCSA, exam EX200, now based on RHEL "
                 "10, is the shared Level 2 foundation and the RHCE prerequisite. RHCE, exam EX294, is the Ansible "
                 "track Engineer exam; EX342 is the Enterprise Linux Engineer exam; the OpenShift track runs EX180 "
                 "to EX280 on OpenShift 4.18 to EX380; Cloud-Native runs EX188 to EX288. The 2026 change is a "
                 "track-specific RHCA: an Administrator exam plus an Engineer exam plus three Specialist electives "
                 "within the same track, replacing the old any-five-specialists rule. EX318 virtualization is "
                 "retired in favor of EX316 OpenShift Virtualization, and renewal offers retake, level up, or "
                 "advance. All labs run free on a Red Hat Developer subscription, AlmaLinux or Rocky, and CRC.")

    c.node_box(250, 42, 460, 42, "mgmt", [
        Line("Red Hat certification program — 100% performance-based", 10.5, 700, "#111827"),
        Line("RHCSA EX200 (RHEL 10) = shared Level-2 foundation & RHCE prerequisite", 8.5, 400, "#374151"),
    ])

    tracks = [
        (35,  "Enterprise Linux", "EX342 Engineer"),
        (220, "Ansible", "EX294 RHCE"),
        (405, "OpenShift", "EX280 -> EX380"),
        (590, "Cloud-Native", "EX188 -> EX288"),
        (775, "AI (provisional)", "codes pending"),
    ]
    for x, name, eng in tracks:
        c.node_box(x, 130, 170, 30, "alt", [Line(name, 9.5, 700, "#111827")])
        c.node_box(x, 168, 170, 40, "neutral", [
            Line("L3 Engineer", 8.5, 700, "#111827"),
            Line(eng, 8, 400, "#374151"),
        ])
        c.node_box(x, 216, 170, 40, "data", [
            Line("L4 Specialists", 8.5, 700, "#111827"),
            Line("x3 in-track", 8, 400, "#374151"),
        ])
        c.connector(x + 85, 160, x + 85, 168, "neutral", label="", label_pos=(0, 0))
        c.connector(x + 85, 208, x + 85, 216, "data", label="", label_pos=(0, 0))

    c.raw('<text x="35" y="300" font-size="9.5" font-weight="700" fill="#166534">'
          'RHCA (Level 5) = Administrator exam + Engineer exam + THREE Specialists — all within the same track (2026 rule)</text>')
    c.raw('<text x="35" y="320" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'EX318 (RHV virtualization) retired -> EX316 (OpenShift Virtualization) · renewal: retake / level up / advance</text>')
    c.raw('<text x="35" y="340" font-size="9.5" font-weight="400" fill="#374151">'
          'Every lab runs free: Red Hat Developer subscription · AlmaLinux / Rocky · CRC (OpenShift Local)</text>')

    c.legend(35, 365, [
        ("alt", "Track (5 total)"),
        ("neutral", "L3 Engineer exam"),
        ("data", "L4 Specialist electives -> RHCA"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
