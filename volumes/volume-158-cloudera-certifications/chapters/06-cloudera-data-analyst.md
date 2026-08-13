# Chapter 06: Cloudera Data Analyst

## Learning Objectives

- Explain the Data Analyst role — querying and visualizing data on CDP.
- Describe the Cloudera Data Warehouse (Hive, Impala).
- Understand Cloudera Data Visualization.
- Recognize the role of governance (Ranger, Atlas) for analysts.

*Cert relevance: the Cloudera Data Analyst certification validates SQL analytics and visualization on CDP.*

## The data analyst role

The **Cloudera Data Analyst** turns data into **insight** — querying curated datasets, analyzing them, and building visualizations and reports that answer business questions. Where engineers and operators *move and prepare* data, the analyst *consumes* it: writing SQL against the **Cloudera Data Warehouse**, exploring with **Cloudera Data Visualization**, and working within the governance the platform enforces. The certification covers **Data Warehouse** and **Data Visualization** products plus **Hive, Impala, Ranger, and Atlas**. This is the consumption/insight end of the platform — the payoff of all the data engineering and operations. The lab models analysis.

## The Cloudera Data Warehouse (Hive, Impala)

The **Cloudera Data Warehouse** provides **SQL analytics** at scale over the platform's data. Its engines:

- **Apache Hive** — SQL over large datasets, strong for **batch** and heavy ETL-style queries.
- **Apache Impala** — a **massively parallel** SQL engine built for **fast, interactive** queries — low-latency analytics for exploration and dashboards.

The analyst writes **SQL** (the universal language of data analysis) against warehouse tables, choosing the right engine for the job — Impala for interactive exploration, Hive for heavy batch. Because the warehouse runs on the shared platform, the analyst queries the **same governed data** engineers produce, without copying it elsewhere. The lab models querying.

## Cloudera Data Visualization

**Cloudera Data Visualization** lets analysts build **dashboards and visualizations** directly on CDP data — charts, reports, and interactive dashboards that communicate insight to business users. It is the **visualization layer** native to the platform, analogous to the [BI tools the Tableau volume (CLIV)](../../volume-154-tableau-certifications/README.md) covers, but integrated into CDP so visualizations run on **governed, in-platform data** without extracting it to a separate BI tool. Turning query results into a clear picture — the right chart for the question — is the analyst's communication skill. The lab models visualization choices.

## Governance for analysts

Analysts work **within governance** — and this matters to the certification. Because CDP enforces [SDX (Ranger/Atlas), Chapter 2](02-the-cloudera-data-platform.md):

- **Ranger** controls **what the analyst can query** — column- and row-level access, so an analyst sees only the data their role permits (e.g., masked or hidden sensitive columns).
- **Atlas** provides **lineage and a catalog** — the analyst can see where a dataset came from and trust its provenance, and discover data through the catalog.

For an analyst, governance is not an obstacle but an **enabler**: it lets them work with real enterprise data safely and find and trust the right datasets. The lab models governed analysis.

## Hands-On Lab

Python models governed SQL analysis and visualization. **Cost:** none.

### Lab 6.1 — Governed SQL analysis and the right visualization

**Objective:** Query governed data (Ranger) and choose a fit-for-purpose chart.

```bash
python3 - <<'EOF'
# analyst queries the warehouse; Ranger enforces column access; pick the right engine + chart
COLUMNS = {"order_id": "public", "region": "public", "revenue": "public", "customer_ssn": "PII-restricted"}
analyst_roles = {"role:analyst"}
def visible(col):
    return "PII-restricted" not in COLUMNS[col] or "role:compliance" in analyst_roles

print("Data Analyst queries the Cloudera Data Warehouse (Ranger-governed):\n")
print("   SELECT region, SUM(revenue) FROM orders GROUP BY region;")
print("   engine: IMPALA (interactive, low-latency -> good for exploration/dashboards)\n")
print("   Ranger column visibility for role:analyst:")
for col in COLUMNS:
    print(f"      {col:14} {'VISIBLE' if visible(col) else 'BLOCKED (PII — masked/denied)'}")
print("   -> analyst can aggregate revenue by region, but customer_ssn is DENIED\n")
# results -> choose the right visualization
regions = {"North": 420, "South": 380, "East": 510, "West": 290}
print("   result -> Cloudera Data Visualization: choose the RIGHT chart:")
print("      comparing revenue across 4 regions -> BAR chart (accurate length comparison)")
best = max(regions, key=regions.get)
for r, v in sorted(regions.items(), key=lambda x:-x[1]):
    bar = "#" * (v // 20)
    print(f"        {r:6} {bar} {v}")
print(f"      insight: {best} leads; a bar chart shows it at a glance (not a pie).\n")
print("The Data Analyst turns governed data into INSIGHT: SQL on the Data Warehouse (IMPALA")
print("interactive vs HIVE batch), visualized in Cloudera Data Visualization. Crucially, they")
print("work WITHIN governance — RANGER controls which columns they see (PII stays hidden),")
print("ATLAS gives lineage to TRUST the data. Governance is an ENABLER: safe access to real")
print("enterprise data + discoverable, trustworthy datasets. Then: the RIGHT chart per question.")
EOF
```

**Expected result:** An analyst running an Impala aggregation where Ranger blocks the PII column but permits the revenue-by-region query, then choosing a bar chart to compare regions. The data-analyst lesson is that the role turns governed data into insight — SQL on the Data Warehouse (Impala for interactive, Hive for batch), visualized in Cloudera Data Visualization — working within SDX governance where Ranger controls column access and Atlas provides trustworthy lineage, with governance an enabler of safe access to real data.

**Negative test:** Extracting warehouse data to a separate spreadsheet or BI tool to bypass governance. That loses Ranger's access controls and Atlas's lineage, risking exposure of restricted data and untrustworthy analysis; analysts query governed data in-platform and visualize it there.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The data-analyst role understood — querying and visualizing data to produce insight.
- [ ] The Cloudera Data Warehouse understood — Hive (batch) and Impala (interactive) SQL engines.
- [ ] Cloudera Data Visualization understood — dashboards on governed, in-platform data.
- [ ] Governance (Ranger access, Atlas lineage) recognized as an enabler of safe, trustworthy analysis.
