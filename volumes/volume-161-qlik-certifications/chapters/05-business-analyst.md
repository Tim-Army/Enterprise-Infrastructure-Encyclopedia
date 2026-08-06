# Chapter 05: Business Analyst — Building Visualizations and Analysis

## Learning Objectives

- Explain the Business Analyst role — building apps and analysis.
- Describe choosing the right visualization for the question.
- Understand selections and the associative exploration experience.
- Recognize stories and communicating insight.

*Cert relevance: the Qlik Sense Business Analyst (QSBA) certification validates building visualizations and analysis.*

## The Business Analyst role

The **Qlik Sense Business Analyst** turns the [Data Architect's data model (Ch 4)](04-data-architect.md) into **insight** — designing apps, building **visualizations**, and enabling analysis that answers business questions. The QSBA certification measures the ability to **identify requirements, design applications, prepare and load data, and develop applications**. The Business Analyst is the bridge between data and decisions: they know the business questions, and they build the sheets, charts, and interactions that let people answer them. The lab models the role.

## Choosing the right visualization

A core Business Analyst skill is **choosing the right visualization** for the question — the same perceptual discipline the [Tableau volume (CLIV)](../../volume-154-tableau-certifications/README.md) teaches. Qlik offers many chart types (bar, line, KPI, table, pie, scatter, map, combo, and more), and the right choice depends on **what the data and question need**:

- **Comparison across categories** → **bar chart** (accurate length comparison).
- **Trend over time** → **line chart**.
- **A single key number** → **KPI object**.
- **Part-to-whole** → sparingly, a pie (bars usually clearer).
- **Relationship between two measures** → **scatter plot**.

Choosing well makes insight **obvious**; choosing poorly hides it. Selecting the appropriate chart for the analytical question is a tested QSBA skill. The lab models the choice.

## Selections and associative exploration

What makes analysis in Qlik distinctive is **selection-driven exploration** on the [associative engine (Ch 2)](02-the-associative-model.md). The Business Analyst builds apps that invite users to **make selections** — click a region, a product, a time period — and every visualization **instantly responds**, showing the associated (green/white) and excluded (gray) data. The analyst designs the sheets, filters, and interactions so this exploration is **intuitive and revealing**: the user drives, and the app reorganizes around them. Designing for associative exploration — not just static dashboards — is the Qlik-specific part of the Business Analyst's craft. The lab models selection-driven analysis.

## Stories and communicating insight

Finding an insight is only half the job — **communicating** it is the other half. Qlik **stories** let the Business Analyst build a **presentation-style narrative** from **snapshots** of visualizations, adding text and annotations to guide an audience through the findings. Stories turn an interactive app into a **shareable narrative** for stakeholders who need the conclusion, not the exploration. Communicating insight clearly — the right chart, a clear narrative — is what turns analysis into **decisions**, and it is part of the Business Analyst's remit (and Qlik's [data-literacy, Ch 8](08-data-literacy-and-ai.md) emphasis). The lab synthesizes.

## Hands-On Lab

Python models chart choice and selection-driven analysis. **Cost:** none.

### Lab 5.1 — Right chart, associative selection, and a story

**Objective:** See fit-for-purpose visualization and selection-driven exploration.

```bash
python3 - <<'EOF'
# choose the right visualization for each analytical question
QUESTIONS = [
  ("compare revenue across 4 regions", "bar chart", "accurate length comparison"),
  ("revenue trend over 12 months",     "line chart", "shows change over time"),
  ("total revenue right now",          "KPI object", "one key number, big"),
  ("relationship: spend vs orders",    "scatter plot", "two measures per point"),
]
print("Business Analyst — RIGHT CHART for the question:\n")
for q, chart, why in QUESTIONS:
    print(f"   '{q}'  ->  {chart:12} ({why})")
print()
# selection-driven associative exploration: user clicks a region, app responds
REGIONS = {"North": 420, "South": 380, "East": 510, "West": 290}
print("Selection-driven analysis (the associative experience):")
print(f"   Revenue by Region (bar): {REGIONS}")
sel = "East"
print(f"   user SELECTS Region='{sel}' -> every viz instantly filters to East:")
print(f"      KPI Revenue -> {REGIONS[sel]}   (was {sum(REGIONS.values())} total)")
print(f"      other regions -> GRAY (excluded); East's products/customers -> associated\n")
# story: snapshot the insight into a narrative
print("STORY (communicate the insight):")
best = max(REGIONS, key=REGIONS.get)
print(f"   snapshot the bar chart -> add text: '{best} leads at {REGIONS[best]}; West lags — investigate.'")
print("   -> a shareable narrative for stakeholders who need the CONCLUSION\n")
print("The BUSINESS ANALYST (QSBA) turns the data model into INSIGHT: pick the RIGHT chart per")
print("question (bar for comparison, line for trend, KPI for one number, scatter for relationship),")
print("design SELECTION-DRIVEN exploration (the associative engine responds instantly to clicks —")
print("green/white/gray), and build STORIES to COMMUNICATE findings. Right chart + clear narrative")
print("= analysis becomes DECISIONS. Designing for associative exploration is the Qlik-specific craft.")
EOF
```

**Expected result:** The right chart chosen per question (bar for comparison, line for trend, KPI for a number, scatter for relationship), a selection on Region=East instantly filtering every visualization (others grayed), and a story snapshot communicating the insight. The Business Analyst lesson is that the role turns the data model into insight by choosing fit-for-purpose visualizations, designing selection-driven associative exploration, and building stories to communicate findings — turning analysis into decisions.

**Negative test:** Building static dashboards with poorly-chosen charts and no interactivity. That hides insight and ignores Qlik's strength; the Business Analyst chooses the right chart for each question and designs selection-driven associative exploration, then communicates via stories.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Business Analyst role understood — designing apps and building visualizations and analysis.
- [ ] Choosing the right visualization for the question understood — bar, line, KPI, scatter by purpose.
- [ ] Selections and associative exploration understood — designing for selection-driven analysis.
- [ ] Stories and communicating insight understood — turning analysis into shareable narratives and decisions.
