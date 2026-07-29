# Chapter 02: Enforcement Models and a Selection Framework

## Learning Objectives

- Enumerate the enforcement models for microsegmentation.
- Explain the trade-offs of agent vs agentless vs hypervisor vs appliance enforcement.
- Apply a selection rubric (coverage, visibility, automation, scale, compliance, TCO).
- Score an option against the rubric.
- Complete a walkthrough for each model-and-selection topic.

## Theory and Architecture

Microsegmentation products differ mainly in **where they enforce** policy. The models:

1. **Network/fabric** — switch/router ACLs or SDN fabric (Cisco ACI). Enforces in the network; no host
   touch, but coarse and topology-bound.
2. **Hypervisor** — a distributed firewall in the virtualization layer (VMware NSX DFW). Agentless for
   VMs, line-rate in the kernel; tied to the hypervisor.
3. **Host agent** — a per-workload agent programs the host firewall (Illumio VEN, Guardicore, Cisco
   Secure Workload, ColorTokens agent). Fine-grained, portable; requires deploying and maintaining agents.
4. **Agentless OS-firewall** — a controller remotely programs the host's **built-in** firewall (Zero
   Networks). No agent, but needs remote-management reachability.
5. **EDR-leveraged** — reuse an existing EDR agent's telemetry/enforcement (TrueFort, ColorTokens via
   CrowdStrike/SentinelOne/Defender). No new agent if the EDR is present.
6. **Agentless appliance/gateway** — an inline appliance segments devices that cannot take an agent
   (ColorTokens Gatekeeper for OT/IoT/legacy).
7. **Cloud-native** — provider constructs (AWS security groups/NACLs, Azure NSG/ASG, GCP firewall).
   Native and free; cloud-only and coarse.
8. **Container/eBPF** — Kubernetes NetworkPolicy, Calico, Cilium (eBPF, identity-based). Native to
   clusters; CNI-dependent.

No model is universally best. The **selection rubric** weighs: **coverage** (Windows/Linux/legacy/OT/
IoT/cloud/K8s/network gear), **visibility & dependency mapping**, **policy automation**, **enforcement
granularity** (L4 vs L7/process/identity), **scale & performance**, **failure mode** (fail-open vs
fail-closed), **compliance** (e.g., FedRAMP), and **TCO/operational burden**. This chapter builds the
rubric the option chapters are scored against.

## Design Considerations

Weight the rubric to **your** environment: a VMware-heavy shop weights hypervisor coverage; a
multi-cloud, agent-averse shop weights agentless and cloud-native. Insist on strong **dependency
mapping** — you cannot segment what you cannot see. Prefer **policy automation** to hand-written rules
at scale. Decide the **failure mode** deliberately (fail-open preserves uptime, fail-closed preserves
containment). Count the **operational** cost, not just the license.

## Implementation and Automation

The labs enumerate the models against an environment, and build and apply a weighted scoring rubric —
the framework used to compare the options in the following chapters.

## Validation and Troubleshooting

Confirm the framework:

```text
Models: network | hypervisor | host-agent | agentless-OS-FW | EDR-leveraged | appliance | cloud-native | container/eBPF
Rubric: coverage + visibility/mapping + automation + granularity + scale + failure-mode + compliance + TCO
Weight the rubric to YOUR environment; score each option; no universal winner
```

Common pitfalls: choosing on a single axis (price, or "agentless") and ignoring **coverage** gaps (OT,
legacy, cloud); and skipping **dependency mapping** capability in the evaluation.

## Security and Best Practices

Choose the model that actually covers your assets and that your team can operate; an unmanaged
best-in-class tool segments nothing. Match the failure mode to your risk tolerance. All work is
authorized.

## Hands-On Lab

Model-and-selection walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 2.1 — Map assets to enforcement models

**Objective:** See which model can cover each asset class.

```python
python3 - <<'PY'
coverage = {
  "Windows/Linux VMs (vSphere)": ["hypervisor(NSX)", "host-agent", "agentless-OS-FW", "EDR"],
  "Bare-metal servers":          ["host-agent", "agentless-OS-FW", "EDR"],
  "OT/IoT/legacy (no agent)":    ["appliance(Gatekeeper)", "network/fabric"],
  "Cloud VMs":                   ["cloud-native(SG/NSG)", "host-agent", "EDR"],
  "Kubernetes pods":             ["container/eBPF (NetworkPolicy/Calico/Cilium)"],
}
for asset, models in coverage.items():
    print(f"{asset:30}: {', '.join(models)}")
print("Rule: pick tools that together cover ALL your asset classes")
PY
```

**Expected result:** each asset class mapped to the models that can enforce it — a coverage map.

**Negative test:** pick one host-agent tool and assume it covers OT/IoT it cannot install on; add an
**appliance/network** model for agentless assets.

**Cleanup:** none.

### Lab 2.2 — Build a weighted scoring rubric

**Objective:** Make the comparison objective.

```python
python3 - <<'PY'
weights = {"coverage":0.25,"visibility":0.15,"automation":0.15,"granularity":0.10,
           "scale":0.10,"failure_mode":0.05,"compliance":0.10,"tco":0.10}
print("Rubric weights (sum = %.2f):" % sum(weights.values()))
for k,v in weights.items(): print(f"  {k:12}: {v}")
PY
```

```text
Rubric weights (sum = 1.00):
  coverage    : 0.25
  visibility  : 0.15
  ...
```

**Expected result:** a normalized weighting reflecting priorities (coverage weighted highest here).

**Negative test:** weight only license price; you may pick a tool that misses half your estate — weight
**coverage** and **operability**.

**Cleanup:** none.

### Lab 2.3 — Score an option against the rubric

**Objective:** Turn judgment into a number.

```python
python3 - <<'PY'
weights = {"coverage":0.25,"visibility":0.15,"automation":0.15,"granularity":0.10,
           "scale":0.10,"failure_mode":0.05,"compliance":0.10,"tco":0.10}
# scores 1-5 for a hypothetical agentless option
scores = {"coverage":4,"visibility":4,"automation":5,"granularity":3,
          "scale":4,"failure_mode":3,"compliance":4,"tco":4}
total = sum(weights[k]*scores[k] for k in weights)
print(f"Weighted score: {total:.2f} / 5")
PY
```

```text
Weighted score: 4.00 / 5
```

**Expected result:** a single weighted score that makes options comparable.

**Negative test:** compare vendors by feature-count checklists; a weighted score against **your**
priorities is more honest than a longest-list-wins tally.

**Cleanup:** none.

### Lab 2.4 — Decide the failure mode

**Objective:** Choose fail-open vs fail-closed deliberately.

```python
python3 - <<'PY'
modes = {
  "fail-open":  "if enforcement breaks, traffic is ALLOWED — preserves uptime, loses containment",
  "fail-closed":"if enforcement breaks, traffic is DENIED — preserves containment, risks outage",
}
for m, effect in modes.items(): print(f"{m:12}: {effect}")
print("Choice: fail-open for availability-critical tiers; fail-closed for crown jewels / OT safety cases")
PY
```

**Expected result:** the two failure modes and where each fits — a deliberate design choice, not a
default.

**Negative test:** accept the vendor default failure mode without deciding; pick it per asset class to
match your risk.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsegmentation is enforced through eight models — network, hypervisor, host-agent, agentless
OS-firewall, EDR-leveraged, agentless appliance, cloud-native, and container/eBPF — each with distinct
trade-offs. A weighted rubric (coverage, visibility, automation, granularity, scale, failure mode,
compliance, TCO) tuned to your environment turns the comparison from opinion into a score.

- [ ] I can enumerate the enforcement models.
- [ ] I can map asset classes to models.
- [ ] I can build and apply a weighted scoring rubric.
- [ ] I can choose a failure mode deliberately.
- [ ] I completed Labs 2.1–2.4 including each negative test.
