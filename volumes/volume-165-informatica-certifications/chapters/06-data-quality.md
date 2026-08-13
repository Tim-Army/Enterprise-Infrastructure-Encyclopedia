# Chapter 06: Cloud Data Quality — Trustworthy Data

## Learning Objectives

- Explain why data quality matters and what "trustworthy data" means.
- Describe profiling — discovering the actual state of your data.
- Apply cleansing and standardization rules.
- Understand validation, scorecards, and quality monitoring.

*Cert relevance: Cloud Data Quality is its own Professional certification; quality rules also apply inside CDI mappings.*

## Why data quality matters

Data that **moves** is not necessarily data you can **trust**. Real source data is full of problems: missing values, inconsistent formats (`NY` vs `New York` vs `new york`), invalid entries (a phone number in an email field), duplicates, and outdated records. Feed that into a warehouse or a decision and you get **wrong answers** — a marketing campaign to `null` addresses, a revenue report double-counting duplicate customers, a compliance failure from bad identifiers. **Cloud Data Quality** is the IDMC module that makes data **trustworthy**: it **measures** quality, **fixes** what it can, and **monitors** it over time.

Quality is not a one-time cleanup — it is a **continuous discipline**. And because IDMC shares one platform, quality rules built here can be **applied inside CDI mappings** ([Ch 3](03-cloud-data-integration.md)), so data is cleansed **as it moves**. The **Cloud Data Quality, Professional** certification validates this skill. The lab profiles, cleanses, and scores a dataset.

## Profiling — knowing your data

You cannot fix what you have not measured, so quality work starts with **profiling** — automatically **analyzing a dataset to discover its actual state**:

- **Completeness** — what fraction of values are populated (how many nulls/blanks)?
- **Uniqueness** — are there duplicates in a column that should be unique?
- **Validity / patterns** — do values match the expected **format** (email, phone, postal code)?
- **Value distribution** — what are the distinct values and their frequencies (revealing `NY`/`New York` inconsistencies)?

Profiling produces a **factual picture** of quality — often surprising, because problems hide until measured. It tells you **where to focus** cleansing effort. The lab profiles a dataset for completeness, validity, and distribution.

## Cleansing and standardization

Once you know the problems, **rules** fix them:

- **Standardization** — bring values to a **canonical form**: uppercase state codes, expand or abbreviate consistently (`NY` ↔ `New York`), trim whitespace, normalize case.
- **Cleansing** — **correct or remove** bad values: strip non-numeric characters from phone numbers, fill or flag missing required fields, reject impossible values.
- **Parsing** — split a combined field into parts (a full name into first/last; an address into street/city/postal).
- **Enrichment** — add missing information from reference data (derive a region from a postal code).

These rules are **reusable** — you define a "standardize US state" rule once and apply it wherever state data appears. Building a **library of quality rules** is the substance of data-quality work. The lab standardizes and cleanses.

## Validation, scorecards, and monitoring

Quality must be **measured and watched**, not assumed:

- **Validation rules** — assert conditions data **must** satisfy (email matches a pattern; amount ≥ 0; status is in an allowed set) and flag violations.
- **Scorecards** — roll validation results into **quality scores** per rule and overall, so you can **track quality as a number** (this dataset is 92% valid) and see it trend.
- **Monitoring** — run quality checks **continuously** so **degradation is caught early** — a new source system feeding bad data shows up as a falling score, not a downstream disaster.

This closes the loop: **profile → cleanse → validate → score → monitor**, repeat. Trustworthy data is data whose quality you can **prove and track**. The lab builds validation rules and a scorecard. *(Master Data Management ([Ch 7](07-master-data-management.md)) builds on quality — you must cleanse before you can reliably match and merge records.)*

## Hands-On Lab

Python profiles a dataset, applies cleansing/standardization rules, then validates and scores it. **Cost:** none.

### Lab 6.1 — Profile, cleanse, and score a dataset

**Objective:** Run the profile → cleanse → validate → score loop on messy data.

```bash
python3 - <<'EOF'
import re
RAW = [  # messy source data (missing, inconsistent, invalid)
  {"id": 1, "name": " Alice Chen ", "state": "NY",       "email": "alice@acme.com",  "amount": "120"},
  {"id": 2, "name": "bob jones",    "state": "New York",  "email": "bob@acme.com",    "amount": "80"},
  {"id": 3, "name": "CARLA DIAZ",   "state": "ca",        "email": "not-an-email",    "amount": "-5"},
  {"id": 4, "name": "",             "state": "CALIF",     "email": "dee@acme.com",    "amount": "200"},
]
# --- PROFILE: discover the actual state ---
def profile(rows):
    n = len(rows)
    complete_name = sum(1 for r in rows if r["name"].strip())
    valid_email   = sum(1 for r in rows if re.match(r"[^@]+@[^@]+\.[^@]+$", r["email"]))
    states        = {}
    for r in rows: states[r["state"]] = states.get(r["state"], 0) + 1
    return {"name_completeness": f"{complete_name}/{n}", "email_validity": f"{valid_email}/{n}",
            "state_distinct_values": states}
print("1) PROFILE (the actual state of the data):")
for k, v in profile(RAW).items(): print(f"      {k}: {v}")

# --- CLEANSE + STANDARDIZE (reusable rules) ---
STATE_STD = {"NY": "NY", "NEW YORK": "NY", "CA": "CA", "CALIF": "CA"}
def cleanse(r):
    return {"id": r["id"],
            "name": " ".join(w.capitalize() for w in r["name"].split()),   # standardize case + trim
            "state": STATE_STD.get(r["state"].strip().upper(), r["state"]), # standardize state
            "email": r["email"].strip().lower(),
            "amount": int(r["amount"])}
clean = [cleanse(r) for r in RAW]
print("\n2) CLEANSE + STANDARDIZE:")
for r in clean: print(f"      {r}")

# --- VALIDATE + SCORECARD ---
def valid_row(r):
    checks = {"name_present": bool(r["name"]),
              "email_valid": bool(re.match(r"[^@]+@[^@]+\.[^@]+$", r["email"])),
              "amount_nonneg": r["amount"] >= 0,
              "state_known": r["state"] in {"NY", "CA"}}
    return checks
print("\n3) VALIDATE + SCORECARD:")
total = passed = 0
for r in clean:
    checks = valid_row(r)
    for name, ok in checks.items():
        total += 1; passed += 1 if ok else 0
    fails = [k for k, ok in checks.items() if not ok]
    print(f"      id={r['id']}: {'OK' if not fails else 'FAIL '+str(fails)}")
print(f"\n   QUALITY SCORE: {passed}/{total} checks passed ({100*passed//total}%)")
print()
print("PROFILE reveals the mess (missing name, invalid email, inconsistent state). Reusable")
print("CLEANSE/STANDARDIZE rules fix case, trim, and canonicalize state. VALIDATE asserts")
print("what must be true; the SCORECARD turns quality into a trackable NUMBER. Profile ->")
print("cleanse -> validate -> score -> monitor is the Cloud Data Quality discipline.")
EOF
```

**Expected result:** A profile exposing incomplete names, an invalid email, and inconsistent state values; cleansing/standardization rules that fix case and canonicalize states; and a validation scorecard turning quality into a percentage. The lesson is the data-quality loop — profile to discover, cleanse/standardize to fix, validate and score to prove and track — the discipline behind the Cloud Data Quality Professional certification.

**Negative test:** Loading the raw data straight to the warehouse. Reports double-count `NY`/`New York`, mail bounces on the blank name and bad email, and a negative amount corrupts totals; profiling and quality rules catch these before they reach decisions.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The value of data quality understood — trustworthy data prevents wrong answers and compliance failures.
- [ ] Profiling understood — measuring completeness, uniqueness, validity, and distribution.
- [ ] Cleansing and standardization understood — reusable rules that canonicalize and correct.
- [ ] Validation, scorecards, and monitoring understood — proving and tracking quality over time.

## See also

- [Chapter 03 — Cloud Data Integration](03-cloud-data-integration.md) — where quality rules apply as data moves.
- [Chapter 07 — Master Data Management](07-master-data-management.md) — which depends on cleansed data to match reliably.
- [Chapter 08 — Data Governance and Catalog](08-governance-and-catalog.md) — where quality scores become governed, visible metadata.
