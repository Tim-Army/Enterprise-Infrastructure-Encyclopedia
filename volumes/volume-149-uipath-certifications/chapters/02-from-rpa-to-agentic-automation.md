# Chapter 02: From RPA to Agentic Automation

## Learning Objectives

- Explain what RPA is and the kind of work it automates.
- Understand the limits of deterministic automation.
- Describe agentic automation — AI agents that reason and act.
- Place robots, agents, and humans as the three collaborators.

*Cert relevance: the RPA-to-agentic shift is the theme of the modern program — the Agentic Automation certifications assume you understand it.*

## What RPA is

**Robotic Process Automation (RPA)** is software **robots** that automate repetitive, rule-based tasks by operating applications *the way a person does* — clicking buttons, reading fields, copying data between systems. A robot logs into the ERP, reads an invoice, types the line items into the accounting system, and moves the file — the same steps, the same way, every time, without tiring or erring.

The defining property of RPA is that it is **deterministic**: it follows explicit rules on structured, predictable inputs. Given the same input, it does exactly the same thing. This is enormously valuable for the vast amount of enterprise work that is high-volume and rule-based — and it is also RPA's boundary.

## The limit of determinism

Deterministic robots break on **ambiguity and judgment**. A robot that processes invoices in one exact format fails when a new vendor sends a differently-laid-out invoice; a robot that follows fixed rules cannot decide what to do with an exception it was not programmed for. Classic RPA needs the world to be **structured and predictable**, and the real world often is not — so pure-RPA automations are brittle at exactly the edges where human judgment used to fill the gap.

Historically, those edges were handled by **routing to a human** (the [human-in-the-loop](#robots-agents-and-humans) pattern). That works, but it caps how much a process can be automated: every judgment call is a handoff. The question the industry asked was: *what if the automation itself could handle judgment?*

## Agentic automation

**Agentic automation** is the answer: adding **AI agents** — powered by large language models — that **reason, decide, and act** on ambiguous inputs, rather than following fixed rules. Where a robot *executes a known procedure*, an agent *figures out what to do*. An agent can read an oddly-formatted invoice it has never seen, understand it, and decide how to handle it; it can triage an exception a deterministic robot would have kicked to a human.

Crucially, agentic automation does not *replace* robots — it **combines** them:

| Collaborator | Strength | Best for |
|:---|:---|:---|
| **Robots** | Deterministic, reliable, fast | High-volume, rule-based, structured steps |
| **AI agents** | Reasoning, flexible, handle ambiguity | Judgment, unstructured input, exceptions |
| **Humans** | Accountability, oversight, edge cases | Approval, governance, the truly novel |

The art is **using each for what it is good at**: robots for the deterministic bulk, agents for the judgment, humans for oversight and accountability. This is why UiPath's agentic certifications emphasize *orchestrating* and *governing* agents alongside robots and people — not just building agents. The lab models the division of labor.

## Robots, agents, and humans

The modern automation is an **orchestration** of all three. A loan application might be: a **robot** pulls the documents and data (deterministic), an **agent** reads the unstructured supporting letters and assesses completeness (judgment), a **human** approves the final decision (accountability), and a **robot** files the result (deterministic). Each does what it is best at, and the orchestrator (UiPath) routes the work between them. The lab models composing such a process.

## Hands-On Lab

Python models the RPA-to-agentic division of labor. **Cost:** none.

### Lab 2.1 — Deterministic robot versus reasoning agent

**Objective:** See where a rule-based robot breaks and an agent is needed.

```bash
python3 - <<'EOF'
# invoices arriving in varied formats; a deterministic robot only handles the known one
INVOICES = [
  # id,      format,            structured
  ("INV-1",  "standard-template", True),
  ("INV-2",  "standard-template", True),
  ("INV-3",  "new-vendor-layout", False),   # never seen -> robot fails
  ("INV-4",  "scanned-handwritten", False),  # unstructured -> robot fails
  ("INV-5",  "standard-template", True),
]
print("Processing invoices.\n")
print("DETERMINISTIC ROBOT (rules for the standard template only):")
robot_done, kicked = [], []
for iid, fmt, structured in INVOICES:
    if fmt == "standard-template":
        robot_done.append(iid)
    else:
        kicked.append((iid, fmt))
print(f"   handled: {robot_done}")
print(f"   FAILED (unknown format) -> kicked to a human: {[i for i,_ in kicked]}")
print(f"   automation rate: {len(robot_done)}/{len(INVOICES)} = {100*len(robot_done)//len(INVOICES)}%")
print("   the robot is reliable on what it KNOWS, brittle on anything new.\n")

print("AGENTIC (AI agent handles the ambiguous ones the robot couldn't):")
agent_done = [i for i, _ in kicked]   # the agent reasons over unfamiliar layouts
print(f"   robot handles the {len(robot_done)} structured (fast, deterministic, cheap)")
print(f"   AGENT reads the {len(agent_done)} unfamiliar/unstructured ones by REASONING")
print(f"      (understands a new layout it's never seen, extracts the fields)")
print(f"   automation rate: {len(robot_done)+len(agent_done)}/{len(INVOICES)} = 100%")
print("   humans now handle only true exceptions, not every unfamiliar format.")
print("\nThe shift: deterministic RPA caps out where the inputs stop being predictable")
print("— every new format is a human handoff. An AI AGENT handles judgment and")
print("ambiguity, lifting the automation ceiling. But you don't replace the robot with")
print("an agent: the robot still does the high-volume structured bulk (cheaper, more")
print("reliable), and the agent handles the edges. Use each for its strength.")
EOF
```

**Expected result:** A deterministic robot handling only the known invoice format and kicking unfamiliar ones to humans, while an AI agent reasons over the unstructured cases to lift automation toward 100%. The RPA-to-agentic lesson is that deterministic automation caps out where inputs stop being predictable, and AI agents handle the judgment and ambiguity — complementing robots, not replacing them.

**Negative test:** Expecting a rule-based robot to handle any invoice format. It breaks on the first unfamiliar layout and kicks it to a human; handling ambiguity needs a reasoning agent, which is the agentic addition.

**Cleanup:** None.

### Lab 2.2 — Orchestrate robots, agents, and humans

**Objective:** Compose a process using each collaborator for its strength.

```bash
python3 - <<'EOF'
# a loan-application process; assign each step to the right collaborator
STEPS = [
  # step,                              best_collaborator, why
  ("pull documents & data from systems","robot",  "deterministic, high-volume, structured"),
  ("read unstructured support letters", "agent",  "ambiguity/judgment — reason over free text"),
  ("assess application completeness",   "agent",  "judgment on messy inputs"),
  ("approve/deny the loan",             "human",  "accountability — a person owns this decision"),
  ("file the outcome in the systems",   "robot",  "deterministic, rule-based"),
  ("handle a truly novel edge case",    "human",  "the genuinely new"),
]
from collections import Counter
print("Loan application — orchestrating robots + agents + humans:\n")
print(f"   {'step':38}{'->':4}assigned")
counts = Counter()
for step, who, why in STEPS:
    counts[who] += 1
    print(f"   {step:38}{'->':4}{who.upper():7} ({why})")
print(f"\n   division of labor: {dict(counts)}")
print("\nThe orchestration principle: ONE process, THREE collaborators, each on the")
print("steps it's best at:")
print("  ROBOTS do the deterministic bulk (pull data, file results) — fast + reliable")
print("  AGENTS do the judgment (read free text, assess completeness) — flexible")
print("  HUMANS own accountability (approve the loan, handle the truly novel)")
print("\nThis is what UiPath's AGENTIC certifications are really about — not just")
print("building an agent, but ORCHESTRATING and GOVERNING the mix: routing each step")
print("to robot, agent, or human, and keeping humans accountable for the decisions")
print("that matter. The platform is the conductor; the certs teach you to conduct.")
EOF
```

**Expected result:** A loan process decomposed so robots do the deterministic steps, agents do the judgment steps, and humans own the accountable decisions and novel edge cases. The orchestration lesson is that modern automation composes all three collaborators — each on the steps it is best at — and the agentic certifications are about orchestrating and governing that mix, not just building agents.

**Negative test:** Handing every step to an AI agent because agents are flexible. Agents are slower, costlier, and less reliable than robots on high-volume deterministic steps, and they cannot own accountable decisions — the value is the right collaborator per step, not agents everywhere.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] RPA understood as deterministic robots automating repetitive, rule-based, structured work.
- [ ] The limit of determinism recognized — brittleness on ambiguity, judgment, and unstructured input.
- [ ] Agentic automation understood as AI agents that reason and act, complementing (not replacing) robots.
- [ ] Robots, agents, and humans placed as three collaborators orchestrated per their strengths.
