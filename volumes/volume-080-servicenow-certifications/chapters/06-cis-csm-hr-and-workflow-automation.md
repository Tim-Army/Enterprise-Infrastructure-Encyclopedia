# Chapter 06: CIS — CSM, HR, and Workflow Automation

## Learning Objectives

- Implement Customer Service Management (CSM).
- Deliver HR services with HR Service Delivery (HRSD).
- Automate processes with Flow Designer.
- Build employee/customer experiences with Service Portal.
- Complete a walkthrough for each CSM/HR/workflow domain.

## Theory and Architecture

ServiceNow extends beyond IT to **customer** and **employee** workflows, unified by a low-code
automation engine. **Customer Service Management (CSM)** manages external customer cases, accounts,
contacts, and entitlements, often with SLAs and omni-channel intake. **HR Service Delivery (HRSD)**
delivers employee services — onboarding, cases, knowledge — with **scoped data separation** (HR data
is sensitive and access-controlled). Both are automated with **Flow Designer** — ServiceNow's
**low-code** workflow tool where **triggers** (record created/updated, scheduled) drive **actions**
(create task, send notification, call a subflow, integrate) without heavy scripting, replacing the
older Workflow editor. The **Service Portal** provides the branded, self-service front end (catalog,
knowledge, requests) that employees and customers actually use. The pattern is consistent: model the
records, automate with **Flow Designer**, and surface via the **Service Portal** — the same platform
serving IT, customer, and HR use cases. This chapter teaches each with a hands-on walkthrough (flow
logic, HR data separation, and portal design).

## Design Considerations

Model **CSM** (accounts/contacts/cases + SLAs) and **HRSD** (with data separation for sensitive HR
records). Automate with **Flow Designer** (trigger → actions), preferring low-code over scripting.
Reuse **subflows**. Deliver via a branded **Service Portal**. Apply **SLAs** and knowledge. Keep HR
data **access-controlled**.

## Implementation and Automation

The labs build a flow, separate HR data, and design a portal.

## Validation and Troubleshooting

Confirm the CSM/HR/workflow model:

```text
CSM = external customer cases/accounts/contacts/entitlements + SLAs. HRSD = employee services with data separation (sensitive). Automate: Flow Designer (trigger -> actions, low-code, subflows) replacing legacy Workflow.
Front end: Service Portal (self-service catalog/knowledge/requests).
```

Common pitfalls: heavy **scripting** where **Flow Designer** suffices; and HR data without **access
separation**.

## Security and Best Practices

Model CSM/HRSD correctly, automate low-code with **Flow Designer**, separate **HR data**, apply
**SLAs**, and deliver via the **Service Portal**. Reuse subflows. All work is authorized administration.

## Hands-On Lab

CSM/HR/workflow walkthroughs. **Shared prerequisites** — `python3`, a free PDI. **Cost:** none.

### Lab 6.1 — Build a Flow Designer flow

**Objective:** Automate low-code.

```python
python3 - <<'PY'
flow={"trigger":"HR case created (category=onboarding)",
      "actions":["create task: provision accounts","create task: order equipment",
                 "notify: manager","wait: all tasks complete","update: case = ready for day 1"]}
print("trigger:",flow["trigger"])
for i,a in enumerate(flow["actions"],1): print(f"  {i}. {a}")
print("Flow Designer: trigger -> ordered actions (low-code, no heavy scripting)")
PY
```

**Expected result:** an onboarding **flow** (trigger → actions) — low-code automation.

**Negative test:** script the whole onboarding in a Business Rule; **Flow Designer** is clearer and
maintainable — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Separate sensitive HR data

**Objective:** Protect employee data.

```python
python3 - <<'PY'
def can_view(user_role, record_type):
    if record_type=="hr_case_sensitive": return user_role in ("hr_admin","hr_manager")
    return True
print("IT agent views sensitive HR case:", can_view("itil","hr_case_sensitive"))
print("HR manager views sensitive HR case:", can_view("hr_manager","hr_case_sensitive"))
print("HRSD: sensitive HR data is access-separated (not visible to general IT/agents)")
PY
```

**Expected result:** sensitive HR records **hidden** from non-HR roles — HR data separation.

**Negative test:** store HR cases in general ITSM tables; IT agents see salary/PII — **separate** HR
data.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Design a Service Portal page

**Objective:** Deliver self-service.

```python
python3 - <<'PY'
portal={"widgets":["search knowledge","popular catalog items","my open requests","announcements"],
        "branding":"company logo + theme","audience":"employees + customers (scoped)"}
for k,v in portal.items(): print(f"{k:9}: {v}")
print("Service Portal: branded self-service (catalog + knowledge + requests) — the user front end")
PY
```

**Expected result:** a **Service Portal** page composed of widgets — the self-service experience.

**Negative test:** send users into the raw platform UI; the **Service Portal** is the intended
front-end — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Apply an SLA

**Objective:** Track response/resolution targets.

```python
python3 - <<'PY'
sla={"P1 incident":{"response":"15 min","resolution":"4 h"},"customer case (gold)":{"response":"1 h","resolution":"1 day"}}
for item,targets in sla.items(): print(f"{item:22}: {targets}")
print("CSM/ITSM: SLAs set + measure response/resolution targets; breaches escalate")
PY
```

**Expected result:** **SLAs** with response/resolution targets — measurable service commitments.

**Negative test:** promise service levels with no **SLA** tracking; breaches go unnoticed — define and
measure SLAs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CIS-CSM/HRSD extend the platform to customer and employee workflows, automated low-code with Flow
Designer, separated for sensitive HR data, delivered via the Service Portal, and measured with SLAs —
one platform across IT, customer, and HR.

- [ ] I can build a Flow Designer flow.
- [ ] I can separate sensitive HR data.
- [ ] I can design a Service Portal page.
- [ ] I can apply an SLA.
- [ ] I completed Labs 6.1–6.4 including each negative test.
