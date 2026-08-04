#!/usr/bin/env python3
"""Volume CXXVI (Aviatrix Certification Tracks) program map.

Chapter 1: the Aviatrix Certified Engineer (ACE) program — a free
self-paced ACE Associate (multicloud networking foundations) gating the
instructor-led ACE Professional (transit/HA, egress, firewall insertion,
connectivity) and the ACE Design Expert capstone, plus focused ACE
courses (Security, Hybrid Cloud, Cloud Backbone, Automation, Operations),
all over the Aviatrix Controller + CoPilot + gateway overlay.

Run from scripts/diagrams:  python3 gen_volume126.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-126-aviatrix-certifications"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Program Map: Aviatrix Certified Engineer (ACE) Program",
        subtitle="Free self-paced ACE Associate gates the instructor-led ACE Professional and the ACE Design Expert capstone, plus focused courses — all over the Aviatrix overlay (Controller + CoPilot + gateways)",
        svg_title="Chapter 1 program map: the Aviatrix Certified Engineer (ACE) program",
        svg_desc="The Aviatrix Certified Engineer program has a free, self-paced ACE Associate covering multicloud "
                 "networking foundations across AWS, Azure, Google Cloud, and OCI; it is the mandatory prerequisite "
                 "for the instructor-led ACE Professional, which is hands-on across multicloud transit and high "
                 "availability, egress security, firewall insertion, and secure user and site connectivity. The ACE "
                 "Design Expert is the capstone for designing scalable resilient multicloud networks. Focused ACE "
                 "courses add depth: Security, Hybrid Cloud, Cloud Backbone, Automation with Terraform, and "
                 "Operations with CoPilot. Everything runs over the Aviatrix overlay: a central Controller as the "
                 "control plane, CoPilot for observability, and gateways forming transit and spoke topology with "
                 "FireNet firewall insertion and Distributed Cloud Firewall segmentation. The ACE Associate needs "
                 "no cloud accounts, so the volume's labs run free on Linux primitives.")

    # the overlay band
    c.node_box(45, 42, 870, 40, "mgmt", [
        Line("Aviatrix overlay: Controller (control plane) + CoPilot (observability) + gateways over AWS / Azure / GCP / OCI", 9.5, 700, "#111827"),
    ])

    # the ladder
    c.node_box(45, 120, 260, 56, "neutral", [
        Line("ACE Associate  (FREE, self-paced)", 10, 700, "#111827"),
        Line("multicloud networking foundations", 8.5, 400, "#374151"),
        Line("mandatory prerequisite", 8, 700, "#166534"),
    ])
    c.node_box(350, 120, 260, 56, "alt", [
        Line("ACE Professional  (instructor-led)", 10, 700, "#111827"),
        Line("transit/HA · egress · FireNet · connectivity", 8.5, 400, "#374151"),
        Line("hands-on labs", 8, 400, "#374151"),
    ])
    c.node_box(655, 120, 260, 56, "data", [
        Line("ACE Design Expert", 10, 700, "#111827"),
        Line("scalable, resilient", 8.5, 400, "#374151"),
        Line("multicloud design (capstone)", 8, 400, "#374151"),
    ])
    c.connector(305, 148, 350, 148, "alt", label="", label_pos=(0, 0))
    c.connector(610, 148, 655, 148, "data", label="", label_pos=(0, 0))

    # focused courses
    c.node_box(45, 210, 870, 40, "neutral", [
        Line("Focused ACE courses: Security · Hybrid Cloud · Cloud Backbone · Automation (Terraform) · Operations (CoPilot)", 9, 400, "#374151"),
    ])

    c.raw('<text x="45" y="300" font-size="9.5" font-weight="700" fill="#1d4ed8">'
          'The overlay solves native multicloud pain: route-table limits, overlapping CIDRs, inconsistent transit (TGW/vWAN/NCC/DRG)</text>')
    c.raw('<text x="45" y="320" font-size="9.5" font-weight="400" fill="#374151">'
          'Associate needs no cloud accounts — every lab in this volume runs free on Linux (namespaces / nftables / FRR / WireGuard / Terraform)</text>')

    c.legend(45, 350, [
        ("neutral", "Free / self-paced tier"),
        ("alt", "Instructor-led Professional"),
        ("data", "Design Expert capstone"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
