# Chapter 02: The SAS Platform and Language

## Learning Objectives

- Describe SAS Viya and its in-memory engine, CAS, and the CASL language.
- Distinguish SAS Viya from the legacy SAS 9.4 platform.
- Explain the SAS language — the DATA step and PROC steps.
- Recognize the tools — SAS Studio, Model Studio, and Visual Analytics.

*Cert relevance: every certification sits on this platform and language; this chapter is the shared foundation.*

## SAS Viya and CAS

**SAS Viya** is SAS's modern **cloud-native analytics and AI platform**. Its defining component is **CAS — Cloud Analytic Services** — a **distributed, in-memory** compute engine. "In-memory" means data is loaded into RAM across a cluster and analyzed there, so large-scale statistics and machine learning run **fast and at scale**; "distributed" means the work spreads across many nodes. CAS is what lets Viya handle big data and heavy modeling that a single machine could not.

You interact with CAS by **loading data into memory** (a CAS table), running **actions** (statistical/ML/data operations) against it, and retrieving results. The language for scripting CAS directly is **CASL (the CAS language)**, and SAS programs and procedures also run against CAS. Understanding that **compute happens in CAS, in memory, distributed** is the mental model for modern SAS. The lab models loading data into CAS and running an action.

## Viya versus SAS 9.4

Two generations of SAS coexist:

- **SAS 9.4** — the **legacy** platform: a mature, single-server (or grid) architecture that has run enterprise analytics for years. Programs are the same SAS language, but the runtime and tooling are the older generation.
- **SAS Viya** — the **modern** platform: cloud-native, containerized (runs on Kubernetes), in-memory (CAS), with web-based tools and open APIs (call SAS from Python, R, REST). Viya is where new development and most current certifications focus.

The **good news** is continuity: the **SAS language is largely the same** across both, so skills transfer. Certifications increasingly specify **Using SAS Viya** because that is the current platform, but the DATA step and PROCs you learn apply broadly. Knowing which platform a credential targets — and that Viya is the modern, in-memory, cloud-native one — matters. The lab contrasts the two.

## The SAS language: DATA step and PROC

The **SAS language** has two halves, and mastering their interplay is the core of SAS programming:

- **The DATA step** — where you **read, transform, and create data sets** row by row. It reads input, applies logic (assignments, conditionals, loops) to **each observation**, and writes an output data set. It is SAS's data-manipulation workhorse: filter, derive columns, merge, reshape.
- **PROC steps (procedures)** — pre-built **procedures** that **do something to a data set**: `PROC MEANS`/`PROC SUMMARY` (descriptive statistics), `PROC FREQ` (frequencies), `PROC SORT`, `PROC SQL` (SQL in SAS), `PROC REG`/`PROC LOGISTIC` (modeling), `PROC SGPLOT` (graphs). You **call a procedure** and it produces results.

The pattern is **DATA step to prepare, PROC to analyze**: shape the data with DATA steps, then run procedures for statistics, models, and reports. This two-part structure recurs in every SAS program and every programming certification. The lab writes a DATA-step-then-PROC flow.

## The tools

SAS Viya provides **web-based tools** for different users:

- **SAS Studio** — the **programming IDE** where you write and run SAS code (DATA steps and PROCs) in the browser.
- **Model Studio** — the **visual machine-learning** environment where you build **pipelines** (drag-and-drop nodes: data → transform → model → assess), used for the Machine Learning Specialist work ([Ch 6](06-machine-learning-on-viya.md)).
- **SAS Visual Analytics** — the **BI/reporting** tool for interactive reports and dashboards, used for Visual Business Analytics ([Ch 7](07-visual-analytics-and-bi.md)).
- **Open interfaces** — call SAS/CAS from **Python** (SWAT), R, Java, and REST, so SAS fits into modern data-science workflows.

Different certifications map to different tools: programmers live in SAS Studio, data scientists in Model Studio, analysts in Visual Analytics. The lab maps tools to work. *(SAS's mix of code and visual tools parallels the code/visual split in other analytics platforms.)*

## Hands-On Lab

Python models CAS in-memory compute, the DATA-step/PROC pattern, and the tools. **Cost:** none.

### Lab 2.1 — Model CAS, the DATA step, and PROC

**Objective:** Load data into an in-memory CAS table, run a DATA step, then a PROC.

```bash
python3 - <<'EOF'
# SAS Viya: load data into CAS (in-memory, distributed), then DATA step + PROC
class CAS:  # a toy in-memory analytic service
    def __init__(self): self.tables = {}
    def load(self, name, rows): self.tables[name] = rows; print(f"   CAS: loaded '{name}' into memory ({len(rows)} rows, distributed)")
    def action(self, name, fn):  # CAS 'action' runs against the in-memory table
        return fn(self.tables[name])

cas = CAS()
raw = [{"id":1,"sales":120,"region":"E"},{"id":2,"sales":80,"region":"W"},
       {"id":3,"sales":200,"region":"E"},{"id":4,"sales":50,"region":"W"}]
cas.load("orders", raw)

# DATA step: read each observation, derive a column, filter
def data_step(rows):
    out = []
    for r in rows:                       # DATA step processes row by row
        rec = dict(r)
        rec["sales_tax"] = round(r["sales"] * 1.08, 2)   # derive a column
        if rec["sales"] >= 80:           # keep (WHERE/IF)
            out.append(rec)
    return out
staged = cas.action("orders", data_step)
print("\n   DATA step (derive sales_tax, keep sales>=80):")
for r in staged: print(f"      {r}")

# PROC step: e.g. PROC MEANS by region (descriptive stats)
def proc_means_by(rows, group, var):
    agg = {}
    for r in rows:
        agg.setdefault(r[group], []).append(r[var])
    return {g: {"n": len(v), "mean": round(sum(v)/len(v),1), "sum": sum(v)} for g,v in agg.items()}
print("\n   PROC MEANS (mean/sum of sales_tax by region):")
for g, stats in proc_means_by(staged, "region", "sales_tax").items():
    print(f"      region {g}: {stats}")
print()
print("SAS VIYA loads data into CAS (in-memory, distributed) for fast analytics at scale.")
print("The SAS LANGUAGE has two halves: the DATA STEP prepares data row by row (derive")
print("sales_tax, filter), and PROC steps ANALYZE it (PROC MEANS = stats by region). DATA")
print("step to prepare, PROC to analyze — the core pattern of every SAS program and cert.")
EOF
```

**Expected result:** Data loaded into an in-memory CAS table, a DATA step deriving a taxed column and filtering rows, then a PROC MEANS-style procedure computing statistics by region. The lesson is the SAS foundation: SAS Viya computes in-memory in CAS at scale, and the SAS language pairs the DATA step (prepare data row by row) with PROC steps (analyze it) — the pattern behind every SAS program and certification.

**Negative test:** Trying to do all analysis inside DATA steps with hand-coded loops. It is slow, error-prone, and reinvents statistics; PROC steps are optimized, validated procedures — DATA step to prepare, PROC to analyze is the idiomatic, testable division.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] SAS Viya and CAS understood — the cloud-native platform and its distributed in-memory engine (with CASL).
- [ ] Viya vs SAS 9.4 understood — the modern in-memory/cloud-native platform versus the legacy one, same language.
- [ ] The SAS language understood — the DATA step (prepare) and PROC steps (analyze).
- [ ] The tools understood — SAS Studio (code), Model Studio (ML pipelines), Visual Analytics (BI), open APIs.

## See also

- [Chapter 03 — SAS Programming Foundations](03-sas-programming-foundations.md) — the DATA step and PROCs in depth.
- [Chapter 06 — Machine Learning on Viya](06-machine-learning-on-viya.md) — Model Studio pipelines on CAS.
- [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md) — another in-memory, distributed analytics platform.
