#!/usr/bin/env python3
"""Volume CXVII (Cisco ACI Build-It-Yourself Lab) topology.

Chapter 1: the APIC drives a Nexus 9000 fabric with an application-centric
whitelist. Endpoints live in EPGs: web (EPG-Web), db (EPG-DB, :5432), hmi
(EPG-Mgmt), plc (EPG-OT, :502). Contracts permit Web->DB:5432 and Mgmt->OT:502;
every other EPG pair is denied by the whitelist default (e.g. Mgmt->DB). uSeg
micro-EPGs reclassify a compromised endpoint into a deny-all quarantine.

Run from scripts/diagrams:  python3 gen_volume117.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-117-cisco-aci-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Application-Centric Whitelist Segmentation with Cisco ACI",
        subtitle="The APIC drives EPGs and contracts; traffic between EPGs is denied unless a contract permits it; Web->DB:5432 and Mgmt->OT:502 permitted, Mgmt->DB denied",
        svg_title="Chapter 1 lab topology: Cisco ACI EPGs and contracts enforcing an application-centric whitelist",
        svg_desc="The APIC drives a Nexus 9000 spine-leaf fabric with an application-centric whitelist. Endpoints "
                 "live in Endpoint Groups: web in EPG-Web, db in EPG-DB listening on 5432, hmi in EPG-Mgmt, and plc "
                 "in EPG-OT listening on 502. Contracts permit only Web to DB on 5432 and Mgmt to OT on 502; every "
                 "other EPG pair, including Mgmt to DB from hmi to db, is denied by the whitelist default. uSeg "
                 "micro-EPGs can reclassify a compromised endpoint into a deny-all quarantine by attribute, and "
                 "intra-EPG isolation denies traffic between members of the same EPG. The volume is two-track: Track 1 "
                 "describes APIC configuration, Track 2 reproduces EPGs and contracts with Linux nftables.")

    c.node_box(320, 50, 320, 44, "mgmt", [
        Line("APIC · Nexus 9000 spine-leaf", 11, 700, "#111827"),
        Line("EPGs + contracts · whitelist default-deny", 9, 400, "#374151"),
    ])
    c.plane_bar(190, 118, 580, 28, "neutral",
                "ACI fabric  ·  deny between EPGs unless a contract permits  ·  fabric-enforced")
    c.raw('<line x1="480" y1="94" x2="480" y2="118" stroke="#33415c" stroke-width="1.4"/>')

    c.node_box(60, 190, 130, 62, "neutral", [
        Line("web", 11, 700, "#111827"),
        Line("EPG-Web", 9.5, 700, "#166534"),
        Line("10.110.1.10", 8.5, 400, "#374151"),
    ])
    c.node_box(285, 190, 130, 62, "data", [
        Line("db", 11, 700, "#111827"),
        Line("EPG-DB · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(510, 190, 130, 62, "neutral", [
        Line("hmi", 11, 700, "#111827"),
        Line("EPG-Mgmt", 9.5, 700, "#166534"),
        Line("operator", 8.5, 400, "#374151"),
    ])
    c.node_box(735, 190, 130, 62, "data", [
        Line("plc", 11, 700, "#111827"),
        Line("EPG-OT · :502", 9, 700, "#7c2d12"),
        Line("Modbus", 8.5, 400, "#374151"),
    ])
    for cx in (125, 350, 575, 800):
        c.raw(f'<line x1="{cx}" y1="146" x2="{cx}" y2="190" stroke="#94a3b8" stroke-width="1.1"/>')

    c.connector(190, 214, 285, 214, "alt",
                label="contract web-db 5432", label_pos=(110, 296))
    c.connector(510, 236, 415, 236, "warn",
                label="Mgmt->DB DENIED (no contract)", label_pos=(350, 330))
    c.connector(640, 214, 735, 214, "alt",
                label="contract mgmt-ot 502", label_pos=(600, 296))

    c.raw('<text x="250" y="372" font-size="9.5" font-weight="700" fill="#374151">'
          'uSeg micro-EPG: reclassify a compromised endpoint into a deny-all quarantine (by attribute)</text>')

    c.legend(60, 420, [
        ("alt", "Permitted by contract"),
        ("warn", "Denied (whitelist default)"),
        ("mgmt", "APIC (EPGs + contracts)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
