# Chapter 02: The Integrated Master Plan and the Work Breakdown Structure

## Learning Objectives

- Build a product-oriented work breakdown structure (WBS) and a WBS dictionary.
- Write an integrated master plan (IMP) as events, accomplishments, and
  criteria.
- Code every IMS task to its WBS element and IMP criterion, so the schedule is
  vertically traceable.
- Explain how control accounts and work packages connect the WBS to cost.
- Set up WBS and IMP coding in Microsoft Project, Primavera P6, and
  ProjectLibre.

## Theory and Architecture

The IMS is only as good as the structure under it. Two structures matter: the
**WBS**, which organizes *what* is being built and done, and the **IMP**, which
defines *how the program knows it is done*. Every IMS task should trace to one
WBS element and to the IMP criterion it helps satisfy.

### The work breakdown structure

A **WBS** is a hierarchical decomposition of the program's total scope. Good
WBSs are **product-oriented**: the upper levels name the things being delivered
(the network, the software, the training), not the departments doing the work.

| Rule | Why it matters |
| --- | --- |
| **100 percent rule** | Each level contains all the work of its parent, no more and no less. Work outside the WBS is out of scope |
| **Mutually exclusive elements** | No work appears in two elements, so it is never budgeted or scheduled twice |
| **Product orientation** | Elements describe deliverables, so the WBS survives reorganizations |
| **Appropriate depth** | Decompose until each lowest element can be estimated, scheduled, and assigned to one owner |

For defense materiel, **MIL-STD-881** defines standard upper-level WBS
structures for system types (aircraft, ships, information systems, and others),
so that programs report cost and schedule in comparable terms. Contracts often
require its structure at levels 1 to 3, with the contractor extending it below.

Each WBS element is described in a **WBS dictionary**: its scope, deliverables,
assumptions, and boundaries with neighboring elements. The dictionary resolves
the question "is this task in or out of this element?"

### Control accounts and work packages

Where the WBS meets the organization, a **control account** is established: one
WBS element managed by one **control account manager (CAM)** with a defined
budget and schedule. Inside each control account, work is planned as:

- **Work packages** — near-term work planned in detail as IMS tasks with
  budgets.
- **Planning packages** — far-term work held as larger blocks until it is
  planned in detail (rolling wave planning, Chapter 08).

Chapter 07 shows how this structure lets the IMS and earned value use the same
plan.

### The integrated master plan

The **IMP** is an event-based plan. It has no dates; it says what must be true
before the program can declare each major event complete.

```text
Event          A significant program point, usually a review or decision
  A  Design Complete
  │
  ├─ Accomplishment   A desired result needed for the event
  │   A01  Network design approved
  │   │
  │   ├─ Criterion    Objective evidence that the accomplishment is done
  │   │   A01a  Design document delivered
  │   │   A01b  Design review action items closed
  │   │
  │   A02  Equipment list finalized
  │       A02a  Bill of materials approved
```

Events are often lettered, accomplishments numbered within each event, and
criteria lettered within each accomplishment, as above. Use whatever convention
your contract or customer specifies.

### Vertical traceability

Coding ties the three structures together:

```text
IMP criterion  A01a  Design document delivered
     ▲
     │  coded on the task
IMS task       "Deliver network design document"   WBS 1.2.2   IMP A01a
     │
     ▼
WBS element    1.2.2  Network Design   (control account, budget)
```

With every task coded, you can filter the IMS to show all the work behind an IMP
event, or all the work in a control account, and the schedule's status for that
event or account comes straight from the tasks. The GAO calls this **vertical
traceability**, and it is one of its schedule best practices.

## Design Considerations

- **Build the WBS before the schedule.** Tasks without a WBS home are either out
  of scope or a sign the WBS is incomplete.
- **Keep the WBS product-oriented even when tempted otherwise.** An
  organizational WBS ("Engineering," "Purchasing") breaks traceability as soon as
  people move.
- **Write IMP criteria as objective evidence.** "Design reviewed" is weak; "Design
  review minutes signed and all action items closed" can be verified.
- **Size control accounts sensibly.** Too few, and problems hide inside large
  accounts. Too many, and the overhead of managing them swamps the work.
- **Use dedicated code fields.** Do not encode WBS or IMP values in task names.
  Use the tool's WBS field and a separate code field for the IMP, so they can be
  filtered, grouped, and checked.

## Implementation and Automation

### The sample program's structure

The branch network modernization uses this WBS:

```text
1      Branch Network Modernization
1.1    Program Management
1.2    Design
1.2.1    Requirements
1.2.2    Network Design
1.3    Procurement
1.4    Staging and Integration
1.5    Site Deployment
1.5.1    Site A
1.5.2    Site B
1.5.3    Site C
1.5.4    Site D
1.6    Test and Acceptance
1.7    Training and Documentation
```

And this IMP (abbreviated):

| Event | Accomplishments | Example criteria |
| --- | --- | --- |
| **A** Design Complete | A01 Network design approved; A02 Equipment list finalized | A01a Design document delivered; A02a Bill of materials approved |
| **B** Ready to Deploy | B01 Equipment received; B02 Configurations staged | B01a All hardware received and inventoried; B02a Configuration templates tested in the lab |
| **C** All Sites Cut Over | C01 Sites A and B cut over; C02 Sites C and D cut over | C01a Site A cutover report signed |
| **D** Final Acceptance | D01 Acceptance testing passed; D02 Training delivered | D01a Acceptance test report approved |

### Setting up the codes

| Task | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Build the WBS hierarchy | Enter summary tasks and indent the tasks below them (**Task > Indent**); define the code format with **Project > WBS > Define Code** | **Project > WBS**; add WBS elements in the WBS window; activities are then assigned to a WBS element | Enter summary tasks and indent; the WBS column follows the outline |
| IMP code field | Rename a custom text field (for example Text1) to `IMP Code` with **Project > Custom Fields** | Create an activity code `IMP` with **Enterprise > Activity Codes** (or a project code), with values A01a, A01b, and so on | Use a custom text field (Text1) as the IMP code |
| Filter by code | **View > Filter** or **Group By** on the IMP field | Group and sort, or filter, by the IMP activity code | Filter or sort on the custom field |

## Validation and Troubleshooting

- **A task does not fit any WBS element.** Either it is out of scope (raise it
  with the program manager) or the WBS is missing an element. Fix the WBS; do not
  park the task under "Miscellaneous."
- **WBS codes change when tasks are moved.** Microsoft Project and ProjectLibre
  derive WBS codes from the outline by default. Renumbering after moving tasks is
  expected; if codes must be stable, check the option that controls renumbering in
  the WBS code definition.
- **An IMP criterion has no tasks.** The IMS is missing work, or the criterion
  is not needed. Either add the tasks or remove the criterion with the customer.
- **A task carries several IMP codes.** A task should support one criterion.
  Split the task so each part traces to one criterion.

## Security and Best Practices

- Version-control the WBS dictionary and IMP alongside the IMS. A change to one
  should prompt a review of the others.
- Agree the WBS and IMP with the customer before baselining. Changing them after
  the baseline is a formal change (Chapter 08).
- Restrict edits to code fields to the scheduler or planning lead, so coding
  stays consistent.
- Check coding every cycle with a filter for blank WBS or IMP values. Gaps creep
  in as tasks are added.

## References and Knowledge Checks

**References:**

- MIL-STD-881 (current revision), *Work Breakdown Structures for Defense Materiel
  Items*.
- U.S. DoD, *Integrated Master Plan and Integrated Master Schedule Preparation
  and Use Guide*.
- U.S. GAO, *Schedule Assessment Guide* (GAO-16-89G), best practice on vertical
  and horizontal traceability.
- PMI, *Practice Standard for Work Breakdown Structures*.

**Knowledge checks:**

1. State the 100 percent rule and explain why it matters.
2. What is the difference between a product-oriented and an organizational WBS?
3. Describe the event, accomplishment, and criterion levels of an IMP.
4. What is a control account, and who manages it?
5. Why should IMP codes live in a dedicated field rather than in task names?

## Hands-On Lab

**Objective:** Build the sample program's WBS and IMP coding in your tool.

**Shared prerequisites** — the project file from Chapter 01. **Cost:** none.

### Lab 2.1 — Build the WBS

**Objective:** Enter the WBS hierarchy.

1. Enter the WBS elements from the Implementation section as summary tasks (or,
   in Primavera P6, as WBS elements).
2. Indent each element under its parent.
3. Display the WBS column (or the WBS window in Primavera P6) and confirm the
   codes match.

**Expected result:** a hierarchy matching the WBS, with codes 1, 1.1, 1.2,
1.2.1, and so on.

**Negative test:** add a task called "Miscellaneous" at the top level. It breaks
the 100 percent rule's discipline, because it has no product meaning. Delete it.

**Rollback:** keep the WBS; later labs build on it.

### Lab 2.2 — Create the IMP code

**Objective:** Add an IMP code field with values for events A to D.

1. Create the IMP code field in your tool, as shown in the Implementation
   section.
2. Add the event milestones under the right WBS elements:
   - `A Design Complete` (1.2)
   - `B Ready to Deploy` (1.4)
   - `C All Sites Cut Over` (1.5)
   - `D Final Acceptance` (1.6)
3. Give each milestone a zero duration and its IMP event letter as the IMP code.

**Expected result:** four milestones, each coded to its event.

**Negative test:** give one milestone a duration of one day. The tool treats it
as a task, not a milestone (in Microsoft Project and ProjectLibre the Milestone
flag clears; in Primavera P6 the activity type is no longer a milestone). Set the
duration back to zero.

**Rollback:** none; later labs build on these milestones.

### Lab 2.3 — Code a few tasks and filter

**Objective:** Prove vertical traceability.

1. Under 1.2.2 Network Design, add three tasks: `Draft network design`, `Review
   network design`, and `Deliver network design document`.
2. Code them to IMP criteria A01a, A01b, and A01a.
3. Filter or group the schedule by IMP code and show only A01.

**Expected result:** the filtered view shows only the tasks behind accomplishment
A01, with their WBS codes.

**Negative test:** leave one task without an IMP code and apply a filter for a
blank IMP code. The task without a code appears, which is how you catch coding gaps.

**Rollback:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The WBS organizes the program's scope as a product-oriented hierarchy that
obeys the 100 percent rule, described in a WBS dictionary and divided into
control accounts with work and planning packages. The IMP defines events,
accomplishments, and objective criteria without dates. Coding every IMS task to
its WBS element and IMP criterion creates vertical traceability, so the schedule
can be viewed and statused by product, by control account, or by program event.

- [ ] Can build a product-oriented WBS that follows the 100 percent rule.
- [ ] Can write an IMP as events, accomplishments, and criteria.
- [ ] Can explain control accounts, work packages, and planning packages.
- [ ] Can set up WBS and IMP coding in a scheduling tool.
- [ ] Completed Labs 2.1–2.3 including each negative test.
