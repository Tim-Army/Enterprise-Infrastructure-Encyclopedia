# Chapter 03: Building the Network — Activities, Logic, and Relationships

## Learning Objectives

- Write well-formed activities that are discrete, measurable, and owned.
- Use the four relationship types correctly, and explain why finish-to-start
  should dominate.
- Explain the risks of leads, lags, and date constraints, and use deadlines
  instead of hard constraints where possible.
- Build a complete network with no open ends, so dates flow from logic.
- Enter the sample program's network in Microsoft Project, Primavera P6, or
  ProjectLibre.

## Theory and Architecture

A schedule is a **network**: tasks connected by logic. If the logic is right, the
tool computes every date, and a change to one task correctly moves everything
that depends on it. If the logic is wrong or missing, the dates are just numbers
someone typed, and the schedule cannot forecast anything. The GAO lists
"sequencing all activities" as a core best practice for exactly this reason.

### Well-formed activities

| Property | Good | Poor |
| --- | --- | --- |
| **Named as verb + object** | `Test configuration templates` | `Templates` |
| **Discrete** | Has a clear start, finish, and deliverable | "Ongoing support" mixed into discrete work |
| **Measurable** | Progress can be judged objectively | "Work on design" |
| **Owned** | One responsible person or team | Shared by everyone and owned by no one |
| **Sized for control** | Usually no longer than about 44 working days (two months) | A six-month task that hides problems until it is late |

**Level of effort (LOE)** work, such as program management or ongoing support,
does not produce discrete deliverables. Keep LOE tasks in the schedule for cost
and resources, but never let them drive dates: they should not be predecessors
of discrete work, and they should not appear on the critical path.

### The four relationship types

| Type | Meaning | Example |
| --- | --- | --- |
| **Finish-to-start (FS)** | B starts after A finishes | Order hardware → Hardware delivery |
| **Start-to-start (SS)** | B starts after A starts | Develop templates → Prepare training materials (start together, offset by a lag) |
| **Finish-to-finish (FF)** | B finishes after A finishes | Write test report → Run acceptance tests (the report finishes after testing) |
| **Start-to-finish (SF)** | B finishes after A starts | Rare; mostly shift handovers. Avoid in an IMS |

Finish-to-start is the clearest and most robust relationship. Schedule guidance,
including the DCMA 14-point assessment (Chapter 06), expects at least 90 percent
of relationships to be finish-to-start. Overusing SS and FF makes the critical
path hard to follow and can hide where work actually overlaps.

### Leads, lags, and why they are suspect

A **lag** delays a successor (`FS+5d` means B starts five days after A finishes).
A **lead** is a negative lag (`FS-5d` means B starts five days *before* A
finishes).

- **Leads** are not allowed in a well-built IMS. They assert that a successor can
  start before its predecessor is done, without saying what part of the
  predecessor it depends on. Split the predecessor instead.
- **Lags** should be rare and should never represent work. "Wait 30 days for
  delivery" is real work by a supplier; model it as a task (`Hardware delivery`,
  30 days) so it can be statused and owned. A lag is acceptable for a true
  waiting period, such as concrete curing, documented in a note.

### Constraints and deadlines

A **constraint** restricts when a task can be scheduled, overriding pure logic.

| Constraint | Type | Effect |
| --- | --- | --- |
| **As Soon As Possible (ASAP)** | None (the default) | The task is scheduled by logic only |
| **Start No Earlier Than (SNET)**, **Finish No Earlier Than (FNET)** | Soft | The task cannot be earlier than the date, but logic can push it later |
| **Start No Later Than (SNLT)**, **Finish No Later Than (FNLT)** | Hard (in schedule-quality terms) | The task cannot be later than the date; logic that would push it later is overridden or creates negative float |
| **Must Start On (MSO)**, **Must Finish On (MFO)** | Hard | The date is fixed regardless of logic |
| **As Late As Possible (ALAP)** | Special | The task consumes all its float; it can delay the finish when combined with uncertainty |

Hard constraints break the network: a slipping predecessor no longer moves the
task, so the schedule stops telling the truth. Limit them (DCMA expects no more
than 5 percent of tasks), and prefer a **deadline**, which flags a late finish
without moving the task. Microsoft Project has a **Deadline** field;
Primavera P6 uses a project *must finish by* date and secondary constraints;
ProjectLibre supports deadlines as a task field.

### No open ends

Every task needs at least one predecessor and one successor, except the project
start milestone (no predecessor) and the finish milestone (no successor). A task
with no successor is an **open end** or **dangling** task: if it slips, nothing
moves, and its delay is invisible. Linking tasks to summary tasks instead of to
other tasks has a similar effect and should be avoided.

## Design Considerations

- **Model external dependencies as milestones.** Government-furnished equipment,
  customer approvals, and supplier deliveries should be explicit milestones with
  owners, linked into the network.
- **Link at the task level, never to summary tasks.** Summary links make logic
  hard to trace and can produce surprising dates.
- **Write logic for how the work really flows, not how resources are scheduled.**
  If sites are cut over one after another because one crew does them all, that is
  a resource dependency. Model it with logic only if the constraint is real and
  documented; otherwise use resource leveling (Chapter 04).
- **Review logic with the people doing the work.** The scheduler owns the
  network's integrity, but the CAMs and engineers own the facts.
- **Keep a clear path from start to finish.** You should be able to trace an
  unbroken chain of logic from the start milestone to the finish milestone
  through every task.

## Implementation and Automation

### The sample program's network

Enter these tasks under the WBS elements from Chapter 02. Durations are in
working days; Chapter 04 refines them. Predecessors use the common notation
`ID` + relationship type + lag (finish-to-start with no lag is just the ID).

| ID | Task | WBS | Dur. | Predecessors |
| --- | --- | --- | --- | --- |
| 1 | Project start | 1 | 0 | — |
| 2 | Hold kickoff meeting | 1.1 | 1 | 1 |
| 3 | Gather site requirements | 1.2.1 | 10 | 2 |
| 4 | Draft network design | 1.2.2 | 10 | 3 |
| 5 | Review network design | 1.2.2 | 5 | 4 |
| 6 | Deliver network design document | 1.2.2 | 2 | 5 |
| 7 | A Design Complete | 1.2 | 0 | 6 |
| 8 | Finalize bill of materials | 1.3 | 3 | 5 |
| 9 | Order hardware | 1.3 | 2 | 8 |
| 10 | Hardware delivery | 1.3 | 30 | 9 |
| 11 | Receive and inventory hardware | 1.3 | 3 | 10 |
| 12 | Build lab environment | 1.4 | 5 | 7 |
| 13 | Develop configuration templates | 1.4 | 10 | 12 |
| 14 | Test templates in lab | 1.4 | 5 | 11, 13 |
| 15 | B Ready to Deploy | 1.4 | 0 | 14 |
| 16 | Cut over Site A | 1.5.1 | 5 | 15 |
| 17 | Cut over Site B | 1.5.2 | 5 | 16 |
| 18 | Cut over Site C | 1.5.3 | 5 | 17 |
| 19 | Cut over Site D | 1.5.4 | 5 | 18 |
| 20 | C All Sites Cut Over | 1.5 | 0 | 19 |
| 21 | Run acceptance testing | 1.6 | 10 | 20 |
| 22 | Prepare training materials | 1.7 | 10 | 13SS+5d |
| 23 | Deliver training | 1.7 | 3 | 20, 22 |
| 24 | D Final Acceptance | 1.6 | 0 | 21, 23 |
| 25 | Project finish | 1 | 0 | 24 |

The sites are cut over one after another because a single deployment team
does them all. That is a resource constraint, written here as logic for
simplicity; Chapter 04 revisits it.

### Entering logic in each tool

| Action | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Finish-to-start link | Select both tasks, **Task > Link** (Ctrl+F2), or type the ID in the **Predecessors** column | Activity Details, **Predecessors** tab, **Assign** | Select both tasks and use the link button, or enter the ID in the **Predecessors** column |
| Other types and lags | In the Predecessors column, type `13SS+5d`, or use **Task Information > Predecessors** | Set **Relationship Type** and **Lag** in the Predecessors tab | In **Task Information > Predecessors**, set the type and lag |
| Constraint | **Task Information > Advanced > Constraint type** | Activity Details, **Status** tab, **Primary Constraint** | **Task Information > Advanced** (constraint type and date) |
| Deadline | **Task Information > Advanced > Deadline** | Project-level must-finish-by date, or a secondary constraint | Task deadline field |
| Find open ends | Filter for tasks with an empty Successors column | Add **Predecessors** and **Successors** columns and filter for blanks | Add Predecessors and Successors columns and sort |
| Trace drivers | **Task > Inspect** (Task Inspector) and **Format > Task Path** | **Trace Logic** view | Network diagram view |

## Validation and Troubleshooting

- **A task does not move when its predecessor slips.** Check for a hard
  constraint, a manually scheduled task (Microsoft Project), or an actual date
  already recorded.
- **Negative float appears.** A hard constraint or deadline-style constraint
  conflicts with logic: the logic says the task finishes later than the
  constraint allows. Investigate and fix the plan; do not delete the constraint
  to hide it.
- **The finish date is driven by an unexpected task.** Trace the driving path
  (Task Inspector, Task Path, or Trace Logic). A missing or wrong link usually
  explains it.
- **The schedule finishes impossibly early.** Look for open ends. Work with no
  successor does not push the finish milestone.

## Security and Best Practices

- Document every lag and every constraint in a task note: who asked for it and
  why. Unexplained constraints are among the first things assessors question.
- Re-check the network after every major change, because new tasks are the most
  common source of open ends.
- Keep the start and finish milestones as the only tasks without a predecessor or
  successor.
- Protect the logic from casual edits. Status updates should change progress, not
  links.

## References and Knowledge Checks

**References:**

- U.S. GAO, *Schedule Assessment Guide* (GAO-16-89G), best practices on
  sequencing activities and confirming the critical path.
- NDIA, *Planning and Scheduling Excellence Guide (PASEG)*, sections on logic,
  constraints, leads, and lags.
- Microsoft Project, Primavera P6, and ProjectLibre help on predecessors,
  relationship types, and constraints.

**Knowledge checks:**

1. Name the four relationship types and the one that should dominate.
2. Why are leads not allowed in an IMS?
3. Why should a supplier's delivery time be a task rather than a lag?
4. What is the difference between a hard constraint and a deadline?
5. What is an open end, and why is it dangerous?

## Hands-On Lab

**Objective:** Enter the sample network, prove it is complete, and see what
constraints and open ends do.

**Shared prerequisites** — the project from Chapter 02 with the WBS and
milestones. **Cost:** none.

### Lab 3.1 — Enter the network

**Objective:** Build the full task network.

1. Enter tasks 1 to 25 from the Implementation section under their WBS elements
   (tasks 7, 15, 20, and 24 are the milestones you created in Chapter 02).
2. Enter durations and predecessors, including `13SS+5d` on task 22.

**Expected result:** a linked schedule whose finish milestone falls about 99
working days after the project start. Every task's dates come from logic.

**Negative test:** delete the link from task 23 to task 24. Lengthen task 23 by
20 days. Task 24 does not move, because task 23 now has no successor. Restore the
link and the finish moves.

**Rollback:** restore task 23's original duration and links.

### Lab 3.2 — Find open ends

**Objective:** Prove every task is linked.

1. Show the Predecessors and Successors columns.
2. Filter or sort to find tasks with an empty predecessor or successor.

**Expected result:** only task 1 (no predecessor) and task 25 (no successor)
appear.

**Negative test:** add a task `Order spare parts` linked only from task 9. It
appears in the open-end check with no successor. Link it to task 14 or delete it.

**Rollback:** delete the test task if you added it.

### Lab 3.3 — See a hard constraint distort the schedule

**Objective:** Observe negative float.

1. Set task 21 `Run acceptance testing` to **Finish No Later Than** a date five
   working days earlier than its current finish.
2. Recalculate (in Primavera P6, run **Schedule**).
3. Look at total float on the critical tasks.

**Expected result:** critical tasks show negative float (about −5 days), because
logic now says the work cannot finish by the constrained date.

**Negative test:** replace the constraint with a **deadline** on the same date
(in Primavera P6, a project must-finish-by date). The task is flagged as late,
but the network itself is no longer overridden.

**Rollback:** set task 21 back to As Soon As Possible and remove the deadline.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

An IMS is a network: well-formed, discrete, owned activities connected by logic,
so the tool computes every date. Finish-to-start links should dominate; leads
are not allowed and lags should be rare and never stand in for work. Hard
constraints override logic and should be minimal, with deadlines used instead
where possible. Every task except the start and finish milestones needs both a
predecessor and a successor, and external dependencies belong in the network as
milestones.

- [ ] Can write discrete, measurable, owned activities.
- [ ] Can use the four relationship types and explain why FS dominates.
- [ ] Can explain the problems with leads, lags, and hard constraints.
- [ ] Can find and fix open ends.
- [ ] Completed Labs 3.1–3.3 including each negative test.
