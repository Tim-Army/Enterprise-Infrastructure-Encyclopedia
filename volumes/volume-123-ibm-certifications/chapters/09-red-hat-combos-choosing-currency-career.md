# Chapter 09: Red Hat Combos, Choosing a Path, Currency, and Career

## Learning Objectives

- Understand the six "PLUS" combination certifications that bundle Red Hat Certified Specialist exams.
- Choose an IBM certification path by portfolio and role.
- Keep certifications current: the "Retiring soon" list, versioned certifications, and the certification/badge/Coursera distinction.

## The Red Hat "PLUS" combinations

Six IBM certifications bundle a **Red Hat Certified Specialist** exam — you pass an IBM Cloud Pak exam **and** a Red Hat OpenShift exam to earn one credential. This reflects IBM's platform strategy: Cloud Paks run on OpenShift, so the combined credential validates both layers.

| Combination certification | Catalog code | Red Hat half |
|:---|:---|:---|
| Solution Architect - WebSphere Hybrid Edition V5.0 PLUS | Cert-C0006421 | OpenShift Administration |
| Administrator - Cloud Pak for Multicloud Management v2.2 PLUS | Cert-C0006621 | OpenShift Administration |
| Solution Architect - Cloud Pak for Multicloud Management v1.3 PLUS | Cert-C0007220 | OpenShift Administration |
| Administrator - Cloud Pak for Multicloud Management v1.3 PLUS | Cert-C0006620 | OpenShift Administration |
| Developer - Cloud Pak for Applications v4.1 PLUS | Cert-C0007320 | OpenShift Application Development |
| Solution Architect - Cloud Pak for Applications V4.1 PLUS | Cert-C0006420 | OpenShift Administration |
| Administrator - Cloud Pak for Security V1.10 PLUS | Cert-F1000100 | OpenShift Administration |

(Also note **Certified Advocate Plus - Cloud v1**, Cert-F1000300 — an advocacy-plus credential, distinct from the exam combinations.) Because the Red Hat half is a full separate exam, IBM's certification map connects directly to **Volume XIV (Red Hat Enterprise Linux)** and the forthcoming Red Hat certification-tracks coverage — plan both exams.

## Choosing a path

| If your work is… | Target portfolio | Start with |
|:---|:---|:---|
| AI/ML engineering | AI/watsonx ([Ch 02](02-ai-watsonx-and-quantum.md)) | Certified AI v1 - Associate, then watsonx role |
| Security operations | Security ([Ch 03](03-security.md)) | QRadar Associate → Analyst |
| Database administration | Data platforms ([Ch 04](04-data-platforms.md)) | Db2 (z/OS or LUW) DBA Associate |
| BI/reporting | Analytics ([Ch 05](05-analytics.md)) | Cognos Analyst |
| Integration engineering | Integration ([Ch 06](06-integration-and-messaging.md)) | MQ Administrator, ACE Developer |
| Platform/automation | Automation ([Ch 07](07-automation-observability-aiops.md)) | a Cloud Pak credential (+ OpenShift) |
| Mainframe/Power ops | Systems ([Ch 08](08-systems-and-asset-management.md)) | z/OS, AIX, or IBM i |
| EAM/facilities | Asset mgmt ([Ch 08](08-systems-and-asset-management.md)) | a Maximo v9 Associate module |

Associate credentials are the entry points; Professional credentials build on the product depth; the PLUS combos add the OpenShift platform layer.

## Currency

- **Watch the "Retiring soon" flags.** Five certifications are currently winding down: Datacap V9.1.8, DOORS Next v7.x, Engineering Test Management v7.x, watsonx Mainframe Modernization Architect v1, and Cloud Pak for Business Automation v21.0.3. Don't target a retiring credential.
- **Certifications are version-pinned.** QRadar V7.5, Db2 13, Maximo v9.1, CP4I v16.1.0 — versions advance and old exams retire. The live catalog is authoritative; a mirror is not.
- **Keep the three credential kinds straight** ([Ch 01](01-the-ibm-certification-program.md)): a Coursera "IBM Professional Certificate" and a TechXchange badge are valuable but are **not** the proctored certification. On a résumé, name which one you hold.
- **Records and recertification** live in IBM My Learning; badges on Credly. Recertification policy is per-credential — verify on the certification's page.

## Hands-On Lab

### Lab 9.1 — Build your IBM certification plan

**Objective:** Commit a portfolio-aligned plan.

```bash
cat > my-ibm-plan.md <<'EOF'
Role: ___                 Portfolio: AI / Security / Data / Analytics / Integration / Automation / Systems / Asset
Target cert 1: ___        Catalog code: Cert-___     Level: Associate/Professional
Exam (Pearson VUE): ___   Delivery: test center / OnVUE
PLUS combo? Red Hat exam needed: yes/no -> ___
Retiring-soon check done: yes    Verify catalog on: ___
EOF
cat my-ibm-plan.md
```

**Expected result:** A plan naming the exact catalog code and level, whether an OpenShift exam is bundled, and a retiring-soon check — the discipline this volume's structure encourages.

**Negative test:** A plan without the catalog code — the 62-item catalog has many similarly named version-pinned certifications; the code disambiguates.

**Rollback:** Keep the plan.

### Lab 9.2 — Verify the catalog is still current

**Objective:** Make the currency check routine.

```text
browser> ibm.com/training/search > Learning type: Certification
# count should be ~62; check your target is present and NOT flagged "Retiring soon"
# toggle "Show Retired/Withdrawn" to confirm your target hasn't already gone
```

**Expected result:** Confirmation your target certification is live and not retiring before you invest study time — a two-minute check against the authoritative catalog.

**Negative test:** Registering off a cached third-party list — version churn and retirements make that how people study for a withdrawn exam.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The six PLUS combinations and their Red Hat halves understood.
- [ ] A portfolio-aligned certification path chosen.
- [ ] Currency habits installed: retiring-soon flags, version pinning, credential-kind clarity.
