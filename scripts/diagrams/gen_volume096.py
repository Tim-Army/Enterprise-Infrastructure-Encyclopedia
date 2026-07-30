#!/usr/bin/env python3
"""Volume XCVI (Zero Networks Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): the segmented IT/OT estate showing
how Zero Networks enforces agentlessly by remotely programming each host's
native firewall, with the agentless PLC protected by policy on its managed
neighbor zn-gw, zn-gw as the single routing choke point between the three
virtual-network segments, the two legitimate east-west flows, and the
lateral-movement flow the design denies. Privileged ports are closed until
a just-in-time MFA grant opens them.

Run from scripts/diagrams:  python3 gen_volume096.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-096-zero-networks-lab"


def ch01():
    c = Canvas(960, 680,
        title="Chapter 1 Lab Topology: Zero Networks Across an IT/OT Estate",
        subtitle="Agentless — Zero Networks remotely programs each host's native firewall; zn-gw is the one routing choke point, privileged ports are just-in-time MFA only",
        svg_title="Chapter 1 lab topology: a five-VM IT/OT estate segmented agentlessly with Zero Networks, native firewalls on the servers and neighbor-enforced protection for the PLC",
        svg_desc="A Windows 11 host running VMware Workstation Pro hosts three virtual-network segments joined by "
                 "one three-legged Linux router, zn-gw, whose native firewall Zero Networks programs remotely and "
                 "which is the enforcement point for the OT cell. The IT/Corporate segment (VMnet8 NAT, "
                 "192.168.170.0/24) carries the host itself, which doubles as the attacker 'IT laptop', and the "
                 "VMware NAT gateway. The Data Center segment (VMnet2 host-only, 10.10.20.0/24) holds three "
                 "workloads whose native firewalls are remotely programmed: zn-app01 (nginx), zn-db01 (PostgreSQL, "
                 "the crown jewels), and zn-win01 (Windows Server SCADA/HMI, Windows Firewall). The OT cell (VMnet3 "
                 "host-only, 10.10.30.0/24) is isolated with no host adapter and holds zn-ot01, a Modbus PLC that "
                 "exposes no manageable firewall; it is protected by policy on its managed neighbors and on zn-gw. "
                 "Two flows are legitimate and allowed: zn-app01 to zn-db01 on TCP 5432, and zn-win01 (the HMI) to "
                 "zn-ot01 on Modbus TCP 502. The lateral-movement flow from the compromised zn-win01 to zn-db01 on "
                 "5432 is denied, and administrative ports such as SSH 22 and RDP 3389 are closed until a "
                 "just-in-time MFA grant opens them.")

    c.node_box(300, 68, 360, 54, "mgmt", [
        Line("Windows 11 Host · Workstation Pro 17", 12.5, 700, "#111827"),
        Line("Zero Networks admin + 'IT laptop' (attacker, Lab 5.3)", 9.5, 400, "#374151"),
    ])
    c.plane_bar(60, 140, 840, 30, "mgmt",
                "VMnet8 — NAT · 'IT / Corporate' · 192.168.170.0/24 · DHCP .128–.254")
    c.node_box(60, 188, 170, 52, "neutral", [
        Line("VMware NAT", 11.5, 700, "#111827"),
        Line("192.168.170.2", 10.5, 700, "#374151"),
    ])
    c.connector(480, 122, 480, 140, "mgmt")

    c.node_box(380, 196, 200, 104, "neutral", [
        Line("zn-gw", 14, 700, "#111827"),
        Line("Ubuntu 22.04 · 3-legged router", 10, 400, "#374151"),
        Line("native fw · enforcement pt for OT", 10, 700, "#b45309"),
        Line(".170.10 / .20.254 / .30.254", 10, 700, "#374151"),
    ])
    c.connector(480, 170, 480, 196, "mgmt")

    c.raw('<line x1="480" y1="315" x2="335" y2="315" stroke="#33415c" stroke-width="1.5"/>')
    c.raw('<line x1="335" y1="315" x2="335" y2="468" stroke="#33415c" stroke-width="1.5"/>')
    c.connector(480, 300, 480, 330, "mgmt")

    c.plane_bar(60, 330, 840, 30, "alt",
                "VMnet2 — Host-only · 'Data Center' · 10.10.20.0/24 · no DHCP")
    c.node_box(70, 372, 250, 74, "alt", [
        Line("zn-app01", 13, 700, "#111827"),
        Line("nginx :80 · app tier", 10, 400, "#374151"),
        Line("native fw · 10.10.20.11", 10, 700, "#166534"),
    ])
    c.node_box(355, 372, 250, 74, "alt", [
        Line("zn-db01", 13, 700, "#111827"),
        Line("PostgreSQL :5432 · CROWN JEWELS", 9.5, 700, "#7f1d1d"),
        Line("native fw · 10.10.20.12", 10, 700, "#166534"),
    ])
    c.node_box(640, 372, 250, 74, "alt", [
        Line("zn-win01", 13, 700, "#111827"),
        Line("Win2022 · SCADA / HMI", 10, 400, "#374151"),
        Line("Windows Firewall · 10.10.20.21", 9, 700, "#166534"),
    ])
    c.connector(195, 360, 195, 372, "alt")
    c.connector(765, 360, 765, 372, "alt")

    c.connector(320, 405, 355, 405, "alt", label="5432", label_pos=(324, 398))
    c.connector(640, 424, 605, 424, "warn", label="5432 DENIED", label_pos=(612, 462))

    c.connector(335, 456, 335, 474, "mgmt")
    c.plane_bar(60, 474, 840, 30, "data",
                "VMnet3 — Host-only · 'OT Cell' · 10.10.30.0/24 · isolated (no host adapter)")
    c.node_box(355, 516, 250, 78, "data", [
        Line("zn-ot01 · 'PLC'", 13, 700, "#111827"),
        Line("Modbus TCP :502", 10, 400, "#374151"),
        Line("AGENTLESS — protected via zn-gw", 9.5, 700, "#7c2d12"),
        Line("10.10.30.50", 9.5, 700, "#374151"),
    ], dashed=True)
    c.connector(765, 446, 585, 516, "alt", label="502", label_pos=(735, 462))

    c.legend(60, 640, [
        ("alt", "Legitimate flow (allowed)"),
        ("warn", "Lateral movement (denied)"),
        ("mgmt", "Routing via zn-gw"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
