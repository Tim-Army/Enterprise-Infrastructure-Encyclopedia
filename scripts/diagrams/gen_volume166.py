#!/usr/bin/env python3
"""Volume CLXVI (Boomi) program map.

Chapter 1: the Boomi Training & Certification program (train.boomi.com) — Associate ->
Professional certifications by service/role (Integration Developer, Administrator,
Architect, API Management, Data Hub, Flow, B2B/EDI) over the Boomi Enterprise Platform
(formerly AtomSphere), a low-code iPaaS run by the Atom / Molecule / Atom Cloud runtimes.

Run from scripts/diagrams:  python3 gen_volume166.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-166-boomi-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Boomi Certification Tracks",
        subtitle="train.boomi.com — Associate→Professional by service: Integration · APIM · Data Hub · Flow · B2B/EDI · Admin · Architect",
        svg_title="Chapter 1 program map: the Boomi certification tracks over the low-code Boomi Enterprise Platform",
        svg_desc="Boomi is the iPaaS pioneer — a cloud-native, low-code platform to connect applications, data, "
                 "people, and devices. Certifications are organized by service and role, mostly Associate then "
                 "Professional: Integration Developer (Associate and Professional), Administrator (Associate plus "
                 "Windows and Linux Operational Administrator), Architect (Integration Architect and Runtime "
                 "Architect), API Management (Professional API Design and Professional API Management), Data Hub "
                 "for master data (Associate and Professional Data Hub Developer), Flow for low-code apps "
                 "(Associate Flow Essentials), and B2B/EDI (Associate EDI for X12). Exams are open-book and "
                 "open-platform, have no time limit, mix multiple-choice and multiple-response with a hands-on "
                 "practical section, are course-backed, and cost one hundred twenty-five dollars. The platform "
                 "beneath is the Boomi Enterprise Platform, formerly AtomSphere, run by the signature Atom "
                 "runtime, with Molecule clusters for high availability and Boomi-hosted Atom Clouds. Boomi AI "
                 "adds Companion, Agentstudio, and Boomi GPT. Boomi connects applications, data, people, and "
                 "devices as the enterprise's low-code integration layer.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("BOOMI ENTERPRISE PLATFORM (formerly AtomSphere) — low-code iPaaS: connect apps · data · people · devices", 9.0, 700, "#111827"),
        Line("runtime: ATOM (single) · MOLECULE (clustered HA) · ATOM CLOUD (Boomi-hosted) — design once, deploy anywhere · Boomi AI", 7.4, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("BOOMI TRAINING & CERTIFICATION (train.boomi.com) — Associate → Professional, by service/role", 8.3, 700, "#111827"),
        Line("open-book + OPEN-PLATFORM · no time limit · MCQ/multi + practical section · course-backed · $125   |   Boomi AI: training only (no cert yet)", 6.4, 400, "#374151"),
    ])

    # service tracks
    c.node_box(40, 176, 288, 46, "data", [
        Line("INTEGRATION DEVELOPER (flagship)", 7.6, 700, "#111827"),
        Line("Associate → Professional · shapes/connectors/maps · processes", 5.9, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("API MANAGEMENT (APIM)", 7.8, 700, "#111827"),
        Line("Professional API Design + Management · gateway/policies · Control Plane", 5.6, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("DATA HUB (MDM)", 7.8, 700, "#111827"),
        Line("Associate + Professional Developer · match → golden record → publish", 5.7, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 46, "alt", [
        Line("B2B/EDI + FLOW", 7.8, 700, "#111827"),
        Line("Assoc EDI for X12 (Trading Partner) · Assoc Flow Essentials (low-code apps)", 5.5, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 46, "alt", [
        Line("ADMINISTRATOR", 7.8, 700, "#111827"),
        Line("Associate + Windows/Linux Operational · env/deploy/monitor · runtimes", 5.8, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 46, "alt", [
        Line("ARCHITECT", 7.8, 700, "#111827"),
        Line("Associate Integration Architect + Runtime Architect · patterns · topology", 5.7, 400, "#374151"),
    ])

    c.raw('<text x="40" y="308" font-size="9.5" font-weight="700" fill="#166534">'
          'CONNECT (integration) + EXPOSE (APIs) + MASTER (Data Hub) + EXCHANGE (EDI) + INVOLVE PEOPLE (Flow) + OPERATE (admin/architecture) — one low-code platform, one runtime.</text>')
    c.raw('<text x="40" y="330" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: tracks + levels + open-book/open-platform mechanics · platform services · Atom/Molecule/Atom-Cloud selection + placement · process (Connector→Map→Decision→Try/Catch) ·</text>')
    c.raw('<text x="40" y="347" font-size="9.5" font-weight="400" fill="#374151">'
          'API gateway policies + Control Plane (zombie APIs) · Data Hub match→golden→publish · X12 850 parse + Flow approval · env/deploy/monitor + runtime arch + Boomi AI. Peers: MuleSoft (CLX), Informatica (CLXV), SAP (CXLIV).</text>')

    c.legend(40, 376, [
        ("data", "Build / expose / master"),
        ("alt", "Exchange / operate / architect"),
        ("neutral", "Cert tracks"),
        ("mgmt", "Low-code iPaaS + Atom"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
