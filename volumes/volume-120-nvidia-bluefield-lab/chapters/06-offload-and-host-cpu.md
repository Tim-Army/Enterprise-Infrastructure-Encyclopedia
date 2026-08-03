# Chapter 06: Offload and Host CPU

## Learning Objectives

- Understand that DPU enforcement runs on the DPU's own cores, not the host CPU.
- See that policy processing is invisible to and unbilled from the host.
- Understand why offload matters for dense, high-throughput servers.

## Enforcement that costs the host nothing

Running microsegmentation on the host CPU (agent or kernel firewall) consumes cycles the application wanted — noticeable on dense virtualization hosts. The BlueField DPU runs the policy on **its own Arm cores**, so the host CPU spends **zero** cycles on segmentation, and the DPU can process at line rate. This chapter shows, on Track 2, that the enforcement executes outside the workload's own resource domain.

## Hands-On Lab

### Exercise 6.1 — Enforcement runs outside the workload

**Objective.** Confirm the policy executes in the DPU namespace, not the workload.

**Track 1 — Walkthrough.** BlueField processes segmentation in the DPU; host CPU utilization for the policy is zero, and the host OS has no firewall load for east-west enforcement — DOCA telemetry attributes the work to the DPU.

**Track 2 — Walkthrough.** The workload namespace has no filtering rules of its own (the enforcement is in the DPU namespace); confirm where the rules — and thus the processing — live:

```bash
echo "== workload (web) ruleset =="; sudo ip netns exec web nft list ruleset 2>/dev/null | wc -l
echo "== DPU (dpu-web) ruleset =="; sudo ip netns exec dpu-web nft list ruleset 2>/dev/null | grep -c "accept\|drop"
```

**Expected result.** The workload namespace has an empty (0-line) ruleset while the DPU namespace holds the enforcing rules — the packet filtering happens in the DPU's domain, modeling the DPU's separate cores doing the work at no cost to the host.

**Negative test.** If the rules were in the workload namespace (a host-agent model, Chapter 05), the host would pay for every packet's filtering; here it pays nothing because the DPU domain does it.

**Cleanup.** None.

### Exercise 6.2 — Line-rate offload (design)

**Objective.** Understand the throughput benefit.

**Design walkthrough.** BlueField offloads not just the *decision* but the *datapath*: permitted flows are handled by the DPU's hardware pipelines at line rate, so segmentation adds no host CPU and minimal latency even at high throughput. This is why DPU segmentation suits dense virtualization and high-bandwidth east-west — the host keeps all its cycles for workloads.

**Expected result (on paper).** A design note: policy and datapath on the DPU, host CPU untouched, line-rate east-west with per-workload segmentation.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Enforcement confirmed to run in the DPU domain, not the workload.
- [ ] The host-CPU-zero-cost property understood.
- [ ] The line-rate offload benefit understood.
- [ ] Why offload matters for dense/high-throughput servers internalized.
