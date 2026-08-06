# Chapter 03: Qlik Sense and Qlik Cloud

## Learning Objectives

- Explain Qlik Sense and the client-managed versus Qlik Cloud deployments.
- Describe apps, sheets, and stories.
- Understand master items and governed self-service.
- Recognize the platform structure the certifications assume.

*Cert relevance: Qlik Sense and Qlik Cloud are the platform every certification operates on.*

## Qlik Sense: client-managed and Qlik Cloud

**Qlik Sense** is Qlik's modern analytics application — where users build and consume **apps** (interactive analytics applications). It comes in two deployment models, and the [certifications are platform-neutral (Ch 1)](01-the-qlik-program.md) across both:

- **Client-managed Qlik Sense** — you host and manage it yourself (**Qlik Sense Enterprise** on your servers/cloud), governed through the [Qlik Management Console (Ch 7)](07-system-administrator.md). Full control, your infrastructure.
- **Qlik Cloud** — Qlik's **SaaS** platform: Qlik hosts and manages it, you consume it as a service. Simpler to adopt, always current, and the strategic direction for most new deployments.

Both run the same [associative engine (Ch 2)](02-the-associative-model.md) and build the same apps; the difference is **who operates the infrastructure**. The lab models the deployment choice.

## Apps, sheets, and stories

A Qlik Sense **app** is the unit of analytics, containing:

- **The data model** — data loaded and associated in memory ([the Data Architect's work, Ch 4](04-data-architect.md)).
- **Sheets** — the pages of an app, each holding **visualizations** (charts, tables, KPIs) that the user interacts with.
- **Stories** — curated, presentation-style narratives built from **snapshots** of visualizations, for communicating findings to an audience (Qlik's guided-storytelling feature).

A user opens an app, interacts with its sheets (making selections that the associative engine responds to), and can build stories to share insight. Understanding the app → sheets → visualizations structure is foundational for the [Business Analyst (Ch 5)](05-business-analyst.md). The lab models app structure.

## Master items and governed self-service

A key concept is **master items** — centrally-defined, **reusable** dimensions, measures, and visualizations that app creators define **once** and reuse everywhere. Master items deliver **governed self-service**: business users can build their own analyses freely, but using **consistent, approved** definitions (a "Revenue" measure defined once means everyone's "Revenue" agrees). This balances the two forces in analytics — **self-service freedom** and **governance/consistency** — the same tension the [certified-data-source discipline of Tableau (CLIV)](../../volume-154-tableau-certifications/README.md) addresses. Master items are how Qlik keeps self-service from becoming inconsistent chaos. The lab models master items.

## The platform structure

The certifications assume fluency in the platform's structure: **apps** containing a **data model** and **sheets** of **visualizations**, built with **master items** for consistency, deployed **client-managed or in Qlik Cloud**, and governed through streams and spaces. The **Business Analyst** builds this, the **Data Architect** provides the data model beneath it, and the **System Administrator** deploys and governs it — three roles on one platform. The lab synthesizes.

## Hands-On Lab

Python models the app structure and master items. **Cost:** none.

### Lab 3.1 — App structure and governed master items

**Objective:** See the app → sheets → visualizations structure and master-item consistency.

```bash
python3 - <<'EOF'
# a Qlik Sense app: data model + sheets of visualizations + master items for governance
app = {
  "name": "Sales Analytics",
  "deployment": "Qlik Cloud (SaaS)  [or client-managed Enterprise — same app]",
  "data_model": "associative model (Country<->Product<->Customer<->Sales)",
  "master_items": {
    "measure:Revenue": "Sum(Sales)      # defined ONCE, reused everywhere",
    "dimension:Region": "Country grouped -> Region",
  },
  "sheets": {
    "Overview": ["KPI: Revenue", "Bar: Revenue by Region", "Line: Revenue over time"],
    "Detail":   ["Table: sales rows", "Pie: Revenue by Product"],
  },
}
print(f"Qlik Sense APP: {app['name']}  ({app['deployment']})\n")
print(f"   data model: {app['data_model']}\n")
print("   MASTER ITEMS (governed, reusable definitions):")
for k, v in app["master_items"].items():
    print(f"      {k:18} = {v}")
print("\n   SHEETS (pages of visualizations):")
for sheet, viz in app["sheets"].items():
    print(f"      [{sheet}] {viz}")
# governance: two analysts both use the SAME master 'Revenue' -> consistent numbers
print("\n   Governed self-service check:")
print("      analyst A's 'Revenue' = master Sum(Sales)")
print("      analyst B's 'Revenue' = master Sum(Sales)")
print("      -> SAME definition -> their numbers AGREE (no 'my revenue vs your revenue' chaos)\n")
print("A Qlik Sense APP = a DATA MODEL + SHEETS of VISUALIZATIONS + STORIES (snapshot narratives).")
print("It runs the SAME on CLIENT-MANAGED (you host, QMC-governed) or QLIK CLOUD (SaaS) — the")
print("certs are platform-neutral. ★ MASTER ITEMS = centrally-defined reusable dims/measures/viz")
print("= GOVERNED SELF-SERVICE: users build freely but on CONSISTENT, APPROVED definitions, so")
print("everyone's 'Revenue' agrees. That balances self-service FREEDOM with GOVERNANCE — the")
print("core platform structure the Business Analyst builds and the Admin governs.")
EOF
```

**Expected result:** A Qlik Sense app with an associative data model, sheets of visualizations, and master items (Revenue = Sum(Sales) defined once), running identically on client-managed or Qlik Cloud, where two analysts using the master Revenue get agreeing numbers. The platform lesson is that an app is a data model plus sheets of visualizations built with reusable master items for governed self-service, deployed either client-managed or in Qlik Cloud — the structure the three certification roles build, model, and govern.

**Negative test:** Letting every analyst define their own "Revenue" measure ad hoc. Definitions drift and numbers disagree ("my revenue vs your revenue"); master items provide one governed definition reused everywhere, delivering self-service freedom with consistency.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Qlik Sense understood — client-managed and Qlik Cloud (SaaS) deployments on the same associative engine.
- [ ] Apps, sheets, and stories understood — the structure of a Qlik analytics application.
- [ ] Master items understood — reusable definitions delivering governed self-service.
- [ ] The platform structure the three certification roles operate on recognized.
