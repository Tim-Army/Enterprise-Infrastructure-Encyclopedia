#!/usr/bin/env python3
"""Volume CLX (MuleSoft) program map.

Chapter 1: the Salesforce-branded MuleSoft certifications (Associate/Developer/
Architect; 7 certs; Platform Architect 60Q/90min/70%/$400) over the Anypoint
Platform and API-led connectivity (System/Process/Experience -> application network).

Run from scripts/diagrams:  python3 gen_volume160.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-160-mulesoft-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: MuleSoft Certification Tracks",
        subtitle="Salesforce-branded MuleSoft certs (Associate/Developer/Architect) · Anypoint Platform · API-led connectivity",
        svg_title="Chapter 1 program map: the MuleSoft certifications over the Anypoint Platform",
        svg_desc="MuleSoft is the API and integration platform owned by Salesforce, and its certifications are "
                 "branded Salesforce Certified MuleSoft credentials across three families. The Associate family "
                 "has MuleSoft Integration Foundations. The Developer family has MuleSoft Developer, MuleSoft "
                 "Developer II for production-ready apps in DevOps, and MuleSoft Hyperautomation Developer. The "
                 "Architect family has MuleSoft Catalyst Consultant, MuleSoft Platform Architect, delivered as "
                 "sixty questions in ninety minutes at seventy percent to pass for four hundred dollars, and "
                 "MuleSoft Platform Integration Architect. The platform beneath is the Anypoint Platform, built "
                 "around API-led connectivity, a three-layer architecture of System APIs that unlock data, "
                 "Process APIs that orchestrate business logic, and Experience APIs that tailor data per "
                 "channel, forming a reusable application network. Developers design APIs with RAML and OpenAPI "
                 "specs in Design Center, publish and reuse them in Anypoint Exchange, build Mule applications "
                 "as flows of connectors and DataWeave transformations in Anypoint Studio, deploy to CloudHub "
                 "or Runtime Fabric, and govern with API Manager policies and Anypoint Monitoring. MuleSoft is "
                 "the integration layer of the Salesforce ecosystem.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("MULESOFT — API-led integration (Anypoint Platform) · owned by SALESFORCE (LXXXIII)", 10, 700, "#111827"),
        Line("compose REUSABLE APIs into an APPLICATION NETWORK — not brittle point-to-point spaghetti", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("SALESFORCE CERTIFIED MULESOFT — 3 families, 7 certifications", 8.3, 700, "#111827"),
        Line("ASSOCIATE: Integration Foundations  |  DEVELOPER: Developer · Developer II (DevOps) · Hyperautomation Developer  |  ARCHITECT: Catalyst Consultant · Platform Architect (60Q/90min/70%/$400) · Platform Integration Architect", 6.6, 400, "#374151"),
    ])

    # API-led 3-layer
    c.node_box(40, 176, 288, 46, "data", [
        Line("EXPERIENCE APIs", 8.3, 700, "#111827"),
        Line("tailor data per channel (mobile/web/partner)", 6.9, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("PROCESS APIs", 8.3, 700, "#111827"),
        Line("orchestrate/compose business logic", 6.9, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("SYSTEM APIs", 8.3, 700, "#111827"),
        Line("unlock data from systems of record (build ONCE)", 6.7, 400, "#374151"),
    ])
    c.raw('<text x="480" y="238" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">★ API-LED CONNECTIVITY — higher layers REUSE lower ones → a reusable APPLICATION NETWORK (integration compounds as an asset, not a cost)</text>')

    # lifecycle
    c.node_box(40, 250, 880, 40, "alt", [
        Line("ANYPOINT PLATFORM lifecycle: DESIGN (Design Center — RAML/OAS specs) → REUSE (Anypoint Exchange) → BUILD (Anypoint Studio — Mule apps = flows of connectors + DataWeave) →", 7.0, 700, "#111827"),
        Line("DEPLOY (CloudHub iPaaS / Runtime Fabric hybrid+K8s) → MANAGE (API Manager policies: rate-limit/OAuth; Anypoint Monitoring). ★ DATAWEAVE = the transformation language (heavily tested).", 7.0, 400, "#374151"),
    ])

    c.raw('<text x="40" y="316" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: 3-family program + architect domains · point-to-point vs 3-layer API-led · unified-platform lifecycle + Mule flow · design-first specs + Exchange reuse · flow with connectors + error handling ·</text>')
    c.raw('<text x="40" y="333" font-size="9.5" font-weight="400" fill="#374151">'
          'DataWeave map/filter/reformat across formats · deploy targets + API-Manager policies + monitoring · hyperautomation spectrum (API/RPA/IDP/Composer) + Catalyst C4E. Salesforce (LXXXIII) owner, Confluent (CXXXV) streaming, UiPath (CXLIX) RPA.</text>')

    c.legend(40, 360, [
        ("data", "API-led 3-layer"),
        ("alt", "Anypoint lifecycle"),
        ("neutral", "Cert families"),
        ("mgmt", "Integration platform"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
