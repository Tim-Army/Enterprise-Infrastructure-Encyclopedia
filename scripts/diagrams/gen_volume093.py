#!/usr/bin/env python3
"""Volume XCIII (ColorTokens Xshield Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): the segmented IT/OT estate showing where
each Xshield enforcement mode lands -- a host agent on the three servers
and the agentless Gatekeeper for the PLC -- with ct-gw as the single
routing choke point between the three virtual-network segments, the two
legitimate east-west flows, and the lateral-movement flow the design
denies. Matches the lab built in the chapter's hands-on section.

Run from scripts/diagrams:  python3 gen_volume093.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-093-colortokens-xshield-lab"


def ch01():
    c = Canvas(960, 680,
        title="Chapter 1 Lab Topology: ColorTokens Xshield Across a Segmented IT/OT Estate",
        subtitle="Host agent on the servers, agentless Gatekeeper for the PLC — ct-gw is the one routing choke point between three segments",
        svg_title="Chapter 1 lab topology: a five-VM IT/OT estate segmented with ColorTokens Xshield, host agents on the servers and an agentless Gatekeeper for the PLC",
        svg_desc="A Windows 11 host running VMware Workstation Pro hosts three virtual-network segments joined by "
                 "one three-legged Linux router, ct-gw, which also plays the agentless Xshield Gatekeeper for the "
                 "OT cell. The IT/Corporate segment (VMnet8 NAT, 192.168.170.0/24) carries the host itself, which "
                 "doubles as the attacker 'IT laptop', and the VMware NAT gateway. The Data Center segment (VMnet2 "
                 "host-only, 10.10.20.0/24) holds three agent-enforced workloads: ct-app01 (nginx), ct-db01 "
                 "(PostgreSQL, the crown jewels), and ct-win01 (Windows Server SCADA/HMI, enforced through the "
                 "Windows Filtering Platform). The OT cell (VMnet3 host-only, 10.10.30.0/24) is isolated with no "
                 "host adapter and holds ct-ot01, a Modbus PLC that can run no agent and is protected only by the "
                 "Gatekeeper in front of it. Two flows are legitimate and allowed: ct-app01 to ct-db01 on TCP 5432, "
                 "and ct-win01 (the HMI) to ct-ot01 on Modbus TCP 502. The lateral-movement flow from the "
                 "compromised ct-win01 to ct-db01 on 5432 is denied by the enforced policy, and the PLC is reachable "
                 "only by routing through ct-gw.")

    # --- IT / Corporate segment (host + NAT) ---
    c.node_box(300, 68, 360, 54, "mgmt", [
        Line("Windows 11 Host · Workstation Pro 17", 12.5, 700, "#111827"),
        Line("Xshield console + 'IT laptop' (attacker, Ex. D3)", 10, 400, "#374151"),
    ])
    c.plane_bar(60, 140, 840, 30, "mgmt",
                "VMnet8 — NAT · 'IT / Corporate' · 192.168.170.0/24 · DHCP .128–.254")
    c.node_box(60, 188, 170, 52, "neutral", [
        Line("VMware NAT", 11.5, 700, "#111827"),
        Line("192.168.170.2", 10.5, 700, "#374151"),
    ])
    c.connector(480, 122, 480, 140, "mgmt")   # host -> IT bar

    # --- ct-gw: the routing + Gatekeeper choke point ---
    c.node_box(380, 196, 200, 104, "neutral", [
        Line("ct-gw", 14, 700, "#111827"),
        Line("Ubuntu 22.04 · 3-legged router", 10, 400, "#374151"),
        Line("GATEKEEPER for OT cell", 10.5, 700, "#b45309"),
        Line(".170.10 / .20.254 / .30.254", 10, 700, "#374151"),
    ])
    c.connector(480, 170, 480, 196, "mgmt")   # IT bar -> ct-gw

    # Gatekeeper routing path down to the OT cell, threaded through the
    # gap between ct-app01 and ct-db01 (drawn before the Data Center bar so
    # the bar cleanly overpaints the crossing).
    c.raw('<line x1="480" y1="315" x2="335" y2="315" stroke="#33415c" stroke-width="1.5"/>')
    c.raw('<line x1="335" y1="315" x2="335" y2="468" stroke="#33415c" stroke-width="1.5"/>')
    c.connector(480, 300, 480, 330, "mgmt")   # ct-gw -> Data Center bar

    # --- Data Center segment (agent-enforced workloads) ---
    c.plane_bar(60, 330, 840, 30, "alt",
                "VMnet2 — Host-only · 'Data Center' · 10.10.20.0/24 · no DHCP")
    c.node_box(70, 372, 250, 74, "alt", [
        Line("ct-app01", 13, 700, "#111827"),
        Line("nginx :80 · app tier", 10, 400, "#374151"),
        Line("host agent · 10.10.20.11", 10, 700, "#166534"),
    ])
    c.node_box(355, 372, 250, 74, "alt", [
        Line("ct-db01", 13, 700, "#111827"),
        Line("PostgreSQL :5432 · CROWN JEWELS", 9.5, 700, "#7f1d1d"),
        Line("host agent · 10.10.20.12", 10, 700, "#166534"),
    ])
    c.node_box(640, 372, 250, 74, "alt", [
        Line("ct-win01", 13, 700, "#111827"),
        Line("Win2022 · SCADA / HMI", 10, 400, "#374151"),
        Line("host agent (WFP) · 10.10.20.21", 9.5, 700, "#166534"),
    ])
    c.connector(195, 360, 195, 372, "alt")    # DC bar -> app01
    c.connector(765, 360, 765, 372, "alt")    # DC bar -> win01

    # legitimate: app01 -> db01 on 5432
    c.connector(320, 405, 355, 405, "alt", label="5432", label_pos=(324, 398))
    # lateral movement (denied): win01 -> db01 on 5432
    c.connector(640, 424, 605, 424, "warn", label="5432 DENIED", label_pos=(612, 462))

    # --- OT cell (agentless, Gatekeeper-protected) ---
    c.connector(335, 456, 335, 474, "mgmt")   # Gatekeeper trunk -> OT bar
    c.plane_bar(60, 474, 840, 30, "data",
                "VMnet3 — Host-only · 'OT Cell' · 10.10.30.0/24 · isolated (no host adapter)")
    c.node_box(355, 516, 250, 78, "data", [
        Line("ct-ot01 · 'PLC'", 13, 700, "#111827"),
        Line("Modbus TCP :502", 10, 400, "#374151"),
        Line("AGENTLESS — via Gatekeeper", 10, 700, "#7c2d12"),
        Line("10.10.30.50", 9.5, 700, "#374151"),
    ], dashed=True)
    # legitimate: win01 (HMI) -> ot01 on 502
    c.connector(765, 446, 585, 516, "alt", label="502", label_pos=(735, 462))

    c.legend(60, 640, [
        ("alt", "Legitimate flow (allowed)"),
        ("warn", "Lateral movement (denied)"),
        ("mgmt", "Routing via Gatekeeper"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
