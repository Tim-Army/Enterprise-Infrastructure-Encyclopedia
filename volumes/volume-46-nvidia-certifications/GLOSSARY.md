# Volume XLVI Glossary

Definitions for terms used in **Volume XLVI — NVIDIA Certification Tracks**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Base Command Manager (BCM)** — NVIDIA's cluster provisioning and management tool
for consistent, image-based GPU-cluster deployment. Used in Chapter 05.

**BlueField DPU** — A data processing unit that offloads networking, storage, and
security from the host CPU. Used in Chapter 07.

**CUDA** — NVIDIA's parallel-computing platform and libraries; the base of the GPU
software stack. Used in Chapters 01 and 02.

**DCGM (Data Center GPU Manager)** — NVIDIA's GPU health, diagnostics, and
telemetry tool, exported to Prometheus/Grafana at fleet scale. Used in Chapters 02
and 06.

**DLI (Deep Learning Institute)** — NVIDIA's training organization for
certification preparation. Used throughout.

**GPUDirect RDMA** — Direct NIC-to-GPU-memory transfers that bypass the CPU for
low-latency GPU-to-GPU communication across nodes. Used in Chapter 07.

**InfiniBand** — A low-latency, RDMA fabric widely used to connect GPU nodes for
distributed training. Used in Chapters 05 and 07.

**MIG (Multi-Instance GPU)** — Hardware partitioning of a GPU into isolated
instances for multi-tenant density. Used in Chapters 02 and 06.

**NCCL** — NVIDIA's collective-communication library (all-reduce, all-gather) that
distributed training uses over the fabric. Used in Chapters 05 and 07.

**NeMo** — NVIDIA's framework for building and customizing LLMs and generative
models. Used in Chapters 03 and 08.

**NGC** — NVIDIA's catalog of validated containers, models, and Helm charts. Used
in Chapter 02.

**NIM** — NVIDIA Inference Microservices: prebuilt, optimized model-serving
containers with an OpenAI-compatible API. Used in Chapters 03 and 08.

**OpenUSD** — Universal Scene Description; a composable 3D scene-graph standard
used in Omniverse and digital twins (NCP-OUSD). Used in Chapter 08.

**RAPIDS** — NVIDIA's GPU data-science suite: cuDF (dataframes), cuML (ML), and
cuGraph (graph analytics). Used in Chapter 04.

**Spectrum-X** — NVIDIA's Ethernet-for-AI (RoCE with congestion control), an
alternative to InfiniBand. Used in Chapter 07.

**TensorRT-LLM** — NVIDIA's library for optimizing LLM inference (kernel fusion,
quantization). Used in Chapter 08.

**Xid error** — A GPU error code (in the kernel log) indicating a GPU fault;
repeated Xid or uncorrectable ECC warrants draining the node. Used in Chapter 06.
