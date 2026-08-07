# Chapter 07: B2B/EDI and Flow

## Learning Objectives

- Explain B2B/EDI integration and the Trading Partner model.
- Describe EDI standards (X12, EDIFACT) and document types.
- Explain Boomi Flow — low-code workflow and user-facing apps.
- Understand the Associate EDI for X12 and Associate Flow Essentials certifications.

*Cert relevance: this chapter covers two tracks — Associate EDI for X12 and Associate Flow Essentials.*

## B2B and EDI

Enterprises do not just integrate their **own** systems — they exchange documents with **external trading partners**: suppliers, customers, logistics providers, banks. **B2B/EDI** is Boomi's service for this **partner-to-partner** exchange. **EDI (Electronic Data Interchange)** is the decades-old set of **standards** for exchanging business documents — purchase orders, invoices, shipping notices — in **structured, machine-readable** formats, so a buyer's system can send a purchase order directly into a supplier's system without paper or re-keying.

EDI is still the backbone of supply chains, retail, healthcare, and logistics. Boomi handles it with the **Trading Partner** model, and the **Associate EDI for X12** certification validates it. The lab parses an EDI document. *(This connects the enterprise outward, complementing the app integration of [Ch 4](04-building-integrations.md) and the APIs of [Ch 5](05-api-management.md).)*

## The Trading Partner model and EDI standards

Boomi models partner exchange with **Trading Partners**:

- A **Trading Partner** component represents **one partner** (a specific supplier or customer) and its **communication** setup (how you connect — AS2, SFTP, etc.) and **document standards**.
- The **Trading Partner step** in a process **sends to or receives from** a partner, handling the EDI envelope and acknowledgements.
- **Standards** define the document formats:
  - **X12** — the dominant standard in North America. Documents are identified by **numeric transaction sets**: **850** (Purchase Order), **810** (Invoice), **856** (Advance Ship Notice), **997** (Functional Acknowledgement).
  - **EDIFACT** — the international standard (ORDERS, INVOIC, DESADV), common in Europe and global trade.
  - **CUSTOM** — flat-file and other partner-specific formats.

An EDI document is **hierarchical and terminated** — segments (like `ST`, `BEG`, `PO1`) separated by delimiters. Boomi **parses** the EDI into a profile you can map to your internal format, and **generates** EDI from your data to send out. The lab parses an X12 850.

## Boomi Flow

**Boomi Flow** is a different kind of building: **low-code workflow and application development**. Where integration processes move data **system to system**, Flow builds **user-facing apps and workflows** that put **people in the loop**:

- **Workflows** — model a business process with **human steps**: approvals, reviews, data entry, decisions. A Flow can route a request through managers for sign-off, then trigger an integration.
- **User interfaces** — Flow generates **web/mobile UIs** (forms, pages) with little or no code, so you build an app, not just a back-end flow.
- **Orchestration** — Flows call **integration processes** and **APIs**, so a human workflow can drive back-end automation (submit a form → Flow calls a process → data lands in systems).

Flow extends Boomi from **system integration** to **human-centered applications** — connecting the **people** in "applications, data, people, and devices" ([Ch 2](02-the-boomi-platform.md)). The **Associate Flow Essentials** certification validates building Flow apps. The lab models a Flow approval workflow.

## Two Associate certifications

This chapter covers two entry-level tracks:

- **Associate EDI for X12** — validates configuring **Trading Partners** and handling **X12** EDI: parsing and generating transaction sets (850, 810, 856), envelopes, and acknowledgements.
- **Associate Flow Essentials** — validates building **low-code workflow apps**: steps, user interfaces, decisions, and calling integrations.

Both are foundational, open-book/open-platform credentials that specialize Boomi skills into **partner exchange** and **human workflow** respectively. The lab exercises both. *(Flow's low-code app-building echoes the low-code platforms elsewhere on this shelf, e.g. [Pega (Vol CLXIV)](../../volume-164-pega-certifications/README.md) and [ServiceNow (Vol LXXX)](../../volume-080-servicenow-certifications/README.md).)*

## Hands-On Lab

Python parses an X12 850 purchase order and runs a Flow approval workflow. **Cost:** none.

### Lab 7.1 — Parse EDI and run a Flow workflow

**Objective:** Parse an X12 850 to an internal order, then route it through a Flow approval.

```bash
python3 - <<'EOF'
# --- B2B/EDI: parse an X12 850 (Purchase Order) into an internal profile ---
# X12 is segment-based; '~' ends a segment, '*' separates elements
EDI_850 = "ST*850*0001~BEG*00*NE*PO-9987**20260806~N1*BY*ACME CORP~PO1*1*10*EA*25.00**CB*WIDGET-A~PO1*2*4*EA*100.00**CB*GADGET-B~CTT*2~SE*7*0001~"
def parse_x12(raw):
    segs = [s for s in raw.split("~") if s]
    order = {"lines": []}
    for seg in segs:
        el = seg.split("*")
        if el[0] == "BEG": order["po_number"] = el[3]           # PO number
        elif el[0] == "N1" and el[1] == "BY": order["buyer"] = el[2]
        elif el[0] == "PO1":                                    # a line item
            # PO1: *line*qty*uom*unitprice*basis*idQualifier*productId
            order["lines"].append({"line": el[1], "qty": int(el[2]), "uom": el[3],
                                    "price": float(el[4]), "item": el[7]})
    order["total"] = round(sum(l["qty"]*l["price"] for l in order["lines"]), 2)
    return order

po = parse_x12(EDI_850)
print("1) B2B/EDI — parse X12 850 Purchase Order -> internal order:")
print(f"      PO {po['po_number']} from {po['buyer']}  total=${po['total']}")
for l in po["lines"]:
    print(f"         line {l['line']}: {l['qty']} x {l['item']} @ ${l['price']} = ${l['qty']*l['price']}")

# --- FLOW: low-code approval workflow with a human step ---
def flow_approval(order):
    steps = []
    steps.append(("Start", "PO received from trading partner"))
    if order["total"] > 500:
        steps.append(("Human step", f"Manager approval required (${order['total']} > $500)"))
        approved = True                    # simulate the manager approving
        steps.append(("Decision", "approved" if approved else "rejected"))
    else:
        steps.append(("Auto", "under threshold — auto-approved"))
        approved = True
    if approved:
        steps.append(("Call process", "invoke integration p_create_order -> ERP"))
    return steps

print("\n2) FLOW — low-code approval workflow (people in the loop):")
for shape, detail in flow_approval(po):
    print(f"      [{shape:12}] {detail}")
print()
print("B2B/EDI parses a partner's X12 850 (segments BEG/N1/PO1 split on * and ~) into an")
print("internal order via the Trading Partner model — the Associate EDI for X12 cert. FLOW")
print("then routes it through a low-code workflow with a HUMAN approval step and calls an")
print("integration process — the Associate Flow Essentials cert. Together they connect")
print("external PARTNERS and internal PEOPLE, beyond system-to-system integration.")
EOF
```

**Expected result:** An X12 850 purchase order parsed into an internal order with buyer, two line items, and a computed total, then routed through a Flow workflow that requires manager approval (because the total exceeds the threshold) and calls an integration process on approval. The lesson is the two tracks: B2B/EDI parses and generates partner documents via the Trading Partner model (Associate EDI for X12), and Flow builds low-code human workflows that orchestrate integrations (Associate Flow Essentials).

**Negative test:** Emailing PDFs to the supplier and manually keying the order into the ERP. It is slow, error-prone, and unauditable; EDI via the Trading Partner model exchanges structured documents automatically, and Flow adds governed human approval before the ERP write.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] B2B/EDI understood — structured document exchange with external trading partners.
- [ ] The Trading Partner model and standards understood — X12 (850/810/856), EDIFACT, CUSTOM.
- [ ] Boomi Flow understood — low-code workflow and user-facing apps with people in the loop.
- [ ] The two Associate certifications placed — EDI for X12 and Flow Essentials.

## See also

- [Chapter 04 — Building Integrations](04-building-integrations.md) — the processes EDI and Flow orchestrate.
- [Chapter 08 — Administration and Architecture](08-administration-and-architecture.md) — operating and architecting the platform.
- [Volume CLXIV — Pega](../../volume-164-pega-certifications/README.md) — low-code workflow apps in the same spirit as Flow.
