#!/usr/bin/env python3
"""Volume CXVIII (Arista MSS-Group Build-It-Yourself Lab) topology.

Chapter 1: CloudVision manages an EOS fabric enforcing group-based policy at
line rate. Endpoints are in security groups: web (SG-Web), db (SG-DB, :5432),
hmi (SG-Mgmt), plc (SG-OT, :502). MSS-Group permits SG-Web->SG-DB:5432 and
SG-Mgmt->SG-OT:502 and denies the rest; MSS macro redirects the SG-Web->SG-DB
flow through a firewall for inspection.

Run from scripts/diagrams:  python3 gen_volume118.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-118-arista-mss-group-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Group-Based Fabric Segmentation with Arista MSS-Group",
        subtitle="EOS enforces group policy at line rate (SG-Web->SG-DB, SG-Mgmt->SG-OT; default deny); MSS macro redirects the SG-Web->SG-DB flow through a firewall for inspection",
        svg_title="Chapter 1 lab topology: Arista EOS enforcing group policy with an MSS macro firewall redirect",
        svg_desc="CloudVision manages an Arista EOS fabric that enforces group-based policy in the switch silicon at "
                 "line rate. Endpoints are in security groups: web in SG-Web, db in SG-DB listening on 5432, hmi in "
                 "SG-Mgmt, and plc in SG-OT listening on 502. MSS-Group permits only SG-Web to SG-DB on 5432 and "
                 "SG-Mgmt to SG-OT on 502, denying every other group pair including SG-Mgmt to SG-DB. MSS "
                 "macro-segmentation redirects the SG-Web to SG-DB flow through an inserted firewall for inspection "
                 "without re-cabling, so a malicious payload on that flow is dropped. The volume is two-track: Track 1 "
                 "describes EOS and CloudVision, Track 2 reproduces group policy and the firewall redirect with Linux "
                 "nftables.")

    c.node_box(320, 50, 320, 44, "mgmt", [
        Line("CloudVision · EOS fabric", 11, 700, "#111827"),
        Line("security groups + MSS policy", 9, 400, "#374151"),
    ])
    c.plane_bar(190, 118, 580, 28, "neutral",
                "EOS fabric  ·  group policy at line rate  ·  default deny between groups")
    c.raw('<line x1="480" y1="94" x2="480" y2="118" stroke="#33415c" stroke-width="1.4"/>')

    c.node_box(60, 190, 130, 62, "neutral", [
        Line("web", 11, 700, "#111827"), Line("SG-Web", 9.5, 700, "#166534"), Line("10.120.1.10", 8.5, 400, "#374151")])
    c.node_box(285, 190, 130, 62, "data", [
        Line("db", 11, 700, "#111827"), Line("SG-DB · :5432", 9, 700, "#7f1d1d"), Line("PostgreSQL", 8.5, 400, "#374151")])
    c.node_box(510, 190, 130, 62, "neutral", [
        Line("hmi", 11, 700, "#111827"), Line("SG-Mgmt", 9.5, 700, "#166534"), Line("operator", 8.5, 400, "#374151")])
    c.node_box(735, 190, 130, 62, "data", [
        Line("plc", 11, 700, "#111827"), Line("SG-OT · :502", 9, 700, "#7c2d12"), Line("Modbus", 8.5, 400, "#374151")])
    for cx in (125, 350, 575, 800):
        c.raw(f'<line x1="{cx}" y1="146" x2="{cx}" y2="190" stroke="#94a3b8" stroke-width="1.1"/>')

    c.connector(190, 214, 285, 214, "alt", label="SG-Web->SG-DB 5432", label_pos=(105, 300))
    c.connector(510, 236, 415, 236, "warn", label="SG-Mgmt->SG-DB DENIED", label_pos=(350, 330))
    c.connector(640, 214, 735, 214, "alt", label="SG-Mgmt->SG-OT 502", label_pos=(600, 300))

    # MSS macro firewall redirect on the web->db flow
    c.node_box(150, 356, 260, 44, "alt", [
        Line("MSS macro: firewall redirect", 10, 700, "#111827"),
        Line("SG-Web -> SG-DB inspected", 8.5, 400, "#374151"),
    ])
    c.raw('<line x1="237" y1="228" x2="237" y2="356" stroke="#166534" stroke-width="1.1" stroke-dasharray="4 3"/>')

    c.legend(60, 430, [
        ("alt", "Permitted by group policy"),
        ("warn", "Denied (default between groups)"),
        ("mgmt", "CloudVision (groups + MSS)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
