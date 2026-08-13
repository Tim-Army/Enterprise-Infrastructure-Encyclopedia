# Chapter 01: The Qlik Certification Program

![The Qlik certification program and the Qlik analytics platform beneath it. Qlik offers a two-tier credential structure. Fundamental-level Qualifications include the Data Literacy Qualification, a non-technical, product-agnostic exam of thirty multiple-choice questions in one hour measuring the ability to read, work with, analyze, and communicate with data; the Qlik Sense Business Analyst Qualification, which requires building a Qlik Sense application plus a multiple-choice exam in one hour fifteen minutes; and the Qlik Sense Data Architect Qualification. Expert-level Certifications include the Qlik Sense Business Analyst, the Qlik Sense Data Architect, each fifty questions in ninety minutes with a sixty-two percent passing score and platform-neutral across client-managed and Qlik Cloud, and the Qlik Sense System Administrator. The platform beneath is Qlik Sense and Qlik Cloud, built on the Associative Engine, an in-memory associative model where selections instantly reveal associated and excluded data across every visualization, with the Data Load Editor, set analysis, the Qlik Management Console, and AI through Insight Advisor and Qlik Answers.](../../../diagrams/volume-161-qlik-certifications/chapter-01-program.svg)

*Figure 1-1. The two-tier Qualifications and Certifications and the associative Qlik platform they validate.*

## Learning Objectives

- Describe the Qlik program — the two-tier Qualifications and Certifications structure.
- Distinguish fundamental Qualifications from expert Certifications.
- State the exam mechanics (e.g., QSBA/QSDA — 50 questions, 90 minutes, 62%).
- Recognize Qlik's position as an associative analytics/BI platform.

## What Qlik is

Qlik is a leader in **analytics and business intelligence (BI)** — its platform, **Qlik Sense** (delivered client-managed or as **Qlik Cloud** SaaS), lets people explore data and build interactive **visualizations, dashboards, and analytics apps**. Qlik's signature technology is its **Associative Engine** ([Chapter 2](02-the-associative-model.md)) — an in-memory, associative data model that lets users explore data **freely in any direction** and see not just what is related but what is *not*. Qlik also champions **data literacy** as a discipline. It sits alongside the other analytics/BI platform this shelf covers, [Tableau (CLIV)](../../volume-154-tableau-certifications/README.md); **Qlik versus Tableau** is the defining BI comparison. The lab models the program.

## The two-tier program

Qlik's credentials come in **two distinct tiers** — worth being precise about:

- **Qualifications** — **fundamental-level**, validating foundational skills. Qlik states explicitly that a Qualification is *not* the expert-level certification. Several require **building a Qlik Sense app** plus a multiple-choice exam.
- **Certifications** — **expert-level**, validating deep, applied proficiency, delivered through the Qlik learning portal.

This two-tier structure lets learners demonstrate **foundational** competence (Qualification) on the way to **expert** competence (Certification). Knowing the difference is the first thing a candidate must understand. The lab models the tiers.

## The Qualifications and Certifications

| Tier | Credential | Notes |
|:---|:---|:---|
| **Qualification** | **Data Literacy Qualification** | Non-technical, **product-agnostic**; 30 questions / 1 hour |
| **Qualification** | **Qlik Sense Business Analyst Qualification** | Build a Qlik Sense app + MCQ; 1h 15m (*not* expert-level) |
| **Qualification** | **Qlik Sense Data Architect Qualification** | Build an app + MCQ |
| **Certification** | **Qlik Sense Business Analyst (QSBA)** | Expert; **50 questions / 90 min / 62%**; platform-neutral |
| **Certification** | **Qlik Sense Data Architect (QSDA)** | Expert; **50 questions / 90 min / 62%**; platform-neutral |
| **Certification** | **Qlik Sense System Administrator (QSSA)** | Expert; deploy, manage, govern |

**Platform-neutral** means the certification content applies to **both** client-managed Qlik Sense *and* Qlik Cloud. The three roles — **Business Analyst** (build apps/visualizations), **Data Architect** (model and load data), **System Administrator** (deploy and govern) — map to the middle chapters. The lab maps the program.

## The role families

The certifications validate three roles, each with a chapter: the **Data Architect** ([loading and modeling, Ch 4](04-data-architect.md)), the **Business Analyst** ([building visualizations, Ch 5](05-business-analyst.md)), and the **System Administrator** ([deploying and governing, Ch 7](07-system-administrator.md)) — over the associative platform, with [set analysis (Ch 6)](06-set-analysis-and-expressions.md) as the distinctive expression skill and [data literacy and AI (Ch 8)](08-data-literacy-and-ai.md) rounding it out. The lab situates them.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the two-tier program

**Objective:** Represent Qualifications versus Certifications.

```bash
python3 - <<'EOF'
PROGRAM = {
  "Qualifications (fundamental)": [
    ("Data Literacy Qualification", "non-technical, product-agnostic; 30Q / 1hr"),
    ("Qlik Sense Business Analyst Qualification", "build an app + MCQ; 1h15m (NOT expert-level)"),
    ("Qlik Sense Data Architect Qualification", "build an app + MCQ"),
  ],
  "Certifications (expert)": [
    ("Qlik Sense Business Analyst (QSBA)", "50Q / 90min / 62%; platform-neutral"),
    ("Qlik Sense Data Architect (QSDA)", "50Q / 90min / 62%; platform-neutral"),
    ("Qlik Sense System Administrator (QSSA)", "deploy / manage / govern"),
  ],
}
print("Qlik — TWO-TIER credential program:\n")
for tier, creds in PROGRAM.items():
    print(f"   {tier}:")
    for name, note in creds:
        print(f"      - {name}")
        print(f"          {note}")
    print()
print("The KEY distinction: QUALIFICATIONS are FUNDAMENTAL-level ('NOT our expert-level")
print("certification', per Qlik) — some require BUILDING a Qlik Sense app + an MCQ.")
print("CERTIFICATIONS are EXPERT-level (QSBA/QSDA = 50Q/90min/62%). 'PLATFORM-NEUTRAL' means")
print("the content applies to BOTH client-managed Qlik Sense AND Qlik Cloud. Three roles:")
print("BUSINESS ANALYST (build apps), DATA ARCHITECT (model/load data), SYSTEM ADMIN (govern).")
print("Qlik = associative analytics/BI — the peer of Tableau (CLIV).")
EOF
```

**Expected result:** The two-tier program — fundamental Qualifications (Data Literacy, Business Analyst, Data Architect, some requiring an app build) and expert Certifications (QSBA/QSDA/QSSA, 50Q/90min/62%, platform-neutral). The program lesson is that Qlik separates fundamental Qualifications from expert Certifications, with three roles (Business Analyst, Data Architect, System Administrator) validated across both client-managed Qlik Sense and Qlik Cloud.

**Negative test:** Treating a Qualification as the expert certification. Qlik explicitly states a Qualification is *not* the expert-level certification; the Qualifications are fundamental, and the QSBA/QSDA/QSSA Certifications are the expert credentials.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Platform-neutral, role-based certifications

**Objective:** Reason about platform-neutrality and the roles.

```bash
python3 - <<'EOF'
CERTS = {
  "Business Analyst (QSBA)": {"builds": "apps, visualizations, stories, analysis",
                              "exam": "50Q / 90min / 62%", "platform": "client-managed + Qlik Cloud"},
  "Data Architect (QSDA)":   {"builds": "data models, load scripts, validated data",
                              "exam": "50Q / 90min / 62%", "platform": "client-managed + Qlik Cloud"},
  "System Administrator (QSSA)": {"builds": "deployment, streams, security, governance",
                              "exam": "expert", "platform": "client-managed (QMC) + Qlik Cloud"},
}
print("Qlik expert Certifications — three roles:\n")
for role, d in CERTS.items():
    print(f"   {role}")
    for k, v in d.items():
        print(f"      {k:9}: {v}")
    print()
print("PLATFORM-NEUTRAL: the exams cover both CLIENT-MANAGED Qlik Sense (on-prem/self-hosted)")
print("AND QLIK CLOUD (SaaS) — so the credential is portable across deployment models. Match")
print("the cert to your ROLE: build APPS (Business Analyst), model DATA (Data Architect), or")
print("GOVERN the platform (System Administrator). All three sit on the same associative engine.")
EOF
```

**Expected result:** The three expert roles (Business Analyst, Data Architect, System Administrator) with QSBA/QSDA at 50Q/90min/62%, all platform-neutral across client-managed and Qlik Cloud. The lesson is that Qlik's certifications are role-based and platform-neutral, so the credential is portable across deployment models — you certify for your role (build apps, model data, or govern the platform) on the same associative engine.

**Negative test:** Assuming a Qlik cert is tied to one deployment. The certifications are platform-neutral, covering both client-managed Qlik Sense and Qlik Cloud; the credential validates role skill regardless of where Qlik runs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The two-tier program understood — fundamental Qualifications versus expert Certifications.
- [ ] The Qualifications (Data Literacy, Business Analyst, Data Architect) and Certifications (QSBA/QSDA/QSSA) placed.
- [ ] The exam mechanics known (QSBA/QSDA — 50 questions, 90 minutes, 62%, platform-neutral).
- [ ] Qlik recognized as an associative analytics/BI platform, the peer of Tableau (CLIV).
