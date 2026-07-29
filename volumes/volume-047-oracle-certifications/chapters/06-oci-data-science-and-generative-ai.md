# Chapter 06: OCI Data Science and Generative AI

## Learning Objectives

- Explain the OCI Data Science and Generative AI Professional credentials.
- Summarize their exam topics.
- Apply the ML lifecycle on OCI Data Science (notebooks, models, deployment, MLOps).
- Apply OCI Generative AI: prompting, fine-tuning, RAG, vector search, and agents.
- Complete a per-topic walkthrough for each area.

## Theory and Architecture

Two professional credentials cover AI on OCI:

- **OCI Data Science Professional (1Z0-1110)** — the **ML lifecycle** on the **OCI
  Data Science** service: JupyterLab notebook sessions, the **Accelerated Data
  Science (ADS) SDK**, the **model catalog**, **model deployment** as HTTP
  endpoints, jobs, pipelines, and **MLOps**.
- **OCI Generative AI Professional (1Z0-1127)** — building with the **OCI
  Generative AI** service: LLM fundamentals, **prompt engineering**, **model
  customization** (fine-tuning, **T-Few**), **retrieval-augmented generation
  (RAG)** with **vector search** (Oracle Database 23ai **AI Vector Search**), and
  **OCI GenAI Agents**.

Both are year-versioned (e.g., **1Z0-1127-26**).

## Design Considerations

**Data Science** is about the end-to-end ML workflow on OCI (build → train →
catalog → deploy → monitor), using the **ADS SDK**. **Generative AI** is about
applying LLMs with OCI's managed service — choosing prompting vs fine-tuning vs
RAG, grounding with **vector search** (23ai), and orchestrating **agents**. The
GenAI credential pairs with the encyclopedia's other GenAI material (NVIDIA XLVI,
Azure/Microsoft AI).

## Implementation and Automation

The labs below use the OCI Data Science/ADS and Generative AI service patterns
(and 23ai vector SQL) to cover the ML lifecycle and the GenAI workflow.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
education.oracle.com > OCI Data Science (1Z0-1110) / Generative AI Professional (1Z0-1127):
  - Data Science: notebooks, ADS SDK, model catalog/deployment, jobs/pipelines, MLOps
  - Generative AI: LLMs, prompting, fine-tuning (T-Few), RAG + vector search, agents
```

Common pitfalls: confusing **fine-tuning** with **RAG** (RAG retrieves at
inference); not versioning models in the **model catalog**; and building RAG
without a **vector store** (23ai AI Vector Search).

## Security and Best Practices

Track experiments and version models in the **model catalog**; deploy behind
managed **endpoints** with monitoring (MLOps); for GenAI, prefer **RAG** for
grounded, current answers and **fine-tuning/T-Few** for behavior; store embeddings
in **23ai AI Vector Search**; and constrain **agents** with least-privilege tools.

## References and Knowledge Checks

- education.oracle.com: OCI Data Science and Generative AI exam topics; OCI Data Science, ADS SDK, OCI Generative AI, and Database 23ai AI Vector Search docs.

**Knowledge checks**

1. What does the OCI Data Science model catalog provide?
2. When do you choose fine-tuning vs RAG on OCI Generative AI?
3. What does Oracle Database 23ai AI Vector Search enable for RAG?

## Hands-On Lab

Per-topic walkthroughs — Data Science and Generative AI areas.

**Shared prerequisites** — a shell with `python3`; an OCI account (Data Science /
Generative AI) and Oracle Database 23ai for execution. **Cost:** none (free tiers
where available).

### Lab 6.1 — Data Science: notebooks and the ADS SDK

**Objective:** Describe the OCI Data Science working environment.

```python
# In an OCI Data Science notebook session:
import ads
ads.set_auth("resource_principal")     # authenticate via resource principal
# ADS provides dataset loading, AutoML, model catalog, and deployment helpers
```

**Expected result:** the ADS SDK entry point (resource-principal auth) — the OCI
Data Science environment the exam covers.

**Negative test:** hard-code API keys in a notebook; use **resource principals** so
the notebook authenticates without stored keys.

**Cleanup:** none.

### Lab 6.2 — Data Science: model catalog and deployment

**Objective:** Catalog and deploy a model.

```python
# Save to the model catalog, then deploy as an HTTPS endpoint
model_id = model.save(display_name="fraud-v1")     # versioned artifact
deployment = model.deploy(display_name="fraud-endpoint")  # managed endpoint
```

**Expected result:** a versioned model in the catalog and a managed deployment —
the model-management lifecycle of the Data Science credential.

**Negative test:** copy model files to an instance and serve by hand; the **model
catalog + deployment** provides versioning, scaling, and monitoring — use them.

**Cleanup:** none.

### Lab 6.3 — Data Science: jobs, pipelines, and MLOps

**Objective:** Automate training with jobs/pipelines.

```python
# ML Jobs run repeatable training; Pipelines orchestrate multi-step ML workflows (MLOps)
# Job: containerized training run; Pipeline: data-prep -> train -> evaluate -> register
```

**Expected result:** the jobs/pipelines/MLOps concept — the automation area of the
Data Science credential.

**Negative test:** train interactively in a notebook for production; use **Jobs/
Pipelines** for repeatable, automated MLOps.

**Cleanup:** none.

### Lab 6.4 — Generative AI: prompting and the OCI GenAI service

**Objective:** Call the OCI Generative AI service with a structured prompt.

```python
# OCI Generative AI: managed LLMs (chat, embeddings) via SDK/API
# Structured prompt: system role + context + task + constraints -> grounded output
```

**Expected result:** the OCI GenAI service invocation with a structured prompt —
the prompting foundation of 1Z0-1127.

**Negative test:** send an open prompt with no constraints; ground and constrain to
reduce hallucination.

**Cleanup:** none.

### Lab 6.5 — Generative AI: model customization (fine-tuning / T-Few)

**Objective:** Choose a customization method.

```python
# Prompting/RAG: no weight change. T-Few: parameter-efficient fine-tuning (few examples).
# Full fine-tune: deeper behavior change, more data/cost. Choose the cheapest sufficient method.
```

**Expected result:** the customization spectrum including **T-Few** (OCI's
parameter-efficient fine-tuning) — a core 1Z0-1127 topic.

**Negative test:** full fine-tune for a small tweak; **T-Few** is cheaper — match
the method to the need.

**Cleanup:** none.

### Lab 6.6 — Generative AI: RAG with 23ai AI Vector Search

**Objective:** Ground answers with vector search in Oracle Database 23ai.

```sql
-- Oracle Database 23ai AI Vector Search: store + query embeddings natively
CREATE TABLE docs (id NUMBER, chunk CLOB, embedding VECTOR);
SELECT id, chunk
FROM docs
ORDER BY VECTOR_DISTANCE(embedding, :query_vec, COSINE)
FETCH FIRST 5 ROWS ONLY;   -- retrieve top-5 for RAG
```

**Expected result:** a native vector similarity query in 23ai returning the top-k
chunks — the RAG + vector-search topic of 1Z0-1127 (and a 23ai feature).

**Negative test:** bolt on a separate vector DB when **23ai AI Vector Search** is
native; keep embeddings with the data where it fits.

**Cleanup:** `DROP TABLE docs;`

### Lab 6.7 — Generative AI: OCI GenAI Agents

**Objective:** Describe an OCI GenAI Agent with tools.

```python
# OCI GenAI Agents: LLM + tools + a knowledge base (RAG) to take grounded actions.
# Constrain tools to least privilege; add human approval for high-impact actions.
```

**Expected result:** the agent model (LLM + tools + knowledge base) with safety —
the agents topic of 1Z0-1127.

**Negative test:** give an agent broad, unapproved tool access; use **least
privilege** and approval gates for high-impact actions.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The OCI Data Science Professional certifies the ML lifecycle on OCI (notebooks,
ADS SDK, model catalog/deployment, jobs/pipelines, MLOps), and the OCI Generative
AI Professional certifies building with LLMs (prompting, T-Few fine-tuning, RAG
with 23ai AI Vector Search, and GenAI Agents). Together they cover OCI's AI
development stack.

- [ ] I can describe the OCI Data Science lifecycle and ADS SDK.
- [ ] I can catalog, deploy, and automate models (MLOps).
- [ ] I can choose prompting vs T-Few vs RAG on OCI GenAI.
- [ ] I can run a 23ai vector search and describe GenAI Agents.
- [ ] I completed Labs 6.1–6.7 including each negative test.
