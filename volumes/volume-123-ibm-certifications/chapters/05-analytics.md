# Chapter 05: Analytics Certifications

## Learning Objectives

- Map the analytics portfolio: Cognos Analytics, Planning Analytics, and Cloud Pak for Data.
- Understand each product's role — reporting, planning, and the unified data platform.
- Complete walkthrough labs on the analytics concepts these certifications test.

## The analytics portfolio

| Certification | Catalog code | Product |
|:---|:---|:---|
| Certified Cognos Analytics v12 Administrator - Professional | Cert-C9006600 | Cognos (BI/reporting) — admin |
| Certified Cognos Analytics v12 Analyst - Professional | Cert-C9007700 | Cognos — authoring/analysis |
| Certified Planning Analytics v2.1.x Analyst - Professional | Cert-C9008500 | Planning Analytics (TM1) |
| Certified Architect - Cloud Pak for Data V4.7 | Cert-C9006000 | Cloud Pak for Data — architecture |
| Certified Administrator - Cloud Pak for Data v4.6 | Cert-C9005300 | Cloud Pak for Data — administration |

Three products: **Cognos Analytics** (enterprise reporting and dashboards, with split Administrator and Analyst credentials), **Planning Analytics** (the TM1 engine for budgeting/forecasting), and **Cloud Pak for Data** (the containerized data-and-AI platform that hosts many of the other products, with Architect and Administrator credentials).

## Hands-On Lab

Walkthroughs model the concepts (dimensional data, reporting metadata, platform services) with free tools; the products themselves are commercial. **Cost:** none.

### Lab 5.1 — Dimensional thinking (Planning Analytics Analyst)

**Objective:** Build the cube model TM1/Planning Analytics is built on.

```python
python3 - <<'EOF'
# A minimal cube: measures by (region, month) — TM1's core structure
cube = {}
for region in ["North","South"]:
    for month in ["Jan","Feb"]:
        cube[(region,month)] = 0
cube[("North","Jan")] = 100; cube[("North","Feb")] = 120
cube[("South","Jan")] = 80;  cube[("South","Feb")] = 90
# a consolidation (rollup) across the region dimension:
for month in ["Jan","Feb"]:
    total = sum(cube[(r,month)] for r in ["North","South"])
    print(f"Total {month}: {total}")
EOF
```

**Expected result:** `Total Jan: 180`, `Total Feb: 210` — dimensions, cells, and consolidations are Planning Analytics' vocabulary; a rollup is a consolidation along a dimension. The exam tests dimensional modeling and rules, exactly this shape at scale.

**Negative test:** Add a region to the data but not to the consolidation logic — its numbers vanish from the total; membership drives rollups, a core planning concept.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Reporting metadata layer (Cognos Analyst)

**Objective:** Understand why Cognos reports sit on a modeled layer, not raw SQL.

```text
cognos> data module / framework model: friendly names, joins, calculations, security filters
cognos> report authored against the MODEL, not the database -> business users reuse governed metadata
```

**Expected result:** The reason for the metadata layer: authors build reports from governed business terms (not table joins), so definitions stay consistent and secured — the Analyst exam tests authoring against modules/packages; the Administrator exam tests the servers, security, and content store beneath them.

**Negative test:** Point every report at raw SQL — definitions diverge report to report; the modeled layer exists to prevent exactly that.

**Rollback:** None (design).

### Lab 5.3 — Cognos administration (Cognos Administrator)

**Objective:** Name the administrator's surfaces.

```text
cognos admin> content store (DB of reports/folders/schedules), dispatchers/services (report/batch/query),
              security namespaces (LDAP/SAML), capabilities and permissions, schedules and delivery
```

**Expected result:** The admin exam's map: content store, the dispatcher services, authentication namespaces, capability-based security, and scheduling — operating the platform rather than authoring on it.

**Negative test:** Confusing capabilities (what a user may *do*) with object permissions (what a user may *see*) — the exam separates them deliberately.

**Rollback:** None (design).

### Lab 5.4 — Cloud Pak for Data platform shape (CP4D Architect/Admin)

**Objective:** State what Cloud Pak for Data is and how its two credentials differ.

```text
cp4d> a containerized (OpenShift) data & AI platform: catalog/governance, data virtualization,
      Db2/Watson services as cartridges, Watson Studio for DS — one platform, many services
architect (V4.7)> sizing, topology, service selection, integration -> the design credential
administrator (v4.6)> install, users/roles, service lifecycle, monitoring -> the operate credential
```

**Expected result:** Cloud Pak for Data as the platform that unifies data services on OpenShift, with the **Architect** credential owning design and the **Administrator** credential owning operations — the same design/operate split seen across IBM's Cloud Pak certifications.

**Negative test:** Treating CP4D as a single product rather than a platform of services — the exams test service composition, not one feature set.

**Rollback:** None (design).

## Summary and Completion Checklist

- [ ] Cognos (Admin vs Analyst), Planning Analytics, and Cloud Pak for Data mapped.
- [ ] Dimensional/consolidation modeling drilled.
- [ ] Cognos metadata layer and admin surfaces understood.
- [ ] CP4D platform shape and the architect/administrator split internalized.
