#!/usr/bin/env python3
"""Volume CXXIX (OPSWAT Certification Tracks) program map.

Chapter 1: the OPSWAT Academy — a free-first Critical Infrastructure
Protection program. Vendor-neutral CIP foundation + Associate certs
(ICIP/OCFA/OFSA/OECA/ONSA/OSSA, many free) building into paid
MetaDefender product Professional certs and the OT Security Expert
designation; Credly badges + ISC2 CPE.

Run from scripts/diagrams:  python3 gen_volume129.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-129-opswat-certifications"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Program Map: OPSWAT Academy (Critical Infrastructure Protection)",
        subtitle="Free-first: vendor-neutral CIP foundation + Associate certs (many free) build into paid MetaDefender Professional certs and the OT Security Expert; Credly badges + ISC2 CPE",
        svg_title="Chapter 1 program map: the OPSWAT Academy certification program",
        svg_desc="The OPSWAT Academy is a free-first Critical Infrastructure Protection program across four "
                 "tracks: CIP Essentials, CyberOps, OPSWAT Product Training, and End-User Guides. The Associate "
                 "ladder, many of them free, is ICIP Introduction to Critical Infrastructure Protection, OCFA "
                 "Cybersecurity Fundamentals Associate, OFSA File Security Associate, OECA Endpoint Compliance "
                 "Associate, ONSA Network Security Associate, and OSSA Secure Storage Associate. These build into "
                 "the paid MetaDefender product Professional certifications, Core, ICAP, Kiosk, and MFT, and the "
                 "OPSWAT OT Security Expert designation. Badges issue on Credly with ISC2 CPE credit, and some "
                 "certifications carry a validity window. The signature technologies are Deep CDR content disarm "
                 "and reconstruction, multiscanning with many engines, endpoint posture and network access control, "
                 "and secure data transfer across boundaries via Kiosk and Vault. The volume models these free in "
                 "Python.")

    c.node_box(280, 42, 400, 42, "mgmt", [
        Line("OPSWAT Academy — free-first CIP program", 10.5, 700, "#111827"),
        Line("Credly badges · ISC2 CPE · some certs expire — verify validity", 8.5, 400, "#374151"),
    ])

    # associate tier (free)
    c.node_box(35, 120, 890, 56, "neutral", [
        Line("Associate certifications (Credly, many FREE) — vendor-neutral CIP foundation", 10, 700, "#111827"),
        Line("ICIP · OCFA (fundamentals) · OFSA (file/CDR) · OECA (endpoint) · ONSA (network) · OSSA (secure storage)", 8.5, 400, "#374151"),
    ])

    # professional + expert
    c.node_box(35, 210, 550, 56, "alt", [
        Line("MetaDefender Professional (paid ~$1,000)", 10, 700, "#111827"),
        Line("Core (multiscan+CDR+DLP hub) · ICAP (web) · Kiosk (media) · MFT (transfer)", 8.5, 400, "#374151"),
    ])
    c.node_box(620, 210, 305, 56, "data", [
        Line("OPSWAT OT Security Expert", 10, 700, "#111827"),
        Line("end-to-end CIP/OT defense", 8.5, 400, "#374151"),
        Line("(products + 62443 + OT ops)", 8, 400, "#374151"),
    ])
    c.connector(310, 176, 310, 210, "alt", label="", label_pos=(0, 0))
    c.connector(770, 176, 770, 210, "data", label="", label_pos=(0, 0))

    c.raw('<text x="35" y="305" font-size="9.5" font-weight="700" fill="#166534">'
          'Signature defenses: Deep CDR (rebuild files clean — zero-day-proof) + Multiscanning (many engines) — "trust no file, no device"</text>')
    c.raw('<text x="35" y="324" font-size="9.5" font-weight="400" fill="#374151">'
          'Boundary into OT: Kiosk (scan removable media) + Vault (scanned storage/transfer) — modeled free in Python (no OPSWAT software)</text>')

    c.legend(35, 350, [
        ("neutral", "Associate tier (free foundation)"),
        ("alt", "MetaDefender Professional (paid)"),
        ("data", "OT Security Expert (capstone)"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
