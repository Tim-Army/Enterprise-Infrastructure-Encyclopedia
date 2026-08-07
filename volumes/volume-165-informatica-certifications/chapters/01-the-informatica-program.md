# Chapter 01: The Informatica Certification Program

## Learning Objectives

- Describe Informatica as the enterprise data-management leader and where certification fits.
- Distinguish the two credential tiers — Certified Professional and Certified Practitioner.
- Understand the exam mechanics — 70% to pass, 90 minutes, release-dated, course-backed.
- Map the certifications to the IDMC modules and the legacy PowerCenter path.

*Cert relevance: this chapter frames the whole program — the tiers, mechanics, and module map that the rest of the volume develops.*

## Informatica and its certifications

**Informatica** is the enterprise **data-management** leader — the company whose tools **integrate**, **cleanse**, **govern**, **catalog**, and **master** data for large organizations. If a bank, retailer, or hospital needs data to move reliably from hundreds of source systems into a warehouse, be **trustworthy** when it arrives, and be **governed** and **discoverable** afterward, Informatica is one of the names that does it. Its cloud flagship is **IDMC — the Intelligent Data Management Cloud** ([Ch 2](02-idmc-platform.md)) — a single platform of separately-licensed modules, and its legacy on-premises flagship is **PowerCenter** ([Ch 4](04-powercenter-to-cloud.md)), the ETL engine that ran enterprise data warehouses for two decades.

Informatica certifications are **role- and product-based**: you certify on a **module** (Cloud Data Integration, Data Quality, MDM, and so on) at a level that matches what you do with it. The program validates that you can **build**, **administer**, or **implement** with a specific Informatica product at a specific release. Because the products are the ones large enterprises actually run their data on, the credentials map directly to real data-engineering and data-governance roles.

## Two credential tiers

Informatica structures its **Certified Professional Program** into **two tiers**:

- **Certified Professional** — the mainstream, **role-based** credential. A Professional exam validates **product knowledge and competency** on specific tasks — for example, the *Cloud Data Integration Developer, Professional* validates that you can build mappings and integration tasks in CDI. This is the tier most engineers pursue, and there is a Professional exam for each major module.
- **Certified Practitioner** — an **implementation-focused** credential aimed at **real customer-project deployment**, with a **two-year validity period**. Practitioners are people who **deliver** Informatica projects; the tier includes **modernization specializations** such as the *PC to CDI Modernization Implementation Practitioner Certification* for teams moving PowerCenter to the cloud.

Read the tiers as **know the product** (Professional) versus **deliver a project with it** (Practitioner). Most people start Professional; consultants and delivery specialists add Practitioner. The lab builds the tier map.

## Exam mechanics

Informatica **Professional** exams share a consistent shape:

- **Passing score: 70%.**
- **Duration: 90 minutes.**
- **Recommended prerequisite: the matching training course** — Instructor-Led or onDemand. For the CDI Professional, that is *Cloud Data Integration for Developers*; each module's Professional exam names its own course.
- **Release-dated.** Exams are **versioned to a platform release** (you will see names like "October 2024 Release" or "Feb 2024"). The credential tracks the **product version**, so recertifying on a newer release keeps the credential current with the platform.

The course-then-exam pattern matters: Informatica designs the certification around a specific training path, so the fastest route to a Professional credential is the vendor course that precedes it. The lab records the mechanics.

## The module map

Every certification maps to a **module** of the platform (or to legacy PowerCenter):

| Module | Certification focus |
| --- | --- |
| **Cloud Data Integration (CDI)** | Developer, Professional — ETL/ELT, mappings, transformations ([Ch 3](03-cloud-data-integration.md)) |
| **Cloud Application Integration (CAI)** | Developer, Professional — real-time / API / process integration ([Ch 5](05-cloud-application-integration.md)) |
| **Cloud Data Quality** | Professional — profiling, cleansing, standardization ([Ch 6](06-data-quality.md)) |
| **Master Data Management (MDM)** | Developer, Administrator, and SaaS variants — golden records ([Ch 7](07-master-data-management.md)) |
| **Cloud Data Governance & Catalog (CDGC)** | Professional — metadata, catalog, lineage, governance ([Ch 8](08-governance-and-catalog.md)) |
| **PowerCenter** | Data Integration Developer + Administrator (on-premises); CDI-PC for modernization ([Ch 4](04-powercenter-to-cloud.md)) |

Practitioner-level certifications exist for CDI, CAI, MDM, CDGC, and Cloud Data Quality, plus the PC→CDI modernization specialization. The rest of this volume takes each module in turn. The lab assembles the full map.

## Hands-On Lab

Python models the program: the tiers, the mechanics, and the module map. **Cost:** none.

### Lab 1.1 — Map the tiers and mechanics

**Objective:** Record the two tiers and the shared Professional exam mechanics.

```bash
python3 - <<'EOF'
TIERS = {
  "Certified Professional": {
    "focus": "role-based product knowledge and task competency",
    "audience": "engineers/developers/admins who BUILD and RUN the product",
    "validity": "tracks the product release (recertify on newer releases)",
  },
  "Certified Practitioner": {
    "focus": "implementation — delivering real customer projects",
    "audience": "consultants / delivery specialists who DEPLOY the product",
    "validity": "two-year validity period",
  },
}
MECHANICS = {"passing_score": "70%", "duration": "90 minutes",
             "prerequisite": "matching training course (ILT or onDemand)",
             "versioning": "release-dated (e.g. 'October 2024 Release')"}

print("INFORMATICA CERTIFIED PROFESSIONAL PROGRAM — two tiers:\n")
for tier, d in TIERS.items():
    print(f"   {tier}")
    for k, v in d.items():
        print(f"      {k:9}: {v}")
    print()
print("Professional exam mechanics (shared):")
for k, v in MECHANICS.items():
    print(f"   {k:14}: {v}")
print()
print("Read it as KNOW THE PRODUCT (Professional) vs DELIVER A PROJECT (Practitioner).")
print("Most engineers start Professional; consultants add Practitioner. Every exam is")
print("course-backed and release-dated — the vendor course is the fast path, and the")
print("credential tracks the platform version.")
EOF
```

**Expected result:** A two-tier map — Certified Professional (role-based product knowledge, for builders/admins) versus Certified Practitioner (implementation-focused, two-year validity, for project delivery) — plus the shared Professional mechanics: 70% to pass, 90 minutes, a matching course prerequisite, and release-dated versioning. The lesson is that Professional is the mainstream "know the product" credential and Practitioner is the "deliver the project" credential, and every exam is course-backed and tracks a platform release.

**Cleanup:** None.

### Lab 1.2 — Assemble the module-to-certification map

**Objective:** Map each IDMC module (and PowerCenter) to its certification focus.

```bash
python3 - <<'EOF'
MODULES = [
  ("Cloud Data Integration (CDI)",       "Developer, Professional",              "ETL/ELT mappings + transformations", "Ch 3"),
  ("Cloud Application Integration (CAI)", "Developer, Professional",              "real-time / API / process integration", "Ch 5"),
  ("Cloud Data Quality",                  "Professional",                         "profiling / cleansing / standardization", "Ch 6"),
  ("Master Data Management (MDM)",        "Developer / Administrator / SaaS",     "golden records / single source of truth", "Ch 7"),
  ("Cloud Data Governance & Catalog",     "Professional",                         "metadata / catalog / lineage / governance", "Ch 8"),
  ("PowerCenter (legacy on-prem)",        "Dev + Admin; CDI-PC modernization",    "on-prem ETL -> cloud modernization", "Ch 4"),
]
print("INFORMATICA CERTIFICATIONS -> MODULE MAP:\n")
print(f"   {'MODULE':38} {'CERTIFICATION':34} COVERS")
for mod, cert, covers, ch in MODULES:
    print(f"   {mod:38} {cert:34} {covers}  [{ch}]")
print()
print("Practitioner-level certs also exist for CDI, CAI, MDM, CDGC, and Data Quality,")
print("plus the 'PC to CDI Modernization Implementation Practitioner' specialization.")
print()
print("Each certification maps to a PLATFORM MODULE. Certify on the module you work with,")
print("at the level (Developer/Administrator, Professional/Practitioner) that matches your")
print("role. The rest of this volume takes each module in turn.")
EOF
```

**Expected result:** A module-to-certification table — CDI (Developer Professional), CAI (Developer Professional), Cloud Data Quality (Professional), MDM (Developer/Administrator/SaaS), CDGC (Professional), and PowerCenter (Dev + Admin, with CDI-PC for modernization) — each pointing at the chapter that develops it. The lesson is that Informatica certifications are organized by platform module, and you certify on the module you use at the level that matches your role.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Informatica placed — the enterprise data-management leader (IDMC in the cloud, PowerCenter on-prem).
- [ ] The two tiers understood — Certified Professional (role-based product knowledge) and Certified Practitioner (implementation, two-year validity).
- [ ] Exam mechanics recorded — 70% to pass, 90 minutes, course-backed, release-dated.
- [ ] The module map read — each certification maps to an IDMC module (or PowerCenter), developed chapter by chapter.

## See also

- [Volume XLIX — Snowflake](../../volume-049-snowflake-certifications/README.md) — a cloud data platform Informatica loads and governs.
- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) — API/application integration, adjacent to Cloud Application Integration.
- [Chapter 02 — IDMC, the Intelligent Data Management Cloud](02-idmc-platform.md).
