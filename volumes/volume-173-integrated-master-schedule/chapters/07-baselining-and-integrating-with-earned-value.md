# Chapter 07: Baselining and Integrating with Earned Value

## Learning Objectives

- Explain what a schedule baseline captures and when to set it.
- Describe the performance measurement baseline (PMB) and how the IMS supplies
  its time phasing.
- Calculate the core earned value measures: planned value, earned value, actual
  cost, variances, and performance indices.
- Calculate the schedule-specific indices BEI and CPLI, and earned schedule.
- Set a baseline and read earned value fields in Microsoft Project, Primavera P6,
  and ProjectLibre.

## Theory and Architecture

A forecast means little without something to compare it to. The **baseline** is
the approved plan, frozen. Every variance the program reports, in dates or in
dollars, is a comparison between current status and that baseline. On programs
with earned value management (EVM), the IMS baseline is also the time-phased
backbone of the cost baseline.

### What a baseline captures

When you set a baseline, the tool copies each task's current planned values into
baseline fields:

| Baseline field | Compared against |
| --- | --- |
| Baseline start and finish | Current (forecast or actual) start and finish |
| Baseline duration | Current duration |
| Baseline work | Current and actual work |
| Baseline cost, time-phased | Earned value and actual cost |

Set the baseline once the schedule is complete, passes its health checks
(Chapter 06), and has been approved. After that, change it only through formal
change control (Chapter 08). A baseline that is quietly reset whenever the
program slips measures nothing.

### The performance measurement baseline

On an EVM program, budgets are assigned to control accounts and spread over time
according to the IMS. The total of all time-phased control account budgets, plus
any budget not yet distributed, forms the **performance measurement baseline
(PMB)**:

```text
Contract budget base
├── Management reserve          held outside the PMB for in-scope unknowns
└── Performance measurement baseline (PMB)
    ├── Control accounts         budgets time-phased by the IMS tasks
    │   ├── Work packages        detailed, near-term
    │   └── Planning packages    far-term, not yet detailed
    └── Undistributed budget     authorized but not yet assigned
```

Because the IMS and the cost system share the same work packages, the IMS sets
*when* each dollar of budget is planned to be earned. That is the integration in
"integrated master schedule."

### Earned value measures

| Measure | Also called | Definition |
| --- | --- | --- |
| **Planned value (PV)** | BCWS | Budget for the work scheduled to be done by the status date |
| **Earned value (EV)** | BCWP | Budget for the work actually done by the status date |
| **Actual cost (AC)** | ACWP | What the work actually done has cost |
| **Schedule variance (SV)** | | EV − PV |
| **Cost variance (CV)** | | EV − AC |
| **Schedule performance index (SPI)** | | EV ÷ PV |
| **Cost performance index (CPI)** | | EV ÷ AC |
| **Budget at completion (BAC)** | | Total budget |
| **Estimate at completion (EAC)** | | Forecast total cost; one common formula is BAC ÷ CPI |

A worked example: BAC is $200,000. At the status date, PV is $100,000, EV is
$80,000, and AC is $95,000.

```text
SV  = 80,000 − 100,000 = −20,000   (behind schedule)
CV  = 80,000 −  95,000 = −15,000   (over cost)
SPI = 80,000 ÷ 100,000 = 0.80
CPI = 80,000 ÷  95,000 = 0.84
EAC = 200,000 ÷ 0.84  ≈ 237,500
```

**Earned value techniques** decide how much EV a task earns as it progresses:
0/100 (earned only at completion), 50/50 (half at start, half at finish),
percent complete, weighted milestones, units complete, and level of effort
(earned with the passage of time, so it can never show a schedule variance).
Choose the technique per work package and keep it consistent.

### Schedule indices

SPI is measured in dollars, and it drifts back to 1.0 at the end of a late
program, because all the budget is eventually earned. Schedule-specific measures
complement it:

| Measure | Formula | Reading |
| --- | --- | --- |
| **Baseline Execution Index (BEI)** | Tasks completed ÷ tasks baselined to finish by the status date | Below 0.95 means tasks are finishing late |
| **Critical Path Length Index (CPLI)** | (Remaining critical path length + total float to the baseline finish) ÷ remaining critical path length | Below 0.95 means the baseline finish is at risk |
| **Earned schedule (ES)** | The time at which the current EV was planned to be earned | Compare with actual time (AT): SV(t) = ES − AT, SPI(t) = ES ÷ AT |

Earned schedule converts the dollar-based SPI into time. If EV of $80,000 was
planned to be earned at week 8, but the status date is week 10, then ES is 8
weeks, SV(t) is −2 weeks, and SPI(t) is 0.80, and unlike SPI it does not drift
back to 1.0 as the program finishes late.

## Design Considerations

- **Baseline only a healthy schedule.** Baselining a schedule with open ends or
  hard constraints locks the defects into every future comparison.
- **Keep baseline and current values separate.** Never overwrite baseline fields
  during status updates.
- **Use spare baseline slots for history, not the primary baseline.** Microsoft
  Project and ProjectLibre offer extra baseline sets (Baseline1 to Baseline10);
  Primavera P6 keeps baselines as separate project copies. Use them to snapshot
  history, and keep the primary baseline as the approved plan.
- **Pick earned value techniques that measure real progress.** Percent complete
  invites optimism; objective milestones are harder to inflate.
- **Reconcile the IMS and cost tool every cycle.** If the IMS feeds a separate EVM
  cost tool (common on large programs), dates and budgets must agree.

## Implementation and Automation

| Action | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Set the baseline | **Project > Set Baseline > Set Baseline**, choose **Baseline** and **Entire project** | **Project > Maintain Baselines > Add** (save a copy of the current project), then **Project > Assign Baselines** to make it the project baseline | **Save Baseline** (in the Project or Tools menu, depending on version) |
| See baseline bars | **Tracking Gantt** view | **View > Bars**: show the project baseline bar | Tracking Gantt view |
| Show variances | Add **Start Variance** and **Finish Variance** columns, or the **Variance** table | Add **Variance - BL Project Start Date** and **Finish Date** columns | Add the baseline and variance columns |
| Earned value fields | **View > Tables > More Tables > Earned Value** (BCWS, BCWP, ACWP, SV, CV, EAC, VAC) and the CPI and SPI fields | Add **Planned Value Cost**, **Earned Value Cost**, **Actual Total Cost**, **Schedule Performance Index**, and **Cost Performance Index** columns; set the technique in **Admin Preferences > Earned Value** | Earned value columns similar to Microsoft Project's |
| Status date | **Project > Status Date** | **Data date** (set when updating progress) | Status date in project information |

## Validation and Troubleshooting

- **All earned value fields are zero.** No baseline is set, no status date is
  set, or no costs are loaded. EVM needs all three.
- **Variances appear immediately after baselining.** The baseline was set before
  final edits, or some tasks were added after baselining (they have no baseline
  values). Baseline the new tasks through change control.
- **SPI is near 1.0 but the program is clearly late.** That is the dollar-based
  SPI drifting at the end of a program. Use BEI, CPLI, and SPI(t).
- **Primavera P6 shows no baseline bars.** The baseline copy exists but is not
  assigned. Use **Project > Assign Baselines**.

## Security and Best Practices

- Protect the baseline: restrict who can set or change it, and keep a record of
  every baseline change with its approval.
- Save the baseline file (or P6 baseline copy) with a date and change number.
- Report variances against the approved baseline only, never against a "current
  baseline" that has been reset informally.
- Keep management reserve outside the PMB and track its use separately.

## References and Knowledge Checks

**References:**

- EIA-748, *Earned Value Management Systems*.
- DoD *Earned Value Management Implementation Guide* (EVMIG).
- U.S. GAO, *Cost Estimating and Assessment Guide* (EVM chapters) and *Schedule
  Assessment Guide* (GAO-16-89G), best practice on maintaining a baseline.
- Project Management Institute, *Practice Standard for Earned Value Management*.

**Knowledge checks:**

1. What does a schedule baseline capture?
2. What makes up the performance measurement baseline, and what sits outside it?
3. With PV $50,000, EV $45,000, and AC $60,000, calculate SV, CV, SPI, and CPI.
4. Why does SPI drift toward 1.0 on a late program, and what measures do not?
5. Write the formula for BEI.

## Hands-On Lab

**Objective:** Baseline the sample IMS, record progress, and read the variances
and earned value.

**Shared prerequisites** — the health-checked sample program from Chapter 06,
with resources and costs loaded. **Cost:** none.

### Lab 7.1 — Set the baseline

**Objective:** Freeze the approved plan.

1. Set the baseline for the entire project, as shown in the Implementation
   section.
2. Switch to the Tracking Gantt (or show baseline bars in Primavera P6).

**Expected result:** each task shows a baseline bar matching its current bar,
and finish variance is zero everywhere.

**Negative test:** add a new task after baselining. It has no baseline bar and no
baseline dates, which is how unbaselined scope shows up. Delete it.

**Rollback:** keep the baseline; Chapter 08 builds on it.

### Lab 7.2 — Record progress and read variances

**Objective:** Create a schedule variance.

1. Set the status date (data date) to day 40 of the project.
2. Record tasks 1 to 9 and task 12 as complete. Enter task 8 as finishing 5 days
   late, which makes task 9 finish 5 days late too. Mark task 10 as started on the
   day after task 9 finished.
3. Recalculate (in Primavera P6, schedule with the new data date).

**Expected result:** tasks 8 and 9 show a 5-day finish variance, and because they
are on the critical path, the project finish shows a 5-day finish variance too.

**Negative test:** make task 6 (21 days of float) finish 5 days late instead of
task 8. Task 6 shows a variance, but the project finish does not move.

**Rollback:** revert to the copy saved before the lab, or undo the progress
entries.

### Lab 7.3 — Calculate BEI and SPI

**Objective:** Compute schedule indices from the lab data.

1. Count the tasks whose baseline finish is on or before the status date, and how
   many of them are actually complete.
2. Calculate BEI.
3. Read SPI from the earned value fields.

**Expected result:** ten tasks (1 to 9 and 12) were baselined to finish by day
40, and all ten are complete, so BEI is 1.0 even though two finished late. SPI is
below 1.0, because hardware delivery started 5 days late and has earned less than
planned. BEI and SPI measure different things.

**Negative test:** record task 8 as still in progress at the status date (so task
9 cannot be complete either). BEI drops to 0.8, because two of the ten tasks due
by the status date have not finished.

**Rollback:** revert to the saved copy.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The baseline freezes the approved plan's dates, durations, work, and time-phased
cost, and every variance is measured against it. On EVM programs, the IMS
time-phases the control account budgets that form the performance measurement
baseline. Earned value compares planned value, earned value, and actual cost to
give variances and indices, while BEI, CPLI, and earned schedule measure schedule
performance in terms that do not drift as a late program finishes. Baselines
change only through formal change control.

- [ ] Can explain what a baseline captures and when to set it.
- [ ] Can describe the PMB and its relationship to the IMS.
- [ ] Can calculate SV, CV, SPI, CPI, and a simple EAC.
- [ ] Can calculate BEI and explain CPLI and earned schedule.
- [ ] Completed Labs 7.1–7.3 including each negative test.
