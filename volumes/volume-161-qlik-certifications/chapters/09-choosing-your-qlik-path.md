# Chapter 09: Choosing Your Qlik Path

## Learning Objectives

- Sequence a Qlik certification path by role and tier.
- Understand currency for an evolving analytics platform.
- Place Qlik/analytics skills in the career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the two-tier program [Chapter 1](01-the-qlik-program.md) laid out.*

## Sequencing your path

The [two-tier program (Ch 1)](01-the-qlik-program.md) sequences by tier and role:

| You are | Start | Then |
|:---|:---|:---|
| **New to data / analytics** | **Data Literacy Qualification** (product-agnostic) | a role Qualification |
| **Business analyst** | **QS Business Analyst Qualification** | **QS Business Analyst (QSBA)** certification |
| **Data architect** | **QS Data Architect Qualification** | **QS Data Architect (QSDA)** certification |
| **Platform administrator** | (platform experience) | **QS System Administrator (QSSA)** certification |

**Start with the Qualification** for your role (or the product-agnostic **Data Literacy Qualification** for the fundamentals), then advance to the **expert Certification** (QSBA/QSDA/QSSA). Because the certifications are [platform-neutral (Ch 1)](01-the-qlik-program.md), the credential works whether you run client-managed Qlik Sense or Qlik Cloud. Focus on the durable core: the [associative model (Ch 2)](02-the-associative-model.md) and [set analysis (Ch 6)](06-set-analysis-and-expressions.md). The lab builds a sequence.

## Currency

Qlik's platform evolves — **Qlik Cloud** (the SaaS direction), **AI** (Insight Advisor, AutoML, Qlik Answers), and the **Qlik Talend** data-integration portfolio are all moving. Treat certification as a snapshot and keep current with the platform and the analytics field. The **associative model** and **set analysis** are the durable core that pays off regardless of tooling changes, while the AI and cloud capabilities are the fast-moving frontier to keep watching. The lab covers currency.

## The analytics / BI career

Qlik skills sit in the **analytics / BI** career — durable and in-demand because **every organization needs to turn data into decisions**, and the shift to self-service and AI-augmented analytics only grows the need. A Qlik analyst or architect fluent in the associative model, data modeling, set analysis, and visualization is exactly the profile enterprises need. The career pairs with adjacent skills this shelf covers:

- **[Tableau (CLIV)](../../volume-154-tableau-certifications/README.md)** — the direct BI/visualization peer; Qlik vs Tableau is *the* comparison, and knowing both broadens your reach (Qlik's edge: the associative model and the power of gray).
- **[Snowflake (XLIX)](../../volume-049-snowflake-certifications/README.md) / [Databricks (XLVIII)](../../volume-048-databricks-certifications/README.md) / [Cloudera (CLVIII)](../../volume-158-cloudera-certifications/README.md)** — the data platforms Qlik analyzes.
- **Data literacy** — the human skill that makes all of it valuable, and increasingly a differentiator.

Qlik is the associative-analytics specialty in the BI/analytics career. The lab positions it.

## Hands-On Lab

Python assembles a personal Qlik plan. **Cost:** none.

### Lab 9.1 — Build your Qlik path

**Objective:** Generate a tier- and role-appropriate sequence.

```bash
python3 - <<'EOF'
PATHS = {
  "business analyst": [
    ("Data Literacy Qualification", "fundamental data skills (product-agnostic, optional start)"),
    ("QS Business Analyst Qualification", "fundamental: build an app + MCQ"),
    ("QS Business Analyst (QSBA) certification", "EXPERT: 50Q/90min/62%, platform-neutral"),
  ],
  "data architect": [
    ("QS Data Architect Qualification", "fundamental: build an app + MCQ"),
    ("QS Data Architect (QSDA) certification", "EXPERT: data modeling, associations, no synthetic keys"),
  ],
  "platform administrator": [
    ("QS System Administrator (QSSA) certification", "EXPERT: QMC, streams/spaces, security rules, reloads"),
  ],
}
role = "business analyst"   # change to taste
print(f"Qlik certification path for: {role}\n")
for i, (cred, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. {cred:44} {why}")
print("\nGuidance:")
print("  - START with the QUALIFICATION for your role (or the product-agnostic DATA LITERACY")
print("    Qualification for fundamentals), then advance to the EXPERT CERTIFICATION (QSBA/QSDA/QSSA).")
print("  - the certs are PLATFORM-NEUTRAL: valid for client-managed Qlik Sense AND Qlik Cloud.")
print("  - the DURABLE core = the ASSOCIATIVE MODEL (Ch 2) + SET ANALYSIS (Ch 6) — invest there.")
print("  - CURRENCY: Qlik Cloud, AI (Insight Advisor/AutoML/Qlik Answers), Qlik Talend are moving.")
EOF
```

**Expected result:** A tier-and-role sequence (e.g., business analyst: Data Literacy Qualification → QS Business Analyst Qualification → QSBA certification). The build-your-path lesson is to start with the Qualification for your role (or product-agnostic Data Literacy) and advance to the expert Certification, leaning on the platform-neutral, durable core of the associative model and set analysis.

**Negative test:** Aiming for the expert QSBA certification without the fundamentals or hands-on modeling. The certification assumes real proficiency in the associative model and set analysis; build via the Qualification and hands-on practice, then take the expert exam.

**Cleanup:** None.

### Lab 9.2 — Position Qlik in the analytics career

**Objective:** Map Qlik skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Qlik (associative analytics)", "explore data freely + the power of gray", "the specialty itself"),
  ("Tableau (CLIV)", "BI / visualization",                    "the direct peer (the comparison)"),
  ("Snowflake (XLIX) / Databricks (XLVIII)", "data platforms","the data Qlik analyzes"),
  ("Cloudera (CLVIII)", "hybrid data platform",               "another data source"),
  ("Data literacy", "read/analyze/communicate with data",     "the human skill that makes it valuable"),
]
print("Qlik in the analytics / BI skill map:\n")
print(f"   {'skill':42}{'domain':40}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:42}{domain:40}{why}")
print("\nThe career thesis: EVERY organization must turn DATA into DECISIONS, and self-service +")
print("AI-augmented analytics only grow the need. An analyst/architect fluent in the associative")
print("model, data modeling, set analysis, and visualization is exactly the in-demand profile.")
print("\nThe rounded analytics professional:")
print("  MODEL     (Data Architect)      — load + associate data (no synthetic keys)")
print("  ANALYZE   (Business Analyst)    — right chart + associative exploration + set analysis")
print("  GOVERN    (System Administrator)— streams/spaces, security rules, reloads")
print("  INTERPRET (data literacy)       — read/question/communicate — the human skill")
print("Qlik's edge = the ASSOCIATIVE engine (explore freely + see the GRAY) vs query-based tools.")
print("Learn it with Tableau (the peer), the data platforms it reads, and data literacy — that's")
print("an analytics career, Qualification to expert Certification.")
EOF
```

**Expected result:** Qlik mapped against Tableau (peer), Snowflake/Databricks/Cloudera (data sources), and data literacy, across the model/analyze/govern/interpret profile. The career-positioning lesson closes the volume: every organization must turn data into decisions, so Qlik's associative-analytics specialty (explore freely and see the gray) is durable and in-demand, learned alongside the Tableau peer, the data platforms it reads, and the data-literacy human skill.

**Negative test:** Treating Qlik as just another chart tool. Its associative engine (free exploration, the power of gray) is a distinct strength, and the role spans modeling, analysis, governance, and interpretation — a full analytics career, not a single feature.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Qlik path sequenced by tier and role — Qualification then expert Certification (QSBA/QSDA/QSSA).
- [ ] Currency understood — an evolving Qlik Cloud/AI/Qlik Talend platform, with the associative model and set analysis as the durable core.
- [ ] Qlik positioned in the analytics career alongside Tableau, the data platforms it reads, and data literacy.
- [ ] The volume assembled into a personal study and career plan — model, analyze, govern, interpret.
