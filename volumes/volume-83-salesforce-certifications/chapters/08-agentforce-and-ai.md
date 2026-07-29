# Chapter 08: Agentforce and AI

## Learning Objectives

- Describe the AI Associate and Agentforce Specialist credentials.
- Ground AI agents in Salesforce data with Data Cloud.
- Apply prompt engineering for Salesforce.
- Build and operate Agentforce agents responsibly.
- Complete a walkthrough for each Agentforce/AI topic.

## Theory and Architecture

The **Agentforce** and **AI** credentials are Salesforce's newest and highest-demand — reflecting the
shift to **AI agents** on the platform. The **AI Associate** covers AI fundamentals and responsible-AI
concepts for Salesforce. The **Agentforce Specialist** (and AI Specialist) covers building,
**grounding**, and operating **Agentforce agents** — autonomous or assistive AI agents that take
actions in Salesforce (answering customer questions, updating records, executing flows). Agents are
made accurate and safe through **grounding** in trusted company data, primarily via **Data Cloud**
(Salesforce's data platform that unifies customer data across sources into a harmonized model the AI
can reference), and through **prompt engineering** — writing effective, guarded **prompt templates**
that instruct the model with context and constraints. **Einstein** provides the underlying AI
services. Because agents act on real data and take actions, **responsible AI** is central: guardrails,
data governance, human oversight, and testing. Understanding grounding, prompt design, Data Cloud, and
responsible operation is the core of these certifications. This chapter teaches each with a hands-on
walkthrough (grounding logic, prompt design, and responsible-agent operation).

> **Scope.** Agentforce agents act on your own org's data. Every lab is **authorized, responsible** AI
> configuration — grounded, guarded, and human-overseen.

## Design Considerations

**Ground** agents in trusted data (**Data Cloud** harmonized model) — never let them improvise facts.
Write **prompt templates** with clear context, instructions, and **guardrails**. Scope agent **actions**
and require confirmation for high-impact ones. Apply **responsible AI** (governance, oversight, testing,
bias awareness). Monitor agent behavior. Start assistive before autonomous.

## Implementation and Automation

The labs ground an agent, design a prompt, and operate an agent responsibly.

## Validation and Troubleshooting

Confirm the Agentforce/AI model:

```text
AI Associate = AI fundamentals + responsible AI. Agentforce Specialist = build/ground/operate agents. Grounding: Data Cloud (unified/harmonized customer data) so the agent references trusted facts. Prompt engineering: prompt templates with context + instructions + guardrails. Einstein = underlying AI.
Responsible AI: guardrails + governance + human oversight + testing throughout.
```

Common pitfalls: an **ungrounded** agent that hallucinates facts; and agents taking **high-impact
actions** with no confirmation/oversight.

## Security and Best Practices

**Ground** agents in Data Cloud, write **guarded prompt templates**, scope **actions** with oversight,
and apply **responsible AI** (governance, testing, human-in-the-loop). Monitor behavior. Start
assistive. All work is authorized and responsible.

## Hands-On Lab

Agentforce/AI walkthroughs. **Shared prerequisites** — `python3`, a free Dev org (Agentforce/Data Cloud
where available). **Cost:** none.

### Lab 8.1 — Ground an agent in Data Cloud

**Objective:** Reference trusted facts.

```python
python3 - <<'PY'
def answer(question, grounded_data):
    if question in grounded_data: return f"grounded answer: {grounded_data[question]}"
    return "I don't have that information (grounded agent won't invent it)"
data={"order status of 1001":"shipped, arriving Aug 3"}
print(answer("order status of 1001", data))
print(answer("order status of 9999", data))
print("Agentforce: ground in Data Cloud -> answers from trusted data, refuses to hallucinate")
PY
```

**Expected result:** the agent answers from **grounded data** and declines when it lacks facts —
grounded, accurate AI.

**Negative test:** let the agent answer without **grounding**; it may hallucinate an order status —
ground it in **Data Cloud**.

**Cleanup:** none.

### Lab 8.2 — Design a prompt template

**Objective:** Instruct the model safely.

```python
python3 - <<'PY'
prompt_template={"context":"{{Account.Name}}, {{Case.Subject}}, grounded knowledge articles",
                 "instruction":"Draft a helpful, concise reply using ONLY the provided data",
                 "guardrails":["do not invent policy","do not share other customers' data","escalate if unsure"]}
for k,v in prompt_template.items(): print(f"{k:12}: {v}")
print("Prompt engineering: context + instruction + guardrails -> safe, useful AI output")
PY
```

**Expected result:** a **prompt template** with context, instruction, and guardrails — effective,
guarded prompting.

**Negative test:** use a vague prompt with no **guardrails**; the model may overshare or invent —
constrain it.

**Cleanup:** none.

### Lab 8.3 — Scope agent actions with oversight

**Objective:** Keep agents safe.

```python
python3 - <<'PY'
actions={"answer a question":"autonomous (low risk)","update a case status":"autonomous (logged)",
         "issue a refund":"require human approval (high impact)","delete records":"deny (not an agent action)"}
for action,policy in actions.items(): print(f"{action:22}: {policy}")
print("Agentforce: scope actions by risk; high-impact actions need human approval")
PY
```

**Expected result:** agent actions **scoped by risk** with human approval for high impact — responsible
operation.

**Negative test:** let the agent **issue refunds** autonomously; a mistake costs money — require
**human approval**.

**Cleanup:** none.

### Lab 8.4 — Apply responsible AI

**Objective:** Govern AI on the platform.

```python
python3 - <<'PY'
checks={"grounding":"trusted Data Cloud sources","guardrails":"prompt constraints + toxicity filters",
        "oversight":"human review for high-impact","testing":"evaluate agent responses before rollout","governance":"data access + audit"}
for k,v in checks.items(): print(f"{k:11}: {v}")
print("Responsible AI: grounding + guardrails + oversight + testing + governance")
PY
```

**Expected result:** **responsible-AI** controls for agents — trustworthy platform AI.

**Negative test:** deploy an agent with no **testing or oversight**; errors reach customers — apply
responsible-AI controls.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Agentforce and AI credentials cover building, grounding, and operating AI agents — grounded in Data
Cloud, driven by guarded prompt templates, powered by Einstein, and governed by responsible-AI
practices with human oversight for high-impact actions.

- [ ] I can ground an agent in Data Cloud.
- [ ] I can design a prompt template.
- [ ] I can scope agent actions with oversight.
- [ ] I can apply responsible AI.
- [ ] I completed Labs 8.1–8.4 including each negative test.
