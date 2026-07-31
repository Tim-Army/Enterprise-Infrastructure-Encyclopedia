#!/usr/bin/env python3
"""Volume CXIII (Claroty xDome Build-It-Yourself Lab) topology.

Chapter 1: a passive collector on a SPAN feeds Claroty xDome, which discovers
assets, baselines communications, groups them into virtual zones, and derives a
least-privilege policy -- then pushes it to an integrated enforcer (firewall/
NAC) that applies allow-only-baseline. web (IT-App), db (IT-Data, :5432), hmi
(OT-Ops), plc (OT-Control, :502). Baseline permits web->db:5432 and hmi->plc:502;
hmi->db is never baselined, so it is denied and flagged as a deviation.

Run from scripts/diagrams:  python3 gen_volume113.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-113-claroty-xdome-lab"


def ch01():
    c = Canvas(960, 460,
        title="Chapter 1 Lab Topology: Observe-then-Enforce OT Segmentation with Claroty xDome",
        subtitle="A passive collector baselines traffic; xDome derives a zone policy; an integrated enforcer applies allow-only-baseline, denying and flagging the unbaselined hmi->db flow",
        svg_title="Chapter 1 lab topology: Claroty xDome baselining traffic passively and pushing a derived policy to an enforcer",
        svg_desc="A passive collector on a SPAN/mirror sees the network without being inline and feeds Claroty xDome, "
                 "which discovers assets, builds a communication baseline, groups assets into virtual zones, and "
                 "derives a least-privilege zone-to-zone policy. Because xDome is passive, it pushes the policy to an "
                 "integrated enforcer -- a firewall or NAC -- that applies allow-only-baseline. The four assets are "
                 "web in zone IT-App, db in zone IT-Data listening on 5432, hmi in zone OT-Ops, and plc in zone "
                 "OT-Control listening on 502. The sanctioned baseline permits web to db on 5432 and hmi to plc on "
                 "502; the hmi to db flow was never sanctioned in the baseline, so the derived policy denies it and "
                 "xDome flags any attempt as a deviation. The volume is two-track: Track 1 describes the real xDome, "
                 "Track 2 reproduces the loop with tcpdump as the collector and an nftables policy as the enforcer.")

    c.node_box(320, 44, 320, 42, "mgmt", [
        Line("Claroty xDome", 11, 700, "#111827"),
        Line("discovery · baseline · zones · derived policy", 8.5, 400, "#374151"),
    ])
    c.node_box(60, 116, 160, 44, "neutral", [
        Line("collector (SPAN)", 10, 700, "#111827"),
        Line("passive discovery", 8.5, 400, "#374151"),
    ])
    c.node_box(740, 116, 160, 44, "alt", [
        Line("enforcer", 10.5, 700, "#111827"),
        Line("firewall / NAC", 8.5, 400, "#374151"),
    ])
    # SPAN feed up to xDome (dashed), policy down to enforcer
    c.raw('<line x1="140" y1="116" x2="330" y2="86" stroke="#33415c" stroke-width="1" stroke-dasharray="3 3"/>')
    c.raw('<text x="150" y="108" font-size="8.5" fill="#374151">mirror feed</text>')
    c.raw('<line x1="630" y1="86" x2="820" y2="116" stroke="#33415c" stroke-width="1.2"/>')
    c.raw('<text x="640" y="108" font-size="8.5" fill="#374151">derived policy</text>')

    c.plane_bar(50, 196, 860, 24, "neutral",
                "Monitored network  ·  enforcer applies allow-only-baseline  ·  everything else denied + flagged")
    c.raw('<line x1="140" y1="196" x2="140" y2="160" stroke="#94a3b8" stroke-width="1.1" stroke-dasharray="3 3"/>')
    c.raw('<line x1="820" y1="196" x2="820" y2="160" stroke="#94a3b8" stroke-width="1.1"/>')

    def zone(x, style, name, sub, extra):
        c.node_box(x, 248, 130, 58, style, [
            Line(name, 11, 700, "#111827"),
            Line(sub, 9, 700, "#166534" if style == "neutral" else "#7f1d1d"),
            Line(extra, 8.5, 400, "#374151"),
        ])
    zone(70,  "neutral", "web", "IT-App", "10.70.1.10")
    zone(290, "data",    "db",  "IT-Data · :5432", "PostgreSQL")
    zone(510, "neutral", "hmi", "OT-Ops", "operator")
    zone(730, "data",    "plc", "OT-Control · :502", "Modbus")
    for cx in (135, 355, 575, 795):
        c.raw(f'<line x1="{cx}" y1="220" x2="{cx}" y2="248" stroke="#94a3b8" stroke-width="1.1"/>')

    c.connector(200, 275, 290, 275, "alt", label="web->db 5432 baseline", label_pos=(120, 336))
    c.connector(640, 275, 730, 275, "alt", label="hmi->plc 502 baseline", label_pos=(600, 336))
    c.connector(510, 298, 420, 298, "warn",
                label="hmi->db DENIED + FLAGGED (deviation)", label_pos=(300, 366))

    c.legend(50, 398, [
        ("alt", "Sanctioned baseline flow (allowed)"),
        ("warn", "Unbaselined flow (denied + flagged)"),
        ("mgmt", "xDome (derives policy)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
