# Chapter 07: Dashboards and Interactivity

## Learning Objectives

- Assemble multiple visualizations into a dashboard.
- Apply dashboard actions — filter, highlight, and navigate.
- Understand stories for guided, sequential narratives.
- Recognize interactivity as turning a report into an exploration.

*Cert relevance: dashboards and actions are core **Data Analyst** material — how analysis becomes a shareable, interactive product.*

## From worksheets to dashboards

A single visualization (a **worksheet**) answers one question. A **dashboard** combines *several* worksheets on one screen, so a viewer sees a **coherent picture** — sales trend, top products, regional map, and key metrics together — and can relate them. Assembling a good dashboard is a design skill: **layout** (what goes where, visual hierarchy), **focus** (a few clear views, not a wall of charts), and **coherence** (the views tell one story). A cluttered dashboard of twenty charts communicates less than a focused one of four. The lab is covered within the actions exercise.

## Dashboard actions

What makes a Tableau dashboard *interactive* — rather than a static image — is **actions**: user interactions on one view that affect others.

| Action | Does |
|:---|:---|
| **Filter action** | Clicking a mark filters the other views to that selection |
| **Highlight action** | Clicking highlights related marks across views |
| **Go-to-URL / navigation** | Clicking opens a URL or another dashboard |
| **Parameter/set actions** | Clicking changes a parameter or set, driving calculations |

The signature is the **filter action**: click a region on the map, and the trend chart, the product bars, and the metrics *all update to that region* — the viewer **explores** by clicking, drilling from overview to detail without the analyst pre-building every view. This turns a dashboard from a *report you read* into a *tool you explore*, which is the whole point of interactive BI. The lab models a filter action.

## Stories

Where a dashboard is for *exploration*, a **story** is for *guided narrative* — a sequence of dashboards or views (story points) that walk a viewer through an analysis in order, like slides that build an argument: "here's the problem, here's the cause, here's the recommendation." Stories are how analysts **communicate findings persuasively** to an audience that needs to be led through the reasoning, not left to explore. Dashboards explore; stories explain. The lab is covered within the interactivity exercise.

## Hands-On Lab

Python models dashboard interactivity. **Cost:** none.

### Lab 7.1 — A filter action turns a report into an exploration

**Objective:** See how clicking one view drives the others.

```bash
python3 - <<'EOF'
# a dashboard: a region map + a product bar chart + a KPI, linked by a filter action
DATA = [
  {"region": "East", "product": "Chairs", "sales": 300},
  {"region": "East", "product": "Phones", "sales": 500},
  {"region": "West", "product": "Chairs", "sales": 200},
  {"region": "West", "product": "Phones", "sales": 800},
  {"region": "West", "product": "Tables", "sales": 400},
]
def dashboard(region_filter=None):
    rows = [d for d in DATA if region_filter is None or d["region"] == region_filter]
    from collections import defaultdict
    by_product = defaultdict(float)
    for d in rows: by_product[d["product"]] += d["sales"]
    total = sum(d["sales"] for d in rows)
    scope = region_filter or "ALL regions"
    print(f"   [scope: {scope}]  KPI total sales = {total}")
    for p, v in sorted(by_product.items(), key=lambda x: -x[1]):
        print(f"      {p:8} {'#'*(int(v)//50)} {v:.0f}")

print("DASHBOARD, no interaction (showing ALL regions):")
dashboard()
print("\n--- user CLICKS 'West' on the region map (a FILTER ACTION fires) ---\n")
print("DASHBOARD now filtered to West (the product bars AND the KPI both updated):")
dashboard("West")
print("\nThe filter action: clicking ONE view (the map) filtered ALL the others (the")
print("product bars, the KPI total) to that selection — no analyst pre-built a 'West")
print("dashboard'; the viewer drilled from overview to detail by CLICKING.")
print("\nThat's what turns a Tableau dashboard from a STATIC REPORT into an interactive")
print("TOOL: actions (filter/highlight/navigate) let viewers EXPLORE — ask their own")
print("questions by clicking, drilling overview->detail. A dashboard is for exploration;")
print("a STORY (sequenced story points) is for guided narrative when you need to LEAD an")
print("audience through the reasoning. Explore vs explain — both are how analysis becomes")
print("a shareable product, which the Data Analyst cert tests.")
EOF
```

**Expected result:** Clicking "West" on the map firing a filter action that updates the product bars and the KPI to West only, letting the viewer drill from overview to detail by clicking. The interactivity lesson is that dashboard actions turn a static report into an exploration tool, with filter actions letting viewers ask their own questions — while stories provide guided narrative to lead an audience through reasoning.

**Negative test:** Building a separate static dashboard for every region. Actions let one dashboard filter dynamically to any selection the viewer clicks — the viewer explores rather than the analyst pre-building every view.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Dashboards understood as combining worksheets into a coherent, focused picture — a design skill.
- [ ] Dashboard actions (filter, highlight, navigate) understood as the interactivity that enables exploration.
- [ ] Stories understood as guided, sequential narratives for explaining findings — explore versus explain.
- [ ] Interactivity recognized as turning a static report into a tool viewers explore.
