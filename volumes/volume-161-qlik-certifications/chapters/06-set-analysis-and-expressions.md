# Chapter 06: Set Analysis and Expressions

## Learning Objectives

- Explain expressions and aggregations in Qlik.
- Describe set analysis — defining a set of data to aggregate.
- Understand set analysis independent of current selections.
- Recognize set analysis as a distinctive, heavily-tested skill.

*Cert relevance: set analysis is Qlik's distinctive expression skill, central to the certifications.*

## Expressions and aggregations

Visualizations in Qlik are driven by **expressions** — formulas that compute the values shown. Most expressions are **aggregations**: `Sum(Sales)`, `Count(OrderID)`, `Avg(Price)`, `Max(Date)`. An aggregation computes over the **currently selected** data — by default, an expression respects the user's [selections (Ch 2)](02-the-associative-model.md), so `Sum(Sales)` shows the sum of sales for whatever the user has selected. Expressions and aggregations are the computational core of every chart, and writing them correctly is a fundamental Qlik skill. The lab models aggregations.

## Set analysis: defining a set of data

The distinctive Qlik skill is **set analysis** — a syntax for **defining exactly which set of data an aggregation operates on**, *independent of (or modifying) the current selections*. Written inside `{ }` in an expression, a set expression overrides or extends what the user has selected. For example:

- `Sum({<Year={2025}>} Sales)` — sum of sales for **2025**, regardless of the year the user has selected.
- `Sum({1} Sales)` — sum of sales for **all** data (`{1}` = the full set, ignoring selections).
- `Sum({<Region={'East'}>} Sales)` — sum for the East region specifically.

Set analysis lets you build expressions that compare **a fixed set** (e.g., last year, a specific region, the whole dataset) against the **user's current selection** — the foundation of comparative analysis (year-over-year, actual-vs-target, this-vs-all). The lab models set analysis.

## Independent of current selections

The power of set analysis is **selection independence**. Without it, every expression moves with the user's clicks. With it, you can pin part of an expression to a **specific set** while the rest responds to selections — enabling KPIs and comparisons that stay meaningful as the user explores. A classic pattern is **year-over-year**: show the selected period's revenue *and* the same period last year (via set analysis) side by side, so the comparison holds no matter what the user selects. Set analysis is what makes sophisticated, comparative Qlik analytics possible. The lab models a comparison.

## A distinctive, tested skill

Set analysis is **distinctive to Qlik** and **heavily tested** — it is the part of expression-writing that separates a proficient Qlik developer from a beginner, and the certifications (especially [Business Analyst, Ch 5](05-business-analyst.md)) probe it: reading a set expression and predicting its result, and writing one to meet a requirement. Like [DataWeave for MuleSoft (CLX)](../../volume-160-mulesoft-certifications/README.md), set analysis is the signature expression language a candidate must master. The lab synthesizes.

## Hands-On Lab

Python models set analysis. **Cost:** none.

### Lab 6.1 — Aggregations and set analysis (selection-independent sets)

**Objective:** See set analysis define a data set independent of selections.

```bash
python3 - <<'EOF'
# sales data; model how Qlik aggregations respond to selection vs set analysis
SALES = [
    {"year": 2024, "region": "East", "amount": 100},
    {"year": 2024, "region": "West", "amount": 150},
    {"year": 2025, "region": "East", "amount": 200},
    {"year": 2025, "region": "West", "amount": 250},
]
def agg_sum(rows, **flt):
    return sum(r["amount"] for r in rows if all(r[k] in v for k, v in flt.items()))

# user's CURRENT selection: Year = 2025
current_selection = {"year": {2025}}
selected_rows = [r for r in SALES if r["year"] in current_selection["year"]]

print("User has SELECTED Year = 2025.\n")
# plain aggregation: respects the selection
print(f"   Sum(Sales)                          = {agg_sum(selected_rows)}   (respects selection: 2025 only)")
# set analysis: {1} = ALL data, ignores selection
print(f"   Sum({{1}} Sales)                      = {agg_sum(SALES)}   (set {{1}} = ALL, IGNORES selection)")
# set analysis: pin to a specific year regardless of selection
print(f"   Sum({{<Year={{2024}}>}} Sales)          = {agg_sum(SALES, year={2024})}   (pinned to 2024, ignores that 2025 is selected)")
# set analysis: specific region within/around selection
print(f"   Sum({{<Region={{'East'}}>}} Sales)      = {agg_sum(SALES, region={'East'})}   (East, all years — modifies selection)")
print()
# the year-over-year pattern
this_year = agg_sum(SALES, year={2025})
last_year = agg_sum(SALES, year={2024})
yoy = 100*(this_year-last_year)/last_year
print("Year-over-year comparison (set analysis makes this possible):")
print(f"   selected 2025 = {this_year}; via set analysis last year 2024 = {last_year}; YoY = +{yoy:.0f}%\n")
print("EXPRESSIONS = aggregations (Sum/Count/Avg...) that by default RESPECT selections. ★ SET")
print("ANALYSIS ({<...>} inside an expression) DEFINES the exact data set to aggregate, INDEPENDENT")
print("of (or modifying) selections: {1}=ALL, {<Year={2024}>}=pinned to 2024. That enables")
print("COMPARATIVE analytics — year-over-year, actual-vs-target, this-vs-all — that stay meaningful")
print("as the user explores. Set analysis is DISTINCTIVE to Qlik + HEAVILY TESTED (like DataWeave")
print("for MuleSoft) — reading + writing set expressions separates proficient from beginner.")
EOF
```

**Expected result:** With Year=2025 selected, `Sum(Sales)` respects the selection (450), `Sum({1} Sales)` ignores it (700, all data), `Sum({<Year={2024}>} Sales)` pins to 2024 (250) regardless, and a year-over-year comparison (+80%) built with set analysis. The set-analysis lesson is that expressions are aggregations that respect selections by default, and set analysis defines the exact data set independent of selections — enabling comparative analytics (year-over-year, this-vs-all) — the distinctive, heavily-tested Qlik skill.

**Negative test:** Trying to build a year-over-year or actual-vs-target comparison with plain aggregations. They all move with the user's selection, so the comparison collapses; set analysis pins part of the expression to a fixed set, which is what makes comparative Qlik analytics possible.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Expressions and aggregations understood — the formulas driving visualizations, respecting selections by default.
- [ ] Set analysis understood — defining exactly which set of data an aggregation operates on.
- [ ] Selection independence understood — pinning part of an expression to a fixed set for comparisons.
- [ ] Set analysis recognized as a distinctive, heavily-tested Qlik skill (the counterpart to DataWeave).
