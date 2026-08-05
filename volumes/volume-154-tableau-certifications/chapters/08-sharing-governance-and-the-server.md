# Chapter 08: Sharing, Governance, and the Server

## Learning Objectives

- Distinguish Tableau Desktop, Server, Cloud, and Public.
- Understand publishing, permissions, and governed data sources.
- Place the certified-data-source and single-source-of-truth idea.
- Recognize AI-driven analytics (Tableau Pulse) as the emerging layer.

*Cert relevance: sharing, governance, and platform architecture are the **Certified Architect** domain — scaling Tableau from one analyst to an organization.*

## The Tableau products

Building a viz in **Tableau Desktop** is one analyst's work; sharing it with an organization needs the **platform**:

| Product | Is |
|:---|:---|
| **Tableau Desktop** | The authoring tool — where analysts build |
| **Tableau Server** | Self-hosted platform to publish, share, and govern content |
| **Tableau Cloud** | The SaaS (Tableau-hosted) version of Server |
| **Tableau Public** | Free public hosting (content is world-visible) |

**Server** and **Cloud** are the enterprise sharing platforms — you **publish** workbooks and data sources to them, and users access dashboards through a browser (no Desktop needed). Cloud is the hosted option (no infrastructure to run); Server is self-hosted (for data-residency or control needs). This is the **Architect's** domain: deploying and scaling the platform. The lab is covered within the governance exercise.

## Publishing, permissions, and governance

Publishing to Server/Cloud raises **governance** questions the Architect certification tests:

- **Permissions** — who can *view*, *edit*, or *download* each workbook and data source, organized by projects/groups. The [least-privilege discipline](../../volume-150-ping-identity-certifications/chapters/08-directory-and-governance.md) applied to analytics content.
- **Governed data sources** — instead of every analyst connecting to raw databases and defining metrics *differently* (three analysts, three definitions of "revenue"), you publish **certified data sources**: curated, documented, trusted datasets with the metrics defined *once*, that everyone builds on. This is the **single source of truth** for the organization's numbers.
- **Content management** — versioning, refresh schedules for extracts, monitoring usage, and ensuring dashboards stay performant at scale.

The core governance idea is **consistency**: without governed data sources, "revenue" means different things in different dashboards, and nobody trusts the numbers; with them, everyone analyzes from the *same* trusted, defined data. The lab models this.

## AI-driven analytics

The emerging layer — reflecting Tableau's Salesforce/Einstein integration — is **AI-driven analytics**. **Tableau Pulse** delivers automated, AI-generated **insights** on key metrics (surfacing trends, anomalies, and drivers in plain language, proactively), and **Ask Data / Explain Data** let users query in natural language and get AI explanations of *why* a value looks the way it does. This is the same [AI-augmentation direction](../../volume-151-sentinelone-certifications/chapters/07-purple-ai-and-the-ai-soc.md) the rest of the shelf shows — AI amplifying the analyst, surfacing insights faster — and it is increasingly certification-relevant. The lab is covered within the governance exercise.

## Hands-On Lab

Python models governance. **Cost:** none.

### Lab 8.1 — Certified data sources: one source of truth

**Objective:** See why governed data sources prevent inconsistent metrics.

```bash
python3 - <<'EOF'
# three analysts each define "revenue" their own way from raw tables
RAW_ORDERS = [{"gross": 1000, "returns": 100, "tax": 80, "discount": 50}]

print("WITHOUT a governed data source — 3 analysts connect to raw tables, each defines")
print("'revenue' differently:\n")
o = RAW_ORDERS[0]
defs = {
  "Analyst A": o["gross"],                                  # gross
  "Analyst B": o["gross"] - o["returns"],                   # net of returns
  "Analyst C": o["gross"] - o["returns"] - o["discount"],   # net of returns + discount
}
for who, val in defs.items():
    print(f"   {who}: 'revenue' = {val}")
print("   -> THREE dashboards, THREE different 'revenue' numbers. In the board meeting,")
print("      three VPs cite three figures. Nobody trusts the data. Chaos.\n")

print("WITH a CERTIFIED data source (revenue defined ONCE, published, everyone uses it):")
certified_revenue = o["gross"] - o["returns"] - o["discount"]   # the agreed definition
print(f"   certified 'Revenue' = gross - returns - discount = {certified_revenue}")
print("   Analyst A, B, C all build on the SAME certified source -> all report", certified_revenue)
print("   -> ONE number, everywhere. The board trusts it.\n")
print("The governance idea: without governed data sources, every analyst reinvents the")
print("metrics from raw tables and 'revenue' means 3 different things — nobody trusts")
print("the numbers. A CERTIFIED data source defines the metrics ONCE (curated,")
print("documented, trusted) and everyone analyzes from it — the SINGLE SOURCE OF TRUTH.")
print("Publishing certified sources + managing PERMISSIONS (who can view/edit/download)")
print("is the Architect's job: scaling Tableau from one analyst to an org where the")
print("numbers are CONSISTENT and GOVERNED. Consistency is the whole point.")
EOF
```

**Expected result:** Three analysts defining "revenue" three different ways from raw tables (chaos in the boardroom) versus a certified data source defining it once so everyone reports the same number. The governance lesson is that governed, certified data sources are the single source of truth — defining metrics once so the organization's numbers are consistent and trusted, which is the Architect's scaling responsibility.

**Negative test:** Letting every analyst connect to raw databases and define metrics themselves. "Revenue" ends up meaning different things in different dashboards and nobody trusts the numbers; a certified data source defines it once for everyone.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Tableau Desktop, Server, Cloud, and Public distinguished by authoring versus sharing versus hosting.
- [ ] Publishing, permissions, and governed/certified data sources understood as the governance layer.
- [ ] The single-source-of-truth idea understood — defining metrics once for organizational consistency.
- [ ] AI-driven analytics (Tableau Pulse, Ask/Explain Data) placed as the emerging, augmenting layer.
