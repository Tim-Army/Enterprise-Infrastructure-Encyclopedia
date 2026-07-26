# Chapter 05: Data and AI Certifications — Data+, DataSys+, and DataAI

## Learning Objectives

- Enumerate the CompTIA data certifications and their current exam codes.
- Distinguish the data-analyst (Data+), data-systems (DataSys+), and advanced (DataAI) roles.
- Describe CompTIA's AI Essentials microcredential line.
- Map the data certifications to the encyclopedia's data and cloud volumes.
- Build a study path for a data or AI-oriented professional.

## Theory and Architecture

CompTIA's **Data and AI** credentials certify analysis, data infrastructure,
and the fast-growing AI skill areas. As verified on comptia.org (26 July
2026):

- **CompTIA Data+** — exam **DA0-002** (V2; DA0-001 retiring) across five
  weighted domains: **Data concepts and environments (20%)**, **Data acquisition
  and preparation (22%)**, **Data analysis (24%)**, **Visualization and
  reporting (20%)**, and **Data governance (14%)** — V2 adds AI concepts (AI
  models, NLP, robotic automation). A 90-question exam (multiple-choice and
  performance-based) over 90 minutes with a **scaled passing score of 675
  (100–900)**; 18–24 months as a data analyst recommended. The **data-analyst**
  credential for turning data into insight — vendor-neutral, complementing tools
  like Power BI (Microsoft PL-300).
- **CompTIA DataSys+** — exam **DS0-001** (V1) across five weighted domains:
  **Database fundamentals (24%)**, **Database deployment (16%)**, **Database
  management and maintenance (25%)**, **Data and database security (23%)**, and
  **Business continuity (12%)**. A 90-question exam (multiple-choice and
  performance-based) over 90 minutes with a **scaled passing score of 700
  (100–900)**; 2–3 years as a database administrator recommended. The
  **database-administrator** credential.
- **CompTIA DataAI (formerly DataX)** — exam **DY0-001** (V1, launched 25 July
  2024). CompTIA's **advanced, expert-level data-science and AI** credential
  (the renamed **DataX**), for senior professionals with roughly **5+ years** of
  experience. It is a **pass/fail** exam of up to **90 questions**
  (multiple-choice and performance-based) over **165 minutes**, offered in
  English and Japanese, and is expected to retire around 2027. Its five weighted
  domains are **Mathematics and statistics (17%)**, **Modeling, analysis, and
  outcomes (24%)**, **Machine learning (24%)**, **Operations and processes
  (22%)**, and **Specialized applications of data science (13%)** — spanning
  statistical and linear-algebra methods, exploratory analysis and model
  iteration, supervised/tree-based/deep/unsupervised learning, the data-science
  life cycle with MLOps and deployment, and specialized areas such as NLP,
  computer vision, and optimization.

Alongside the exam-based data certs, CompTIA offers a broad **AI Essentials**
microcredential line — **AI Essentials**, **AI Fundamentals**, **AI Prompting
Essentials**, **AI Agent Essentials**, **Copilot 365 Essentials**, and
role-specific AI essentials (marketing, sales, help desk, customer support,
agent) — short courses that build foundational, practical AI literacy for a wide
audience. These are **hands-on courses validated by a CompTIA "CompCert"
(Competency Certificate) assessment** rather than proctored coded exams. Most
are short (roughly 2–8 hours) — **AI Agent Essentials**, for example, is a 4–5
hour course on agentic systems (agent workflows, tool and memory management,
guardrails, and human oversight) with practice in CompTIA's proprietary **Agent
Simulator**. The exception is **AI Fundamentals**, a much larger **three-credit
academic course (~50–56 hours)** aimed at institutions and non-technical student
populations, with AI labs and auto-graded feedback. The security-focused AI
certification **SecAI+** (Expansion Series, Chapter 06) sits above this literacy
tier.

## Design Considerations

Choose by role. **Data+** is the entry data-analyst credential; **DataSys+** is
for database administrators; **DataAI** (ex-DataX) is the advanced,
senior-level data-and-AI credential for experienced professionals. The **AI
Essentials** line is deliberately broad and foundational — good for
upskilling non-specialists and building AI literacy across a team, not a
substitute for the deeper data or AI engineering credentials of the cloud
vendors (Azure/AWS/GCP).

Pair CompTIA's vendor-neutral data credentials with the vendor data
certifications elsewhere in the encyclopedia: **Data+** with Microsoft
**PL-300** (Power BI) and the cloud analytics tracks, and **DataSys+** with the
cloud database certifications (Azure DP-300, AWS Database). CompTIA teaches the
vendor-neutral fundamentals those platform certs then apply.

## Implementation and Automation

Verify the data codes and the DataX → DataAI rename from comptia.org:

```bash
for slug in data datasys dataai; do
  code=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '\b(DA0-[0-9]{3}|DS0-[0-9]{3}|DY0-[0-9]{3})\b' | sort -u | tr '\n' ' ')
  title=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '<title>[^<]*</title>' | head -1)
  echo "$slug -> ${code:-see page} | $title"
done
# data -> DA0-002 ; datasys -> DS0-001 ; dataai -> DY0-001 (formerly DataX)
```

## Validation and Troubleshooting

Map the data certifications:

| Certification | Exam | Role | Complements |
| --- | --- | --- | --- |
| Data+ | DA0-002 | Data analyst | Microsoft PL-300; cloud analytics |
| DataSys+ | DS0-001 | Database administrator | Azure DP-300; AWS Database |
| DataAI (ex-DataX) | DY0-001 | Advanced data/AI (5+ yrs) | Cloud AI/ML certs |
| AI Essentials line | microcredentials | Broad AI literacy | — |

Common pitfalls: studying **Data+ DA0-001** instead of the current **DA0-002**;
looking for **DataX** by name (now **DataAI**); and treating the **AI
Essentials** microcredentials as equivalent to the deeper data-analyst or
cloud AI-engineering certifications — they are foundational literacy
credentials, valuable but different in scope.

## Security and Best Practices

Verify the **current exam versions** (Data+ moved to DA0-002; DataX became
DataAI). Choose the credential by role — analyst (Data+), DBA (DataSys+),
advanced (DataAI) — and use the **AI Essentials** line to build broad,
practical AI literacy across a team. Pair CompTIA's vendor-neutral data
credentials with the vendor data and AI certifications for platform depth, and
apply the **data governance and security** concepts (which Data+ and DataSys+
both cover) to real controls. Plan **CE renewal** (Chapter 08).

## References and Knowledge Checks

- comptia.org: certification pages for Data+, DataSys+, DataAI, and the AI Essentials line.
- Cross-reference: [Volume XXXVIII — Microsoft Certifications Beyond Azure](../volume-38-microsoft-certifications-beyond-azure/README.md) (PL-300, DP family).

**Knowledge checks**

1. What is the current Data+ exam code, and which version did it replace?
2. What was DataAI previously called?
3. How do the AI Essentials microcredentials differ from the data-analyst and cloud AI certifications?

## Hands-On Lab

Exam-preparation walkthroughs for the data and AI certifications.

**Shared prerequisites for Labs 5.1–5.2** — a browser and `curl`. **Cost:** none.

### Lab 5.1 — Confirm the data codes and DataX rename (Topic: Verify currency)

**Objective:** Prove Data+ DA0-002 and the DataAI rename.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/data/" \
  | grep -oE '\bDA0-[0-9]{3}\b' | sort -u
curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/dataai/" \
  | grep -oE '\bDY0-[0-9]{3}\b' | sort -u
```

**Expected result:** **DA0-002** for Data+, and **DY0-001** for DataAI (whose
page notes *formerly DataX*) — the current data-analyst exam and the advanced
credential's code and rename.

**Negative test:** search for "DataX" as a current credential; it is renamed to
DataAI — verify on the page.

**Cleanup:** none.

### Lab 5.2 — Plan a data path (Topic: Study plan)

**Objective:** Sequence the data credentials for an analyst-to-advanced route.

```text
(Core: Tech+/A+ groundwork)
  -> Data+ (DA0-002)        data analyst
  -> DataSys+ (DS0-001)     database administration (if infrastructure-focused)
  -> DataAI (ex-DataX)      advanced data/AI (experienced)
AI literacy: AI Essentials line. Vendor depth: Microsoft PL-300, cloud data certs.
```

**Expected result:** a Data+ → DataSys+/DataAI path with an AI-literacy branch,
tied to the vendor data certifications.

**Negative test:** substitute an AI Essentials microcredential for Data+ on a
data-analyst resume; it proves literacy, not analyst competency — use the right
credential for the role.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CompTIA's data credentials run Data+ (DA0-002, analyst), DataSys+ (DS0-001,
DBA), and the advanced DataAI (DY0-001, formerly DataX), plus a broad AI
Essentials microcredential line. They are vendor-neutral fundamentals that pair with the
vendor data and AI certifications for platform depth.

- [ ] I can list the data certs and current exam codes.
- [ ] I know DataX is now DataAI and Data+ is DA0-002.
- [ ] I can place the AI Essentials line correctly in scope.
- [ ] I can build a data/AI study path with vendor pairings.
- [ ] I completed Labs 5.1–5.2 including each negative test.
