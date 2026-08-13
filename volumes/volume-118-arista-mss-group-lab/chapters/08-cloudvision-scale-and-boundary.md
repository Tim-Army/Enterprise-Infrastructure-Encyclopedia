# Chapter 08: CloudVision, Scale, and the Boundary

## Learning Objectives

- Understand how CloudVision manages groups and policy across the fabric.
- See how group policy scales at line rate.
- Recognize the limits of switch-enforced group segmentation.

## Hands-On Lab

### Exercise 8.1 — CloudVision and scale (design)

**Objective.** Understand fleet management.

**Design walkthrough.** **CloudVision** is the single plane for defining security groups and MSS/MSS-Group policy and pushing it to every EOS switch, with fabric-wide telemetry showing group flows and policy hits. Because enforcement is in the switch ASICs, policy scales at line rate across the fabric with no hairpin; membership can be driven by subnet/VLAN/interface or integrations. Adding capacity is adding switches to the fabric, with the same group policy applied.

**Expected result (on paper).** A design note: groups and policy authored once in CloudVision, enforced at line rate on every switch, telemetry centralized.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.2 — Macro and micro together at scale (design)

**Objective.** See how the two modes combine.

**Design walkthrough.** At scale you use **MSS-Group (micro)** for the bulk of east-west policy — cheap, line-rate, default-deny between groups — and **MSS (macro)** selectively to steer the flows that need deep inspection through firewalls. This keeps the firewalls out of the path of most traffic (no bottleneck) while still inspecting the sensitive flows.

**Expected result (on paper).** A design note: micro for the many, macro-redirect for the few — line-rate segmentation plus targeted inspection.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.3 — The boundary

**Objective.** Identify the limits of switch-enforced group segmentation.

**Track 1 & 2 — Walkthrough.** Arista MSS boundaries:

- **It enforces on the fabric.** Endpoints not behind an EOS switch are outside its policy; hybrid estates need consistent policy across fabric and non-fabric.
- **Micro policy is L3/L4.** Deep inspection needs the macro firewall redirect or a host control.
- **Group resolution must be correct.** An endpoint in the wrong group gets the wrong policy; membership criteria and integrations must be accurate.

```bash
echo "MSS enforces on the EOS fabric; off-fabric endpoints and L7 need macro redirect or host controls."
```

**Expected result.** A boundary note: use MSS-Group for fabric-attached east-west, MSS macro for inspection, and pair with host/cloud controls (Volumes XCIII–CXVI) for off-fabric workloads.

**Negative test.** Assume MSS secures every workload. It secures fabric-attached endpoints; a workload not behind an EOS switch needs another control applying consistent policy.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] CloudVision management and line-rate scale understood.
- [ ] Micro-for-the-many / macro-for-the-few design understood.
- [ ] The on-fabric / L3-L4 / group-resolution boundaries recognized.
- [ ] Complementary controls identified.
