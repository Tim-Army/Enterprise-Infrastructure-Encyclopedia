#!/usr/bin/env python3
"""Volume CLXIII (Trend Micro) program map.

Chapter 1: the Trend Micro Certified Professional program (per product, scenario-
based exams, on-demand + ILT) over the Trend Vision One platform — XDR + ASRM +
threat intel, spanning Apex One, Deep Security/Cloud, email/network, Smart
Protection Network.

Run from scripts/diagrams:  python3 gen_volume163.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-163-trend-micro-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Trend Micro Certification Tracks",
        subtitle="Trend Micro Certified Professional (per product, scenario-based) · Trend Vision One platform · defensive",
        svg_title="Chapter 1 program map: the Trend Micro Certified Professional program over Trend Vision One",
        svg_desc="Trend Micro Education offers product certifications through on-demand self-paced training and "
                 "instructor-led courses, for partners, customers, and communities. The credential is the Trend "
                 "Micro Certified Professional, earned per product, validating the skills to deploy and manage a "
                 "solution; exams combine multiple-choice with scenario-based items testing practical judgment. "
                 "The platform beneath is Trend Vision One, the unified cybersecurity platform with three "
                 "pillars: XDR, extended detection and response correlating telemetry across endpoint, email, "
                 "network, cloud, and identity into one attack story; Attack Surface Risk Management, "
                 "proactively discovering and risk-scoring the attack surface to reduce it before an attack; "
                 "and threat intelligence from the Smart Protection Network, a global backbone where a threat "
                 "seen anywhere protects everyone. Products include Apex One endpoint protection with layered "
                 "detection and virtual patching, Deep Security and Cloud Security for server, cloud, and "
                 "container workloads, Cloud App Security for email, TippingPoint and Deep Discovery for "
                 "network, and Zero Trust Secure Access. Trend Micro is a veteran defensive cybersecurity vendor.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("TREND MICRO — veteran defensive cybersecurity (founded 1988), now platform-centric", 10, 700, "#111827"),
        Line("★ TREND VISION ONE — one unified platform: XDR + Attack Surface Risk Mgmt (ASRM) + threat intel, across ALL layers", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 34, "neutral", [
        Line("TREND MICRO EDUCATION — CERTIFIED PROFESSIONAL (per product; deploy + manage) · on-demand self-paced + instructor-led · partner / customer / community", 7.6, 700, "#111827"),
        Line("exams combine MULTIPLE-CHOICE + ★ SCENARIO-BASED items (server-protection requirements, policy conflicts, tenant isolation) — test practical JUDGMENT, not recall. 2026: cloud/container, automated response, ML, zero-trust", 6.7, 400, "#374151"),
    ])

    # 3 pillars
    c.node_box(40, 168, 288, 44, "data", [
        Line("XDR (detect + respond)", 8.2, 700, "#111827"),
        Line("correlate endpoint+email+network+cloud+identity → one attack story", 6.4, 400, "#374151"),
    ])
    c.node_box(336, 168, 288, 44, "data", [
        Line("★ ASRM (reduce risk — proactive)", 7.6, 700, "#111827"),
        Line("discover + RISK-SCORE the attack surface (before attack)", 6.6, 400, "#374151"),
    ])
    c.node_box(632, 168, 288, 44, "data", [
        Line("THREAT INTEL (Smart Protection Network)", 7.2, 700, "#111827"),
        Line("global sensors — seen anywhere = protects everyone", 6.6, 400, "#374151"),
    ])

    # products
    c.node_box(40, 224, 288, 46, "alt", [
        Line("APEX ONE (endpoint + EDR)", 8.0, 700, "#111827"),
        Line("signature+behavior+ML+exploit · ★ VIRTUAL PATCHING", 6.5, 400, "#374151"),
    ])
    c.node_box(336, 224, 288, 46, "alt", [
        Line("DEEP SECURITY / CLOUD (workloads)", 7.4, 700, "#111827"),
        Line("IPS/virtual-patch, anti-malware, integrity mon, CSPM · phys/virt/cloud/container", 6.0, 400, "#374151"),
    ])
    c.node_box(632, 224, 288, 46, "alt", [
        Line("EMAIL + NETWORK", 8.0, 700, "#111827"),
        Line("Cloud App Security (M365/Google) · TippingPoint IPS · Deep Discovery (APT sandbox)", 5.9, 400, "#374151"),
    ])

    c.raw('<text x="40" y="298" font-size="9.5" font-weight="700" fill="#166534">'
          'PROTECT (endpoint/workload/email/network, layered + virtual patching) + DETECT/RESPOND (XDR cross-layer) + REDUCE RISK (ASRM proactive) — informed by global THREAT INTEL. Zero Trust Secure Access ties access to LIVE risk. Defensive throughout.</text>')
    c.raw('<text x="40" y="320" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: Certified-Professional program + scenario-based exam · one-platform-vs-silos · XDR correlation → attack story · layered endpoint + virtual-patch window · workload modules + CSPM ·</text>')
    c.raw('<text x="40" y="337" font-size="9.5" font-weight="400" fill="#374151">'
          'ASRM risk-scored prioritization (incl. shadow IT) · email/network as XDR sensors · Smart Protection Network shared intel + risk-based ZTSA. Peers: Sophos (CLXII)/SentinelOne (CLI)/CrowdStrike (L) endpoint, Sysdig (CLV)/Wiz (CXLVII) cloud, Fortinet (XIX) network, Rapid7 (CXXXVII) SOC.</text>')

    c.legend(40, 366, [
        ("data", "Vision One pillars"),
        ("alt", "Products"),
        ("neutral", "Cert program"),
        ("mgmt", "Defensive platform"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
