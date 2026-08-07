# Chapter 01: The SAS Certification Program

## Learning Objectives

- Describe SAS as the analytics, statistics, and data-management leader and where certification fits.
- Distinguish the credential levels — Specialist, Professional, and the composite Data Scientist.
- Map the credential categories — programming, analytics/statistics, AI/ML, data curation, visual/BI, administration.
- Understand the exam mechanics — Pearson VUE, ~$180, five-year validity, some performance-based.

*Cert relevance: this chapter frames the whole program — the levels, categories, and mechanics the rest of the volume develops.*

## SAS and its certifications

**SAS** is the long-standing leader in **analytics, statistics, and data management** — the software that enterprises, banks, governments, and researchers have used for decades to analyze data, build statistical and machine-learning models, and produce trusted results. Two things define it: the **SAS programming language** (the DATA step and PROC steps, [Ch 2](02-the-sas-platform.md)) and **SAS Viya**, the modern **cloud-native, in-memory AI and analytics platform**. Where some tools focus on dashboards, SAS's heritage is **rigorous analytics and statistics** end to end — from data preparation through modeling to deployment.

**SAS Global Certification** validates skill with the SAS language and platform. Because SAS spans programming, statistics, machine learning, and BI, the certification catalog is broad, organized into **categories** and **levels**. SAS sits alongside the analytics and data platforms this shelf covers ([Tableau CLIV](../../volume-154-tableau-certifications/README.md), [Qlik CLXI](../../volume-161-qlik-certifications/README.md), [Databricks XLVIII](../../volume-048-databricks-certifications/README.md)) — its distinctive angle is the SAS language and deep statistical analytics. The lab builds the program map.

## The credential levels

SAS certifications come in **three levels of scope**:

- **SAS Certified Specialist** — earned by passing a **single exam** in a focused area (e.g. *Machine Learning Using SAS Viya*, *Visual Business Analytics*). The mainstream credential.
- **SAS Certified Professional** — earned by passing **multiple exams** in a track, validating broader competency (e.g. a programming professional passing foundation plus advanced exams).
- **SAS Certified Data Scientist** — a **composite** credential earned by **combining** several credentials across data curation, programming, AI/ML, and advanced analytics. The capstone, reflecting the full data-science skill set. *(The Data Scientist path was updated 30 June 2025.)*

Read the levels as **one skill** (Specialist), **a track** (Professional), and **the whole discipline** (Data Scientist). Credentials are issued as **digital badges**. The lab models the levels. *(A composite, multi-credential capstone is similar in spirit to layered credential programs across the encyclopedia.)*

## The credential categories

Certifications are organized by **what you do with SAS**:

| Category | Representative credential |
| --- | --- |
| **Programming** | Fundamentals of Programming Using SAS Viya; Programming Specialist; Advanced Programming ([Ch 3](03-sas-programming-foundations.md), [Ch 4](04-preparing-and-curating-data.md)) |
| **Advanced Analytics / Statistics** | Statistical Business Analyst — regression and modeling ([Ch 5](05-statistical-analysis.md)) |
| **AI & Machine Learning** | Machine Learning Specialist Using SAS Viya ([Ch 6](06-machine-learning-on-viya.md)) |
| **Data Curation** | data preparation and management ([Ch 4](04-preparing-and-curating-data.md)) |
| **Visual / BI** | Visual Business Analytics Using SAS Viya ([Ch 7](07-visual-analytics-and-bi.md)) |
| **Administration** | SAS Viya Administration ([Ch 8](08-data-scientist-and-administration.md)) |

You certify in the **category your role centers on** — a programmer in programming, a statistician in advanced analytics, a data scientist across several. The lab maps the categories.

## Exam mechanics

SAS exams share a consistent shape:

- **Delivery** — through **Pearson VUE** (test center or online proctoring); some are SAS-proctored.
- **Format** — typically **60–70 questions**; some exams are **performance-based** (you complete tasks **hands-on in SAS**, not just multiple choice).
- **Passing score** — varies by exam (commonly in the high-60s to low-70s percent; e.g. the Programming Specialist exam is **71%**).
- **Cost** — about **$180 USD** per exam.
- **Validity** — credentials are valid **five years**.
- **Exam codes** — the familiar **A00-xxx** codes (e.g. A00-420 Programming Specialist, A00-240 Statistical Business Analyst, A00-451 Viya Administration).

The performance-based exams matter: SAS validates that you can **actually do the work** in the software, not just recall syntax. The lab records the mechanics.

## Hands-On Lab

Python models the program: levels, categories, and mechanics. **Cost:** none.

### Lab 1.1 — Map the levels and categories

**Objective:** Record the three levels and the credential categories.

```bash
python3 - <<'EOF'
LEVELS = {
  "SAS Certified Specialist":     "single exam in a focused area (mainstream)",
  "SAS Certified Professional":   "multiple exams in a track (broader competency)",
  "SAS Certified Data Scientist": "composite — combine credentials across the discipline (capstone)",
}
CATEGORIES = {
  "Programming":                 "Fundamentals / Specialist / Advanced (SAS language)",
  "Advanced Analytics/Statistics":"Statistical Business Analyst (regression, modeling)",
  "AI & Machine Learning":       "Machine Learning Specialist (SAS Viya, Model Studio)",
  "Data Curation":               "data preparation and management",
  "Visual / BI":                 "Visual Business Analytics (SAS Visual Analytics)",
  "Administration":              "SAS Viya Administration",
}
print("SAS GLOBAL CERTIFICATION — levels:\n")
for lvl, d in LEVELS.items():
    print(f"   {lvl:32} {d}")
print("\nCategories (certify where your role centers):")
for cat, d in CATEGORIES.items():
    print(f"   {cat:30} {d}")
print()
print("Read the levels as ONE SKILL (Specialist) -> A TRACK (Professional) -> THE WHOLE")
print("DISCIPLINE (Data Scientist, composite). Certify in the category your role centers on.")
EOF
```

**Expected result:** A level map (Specialist single-exam, Professional multi-exam, Data Scientist composite) and the credential categories (programming, analytics/statistics, AI/ML, data curation, visual/BI, administration). The lesson is that SAS certifications scale from one skill to a track to the whole discipline, organized by what you do with SAS, and you certify in the category matching your role.

**Cleanup:** None.

### Lab 1.2 — Record the exam mechanics

**Objective:** Capture the SAS exam format and codes.

```bash
python3 - <<'EOF'
MECHANICS = {
  "delivery":   "Pearson VUE (test center or online); some SAS-proctored",
  "format":     "~60-70 questions; some exams are PERFORMANCE-BASED (hands-on in SAS)",
  "passing":    "varies by exam (~high-60s to low-70s %; Programming Specialist = 71%)",
  "cost":       "~$180 USD per exam",
  "validity":   "5 years",
  "codes":      "A00-xxx (e.g. A00-420 Programming Specialist, A00-240 Stat Business Analyst, A00-451 Viya Admin)",
}
print("SAS EXAM MECHANICS:\n")
for k, v in MECHANICS.items():
    print(f"   {k:9}: {v}")
print()
print("PERFORMANCE-BASED exams are the key point: SAS validates that you can DO the work")
print("hands-on in the software, not only recall syntax. Exams are A00-xxx, via Pearson VUE,")
print("~$180, valid 5 years.")
EOF
```

**Expected result:** A record of the exam mechanics — Pearson VUE delivery, ~60–70 questions with some performance-based, passing scores in the high-60s to low-70s (Programming Specialist 71%), ~$180, five-year validity, A00-xxx codes. The lesson is that SAS certification is hands-on and rigorous — performance-based exams test doing the work in the software — delivered through Pearson VUE at about $180 with five-year validity.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] SAS placed — the analytics, statistics, and data-management leader (the SAS language + SAS Viya).
- [ ] The levels understood — Specialist (one exam), Professional (a track), Data Scientist (composite capstone).
- [ ] The categories mapped — programming, analytics/statistics, AI/ML, data curation, visual/BI, administration.
- [ ] The exam mechanics recorded — Pearson VUE, ~$180, five-year validity, some performance-based, A00-xxx codes.

## See also

- [Volume CLIV — Tableau](../../volume-154-tableau-certifications/README.md) and [Volume CLXI — Qlik](../../volume-161-qlik-certifications/README.md) — visual-analytics peers.
- [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md) — a data-science/ML platform peer.
- [Chapter 02 — The SAS Platform and Language](02-the-sas-platform.md).
