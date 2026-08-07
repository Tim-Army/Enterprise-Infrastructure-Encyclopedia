# Chapter 09: Choosing Your Automation Anywhere Path

## Learning Objectives

- Map roles (bot developer, senior developer, AI automation engineer, admin, CoE lead) to certifications.
- Sequence certifications — start free with Essentials, then Advanced, then AI Automation Engineer.
- Understand where AI/agentic skills fit a modern automation career.
- Place Automation Anywhere in the automation ecosystem.

*Cert relevance: this chapter turns the tier map ([Ch 1](01-the-automation-anywhere-program.md)) into a personal plan and ends with a capstone.*

## Match the credential to your role

Automation Anywhere certifications map to what you do:

| Your role | Start here | Then consider |
| --- | --- | --- |
| **New to automation** | Essentials Certification (free) ([Ch 3](03-building-bots.md)) | Advanced Certification |
| **Bot / automation developer** | Advanced Certification ([Ch 3](03-building-bots.md), [Ch 4](04-the-control-room.md)) | AI Automation Engineer |
| **AI automation engineer** | AI Automation Engineer ([Ch 6](06-document-automation.md), [Ch 7](07-agentic-process-automation.md)) | (deepen with Masterclasses) |
| **Platform administrator** | Advanced (Control Room focus) ([Ch 4](04-the-control-room.md)) | AI Automation Engineer for AI governance |
| **CoE lead / architect** | Advanced + AI Automation Engineer | APA Leader Masterclass ([Ch 8](08-process-discovery-and-coe.md)) |

The pattern: **start free with Essentials**, prove development skill with **Advanced**, then move to **AI Automation Engineer** as automation becomes AI-driven. The lab builds a role-to-path planner.

## Sequence sensibly

A workable sequence for most people:

1. **Start with Essentials (free).** It removes the barrier to entry and teaches core bot building on Automation 360 — do this first, at no cost.
2. **Earn the Advanced Certification.** Prove real development competency — complex bots, the Control Room, error handling, reuse, deployment, and governance. This is the mainstream developer credential (60 questions, 2 hours, 80% to pass; renew with the $50 renewal).
3. **Move to AI Automation Engineer.** As the platform and the industry shift to **Agentic Process Automation**, this is where the growth is — Document Automation, Automation Co-Pilot, and AI Agent Studio. It is what turns a bot developer into an automation **engineer**.
4. **Add program skills.** For senior/lead roles, the Masterclasses (APA Developer, APA Leader) and CoE competency ([Ch 8](08-process-discovery-and-coe.md)) round out the picture.

Because training is **free** on Automation Anywhere University, the main investment is time and the exam. Plan to **recertify** as Automation 360 advances. The lab sequences a plan.

## Where AI fits a modern automation career

The single most important career signal in this volume is the **RPA→APA shift** ([Ch 1](01-the-automation-anywhere-program.md)). Automation used to be about **scripting deterministic bots**; increasingly it is about **engineering AI-driven automation** — agents that reason, document AI that reads, copilots that assist. The certifications reflect this: the flagship is **AI Automation Engineer**, not a pure-RPA credential.

For your career, that means: **learn the RPA fundamentals** (they are the reliable, auditable actions that still matter) **and** the **AI/agentic** skills (Document Automation, AI Agent Studio, governance of AI). The engineers who combine deterministic reliability with AI reasoning — and can **govern** the result — are the ones who deliver production automation in the agentic era. The capstone exercises exactly that combination.

## Automation Anywhere in the ecosystem

Automation Anywhere is a leader in a competitive, converging space:

- **RPA / automation peers** — [UiPath (CXLIX)](../../volume-149-uipath-certifications/README.md) and [Pega Robotics (CLXIV)](../../volume-164-pega-certifications/README.md): overlapping RPA-to-agentic evolution. Automation Anywhere's angle is a **cloud-native, web-based** platform with a strong pivot to **Agentic Process Automation**.
- **Broader automation and integration** — the work automation touches spans low-code platforms ([ServiceNow LXXX](../../volume-080-servicenow-certifications/README.md), [Pega CLXIV](../../volume-164-pega-certifications/README.md)) and integration ([MuleSoft CLX](../../volume-160-mulesoft-certifications/README.md), [Boomi CLXVI](../../volume-166-boomi-certifications/README.md)).
- **The AI layer** — generative AI and agents are now common across all of them; the differentiator is how well each **governs** AI-driven automation.

Learning Automation Anywhere is learning the **digital-workforce** discipline in its modern, AI-driven form. The capstone builds an end-to-end agentic automation. The lab closes with it.

## Hands-On Lab

Python builds a role-to-path planner, then a capstone combining RPA, IDP, and an AI agent. **Cost:** none.

### Lab 9.1 — Plan your Automation Anywhere path

**Objective:** Turn a role into a sequenced certification plan.

```bash
python3 - <<'EOF'
ROLE_PATHS = {
  "New to automation":     ["Essentials (free)", "Advanced Certification"],
  "Automation developer":  ["Advanced Certification", "AI Automation Engineer"],
  "AI automation engineer":["AI Automation Engineer", "APA Developer Masterclass"],
  "CoE lead":              ["Advanced Certification", "AI Automation Engineer", "APA Leader Masterclass"],
}
def plan(role):
    steps = ROLE_PATHS[role]
    print(f"   ROLE: {role}")
    print(f"      1. START: {steps[0]}")
    for i, s in enumerate(steps[1:], 2):
        print(f"      {i}. THEN:  {s}")
    print("      note: training is FREE on Automation Anywhere University; Advanced = 60Q/2h/80%")
print("AUTOMATION ANYWHERE ROLE -> CERTIFICATION PATH:\n")
for role in ["New to automation", "Automation developer", "CoE lead"]:
    plan(role); print()
print("Start FREE with Essentials, prove development with Advanced, then move to AI Automation")
print("Engineer as automation becomes AI-driven — the growth direction of the whole platform.")
EOF
```

**Expected result:** A planner turning roles into sequenced paths — a newcomer starts free with Essentials then Advanced; a developer takes Advanced then AI Automation Engineer; a CoE lead adds the APA Leader Masterclass. The lesson is to start free with Essentials, prove development with Advanced, and move to AI Automation Engineer as automation becomes AI-driven.

**Cleanup:** None.

### Lab 9.2 — Capstone: an end-to-end agentic automation

**Objective:** Combine RPA, Document Automation, and an AI agent under governance.

```bash
python3 - <<'EOF'
# CAPSTONE: accounts-payable, agentic — IDP reads, agent reasons, bot acts, human oversees
log = []
# 1) Document Automation (IDP): read the invoice (unstructured -> structured)
invoice = {"no": "INV-900", "vendor": "Acme", "total": 1800.0, "confidence": 0.95}
log.append(f"IDP: extracted {invoice['no']} total ${invoice['total']} (confidence {invoice['confidence']})")
# 2) AI agent: reason about the goal, decide, under guardrails
GUARDRAIL = 1000
if invoice["confidence"] < 0.80:
    log.append("agent: low confidence -> route to human review (Document Automation)")
elif invoice["total"] > GUARDRAIL:
    log.append(f"agent: ${invoice['total']} > ${GUARDRAIL} guardrail -> escalate for human approval")
    log.append("human: approves (oversight)")
# 3) deterministic bot: perform the audited action
log.append(f"bot: entered {invoice['no']} into ERP (deterministic, audited in Control Room)")
# 4) Bot Insight: measure
log.append("Bot Insight: +1 invoice processed, ~0.1 hr saved, exception rate 0%")

print("CAPSTONE — agentic accounts-payable (IDP + agent + bot + human, governed):\n")
for step in log: print(f"   {step}")
print()
print("Document Automation READS the unstructured invoice; the AI AGENT reasons about the goal")
print("and, bounded by a GUARDRAIL, escalates a large amount for HUMAN oversight; a deterministic")
print("BOT performs the audited ERP entry; and Bot Insight MEASURES the impact. AI to understand,")
print("agents to reason, bots to act, humans to oversee — governed and measured. That combination")
print("is modern Agentic Process Automation, and what this volume's certifications prepare you to build.")
EOF
```

**Expected result:** A capstone where Document Automation extracts an invoice, an AI agent reasons and escalates the over-threshold amount for human approval under a guardrail, a deterministic bot performs the audited ERP entry, and Bot Insight measures the impact. The lesson synthesizes the volume: modern automation combines AI understanding (IDP), agent reasoning, deterministic bot action, and human oversight — governed and measured — which is exactly what the Essentials → Advanced → AI Automation Engineer path prepares you to build.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Roles mapped to certifications — developer, AI automation engineer, admin, CoE lead.
- [ ] A sensible sequence chosen — free Essentials, then Advanced, then AI Automation Engineer.
- [ ] The AI/agentic direction understood — combine deterministic RPA with AI reasoning, and govern it.
- [ ] Automation Anywhere placed in the ecosystem — cloud-native digital-workforce automation, pivoting to agentic AI.

## See also

- [Chapter 01 — The Automation Anywhere Certification Program](01-the-automation-anywhere-program.md) — the tiers and mechanics this plan draws on.
- [Volume CXLIX — UiPath](../../volume-149-uipath-certifications/README.md) and [Volume CLXIV — Pega](../../volume-164-pega-certifications/README.md) — automation peers.
- [Volume CLXVI — Boomi](../../volume-166-boomi-certifications/README.md) — integration that automation connects to.
