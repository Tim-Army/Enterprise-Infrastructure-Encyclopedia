# Chapter 07: Pega Robotics and GenAI

## Learning Objectives

- Explain Pega Robotics — RPA and the Robotics System Architect.
- Describe attended and unattended automation.
- Understand robotics within hyperautomation.
- Recognize Pega GenAI and AI-assisted development.

*Cert relevance: the Certified Pega Robotics System Architect and Pega's AI direction round out the platform.*

## Pega Robotics

**Pega Robotics** is Pega's **robotic process automation (RPA)** capability, and the **Certified Pega Robotics System Architect** validates it. RPA uses software **robots (bots)** to automate **repetitive, rule-based tasks** — especially tasks involving systems that have **no API** (legacy applications, desktop software), by having the bot **interact with the user interface** the way a human would (clicking, typing, reading screens). Bots are built in **Robot Studio**. RPA complements Pega's [case management (Ch 3)](03-case-management.md): where a case orchestrates a process, bots handle the **manual, UI-driven steps** within it that would otherwise need a human — the same RPA discipline the [UiPath volume (CXLIX)](../../volume-149-uipath-certifications/README.md) covers. The lab models RPA.

## Attended and unattended automation

Pega Robotics supports two modes:

- **Attended automation (RDA)** — bots that run **alongside a human**, on the employee's desktop, **assisting** with tasks in real time (auto-filling data across applications, surfacing information). The human is in the loop; the bot speeds their work.
- **Unattended automation (RPA)** — bots that run **independently**, without a human, on a schedule or trigger — processing **high-volume, back-office** work (batch data entry, reconciliation) autonomously.

Attended augments a worker; unattended replaces manual effort entirely for suitable tasks. Choosing the right mode for a task is part of robotics design. The lab models the modes.

## Robotics within hyperautomation

RPA is one part of **hyperautomation** — combining **API-led integration**, **RPA**, **case management**, and **AI** to automate **end-to-end** processes, including the parts without clean APIs. Pega's strength is that robotics sits **within** a broader automation platform: a case orchestrates the process, calls **integrations** where systems have APIs, uses **bots** where they don't, applies **decisioning** for intelligence, and involves humans where judgment is needed. This **combined** automation — not RPA alone — is how complex enterprise processes get fully automated. Robotics is a tool in Pega's hyperautomation toolkit, alongside cases and decisioning. The lab models the combination.

## Pega GenAI and AI-assisted development

Pega is investing in **generative AI** across the platform — **Pega GenAI**. A notable capability is **Pega GenAI Blueprint** — using generative AI to help **design an application**: you describe the business process in natural language, and the AI generates a **Blueprint** (a draft application design — case types, stages, data) you refine. This accelerates the early design phase and lowers the barrier to building on Pega. More broadly, GenAI is being woven into development (assisting authoring), operations (summarizing cases, drafting responses), and decisioning (generative interactions). AI-assisted development is Pega's modern direction, making the already-low-code platform even faster. The lab models AI-assisted design.

## Hands-On Lab

Python models RPA modes and AI-assisted design. **Cost:** none.

### Lab 7.1 — Attended vs unattended bots, and a GenAI Blueprint

**Objective:** See RPA modes and generative-AI app design.

```bash
python3 - <<'EOF'
# 1) choose attended vs unattended automation per task
TASKS = [
  ("agent copies data across 3 legacy apps during a call", "attended (RDA)", "assist the human in real time"),
  ("nightly batch: reconcile 10,000 records (no API)",      "unattended (RPA)", "run autonomously, high volume"),
  ("surface customer info to a rep as they work",           "attended (RDA)", "augment the worker"),
]
print("Pega Robotics — attended vs unattended automation:\n")
for task, mode, why in TASKS:
    print(f"   {task}")
    print(f"      -> {mode}: {why}")
print()
# 2) robotics within hyperautomation (a case uses the right tool per step)
print("Hyperautomation — a CASE uses the right tool per step:")
steps = [("look up modern CRM (has API)", "API integration"),
         ("update legacy app (NO API)", "RPA bot"),
         ("decide next best action", "decisioning"),
         ("underwriter judgment call", "human task")]
for step, tool in steps:
    print(f"   {step:34} -> {tool}")
print("   -> RPA is ONE tool among integration + decisioning + human work (not RPA alone)\n")
# 3) Pega GenAI Blueprint: describe -> AI drafts an app design
print("Pega GenAI BLUEPRINT — describe a process, AI drafts the app design:")
desc = "an employee onboarding process with IT setup, HR paperwork, and manager approval"
print(f"   input (natural language): '{desc}'")
print("   -> GenAI generates a BLUEPRINT: case type 'Onboarding' with stages")
print("      [Offer -> IT Setup -> HR Paperwork -> Manager Approval -> Complete] + data model")
print("   -> you refine it -> accelerates design (AI-assisted, on top of low-code)\n")
print("Pega ROBOTICS (Robotics System Architect cert) = RPA: bots automate repetitive, UI-driven")
print("tasks (esp. NO-API legacy) via Robot Studio. ATTENDED (RDA — assist a human live) vs")
print("UNATTENDED (RPA — run autonomously, high volume). RPA sits WITHIN hyperautomation (cases +")
print("integration + decisioning + humans). And ★ PEGA GENAI (Blueprint) uses generative AI to DRAFT")
print("app designs from a description — AI-assisted development making low-code even faster.")
EOF
```

**Expected result:** Tasks assigned to attended (RDA, assisting a human live) or unattended (RPA, autonomous high-volume) automation, robotics shown as one tool within hyperautomation (integration, RPA, decisioning, human work per step), and a Pega GenAI Blueprint drafting an onboarding case design from a natural-language description. The lesson is that Pega Robotics automates UI-driven and no-API tasks (attended to augment workers, unattended to run autonomously) as one tool within hyperautomation, and Pega GenAI accelerates development by generating application blueprints from descriptions.

**Negative test:** Trying to automate a whole process with RPA bots alone. Bots handle UI-driven and no-API tasks but not integration, decisioning, or judgment; Pega combines RPA with integration, cases, decisioning, and humans (hyperautomation), and GenAI accelerates the design.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Pega Robotics understood — RPA automating repetitive, UI-driven, no-API tasks (Robot Studio).
- [ ] Attended and unattended automation understood — augmenting a worker versus running autonomously.
- [ ] Robotics within hyperautomation understood — one tool alongside integration, cases, and decisioning.
- [ ] Pega GenAI understood — generative AI (Blueprint) assisting application design and development.
