# Chapter 02: NCA — AI Infrastructure and Operations (NCA-AIIO)

## Learning Objectives

- Explain what NCA-AIIO certifies and its exam format.
- Summarize the blueprint areas: AI fundamentals, the NVIDIA stack, infrastructure, and operations.
- Apply GPU inspection, MIG, and orchestration concepts.
- Relate AI infrastructure and operations to the data center.
- Complete a per-topic walkthrough for each NCA-AIIO area.

## Theory and Architecture

The **NVIDIA-Certified Associate: AI Infrastructure and Operations (NCA-AIIO)**
validates **foundational** knowledge of AI computing — the concepts of AI, machine
learning, and deep learning; the **NVIDIA software and hardware stack**; the
**infrastructure** that runs AI (GPUs, DGX systems, data-center networking); and
the **operations** of AI environments (GPU management, monitoring, orchestration).
The exam is **50 questions in 60 minutes** ($125), online-proctored. Its blueprint
groups into these areas:

- **AI / ML / DL fundamentals** — what AI workloads are and how GPUs accelerate
  them.
- **NVIDIA AI software** — CUDA, frameworks, **NGC**, **NIM** microservices.
- **AI infrastructure** — GPUs, **DGX/HGX**, data-center networking (InfiniBand).
- **AI operations** — **MIG** partitioning, monitoring, and orchestration
  (Kubernetes GPU Operator / Slurm).

## Design Considerations

NCA-AIIO is the **breadth** credential — it covers the whole AI-infrastructure
picture at a foundational level and is the recommended entry point before the
Professional infra exams (NCP-AII/AIO/AIN). Learn the **stack layers**, the role
of each NVIDIA software component, and the operational concepts (MIG, monitoring,
scheduling) that the Professional exams then deepen.

## Implementation and Automation

The labs below use **`nvidia-smi`** and orchestration concepts (real commands on a
GPU host; concepts otherwise) to make each blueprint area concrete — GPU
inspection, MIG, monitoring, and orchestration.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nvidia.com/learn/certification > NCA-AIIO:
  - areas: AI/ML/DL fundamentals, NVIDIA AI software, AI infrastructure, AI operations
  - 50 questions / 60 minutes, associate level
```

Common pitfalls: confusing **CUDA** (the compute platform) with the **driver**;
assuming one GPU = one workload (MIG partitions a GPU); and treating AI ops as
generic ops (GPU scheduling and health differ).

## Security and Best Practices

Right-size GPUs to workloads (use **MIG** to partition large GPUs for many small
jobs), monitor **GPU health and utilization**, orchestrate with the **Kubernetes
GPU Operator** or **Slurm**, and keep the **driver/CUDA/container-toolkit** stack
compatible. Use **NGC** for validated containers and models.

## References and Knowledge Checks

- nvidia.com/learn/certification: NCA-AIIO blueprint; NVIDIA DLI; NGC catalog documentation.

**Knowledge checks**

1. What does MIG allow you to do with a GPU?
2. What is the role of NGC and NIM in the NVIDIA stack?
3. How does AI operations differ from generic IT operations?

## Hands-On Lab

Per-topic walkthroughs — **one lab per NCA-AIIO area**. `nvidia-smi` runs on a GPU
host; concepts apply anywhere.

**Shared prerequisites** — a shell; a GPU host (or cloud GPU instance) for
`nvidia-smi` where available; `python3`. **Cost:** none (concepts run without a
GPU).

### Lab 2.1 — AI/ML/DL fundamentals (why GPUs)

**Objective:** Reason about why AI workloads use GPUs.

```bash
python3 - <<'PY'
print("Training/inference = massive parallel matrix math (GEMM).")
print("GPUs: thousands of cores + high-bandwidth memory -> parallel throughput >> CPU.")
print("Precision: FP32/TF32/FP16/BF16/FP8 trade accuracy for speed/memory.")
PY
```

**Expected result:** why GPUs accelerate AI (parallel matrix math, precision
options) — the fundamentals NCA-AIIO tests.

**Negative test:** assume more CPU cores match a GPU for training; GPU parallelism
and memory bandwidth are the differentiator — use GPUs for AI math.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — NVIDIA AI software stack (CUDA, NGC, NIM)

**Objective:** Identify the software layers and their roles.

```bash
nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null || echo "(driver version on a GPU host)"
python3 - <<'PY'
layers = {"CUDA":"parallel compute platform/libraries",
          "cuDNN/NCCL":"DL primitives / multi-GPU communication",
          "NGC":"catalog of validated containers, models, Helm charts",
          "NIM":"prebuilt inference microservices for models"}
for k,v in layers.items(): print(f"{k:10}: {v}")
PY
```

**Expected result:** the NVIDIA software layers (CUDA, cuDNN/NCCL, NGC, NIM) —
the stack NCA-AIIO covers.

**Negative test:** pull random model containers from anywhere; **NGC** provides
validated, optimized images — prefer it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — AI infrastructure (DGX and networking)

**Objective:** Describe the AI data-center building blocks.

```bash
python3 - <<'PY'
print("DGX/HGX: integrated multi-GPU systems (NVLink between GPUs for fast GPU-GPU).")
print("Scale-out: InfiniBand / Spectrum-X networking connects nodes for distributed training.")
print("Storage: high-throughput parallel storage feeds GPUs to avoid starvation.")
PY
```

**Expected result:** the DGX/NVLink/InfiniBand/storage building blocks — the
AI-infrastructure area of NCA-AIIO.

**Negative test:** connect training nodes with ordinary Ethernet and expect linear
scaling; **InfiniBand/Spectrum-X** and NVLink are what make distributed training
scale.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — AI operations: MIG partitioning

**Objective:** Understand Multi-Instance GPU (MIG).

```bash
nvidia-smi mig -lgip 2>/dev/null || echo "(MIG: partition one GPU into isolated instances)"
python3 - <<'PY'
print("MIG splits a GPU (e.g., A100/H100) into up to 7 isolated instances.")
print("Use: pack many small inference/dev jobs onto one GPU with isolation.")
PY
```

**Expected result:** the MIG concept (partitioning a GPU into isolated instances)
— an AI-operations skill NCA-AIIO tests.

**Negative test:** give every small job a whole GPU; **MIG** improves utilization
by partitioning — use it for small workloads.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.5 — AI operations: monitoring and health

**Objective:** Monitor GPU utilization and health.

```bash
nvidia-smi --query-gpu=index,utilization.gpu,memory.used,temperature.gpu,power.draw \
  --format=csv 2>/dev/null || echo "(these metrics feed DCGM/Prometheus dashboards)"
echo "At scale: DCGM exporter -> Prometheus/Grafana for fleet GPU health."
```

**Expected result:** per-GPU utilization/memory/temp/power (or the concept) — the
monitoring signals AI operations tracks (via DCGM at scale).

**Negative test:** monitor only CPU/RAM on a GPU host; **GPU** utilization,
memory, and temperature are the signals that matter — monitor the GPUs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.6 — AI operations: orchestration

**Objective:** Describe GPU orchestration options.

```bash
python3 - <<'PY'
print("Kubernetes: NVIDIA GPU Operator installs drivers, toolkit, DCGM; pods request nvidia.com/gpu.")
print("Slurm: HPC scheduler for batch training jobs (gres=gpu).")
print("Choose K8s for services/inference, Slurm for large batch training.")
PY
```

**Expected result:** the two orchestration paths (Kubernetes GPU Operator vs
Slurm) and when to use each — the operations orchestration of NCA-AIIO.

**Negative test:** schedule GPU pods without the **GPU Operator/device plugin**;
Kubernetes needs it to expose and manage GPUs — install it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NCA-AIIO is NVIDIA's foundational AI-infrastructure-and-operations credential: a
50-question associate exam spanning AI/ML/DL fundamentals, the NVIDIA software
stack (CUDA, NGC, NIM), AI infrastructure (DGX, NVLink, InfiniBand), and AI
operations (MIG, monitoring, orchestration). It is the breadth entry point before
the Professional infrastructure exams.

- [ ] I can summarize the NCA-AIIO blueprint areas.
- [ ] I can explain why GPUs accelerate AI and name the software stack.
- [ ] I can describe DGX/NVLink/InfiniBand infrastructure.
- [ ] I can explain MIG, GPU monitoring, and orchestration.
- [ ] I completed Labs 2.1–2.6 including each negative test.
