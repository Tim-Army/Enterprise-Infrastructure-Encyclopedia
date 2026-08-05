#!/usr/bin/env python3
"""Volume CL (Ping Identity) certification-program map.

Chapter 1: the product-specific Ping Identity Certified Professional program
(PingFederate / PingAccess / PingDirectory / PingOne / DaVinci / Advanced
Identity Cloud / Identity Governance / PingAM) over the merged Ping + ForgeRock
portfolio. ~$395, proctored, ~70Q/90min, pass marks 64-75% (published).

Run from scripts/diagrams:  python3 gen_volume150.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-150-ping-identity-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Ping Identity Certification Tracks",
        subtitle="product-specific (Professional/Advanced/Expert) · Ping + ForgeRock merger · ~$395 · ~70Q/90min · pass 64-75% (published)",
        svg_title="Chapter 1 program map: the product-specific Ping Identity program over the merged Ping + ForgeRock portfolio",
        svg_desc="The Ping Identity Certified Professional program is product-specific: proctored exams at "
                 "the Certified Professional level, plus Advanced Administrator and Expert tiers, each tied "
                 "to a product. Certified Professional exams include PingFederate for federation, PingAccess "
                 "for access management, PingDirectory for the directory, PingOne for cloud single sign-on "
                 "and multi-factor authentication, PingOne DaVinci for identity orchestration, PingOne "
                 "Advanced Identity Cloud, PingOne Identity Governance, and PingAM for access management. "
                 "Each exam is remotely proctored, multiple choice, roughly seventy questions in ninety "
                 "minutes, priced around three hundred ninety-five US dollars, with pass marks that vary by "
                 "product from sixty-four to seventy-five percent, and a voucher valid for a single attempt; "
                 "Ping publishes these mechanics. The portfolio reflects the 2023 Ping Identity and "
                 "ForgeRock merger, spanning Ping-origin products PingFederate, PingAccess, PingDirectory, "
                 "PingOne, PingID, PingOne DaVinci, and PingOne Protect, and ForgeRock-origin products "
                 "rebranded as PingOne Advanced Identity Cloud, PingAM, PingIDM, PingDS, PingGateway, and "
                 "PingOne Identity Governance. Together they cover the identity stack: authentication and "
                 "federation, access management and authorization, cloud identity, multi-factor and "
                 "passwordless authentication with adaptive threat protection, identity orchestration, the "
                 "directory, and governance, for both workforce and customer identity.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("PING IDENTITY — identity & access management (federation + access is the depth)", 10.5, 700, "#111827"),
        Line("IDENTITY IS THE CONTROL PLANE · workforce + customer (CIAM) · merged with ForgeRock (2023)", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 26, "neutral", [
        Line("PRODUCT-SPECIFIC program — each exam certifies ONE product · Certified Professional -> Advanced Administrator / Expert · certify for what you OPERATE", 8, 700, "#111827"),
    ])

    # Ping-origin certs
    c.node_box(40, 152, 430, 74, "alt", [
        Line("PING-ORIGIN products", 8.5, 700, "#111827"),
        Line("PingFederate (PFP-001, federation, 64%) — the flagship", 7.3, 400, "#374151"),
        Line("PingAccess (PAP-001, access mgmt, 64%) · PingDirectory (PDP-001, 67%)", 7.3, 400, "#374151"),
        Line("PingOne (POP-001, cloud SSO+MFA, 75%) · DaVinci (PODV-001, orchestration, 68%)", 7.3, 400, "#374151"),
    ])
    c.node_box(490, 152, 430, 74, "data", [
        Line("FORGEROCK-ORIGIN products (rebranded)", 8.5, 700, "#111827"),
        Line("PingOne Advanced Identity Cloud (PAICP-001, IAM SaaS, 70%)", 7.3, 400, "#374151"),
        Line("PingOne Identity Governance (IGAP-001, IGA, 70%)", 7.3, 400, "#374151"),
        Line("PingAM (PT-AM-CPE, access mgmt) · PingIDM / PingDS / PingGateway", 7.3, 400, "#374151"),
    ])

    c.node_box(40, 240, 880, 28, "alt", [
        Line("all ~$395 (€365/£310) · remotely PROCTORED · multiple choice · ~70Q / 90min (PingOne 60-70; PingAM ~100) · voucher = single attempt · Ping PUBLISHES the mechanics", 7.5, 700, "#111827"),
    ])

    # the identity stack the portfolio covers
    c.node_box(40, 282, 880, 60, "mgmt", [
        Line("THE IDENTITY STACK the portfolio covers", 8.5, 700, "#111827"),
        Line("AUTHENTICATE (PingOne/PingID) · FEDERATE (PingFederate — SAML/OIDC/OAuth, signed assertions) · AUTHORIZE (PingAccess/PingAM — central policy)", 7.3, 400, "#374151"),
        Line("MFA/PASSWORDLESS + adaptive risk (PingID/PingOne Protect) · ORCHESTRATE (DaVinci no-code flows) · STORE (PingDirectory/DS) · GOVERN (Identity Governance — the 'should')", 7.3, 400, "#374151"),
    ])

    c.raw('<text x="40" y="366" font-size="9.5" font-weight="700" fill="#166534">'
          'Completes the identity shelf: Okta (IDaaS, LXXVI) · SailPoint (IGA, CXXXII) · CyberArk (PAM) · Ping (federation + access). CAN (access mgmt) vs SHOULD (governance).</text>')
    c.raw('<text x="40" y="385" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Pass marks VARY by product (64% PingFederate/PingAccess · 67% PingDirectory · 68% DaVinci · 70% Advanced Identity Cloud/Governance · 75% PingOne) — verified per exam.</text>')
    c.raw('<text x="40" y="404" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: program-by-product · portfolio-to-function map · authN-vs-authZ · SSO/federated trust · signed assertion (forgery rejected) · least-privilege OAuth scopes ·</text>')
    c.raw('<text x="40" y="421" font-size="9.5" font-weight="400" fill="#374151">'
          'central policy access decisions · cloud-vs-on-prem elastic scale · adaptive step-up by risk · MFA/passwordless takeover math · branching orchestration flow · access certification (privilege creep).</text>')

    c.legend(40, 452, [
        ("alt", "Ping-origin"),
        ("data", "ForgeRock-origin"),
        ("neutral", "Program shape"),
        ("mgmt", "Platform / stack"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
