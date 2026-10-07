# Chapter 10: Reporting and Contract Deliverables

## Learning Objectives

- Describe the schedule content of the IPMDAR and how an IMS is delivered on a
  DoD contract.
- Write a schedule narrative that explains the critical path, changes, variances,
  margin, and risk.
- Choose the right visuals for each audience: summary Gantt charts, milestone
  charts, critical path views, and trend charts.
- Exchange schedules between Microsoft Project, Primavera P6, and ProjectLibre,
  and know what is lost in conversion.
- Assemble a monthly IMS reporting package.

## Theory and Architecture

An IMS earns its keep when it informs decisions. Reporting turns the statused
schedule into answers for program managers, executives, and customers, and on
government contracts the IMS itself is a formal deliverable with defined
content.

### The IMS as a contract deliverable

On DoD contracts that require earned value management, schedule and cost data
are typically delivered under the **Integrated Program Management Data and
Analysis Report (IPMDAR)**, data item DI-MGMT-81861 (current revision). The
contract's Contract Data Requirements List (CDRL) entry tailors what is required
and how often. The IPMDAR's schedule-related content includes:

| Component | Content |
| --- | --- |
| **Native schedule file** | The IMS in the contractor's scheduling tool format (for example `.mpp` or a Primavera P6 export) |
| **Schedule Performance Dataset (SPD)** | Structured schedule data (tasks, relationships, baselines, and status) in the format defined by DoD's IPMDAR file format specifications |
| **Contract Performance Dataset (CPD)** | The time-phased cost and earned value data that the IMS supports |
| **Performance Narrative Report** | Analysis and explanation of variances, the critical path, and corrective actions |

Deliveries usually go to a DoD repository specified in the contract. Check the
current IPMDAR implementation guide and file format specifications for the exact
requirements, because they are revised over time.

Commercial customers rarely require this formality, but the same parts (a native
file, structured data, and a narrative) make a sound reporting package for any
program.

### The schedule narrative

A good narrative answers, in order:

1. **Where is the finish forecast, and how did it move this period?** State the
   forecast against the baseline and the previous cycle.
2. **What is the critical path, and what changed on it?** Name the driving chain
   and any new near-critical paths.
3. **Which variances exceed thresholds, and why?** Explain cause, impact, and
   corrective action for each.
4. **How much margin has been consumed?** Report margin remaining and what used
   it.
5. **What do the health metrics and risk analysis say?** Summarize DCMA metrics,
   BEI, CPLI, and the latest SRA confidence.
6. **What decisions are needed?** Be explicit about what you need from
   management or the customer.

### Visuals for each audience

| Audience | Best visuals |
| --- | --- |
| **Executives and customers** | Milestone chart of IMP events (baseline vs. forecast); finish-date trend over time; SRA confidence |
| **Program manager** | Summary Gantt chart by WBS; critical and near-critical path view; margin burn-down |
| **CAMs and leads** | Detailed Gantt charts filtered to their control accounts; upcoming tasks for the next period |
| **Schedulers and analysts** | DCMA metric trends; BEI and CPLI trends; logic and float reports |

A **finish-date trend** (the forecast finish plotted for each status cycle) shows
whether a program is stable or steadily slipping, which a single snapshot
cannot. A steady slip of a week every month is the classic sign of an optimistic
schedule.

### Exchanging schedules between tools

| Format | Read and written by | Notes |
| --- | --- | --- |
| **`.mpp`** | Microsoft Project; read by many tools | Proprietary; version-specific |
| **Microsoft Project XML (MSPDI)** | Microsoft Project, ProjectLibre, Primavera P6 (import and export) | The most portable exchange format among the three tools |
| **`.xer`** | Primavera P6 | P6's native exchange format; widely read by analysis tools |
| **P6 XML** | Primavera P6 | Oracle's XML format for P6 data |
| **`.pod`** | ProjectLibre | ProjectLibre's native format |

Conversion between tools is never perfect. Calendars, constraints, custom fields
and codes, resource details, and baselines are the usual casualties. After any
conversion, check the finish date, the critical path, and a sample of task dates
and baselines against the source.

## Design Considerations

- **Report from the statused, health-checked file only.** Never produce reports
  from a working copy that has not been through the full status cycle.
- **Keep the narrative factual and specific.** "Hardware delivery slipped 5 days
  because the supplier's factory closed for a holiday; the finish moved 5 days;
  we have asked the supplier to expedite" is useful. "Some slippage occurred" is
  not.
- **Match the delivery format to the CDRL.** The contract governs format,
  frequency, and content. Do not assume last contract's requirements apply.
- **Use the same views every month.** Consistent visuals let readers spot change
  quickly.
- **Mark data correctly.** Apply the distribution statements, controlled
  unclassified information (CUI) markings, or proprietary notices the contract
  requires to every report and file.

## Implementation and Automation

| Action | Microsoft Project | Primavera P6 | ProjectLibre |
| --- | --- | --- | --- |
| Built-in reports | **Report** tab (dashboards, **In Progress > Critical Tasks**, **Late Tasks**, milestone reports) | **Tools > Reports** and print layouts | Print and print preview of views |
| Milestone view | Filter **Milestones**, or **Timeline** view | Filter activities by type **Milestone**, saved as a layout | Filter milestones in the Gantt view |
| Copy a chart into a document | **Task > Copy > Copy Picture**, or export the timeline | **File > Print Preview**, then print or save to PDF | Print to PDF |
| Export for exchange | **File > Save As > XML Format (*.xml)** | **File > Export**: XER, P6 XML, or Microsoft Project XML | **File > Save As**: Microsoft Project XML |
| Save the delivered native file | **File > Save As**, named with the data date | **File > Export** to XER for the delivered copy | **File > Save As** `.pod` and XML |

For the finish-date trend, record the forecast finish of the finish milestone
from each archived cycle copy (Chapter 08) in a spreadsheet, one row per cycle,
and chart it. Add the baseline finish as a flat reference line.

## Validation and Troubleshooting

- **Report dates do not match the delivered file.** The report was produced from
  a different copy. Generate reports from the same archived file you deliver.
- **The customer cannot open the native file.** Confirm the tool and version they
  use, and supply an exchange format (Microsoft Project XML or XER) alongside the
  native file if the CDRL allows.
- **A converted schedule shows a different finish date.** Calendars or
  constraints changed in conversion. Compare calendars first, then constraints,
  then individual task dates along the critical path.
- **Narrative and metrics disagree.** The narrative was written before the final
  status. Write the narrative last, from the final metrics.

## Security and Best Practices

- Deliver only through the channels the contract specifies, and never email
  controlled schedule data outside them.
- Keep a record of each delivery: file name, data date, recipient, and date
  delivered.
- Apply required markings to every file and page, including exports and
  screenshots.
- Review reports for sensitive details (such as supplier names or capability
  dates) before sharing beyond the program.

## References and Knowledge Checks

**References:**

- DI-MGMT-81861, *Integrated Program Management Data and Analysis Report
  (IPMDAR)*, with the DoD IPMDAR implementation guide and file format
  specifications.
- U.S. DoD, *Integrated Master Plan and Integrated Master Schedule Preparation
  and Use Guide*.
- U.S. GAO, *Schedule Assessment Guide* (GAO-16-89G).
- Microsoft Project, Primavera P6, and ProjectLibre documentation on reporting
  and import and export.

**Knowledge checks:**

1. Name the IPMDAR components that relate to the schedule.
2. List the six questions a schedule narrative should answer.
3. Why is a finish-date trend more informative than a single snapshot?
4. Which exchange format works across all three tools in this volume?
5. What should you check after converting a schedule between tools?

## Hands-On Lab

**Objective:** Assemble a monthly reporting package for the sample program and
test schedule exchange between tools.

**Shared prerequisites** — the statused sample program from Chapter 08, the SRA
results from Chapter 09, and a spreadsheet tool. **Cost:** none.

### Lab 10.1 — Build the reporting views

**Objective:** Produce the views for each audience.

1. Create a milestone view showing IMP events A to D with baseline and forecast
   dates.
2. Create a critical path view (critical tasks only, with total float).
3. Export both to PDF or copy them into a document.

**Expected result:** two clear views that match the statused file, ready to drop
into a report.

**Negative test:** produce the milestone view from the copy saved *before* the
Chapter 08 status cycle. Its forecast dates differ from the statused file, which
is why reports must come from the delivered, statused copy.

**Rollback:** none.

### Lab 10.2 — Write the narrative and trend

**Objective:** Write a one-page schedule narrative with a finish-date trend.

1. In a spreadsheet, record the forecast finish from each saved cycle copy (the
   baseline, the Chapter 07 status, and the Chapter 08 status) and chart it.
2. Write a narrative answering the six questions in the Theory and Architecture
   section, using the critical path, variances, DCMA results from Chapter 06, and
   SRA results from Chapter 09.

**Expected result:** a one-page narrative and a trend chart that a program
manager could act on.

**Negative test:** write the narrative's first paragraph without numbers ("the
program is generally on track"). Compare it with a paragraph that states the
finish forecast, its movement, and the cause. Only the second supports a
decision. Rewrite with numbers.

**Rollback:** none.

### Lab 10.3 — Exchange the schedule between tools

**Objective:** Move the IMS through Microsoft Project XML and check what
survives.

1. Export the sample program as Microsoft Project XML from your tool.
2. Import the XML into a different tool (for example, from Microsoft Project or
   Primavera P6 into ProjectLibre, or from ProjectLibre into Microsoft Project).
3. Compare the finish date, the critical path, and the baseline dates of tasks
   10, 16, and 21.

**Expected result:** the finish date and critical path match. Note anything that
differs, such as calendars, custom fields (the IMP code), or baselines.

**Negative test:** check the IMP code field from Chapter 02 in the imported
schedule. Custom fields and activity codes often do not survive conversion, or
arrive under a different name, which is why traceability must be checked after
every exchange.

**Rollback:** delete the imported copy.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Reporting turns the statused IMS into decisions. On DoD contracts, the IPMDAR
requires the native schedule file, the Schedule Performance Dataset, and a
performance narrative, tailored by the CDRL. A good narrative states the finish
forecast and its movement, the critical path, variances, margin, health metrics,
risk, and the decisions needed, supported by visuals matched to each audience and
trend charts across cycles. Schedules move between tools most reliably through
Microsoft Project XML, and every conversion must be checked for lost calendars,
codes, and baselines.

- [ ] Can describe the IPMDAR schedule components.
- [ ] Can write a schedule narrative that answers the six questions.
- [ ] Can choose visuals for each audience and build a finish-date trend.
- [ ] Can exchange schedules between tools and check the result.
- [ ] Completed Labs 10.1–10.3 including each negative test.
