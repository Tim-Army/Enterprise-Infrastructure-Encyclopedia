# Chapter 04: Building an Application — The System Architect

## Learning Objectives

- Explain the System Architect's core build activities.
- Describe the data model — data types, data pages, integrations.
- Understand the model-driven UI.
- Recognize flows, decisions, and validation as rules.

*Cert relevance: building applications is the heart of the Certified System Architect (CSA) role.*

## The System Architect's job

The **Certified System Architect (CSA)** **builds Pega applications** — turning a [case type (Ch 3)](03-case-management.md) into a working application by defining its **data**, its **UI**, its **logic**, and its **integrations**. Where a [business architect (Ch 8)](08-business-architect-and-dco.md) captures *what* the application should do, the System Architect **implements** it on the [platform (Ch 2)](02-the-pega-platform.md) — model-driven, in App Studio and Dev Studio. Building an application is the foundational Pega skill and the core of the CSA certification. The lab models building.

## The data model

An application needs **data**, and Pega's **data model** defines it:

- **Data types** — the business objects the app works with (Applicant, Loan, Account) — Pega's equivalent of data entities.
- **Data pages** — cached, reusable **sources of data** that load data (from Pega or external systems) on demand, so the app has the data it needs without repeated fetching.
- **Integrations** — **connectors** to external **systems of record** (databases, REST/SOAP services, [MuleSoft-style integration, CLX](../../volume-160-mulesoft-certifications/README.md)) so Pega reads and writes data where it lives, rather than duplicating it.

A well-designed data model gives the case the data it needs, sourced efficiently and integrated with the enterprise's systems. The lab models the data model.

## The model-driven UI

Pega generates a **model-driven UI** — you define the **fields and layout** in the model, and Pega renders a **responsive** user interface automatically (working on desktop and mobile). This is part of low-code: you don't hand-code HTML/CSS/JavaScript for standard screens; you model the UI (which fields, which layout, which controls) and Pega produces it. This dramatically speeds UI development and keeps it consistent, and it stays **in the guardrails** ([Ch 2](02-the-pega-platform.md)). For most enterprise applications, model-driven UI delivers the screens users need without custom front-end code. The lab models the UI.

## Flows, decisions, and validation

The application's **logic** is expressed as **rules** ([Ch 2](02-the-pega-platform.md)):

- **Flows** — the sequence of steps in a process (route here, then there, based on conditions).
- **Decisions** — logic that determines an outcome (decision tables, decision trees, when-rules) — e.g., "if credit score ≥ 700 and income ≥ X, auto-approve."
- **Validation** — rules ensuring data is correct and complete before proceeding.

Because these are all **rules** in the model, they're **visual**, **reusable**, and **changeable** without code — a business analyst can often read (and sometimes edit) a decision table. Assembling data, UI, flows, decisions, and validation into a working application is exactly what the System Architect does. The lab synthesizes.

## Hands-On Lab

Python models building an application. **Cost:** none.

### Lab 4.1 — Assemble data, UI, decisions, and integration

**Objective:** Model the System Architect building an application.

```bash
python3 - <<'EOF'
# a System Architect assembles: data model + model-driven UI + decision rules + integration
data_types = {"Applicant": ["name", "income", "creditScore"], "Loan": ["amount", "term", "status"]}
data_pages = {"D_CreditScore": "loads credit score from external bureau (REST connector)"}
ui_form = {"fields": ["Applicant.name", "Applicant.income", "Loan.amount"], "rendered": "responsive (model-driven, no HTML)"}

print("System Architect builds the app (model-driven, in App/Dev Studio):\n")
print("1) DATA MODEL:")
for dt, fields in data_types.items():
    print(f"     data type {dt}: {fields}")
print(f"     data page {list(data_pages)[0]}: {data_pages['D_CreditScore']}  (INTEGRATION to system of record)\n")
print("2) MODEL-DRIVEN UI (auto-rendered, no hand-coded front end):")
print(f"     form fields: {ui_form['fields']}  -> {ui_form['rendered']}\n")

# 3) DECISION rule (a decision table — reusable, readable, no code)
def auto_approve(credit, income):
    # decision table logic (what a Pega decision table encodes)
    if credit >= 700 and income >= 50000: return "AUTO-APPROVE"
    if credit >= 640: return "MANUAL REVIEW"
    return "DECLINE"
print("3) DECISION rule (decision table — a RULE, readable by business):")
for c, i in [(760, 80000), (660, 40000), (600, 30000)]:
    print(f"     credit={c}, income={i:>6} -> {auto_approve(c, i)}")
print()
print("The SYSTEM ARCHITECT (CSA) BUILDS the app: a DATA MODEL (data types + data pages that source")
print("data, INTEGRATIONS/connectors to systems of record), a MODEL-DRIVEN UI (responsive, auto-")
print("rendered, no front-end code), and LOGIC as rules — FLOWS, DECISIONS (decision tables/trees),")
print("VALIDATION. Because these are RULES in the model, they're visual + reusable + changeable")
print("WITHOUT code. Assembling all of it into a working app is the core CSA skill.")
EOF
```

**Expected result:** A System Architect assembling an application — a data model (data types, data pages with an external integration), a model-driven responsive UI (no hand-coded front end), and a decision-table rule that auto-approves, sends to manual review, or declines by credit and income. The build lesson is that the System Architect implements a case type by defining data (data types, data pages, connectors to systems of record), a model-driven UI, and logic as rules (flows, decisions, validation) — all visual, reusable, and changeable without code.

**Negative test:** Hand-coding data access, UI, and business logic in a custom language. That loses Pega's model-driven speed, reuse, and guardrail compliance; the System Architect builds with data types, data pages, model-driven UI, and decision rules on the platform.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The System Architect's job understood — building applications from case types on the platform.
- [ ] The data model understood — data types, data pages, and integrations to systems of record.
- [ ] The model-driven UI understood — responsive screens generated from the model without front-end code.
- [ ] Flows, decisions, and validation understood as rules — visual, reusable, and changeable logic.
