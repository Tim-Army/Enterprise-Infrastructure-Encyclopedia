#!/usr/bin/env python3
"""Volume CLVI (BeyondTrust) program map.

Chapter 1: the BeyondTrust University Certified Administrator credentials (one per
product, Credly, ILT + 40Q/75%/2yr) over the PAM platform — Password Safe, EPM,
PRA, Remote Support, AD Bridge, Entitle — securing privileged access.

Run from scripts/diagrams:  python3 gen_volume156.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-156-beyondtrust-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: BeyondTrust Certification Tracks",
        subtitle="BeyondTrust University — Certified Administrator (one per product) · Credly · ILT + 40Q/75%/2yr · PAM",
        svg_title="Chapter 1 program map: the BeyondTrust Certified Administrator credentials over the PAM platform",
        svg_desc="BeyondTrust University issues one Certified Administrator credential per product, delivered as "
                 "Credly verified digital badges. Each certification is granted on completion of the required "
                 "Instructor-Led Training course plus a passing score of seventy-five percent or higher on a "
                 "forty-question exam, delivered online through the BTU portal, open note but completed "
                 "independently, with two attempts allowed. Certifications are valid for two years and renew by "
                 "purchasing new training and passing again, and each course grants up to sixteen hours of "
                 "Continuing Professional Education credit. Eight Certified Administrator programs cover the "
                 "product line: Password Safe for credential vaulting, rotation, and privileged session "
                 "management; Endpoint Privilege Management for Windows, Mac, and Linux for endpoint least "
                 "privilege; Privileged Remote Access for VPN-less brokered privileged access with credential "
                 "injection; Remote Support for secure remote support; AD Bridge for extending Active Directory "
                 "to Linux, Unix, and Mac; and Entitle for cloud and SaaS just-in-time access. The platform "
                 "beneath is Privileged Access Management, the discipline of securing, controlling, and "
                 "monitoring privileged access, the primary path in nearly every breach. BeyondTrust is a PAM "
                 "leader alongside CyberArk.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("BEYONDTRUST — Privileged Access Management (PAM) leader (peer of CyberArk LXXVII)", 10.5, 700, "#111827"),
        Line("secure, control + monitor PRIVILEGED access (admin/root/service) — the #1 path in nearly every breach", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("BeyondTrust University — CERTIFIED ADMINISTRATOR (one credential PER PRODUCT) · Credly digital badges", 8.5, 700, "#111827"),
        Line("uniform mechanics: required INSTRUCTOR-LED TRAINING + 40-question exam / 75% to pass · online BTU portal · OPEN-NOTE, independent · 2 attempts · valid 2 YEARS · up to 16 CPE", 7.2, 400, "#374151"),
    ])

    # 8 products across two rows
    c.node_box(40, 176, 288, 52, "data", [
        Line("PASSWORD SAFE", 8.5, 700, "#111827"),
        Line("credential VAULT + rotation +", 7.2, 400, "#374151"),
        Line("privileged SESSION mgmt (isolate/record)", 7.2, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 52, "data", [
        Line("ENDPOINT PRIVILEGE MGMT (Win/Mac/Linux)", 8.0, 700, "#111827"),
        Line("least privilege on endpoints — remove local", 7.2, 400, "#374151"),
        Line("admin; ELEVATE the app, not the user (3 certs)", 7.2, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 52, "data", [
        Line("PRIVILEGED REMOTE ACCESS", 8.5, 700, "#111827"),
        Line("VPN-less BROKERED access + credential", 7.2, 400, "#374151"),
        Line("INJECTION (user never sees creds) · vendors", 7.2, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 52, "alt", [
        Line("REMOTE SUPPORT (Bomgar)", 8.5, 700, "#111827"),
        Line("secure remote support — granular perms,", 7.2, 400, "#374151"),
        Line("consent, session recording", 7.2, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 52, "alt", [
        Line("AD BRIDGE", 8.5, 700, "#111827"),
        Line("extend Active Directory (auth/SSO/GPO)", 7.2, 400, "#374151"),
        Line("to Linux/Unix/Mac — one identity, one policy", 7.2, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 52, "alt", [
        Line("ENTITLE (cloud/SaaS · acq. 2024)", 8.0, 700, "#111827"),
        Line("JUST-IN-TIME access — self-service request +", 7.2, 400, "#374151"),
        Line("auto-approve + AUTO-EXPIRE (modern PAM)", 7.2, 400, "#374151"),
    ])

    c.raw('<text x="40" y="312" font-size="9.5" font-weight="700" fill="#166534">'
          'The PAM endgame: ELIMINATE STANDING PRIVILEGE — vault + rotate secrets (never exposed), remove local admin, broker + inject + record sessions, grant privilege JUST-IN-TIME then revoke.</text>')
    c.raw('<text x="40" y="331" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Breaks the breach chain at every link: no admin creds to steal (EPM), no static passwords to reuse (Password Safe), no network foothold or disclosed creds (PRA), no idle standing privilege (Entitle). Defensive throughout.</text>')
    c.raw('<text x="40" y="350" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: per-product credential model + exam rule set · privilege attack chain · least privilege / JIT · vault+rotate+inject · session isolation/recording · per-app elevation ·</text>')
    c.raw('<text x="40" y="367" font-size="9.5" font-weight="400" fill="#374151">'
          'brokered VPN-less access · consent-based support · AD-centralized identity · cloud JIT auto-expiry. Identity cluster: CyberArk (LXXVII) peer PAM, SailPoint (CXXXII) IGA, Ping (CL)/Okta (LXXVI) access mgmt, CIEM (Sysdig CLV/Wiz CXLVII).</text>')

    c.legend(40, 398, [
        ("data", "Core PAM"),
        ("alt", "Support/bridge/cloud"),
        ("neutral", "Cert program"),
        ("mgmt", "PAM discipline"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
