#!/usr/bin/env python3
"""Volume CIX (Fortinet ISFW + VDOM Build-It-Yourself Lab) topology.

Chapter 1: a FortiGate placed internally (ISFW) segments a four-zone estate.
web (zone APP), db (zone DB, :5432), hmi (zone MGMT), plc (zone OT, :502).
Firewall policies permit APP->DB PGSQL and MGMT->OT MODBUS and rely on the
implicit deny; the MGMT->DB (hmi->db) lateral flow is denied. The OT tier is
moved to its own VDOM, so IT<->OT crosses only a scoped inter-VDOM link.

Run from scripts/diagrams:  python3 gen_volume109.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-109-fortinet-isfw-vdom-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Internal Segmentation with Fortinet ISFW and VDOMs",
        subtitle="A FortiGate ISFW enforces zone policies (permit APP->DB, MGMT->OT; implicit deny), and the OT tier is isolated in its own VDOM crossed only by a scoped inter-VDOM link",
        svg_title="Chapter 1 lab topology: a FortiGate internal segmentation firewall enforcing zone policies with the OT tier in its own VDOM",
        svg_desc="A FortiGate placed inside the network as an Internal Segmentation Firewall segments a four-zone "
                 "estate. web is in zone APP, db is in zone DB listening on 5432, hmi is in zone MGMT, and plc is in "
                 "zone OT listening on 502. Firewall policies permit APP to DB with the PGSQL service and MGMT to OT "
                 "with the MODBUS service, and the FortiGate implicit deny drops everything else, including the MGMT "
                 "to DB lateral flow from hmi to db. The OT tier is moved into its own VDOM, so IT to OT traffic "
                 "crosses only a tightly scoped inter-VDOM link permitting MODBUS. The volume is two-track: Track 1 "
                 "uses a real FortiGate-VM, Track 2 reproduces zones and VDOMs with Linux nftables tables.")

    c.node_box(330, 50, 300, 44, "mgmt", [
        Line("FortiGate ISFW  ·  FortiOS", 11, 700, "#111827"),
        Line("firewall policies · VDOMs · implicit deny", 9, 400, "#374151"),
    ])
    c.plane_bar(190, 118, 580, 28, "neutral",
                "Internal Segmentation Firewall  ·  permit by policy (address + service)  ·  implicit deny")
    c.raw('<line x1="480" y1="94" x2="480" y2="118" stroke="#33415c" stroke-width="1.4"/>')

    c.node_box(60, 190, 130, 62, "neutral", [
        Line("web", 11, 700, "#111827"),
        Line("zone APP (VDOM IT)", 8.5, 700, "#166534"),
        Line("10.30.1.10", 8.5, 400, "#374151"),
    ])
    c.node_box(285, 190, 130, 62, "data", [
        Line("db", 11, 700, "#111827"),
        Line("zone DB · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(510, 190, 130, 62, "neutral", [
        Line("hmi", 11, 700, "#111827"),
        Line("zone MGMT (VDOM IT)", 8.5, 700, "#166534"),
        Line("operator", 8.5, 400, "#374151"),
    ])
    c.node_box(735, 190, 130, 62, "data", [
        Line("plc", 11, 700, "#111827"),
        Line("zone OT · VDOM OT · :502", 8, 700, "#7c2d12"),
        Line("Modbus", 8.5, 400, "#374151"),
    ], dashed=True)
    for cx in (125, 350, 575):
        c.raw(f'<line x1="{cx}" y1="146" x2="{cx}" y2="190" stroke="#94a3b8" stroke-width="1.1"/>')
    # OT crosses only the inter-VDOM link (dashed)
    c.raw('<line x1="800" y1="146" x2="800" y2="190" stroke="#94a3b8" stroke-width="1.1" stroke-dasharray="4 3"/>')

    c.connector(190, 214, 285, 214, "alt",
                label="APP->DB PGSQL permit", label_pos=(120, 296))
    c.connector(510, 236, 415, 236, "warn",
                label="MGMT->DB DENIED (lateral)", label_pos=(356, 330))
    c.connector(640, 214, 735, 214, "alt",
                label="MGMT->OT MODBUS (inter-VDOM)", label_pos=(590, 296))

    c.legend(60, 420, [
        ("alt", "Permitted by firewall policy"),
        ("warn", "Lateral movement (implicit deny)"),
        ("data", "OT isolated in its own VDOM"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
