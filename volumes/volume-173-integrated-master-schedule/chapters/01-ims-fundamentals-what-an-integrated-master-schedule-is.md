# Chapter 01: IMS Fundamentals — What an Integrated Master Schedule Is

## Learning Objectives

- Define an integrated master schedule (IMS) and explain what "integrated"
  means in practice.
- Describe how the IMS relates to the integrated master plan (IMP), the work
  breakdown structure (WBS), and earned value management (EVM).
- Identify the guidance that governs an IMS on U.S. government programs.
- Compare Microsoft Project, Primavera P6, and ProjectLibre as IMS tools.
- Set up a project file with the correct start date and calendar in all three
  tools.

## Theory and Architecture

An **integrated master schedule (IMS)** is a single, networked schedule of all
the work needed to deliver a program. It contains every discrete task, from
contract award to final delivery, linked by logic so that a change anywhere
ripples correctly through the rest. Programs use it to answer three questions
every week: *When will we finish? What drives that date? What happens if
something slips?*

"Integrated" is the important word. An IMS integrates in three directions:

| Direction | What it means |
| --- | --- |
| **Across the work** | One schedule covers all of the program's work, including subcontractor and government tasks, rather than separate schedules per team |
| **Vertically** | Detailed tasks roll up to summary tasks, WBS elements, and the events in the IMP, so a detailed slip shows up at the program level |
| **With cost** | The same tasks carry the budget used for earned value management, so schedule progress and cost performance are measured against the same plan |

### The IMS among its companions

```text
Integrated Master Plan (IMP)      WHAT must be accomplished, and how completion
  events → accomplishments          is judged (event-based, no dates)
          → criteria
                │  traceability
                ▼
Integrated Master Schedule (IMS)  WHEN and in what ORDER the work happens
  tasks, logic, durations,          (time-based, networked)
  resources, baseline
                │  same work packages
                ▼
Earned Value Management (EVM)     HOW MUCH it costs and whether progress
  budgets, earned value,            matches the plan
  performance indices
                ▲
Work Breakdown Structure (WBS)    The product-oriented hierarchy that organizes
                                  all three
```

- The **IMP** is event-based. It lists the program's major events (such as a
  design review), the accomplishments that must be complete for each event, and
  the criteria that prove each accomplishment. It has no dates. Chapter 02
  covers it.
- The **WBS** breaks the product and work into a hierarchy. IMS tasks are
  organized by WBS element, and so are budgets. Chapter 02 covers it too.
- **EVM** measures cost and schedule performance against a baseline. The IMS
  provides the time-phased plan EVM depends on. Chapter 07 covers the link.

### The building blocks of a schedule

| Element | Definition |
| --- | --- |
| **Task (activity)** | A unit of work with a duration, a start, and a finish |
| **Milestone** | A zero-duration point marking an event, such as a review or a delivery |
| **Summary task** | A grouping of tasks, usually by WBS element; it has no logic or work of its own |
| **Relationship (dependency)** | A logic link between two tasks, such as "B cannot start until A finishes" |
| **Duration** | How many working periods a task takes |
| **Calendar** | Which days and hours are working time |
| **Resource** | The labor, material, or equipment assigned to a task |
| **Baseline** | A frozen copy of the approved plan, used to measure progress |
| **Data date (status date)** | The date as of which progress is recorded |
| **Total float** | How long a task can slip without delaying the project finish |
| **Critical path** | The longest chain of dependent tasks, which sets the earliest finish date |

### Governing guidance

On U.S. Department of Defense (DoD) and many federal programs, the IMS is a
contract deliverable with defined expectations:

| Source | What it covers |
| --- | --- |
| **DoD Integrated Master Plan and Integrated Master Schedule Preparation and Use Guide** | How to prepare an IMP and IMS and keep them traceable |
| **Integrated Program Management Data and Analysis Report (IPMDAR)**, DI-MGMT-81861 (current revision) | The data item that requires delivery of the native IMS file and schedule performance data (Chapter 10) |
| **EIA-748**, Earned Value Management Systems | The industry standard for EVM systems, including scheduling guidelines |
| **GAO Schedule Assessment Guide** (GAO-16-89G) | The Government Accountability Office's ten best practices for reliable schedules |
| **DCMA 14-Point Schedule Assessment** | Defense Contract Management Agency metrics for schedule health (Chapter 06) |
| **NDIA Planning and Scheduling Excellence Guide (PASEG)** | Industry guidance on practical scheduling techniques |
| **MIL-STD-881** (current revision) | Standard WBS structures for defense materiel (Chapter 02) |

Commercial programs are not bound by these documents, but they are the most
complete public guidance on building a schedule that holds up under scrutiny.

### The three tools in this volume

| | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Publisher | Microsoft | Oracle | Open source (ProjectLibre project) |
| Typical use | Most DoD contractor IMS files; general project scheduling | Very large, multi-project programs; construction and defense | Learning, small programs, budget-constrained teams |
| Cost | Commercial license | Commercial license | Free |
| Native file | `.mpp` | Database; exports `.xer` and `.xml` | `.pod`; reads and writes Microsoft Project XML |
| Data model | One file per project | Enterprise database with projects, WBS, and activities | One file per project, Microsoft Project-like |
| Terms | Task, slack | Activity, float | Task, slack |

Every lab in this volume gives steps for all three. Microsoft Project and
ProjectLibre share a similar model and vocabulary; Primavera P6 differs most,
because it stores projects in an enterprise database and calls tasks
*activities* and slack *float*.

## Design Considerations

- **One schedule, not many.** Resist separate schedules for engineering,
  procurement, and test. If teams need their own views, give them filtered views
  of the one IMS.
- **Decide the level of detail up front.** Detail should be fine enough to
  manage and status (tasks typically no longer than about two months) but not so
  fine that the schedule cannot be maintained. Rolling wave planning (Chapter 08)
  adds detail as work approaches.
- **Pick the tool your customer can read.** If the contract requires delivery of
  the native file, use a tool the customer can open. Many DoD customers expect
  Microsoft Project files; some expect Primavera P6 exports.
- **Agree calendars and units early.** Working days, holidays, and whether
  durations are in days or hours affect every number in the schedule. Changing
  them later distorts history.
- **Plan for traceability from day one.** Coding every task to its WBS element
  and IMP criterion (Chapter 02) is easy at the start and very hard to retrofit.

## Implementation and Automation

Every IMS starts with three settings: the project start date, the project
calendar, and the scheduling defaults. The table shows where each lives in the
three tools.

| Setting | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Create the project | **File > New > Blank Project** | **Enterprise > Projects**, then **Add** | **File > New**; the new project dialog asks for a name and start date |
| Project start date | **Project > Project Information > Start date** | Project's **Dates** tab: **Planned Start** | Set in the new project dialog, or in **Project Information** |
| Working time and holidays | **Project > Change Working Time** | **Enterprise > Calendars** (global, resource, or project calendars) | **Tools > Change Working Calendar** (the menu location varies by version) |
| Default task type and units | **File > Options > Schedule** | **User Preferences** and **Admin Preferences** | **Tools > Options** (or the equivalent preferences dialog) |

Keep the scheduling mode automatic. Microsoft Project allows *manually
scheduled* tasks, which ignore logic. An IMS must use **automatically
scheduled** tasks so that dates come from the network, not from typing. In
Microsoft Project, set **New tasks: Auto Scheduled** on the status bar or in
**File > Options > Schedule**.

## Validation and Troubleshooting

- **Dates are not moving when logic changes.** In Microsoft Project, check for
  manually scheduled tasks (a pin icon in the Task Mode column). In Primavera P6,
  remember that nothing recalculates until you run **Schedule** (F9).
- **Durations look wrong by a factor of three.** The calendar or the hours per
  day setting is inconsistent. A one-day task on an 8-hour-day calendar shows as
  24 hours on a 24-hour calendar. Check the project calendar and the options.
- **ProjectLibre opens a Microsoft Project file with differences.** ProjectLibre
  reads and writes Microsoft Project XML well, but some features (certain custom
  fields, some views) do not carry across. Use XML rather than `.mpp` for
  exchange, and check key dates after import.
- **Primavera P6 shows no project.** Projects must be opened from the Projects
  window (**File > Open**). Check you have access to the right EPS node.

## Security and Best Practices

- Treat the IMS as controlled program data. It can reveal capability dates,
  supplier relationships, and staffing, and on defense programs it may carry
  distribution or export control markings.
- Keep the master file in a controlled location with version history. A single
  shared file that anyone can edit without trace is the most common way an IMS
  loses integrity.
- Restrict who can edit the baseline. Most schedulers need to update status, not
  rewrite the approved plan.
- Save a dated copy at each status cycle, so any past report can be reproduced.

## References and Knowledge Checks

**References:**

- U.S. DoD, *Integrated Master Plan and Integrated Master Schedule Preparation
  and Use Guide*.
- U.S. GAO, *Schedule Assessment Guide: Best Practices for Project Schedules*
  (GAO-16-89G).
- DI-MGMT-81861, *Integrated Program Management Data and Analysis Report
  (IPMDAR)*, and its implementation guide.
- EIA-748, *Earned Value Management Systems*.
- NDIA, *Planning and Scheduling Excellence Guide (PASEG)*.
- Microsoft Project, Oracle Primavera P6, and ProjectLibre documentation.

**Knowledge checks:**

1. What three kinds of integration make a schedule an *integrated* master
   schedule?
2. How does the IMP differ from the IMS?
3. What does the WBS provide to both the IMS and EVM?
4. Why must IMS tasks be automatically scheduled?
5. Name two differences between Primavera P6 and Microsoft Project.

## Hands-On Lab

**Objective:** Install a scheduling tool and create the project file for the
sample program used throughout this volume.

**The sample program.** Every lab builds the IMS for the same small program: a
**branch network modernization** that replaces firewalls and adds SD-WAN at four
branch offices. It is small enough to build by hand and realistic enough to show
every technique in the volume.

**Shared prerequisites** — at least one of Microsoft Project (desktop),
Primavera P6 Professional, or ProjectLibre (free download from the ProjectLibre
website; it requires a Java runtime on some platforms). The ProjectLibre steps
work for anyone without a commercial license. **Cost:** none with ProjectLibre;
license costs for the commercial tools.

### Lab 1.1 — Create the project

**Objective:** Create the sample program's project file with the right start
date.

1. Create a new project named `Branch Network Modernization`.
2. Set the project start date to the first Monday of next month.

| Step | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| New project | **File > New > Blank Project**, then save as `BNM-IMS.mpp` | **Enterprise > Projects > Add**; choose an EPS node; ID `BNM` | **File > New**; enter the name |
| Start date | **Project > Project Information** | **Dates** tab, **Planned Start** | In the new project dialog |

**Expected result:** an empty project whose start date is the date you chose.

**Negative test:** in Microsoft Project, add a task with the Task Mode set to
**Manually Scheduled** and give it a start date before the project start. It
accepts the date, which shows why manual mode must stay off in an IMS. Delete
the task and set new tasks to **Auto Scheduled**.

**Rollback:** delete the project file (or the project in Primavera P6).

### Lab 1.2 — Set the calendar

**Objective:** Define working time and holidays.

1. Use a five-day, eight-hour working week.
2. Add the public holidays that fall in the next twelve months as non-working
   days.

| Step | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Edit calendar | **Project > Change Working Time**; add each holiday under **Exceptions** | **Enterprise > Calendars**; create `BNM Standard`; mark holidays as non-work | Open the working calendar dialog; mark holidays as non-working |
| Assign to project | Project Information: **Calendar** | Project **Defaults** tab: default calendar | Project information: base calendar |

**Expected result:** the calendar shows holidays as non-working days.

**Negative test:** add a five-day task that spans a holiday. Its finish moves one
day later than a simple count of five weekdays, because the holiday is skipped.

**Rollback:** remove the test task.

### Lab 1.3 — Compare the tools' vocabulary

**Objective:** Map terms so the rest of the volume reads cleanly in any tool.

1. In your tool, find the column for total slack or total float and add it to
   the main table or Gantt view.
2. Find where you would set a task's predecessors.

**Expected result:** you can show total slack (Microsoft Project, ProjectLibre)
or total float (Primavera P6), and you know where predecessors are entered.

**Negative test:** in Primavera P6, change a duration and look at total float
before running **Schedule** (F9). It has not updated. Run the scheduler and it
does.

**Rollback:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

An IMS is a single networked schedule of all program work, integrated across
the work, vertically through the WBS and IMP, and with cost for EVM. It is built
from tasks, milestones, logic, durations, calendars, resources, and a baseline,
and it reveals the critical path and float. On DoD programs it is governed by
the IMP/IMS guide, the IPMDAR data item, EIA-748, and the GAO and DCMA
assessment criteria. Microsoft Project, Primavera P6, and ProjectLibre can all
produce an IMS; every lab in this volume covers all three.

- [ ] Can define an IMS and its three kinds of integration.
- [ ] Can explain the roles of the IMP, WBS, and EVM.
- [ ] Can name the main guidance documents for an IMS.
- [ ] Can set up a project with the right start date and calendar in a tool.
- [ ] Completed Labs 1.1–1.3 including each negative test.
