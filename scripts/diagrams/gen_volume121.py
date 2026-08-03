#!/usr/bin/env python3
"""Volume CXXI (Nutanix Flow Build-It-Yourself Lab) topology.

Chapter 1: four VMs on one AHV virtual switch, microsegmented by Flow
Network Security. Prism Central holds category-driven policy: application
permits web->db:5432 and hmi->plc:502, isolation separates Environment:corp
from Environment:ot, and quarantine can cut a VM off entirely. Enforcement
is at the virtual switch — agentless, beneath every guest.

Run from scripts/diagrams:  python3 gen_volume121.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-121-nutanix-flow-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Category-Driven Microsegmentation with Nutanix Flow",
        subtitle="Prism Central distributes category-driven policy to every AHV host; enforcement is at the virtual switch — agentless, monitor mode first, quarantine > isolation > application",
        svg_title="Chapter 1 lab topology: Nutanix Flow Network Security enforcing category-driven policy at the AHV virtual switch",
        svg_desc="Four VMs sit on one AHV virtual switch: web and db carry the Environment corp category, hmi and "
                 "plc carry the Environment ot category, and each carries an AppTier category. Prism Central holds "
                 "the category-driven policy and distributes it to every AHV host, which enforces at the virtual "
                 "switch with no agent in any guest. An application policy permits web to db on 5432 and hmi to plc "
                 "on 502; an isolation policy forbids all traffic between Environment corp and Environment ot, which "
                 "kills the lateral hmi to db path; and a quarantine policy can remove a compromised VM's "
                 "connectivity entirely, overriding every permit. Policies are written in monitor mode first, where "
                 "flows are visualized without being dropped, then applied. The volume is two-track: Track 1 "
                 "describes Prism Central, Track 2 builds the model with a Linux bridge, nftables sets as "
                 "categories, and enforcement in the host's bridge table.")

    c.node_box(310, 42, 340, 42, "mgmt", [
        Line("Prism Central (Flow)", 11, 700, "#111827"),
        Line("categories + policy · monitor -> apply", 9, 400, "#374151"),
    ])

    # the AHV virtual switch band
    c.node_box(45, 130, 870, 40, "alt", [
        Line("AHV virtual switch — enforcement point (agentless, beneath every guest)", 10, 700, "#111827"),
    ])
    c.connector(480, 84, 480, 130, "mgmt", label="policy", label_pos=(492, 112))

    def vm(x, name, ip, tier, env, color):
        c.node_box(x, 210, 180, 64, "neutral", [
            Line(name + " · " + ip, 10.5, 700, "#111827"),
            Line("AppTier: " + tier, 9, 400, "#374151"),
            Line("Environment: " + env, 9, 700, color),
        ])
        c.connector(x + 90, 170, x + 90, 210, "neutral", label="", label_pos=(0, 0))

    vm(45,  "web", ".10", "web", "corp", "#1d4ed8")
    vm(275, "db · :5432", ".20", "db", "corp", "#1d4ed8")
    vm(505, "hmi", ".30", "hmi", "ot", "#92400e")
    vm(735, "plc · :502", ".40", "plc", "ot", "#92400e")

    c.connector(225, 242, 275, 242, "alt", label="5432", label_pos=(228, 232))
    c.connector(685, 242, 735, 242, "alt", label="502", label_pos=(696, 232))

    c.raw('<text x="45" y="320" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'isolation: Environment:corp &lt;-X-&gt; Environment:ot — the lateral hmi -&gt; db path dies by name</text>')
    c.raw('<text x="45" y="340" font-size="9.5" font-weight="400" fill="#374151">'
          'application: only web -&gt; db:5432 and hmi -&gt; plc:502 are permitted (default-deny)</text>')

    c.node_box(700, 360, 220, 74, "warn", [
        Line("Quarantine", 10, 700, "#111827"),
        Line("one category assignment", 9, 400, "#7f1d1d"),
        Line("cuts a VM off entirely —", 9, 400, "#7f1d1d"),
        Line("beats every permit", 9, 700, "#7f1d1d"),
    ])

    c.legend(45, 430, [
        ("alt", "Permitted by application policy"),
        ("warn", "Quarantine (top precedence)"),
        ("mgmt", "Prism Central / categories"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
