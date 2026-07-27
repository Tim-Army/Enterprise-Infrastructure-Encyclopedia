# Chapter 06: NCP — AI Operations (NCP-AIO)

## Learning Objectives

- Explain what NCP-AIO certifies and how it differs from NCP-AII.
- Summarize the blueprint: monitoring, troubleshooting, and optimizing AI infrastructure.
- Apply GPU telemetry, performance tuning, and capacity optimization.
- Keep a GPU cluster healthy and efficient in production.
- Complete a per-topic walkthrough for each NCP-AIO area.

## Theory and Architecture

The **NVIDIA-Certified Professional: AI Operations (NCP-AIO)** validates the skills
to **monitor, troubleshoot, and optimize** NVIDIA AI infrastructure in production —
the run phase after NCP-AII's build phase. It is a **2-hour, $500** professional
exam. Its blueprint centers on:

- **Monitoring** — GPU telemetry with **DCGM**, exporting to Prometheus/Grafana,
  and alerting on health/utilization.
- **Troubleshooting** — diagnosing GPU, driver, fabric (NCCL/InfiniBand), and job
  failures.
- **Optimization** — utilization (MIG, time-slicing), performance tuning, and
  capacity management.

## Design Considerations

NCP-AIO is the **operator's** exam. Master **DCGM** (health, diagnostics, metrics
export), a systematic **troubleshooting** method for GPU/fabric/job issues, and
**optimization** levers (MIG vs time-slicing, right-sizing, scheduling policy).
It pairs with NCP-AII (build) and the observability skills in the encyclopedia's
Volume XI and the Splunk O11y material.

## Implementation and Automation

The labs below use **`nvidia-smi`** and **DCGM** (real commands on a GPU host;
concepts otherwise) for monitoring, troubleshooting, and optimization.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nvidia.com/learn/certification > NCP-AIO:
  - monitoring (DCGM), troubleshooting (GPU/driver/fabric/jobs), optimization (MIG, tuning)
  - 2 hours, $500, professional
```

Common pitfalls: monitoring only utilization (also watch **temperature, power,
ECC/Xid errors**); ignoring **NCCL/fabric** as a failure source; and leaving GPUs
under-utilized (MIG/time-slicing improve density).

## Security and Best Practices

Export **DCGM** metrics to Prometheus/Grafana and alert on health (Xid/ECC
errors, thermal, power) and utilization; triage systematically (job → GPU →
driver → fabric); optimize density with **MIG** (isolation) or **time-slicing**
(sharing) as appropriate; and plan capacity from utilization trends.

## References and Knowledge Checks

- nvidia.com/learn/certification: NCP-AIO blueprint; DCGM, GPU telemetry, and troubleshooting documentation.

**Knowledge checks**

1. What does DCGM provide for AI operations?
2. What is the difference between MIG and time-slicing for sharing GPUs?
3. What GPU signals beyond utilization must you monitor?

## Hands-On Lab

Per-topic walkthroughs — monitoring, troubleshooting, optimization. `nvidia-smi`/
DCGM run on a GPU host; concepts apply anywhere.

**Shared prerequisites** — a shell; a GPU host for `nvidia-smi`/`dcgmi` where
available; `python3`. **Cost:** none.

### Lab 6.1 — Monitoring: GPU telemetry with DCGM

**Objective:** Read the health/utilization signals operations tracks.

```bash
dcgmi dmon -e 203,252,155,150 2>/dev/null | head \
  || nvidia-smi --query-gpu=utilization.gpu,memory.used,temperature.gpu,power.draw,ecc.errors.uncorrected.aggregate.total --format=csv 2>/dev/null \
  || echo "(DCGM/nvidia-smi expose util, memory, temp, power, ECC/Xid errors)"
```

**Expected result:** GPU utilization, memory, temperature, power, and ECC signals
— the telemetry NCP-AIO monitors (DCGM exports these to Prometheus).

**Negative test:** watch only utilization; **thermal/power/ECC/Xid** errors
predict failures — monitor them too.

**Cleanup:** none.

### Lab 6.2 — Monitoring: fleet dashboards and alerting

**Objective:** Describe the fleet-monitoring pipeline.

```bash
python3 - <<'PY'
print("DCGM exporter -> Prometheus -> Grafana dashboards for the GPU fleet.")
print("Alert on: Xid errors, ECC uncorrectable, thermal throttling, GPU down, low utilization.")
PY
```

**Expected result:** the DCGM→Prometheus→Grafana pipeline and alert conditions —
fleet monitoring for AI operations.

**Negative test:** monitor node-by-node manually; a **fleet dashboard** with
alerts scales — centralize.

**Cleanup:** none.

### Lab 6.3 — Troubleshooting: a systematic method

**Objective:** Triage a failed GPU job.

```bash
python3 - <<'PY'
flow = ["Job: read logs/exit code (OOM? NCCL timeout?)",
        "GPU: nvidia-smi (util, ECC/Xid errors, fallen off bus?)",
        "Driver/toolkit: version compatibility + dmesg",
        "Fabric: NCCL test / ibstat for InfiniBand errors"]
for s in flow: print("-", s)
PY
```

**Expected result:** the job→GPU→driver→fabric triage order — the troubleshooting
method NCP-AIO tests.

**Negative test:** blame the model first; check **infrastructure** (GPU/driver/
fabric) systematically before assuming a code bug.

**Cleanup:** none.

### Lab 6.4 — Troubleshooting: Xid and ECC errors

**Objective:** Interpret GPU hardware error signals.

```bash
nvidia-smi -q -d ECC,ERROR 2>/dev/null | grep -iE 'Xid|ECC|Pending' | head \
  || echo "(Xid errors in dmesg + ECC counters indicate GPU faults)"
echo "Uncorrectable ECC / repeated Xid -> drain the node, RMA/replace the GPU."
```

**Expected result:** ECC/Xid error signals and the response (drain/replace) — the
hardware-fault troubleshooting of NCP-AIO.

**Negative test:** keep scheduling on a GPU with uncorrectable ECC/Xid errors; it
corrupts results — **drain** and remediate.

**Cleanup:** none.

### Lab 6.5 — Optimization: MIG vs time-slicing

**Objective:** Choose a GPU-sharing strategy.

```bash
python3 - <<'PY'
print("MIG: hardware-isolated partitions (predictable QoS) -> multi-tenant inference/dev.")
print("Time-slicing: software time-sharing (no isolation) -> bursty/dev workloads.")
print("Choose MIG for isolation/SLA; time-slicing for cheap sharing without isolation.")
PY
```

**Expected result:** the MIG-vs-time-slicing decision — the utilization
optimization NCP-AIO covers.

**Negative test:** time-slice a GPU across untrusted tenants expecting isolation;
only **MIG** isolates — use it for multi-tenant SLAs.

**Cleanup:** none.

### Lab 6.6 — Optimization: performance and capacity

**Objective:** Tune for throughput and plan capacity.

```bash
python3 - <<'PY'
print("Perf: batch size, mixed precision (FP16/FP8), NCCL topology, data pipeline (avoid GPU starvation).")
print("Capacity: trend utilization; if sustained >80% with queueing -> add GPUs; if <30% -> consolidate (MIG).")
PY
```

**Expected result:** performance levers and a capacity rule of thumb — the
optimization/capacity domain of NCP-AIO.

**Negative test:** add GPUs when utilization is low but throughput is poor; the
bottleneck may be the **data pipeline** — profile before scaling.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NCP-AIO is NVIDIA's AI-operations professional credential: a two-hour exam
covering monitoring (DCGM telemetry, fleet dashboards), troubleshooting (a
systematic job→GPU→driver→fabric method, Xid/ECC faults), and optimization (MIG
vs time-slicing, performance and capacity). It is the run-phase counterpart to
NCP-AII.

- [ ] I can read and alert on the full set of GPU health signals.
- [ ] I can triage a failed GPU job systematically.
- [ ] I can interpret Xid/ECC errors and respond.
- [ ] I can choose MIG vs time-slicing and tune for throughput.
- [ ] I completed Labs 6.1–6.6 including each negative test.
