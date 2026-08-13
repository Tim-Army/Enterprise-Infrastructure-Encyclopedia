# Chapter 09: Choosing Your Boomi Path

## Learning Objectives

- Map roles (integration developer, API developer, MDM/Data Hub developer, EDI specialist, admin, architect) to certifications.
- Sequence certifications — start with Integration Developer, then specialize.
- Understand the Associate → Professional progression across tracks.
- Place Boomi in the integration and iPaaS ecosystem.

*Cert relevance: this chapter turns the track map ([Ch 1](01-the-boomi-program.md)) into a personal plan and ends with a capstone.*

## Match the certification to your role

Boomi certifications are **service- and role-based**, so start from **what you do**:

| Your role | Start here | Then consider |
| --- | --- | --- |
| **Integration developer** | Associate Integration Developer ([Ch 4](04-building-integrations.md)) | Professional Integration Developer |
| **API developer** | Professional API Design ([Ch 5](05-api-management.md)) | Professional API Management |
| **MDM / Data Hub developer** | Associate Data Hub ([Ch 6](06-data-hub-mdm.md)) | Professional Data Hub Developer |
| **EDI / B2B specialist** | Associate EDI for X12 ([Ch 7](07-b2b-edi-and-flow.md)) | Professional Integration Developer |
| **Low-code app builder** | Associate Flow Essentials ([Ch 7](07-b2b-edi-and-flow.md)) | Associate Integration Developer |
| **Administrator** | Associate Administrator ([Ch 8](08-administration-and-architecture.md)) | Windows / Linux Operational Administrator |
| **Architect** | Associate Integration Architect ([Ch 8](08-administration-and-architecture.md)) | Associate Runtime Architect |

The pattern: certify on the **service you work with**, at the **level** that matches your role, then broaden. The lab builds a role-to-path planner.

## Sequence sensibly

A workable sequence for most people:

1. **Start with Integration Developer.** It is the flagship track and the foundation the others build on — even API management, Data Hub, and EDI assume you understand processes, connectors, and maps. Take *Integration Essentials* → Associate Integration Developer.
2. **Climb to Professional** in your central track — Professional Integration Developer, or the Professional credential in API Management or Data Hub.
3. **Broaden across services.** Because it is one platform ([Ch 2](02-the-boomi-platform.md)), a second service makes you far more effective (a developer who adds API Management publishes reusable APIs; add Data Hub and you master the data too).
4. **Add operations or architecture.** Administrators add the Operational Administrator credentials; senior builders add the **Integration Architect** and **Runtime Architect** credentials to design at scale.

Every exam is **open-book, open-platform, course-backed** ([Ch 1](01-the-boomi-program.md)), so pair each with its course and practice on the platform. The lab sequences a plan.

## Associate and Professional across tracks

Remember the two-level shape:

- **Associate** credentials (Integration Developer, Data Hub, Flow, EDI, Administrator, the two Architect credentials) validate **foundational** competency — the right first target in any track.
- **Professional** credentials (Integration Developer, API Design, API Management, Data Hub Developer, Windows/Linux Operational Administrator) validate **advanced** competency — the deeper target once you work in a track seriously.

Many careers collect **several Associate** credentials across services (breadth) plus **one or two Professional** credentials in the track they specialize in (depth). The lab reflects breadth vs depth.

## Boomi in the ecosystem

Boomi is the **connective tissue** of the enterprise. It sits alongside:

- **Integration peers** — [MuleSoft (CLX)](../../volume-160-mulesoft-certifications/README.md) and [Informatica's Cloud Application Integration (CLXV)](../../volume-165-informatica-certifications/README.md): overlapping iPaaS/integration space; Boomi's edge is a broad low-code platform with the deployable Atom runtime.
- **Data management** — [Informatica (CLXV)](../../volume-165-informatica-certifications/README.md): Data Hub overlaps Informatica MDM; many enterprises run both, using Boomi for application/EDI integration and a data platform for heavy ETL/governance.
- **Applications it connects** — [SAP (CXLIV)](../../volume-144-sap-certifications/README.md) (Boomi for SAP), plus the CRMs, ERPs, and SaaS apps across this shelf. Boomi was **Dell Boomi** ([Dell, XXXII](../../volume-032-dell-technologies-certifications/README.md)) before becoming independent.

Learning Boomi is learning **how the enterprise is wired together** — the low-code layer that connects applications, data, people, and devices. The capstone builds that end-to-end. The lab closes with a full scenario.

## Hands-On Lab

Python builds a role-to-path planner, then a capstone spanning the platform. **Cost:** none.

### Lab 9.1 — Plan your Boomi path

**Objective:** Turn a role into a sequenced certification plan.

```bash
python3 - <<'EOF'
ROLE_PATHS = {
  "Integration developer": ["Associate Integration Developer", "Professional Integration Developer"],
  "API developer":         ["Professional API Design", "Professional API Management"],
  "Data Hub developer":    ["Associate Data Hub", "Professional Data Hub Developer"],
  "Administrator":         ["Associate Administrator", "Linux Operational Administrator"],
  "Architect":             ["Associate Integration Architect", "Associate Runtime Architect"],
}
def plan(role):
    steps = ROLE_PATHS[role]
    print(f"   ROLE: {role}")
    print(f"      1. START: {steps[0]}")
    for i, s in enumerate(steps[1:], 2):
        print(f"      {i}. THEN:  {s}")
    print("      note: every exam is open-book, open-platform, course-backed, $125")
print("BOOMI ROLE -> CERTIFICATION PATH:\n")
for role in ["Integration developer", "API developer", "Architect"]:
    plan(role); print()
print("Start with Integration Developer (the flagship foundation), climb to Professional in")
print("your track, broaden across services (breadth), and add architecture/ops to design at scale.")
EOF
```

**Expected result:** A planner turning roles into sequenced paths — a developer starts with Associate then Professional Integration Developer; an API developer takes Professional API Design then API Management; an architect takes Integration Architect then Runtime Architect. The lesson is to start with Integration Developer, climb to Professional in your track, and broaden across services and into architecture.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Capstone: an order across the platform

**Objective:** Trace an order through EDI, integration, Data Hub, API, and a Flow approval.

```bash
python3 - <<'EOF'
# CAPSTONE: a partner order flows across Boomi's services on one platform
log = []
# 1) B2B/EDI: receive an X12 850 from a trading partner
order = {"po": "PO-9987", "customer": "Acme Corp", "email": "buyer@acme.com", "amount": 1350.0}
log.append(f"B2B/EDI: received X12 850 {order['po']} from trading partner")
# 2) Integration: map + validate the order
order["region"] = "Americas"; log.append("Integration: mapped EDI -> internal order, validated")
# 3) Data Hub: match the customer to a golden record
golden = {"name": order["customer"], "email": order["email"], "golden_id": "C-100"}
log.append(f"Data Hub: matched '{order['customer']}' -> golden {golden['golden_id']}")
# 4) Flow: human approval because amount > $1000
approved = order["amount"] > 1000
log.append(f"Flow: amount ${order['amount']} > $1000 -> manager approval -> {'APPROVED' if approved else 'HELD'}")
# 5) API Management: expose order status as a governed API
log.append("API Mgmt: published GET /orders/PO-9987 (auth + rate-limited) for partners")
# 6) Integration: write to ERP
if approved: log.append("Integration: created order in ERP (Atom runtime, prod Molecule)")

print("CAPSTONE — one order across the WHOLE Boomi platform:\n")
for step in log: print(f"   {step}")
print()
print("An X12 partner order flows through B2B/EDI (receive), INTEGRATION (map/validate/write),")
print("DATA HUB (golden customer), FLOW (human approval), and API MANAGEMENT (governed status")
print("API) — all on ONE low-code platform over the Atom runtime. That end-to-end connectivity")
print("is what Boomi delivers, and what this volume's certifications, track by track, prepare you")
print("to build.")
EOF
```

**Expected result:** A capstone tracing a partner order through B2B/EDI (receive an X12 850), Integration (map/validate/write), Data Hub (match to a golden customer), Flow (manager approval over the threshold), and API Management (a governed status API) — all on one platform over the Atom runtime. The lesson synthesizes the volume: Boomi connects applications, data, people, and partners on one low-code iPaaS, and each certification track prepares you to build one part of that end-to-end flow.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Roles mapped to certifications — developer, API, Data Hub, EDI, Flow, admin, architect.
- [ ] A sensible sequence chosen — start with Integration Developer, climb to Professional, broaden, then architect/operate.
- [ ] The Associate → Professional progression understood across tracks — breadth plus depth.
- [ ] Boomi placed in the ecosystem — the low-code connective tissue among apps, data, people, and partners.

## See also

- [Chapter 01 — The Boomi Certification Program](01-the-boomi-program.md) — the tracks and mechanics this plan draws on.
- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) and [Volume CLXV — Informatica](../../volume-165-informatica-certifications/README.md) — integration and data-management peers.
- [Volume CXLIV — SAP](../../volume-144-sap-certifications/README.md) — a major system Boomi connects (Boomi for SAP).
