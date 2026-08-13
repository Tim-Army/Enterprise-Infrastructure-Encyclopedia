# Chapter 02: The Boomi Enterprise Platform

## Learning Objectives

- Describe the Boomi Enterprise Platform as a unified, low-code iPaaS.
- Name the platform services and what each does.
- Explain the low-code, visual, cloud-native approach.
- Understand "connect anything" — apps, data, people, and devices.

*Cert relevance: every track certification sits on this platform; this chapter is the shared context they build on.*

## One low-code platform

The **Boomi Enterprise Platform** (formerly **AtomSphere**) is a **unified, low-code, cloud-native iPaaS** — one platform to **connect everything** an enterprise runs. The key ideas are **unified** (many integration and data services in one place), **low-code** (you build **visually**, dragging and configuring rather than hand-coding), and **cloud-native** (you design in a browser; the platform manages the heavy lifting). A business that has data trapped in a dozen SaaS apps, an ERP, several databases, and EDI trading partners uses Boomi to **connect them all** — quickly, visibly, and maintainably.

Boomi's promise is **speed with governance**: integrations that would take months of custom code are built in days on a visual canvas, while the platform provides monitoring, versioning, and reuse. Every certification track ([Ch 1](01-the-boomi-program.md)) is a specialization within this one platform. The lab models the unified platform.

## The platform services

The Boomi Enterprise Platform bundles several **services**, each addressing a connection problem:

- **Integration** — the core: build **processes** that move and transform data between systems ([Ch 4](04-building-integrations.md)).
- **API Management (APIM)** — design, publish, secure, and govern **APIs** ([Ch 5](05-api-management.md)).
- **B2B/EDI** — exchange documents with **trading partners** (X12, EDIFACT) ([Ch 7](07-b2b-edi-and-flow.md)).
- **Flow** — build **low-code workflow applications** and user-facing apps ([Ch 7](07-b2b-edi-and-flow.md)).
- **Data Hub** — **master data management** for golden records ([Ch 6](06-data-hub-mdm.md)).
- **Event Streams** — event-driven, publish/subscribe messaging.
- **Boomi AI** — AI-assisted building: **Boomi Companion**, **Agentstudio** (build AI agents), and **Boomi GPT** ([Ch 8](08-administration-and-architecture.md)).
- **Task Automation, Boomi Data Integration, Boomi for SAP, DCP (Data Catalog & Prep)** — task/RPA-style automation, bulk data pipelines, SAP-specific connectivity, and cataloging/preparation.

The advantage of one platform is that these **share connectivity, runtime, and governance** — an integration process can call an API, feed Data Hub, and trigger a Flow app, all on the same foundation. The lab maps the services.

## Low-code and visual

Boomi development is **model-driven and visual**:

- You build a **process** on a **canvas** by placing and connecting **shapes** — a Connector shape to read from a system, a Map shape to transform, a Decision shape to branch, another Connector to write ([Ch 4](04-building-integrations.md)).
- **Connectors** provide pre-built connectivity to hundreds of applications and technologies (Salesforce, NetSuite, SAP, databases, REST/SOAP, files) so you **configure** a connection instead of coding a client.
- **The Boomi Suggest / AI** features recommend mappings and next steps, drawing on the platform's crowd-sourced metadata.

Low-code does not mean low-power: complex logic, scripting, and error handling are all available — but the **default path is visual and fast**. This is why integrations ship quickly and why the certifications emphasize **doing** on the canvas. The lab models building visually.

## Connect anything

Boomi's tagline is connecting **applications, data, people, and devices**:

- **Applications** — SaaS and on-premises apps, wired together so data flows between them.
- **Data** — databases, warehouses, files, and lakes, integrated and mastered.
- **People** — via **Flow** low-code apps and workflows that put humans in the loop.
- **Devices** — edge and IoT endpoints via lightweight runtimes.

The unifying element is the **runtime** — the **Atom** and its variants ([Ch 3](03-atoms-molecules-atom-clouds.md)) — which executes your integrations wherever the data lives. **Design once in the cloud; run anywhere.** That combination of a broad, low-code platform and a deployable runtime is Boomi's signature, and the foundation for every track. The lab synthesizes the platform.

## Hands-On Lab

Python models the Boomi Enterprise Platform — its services and the connect-anything reach. **Cost:** none.

### Lab 2.1 — Model the unified platform

**Objective:** See the platform services as one foundation with shared connectivity and runtime.

```bash
python3 - <<'EOF'
SERVICES = {
  "Integration":     "build processes to move + transform data between systems",
  "API Management":  "design, publish, secure, and govern APIs",
  "B2B/EDI":         "exchange documents with trading partners (X12, EDIFACT)",
  "Flow":            "low-code workflow apps with humans in the loop",
  "Data Hub":        "master data management — golden records",
  "Event Streams":   "event-driven publish/subscribe messaging",
  "Boomi AI":        "AI-assisted build: Companion, Agentstudio, Boomi GPT",
}
CONNECT = ["applications (SaaS + on-prem)", "data (DBs, warehouses, files)",
           "people (Flow apps/workflows)", "devices (edge/IoT)"]

print("BOOMI ENTERPRISE PLATFORM — one low-code iPaaS, many services:\n")
for svc, desc in SERVICES.items():
    print(f"   {svc:16} {desc}")
print("\n   CONNECT ANYTHING:")
for c in CONNECT:
    print(f"      - {c}")
print()
# demonstrate the shared foundation: one flow crossing three services
scenario = ["Integration process reads an order from SAP",
            "-> publishes it via API Management as a REST endpoint",
            "-> feeds the customer into Data Hub (golden record)",
            "-> triggers a Flow app for human approval"]
print("   SHARED FOUNDATION (one scenario crossing services):")
for step in scenario:
    print(f"      {step}")
print()
print("The services SHARE connectivity, runtime, and governance — an integration can call")
print("an API, feed Data Hub, and trigger a Flow app on the SAME platform. That unification,")
print("plus low-code visual building and a deployable runtime, is Boomi's signature.")
EOF
```

**Expected result:** A model of the Boomi Enterprise Platform listing its services (Integration, API Management, B2B/EDI, Flow, Data Hub, Event Streams, Boomi AI) and the four things it connects (apps, data, people, devices), plus a scenario crossing three services on one foundation. The lesson is that Boomi is one unified low-code iPaaS whose services share connectivity, runtime, and governance, enabling a single flow to span integration, API management, master data, and low-code apps.

**Negative test:** Buying a separate point tool for integration, another for API management, another for MDM, and another for EDI. They do not share connectivity, runtime, or governance, so every cross-service flow is a fresh integration; Boomi's unified platform lets one flow span services on a shared foundation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The platform placed — a unified, low-code, cloud-native iPaaS (formerly AtomSphere).
- [ ] The services named — Integration, APIM, B2B/EDI, Flow, Data Hub, Event Streams, Boomi AI, and more.
- [ ] Low-code and visual understood — building processes from shapes and connectors on a canvas.
- [ ] Connect anything understood — applications, data, people, and devices, run by the Atom runtime.

## See also

- [Chapter 03 — Atoms, Molecules, and Atom Clouds](03-atoms-molecules-atom-clouds.md) — the runtime that executes it all.
- [Chapter 04 — Building Integrations](04-building-integrations.md) — the core service and the flagship track.
- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) — the closest platform peer for comparison.
