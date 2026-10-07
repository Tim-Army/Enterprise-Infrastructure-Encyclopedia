# Chapter 06: Schedule Quality — The DCMA 14-Point Assessment and GAO Best Practices

## Learning Objectives

- Explain each metric in the DCMA 14-point schedule assessment and its
  threshold.
- Map the GAO's ten schedule best practices to concrete checks.
- Export schedule data from Microsoft Project, Primavera P6, or ProjectLibre
  and check it with a script.
- Interpret failures: tell a real problem from a justified exception.
- Build a repeatable schedule health check into each status cycle.

## Theory and Architecture

A schedule can compute a finish date and still be wrong. Schedule assessments
test whether the network is built well enough to trust. Two sets of criteria are
widely used on government programs: the **DCMA 14-point assessment** and the
**GAO Schedule Assessment Guide**.

### The DCMA 14-point assessment

The Defense Contract Management Agency developed 14 metrics to screen schedule
health quickly. They are screening thresholds, not absolute rules: a failure
means "look closer," and a justified exception can be acceptable. Percentages are
generally measured against incomplete, non-summary tasks.

| # | Metric | Threshold | What it catches |
| --- | --- | --- | --- |
| 1 | **Logic** | ≤ 5% of tasks missing a predecessor or successor | Open ends (Chapter 03) |
| 2 | **Leads** | 0% of relationships with a negative lag | Overlaps without stated logic |
| 3 | **Lags** | ≤ 5% of relationships with a positive lag | Lags standing in for work |
| 4 | **Relationship types** | ≥ 90% finish-to-start | Over-use of SS, FF, and SF |
| 5 | **Hard constraints** | ≤ 5% of tasks (MSO, MFO, SNLT, FNLT) | Dates typed in rather than computed |
| 6 | **High float** | ≤ 5% of tasks with total float > 44 working days | Missing successors |
| 7 | **Negative float** | 0% of tasks | Constraints the plan cannot meet |
| 8 | **High duration** | ≤ 5% of tasks with baseline duration > 44 working days | Tasks too long to control |
| 9 | **Invalid dates** | 0% (forecasts before the status date, or actuals after it) | Statusing errors |
| 10 | **Resources** | All tasks with duration carry resources or cost | Schedules not integrated with cost |
| 11 | **Missed tasks** | ≤ 5% of tasks due by the status date that finished late or not at all | Execution slipping against the baseline |
| 12 | **Critical path test** | Delaying a critical task delays the finish by the same amount | A broken critical path |
| 13 | **Critical Path Length Index (CPLI)** | ≥ 0.95 | Whether the remaining critical path can meet the baseline finish |
| 14 | **Baseline Execution Index (BEI)** | ≥ 0.95 | Whether tasks are finishing as planned |

Metrics 1 to 8 and 10 test how the schedule is **built** and can be checked at
any time. Metrics 9 and 11 to 14 test how it is **executed** and need a baseline
and status data (Chapters 07 and 08).

CPLI and BEI are calculated as:

```text
CPLI = (critical path length + total float of the finish) / critical path length
BEI  = tasks actually completed / tasks baselined to complete by the status date
```

DCMA has since folded schedule checks into its broader **DCMA EVMS Compliance
Metrics (DECM)**, but the 14-point assessment remains the common shorthand for
schedule health across government and industry.

### The GAO's ten best practices

The GAO Schedule Assessment Guide groups schedule quality into four
characteristics and ten best practices:

| Characteristic | Best practices |
| --- | --- |
| **Comprehensive** | 1. Capture all activities. 2. Assign resources to all activities. 3. Establish the durations of all activities |
| **Well-constructed** | 4. Sequence all activities. 5. Confirm the critical path is valid. 6. Ensure reasonable total float |
| **Credible** | 7. Verify the schedule can be traced horizontally and vertically. 8. Conduct a schedule risk analysis |
| **Controlled** | 9. Update the schedule with actual progress and logic. 10. Maintain a baseline schedule |

The DCMA metrics cover many of these mechanically. The GAO practices add
judgment: whether all the work is really there, whether durations have a basis,
and whether a risk analysis supports the dates (Chapter 09).

## Design Considerations

- **Check every cycle, not once.** Schedules degrade as tasks are added and
  status is entered. A health check before each report catches problems while
  they are small.
- **Document exceptions.** A 30-day supplier lead time over 44 days, or a
  contractual constraint, can be legitimate. Record the reason so the next
  assessor does not raise it again.
- **Do not game the metrics.** Splitting tasks just to get under 44 days, or
  adding fake successors to cut float, makes the numbers pass and the schedule
  worse.
- **Pick your tooling.** Primavera P6 includes a schedule check feature based on
  these metrics in recent versions; commercial analyzers (for example Deltek
  Acumen Fuse or Steelray Project Analyzer) cover Microsoft Project and others; a
  simple script, like the one in this chapter, covers the build metrics for any
  tool that can export a table.

## Implementation and Automation

### Export a task table

Export these columns, one row per task, to a CSV file. Column names in the file
must match the left column.

| CSV column | Meaning | Microsoft Project field | Primavera P6 column | ProjectLibre field |
| --- | --- | --- | --- | --- |
| `id` | Task ID | ID | Activity ID | ID |
| `name` | Task name | Name | Activity Name | Name |
| `duration_days` | Duration in working days | Duration | Original Duration | Duration |
| `predecessors` | Predecessor list, such as `11, 13` or `13SS+5d` | Predecessors | Predecessors (with relationship details) | Predecessors |
| `constraint` | Constraint type | Constraint Type | Primary Constraint | Constraint Type |
| `total_float_days` | Total float in working days | Total Slack | Total Float | Total Slack |
| `resources` | Assigned resources | Resource Names | Resources | Resource Names |
| `summary` | Yes for summary tasks | Summary | (WBS rows are not activities) | Summary |

How to export:

- **Microsoft Project:** **File > Save As**, choose **CSV**, and use the Export
  Wizard to map the fields above.
- **Primavera P6:** build a layout with the columns, then copy the activity rows
  into a spreadsheet and save as CSV (or use **File > Export** to a spreadsheet).
  Relationship details may need a predecessors column that includes type and
  lag; check what your version displays.
- **ProjectLibre:** add the columns to the Gantt table, select the rows, copy
  them into a spreadsheet, and save as CSV.

Rename the header row to the CSV column names before running the script.

### A build-quality checker

This script checks DCMA metrics 1 to 8 and 10 on the exported CSV. It accepts
predecessor entries such as `11`, `13SS+5d`, and `9FS-2d`, separated by commas
or semicolons. It treats the first and last rows as the project start and finish
milestones, the two legitimate open ends, so export the table in schedule order:

```python
#!/usr/bin/env python3
"""Check DCMA 14-point build metrics on a schedule exported to CSV."""
import csv
import re
import sys

HARD = {"must start on", "must finish on", "start no later than",
        "finish no later than", "mso", "mfo", "snlt", "fnlt"}
LINK = re.compile(r"^\s*([A-Za-z0-9.-]+?)\s*(FS|SS|FF|SF)?\s*([+-]\s*\d+(?:\.\d+)?)?\s*[A-Za-z]*\s*$", re.I)

def num(text):
    match = re.search(r"-?\d+(?:\.\d+)?", text or "")
    return float(match.group()) if match else 0.0

rows = [r for r in csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8-sig"))
        if (r.get("summary") or "").strip().lower() not in ("yes", "true", "1")]
ids = {r["id"].strip() for r in rows}
links, has_succ = [], set()
for r in rows:
    for part in re.split(r"[;,]", r.get("predecessors") or ""):
        if not part.strip():
            continue
        m = LINK.match(part)
        if not m:
            print(f"  could not parse predecessor '{part}' on task {r['id']}")
            continue
        pred, kind, lag = m.group(1), (m.group(2) or "FS").upper(), num(m.group(3))
        links.append((pred, r["id"].strip(), kind, lag))
        has_succ.add(pred)

n, nl = len(rows), max(len(links), 1)
pct = lambda count, total: 100.0 * count / max(total, 1)
# The project start and finish milestones are the two legitimate open ends.
exempt = {rows[0]["id"].strip(), rows[-1]["id"].strip()}
missing = [r["id"] for r in rows if r["id"].strip() not in exempt
           and (not (r.get("predecessors") or "").strip() or r["id"].strip() not in has_succ)]
checks = [
    ("1 Logic (missing pred/succ)", pct(len(missing), n), "<=", 5),
    ("2 Leads", pct(sum(1 for l in links if l[3] < 0), nl), "<=", 0),
    ("3 Lags", pct(sum(1 for l in links if l[3] > 0), nl), "<=", 5),
    ("4 FS relationships", pct(sum(1 for l in links if l[2] == "FS"), nl), ">=", 90),
    ("5 Hard constraints", pct(sum(1 for r in rows
        if (r.get("constraint") or "").strip().lower() in HARD), n), "<=", 5),
    ("6 High float (>44d)", pct(sum(1 for r in rows if num(r.get("total_float_days")) > 44), n), "<=", 5),
    ("7 Negative float", pct(sum(1 for r in rows if num(r.get("total_float_days")) < 0), n), "<=", 0),
    ("8 High duration (>44d)", pct(sum(1 for r in rows if num(r.get("duration_days")) > 44), n), "<=", 5),
    ("10 Missing resources", pct(sum(1 for r in rows if num(r.get("duration_days")) > 0
        and not (r.get("resources") or "").strip()), n), "<=", 0),
]
print(f"{n} tasks, {len(links)} relationships")
for name, value, op, limit in checks:
    ok = value <= limit if op == "<=" else value >= limit
    print(f"{'PASS' if ok else 'FAIL'}  {name:<30} {value:6.1f}%  (target {op} {limit}%)")
print("Exempt as start and finish milestones:", ", ".join(sorted(exempt)))
print("Tasks missing a predecessor or successor:", ", ".join(missing) or "none")
```

Save it as `dcma_check.py` and run it:

```bash
python3 dcma_check.py bnm-ims.csv
```

## Validation and Troubleshooting

- **Every task fails the logic check.** The predecessor column was exported as
  task names or unique IDs rather than the IDs in the `id` column. Export
  matching identifiers.
- **"could not parse predecessor" messages.** The tool used a notation the script
  does not expect (for example lags in hours or elapsed days). Normalize the
  column, or extend the regular expression.
- **Float and duration counts look wrong.** Check that the exported values are in
  working days. Some tools export durations in hours or elapsed days.
- **The start and finish milestones show as missing logic.** The script exempts
  the first and last rows only. If your export is not in schedule order, sort it
  so the start milestone is first and the finish milestone is last.
- **A failure is legitimate.** Record the justification (for example, a
  contractual milestone constraint) and report it alongside the metric.

## Security and Best Practices

- Run the health check before every delivery of the IMS, and keep the results
  with the delivered file.
- Treat negative float and leads as must-fix items, not reporting details.
- Use metric trends, not single snapshots: rising high-float counts often mean
  logic is being lost as the schedule grows.
- Exports contain program data; store them as carefully as the IMS itself.

## References and Knowledge Checks

**References:**

- Defense Contract Management Agency, 14-point schedule assessment and DCMA EVMS
  Compliance Metrics (DECM).
- U.S. GAO, *Schedule Assessment Guide: Best Practices for Project Schedules*
  (GAO-16-89G).
- NDIA, *Planning and Scheduling Excellence Guide (PASEG)*.
- Microsoft Project export documentation; Primavera P6 schedule check
  documentation; ProjectLibre documentation.

**Knowledge checks:**

1. Name the eight DCMA metrics that test how a schedule is built.
2. What are the thresholds for leads, lags, and finish-to-start relationships?
3. Write the formulas for CPLI and BEI.
4. Which GAO characteristic covers schedule risk analysis?
5. Why is splitting tasks to pass the high-duration check a bad idea?

## Hands-On Lab

**Objective:** Export the sample IMS, check it with the script, and fix what
fails.

**Shared prerequisites** — the resource-loaded sample program from Chapter 04,
Python 3, and a spreadsheet tool. **Cost:** none.

### Lab 6.1 — Export and check

**Objective:** Run the DCMA build checks on the sample IMS.

1. Export the task table with the columns in the Implementation section and save
   it as `bnm-ims.csv`.
2. Save the script as `dcma_check.py` and run it.

**Expected result:** a pass or fail for each metric. With the sample program as
built in Chapter 04, logic passes (tasks 1 and 25 are reported as exempt); leads,
lags, relationship types, constraints, negative float, and duration pass (the one
SS link with a lag keeps lags at about 4 percent and finish-to-start at about 96
percent); high float passes narrowly at 4 percent, because only task 22 (48 days)
exceeds 44; and resources fail for the discrete tasks you did not
resource-load.

**Negative test:** delete task 22's link to task 23 and re-export. Task 22 now
has no successor and appears in the missing-logic list, yet the logic metric
still passes at 4 percent: on a schedule this small, one open end is under the 5
percent threshold. That is why you read the list, not just the percentage.
Restore the link.

**Rollback:** restore any links you removed.

### Lab 6.2 — Fix the failures

**Objective:** Clear or justify every failure.

1. For missing resources, assign resources to the remaining tasks with duration.
2. For task 22's high float, decide whether logic is missing (is there a later
   task that really needs the training materials?) or whether the float is real.
   If it is real, record a justification.
3. Re-export and re-run.

**Expected result:** all build metrics pass, or each remaining failure has a
written justification.

**Negative test:** "fix" task 22's float by linking it to task 21 with no real
dependency. The metric passes, but the logic is now false. Remove the fake link
and keep the justification instead.

**Rollback:** remove any fake links.

### Lab 6.3 — Run the critical path test

**Objective:** Perform DCMA metric 12 by hand.

1. Note the finish date of task 25.
2. Add 10 days to task 16 `Cut over Site A`, a critical task.
3. Check that task 25 moves exactly 10 working days later.

**Expected result:** the finish moves by exactly 10 working days, so the critical
path passes the test.

**Negative test:** add 10 days to task 13 instead, which has 21 days of float.
The finish does not move, which is correct for a non-critical task and shows why
the test must use a critical task.

**Rollback:** restore the original durations.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The DCMA 14-point assessment screens schedule health with metrics for logic,
leads, lags, relationship types, constraints, float, duration, invalid dates,
resources, missed tasks, the critical path test, CPLI, and BEI. The GAO's ten
best practices add judgment about completeness, construction, credibility, and
control. A simple export and script can check the build metrics in any of the
three tools, and every failure should be either fixed or justified, never gamed.

- [ ] Can explain all 14 DCMA metrics and their thresholds.
- [ ] Can map the GAO best practices to checks.
- [ ] Can export a schedule and run the build checks.
- [ ] Can tell a real problem from a justified exception.
- [ ] Completed Labs 6.1–6.3 including each negative test.
