#!/usr/bin/env python3
"""House-style diagrams for Volume CM — Tim's Lab Gear (Chapter 03).
Run from scripts/diagrams/ :  python3 gen_volume0900.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-900-tims-lab-gear"
INK = "#111827"; GREY = "#374151"; MUTE = "#6b7280"


def topology():
    c = Canvas(
        960, 620,
        title="Tim's Lab — Network Topology",
        subtitle="ISP modem → UCGF edge gateway → one Cisco Nexus that trunks the data VLANs to five PowerEdge hosts (native 1611); out-of-band management is a separate segment.",
        svg_title="Tim's Lab network topology",
        svg_desc="From the top: an ISP modem hands off to the UCGF (Ubiquiti UniFi Cloud Gateway "
                 "Fiber) on WAN1; the UCGF is the router, firewall, DHCP server and Wi-Fi controller "
                 "and holds the .1 gateway for every VLAN. A 10 Gb SFP+ uplink (UCGF port 6 to "
                 "port-channel1) reaches a single Cisco Nexus 9000 C9396PX switch (nexus-9k-1) that "
                 "trunks the data VLANs to five Dell PowerEdge hosts at rack units ru08 through ru12, "
                 "each with four 10 Gb NICs, native VLAN 1611. The Unraid NAS sits on VLAN 1. iDRAC "
                 "out-of-band management and the switch mgmt0 live on the separate 10.30.99.0/24 segment.")

    # ISP modem (redacted) → UCGF edge gateway
    c.node_box(392, 70, 176, 44, "neutral", [
        Line("ISP modem", 11, 700, INK),
        Line("internet handoff (redacted)", 8.5, 400, GREY),
    ])
    c.connector(480, 114, 480, 132, "mgmt")
    c.text(494, 128, "WAN1 · UCGF port 5", size=9, weight=600, color=MUTE, anchor="start")
    c.node_box(350, 132, 260, 58, "mgmt", [
        Line("UCGF — UniFi Cloud Gateway Fiber", 12, 700, INK),
        Line("edge router · firewall · DHCP · Wi-Fi", 9, 400, GREY),
        Line("holds .1 gateway for every VLAN", 9, 400, GREY),
    ])

    # UCGF → Nexus core switch (10 GbE SFP+ uplink)
    c.connector(480, 190, 480, 214, "mgmt")
    c.text(494, 208, "port 6 SFP+ 10 GbE ↔ port-channel1", size=9, weight=600, color=MUTE, anchor="start")
    c.node_box(350, 214, 260, 58, "mgmt", [
        Line("nexus-9k-1", 13, 700, INK),
        Line("Cisco Nexus 9000 C9396PX · NX-OS 7.0(3)I2(2d)", 9, 400, GREY),
        Line("Layer 2 trunk (native 1611) · LACP", 9, 400, GREY),
    ])

    # Five hosts
    hosts = [("ru08", None), ("ru09", None), ("ru10", None), ("ru11", None), ("ru12", "proxmox-1")]
    xs = [18, 208, 398, 588, 778]
    for (ru, name), x in zip(hosts, xs):
        cx = x + 83
        c.connector(480, 272, cx, 352, "alt")
        lines = [Line(ru, 12, 700, INK)]
        if name:
            lines.append(Line(name, 10, 700, "#166534"))
            lines.append(Line("R640 · Proxmox VE · .10", 8.5, 400, GREY))
        else:
            lines.append(Line("PowerEdge (TBD)", 9, 400, GREY))
            lines.append(Line("4×10G · vmnic0–3", 8.5, 400, GREY))
        c.node_box(x, 352, 166, 58, "alt" if name else "neutral", lines)
    c.text(150, 335, "trunk · 4×10G per host", size=9.5, weight=600, color="#166534", anchor="middle")

    # Unraid NAS — a VLAN 1 leaf off the Nexus (Eth1/33-34)
    c.node_box(18, 452, 230, 52, "data", [
        Line("unraid-1", 12, 700, INK),
        Line("Unraid NAS · 192.168.1.209 · VLAN 1", 9, 400, GREY),
        Line("→ nexus-9k-1 Eth1/33-34 · bulk / ISO", 8.5, 400, GREY),
    ])

    # Out-of-band management plane
    c.node_box(18, 528, 924, 56, "warn", [
        Line("Out-of-band management — 10.30.99.0/24", 11, 700, "#7c2d12"),
        Line("Nexus mgmt0 .250  ·  iDRAC on every host (access VLAN 1611)  ·  reached by routing through 10.30.99.1 (UCGF), not by a data-VLAN tag", 9, 400, "#7c2d12"),
    ], dashed=True)

    c.legend(18, 606, [
        ("mgmt", "Edge / uplink"),
        ("alt", "Data trunk (tagged VLANs)"),
        ("data", "Storage / VLAN 1"),
        ("warn", "Out-of-band management"),
    ])
    c.save(f"{OUT}/chapter-03-lab-network-topology.svg")


def rack():
    c = Canvas(
        640, 640,
        title="Tim's Lab — Rack Elevation",
        subtitle="Physical placement: switch on top, five PowerEdge hosts (ru08–ru12 = actual rack units), the Unraid NAS, and an APC 30 A UPS in the bottom 5 U.",
        svg_title="Tim's Lab rack elevation",
        svg_desc="A rack elevation with, from top: the Cisco Nexus 9000 C9396PX switch, five Dell "
                 "PowerEdge servers whose hostnames encode their actual rack units (ru08 through ru12), "
                 "the Unraid NAS, and an APC 30 A UPS occupying the bottom five rack units — each "
                 "labeled with its role and management address.")

    left, w = 150, 360
    # rack rails
    c.raw(f'<rect x="{left-24}" y="86" width="{w+48}" height="508" rx="6" fill="none" stroke="{MUTE}" stroke-width="1.5"/>')
    c.raw(f'<line x1="{left-12}" y1="86" x2="{left-12}" y2="594" stroke="#93a3b8" stroke-width="1"/>')
    c.raw(f'<line x1="{left+w+12}" y1="86" x2="{left+w+12}" y2="594" stroke="#93a3b8" stroke-width="1"/>')

    rows = [
        ("mgmt",  "nexus-9k-1", "Cisco Nexus 9000 C9396PX · OOB mgmt0 10.30.99.250"),
        ("alt",   "ru12 · proxmox-1", "PowerEdge R640 · Proxmox VE · 10.30.161.10"),
        ("neutral", "ru11 · host (TBD)", "PowerEdge (TBD) · 4×10G"),
        ("neutral", "ru10 · host (TBD)", "PowerEdge (TBD) · 4×10G"),
        ("neutral", "ru09 · host (TBD)", "PowerEdge (TBD) · 4×10G"),
        ("neutral", "ru08 · host (TBD)", "PowerEdge (TBD) · 4×10G"),
        ("data",  "unraid-1", "Unraid NAS · 192.168.1.209 · VLAN 1"),
        ("warn",  "APC 30 A UPS", "bottom 5 U · feeds the whole rack"),
    ]
    y = 96
    for plane, name, sub in rows:
        c.node_box(left, y, w, 54, plane, [
            Line(name, 12, 700, INK),
            Line(sub, 9, 400, GREY),
        ])
        y += 62
    c.save(f"{OUT}/chapter-03-rack-elevation.svg")


if __name__ == "__main__":
    topology(); rack()
