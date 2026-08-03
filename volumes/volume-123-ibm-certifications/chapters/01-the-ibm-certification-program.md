# Chapter 01: The IBM Certification Program

![IBM certification program: 62 current certifications across seven portfolios — AI/watsonx and quantum, security, data platforms, analytics, integration and messaging, automation/observability, and systems/asset management — at Associate, Professional, and Specialty levels, delivered by Pearson VUE (test center or OnVUE online), with badges on Credly. Six "PLUS" combination certifications bundle Red Hat Certified Specialist exams, and five credentials are flagged Retiring soon.](../../../diagrams/volume-123-ibm-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The IBM Professional Certification Program: 62 current credentials in one catalog, spanning watsonx to z/OS — and three different things called "IBM credentials" (proctored certifications, TechXchange badges, Coursera certificates) that this chapter teaches you to tell apart.*

## Learning Objectives

- Describe the IBM Professional Certification Program: 62 current certifications, levels, and portfolios.
- Distinguish the three credential kinds: proctored **certifications**, **TechXchange badges**, and Coursera **Professional Certificates**.
- Know the exam logistics: Pearson VUE / OnVUE delivery, Credly badges, and the "Retiring soon" catalog flags.
- Navigate the authoritative catalog and verify a certification before targeting it.

## Three things called "IBM credentials"

IBM's credential landscape has three distinct kinds, routinely confused:

| Kind | What it is | Where |
|:---|:---|:---|
| **Professional Certifications** | Proctored exams validating product/role skill — the subject of this volume | ibm.com/training/credentials; exams at Pearson VUE |
| **TechXchange badges** | Training badges (courses/labs), advocacy badges (community contribution), event badges | IBM Training badge program; Credly |
| **Coursera "IBM Professional Certificates"** | Course-completion certificates (Data Science, Full Stack, etc.) — training, not proctored certification | Coursera |

A résumé line "IBM Certified …" should mean the first kind. The 10M+ badges IBM has issued are overwhelmingly the second and third — valuable learning, but not the proctored credential this volume maps.

## The program shape

The catalog (verified 3 August 2026 on the IBM Training credentials search) lists **62 current certifications**, with:

- **Levels:** *Associate* (entry, basic), *Professional* (intermediate/advanced), *Specialty/Specialist* (narrow product scope), plus one *Advocate* credential. Older certifications keep legacy role titles (Administrator, Developer, Deployment Professional, Solution Architect) without an explicit level suffix; newer ones carry `- Associate` / `- Professional`.
- **Portfolios:** AI/watsonx and quantum, Security, Data platforms, Analytics, Integration/messaging, Automation/observability/AIOps, Systems (z/OS, AIX, IBM i, WebSphere), and asset management (Maximo, TRIRIGA).
- **"PLUS" combinations:** six certifications bundle a **Red Hat Certified Specialist** exam (OpenShift Administration or Application Development) with an IBM Cloud Pak exam — one credential, two vendors' exams.
- **Catalog hygiene flags:** the catalog marks credentials **"Retiring soon"** (five as of this writing) and can include or exclude **Retired/Withdrawn** certificates — a first-class filter, and the reason to check the catalog rather than a mirror.

## Exam logistics

| Fact | Value |
|:---|:---|
| Delivery | Pearson VUE test centers or **OnVUE** online proctoring |
| Registration | Pearson VUE (pearsonvue.com/ibm); vouchers via the IBM certification marketplace |
| Exam codes | C1000-series (each certification page names its exam) |
| Badge | Credly, issued on pass |
| History/records | IBM My Learning (certification history, certificates) |

Certification pages on the IBM Training catalog carry each credential's exam, objectives, recommended training, and study resources — the per-certification source of truth.

## Hands-On Lab

### Lab 1.1 — Pull the live catalog

**Objective:** Read the authoritative certification list the way this volume was verified.

```text
browser> ibm.com/training/search  > Learning type: Certification
# 62 results (3 pages); toggle "Show Retired/Withdrawn Certificates" to see the graveyard
```

**Expected result:** The 62-item list this volume maps, each with a `Cert-` catalog code and level; five marked "Retiring soon." Any drift from this volume's tables means the catalog moved — trust the catalog.

**Negative test:** Search a third-party mirror for "IBM certification list" — counts and versions rarely match the live catalog; version-pinned certifications (QRadar V7.5, Db2 13, Maximo v9.1) churn constantly.

**Cleanup:** None.

### Lab 1.2 — Verify one certification end to end

**Objective:** Trace a credential from catalog to exam registration.

```text
browser> catalog entry "IBM Certified watsonx Generative AI Engineer - Associate" > Explore
# note: exam code (C1000-series), objectives, recommended training
browser> pearsonvue.com/ibm > View exams > find the exam code > delivery options (test center / OnVUE)
```

**Expected result:** The full chain: catalog entry → exam objectives → Pearson VUE registration with both delivery options — the drill you repeat for whichever certification you target.

**Negative test:** A certification page whose exam no longer appears at Pearson VUE is mid-retirement — the "Retiring soon" flag usually says so first.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The three credential kinds distinguished (certification vs badge vs Coursera certificate).
- [ ] 62-certification catalog shape, levels, and portfolios internalized.
- [ ] PLUS/Red Hat combinations and "Retiring soon" flags understood.
- [ ] Catalog-to-Pearson-VUE verification drill practiced.
