# Chapter 04: App Builder — Declarative Automation

## Learning Objectives

- Automate processes with Flow.
- Enforce data quality with validation rules.
- Build apps declaratively (Platform App Builder).
- Choose the right automation tool.
- Complete a walkthrough for each automation topic.

## Theory and Architecture

Salesforce's power is **low-code automation** — building business logic with clicks, validated by the
**Platform App Builder** certification. The primary tool is **Flow** (Flow Builder): a visual
automation engine with **triggers** (record-triggered before/after save, scheduled, screen flows for
UI) that run **elements** — create/update/delete records, decisions, loops, calls to Apex — replacing
the older Workflow Rules and Process Builder (now retired). **Validation rules** enforce **data
quality** at save time (block a record if a condition is violated, e.g., close date must be in the
future), returning an error to the user. Declarative app building also includes **custom apps**
(bundles of objects, tabs, and Lightning pages), **Lightning App Builder** (drag-and-drop record and
home pages), and **formula fields**. The guiding principle is **declarative before code** — use Flow
and configuration for most logic, dropping to Apex only when necessary. Choosing the right automation
tool and building maintainable, low-code solutions is the heart of the App Builder credential. This
chapter teaches each with a hands-on walkthrough (Flow logic, validation rules, and tool selection).

## Design Considerations

Automate with **Flow** (record-triggered for data logic, screen flows for guided UI). Enforce quality
with **validation rules**. Use **formula fields** for calculated values. Prefer **declarative** over
Apex. Keep flows **maintainable** (one per object where possible, well-documented). Bulkify logic
(flows handle multiple records).

## Implementation and Automation

The labs design a Flow, write a validation rule, and choose the automation tool.

## Validation and Troubleshooting

Confirm the automation model:

```text
Flow (Flow Builder): visual automation — triggers (record-triggered before/after, scheduled, screen) + elements (CRUD/decision/loop/Apex). Replaces retired Workflow Rules + Process Builder.
Validation rules: enforce data quality at save (block + error message). Also: custom apps, Lightning App Builder, formula fields. Principle: declarative before code.
```

Common pitfalls: reaching for **Apex** where **Flow** suffices; and multiple overlapping flows/triggers
on one object (hard to maintain).

## Security and Best Practices

Automate declaratively with **Flow**, enforce quality with **validation rules**, use **formula fields**,
and keep automation **maintainable and bulk-safe**. Declarative before code. All work is authorized
administration.

## Hands-On Lab

Automation walkthroughs. **Shared prerequisites** — `python3`, a free Dev org (Flow Builder). **Cost:**
none.

### Lab 4.1 — Design a record-triggered Flow

**Objective:** Automate on save.

```python
python3 - <<'PY'
flow={"trigger":"Opportunity updated, Stage = 'Closed Won'",
      "elements":["create a follow-up Task for the owner","update Account.Status__c = 'Customer'","send email alert"]}
print("trigger:",flow["trigger"])
for i,e in enumerate(flow["elements"],1): print(f"  {i}. {e}")
print("Flow: record-triggered automation runs elements when the criteria are met (no code)")
PY
```

**Expected result:** a **record-triggered Flow** (trigger → elements) — low-code automation.

**Negative test:** write an Apex trigger for this simple automation; **Flow** handles it declaratively —
use Flow.

**Cleanup:** none.

### Lab 4.2 — Write a validation rule

**Objective:** Enforce data quality.

```python
python3 - <<'PY'
def validate(close_date_in_past, amount):
    errors=[]
    if close_date_in_past: errors.append("Close Date cannot be in the past")
    if amount is not None and amount<=0: errors.append("Amount must be positive")
    return errors or ["OK — save allowed"]
print(validate(True, 100))
print(validate(False, 5000))
print("Validation rule: block the save + show an error when the condition is violated")
PY
```

**Expected result:** the save **blocked** with an error for a past close date — validation-rule data
quality.

**Negative test:** rely on users to enter valid data with no **validation rule**; bad data creeps in —
enforce at save.

**Cleanup:** none.

### Lab 4.3 — Choose the right automation tool

**Objective:** Match tool to task.

```python
python3 - <<'PY'
tasks={"complex record logic on save":"Flow (record-triggered)","guided multi-step user input":"Screen Flow",
       "block invalid data at save":"Validation rule","calculated read-only value":"Formula field",
       "logic beyond Flow's limits / callouts / complex bulk":"Apex (code)"}
for task,tool in tasks.items(): print(f"- {task}\n    -> {tool}")
PY
```

**Expected result:** each task matched to **Flow/validation/formula/Apex** — correct tool selection.

**Negative test:** use a **formula field** to modify other records; formulas are read-only — use a
**Flow**.

**Cleanup:** none.

### Lab 4.4 — Build a declarative app

**Objective:** Assemble a low-code app.

```python
python3 - <<'PY'
app={"name":"Project Tracker","objects":["Project__c","Milestone__c"],"tabs":["Projects","Milestones"],
     "lightning_page":"Project record page (drag-drop components)","automation":"Flow + validation rules"}
for k,v in app.items(): print(f"{k:14}: {v}")
print("App Builder: assemble objects + tabs + Lightning pages + automation with clicks")
PY
```

**Expected result:** a **declarative app** (objects, tabs, pages, automation) — Platform App Builder.

**Negative test:** hand-code the UI in Apex/LWC for a simple CRUD app; **App Builder** assembles it
declaratively — use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Platform App Builder automates with Flow (record-triggered and screen flows), enforces data quality
with validation rules, and assembles low-code apps with objects, tabs, and Lightning pages —
declarative before code.

- [ ] I can design a record-triggered Flow.
- [ ] I can write a validation rule.
- [ ] I can choose the right automation tool.
- [ ] I can build a declarative app.
- [ ] I completed Labs 4.1–4.4 including each negative test.
