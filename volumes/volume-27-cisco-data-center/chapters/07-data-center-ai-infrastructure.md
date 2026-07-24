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

This chapter carries a topic-level walkthrough lab for **DCCOR 350-601 v1.2
Objective 4.3 (AI-enabling network technologies) and every objective of the
DCAI 300-640 v1.0 exam guide** — the Implementing Cisco Data Center AI
Infrastructure concentration (GA 3 February 2026) — mapped in the volume
README's coverage tables. Labs use the NX-OS CLI on a Nexus 9000 AI/ML back-end
fabric, Cisco UCS/Intersight for GPU compute, and Nexus Dashboard for
monitoring. Design-oriented "Describe/Evaluate" objectives are walkthroughs that
read the state or requirement they reason about. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 7.1–7.19** — a Nexus 9000 leaf carrying RoCEv2
traffic between GPU servers, a UCS/UCS-X domain with GPU-equipped servers
managed by Intersight, and Nexus Dashboard reachable at `$ND`. **Cost:** none
beyond lab resources.

### Lab 7.1 — Describe high-performance network technologies for AI infrastructure (DCCOR Objective 4.3)

**Objective:** Verify the lossless, low-latency plumbing an AI/ML (GPU) fabric
needs — PFC, ECN/WRED, and RoCEv2 — and read the congestion counters.

```text
show queuing interface ethernet 1/5 | include "PFC|ECN|WRED"
show interface ethernet 1/5 priority-flow-control
show interface ethernet 1/5 counters detailed | include "ECN|pause|pfc"
```

**Expected result:** PFC enabled on the RoCEv2 no-drop class, ECN marking with a
WRED profile, and pause/ECN counters incrementing under load — RoCEv2 needs a
lossless class (PFC) plus proactive congestion signaling (ECN) so GPU
collectives do not stall on drops.

**Negative test:** send RDMA over a best-effort class with PFC disabled; under
incast the switch drops frames, RoCEv2 retransmits, and job completion time
spikes — the no-drop class is mandatory for AI, not optional tuning.

**Cleanup:** none (read-only); `clear counters interface ethernet 1/5` if
desired.

### Lab 7.2 — Describe AI/ML workload types (DCAI Objective 1.1)

**Objective:** Distinguish training, fine-tuning, and inference by their fabric
demands.

```text
show interface ethernet 1/5 counters detailed | include "rx|tx"
show queuing interface ethernet 1/5 | include "unicast"
```

**Expected result:** heavy sustained east-west on the training pod versus
bursty, latency-sensitive traffic on inference — **training** is bandwidth-bound
all-to-all (GPU collectives), **fine-tuning** is a lighter training variant, and
**inference** is latency-bound request/response; each stresses the fabric
differently.

**Negative test:** size an inference-only fabric for training's all-to-all
bandwidth and you overspend; size a training fabric for inference latency and
collectives stall — matching workload type to design is the objective.

**Cleanup:** none (read-only).

### Lab 7.3 — Describe the AI lifecycle (DCAI Objective 1.2)

**Objective:** Map the data → train → deploy → monitor stages to infrastructure
touchpoints.

```bash
curl -s -H "X-Starship-Api-Key: $IK" "https://intersight.com/api/v1/compute/PhysicalSummaries?\$filter=contains(Name,'gpu')&\$select=Name,OperState" | jq -r '.Results[] | "\(.Name) \(.OperState)"'
```

**Expected result:** the GPU nodes and their state — the AI lifecycle (data
ingestion/prep, training, validation, deployment, monitoring/retraining) maps to
storage (data), the GPU fabric (train), UCS/edge (deploy), and Nexus
Dashboard/Intersight (monitor); each stage has an infrastructure owner.

**Negative test:** treat training infrastructure as static; without a
monitor→retrain loop the model drifts — the lifecycle is a cycle, not a line.

**Cleanup:** none (read-only).

### Lab 7.4 — Describe AI use cases (DCAI Objective 1.3)

**Objective:** Relate common use cases to their infrastructure profile.

```bash
nvidia-smi --query-gpu=name,memory.total,utilization.gpu --format=csv 2>/dev/null | head
```

**Expected result:** the GPU model, memory, and utilization — LLM training needs
large multi-GPU clusters with RDMA; computer vision and recommendation are
GPU-memory-bound; edge inference needs small low-latency footprints; RAG adds a
vector-store I/O profile. The GPU inventory anchors the use case to hardware.

**Negative test:** run an LLM training job on a single small-memory GPU; it OOMs
— the use case dictates the memory/interconnect the infrastructure must provide.

**Cleanup:** none (read-only).

### Lab 7.5 — Describe the types of AI infrastructure (DCAI Objective 1.4)

**Objective:** Contrast on-prem GPU cluster, cloud, and hybrid.

```bash
show interface ethernet 1/5 | include "rate"
curl -s -H "X-Starship-Api-Key: $IK" "https://intersight.com/api/v1/asset/DeviceRegistrations?\$select=PlatformType" | jq -r '.Results[].PlatformType' | sort -u
```

**Expected result:** the on-prem fabric plus the platform types Intersight
manages — AI infrastructure is **on-prem** (owned GPU clusters, lowest
long-run cost at scale), **cloud** (elastic, opex, fastest to start), or
**hybrid** (burst/train split); the objective is choosing per constraint.

**Negative test:** run continuous large-scale training in the cloud on-demand;
cost dwarfs an owned cluster — the type must match the utilization pattern.

**Cleanup:** none (read-only).

### Lab 7.6 — Describe the components used for AI environments (DCAI Objective 1.5)

**Objective:** Inventory the GPU, interconnect, storage, and network components.

```bash
nvidia-smi topo -m 2>/dev/null | head        # GPU/NVLink topology
show interface ethernet 1/5 transceiver | include "type|400"
```

**Expected result:** the intra-node GPU interconnect (NVLink) and the
inter-node 400G optics — an AI environment combines GPUs with NVLink/NVSwitch
(scale-up), a RoCEv2/InfiniBand back-end fabric (scale-out), high-throughput
storage, and the front-end management network.

**Negative test:** connect GPU nodes with 10G access links; the interconnect
bottlenecks the collective and GPUs idle — component balance (GPU-to-network) is
the design point.

**Cleanup:** none (read-only).

### Lab 7.7 — Describe Cisco AI solutions (DCAI Objective 1.6)

**Objective:** Identify the Cisco building blocks for an AI data center.

```bash
curl -s -H "X-Starship-Api-Key: $IK" "https://intersight.com/api/v1/compute/PhysicalSummaries?\$select=Model" | jq -r '.Results[].Model' | sort -u | head
```

**Expected result:** Cisco AI-relevant models — **UCS X-Series / C-Series with
GPUs** for compute, **Nexus 9000 (and the AI-fabric designs)** for the RoCEv2
back-end, **Nexus Dashboard** for assurance, **Intersight** for lifecycle, and
**Cisco Validated Designs** (e.g., with NVIDIA) that tie them together.

**Negative test:** assemble GPU nodes with an unvalidated ad-hoc fabric design;
you forfeit the tested QoS/RoCEv2 blueprint a CVD provides — the solutions exist
to de-risk exactly that.

**Cleanup:** none (read-only).

### Lab 7.8 — Evaluate network deployment for AI workloads (DCAI Objective 2.1)

**Objective:** Assess bandwidth, latency, redundancy, scalability, and security
against workload need.

```text
show interface ethernet 1/5 | include "BW|rate"
show port-channel summary
show queuing interface ethernet 1/5 | include "ECN|PFC"
```

**Expected result:** link bandwidth, redundant port-channels, and lossless
queuing — an AI network is evaluated on non-blocking bandwidth (rail-optimized
400G), µs latency, redundancy (no collective stalls on a link loss), horizontal
scale (add leaves/rails), and segmentation of the AI pod.

**Negative test:** a design meeting bandwidth but lacking PFC/ECN fails the
latency/lossless requirement under incast — every axis must be met, not just
throughput.

**Cleanup:** none (read-only).

### Lab 7.9 — Evaluate compute deployment for AI workloads (DCAI Objective 2.2)

**Objective:** Assess CPU, GPU, GPU connectivity, memory, and virtualization.

```bash
nvidia-smi --query-gpu=name,memory.total,pcie.link.gen.current --format=csv 2>/dev/null
show server 1/1 detail 2>/dev/null | include "Memory|CPU" || true
```

**Expected result:** GPU model/memory/PCIe generation and host CPU/RAM — compute
is evaluated on GPU count and memory (model size), GPU interconnect
(NVLink/PCIe gen), host CPU/memory to feed the GPUs, and whether virtualization
(vGPU/MIG) or bare metal fits the workload.

**Negative test:** pair top-end GPUs with an undersized host CPU/PCIe; data
starvation leaves GPUs idle — balanced compute, not just GPU count, is what the
objective evaluates.

**Cleanup:** none (read-only).

### Lab 7.10 — Evaluate storage deployment for AI workloads (DCAI Objective 2.3)

**Objective:** Assess capacity, performance, redundancy, and scalability for the
data pipeline.

```bash
showmount -e 10.0.0.60 2>/dev/null | head
fio --name=read --rw=read --bs=1M --size=1G --numjobs=8 --runtime=10 --group_reporting 2>/dev/null | grep -E 'READ|IOPS' | head
```

**Expected result:** the dataset share and a throughput measurement — AI storage
is evaluated on capacity (datasets/checkpoints), sustained read throughput
(GB/s to feed GPUs), parallel/scale-out access (NFS/pNFS, parallel FS), and
redundancy; checkpoint writes add a bursty write profile.

**Negative test:** back a GPU cluster with a single low-throughput NFS mount; the
data loader bottlenecks and GPUs wait — storage throughput must match GPU
appetite.

**Cleanup:** remove the `fio` test file.

### Lab 7.11 — Evaluate power, efficiency, and sustainability (DCAI Objective 2.4)

**Objective:** Read power/thermal telemetry and reason about PUE.

```text
show environment power
show environment temperature | include "Module|Intake"
```

**Expected result:** per-module power draw and intake temperatures — AI racks
are power- and cooling-dense (multi-kW GPU nodes), so design evaluates power
delivery, cooling (often liquid), **PUE** (facility power ÷ IT power), and
sustainability (renewable sourcing, efficiency).

**Negative test:** populate a rack beyond its power/cooling envelope; nodes
throttle or trip — power and cooling are hard design constraints for GPU
density, not afterthoughts.

**Cleanup:** none (read-only).

### Lab 7.12 — Evaluate hybrid AI deployment with cloud integration (DCAI Objective 2.5)

**Objective:** Assess secure connectivity, data sync, and workload mobility to
cloud.

```bash
show interface tunnel 1 2>/dev/null | include "state|dest" || true
curl -s -H "X-Starship-Api-Key: $IK" "https://intersight.com/api/v1/asset/DeviceRegistrations?\$select=ConnectionStatus" | jq -r '.Results[].ConnectionStatus' | sort | uniq -c
```

**Expected result:** the DCI/cloud tunnel state and Intersight (SaaS) reach —
hybrid AI is evaluated on secure connectivity (encrypted DCI/VPN to cloud), data
synchronization (dataset/checkpoint replication), and workload mobility
(bursting training to cloud GPUs), balancing cost and data gravity.

**Negative test:** burst training to cloud without co-locating the dataset; data
egress/latency dominates and the burst is slower than on-prem — data gravity
governs hybrid design.

**Cleanup:** none (read-only).

### Lab 7.13 — Configure high-performance networks for AI using Cisco Data Center (DCAI Objective 3.1)

**Objective:** Configure the lossless RoCEv2 class on a Nexus AI leaf.

```text
config t
 class-map type qos match-all ROCE
  match dscp 24
 policy-map type qos AI-CLASSIFY
  class ROCE
   set qos-group 3
 policy-map type network-qos AI-NQ
  class type network-qos c-nq3
   pause pfc-cos 3
   mtu 9216
 system qos
  service-policy type network-qos AI-NQ
end
show queuing interface ethernet 1/5 | include "PFC|ECN|group 3"
```

**Expected result:** qos-group 3 marked no-drop with PFC on CoS 3 and jumbo MTU
— the RoCEv2 lossless class configured end to end, the network half of an
AI-ready fabric.

**Negative test:** omit `pause pfc-cos 3`; RoCEv2 traffic is best-effort and
drops under load — PFC on the RoCE class is what makes it lossless.

**Cleanup:** remove the service-policy and class/policy-maps.

### Lab 7.14 — Configure high-performance compute and storage using Cisco UCS (DCAI Objective 3.2)

**Objective:** Verify a UCS/Intersight GPU server profile and its storage/network
policy.

```bash
curl -s -H "X-Starship-Api-Key: $IK" "https://intersight.com/api/v1/server/Profiles?\$select=Name,ConfigContext" | jq -r '.Results[] | "\(.Name) \(.ConfigContext.ConfigState)"'
```

**Expected result:** the GPU server profile `Associated` with its policies — the
Intersight profile provisions the GPU node's BIOS (GPU-optimized), network
(RoCEv2 vNICs), and storage (NVMe/high-throughput) consistently, the compute half
of an AI-ready pod.

**Negative test:** a profile missing the GPU/BIOS policy leaves GPUs
mis-tuned; performance drops — the profile must include the AI-specific policies.

**Cleanup:** none (read-only).

### Lab 7.15 — Deploy AI-ready fabrics using Cisco orchestration tools (DCAI Objective 3.3)

**Objective:** Deploy the AI fabric via NDFC/Nexus Dashboard templates.

```bash
curl -sk -H "Authorization: $NDFC_TOK" \
  "https://$ND/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates" \
  | jq -r '.[].name' | grep -iE 'AI|Easy_Fabric' | head
```

**Expected result:** the fabric templates (e.g., an AI/`Easy_Fabric` template)
NDFC uses to render a consistent RoCEv2 spine-leaf — orchestration deploys the
tested QoS/underlay across every switch rather than hand-configuring each.

**Negative test:** hand-build each leaf's QoS; one inconsistent switch creates a
lossy path that stalls collectives — orchestration's consistency is the point.

**Cleanup:** none (read-only).

### Lab 7.16 — Implement benchmarks to evaluate AI infrastructure performance (DCAI Objective 4.1)

**Objective:** Run a collective-communication benchmark across the GPU fabric.

```bash
# NCCL all-reduce bandwidth across nodes (the fabric-level AI benchmark)
mpirun -np 16 -H node1,node2 all_reduce_perf -b 8 -e 8G -f 2 -g 1 2>/dev/null | tail -5
```

**Expected result:** the NCCL all-reduce bus bandwidth approaching line rate —
benchmarks (NCCL tests, MLPerf) quantify whether the fabric delivers the
bandwidth/latency GPU collectives need, the objective measure of an AI fabric.

**Negative test:** a benchmark far below line rate points to a lossy path
(missing PFC) or an oversubscribed rail — the number localizes the design flaw.

**Cleanup:** none.

### Lab 7.17 — Implement monitoring with Nexus Dashboard and Intersight (DCAI Objective 4.2)

**Objective:** Read AI-fabric anomalies and GPU-node health from the Cisco
platforms.

```bash
curl -sk -b cookie.txt "https://$ND/sedgeapi/v1/cisco-nir/api/api/telemetry/v2/anomalies/summary" | jq '.totalItemsCount'
curl -s -H "X-Starship-Api-Key: $IK" "https://intersight.com/api/v1/cond/Alarms?\$filter=Severity eq 'Critical'" | jq '.Results | length'
```

**Expected result:** the fabric anomaly count (Nexus Dashboard Insights) and
critical Intersight alarms — monitoring correlates fabric congestion (PFC/ECN
events) with GPU-node health, the two failure domains of an AI cluster.

**Negative test:** monitor only the servers and miss a fabric PFC storm stalling
collectives — AI monitoring must span fabric and compute together.

**Cleanup:** none (read-only).

### Lab 7.18 — Monitor AI infrastructure using system messages and management tools (DCAI Objective 4.3)

**Objective:** Watch the syslog/telemetry signals specific to AI congestion.

```text
show logging last 30 | include "PFC|pause|ECN|BUFFER"
show hardware qos pfc-status
show interface priority-flow-control | include "Rx|Tx"
```

**Expected result:** PFC pause frames and buffer/ECN events in the log — the
system messages that signal an AI fabric under congestion; watched continuously
(with the telemetry from Lab 6.22), they give early warning before jobs stall.

**Negative test:** rely on interface up/down alone; a fabric can be "all up"
while PFC storms stall collectives — the AI-specific counters are what reveal it.

**Cleanup:** none (read-only).

### Lab 7.19 — Troubleshoot AI infrastructure (DCAI Objective 4.4)

**Objective:** Diagnose slow GPU-job completion to its layer — fabric, compute,
or storage.

```text
show interface ethernet 1/5 counters detailed | include "pause|ECN|discard"
show queuing interface ethernet 1/5 | include "drop"
```

```bash
nvidia-smi --query-gpu=utilization.gpu,utilization.memory --format=csv 2>/dev/null
```

**Expected result:** fabric pause/discard counters plus GPU utilization — a slow
job with **high pause and low GPU utilization** is a fabric-congestion problem
(PFC/incast); **high GPU but low throughput** is compute-bound; **low both with
storage waits** is a data-loader/storage bottleneck — the counters localize the
layer.

**Negative test:** blame the GPUs when GPU utilization is low and pause frames
are high; the fabric is starving them — read the fabric before the accelerators.

**Cleanup:** none (read-only); `clear counters` after recording if desired.

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
