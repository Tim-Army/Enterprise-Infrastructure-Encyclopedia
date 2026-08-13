# Chapter 09: Choosing Your Informatica Path

## Learning Objectives

- Map roles (data engineer, integration developer, data-quality analyst, MDM developer, data steward) to certifications.
- Sequence certifications sensibly — start with CDI, then specialize.
- Decide between Professional and Practitioner tiers.
- Place Informatica in the wider data-platform ecosystem.

*Cert relevance: this chapter turns the module map ([Ch 1](01-the-informatica-program.md)) into a personal plan and ends with a capstone.*

## Match the credential to your role

Informatica certifications are **role- and module-based**, so start from **what you do**:

| Your role | Start here | Then consider |
| --- | --- | --- |
| **Data / ETL engineer** | Cloud Data Integration Developer, Professional ([Ch 3](03-cloud-data-integration.md)) | Data Quality; PowerCenter/CDI-PC if modernizing |
| **Integration / API developer** | Cloud Application Integration Developer, Professional ([Ch 5](05-cloud-application-integration.md)) | CDI for the batch side |
| **Data-quality analyst** | Cloud Data Quality, Professional ([Ch 6](06-data-quality.md)) | CDI to embed rules in mappings |
| **MDM developer** | MDM Developer ([Ch 7](07-master-data-management.md)) | MDM Administrator or SaaS variant |
| **Data governance lead / steward** | Cloud Data Governance & Catalog, Professional ([Ch 8](08-governance-and-catalog.md)) | MDM for master-data stewardship |
| **PowerCenter developer (modernizing)** | PowerCenter Developer ([Ch 4](04-powercenter-to-cloud.md)) | PC→CDI Modernization Practitioner |
| **Delivery consultant** | Professional in your module | the matching **Practitioner** credential |

The pattern: certify on the **module you work with**, at the **level** that matches your role, then broaden into adjacent modules on the shared platform. The lab builds a role-to-path planner.

## Sequence sensibly

A workable sequence for most people:

1. **Start with Cloud Data Integration.** It is the core module, the most widely held credential, and the foundation the others build on — even quality, MDM, and governance assume you understand how data moves.
2. **Add the module your role centers on** — quality, application integration, MDM, or governance/catalog.
3. **Broaden across the platform.** Because IDMC modules share the metadata fabric, a second module makes you far more effective (a CDI engineer who also knows Data Quality builds cleansing into pipelines; add CDGC and you understand lineage end to end).
4. **Add Practitioner** if you **deliver projects** — the Practitioner tier ([Ch 1](01-the-informatica-program.md)) validates implementation, and the PC→CDI specialization is valuable while enterprises modernize.

Each step is **course-backed** (the recommended training precedes each Professional exam) and **release-dated**, so plan to recertify as the platform advances. The lab sequences a plan.

## Professional or Practitioner

- **Certified Professional** — choose this if you **build and run** the product day to day. It is the mainstream credential and the right first target for engineers, developers, and administrators.
- **Certified Practitioner** — add this if you **implement Informatica for customers** (a partner or delivery consultant). It is implementation-focused, **valid two years**, and includes the **modernization** specialization. Practitioner **complements** Professional; it does not replace it.

Most careers are **Professional-first**, adding **Practitioner** when the job becomes about **delivering** rather than **building**. The lab records the tier decision.

## Informatica in the ecosystem

Informatica is the **data-management layer** that makes other platforms trustworthy. It **feeds and governs**:

- **Cloud data platforms** — [Snowflake (XLIX)](../../volume-049-snowflake-certifications/README.md), [Databricks (XLVIII)](../../volume-048-databricks-certifications/README.md), and [Cloudera (CLVIII)](../../volume-158-cloudera-certifications/README.md): Informatica integrates data into them and governs it.
- **Analytics and BI** — [Qlik (CLXI)](../../volume-161-qlik-certifications/README.md) and [Tableau (CLIV)](../../volume-154-tableau-certifications/README.md): dashboards are only as trustworthy as the integrated, quality-checked, mastered data beneath them.
- **Integration peers** — [MuleSoft (CLX)](../../volume-160-mulesoft-certifications/README.md) and Boomi (CLXVI): overlapping application/API integration, where Informatica's edge is doing it **inside** a full data-management platform.

Learning Informatica is learning the **plumbing and governance** of the enterprise data estate — the layer that turns scattered source data into integrated, trustworthy, governed, discoverable data for everything downstream. The capstone builds that end-to-end flow.

## Hands-On Lab

Python builds a role-to-path planner, then a capstone tracing data through every module. **Cost:** none.

### Lab 9.1 — Plan your Informatica path

**Objective:** Turn a role into a sequenced certification plan.

```bash
python3 - <<'EOF'
ROLE_PATHS = {
  "Data/ETL engineer":       ["CDI Developer Professional", "Cloud Data Quality Professional"],
  "Integration developer":   ["CAI Developer Professional", "CDI Developer Professional"],
  "Data-quality analyst":    ["Cloud Data Quality Professional", "CDI Developer Professional"],
  "MDM developer":           ["MDM Developer", "MDM Administrator"],
  "Governance lead":         ["CDGC Professional", "MDM Developer"],
  "Delivery consultant":     ["CDI Developer Professional", "PC->CDI Modernization Practitioner"],
}
def plan(role):
    steps = ROLE_PATHS[role]
    print(f"   ROLE: {role}")
    print(f"      1. START: {steps[0]}")
    for i, s in enumerate(steps[1:], 2):
        print(f"      {i}. THEN:  {s}")
    print(f"      note: each Professional exam is course-backed, 70% to pass, 90 min, release-dated")
print("INFORMATICA ROLE -> CERTIFICATION PATH:\n")
for role in ["Data/ETL engineer", "MDM developer", "Governance lead"]:
    plan(role); print()
print("Start with the module your role centers on (CDI for most), then broaden across the")
print("shared platform, and add a Practitioner credential if you DELIVER projects.")
EOF
```

**Expected result:** A planner turning roles into sequenced paths — e.g. a data engineer starts with CDI Developer Professional then adds Cloud Data Quality; a governance lead starts with CDGC Professional then MDM Developer. The lesson is to certify on your central module first (CDI for most), broaden across the shared platform, and add Practitioner when you deliver projects.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Capstone: data through every module

**Objective:** Trace one dataset through integration, quality, MDM, and governance — the whole platform.

```bash
python3 - <<'EOF'
# CAPSTONE: raw source data -> the full IDMC life cycle -> trustworthy governed data
raw = [
  {"id": "a", "name": "Robert Smith", "email": "rob@acme.com",  "state": "NY"},
  {"id": "b", "name": "Bob Smith",    "email": "rob@acme.com",  "state": "New York"},
  {"id": "c", "name": "Aisha Khan",   "email": "aisha@acme.com","state": "ca"},
]
log = []
# 1) CDI (integration): ingest source rows
staged = list(raw); log.append(f"CDI: ingested {len(staged)} source rows")
# 2) Cloud Data Quality: standardize state, validate email
STATE = {"NY":"NY","NEW YORK":"NY","CA":"CA"}
import re
for r in staged:
    r["state"] = STATE.get(r["state"].upper(), r["state"])
    r["email_valid"] = bool(re.match(r"[^@]+@[^@]+\.[^@]+$", r["email"]))
score = sum(r["email_valid"] for r in staged)/len(staged)
log.append(f"DQ: standardized state, validated email (quality={score:.2f})")
# 3) MDM: match on email -> golden records with survivorship (longest name wins)
groups = {}
for r in staged: groups.setdefault(r["email"], []).append(r)
golden = []
for email, recs in groups.items():
    golden.append({"email": email,
                   "name": max((x["name"] for x in recs), key=len),
                   "state": recs[0]["state"], "xref": [x["id"] for x in recs]})
log.append(f"MDM: matched {len(staged)} rows -> {len(golden)} golden records")
# 4) CDGC (governance): catalog + classify PII + lineage
pii = [c for c in ["name","email"] ]
log.append(f"CDGC: cataloged golden records, classified PII={pii}, captured lineage raw->golden")

print("CAPSTONE — one dataset through the WHOLE IDMC platform:\n")
for step in log: print(f"   {step}")
print("\n   GOLDEN RECORDS (trustworthy, governed):")
for g in golden: print(f"      {g}")
print()
print("Raw scattered source data (3 rows, 2 are the same person, messy state) becomes")
print("INTEGRATED (CDI), TRUSTWORTHY (Data Quality), MASTERED (MDM: 2 golden records), and")
print("GOVERNED (CDGC: cataloged, PII-classified, lineage-traced). That end-to-end life")
print("cycle — on one platform, over one metadata fabric — is what Informatica delivers, and")
print("what this volume's certifications, module by module, prepare you to build.")
EOF
```

**Expected result:** A capstone tracing three raw rows through CDI (ingest), Cloud Data Quality (standardize/validate), MDM (match to two golden records), and CDGC (catalog, classify PII, lineage) — ending with governed golden records. The lesson synthesizes the volume: Informatica turns scattered source data into integrated, trustworthy, mastered, governed data on one platform over one metadata fabric, and the module certifications each prepare you to build one stage of that life cycle.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Roles mapped to certifications — engineer, integration developer, quality analyst, MDM developer, steward.
- [ ] A sensible sequence chosen — start with CDI, add your central module, broaden across the platform.
- [ ] The tier decision made — Professional to build, Practitioner to deliver.
- [ ] Informatica placed in the ecosystem — the integration/quality/MDM/governance layer beneath data platforms and BI.

## See also

- [Chapter 01 — The Informatica Certification Program](01-the-informatica-program.md) — the tiers and module map this plan draws on.
- [Volume XLIX — Snowflake](../../volume-049-snowflake-certifications/README.md) and [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md) — platforms Informatica feeds and governs.
- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) — an integration peer in the same problem space.
