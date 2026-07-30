#!/usr/bin/env python3
"""Volume XCIX (Tempered Airwall Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): the segmented estate showing Airwall's
HIP encrypted-overlay model. aw-gw is the three-legged router that is the
overlay hub and the Airwall Gateway for the agentless PLC. The servers and
HMI run an overlay agent (WireGuard in Track 2); after cloaking they are dark
on the underlay and reach each other only over the encrypted overlay, where
trust policy on aw-gw permits app->db and hmi->plc and denies the rest.

Run from scripts/diagrams:  python3 gen_volume099.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-099-tempered-airwall-lab"


def ch01():
    c = Canvas(960, 680,
        title="Chapter 1 Lab Topology: Tempered Airwall HIP Encrypted Overlay",
        subtitle="aw-gw is the overlay hub and Airwall Gateway; after cloaking the underlay goes dark and protected devices talk only over the encrypted overlay (10.99.0.0/24)",
        svg_title="Chapter 1 lab topology: a five-VM estate segmented with Tempered Airwall, an encrypted HIP overlay over three underlay segments",
        svg_desc="A Windows 11 host running VMware Workstation Pro hosts three virtual-network underlay segments "
                 "joined by one three-legged Linux router, aw-gw, which is the overlay hub and the Airwall Gateway "
                 "for the OT cell. The IT/Corporate segment (VMnet8 NAT, 192.168.170.0/24) carries the host, which "
                 "doubles as the attacker 'IT laptop', and the VMware NAT gateway. The Data Center segment (VMnet2 "
                 "host-only, 10.10.20.0/24) holds aw-app01 (nginx, overlay 10.99.0.11), aw-db01 (PostgreSQL, the "
                 "crown jewels, overlay 10.99.0.12), and aw-win01 (Windows SCADA/HMI, overlay 10.99.0.21), each "
                 "running an overlay agent. The OT cell (VMnet3 host-only, 10.10.30.0/24) is isolated with no host "
                 "adapter and holds aw-ot01, an agentless Modbus PLC carried onto the overlay by the aw-gw gateway. "
                 "After cloaking, the protected devices are dark on the underlay and reach each other only over the "
                 "encrypted overlay 10.99.0.0/24, where trust policy on aw-gw permits aw-app01 to aw-db01 on TCP "
                 "5432 and aw-win01 to the PLC on Modbus TCP 502 and denies the compromised-HMI-to-database flow.")

    c.node_box(300, 68, 360, 54, "mgmt", [
        Line("Windows 11 Host · Workstation Pro 17", 12.5, 700, "#111827"),
        Line("Airwall admin + 'IT laptop' (attacker, Lab 5.3)", 9.5, 400, "#374151"),
    ])
    c.plane_bar(60, 140, 840, 30, "mgmt",
                "VMnet8 — NAT · 'IT / Corporate' underlay · 192.168.170.0/24")
    c.node_box(60, 188, 170, 52, "neutral", [
        Line("VMware NAT", 11.5, 700, "#111827"),
        Line("192.168.170.2", 10.5, 700, "#374151"),
    ])
    c.connector(480, 122, 480, 140, "mgmt")

    c.node_box(380, 196, 200, 104, "neutral", [
        Line("aw-gw", 14, 700, "#111827"),
        Line("Ubuntu 22.04 · 3-legged router", 10, 400, "#374151"),
        Line("OVERLAY HUB + GATEWAY", 10, 700, "#b45309"),
        Line("overlay 10.99.0.254", 10, 700, "#374151"),
    ])
    c.connector(480, 170, 480, 196, "mgmt")

    c.raw('<line x1="480" y1="315" x2="335" y2="315" stroke="#33415c" stroke-width="1.5"/>')
    c.raw('<line x1="335" y1="315" x2="335" y2="468" stroke="#33415c" stroke-width="1.5"/>')
    c.connector(480, 300, 480, 330, "mgmt")

    c.plane_bar(60, 330, 840, 30, "alt",
                "VMnet2 — Host-only · 'Data Center' underlay · 10.10.20.0/24 · encrypted overlay 10.99.0.0/24")
    c.node_box(70, 372, 250, 74, "alt", [
        Line("aw-app01", 13, 700, "#111827"),
        Line("nginx :80 · app tier", 10, 400, "#374151"),
        Line("agent · ovl 10.99.0.11", 10, 700, "#166534"),
    ])
    c.node_box(355, 372, 250, 74, "alt", [
        Line("aw-db01", 13, 700, "#111827"),
        Line("PostgreSQL :5432 · CROWN JEWELS", 9.5, 700, "#7f1d1d"),
        Line("agent · ovl 10.99.0.12", 10, 700, "#166534"),
    ])
    c.node_box(640, 372, 250, 74, "alt", [
        Line("aw-win01", 13, 700, "#111827"),
        Line("Win2022 · SCADA / HMI", 10, 400, "#374151"),
        Line("agent · ovl 10.99.0.21", 10, 700, "#166534"),
    ])
    c.connector(195, 360, 195, 372, "alt")
    c.connector(765, 360, 765, 372, "alt")

    c.connector(320, 405, 355, 405, "alt", label="5432 (overlay)", label_pos=(300, 398))
    c.connector(640, 424, 605, 424, "warn", label="5432 DENIED", label_pos=(612, 462))

    c.connector(335, 456, 335, 474, "mgmt")
    c.plane_bar(60, 474, 840, 30, "data",
                "VMnet3 — Host-only · 'OT Cell' underlay · 10.10.30.0/24 · isolated (no host adapter)")
    c.node_box(355, 516, 250, 78, "data", [
        Line("aw-ot01 · 'PLC'", 13, 700, "#111827"),
        Line("Modbus TCP :502", 10, 400, "#374151"),
        Line("AGENTLESS — via aw-gw gateway", 9.5, 700, "#7c2d12"),
        Line("10.10.30.50", 9.5, 700, "#374151"),
    ], dashed=True)
    c.connector(765, 446, 585, 516, "alt", label="502 (overlay)", label_pos=(730, 462))

    c.legend(60, 640, [
        ("alt", "Legitimate flow (allowed)"),
        ("warn", "Lateral movement (denied)"),
        ("mgmt", "Encrypted overlay via aw-gw"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
