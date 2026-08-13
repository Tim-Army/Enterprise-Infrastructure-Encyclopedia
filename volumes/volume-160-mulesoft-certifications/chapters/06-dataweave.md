# Chapter 06: DataWeave — The Transformation Language

## Learning Objectives

- Explain DataWeave as MuleSoft's transformation language.
- Describe transforming data between formats (JSON, XML, CSV, Java).
- Understand mapping, filtering, and functional transformation.
- Recognize DataWeave as a distinctive, heavily-tested skill.

*Cert relevance: DataWeave is central to the Developer certifications and a distinctive MuleSoft skill.*

## What DataWeave is

**DataWeave** is MuleSoft's **functional transformation language** — the language used inside Mule applications to **transform data** from one shape and format to another. Integration is largely about **data transformation**: one system speaks JSON, another XML, a third a flat CSV or a Java object, and the integration must **map** between them. DataWeave is purpose-built for this: a concise, functional language that reads an input payload and produces an output in whatever format and structure is needed. It is **distinctive to MuleSoft** and **heavily tested** in the Developer certifications — proficiency in DataWeave is a core marker of a MuleSoft developer. The lab models a transformation.

## Transforming between formats

A defining DataWeave capability is **format independence**: the same transformation logic can read **JSON, XML, CSV, or Java** input and write **JSON, XML, CSV, or Java** output — you declare the **output format** (`output application/json`) and DataWeave handles the serialization. This means an integration can accept XML from a legacy SOAP service and emit JSON for a mobile app (or vice versa) with a single transformation, without manual parsing and serialization code. Format-agnostic transformation is exactly what integrations between heterogeneous systems need. The lab models format conversion.

## Mapping, filtering, and functional transformation

DataWeave is **functional** — transformations are expressions that map inputs to outputs, using operations like:

- **Mapping** — `map` over an array to reshape each element (e.g., rename fields, restructure objects).
- **Filtering** — `filter` to keep only elements meeting a condition.
- **Field mapping** — building the output object by selecting and renaming input fields.
- **Functions and operators** — `reduce`, `groupBy`, `orderBy`, string/date functions, and custom functions.

Because it is functional and declarative, a DataWeave script describes **what the output should be** rather than a step-by-step procedure — concise and composable. A single script can restructure, rename, filter, aggregate, and reformat in one expression. The lab models mapping and filtering.

## A distinctive, tested skill

DataWeave is a **differentiator**: it is specific to MuleSoft, powerful, and the part of the platform developers spend the most time in, so the Developer certifications test it heavily — reading a DataWeave script, predicting its output, and writing transformations. Investing in DataWeave fluency is investing in the core of MuleSoft development. (The concepts transfer, too: functional data transformation is a broadly useful skill.) The lab synthesizes.

## Hands-On Lab

Python models DataWeave-style transformation. **Cost:** none.

### Lab 6.1 — Map, filter, and reformat across formats

**Objective:** Model a DataWeave transformation (the logic, in Python).

```bash
python3 - <<'EOF'
# input: a list of customer records (imagine parsed from XML or a DB); transform -> JSON output
INPUT = [
    {"cust_id": 1, "first": "Ana",  "last": "Lee",   "spend": 1200, "active": True},
    {"cust_id": 2, "first": "Bo",   "last": "Ng",    "spend": 300,  "active": False},
    {"cust_id": 3, "first": "Cy",   "last": "Ortiz", "spend": 5000, "active": True},
]
# DataWeave-style transformation (functional: map + filter + field mapping), output = JSON
# %dw 2.0 / output application/json / payload filter (active) map { id:, name:, tier: }
def transform(payload):
    return [
        {
            "id":   c["cust_id"],                                  # field rename
            "name": c["first"] + " " + c["last"],                  # concat
            "tier": "gold" if c["spend"] >= 1000 else "standard",  # derived field
        }
        for c in payload
        if c["active"]                                             # filter: active only
    ]

import json
out = transform(INPUT)
print("DataWeave-style transformation (map + filter + field mapping):\n")
print("   INPUT (e.g. from XML/DB):")
for c in INPUT:
    print(f"      {c}")
print("\n   OUTPUT (output application/json):")
print(json.dumps(out, indent=6))
print("\nDataWeave is MuleSoft's FUNCTIONAL TRANSFORMATION language — the heart of integration,")
print("which is mostly about MAPPING data between shapes + formats. Here it: FILTERED to active")
print("customers, RENAMED fields (cust_id->id), CONCATENATED a name, and DERIVED a tier — in one")
print("declarative expression. FORMAT-INDEPENDENT: the same logic reads JSON/XML/CSV/Java and")
print("writes any of them (you declare 'output application/json'). It's DISTINCTIVE to MuleSoft")
print("and HEAVILY TESTED — reading a script + predicting output is core to the Developer certs.")
EOF
```

**Expected result:** An input list of customer records transformed — filtered to active customers, fields renamed (cust_id → id), a name concatenated, and a tier derived — producing clean JSON output in one declarative expression. The DataWeave lesson is that it is MuleSoft's functional transformation language for mapping data between shapes and formats (format-independent across JSON/XML/CSV/Java), and it is the distinctive, heavily-tested core of MuleSoft development.

**Negative test:** Writing manual parsing and serialization code per format to transform data. That is verbose and error-prone; DataWeave declares the output format and expresses map/filter/field-mapping in one concise functional script, which is why it is central to the platform and the exams.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] DataWeave understood as MuleSoft's functional transformation language.
- [ ] Transforming between formats (JSON, XML, CSV, Java) understood — format-independent output.
- [ ] Mapping, filtering, and functional transformation understood — declarative, composable expressions.
- [ ] DataWeave recognized as a distinctive, heavily-tested core MuleSoft skill.
