# Chapter 04: From PowerCenter to the Cloud

## Learning Objectives

- Describe PowerCenter, the legacy on-premises ETL flagship, and its core objects.
- Explain the on-premises architecture — repository, Integration Service, client tools.
- Understand the modernization path to Cloud Data Integration (CDI-PC / "PC to CDI").
- Recognize the PowerCenter certifications and the modernization Practitioner specialization.

*Cert relevance: PowerCenter has its own Developer and Administrator certifications, and the PC→CDI modernization is a Practitioner specialization.*

## The legacy flagship

**PowerCenter** is Informatica's **on-premises ETL** product — the engine that ran enterprise data warehouses for two decades and still does at many organizations. It is the **predecessor to Cloud Data Integration** ([Ch 3](03-cloud-data-integration.md)): the same core idea (**mappings** that move data from source to target through transformations) but installed and run **in your own data center** rather than as SaaS. PowerCenter is mature, powerful, and deeply embedded — which is exactly why **modernizing it to the cloud** is a major Informatica theme, and why the certification program covers **both** PowerCenter itself and the **migration** to CDI.

Understanding PowerCenter matters even in a cloud world: its **object model** (mappings, sessions, workflows) shaped CDI, and huge amounts of enterprise logic still live in PowerCenter mappings that teams are now moving. The lab models the PowerCenter object model.

## The PowerCenter object model

PowerCenter organizes work into a well-defined **object hierarchy**:

- **Mapping** — the **data-flow** design: sources → transformations → targets (the same concept CDI inherited). Mappings hold the transformation logic.
- **Session** — a **runnable instance** of a mapping: it binds the mapping to **actual connections** and runtime properties (like a CDI Mapping Task).
- **Workflow** — an **orchestration** of one or more sessions (and other tasks) with **order, conditions, and error handling** (like a CDI Taskflow).
- **Repository** — the **metadata store** where all mappings, sessions, and workflows are saved and versioned.

So the PowerCenter chain is **mapping → session → workflow**, stored in the **repository** — and you can see how directly this maps onto CDI's **mapping → task → taskflow**. That correspondence is what makes migration systematic. The lab models the object model and the CDI correspondence.

## The on-premises architecture

PowerCenter is a **client/server** system you install and operate:

- **Repository Service** — manages the **repository** database of metadata.
- **Integration Service** — the **engine** that actually **runs sessions/workflows**, reading sources and writing targets.
- **Client tools** — the thick-client **Designer** (build mappings), **Workflow Manager** (build and schedule workflows), **Workflow Monitor** (watch runs), and **Repository Manager** (manage the repository).
- **Administrator console** — configure services, security, and nodes.

You **run and patch all of this yourself** — servers, databases, upgrades, high availability. That operational burden is one of the main reasons organizations modernize to CDI, where the **control plane is SaaS** and only a lightweight **Secure Agent** runs on-premises ([Ch 2](02-idmc-platform.md)). The lab contrasts the two architectures.

## Modernizing to Cloud Data Integration

Informatica's modernization path is **CDI-PC** — **Cloud Data Integration for PowerCenter**, often called **"PC to CDI."** The goal is to move existing PowerCenter assets to IDMC **without rebuilding them by hand**:

- **Asset conversion** — tooling **converts PowerCenter mappings/sessions/workflows into CDI mappings/tasks/taskflows**, reusing the logic you already built.
- **Incremental migration** — you migrate in **waves**, running PowerCenter and CDI **side by side** during the transition rather than a risky big-bang cutover.
- **The payoff** — SaaS control plane, elastic cloud execution, no server fleet to patch, and access to the rest of IDMC (quality, catalog, MDM) on the same platform.

The certifications reflect this: **PowerCenter Developer and Administrator** validate the on-premises product; the **PC to CDI Modernization Implementation Practitioner** validates that you can **run the migration**. The lab models a migration inventory and conversion. *(Exam names are release-dated, e.g. "PowerCenter Cloud Edition, Feb 2024.")*

## Hands-On Lab

Python models the PowerCenter object model, the CDI correspondence, and a migration inventory. **Cost:** none.

### Lab 4.1 — Inventory and convert PowerCenter assets to CDI

**Objective:** Map PowerCenter objects to their CDI equivalents and plan a wave-based migration.

```bash
python3 - <<'EOF'
# PowerCenter object model -> CDI correspondence (this is why migration is systematic)
CORRESPONDENCE = {
  "PowerCenter Mapping":  "CDI Mapping",
  "PowerCenter Session":  "CDI Mapping Task",
  "PowerCenter Workflow": "CDI Taskflow",
  "PowerCenter Repository": "IDMC metadata fabric",
}
# an inventory of existing PowerCenter assets to modernize
INVENTORY = [
  {"asset": "wf_customer_load",   "type": "Workflow", "sessions": 3, "complexity": "medium", "wave": 1},
  {"asset": "wf_orders_nightly",  "type": "Workflow", "sessions": 5, "complexity": "high",   "wave": 2},
  {"asset": "m_dim_product",      "type": "Mapping",  "sessions": 0, "complexity": "low",    "wave": 1},
  {"asset": "wf_finance_close",   "type": "Workflow", "sessions": 8, "complexity": "high",   "wave": 3},
]
print("PC -> CDI OBJECT CORRESPONDENCE (why 'PC to CDI' can convert, not rebuild):\n")
for pc, cdi in CORRESPONDENCE.items():
    print(f"   {pc:24} -> {cdi}")
print()
print("MIGRATION INVENTORY (wave-based, run side-by-side during transition):")
waves = {}
for a in INVENTORY:
    waves.setdefault(a["wave"], []).append(a)
for w in sorted(waves):
    assets = waves[w]
    print(f"   Wave {w}: {len(assets)} asset(s)")
    for a in assets:
        print(f"      {a['asset']:20} {a['type']:9} complexity={a['complexity']}")
print()
print("PowerCenter's mapping/session/workflow model maps DIRECTLY onto CDI's")
print("mapping/task/taskflow model, so CDI-PC tooling CONVERTS assets rather than")
print("forcing a hand-rebuild. Migrate in WAVES (low-complexity first), running")
print("PowerCenter and CDI SIDE BY SIDE — no big-bang cutover. Running that migration")
print("is the PC to CDI Modernization Implementation Practitioner certification.")
EOF
```

**Expected result:** A correspondence table mapping PowerCenter mapping/session/workflow/repository onto CDI mapping/task/taskflow/metadata-fabric, plus a wave-based migration inventory grouping four assets into three waves by complexity. The lesson is that PowerCenter's object model maps directly onto CDI's, so "PC to CDI" tooling converts assets rather than rebuilding them, and migrations proceed in waves with the two platforms running side by side — the skill validated by the modernization Practitioner certification.

**Negative test:** A big-bang cutover — switching everything from PowerCenter to CDI in one weekend. High risk, no fallback, and no way to validate incrementally; wave-based migration with side-by-side running lets each wave be verified before the next.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] PowerCenter placed — the legacy on-premises ETL flagship and CDI's predecessor.
- [ ] The object model understood — mapping → session → workflow, stored in the repository.
- [ ] The on-premises architecture understood — Repository/Integration Services and thick-client tools you operate yourself.
- [ ] The modernization path understood — CDI-PC ("PC to CDI") converts assets in waves; a Practitioner specialization covers it.

## See also

- [Chapter 03 — Cloud Data Integration](03-cloud-data-integration.md) — the cloud successor PowerCenter migrates to.
- [Chapter 02 — IDMC](02-idmc-platform.md) — the SaaS control plane and Secure Agent that replace the server fleet.
- [Chapter 09 — Choosing Your Informatica Path](09-choosing-your-informatica-path.md) — where PowerCenter and modernization fit a career path.
