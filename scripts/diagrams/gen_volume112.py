#!/usr/bin/env python3
"""Volume CXII (Xage Security Build-It-Yourself Lab) topology.

Chapter 1: Xage brokers every connection through an identity check. The Xage
Fabric holds identities and access policy in a decentralized, tamper-resistant
store. An enforcement point (broker) sits in front of each asset; the asset has
no direct path. svc-web is brokered to db:5432, op-hmi is brokered to plc:502
(a legacy Modbus device); an attacker with no identity is denied at the broker.

Run from scripts/diagrams:  python3 gen_volume112.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-112-xage-security-lab"


def ch01():
    c = Canvas(960, 450,
        title="Chapter 1 Lab Topology: Identity-Brokered OT Access with Xage",
        subtitle="Every connection is brokered through an identity check; assets have no direct path; a legacy PLC is reachable only by a granted, authenticated identity",
        svg_title="Chapter 1 lab topology: Xage brokering access to a database and a legacy PLC by identity",
        svg_desc="The Xage Fabric holds identities and access policy in a decentralized, tamper-resistant store and "
                 "distributes them to enforcement points. Each protected asset sits behind a broker and has no direct "
                 "network path. In the IT row, the web application's service identity svc-web is brokered to the "
                 "database on 5432. In the OT row, the operator identity op-hmi is brokered to a legacy Modbus PLC on "
                 "502. An attacker with no valid identity is denied at the broker even though the PLC has no "
                 "authentication of its own. The volume is two-track: Track 1 describes the real Xage Fabric at design "
                 "level, Track 2 builds a working identity-broker with socat and nftables so the asset is reachable "
                 "only through the broker.")

    c.node_box(300, 44, 360, 42, "mgmt", [
        Line("Xage Fabric  ·  identities + access policy", 10.5, 700, "#111827"),
        Line("decentralized · tamper-resistant", 9, 400, "#374151"),
    ])

    def row(y, who, who_sub, ident, asset, asset_sub, dashed):
        c.node_box(50, y, 110, 54, "neutral", [Line(who, 11, 700, "#111827"), Line(who_sub, 8.5, 400, "#374151")])
        c.node_box(275, y, 140, 54, "alt", [Line("broker (node)", 10, 700, "#111827"),
                                            Line("identity check", 8.5, 400, "#374151")])
        c.node_box(530, y, 120, 54, "data", [Line(asset, 10.5, 700, "#111827"),
                                             Line(asset_sub, 8.5, 400, "#374151")], dashed=dashed)
        c.connector(160, y + 27, 275, y + 27, "alt", label=ident, label_pos=(175, y - 8))
        c.connector(415, y + 27, 530, y + 27, "alt", label="brokered", label_pos=(430, y - 8))

    row(135, "web", "IT app", "svc-web", "db · :5432", "PostgreSQL", False)
    row(240, "hmi", "operator", "op-hmi", "plc · :502", "legacy Modbus", True)

    # policy distribution from fabric to each broker
    c.raw('<line x1="470" y1="86" x2="345" y2="135" stroke="#33415c" stroke-width="1" stroke-dasharray="3 3"/>')
    c.raw('<line x1="490" y1="86" x2="345" y2="240" stroke="#33415c" stroke-width="1" stroke-dasharray="3 3"/>')

    # attacker denied at the broker
    c.node_box(50, 330, 110, 44, "warn", [Line("attacker", 10.5, 700, "#111827"),
                                          Line("no identity", 8.5, 400, "#7f1d1d")])
    c.connector(160, 352, 275, 300, "warn", label="DENIED at broker", label_pos=(175, 372))

    # note on the right
    c.raw('<text x="680" y="188" font-size="9.5" font-weight="700" fill="#374151">Assets have no direct path;</text>')
    c.raw('<text x="680" y="204" font-size="9.5" font-weight="700" fill="#374151">reachable only via broker.</text>')

    c.legend(50, 398, [
        ("alt", "Brokered by valid identity"),
        ("warn", "No identity (denied)"),
        ("mgmt", "Xage Fabric (policy)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
