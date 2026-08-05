# Chapter 01: The Tableau Certification Program

![The Tableau certification program and the platform beneath it. Tableau is owned by Salesforce, and its certifications form a three-step track. The Tableau Desktop Specialist, also called Tableau Desktop Foundations, is the entry-level credential: a proctored exam of forty-five questions in sixty minutes with a passing score of seven hundred fifty, priced around seventy-five US dollars, validating the ability to connect to and prepare data and build basic visualizations. The Salesforce Certified Tableau Data Analyst is the mid-level, most widely recognized credential: forty to forty-five questions plus eight to ten hands-on labs in one hundred twenty minutes, validating high proficiency in data visualization and analysis. The Salesforce Certified Tableau Architect is the advanced credential for enterprise deployment, Server and Cloud architecture, and governance. The recommended progression runs Desktop Specialist to Certified Data Analyst to Certified Architect. The platform beneath turns data into understanding: connect to data sources live or by extract, prepare and model the data with joins and relationships and Tableau Prep, build visualizations with the VizQL engine that translates drag-and-drop into queries and visuals, add analytical depth with calculated fields, level-of-detail expressions, and table calculations, assemble interactive dashboards and stories with actions, and publish and govern them on Tableau Server or Cloud, increasingly augmented by AI through Tableau Pulse and Einstein.](../../../diagrams/volume-154-tableau-certifications/chapter-01-certification-program.svg)

*Figure 1-1. A three-step certification track over the connect-prepare-visualize-share platform.*

## Learning Objectives

- Describe the Tableau certification program — the three-step track and Salesforce ownership.
- Distinguish Desktop Specialist, Certified Data Analyst, and Certified Architect.
- Place the Tableau platform — connect, prepare, visualize, share.
- Recognize Tableau's position in the data-and-analytics landscape.

## What Tableau is

Tableau is the leading **data visualization and business-intelligence (BI)** platform — its purpose is to help people **"see and understand their data"** by turning tables of numbers into interactive visualizations and dashboards that reveal patterns a spreadsheet hides. Where the [Snowflake (XLIX)](../../volume-049-snowflake-certifications/README.md) and [Databricks (XLVIII)](../../volume-048-databricks-certifications/README.md) volumes cover the *data platforms* that store and process data, **Tableau is the *analytics and visualization* layer on top** — where humans actually explore and make decisions from that data. Tableau has been owned by **Salesforce** since 2019, and its newer certifications carry the Salesforce brand.

## The certification track

Tableau's certifications form a clear **three-step progression**:

| Certification | Level | Validates |
|:---|:---|:---|
| **Tableau Desktop Specialist** (a.k.a. Desktop Foundations) | Entry | Connecting to and preparing data; basic visualizations |
| **Salesforce Certified Tableau Data Analyst** | Mid | High proficiency in visualization and analysis |
| **Salesforce Certified Tableau Architect** | Advanced | Enterprise deployment, Server/Cloud architecture, governance |

**Desktop Specialist is the anchor and entry point** — a foundational, affordable credential proving you can connect to data and build visualizations. The **Certified Data Analyst** is the mid-level, most widely-recognized practical credential (with **hands-on labs**, so it validates *doing* analysis, not just recall). The **Architect** is for those who *deploy and govern* Tableau at enterprise scale. The track maps the journey from *using* Tableau to *analyzing* with it to *architecting* it.

## What is published

Tableau (via Salesforce) publishes the exam mechanics:

> **Published:** the **Desktop Specialist** exam is **proctored**, **45 questions**, **60 minutes**, **750 to pass** (on Salesforce's scaled scoring), priced around **$75** — an accessible entry credential. The **Certified Data Analyst** exam is **40–45 questions plus 8–10 hands-on labs** in **120 minutes** — the labs make it a *practical* credential. The Salesforce-branded certifications follow Salesforce's maintenance model (periodic maintenance to stay current). This is a program that publishes its mechanics.

## The platform

Every certification sits on the Tableau workflow — **connect → prepare → visualize → share**:

| Stage | Is | Chapter |
|:---|:---|:---|
| **Connect** | Live or extract connections to data sources | [03](03-connecting-and-preparing-data.md) |
| **Prepare** | Model and shape data (joins, relationships, Tableau Prep) | [03](03-connecting-and-preparing-data.md) |
| **Visualize** | Build charts with VizQL; add calculations | [05](05-building-visualizations.md), [06](06-calculations-lod-and-table-calcs.md) |
| **Share** | Dashboards, then publish to Server/Cloud | [07](07-dashboards-and-interactivity.md), [08](08-sharing-governance-and-the-server.md) |

The lab reads the track and the workflow.

## Hands-On Lab

The labs in this volume model data-visualization and analysis concepts in Python at no cost — Tableau is a GUI tool, so the labs model the *decisions and disciplines* the certifications test (choosing the right chart, dimensions vs measures, level-of-detail calculations). Tableau offers a **free trial** and **Tableau Public** (free).

### Lab 1.1 — Read the certification track

**Objective:** Place a certification by level and what it validates.

```bash
python3 - <<'EOF'
CERTS = [
  # cert,                                level,    validates,                          mechanics
  ("Tableau Desktop Specialist",         "Entry",  "connect + prepare data, basic viz","45Q / 60min / 750 / ~$75 / proctored"),
  ("Salesforce Certified Tableau Data Analyst","Mid","viz + analysis proficiency",     "40-45Q + 8-10 HANDS-ON LABS / 120min"),
  ("Salesforce Certified Tableau Architect","Advanced","enterprise deploy, Server/Cloud, governance","(Salesforce-branded)"),
]
print(f"{'certification':44}{'level':10}validates")
for cert, level, val, mech in CERTS:
    print(f"{cert:44}{level:10}{val}")
    print(f"{'':44}{'':10}  ({mech})")
print("\nThe three-step TRACK:")
print("  DESKTOP SPECIALIST (entry, the anchor) — prove you can connect to data + build")
print("     visualizations. Affordable (~$75), proctored, 45Q/60min/750-to-pass.")
print("  CERTIFIED DATA ANALYST (mid, most recognized) — the PRACTICAL credential: it")
print("     has HANDS-ON LABS, so it validates DOING analysis, not just recall.")
print("  CERTIFIED ARCHITECT (advanced) — for those who DEPLOY + GOVERN Tableau at scale.")
print("\nThe track maps the journey: USING Tableau -> ANALYZING with it -> ARCHITECTING")
print("it. Tableau is SALESFORCE-owned (since 2019), so the mid/advanced certs carry")
print("the Salesforce brand and maintenance model. Start at Desktop Specialist.")
EOF
```

**Expected result:** The three certifications placed on the entry-to-advanced track — Desktop Specialist (connect and visualize), Certified Data Analyst (viz and analysis, with hands-on labs), and Certified Architect (deploy and govern) — under Salesforce ownership. The track lesson is the progression from using to analyzing to architecting Tableau, anchored on the affordable Desktop Specialist.

**Negative test:** Treating the Certified Data Analyst as a multiple-choice recall exam. It includes 8–10 hands-on labs — it validates *performing* analysis in Tableau, which a question bank cannot cover.

**Cleanup:** None.

### Lab 1.2 — Where Tableau fits in the data stack

**Objective:** See Tableau as the analytics/visualization layer on the data platforms.

```bash
python3 - <<'EOF'
STACK = [
  # layer,                  example,                       role
  ("data sources",          "databases, SaaS, files, APIs","where data originates"),
  ("data platform / warehouse","Snowflake, Databricks, BigQuery","store + process at scale"),
  ("data prep / modeling",  "Tableau Prep, dbt",           "shape + clean the data"),
  ("VISUALIZATION / BI",    "TABLEAU  <-- here",            "SEE + understand + decide"),
  ("the decision",          "a human",                     "acts on the insight"),
]
print(f"{'layer':28}{'example':34}role")
for layer, ex, role in STACK:
    print(f"{layer:28}{ex:34}{role}")
print("\nThe insight: the data platforms (Snowflake XLIX, Databricks XLVIII) STORE and")
print("PROCESS data at scale — but data in a warehouse is invisible to a human. Someone")
print("has to turn it into something a person can SEE and UNDERSTAND to make a decision.")
print("\nThat's Tableau's layer: the VISUALIZATION + BI layer where humans actually")
print("explore data and decide. It connects to the platforms below, turns their data")
print("into interactive charts and dashboards, and puts insight in front of people.")
print("'See and understand your data' is the whole pitch — Tableau is the human-facing")
print("end of the data stack, where numbers become decisions. The certs validate the")
print("skills to build that layer well (the RIGHT chart, real analysis, good dashboards).")
EOF
```

**Expected result:** The data stack showing data platforms (Snowflake, Databricks) storing and processing data and Tableau as the visualization/BI layer where humans see, understand, and decide. The positioning lesson is that data in a warehouse is invisible to humans, and Tableau is the human-facing analytics layer that turns it into interactive visualizations for decisions.

**Negative test:** Treating a data warehouse as sufficient for analytics. It stores and processes data but does not make it human-understandable; Tableau is the visualization layer that turns stored data into insight a person can act on.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Tableau program understood as a three-step track (Desktop Specialist → Data Analyst → Architect) under Salesforce.
- [ ] The three certifications distinguished by level and what each validates, with the Data Analyst's hands-on labs noted.
- [ ] The connect-prepare-visualize-share platform workflow placed.
- [ ] Tableau positioned as the visualization/BI layer on the data platforms — where data becomes decisions.
