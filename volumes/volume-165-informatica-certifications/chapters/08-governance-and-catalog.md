# Chapter 08: Data Governance and Catalog

## Learning Objectives

- Explain the data catalog — knowing what data you have.
- Describe data lineage — where data came from and where it goes.
- Understand governance — glossary, ownership, policy, and stewardship.
- Recognize CLAIRE's role in metadata intelligence and classification.

*Cert relevance: Cloud Data Governance & Catalog is its own Professional certification; this chapter is where CLAIRE is most visible.*

## Knowing what data you have

A large enterprise has **thousands** of tables, files, and reports spread across databases, warehouses, and lakes. Ask "**where is customer data, and can I trust it?**" and most organizations cannot answer. **Cloud Data Governance & Catalog (CDGC)** is the IDMC module that answers it: it **scans** your data estate, **catalogs** every asset, records **where data comes from and goes** (lineage), and applies **governance** — a business glossary, ownership, and policy — so data is **discoverable, understood, and controlled**.

If integration ([Ch 3](03-cloud-data-integration.md)) moves data and quality ([Ch 6](06-data-quality.md)) makes it trustworthy, governance and catalog make it **known and governed**. This is the module where the **metadata fabric** ([Ch 2](02-idmc-platform.md)) and **CLAIRE** are most visible, because governance **is** the discipline of managing metadata. The **Cloud Data Governance & Catalog, Professional** certification validates it. The lab builds a catalog with lineage and governance.

## The data catalog

A **catalog** is a **searchable inventory of data assets**. CDGC **scans** connected systems and records, for each asset:

- **Technical metadata** — the table/file name, columns, data types, row counts, location.
- **Business metadata** — a plain-language description, the **glossary terms** it relates to (this column is a "Customer Email"), and tags.
- **Operational metadata** — when it was last loaded, by which job, and its **quality score** ([Ch 6](06-data-quality.md)).

The result is a place where a data analyst can **search "customer revenue"** and find the **right, trusted** table — with its description, owner, freshness, and quality — instead of guessing among a dozen similarly named tables. The catalog turns a sprawling data estate into something **discoverable**. The lab builds and searches a catalog.

## Data lineage

**Lineage** answers **"where did this data come from, and where does it go?"** — the **end-to-end path** of data through your systems:

- **Upstream** — this warehouse column was loaded by that mapping from those source tables.
- **Downstream** — this source column feeds those warehouse tables and, ultimately, those reports and dashboards.

Lineage is essential for **impact analysis** (if we change this source, what breaks?), **root-cause analysis** (this report is wrong — trace it back to the bad source), and **compliance** (prove where personal data flows). Because IDMC's modules share the **metadata fabric**, lineage is captured **automatically** as integration mappings run — CDGC can show a **column-level path** from source system to final dashboard. The lab computes lineage across a pipeline.

## Governance — glossary, ownership, and policy

**Governance** turns a catalog into a **controlled** asset:

- **Business glossary** — an agreed vocabulary of **business terms** ("Active Customer", "Net Revenue") with definitions, **linked to the technical assets** that implement them, so business and IT share one language.
- **Ownership and stewardship** — every important asset has an **owner** and **steward** accountable for it (the same stewardship idea as MDM, [Ch 7](07-master-data-management.md)).
- **Policies and classification** — rules that **classify** data (this column is **PII**; that dataset is **confidential**) and govern its use, feeding access control and compliance.

Governance makes data **trustworthy and defensible**: you can show **what** you have, **who owns it**, **what it means**, and **how it must be handled**. The lab adds a glossary and PII classification. *(Governed, classified data underpins compliance and security programs across this shelf — the data-protection and privacy work in security volumes rests on knowing where sensitive data lives.)*

## CLAIRE — metadata intelligence

**CLAIRE** ([Ch 2](02-idmc-platform.md)) is most visible here because governance is metadata-heavy, and CLAIRE is the **AI/ML engine over metadata**:

- **Auto-classification** — CLAIRE **recognizes** that a column contains email addresses or national IDs and **tags it as PII automatically**, across thousands of assets no human could hand-label.
- **Auto-curation** — it **suggests glossary associations**, descriptions, and relationships, bootstrapping a catalog that would take years to build by hand.
- **Similarity and discovery** — it finds **similar and duplicate datasets** and surfaces relationships humans miss.

The pattern is the platform's core promise: **the more metadata the fabric holds, the more CLAIRE can automate**. Governance at enterprise scale is only feasible because AI does the first pass of classification and curation, leaving humans to **review and approve**. The lab uses a CLAIRE-style auto-classifier.

## Hands-On Lab

Python builds a catalog, computes lineage, classifies PII (CLAIRE-style), and adds a glossary. **Cost:** none.

### Lab 8.1 — Catalog, lineage, and CLAIRE-style classification

**Objective:** Inventory assets, trace column lineage, and auto-classify sensitive data.

```bash
python3 - <<'EOF'
import re
# --- CATALOG: scanned assets (technical + operational metadata) ---
CATALOG = [
  {"asset": "src.crm.customer",  "columns": ["cust_id", "email", "full_name", "ssn"],       "quality": 0.86},
  {"asset": "wh.dim_customer",   "columns": ["customer_key", "email", "name", "region"],    "quality": 0.94},
  {"asset": "bi.customer_report","columns": ["region", "active_customers", "net_revenue"],  "quality": 0.91},
]
# --- LINEAGE: how columns flow source -> warehouse -> report ---
LINEAGE = [
  ("src.crm.customer.email",    "wh.dim_customer.email"),
  ("src.crm.customer.full_name","wh.dim_customer.name"),
  ("wh.dim_customer.region",    "bi.customer_report.region"),
]
def upstream_of(col):
    seen, frontier = [], [col]
    while frontier:
        c = frontier.pop()
        for s, t in LINEAGE:
            if t == c:
                seen.append(s); frontier.append(s)
    return seen

print("1) CATALOG (searchable inventory):")
for a in CATALOG:
    print(f"      {a['asset']:22} cols={a['columns']}  quality={a['quality']}")

print("\n2) LINEAGE (impact + root cause):")
target = "bi.customer_report.region"
print(f"      upstream of {target}: {upstream_of(target)}")

# --- CLAIRE-style AUTO-CLASSIFICATION of sensitive data ---
CLASSIFIERS = {
  "PII:email": re.compile(r"email", re.I),
  "PII:national_id": re.compile(r"ssn|national_id", re.I),
  "PII:name": re.compile(r"name", re.I),
}
print("\n3) CLAIRE-style AUTO-CLASSIFICATION (PII tagging across all assets):")
for a in CATALOG:
    for col in a["columns"]:
        tags = [label for label, rx in CLASSIFIERS.items() if rx.search(col)]
        if tags:
            print(f"      {a['asset']}.{col:14} -> {tags}")

# --- GOVERNANCE: business glossary linked to technical assets ---
GLOSSARY = {"Active Customer": "bi.customer_report.active_customers",
            "Net Revenue": "bi.customer_report.net_revenue"}
print("\n4) GLOSSARY (business term -> technical asset):")
for term, asset in GLOSSARY.items():
    print(f"      '{term}' -> {asset}")
print()
print("The CATALOG makes the estate discoverable; LINEAGE traces columns source->report")
print("for impact and root-cause; CLAIRE AUTO-CLASSIFIES PII across thousands of columns no")
print("human could hand-label; the GLOSSARY links business language to technical assets.")
print("Knowing WHAT data you have, WHERE it flows, WHAT it means, and HOW it must be handled")
print("is the Cloud Data Governance & Catalog Professional certification.")
EOF
```

**Expected result:** A catalog of three assets with quality scores, a column-lineage trace from the report back to source, a CLAIRE-style auto-classifier tagging email/SSN/name columns as PII across all assets, and a business glossary linking terms to technical assets. The lesson is CDGC's scope — catalog (discoverable), lineage (traceable), classification (AI-assisted governance), and glossary (shared language) — with CLAIRE doing the classification pass at a scale no human could, the substance of the CDGC Professional certification.

**Negative test:** Governing a large estate by hand — analysts manually documenting and classifying thousands of columns. It never finishes and drifts immediately; CLAIRE's automated scanning, lineage capture, and auto-classification is what makes enterprise governance feasible, with humans reviewing rather than labeling from scratch.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The catalog understood — a searchable inventory of assets with technical, business, and operational metadata.
- [ ] Lineage understood — end-to-end column paths for impact analysis, root cause, and compliance.
- [ ] Governance understood — glossary, ownership/stewardship, and classification/policy.
- [ ] CLAIRE placed — metadata intelligence that auto-classifies and auto-curates at enterprise scale.

## See also

- [Chapter 02 — IDMC](02-idmc-platform.md) — the metadata fabric and CLAIRE that power governance.
- [Chapter 06 — Cloud Data Quality](06-data-quality.md) — quality scores that become governed catalog metadata.
- [Chapter 07 — Master Data Management](07-master-data-management.md) — the stewardship discipline governance shares.
