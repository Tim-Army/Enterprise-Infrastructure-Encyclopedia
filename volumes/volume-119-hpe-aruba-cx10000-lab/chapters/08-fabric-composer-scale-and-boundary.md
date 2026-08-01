# Chapter 08: Fabric Composer, Scale, and the Boundary

## Learning Objectives

- Understand how PSM/Fabric Composer manage stateful policy across many ToRs.
- See how DPU offload scales stateful firewalling to a whole data center.
- Recognize the limits of the DPU/ToR model.

## Hands-On Lab

### Exercise 8.1 — Central management and scale (design)

**Objective.** Understand fleet-scale stateful segmentation.

**Design walkthrough.** Each rack's CX 10000 has its own DPU enforcing stateful policy locally, and **PSM/Aruba Fabric Composer** author and distribute the policy and collect telemetry across every ToR. Because each DPU firewalls only its own rack's east-west traffic at line rate, stateful capacity scales **with the fabric** — adding a rack adds a DPU and its firewall throughput, with no central firewall to become a bottleneck. This is the core advantage of distributing stateful services to the ToR.

**Expected result (on paper).** A design note: one DPU per ToR firewalling its rack, PSM/FC as the central policy and telemetry plane, stateful capacity scaling with the fabric.

**Cleanup.** None.

### Exercise 8.2 — Where the DPU model fits (design)

**Objective.** See the CX 10000 alongside the other fabric models.

**Design walkthrough.** The ASIC fabrics (ACI, Arista MSS) do fast, largely **stateless** group/contract policy; the CX 10000 adds **stateful** firewalling and NAT in the ToR DPU. In a data center you might use both — fast group segmentation plus stateful east-west firewalling where firewall-grade behavior is required — and pair with host controls for the workloads and L7 the fabric does not inspect.

**Expected result (on paper).** A design note: stateless group policy for speed, DPU stateful firewalling for firewall-grade east-west, host/service controls for L7.

**Cleanup.** None.

### Exercise 8.3 — The boundary

**Objective.** Identify the limits of the DPU/ToR model.

**Track 1 & 2 — Walkthrough.** Boundaries:

- **It enforces on traffic crossing the CX 10000.** Servers not attached to a CX 10000 ToR are outside its stateful policy; coverage is per-rack/ToR.
- **Stateful L3/L4 (plus NAT), not full L7.** Deep application inspection still needs a service device or host control.
- **DPU capacity is finite.** Very large connection counts and throughput have limits per DPU, sized per rack.

```bash
echo "The DPU firewalls its rack's east-west; off-ToR servers and L7 need complementary controls."
```

**Expected result.** A boundary note: use CX 10000 DPUs for stateful east-west in the rack, and pair with host/cloud controls (Volumes XCIII–CXVI) and L7 inspection where needed.

**Negative test.** Assume the CX 10000 secures every workload. It secures traffic crossing its ToR; a server on a non-CX-10000 switch needs another control applying consistent stateful policy.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Central management and per-ToR DPU scaling understood.
- [ ] The stateful-DPU role alongside stateless fabrics understood.
- [ ] The per-ToR / L3-L4 / DPU-capacity boundaries recognized.
- [ ] Complementary controls identified.
