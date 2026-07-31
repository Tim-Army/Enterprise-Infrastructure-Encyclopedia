#!/usr/bin/env python3
"""Volume CXI (VMware NSX Distributed Firewall Build-It-Yourself Lab) topology.

Chapter 1: all four workloads share ONE subnet (10.50.1.0/24). NSX Manager
distributes tag-based group rules to every VM's vNIC, where the DFW enforces
in the hypervisor kernel. web (role=web), db (role=db, :5432), hmi (role=hmi),
plc (role=plc, :502). The DFW permits Web->Database:5432 and Operators->OT:502
and drops everything else -- including hmi->db BETWEEN SAME-SUBNET PEERS, the
case a centralized firewall cannot filter.

Run from scripts/diagrams:  python3 gen_volume111.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-111-vmware-nsx-dfw-lab"


def ch01():
    c = Canvas(960, 470,
        title="Chapter 1 Lab Topology: Distributed Microsegmentation with VMware NSX DFW",
        subtitle="All four workloads on one subnet; NSX distributes tag-group rules to every vNIC, so hmi->db is denied at db's own interface with no gateway between the peers",
        svg_title="Chapter 1 lab topology: the NSX Distributed Firewall enforcing at each vNIC across four workloads on one subnet",
        svg_desc="All four workloads share a single subnet 10.50.1.0/24 with no gateway between them. NSX Manager "
                 "defines security tags, dynamic groups, and a distributed firewall policy and distributes the rules "
                 "to every VM's vNIC, where the DFW enforces in the hypervisor kernel. web carries tag role=web, db "
                 "carries role=db and listens on 5432, hmi carries role=hmi, and plc carries role=plc and listens on "
                 "502. The DFW permits Web to Database on 5432 and Operators to OT on 502 with a zero-trust Drop "
                 "default; the hmi to db lateral flow is denied at db's own vNIC even though hmi and db are direct "
                 "same-subnet peers -- the case a centralized firewall or ISFW cannot see. The volume is two-track: "
                 "Track 1 uses a real NSX Manager and ESXi transport node, Track 2 reproduces distributed enforcement "
                 "by having each workload namespace enforce its own nftables ruleset.")

    c.node_box(320, 44, 320, 42, "mgmt", [
        Line("NSX Manager  ·  tags · groups · DFW policy", 10.5, 700, "#111827"),
        Line("distributes rules to every vNIC", 9, 400, "#374151"),
    ])
    c.plane_bar(50, 106, 860, 26, "neutral",
                "One L2 segment 10.50.1.0/24  ·  DFW enforces at each vNIC  ·  no gateway between peers")
    # distribution arrows from manager to each vNIC
    for cx in (135, 355, 575, 795):
        c.raw(f'<line x1="480" y1="86" x2="{cx}" y2="106" stroke="#33415c" stroke-width="1" stroke-dasharray="3 3"/>')

    def vm(x, style, name, tag, extra):
        c.node_box(x, 168, 150, 66, style, [
            Line(name, 11, 700, "#111827"),
            Line(tag, 9.5, 700, "#166534" if style == "neutral" else "#7f1d1d"),
            Line(extra, 8.5, 400, "#374151"),
        ])
        # vNIC-DFW badge along the box top edge
        c.raw(f'<text x="{x + 75}" y="163" text-anchor="middle" font-size="8" font-weight="700" '
              f'fill="#1d4ed8">[vNIC-DFW]</text>')

    vm(60,  "neutral", "web", "role=web", "10.50.1.10")
    vm(280, "data",    "db",  "role=db · :5432", "PostgreSQL")
    vm(500, "neutral", "hmi", "role=hmi", "operator")
    vm(720, "data",    "plc", "role=plc · :502", "Modbus")

    # allowed same-subnet flows
    c.connector(210, 198, 280, 198, "alt", label="Web->Database 5432 allow", label_pos=(120, 262))
    c.connector(650, 198, 720, 198, "alt", label="Operators->OT 502 allow", label_pos=(610, 262))
    # denied same-subnet lateral flow (hmi -> db)
    c.connector(500, 224, 430, 224, "warn",
                label="hmi->db DENIED at db's vNIC (same subnet, no gateway)", label_pos=(300, 300))

    c.legend(50, 388, [
        ("alt", "Permitted by DFW rule"),
        ("warn", "Same-subnet lateral (denied at vNIC)"),
        ("mgmt", "NSX Manager (policy)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
