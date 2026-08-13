# Chapter 04: Preparing and Curating Data

## Learning Objectives

- Combine data sets — concatenation and match-merge by key.
- Apply formats and informats to read and present values.
- Clean data — standardize, validate, and handle missing values.
- Understand data curation as the foundation of trustworthy analytics.

*Cert relevance: this is the Data Curation category and part of Advanced Programming — and a pillar of the Data Scientist path.*

## Combining data sets

Real analysis draws on **multiple data sets**, so combining them is essential:

- **Concatenation (stacking)** — append rows from several data sets with the same structure (this month's transactions + last month's) using a `SET` statement in a DATA step.
- **Match-merge (joining)** — combine data sets **side by side by a key** (customer demographics + customer orders on `customer_id`), using `MERGE` with a `BY` variable (data sorted first), or `PROC SQL` joins.

Match-merging is where care matters: the data must be **sorted by the key** (for DATA-step merge), keys must align, and you must decide how to handle **non-matches** (keep all, or only matches — like SQL inner vs outer joins). Getting merges right is a frequent exam topic and a common source of real-world errors. The lab merges two data sets by key.

## Formats and informats

SAS separates a value's **stored form** from its **displayed form**:

- **Informats** tell SAS how to **read** an input value (read `01/15/2026` as a date, `$1,200` as a number).
- **Formats** tell SAS how to **display** a stored value (show a date as `15JAN2026`, a number as currency, a code as a label).

Crucially, a **format changes the display, not the stored value** — a numeric date is stored as a number and formatted for humans. Custom formats (via `PROC FORMAT`) map codes to labels (1 → "Yes"). Mastering formats/informats is essential for reading messy input and producing readable output. The lab applies a format.

## Cleaning and validating

Trustworthy analysis needs **clean** data, and SAS's explicitness helps:

- **Standardize** — consistent case, trimmed text, canonical categories (`NY`/`New York` → one form) using functions (`UPCASE`, `STRIP`, `TRANWRD`).
- **Validate** — check values against rules (a valid date, an amount ≥ 0, a code in an allowed set) and flag or fix violations.
- **Missing values** — detect and handle them deliberately (impute, drop, or flag) rather than letting them silently distort results — SAS's explicit missing representation makes this tractable.

This **data curation** — combining, formatting, cleaning, validating — is unglamorous but decisive: models and reports are only as good as the data beneath them. The lab standardizes and validates. *(Data curation here parallels data quality in [Informatica (CLXV Ch 6)](../../volume-165-informatica-certifications/chapters/06-data-quality.md).)*

## Curation as the analytics foundation

SAS makes **Data Curation** its own certification category, and it is one of the credentials that composes into the **SAS Certified Data Scientist** ([Ch 8](08-data-scientist-and-administration.md)). That reflects a truth of analytics: **most of the work is preparing the data**, and a data scientist who cannot curate data cannot deliver reliable models. Combining, formatting, and cleaning are not preliminaries to the "real" work — they **are** much of the real work, and the foundation everything statistical and predictive rests on. The lab runs a full curation flow. The strength of the SAS language here is why it remains a trusted analytics platform.

## Hands-On Lab

Python models merging, formats, and cleaning/validation. **Cost:** none.

### Lab 4.1 — Merge, format, clean, and validate

**Objective:** Match-merge two data sets, apply a format, and standardize/validate.

```bash
python3 - <<'EOF'
# two data sets to MATCH-MERGE by key (customer_id)
demographics = {1:{"name":"acme corp","region_code":"E"}, 2:{"name":"globex","region_code":"W"}}
orders = [{"customer_id":1,"amount":"1,200","date":"20260115"},
          {"customer_id":2,"amount":"300",  "date":"20260220"},
          {"customer_id":3,"amount":"500",  "date":"bad"}]        # non-match + bad date

REGION_FMT = {"E":"East","W":"West"}   # custom format (PROC FORMAT: code -> label)
def informat_num(s):  return int(s.replace(",",""))              # read "1,200" -> 1200
def informat_date(s):                                            # read YYYYMMDD -> date or missing
    return s if len(s)==8 and s.isdigit() else "."               # SAS missing = .

print("MATCH-MERGE demographics + orders BY customer_id, format + clean:\n")
merged = []
for o in orders:
    demo = demographics.get(o["customer_id"])                    # match on key
    rec = {"customer_id": o["customer_id"]}
    rec["matched"] = demo is not None
    rec["name"] = demo["name"].title() if demo else "(no match)" # standardize case
    rec["region"] = REGION_FMT.get(demo["region_code"], "?") if demo else "?"   # apply format
    rec["amount"] = informat_num(o["amount"])                    # informat
    rec["date"] = informat_date(o["date"])                       # validate/missing
    merged.append(rec)
    print(f"   id={rec['customer_id']} matched={rec['matched']!s:5} {rec['name']:12} region={rec['region']:5} amount={rec['amount']:>5} date={rec['date']}")

# validate: flag issues
print("\nVALIDATION:")
for r in merged:
    issues = []
    if not r["matched"]: issues.append("no demographic match")
    if r["date"] == ".": issues.append("missing/invalid date")
    print(f"   id={r['customer_id']}: {'OK' if not issues else issues}")
print()
print("MATCH-MERGE joins demographics + orders BY customer_id (id 3 has no match). INFORMATS")
print("read '1,200'->1200 and validate the date (bad -> SAS missing '.'). A custom FORMAT maps")
print("region codes E/W -> East/West for display. Standardize (title-case name) and VALIDATE")
print("(flag non-match + bad date). This DATA CURATION is the foundation of trustworthy analytics.")
EOF
```

**Expected result:** Two data sets match-merged by customer_id (with one non-match), amounts read via an informat, a bad date flagged as SAS missing, region codes formatted to labels, names standardized, and validation flagging the issues. The lesson is data curation in SAS: combine data sets by key, use informats/formats to read and present values, and standardize/validate/handle-missing to produce clean data — the Data Curation competency and a pillar of the Data Scientist path.

**Negative test:** Merging without sorting by the key, or ignoring non-matches and bad dates. Rows misalign, unmatched records vanish silently, and invalid dates corrupt time analysis; sorted match-merge plus explicit validation and missing-value handling is what makes curated data trustworthy.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Combining data sets understood — concatenation (stack) and match-merge by key (join).
- [ ] Formats and informats understood — reading input and displaying values without changing storage.
- [ ] Cleaning and validation understood — standardize, validate, and handle missing values explicitly.
- [ ] Data curation placed — its own category, part of Advanced Programming, and a Data Scientist pillar.

## See also

- [Chapter 03 — SAS Programming Foundations](03-sas-programming-foundations.md) — the DATA step and PROCs curation builds on.
- [Chapter 05 — Statistical Analysis](05-statistical-analysis.md) — the modeling that curated data feeds.
- [Chapter 08 — The Data Scientist Path and Viya Administration](08-data-scientist-and-administration.md) — how curation composes into the Data Scientist credential.
