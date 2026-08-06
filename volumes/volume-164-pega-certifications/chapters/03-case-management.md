# Chapter 03: Case Management — The Pega Core

## Learning Objectives

- Explain case management as Pega's core concept.
- Describe cases, stages, steps, and processes.
- Understand dynamic case management versus rigid workflow.
- Recognize the case lifecycle and automation.

*Cert relevance: case management is the heart of Pega and central to the System Architect certifications.*

## What a case is

**Case management** is the **core** of Pega — the way Pega models **work**. A **case** is a **unit of work** that needs to be **completed** — a loan application, a customer service request, an insurance claim, an onboarding. The case has a **lifecycle** (from creation to resolution), carries **data**, moves through **steps**, involves **people and automations**, and has an **outcome**. Instead of scattering a business process across code, forms, and integrations, Pega models it as a **case type** — a reusable template for that kind of work. Thinking in **cases** is the fundamental Pega mindset, and building case types is the primary System Architect skill. The lab models a case.

## Stages, steps, and processes

A case type is structured as **stages** and **steps** — the **Pega case lifecycle**:

- **Stages** — the major **phases** of the work (e.g., a loan case: *Submission → Review → Underwriting → Decision → Fulfillment*). Stages give the case a clear, business-readable shape.
- **Steps** — the individual **tasks** within a stage (collect data, get approval, send a letter, call a service). A step can be a **human task** (someone does work) or an **automation** (the system does it).
- **Processes / flows** — sequences of steps with logic and routing.

This stage-based lifecycle is **visual and business-readable** — a business architect can look at the stages and understand the process, and the model *is* the running application. Modeling work as stages and steps is core case design. The lab models the lifecycle.

## Dynamic case management versus rigid workflow

Pega's distinctive strength is **dynamic** case management, contrasted with **rigid, hard-coded workflow**. Traditional BPM often models a process as a **fixed flowchart** — every path predetermined. Real work is **messier**: cases need to **adapt** — skip a step, add an approval, wait for an event, handle an exception, be reassigned. Pega cases are **dynamic**: the lifecycle can respond to data and events, cases can be **adjusted at runtime**, and the case "knows" its state and what's next. This **case-centric, adaptive** model handles the complexity and exceptions of real business work that rigid workflows can't. Dynamic case management is why Pega is used for complex enterprise processes. The lab models adaptability.

## The case lifecycle and automation

A case moves through its lifecycle driven by a mix of **human work** and **automation**. Pega **orchestrates** this: routing tasks to the right people (by skill, workload, role), automating steps that don't need a human (calling a service, making a [decision, Ch 6](06-decisioning-and-next-best-action.md), sending a notification), enforcing **service-level agreements (SLAs)** so work doesn't stall, and tracking the case to resolution. This orchestration — humans and automation working together on a case, with routing, SLAs, and tracking — is what turns a case type into a **running business process** that scales. The lab synthesizes.

## Hands-On Lab

Python models a case lifecycle. **Cost:** none.

### Lab 3.1 — A dynamic case lifecycle with stages, steps, and automation

**Objective:** Model a case moving through stages with human and automated steps.

```bash
python3 - <<'EOF'
# a loan case type: stages -> steps (human or automated), dynamic + adaptive
CASE_TYPE = "LoanApplication"
STAGES = {
  "Submission":   [("collect applicant data", "human"), ("validate completeness", "auto")],
  "Review":       [("credit check", "auto (decision)"), ("manual review if flagged", "human")],
  "Underwriting": [("risk assessment", "auto"), ("underwriter approval", "human")],
  "Decision":     [("approve/decline", "auto"), ("notify applicant", "auto")],
  "Fulfillment":  [("disburse funds", "auto")],
}
print(f"Case type: {CASE_TYPE}  (a unit of work with a lifecycle)\n")
print("Lifecycle = STAGES -> STEPS (human or automation):\n")
for stage, steps in STAGES.items():
    print(f"   [{stage}]")
    for step, kind in steps:
        print(f"      - {step:28} ({kind})")
print()
# dynamic behavior: a case ADAPTS at runtime (skip/add steps, SLAs)
print("DYNAMIC case management (vs rigid workflow):")
print("   - low-risk applicant -> SKIP 'manual review' step (adapt at runtime)")
print("   - high-value loan -> ADD a second underwriter approval (adapt)")
print("   - SLA: 'underwriter approval' due in 24h -> escalate if breached")
print("   - a rigid hard-coded flowchart CAN'T adapt like this; a Pega case CAN\n")
print("A CASE = a unit of work (loan/claim/request) with a LIFECYCLE. Pega models it as STAGES")
print("(business-readable phases) -> STEPS (human tasks + AUTOMATIONS). ★ DYNAMIC (not rigid): the")
print("case ADAPTS to data + events at runtime — skip/add steps, handle exceptions, enforce SLAs,")
print("route to the right people. Pega ORCHESTRATES humans + automation to drive the case to")
print("resolution. Case management is the HEART of Pega + the core System Architect skill.")
EOF
```

**Expected result:** A LoanApplication case type modeled as stages (Submission → Review → Underwriting → Decision → Fulfillment) with human and automated steps, plus dynamic behavior (skipping the manual review for low-risk applicants, adding an approval for high-value loans, escalating on SLA breach). The case-management lesson is that a case is a unit of work with a lifecycle modeled as stages and steps, and Pega's dynamic case management adapts to data and events at runtime (unlike rigid workflow), orchestrating humans and automation to resolution.

**Negative test:** Modeling a business process as a fixed, hard-coded flowchart. Real work has exceptions and adaptations a rigid flow can't handle; Pega's dynamic cases adapt at runtime — skipping, adding, escalating — which is why case management is its core.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Case management understood as Pega's core — modeling work as cases (units of work with a lifecycle).
- [ ] Stages, steps, and processes understood — the visual, business-readable case lifecycle.
- [ ] Dynamic case management versus rigid workflow understood — adapting to data and events at runtime.
- [ ] The case lifecycle and automation understood — orchestrating humans and automation with routing and SLAs.
