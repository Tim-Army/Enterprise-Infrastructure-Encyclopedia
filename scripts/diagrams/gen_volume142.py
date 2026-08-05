#!/usr/bin/env python3
"""Volume CXLII (Cloudflare) certification program + platform map.

Chapter 1: the youngest certification track on the shelf -- two Associate
exams (Application Security, Zero Trust) on Cloudflare's own exam platform,
the Connect 2026 $495 dual-attempt University Pass, unpublished mechanics --
beside the separate partner accreditation track, over the anycast edge
carrying the Application Security family, Cloudflare One, and Workers.

Run from scripts/diagrams:  python3 gen_volume142.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-142-cloudflare-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Cloudflare Certification Tracks",
        subtitle="2 Associate exams · Cloudflare's OWN exam platform · portal still says 'Register Interest' · mechanics NOT published",
        svg_title="Chapter 1 program map: the Cloudflare certification program and the platform beneath it",
        svg_desc="Cloudflare's certification track is the youngest in this encyclopedia: two Associate "
                 "exams. The Application Security Associate assesses foundational knowledge of the "
                 "application security family, with basic hands-on experience highly recommended; the "
                 "Zero Trust Associate covers the Cloudflare One family. Both are delivered on "
                 "Cloudflare's own exam platform at certifications.cloudflare.com, whose public portal "
                 "still shows Register Interest alongside Launch Certification Exam. At Cloudflare "
                 "Connect 2026, October nineteenth through twenty-first at Moscone West in San "
                 "Francisco, a four hundred ninety-five dollar University Pass adds a full day of live "
                 "technical training plus one attempt at both exams, delivered in-person proctored in a "
                 "private quiet environment with live support; laptops are required. Exam duration, "
                 "question count, passing score, validity period, retake policy, and standalone pricing "
                 "are not published, and the detailed domain outlines sit behind the exam platform "
                 "login. A separate partner accreditation track through Cloudflare University covers "
                 "the Accredited Sales Professional, Accredited Sales Engineer, Accredited "
                 "Configuration Engineer, Accredited Services Architect, and an Accredited Workers "
                 "Developer announced as in development; accreditations are course-completion partner "
                 "credentials, not proctored certifications. The platform beneath is a global anycast "
                 "edge network: the same addresses announced from every data center, delivering users "
                 "and distributing attacks alike. On it run the Application Security family of WAF "
                 "managed and custom rules, rate limiting, DDoS protection, Bot Management, and API "
                 "Shield; the Cloudflare One Zero Trust family of Access, Gateway, WARP, and Tunnel; "
                 "and the Workers developer platform with KV, R2, D1, and Durable Objects — all "
                 "manageable by API and Terraform. Cloudflare's free tier covers nearly the entire "
                 "hands-on practice syllabus for both exams.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("CLOUDFLARE — one anycast edge; apps, users, and code all meet the network first", 10.5, 700, "#111827"),
        Line("the same substrate fronts Application Security, Cloudflare One, and Workers", 8, 400, "#374151"),
    ])

    # the two exams
    c.node_box(40, 122, 430, 66, "data", [
        Line("APPLICATION SECURITY ASSOCIATE", 9.5, 700, "#111827"),
        Line("WAF · rate limiting · DDoS · Bot Management · API Shield", 8, 400, "#374151"),
        Line("\"basic, hands-on experience… highly recommended\"", 7.5, 400, "#374151"),
        Line("chapters 02-04 of this volume", 7.5, 700, "#166534"),
    ])
    c.node_box(490, 122, 430, 66, "data", [
        Line("ZERO TRUST ASSOCIATE", 9.5, 700, "#111827"),
        Line("Access (ZTNA) · Gateway (SWG) · WARP · Tunnel", 8, 400, "#374151"),
        Line("named on the Connect 2026 University page", 7.5, 400, "#374151"),
        Line("chapters 05-06 of this volume", 7.5, 700, "#166534"),
    ])

    c.node_box(40, 208, 880, 40, "alt", [
        Line("DELIVERY: Cloudflare's OWN exam platform (certifications.cloudflare.com) — portal shows 'REGISTER INTEREST' · a program in ROLLOUT", 8.5, 700, "#111827"),
        Line("CONNECT 2026 (Oct 19-21, SF): $495 University Pass = training day + ONE ATTEMPT AT BOTH exams · in-person proctored · laptops required", 8, 400, "#374151"),
    ])

    c.node_box(40, 268, 880, 34, "neutral", [
        Line("NOT PUBLISHED: duration · question count · passing score · validity · retake policy · standalone price — domain outlines behind the exam login", 8.5, 700, "#b91c1c"),
    ])

    # accreditation track
    c.node_box(40, 322, 880, 46, "neutral", [
        Line("PARTNER ACCREDITATION TRACK (course completion — NOT certifications)", 8.5, 700, "#111827"),
        Line("Accredited Sales Professional · Sales Engineer (ASE) · Configuration Engineer (ACE) · Services Architect (ASA) · Workers Developer (in development)", 7.5, 400, "#374151"),
        Line("note the collision: Cloudflare ACE ≠ Aviatrix ACE (Vol CXXVI)", 7.5, 400, "#b91c1c"),
    ])

    # platform spine
    c.node_box(40, 388, 880, 56, "mgmt", [
        Line("PLATFORM SPINE — the anycast edge", 8.5, 700, "#111827"),
        Line("DNS (proxy toggle — gray-cloud records EXPOSE the origin) · CDN/cache · WAF + rate limiting + DDoS + bots + API Shield (log→challenge→block)", 7.5, 400, "#374151"),
        Line("Cloudflare One: Access · Gateway · WARP · Tunnel (no inbound ports) · Workers/KV/R2/D1/Durable Objects · API + Terraform + Logpush", 7.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="474" font-size="9.5" font-weight="700" fill="#166534">'
          'The FREE TIER covers nearly the whole practice syllabus — DNS, caching, WAF, rate limiting, Access (50 users), Gateway DNS filtering, Tunnel, Workers.</text>')
    c.raw('<text x="40" y="493" font-size="9.5" font-weight="400" fill="#374151">'
          'Batch F disclosure arc completed: Dynatrace publishes nothing · New Relic publishes everything · Cloudflare publishes that the exams exist. Verify today, not the genre.</text>')
    c.raw('<text x="40" y="512" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: anycast absorption · gray-cloud audit · purge economics · rule shadowing · precision ladders · schema validation · shadow APIs · blast radius · tunnel exposure · drift detection.</text>')

    c.legend(40, 540, [
        ("data", "Exams"),
        ("alt", "Delivery"),
        ("neutral", "Unpublished / partner"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
