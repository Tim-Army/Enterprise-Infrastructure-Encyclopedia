# Chapter 06: Data Hub — Master Data Management

## Learning Objectives

- Explain Boomi Data Hub and the master-data problem it solves.
- Describe models (domains), sources, and the golden record.
- Apply match rules to deduplicate contributed records.
- Understand contribute-and-publish synchronization and the Data Hub certifications.

*Cert relevance: this is the Associate Data Hub and Professional Data Hub Developer track.*

## The master-data problem

The same **customers, products, and suppliers** live in **many systems** across an enterprise, each with its own slightly different version — and integrations ([Ch 4](04-building-integrations.md)) that sync them all can spread **inconsistencies** everywhere. **Boomi Data Hub** is Boomi's **master data management (MDM)** service: a **central hub** that holds the **authoritative, golden version** of each entity and keeps every connected system **consistent** with it. Instead of every system having its own conflicting "customer," Data Hub maintains **one golden record** and synchronizes it out.

Data Hub complements integration: processes **contribute** data into the hub and **consume** the golden records back out. The **Associate Data Hub** and **Professional Data Hub Developer** certifications validate building and running it. This is the same discipline as [Informatica MDM (Vol CLXV Ch 7)](../../volume-165-informatica-certifications/chapters/07-master-data-management.md), framed through Boomi's model. The lab builds a golden record in a hub. *(The overlap is real — both do MDM; the difference is Data Hub is one service inside the Boomi iPaaS, tightly coupled to Boomi integration.)*

## Models, sources, and golden records

Data Hub is organized around three concepts:

- **Model (domain)** — the **definition of an entity** you want to master: its fields and structure (a "Customer" model with name, email, address, and match/validation rules). The model is the schema of the golden records.
- **Sources** — the **systems that contribute** data to the model (CRM, billing, e-commerce). Each source **contributes records**, and Data Hub reconciles them.
- **Golden record** — the **single trusted version** of an entity that Data Hub builds by **matching and merging** contributed records. The hub stores golden records and their **links back to each source**.

So you **define a model**, connect **sources** that contribute to it, and Data Hub produces **golden records**. The lab defines a model and contributes source records.

## Match rules

The heart of Data Hub is **matching** — deciding which contributed records refer to the **same entity** so they merge instead of duplicating:

- **Match rules** compare incoming records to existing golden records on chosen fields (email exact, name fuzzy, address similarity) and decide **match** (update the existing golden record), **no match** (create a new one), or **needs review** (ambiguous — send to a steward).
- Well-tuned rules avoid **false merges** (combining two real entities) and **missed matches** (leaving duplicates).
- **Data quality** steps — standardization and validation — run so records are **clean before matching**, because dirty data matches badly (the same idea as [data quality in Informatica (Vol CLXV Ch 6)](../../volume-165-informatica-certifications/chapters/06-data-quality.md)).

Matching is what turns a pile of contributed records into a **deduplicated** set of golden records. The lab applies match rules to contributed records.

## Contribute and publish

Data Hub keeps systems consistent through a **contribute-and-publish** cycle:

- **Contribute** — a source system **sends its records** to the hub (usually via a Boomi integration process). The hub matches and **updates the golden records**.
- **Publish** — the hub **sends updated golden records back** to the connected systems, so a correction made once propagates **everywhere**. If billing fixes a customer's address, the golden record updates and all other systems receive the corrected value.
- **Stewardship** — data stewards review the **needs-review** matches and resolve conflicts the rules cannot.

This **two-way sync around a golden master** is what makes the whole enterprise consistent: fix data once, and the hub distributes the truth. The certifications — **Associate** (foundational modeling and contribution) and **Professional Data Hub Developer** (advanced matching, quality, and sync) — validate building this. The lab runs contribute → match → golden → publish.

## Hands-On Lab

Python builds a Data Hub model, contributes source records, matches to golden records, and publishes. **Cost:** none.

### Lab 6.1 — Master data in a hub

**Objective:** Contribute records from sources, match to golden records, and publish back.

```bash
python3 - <<'EOF'
from difflib import SequenceMatcher
# MODEL (domain): Customer — match on email (exact) OR strong name+... similarity
CONTRIBUTED = [  # records contributed by SOURCES into the hub
  {"src": "CRM",     "name": "Robert Smith", "email": "rob@acme.com",   "addr": "1 Main St"},
  {"src": "Billing", "name": "Bob Smith",    "email": "rob@acme.com",   "addr": "1 Main Street"},
  {"src": "Ecomm",   "name": "Aisha Khan",   "email": "aisha@acme.com", "addr": "9 Oak Ave"},
  {"src": "Support", "name": "A. Khan",      "email": "aisha@acme.com", "addr": ""},
]
def sim(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() if a and b else 0.0

golden = []   # the hub's golden records
def match_rule(rec, g):
    if rec["email"] and rec["email"].lower() == g["email"].lower():
        return "match"                                  # deterministic: same email
    if 0.6*sim(rec["name"], g["name"]) + 0.4*sim(rec["addr"], g["addr"]) >= 0.7:
        return "match"                                  # probabilistic
    return "no_match"

print("BOOMI DATA HUB — contribute -> match -> golden -> publish:\n")
print("1) CONTRIBUTE + MATCH:")
for rec in CONTRIBUTED:
    hit = next((g for g in golden if match_rule(rec, g) == "match"), None)
    if hit:
        hit["sources"].append(rec["src"])
        # survivorship: keep most-complete address, longest name
        if len(rec["addr"]) > len(hit["addr"]): hit["addr"] = rec["addr"]
        if len(rec["name"]) > len(hit["name"]): hit["name"] = rec["name"]
        print(f"      {rec['src']:8} {rec['name']:14} -> MATCH golden #{golden.index(hit)+1}")
    else:
        golden.append({"name": rec["name"], "email": rec["email"], "addr": rec["addr"], "sources": [rec["src"]]})
        print(f"      {rec['src']:8} {rec['name']:14} -> NEW golden #{len(golden)}")

print(f"\n2) GOLDEN RECORDS ({len(golden)} from {len(CONTRIBUTED)} contributed):")
for i, g in enumerate(golden, 1):
    print(f"      #{i} {g['name']:14} {g['email']:16} {g['addr']:14} sources={g['sources']}")

print("\n3) PUBLISH (send golden records back to all connected systems):")
for g in golden:
    print(f"      publish '{g['name']}' -> {sorted(set(['CRM','Billing','Ecomm','Support']))}")
print()
print("SOURCES CONTRIBUTE records; MATCH RULES (email exact OR name+addr similarity) collapse")
print("duplicates ('Robert'/'Bob', 'Aisha'/'A. Khan') into GOLDEN records with survivorship;")
print("the hub PUBLISHES the golden version back to every system, so a fix made once propagates")
print("everywhere. Modeling, matching, and sync is the Associate/Professional Data Hub cert.")
EOF
```

**Expected result:** Four contributed records from four sources collapse into two golden records (the two Smiths match on email, the two Khans match on email), with survivorship keeping the most complete values, then the hub publishes each golden record back to all systems. The lesson is Data Hub's model: sources contribute, match rules deduplicate into golden records, and publish synchronizes the truth back out — keeping the enterprise consistent, the discipline of the Data Hub certifications.

**Negative test:** Letting each system keep its own customer copy and syncing them peer-to-peer. Conflicting edits spread and no version is authoritative; a central hub with match rules and contribute-and-publish gives one golden record that all systems stay consistent with.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The master-data problem understood — the same entity scattered and inconsistent across systems.
- [ ] Models, sources, and golden records understood — the domain schema, contributors, and the trusted version.
- [ ] Match rules understood — deterministic and probabilistic matching into deduplicated golden records.
- [ ] Contribute-and-publish understood — two-way sync around a golden master; Associate and Professional certs.

## See also

- [Chapter 04 — Building Integrations](04-building-integrations.md) — the processes that contribute to and consume from the hub.
- [Volume CLXV — Informatica MDM](../../volume-165-informatica-certifications/chapters/07-master-data-management.md) — the same MDM discipline on a data-management platform.
- [Chapter 07 — B2B/EDI and Flow](07-b2b-edi-and-flow.md) — partner data exchange and low-code apps.
