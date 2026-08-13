# Chapter 02: IDMC — The Intelligent Data Management Cloud

## Learning Objectives

- Describe IDMC as a single cloud platform of separately-licensed modules.
- Name the core data-management disciplines IDMC spans.
- Explain the shared foundation — one metadata fabric, one control plane, Secure Agents.
- Understand CLAIRE, the AI/ML metadata-intelligence engine, at a high level.

*Cert relevance: every module certification ([Ch 1](01-the-informatica-program.md)) sits inside IDMC; this chapter is the platform context they share.*

## One platform, many modules

**IDMC — the Intelligent Data Management Cloud** — is Informatica's unified **cloud data-management platform**. The key idea is **one platform, many modules**: a single environment, one login, one metadata fabric, and one processing foundation — but you **license the modules you need**. A team doing only cloud ETL licenses **Cloud Data Integration**; a team that also needs trustworthy data adds **Cloud Data Quality**; a team building a single customer view adds **MDM**; a team cataloging and governing everything adds **Cloud Data Governance & Catalog**. The modules are **separately licensed** but **integrated** — they share metadata and run on the same foundation, so quality rules can be applied inside integration mappings, and cataloged assets carry lineage across modules.

This modular design is why the certification program is organized by module ([Ch 1](01-the-informatica-program.md)): each module is a distinct product with its own developer/admin skills, yet they compose into one platform. The lab models the module catalog and licensing.

## The data-management disciplines

IDMC spans the **major data-management disciplines**, each a module (and a chapter in this volume):

- **Data integration** — moving and transforming data at scale, batch and bulk (**Cloud Data Integration**, [Ch 3](03-cloud-data-integration.md); the legacy engine is **PowerCenter**, [Ch 4](04-powercenter-to-cloud.md)).
- **Application / API integration** — connecting applications and services in **real time** (**Cloud Application Integration**, [Ch 5](05-cloud-application-integration.md)).
- **Data quality** — profiling, cleansing, and standardizing so data is **trustworthy** (**Cloud Data Quality**, [Ch 6](06-data-quality.md)).
- **Master data management** — reconciling records into a **single source of truth** (**MDM**, [Ch 7](07-master-data-management.md)).
- **Governance and catalog** — knowing **what data you have**, where it came from, and who owns it (**Cloud Data Governance & Catalog**, [Ch 8](08-governance-and-catalog.md)).

Together these turn **raw source data** into **integrated, trustworthy, governed, discoverable** data — the full life cycle. Each discipline is valuable alone; the platform's advantage is that they **share metadata and lineage**. The lab maps the disciplines.

## The shared foundation

Under the modules is a **shared foundation** that every module uses:

- **A metadata fabric** — one place where the platform records **what data exists, its structure, and its relationships**. Because all modules write to it, an asset discovered by the catalog can carry **lineage** into integration and quality.
- **A cloud control plane** — the SaaS layer where you design mappings, rules, and processes in the browser, schedule jobs, and monitor runs.
- **Secure Agents** — lightweight **runtime engines** you deploy near your data (in your cloud VPC or data center). The control plane orchestrates; the **Secure Agent does the actual data processing**, so sensitive data can be processed **close to where it lives** without shipping it all to the SaaS. This hybrid design — **design in the cloud, execute near the data** — is core to how IDMC runs at enterprise scale.

The lab models the control-plane/Secure-Agent split.

## CLAIRE — the AI engine

**CLAIRE** is Informatica's **AI/ML engine** — the "Intelligent" in Intelligent Data Management Cloud. CLAIRE works over the **metadata fabric**: because the platform holds metadata about all your data and how it is used, CLAIRE can make **recommendations and automate** data-management work — suggesting mappings and transformations, **discovering and classifying** sensitive data, recommending data-quality rules, matching records for MDM, and auto-tagging cataloged assets. The pattern is **metadata in, intelligence out**: the more the platform knows about your data (through the shared fabric), the more CLAIRE can automate. You will meet CLAIRE again in governance and cataloging ([Ch 8](08-governance-and-catalog.md)), where metadata intelligence is most visible. The lab notes CLAIRE's role. *(CLAIRE is a platform capability rather than a separate certification; the module certifications assume you understand where AI assists the work.)*

## Hands-On Lab

Python models IDMC — the module catalog, the disciplines, and the control-plane/Secure-Agent split. **Cost:** none.

### Lab 2.1 — Model the IDMC module catalog and licensing

**Objective:** See modules as separately-licensed but integrated, sharing one metadata fabric.

```bash
python3 - <<'EOF'
MODULES = {
  "Cloud Data Integration":        {"discipline": "batch/bulk ETL-ELT",        "chapter": 3},
  "Cloud Application Integration": {"discipline": "real-time / API / process",  "chapter": 5},
  "Cloud Data Quality":            {"discipline": "profile / cleanse / standardize", "chapter": 6},
  "Master Data Management":        {"discipline": "golden record / single view", "chapter": 7},
  "Cloud Data Governance & Catalog": {"discipline": "metadata / lineage / govern", "chapter": 8},
}
# a customer licenses a SUBSET; all licensed modules share ONE metadata fabric
licensed = ["Cloud Data Integration", "Cloud Data Quality", "Cloud Data Governance & Catalog"]

print("IDMC — ONE platform, MANY modules (license the ones you need):\n")
for m, d in MODULES.items():
    mark = "LICENSED" if m in licensed else "  --    "
    print(f"   [{mark}] {m:34} {d['discipline']:34} [Ch {d['chapter']}]")
print()
print(f"   This customer licensed {len(licensed)} of {len(MODULES)} modules.")
print("   All licensed modules share ONE metadata fabric, so:")
print("      - Data Quality rules apply INSIDE Data Integration mappings.")
print("      - Cataloged assets carry LINEAGE across integration + governance.")
print()
print("Separately LICENSED but INTEGRATED — that shared metadata fabric is what makes")
print("IDMC a platform rather than a bag of tools, and it's what CLAIRE (the AI engine)")
print("reasons over to automate data-management work.")
EOF
```

**Expected result:** A module catalog showing a customer licensing a subset (CDI, Data Quality, CDGC) of the modules, with all licensed modules sharing one metadata fabric so quality rules apply inside integration mappings and cataloged assets carry lineage across modules. The lesson is that IDMC is one platform of separately-licensed but integrated modules — the shared metadata fabric is what distinguishes a platform from a collection of tools, and it is what CLAIRE reasons over.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — The control plane and the Secure Agent

**Objective:** See the design-in-cloud / execute-near-data split.

```bash
python3 - <<'EOF'
# IDMC hybrid runtime: CLOUD control plane orchestrates; SECURE AGENT executes near the data
def run_job(job, data_location):
    print(f"   CONTROL PLANE (SaaS): design '{job['name']}', schedule, monitor")
    print(f"   -> dispatches to Secure Agent in '{data_location}'")
    print(f"   SECURE AGENT ({data_location}): reads source, runs transforms, writes target")
    print(f"      (sensitive data processed NEAR where it lives — not shipped to SaaS)")
    return {"job": job["name"], "executed_in": data_location, "rows": job["rows"]}

job = {"name": "load_customers_to_warehouse", "rows": 1_200_000}
print("IDMC RUNTIME — design in the cloud, execute near the data:\n")
result = run_job(job, "customer-vpc-us-east")
print(f"\n   result: {result}")
print()
print("The CONTROL PLANE is the browser SaaS where you build mappings/rules/processes,")
print("schedule, and monitor. The SECURE AGENT is a lightweight runtime you deploy in")
print("your own VPC/data center that does the ACTUAL data processing. Design once in the")
print("cloud; execute close to the data. This hybrid split is how IDMC runs at enterprise")
print("scale without shipping all your sensitive data to the SaaS.")
EOF
```

**Expected result:** A runtime model where the cloud control plane designs, schedules, and monitors a job while a Secure Agent deployed in the customer's own VPC does the actual data processing near the data. The lesson is IDMC's hybrid design — design in the cloud, execute near the data — which lets enterprises use a SaaS control plane while keeping sensitive data processing local.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] IDMC understood — one cloud platform of separately-licensed but integrated modules.
- [ ] The data-management disciplines named — integration, app integration, quality, MDM, governance/catalog.
- [ ] The shared foundation understood — metadata fabric, cloud control plane, Secure Agents.
- [ ] CLAIRE placed — the AI/ML engine that reasons over the metadata fabric to automate work.

## See also

- [Chapter 03 — Cloud Data Integration](03-cloud-data-integration.md) — the core ETL/ELT module.
- [Chapter 08 — Data Governance and Catalog](08-governance-and-catalog.md) — where the metadata fabric and CLAIRE are most visible.
- [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md) — a lakehouse IDMC integrates and governs.
