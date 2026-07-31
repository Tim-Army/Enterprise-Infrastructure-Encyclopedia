#!/usr/bin/env python3
"""Volume CVII (Cisco ISE + TrustSec Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): Cisco ISE is the policy engine (SGTs,
the SGACL egress matrix, SXP). An IOS-XE enforcer downloads the matrix over
RADIUS and learns IP-SGT bindings over SXP, then enforces on egress. Four
endpoints carry SGTs: web WEB=10, db DB=20, hmi HMI=30, plc PLC=40. The matrix
permits WEB->DB:5432 and HMI->PLC:502 and denies the HMI->DB lateral flow.

Run from scripts/diagrams:  python3 gen_volume107.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-107-cisco-ise-trustsec-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Fabric Microsegmentation with Cisco ISE and TrustSec",
        subtitle="ISE defines SGTs and the SGACL matrix; the IOS-XE enforcer downloads it and enforces by group tag; WEB->DB:5432 and HMI->PLC:502 permitted, HMI->DB denied",
        svg_title="Chapter 1 lab topology: Cisco ISE as policy engine and an IOS-XE enforcer applying an SGACL matrix to four tagged endpoints",
        svg_desc="Cisco ISE at 10.10.0.10 is the policy engine: it defines the Security Group Tags, holds the "
                 "SGACL egress matrix, and distributes IP-SGT bindings over SXP. An IOS-XE enforcement device "
                 "registers with ISE over RADIUS, downloads the matrix, learns the bindings over SXP, and enforces "
                 "on egress with cts role-based enforcement. Four endpoints carry Security Group Tags: web is WEB "
                 "value 10, db is DB value 20 listening on 5432, hmi is HMI value 30, and plc is PLC value 40 "
                 "listening on 502. The egress matrix is default-deny with two permits: WEB to DB on 5432 and HMI to "
                 "PLC on 502. The HMI to DB flow is the lateral movement, denied by the matrix default. The volume is "
                 "two-track: Track 1 uses real ISE and IOS-XE, Track 2 reproduces the IP-SGT binding table and the "
                 "tag-to-tag matrix with Linux nftables on a single host.")

    # policy engine
    c.node_box(330, 50, 300, 44, "mgmt", [
        Line("Cisco ISE  ·  policy engine", 11, 700, "#111827"),
        Line("SGTs · SGACL egress matrix · SXP · 10.10.0.10", 9, 400, "#374151"),
    ])
    # enforcer
    c.plane_bar(190, 118, 580, 28, "neutral",
                "IOS-XE enforcer  ·  cts role-based enforcement  ·  downloads SGACL matrix, enforces on egress")
    # policy -> enforcer links
    c.raw('<line x1="470" y1="94" x2="470" y2="118" stroke="#33415c" stroke-width="1.4"/>')
    c.raw('<line x1="490" y1="94" x2="490" y2="118" stroke="#33415c" stroke-width="1.4" stroke-dasharray="4 3"/>')
    c.raw('<text x="500" y="110" font-size="9" fill="#374151">RADIUS + SXP (IP-SGT bindings)</text>')

    # endpoints
    c.node_box(60, 190, 130, 62, "neutral", [
        Line("web", 11, 700, "#111827"),
        Line("SGT WEB = 10", 9.5, 700, "#166534"),
        Line("app tier", 8.5, 400, "#374151"),
    ])
    c.node_box(285, 190, 130, 62, "data", [
        Line("db", 11, 700, "#111827"),
        Line("SGT DB = 20 · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(510, 190, 130, 62, "neutral", [
        Line("hmi", 11, 700, "#111827"),
        Line("SGT HMI = 30", 9.5, 700, "#166534"),
        Line("operator", 8.5, 400, "#374151"),
    ])
    c.node_box(735, 190, 130, 62, "data", [
        Line("plc", 11, 700, "#111827"),
        Line("SGT PLC = 40 · :502", 9, 700, "#7c2d12"),
        Line("Modbus", 8.5, 400, "#374151"),
    ])
    # enforcer -> endpoints (fabric)
    for cx in (125, 350, 575, 800):
        c.raw(f'<line x1="{cx}" y1="146" x2="{cx}" y2="190" stroke="#94a3b8" stroke-width="1.1"/>')

    # flows
    c.connector(190, 214, 285, 214, "alt",
                label="WEB->DB 5432 permit", label_pos=(120, 296))
    c.connector(510, 236, 415, 236, "warn",
                label="HMI->DB DENIED (lateral)", label_pos=(360, 330))
    c.connector(640, 214, 735, 214, "alt",
                label="HMI->PLC 502 permit", label_pos=(600, 296))

    c.legend(60, 420, [
        ("alt", "Permitted by SGACL (group tag)"),
        ("warn", "Lateral movement (matrix default deny)"),
        ("mgmt", "Policy engine (ISE)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
