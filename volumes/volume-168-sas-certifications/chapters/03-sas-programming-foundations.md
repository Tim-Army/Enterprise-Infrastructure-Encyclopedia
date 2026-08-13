# Chapter 03: SAS Programming Foundations

## Learning Objectives

- Read data into SAS data sets and understand the observation/variable model.
- Use the DATA step — assignments, conditionals, and functions.
- Summarize data with core PROCs — MEANS, FREQ, SORT, and SQL.
- Recognize what the Fundamentals/Programming Specialist certifications validate.

*Cert relevance: this is the Fundamentals of Programming and Programming Specialist track — the SAS foundation.*

## Data sets: observations and variables

Everything in SAS revolves around the **data set** — a table of **observations** (rows) and **variables** (columns). A variable is either **numeric** or **character**. You **read data in** from many sources — raw files, CSVs, databases, existing data sets — into a SAS data set, then work with it. The foundational skill is getting data **in** correctly (right types, right lengths, missing values handled) because everything downstream depends on it.

This observation/variable model is simple but rigorous: SAS is explicit about types, lengths, and missing values, which is part of why it is trusted for regulated analytics. The **Fundamentals of Programming Using SAS Viya** certification starts here. The lab reads data into a data set.

## The DATA step in depth

The **DATA step** is where you **build and transform** data sets. For **each observation** it executes your statements top to bottom, then writes the result:

- **Assignment** — create or change variables (`profit = revenue - cost;`).
- **Conditional logic** — `IF/THEN/ELSE` to branch, and `WHERE`/subsetting `IF` to keep or drop rows.
- **Functions** — built-in functions for text (`SUBSTR`, `UPCASE`, `CATX`), numbers (`ROUND`, `SUM`), and dates.
- **Iteration** — `DO` loops for repeated logic.
- **Missing values** — SAS represents missing explicitly (`.` for numeric, blank for character); handling them correctly is essential.

The DATA step is the **data-manipulation engine**: filtering, deriving columns, cleaning, and reshaping all happen here. Fluency with it — especially conditionals, functions, and missing-value handling — is what the programming exams test most. The lab uses DATA-step logic.

## Summarizing with PROCs

Once data is prepared, **procedures** summarize and analyze it. The foundational PROCs:

- **`PROC MEANS` / `PROC SUMMARY`** — descriptive statistics (n, mean, min, max, sum, std) overall or **by group**.
- **`PROC FREQ`** — frequency counts and cross-tabulations for categorical variables.
- **`PROC SORT`** — order a data set (often required before by-group processing or merging).
- **`PROC SQL`** — run **SQL** inside SAS (joins, aggregations, subqueries) — a bridge for those who know SQL.
- **`PROC PRINT`** — display observations.

These cover the everyday "what does this data look like?" work — distributions, group summaries, counts. Knowing which PROC answers which question, and reading their output, is core competency. The lab runs MEANS, FREQ, and an SQL-style query. *(PROC SQL makes SAS approachable to anyone who knows SQL, like the analysts in [Snowflake XLIX](../../volume-049-snowflake-certifications/README.md).)*

## What the programming certifications validate

The **Fundamentals of Programming Using SAS Viya** validates the foundation — reading data, DATA-step basics, and core PROCs. The **Programming Specialist** (A00-420, 71% to pass) goes deeper into intermediate programming, and **Advanced Programming** (a performance-based exam) tests sophisticated techniques — macro programming, advanced DATA-step and PROC SQL, efficiency. Together they form the **programming track**, and they are the most common starting point in SAS certification because **everything else builds on the language**. The lab exercises the foundation end to end.

## Hands-On Lab

Python models the DATA step and the core PROCs on a small data set. **Cost:** none.

### Lab 3.1 — Read, transform with a DATA step, and summarize with PROCs

**Objective:** Build a data set, apply DATA-step logic, then run MEANS/FREQ/SQL-style summaries.

```bash
python3 - <<'EOF'
# read raw data into a SAS-style DATA SET (observations x variables)
RAW = [
  {"id":1,"region":"East","revenue":1200,"cost":800},
  {"id":2,"region":"West","revenue":300, "cost":350},   # loss
  {"id":3,"region":"East","revenue":900, "cost":400},
  {"id":4,"region":"West","revenue":1500,"cost":600},
]
# DATA step: derive profit, classify, keep profitable (subsetting IF)
def data_step(rows):
    out = []
    for r in rows:                                  # process each observation
        rec = dict(r)
        rec["profit"] = r["revenue"] - r["cost"]    # assignment
        rec["status"] = "profit" if rec["profit"] > 0 else "loss"   # IF/THEN
        out.append(rec)
    return out
work = data_step(RAW)
print("DATA step (derive profit + status):")
for r in work: print(f"   id={r['id']} {r['region']:4} profit={r['profit']:>5} {r['status']}")

# PROC MEANS: mean/sum of profit by region
def proc_means(rows, group, var):
    agg = {}
    for r in rows: agg.setdefault(r[group], []).append(r[var])
    return {g:{"n":len(v),"mean":round(sum(v)/len(v),1),"sum":sum(v)} for g,v in agg.items()}
print("\nPROC MEANS (profit by region):")
for g,s in proc_means(work,"region","profit").items(): print(f"   {g:4}: {s}")

# PROC FREQ: counts of status
def proc_freq(rows, var):
    f = {}
    for r in rows: f[r[var]] = f.get(r[var],0)+1
    return f
print("\nPROC FREQ (status):", proc_freq(work, "status"))

# PROC SQL: SQL inside SAS (total revenue where profit>0)
total_rev = sum(r["revenue"] for r in work if r["profit"] > 0)
print(f"\nPROC SQL (SELECT SUM(revenue) WHERE profit>0): {total_rev}")
print()
print("The DATA STEP reads observations and derives/filters (profit, status) row by row. Core")
print("PROCs then summarize: PROC MEANS (stats by group), PROC FREQ (counts), PROC SQL (SQL in")
print("SAS). DATA step to prepare, PROC to analyze — the Fundamentals / Programming Specialist core.")
EOF
```

**Expected result:** A DATA step deriving profit and a status flag per observation, then PROC MEANS (profit by region), PROC FREQ (status counts), and a PROC SQL-style aggregate. The lesson is the SAS programming foundation: the DATA step prepares data observation by observation, and core PROCs (MEANS, FREQ, SORT, SQL) summarize it — the competency the Fundamentals and Programming Specialist certifications validate.

**Negative test:** Skipping the DATA step and computing profit ad hoc inside each PROC. Logic is duplicated and inconsistent, and missing values are mishandled; deriving analysis variables once in a DATA step, then summarizing with PROCs, is the correct, testable structure.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The data-set model understood — observations and variables, numeric/character, missing values.
- [ ] The DATA step understood — assignments, conditionals, functions, iteration, and subsetting.
- [ ] Core PROCs understood — MEANS/SUMMARY, FREQ, SORT, SQL, PRINT.
- [ ] The programming track placed — Fundamentals, Programming Specialist (71%), and Advanced Programming.

## See also

- [Chapter 02 — The SAS Platform and Language](02-the-sas-platform.md) — the DATA step / PROC pattern and CAS.
- [Chapter 04 — Preparing and Curating Data](04-preparing-and-curating-data.md) — merging, formatting, and cleaning at scale.
- [Chapter 05 — Statistical Analysis](05-statistical-analysis.md) — the analytic PROCs the foundation leads to.
