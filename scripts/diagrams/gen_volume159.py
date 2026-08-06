#!/usr/bin/env python3
"""Volume CLIX (Delinea) program map.

Chapter 1: the Delinea Security Academy tiers (Associate/Engineer/Consultant;
e-learning + expert-assessed hands-on labs; badges) over the PAM portfolio —
Secret Server, Privilege Manager, Server PAM, DevOps Secrets Vault, ALM, and the
Delinea Platform (ITDR/ISPM). Thycotic + Centrify merged 2021.

Run from scripts/diagrams:  python3 gen_volume159.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-159-delinea-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Delinea Certification Tracks",
        subtitle="Delinea Security Academy — Associate / Engineer / Consultant · e-learning + EXPERT-ASSESSED labs · badges · PAM",
        svg_title="Chapter 1 program map: the Delinea Security Academy tiers over the PAM portfolio",
        svg_desc="Delinea is a Privileged Access Management leader formed from the 2021 merger of Thycotic and "
                 "Centrify. The Security Academy certification program has three tiers. Associate is a self-paced, "
                 "online-only certification of e-learning coursework and an online exam. Engineer validates the "
                 "ability to install, configure, and manage to best practice through hands-on lab challenges "
                 "assessed by a live Delinea Security Academy expert, including break-fix troubleshooting. "
                 "Consultant, by invitation only, adds customizations and integrations through coursework, an "
                 "online exam, and hands-on labs. Certified professionals receive a printable certificate and "
                 "digital badges, and can request Not-for-Resale license keys for practice. The portfolio spans "
                 "Secret Server for credential vaulting, rotation, and session recording; Privilege Manager for "
                 "endpoint least privilege; Server PAM for server privilege elevation and Active Directory "
                 "bridging with MFA; DevOps Secrets Vault for machine and DevOps secrets; Account Lifecycle "
                 "Manager for service-account governance; and the unified Delinea Platform, which extends PAM "
                 "into identity security with Privileged Behavior Analytics, identity threat detection and "
                 "response, and identity security posture management. Delinea is one of the three PAM leaders "
                 "with BeyondTrust and CyberArk.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("DELINEA — Privileged Access Management (PAM) leader · Thycotic + Centrify merged 2021", 10, 700, "#111827"),
        Line("one of the PAM TRIO with BeyondTrust (CLVI) + CyberArk (LXXVII); PAM extending into IDENTITY SECURITY", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("DELINEA SECURITY ACADEMY — 3 TIERS · digital badges + printable cert · free via Delinea University · NFR license keys to practice", 8, 700, "#111827"),
        Line("ASSOCIATE (self-paced e-learning + online exam) → ENGINEER (★ hands-on LABS assessed by a LIVE expert + break-fix) → CONSULTANT (coursework+exam+labs, BY INVITATION)", 7.0, 400, "#374151"),
    ])

    # product tiles
    c.node_box(40, 176, 288, 50, "data", [
        Line("SECRET SERVER (flagship, Thycotic)", 8.0, 700, "#111827"),
        Line("credential VAULT — secret policies, rule-based", 7.0, 400, "#374151"),
        Line("passwords, ROTATION, session record + keystroke log", 6.8, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 50, "data", [
        Line("PRIVILEGE MANAGER (Thycotic)", 8.0, 700, "#111827"),
        Line("ENDPOINT least privilege — remove local admin,", 7.0, 400, "#374151"),
        Line("app control allow/deny/ELEVATE (app not user)", 6.8, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 50, "data", [
        Line("SERVER PAM (Centrify)", 8.0, 700, "#111827"),
        Line("server PEDM (dzdo, not blanket root) +", 7.0, 400, "#374151"),
        Line("AD BRIDGING (Linux/Unix) + MFA at the server", 6.8, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 50, "alt", [
        Line("DEVOPS SECRETS VAULT", 8.0, 700, "#111827"),
        Line("MACHINE / DevOps secrets — high-speed API,", 7.0, 400, "#374151"),
        Line("★ SHORT-LIVED dynamic secrets (JIT for machines)", 6.8, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 50, "alt", [
        Line("ACCOUNT LIFECYCLE MANAGER", 7.8, 700, "#111827"),
        Line("SERVICE-ACCOUNT governance — discover, map", 7.0, 400, "#374151"),
        Line("deps, vault+rotate, decommission (cradle-to-grave)", 6.8, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 50, "alt", [
        Line("DELINEA PLATFORM + IDENTITY SECURITY", 7.4, 700, "#111827"),
        Line("unified SaaS control plane · PBA analytics ·", 7.0, 400, "#374151"),
        Line("★ ITDR (identity threats) + ISPM (reduce risk)", 6.8, 400, "#374151"),
    ])

    c.raw('<text x="40" y="312" font-size="9.5" font-weight="700" fill="#166534">'
          'PAM endgame: eliminate STANDING privilege — vault + rotate secrets (never exposed), remove local admin, granular server PEDM + MFA, short-lived machine secrets, govern service accounts. Prevent + GOVERN + DETECT.</text>')
    c.raw('<text x="40" y="331" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Prevention is necessary-but-not-sufficient: a compromised admin/insider still misuses privilege → PBA/ITDR detect anomalies, ISPM reduces identity attack surface. Defensive throughout.</text>')
    c.raw('<text x="40" y="350" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: 3-tier program + expert-assessed practical value · end-to-end merged portfolio · policy vault + rotation + session recording · endpoint app control · server PEDM+AD+MFA ·</text>')
    c.raw('<text x="40" y="367" font-size="9.5" font-weight="400" fill="#374151">'
          'machine short-lived secrets · service-account lifecycle governance · unified-platform prevent/govern/detect. PAM trio: BeyondTrust (CLVI), CyberArk (LXXVII); identity cluster: SailPoint (CXXXII), Ping (CL)/Okta (LXXVI), CIEM (Sysdig CLV/Wiz CXLVII).</text>')

    c.legend(40, 398, [
        ("data", "Core PAM"),
        ("alt", "DevOps/accounts/platform"),
        ("neutral", "Academy program"),
        ("mgmt", "Identity security"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
