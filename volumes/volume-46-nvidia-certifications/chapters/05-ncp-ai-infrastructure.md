# Chapter 05: NCP — AI Infrastructure (NCP-AII)

## Learning Objectives

- Explain what NCP-AII certifies and its hands-on emphasis.
- Summarize the blueprint: hardware deployment, Slurm, Kubernetes GPU Operator, and Base Command Manager.
- Apply GPU-cluster deployment, configuration, and validation concepts.
- Understand the software stack that turns GPUs into a usable cluster.
- Complete a per-topic walkthrough for each NCP-AII area.

## Theory and Architecture

The **NVIDIA-Certified Professional: AI Infrastructure (NCP-AII)** validates the
ability to **deploy, configure, and validate advanced NVIDIA AI infrastructure** —
the hands-on work of standing up GPU clusters. It is a **2-hour, $400** exam and
assumes **1–3 years** of operational experience. Its blueprint centers on:

- **Hardware deployment** — DGX/HGX systems, GPUs, and **InfiniBand** fabric.
- **Cluster software** — **Slurm** workload manager, **Kubernetes** with the
  **NVIDIA GPU Operator**, and **Base Command Manager (BCM)** for provisioning.
- **Validation** — health checks, burn-in, firmware, and driver/CUDA
  compatibility.

## Design Considerations

NCP-AII is a **builder's** exam — it assumes you can rack, cable, provision, and
validate a GPU cluster. Master the **provisioning** path (BCM), both
**schedulers** (Slurm for batch training, Kubernetes + GPU Operator for
services), the **driver/toolkit** installation the GPU Operator automates, and
**validation** (DCGM diagnostics, NCCL tests, firmware). Prepare with hands-on
cluster work; reading is not enough.

## Implementation and Automation

The labs below use the real cluster tooling (Slurm, Kubernetes GPU Operator,
`nvidia-smi`/DCGM) as commands and configuration you can adapt on a GPU cluster.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nvidia.com/learn/certification > NCP-AII:
  - hardware deployment (DGX/HGX, InfiniBand), Slurm, Kubernetes GPU Operator, BCM, validation
  - 2 hours, $400, professional (1-3 years experience recommended)
```

Common pitfalls: mismatched **driver/CUDA/firmware** versions; deploying GPU pods
without the **GPU Operator**; and skipping **validation** (NCCL/DCGM) before
handing a cluster to users.

## Security and Best Practices

Provision consistently with **BCM**; install the GPU stack via the **GPU
Operator** (driver, toolkit, DCGM) rather than by hand; **validate** with DCGM
diagnostics and **NCCL** bandwidth tests before go-live; keep firmware and drivers
compatible; and document the cluster's topology and versions.

## References and Knowledge Checks

- nvidia.com/learn/certification: NCP-AII blueprint; DGX, Base Command Manager, GPU Operator, and DCGM documentation.

**Knowledge checks**

1. When do you choose Slurm vs Kubernetes for a GPU cluster?
2. What does the NVIDIA GPU Operator install and manage?
3. How do you validate a new GPU cluster before go-live?

## Hands-On Lab

Per-topic walkthroughs — cluster deployment/validation. Commands are real Slurm/
Kubernetes/NVIDIA tooling (adapt to a GPU cluster).

**Shared prerequisites** — a shell; a GPU cluster (or single GPU host) for
execution; `python3`. **Cost:** none (concepts run without hardware).

### Lab 5.1 — Hardware deployment and topology

**Objective:** Read GPU topology and interconnect.

```bash
nvidia-smi topo -m 2>/dev/null | head \
  || echo "(topo -m shows NVLink/PCIe/NUMA paths between GPUs and NICs)"
echo "InfiniBand: ibstat / ibnetdiscover map the fabric for distributed training."
```

**Expected result:** the GPU interconnect matrix (NVLink/PCIe) and IB tools — the
hardware/topology awareness NCP-AII requires.

**Negative test:** ignore topology and pin unrelated GPUs across NUMA/PCIe for one
job; place co-working GPUs on **NVLink** for bandwidth.

**Cleanup:** none.

### Lab 5.2 — Provisioning with Base Command Manager

**Objective:** Describe consistent cluster provisioning.

```bash
python3 - <<'PY'
print("BCM: image-based provisioning of head + compute nodes; manages images, roles, and the stack.")
print("Ensures every node has matching driver/CUDA/toolkit -> consistent, reproducible cluster.")
PY
```

**Expected result:** the BCM provisioning model (consistent images/roles) — the
provisioning area of NCP-AII.

**Negative test:** hand-configure each node; drift causes hard-to-debug failures —
**provision from images** with BCM.

**Cleanup:** none.

### Lab 5.3 — Kubernetes GPU Operator

**Objective:** Expose GPUs to Kubernetes via the GPU Operator.

```bash
kubectl get pods -n gpu-operator 2>/dev/null | head \
  || echo "(GPU Operator installs driver, container toolkit, device plugin, DCGM)"
cat <<'YAML'
resources:
  limits:
    nvidia.com/gpu: 1     # a pod requests a GPU once the Operator is installed
YAML
```

**Expected result:** the GPU Operator components and a pod GPU request — the
Kubernetes GPU enablement NCP-AII tests.

**Negative test:** request `nvidia.com/gpu` with no GPU Operator/device plugin;
Kubernetes cannot schedule it — install the Operator first.

**Cleanup:** none.

### Lab 5.4 — Slurm for batch training

**Objective:** Submit a GPU batch job with Slurm.

```bash
cat <<'SBATCH'
#!/bin/bash
#SBATCH --job-name=train
#SBATCH --gres=gpu:8          # request 8 GPUs
#SBATCH --nodes=2
srun python train.py
SBATCH
echo "sbatch job.slurm ; squeue -u $USER ; sacct for accounting"
```

**Expected result:** a Slurm batch script requesting GPUs across nodes — the HPC
scheduling path NCP-AII covers.

**Negative test:** run large multi-node training interactively; use **Slurm**
(`sbatch`, `gres=gpu`) for reproducible, scheduled batch jobs.

**Cleanup:** none.

### Lab 5.5 — Validation: DCGM diagnostics and NCCL

**Objective:** Validate GPU health and inter-GPU bandwidth.

```bash
dcgmi diag -r 2 2>/dev/null || echo "(dcgmi diag runs GPU health diagnostics)"
echo "NCCL tests (all_reduce_perf) validate inter-GPU/inter-node bandwidth before go-live."
```

**Expected result:** DCGM diagnostics and NCCL bandwidth validation — the
pre-go-live validation NCP-AII requires.

**Negative test:** hand a cluster to users without **DCGM/NCCL** validation;
silent GPU/fabric faults ruin training — validate first.

**Cleanup:** none.

### Lab 5.6 — Driver, firmware, and compatibility

**Objective:** Verify the stack is compatible.

```bash
nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null || echo "(driver version)"
echo "Check the compatibility matrix: GPU firmware <-> driver <-> CUDA <-> framework."
```

**Expected result:** the driver version and the compatibility-matrix concept — the
version discipline NCP-AII enforces.

**Negative test:** upgrade CUDA without checking the **driver** minimum; mismatched
versions break workloads — follow the compatibility matrix.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NCP-AII is NVIDIA's hands-on AI-infrastructure professional credential: a two-hour
exam (1–3 years experience) covering hardware deployment (DGX/HGX, InfiniBand),
provisioning (Base Command Manager), both schedulers (Slurm, Kubernetes GPU
Operator), and validation (DCGM, NCCL). It certifies the ability to stand up and
validate GPU clusters.

- [ ] I can read GPU topology and describe InfiniBand fabric.
- [ ] I can provision with BCM and enable GPUs in Kubernetes.
- [ ] I can submit Slurm GPU jobs and choose the right scheduler.
- [ ] I can validate a cluster with DCGM and NCCL.
- [ ] I completed Labs 5.1–5.6 including each negative test.
