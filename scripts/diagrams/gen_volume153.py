#!/usr/bin/env python3
"""Volume CLIII (Cato Networks) SASE certification-program map.

Chapter 1: the free, Credly-badged Cato SASE certifications (SASE Expert L1/L2,
SSE Fundamentals, Zero Trust, Advanced Security, Deployment & Management, AI in
Cybersecurity, Business Impact & Strategy; 85% pass) over the converged
single-vendor SASE cloud (SD-WAN + FWaaS/SWG/CASB/ZTNA, global backbone,
single-pass). Cato pioneered SASE and SASE certification.

Run from scripts/diagrams:  python3 gen_volume153.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-153-cato-networks-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Cato Networks SASE Certification Tracks",
        subtitle="FREE · Credly badges · 85% to pass · no prereqs · + ISC2 CPE credits · converged single-vendor SASE cloud",
        svg_title="Chapter 1 program map: the free Cato SASE certifications over the converged SASE cloud",
        svg_desc="Cato Networks pioneered SASE and the industry's first SASE certification. The program is "
                 "free, awards Credly badges and downloadable certificates, requires no prerequisites, passes "
                 "at eighty-five percent, and grants ISC2 continuing-education CPE credits. The eight "
                 "certifications span levels: SASE Expert Level 1 and AI in Cybersecurity at the foundational "
                 "level; SASE Expert Level 2 and SSE Fundamentals at the intermediate level; SASE Deployment "
                 "and Management at the technical level; Zero Trust and Advanced Security at the advanced "
                 "level; and SASE Business Impact and Strategy at the executive level. The platform beneath "
                 "is a single-vendor converged SASE cloud combining networking and security: SD-WAN for "
                 "optimized connectivity, Firewall-as-a-Service, Secure Web Gateway, Cloud Access Security "
                 "Broker, Zero Trust Network Access, and intrusion prevention, all delivered from a global "
                 "private backbone of points of presence through a single-pass architecture that decrypts "
                 "and parses traffic once and applies every security function against that one "
                 "representation. Secure Access Service Edge, the Gartner term, converges networking and "
                 "network security into one cloud-delivered service, replacing the traditional stack of "
                 "separate point products with one platform, one policy, and one console; Security Service "
                 "Edge is the security subset of SASE without the networking. Zero Trust Network Access "
                 "replaces the VPN with per-application, identity-verified, least-privilege access.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("CATO NETWORKS — the SASE PIONEER · converged single-vendor SASE cloud", 10.5, 700, "#111827"),
        Line("networking (SD-WAN) + security (SWG/CASB/FWaaS/ZTNA) as ONE cloud service — one platform, one policy", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 26, "neutral", [
        Line("★ FREE · Credly badges + certificates · 85% to pass · NO prerequisites · + ISC2 CPE credits · Cato pioneered SASE certification (badges/education model)", 8, 700, "#111827"),
    ])

    # certs by level
    c.node_box(40, 152, 215, 60, "data", [
        Line("FOUNDATIONAL", 8.3, 700, "#111827"),
        Line("SASE Expert Level 1", 7.5, 700, "#166534"),
        Line("(the anchor)", 7, 400, "#374151"),
        Line("AI in Cybersecurity", 7.3, 400, "#374151"),
    ])
    c.node_box(263, 152, 215, 60, "alt", [
        Line("INTERMEDIATE", 8.3, 700, "#111827"),
        Line("SASE Expert Level 2", 7.3, 400, "#374151"),
        Line("SSE Fundamentals", 7.3, 400, "#374151"),
        Line("(Technical: Deployment & Mgmt)", 6.8, 400, "#374151"),
    ])
    c.node_box(486, 152, 210, 60, "alt", [
        Line("ADVANCED", 8.3, 700, "#111827"),
        Line("Zero Trust (ZTNA)", 7.3, 400, "#374151"),
        Line("Advanced Security", 7.3, 400, "#374151"),
    ])
    c.node_box(704, 152, 216, 60, "data", [
        Line("EXECUTIVE", 8.3, 700, "#111827"),
        Line("SASE Business Impact", 7.3, 400, "#374151"),
        Line("& Strategy", 7.3, 400, "#374151"),
    ])

    # SASE vs SSE
    c.node_box(40, 226, 880, 30, "neutral", [
        Line("SASE (Gartner) = NETWORKING (SD-WAN) + SECURITY (SWG/CASB/FWaaS/ZTNA), one cloud service · SSE = the SECURITY subset (SASE minus the WAN)", 8, 700, "#111827"),
    ])

    # platform
    c.node_box(40, 276, 880, 60, "mgmt", [
        Line("CONVERGED SASE CLOUD", 8.5, 700, "#111827"),
        Line("SD-WAN (active-active links, app-aware routing) · FWaaS · SWG · CASB (shadow-IT discovery) · ZTNA (replaces VPN — per-app least-privilege, rest is DARK) · IPS/anti-malware/sandbox/DLP", 7.2, 400, "#374151"),
        Line("★ SINGLE-PASS (decrypt+parse ONCE, apply all functions) + GLOBAL PRIVATE BACKBONE (PoPs near every user, optimized routing) = converged AND fast", 7.3, 700, "#166534"),
    ])

    c.raw('<text x="40" y="362" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'The perimeter dissolved (cloud apps + remote users) — so backhauling traffic to a data-center appliance stack is absurd. SASE moves security to a cloud PoP NEAR the user.</text>')
    c.raw('<text x="40" y="381" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: free level-based program · convergence vs the point-product stack · backhaul vs edge inspection · single-pass vs service-chaining · private backbone vs internet ·</text>')
    c.raw('<text x="40" y="398" font-size="9.5" font-weight="400" fill="#374151">'
          'active-active SD-WAN link selection · CASB shadow-IT discovery · ZTNA vs VPN attack-surface · SSE relationship + uniform coverage. Completes the SASE cluster (Zscaler XXXV, Netskope CXXVII, Cloudflare CXLII). Defensive.</text>')

    c.legend(40, 430, [
        ("data", "Foundational / executive"),
        ("alt", "Intermediate / advanced"),
        ("neutral", "Structure / concept"),
        ("mgmt", "Converged cloud"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
