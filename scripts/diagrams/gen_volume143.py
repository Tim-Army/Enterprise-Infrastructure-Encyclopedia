#!/usr/bin/env python3
"""Volume CXLIII (Akamai) credential landscape + platform map.

Chapter 1: the four credential groups -- University course badges
(course-is-the-credential), the certification tier (Guardicore ladder + API
Security Architect + Cloud Foundations), the partner track, and the Technical
Academy -- inside a 192-badge Credly catalog, over the platform: intelligent
edge (delivery/performance), security portfolio, zero trust + Guardicore
segmentation, and Akamai Cloud.

Run from scripts/diagrams:  python3 gen_volume143.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-143-akamai-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Akamai Certification Tracks",
        subtitle="192-badge Credly catalog · course-is-the-credential + a real Guardicore exam ladder · exam mechanics NOT published",
        svg_title="Chapter 1 program map: the Akamai credential landscape and the platform beneath it",
        svg_desc="Akamai's credentials divide into four groups inside a 192-badge Credly issuer catalog. "
                 "First, Akamai University Customer Enablement course badges, following the "
                 "course-is-the-credential model: completing an instructor-led or virtual instructor-led "
                 "course earns a Credly badge. These cover Web Performance Foundations and Offload, Media "
                 "Delivery, Web Application and API Protection, Bot and Abuse Protection, Client-Side "
                 "Protection and Compliance, Zero Trust Solutions, Automation and DevOps, and Fraud "
                 "Management. Second, the certification tier with real exams: the Guardicore ladder, "
                 "comprising the Certified Segmentation Administrator and its Advanced variant, the "
                 "Certified Segmentation Engineer and its On-Premise variant, and the partner Certified "
                 "Services Provider for Implementation and Support; the API Security Architect credential "
                 "at Advanced level; and the Cloud Computing Foundations Certification at Foundational "
                 "level. Third, a partner track with Certified Partner Solutions Architect badges for "
                 "twelve products and Partner Foundations and Advanced badges across four solution areas. "
                 "Fourth, the Akamai Technical Academy, offering two Coursera professional certificates in "
                 "Network Engineering and Customer Consulting and Support for career entry. Badge metadata "
                 "publishes level, a Paid or Free flag, and a time-to-earn band, but no exam durations, "
                 "question counts, or passing scores are public for any credential. The platform beneath "
                 "has four families: the intelligent edge for delivery and performance, including DNS "
                 "mapping, Edge DNS, Global Traffic Management, Ion, mPulse, and media delivery; the "
                 "security portfolio of App and API Protector, Bot Manager, Account Protector, Content "
                 "Protector, and API Security; the zero trust products Enterprise Application Access, "
                 "Secure Internet Access, and MFA alongside Guardicore east-west segmentation; and Akamai "
                 "Cloud compute from the Linode lineage. Guardicore uniquely has a matching hands-on "
                 "build-it-yourself lab already in this encyclopedia, Volume 95.")

    c.node_box(170, 42, 620, 44, "mgmt", [
        Line("AKAMAI — the enterprise edge incumbent: per-product depth, course-based enablement", 10.5, 700, "#111827"),
        Line("the contrast with Cloudflare (Vol CXLII): breadth + relationship vs one self-serve model", 8, 400, "#374151"),
    ])

    # four credential groups
    c.node_box(40, 122, 220, 74, "data", [
        Line("COURSE BADGES", 9.5, 700, "#111827"),
        Line("Akamai University (ILT/VILT)", 7.5, 400, "#374151"),
        Line("Web Perf · Media · WAAP · Bot", 7, 400, "#374151"),
        Line("& Abuse · DevOps · Zero Trust", 7, 400, "#374151"),
        Line("course-IS-the-credential", 7, 700, "#166534"),
    ])
    c.node_box(270, 122, 240, 74, "alt", [
        Line("CERTIFICATION TIER (exams)", 9, 700, "#111827"),
        Line("GUARDICORE ladder: GCSA/GCSA-Adv", 7, 400, "#374151"),
        Line("GCSE (+On-Prem) · GCSP partner", 7, 400, "#374151"),
        Line("API Security - Architect (Adv)", 7, 400, "#374151"),
        Line("Cloud Computing Foundations", 7, 400, "#374151"),
    ])
    c.node_box(520, 122, 200, 74, "neutral", [
        Line("PARTNER TRACK", 9.5, 700, "#111827"),
        Line("Certified Partner:", 7.5, 400, "#374151"),
        Line("Solutions Architect x12", 7.5, 400, "#374151"),
        Line("Foundations/Advanced x4", 7.5, 400, "#374151"),
        Line("(partner org only)", 7, 400, "#374151"),
    ])
    c.node_box(730, 122, 190, 74, "neutral", [
        Line("CAREER ENTRY", 9.5, 700, "#111827"),
        Line("Technical Academy", 7.5, 400, "#374151"),
        Line("(Coursera):", 7.5, 400, "#374151"),
        Line("Network Engineering ·", 7, 400, "#374151"),
        Line("Customer Consulting", 7, 400, "#374151"),
    ])

    c.node_box(40, 214, 880, 30, "neutral", [
        Line("192 badges in the Credly issuer catalog — ~21 practitioner-pursuable; the rest are partner, career-entry, or INTERNAL AWARDS (Titans Club, MVP...)", 8, 700, "#b91c1c"),
    ])

    c.node_box(40, 264, 880, 34, "alt", [
        Line("NOT PUBLISHED: exam duration · question count · passing score — badge metadata gives level + Paid/Free + time-band only. This volume asserts nothing more.", 8.5, 700, "#111827"),
    ])

    # platform spine
    c.node_box(40, 318, 880, 70, "mgmt", [
        Line("PLATFORM (four families on the intelligent edge)", 8.5, 700, "#111827"),
        Line("DELIVERY/PERF: DNS mapping (not anycast) · Edge DNS · GTM · Ion · mPulse · Image&Video · Media (rebuffer, not LCP)  [ch02-03]", 7.5, 400, "#374151"),
        Line("SECURITY: App & API Protector (KSD lineage) · Bot Manager/Account/Content Protector · API Security (discover→posture→runtime)  [ch04-06]", 7.5, 400, "#374151"),
        Line("ZERO TRUST: EAA (north-south) · SIA · MFA  +  GUARDICORE east-west segmentation [ch07]  ·  AKAMAI CLOUD compute (Linode) [ch08]", 7.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="404" font-size="9.5" font-weight="700" fill="#166534">'
          'GUARDICORE is Akamai\'s ONE real exam ladder — and uniquely has a matching hands-on build already in this encyclopedia: Volume XCV (5-VM lab).</text>')
    c.raw('<text x="40" y="423" font-size="9.5" font-weight="400" fill="#374151">'
          'Akamai sells BOTH halves of zero trust: EAA/SIA (north-south, user→app) and Guardicore (east-west, workload↔workload) — the estate-consolidation pitch.</text>')
    c.raw('<text x="40" y="442" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: catalog sort · DNS-mapping answers · GTM failover math · byte-weighted offload · RUM steering · adaptive-WAF review · which-WAF diagnosis ·</text>')
    c.raw('<text x="40" y="459" font-size="9.5" font-weight="400" fill="#374151">'
          'bot-by-intent · account anomaly · PCI-v4 script drift · API discover/posture/runtime · flow-map-before-segment · label-vs-address policy · ransomware containment · config drift.</text>')

    c.legend(40, 492, [
        ("data", "Course badges"),
        ("alt", "Certifications"),
        ("neutral", "Partner / entry"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-credential-landscape.svg")


if __name__ == "__main__":
    ch01()
