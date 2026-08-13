# Chapter 07: Visual Analytics and BI

## Learning Objectives

- Describe SAS Visual Analytics and the Visual Business Analytics credential.
- Build interactive reports — data items, visualizations, and interactions.
- Add analytics to reports — forecasts, correlations, and what SAS adds over generic BI.
- Understand self-service analytics and its place alongside programming.

*Cert relevance: this is the Visual / BI category — Visual Business Analytics Using SAS Viya.*

## SAS Visual Analytics

Not everyone who uses data writes SAS code. **SAS Visual Analytics** is the **self-service BI** side of Viya — a web tool for **exploring data and building interactive reports and dashboards** by pointing and clicking, no programming required. Business analysts load data, drag fields onto a canvas, choose visualizations, and publish reports that others can interact with. The **Visual Business Analytics Using SAS Viya** credential (A00-470) validates adding and manipulating data items, analyzing data, and designing reports with the tool.

Visual Analytics broadens SAS from a **programmer's** platform to one **analysts** use directly, and it runs on the same **in-memory CAS** engine ([Ch 2](02-the-sas-platform.md)) so reports stay fast on large data. It sits alongside the dedicated BI tools this shelf covers ([Tableau CLIV](../../volume-154-tableau-certifications/README.md), [Qlik CLXI](../../volume-161-qlik-certifications/README.md)) — its edge is being part of an analytics platform with statistics and ML behind it. The lab builds a report.

## Building interactive reports

A Visual Analytics report is assembled from a few concepts:

- **Data items** — the fields from your data, classified as **categories** (dimensions to group by — region, product) or **measures** (numbers to aggregate — sales, count), plus **aggregations** (sum, average) and calculated items.
- **Visualizations** — bar/line/pie charts, tables, maps, and more; you choose the one that answers the question and drag data items onto its roles.
- **Interactions and filters** — link visualizations so selecting a bar filters the rest, add **prompts/filters** so users slice the data, and add **drill-downs** from summary to detail.

The skill is turning a question ("sales by region over time, filterable by product") into the right visualization with the right data-item roles and interactions — the same design thinking as any BI tool, on the SAS platform. The lab assembles data items into a report with a filter.

## Analytics in the report

What distinguishes SAS Visual Analytics from generic dashboarding is the **analytics built in**. Beyond charts, an analyst can add, without code:

- **Forecasting** — project a time series forward with confidence bands.
- **Correlation and relationships** — surface which measures move together.
- **Decision trees / clustering** — lightweight predictive/segmentation analytics inside the report.
- **What-if / goal-seeking** — interactive scenario analysis.

So a report is not just a **rear-view** dashboard; it can include **forward-looking** analytics. This is the payoff of BI **on an analytics platform**: the statistics and ML from the rest of SAS ([Ch 5](05-statistical-analysis.md), [Ch 6](06-machine-learning-on-viya.md)) are available to point-and-click users. The lab adds a forecast to the report.

## Self-service alongside programming

Visual Analytics represents **self-service analytics** — empowering business users to answer their own questions — which **complements** rather than replaces SAS programming. The two work together: **programmers and data scientists** curate data, build models, and prepare trusted data sources; **analysts** explore and report on them in Visual Analytics. A healthy SAS practice uses both: governed, curated data underneath, self-service exploration on top. Knowing where Visual Analytics fits — and its certification — rounds out the SAS skill set beyond code. The lab reflects the division of labor. *(This self-service-on-governed-data pattern mirrors [Qlik (CLXI)](../../volume-161-qlik-certifications/README.md) and [Tableau (CLIV)](../../volume-154-tableau-certifications/README.md).)*

## Hands-On Lab

Python models a Visual Analytics report — data items, a visualization, a filter, and a forecast. **Cost:** none.

### Lab 7.1 — Build an interactive report with a forecast

**Objective:** Assemble data items into a filtered report and add a forecast.

```bash
python3 - <<'EOF'
# SAS Visual Analytics report: data items (category/measure) -> visualization -> filter -> forecast
DATA = [
  {"region":"East","product":"A","month":1,"sales":100},
  {"region":"East","product":"A","month":2,"sales":120},
  {"region":"East","product":"A","month":3,"sales":140},
  {"region":"West","product":"B","month":1,"sales":60},
  {"region":"West","product":"B","month":2,"sales":80},
]
# data items: category = region/product/month, measure = sales (aggregate = SUM)
def report(rows, category, measure, filt=None):
    if filt: rows = [r for r in rows if all(r[k]==v for k,v in filt.items())]
    agg = {}
    for r in rows: agg[r[category]] = agg.get(r[category],0) + r[measure]
    return agg

print("VISUAL ANALYTICS REPORT — data items -> visualization -> filter:\n")
print("   Bar chart: SUM(sales) by region (all data):")
for k,v in report(DATA,"region","sales").items(): print(f"      {k:5} {'#'*(v//20)} {v}")

print("\n   Same report FILTERED to product=A (interaction):")
for k,v in report(DATA,"region","sales",{"product":"A"}).items(): print(f"      {k:5} {v}")

# forecasting (analytics in the report): project East product A sales forward (linear trend)
series = [(1,100),(2,120),(3,140)]
b1 = (series[-1][1]-series[0][1])/(series[-1][0]-series[0][0])   # slope 20/month
b0 = series[0][1] - b1*series[0][0]
print("\n   FORECAST (analytics in the report) — East/A next 2 months:")
for m in (4,5):
    print(f"      month {m}: forecast sales = {b0 + b1*m:.0f}")
print()
print("A report assembles DATA ITEMS (category=region, measure=SUM(sales)) into a VISUALIZATION,")
print("with FILTERS/interactions (product=A). Unlike generic dashboards, SAS Visual Analytics adds")
print("ANALYTICS in the report — a FORECAST projects the trend forward. Self-service on the same")
print("in-memory platform as SAS's statistics and ML — the Visual Business Analytics credential.")
EOF
```

**Expected result:** A report aggregating sales by region from data items, the same report filtered to one product, and a forecast projecting a series forward. The lesson is self-service BI in SAS: assemble data items into visualizations with filters and interactions, and add built-in analytics (forecasting) that generic dashboards lack — the Visual Business Analytics competency, on the same analytics platform as SAS's statistics and ML.

**Negative test:** Treating Visual Analytics as only a static dashboard and exporting numbers to another tool for any analysis. You lose the built-in forecasting/analytics and the governed, in-memory data; SAS Visual Analytics puts analytics in the report itself, on trusted data.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SAS Visual Analytics understood — self-service, web-based interactive reporting on CAS.
- [ ] Building reports understood — data items (category/measure), visualizations, interactions, and filters.
- [ ] Analytics in the report understood — forecasting, correlations, and lightweight predictive analytics without code.
- [ ] Self-service alongside programming understood — analysts explore governed data curated by programmers.

## See also

- [Chapter 02 — The SAS Platform and Language](02-the-sas-platform.md) — the CAS engine reports run on.
- [Volume CLIV — Tableau](../../volume-154-tableau-certifications/README.md) and [Volume CLXI — Qlik](../../volume-161-qlik-certifications/README.md) — dedicated visual-analytics peers.
- [Chapter 09 — Choosing Your SAS Path](09-choosing-your-sas-path.md) — where the analyst path fits.
