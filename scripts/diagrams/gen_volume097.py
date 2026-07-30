#!/usr/bin/env python3
"""Volume XCVII (TrueFort Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): the segmented IT/OT estate showing
how TrueFort reasons over process/network/identity telemetry and enforces
on each host's native firewall, with the agentless PLC protected by policy
on its managed neighbor tf-gw, tf-gw as the single routing choke point, the
two legitimate east-west flows, and the lateral-movement flow -- including
reuse of a stolen service account -- that the design denies.

Run from scripts/diagrams:  python3 gen_volume097.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-097-truefort-lab"


def ch01():
    c = Canvas(960, 680,
        title="Chapter 1 Lab Topology: TrueFort Across an IT/OT Estate",
        subtitle="Application-centric, EDR-leveraged telemetry; enforcement on each host's native firewall; tf-gw is the one routing choke point; the stolen service account is bound to its sanctioned identity",
        svg_title="Chapter 1 lab topology: a five-VM IT/OT estate segmented with TrueFort, native-firewall enforcement on the servers and neighbor-enforced protection for the PLC",
        svg_desc="A Windows 11 host running VMware Workstation Pro hosts three virtual-network segments joined by "
                 "one three-legged Linux router, tf-gw, over which TrueFort reasons about process, network, and "
                 "identity telemetry and which is the enforcement point for the OT cell. The IT/Corporate segment "
                 "(VMnet8 NAT, 192.168.170.0/24) carries the host itself, which doubles as the attacker 'IT laptop', "
                 "and the VMware NAT gateway. The Data Center segment (VMnet2 host-only, 10.10.20.0/24) holds three "
                 "workloads enforced on their native firewalls: tf-app01 (nginx), tf-db01 (PostgreSQL, the crown "
                 "jewels, served by the svc_app service account), and tf-win01 (Windows Server SCADA/HMI). The OT "
                 "cell (VMnet3 host-only, 10.10.30.0/24) is isolated with no host adapter and holds tf-ot01, a "
                 "Modbus PLC that runs no agent; it is protected by policy on its managed neighbors and on tf-gw. "
                 "Two flows are legitimate and allowed: tf-app01 to tf-db01 on TCP 5432 as svc_app, and tf-win01 "
                 "(the HMI) to tf-ot01 on Modbus TCP 502. The lateral-movement flow from the compromised tf-win01 "
                 "to tf-db01 on 5432, reusing the stolen svc_app credential, is denied, and svc_app is bound to its "
                 "sanctioned host and process identity so the same credential fails from any other process.")

    c.node_box(300, 68, 360, 54, "mgmt", [
        Line("Windows 11 Host · Workstation Pro 17", 12.5, 700, "#111827"),
        Line("TrueFort admin + 'IT laptop' (attacker, Lab 5.3)", 9.5, 400, "#374151"),
    ])
    c.plane_bar(60, 140, 840, 30, "mgmt",
                "VMnet8 — NAT · 'IT / Corporate' · 192.168.170.0/24 · DHCP .128–.254")
    c.node_box(60, 188, 170, 52, "neutral", [
        Line("VMware NAT", 11.5, 700, "#111827"),
        Line("192.168.170.2", 10.5, 700, "#374151"),
    ])
    c.connector(480, 122, 480, 140, "mgmt")

    c.node_box(380, 196, 200, 104, "neutral", [
        Line("tf-gw", 14, 700, "#111827"),
        Line("Ubuntu 22.04 · 3-legged router", 10, 400, "#374151"),
        Line("telemetry · enforcement pt for OT", 9.5, 700, "#b45309"),
        Line(".170.10 / .20.254 / .30.254", 10, 700, "#374151"),
    ])
    c.connector(480, 170, 480, 196, "mgmt")

    c.raw('<line x1="480" y1="315" x2="335" y2="315" stroke="#33415c" stroke-width="1.5"/>')
    c.raw('<line x1="335" y1="315" x2="335" y2="468" stroke="#33415c" stroke-width="1.5"/>')
    c.connector(480, 300, 480, 330, "mgmt")

    c.plane_bar(60, 330, 840, 30, "alt",
                "VMnet2 — Host-only · 'Data Center' · 10.10.20.0/24 · no DHCP")
    c.node_box(70, 372, 250, 74, "alt", [
        Line("tf-app01", 13, 700, "#111827"),
        Line("nginx :80 · app tier", 10, 400, "#374151"),
        Line("app baseline · 10.10.20.11", 9.5, 700, "#166534"),
    ])
    c.node_box(355, 372, 250, 74, "alt", [
        Line("tf-db01", 13, 700, "#111827"),
        Line("PostgreSQL :5432 · svc_app · JEWELS", 9, 700, "#7f1d1d"),
        Line("native fw · 10.10.20.12", 10, 700, "#166534"),
    ])
    c.node_box(640, 372, 250, 74, "alt", [
        Line("tf-win01", 13, 700, "#111827"),
        Line("Win2022 · SCADA / HMI", 10, 400, "#374151"),
        Line("Windows Firewall · 10.10.20.21", 9, 700, "#166534"),
    ])
    c.connector(195, 360, 195, 372, "alt")
    c.connector(765, 360, 765, 372, "alt")

    c.connector(320, 405, 355, 405, "alt", label="5432", label_pos=(324, 398))
    c.connector(640, 424, 605, 424, "warn", label="svc_app DENIED", label_pos=(608, 462))

    c.connector(335, 456, 335, 474, "mgmt")
    c.plane_bar(60, 474, 840, 30, "data",
                "VMnet3 — Host-only · 'OT Cell' · 10.10.30.0/24 · isolated (no host adapter)")
    c.node_box(355, 516, 250, 78, "data", [
        Line("tf-ot01 · 'PLC'", 13, 700, "#111827"),
        Line("Modbus TCP :502", 10, 400, "#374151"),
        Line("AGENTLESS — protected via tf-gw", 9.5, 700, "#7c2d12"),
        Line("10.10.30.50", 9.5, 700, "#374151"),
    ], dashed=True)
    c.connector(765, 446, 585, 516, "alt", label="502", label_pos=(735, 462))

    c.legend(60, 640, [
        ("alt", "Legitimate flow (allowed)"),
        ("warn", "Stolen service account (denied)"),
        ("mgmt", "Routing via tf-gw"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
