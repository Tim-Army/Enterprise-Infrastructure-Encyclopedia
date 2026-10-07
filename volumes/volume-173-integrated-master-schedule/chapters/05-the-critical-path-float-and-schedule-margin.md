# Chapter 05: The Critical Path, Float, and Schedule Margin

## Learning Objectives

- Perform a forward and backward pass by hand and compute early and late dates.
- Calculate total float and free float, and explain the difference.
- Identify the critical path and near-critical paths, and know when to use the
  longest path instead of a float threshold.
- Plan schedule margin and explain why it is not the same as float.
- Display critical tasks and float in Microsoft Project, Primavera P6, and
  ProjectLibre.

## Theory and Architecture

The **critical path method (CPM)** finds the earliest possible finish of a
network and the chain of tasks that determines it. Those tasks form the
**critical path**: if any of them slips, the finish slips. Everything else has
some **float**, room to slip without moving the finish. Knowing which tasks are
critical, and by how much the others can move, is the main reason an IMS exists.

### The forward pass

Starting at the project start, compute each task's **early start (ES)** and
**early finish (EF)**:

- ES = the latest EF of its finish-to-start predecessors (adjusted for lags and
  other relationship types).
- EF = ES + duration.

The largest EF in the network is the earliest possible project finish.

### The backward pass

Starting at the project finish, compute each task's **late finish (LF)** and
**late start (LS)**:

- LF = the earliest LS of its finish-to-start successors (adjusted for lags and
  other relationship types).
- LS = LF − duration.

### Float

| Term | Formula | Meaning |
| --- | --- | --- |
| **Total float (TF)** | LS − ES (or LF − EF) | How far the task can slip without delaying the project finish |
| **Free float (FF)** | Earliest ES of successors − EF | How far the task can slip without delaying any successor |

Free float can never exceed total float. A task can have plenty of total float
but no free float, which means any slip pushes its successor even though the
finish is safe.

### The sample program, by hand

Applying both passes to the Chapter 03 network (days counted from the project
start, day 0) gives:

| ID | Task | Dur. | ES | EF | LS | LF | TF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | Hold kickoff meeting | 1 | 0 | 1 | 0 | 1 | **0** |
| 3 | Gather site requirements | 10 | 1 | 11 | 1 | 11 | **0** |
| 4 | Draft network design | 10 | 11 | 21 | 11 | 21 | **0** |
| 5 | Review network design | 5 | 21 | 26 | 21 | 26 | **0** |
| 6 | Deliver network design document | 2 | 26 | 28 | 47 | 49 | 21 |
| 8 | Finalize bill of materials | 3 | 26 | 29 | 26 | 29 | **0** |
| 9 | Order hardware | 2 | 29 | 31 | 29 | 31 | **0** |
| 10 | Hardware delivery | 30 | 31 | 61 | 31 | 61 | **0** |
| 11 | Receive and inventory hardware | 3 | 61 | 64 | 61 | 64 | **0** |
| 12 | Build lab environment | 5 | 28 | 33 | 49 | 54 | 21 |
| 13 | Develop configuration templates | 10 | 33 | 43 | 54 | 64 | 21 |
| 14 | Test templates in lab | 5 | 64 | 69 | 64 | 69 | **0** |
| 16–19 | Cut over Sites A–D | 5 each | 69 | 89 | 69 | 89 | **0** |
| 21 | Run acceptance testing | 10 | 89 | 99 | 89 | 99 | **0** |
| 22 | Prepare training materials | 10 | 38 | 48 | 86 | 96 | 48 |
| 23 | Deliver training | 3 | 89 | 92 | 96 | 99 | 7 |

The project finishes on day 99. The critical path runs through the requirements,
design review, bill of materials, ordering, the 30-day hardware delivery,
receiving, lab testing, the four cutovers, and acceptance testing. The design
document and template development have 21 days of float, because they wait on
the hardware, not the other way round. That is a useful insight: speeding up the
design document does nothing for the finish date, while a faster supplier does.

### Critical path definitions

Tools offer two ways to flag critical tasks:

| Definition | How it works | Weakness |
| --- | --- | --- |
| **Total float threshold** | Tasks with total float at or below a value (usually 0) are critical | Misleading with multiple calendars or constraints, where float differs for reasons unrelated to the finish |
| **Longest path** | The continuous chain of driving relationships from start to finish | Requires the tool to trace driving logic; best for complex schedules |

On a clean schedule both give the same answer. When they differ, the longest
path is usually the true critical path. Also watch **near-critical** paths (for
example total float of 10 days or less): they can become critical with a modest
slip.

### Schedule margin

**Schedule margin** is time the program deliberately holds between the planned
finish of the work and a committed date, to absorb risk. Model it as a task
named clearly as margin, owned by the program manager, placed just before the
committed milestone:

```text
... → Run acceptance testing → D Final Acceptance → [Schedule margin, 10 days] → Contract delivery
```

Margin is not float. **Float** falls out of the network logic and belongs to the
paths that have it. **Margin** is a planned, visible buffer controlled by
management and consumed deliberately as risks occur. Hiding contingency inside
inflated task durations does the opposite: nobody can see or manage it.

## Design Considerations

- **Report the critical path every cycle.** It changes as work progresses.
  Program reviews should look at the current critical path and the near-critical
  paths, not last month's.
- **Expect a sensible critical path.** It should run from start to finish
  through discrete work, not through LOE tasks, constraints, or lags. A critical
  path made of administrative tasks indicates broken logic.
- **Investigate very high float.** Tasks with hundreds of days of float usually
  have missing successors. DCMA flags float above 44 working days (Chapter 06).
- **Investigate negative float immediately.** It means a constraint or deadline
  cannot be met with the current plan.
- **Size margin from risk, not habit.** Schedule risk analysis (Chapter 09) gives
  a defensible margin.

## Implementation and Automation

| Action | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Highlight critical tasks | **Gantt Chart Format > Critical Tasks** | Critical activities are shown on the Gantt bars after scheduling; filter with **View > Filter By > Critical** | Critical tasks are drawn in red on the Gantt chart |
| Show float | Add **Total Slack** and **Free Slack** columns | Add **Total Float** and **Free Float** columns | Add the total slack and free slack columns |
| Show early and late dates | Add **Early Start**, **Early Finish**, **Late Start**, **Late Finish** | Add **Early Start**, **Early Finish**, **Late Start**, **Late Finish** | Add the early and late date columns |
| Critical definition | **File > Options > Advanced**: *Tasks are critical if slack is less than or equal to* | **Tools > Schedule > Options**: *Define critical activities as* Total Float or Longest Path | Uses total slack |
| Trace the driving path | **Format > Task Path > Driving Predecessors**, and **Task > Inspect** | Schedule with **Longest Path**; use **Trace Logic** | Network diagram view |

## Validation and Troubleshooting

- **No tasks show as critical.** A constraint or deadline is creating positive
  float on every path, or the finish milestone has a constraint. Check the finish
  milestone and the critical definition.
- **Many unrelated tasks show as critical.** Look for open ends and hard
  constraints. A task with no successor can show zero float without being on the
  real critical path.
- **Your hand calculation disagrees with the tool.** Check calendars and
  holidays, and that durations are in working days. The tool counts calendar
  dates; the hand calculation counts working days.
- **Margin shows up as the only critical task.** Margin is on the critical path
  by design. Look at the driving path *into* the margin task to see the real
  critical work.

## Security and Best Practices

- Never shorten a critical path by deleting logic. If the plan must finish
  earlier, change the work (fast-track or crash) and document it.
- Keep margin visible and controlled by the program manager. Track how much has
  been consumed each cycle.
- Show near-critical paths alongside the critical path in program reviews.
- Re-check the critical path after every significant change to logic.

## References and Knowledge Checks

**References:**

- U.S. GAO, *Schedule Assessment Guide* (GAO-16-89G), best practices on
  confirming the critical path and ensuring reasonable total float.
- NDIA, *Planning and Scheduling Excellence Guide (PASEG)*, sections on the
  critical path and schedule margin.
- Microsoft Project, Primavera P6, and ProjectLibre help on slack, float, and the
  critical path.

**Knowledge checks:**

1. Give the formulas for ES, EF, LS, LF, and total float.
2. Why can free float never exceed total float?
3. In the sample program, why does the design document have 21 days of float?
4. When is the longest path more reliable than a total float threshold?
5. What is the difference between schedule margin and float?

## Hands-On Lab

**Objective:** Prove the hand calculation in your tool, find the critical path,
and add schedule margin.

**Shared prerequisites** — the sample network from Chapter 03, restored to the
99-day plan. **Cost:** none.

### Lab 5.1 — Check the hand calculation

**Objective:** Compare the tool's float with the table in this chapter.

1. Add the early start, late start, total float, and free float columns.
2. Compare total float for tasks 6, 12, 13, 22, and 23 with the table.

**Expected result:** total float of 21 days for tasks 6, 12, and 13, 48 days for
task 22, 7 days for task 23, and 0 for the critical tasks.

**Negative test:** change task 10 `Hardware delivery` from 30 to 5 days, a
25-day improvement. The finish moves only 21 days earlier, to day 78, because the
critical path switches: tasks 6, 7, 12, and 13 (the design document and template
work) now have zero float and drive lab testing, while the hardware tasks gain 4
days of float. Shortening one path only helps until another path becomes the
longest. Restore 30 days.

**Rollback:** set task 10 back to 30 days.

### Lab 5.2 — Show and trace the critical path

**Objective:** Highlight critical tasks and trace the driving path to the finish.

1. Turn on critical task highlighting.
2. Trace the driving predecessors of task 25.

**Expected result:** the highlighted path matches the critical path described in
this chapter, running through the hardware delivery and the site cutovers.

**Negative test:** set a **Must Finish On** constraint on task 21 ten days later
than its current finish. The constraint, not the work, now sets the finish: the
hardware and cutover tasks before it gain 10 days of float and stop showing as
critical under a total-float threshold, so the highlighted path no longer shows
which work really matters. Remove the constraint.

**Rollback:** remove the constraint.

### Lab 5.3 — Add schedule margin

**Objective:** Insert visible margin before a committed delivery.

1. Add a task `Schedule margin` (10 days) between task 24 and task 25, and a new
   milestone `Contract delivery` after it.
2. Note the finish date of `Contract delivery`.

**Expected result:** the delivery milestone falls 10 working days after D Final
Acceptance, and the margin task sits on the critical path.

**Negative test:** instead of a margin task, add 10 days to task 21. The finish
is the same, but the buffer is now hidden inside acceptance testing, and nobody
can tell how much of that duration is real work. Undo the change.

**Rollback:** keep the margin task and delivery milestone, or remove them; later
labs work either way.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The critical path method computes early dates with a forward pass and late dates
with a backward pass. Total float measures how far a task can slip without moving
the finish; free float, how far without moving any successor. The critical path
is the chain with no float, or more reliably the longest driving path, and
near-critical paths deserve the same attention. Schedule margin is a visible,
management-owned buffer before a committed date, distinct from the float that
falls out of the network.

- [ ] Can perform forward and backward passes by hand.
- [ ] Can calculate and explain total and free float.
- [ ] Can identify the critical and near-critical paths.
- [ ] Can plan and explain schedule margin.
- [ ] Completed Labs 5.1–5.3 including each negative test.
