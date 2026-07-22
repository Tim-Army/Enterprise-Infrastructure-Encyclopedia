# Chapter 07: Data Center AI Infrastructure

## Learning Objectives

- Explain what AI training and inference workloads demand from
  infrastructure, and why those demands broke general-purpose designs
- Describe AI cluster anatomy: GPU compute, the scale-out backend
  fabric, storage feeds, and the frontend/management networks
- Engineer lossless Ethernet for RoCEv2 — PFC, ECN, and congestion
  management — and relate it to Chapter 05's machinery
- Plan deployment and data management: cluster bring-up, job
  scheduling context, and the data pipeline that keeps GPUs fed
- Operate and troubleshoot AI fabrics with the telemetry and failure
  patterns unique to collective communication

## Theory and Architecture

### What the workload actually does to the network

Distributed training runs the same computation across many GPUs and
synchronizes constantly: **collective operations** (all-reduce,
all-gather) exchange gradient data between every participant at each
step. The consequences are unlike enterprise traffic. The pattern is
synchronized bursts — every GPU transmits at line rate
simultaneously, then waits. The job runs at the pace of the slowest
exchange, so **tail latency is the metric**, not average. And a
single loss event stalls the collective: retransmission delay on one
flow delays every GPU in the job. Training jobs also run for days —
one 30-second fabric brownout can discard hours of progress to the
last checkpoint.

Inference is gentler per-flow — request/response at scale, latency
SLOs in milliseconds — but multiplies east-west when models shard
across GPUs. DCAI's Fundamentals domain (20%) tests exactly this
literacy: which workload stresses what.

### Cluster anatomy: four networks, not one

The converged pattern separates concerns:

- **Backend (scale-out) fabric** — GPU-to-GPU for collectives:
  spine-leaf, non-blocking (1:1 — the one place oversubscription is
  simply wrong), 400G-class links, RoCEv2 transport, often organized
  in **rails** (each GPU's NIC *n* into rail-*n* switching) to match
  collective traffic patterns.
- **Frontend network** — users, orchestration, model serving; normal
  enterprise rules apply.
- **Storage network** — the data pipeline feeding training; high
  throughput sequential reads plus the checkpoint write bursts.
- **Management/OOB** — as always, and Chapter 01's rule holds
  hardest here: you cannot debug a stalled collective through the
  fabric that is stalling.

Inside the server, GPUs interconnect over NVLink-class links; between
servers, the backend fabric is the interconnect — which is why its
engineering gets the DCAI architecture domain's 30%.

### RoCEv2 and the return of lossless Ethernet

RDMA lets NICs move memory-to-memory without CPUs; **RoCEv2** runs it
over routable UDP/IP Ethernet. RDMA tolerates loss catastrophically —
go-back-N retransmission — so the fabric must not lose: **PFC** gives
the no-drop class (Chapter 05's machinery, same DCBX negotiation),
and because pause alone head-of-line-blocks at scale, **ECN**-based
congestion control (DCQCN) marks early so senders slow before pause
ever fires. Tuning is the craft: ECN thresholds low enough to signal
before buffers fill, PFC as the backstop rather than the mechanism,
watchdogs against pause storms, and buffer profiles fitted to burst
size. Nexus 9000 AI-fabric guidance packages these; the exam and the
field both expect you to know *why* each knob exists.

### Deployment and the data pipeline

The DCAI deployment domain (30%) spans bring-up and data: imaging and
firmware alignment across GPU nodes (Intersight territory — Chapter
04's fleet discipline applied to denser, hotter servers), fabric
rendering from templates (Chapter 06's automation, non-negotiable at
rail scale), integration with schedulers (Kubernetes device plugins,
Slurm) that place jobs onto GPUs, and the pipeline: datasets staged to
parallel storage fast enough that GPUs never starve, checkpoints
written at intervals that bound loss without throttling the run.
Power and cooling stop being facilities trivia — AI racks draw
30–100+ kW, and design reviews now start there.

## Design Considerations

- **Non-blocking backend, rails-aligned**: size for every GPU
  transmitting simultaneously, because they will.
- **Separate the networks physically** where budget allows; converged
  AI fabrics inherit every noisy-neighbor problem the pattern exists
  to avoid.
- **Checkpoint cadence versus storage burst capacity** is a real
  trade: frequent checkpoints bound job loss but hammer storage —
  size the write path for it.
- **Buy the telemetry**: per-queue microburst visibility, PFC/ECN
  counters streamed (Chapter 06 telemetry), and job-level correlation
  — a fabric you cannot observe at millisecond granularity will
  gaslight you.

## Implementation and Automation

The no-drop class on Nexus for RoCEv2 (representative pattern):

```text
class-map type qos match-all ROCE
  match dscp 26                     ! RoCEv2 traffic marked by hosts
policy-map type qos QOS-IN
  class ROCE
    set qos-group 3
policy-map type network-qos NQOS-AI
  class type network-qos c-8q-nq3
    pause pfc-cos 3                 ! lossless class
    mtu 9216
system qos
  service-policy type network-qos NQOS-AI

! ECN on the egress queue serving the no-drop class
policy-map type queuing QUEUE-AI
  class type queuing c-out-8q-q3
    random-detect minimum-threshold 150 kbytes maximum-threshold 3000 kbytes
    ecn
```

Validation counters that matter:

```text
show interface priority-flow-control        ! PFC frames rx/tx per port
show queuing interface e1/1                 ! ECN marks, drops per queue
show interface e1/1 | include pause
```

Fleet bring-up is Chapter 06 practice at higher stakes: rail switch
configs rendered from data, host NIC settings (DSCP marking, DCBX)
enforced by host automation, and a **synthetic RDMA benchmark**
(`ib_write_bw`-class tools between node pairs, then all-to-all) run
as acceptance *before* the first real job — the cluster's birth
certificate.

## Validation and Troubleshooting

The failure signature of AI fabrics is **the slow job, not the down
link**. Method: establish the baseline (the acceptance benchmark
above, kept); when a job degrades, check ECN mark and PFC pause
counters per rail for hotspots; look for asymmetry (one flapping or
CRC-erroring link in an ECMP group degrades the whole collective —
the Chapter 02 intermittent-loss lesson at 400G); verify DCBX/PFC
agreement end to end including the *hosts* (one NIC missing its no-drop
class can pause-storm a rail); and correlate with job events —
checkpoint stalls implicate the storage path, uniform slowness
implicates thresholds, single-node laggards implicate that node's
NIC, link, or thermals. Pause storms deserve their own drill: PFC
watchdog counters identify the port sourcing sustained pause, and the
cure is usually a host, not a switch.

## Security and Best Practices

- Training data and model artifacts are often the most valuable data
  in the building: storage-path encryption, scheduler AAA, and
  artifact registries with provenance apply — Volume X's controls,
  aimed at the new crown jewels.
- The backend fabric is single-tenant by design; keep it
  unreachable from general networks — its management plane included.
- GPU firmware and driver supply chains get the same signing and
  staging discipline as network images; a bad driver at rail scale is
  a cluster outage.

## References and Knowledge Checks

- DCAI 300-640 v1.0 exam topics (the four domains: 20/30/30/20)
- Cisco Nexus 9000 AI/ML fabric design guidance and validated designs
- Cisco U. DCAIE and DCAIAOT training paths (the published DCAI prep)

Knowledge checks:

1. Why does one dropped frame degrade an entire training job, and
   which two mechanisms together keep the fabric lossless-in-practice?
2. What ratio of oversubscription is acceptable on the backend
   fabric, and what workload fact makes any other answer wrong?
3. A 512-GPU job runs 20% slower this week. Give three fabric-side
   hypotheses and the counter or comparison that tests each.
4. Where do ECN and PFC each act, and why is "ECN early, PFC
   backstop" the design intent rather than the reverse?

## Hands-On Lab

Hardware honesty: no home lab has GPU rails, so this lab drives design
and configuration artifacts — the DCAI-relevant skills that are
paper-testable. Produce: (1) a rails-aligned backend design for 32
GPU nodes × 4 NICs — topology, non-blocking math shown, rail diagram;
(2) the complete Nexus no-drop/ECN configuration for one rail switch,
annotated line-by-line with *why*; (3) the acceptance-test plan
(pair and all-to-all benchmark stages, pass thresholds, counters
captured); (4) a troubleshooting runbook entry for "job slow, no
alarms" following the method above. In CML, render the rail switch
configuration onto a 9000v and validate syntax and queuing policy
attachment (`show policy-map system type network-qos`).

## Lab Verification

Verification means the design's math is checkable, the rendered
configuration attached cleanly in CML with queuing policy verified,
and the runbook entry names counters, not vibes. Until then, the lab
is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

AI infrastructure is Chapter 02's fabric discipline, Chapter 04's
fleet discipline, Chapter 05's losslessness, and Chapter 06's
automation — turned up to the point where tail latency is the SLA.
Collectives synchronize, so the fabric must not lose or lag; PFC and
ECN make Ethernet keep that promise; and operations shift from
watching links to watching jobs. This chapter is the whole DCAI exam
and the Automation-and-AI slice of DCCOR.

- [ ] I can explain all-reduce's traffic pattern and its tail-latency
      consequence
- [ ] I can configure and validate the no-drop class with ECN
- [ ] My design artifacts pass their own non-blocking arithmetic
- [ ] My runbook diagnoses the slow-job case by counters
