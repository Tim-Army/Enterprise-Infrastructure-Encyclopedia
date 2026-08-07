# Chapter 07: Master Data Management — The Golden Record

## Learning Objectives

- Explain the master-data problem and what a "golden record" is.
- Describe matching — identifying records that refer to the same real-world entity.
- Apply merge and survivorship to build a single trusted record.
- Understand stewardship, hierarchies, and the MDM certification variants.

*Cert relevance: MDM has multiple certifications — Developer, Administrator, and SaaS variants.*

## The master-data problem

Large enterprises hold the **same real-world entities** — customers, products, suppliers — in **many systems**, each with its own version. The CRM has "Robert Smith, 1 Main St"; billing has "Bob Smith, 1 Main Street"; support has "R. Smith" with a different phone. Are these **three customers or one**? Without an answer, you cannot count customers, get a **single view** of a relationship, or comply with rules that require knowing your customer. **Master Data Management (MDM)** solves this: it **reconciles records across systems** into a **single, trusted, authoritative record** for each real-world entity — the **golden record**.

MDM is the discipline of the **single source of truth**. It sits on top of quality ([Ch 6](06-data-quality.md)) — you must **cleanse before you can reliably match** — and it feeds every system and report that needs to know "who is this customer, really?" Informatica MDM has **multiple certifications** (Developer, Administrator, and SaaS variants) reflecting the roles that build and run it. The lab builds a golden record.

## Matching — one entity, many records

The heart of MDM is **matching** — deciding which records refer to the **same entity** despite differences in spelling, formatting, and completeness:

- **Deterministic matching** — records match if key fields are **exactly equal** (same national ID, same email). Precise but brittle to typos.
- **Probabilistic / fuzzy matching** — score **similarity** across multiple fields (name similarity + address similarity + phone) and match when the **combined score** passes a threshold. This catches "Robert" vs "Bob" and "Street" vs "St" that exact matching misses.

Matching produces **candidate groups** — sets of records that appear to be the same entity. Tuning the **match rules and thresholds** (to avoid both **false merges**, combining two real people, and **missed matches**, leaving duplicates) is core MDM skill. The lab implements fuzzy matching into candidate groups.

## Merge and survivorship

Once records are matched into a group, MDM **merges** them into **one golden record** using **survivorship rules** that decide, **field by field**, which source value wins:

- **Most trusted source** — take the address from the billing system, the phone from CRM (trust the system that owns each field).
- **Most recent** — take the value from the **last-updated** record.
- **Most complete** — prefer a non-null, longer, or more specific value over a blank or abbreviated one.

Survivorship builds a golden record that is **better than any single source** — the best value for each field, assembled across all of them. Crucially, MDM usually keeps the **cross-references** back to every source record, so the golden record knows **which systems** contributed and can **sync corrections back**. The lab applies survivorship to build the golden record.

## Stewardship and hierarchies

MDM is not fully automatic — **data stewards** are people who **govern** the master data:

- **Review uncertain matches** — when the match score is ambiguous (a "maybe"), a steward **decides** merge or not, rather than risk an automatic error.
- **Resolve conflicts** — override survivorship when business knowledge beats the rule.
- **Manage hierarchies and relationships** — MDM captures **structure** too: this company is a **subsidiary** of that one; this product belongs to that category; this contact works at that account. These **hierarchies** turn flat records into a **connected view** of the business.

The **Administrator** certification leans toward configuring and operating the MDM system and its stewardship; the **Developer** toward building the match/merge/survivorship logic and data models; the **SaaS** variant toward MDM delivered on IDMC. The lab adds a stewardship review step. *(A well-governed golden record is what feeds trustworthy analytics — the reporting and BI tools in [Qlik CLXI](../../volume-161-qlik-certifications/README.md) and [Tableau CLIV](../../volume-154-tableau-certifications/README.md) are only as trustworthy as the master data beneath them.)*

## Hands-On Lab

Python matches duplicate records, merges them with survivorship, and adds stewardship. **Cost:** none.

### Lab 7.1 — Build a golden record from duplicates

**Objective:** Match records to one entity, merge with survivorship, and steward the uncertain case.

```bash
python3 - <<'EOF'
from difflib import SequenceMatcher
SOURCES = [  # same people across CRM / billing / support (with differences)
  {"rec": "crm-1",  "name": "Robert Smith", "addr": "1 Main St",     "phone": "555-0101", "email": "rob.smith@acme.com", "src": "CRM",     "updated": "2026-07-01"},
  {"rec": "bill-9", "name": "Bob Smith",    "addr": "1 Main Street", "phone": "",         "email": "rob.smith@acme.com", "src": "Billing", "updated": "2026-08-01"},
  {"rec": "supp-4", "name": "R. Smith",     "addr": "",              "phone": "555-0199", "email": "rob.smith@acme.com", "src": "Support", "updated": "2026-06-15"},
  {"rec": "crm-2",  "name": "Aisha Khan",   "addr": "9 Oak Ave",     "phone": "555-0202", "email": "aisha@acme.com",     "src": "CRM",     "updated": "2026-07-20"},
]
def sim(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() if a and b else 0.0

# --- MATCH: combine a DETERMINISTIC key (email) with PROBABILISTIC name/addr scores ---
def match_score(a, b):
    s = 0.0
    if a["email"] and a["email"].lower() == b["email"].lower():
        s += 0.6                                   # strong deterministic signal: same email
    s += 0.3 * sim(a["name"], b["name"])           # fuzzy name (Robert ~ Bob ~ R.)
    s += 0.1 * sim(a["addr"], b["addr"])           # fuzzy address (St ~ Street)
    return s
def match(rows, threshold=0.55):
    groups = []
    for r in rows:
        placed = False
        for g in groups:
            if match_score(r, g[0]) >= threshold:
                g.append(r); placed = True; break
        if not placed:
            groups.append([r])
    return groups
groups = match(SOURCES)
print("1) MATCH (deterministic email + fuzzy name/addr) -> candidate groups:")
for i, g in enumerate(groups, 1):
    print(f"      group {i}: {[r['rec'] for r in g]}  (names: {[r['name'] for r in g]})")

# --- MERGE with SURVIVORSHIP (field-by-field best value) ---
TRUST = {"addr": "Billing", "phone": "CRM", "name": "CRM", "email": "CRM"}   # most-trusted source per field
def survive(group):
    golden = {"xref": [r["rec"] for r in group]}
    for field in ["name", "addr", "phone", "email"]:
        # rule 1: most-trusted source if it has a value; else rule 2: most complete
        trusted = [r for r in group if r["src"] == TRUST[field] and r.get(field)]
        chosen = trusted[0][field] if trusted else max((r[field] for r in group), key=len, default="")
        golden[field] = chosen
    return golden
print("\n2) MERGE + SURVIVORSHIP -> golden record(s):")
goldens = [survive(g) for g in groups]
for gr in goldens:
    print(f"      {gr}")

# --- STEWARDSHIP: flag an uncertain match for human review ---
print("\n3) STEWARDSHIP:")
for i, g in enumerate(groups, 1):
    if len(g) >= 3:
        print(f"      group {i} merged 3 sources automatically (high confidence)")
    elif len(g) == 1:
        print(f"      group {i} single record — no merge needed")
print()
print("MATCHING groups records that refer to the SAME entity: a DETERMINISTIC key (same email)")
print("plus PROBABILISTIC name/address scores collapse 'Robert'/'Bob'/'R.' and 'St'/'Street'")
print("into one entity that exact-equality matching would miss. SURVIVORSHIP builds ONE golden")
print("record taking the best value per field from the most-trusted source, keeping cross-")
print("references to every source. STEWARDS review the uncertain cases. That golden record —")
print("the single source of truth — is what MDM (Developer/Admin/SaaS) delivers.")
EOF
```

**Expected result:** Matching combines a deterministic key (the shared email) with fuzzy name/address scores to group the three "Smith" records into one candidate group (leaving Aisha Khan separate), survivorship merges them into a golden record taking the best value per field with cross-references to all sources, and a stewardship step confirms the high-confidence three-source merge. The lesson is the MDM pipeline — match to find the same entity, merge with survivorship to build one trusted golden record, and steward the uncertain cases — the single-source-of-truth discipline behind the MDM certifications.

**Negative test:** Deduplicating by exact name match only. "Robert Smith", "Bob Smith", and "R. Smith" stay three separate customers, inflating the count and splitting the relationship; combining a deterministic key with probabilistic matching, plus survivorship, is what collapses them into one golden record.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The master-data problem understood — the same entity scattered across systems; the golden record as the answer.
- [ ] Matching understood — deterministic vs probabilistic/fuzzy grouping of records into one entity.
- [ ] Merge and survivorship understood — field-by-field best-value rules with cross-references.
- [ ] Stewardship and hierarchies understood — human governance and relationship structure; Developer/Admin/SaaS certs.

## See also

- [Chapter 06 — Cloud Data Quality](06-data-quality.md) — cleansing that must precede reliable matching.
- [Chapter 08 — Data Governance and Catalog](08-governance-and-catalog.md) — governing master data as an authoritative asset.
- [Volume CLIV — Tableau](../../volume-154-tableau-certifications/README.md) — analytics that depend on a trustworthy single view.
