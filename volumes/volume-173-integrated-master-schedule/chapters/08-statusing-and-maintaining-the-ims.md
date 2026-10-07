# Chapter 08: Statusing and Maintaining the IMS

## Learning Objectives

- Run a disciplined status cycle around a data date, collecting actual dates,
  remaining durations, and progress.
- Avoid invalid dates and handle out-of-sequence progress with retained logic or
  progress override.
- Move incomplete work past the data date so forecasts stay realistic.
- Control baseline changes through a formal change process, including adding new
  scope.
- Use rolling wave planning to convert planning packages into detailed work.

## Theory and Architecture

A baseline shows the plan; status shows reality. An IMS is only useful if it is
**statused** regularly and honestly, so the forecast reflects what has actually
happened and what remains. The GAO's ninth best practice is exactly this:
"update the schedule using actual progress and logic."

### The status cycle

```text
1. Set the data date          the "as of" date for this cycle
2. Collect status from CAMs   actual starts and finishes, remaining durations
3. Enter status               no actuals after, no forecasts before, the data date
4. Reschedule                 incomplete work moves to after the data date
5. Check health               DCMA metrics, especially invalid dates (Chapter 06)
6. Analyze                    critical path changes, variances, near-critical paths
7. Report and archive         narrative, deliverables, a dated copy of the file
```

Most programs status weekly for internal management and monthly for formal
reporting. The cycle must be the same every time, so period-to-period
comparisons mean something.

### What to collect

| Task state | What to record |
| --- | --- |
| **Complete** | Actual start and actual finish |
| **In progress** | Actual start, plus remaining duration (preferred) or percent complete |
| **Not started** | Nothing, unless the forecast start has changed; then update logic or duration, not a typed date |

**Remaining duration** is more reliable than percent complete. Asking "how many
working days of work are left?" gets a more honest answer than "what percent are
you done?", which tends to sit at 90 percent for weeks.

### Invalid dates

Two kinds of date are always errors, and DCMA metric 9 checks for both:

- An **actual** start or finish *after* the data date: you cannot have done work
  in the future.
- A **forecast** start or finish *before* the data date: incomplete work cannot
  happen in the past.

After status is entered, all incomplete work must be rescheduled to start no
earlier than the data date.

### Out-of-sequence progress

Sometimes a task starts before its predecessor finishes, against the logic. The
tool must decide how to schedule the rest of that task:

| Option | Behavior | When it fits |
| --- | --- | --- |
| **Retained logic** | The remaining work waits for the predecessor to finish | The logic is real; the early start was partial work |
| **Progress override** | The remaining work ignores the predecessor | The logic was wrong; the task really is independent |

Primavera P6 sets this in its schedule options. Microsoft Project behaves closer
to retained logic for in-progress tasks with finish-to-start predecessors, and
offers options for splitting in-progress tasks. Whichever applies, investigate
every out-of-sequence task: it usually means the logic needs correcting.

### Change control

The baseline changes only through an approved **baseline change request
(BCR)**. Typical rules:

- **No retroactive changes.** History before the data date is never rewritten.
- **Freeze period.** Near-term baseline work (for example, the current and next
  month) is not changed except for approved scope changes.
- **New scope gets its own baseline.** When a change adds work, baseline the new
  tasks without re-baselining existing ones, so existing variances stay visible.
- **Re-planning beyond the baseline.** When a program can no longer perform
  against its baseline, a formal **over target baseline (OTB)** or **over target
  schedule (OTS)** may be approved. It is a significant, customer-approved event,
  not a routine reset.

### Rolling wave planning

Far-term work is held in **planning packages** (Chapter 02) because detail would
be guesswork. As the work approaches (often within a six-month window), CAMs
**plan it in detail**: the planning package is replaced by work packages with
discrete tasks, logic, durations, and resources, within the same budget and
dates. Rolling wave planning keeps the near term detailed and the far term
honest.

## Design Considerations

- **Set a fixed status calendar.** Publish the data dates for the year, and the
  deadlines for CAM inputs, so status always describes the same point in time.
- **Status, then analyze, then report.** Never adjust status to make a report look
  better. The report explains the status; it does not shape it.
- **Keep remaining durations honest.** A task whose remaining duration never
  shrinks is a problem to raise, not a number to keep typing.
- **Archive every cycle.** Save a dated copy of the statused file. Trend analysis
  and audits depend on being able to see what the schedule said at each date.
- **Apply change control to logic too.** Big logic changes alter the critical
  path. Record them in the cycle's narrative, even when the baseline is untouched.

## Implementation and Automation

| Action | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Set the data date | **Project > Status Date** | Set **Current Data Date** in the **Schedule** dialog (F9) | Status date in project information |
| Enter actuals | **Task > Mark on Track > Update Tasks**: actual start, actual finish, remaining duration | Activity Details, **Status** tab: **Started**, **Finished**, actual dates, remaining duration | **Update Tasks** dialog or the actual date and percent complete fields |
| Reschedule incomplete work | **Project > Update Project > Reschedule uncompleted work to start after** the status date | Automatic: scheduling with the data date moves remaining work after it | Use the update project command, or reschedule remaining work after the status date manually |
| Out-of-sequence handling | Options in **File > Options > Schedule** and **Advanced** (split in-progress tasks) | **Schedule > Options**: *Retained Logic*, *Progress Override*, or *Actual Dates* | Microsoft Project-like behavior |
| Baseline new scope only | **Set Baseline > Selected tasks**, with *Roll up baselines to all summary tasks* | **Project > Maintain Baselines > Update** (update the baseline for selected activities), or add the activities to a new baseline copy | **Save Baseline** for the selected tasks |
| Save the cycle copy | **File > Save As** with the data date in the name | Create a baseline copy for the cycle, or export to XER | **File > Save As** with the data date in the name |

## Validation and Troubleshooting

- **Forecast dates sit before the data date.** Incomplete work was not
  rescheduled. Run the reschedule step (Microsoft Project, ProjectLibre) or
  schedule with the correct data date (Primavera P6).
- **A completed task has an actual finish in the future.** Someone typed the
  planned finish as the actual. Correct it, and remind CAMs that actuals record
  what happened.
- **The finish date jumped after status.** Look at the critical path: a critical
  task finished late, or a remaining duration grew. Report it; do not absorb it
  silently in margin without noting the margin consumed.
- **New tasks show huge variances.** They were added without baselines, so the
  tool compares them with nothing (or zero). Baseline them through change
  control.
- **Out-of-sequence tasks keep appearing.** The logic does not match how work is
  really done. Fix the logic with the CAMs.

## Security and Best Practices

- Limit who can enter actuals. CAMs supply status; the scheduler enters and
  checks it.
- Keep a log of every BCR: what changed, why, who approved it, and when.
- Never re-baseline to hide variances. Variances are the information the program
  and customer need.
- Archive cycle copies with access controls; they are as sensitive as the live
  IMS.

## References and Knowledge Checks

**References:**

- U.S. GAO, *Schedule Assessment Guide* (GAO-16-89G), best practices on updating
  the schedule and maintaining a baseline.
- NDIA, *Planning and Scheduling Excellence Guide (PASEG)*, sections on status,
  baseline change management, and rolling wave planning.
- EIA-748, *Earned Value Management Systems*, guidelines on change control and
  revisions.

**Knowledge checks:**

1. List the steps of a status cycle in order.
2. Why is remaining duration more reliable than percent complete?
3. Name the two kinds of invalid date.
4. What is the difference between retained logic and progress override?
5. How do you add new scope to a baselined IMS without hiding existing variances?

## Hands-On Lab

**Objective:** Run a full status cycle on the sample IMS, handle an
out-of-sequence task, and add new scope through change control.

**Shared prerequisites** — the baselined sample program from Chapter 07 (a copy
from before the Lab 7.2 progress entries works best). **Cost:** none.

### Lab 8.1 — Run a status cycle

**Objective:** Status the schedule at day 60.

1. Set the data date to day 60.
2. Record tasks 1 to 9 and 12 as complete on their baseline dates.
3. Record task 13 as complete, 3 days late.
4. Record task 10 `Hardware delivery` as in progress with 3 days remaining.
5. Reschedule incomplete work after the data date and recalculate.

**Expected result:** no incomplete work is scheduled before day 60, and the
finish forecast reflects task 10's remaining duration.

**Negative test:** give task 11 an actual start of day 65, after the data date,
and re-run the Chapter 06 health check or inspect the dates. It is an invalid
date. Remove it.

**Rollback:** remove the invalid actual date.

### Lab 8.2 — Handle out-of-sequence progress

**Objective:** See how the tool treats a task that started early.

1. Record task 14 `Test templates in lab` as started on day 58, although its
   predecessor task 11 has not finished.
2. In Primavera P6, schedule once with *Retained Logic* and once with *Progress
   Override*, and compare task 14's forecast finish. In Microsoft Project or
   ProjectLibre, note where the remaining work of task 14 is scheduled.

**Expected result:** with retained logic, task 14's remaining work waits for task
11 to finish; with progress override, it continues straight away and finishes
earlier.

**Negative test:** decide which result is right by asking whether task 14 really
needs the hardware from task 11. If it does, the early start was partial work and
retained logic is correct. If you choose progress override, the logic should be
changed to match.

**Rollback:** remove the actual start from task 14.

### Lab 8.3 — Add new scope through change control

**Objective:** Add a fifth site without hiding existing variances.

1. Under 1.5 Site Deployment, add `1.5.5 Site E` with task `Cut over Site E` (5
   days), linked after task 19 and before task 20.
2. Baseline only the new task, rolling the baseline up to summaries.
3. Record the change in a short BCR note: what was added, why, and the approval.

**Expected result:** the new task has its own baseline, the finish forecast moves
5 days later, and the variances of existing tasks are unchanged.

**Negative test:** re-baseline the entire project instead. All existing variances
disappear, including the earlier slips, which hides the program's real
performance. Revert to the copy saved before this step.

**Rollback:** revert to the saved copy, or remove the Site E task and its
baseline.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

An IMS stays useful only through a disciplined status cycle around a fixed data
date: collect actuals and remaining durations, enter them without invalid dates,
reschedule incomplete work after the data date, check health, analyze, report,
and archive. Out-of-sequence progress is handled with retained logic or progress
override and usually signals a logic fix. Baseline changes go through formal
change control, new scope gets its own baseline, and rolling wave planning
details far-term work as it approaches.

- [ ] Can run a complete status cycle.
- [ ] Can avoid and detect invalid dates.
- [ ] Can explain and choose between retained logic and progress override.
- [ ] Can add new scope through change control without hiding variances.
- [ ] Completed Labs 8.1–8.3 including each negative test.
