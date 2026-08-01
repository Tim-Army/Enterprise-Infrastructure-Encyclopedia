#!/usr/bin/env python3
"""Volume CXIX (HPE Aruba CX 10000 Build-It-Yourself Lab) topology.

Chapter 1: the CX 10000 top-of-rack switch embeds an AMD Pensando DPU that runs
a stateful firewall for east-west traffic at line rate, managed by PSM / Aruba
Fabric Composer. Endpoints web (:5432 target db), hmi (:502 target plc). A
default-deny stateful policy permits web->db:5432 and hmi->plc:502; return
traffic is permitted by state (no reverse rule), and hmi->db plus any
unsolicited/invalid packet is dropped.

Run from scripts/diagrams:  python3 gen_volume119.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-119-hpe-aruba-cx10000-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Stateful East-West Firewalling with the Aruba CX 10000 DPU",
        subtitle="The CX 10000 ToR DPU firewalls east-west with connection tracking at line rate; web->db:5432 and hmi->plc:502 permitted, return traffic by state, hmi->db and unsolicited packets dropped",
        svg_title="Chapter 1 lab topology: the Aruba CX 10000 top-of-rack DPU applying a stateful firewall to east-west traffic",
        svg_desc="The HPE Aruba CX 10000 top-of-rack switch embeds an AMD Pensando DPU that runs a stateful firewall "
                 "for east-west traffic at line rate, managed by the Pensando Policy and Services Manager and Aruba "
                 "Fabric Composer. Endpoints are web at 10.130.1.10, db at 10.130.2.20 listening on 5432, hmi at "
                 "10.130.3.30, and plc at 10.130.4.40 listening on 502. A default-deny stateful policy permits only "
                 "web to db on 5432 and hmi to plc on 502; return traffic is permitted automatically by connection "
                 "state with no reverse rule, and the hmi to db lateral flow plus any unsolicited or invalid packet "
                 "on the reverse tuple is dropped. The volume is design-leaning two-track: Track 1 describes the CX "
                 "10000 and PSM, Track 2 reproduces the stateful firewall with Linux nftables connection tracking.")

    c.node_box(320, 50, 320, 44, "mgmt", [
        Line("PSM / Aruba Fabric Composer", 11, 700, "#111827"),
        Line("stateful policy + per-flow telemetry", 9, 400, "#374151"),
    ])
    c.plane_bar(170, 118, 620, 28, "neutral",
                "CX 10000 ToR · embedded DPU · stateful firewall east-west (line rate, no hairpin)")
    c.raw('<line x1="480" y1="94" x2="480" y2="118" stroke="#33415c" stroke-width="1.4"/>')

    c.node_box(60, 190, 130, 62, "neutral", [
        Line("web", 11, 700, "#111827"), Line("client", 9, 400, "#374151"), Line("10.130.1.10", 8.5, 400, "#374151")])
    c.node_box(285, 190, 130, 62, "data", [
        Line("db · :5432", 10, 700, "#111827"), Line("PostgreSQL", 9, 400, "#374151"), Line("10.130.2.20", 8.5, 400, "#374151")])
    c.node_box(510, 190, 130, 62, "neutral", [
        Line("hmi", 11, 700, "#111827"), Line("operator", 9, 400, "#374151"), Line("10.130.3.30", 8.5, 400, "#374151")])
    c.node_box(735, 190, 130, 62, "data", [
        Line("plc · :502", 10, 700, "#111827"), Line("Modbus", 9, 400, "#374151"), Line("10.130.4.40", 8.5, 400, "#374151")])
    for cx in (125, 350, 575, 800):
        c.raw(f'<line x1="{cx}" y1="146" x2="{cx}" y2="190" stroke="#94a3b8" stroke-width="1.1"/>')

    c.connector(190, 214, 285, 214, "alt", label="web->db 5432 (return by state)", label_pos=(100, 300))
    c.connector(510, 236, 415, 236, "warn", label="hmi->db DENIED", label_pos=(360, 330))
    c.connector(640, 214, 735, 214, "alt", label="hmi->plc 502", label_pos=(610, 300))

    c.raw('<text x="230" y="372" font-size="9.5" font-weight="700" fill="#374151">'
          'reply permitted by connection state (no reverse rule); unsolicited / invalid packets dropped</text>')

    c.legend(60, 420, [
        ("alt", "Permitted (stateful)"),
        ("warn", "Denied (default / unsolicited)"),
        ("mgmt", "PSM (stateful policy)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
