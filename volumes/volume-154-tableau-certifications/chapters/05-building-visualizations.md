# Chapter 05: Building Visualizations

## Learning Objectives

- Choose the right chart type for the analytical question.
- Understand Show Me and the marks card.
- Apply filtering, sorting, and color effectively.
- Recognize chart choice as answering a question, not decorating.

*Cert relevance: building the right visualization is the heart of **Desktop Specialist** and **Data Analyst** — the practical skill the labs test.*

## The right chart for the question

The most important visualization skill is **matching the chart type to the analytical question**, using the [perceptual principles from Chapter 2](02-what-is-data-visualization.md). Different questions call for different charts:

| Question | Chart |
|:---|:---|
| Compare values across categories | Bar chart |
| Trend over time | Line chart |
| Relationship between two measures | Scatter plot |
| Part-to-whole (few parts) | Stacked bar (rarely pie) |
| Distribution | Histogram / box plot |
| Geographic pattern | Map |
| Two dimensions × a measure | Heatmap / highlight table |

The discipline: **start from the question, then pick the chart that answers it most clearly** — not "which chart looks impressive." A trend question needs a line (not a bar); a comparison needs a bar (not a pie); a relationship needs a scatter. The certifications' hands-on labs test exactly this judgment. The lab models chart selection.

## Show Me and the marks card

Tableau's **Show Me** panel suggests appropriate chart types based on the fields you have selected — a helpful nudge toward suitable visualizations (and it greys out charts your fields cannot support). It is a teaching tool, but the skilled analyst knows *why* Show Me suggests what it does and often builds the viz manually for precise control.

The **marks card** is where the fine control lives: it controls how data is drawn — the **mark type** (bar, line, circle, square), and the visual encodings **Color**, **Size**, **Label**, **Detail**, and **Tooltip**. Dragging a dimension to **Color** colors marks by category; a measure to **Size** sizes them by value. Mastering the marks card — encoding the *right* fields in the *right* visual channels ([perceptual accuracy, Chapter 2](02-what-is-data-visualization.md)) — is what separates a clear viz from a cluttered one. The lab is covered within the chart-selection exercise.

## Filtering, sorting, and focus

Beyond the chart, **filtering** (showing a relevant subset), **sorting** (ordering bars by value so the ranking is obvious), and **focus** (removing clutter, highlighting what matters) turn a raw chart into a clear answer. A sorted bar chart reveals the ranking instantly; an unsorted one makes the reader hunt. These finishing skills — small but high-impact — are part of the practical competency the certifications validate. The lab shows sorting's impact.

## Hands-On Lab

Python models chart selection. **Cost:** none.

### Lab 5.1 — Match the chart to the question

**Objective:** Pick the visualization that answers each analytical question.

```bash
python3 - <<'EOF'
QUESTIONS = [
  ("How did sales trend over the last 12 months?",      "LINE chart",    "trend over time = line"),
  ("Which region sold the most?",                        "BAR chart",     "compare categories = bar (sorted!)"),
  ("Is there a relationship between discount & profit?", "SCATTER plot",  "two measures' relationship = scatter"),
  ("How are order sizes distributed?",                   "HISTOGRAM",     "distribution = histogram"),
  ("Which states have the highest sales?",               "MAP",           "geographic = map"),
  ("Sales by region AND category at a glance?",          "HEATMAP",       "two dims x a measure = heatmap"),
  ("What share is each of 3 segments?",                  "STACKED BAR",   "part-to-whole, few parts (NOT a pie)"),
]
print(f"{'question':52}{'chart':>14}")
for q, chart, why in QUESTIONS:
    print(f"{q:52}{chart:>14}")
    print(f"   -> {why}")
print("\nThe discipline: START FROM THE QUESTION, then pick the chart that answers it")
print("most CLEARLY — not the flashiest one.")
print("  TREND over time    -> LINE (a bar chart of months hides the trend)")
print("  COMPARE categories -> BAR, SORTED (not a pie — the eye can't rank angles)")
print("  RELATIONSHIP       -> SCATTER (position, the most accurate encoding)")
print("  DISTRIBUTION       -> HISTOGRAM; GEOGRAPHIC -> MAP")
print("\nTableau's SHOW ME panel suggests appropriate charts for your selected fields —")
print("a good nudge — but the skilled analyst knows WHY, and builds manually for control")
print("via the MARKS CARD (mark type + Color/Size/Label/Detail encodings). Chart choice")
print("is answering a QUESTION, not decorating — which is exactly what the hands-on")
print("Data Analyst labs test: given data and a question, build the RIGHT viz.")
EOF
```

**Expected result:** Each analytical question matched to the chart that answers it clearly — trend to line, comparison to sorted bar, relationship to scatter, distribution to histogram, geography to map. The chart-selection lesson is to start from the question and pick the clearest chart (not the flashiest), the practical judgment the hands-on certification labs test.

**Negative test:** Choosing charts by visual impressiveness rather than the question. A pie chart for ranking, or a bar chart for a time trend, obscures the answer — the right chart follows from what the viewer needs to understand.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Chart choice understood as matching the visualization to the analytical question, using perceptual principles.
- [ ] Show Me understood as a suggestion tool, and the marks card as the fine control (mark type, Color, Size, Label).
- [ ] Filtering, sorting, and focus understood as finishing skills that turn a raw chart into a clear answer.
- [ ] Visualization recognized as answering a question, not decorating — the practical skill the labs validate.
