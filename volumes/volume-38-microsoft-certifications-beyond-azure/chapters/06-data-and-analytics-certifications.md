# Chapter 06: Data and Analytics Certifications

## Learning Objectives

- Enumerate the current DP-family certifications and exam codes.
- Explain the shift to Microsoft Fabric (DP-700, DP-600) and where DP-203 went.
- Distinguish the data engineer, analyst, scientist, and database roles.
- Recognize the newer DP additions — Databricks (DP-750) and AI-enabled databases (DP-800).
- Build a study path for a data engineer or analyst role.

## Theory and Architecture

The **DP** family certifies data roles across **Microsoft Fabric**, **Azure
databases**, and **Power BI**. The big recent shift is **Microsoft Fabric**,
the unified analytics platform that absorbed much of what used to be separate
Azure Synapse and Data Factory certification scope. As verified on Microsoft
Learn (26 July 2026):

- **Microsoft Certified: Azure Data Fundamentals** — exam **DP-900**
  (Fundamentals). Core data concepts and Azure/Fabric data services.
- **Microsoft Certified: Fabric Data Engineer Associate** — exam **DP-700**
  (Associate). Ingest, transform, and serve data in Microsoft Fabric. This is
  the successor to the retired **DP-203** (Azure Data Engineer).
- **Microsoft Certified: Fabric Analytics Engineer Associate** — exam
  **DP-600** (Associate). Design and build analytics solutions in Fabric,
  including semantic models and Power BI.
- **Microsoft Certified: Azure Database Administrator Associate** — exam
  **DP-300** (Associate). Manage SQL Server and Azure SQL databases.
- **Microsoft Certified: Azure Cosmos DB Developer Specialty** — exam
  **DP-420** (Specialty). Build applications on Azure Cosmos DB.
- **Microsoft Certified: Azure Data Scientist Associate** — exam **DP-100**
  (Associate). Machine learning with Azure Machine Learning.
- **Microsoft Certified: Azure Databricks Data Engineer Associate** — exam
  **DP-750** (Associate). Data engineering on Azure Databricks — a newer
  credential reflecting the Databricks partnership.
- A newer **AI-enabled database solutions** credential — exam **DP-800** —
  bridging databases and generative AI.

**Power BI Data Analyst (PL-300)** lives in the Power Platform family
(Chapter 04) but belongs to any data professional's toolkit.

## Design Considerations

Lead with **DP-900** for the vocabulary, then choose by role. **Data
engineers** target **DP-700** (Fabric) — and note that if a study plan cites
**DP-203**, it is out of date; Fabric's DP-700 replaced it. **Analytics
engineers** take **DP-600** and typically **PL-300** for Power BI depth.
**Database administrators** take **DP-300**; **Cosmos DB** developers take the
**DP-420** specialty; and **data scientists** take **DP-100**. The newer
**DP-750** (Databricks) and **DP-800** (AI-enabled databases) reflect where
the platform is heading — lakehouse engineering and database-plus-GenAI.

Because Fabric, Power BI, and AI overlap, plan across families: an analytics
engineer might hold **DP-600 + PL-300**, and a data-plus-AI engineer might add
**DP-800** or the AI family's data-science credentials (Chapter 07).

## Implementation and Automation

Verify the Fabric shift and newer additions from Microsoft Learn:

```bash
for slug in azure-data-fundamentals fabric-data-engineer-associate fabric-analytics-engineer-associate \
            azure-database-administrator-associate azure-cosmos-db-developer-specialty azure-data-scientist \
            implementing-data-engineering-solutions-using-azure-databricks; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bDP-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# fabric-data-engineer-associate -> DP-700 (replaced DP-203)
# ...-azure-databricks -> DP-750
```

## Validation and Troubleshooting

Map credentials to roles:

| Credential | Exam | Tier | Role |
| --- | --- | --- | --- |
| Azure Data Fundamentals | DP-900 | Fundamentals | Gateway |
| Fabric Data Engineer | DP-700 | Associate | Data engineer (ex-DP-203) |
| Fabric Analytics Engineer | DP-600 | Associate | Analytics engineer |
| Azure Database Administrator | DP-300 | Associate | DBA |
| Azure Cosmos DB Developer | DP-420 | Specialty | NoSQL developer |
| Azure Data Scientist | DP-100 | Associate | Data scientist |
| Azure Databricks Data Engineer | DP-750 | Associate | Lakehouse engineer |
| AI-enabled database solutions | DP-800 | Associate | Data + GenAI |

Common pitfalls: studying **DP-203** (retired — Fabric's **DP-700** is
current); confusing **DP-600** (analytics engineering) with **DP-700** (data
engineering) — they are distinct Fabric roles; and missing the newer
**DP-750** and **DP-800**. As always, confirm on Learn — the data family has
moved fastest of all into Fabric and AI.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
practice in a **Microsoft Fabric trial** and **Azure** free account. Verify
the **Fabric transition** (DP-700 over DP-203) and the newer **DP-750/DP-800**
before planning. Pair analytics credentials with **PL-300** (Power BI) and
data-science credentials with the **AI** family (Chapter 07). Renew annually
through the free assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for DP-900, DP-700, DP-600, DP-300, DP-420, DP-100, DP-750, DP-800.
- Cross-reference: [Chapter 07 — AI and Copilot](07-ai-and-copilot-certifications.md); [Volume XXXIII](../volume-33-microsoft-azure-certifications/README.md).

**Knowledge checks**

1. Which Fabric exam replaced the retired DP-203, and what role does it certify?
2. How do DP-600 and DP-700 differ?
3. What do the newer DP-750 and DP-800 reflect about the platform?

## Hands-On Lab

Exam-preparation walkthroughs for the data family.

**Shared prerequisites for Labs 6.1–6.2** — a browser; `curl` for Lab 6.1.
**Cost:** none.

### Lab 6.1 — Confirm the Fabric transition (Topic: Verify currency)

**Objective:** Prove DP-700 is the current data-engineering exam.

```bash
curl -s "https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/" \
  | grep -oE '\bDP-[0-9]{3}\b' | sort -u
```

**Expected result:** **DP-700** — the Fabric Data Engineer exam that replaced
DP-203.

**Negative test:** search for a "DP-203" certification page; it is retired —
do not study the old Synapse-era exam.

**Cleanup:** none.

### Lab 6.2 — Plan a data-engineering path (Topic: Study plan)

**Objective:** Sequence for a Fabric data engineer.

```text
DP-900 (Fundamentals)
  -> DP-700 (Fabric Data Engineer) as the core role
  -> DP-600 (Fabric Analytics Engineer) + PL-300 (Power BI) for analytics depth
  -> DP-750 (Databricks) or DP-800 (AI-enabled databases) for specialization.
```

**Expected result:** a Fundamentals→Associate path centred on Fabric with a
specialization branch.

**Negative test:** build a plan around DP-203; it is retired — anchor on
DP-700.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The DP family runs DP-900 (Fundamentals), the Fabric pair DP-700 (Data
Engineer, replacing DP-203) and DP-600 (Analytics Engineer), DP-300 (DBA),
DP-420 (Cosmos DB Specialty), DP-100 (Data Scientist), and the newer DP-750
(Databricks) and DP-800 (AI-enabled databases). Power BI depth comes from
PL-300. The family has moved decisively into Fabric and AI.

- [ ] I can list the DP credentials and exam codes.
- [ ] I know DP-700 replaced DP-203 and how DP-600 differs.
- [ ] I recognize the newer DP-750 and DP-800.
- [ ] I can build a data-engineering study path on Fabric.
- [ ] I completed Labs 6.1–6.2 including each negative test.
