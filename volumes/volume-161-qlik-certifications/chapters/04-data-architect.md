# Chapter 04: Data Architect — Loading and Modeling Data

## Learning Objectives

- Explain the Data Architect role — building the data model.
- Describe the Data Load Editor and load script.
- Understand associations, keys, and avoiding synthetic keys.
- Recognize QVD files and optimized loading.

*Cert relevance: the Qlik Sense Data Architect (QSDA) certification validates modeling and loading data.*

## The Data Architect role

The **Qlik Sense Data Architect** builds the **data model** that everything else depends on — identifying requirements for the model, **designing and building** it, and **validating** the data. Before an analyst can build a single chart, the data must be **loaded, associated, and correct**. The Data Architect writes the **load script** that pulls data from sources, transforms it, and shapes it into a well-formed [associative model (Ch 2)](02-the-associative-model.md). A good data model makes analysis fast and correct; a bad one makes every downstream app slow, wrong, or confusing. The QSDA certification validates this foundational skill. The lab models the role.

## The Data Load Editor and load script

The Data Architect works in the **Data Load Editor**, writing a **load script** — Qlik's scripting language for **extracting, transforming, and loading (ETL)** data:

- **Connect** to sources (databases, files, REST APIs, SaaS).
- **LOAD** statements read tables and select/rename/derive fields.
- **Transformations** — join, concatenate, map, aggregate, and clean data in the script.
- **Reload** runs the script to refresh the model with current data.

The script is where raw source data becomes the clean, associated model the app uses. Scripting is the core Data Architect skill the QSDA exam tests. The lab models a load script.

## Associations, keys, and synthetic keys

Qlik **automatically associates** tables through **fields with the same name** — this is the heart of the associative model, and it means the Data Architect must be deliberate about field names. Two rules dominate:

- **One common field = a clean association.** Tables link through a shared key field (e.g., `CustomerID`), and Qlik associates them automatically.
- **Multiple common fields = a synthetic key** — when two tables share *more than one* field name, Qlik creates an artificial **synthetic key**, usually a **modeling error** that bloats the model and confuses associations. The Data Architect **avoids synthetic keys** by renaming or combining fields deliberately.

Getting associations right — clean single keys, no accidental synthetic keys, no circular references (**loops**) — is the essence of Qlik data modeling and a heavily-tested QSDA skill. The lab models association and synthetic keys.

## QVD files and optimized loading

**QVD (QlikView Data)** files are Qlik's **optimized binary data format** — a table stored in a single file that loads **very fast**. Data Architects use QVDs as an intermediate layer: extract from slow sources into QVDs once, then load apps rapidly from the QVDs (an **optimized load**), rather than hitting the source systems every reload. QVDs enable a **layered architecture** (extract → transform → present) that is efficient and reusable across apps. Understanding QVDs and optimized loading is part of building a performant Qlik environment. The lab models QVD efficiency.

## Hands-On Lab

Python models associations and synthetic keys. **Cost:** none.

### Lab 4.1 — Clean associations, synthetic keys, and QVD loading

**Objective:** See correct modeling and the synthetic-key pitfall.

```bash
python3 - <<'EOF'
# Qlik associates tables by SAME-NAMED fields. Model two ways: clean vs synthetic key.
def common_fields(t1, t2): return set(t1) & set(t2)

print("CASE A — clean model (ONE common field = a good association):")
customers = ["CustomerID", "CustomerName", "Region"]
sales_a   = ["SaleID", "CustomerID", "Amount"]          # shares ONLY CustomerID
common = common_fields(customers, sales_a)
print(f"   Customers{customers}")
print(f"   Sales{sales_a}")
print(f"   common fields: {common} -> associate cleanly on CustomerID  (GOOD)\n")

print("CASE B — SYNTHETIC KEY (TWO+ common fields = a modeling error):")
sales_b = ["SaleID", "CustomerID", "Region", "Amount"]  # shares CustomerID AND Region
common = common_fields(customers, sales_b)
print(f"   Customers{customers}")
print(f"   Sales{sales_b}")
print(f"   common fields: {common} -> Qlik builds a SYNTHETIC KEY $Syn1 (BAD: bloats model,")
print(f"      confuses associations). FIX: rename/qualify (e.g. drop Region from Sales, or")
print(f"      derive Region via the Customers table only).\n")

# QVD optimized loading
print("QVD (QlikView Data) — optimized binary format for FAST loads:")
print("   layered: EXTRACT source -> store to QVD (once)  ->  apps LOAD from QVD (fast, reusable)")
print("   vs hitting the slow source system on every reload\n")
print("The DATA ARCHITECT (QSDA) builds the MODEL in the Data Load Editor (load script = Qlik's")
print("ETL). Qlik AUTO-ASSOCIATES tables by SAME-NAMED fields, so: ONE common field = clean")
print("association; TWO+ common fields = a SYNTHETIC KEY (a modeling ERROR to avoid by renaming).")
print("Also avoid circular LOOPS. QVD files enable fast, LAYERED loading (extract->transform->")
print("present). Clean associations + no synthetic keys/loops + QVD efficiency = the QSDA core.")
EOF
```

**Expected result:** A clean model associating Customers and Sales on the single `CustomerID`, versus a synthetic-key error when they also share `Region` (Qlik builds `$Syn1`), with the fix (rename/qualify), plus QVD layered loading for speed. The Data Architect lesson is that Qlik auto-associates tables by same-named fields, so one common field gives a clean association while multiple common fields create synthetic-key modeling errors to avoid, and QVD files enable a fast, layered load architecture — the QSDA core skills.

**Negative test:** Loading tables that share several field names without checking associations. Qlik silently builds synthetic keys that bloat the model and confuse analysis; the Data Architect deliberately manages field names for clean single-key associations and uses QVDs for efficient loading.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Data Architect role understood — designing, building, and validating the data model.
- [ ] The Data Load Editor and load script understood — Qlik's ETL for shaping the model.
- [ ] Associations and synthetic keys understood — clean single-key associations, avoiding synthetic keys and loops.
- [ ] QVD files and optimized loading understood — fast, layered, reusable data loading.
