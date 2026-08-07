# Chapter 01: The Automation Anywhere Certification Program

## Learning Objectives

- Describe Automation Anywhere and its pivot from RPA to Agentic Process Automation.
- Map the certification tiers — Essentials, Advanced, and AI Automation Engineer.
- Understand the Advanced exam mechanics — 60 questions, 2 hours, 80% to pass.
- Recognize Automation Anywhere University as the free training path.

*Cert relevance: this chapter frames the whole program — the tiers, mechanics, and platform the rest of the volume develops.*

## Automation Anywhere and its certifications

**Automation Anywhere** is one of the pioneers of **RPA — robotic process automation**, the practice of building software "bots" that automate repetitive, rules-based work across applications (log into a system, read a spreadsheet, key data into another app). What distinguishes Automation Anywhere today is a decisive pivot to **Agentic Process Automation (APA)**: combining classic RPA with **AI agents** and **generative AI**, so automations can not only follow fixed rules but also **reason, decide, and handle unstructured work**. Its platform is the **Automation Success Platform**, built on **Automation 360** — cloud-native and fully **web-based**, so you build and run bots from a browser.

Automation Anywhere certifications are delivered through **Automation Anywhere University** (`pathfinder.automationanywhere.com/university`), where **training is free**. The certifications validate that you can build, run, and govern automations on Automation 360 — and, at the top tier, that you can build **AI-driven** automations. Automation Anywhere sits alongside the automation platforms this shelf covers ([UiPath CXLIX](../../volume-149-uipath-certifications/README.md), [Pega CLXIV](../../volume-164-pega-certifications/README.md)). The lab builds the program map.

## The certification tiers

Automation Anywhere University offers **three certification tiers**, foundational to advanced:

| Tier | Certification | Focus |
| --- | --- | --- |
| **Foundational** | **Essentials Certification** (free) | Building basic bots on Automation 360 |
| **Advanced** | **Advanced Certification** (Certified Advanced Automation Professional) | Advanced development on Automation 360 ([Ch 3](03-building-bots.md), [Ch 4](04-the-control-room.md)) |
| **AI / Agentic** | **AI Automation Engineer Certification** | AI-driven automation — Document Automation, AI Agent Studio, Co-Pilot ([Ch 6](06-document-automation.md), [Ch 7](07-agentic-process-automation.md)) |

The progression mirrors the platform's evolution: **build bots** (Essentials/Advanced) then **build AI-powered, agentic automations** (AI Automation Engineer). There are also **Masterclasses** — learning paths like *Agentic Process Automation Developer*, *APA Leader*, and *Document Automation* — that prepare you but are courses, not exams. The lab maps the tiers.

## Exam mechanics

The **Advanced Certification** exam has a well-defined shape (representative of the program's proctored exams):

- **60 multiple-choice questions.**
- **2 hours (120 minutes).**
- **80% to pass** — a demanding bar.
- **2 attempts** allowed.
- **Renewal** — the Advanced credential is renewed with a **$50** renewal certification, keeping it current with the platform.
- **Preparation** — free Automation Anywhere University courses and structured **learning trails** (e.g. "Advanced RPA Professional Prep (Automation 360)").

The **Essentials** tier is **free**, lowering the barrier to entry, while Advanced and AI Automation Engineer validate deeper, hands-on competency. Because the platform updates continually, credentials track the current Automation 360 release, and renewal keeps them valid. The lab records the mechanics.

## The Agentic pivot

Understanding the program means understanding where Automation Anywhere is going. Classic RPA automates **rules-based, structured** work — perfect for stable, repetitive processes, but brittle when inputs vary or judgment is needed. **Agentic Process Automation** adds **AI**:

- **AI agents** that can reason about a goal and orchestrate steps, not just replay a fixed script.
- **Generative AI** (via **Automation Co-Pilot** and **AI Agent Studio**) to handle language, summarize, decide, and assist humans.
- **Intelligent Document Processing** (**Document Automation**) to read unstructured documents (invoices, forms) that classic RPA cannot.

This is why the top certification is **AI Automation Engineer**, not "Master RPA Professional" — the discipline has moved from **scripting bots** to **engineering AI-driven automation**. The rest of this volume follows that arc: platform and bots first, then Control Room governance, then attended AI, documents, and agentic AI. The lab notes the shift.

## Hands-On Lab

Python models the program: the tiers, the mechanics, and the RPA→APA shift. **Cost:** none.

### Lab 1.1 — Map the certification tiers

**Objective:** Record the three tiers and the free-to-advanced progression.

```bash
python3 - <<'EOF'
TIERS = [
  ("Essentials Certification",       "Foundational", "free",     "build basic bots on Automation 360"),
  ("Advanced Certification",         "Advanced",     "60Q/2h/80%","advanced development; renewal $50"),
  ("AI Automation Engineer Cert",    "AI / Agentic", "exam",     "Document Automation, AI Agent Studio, Co-Pilot"),
]
print("AUTOMATION ANYWHERE UNIVERSITY — certification tiers:\n")
for name, tier, mech, focus in TIERS:
    print(f"   [{tier:12}] {name:32} ({mech})")
    print(f"                  -> {focus}")
print()
print("Masterclasses (learning paths, not exams): Agentic Process Automation Developer,")
print("APA Leader, Document Automation. Training is FREE; certs validate hands-on skill.")
print()
print("The progression mirrors the platform: BUILD BOTS (Essentials/Advanced) then build")
print("AI-POWERED, AGENTIC automations (AI Automation Engineer). Start free with Essentials.")
EOF
```

**Expected result:** A tier map — Essentials (free, foundational), Advanced (60Q/2h/80%, renewal $50), and AI Automation Engineer (AI/agentic) — plus the non-exam Masterclasses. The lesson is that the program runs from a free foundational credential to advanced development to AI-driven automation, mirroring the platform's evolution, with free University training throughout.

**Cleanup:** None.

### Lab 1.2 — RPA versus Agentic Process Automation

**Objective:** Contrast classic RPA with the AI-driven APA the top tier validates.

```bash
python3 - <<'EOF'
# route a task to RPA (rules/structured) or APA (AI/agentic) by its characteristics
def route(task):
    if task["structured"] and task["rules_based"] and not task["needs_judgment"]:
        return "RPA (Task Bot)"          # classic, deterministic
    return "Agentic (AI agent / Co-Pilot / Document Automation)"  # AI-driven

TASKS = [
  {"name": "copy invoices CSV -> ERP",        "structured": True,  "rules_based": True,  "needs_judgment": False},
  {"name": "extract data from PDF invoices",  "structured": False, "rules_based": True,  "needs_judgment": False},
  {"name": "triage a free-text support email","structured": False, "rules_based": False, "needs_judgment": True},
]
print("RPA vs AGENTIC PROCESS AUTOMATION — route by task nature:\n")
for t in TASKS:
    print(f"   '{t['name']}'")
    print(f"      structured={t['structured']!s:5} rules={t['rules_based']!s:5} judgment={t['needs_judgment']!s:5} -> {route(t)}")
print()
print("Classic RPA automates STRUCTURED, RULES-BASED work deterministically (copy CSV->ERP).")
print("AGENTIC PROCESS AUTOMATION adds AI for UNSTRUCTURED input (read a PDF -> Document")
print("Automation) and JUDGMENT (triage free text -> AI agent). The discipline moved from")
print("scripting bots to engineering AI-driven automation — hence the AI Automation Engineer cert.")
EOF
```

**Expected result:** A router sending a structured CSV-to-ERP copy to classic RPA, a PDF-extraction task to Document Automation, and a free-text triage to an AI agent. The lesson is the RPA→APA shift: classic RPA handles structured rules-based work deterministically, while Agentic Process Automation adds AI for unstructured input and judgment — the competency the AI Automation Engineer certification validates.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Automation Anywhere placed — an RPA pioneer pivoting to Agentic Process Automation on the cloud-native Automation Success Platform.
- [ ] The tiers mapped — Essentials (free), Advanced, and AI Automation Engineer.
- [ ] The Advanced exam mechanics recorded — 60 questions, 2 hours, 80% to pass, renewal $50.
- [ ] The RPA→APA shift understood — from scripting bots to engineering AI-driven automation.

## See also

- [Volume CXLIX — UiPath](../../volume-149-uipath-certifications/README.md) — the closest RPA-to-agentic peer.
- [Volume CLXIV — Pega](../../volume-164-pega-certifications/README.md) — low-code automation with Robotics and GenAI.
- [Chapter 02 — The Automation Success Platform](02-automation-success-platform.md).
