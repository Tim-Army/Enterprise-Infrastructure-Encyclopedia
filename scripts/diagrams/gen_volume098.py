#!/usr/bin/env python3
"""Volume XCVIII (Elisity Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): the four-segment estate showing
Elisity's identity-based, network-enforced, agentless model. el-gw is the
four-legged router that stands in for the Elisity-managed access switch and
is the single network enforcement point every cross-segment flow crosses.
The database sits on its own segment behind el-gw so all access to the crown
jewel is policed at the enforcement point; the agentless PLC sits on the
isolated OT segment. Two legitimate identity-to-identity flows are allowed;
the compromised-HMI-to-database lateral movement is denied.

Run from scripts/diagrams:  python3 gen_volume098.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-098-elisity-lab"


def ch01():
    c = Canvas(960, 720,
        title="Chapter 1 Lab Topology: Elisity Identity-Based Segmentation Across Four Segments",
        subtitle="el-gw is the network enforcement point (Elisity access-switch stand-in) every cross-segment flow crosses; the database is isolated behind it; policy is written by identity, enforced with no endpoint agents",
        svg_title="Chapter 1 lab topology: a five-VM estate segmented with Elisity, identity-based policy enforced on the network with the database isolated behind the enforcement point",
        svg_desc="A Windows 11 host running VMware Workstation Pro hosts four virtual-network segments joined by one "
                 "four-legged Linux router, el-gw, which stands in for the Elisity-managed access switch and is the "
                 "single network enforcement point every cross-segment flow crosses. The IT/Corporate segment "
                 "(VMnet8 NAT, 192.168.170.0/24) carries the host, which doubles as the attacker 'IT laptop', and "
                 "the VMware NAT gateway. The Data Center segment (VMnet2 host-only, 10.10.20.0/24) holds el-app01 "
                 "(nginx, classified AppServer) and el-win01 (Windows SCADA/HMI, classified HMI). The Database "
                 "segment (VMnet4 host-only, 10.10.40.0/24) isolates el-db01 (PostgreSQL, classified Database, the "
                 "crown jewels) behind el-gw so all access to it is policed at the enforcement point. The OT cell "
                 "(VMnet3 host-only, 10.10.30.0/24) is isolated with no host adapter and holds el-ot01, an agentless "
                 "Modbus PLC classified as PLC in the IdentityGraph. Two legitimate identity-to-identity flows are "
                 "allowed: AppServer to Database on TCP 5432, and HMI to PLC on Modbus TCP 502. The lateral-movement "
                 "flow from the compromised HMI to the Database on 5432 is denied at el-gw by identity-based policy, "
                 "with no agent on any endpoint.")

    # Host at top
    c.node_box(320, 58, 330, 44, "mgmt", [
        Line("Windows 11 Host · Workstation Pro 17", 12, 700, "#111827"),
        Line("Elisity admin + 'IT laptop' (attacker, Lab 5.3)", 9.5, 400, "#374151"),
    ])
    c.connector(485, 102, 485, 132, "mgmt")

    # el-gw spine on the left
    c.node_box(55, 150, 170, 470, "neutral", [
        Line("el-gw", 15, 700, "#111827"),
        Line("Ubuntu 22.04", 10, 400, "#374151"),
        Line("4-legged router", 10, 400, "#374151"),
        Line("= NETWORK", 10.5, 700, "#b45309"),
        Line("ENFORCEMENT POINT", 10.5, 700, "#b45309"),
        Line("(Elisity access-", 9, 400, "#374151"),
        Line("switch stand-in)", 9, 400, "#374151"),
        Line(".170.10 / .20.254", 9, 700, "#374151"),
        Line(".30.254 / .40.254", 9, 700, "#374151"),
    ])

    # Four segment bars to the right of the spine
    c.plane_bar(240, 132, 665, 26, "mgmt",
                "VMnet8 — NAT · 'IT / Corporate' · 192.168.170.0/24")
    c.node_box(720, 166, 180, 40, "neutral", [
        Line("VMware NAT · .2", 10.5, 700, "#111827"),
    ])
    c.connector(225, 145, 240, 145, "mgmt")   # el-gw leg -> IT

    c.plane_bar(240, 250, 665, 26, "alt",
                "VMnet2 — Host-only · 'Data Center' · 10.10.20.0/24 · no DHCP")
    c.node_box(250, 285, 250, 62, "alt", [
        Line("el-app01", 12.5, 700, "#111827"),
        Line("nginx :80 · AppServer", 9.5, 400, "#374151"),
        Line("10.10.20.11", 9.5, 700, "#166534"),
    ])
    c.node_box(650, 285, 250, 62, "alt", [
        Line("el-win01", 12.5, 700, "#111827"),
        Line("Win2022 · SCADA/HMI · HMI", 9, 400, "#374151"),
        Line("10.10.20.21", 9.5, 700, "#166534"),
    ])
    c.connector(225, 263, 240, 263, "alt")     # el-gw leg -> DC

    c.plane_bar(240, 385, 665, 26, "data",
                "VMnet4 — Host-only · 'Database' (isolated behind el-gw) · 10.10.40.0/24")
    c.node_box(430, 420, 270, 62, "data", [
        Line("el-db01 · Database", 12.5, 700, "#111827"),
        Line("PostgreSQL :5432 · CROWN JEWELS", 9, 700, "#7f1d1d"),
        Line("10.10.40.40", 9.5, 700, "#374151"),
    ])
    c.connector(225, 398, 240, 398, "data")    # el-gw leg -> DB

    c.plane_bar(240, 520, 665, 26, "data",
                "VMnet3 — Host-only · 'OT Cell' (isolated, no host adapter) · 10.10.30.0/24")
    c.node_box(430, 555, 270, 66, "data", [
        Line("el-ot01 · 'PLC'", 12.5, 700, "#111827"),
        Line("Modbus TCP :502 · PLC", 9, 400, "#374151"),
        Line("AGENTLESS · 10.10.30.50", 9, 700, "#7c2d12"),
    ], dashed=True)
    c.connector(225, 533, 240, 533, "data")    # el-gw leg -> OT

    # Identity-to-identity flows
    c.connector(375, 347, 470, 420, "alt", label="5432 (AppServer→Database)", label_pos=(300, 372))
    c.connector(720, 347, 640, 420, "warn", label="5432 DENIED (HMI→Database)", label_pos=(640, 372))
    c.connector(775, 347, 690, 555, "alt", label="502 (HMI→PLC)", label_pos=(760, 500))

    c.legend(60, 665, [
        ("alt", "Legitimate flow (allowed)"),
        ("warn", "Lateral movement (denied)"),
        ("mgmt", "Enforced at el-gw"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
