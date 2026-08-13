# Chapter 09: Choosing Your Tableau Path

## Learning Objectives

- Sequence a Tableau certification path by role.
- Understand currency and the Salesforce maintenance model.
- Place Tableau skills in the data-analytics career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the track [Chapter 1](01-the-tableau-certification-program.md) laid out.*

## Sequencing your path

The [three-step track](01-the-tableau-certification-program.md) maps cleanly to roles and experience:

| You are | Start | Then |
|:---|:---|:---|
| **New to Tableau / analyst** | Tableau Desktop Specialist | Certified Data Analyst |
| **Working data analyst** | Certified Data Analyst | (Desktop Specialist first if new) |
| **BI developer / architect** | Certified Data Analyst | Certified Architect |
| **Platform admin** | Desktop Specialist (context) | Certified Architect |

**Desktop Specialist is the anchor for everyone new** — it is affordable (~$75), foundational, and proves the connect-and-visualize basics the rest assume. The **Certified Data Analyst** is the credential most working analysts want — with its **hands-on labs**, it validates real analytical competence and is the most recognized. The **Architect** is for those moving into *deploying and governing* Tableau at scale.

The sensible path for most: **Desktop Specialist → Certified Data Analyst**, adding **Architect** if your role moves toward platform ownership. Because the Data Analyst has hands-on labs, prepare by *building* in Tableau (the free **Tableau Public** and trial make this cost-free), not just reading.

## Currency

The entry **Desktop Specialist** historically has no fixed expiry, but the **Salesforce-branded** certifications (Data Analyst, Architect) follow **Salesforce's maintenance model** — periodic maintenance to keep the credential current as the product evolves. Tableau updates frequently (new features, and the AI capabilities of [Chapter 8](08-sharing-governance-and-the-server.md) are advancing fast), so maintenance keeps skills aligned with the current product.

The discipline: treat each major Tableau release and each Salesforce maintenance cycle as the drumbeat, and — because analysis is a hands-on craft — keep *building*, not just holding the badge. A two-year-old Tableau skillset predates much of the current AI-analytics story.

## The data-analytics career

Tableau skills sit in a large, durable market: **every organization has data and needs people who can turn it into insight.** Data visualization and analysis is a core competency across analytics, BI, data science, and business roles, and Tableau is one of the most widely-used tools for it. An analyst who can connect, model, visualize, and communicate from data — and increasingly, work with AI-driven analytics — is broadly employable.

The career pairs naturally with adjacent skills this shelf covers:

- **[Snowflake (XLIX)](../../volume-049-snowflake-certifications/README.md) / [Databricks (XLVIII)](../../volume-048-databricks-certifications/README.md)** — the data platforms Tableau visualizes; knowing the source deepens the analysis.
- **SQL / data modeling** — the foundation beneath any BI tool.
- **[Confluent (CXXXV)](../../volume-135-confluent-certifications/README.md) / data pipelines** — how data flows to the warehouse Tableau reads.
- **[Salesforce (LXXXIII)](../../volume-083-salesforce-certifications/README.md)** — Tableau's owner; the two increasingly integrate (Tableau + Einstein).

Tableau is the visualization-and-analytics specialty in a world where every decision wants to be data-driven. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal Tableau plan. **Cost:** none.

### Lab 9.1 — Build your Tableau certification path

**Objective:** Generate a role-appropriate sequence.

```bash
python3 - <<'EOF'
PATHS = {
  "new analyst": [
    ("Tableau Desktop Specialist", "the anchor — connect + visualize (~$75, 45Q/60min)"),
    ("Salesforce Certified Tableau Data Analyst", "viz + analysis, HANDS-ON LABS (the recognized cert)"),
  ],
  "BI developer / architect": [
    ("Certified Tableau Data Analyst", "prove analytical competence first"),
    ("Salesforce Certified Tableau Architect", "deploy + govern Tableau at scale"),
  ],
}
role = "new analyst"   # change to taste
print(f"Tableau path for: {role}\n")
for i, (cert, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. {cert:44} {why}")
print("\nGuidance:")
print("  - START at DESKTOP SPECIALIST if new — affordable, foundational, proves the")
print("    connect-and-visualize basics the rest assume.")
print("  - the CERTIFIED DATA ANALYST is what most working analysts want: HANDS-ON LABS")
print("    validate real competence, and it's the most recognized. PREPARE BY BUILDING")
print("    (free Tableau Public + trial), not just reading.")
print("  - the ARCHITECT is for moving into platform deploy + governance.")
print("  - CURRENCY: Desktop Specialist historically no expiry; the Salesforce-branded")
print("    certs follow Salesforce's MAINTENANCE model. Tableau + its AI features move")
print("    fast — keep building.")
EOF
```

**Expected result:** A role-specific sequence anchored on the affordable Desktop Specialist, climbing to the hands-on Certified Data Analyst and (for platform roles) the Architect. The build-your-path lesson is to anchor on the entry credential, pursue the recognized Data Analyst by actually building in Tableau, and add the Architect for platform ownership, keeping currency via Salesforce's maintenance model.

**Negative test:** Cramming the Certified Data Analyst from a question bank. It has hands-on labs that test performing analysis in Tableau — preparation means building real workbooks (free via Tableau Public), not memorizing facts.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Position Tableau in the data-analytics career

**Objective:** Map Tableau skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Tableau (viz/BI)", "data visualization + analysis", "the specialty itself"),
  ("Snowflake / Databricks", "the data platforms", "the source Tableau visualizes"),
  ("SQL / data modeling", "querying + shaping data", "the foundation beneath any BI tool"),
  ("Confluent / pipelines", "how data flows to the warehouse", "the plumbing behind the analysis"),
  ("Salesforce / Einstein", "Tableau's owner + AI", "increasing integration (Tableau Pulse)"),
  ("statistics / data literacy", "reading data honestly", "the judgment behind good analysis"),
]
print("Tableau in the data-analytics skill map:\n")
print(f"   {'skill':26}{'domain':38}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:26}{domain:38}{why}")
print("\nThe career thesis: EVERY organization has data and needs people who turn it into")
print("INSIGHT. Data viz + analysis is a core competency across analytics, BI, data")
print("science, and business roles — and Tableau is one of the most-used tools for it.")
print("\nThe rounded data analyst combines:")
print("  CONNECT    (SQL, the data platforms) — get + understand the data")
print("  VISUALIZE  (Tableau)                 — turn it into something humans SEE")
print("  ANALYZE    (calcs, LOD, stats)       — find the real insight")
print("  COMMUNICATE (dashboards, stories)    — persuade with evidence")
print("  GOVERN     (certified sources)       — one trusted source of truth")
print("  AUGMENT    (Tableau Pulse / AI)      — AI-surfaced insight")
print("\nNone of it is siloed — it's the data->insight->decision pipeline, and Tableau")
print("owns the human-facing VISUALIZATION + ANALYSIS heart of it. Start at Desktop")
print("Specialist, build toward Data Analyst, and pair with SQL + data-platform +")
print("data-literacy skills — that's a data-analytics career, not just a certificate.")
EOF
```

**Expected result:** Tableau skills mapped to adjacent competencies — data platforms (Snowflake, Databricks), SQL, pipelines (Confluent), Salesforce/Einstein, and statistics — showing the rounded connect/visualize/analyze/communicate/govern profile. The career-positioning lesson closes the volume: Tableau owns the visualization-and-analysis heart of the data-to-decision pipeline, pairing with the data-platform, SQL, and data-literacy skills the rest of the shelf teaches.

**Negative test:** Treating Tableau as a standalone drawing tool. It sits on data platforms, rests on SQL and data-modeling, and increasingly integrates AI — isolating it from the data stack and data literacy undersells both the tool and the analytics career.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A Tableau path sequenced by role, anchored on Desktop Specialist and climbing to Data Analyst and Architect.
- [ ] Currency understood — Desktop Specialist's longevity and the Salesforce maintenance model for the branded certs.
- [ ] Tableau positioned in the data-analytics career alongside data platforms, SQL, pipelines, and data literacy.
- [ ] The volume assembled into a personal study and career plan — connect, visualize, analyze, communicate, govern.
