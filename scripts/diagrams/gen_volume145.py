#!/usr/bin/env python3
"""Volume CXLV (Atlassian) credential program map.

Chapter 1: the three-tier credential structure (ACH free / ACA / ACP) plus
designations, over a cloud-first platform (Jira, Confluence, JSM, org admin)
after Server's Feb 2024 end of life. Per-exam mechanics are portal-gated.

Run from scripts/diagrams:  python3 gen_volume145.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-145-atlassian-certifications"


def ch01():
    c = Canvas(960, 580,
        title="Chapter 1 Program Map: Atlassian Certification Tracks",
        subtitle="three tiers + designations · ACH is FREE · cloud-first (Server EOL Feb 2024) · per-exam mechanics portal-gated",
        svg_title="Chapter 1 program map: the Atlassian credential program and the platform beneath it",
        svg_desc="Atlassian restructured its credentials into three tiers plus designations. At the base, "
                 "Atlassian Certificate Holder, ACH, credentials are free and foundational, built for app "
                 "users to demonstrate basic knowledge; the Atlassian Cloud Fundamentals certificate is an "
                 "example. In the middle, Atlassian Certified Associate, ACA, certifications are for "
                 "professionals who use the apps in their jobs, such as Managing Jira Projects for Cloud. At "
                 "the top, Atlassian Certified Professional, ACP, certifications are role-based credentials "
                 "for solution administrators, including Jira Administration for Cloud, Confluence "
                 "Administration, and Atlassian Cloud Organization Admin. Designations stack multiple "
                 "credentials in a related path into a meta-credential. The tiers form a responsibility "
                 "ladder, not a difficulty ladder: ACH asks whether you can use the app, ACA whether you "
                 "can work effectively in it, and ACP whether you can administer it for others. The program "
                 "is cloud-first: Atlassian Server reached end of support in February 2024, leaving Cloud "
                 "and Data Center as the deployments, and the catalog now leads with the for-Cloud variants "
                 "while Data Center certifications persist for on-premise holdouts. The Data-Center-to-Cloud "
                 "migration is a prominent skill area. Preparation is largely free: on-demand training, "
                 "exam-prep courses with business-case study guides and hands-on labs, and a free Cloud "
                 "tier for up to ten users. Per-exam mechanics such as question count, duration, passing "
                 "score, price, and validity sit behind the credential portal's full exam details panel. "
                 "The platform beneath is Jira for work tracking, Confluence for knowledge, Jira Service "
                 "Management for IT service management, and the Atlassian cloud organization admin hub with "
                 "Atlassian Guard for security.")

    c.node_box(180, 42, 600, 44, "mgmt", [
        Line("ATLASSIAN — the PLAN & COORDINATE layer of the toolchain", 10.5, 700, "#111827"),
        Line("Jira / Confluence / JSM sit ABOVE the code (GitLab CXXXVI, GitHub LXXXIX own the build)", 8, 400, "#374151"),
    ])

    # three tiers
    c.node_box(40, 124, 280, 66, "alt", [
        Line("ACH — Certificate Holder", 9.5, 700, "#111827"),
        Line("app USERS · foundational", 8, 400, "#374151"),
        Line("FREE, quick to earn", 8, 700, "#166534"),
        Line("e.g. Atlassian Cloud Fundamentals", 7, 400, "#374151"),
    ])
    c.node_box(340, 124, 260, 66, "data", [
        Line("ACA — Certified Associate", 9.5, 700, "#111827"),
        Line("professionals who USE the apps", 8, 400, "#374151"),
        Line("paid · industry-recognized", 7.5, 400, "#374151"),
        Line("e.g. Managing Jira Projects", 7, 400, "#374151"),
    ])
    c.node_box(620, 124, 300, 66, "data", [
        Line("ACP — Certified Professional", 9.5, 700, "#111827"),
        Line("solution ADMINISTRATORS · role-based", 8, 400, "#374151"),
        Line("Jira Admin · Confluence Admin ·", 7, 400, "#374151"),
        Line("Cloud Org Admin (Cloud AND Data Center)", 7, 400, "#374151"),
    ])
    c.connector(320, 157, 340, 157, "data", label="", label_pos=(0, 0))
    c.connector(600, 157, 620, 157, "data", label="", label_pos=(0, 0))

    c.node_box(40, 208, 880, 30, "neutral", [
        Line("responsibility ladder (NOT difficulty): ACH = can you USE it? · ACA = WORK in it well? · ACP = ADMINISTER it for others?  +  DESIGNATIONS stack multiple certs", 8, 700, "#111827"),
    ])

    # cloud-first
    c.node_box(40, 258, 880, 40, "alt", [
        Line("★ CLOUD-FIRST: Atlassian SERVER reached END OF SUPPORT Feb 2024 → only Cloud + Data Center remain", 8.5, 700, "#111827"),
        Line("catalog LEADS with 'for Cloud' variants · Data Center certs persist for on-prem · Data-Center-to-Cloud MIGRATION is its own skill area (ch08)", 8, 400, "#374151"),
    ])

    # platform
    c.node_box(40, 318, 880, 50, "mgmt", [
        Line("PLATFORM", 8.5, 700, "#111827"),
        Line("JIRA (company-managed vs team-managed · schemes · workflows · JQL · automation) · CONFLUENCE (spaces · page tree · narrow-never-widen perms)", 7.5, 400, "#374151"),
        Line("JIRA SERVICE MANAGEMENT (request types · queues · SLAs · agents vs customers) · ORG ADMIN hub + ATLASSIAN GUARD (SSO · SCIM · domain verification)", 7.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="392" font-size="9.5" font-weight="700" fill="#166534">'
          'Preparation is largely FREE: on-demand training + exam-prep courses (business-case study guides, hands-on labs) + a FREE Cloud tier (10 users) to practice on.</text>')
    c.raw('<text x="40" y="411" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Per-exam mechanics (question count · duration · passing score · price · validity) are behind the credential portal\'s "Open full exam details" — the volume asserts none.</text>')
    c.raw('<text x="40" y="430" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: tier/audience reading · deployment choice · project-type decision · scheme blast radius + sprawl · workflow over-engineering · JQL narrow-first ·</text>')
    c.raw('<text x="40" y="447" font-size="9.5" font-weight="400" fill="#374151">'
          'automation loops · Confluence perms (narrow≠widen) · knowledge rot · domain verification · SCIM offboarding · JSM SLA pause · agent sizing · app governance · wave migration.</text>')

    c.legend(40, 480, [
        ("alt", "Free / cloud-first"),
        ("data", "Paid certifications"),
        ("neutral", "Structure"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-credential-program.svg")


if __name__ == "__main__":
    ch01()
