#!/usr/bin/env python3
"""Volume CXV (TXOne Networks Build-It-Yourself Lab) topology.

Chapter 1: TXOne EdgeIPS sits inline as a transparent bump-in-the-wire in front
of an unpatchable PLC, applying a virtual patch, a trust list, and command
filtering. The operator's sanctioned Modbus read passes; the attacker's exploit
and untrusted traffic are dropped inline; the PLC is shielded without being
patched. StellarProtect locks the engineering host to an application allowlist,
blocking a malware binary.

Run from scripts/diagrams:  python3 gen_volume115.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-115-txone-networks-lab"


def ch01():
    c = Canvas(960, 440,
        title="Chapter 1 Lab Topology: Inline OT Protection with TXOne EdgeIPS + StellarProtect",
        subtitle="A transparent inline EdgeIPS virtual-patches an unpatchable PLC and enforces a trust list and command filter; StellarProtect locks the engineering host to an allowlist",
        svg_title="Chapter 1 lab topology: TXOne EdgeIPS inline in front of an unpatchable PLC, plus StellarProtect endpoint lockdown",
        svg_desc="TXOne EdgeIPS is inserted inline as a transparent bump-in-the-wire in front of an unpatchable PLC "
                 "on port 502, applying a virtual patch, a trust list, and command filtering without changing the "
                 "PLC's IP. The operator's sanctioned Modbus read passes through to the PLC. The attacker's exploit "
                 "and any untrusted traffic are dropped inline, so the vulnerable PLC is shielded without being "
                 "patched. StellarProtect locks the engineering workstation to a hash-based application allowlist, so "
                 "an unapproved malware binary is blocked from executing. The volume is two-track: Track 1 describes "
                 "EdgeIPS, EdgeFire, and StellarProtect, Track 2 builds a transparent inline inspector and an "
                 "application-lockdown launcher in Python plus nftables.")

    c.node_box(40, 108, 120, 50, "neutral", [
        Line("hmi", 11, 700, "#111827"), Line("operator", 9, 400, "#374151")])
    c.node_box(40, 190, 120, 50, "warn", [
        Line("atk", 11, 700, "#111827"), Line("attacker", 9, 400, "#7f1d1d")])

    c.node_box(320, 118, 280, 122, "mgmt", [
        Line("TXOne EdgeIPS (inline)", 11, 700, "#111827"),
        Line("transparent bump-in-the-wire", 9, 400, "#374151"),
        Line("virtual patch", 9.5, 700, "#166534"),
        Line("trust list · command filter", 9.5, 700, "#166534"),
        Line("no IP change to the PLC", 8.5, 400, "#374151"),
    ])
    c.node_box(730, 140, 175, 76, "data", [
        Line("plc · :502", 10.5, 700, "#111827"),
        Line("unpatchable", 9, 700, "#7c2d12"),
        Line("shielded, not patched", 8.5, 400, "#374151"),
    ], dashed=True)

    c.connector(160, 133, 320, 150, "alt", label="Modbus read", label_pos=(175, 120))
    c.connector(160, 215, 320, 205, "warn", label="exploit / untrusted", label_pos=(165, 250))
    c.connector(600, 178, 730, 178, "alt", label="sanctioned only", label_pos=(615, 150))
    c.raw('<text x="618" y="238" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'exploit dropped inline; PLC never patched</text>')

    # endpoint lockdown row
    c.node_box(40, 300, 120, 50, "warn", [
        Line("malware", 10.5, 700, "#111827"), Line("binary", 9, 400, "#7f1d1d")])
    c.node_box(320, 296, 280, 58, "mgmt", [
        Line("ews (engineering host)", 10.5, 700, "#111827"),
        Line("StellarProtect: application lockdown", 9, 700, "#166534"),
    ])
    c.connector(160, 325, 320, 325, "warn", label="blocked: not allowlisted", label_pos=(168, 372))

    c.legend(40, 400, [
        ("alt", "Allowed"),
        ("warn", "Blocked (inline / lockdown)"),
        ("mgmt", "TXOne controls"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
