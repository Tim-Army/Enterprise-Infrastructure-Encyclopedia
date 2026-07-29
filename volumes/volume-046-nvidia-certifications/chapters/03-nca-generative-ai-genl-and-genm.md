# Chapter 03: NCA — Generative AI (NCA-GENL and NCA-GENM)

## Learning Objectives

- Explain the Generative AI associate credentials: NCA-GENL (LLMs) and NCA-GENM (Multimodal).
- Summarize the blueprint areas for each.
- Apply LLM concepts: prompting, RAG, fine-tuning, and evaluation with NVIDIA tooling.
- Understand multimodal generative AI (vision + language, diffusion).
- Complete a per-topic walkthrough for each Generative AI area.

## Theory and Architecture

Two associate credentials cover generative AI foundations on NVIDIA:

- **NCA-GENL (Generative AI LLM)** — foundational knowledge for developing,
  integrating, and maintaining **LLM**-driven applications: LLM fundamentals,
  **prompt engineering**, **retrieval-augmented generation (RAG)**, fine-tuning
  concepts, evaluation, and responsible AI — using NVIDIA tooling (**NeMo**,
  **NIM**, **NGC**).
- **NCA-GENM (Generative AI Multimodal)** — the foundational skills to design and
  manage **multimodal** AI systems that combine **text, image, audio, and video**
  (vision-language models, **diffusion** image generation, multimodal data
  preparation).

Both are **50-question, 60-minute** associate exams ($125).

## Design Considerations

**NCA-GENL** suits developers building LLM applications; **NCA-GENM** extends to
multimodal systems. Learn the generative-AI workflow — data → model (pretrained/
fine-tuned) → deployment (NIM) → evaluation — and NVIDIA's role at each step
(NeMo for building/customizing, NIM for serving, NGC for models). For multimodal,
add the vision/diffusion concepts and multimodal data handling.

## Implementation and Automation

The labs below use portable Python and NVIDIA-tooling concepts to make each area
concrete — LLM prompting, RAG, fine-tuning approach, NIM serving, evaluation, and
multimodal concepts (no GPU required to study the concepts).

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
nvidia.com/learn/certification > NCA-GENL / NCA-GENM:
  - GENL: LLM fundamentals, prompting, RAG, fine-tuning, evaluation, responsible AI
  - GENM: multimodal (vision-language, diffusion), multimodal data
  - 50 questions / 60 minutes, associate level
```

Common pitfalls: confusing **fine-tuning** with **RAG** (RAG retrieves at
inference; fine-tuning changes weights); and treating multimodal as "just add
images" (it needs aligned, multimodal data and models).

## Security and Best Practices

Prefer **RAG** for knowledge freshness/citations and **fine-tuning** (or PEFT/
LoRA) for behavior/format; ground generation to reduce hallucination; evaluate
with task-appropriate metrics and human review; apply **responsible-AI** guardrails
(NeMo Guardrails); and serve with **NIM** for optimized, secure inference.

## References and Knowledge Checks

- nvidia.com/learn/certification: NCA-GENL and NCA-GENM blueprints; NeMo, NIM, and NGC documentation.

**Knowledge checks**

1. What is the difference between RAG and fine-tuning?
2. What do NeMo and NIM do in the generative-AI workflow?
3. What makes a system "multimodal," and what data does it need?

## Hands-On Lab

Per-topic walkthroughs — LLM areas (GENL) and multimodal areas (GENM). Concepts
run without a GPU.

**Shared prerequisites** — a shell with `python3`. **Cost:** none.

### Lab 3.1 — GENL: LLM fundamentals and prompting

**Objective:** Structure a prompt with role, context, and constraints.

```bash
python3 - <<'PY'
prompt = {"system":"You are a precise assistant. Answer only from the context.",
          "context":"<retrieved docs>","user":"Summarize the SLA in 2 bullets",
          "constraints":"cite sources; say 'unknown' if not in context"}
for k,v in prompt.items(): print(f"{k:11}: {v}")
PY
```

**Expected result:** a structured prompt (system/context/user/constraints) — the
prompt-engineering foundation NCA-GENL tests.

**Negative test:** ask an open question with no context or constraints; you invite
hallucination — ground and constrain the prompt.

**Cleanup:** none.

### Lab 3.2 — GENL: retrieval-augmented generation (RAG)

**Objective:** Outline the RAG pipeline.

```bash
python3 - <<'PY'
steps = ["Embed documents -> vector store","Embed the query","Retrieve top-k relevant chunks",
         "Augment the prompt with retrieved context","Generate grounded answer with citations"]
for i,s in enumerate(steps,1): print(f"{i}. {s}")
PY
```

**Expected result:** the RAG pipeline (embed → retrieve → augment → generate) —
the grounding technique central to GENL.

**Negative test:** fine-tune a model to memorize changing facts; **RAG** keeps
knowledge fresh and citable without retraining — use it for knowledge.

**Cleanup:** none.

### Lab 3.3 — GENL: fine-tuning approaches

**Objective:** Choose a customization approach.

```bash
python3 - <<'PY'
approaches = {"Prompting/RAG":"no weight change; fast; knowledge + light behavior",
              "PEFT/LoRA":"adapt a few parameters; efficient behavior/format tuning",
              "Full fine-tune":"update all weights; costly; deep behavior change"}
for k,v in approaches.items(): print(f"{k:16}: {v}")
PY
```

**Expected result:** the customization spectrum (prompt/RAG → PEFT/LoRA → full
fine-tune) — the fine-tuning concepts GENL covers (NeMo enables these).

**Negative test:** full fine-tune for a small format change; **LoRA/PEFT** is far
cheaper — match the method to the need.

**Cleanup:** none.

### Lab 3.4 — GENL: serving with NIM and evaluation

**Objective:** Describe serving and evaluating an LLM app.

```bash
python3 - <<'PY'
print("Serve: NVIDIA NIM = prebuilt, optimized inference microservice (OpenAI-compatible API).")
print("Evaluate: task metrics (accuracy/exact-match), groundedness, latency/throughput, human review.")
PY
```

**Expected result:** NIM serving and an evaluation approach — the deploy-and-evaluate
steps of GENL.

**Negative test:** ship an LLM app with no evaluation; measure **groundedness and
task metrics** before and after changes.

**Cleanup:** none.

### Lab 3.5 — GENM: multimodal models and data

**Objective:** Describe a vision-language multimodal pipeline.

```bash
python3 - <<'PY'
print("Multimodal: encode each modality (image encoder + text encoder) into a shared space.")
print("Tasks: image captioning, VQA (visual question answering), text-to-image.")
print("Data: aligned pairs (image+caption); quality/alignment drives results.")
PY
```

**Expected result:** the multimodal architecture (shared embedding space) and
tasks — the foundation of NCA-GENM.

**Negative test:** train multimodal on unaligned data; **aligned** multimodal
pairs are required — data alignment is critical.

**Cleanup:** none.

### Lab 3.6 — GENM: diffusion and generation

**Objective:** Explain diffusion-based image generation.

```bash
python3 - <<'PY'
print("Diffusion: start from noise, iteratively denoise toward an image conditioned on a prompt.")
print("Control: guidance scale, steps, seeds; NVIDIA optimizes inference (TensorRT).")
PY
```

**Expected result:** the diffusion generation concept (iterative denoising,
conditioning) — a GENM topic.

**Negative test:** expect deterministic output without fixing the **seed**;
generation is stochastic — set the seed for reproducibility.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Generative AI associates cover LLMs (**NCA-GENL** — prompting, RAG,
fine-tuning, NIM serving, evaluation) and multimodal AI (**NCA-GENM** —
vision-language models, diffusion, multimodal data), both using NVIDIA's NeMo/NIM/
NGC tooling. They are the generative-AI foundation before the professional GenAI
credentials.

- [ ] I can summarize the GENL and GENM blueprint areas.
- [ ] I can structure a prompt and outline a RAG pipeline.
- [ ] I can choose a fine-tuning approach and describe NIM serving.
- [ ] I can explain multimodal models and diffusion generation.
- [ ] I completed Labs 3.1–3.6 including each negative test.
