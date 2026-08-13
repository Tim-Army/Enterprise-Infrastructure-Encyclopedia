# Chapter 04: Building Automations — Studio and Workflows

## Learning Objectives

- Explain the workflow-and-activity model of building automations.
- Understand selectors — how a robot finds UI elements reliably.
- Apply exception handling and the design practices that make automations robust.
- Recognize why robust design separates a demo from a production automation.

*Cert relevance: building automations well is the core of the **Automation Developer Associate and Professional** certifications.*

## Workflows and activities

An automation in Studio is a **workflow** — a sequence (or flowchart) of **activities**, each a single action: *Click* a button, *Type Into* a field, *Read Range* from a spreadsheet, *If* a condition, *For Each* over a list. You assemble activities visually into the logic of the process, passing data between them via **variables** (local) and **arguments** (passed in/out of a workflow). A well-built automation reads like the process it automates: open the app, log in, for each invoice, read it, enter it, save.

The **Developer Associate** skills are exactly this: modeling a process as a clean workflow, using variables and arguments correctly, and reusing sub-workflows so logic is not copy-pasted. The **Professional** level adds scale and best practices — the difference between an automation that works on your machine and one that runs unattended a thousand times a night.

## Selectors: finding the UI

The trickiest part of UI automation is **finding the right element**. When a robot clicks a button, it must locate that button in the application's UI — and UIs change, shift, and re-render. UiPath uses **selectors** — structured descriptions of a UI element (its type, name, attributes, position in the element tree). A **brittle selector** that depends on an element's exact screen position breaks the moment the window moves; a **robust selector** that keys on stable attributes (an element's automation ID or name) survives layout changes.

Writing robust selectors is a signature developer skill: prefer stable attributes, use wildcards for the parts that legitimately vary (a dynamic record ID), and avoid depending on anything cosmetic. The lab models selector robustness.

## Exception handling

A demo automation assumes everything goes right; a **production** automation assumes things go wrong. Applications hang, elements do not appear, data is malformed, the network blips. Robust automations wrap risky steps in **Try/Catch**, **retry** transient failures (the app was slow, try again), distinguish **business exceptions** (this invoice is genuinely invalid — route to a human) from **application exceptions** (the app crashed — retry or alert), and always **clean up** (close the app, log out) even on failure.

This is the single biggest gap between amateur and professional automation, and the certifications weight it heavily: an unattended robot running at 2 a.m. with no human watching *must* handle its own failures gracefully, or one bad record halts the whole batch. The lab models retry-versus-route.

## Hands-On Lab

Python models robust automation design. **Cost:** none.

### Lab 4.1 — Robust versus brittle selectors

**Objective:** See why keying on stable attributes survives UI change.

```bash
python3 - <<'EOF'
# a UI element described two ways; then the UI changes slightly
ELEMENT_BEFORE = {"type": "button", "name": "Submit", "auto_id": "btnSubmit",
                  "x": 450, "y": 600, "window_title": "Invoice Entry - Record 1187"}
ELEMENT_AFTER  = {"type": "button", "name": "Submit", "auto_id": "btnSubmit",
                  "x": 520, "y": 640, "window_title": "Invoice Entry - Record 2043"}  # moved + new record

SELECTORS = {
  "BRITTLE (position + exact title)": lambda e: e["x"]==450 and e["y"]==600 and e["window_title"]=="Invoice Entry - Record 1187",
  "ROBUST (stable auto_id + wildcard)": lambda e: e["auto_id"]=="btnSubmit" and e["type"]=="button",
}
print("The UI changed: the window moved (x,y) and the record number in the title changed.\n")
print(f"   {'selector':38}{'matches BEFORE':>16}{'matches AFTER':>16}")
for name, sel in SELECTORS.items():
    b = sel(ELEMENT_BEFORE); a = sel(ELEMENT_AFTER)
    print(f"   {name:38}{str(b):>16}{str(a):>16}")
print("\nThe BRITTLE selector keyed on x/y position and the EXACT window title")
print("('...Record 1187'). It matched before — and BROKE the moment the window moved")
print("and the record number changed. Every run with a new record fails.")
print("\nThe ROBUST selector keys on the stable auto_id ('btnSubmit') and element type,")
print("ignoring position and the varying record number. It matches BOTH — it survives")
print("the UI change.")
print("\nThe developer skill: key selectors on STABLE attributes (automation IDs,")
print("names), WILDCARD the parts that legitimately vary (the record number), and")
print("NEVER depend on cosmetic things (screen position, exact dynamic titles). A")
print("brittle selector is why 'it worked yesterday' — robust selectors are why an")
print("automation survives in production.")
EOF
```

**Expected result:** A brittle selector keyed on screen position and an exact dynamic title breaking when the UI shifts, while a robust selector on stable attributes with a wildcard survives. The selector lesson is to key on stable attributes and wildcard the legitimately-varying parts — brittle position-based selectors are the classic cause of automations that break on the next run.

**Negative test:** Building selectors that depend on screen coordinates or an exact dynamic window title. They match in the demo and break the moment the window moves or the record changes — robust selectors key on stable identifiers.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Retry transient, route business exceptions

**Objective:** Handle failures the way an unattended robot must.

```bash
python3 - <<'EOF'
import random
random.seed(12)
# process a batch of items; classify failures and handle each correctly
ITEMS = [
  ("item-1", "ok"),
  ("item-2", "app_timeout"),     # transient -> RETRY
  ("item-3", "invalid_data"),    # business exception -> ROUTE to human, continue
  ("item-4", "ok"),
  ("item-5", "app_timeout"),     # transient -> RETRY (succeeds on retry)
  ("item-6", "ok"),
]
MAX_RETRIES = 3
processed, routed, failed = [], [], []
for iid, outcome in ITEMS:
    if outcome == "ok":
        processed.append(iid)
    elif outcome == "app_timeout":
        # retry transient failures; assume it succeeds within retries
        for attempt in range(1, MAX_RETRIES+1):
            if attempt >= 2:   # succeeds on 2nd try
                processed.append(iid)
                print(f"   {iid}: app timeout -> RETRY (succeeded on attempt {attempt})")
                break
    elif outcome == "invalid_data":
        routed.append(iid)
        print(f"   {iid}: invalid data -> BUSINESS exception -> route to human, CONTINUE batch")
print(f"\nprocessed: {processed}")
print(f"routed to human (business exceptions): {routed}")
print(f"\nThe key distinction an unattended robot MUST make:")
print("  APPLICATION exception (app timeout, element missing, crash) -> TRANSIENT.")
print("     RETRY it (the app was just slow). Most succeed on the 2nd try.")
print("  BUSINESS exception (invalid data, failed validation) -> the ITEM is bad, not")
print("     the system. Don't retry (it'll fail again) — ROUTE it to a human and")
print("     CONTINUE the batch. One bad invoice must not halt the other 999.")
print("\nWithout this, a single malformed record either (a) crashes the whole 2am batch,")
print("or (b) gets retried forever. Distinguishing transient-retry from business-route,")
print("and always continuing the batch, is what makes unattended automation reliable —")
print("and it's the #1 thing separating a demo from a production automation.")
EOF
```

**Expected result:** Transient application timeouts retried until they succeed, a business exception (invalid data) routed to a human without halting the batch, and the batch continuing throughout. The exception-handling lesson is that an unattended robot must distinguish transient application failures (retry) from business exceptions (route and continue) so one bad record never stops the batch — the biggest gap between a demo and production.

**Negative test:** Treating every failure the same — retrying a genuinely invalid record forever, or crashing the whole batch on one bad item. Unattended reliability requires classifying failures and always continuing the batch past a routed business exception.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The workflow-and-activity model understood, with variables and arguments passing data.
- [ ] Selectors understood — keying on stable attributes and wildcarding variable parts for robustness.
- [ ] Exception handling understood — retry transient application failures, route business exceptions, always continue and clean up.
- [ ] Robust design recognized as the gap between a demo and a production, unattended automation.
