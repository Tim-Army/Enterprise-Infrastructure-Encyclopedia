# Chapter 02: What Is Data Visualization?

## Learning Objectives

- Explain why visualization reveals what tables hide.
- Understand pre-attentive attributes and how the eye reads a chart.
- Place business intelligence as decision-support.
- Recognize good visualization as a discipline, not decoration.

*Cert relevance: the *why* and *principles* of visualization underlie every Tableau certification — especially the design judgment the Data Analyst tests.*

## Why visualize?

A table of numbers is **precise but not perceptible** — a human staring at 10,000 rows sees no pattern, no trend, no outlier. The same data as a chart is **instantly readable**: a line trending up, a bar far taller than the rest, a cluster of points pulling away. Visualization works because it maps data onto **visual properties the eye processes automatically** — position, length, color, size — turning analysis into *seeing*.

The classic demonstration is that datasets with *identical* summary statistics (same mean, same correlation) can have *completely different* shapes — a fact invisible in the numbers and obvious the instant you plot them. This is the core justification for visualization: **the numbers can lie by omission; the picture tells the truth.** The lab demonstrates it.

## Pre-attentive attributes

Good visualization exploits **pre-attentive attributes** — visual properties the brain processes *before* conscious attention, in milliseconds, without effort: **position** (where something is), **length** (how long a bar is), **color** (hue), **size**. Encoding data in these is what makes a chart instantly readable.

Crucially, some encodings are **more accurate** than others for human perception: people judge **position and length** very accurately (a bar chart, a scatter plot), but judge **area, angle, and color-intensity** poorly (pie charts, which use angle; heatmaps, which use color). This is why a bar chart usually beats a pie chart — not taste, but *how accurately the eye can decode the difference*. Choosing encodings the eye reads well is a core skill the certifications test. The lab models the accuracy hierarchy.

## Business intelligence

**Business intelligence (BI)** is the broader discipline visualization serves: turning an organization's data into **insight that supports decisions.** A BI tool like Tableau lets analysts and business users **explore** data (ask questions, drill down, filter), **monitor** it (dashboards of key metrics), and **communicate** findings (charts and stories that persuade) — so decisions are made from *evidence* rather than intuition. Visualization is the *how*; better decisions are the *why*. The lab is covered within the perception exercises.

## Good visualization is a discipline

The final principle: visualization is a **discipline with right and wrong answers**, not decoration. A chart can **mislead** (a truncated axis exaggerating a difference, a 3D pie distorting proportions, chart-junk obscuring the data) or **clarify** (the right chart type, honest scales, minimal ink). The certifications — especially the Data Analyst — test the *judgment* to choose visualizations that reveal the truth clearly, which is why this chapter's principles matter before any Tableau button. The lab makes the accuracy principle concrete.

## Hands-On Lab

Python models visualization principles. **Cost:** none.

### Lab 2.1 — The numbers hide what the picture reveals

**Objective:** See why identical statistics can mean different shapes.

```bash
python3 - <<'EOF'
# two datasets with (nearly) identical summary stats but different shapes
import statistics
A = [(10,8.04),(8,6.95),(13,7.58),(9,8.81),(11,8.33),(14,9.96),(6,7.24),(4,4.26),(12,10.84),(7,4.82),(5,5.68)]
B = [(10,9.14),(8,8.14),(13,8.74),(9,8.77),(11,9.26),(14,8.10),(6,6.13),(4,3.10),(12,9.13),(7,7.26),(5,4.74)]
def stats(d):
    xs=[p[0] for p in d]; ys=[p[1] for p in d]
    return (statistics.mean(xs), statistics.mean(ys), statistics.pstdev(ys))
for name, d in [("A", A), ("B", B)]:
    mx, my, sy = stats(d)
    print(f"dataset {name}: mean(x)={mx:.1f}  mean(y)={my:.2f}  stdev(y)={sy:.2f}")
print("\n   -> BY THE NUMBERS, A and B look IDENTICAL (same means, same spread).")
print("      A spreadsheet of summary stats says 'these are the same dataset.'\n")
# but their SHAPES differ — sketch a crude ASCII scatter to reveal it
def sketch(d, label):
    print(f"   {label} (x across, y up):")
    grid = [[" "]*15 for _ in range(11)]
    for x,y in d:
        gx=int(x); gy=int(round(y))
        if 0<=gx<15 and 0<=gy<11: grid[10-gy][gx]="*"
    for row in grid: print("     "+"".join(row))
sketch(A, "dataset A")
sketch(B, "dataset B")
print("\n   -> the PICTURES are clearly DIFFERENT — A is roughly linear, B curves.")
print("      Identical statistics, different reality. The numbers hid it; the plot")
print("      revealed it instantly.")
print("\nThis is why we VISUALIZE: summary statistics can lie by omission — two datasets")
print("with the same mean/correlation can have totally different shapes (outliers,")
print("curves, clusters) that ONLY a picture reveals. The eye sees a pattern in a chart")
print("that a human staring at rows of numbers never would. 'See and understand your")
print("data' isn't a slogan — it's that seeing is a different, more powerful mode of")
print("analysis than reading. That's Tableau's whole reason to exist.")
EOF
```

**Expected result:** Two datasets with identical summary statistics (mean, spread) but visibly different shapes when plotted — one roughly linear, one curved. The visualization lesson is that summary statistics can lie by omission, and a picture reveals patterns, outliers, and shapes that rows of numbers hide — the core justification for visualizing data.

**Negative test:** Trusting summary statistics alone to characterize a dataset. Two datasets with the same mean and correlation can have completely different shapes; only plotting them reveals outliers, curves, and clusters the numbers conceal.

**Cleanup:** None.

### Lab 2.2 — The perceptual-accuracy hierarchy

**Objective:** Choose encodings the eye reads accurately.

```bash
python3 - <<'EOF'
# how accurately humans decode different visual encodings (Cleveland-McGill style ranking)
ENCODINGS = [
  ("position (scatter, common scale)", 1, "MOST accurate"),
  ("length (bar chart)",               2, "very accurate"),
  ("angle / slope",                    3, "moderate"),
  ("area (bubble size)",               4, "poor"),
  ("color intensity / saturation",     5, "poor"),
  ("color hue",                        6, "categorical only, not magnitude"),
]
print("How ACCURATELY the eye decodes each encoding (1 = best):\n")
print(f"   {'encoding':38}{'rank':>6}   accuracy")
for enc, rank, note in ENCODINGS:
    print(f"   {enc:38}{rank:>6}   {note}")
print("\nThe practical rule this gives you:")
print("  BAR CHART (length) beats PIE CHART (angle/area) for comparing values — the eye")
print("     judges bar lengths accurately but angles/areas poorly. That's why 'use a bar")
print("     not a pie' is a RULE, not a preference.")
print("  POSITION (scatter) is the most accurate — great for showing relationships.")
print("  COLOR HUE is for CATEGORIES (which group), NOT magnitude (how much) — don't")
print("     encode a quantity in a rainbow; the eye can't rank hues.")
print("\nGood visualization ENCODES data in the properties the eye reads WELL. This isn't")
print("taste — it's perception science: choose position/length for precise comparison,")
print("reserve area/color for when accuracy matters less. Picking the encoding the eye")
print("decodes accurately is a core skill the Data Analyst cert tests — and why Tableau's")
print("'Show Me' nudges you toward appropriate chart types (Chapter 5).")
EOF
```

**Expected result:** The perceptual-accuracy ranking of encodings — position and length most accurate, area and color poor — yielding the rule that bar charts beat pie charts for comparison and color hue is for categories not magnitude. The perception lesson is that good visualization encodes data in the properties the eye reads accurately, which is science, not taste, and a core certification skill.

**Negative test:** Choosing a pie chart to compare many values, or encoding a quantity in color hue. The eye judges angles, areas, and hues poorly; position and length (a bar or scatter) let viewers decode the differences accurately.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The value of visualization understood — pictures reveal patterns and shapes that summary statistics hide.
- [ ] Pre-attentive attributes and the perceptual-accuracy hierarchy understood — position/length beat area/color.
- [ ] Business intelligence placed as decision-support: explore, monitor, communicate from data.
- [ ] Visualization recognized as a discipline with right and wrong answers, not decoration.
