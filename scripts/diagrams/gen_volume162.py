#!/usr/bin/env python3
"""Volume CLXII (Sophos) program map.

Chapter 1: the Sophos Academy role tiers (Technician/Administrator/Engineer/
Architect, per product) over the Sophos platform — Central, Intercept X (+
CryptoGuard), Sophos Firewall, Synchronized Security (Security Heartbeat), and MDR/XDR.

Run from scripts/diagrams:  python3 gen_volume162.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-162-sophos-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Sophos Certification Tracks",
        subtitle="Sophos Academy — Technician / Administrator / Engineer / Architect (per product) · defensive cybersecurity",
        svg_title="Chapter 1 program map: the Sophos Academy role tiers over the Sophos security platform",
        svg_desc="Sophos offers role-based technical certifications through Sophos Academy across four tiers, "
                 "earned per product: Technician for support, Administrator for day-to-day operations, Engineer "
                 "for configuration, and Architect for deployment and design. Training is instructor-led or "
                 "self-study eLearning, with free foundational training and separate customer and partner "
                 "tracks. The platform beneath is Sophos Central, the single cloud console managing every "
                 "Sophos product; Intercept X endpoint protection with Deep Learning AI detection, Exploit "
                 "Prevention, and CryptoGuard anti-ransomware that detects malicious encryption and rolls back "
                 "files; the Sophos Firewall next-generation firewall with TLS inspection, IPS, and web and app "
                 "control on the Xstream architecture; Synchronized Security, which links firewall and endpoint "
                 "through the Security Heartbeat so a red endpoint is automatically isolated to stop lateral "
                 "movement; and Sophos MDR, a twenty-four-seven managed detection and response service built on "
                 "XDR. Sophos is a defensive cybersecurity vendor, a peer of the endpoint, firewall, and MDR vendors.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("SOPHOS — defensive cybersecurity: ENDPOINT + FIREWALL + MDR, unified by Sophos Central", 10, 700, "#111827"),
        Line("★ SYNCHRONIZED SECURITY — products that WORK TOGETHER (share intel + respond as one), not silos", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 34, "neutral", [
        Line("SOPHOS ACADEMY — role-based tiers, PER PRODUCT · instructor-led OR self-study eLearning · FREE foundational · customer + partner tracks", 7.8, 700, "#111827"),
        Line("TECHNICIAN (support) → ADMINISTRATOR (day-to-day ops) → ENGINEER (configure) → ARCHITECT (deploy + design; e.g. AT15 Central Endpoint)", 7.2, 400, "#374151"),
    ])

    # product tiles
    c.node_box(40, 168, 288, 50, "data", [
        Line("INTERCEPT X (endpoint + EDR)", 8.0, 700, "#111827"),
        Line("★ Deep Learning AI · Exploit Prevention ·", 6.9, 400, "#374151"),
        Line("★ CryptoGuard anti-ransomware (roll BACK files)", 6.7, 400, "#374151"),
    ])
    c.node_box(336, 168, 288, 50, "data", [
        Line("SOPHOS FIREWALL (NGFW, XGS)", 8.0, 700, "#111827"),
        Line("TLS inspection · IPS · web/app control ·", 6.9, 400, "#374151"),
        Line("Xstream architecture · Sandstorm sandbox", 6.7, 400, "#374151"),
    ])
    c.node_box(632, 168, 288, 50, "data", [
        Line("SOPHOS MDR / XDR", 8.0, 700, "#111827"),
        Line("★ 24/7 managed SOC-as-a-service · threat hunt ·", 6.7, 400, "#374151"),
        Line("XDR correlate endpoint+net+email+cloud+identity", 6.5, 400, "#374151"),
    ])

    c.node_box(40, 228, 880, 34, "alt", [
        Line("★ SYNCHRONIZED SECURITY — the SECURITY HEARTBEAT: a live link (endpoint ⇄ firewall) reports GREEN/YELLOW/RED health.", 7.6, 700, "#111827"),
        Line("Endpoint detects a threat (RED) → FIREWALL AUTO-ISOLATES the device in seconds → lateral movement STOPPED. Detect (endpoint) + contain (firewall) as ONE. The Sophos signature differentiator.", 6.9, 400, "#374151"),
    ])

    c.raw('<text x="40" y="290" font-size="9.5" font-weight="700" fill="#166534">'
          'BEHAVIOR-BASED, DEFENSE-IN-DEPTH: detect the FILE (Deep Learning) + block the TECHNIQUE (Exploit Prevention) + stop the ENCRYPTION + rollback (CryptoGuard) + inspect the NETWORK + synchronize + 24/7 MDR. Defensive throughout.</text>')
    c.raw('<text x="40" y="312" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: role-tier×product program · one-console vs silos · layered endpoint (DL/exploit/EDR) · CryptoGuard detect+rollback · NGFW deep inspection vs port-only · heartbeat auto-isolation ·</text>')
    c.raw('<text x="40" y="329" font-size="9.5" font-weight="400" fill="#374151">'
          'XDR correlation + 24/7 MDR response · segmented policy + scaled deployment (update caches/relays/AD sync). Peers: SentinelOne (CLI)/CrowdStrike (L)/Trellix (LXX) endpoint, Fortinet (XIX)/Check Point (LXXIII)/Palo Alto (XVI) firewall, Rapid7 (CXXXVII) MDR.</text>')

    c.legend(40, 360, [
        ("data", "Products (endpoint/fw/MDR)"),
        ("alt", "Synchronized Security"),
        ("neutral", "Academy program"),
        ("mgmt", "Defensive platform"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
