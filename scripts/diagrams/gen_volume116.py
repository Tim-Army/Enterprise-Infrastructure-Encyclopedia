#!/usr/bin/env python3
"""Volume CXVI (Zscaler/Airgap Build-It-Yourself Lab) topology.

Chapter 1: every device on one flat VLAN is collapsed into a network of one,
so its only neighbor is the Airgap enforcement point -- no direct L2 path
between any two devices. The enforcement point denies east-west by default,
permits only web->db:5432, and offers a ransomware kill switch. An infected
victim is isolated and cannot spread.

Run from scripts/diagrams:  python3 gen_volume116.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-116-zscaler-airgap-lab"


def ch01():
    c = Canvas(960, 430,
        title="Chapter 1 Lab Topology: Agentless Network-of-One Isolation with Zscaler/Airgap",
        subtitle="Every device on one VLAN is isolated to a network of one; all east-west is brokered by the enforcement point, which permits only web->db:5432 and can kill-switch all lateral traffic",
        svg_title="Chapter 1 lab topology: five devices on one VLAN, each isolated to a network of one around the Airgap enforcement point",
        svg_desc="Five devices share one flat VLAN 10.100.1.0/24: web at .10, db at .20 on 5432, hmi at .30, plc "
                 "at .40 on 502, and an infected victim at .50. Airgap collapses every device into a network of one "
                 "by controlling ARP and DHCP, so each device's only neighbor is the enforcement point and there is "
                 "no direct Layer 2 path between any two devices even on the same subnet. The enforcement point denies "
                 "east-west by default and permits only the sanctioned web to db flow on 5432; every other pair, "
                 "including the infected victim, is isolated so ransomware cannot spread. A single ransomware kill "
                 "switch can sever all east-west instantly. No agent is installed on any device and no IP or VLAN "
                 "changes. The volume is two-track: Track 1 describes Zscaler/Airgap, Track 2 builds the isolation "
                 "with /32 host views and an nftables enforcer.")

    c.node_box(360, 188, 240, 78, "mgmt", [
        Line("Airgap enforcement point", 11, 700, "#111827"),
        Line("network-of-one · default deny", 9, 400, "#374151"),
        Line("ransomware kill switch", 9.5, 700, "#7f1d1d"),
    ])

    c.node_box(55, 70, 120, 50, "neutral", [Line("web", 11, 700, "#111827"), Line(".10", 9, 400, "#374151")])
    c.node_box(400, 48, 130, 50, "data", [Line("db · :5432", 10, 700, "#111827"), Line(".20", 9, 400, "#374151")])
    c.node_box(700, 70, 130, 50, "warn", [Line("victim", 11, 700, "#111827"), Line(".50 (infected)", 8.5, 400, "#7f1d1d")])
    c.node_box(70, 330, 120, 50, "neutral", [Line("hmi", 11, 700, "#111827"), Line(".30", 9, 400, "#374151")])
    c.node_box(710, 330, 130, 50, "data", [Line("plc · :502", 10, 700, "#111827"), Line(".40", 9, 400, "#374151")])

    # isolated spokes (plain grey) for hmi and plc
    c.raw('<line x1="190" y1="355" x2="360" y2="250" stroke="#94a3b8" stroke-width="1.2"/>')
    c.raw('<line x1="710" y1="355" x2="600" y2="250" stroke="#94a3b8" stroke-width="1.2"/>')
    # sanctioned flow: web -> enforcer -> db
    c.connector(175, 100, 360, 210, "alt", label="web", label_pos=(215, 150))
    c.connector(465, 188, 465, 98, "alt", label="db:5432 sanctioned", label_pos=(475, 150))
    # victim isolated (blocked)
    c.connector(760, 120, 600, 210, "warn", label="isolated (no spread)", label_pos=(640, 165))

    c.raw('<text x="220" y="300" font-size="9.5" font-weight="700" fill="#374151">'
          'same VLAN 10.100.1.0/24 — no direct L2 path; all east-west brokered</text>')

    c.legend(55, 398, [
        ("alt", "Sanctioned flow (web -> db)"),
        ("warn", "Infected / isolated (no lateral path)"),
        ("mgmt", "Enforcement point (+ kill switch)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
