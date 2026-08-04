#!/usr/bin/env python3
"""Volume CXXXII (SailPoint Certification Tracks) program map.

Chapter 1: SailPoint's two-track program in Identity University — three
training-gated Knowledge Credentials (Leader/Professional/Expert, free
attempts, badges never expire) and four proctored role-based Professional
Certifications ($300-$400, two attempts, 364 days to schedule, two-year
recertification) split across Identity Security Cloud and on-premises
IdentityIQ. Both rest on the IGA disciplines the volume teaches.

Run from scripts/diagrams:  python3 gen_volume132.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-132-sailpoint-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: SailPoint Certification (Identity Governance)",
        subtitle="Two tracks — free, never-expiring Knowledge Credentials and proctored, 2-year Professional Certifications — across Identity Security Cloud and IdentityIQ",
        svg_title="Chapter 1 program map: the SailPoint certification program",
        svg_desc="SailPoint's Professional Certification and Credentialing Program runs in Identity University and "
                 "has two parallel tracks. The Knowledge Credentials are training-gated, online, immediate, and "
                 "adaptive, with badges that never expire: Identity Security Leader, a free product-agnostic path "
                 "with three free attempts and up to 45 minutes for up to 30 questions; Identity Security "
                 "Professional, with two free attempts and up to 90 minutes for up to 51 questions; and Identity "
                 "Security Expert, with two free attempts and up to 90 minutes for up to 65 questions, covering "
                 "transforms, rules, workflows, event triggers, APIs, and connectivity. The Professional "
                 "Certifications are proctored and role-based, each including two attempts with 364 days to "
                 "schedule, and renewing on a two-year Recertification Program launched in February 2026: on "
                 "Identity Security Cloud, the Certified Identity Security Administrator at 400 dollars with six "
                 "months of experience recommended and the Certified Identity Security Engineer at 400 dollars with "
                 "one year recommended, which adds Architecture and Rules and Transforms; on on-premises "
                 "IdentityIQ, the Certified IdentityIQ Associate at 300 dollars and the Certified IdentityIQ "
                 "Engineer at 400 dollars. Seven exams serve over 12,000 certified professionals, badged on Credly. "
                 "Both tracks rest on identity governance and administration: sources and identity data, access "
                 "modeling, lifecycle management and provisioning, governance and compliance, platform and virtual "
                 "appliances, and rules and transforms. The volume models all of it free in Python.")

    c.node_box(230, 42, 500, 44, "mgmt", [
        Line("SailPoint Identity Security — who has access to what, and should they?", 10.5, 700, "#111827"),
        Line("Identity University · 7 exams · 12,000+ certified · Credly badges", 8.5, 400, "#374151"),
    ])

    # two tracks
    c.node_box(40, 130, 420, 46, "neutral", [
        Line("KNOWLEDGE CREDENTIALS — training-gated, free attempts", 9.5, 700, "#111827"),
        Line("online · adaptive · one sitting · badge NEVER expires", 8.5, 400, "#374151"),
    ])
    c.node_box(500, 130, 420, 46, "data", [
        Line("PROFESSIONAL CERTIFICATIONS — proctored, $300-$400", 9.5, 700, "#111827"),
        Line("2 attempts included · 364 days to schedule · recertify every 2 yrs", 8.5, 400, "#374151"),
    ])
    c.connector(480, 86, 250, 130, "neutral", label="", label_pos=(0, 0))
    c.connector(480, 86, 710, 130, "data", label="", label_pos=(0, 0))

    # credential ladder
    c.node_box(40, 205, 420, 62, "neutral", [
        Line("Identity Security Leader   free path · 3 free tries · <=45min/<=30Q", 8.5, 400, "#374151"),
        Line("Identity Security Professional   2 free tries · <=90min/<=51Q", 8.5, 400, "#374151"),
        Line("Identity Security Expert   2 free tries · <=90min/<=65Q", 8.5, 400, "#374151"),
    ])

    # certs, split by product
    c.node_box(500, 205, 420, 30, "alt", [
        Line("Identity Security Cloud (SaaS)", 9, 700, "#111827"),
    ])
    c.node_box(500, 243, 420, 40, "data", [
        Line("Certified Identity Security Administrator  $400 · 6 mo exp", 8.5, 400, "#374151"),
        Line("Certified Identity Security Engineer  $400 · 1 yr · +Architecture/Rules", 8.5, 400, "#374151"),
    ])
    c.node_box(500, 293, 420, 30, "alt", [
        Line("IdentityIQ (on-premises)", 9, 700, "#111827"),
    ])
    c.node_box(500, 331, 420, 40, "data", [
        Line("Certified IdentityIQ Associate  $300", 8.5, 400, "#374151"),
        Line("Certified IdentityIQ Engineer  $400 · install/build/deploy · LCM", 8.5, 400, "#374151"),
    ])

    # IGA domain band
    c.node_box(40, 293, 420, 78, "mgmt", [
        Line("The IGA disciplines both tracks test:", 9, 700, "#111827"),
        Line("sources & identity data · access modeling", 8.5, 400, "#374151"),
        Line("lifecycle & provisioning · governance & compliance", 8.5, 400, "#374151"),
        Line("platform & virtual appliances · rules & transforms", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="410" font-size="9.5" font-weight="700" fill="#166534">'
          'IGA answers what access is APPROPRIATE and proves it — the governance third alongside Okta (access) and CyberArk (PAM)</text>')
    c.raw('<text x="40" y="429" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: identity correlation · role mining · joiner-mover-leaver · SoD policy · certification campaigns · transforms</text>')

    c.legend(40, 460, [
        ("neutral", "Knowledge Credentials"),
        ("data", "Professional Certs"),
        ("alt", "Product line"),
        ("mgmt", "IGA domains"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
