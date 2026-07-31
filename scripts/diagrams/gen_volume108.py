#!/usr/bin/env python3
"""Volume CVIII (Juniper Connected Security Build-It-Yourself Lab) topology.

Chapter 1: a vSRX firewall segments a four-zone estate. Endpoints web (zone
APP), db (zone DB, :5432), hmi (zone MGMT), plc (zone OT, :502) sit in four
security zones. Security policies permit APP->DB:5432 and MGMT->OT:502 and rely
on the SRX default inter-zone deny; the MGMT->DB (hmi->db) lateral flow is
denied. A dynamic address group can quarantine a host by membership.

Run from scripts/diagrams:  python3 gen_volume108.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-108-juniper-connected-security-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Firewall Microsegmentation with Juniper Connected Security",
        subtitle="A vSRX segments four security zones; policies permit APP->DB:5432 and MGMT->OT:502, the default denies the rest, and a dynamic group can quarantine a host",
        svg_title="Chapter 1 lab topology: a vSRX firewall enforcing zone policies over a four-zone estate",
        svg_desc="A vSRX firewall, optionally managed by Security Director, segments a four-zone estate. The web "
                 "endpoint is in zone APP, db is in zone DB listening on 5432, hmi is in zone MGMT, and plc is in "
                 "zone OT listening on 502. Security policies permit APP to DB on 5432 and MGMT to OT on 502, and the "
                 "SRX default inter-zone deny drops everything else, including the MGMT to DB lateral flow from hmi to "
                 "db. Connected Security adds reactive containment: a dynamic address group can quarantine a "
                 "compromised host by membership, with a standing deny policy, without editing a rule. The volume is "
                 "two-track: Track 1 uses a real vSRX, Track 2 reproduces zones and policies with Linux nftables.")

    c.node_box(330, 50, 300, 44, "mgmt", [
        Line("vSRX firewall  ·  Security Director", 11, 700, "#111827"),
        Line("zones · policies · dynamic-address groups", 9, 400, "#374151"),
    ])
    c.plane_bar(190, 118, 580, 28, "neutral",
                "vSRX enforcement  ·  default inter-zone deny  ·  permit by policy (address + application)")
    c.raw('<line x1="480" y1="94" x2="480" y2="118" stroke="#33415c" stroke-width="1.4"/>')

    c.node_box(60, 190, 130, 62, "neutral", [
        Line("web", 11, 700, "#111827"),
        Line("zone APP", 9.5, 700, "#166534"),
        Line("10.20.1.10", 8.5, 400, "#374151"),
    ])
    c.node_box(285, 190, 130, 62, "data", [
        Line("db", 11, 700, "#111827"),
        Line("zone DB · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(510, 190, 130, 62, "neutral", [
        Line("hmi", 11, 700, "#111827"),
        Line("zone MGMT", 9.5, 700, "#166534"),
        Line("operator", 8.5, 400, "#374151"),
    ])
    c.node_box(735, 190, 130, 62, "data", [
        Line("plc", 11, 700, "#111827"),
        Line("zone OT · :502", 9, 700, "#7c2d12"),
        Line("Modbus", 8.5, 400, "#374151"),
    ])
    for cx in (125, 350, 575, 800):
        c.raw(f'<line x1="{cx}" y1="146" x2="{cx}" y2="190" stroke="#94a3b8" stroke-width="1.1"/>')

    c.connector(190, 214, 285, 214, "alt",
                label="APP->DB 5432 permit", label_pos=(120, 296))
    c.connector(510, 236, 415, 236, "warn",
                label="MGMT->DB DENIED (lateral)", label_pos=(356, 330))
    c.connector(640, 214, 735, 214, "alt",
                label="MGMT->OT 502 permit", label_pos=(600, 296))

    c.legend(60, 420, [
        ("alt", "Permitted by security policy"),
        ("warn", "Lateral movement (default inter-zone deny)"),
        ("mgmt", "Firewall + central management"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
