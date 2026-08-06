# Chapter 08: The Business Architect and DCO

## Learning Objectives

- Explain the Business Architect role.
- Describe DCO (Directly Capture Objectives).
- Understand executable requirements versus disconnected documents.
- Recognize business-IT collaboration in Pega.

*Cert relevance: the Certified Pega Business Architect (CPBA) validates capturing requirements the Pega way.*

## The Business Architect role

The **Certified Pega Business Architect (CPBA)** is the **business-facing** role — analyzing, designing, and **capturing business requirements** in Pega applications. Where the [System Architect (Ch 4)](04-building-an-application.md) implements the technical solution, the Business Architect **defines what the business needs**: the case types, the process stages, the business rules, the data the business cares about. The Business Architect is the **bridge** between the business stakeholders (who know the requirements) and the technical build — and in Pega, because it's [low-code and model-driven (Ch 2)](02-the-pega-platform.md), the Business Architect can capture requirements **directly in the tool**. The lab models the role.

## DCO: Directly Capture Objectives

Pega's distinctive methodology is **DCO — Directly Capture Objectives**. Traditionally, requirements are captured in **documents** (Word specs, spreadsheets) that are **disconnected** from the application — the developer reads the doc and builds something, and the two **drift apart** (the doc goes stale, the app doesn't match). DCO flips this: business and IT **collaborate in Pega itself** to capture objectives **directly** as **executable application artifacts** — the requirements are captured as actual case stages, steps, and rules in a **working (if incomplete) application**, refined together in real time. The requirement **is** the beginning of the application. This eliminates the doc-to-code translation gap. The lab models DCO.

## Executable requirements versus disconnected documents

The power of DCO is **executable requirements**. Because business and IT capture objectives **in the model**, the requirements are **immediately real**:

- **No translation gap** — there's no separate spec to misinterpret; the captured objective **is** the application structure.
- **Immediate feedback** — stakeholders **see and try** the emerging application as requirements are captured (via [App Studio, Ch 2](02-the-pega-platform.md)), so misunderstandings surface early.
- **Living, not stale** — the "requirements" evolve **with** the application because they're the same artifact.

This is the low-code advantage applied to **requirements**: capture them directly, as executable artifacts, collaboratively — far faster and more accurate than the traditional document-then-build handoff. The lab models executable requirements.

## Business-IT collaboration

DCO embodies Pega's **business-IT collaboration** model. Because the platform is model-driven and has both [App Studio (business) and Dev Studio (developer), Ch 2](02-the-pega-platform.md), business architects and system architects **work on the same application** at the appropriate level — the business architect captures and refines objectives, the system architect adds technical depth. This tight collaboration, in **one tool**, on **one evolving application**, is what makes Pega development **fast** and **aligned** with business needs. The Business Architect and System Architect are complementary roles delivering the same application together. The lab synthesizes.

## Hands-On Lab

Python models DCO and executable requirements. **Cost:** none.

### Lab 8.1 — DCO: capture objectives directly as an executable app

**Objective:** Contrast document-then-build with Directly Capture Objectives.

```bash
python3 - <<'EOF'
# TRADITIONAL: requirements in a document, disconnected from the build
print("TRADITIONAL requirements (document-then-build):")
print("   1. business writes a 40-page Word spec")
print("   2. IT reads it, INTERPRETS it, builds something weeks later")
print("   3. doc goes STALE; app DRIFTS from the spec; misunderstandings found LATE")
print("   -> a translation GAP between requirement and application\n")

# DCO: capture objectives DIRECTLY in Pega as executable app artifacts
print("DCO — Directly Capture Objectives (business + IT collaborate IN Pega):")
captured = {
  "case type": "AccountOpening",
  "stages (captured directly)": ["Application", "Verification", "Approval", "Activation"],
  "business rule (captured directly)": "if balance >= 10000 -> priority handling",
  "status": "an EXECUTABLE (if incomplete) application — not a document",
}
for k, v in captured.items():
    print(f"   {k:32}: {v}")
print()
print("   -> stakeholders SEE + TRY the emerging app (App Studio) as objectives are captured")
print("   -> the requirement IS the application structure — NO translation gap, immediate feedback\n")
print("The BUSINESS ARCHITECT (CPBA) captures WHAT the business needs. ★ DCO (Directly Capture")
print("Objectives) = business + IT collaborate IN Pega to capture objectives DIRECTLY as EXECUTABLE")
print("app artifacts (case stages/steps/rules in a working app) — NOT disconnected Word docs that go")
print("stale + drift. Requirements become IMMEDIATELY REAL: no doc-to-code translation gap, stakeholders")
print("try the emerging app + surface misunderstandings EARLY. Low-code applied to REQUIREMENTS —")
print("business + IT on ONE evolving application, fast + aligned. The BA + SA deliver it together.")
EOF
```

**Expected result:** Traditional document-then-build (a Word spec that IT interprets weeks later, drifting and stale, with a translation gap) contrasted with DCO (business and IT capturing objectives directly in Pega as an executable AccountOpening application — stages, rules — that stakeholders see and try immediately). The Business Architect lesson is that DCO captures requirements directly as executable application artifacts rather than disconnected documents, eliminating the doc-to-code translation gap and enabling immediate feedback — low-code applied to requirements, with business and IT collaborating on one evolving application.

**Negative test:** Capturing requirements in a Word document handed to developers to build later. The document drifts from the app, gets misinterpreted, and surfaces problems late; DCO captures objectives directly as executable artifacts in Pega, keeping requirements real, aligned, and validated early.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Business Architect role understood — analyzing and capturing business requirements in Pega.
- [ ] DCO (Directly Capture Objectives) understood — capturing objectives directly in the tool with business and IT.
- [ ] Executable requirements versus disconnected documents understood — no translation gap, immediate feedback.
- [ ] Business-IT collaboration understood — business and system architects on one evolving application.
