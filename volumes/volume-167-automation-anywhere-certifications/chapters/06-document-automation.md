# Chapter 06: Document Automation

## Learning Objectives

- Explain why unstructured documents defeat classic RPA.
- Describe Document Automation (intelligent document processing).
- Understand extraction, validation, and human-in-the-loop correction.
- Recognize where Document Automation fits the AI Automation Engineer path.

*Cert relevance: Document Automation is a pillar of the AI Automation Engineer certification.*

## Why documents break classic RPA

Classic RPA ([Ch 3](03-building-bots.md)) automates **structured, predictable** interactions — click this field, read that cell. But a huge amount of business input is **unstructured documents**: **invoices, purchase orders, receipts, forms, contracts**. These vary wildly — every vendor's invoice has a different layout, the total is in a different place, fields are named differently — so a bot that expects data at fixed coordinates **fails immediately**. Extracting data from documents is the classic **"last mile" problem** of automation, and it is exactly where AI is needed.

**Document Automation** is Automation Anywhere's **intelligent document processing (IDP)** — AI/ML that **reads** documents and **extracts structured data** from them, so a bot can process what a human would otherwise re-key by hand. (It is the successor to the earlier **IQ Bot**.) This is a pillar of the **AI Automation Engineer** path ([Ch 1](01-the-automation-anywhere-program.md)). The lab extracts fields from varied documents.

## Extraction

Document Automation **turns a document into data**:

- **Classify** — identify the document **type** (is this an invoice, a PO, a receipt?).
- **Extract** — pull the **fields** you care about (invoice number, date, vendor, line items, total) regardless of where they sit on the page, using AI models rather than fixed positions.
- **Handle variation** — because it learns **patterns and context** (the total is the number near the word "Total"/"Amount Due"), it generalizes across layouts it has not seen exactly before.

The output is **structured data** — a clean record a downstream bot can enter into the ERP. This is the step that lets automation handle the messy, high-volume document work (accounts payable, onboarding, claims) that was previously manual. The lab classifies and extracts.

## Validation and human-in-the-loop

AI extraction is powerful but **not perfect**, so Document Automation builds in **confidence and correction**:

- **Confidence scores** — each extracted field carries a confidence. High-confidence fields flow straight through; low-confidence ones are flagged.
- **Validation rules** — assert what must be true (the line items sum to the total; the date is valid; the vendor exists) and catch extraction errors.
- **Human-in-the-loop review** — low-confidence or failed-validation documents route to a **person** ([Ch 5](05-attended-unattended-and-copilot.md)) who corrects the value in a review interface; the correction can **improve the model** over time.

This **straight-through where confident, human where not** design is what makes IDP trustworthy at scale: most documents process automatically, and only the genuinely ambiguous ones need a human. The lab adds confidence-based routing and validation. *(The confidence/validation pattern parallels data-quality scoring in [Informatica (CLXV Ch 6)](../../volume-165-informatica-certifications/chapters/06-data-quality.md).)*

## Fitting the AI Automation Engineer path

Document Automation is where **RPA meets AI** most concretely: a deterministic bot alone cannot read a novel invoice, but a bot **plus** IDP can process the whole accounts-payable pipeline end to end — read the invoice, validate it, enter it, route exceptions to a human. This composition — **AI to understand, RPA to act** — is the essence of the **AI Automation Engineer** competency. Mastering extraction, confidence handling, and human-in-the-loop correction is what turns a bot developer into an automation **engineer** who can deliver document-heavy processes. The lab runs the full extract → validate → route pipeline.

## Hands-On Lab

Python simulates Document Automation — classify, extract, confidence, validation, and routing. **Cost:** none.

### Lab 6.1 — Read documents with intelligent document processing

**Objective:** Classify and extract fields, score confidence, validate, and route exceptions to a human.

```bash
python3 - <<'EOF'
# Document Automation (IDP): classify -> extract fields (with confidence) -> validate -> route
DOCS = [
  {"text": "INVOICE  No INV-100  Vendor: Acme  Line: 2x50=100  Total: 100.00", "layout": "A"},
  {"text": "Invoice#INV-200 | Globex | items 80 | AMOUNT DUE 80.00",           "layout": "B"},  # different layout
  {"text": "INVOICE  No INV-300  Vendor: Initech  Total: ????",                "layout": "C"},  # unreadable total -> low confidence
]
import re
def classify(t):  return "invoice" if re.search(r"invoice", t, re.I) else "unknown"
def extract(t):
    num  = (re.search(r"INV-\d+", t) or [None])
    num  = num.group() if hasattr(num, "group") else None
    tot  = re.search(r"(?:total|amount due)[:\s]*([0-9.]+)", t, re.I)
    total, conf = (float(tot.group(1)), 0.98) if tot and tot.group(1).replace('.','').isdigit() else (None, 0.30)
    return {"invoice_no": num, "total": total, "confidence": conf}

print("DOCUMENT AUTOMATION (IDP) — classify -> extract -> validate -> route:\n")
straight_through, to_human = [], []
for d in DOCS:
    doc_type = classify(d["text"])
    fields = extract(d["text"])
    # validate + confidence routing
    valid = fields["total"] is not None and fields["confidence"] >= 0.80
    print(f"   layout {d['layout']}: type={doc_type} {fields}")
    if valid:
        straight_through.append(fields["invoice_no"]); print(f"      -> STRAIGHT-THROUGH (high confidence, valid)")
    else:
        to_human.append(fields["invoice_no"]); print(f"      -> HUMAN REVIEW (low confidence / failed validation)")
print()
print(f"   straight-through: {straight_through}   human review: {to_human}")
print()
print("IDP CLASSIFIES the document and EXTRACTS fields across DIFFERENT LAYOUTS (A/B) that")
print("fixed-position RPA could not — finding the total near 'Total'/'Amount Due'. Each field")
print("carries a CONFIDENCE score; high-confidence valid docs go STRAIGHT-THROUGH, low-confidence")
print("ones (unreadable total) route to a HUMAN. AI to understand + RPA to act = the AI Automation")
print("Engineer competency.")
EOF
```

**Expected result:** Two invoices in different layouts are classified and extracted straight-through with high confidence, while a third with an unreadable total is flagged low-confidence and routed to human review. The lesson is intelligent document processing: classify and extract fields across varied layouts (where fixed-position RPA fails), score confidence, validate, and route only the ambiguous documents to a human — the AI-understands/RPA-acts composition central to the AI Automation Engineer certification.

**Negative test:** Using a fixed-position RPA bot to read invoices. The moment a vendor's layout differs, the bot reads the wrong cell or fails; IDP generalizes across layouts by learning context, and confidence-based routing keeps the errors it does make from flowing through unchecked.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The unstructured-document problem understood — varied layouts defeat fixed-position RPA.
- [ ] Document Automation understood — AI/ML intelligent document processing (successor to IQ Bot).
- [ ] Extraction, confidence, and validation understood — turn documents into validated structured data.
- [ ] Human-in-the-loop correction understood — straight-through where confident, human where not.

## See also

- [Chapter 05 — Attended, Unattended, and Automation Co-Pilot](05-attended-unattended-and-copilot.md) — the human-in-the-loop review interface.
- [Chapter 07 — Agentic Process Automation and AI Agent Studio](07-agentic-process-automation.md) — the broader AI/agentic layer over automation.
- [Volume CLXV — Informatica](../../volume-165-informatica-certifications/chapters/06-data-quality.md) — confidence and validation in data quality.
