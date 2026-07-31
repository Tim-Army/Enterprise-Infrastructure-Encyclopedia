#!/usr/bin/env python3
"""Volume CX (Check Point CloudGuard Build-It-Yourself Lab) topology.

Chapter 1: a Check Point Management server defines objects and an ordered
rulebase and installs policy to a Security Gateway that enforces it east-west.
Endpoints web (seg APP, role=web), db (seg DB, role=db, :5432), hmi (seg MGMT,
role=hmi), plc (seg OT, role=plc, :502). The rulebase permits web->db PGSQL and
hmi->plc MODBUS; the Cleanup rule drops everything else including hmi->db.
CloudGuard tag-based dynamic objects make the policy follow the workloads.

Run from scripts/diagrams:  python3 gen_volume110.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-110-checkpoint-cloudguard-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Rulebase Microsegmentation with Check Point CloudGuard",
        subtitle="Management defines the ordered rulebase and installs policy to a Security Gateway; permits web->db and hmi->plc, the Cleanup rule drops the rest; tag-based objects follow workloads",
        svg_title="Chapter 1 lab topology: a Check Point management server installing an ordered rulebase to a Security Gateway that enforces it over four segments",
        svg_desc="A Check Point management server, driven through SmartConsole and the mgmt_cli API, defines objects "
                 "and a single ordered access rulebase and installs policy to a Security Gateway. The gateway enforces "
                 "the rulebase east-west over four segments: web in segment APP with tag role=web, db in segment DB "
                 "with tag role=db listening on 5432, hmi in segment MGMT with tag role=hmi, and plc in segment OT "
                 "with tag role=plc listening on 502. The rulebase permits web to db with the PGSQL service and hmi "
                 "to plc with the MODBUS service; the explicit Cleanup rule drops everything else, including the hmi "
                 "to db lateral flow. CloudGuard data-center and dynamic objects import membership from cloud or "
                 "vCenter tags so the policy follows workloads as they are created, moved, or re-addressed. The volume "
                 "is two-track: Track 1 uses a real Management plus Gateway, Track 2 reproduces the rulebase and "
                 "tag-based objects with Linux nftables.")

    c.node_box(320, 50, 320, 44, "mgmt", [
        Line("Check Point Management", 11, 700, "#111827"),
        Line("SmartConsole · mgmt_cli · define + install policy", 8.5, 400, "#374151"),
    ])
    c.plane_bar(190, 118, 580, 28, "neutral",
                "Security Gateway  ·  enforces ordered rulebase + Cleanup drop  ·  tag-based dynamic objects")
    c.raw('<line x1="480" y1="94" x2="480" y2="118" stroke="#33415c" stroke-width="1.4"/>')
    c.raw('<text x="490" y="110" font-size="9" fill="#374151">install-policy</text>')

    c.node_box(60, 190, 130, 62, "neutral", [
        Line("web", 11, 700, "#111827"),
        Line("seg APP · role=web", 8.5, 700, "#166534"),
        Line("10.40.1.10", 8.5, 400, "#374151"),
    ])
    c.node_box(285, 190, 130, 62, "data", [
        Line("db", 11, 700, "#111827"),
        Line("role=db · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(510, 190, 130, 62, "neutral", [
        Line("hmi", 11, 700, "#111827"),
        Line("seg MGMT · role=hmi", 8.5, 700, "#166534"),
        Line("operator", 8.5, 400, "#374151"),
    ])
    c.node_box(735, 190, 130, 62, "data", [
        Line("plc", 11, 700, "#111827"),
        Line("role=plc · :502", 9, 700, "#7c2d12"),
        Line("Modbus", 8.5, 400, "#374151"),
    ])
    for cx in (125, 350, 575, 800):
        c.raw(f'<line x1="{cx}" y1="146" x2="{cx}" y2="190" stroke="#94a3b8" stroke-width="1.1"/>')

    c.connector(190, 214, 285, 214, "alt",
                label="web->db PGSQL permit", label_pos=(120, 296))
    c.connector(510, 236, 415, 236, "warn",
                label="hmi->db DROP (Cleanup rule)", label_pos=(356, 330))
    c.connector(640, 214, 735, 214, "alt",
                label="hmi->plc MODBUS permit", label_pos=(600, 296))

    c.legend(60, 420, [
        ("alt", "Permitted by access rule"),
        ("warn", "Lateral movement (Cleanup drop)"),
        ("mgmt", "Management (defines + installs policy)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
