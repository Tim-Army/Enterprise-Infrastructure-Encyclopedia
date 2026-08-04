#!/usr/bin/env python3
"""Volume CXXXVII (Rapid7 Certification Tracks) program map.

Chapter 1: the Rapid7 Academy's four certification exams ($215 each,
purchase-order + promo-code enrollment), the five Academy content types
beneath them, the products that have training but no exam, and the CPE
credit tie-in.

Run from scripts/diagrams:  python3 gen_volume137.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-137-rapid7-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: Rapid7 Certification (Insight Platform)",
        subtitle="Four exams at $215 · purchase-order + promo-code enrollment · VILT courses include one attempt · 16-24 CPE credits",
        svg_title="Chapter 1 program map: the Rapid7 certification program",
        svg_desc="Rapid7 certification runs through the Rapid7 Academy and comprises four exams, each costing "
                 "215 US dollars. The InsightVM exam, for Rapid7 Vulnerability Management, awards Certified "
                 "Administrator and covers environment architecture, deployment and scaling, scanning scope "
                 "optimization, endpoint vulnerability detection and remediation using Insight Agents, compliance "
                 "reporting, remediation prioritization, and workflow automation. The InsightIDR exam, for Rapid7 "
                 "SIEM, awards Certified Specialist and covers log data collection, the log query language, "
                 "deception technology, endpoint detection, alert framework optimization, threat intelligence "
                 "correlation, and incident response automation. The InsightAppSec exam, for Rapid7 Application "
                 "Security, awards Certified Specialist for dynamic application security testing. The "
                 "InsightConnect exam, for Rapid7 Automation, awards Certified Specialist for security "
                 "orchestration and playbooks. Exams are purchased by purchase order and enrolled using a promo "
                 "code supplied in the registration email, rather than by card checkout; virtual instructor-led "
                 "courses include one exam attempt. The Academy offers five content types: on-demand training, "
                 "product and technology demonstrations, virtual instructor-led courses with lab environments, "
                 "certification exams, and product workshops of an hour or less. Courses carry 16 to 24 CPE "
                 "credits toward ISC2 and ISACA renewals. InsightCloudSec and Metasploit have training courses but "
                 "no certification exam. Exam duration, question count, passing score, and validity are not "
                 "published, so candidates confirm them at enrollment. The volume models these defensive "
                 "disciplines free in Python.")

    c.node_box(230, 42, 500, 44, "mgmt", [
        Line("Rapid7 Insight platform — security operations", 10.5, 700, "#111827"),
        Line("vulnerability management · SIEM/detection · app security · automation", 8.5, 400, "#374151"),
    ])

    # four exams
    c.node_box(40, 128, 210, 66, "data", [
        Line("InsightVM", 9.5, 700, "#111827"),
        Line("Certified ADMINISTRATOR", 8, 700, "#374151"),
        Line("vulnerability management", 7.5, 400, "#374151"),
        Line("$215", 8, 400, "#374151"),
    ])
    c.node_box(268, 128, 210, 66, "data", [
        Line("InsightIDR", 9.5, 700, "#111827"),
        Line("Certified SPECIALIST", 8, 700, "#374151"),
        Line("SIEM · deception · UBA", 7.5, 400, "#374151"),
        Line("$215", 8, 400, "#374151"),
    ])
    c.node_box(496, 128, 210, 66, "data", [
        Line("InsightAppSec", 9.5, 700, "#111827"),
        Line("Certified SPECIALIST", 8, 700, "#374151"),
        Line("DAST — running apps", 7.5, 400, "#374151"),
        Line("$215", 8, 400, "#374151"),
    ])
    c.node_box(724, 128, 196, 66, "data", [
        Line("InsightConnect", 9.5, 700, "#111827"),
        Line("Certified SPECIALIST", 8, 700, "#374151"),
        Line("SOAR · playbooks", 7.5, 400, "#374151"),
        Line("$215", 8, 400, "#374151"),
    ])

    # enrollment
    c.node_box(40, 214, 880, 40, "alt", [
        Line("ENROLLMENT: purchased by PURCHASE ORDER, then a PROMO CODE from the registration email — not a card checkout", 8.5, 700, "#111827"),
        Line("Virtual instructor-led courses INCLUDE one exam attempt — often the simplest route", 8.5, 400, "#374151"),
    ])

    # academy content types
    c.node_box(40, 274, 880, 40, "neutral", [
        Line("Rapid7 Academy: On-Demand Training · Product Demos · Virtual Instructor-Led (lab env) · Certification Exams · Product Workshops (<=1 hr)", 8.5, 400, "#374151"),
        Line("Courses carry 16-24 CPE credits toward ISC2 / ISACA renewals · public Training Calendar", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="348" font-size="9.5" font-weight="700" fill="#991b1b">'
          'InsightCloudSec and Metasploit have TRAINING but NO certification exam — products are not certifications.</text>')
    c.raw('<text x="40" y="367" font-size="9.5" font-weight="400" fill="#374151">'
          'Duration, question count, passing score and validity are NOT published — confirm at enrollment (same discipline as SolarWinds, Vol CXXXIV).</text>')
    c.raw('<text x="40" y="392" font-size="9.5" font-weight="700" fill="#166534">'
          'DEFENSIVE volume. Modeled free in Python: scan coverage &amp; blind spots · credentialed-scan uplift · risk vs raw CVSS · SLA aging · log attribution · deception · precision/recall · playbook gating.</text>')

    c.legend(40, 424, [
        ("data", "The four exams"),
        ("alt", "Enrollment path"),
        ("neutral", "Academy content"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
