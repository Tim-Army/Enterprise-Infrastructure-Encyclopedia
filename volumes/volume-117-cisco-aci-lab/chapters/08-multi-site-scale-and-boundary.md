# Chapter 08: Multi-Site, Scale, and the Boundary

## Learning Objectives

- Understand how ACI Multi-Site stretches EPGs and contracts across fabrics.
- See how the application-centric model scales policy.
- Recognize the limits of the ACI fabric model.

## Hands-On Lab

### Exercise 8.1 — Multi-Site and scale (design)

**Objective.** Understand ACI at fabric and multi-fabric scale.

**Design walkthrough.** Within a fabric, contracts are enforced consistently on every leaf by the ASICs, so policy follows the endpoint wherever it attaches. **ACI Multi-Site Orchestrator (Nexus Dashboard Orchestrator)** stretches tenants, EPGs, and contracts across multiple fabrics/sites, so the same application policy is enforced in each data center and an endpoint keeps its EPG across sites. Scaling is adding leaves or sites, not re-authoring policy — the application-centric model is defined once and applied everywhere.

**Expected result (on paper).** A design note: contracts enforced fabric-wide by the leaves, stretched across sites by the orchestrator, policy defined per application not per switch.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.2 — Integrations (design)

**Objective.** See how ACI ties to compute and security.

**Design walkthrough.** ACI integrates with hypervisors (VMM domains) so EPG membership can follow VMs, and with security tools (for example Cisco Secure Workload for policy discovery, or service graphs that insert firewalls/IPS into a contract's path). Contracts can therefore redirect traffic through an inserted service device — combining the whitelist with deeper inspection.

**Expected result (on paper).** A design note: VMM integration for dynamic EPG membership, service graphs to insert inspection into a contract path.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.3 — The boundary

**Objective.** Identify the limits of the ACI fabric model.

**Track 1 & 2 — Walkthrough.** ACI's segmentation has boundaries:

- **It governs traffic on the fabric.** Endpoints not attached to the ACI fabric are outside its enforcement; hybrid estates need consistent policy across ACI and non-ACI (Cisco Cloud ACI/other controllers or host controls).
- **Contracts are L3/L4 plus service graphs.** Deep application/protocol control needs an inserted service device or a host/OT-aware control.
- **Model complexity.** The tenant/AP/EPG/BD/VRF/contract model is powerful but easy to misconfigure; disciplined naming and templates matter.

```bash
echo "ACI enforces on the fabric; off-fabric endpoints and L7 need complementary controls."
```

**Expected result.** A boundary note: use ACI for fabric-attached data-center segmentation, service graphs for inspection in a contract path, and pair with host/cloud controls (Volumes XCIII–CXVI) for off-fabric and endpoint coverage.

**Negative test.** Assume ACI secures every workload. It secures fabric-attached endpoints; a VM on a non-ACI host or a cloud workload needs a consistent policy applied by another control.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Multi-Site stretching of EPGs/contracts understood.
- [ ] VMM and service-graph integrations understood.
- [ ] The on-fabric / L3-L4 / complexity boundaries recognized.
- [ ] Complementary controls identified.
