# Chapter 07: Pentaho — Data Integration and Analytics

## Learning Objectives

- Describe Pentaho and its place in the Hitachi Vantara portfolio.
- Explain Pentaho Data Integration (PDI) — ETL transformations and jobs.
- Describe Pentaho Business Analytics — reporting, dashboards, and analysis.
- Understand where Pentaho fits alongside Hitachi's storage.

*Cert relevance: this is the Pentaho track — Data Integration and Business Analytics.*

## Pentaho in the portfolio

Hitachi Vantara is not only storage — it also owns **Pentaho**, a **data integration and business-analytics** platform. This is the **software/data** side of the portfolio: where the storage products **hold** data, Pentaho **moves, transforms, and analyzes** it. Pentaho has two halves — **Pentaho Data Integration (PDI)** for **ETL/data pipelines** and **Pentaho Business Analytics** for **reporting and dashboards** — and its own certification track (Data Integration and Business Analytics).

Pentaho reflects Hitachi Vantara's positioning as a **data infrastructure** company: the whole data lifecycle from the storage that holds it to the pipelines that prepare it and the analytics that make it useful. It sits alongside the data-integration and BI platforms this shelf covers ([Informatica CLXV](../../volume-165-informatica-certifications/README.md), [Tableau CLIV](../../volume-154-tableau-certifications/README.md)). The lab maps Pentaho's halves.

## Pentaho Data Integration (PDI)

**Pentaho Data Integration (PDI)**, historically known as **Kettle**, is Pentaho's **ETL** tool — it **extracts** data from sources, **transforms** it, and **loads** it into targets. Its model:

- **Transformations** — a **data flow** of **steps** connected by "hops": input steps read data (files, databases, APIs), transform steps reshape it (filter, join, calculate, look up, sort), and output steps write it. Data flows through the steps row by row.
- **Jobs** — **orchestrate** transformations and other tasks (run this transformation, then that one, send a notification, handle errors) with sequencing and conditions.
- **Visual designer (Spoon)** — build transformations and jobs **visually**, dragging steps onto a canvas — low-code ETL.

So PDI is **transformation (what to do to the data) + job (orchestrate the flow)**, built visually. This is the same ETL discipline as dedicated integration platforms, and it is what the Pentaho Data Integration certification tests. The lab builds a PDI transformation. *(PDI's transform/job model parallels [Informatica's mapping/taskflow (CLXV Ch 3)](../../volume-165-informatica-certifications/chapters/03-cloud-data-integration.md).)*

## Pentaho Business Analytics

The **Business Analytics** side turns prepared data into **insight**:

- **Reporting** — pixel-perfect and ad-hoc **reports** over the data.
- **Dashboards** — interactive **dashboards** combining charts, KPIs, and filters for business monitoring.
- **Analysis (OLAP)** — **multidimensional** analysis (slice and dice by dimensions — time, region, product) over cubes for exploratory analytics.
- **Data visualization** — charts and visual exploration.

Business Analytics is the **consumption** layer — where business users see and explore the data that PDI prepared. Together, **PDI feeds Business Analytics**: pipelines land clean, integrated data, and analytics presents it. Knowing both halves — and how they connect — is the Pentaho competency. The lab builds a report over PDI output.

## Pentaho alongside storage

Pentaho's presence in Hitachi Vantara means the company spans **infrastructure and data software**, and the two connect: Pentaho pipelines can **integrate data across systems**, including data on Hitachi storage, and **object storage** ([Ch 4](04-file-and-object-storage.md)) is a natural landing zone for the large datasets analytics consumes. For a certification candidate, Pentaho is a **distinct track** from storage — a different skill set (data engineering/analytics rather than storage administration) — but part of the same portfolio. Understanding that Hitachi Vantara certifications span **both storage and data** helps you choose a path ([Ch 9](09-choosing-your-hitachi-vantara-path.md)). The lab connects a pipeline to analytics.

## Hands-On Lab

Python models a PDI transformation, a job, and a Business Analytics report. **Cost:** none.

### Lab 7.1 — Build a PDI pipeline and a report

**Objective:** Run an ETL transformation, orchestrate it in a job, and report on the output.

```bash
python3 - <<'EOF'
# Pentaho Data Integration (PDI): a TRANSFORMATION = input -> transform steps -> output
SOURCE = [
  {"order":1,"region":"East","amount":"120","status":"paid"},
  {"order":2,"region":"West","amount":"80", "status":"paid"},
  {"order":3,"region":"East","amount":"200","status":"cancelled"},
]
def pdi_transformation(rows):
    # step: filter (keep paid) -> step: calculate (amount to number + tax) -> step: output
    out = []
    for r in rows:
        if r["status"] != "paid": continue                  # Filter Rows step
        out.append({"order":r["order"],"region":r["region"],
                    "amount":int(r["amount"]),"amount_tax":round(int(r["amount"])*1.08,2)})  # Calculator step
    return out
staged = pdi_transformation(SOURCE)
print("PENTAHO DATA INTEGRATION (PDI) — transformation (input -> filter -> calc -> output):")
for r in staged: print(f"   {r}")

# PDI JOB: orchestrate (run transformation, then load, then notify)
job = ["start", "run transformation t_orders", "load to warehouse", "email on success"]
print(f"\nPDI JOB (orchestration): {' -> '.join(job)}")

# Pentaho Business Analytics: report/dashboard over the prepared data
def report(rows):
    agg = {}
    for r in rows: agg[r["region"]] = agg.get(r["region"],0) + r["amount_tax"]
    return agg
print("\nPENTAHO BUSINESS ANALYTICS (report — taxed sales by region):")
for region, total in report(staged).items(): print(f"   {region:5} {total}")
print()
print("PDI runs a TRANSFORMATION (input -> Filter paid -> Calculator taxed amount -> output),")
print("orchestrated by a JOB (run transform -> load -> notify) — visual, low-code ETL. Pentaho")
print("BUSINESS ANALYTICS then reports/dashboards over the prepared data (taxed sales by region).")
print("PDI feeds Business Analytics: pipelines prepare, analytics presents — the Pentaho track.")
EOF
```

**Expected result:** A PDI transformation filtering to paid orders and calculating a taxed amount, a job orchestrating it, and a Business Analytics report aggregating by region. The lesson is Pentaho: Data Integration (PDI) builds visual ETL transformations orchestrated by jobs, and Business Analytics reports and dashboards over the prepared data — PDI feeds analytics, the two halves of the Pentaho track and the data-software side of Hitachi Vantara.

**Negative test:** Reporting directly on the raw source without the PDI transformation. Cancelled orders and string amounts corrupt the totals; the ETL transformation (filter, type-convert, calculate) is what prepares clean, correct data for the analytics to present.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Pentaho placed — Hitachi Vantara's data-integration and business-analytics platform.
- [ ] PDI understood — transformations (visual ETL steps) and jobs (orchestration), the Kettle heritage.
- [ ] Business Analytics understood — reporting, dashboards, and OLAP analysis over prepared data.
- [ ] Pentaho alongside storage understood — a distinct data track within the storage-plus-data portfolio.

## See also

- [Chapter 04 — File and Object Storage](04-file-and-object-storage.md) — object storage as a landing zone for analytics data.
- [Volume CLXV — Informatica](../../volume-165-informatica-certifications/README.md) — a data-integration peer (mapping/taskflow model).
- [Volume CLIV — Tableau](../../volume-154-tableau-certifications/README.md) — a visual-analytics peer.
