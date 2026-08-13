# Chapter 01: The NVIDIA Certification Program

## Learning Objectives

- Explain what NVIDIA certifies and its place in the AI-infrastructure stack.
- Describe the credential map across the Associate and Professional levels.
- Explain the exam experience (Pearson VUE), exam blueprints, and DLI training.
- Understand the recent expansion of the program (AI networking, agentic AI, OpenUSD).
- Verify a current exam blueprint from the authoritative source.

## Theory and Architecture

**NVIDIA** certifies the skills to **build, operate, and develop on AI
infrastructure** — the GPUs, networking, and software that run modern AI. As AI
workloads move to the center of enterprise infrastructure, NVIDIA-Certified
credentials validate the ability to deploy and operate GPU clusters, accelerate
data science, and develop generative and agentic AI. This places the volume
alongside the encyclopedia's cloud, automation, and platform volumes at the
AI-infrastructure frontier (and it pairs with the Dell/NVIDIA and Nutanix
co-skilled solution material referenced in the Dell volume).

The program has two levels and has expanded rapidly:

- **Associate (NCA)** — foundational: **NCA-AIIO** (AI Infrastructure and
  Operations), **NCA-ADS** (Accelerated Data Science), **NCA-GENL** (Generative
  AI LLM), and **NCA-GENM** (Generative AI Multimodal).
- **Professional (NCP)** — advanced, experience-backed: **NCP-AII** (AI
  Infrastructure), **NCP-AIO** (AI Operations), **NCP-AIN** (AI Networking),
  **NCP-ADS** (Accelerated Data Science), **NCP-GENL** (Generative AI LLMs),
  **NCP-AAI** (Agentic AI), and **NCP-OUSD** (OpenUSD Development).

The **Agentic AI (NCP-AAI)** and **OpenUSD (NCP-OUSD)** professional credentials,
the **Multimodal (NCA-GENM)** associate, and **AI Networking (NCP-AIN)** are
recent additions — the program tracks the AI field closely.

## Design Considerations

Plan a path by **role**. Newcomers and generalists start at the **Associate**
level — **NCA-AIIO** for infrastructure/operations breadth, **NCA-GENL/GENM** for
generative AI, **NCA-ADS** for data science. Practitioners advance to the
**Professional** level for their specialty: **NCP-AII/AIO/AIN** for infrastructure,
operations, and networking (NVIDIA recommends 1–3 years of hands-on experience),
and **NCP-GENL/AAI/OUSD** for generative, agentic, and OpenUSD development. Because
the Professional infrastructure exams are deeply practical (Slurm, Kubernetes GPU
Operator, Base Command Manager), prepare with **hands-on** cluster work.

## Implementation and Automation

Every NVIDIA exam has a published **exam blueprint** with weighted sections — the
authoritative study scope. Confirm the current blueprint before studying, and use
the **NVIDIA Deep Learning Institute (DLI)** for training. Where GPUs are
available, the primary tool is **`nvidia-smi`**:

```bash
# Inspect GPUs, driver, and utilization (the AI-infra practitioner's first command)
nvidia-smi --query-gpu=name,driver_version,memory.total,utilization.gpu --format=csv 2>/dev/null \
  || echo "(no GPU here — concepts still apply; run on a GPU host/cloud instance)"
```

## Validation and Troubleshooting

Confirm a credential's blueprint, level, and mechanics:

```text
nvidia.com/learn/certification > open the certification:
  - the exam blueprint (weighted sections)
  - level (Associate NCA vs Professional NCP), duration, and price
  - recommended experience and DLI training
```

Common pitfalls: studying an **old program map** that misses the new NCP exams
(Agentic AI, OpenUSD, AI Networking, Multimodal); treating Professional infra
exams as theory (they assume **hands-on** cluster experience); and confusing the
GPU **driver/CUDA** stack layers.

## Security and Best Practices

Verify facts on **nvidia.com** and train with **DLI**. Practice on real GPUs
(a workstation, a DGX, or a cloud GPU instance) for the Professional exams.
Understand the full stack — **driver → CUDA → container runtime (NVIDIA Container
Toolkit) → orchestration (Kubernetes GPU Operator / Slurm) → frameworks (NeMo,
NIM, RAPIDS)** — since the exams span it.

## References and Knowledge Checks

- nvidia.com/learn/certification: the certification catalog and per-exam blueprints; NVIDIA Deep Learning Institute (DLI).

**Knowledge checks**

1. How do the NCA (Associate) and NCP (Professional) levels differ?
2. Which NVIDIA credentials are recent additions, and what do they cover?
3. What is the AI-infrastructure software stack from driver to frameworks?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and inspecting GPUs.

**Shared prerequisites for Labs 1.1–1.3** — a shell with `curl`; a GPU host (or
cloud GPU instance) for `nvidia-smi` where available. **Cost:** none (concepts run
without a GPU).

### Lab 1.1 — Enumerate the certification catalog (Topic: Read the program)

**Objective:** List the current certifications from the authoritative source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.nvidia.com/en-us/learn/certification/" \
  | grep -oiE 'NC[AP]-[A-Z]{3,4}' | sort -u
```

**Expected result:** the current exam codes — NCA-AIIO/ADS/GENL/GENM and
NCP-AII/AIO/AIN/ADS/GENL/AAI/OUSD — the whole program in one view.

**Negative test:** rely on an old list; it misses **NCP-AAI (Agentic AI)** and
**NCP-OUSD (OpenUSD)** — use the live catalog.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Inspect the GPU stack (Topic: AI-infra foundation)

**Objective:** Read the GPU and driver with `nvidia-smi`.

```bash
nvidia-smi 2>/dev/null | head -15 \
  || echo "(no GPU — on a GPU host this shows driver, CUDA, GPUs, and utilization)"
```

**Expected result (on a GPU host):** the driver/CUDA versions, GPU model, memory,
and utilization — the foundational inspection every NVIDIA infra role begins with.

**Negative test:** assume CUDA works without a matching **driver**; the driver and
CUDA versions must be compatible — check both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Map the AI-infrastructure stack (Topic: Understand the layers)

**Objective:** Lay out the stack the exams span.

```bash
python3 - <<'PY'
stack = ["GPU hardware (H100/H200/Blackwell)","NVIDIA driver","CUDA toolkit",
         "NVIDIA Container Toolkit","Orchestration: Kubernetes GPU Operator / Slurm",
         "Frameworks: NeMo, NIM microservices, RAPIDS, Triton"]
for i,l in enumerate(stack,1): print(f"{i}. {l}")
PY
```

**Expected result:** the layered AI-infrastructure stack from hardware to
frameworks — the map that organizes the whole NVIDIA program.

**Negative test:** study only frameworks; the Professional infra exams test the
**whole stack** (driver, container, orchestration) — learn each layer.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NVIDIA certifies AI-infrastructure, data-science, and generative/agentic AI skills
across two levels — Associate (NCA) and Professional (NCP) — with Pearson VUE
exams governed by published blueprints and DLI training. The program has expanded
fast, adding AI Networking, Agentic AI, OpenUSD, and Multimodal credentials.

- [ ] I can map the NCA and NCP credentials and their levels.
- [ ] I can name the recent additions to the program.
- [ ] I can inspect a GPU with `nvidia-smi` and describe the stack.
- [ ] I can find a current exam blueprint on nvidia.com.
- [ ] I completed Labs 1.1–1.3 including each negative test.
