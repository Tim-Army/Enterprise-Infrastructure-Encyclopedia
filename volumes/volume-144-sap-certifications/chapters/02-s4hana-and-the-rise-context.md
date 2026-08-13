# Chapter 02: S/4HANA and the RISE Context

## Learning Objectives

- Explain what S/4HANA is and how it differs from the ECC systems it replaces.
- Distinguish Cloud Public Edition, Cloud Private Edition, and on-premise deployment.
- Understand the RISE with SAP and GROW with SAP transformation offers.
- Read the S/4HANA certification landscape by functional module.

*Cert relevance: the S/4HANA certifications (Finance, Controlling, Sales, Sourcing & Procurement, Project Systems, Conversion & Upgrade) and the experience-gated **RISE with SAP Methodology** (C_RISME).*

## What S/4HANA is

**S/4HANA** is SAP's current-generation ERP suite, the successor to **ECC** (ERP Central Component, the "SAP" most people over a certain age picture). Two changes define it:

| | ECC (the predecessor) | S/4HANA |
|:---|:---|:---|
| Database | Any (Oracle, DB2, SQL Server, …) | **HANA only** — SAP's in-memory columnar database |
| Data model | Many aggregate/index tables maintained alongside line items | **Simplified** — aggregates computed on the fly from line items in memory |
| UI | SAP GUI (transaction codes) | **Fiori** — role-based web apps, though GUI persists underneath |

The in-memory point is the one that changed the software rather than just the hardware: because HANA holds the data in memory in columnar form, aggregates that ECC pre-computed into separate tables (and had to keep in sync) can be calculated instantly from the source line items. Whole categories of table, reconciliation, and batch job simply disappear. That simplification is why an S/4HANA *conversion* from ECC is a project, not an upgrade — the data model beneath the business processes changed.

## Three deployments

The single most confused point in the S/4HANA landscape, and the one the certifications split along:

| Deployment | What it is | Who runs it |
|:---|:---|:---|
| **Cloud Public Edition** | Multi-tenant SaaS, standardized processes, quarterly updates | SAP — you adopt SAP's best-practice processes |
| **Cloud Private Edition** | Single-tenant, more customizable, cloud-hosted | SAP/hyperscaler — your configuration, cloud-operated |
| **On-premise** | You run it, maximum customization | You |

The trade is the classic SaaS one, at ERP scale: **Public Edition gives up customization for SAP-managed standardization and continuous updates; Private Edition keeps customization at the cost of carrying more of the change**. The certification catalog reflects the split — many current certs specify "Cloud Private Edition" (e.g. Financial Accounting, Management Accounting, Sourcing and Procurement), because the configuration a consultant learns differs by edition.

## RISE and GROW

Two transformation offers wrap S/4HANA, and the certifications reference them:

- **RISE with SAP** — the bundled offer to move existing SAP customers to **S/4HANA Cloud Private Edition** as a managed transformation: software, infrastructure, and methodology together. The **RISE with SAP Methodology** certification (C_RISME) is experience-gated precisely because it certifies the ability to *run these transformations*, not to recite them.
- **GROW with SAP** — the equivalent for *new* customers adopting **S/4HANA Cloud Public Edition** — a faster, standardized on-ramp.

The mnemonic: **RISE = existing customers → Private Edition; GROW = new customers → Public Edition.** Both sit on top of the [SAP Activate methodology](03-sap-activate-and-project-methodology.md) (Chapter 03).

## The certification landscape by module

S/4HANA certifications are organized by **functional module** — the business areas SAP has always been structured around:

| Module | Covers |
|:---|:---|
| **FI** (Financial Accounting) | General ledger, AP/AR, asset accounting, external reporting |
| **CO** (Management Accounting / Controlling) | Cost centers, internal orders, profitability analysis |
| **SD** (Sales) | Order-to-cash, pricing, delivery, billing |
| **MM** (Sourcing & Procurement) | Procure-to-pay, purchasing, inventory |
| **PS** (Project Systems) | Project planning, costing, execution |
| **Conversion & Upgrade** | The ECC → S/4HANA transition (Specialist) |

Choosing a module is choosing a career lane — an FI consultant and an SD consultant do genuinely different work — and it is the first real decision in an SAP path (Chapter 09).

## Hands-On Lab

Python models the S/4HANA decisions. **Cost:** none.

### Lab 2.1 — Why conversion is a project, not an upgrade

**Objective:** See what the in-memory simplification removes.

```bash
python3 - <<'EOF'
# ECC kept aggregate tables in sync with line items; S/4HANA computes on the fly
ECC_TABLES = {
  "BKPF/BSEG":     "accounting doc header + line items (the source of truth)",
  "GLT0":          "G/L totals — AGGREGATE, kept in sync by updates",
  "KNC1/LFC1":     "customer/vendor totals — AGGREGATE",
  "FAGLFLEXT":     "new-G/L totals — AGGREGATE",
  "index tables":  "secondary indexes for reporting — REDUNDANT copies",
}
S4_TABLES = {
  "ACDOCA":        "Universal Journal — ONE line-item table; totals computed in memory",
}
print("ECC financial data model:")
for t, role in ECC_TABLES.items():
    print(f"   {t:16} {role}")
print(f"\n   {len(ECC_TABLES)} table groups, {len([r for r in ECC_TABLES.values() if 'AGGREGATE' in r or 'REDUNDANT' in r])} of them")
print("   redundant aggregates that must be RECONCILED when they drift.\n")
print("S/4HANA financial data model:")
for t, role in S4_TABLES.items():
    print(f"   {t:16} {role}")
print("\n   1 line-item table. Aggregates are QUERIES against it, computed in memory,")
print("   so they cannot drift — there is nothing to reconcile.\n")
print("This is why conversion is a PROJECT: the data model changed under the")
print("business processes. Custom code that read GLT0 must be rewritten to read")
print("ACDOCA; month-end reconciliation jobs between line items and totals become")
print("meaningless; reports change. An 'upgrade' changes the version; a CONVERSION")
print("changes the shape of the data. The Conversion & Upgrade Specialist cert")
print("exists because this is genuinely hard and genuinely different work.")
EOF
```

**Expected result:** ECC's several aggregate/redundant table groups collapsing into S/4HANA's single Universal Journal (ACDOCA), with the reconciliation work disappearing. The project-not-upgrade framing is the takeaway — the data model changed beneath the processes, which is why custom code breaks and a dedicated Conversion certification exists.

**Negative test:** Scoping an ECC→S/4HANA move as a version upgrade. The custom reports reading the old aggregate tables break, and "why is finance's report empty?" becomes the go-live incident.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Public vs Private vs on-premise, by requirement

**Objective:** Match a deployment to what actually decides it.

```bash
python3 - <<'EOF'
CRITERIA = [
  # criterion,                         weight, public, private, onprem
  ("adopt SAP standard processes",         5,    5,      3,      1),
  ("heavy existing customization to keep", 5,    1,      4,      5),
  ("continuous quarterly updates ok",      4,    5,      3,      1),
  ("data residency / full control",        4,    2,      4,      5),
  ("speed to value / low ops burden",      4,    5,      3,      1),
  ("existing SAP customer (brownfield)",   3,    2,      5,      4),
]
def score(col):
    return sum(w * c[col] for c in ((cr, w, pu, pr, on) for cr, w, pu, pr, on in CRITERIA) for _ in [0])
pub = sum(w*pu for _, w, pu, _, _ in CRITERIA)
pri = sum(w*pr for _, w, _, pr, _ in CRITERIA)
onp = sum(w*on for _, w, _, _, on in CRITERIA)
print(f"{'criterion':36}{'wt':>4}{'Public':>8}{'Private':>9}{'OnPrem':>8}")
for cr, w, pu, pr, on in CRITERIA:
    print(f"{cr:36}{w:>4}{pu:>8}{pr:>9}{on:>8}")
print(f"\n{'WEIGHTED':36}{'':>4}{pub:>8}{pri:>9}{onp:>8}")
print("\nThe profile decides, and the profile is mostly two questions:")
print("  'new or existing SAP customer?' and 'how much customization must survive?'")
print("  new + willing to standardize -> PUBLIC (GROW with SAP)")
print("  existing + heavy customization -> PRIVATE (RISE with SAP)")
print("  absolute control / regulatory -> ON-PREMISE (and you carry everything)")
print("\nThe certifications follow this split: 'Cloud Private Edition' in a cert name")
print("is not decoration — the configuration you learn differs by edition, so the")
print("credential is edition-specific on purpose.")
EOF
```

**Expected result:** A weighted comparison resolving to the two questions that actually decide edition — customer status and customization needs — with RISE/GROW mapped onto Private/Public. The certification note is the practical payoff: edition names in cert titles signal genuinely different configuration content, not marketing.

**Negative test:** Studying Public Edition configuration for a Private Edition role. The processes and customization model differ; the certification specifies the edition because the work does.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — RISE vs GROW, and the module lane

**Objective:** Place a customer and pick a certification lane.

```bash
python3 - <<'EOF'
CUSTOMERS = [
  ("20-yr SAP ECC shop, heavy custom code",  "existing", "high custom"),
  ("startup, no SAP, wants ERP fast",         "new",      "standard"),
  ("mid-size, some SAP, modernizing",         "existing", "moderate"),
]
for desc, status, custom in CUSTOMERS:
    offer = "RISE with SAP -> S/4HANA Cloud PRIVATE Edition" if status == "existing" else "GROW with SAP -> S/4HANA Cloud PUBLIC Edition"
    print(f"  {desc}")
    print(f"     {status} customer, {custom} -> {offer}\n")

print("RISE = existing customers move to PRIVATE. GROW = new customers adopt PUBLIC.")
print("Both run on SAP Activate methodology (Chapter 03).\n")

MODULES = {
  "FI (Financial Accounting)":  "GL, AP/AR, assets, external reporting",
  "CO (Controlling)":           "cost centers, internal orders, profitability",
  "SD (Sales)":                 "order-to-cash, pricing, billing",
  "MM (Sourcing & Procurement)":"procure-to-pay, inventory",
  "PS (Project Systems)":       "project planning, costing, execution",
}
print("Then choose the MODULE lane — a genuine career fork:")
for m, scope in MODULES.items():
    print(f"   {m:30} {scope}")
print("\nAn FI consultant and an SD consultant do DIFFERENT jobs, hold DIFFERENT")
print("certifications, and rarely cross over deeply. The module is the first big")
print("career decision (Chapter 09) — pick it by the business area you want to")
print("live in, because the certification, the projects, and the roles all follow it.")
EOF
```

**Expected result:** Three customers routed to RISE or GROW by status, and the module lanes laid out as career forks. The two mnemonics (RISE/existing/Private, GROW/new/Public) and the module-as-career-choice framing are the durable takeaways from an otherwise sprawling landscape.

**Negative test:** Pursuing a broad "S/4HANA certification" with no module. The catalog has no such thing at consultant level — you certify in FI, or SD, or MM; the module is the credential.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] S/4HANA distinguished from ECC by the HANA in-memory data-model simplification.
- [ ] Conversion understood as a project because the data model changed, not just the version.
- [ ] Public, Private, and on-premise editions matched to customer status and customization needs.
- [ ] RISE (existing→Private) and GROW (new→Public) placed, and a module lane chosen.
