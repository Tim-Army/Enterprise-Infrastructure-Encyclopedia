# Chapter 05: Attended, Unattended, and Automation Co-Pilot

## Learning Objectives

- Distinguish attended and unattended automation and when to use each.
- Describe Automation Co-Pilot as an AI assistant for developers and business users.
- Explain human-in-the-loop automation and front-office use cases.
- Understand how AI accelerates both building and running automations.

*Cert relevance: attended/unattended models and Automation Co-Pilot span the Advanced and AI Automation Engineer certifications.*

## Attended versus unattended

Bots run in two fundamentally different modes:

- **Unattended automation** — bots run **on their own**, on dedicated Bot Runners, **without a human present**. They are scheduled or triggered ([Ch 4](04-the-control-room.md)) and process work in the **back office** — overnight batch jobs, high-volume queues, system-to-system flows. This is the classic "digital workforce" that runs 24/7.
- **Attended automation** — bots run **alongside a person**, on that person's desktop, **assisting them** in real time. A call-center agent clicks a button and a bot gathers customer data across systems while they talk; the human stays in control and the bot handles the tedious steps. This is **front-office** automation.

The distinction drives licensing, design, and deployment: unattended bots need runners and orchestration; attended bots need to integrate into a person's workflow and be **triggered by them**. Many real programs use **both** — attended bots for human-in-the-loop tasks, unattended bots for lights-out processing. The lab routes tasks to the right mode.

## Human in the loop

Not every process can be fully automated — some steps need **human judgment or approval**. **Human-in-the-loop** automation combines bots and people:

- A bot does the **mechanical** work (gather, prepare, pre-fill), then **pauses for a human** to review, decide, or approve, then **continues** with the outcome.
- **Automation Co-Pilot** (below) surfaces these interactions **in the flow of work** — a business user approves or provides input without leaving their application.

This pattern is essential for processes involving exceptions, judgment, or compliance sign-off: the bot removes the drudgery while the human keeps control of the decision. It is also how automation earns trust — humans stay in charge of what matters. The lab adds a human-approval step.

## Automation Co-Pilot

**Automation Co-Pilot** is Automation Anywhere's **AI assistant**, and it works two ways:

- **Co-Pilot for developers** — an **AI helper inside the Bot Creator** that speeds building: it can generate automation logic from a **natural-language** description, suggest actions and mappings, and help debug. It lowers the skill barrier and accelerates development.
- **Co-Pilot for business users** — brings automation **into the applications people already use** (a browser, a CRM). A business user invokes automations, gets AI assistance, and completes work **in the flow**, without switching to the automation platform. It is the front-end of attended, human-in-the-loop automation.

Co-Pilot is central to the **AI Automation Engineer** direction ([Ch 1](01-the-automation-anywhere-program.md)): automation is no longer only pre-built bots but **AI-assisted** work, generated and guided by natural language. The lab models Co-Pilot assistance. *(This mirrors AI copilots across enterprise platforms — e.g. GenAI assistance in [Pega (CLXIV)](../../volume-164-pega-certifications/README.md) and [UiPath (CXLIX)](../../volume-149-uipath-certifications/README.md).)*

## AI accelerates building and running

The through-line is that **AI accelerates both sides** of automation:

- **Building** — Co-Pilot for developers generates and suggests, so you build bots faster and with less expertise.
- **Running** — Co-Pilot for business users puts automation and AI assistance **where work happens**, so more people benefit from it, in the flow.

This is why the platform's certifications culminate in **AI Automation Engineer**: modern automation engineering is as much about **applying AI** (to generate, assist, and decide) as about wiring deterministic bots. Attended/unattended is the deployment model; Co-Pilot is the AI layer over both. The lab synthesizes the modes and AI assistance.

## Hands-On Lab

Python models attended vs unattended, human-in-the-loop, and Co-Pilot assistance. **Cost:** none.

### Lab 5.1 — Route work across modes with a human step and Co-Pilot

**Objective:** Send tasks to attended or unattended runs, pause for a human, and use Co-Pilot.

```bash
python3 - <<'EOF'
# choose the automation MODE by the task's nature
def mode(task):
    if task["human_present"] and task["realtime"]:
        return "ATTENDED (runs with the person, front office)"
    return "UNATTENDED (runs on its own, back office)"

TASKS = [
  {"name": "nightly invoice batch",      "human_present": False, "realtime": False},
  {"name": "agent-assist during a call", "human_present": True,  "realtime": True},
]
print("ATTENDED vs UNATTENDED — route by task nature:\n")
for t in TASKS:
    print(f"   '{t['name']}' -> {mode(t)}")

# human-in-the-loop: bot prepares, human approves, bot continues
def process_refund(amount):
    print(f"\n   [bot] prepared refund ${amount} (gathered + validated)")
    if amount > 500:
        approved = True    # simulate the human approving in the flow via Co-Pilot
        print(f"   [human-in-the-loop] ${amount} > $500 -> human approval via Co-Pilot -> {'APPROVED' if approved else 'REJECTED'}")
    else:
        approved = True; print(f"   [bot] ${amount} under threshold -> auto-approved")
    if approved: print(f"   [bot] issued refund and updated systems")

process_refund(750)

# Automation Co-Pilot for developers: natural language -> automation logic
def copilot_build(nl):
    KB = {"read the invoice and enter it in the ERP":
          ["action: Excel read invoice", "action: connect ERP", "action: enter fields", "action: submit"]}
    return KB.get(nl, ["(Co-Pilot drafts actions from the description)"])
print("\n   CO-PILOT (developer): natural language -> suggested actions:")
for a in copilot_build("read the invoice and enter it in the ERP"):
    print(f"      {a}")
print()
print("UNATTENDED bots run lights-out (nightly batch); ATTENDED bots assist a person in real")
print("time (agent-assist). HUMAN-IN-THE-LOOP pauses for approval (refund > $500) surfaced in")
print("the flow by Automation CO-PILOT, which also helps DEVELOPERS build from natural language.")
print("AI accelerates both BUILDING and RUNNING — the AI Automation Engineer direction.")
EOF
```

**Expected result:** A router sending a nightly batch to unattended and agent-assist to attended, a refund that pauses for human approval over the threshold via Co-Pilot, and Co-Pilot drafting automation actions from a natural-language description. The lesson spans the deployment models (unattended lights-out, attended front-office), the human-in-the-loop pattern, and Automation Co-Pilot as the AI layer that assists both developers (build from language) and business users (approve in the flow) — the substance of the Advanced and AI Automation Engineer certifications.

**Negative test:** Forcing a real-time agent-assist task into an unattended nightly batch. The agent gets no help during the call, and a refund needing judgment is auto-processed with no human check; matching the mode to the task and inserting a human-in-the-loop step is what makes the automation fit the work.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Attended vs unattended understood — front-office assistance versus back-office lights-out automation.
- [ ] Human-in-the-loop understood — bots do the mechanical work and pause for human judgment or approval.
- [ ] Automation Co-Pilot understood — AI assistance for developers (build from language) and business users (in the flow).
- [ ] The AI acceleration understood — AI speeds both building and running automation.

## See also

- [Chapter 04 — The Control Room](04-the-control-room.md) — where unattended runners are orchestrated.
- [Chapter 07 — Agentic Process Automation and AI Agent Studio](07-agentic-process-automation.md) — the deeper AI/agentic layer.
- [Chapter 06 — Document Automation](06-document-automation.md) — the AI that reads the documents these processes handle.
