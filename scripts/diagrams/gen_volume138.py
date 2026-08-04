#!/usr/bin/env python3
"""Volume CXXXVIII (Everpure, formerly Pure Storage) program map.

Chapter 1: the twelve IT Professional Certifications across four levels
(Associate $200, Professional $300, Specialist $300, Expert $400),
proctored closed-book multiple choice, three-year validity, with the DSA
auto-renewal and CEE credit recertification paths — plus the Pure Storage
to Everpure rebrand.

Run from scripts/diagrams:  python3 gen_volume138.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-138-everpure-purestorage-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: Everpure (formerly Pure Storage) Certification",
        subtitle="12 certifications across 4 levels · $200/$300/$400 · online proctored, closed book · valid 3 years · DSA auto-renews",
        svg_title="Chapter 1 program map: the Everpure IT Professional Certification program",
        svg_desc="Everpure, the company formerly known as Pure Storage, offers twelve IT Professional "
                 "Certifications across four levels through Everpure Academy. The Associate level has one "
                 "certification, Data Storage, at 200 US dollars. The Professional level has four at 300 dollars "
                 "each: FlashArray Storage, FlashBlade Storage, Portworx Enterprise, and Cyber Resilience. The "
                 "Specialist level has six at 300 dollars each: FlashArray Implementation, FlashBlade "
                 "Implementation, FlashArray Support, FlashBlade Support, Cloud, and Migration. The Expert level "
                 "has one, Platform Architect, at 400 dollars. All exams are multiple choice, delivered online and "
                 "proctored with a webcam, and are closed book with no external materials permitted. Training is "
                 "not required because each exam is designed to test on-the-job experience. Certifications are "
                 "valid for three years and renewed by retaking the updated exam; additionally the Associate Data "
                 "Storage certification renews automatically when any higher certification is earned, and "
                 "Continuing Everpure Education credits apply to selected FlashArray exams. Badges issue through "
                 "Credly. The rebrand is partial: the company and certifications are now Everpure, while the "
                 "FlashArray, FlashBlade, Portworx, and Evergreen product names are unchanged, the conference "
                 "remains Pure Accelerate, and the academy is still hosted at academy.purestorage.com.")

    c.node_box(200, 42, 560, 46, "mgmt", [
        Line("Everpure, Inc. — formerly PURE STORAGE", 10.5, 700, "#111827"),
        Line("company + certifications renamed; FlashArray/FlashBlade/Portworx/Evergreen unchanged", 8.5, 400, "#374151"),
        Line("academy still hosted at academy.purestorage.com — an old-looking URL that is current", 8, 400, "#374151"),
    ])

    # four levels
    c.node_box(40, 132, 200, 62, "neutral", [
        Line("ASSOCIATE   $200", 9.5, 700, "#111827"),
        Line("Data Storage (DSA)", 8.5, 400, "#374151"),
        Line("auto-renews when you", 7.5, 400, "#166534"),
        Line("earn any higher cert", 7.5, 400, "#166534"),
    ])
    c.node_box(250, 132, 230, 62, "data", [
        Line("PROFESSIONAL   $300", 9.5, 700, "#111827"),
        Line("FlashArray Storage", 7.5, 400, "#374151"),
        Line("FlashBlade Storage", 7.5, 400, "#374151"),
        Line("Portworx · Cyber Resilience", 7.5, 400, "#374151"),
    ])
    c.node_box(490, 132, 240, 62, "data", [
        Line("SPECIALIST   $300", 9.5, 700, "#111827"),
        Line("FlashArray/Blade Implementation", 7, 400, "#374151"),
        Line("FlashArray/Blade Support", 7.5, 400, "#374151"),
        Line("Cloud · Migration", 7.5, 400, "#374151"),
    ])
    c.node_box(740, 132, 180, 62, "alt", [
        Line("EXPERT   $400", 9.5, 700, "#111827"),
        Line("Platform Architect", 8.5, 400, "#374151"),
        Line("designs whole", 7.5, 400, "#374151"),
        Line("solutions", 7.5, 400, "#374151"),
    ])
    c.connector(240, 163, 250, 163, "data", label="", label_pos=(0, 0))
    c.connector(480, 163, 490, 163, "data", label="", label_pos=(0, 0))
    c.connector(730, 163, 740, 163, "alt", label="", label_pos=(0, 0))

    # products band
    c.node_box(40, 214, 880, 40, "mgmt", [
        Line("Products: FlashArray (block) · FlashBlade (file + object) · FlashBlade//EXA (AI/HPC) · Portworx (Kubernetes) · Evergreen//One (as-a-service)", 8.5, 400, "#374151"),
    ])

    # mechanics
    c.node_box(40, 268, 880, 56, "neutral", [
        Line("Exam mechanics: multiple choice · ONLINE PROCTORED (webcam) · CLOSED BOOK — no external materials", 8.5, 700, "#111827"),
        Line("Training NOT required: \"each exam is designed to test your on-the-job experience\" · Credly badges", 8.5, 400, "#374151"),
        Line("Valid 3 YEARS — retake the updated exam, OR: DSA auto-renews · CEE credits (SELECT FlashArray exams only)", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="358" font-size="9.5" font-weight="700" fill="#166534">'
          'Note the Specialist split: IMPLEMENTATION (deploying) vs SUPPORT (diagnosing) are different jobs — choose the one that matches your work.</text>')
    c.raw('<text x="40" y="377" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: upgrade sequencing &amp; controller headroom · volume/host mapping · file-vs-object · reduction ratios · RPO &amp; the speed of light · immutability vs dwell time · K8s PVs.</text>')

    c.legend(40, 408, [
        ("neutral", "Associate / mechanics"),
        ("data", "Professional / Specialist"),
        ("alt", "Expert"),
        ("mgmt", "Company & products"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
