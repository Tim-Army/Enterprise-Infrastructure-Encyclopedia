# Chapter 07: NCP — AI Networking (NCP-AIN)

## Learning Objectives

- Explain what NCP-AIN certifies and why AI networking is distinct.
- Describe the AI-networking fabric: InfiniBand, Spectrum-X, RDMA, and NCCL.
- Apply topology, congestion-control, and GPUDirect concepts.
- Understand the DPU (BlueField) role in AI fabrics.
- Complete a per-topic walkthrough for each NCP-AIN area.

## Theory and Architecture

The **NVIDIA-Certified Professional: AI Networking (NCP-AIN)** validates the
design and operation of the **high-performance networks** that connect GPU nodes
for distributed training and inference — where the network, not the GPU, is often
the bottleneck. It is a **2-hour, $400** professional exam. Its blueprint centers
on:

- **InfiniBand** — the low-latency, RDMA fabric for AI clusters (subnet manager,
  fat-tree topology, adaptive routing).
- **Spectrum-X** — NVIDIA's Ethernet-for-AI (RoCE with congestion control) as an
  alternative to InfiniBand.
- **RDMA / GPUDirect** — direct GPU-to-GPU/network memory access bypassing the CPU.
- **NCCL** — the collective-communication library training uses over the fabric.
- **BlueField DPUs** — offload networking/security/storage from the host.

## Design Considerations

AI networking is distinct because **collective operations** (all-reduce) at scale
demand full, non-blocking bandwidth and ultra-low latency. Learn **InfiniBand**
(subnet manager, fat-tree, adaptive routing) and **Spectrum-X** (RoCE + congestion
control), how **RDMA/GPUDirect** removes CPU/memory copies, how **NCCL** maps
collectives to the topology, and where **BlueField DPUs** offload. This pairs with
the encyclopedia's networking volumes at the AI-fabric frontier.

## Implementation and Automation

The labs below use InfiniBand tooling (`ibstat`, `ibnetdiscover`) and NCCL/topology
concepts (real commands on an IB host; concepts otherwise).

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nvidia.com/learn/certification > NCP-AIN:
  - InfiniBand, Spectrum-X (RoCE), RDMA/GPUDirect, NCCL, BlueField DPUs
  - 2 hours, $400, professional
```

Common pitfalls: designing AI fabric like a general LAN (it needs **non-blocking**
fat-tree and low latency); ignoring **congestion control** on RoCE/Ethernet; and
forgetting the **subnet manager** on InfiniBand.

## Security and Best Practices

Design **non-blocking fat-tree** topologies sized to collective bandwidth; run a
**subnet manager** on InfiniBand; enable **congestion control** and lossless
config on **Spectrum-X/RoCE**; use **RDMA/GPUDirect** to bypass the CPU; and
validate with **NCCL** bandwidth tests. Offload with **BlueField DPUs** where
appropriate.

## References and Knowledge Checks

- nvidia.com/learn/certification: NCP-AIN blueprint; InfiniBand, Spectrum-X, DOCA/BlueField, and NCCL documentation.

**Knowledge checks**

1. Why does AI training demand a non-blocking, low-latency fabric?
2. What is the difference between InfiniBand and Spectrum-X?
3. What do RDMA/GPUDirect and NCCL each provide?

## Hands-On Lab

Per-topic walkthroughs — IB tooling and fabric concepts. Commands run on an
InfiniBand host; concepts apply anywhere.

**Shared prerequisites** — a shell; an InfiniBand host for `ibstat`/`ibnetdiscover`
where available; `python3`. **Cost:** none.

### Lab 7.1 — InfiniBand fabric basics

**Objective:** Inspect InfiniBand link state and rate.

```bash
ibstat 2>/dev/null | grep -E 'State|Rate|Physical' | head \
  || echo "(ibstat shows port state/rate; ibnetdiscover maps the fabric)"
```

**Expected result:** IB port state (Active) and rate (e.g., NDR 400 Gb/s) — the
fabric health NCP-AIN starts from.

**Negative test:** assume a link is fine because it is up; check **rate** and
errors — a downgraded link throttles training.

**Cleanup:** none.

### Lab 7.2 — Topology: non-blocking fat-tree

**Objective:** Reason about AI-cluster topology.

```bash
python3 - <<'PY'
print("Fat-tree (Clos): full bisection bandwidth so any-to-any GPU comms don't bottleneck.")
print("Rails: each GPU maps to a NIC/rail; rail-optimized topology speeds all-reduce.")
PY
```

**Expected result:** the fat-tree/rail-optimized design — the topology NCP-AIN
requires for scalable collectives.

**Negative test:** oversubscribe the fabric to save cost; **all-reduce** needs full
bisection bandwidth — under-provisioning throttles training.

**Cleanup:** none.

### Lab 7.3 — Spectrum-X (Ethernet for AI)

**Objective:** Contrast Spectrum-X/RoCE with InfiniBand.

```bash
python3 - <<'PY'
print("Spectrum-X: Ethernet for AI = RoCE + adaptive routing + congestion control (lossless).")
print("Choose IB for lowest latency/largest scale; Spectrum-X to leverage Ethernet operations.")
PY
```

**Expected result:** the Spectrum-X (RoCE) alternative and when to choose it — a
core NCP-AIN comparison.

**Negative test:** run RoCE without **congestion control/lossless** config;
Ethernet AI fabric needs it to avoid drops — configure it.

**Cleanup:** none.

### Lab 7.4 — RDMA and GPUDirect

**Objective:** Explain CPU-bypass data movement.

```bash
python3 - <<'PY'
print("RDMA: NIC reads/writes remote memory directly (no CPU copy).")
print("GPUDirect RDMA: NIC <-> GPU memory directly -> lowest-latency GPU-to-GPU across nodes.")
PY
```

**Expected result:** RDMA and GPUDirect RDMA (CPU/GPU-memory bypass) — the
data-path efficiency NCP-AIN tests.

**Negative test:** route GPU-to-GPU traffic through host memory; **GPUDirect**
avoids that copy — enable it for performance.

**Cleanup:** none.

### Lab 7.5 — NCCL over the fabric

**Objective:** Validate collective bandwidth with NCCL.

```bash
echo "all_reduce_perf -b 8 -e 8G -f 2 -g 8   # NCCL test across 8 GPUs"
python3 - <<'PY'
print("NCCL maps collectives (all-reduce/all-gather) to topology; test measures busbw (GB/s).")
print("Low busbw vs line rate -> topology/config problem, not the GPUs.")
PY
```

**Expected result:** the NCCL bandwidth test and how to read busbw — the
fabric-validation skill NCP-AIN requires.

**Negative test:** benchmark single-GPU FLOPS and assume the cluster scales;
**NCCL busbw** reveals the network's real collective throughput — test it.

**Cleanup:** none.

### Lab 7.6 — BlueField DPUs

**Objective:** Describe DPU offload in AI fabrics.

```bash
python3 - <<'PY'
print("BlueField DPU: offloads networking, storage, and security from the host CPU.")
print("In AI fabric: accelerates/isolates east-west traffic, enables zero-trust + multi-tenancy.")
PY
```

**Expected result:** the DPU offload role — the BlueField topic in NCP-AIN.

**Negative test:** assume the host CPU handles all network/security at line rate;
**DPUs** offload it, freeing the CPU and adding isolation.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NCP-AIN is NVIDIA's AI-networking professional credential: a two-hour exam
covering InfiniBand, Spectrum-X (RoCE), RDMA/GPUDirect, NCCL, and BlueField DPUs —
the high-performance fabric that keeps distributed training from bottlenecking on
the network. It complements the AI-infrastructure and operations credentials.

- [ ] I can inspect InfiniBand and reason about fat-tree topology.
- [ ] I can contrast InfiniBand with Spectrum-X/RoCE.
- [ ] I can explain RDMA/GPUDirect and validate NCCL bandwidth.
- [ ] I can describe the BlueField DPU role.
- [ ] I completed Labs 7.1–7.6 including each negative test.
