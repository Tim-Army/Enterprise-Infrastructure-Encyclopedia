# Chapter 08: Scale, Management, and the Boundary

## Learning Objectives

- Understand how DPU policy is managed across a fleet of servers.
- See where the BlueField model fits alongside the fabric DPUs and host agents.
- Recognize the limits of per-server DPU enforcement.

## Hands-On Lab

### Exercise 8.1 — Fleet management (design)

**Objective.** Understand DPU segmentation at data-center scale.

**Design walkthrough.** Each server's BlueField enforces its own workloads, and a management plane (DOCA-based tooling, an orchestrator, or a partner microsegmentation product running on the DPUs) distributes policy and collects telemetry across every DPU. Because enforcement and datapath are on the DPUs, segmentation capacity scales **per server** — every host added brings its own enforcement, with no central bottleneck, and the policy is applied out-of-band on every one.

**Expected result (on paper).** A design note: per-server DPU enforcement, central policy distribution and telemetry, capacity scaling with the server count.

**Cleanup.** None.

### Exercise 8.2 — Where BlueField fits (design)

**Objective.** Compare with the ToR-DPU and host-agent models.

**Design walkthrough.** Three enforcement locations, three trade-offs:

- **Host agent** (Volumes XCIII–C): richest workload/process context, but runs on the host an attacker can own.
- **ToR-switch DPU** (Volume CXIX): stateful east-west for the whole rack in the switch, off the servers.
- **Per-server DPU** (this volume): enforcement at each NIC, in an isolated trust domain that survives host compromise, at zero host-CPU cost.

They compose: use per-server DPUs for tamper-resistant, host-adjacent enforcement, ToR DPUs or fabric policy for broader east-west, and host agents where deep process identity is needed.

**Expected result (on paper).** A design note placing BlueField as the tamper-resistant, host-adjacent enforcement layer.

**Cleanup.** None.

### Exercise 8.3 — The boundary

**Objective.** Identify the limits of per-server DPU enforcement.

**Track 1 & 2 — Walkthrough.** BlueField boundaries:

- **It requires a DPU in each server.** Hosts without a BlueField are outside its enforcement; coverage is per-DPU-equipped server.
- **Policy source of truth must be protected.** The DPU is tamper-resistant, but the management plane that programs it must itself be secured.
- **Workload/process identity is limited.** The DPU sees the workload's traffic at the NIC; deep process-level identity may still want a host signal, fed to the DPU policy.

```bash
echo "BlueField enforces at DPU-equipped NICs; non-DPU servers and deep process identity need complementary controls."
```

**Expected result.** A boundary note: deploy DPUs across the estate, secure the management plane, and pair with host context and fabric controls (Volumes XCIII–CXIX) where needed.

**Negative test.** Assume a BlueField secures a server with no DPU. It does not — enforcement is where the DPU is; a non-DPU host needs another control.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Per-server DPU fleet management understood.
- [ ] BlueField placed alongside host-agent and ToR-DPU models.
- [ ] The per-DPU-server / management-plane / process-identity boundaries recognized.
- [ ] Complementary controls identified.
