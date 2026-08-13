# Chapter 04: Building Integrations

## Learning Objectives

- Describe a Boomi integration process — the visual data flow.
- Recognize the core shapes — Connector, Map, Decision, Branch, and more.
- Explain connectors, profiles, and maps.
- Understand the Integration Developer certifications and what they validate.

*Cert relevance: this is the Associate and Professional Integration Developer track — the flagship Boomi certification.*

## The process

An **integration process** is the heart of Boomi — a **visual flow** that moves and transforms data from a **source** to a **target**. You build it on a canvas by placing **shapes** and connecting them with lines, left to right:

```text
[Start/Connector]  ->  [Map]  ->  [Decision]  ->  [Connector]
   read source        transform     branch        write target
```

Data enters as **documents** (records — an order, a customer), flows through each shape in order, and lands in the target system. A process is **declarative and visual**: you describe the flow with shapes, and the **Atom** ([Ch 3](03-atoms-molecules-atom-clouds.md)) executes it. The **Integration Developer** certifications validate that you can build these processes correctly and efficiently — it is the flagship Boomi track. The lab builds a process from shapes.

## The core shapes

A handful of **shapes** cover most integration logic:

- **Connector (Start / operation)** — read from or write to a system (Salesforce, database, HTTP, disk). The Start shape usually reads the inbound data.
- **Map** — **transform** one data shape into another: map source fields to target fields, apply functions (concatenate, format, look up).
- **Decision** — **branch** on a condition (if amount > 1000, take the true path; else the false path).
- **Branch** — split the flow so the **same documents** go down **multiple paths** in parallel.
- **Route** — send documents down **different paths** by a value (route by country, by type).
- **Data Process / Business Rules / Cleanse** — scripting, validation, and cleansing steps.
- **Try/Catch** — catch errors and handle them (retry, notify, route to an error path).
- **Stop / Return Documents** — end the flow or return results.

Learning **which shape solves which problem** and sequencing them is the substance of integration development. The lab wires Connector → Map → Decision → Connector with a Try/Catch.

## Connectors, profiles, and maps

Three concepts make transformation work:

- **Connectors** provide **pre-built connectivity** to hundreds of applications and technologies. A **connection** holds the endpoint and credentials; an **operation** defines the action (query, create, update) and the data it exchanges. You **configure** a connector rather than code a client — this is a big part of Boomi's speed.
- **Profiles** describe the **structure** of data — the shape of a source record and of a target record (XML, JSON, database, flat file, EDI). Profiles are how Boomi knows the fields on each side.
- **Maps** connect a **source profile** to a **target profile** field by field, with **functions** in between for transformation. The map is where "the source's `cust_name` becomes the target's `CustomerName`, upper-cased" is defined.

Together: connectors get data in and out, profiles define its structure, and maps transform between structures. The lab uses a source profile, a map, and a target profile.

## The Integration Developer certifications

The Integration Developer track has two levels:

- **Associate Integration Developer** — validates **foundational** process-building: shapes, connectors, simple maps, and running a process. Preceded by *Integration Essentials* and the *Associate Integration Developer* course.
- **Professional Integration Developer** — validates **advanced** development: complex maps and functions, error handling, performance, reuse, and more sophisticated flows. The deeper credential.

Both are **open-book and open-platform** ([Ch 1](01-the-boomi-program.md)) — you build and reason **on the canvas**. This is the most widely pursued Boomi track because building integrations is what most Boomi developers do. The lab runs a complete process end to end.

## Hands-On Lab

Python simulates a Boomi integration process — shapes, a map with a profile, and a Try/Catch. **Cost:** none.

### Lab 4.1 — Build and run an integration process

**Objective:** Wire Connector → Map → Decision → Connector with error handling.

```bash
python3 - <<'EOF'
# a Boomi PROCESS is an ordered flow of SHAPES over DOCUMENTS (records)
SOURCE_DOCS = [  # inbound documents read by the Start connector (source profile)
  {"cust_name": "acme corp",   "order_amt": "1500", "country": "US"},
  {"cust_name": "globex",      "order_amt": "80",   "country": "DE"},
  {"cust_name": "initech",     "order_amt": "bad",  "country": "US"},   # will error in Map
]
# --- MAP shape: source profile -> target profile, with functions ---
def shape_map(doc):
    return {"CustomerName": doc["cust_name"].upper(),            # function: upper-case
            "Amount": int(doc["order_amt"]),                     # type convert (may raise)
            "Region": {"US": "Americas", "DE": "EMEA"}.get(doc["country"], "Other")}
# --- DECISION shape: branch on a condition ---
def shape_decision(doc):
    return "priority" if doc["Amount"] >= 1000 else "standard"

processed, errors = [], []
print("PROCESS: Start(Connector) -> Map -> Decision -> Connector, with Try/Catch\n")
for i, doc in enumerate(SOURCE_DOCS, 1):
    print(f"   doc {i}: {doc}")
    try:                                    # TRY/CATCH shape
        mapped = shape_map(doc)             # MAP shape
        path = shape_decision(mapped)       # DECISION shape
        mapped["_path"] = path
        processed.append(mapped)            # CONNECTOR (write target)
        print(f"      -> mapped {mapped} -> route '{path}'")
    except Exception as e:
        errors.append({"doc": doc, "error": str(e)})
        print(f"      -> CATCH: error ({e}) -> error path")
print()
print(f"   TARGET writes ({len(processed)}):")
for p in processed:
    print(f"      {p['CustomerName']:12} {p['Amount']:>5}  {p['Region']:9} [{p['_path']}]")
print(f"   ERROR path ({len(errors)}): {[e['doc']['cust_name'] for e in errors]}")
print()
print("A PROCESS flows DOCUMENTS through SHAPES: a Connector reads the source (source PROFILE),")
print("a MAP transforms to the target profile with functions (upper-case, type-convert, lookup),")
print("a DECISION branches (priority vs standard), and a Connector writes the target. TRY/CATCH")
print("routes the bad record to an error path instead of failing the whole run. Building this on")
print("the canvas is the Associate/Professional Integration Developer certification.")
EOF
```

**Expected result:** A process that reads three documents, maps each (upper-casing the name, converting the amount, deriving a region), branches priority vs standard on the amount, and routes the record with a non-numeric amount to an error path via Try/Catch — writing two good records and catching one error. The lesson is the Boomi process model: documents flow through shapes (Connector, Map, Decision, Try/Catch), with profiles defining structure and maps transforming between them — the core skill of the Integration Developer certifications.

**Negative test:** Omitting the Try/Catch shape. The non-numeric amount throws and aborts the entire process, losing the two valid records; error handling with Try/Catch is what makes a production integration resilient to bad documents.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The process understood — a visual, left-to-right flow of documents through shapes.
- [ ] The core shapes recognized — Connector, Map, Decision, Branch, Route, Try/Catch, and more.
- [ ] Connectors, profiles, and maps understood — connectivity, data structure, and transformation.
- [ ] The Integration Developer certifications placed — Associate (foundational) and Professional (advanced).

## See also

- [Chapter 03 — Atoms, Molecules, and Atom Clouds](03-atoms-molecules-atom-clouds.md) — the runtime that executes processes.
- [Chapter 05 — API Management](05-api-management.md) — publishing a process as an API.
- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) — the same integration problem, a different platform.
