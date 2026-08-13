# Chapter 07: Generative AI Engineer and Context Engineer

## Learning Objectives

- Explain the new Generative AI Engineer and Context Engineer Associate credentials.
- Summarize their exam-guide sections.
- Apply GenAI on Databricks: RAG, vector search, Mosaic AI, evaluation, and deployment.
- Design context for AI agent systems.
- Complete a per-topic walkthrough for each area.

## Theory and Architecture

Two recent credentials cover generative and agentic AI on Databricks:

- **Generative AI Engineer Associate** — designing, building, and deploying GenAI
  applications: **RAG** with **Mosaic AI Vector Search**, model selection and
  **Foundation Model APIs**, prompt engineering, **evaluation** (Mosaic AI Agent
  Evaluation / MLflow LLM evaluate), **governance and guardrails**, and deployment
  via **Model Serving** — much of it through the **Mosaic AI Agent Framework**.
- **Context Engineer Associate** — designing the **context** that AI agent systems
  operate on: context assembly and retrieval, tool/function design, memory, and
  grounding, so agents act reliably and safely.

Both reflect the platform's move toward **agentic AI** on governed data.

## Design Considerations

The GenAI Engineer builds **RAG and agent** applications end to end — chunk and
embed data, store vectors (**Mosaic AI Vector Search**), retrieve and augment,
generate with a chosen model, **evaluate** rigorously, and deploy behind **Model
Serving** with guardrails and governance (Unity Catalog). The Context Engineer
focuses on **what the model sees** — assembling the right context, tools, and
memory for agents. Both center on grounding, evaluation, and safety.

## Implementation and Automation

The labs below use Databricks GenAI patterns — vector search, RAG, Foundation Model
APIs, agent tools, evaluation, and serving — as code/config you can adapt on the
platform.

## Validation and Troubleshooting

Confirm the exam guides before studying:

```text
databricks.com/learn/certification > Generative AI Engineer / Context Engineer Associate:
  - GenAI: RAG, Vector Search, model selection, prompting, evaluation, governance, deployment
  - Context Engineer: context assembly/retrieval, tools, memory for agent systems
```

Common pitfalls: fine-tuning when **RAG** fits (RAG grounds with current data);
skipping **evaluation** of GenAI outputs; and giving agents **unbounded tools**.

## Security and Best Practices

Ground with **RAG + Vector Search** for current, citable answers; **evaluate**
groundedness/quality (Agent Evaluation / MLflow) before and after changes; add
**guardrails** and govern data/models with **Unity Catalog**; deploy behind
**Model Serving**; and for agents, use **least-privilege tools** with human
approval for high-impact actions.

## References and Knowledge Checks

- databricks.com: Generative AI Engineer and Context Engineer exam guides; Mosaic AI (Vector Search, Agent Framework, Model Serving) docs.

**Knowledge checks**

1. When do you choose RAG versus fine-tuning on Databricks?
2. What does Mosaic AI Vector Search provide for RAG?
3. What does a Context Engineer design for an agent system?

## Hands-On Lab

Per-topic walkthroughs — GenAI Engineer and Context Engineer areas. Adapt on a
Databricks workspace.

**Shared prerequisites** — a Databricks workspace with Mosaic AI; `python3`.
**Cost:** none (Free Edition where available).

### Lab 7.1 — GenAI: chunk and embed for RAG

**Objective:** Prepare documents for retrieval.

```python
# Chunk documents, embed with a Foundation Model API embeddings model,
# and write embeddings to a Delta table for Vector Search sync.
# chunk -> embed -> store {id, text, embedding} in Delta
```

**Expected result:** a chunk→embed→store pipeline feeding Vector Search — the RAG
preparation the GenAI exam tests.

**Negative test:** embed whole documents without chunking; retrieval quality drops
— chunk to retrievable units.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — GenAI: Mosaic AI Vector Search retrieval

**Objective:** Create a vector index and retrieve top-k.

```python
# Create a Vector Search index over the embeddings Delta table (auto-synced),
# then query: index.similarity_search(query_text, num_results=5)
```

**Expected result:** top-5 relevant chunks from the vector index — the retrieval
half of RAG on Databricks.

**Negative test:** keyword-search a plain table for semantic queries; **Vector
Search** does semantic retrieval — use it for RAG.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — GenAI: model selection and Foundation Model APIs

**Objective:** Call a foundation model for generation.

```python
# Foundation Model APIs (pay-per-token or provisioned throughput):
# client.predict(endpoint="databricks-<model>", inputs={"messages":[...]})
# Choose model by quality/latency/cost; keep the prompt grounded in retrieved context.
```

**Expected result:** a grounded generation via a Foundation Model API — the
model-selection/generation area of the exam.

**Negative test:** pick the largest model regardless of latency/cost; select by
**quality/latency/cost** for the use case.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — GenAI: evaluation

**Objective:** Evaluate a RAG/agent output.

```python
import mlflow
# mlflow.evaluate(..., model_type="databricks-agent")  # Mosaic AI Agent Evaluation
# Metrics: groundedness, relevance, correctness, safety; use a labeled eval set + judges.
```

**Expected result:** an evaluation over an eval set (groundedness/relevance/safety)
— the evaluation discipline the GenAI exam emphasizes.

**Negative test:** ship without evaluation; **measure** groundedness/quality before
and after changes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.5 — GenAI: deploy with Model Serving + governance

**Objective:** Serve a GenAI app with guardrails.

```python
# Log the RAG chain/agent as an MLflow model -> deploy to Model Serving endpoint.
# Govern data/models with Unity Catalog; add guardrails; log to inference tables.
```

**Expected result:** a served, governed GenAI app with guardrails and logging —
the deployment/governance area of the exam.

**Negative test:** expose an ungoverned model on raw data; govern with **Unity
Catalog** and add guardrails.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.6 — Context Engineer: assemble agent context

**Objective:** Design the context an agent receives.

```python
context = {
  "system": "You are a support agent. Use only the provided context and tools.",
  "retrieved": "<top-k RAG chunks>",
  "tools": ["lookup_order(id)", "create_ticket(subject, body)"],
  "memory": "<relevant conversation history>",
}
# Context engineering = choosing what the model sees to act reliably.
```

**Expected result:** a structured agent context (instructions + retrieval + tools +
memory) — the core of the Context Engineer credential.

**Negative test:** stuff everything into the prompt; curate **relevant** context —
too much dilutes and raises cost/risk.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.7 — Context Engineer: tools and memory for agents

**Objective:** Define least-privilege tools and bounded memory.

```python
# Tool: least-privilege, typed, side-effect-aware (read vs write; approval for writes).
# Memory: short-term (conversation) + long-term (retrieved facts); bound size + relevance.
```

**Expected result:** least-privilege tools and bounded memory — the reliable/safe
agent design a Context Engineer produces.

**Negative test:** give an agent a broad write tool with no approval; gate
**high-impact** actions and scope tools.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Generative AI Engineer builds RAG/agent applications on Databricks (Vector
Search, Foundation Model APIs, evaluation, Model Serving, governance), and the
Context Engineer designs the context — retrieval, tools, and memory — that agent
systems act on. Both center on grounding, evaluation, and safety, reflecting the
platform's agentic-AI direction.

- [ ] I can summarize the GenAI Engineer and Context Engineer exam areas.
- [ ] I can build a RAG pipeline with Vector Search and Foundation Model APIs.
- [ ] I can evaluate and deploy a governed GenAI app.
- [ ] I can assemble agent context with least-privilege tools and bounded memory.
- [ ] I completed Labs 7.1–7.7 including each negative test.
