# Chapter 04: Durations, Calendars, and Resource Loading

## Learning Objectives

- Estimate task durations with analogous, parametric, bottom-up, and three-point
  methods, and record the basis of each estimate.
- Explain the relationship between duration, work, and units, and how each tool
  models it.
- Use project, task, and resource calendars correctly.
- Load resources and costs onto IMS tasks.
- Find over-allocations and resolve them by leveling or by adjusting the plan.

## Theory and Architecture

Logic decides the *order* of work. Durations and resources decide *how long* it
takes and *who* does it. An IMS whose durations are guesses and whose tasks
carry no resources may compute a date, but it cannot support cost or staffing
decisions, and it fails the resource checks in schedule assessments.

### Estimating durations

| Method | How it works | When to use it |
| --- | --- | --- |
| **Analogous** | Base the estimate on a similar past task | Early, with little detail |
| **Parametric** | Multiply a unit rate by a quantity (for example, four days per site) | Repeatable work with good historical rates |
| **Bottom-up** | Sum estimates of smaller pieces from the people doing the work | Detailed planning of near-term work |
| **Three-point** | Estimate optimistic (O), most likely (M), and pessimistic (P) durations | Uncertain work, and as input to risk analysis (Chapter 09) |

A common three-point formula is the PERT weighted mean, `(O + 4M + P) / 6`. For
hardware delivery with O = 20, M = 30, and P = 50 days, the PERT estimate is
about 31.7 days. Whatever the method, record the **basis of estimate** in a note
or a custom field. Assessors and the people who maintain the schedule later need
to know where each number came from.

### Duration, work, and units

For resourced tasks, three quantities are linked:

```text
Work (hours)  =  Duration (hours)  ×  Units (fraction of a resource's time)

Example: 2 engineers (units 200%) on a 5-day task (40 hours) = 80 hours of work
```

Each tool lets you choose which quantity stays fixed when another changes:

| Tool | Setting | Options |
| --- | --- | --- |
| Microsoft Project | **Task type**, plus the **Effort driven** flag | Fixed Units, Fixed Duration, Fixed Work |
| Primavera P6 | **Duration Type** | Fixed Duration and Units, Fixed Duration and Units/Time, Fixed Units, Fixed Units/Time |
| ProjectLibre | **Task type** in Task Information | Fixed Units, Fixed Duration, Fixed Work (Microsoft Project-like) |

Choose a default deliberately. For most IMS work packages, the duration is the
planned outcome, so **fixed duration** is a common choice: adding a resource
changes the work, not the dates.

### Calendars

| Calendar | Applies to | Example |
| --- | --- | --- |
| **Project calendar** | All tasks by default | Five-day week with public holidays |
| **Task calendar** | One task | A maintenance-window task that can only run on weekends |
| **Resource calendar** | One resource | A contractor's vacation, or a team that works four ten-hour days |

Keep calendars few and well named. Many slightly different calendars make
durations and float hard to compare and are a common source of confusing
dates.

### Resources and cost

A resource can be **labor** (people or teams, with an hourly rate), **material**
(consumed in quantities), or **cost** (a fixed amount such as travel). Loading
resources onto tasks gives the IMS a time-phased view of hours and cost. That is
what earned value is measured against (Chapter 07) and what lets managers see
staffing peaks.

**Over-allocation** happens when a resource is assigned more work in a period
than it has available. **Resource leveling** resolves it by delaying or splitting
tasks within their float, or past it if necessary. Leveling can move the finish
date, so review its results; do not accept them blindly.

## Design Considerations

- **Load resources at the right level.** Name roles or teams (Network Engineer,
  Deployment Team) rather than individuals unless individual names matter.
  Role-based loading survives staff changes.
- **Keep LOE separate.** Program management and similar support work should be
  LOE tasks spanning the period they support, with resources, but without driving
  logic (Chapter 03).
- **Do not add logic just to force resource order.** If tasks are sequential only
  because one team does them all, consider leveling instead of hard-coding the
  order as logic. Either is defensible if documented, but the choice affects what
  the critical path means.
- **Watch long durations.** Tasks longer than 44 working days hide problems and
  are flagged by schedule assessments. Break them up unless they are genuinely
  indivisible, such as a supplier's lead time.
- **Agree rates and units with finance.** If the IMS feeds cost reporting, the
  rates and hours must reconcile with the cost system.

## Implementation and Automation

### Resources for the sample program

| Resource | Type | Max units | Rate (example) |
| --- | --- | --- | --- |
| Project Manager | Labor | 1 | $95/hour |
| Network Engineer | Labor | 2 | $85/hour |
| Deployment Team | Labor | 1 | $240/hour (team rate) |
| Hardware | Cost | — | Lump sum on task 10 |

### Doing it in each tool

| Action | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Define resources | **View > Resource Sheet** | **Enterprise > Resources** | **Resource** view (resource sheet) |
| Assign to a task | **Resource > Assign Resources** (Alt+F10) | Activity Details, **Resources** tab, **Add Resource** | **Task Information > Resources**, or the resource assignment dialog |
| Set task type | **Task Information > Advanced > Task type** | Activity Details, **General** tab, **Duration Type** | **Task Information > Advanced > Task type** |
| See over-allocation | **Resource Usage** view; over-allocated resources show in red | **Resource Usage Profile** and **Resource Usage Spreadsheet** | Resource histogram and resource usage views |
| Level resources | **Resource > Level All** (options in **Leveling Options**) | **Tools > Level Resources** | Limited or no automatic leveling in the free edition; resolve over-allocations by adjusting assignments or logic |
| Record basis of estimate | Task **Notes** or a custom text field | Activity **Notebook** topics | Task **Notes** |

## Validation and Troubleshooting

- **Adding a resource shortened the task.** The task is effort-driven, or its
  type is fixed work. Change the task type to fixed duration if the duration is
  what you planned.
- **Work is far higher than expected.** Units are probably entered as a count of
  people at 100 percent each when the people only spend part of their time on the
  task. Check the units.
- **Leveling pushed the finish much later.** Leveling resolved a real conflict
  that the plan ignored. Decide whether to add people, change logic, or accept the
  later date, and record the decision.
- **A resource looks over-allocated on non-working days.** Its resource calendar
  differs from the project calendar. Check the resource's calendar.

## Security and Best Practices

- Restrict access to labor rates. They are commercially sensitive.
- Record a basis of estimate for every significant duration, and revisit it when
  actuals come in.
- Review leveling results with the people involved before saving them.
- Keep resource names consistent with the cost system so hours reconcile.

## References and Knowledge Checks

**References:**

- U.S. GAO, *Schedule Assessment Guide* (GAO-16-89G), best practices on assigning
  resources and establishing durations.
- NDIA, *Planning and Scheduling Excellence Guide (PASEG)*, sections on durations,
  calendars, and resource loading.
- Microsoft Project, Primavera P6, and ProjectLibre help on task types,
  resources, and leveling.

**Knowledge checks:**

1. Calculate the PERT estimate for O = 5, M = 8, P = 17 days.
2. Write the relationship between work, duration, and units.
3. What is the difference between a task calendar and a resource calendar?
4. Why should LOE tasks not drive discrete work?
5. What can resource leveling do to the finish date, and why must you review it?

## Hands-On Lab

**Objective:** Load resources onto the sample program, create an
over-allocation, and resolve it.

**Shared prerequisites** — the sample network from Chapter 03. **Cost:** none.

### Lab 4.1 — Define and assign resources

**Objective:** Resource-load the schedule.

1. Create the four resources from the Implementation section.
2. Assign Network Engineer to tasks 3 to 6 and 12 to 14, Deployment Team to
   tasks 16 to 19, and Project Manager to task 2 and to a new LOE task
   `Manage program` that spans tasks 2 to 24 (link it from task 1 and to task 25,
   and leave it out of all other logic).
3. Add the hardware cost to task 10.

**Expected result:** every discrete task with work has a resource, and the
project shows a total labor cost and the hardware cost.

In Primavera P6, set the activity type of `Manage program` to **Level of
Effort**; P6 then stretches it automatically to span the activities it is linked
to. In Microsoft Project and ProjectLibre, give it a duration that matches the
span of tasks 2 to 24.

**Negative test:** in Microsoft Project or ProjectLibre, extend `Manage program`
by 20 days. Because it is linked to task 25, the finish moves: LOE is now driving
the end date, which it must never do. Shorten it back so it ends with the work it
supports. (In Primavera P6 the Level of Effort type prevents this.)

**Rollback:** keep the resources; later labs use them.

### Lab 4.2 — Create and see an over-allocation

**Objective:** Show what happens when one team is planned in two places at
once.

1. Change the logic so tasks 17, 18, and 19 each depend only on task 15 (the
   sites run in parallel), and link each of them to task 20.
2. Open the resource usage view for Deployment Team.

**Expected result:** the finish date moves about 15 days earlier, and Deployment
Team shows 400 percent allocation during the cutover weeks: one team planned on
four sites at once.

**Negative test:** check the finish date and conclude the plan is now faster. It
is not achievable, because the team cannot be in four places. The over-allocation
is the warning.

**Rollback:** continue to Lab 4.3.

### Lab 4.3 — Resolve the over-allocation

**Objective:** Resolve it by leveling or by plan changes.

1. In Microsoft Project or Primavera P6, level the Deployment Team resource. In
   ProjectLibre, resolve it by hand: restore the sequential logic from Chapter 03
   (16 → 17 → 18 → 19).
2. Compare the finish date with the original 99-day plan.

**Expected result:** the sites are again done one after another and the finish
returns to about the original date. Whether the order comes from leveling or from
logic, it reflects the single team.

**Negative test:** add a second Deployment Team resource with max units 2 and
level again. The sites now run two at a time and the finish moves earlier, which
shows the trade between staffing and schedule.

**Rollback:** restore the Chapter 03 logic and one Deployment Team, so later labs
start from the 99-day plan.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Durations come from analogous, parametric, bottom-up, or three-point estimates,
each with a recorded basis. Work, duration, and units are linked, and each tool's
task or duration type decides which one stays fixed. Project, task, and resource
calendars control working time and should be few and clear. Resource loading
gives the IMS cost and staffing data; over-allocations are resolved by leveling
or by changing the plan, and the effect on the finish date must be reviewed.

- [ ] Can estimate durations with the four methods and record a basis.
- [ ] Can explain work, duration, units, and task types.
- [ ] Can use project, task, and resource calendars correctly.
- [ ] Can load resources and resolve over-allocations.
- [ ] Completed Labs 4.1–4.3 including each negative test.
