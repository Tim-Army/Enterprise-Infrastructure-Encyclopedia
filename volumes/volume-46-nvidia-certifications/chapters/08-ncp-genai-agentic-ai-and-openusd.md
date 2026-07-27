# Chapter 08: NCP — Generative AI, Agentic AI, and OpenUSD

## Learning Objectives

- Explain the professional development credentials: NCP-GENL, NCP-AAI, and NCP-OUSD.
- Describe advanced LLM development, agentic AI, and OpenUSD.
- Apply NeMo customization, agent orchestration, and USD scene concepts.
- Understand safety and evaluation for generative and agentic systems.
- Complete a per-topic walkthrough for each professional development area.

## Theory and Architecture

Three professional credentials cover advanced AI **development** on NVIDIA:

- **NCP-GENL (Generative AI LLMs)** — advanced LLM development: customizing models
  with **NeMo** (fine-tuning, PEFT/LoRA), production **RAG**, **guardrails**, and
  deployment/optimization with **NIM** and **TensorRT-LLM**.
- **NCP-AAI (Agentic AI)** — building **AI agents**: tool/function calling,
  planning and orchestration, **multi-agent** systems, memory, and agent safety.
- **NCP-OUSD (OpenUSD Development)** — **OpenUSD** (Universal Scene Description)
  development in **Omniverse**: USD data model, scene composition, and digital
  twins/simulation.

Each is a **2-hour, $200** professional exam.

## Design Considerations

**NCP-GENL** deepens the GENL associate into production LLM engineering.
**NCP-AAI** is the newest frontier — agents that **use tools and act**, where
orchestration and **safety** (bounded permissions, human oversight) matter most.
**NCP-OUSD** is a distinct discipline (3D/simulation) for Omniverse and digital
twins. Choose by the systems you build.

## Implementation and Automation

The labs below use portable Python and NVIDIA-tooling concepts — NeMo/NIM/
TensorRT-LLM for GENL, agent/tool-calling patterns for AAI, and USD composition
for OUSD.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
nvidia.com/learn/certification > NCP-GENL / NCP-AAI / NCP-OUSD:
  - GENL: NeMo customization, production RAG, guardrails, NIM/TensorRT-LLM
  - AAI: agents, tool calling, orchestration, multi-agent, safety
  - OUSD: OpenUSD data model, composition, Omniverse, digital twins
  - 2 hours, $200 each, professional
```

Common pitfalls: giving agents **unbounded tool permissions** (a safety failure);
confusing **RAG** with fine-tuning at scale; and treating USD like a static file
format (it is a **composable** scene graph).

## Security and Best Practices

For LLMs: customize with the cheapest sufficient method (RAG/LoRA before full
fine-tune), add **guardrails** (NeMo Guardrails), and evaluate groundedness. For
agents: **least-privilege tools**, human approval for high-impact actions, bounded
autonomy, and observability of agent actions. For OpenUSD: use **composition
arcs** (references/layers) for scalable, non-destructive scenes.

## References and Knowledge Checks

- nvidia.com/learn/certification: NCP-GENL, NCP-AAI, NCP-OUSD blueprints; NeMo, NIM, TensorRT-LLM, and OpenUSD/Omniverse documentation.

**Knowledge checks**

1. What does NeMo add for production LLM development?
2. Why is least-privilege tooling essential for AI agents?
3. What makes OpenUSD composable rather than a flat file?

## Hands-On Lab

Per-topic walkthroughs — GENL, AAI, and OUSD. Concepts run without a GPU.

**Shared prerequisites** — a shell with `python3`. **Cost:** none.

### NCP-GENL — Generative AI LLMs (Professional)

### Lab 8.1 — GENL: NeMo customization pipeline

**Objective:** Outline a production LLM customization pipeline.

```bash
python3 - <<'PY'
steps = ["Curate data (NeMo Curator: dedup, filter, quality)",
         "Customize: PEFT/LoRA or full fine-tune (NeMo)",
         "Align: SFT + preference tuning",
         "Deploy: export to NIM / TensorRT-LLM for optimized inference",
         "Evaluate + guardrail (NeMo Guardrails)"]
for i,s in enumerate(steps,1): print(f"{i}. {s}")
PY
```

**Expected result:** the NeMo customization-to-deployment pipeline — the
production LLM engineering NCP-GENL certifies.

**Negative test:** fine-tune on raw, unfiltered data; **data curation** drives
quality — curate first.

**Cleanup:** none.

### Lab 8.2 — GENL: production RAG and optimization

**Objective:** Describe scaling and optimizing inference.

```bash
python3 - <<'PY'
print("Production RAG: managed vector store, chunking strategy, reranking, caching.")
print("Optimize inference: TensorRT-LLM (kernel fusion, quantization), NIM autoscaling, batching.")
PY
```

**Expected result:** production RAG and inference optimization (TensorRT-LLM, NIM)
— the scaling side of NCP-GENL.

**Negative test:** serve an unoptimized model at scale; **TensorRT-LLM/NIM**
cut latency and cost — optimize for production.

**Cleanup:** none.

### NCP-AAI — Agentic AI (Professional)

### Lab 8.3 — AAI: tool/function calling

**Objective:** Define an agent tool with a schema.

```bash
python3 - <<'PY'
tool = {"name":"get_ticket_status",
        "description":"Look up a support ticket by id",
        "parameters":{"ticket_id":"string"},
        "permission":"read-only"}
for k,v in tool.items(): print(f"{k:12}: {v}")
print("The model calls the tool with structured args; the runtime executes and returns results.")
PY
```

**Expected result:** a tool definition (schema + least-privilege permission) — the
tool-calling foundation of NCP-AAI.

**Negative test:** expose a broad `run_shell` tool to an agent; grant **narrow,
least-privilege** tools only.

**Cleanup:** none.

### Lab 8.4 — AAI: planning and orchestration

**Objective:** Outline an agent's plan-act-observe loop.

```bash
python3 - <<'PY'
loop = ["Plan: decompose the goal into steps",
        "Act: call a tool for the current step",
        "Observe: read the result",
        "Reflect: adjust the plan; repeat until done or hand off"]
for s in loop: print("-", s)
PY
```

**Expected result:** the plan→act→observe→reflect agent loop — the orchestration
NCP-AAI tests.

**Negative test:** let an agent loop without a **termination/budget** condition; it
can run away — bound steps and cost.

**Cleanup:** none.

### Lab 8.5 — AAI: multi-agent and safety

**Objective:** Design a bounded multi-agent system with safety.

```bash
python3 - <<'PY'
print("Multi-agent: specialized agents (planner, researcher, executor) coordinated by an orchestrator.")
print("Safety: least-privilege tools, human approval for high-impact actions, output validation,")
print("        action logging/observability, and hard limits on autonomy.")
PY
```

**Expected result:** a multi-agent design with safety controls — the agentic-AI
safety NCP-AAI emphasizes.

**Negative test:** deploy autonomous agents that take irreversible actions without
approval; gate **high-impact** actions behind humans.

**Cleanup:** none.

### NCP-OUSD — OpenUSD Development (Professional)

### Lab 8.6 — OUSD: the OpenUSD data model

**Objective:** Read the USD scene-graph concepts.

```bash
python3 - <<'PY'
print("USD: a composable scene graph of Prims (objects) with Attributes and Relationships.")
print("Stage: the composed scene; Layers: files composited via composition arcs.")
PY
```

**Expected result:** the USD data model (prims, attributes, stage, layers) — the
foundation of NCP-OUSD.

**Negative test:** treat a `.usd` file as a flat mesh export; USD is a
**composable** scene graph — model with prims and layers.

**Cleanup:** none.

### Lab 8.7 — OUSD: composition and digital twins

**Objective:** Compose a scene non-destructively and describe digital twins.

```bash
python3 - <<'PY'
print("Composition arcs: references, payloads, sublayers, variants -> non-destructive assembly.")
print("Digital twin (Omniverse): USD scene + physics + live data -> simulate/operate a real system.")
PY
```

**Expected result:** composition arcs and the digital-twin use — the OpenUSD
development NCP-OUSD certifies.

**Negative test:** edit a referenced asset in place for one scene; use **variants/
overrides** so the base asset stays reusable — compose non-destructively.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Three professional development credentials extend the frontier: **NCP-GENL**
(production LLM engineering with NeMo/NIM/TensorRT-LLM), **NCP-AAI** (agentic AI —
tools, orchestration, multi-agent, and safety), and **NCP-OUSD** (OpenUSD
development and digital twins in Omniverse). Each is a two-hour professional exam.

- [ ] I can outline a NeMo LLM customization and optimization pipeline.
- [ ] I can define least-privilege agent tools and a plan-act loop.
- [ ] I can design a bounded, safe multi-agent system.
- [ ] I can explain the OpenUSD data model and composition.
- [ ] I completed Labs 8.1–8.7 including each negative test.
