# Volume XLVI — NVIDIA Certification Tracks

> The whole NVIDIA-Certified program in one volume — the Associate (NCA) and
> Professional (NCP) credentials across AI infrastructure, operations, networking,
> accelerated data science, and generative/agentic AI — with hands-on labs mapped
> to every exam-blueprint area, verified against nvidia.com.

## Overview

Volume XLVI maps the **NVIDIA** certification program — the credentials for
building, operating, and developing on **AI infrastructure**. As AI moves to the
center of enterprise infrastructure, these credentials validate the GPU, network,
and software skills behind it, placing this volume at the AI-infrastructure
frontier alongside the encyclopedia's cloud, automation, and networking volumes
(and complementing the Dell/NVIDIA and Nutanix co-skilled material).

This is a **certification-tracks** volume, like CompTIA (XXXIX), ISC2 (XL),
CNCF/Kubernetes (XLI), HashiCorp (XLII), OffSec (XLIII), ISACA (XLIV), and Splunk
(XLV): it maps the program — which credentials exist, their **blueprint areas**,
levels, and delivery — and teaches each with a hands-on walkthrough. Every
credential was **verified against nvidia.com on 26 July 2026**, which matters
because the program expanded fast: the Professional (NCP) tier now spans AI
infrastructure, operations, **networking**, data science, generative AI, **agentic
AI**, and **OpenUSD**, and the Associate tier added **Multimodal** generative AI.

Chapters are organized by credential:

- **Chapter 01** frames the program — levels, blueprints, DLI, and the GPU stack.
- **Chapters 02–04** take the Associate tier: AI Infrastructure and Operations,
  Generative AI (LLM and Multimodal), and Accelerated Data Science.
- **Chapters 05–07** take the Professional infrastructure tier: AI Infrastructure,
  AI Operations, and AI Networking.
- **Chapter 08** takes the Professional development tier: Generative AI, Agentic
  AI, and OpenUSD.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic
hands-on labs and knowledge checks.

## Chapters

1. [The NVIDIA Certification Program](chapters/01-the-nvidia-certification-program.md) — levels, blueprints, DLI, and the AI-infrastructure stack.
2. [NCA — AI Infrastructure and Operations (NCA-AIIO)](chapters/02-nca-ai-infrastructure-and-operations.md) — the foundational AI-infra breadth credential.
3. [NCA — Generative AI (NCA-GENL and NCA-GENM)](chapters/03-nca-generative-ai-genl-and-genm.md) — LLM and multimodal generative AI foundations.
4. [Accelerated Data Science (NCA-ADS and NCP-ADS)](chapters/04-accelerated-data-science-nca-ads-and-ncp-ads.md) — RAPIDS-based GPU data science.
5. [NCP — AI Infrastructure (NCP-AII)](chapters/05-ncp-ai-infrastructure.md) — deploying and validating GPU clusters.
6. [NCP — AI Operations (NCP-AIO)](chapters/06-ncp-ai-operations.md) — monitoring, troubleshooting, and optimizing AI infrastructure.
7. [NCP — AI Networking (NCP-AIN)](chapters/07-ncp-ai-networking.md) — InfiniBand, Spectrum-X, RDMA/GPUDirect, and NCCL.
8. [NCP — Generative AI, Agentic AI, and OpenUSD](chapters/08-ncp-genai-agentic-ai-and-openusd.md) — advanced LLM development, AI agents, and OpenUSD.
9. [Keeping the NVIDIA Program Current and Career Paths](chapters/09-keeping-the-nvidia-program-current-and-career-paths.md) — renewal, the expanding program, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for NVIDIA, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with levels, blueprint areas, prices, delivery, and DLI training is in the
[NVIDIA certification appendix](../volume-997-master-appendices/chapters/20-appendix-nvidia-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the containers/platform
(VIII), automation (IX), observability (XI), and cloud volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every
exam-blueprint area** of each NVIDIA credential — roughly **48 topic-area labs**
across the program — plus the program and currency labs in Chapters 01 and 09.
Because NVIDIA credentials are hands-on AI-infrastructure skills, the walkthroughs
use the real tooling — **`nvidia-smi`**, **DCGM**, **Slurm**, the **Kubernetes GPU
Operator**, **RAPIDS** (cuDF/cuML/cuGraph), **InfiniBand** utilities, and
NeMo/NIM/agent patterns — as commands to run on a GPU host or cloud GPU instance
(with the concepts studyable without a GPU). Each lab states an objective,
commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **nvidia.com/learn/certification** (catalog and blueprints),
the **NVIDIA Deep Learning Institute (DLI)**, **CUDA**, **DCGM**, **RAPIDS**,
**NeMo/NIM/TensorRT-LLM**, **InfiniBand/Spectrum-X**, **Base Command Manager**, and
**Pearson VUE** delivery. Credentials and blueprints were verified against
nvidia.com on 26 July 2026; NVIDIA updates and expands the program frequently, so
confirm the current blueprint before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-46-nvidia-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
