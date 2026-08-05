#!/usr/bin/env python3
"""Volume CXLVI (Jamf) certification-ladder map.

Chapter 1: the three product tracks (Jamf Pro 100/200/300/400, Jamf School
140/240, Jamf Protect 170/270/370), the escalating exam format (MC -> practical
-> scenario), and the Apple-management platform beneath. The Jamf 100 specifics
($100, 50 MC, no expiry) are public; 200-400 mechanics are portal-gated.

Run from scripts/diagrams:  python3 gen_volume146.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-146-jamf-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Jamf Certification Tracks",
        subtitle="three tracks (Pro / School / Protect) · exam format ESCALATES with level · Jamf 100 public · 200-400 portal-gated",
        svg_title="Chapter 1 program map: the Jamf certification ladder across three product tracks",
        svg_desc="Jamf's certification program runs three product tracks over an ascending exam-format "
                 "ladder. The Jamf Pro track, for Apple device management, is the flagship: Jamf 100, a "
                 "self-paced course, leads to Jamf Certified Associate; Jamf 200, instructor-led, to Jamf "
                 "Certified Tech; Jamf 300 to Jamf Certified Admin; and Jamf 400 to Jamf Certified Expert. "
                 "The Jamf School track, for education, runs Jamf 140 to Certified Associate and Jamf 240 "
                 "to Certified Tech. The Jamf Protect track, for Apple endpoint security, runs Jamf 170 to "
                 "Certified Associate, Jamf 270 to Certified Tech, and Jamf 370 to Certified Admin. The "
                 "numbering encodes both level and track: the leading digit is the level, one through four, "
                 "and the middle digit marks the track, zero for Pro, four for School, seven for Protect, so "
                 "that 370 reads as Protect Admin. The exam format escalates deliberately with the level: "
                 "Associate courses use multiple-choice questions and test knowledge; Tech courses add "
                 "practical tasks and test whether you can do it; Admin courses use graded scenarios and "
                 "practical tasks and test judgment; and the Expert course is scenario-based and tests "
                 "design and troubleshooting. The Jamf 100 exam is public: one hundred US dollars, fifty "
                 "multiple-choice questions, and the Associate certification does not expire, while the 200 "
                 "through 400 certifications carry a three-year validity; per-exam passing scores and exact "
                 "durations for the instructor-led courses are behind the training portal. The platform "
                 "beneath is Jamf Pro for mobile device management on Apple's MDM framework, Jamf Connect "
                 "for cloud identity at the Mac login window, Jamf Protect for endpoint security, and Jamf "
                 "School for education, positioning Jamf as the Apple-in-enterprise specialist against the "
                 "cross-platform generalists such as Microsoft Intune.")

    c.node_box(170, 42, 620, 44, "mgmt", [
        Line("JAMF — the APPLE-IN-ENTERPRISE management specialist", 10.5, 700, "#111827"),
        Line("deeper on Apple's framework than a cross-platform generalist (Intune XXXVII) can go", 8, 400, "#374151"),
    ])

    # three track columns
    c.node_box(40, 120, 300, 150, "alt", [
        Line("JAMF PRO track — device management", 9.5, 700, "#111827"),
        Line("(the flagship)", 7.5, 400, "#374151"),
        Line("100  self-paced   → Associate", 8.5, 700, "#166534"),
        Line("200  instructor   → Tech", 8.5, 400, "#374151"),
        Line("300  instructor   → Admin", 8.5, 400, "#374151"),
        Line("400  instructor   → Expert", 8.5, 400, "#374151"),
    ])
    c.node_box(360, 120, 250, 150, "data", [
        Line("JAMF SCHOOL track — education", 9.5, 700, "#111827"),
        Line("(shared iPads, classroom)", 7.5, 400, "#374151"),
        Line("140  self-paced   → Associate", 8.5, 700, "#166534"),
        Line("240  instructor   → Tech", 8.5, 400, "#374151"),
        Line("", 8.5, 400, "#374151"),
        Line("same Apple base, a SECTOR workflow", 7.5, 400, "#374151"),
    ])
    c.node_box(630, 120, 290, 150, "data", [
        Line("JAMF PROTECT track — endpoint security", 9, 700, "#111827"),
        Line("(defensive: telemetry, prevention)", 7.5, 400, "#374151"),
        Line("170  self-paced   → Associate", 8.5, 700, "#166534"),
        Line("270  instructor   → Tech", 8.5, 400, "#374151"),
        Line("370  instructor   → Admin", 8.5, 400, "#374151"),
        Line("a DIFFERENT product, its own ladder", 7.5, 400, "#374151"),
    ])

    c.node_box(40, 286, 880, 30, "neutral", [
        Line("NUMBERING: leading digit = LEVEL (1/2/3/4) · middle digit = TRACK (x0x=Pro · x4x=School · x7x=Protect)  →  '370' = Protect Admin", 8.5, 700, "#111827"),
    ])

    # escalating format band
    c.node_box(40, 336, 880, 48, "alt", [
        Line("★ EXAM FORMAT ESCALATES WITH LEVEL — the honest signal of what each rung validates", 8.5, 700, "#111827"),
        Line("Associate = multiple choice (KNOWLEDGE) · Tech = MC + practical tasks (CAN YOU DO IT) · Admin = graded scenarios (JUDGMENT) · Expert = scenario-based (DESIGN)", 7.5, 400, "#374151"),
    ])

    # platform
    c.node_box(40, 404, 880, 50, "mgmt", [
        Line("PLATFORM (all on Apple's MDM framework — cooperative, not coercive)", 8.5, 700, "#111827"),
        Line("JAMF PRO (enrollment · Smart Groups · profiles · policies · patch · Self Service) · JAMF CONNECT (cloud identity + password sync at the Mac login)", 7.5, 400, "#374151"),
        Line("JAMF PROTECT (Endpoint Security framework · telemetry · threat prevention · CIS compliance) · JAMF SCHOOL (shared devices · classroom workflows)", 7.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="478" font-size="9.5" font-weight="700" fill="#166534">'
          'Jamf 100 is PUBLIC: USD 100 · 50 multiple-choice questions · Associate certification does NOT expire (200-400 carry a 3-year validity).</text>')
    c.raw('<text x="40" y="497" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Per-exam passing scores and exact durations for the instructor-led 200-400 courses are portal-gated; instructor-led pricing is arranged, not listed — the volume asserts neither.</text>')
    c.raw('<text x="40" y="516" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: ladder-by-format · track-by-job · MDM boundaries (cooperative≠coercive) · ADE zero-touch · imperative vs declarative (DDM) · Smart Groups vs static ·</text>')
    c.raw('<text x="40" y="533" font-size="9.5" font-weight="400" fill="#374151">'
          'scope pre-flight · extension attributes · profiles vs policies · patch compliance · Self Service push-vs-offer · script piloting · password drift · shared-device lifecycle · CIS mapping.</text>')

    c.legend(40, 556, [
        ("alt", "Self-paced / structure"),
        ("data", "Instructor-led / paid"),
        ("neutral", "Numbering key"),
        ("mgmt", "Apple platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-ladder.svg")


if __name__ == "__main__":
    ch01()
