# Chapter 09: Choosing Your SAS Path

## Learning Objectives

- Map roles (programmer, statistician, data scientist, BI analyst, administrator) to credentials.
- Sequence certifications — start with programming, then specialize.
- Decide between Specialist, Professional, and the composite Data Scientist.
- Place SAS in the analytics and data-science ecosystem.

*Cert relevance: this chapter turns the category map ([Ch 1](01-the-sas-program.md)) into a personal plan and ends with a capstone.*

## Match the credential to your role

SAS certifications map to what you do:

| Your role | Start here | Then consider |
| --- | --- | --- |
| **SAS programmer** | Fundamentals / Programming Specialist ([Ch 3](03-sas-programming-foundations.md)) | Advanced Programming |
| **Statistician / analyst** | Statistical Business Analyst ([Ch 5](05-statistical-analysis.md)) | Machine Learning Specialist |
| **Data scientist** | Programming + curation, then compose | SAS Certified Data Scientist ([Ch 8](08-data-scientist-and-administration.md)) |
| **BI / visual analyst** | Visual Business Analytics ([Ch 7](07-visual-analytics-and-bi.md)) | Programming for data prep |
| **ML engineer** | Machine Learning Specialist ([Ch 6](06-machine-learning-on-viya.md)) | Statistical Business Analyst |
| **Platform administrator** | SAS Viya Administration ([Ch 8](08-data-scientist-and-administration.md)) | — |

The pattern: certify in the **category your role centers on**, at the **level** that matches (Specialist, Professional, or the composite Data Scientist). The lab builds a role-to-path planner.

## Sequence sensibly

A workable sequence for most people:

1. **Start with programming.** The SAS language (DATA step + PROCs) is the foundation everything else uses — even statistics, ML, and curation are expressed through it. Take Fundamentals, then Programming Specialist.
2. **Add your specialty.** Statistics (Statistical Business Analyst), machine learning (ML Specialist), data curation, or visual analytics — whichever your role centers on.
3. **Compose toward Data Scientist** if that is your goal — combine curation, programming, ML, and advanced analytics into the composite ([Ch 8](08-data-scientist-and-administration.md)).
4. **Or take the admin pole** — SAS Viya Administration if you operate the platform rather than build analytics.

Because credentials are **valid five years**, plan to recertify, and note whether an exam targets **SAS Viya** (the modern platform) — the current focus of most certifications. The lab sequences a plan.

## Specialist, Professional, or Data Scientist

- **Specialist** — a single exam in a focused area. The right target for most people proving a specific skill (programming, ML, visual analytics).
- **Professional** — multiple exams in a track, for broader depth.
- **Data Scientist (composite)** — the capstone, for those who want to certify the **whole** data-science lifecycle by combining credentials.

Most careers collect one or a few **Specialist** credentials in their area; data-science-track people work toward the **composite**; platform people take **Administration**. The lab reflects the decision. The strength of SAS is the **rigor** behind all of them — statistical soundness and a trusted platform.

## SAS in the ecosystem

SAS is a leader in a competitive analytics/data-science space:

- **Analytics / BI peers** — [Tableau (CLIV)](../../volume-154-tableau-certifications/README.md) and [Qlik (CLXI)](../../volume-161-qlik-certifications/README.md): strong at visualization; SAS's edge is deep **statistics and ML** behind the reports.
- **Data-science / ML platforms** — [Databricks (XLVIII)](../../volume-048-databricks-certifications/README.md) and [Snowflake (XLIX)](../../volume-049-snowflake-certifications/README.md): modern cloud data/ML; SAS's edge is **decades of validated statistical methods** and use in **regulated** industries.
- **Open source** — Python and R are ubiquitous in data science; SAS interoperates (call SAS/CAS from Python via SWAT) and competes on **rigor, support, and governance** for enterprises that need them.

Learning SAS is learning **rigorous, end-to-end analytics** — from data curation through validated statistics and ML to trusted deployment — in a platform enterprises rely on where correctness matters. The capstone builds that end to end. The lab closes with it.

## Hands-On Lab

Python builds a role-to-path planner, then a capstone spanning the SAS lifecycle. **Cost:** none.

### Lab 9.1 — Plan your SAS path

**Objective:** Turn a role into a sequenced certification plan.

```bash
python3 - <<'EOF'
ROLE_PATHS = {
  "SAS programmer":      ["Programming Specialist", "Advanced Programming"],
  "Statistician":        ["Statistical Business Analyst", "Machine Learning Specialist"],
  "Data scientist":      ["Programming + Data Curation", "ML + Advanced Analytics", "SAS Certified Data Scientist (composite)"],
  "BI analyst":          ["Visual Business Analytics", "Programming (data prep)"],
  "Platform admin":      ["SAS Viya Administration"],
}
def plan(role):
    steps = ROLE_PATHS[role]
    print(f"   ROLE: {role}")
    print(f"      1. START: {steps[0]}")
    for i, s in enumerate(steps[1:], 2):
        print(f"      {i}. THEN:  {s}")
    print("      note: exams via Pearson VUE (~$180), valid 5 years; prefer 'Using SAS Viya' (modern platform)")
print("SAS ROLE -> CERTIFICATION PATH:\n")
for role in ["SAS programmer", "Data scientist", "Platform admin"]:
    plan(role); print()
print("Start with PROGRAMMING (the foundation), add your specialty (stats/ML/BI/curation), and")
print("compose toward the Data Scientist capstone — or take the Administration pole to run Viya.")
EOF
```

**Expected result:** A planner turning roles into sequenced paths — a programmer takes Programming Specialist then Advanced; a data scientist builds toward the composite; an admin takes Viya Administration. The lesson is to start with programming, add your specialty, and either compose toward the Data Scientist capstone or take the administration pole.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Capstone: the SAS analytics lifecycle end to end

**Objective:** Take raw data through curation, statistics, ML, and reporting.

```bash
python3 - <<'EOF'
# CAPSTONE: raw data -> curate -> describe -> model -> assess -> report (the SAS lifecycle)
raw = [{"id":1,"spend":"20","churn":1},{"id":2,"spend":"40","churn":0},
       {"id":3,"spend":"bad","churn":1},{"id":4,"spend":"60","churn":0}]
log = []
# 1) CURATE (DATA step + validation): clean 'spend', drop invalid
clean = []
for r in raw:
    try: clean.append({"id":r["id"],"spend":int(r["spend"]),"churn":r["churn"]})
    except ValueError: pass
log.append(f"CURATE: {len(raw)} raw -> {len(clean)} clean (dropped invalid spend)")
# 2) DESCRIBE (PROC MEANS): mean spend by churn
byc = {}
for r in clean: byc.setdefault(r["churn"], []).append(r["spend"])
log.append("DESCRIBE: mean spend by churn -> " + str({k: sum(v)/len(v) for k,v in byc.items()}))
# 3) MODEL (logistic-style rule) + 4) ASSESS on the data
def model(spend): return 1 if spend < 40 else 0   # low spend -> churn
correct = sum(1 for r in clean if model(r["spend"])==r["churn"])
log.append(f"MODEL + ASSESS: rule 'spend<40 -> churn' accuracy = {correct}/{len(clean)}")
# 5) REPORT (Visual Analytics): summarize for the business
log.append(f"REPORT: {sum(r['churn'] for r in clean)}/{len(clean)} churned; lower spend correlates with churn")

print("CAPSTONE — the SAS analytics lifecycle end to end:\n")
for step in log: print(f"   {step}")
print()
print("Raw data becomes CURATED (DATA step + validation drops the bad 'spend'), DESCRIBED (PROC")
print("MEANS by churn), MODELED + ASSESSED (a rule + accuracy on held-out logic), and REPORTED")
print("(Visual Analytics summary). Curate -> describe -> model -> assess -> report, with rigor at")
print("each step, IS data science — and what the SAS Certified Data Scientist path certifies end to end.")
EOF
```

**Expected result:** A capstone taking raw data through curation (drop invalid), description (means by group), modeling and assessment (a rule and its accuracy), and reporting. The lesson synthesizes the volume: SAS covers the whole analytics lifecycle — curate, describe, model, assess, report — with statistical rigor at each step, which is exactly what the programming, analytics, ML, and Data Scientist certifications prepare you to do.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Roles mapped to credentials — programmer, statistician, data scientist, BI analyst, administrator.
- [ ] A sensible sequence chosen — start with programming, add a specialty, compose toward Data Scientist or take admin.
- [ ] The level decision made — Specialist, Professional, or the composite Data Scientist.
- [ ] SAS placed in the ecosystem — rigorous, end-to-end analytics for enterprises where correctness matters.

## See also

- [Chapter 01 — The SAS Certification Program](01-the-sas-program.md) — the levels and categories this plan draws on.
- [Volume CLIV — Tableau](../../volume-154-tableau-certifications/README.md), [Volume CLXI — Qlik](../../volume-161-qlik-certifications/README.md), and [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md) — analytics and data-science peers.
