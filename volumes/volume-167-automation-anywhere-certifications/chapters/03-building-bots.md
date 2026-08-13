# Chapter 03: Building Bots

## Learning Objectives

- Build a Task Bot from actions and variables in the Bot Creator.
- Use recorders and pre-built action packages instead of low-level code.
- Apply control flow — loops, conditions, and error handling.
- Understand reuse — subtasks, packages, and modular bots.

*Cert relevance: bot building is the core of the Essentials and Advanced certifications.*

## The Task Bot

The **Task Bot** is the workhorse — the automation logic that performs a process end to end. You build it in the **Bot Creator** ([Ch 2](02-automation-success-platform.md)), a browser-based visual builder, by assembling **actions** in sequence. Each action is a step a human would take: *Open browser*, *Click*, *Type*, *Read cell from Excel*, *Run SQL*, *Send email*. Actions operate on **variables** — the data flowing through the bot (a customer name, an invoice total, a file path).

A bot is therefore a **structured program built visually**: actions in order, data in variables, decisions and loops controlling flow. The skill is decomposing a real process into the right sequence of actions and managing the data between them cleanly. This is exactly what the Essentials and Advanced certifications validate. The lab builds a Task Bot from actions and variables.

## Recorders and action packages

You rarely start from a blank canvas. Automation 360 gives you two accelerators:

- **Recorders** — capture your interactions with an application (clicks, typing) and turn them into actions automatically. The **Universal Recorder** works across web, desktop, and applications, identifying UI objects reliably so the recorded bot is resilient.
- **Action packages** — libraries of **pre-built actions** grouped by capability: Excel, PDF, Email, Database, String, REST/SOAP web services, and hundreds more. You **configure** an action (which file, which cell) rather than code the integration.

This is why RPA is faster than custom scripting: the connectors and UI interactions are pre-built, so you assemble and configure rather than write low-level code. Choosing the right package for each step — and the right recorder — is core building skill. The lab uses packaged actions.

## Control flow

Real processes are not straight lines; bots need **control flow**:

- **Loop** — repeat actions over a collection (each row of a spreadsheet, each file in a folder, each record from a query).
- **If / Else** — branch on a condition (if the amount exceeds a threshold, route for approval; else auto-process).
- **Try / Catch** — handle errors gracefully (if an app is slow or a value is missing, catch it, log it, and recover or route to an error queue) rather than crashing the whole run.
- **Wait / delays** — synchronize with applications that respond at their own pace.

Robust bots are defined by their **error handling and resilience**, not just the happy path — a production bot processing thousands of items must survive the occasional bad record. The lab adds a loop, a condition, and a Try/Catch.

## Reuse and modularity

Automation 360 encourages **modular** bots over monolithic scripts:

- **Subtasks / child bots** — factor common logic into a reusable bot that other bots call (a "log in to the ERP" subtask used by many automations).
- **Packages** — bundle reusable actions and logic.
- **Variables and configuration** — parameterize bots so the same logic runs against different inputs/environments.

Modularity makes automations **maintainable and scalable** — fix the shared login once and every bot benefits — and it is a hallmark of Advanced-level development. The lab factors a reusable subtask. *(This mirrors reuse patterns across automation platforms, e.g. [UiPath (CXLIX)](../../volume-149-uipath-certifications/README.md) libraries and [Pega's layer cake (CLXIV)](../../volume-164-pega-certifications/README.md).)*

## Hands-On Lab

Python simulates a Task Bot — actions, variables, control flow, and a reusable subtask. **Cost:** none.

### Lab 3.1 — Build a Task Bot

**Objective:** Assemble actions over variables with a loop, a condition, a Try/Catch, and a subtask.

```bash
python3 - <<'EOF'
# a Task Bot = ordered ACTIONS over VARIABLES, with control flow. Actions from "packages".
def pkg_excel_read():   # Excel package: read rows
    return [{"id": 1, "amount": "1500", "vendor": "Acme"},
            {"id": 2, "amount": "80",   "vendor": "Globex"},
            {"id": 3, "amount": "bad",  "vendor": "Initech"}]   # bad row -> Try/Catch
def subtask_login(system):    # reusable child bot: log in once, reused by many bots
    return f"logged into {system}"

print("TASK BOT: read invoices -> classify -> enter into ERP (with Try/Catch)\n")
print(f"   [subtask] {subtask_login('ERP')}")   # modular reuse
rows = pkg_excel_read()                          # action package
processed, errors = [], []
for r in rows:                                   # LOOP over rows
    try:
        amount = int(r["amount"])                # (may raise on 'bad')
        route = "approval" if amount >= 1000 else "auto"   # IF/ELSE condition
        processed.append({**r, "amount": amount, "route": route})
        print(f"   row {r['id']}: {r['vendor']:8} {amount:>5} -> {route}")
    except ValueError:                           # TRY/CATCH
        errors.append(r); print(f"   row {r['id']}: {r['vendor']:8} -> CATCH: bad amount -> error queue")
print()
print(f"   entered into ERP: {len(processed)}   error queue: {len(errors)}")
print()
print("A TASK BOT assembles packaged ACTIONS (Excel read) over VARIABLES, with a LOOP over")
print("rows, an IF/ELSE to classify, and a TRY/CATCH so one bad row goes to an error queue")
print("instead of crashing the run. A reusable SUBTASK (login) is called rather than repeated.")
print("Decomposing a process into resilient, modular actions is the Essentials/Advanced skill.")
EOF
```

**Expected result:** A Task Bot that calls a reusable login subtask, loops over three invoice rows, classifies each as approval or auto by amount, and catches the malformed row into an error queue — entering two rows into the ERP. The lesson is the bot-building model: packaged actions over variables, with loops, conditions, error handling, and reusable subtasks — the resilient, modular development the Essentials and Advanced certifications validate.

**Negative test:** Building the bot with no Try/Catch and inline repeated login logic. The malformed row crashes the whole run, and a change to the login must be made in every bot; control flow and modular subtasks are what make automations production-grade.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Task Bot understood — ordered actions over variables, built visually in the Bot Creator.
- [ ] Recorders and action packages understood — capture interactions and configure pre-built actions.
- [ ] Control flow understood — loops, if/else, try/catch, and waits for resilient bots.
- [ ] Reuse understood — subtasks, packages, and parameterization for maintainable, scalable automation.

## See also

- [Chapter 04 — The Control Room](04-the-control-room.md) — where bots are stored, deployed, and governed.
- [Chapter 05 — Attended, Unattended, and Automation Co-Pilot](05-attended-unattended-and-copilot.md) — how bots are triggered and assisted by AI.
- [Chapter 06 — Document Automation](06-document-automation.md) — handling the unstructured inputs plain bots cannot.
