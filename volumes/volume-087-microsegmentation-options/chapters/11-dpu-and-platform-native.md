# Chapter 11: DPU-Accelerated and Platform-Native Segmentation

## Learning Objectives

- Explain why DPU/SmartNIC offload is a distinct enforcement model, not a faster host agent.
- Describe the HPE Aruba CX 10000 with AMD Pensando and the NVIDIA BlueField approach.
- Explain Nutanix Flow Network Security and its Prism Central scoping constraint.
- Record cost model, implementation effort, FIPS, FedRAMP, and air-gap posture for each.
- Complete a walkthrough for each topic.

## Theory and Architecture

Two models sit between the fabric of Chapter 10 and the host agents of Chapter 04, and both belong to
the platform rather than to the workload.

**DPU/SmartNIC offload** puts a stateful firewall in programmable silicon in the data path. The
**HPE Aruba CX 10000** pairs the AOS-CX network operating system with a fully programmable **AMD
Pensando DPU**, delivering stateful services inline at wire rate: the CX 10040 provides **8 Tbps of
switching capacity with 1.6 Tbps of L4 stateful inspection**, extending a leaf-spine fabric with
distributed microsegmentation, east-west firewalling, NAT, encryption, and telemetry on every port.
**NVIDIA BlueField** takes the same idea to the server NIC, running enforcement on the DPU's own cores
and operating system so that policy executes beside the workload but outside it — invisible to, and
uncompromisable by, the host OS.

This is not merely a performance optimization. It changes the trust boundary. A host agent shares fate
with the operating system it protects; if the host is fully compromised, the agent is compromised with
it. A DPU enforces from a separate execution domain the host does not control. That property is the
reason to consider the model at all, and it is what you are paying for.

**Nutanix Flow Network Security** is the platform-native option for AHV. Policy and visibility live in
**Prism Central**, and enforcement is applied to every AHV host it manages, using categories rather than
addresses. It sits in the hypervisor tier beside VMware NSX (Chapter 03) but is tied to the Nutanix
platform.

## Pros, Cons, Compatibility, and Requirements

- **Pros (DPU):** wire-rate stateful enforcement with no host CPU cost; enforcement outside the host's
  trust domain; per-port east-west policy without hairpinning to a firewall; telemetry from the data
  path itself.
- **Cons (DPU):** requires specific hardware — this is a purchase decision, not a software rollout;
  smaller operational ecosystem than mature agent platforms; the enforcement point is the switch or NIC,
  so it protects north of the workload, not inside it.
- **Pros (Nutanix Flow):** no third-party agent; policy in the platform console administrators already
  use; categories decouple policy from addressing; strong fit where AHV is already standard.
- **Cons (Nutanix Flow):** **AHV only**; a per-node license for every node in a protected cluster; and
  **categories and security policies do not replicate between Prism Central instances** — a real
  constraint for disaster-recovery designs, where the second site needs its policy rebuilt or
  synchronized externally.
- **Compatibility:** CX 10000 requires that switch series; BlueField requires supported servers and a
  supported enforcement stack; Flow requires AHV plus Prism Central (Starter license or above).
- **Requirements:** hardware first, then a policy plane, then a discovery period. All three assume an
  accurate inventory.

**Cost model.** The CX 10000 is a switch purchase with **published list pricing on the HPE Store**,
which makes it one of the few options in this volume where a real number can be obtained without a sales
conversation. BlueField pricing is per adapter through server vendors. **Nutanix Flow Network Security
is an annual per-node subscription, sold in 1–5 year terms, and licenses are required for every node in
any cluster where microsegmentation is used** — partial licensing of a cluster is not a design.

**Implementation time (estimate, not a vendor commitment).** DPU options are gated by procurement and
change windows rather than software: **3–6 months** including hardware lead time, or a data-center
refresh cycle if aligned to one. Nutanix Flow on an existing AHV estate is far quicker — **2–6 weeks**
to categorize workloads, run policies in monitor mode, and enforce.

**FIPS 140-3.** Verify per platform and firmware in the
[NIST CMVP list](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search);
DPU-based encryption in particular is validated against the specific silicon and firmware build, so a
vendor-level claim tells you nothing about the model you are buying.

**FedRAMP.** All three are deployed on customer premises and are outside FedRAMP's scope as products.
Where a cloud-hosted management plane is used, check that service in the
[FedRAMP Marketplace](https://marketplace.fedramp.gov/).

**Air-gap.** Strong. The CX 10000 and BlueField enforce entirely on-premises. Nutanix Flow requires
Prism Central, which supports on-premises deployment with offline licensing — Flow's scoping constraint,
not connectivity, is the thing to design around in a disconnected site.

## Design Considerations

Choose a DPU when the workloads are dense and east-west traffic is heavy enough that hairpinning to a
firewall is untenable, or when the threat model includes a fully compromised host. Choose Nutanix Flow
when AHV is the standard and you want segmentation without introducing a second vendor.

For DR designs on Nutanix, decide early how policy reaches the second Prism Central. Discovering after
a failover that the recovery site has no policy is the failure mode this constraint produces.

## Implementation and Automation

Both models are driven from a policy plane with an API — Prism Central for Flow, CloudVision or the
switch API for the CX 10000. Express policy as code against categories or groups, keep it in version
control, and let the platform compile it to enforcement rules.

## Validation and Troubleshooting

Validate that enforcement is actually happening in the DPU rather than falling back to software: check
session tables and counters on the enforcement device, not just the policy console. For Flow, confirm a
VM's category membership before debugging the rule — most "policy not applied" tickets are a VM that
never received its category.

## Security and Best Practices

Keep an out-of-band management path that policy cannot deny. Patch DPU firmware on the same cadence as
the host — an enforcement point outside the host's trust domain is only trustworthy while it is patched.
Monitor first; enforce after a full business cycle.

## Hands-On Lab

### Lab 11.1 — Reason about the DPU trust boundary

**Objective.** State precisely what a DPU protects that a host agent does not.

```python
scenarios = [
    ("malware in userspace",        "agent: enforces", "dpu: enforces"),
    ("kernel rootkit on the host",  "agent: COMPROMISED", "dpu: enforces"),
    ("hypervisor escape",           "agent: COMPROMISED", "dpu: enforces"),
    ("compromised DPU firmware",    "agent: enforces", "dpu: COMPROMISED"),
]
for s, a, d in scenarios:
    print(f"{s:<28}{a:<22}{d}")
```

**Expected result.** The DPU survives host compromise; the agent survives DPU compromise. Neither is
unconditionally superior — they fail in different places.

**Negative test.** Argue a DPU makes host hardening unnecessary. The last row disproves it: unpatched
DPU firmware is an enforcement point you no longer control, and it is not visible to host tooling.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 11.2 — Size CX 10000 stateful inspection capacity

**Objective.** Check a published capacity figure against a real east-west load.

```python
L4_STATEFUL_TBPS = 1.6           # published for CX 10040
racks, gbps_per_rack = 18, 65
demand_tbps = racks * gbps_per_rack / 1000
print(f"east-west demand: {demand_tbps:.2f} Tbps   inspection capacity: {L4_STATEFUL_TBPS} Tbps")
print("WITHIN CAPACITY" if demand_tbps <= L4_STATEFUL_TBPS else "EXCEEDS - add switches or reduce scope")
```

**Expected result.** 1.17 Tbps against 1.6 Tbps — within capacity.

**Negative test.** Raise `gbps_per_rack` to 95. Demand becomes 1.71 Tbps and exceeds inspection
capacity; enforcement, not switching, is the bottleneck. Size on the stateful figure, never the
switching figure.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 11.3 — Model the Nutanix Flow DR scoping constraint

**Objective.** Expose the Prism Central boundary before it surprises you in a failover.

```python
prism_central = {
    "pc-primary": {"clusters": ["prod-a", "prod-b"], "policies": ["ringfence-db", "deny-hmi-to-it"]},
    "pc-dr":      {"clusters": ["dr-a"],             "policies": []},
}
for pc, cfg in prism_central.items():
    print(f"{pc:<12}clusters={cfg['clusters']}  policies={len(cfg['policies'])}")
missing = set(prism_central['pc-primary']['policies']) - set(prism_central['pc-dr']['policies'])
print(f"\npolicies absent at DR after failover: {sorted(missing)}")
```

**Expected result.** Both policies are absent at the DR site — categories and policies do not replicate
between Prism Central instances.

**Negative test.** Assume replication happens because the clusters replicate. Fail over and the
recovered workloads run unsegmented. Rebuild or synchronize policy at the second Prism Central
explicitly.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 11.4 — Score DPU and platform-native against the rubric

**Objective.** Score this tier on the five **constraint axes** used across Chapters 10–15 — a deliberate reduction of Chapter 02's eight-dimension rubric that promotes air-gap capability to a first-class axis, because it disqualifies options outright rather than merely scoring them.

```python
weights = {"agentless": 0.30, "granularity": 0.25, "coverage": 0.20,
           "air_gap": 0.15, "effort": 0.10}
options = {
    "dpu":          {"agentless": 5, "granularity": 4, "coverage": 3, "air_gap": 5, "effort": 2},
    "nutanix_flow": {"agentless": 5, "granularity": 3, "coverage": 2, "air_gap": 4, "effort": 4},
}
for name, s in options.items():
    print(f"{name:<14}{sum(weights[k] * s[k] for k in weights):.2f} / 5.00")
```

**Expected result.** dpu 3.95, nutanix_flow 3.65 — the DPU leads on granularity and air-gap, Flow on
effort.

**Negative test.** Set `coverage` weight to 0.50 and both fall behind a host agent, which reaches
workloads neither model can. Coverage breadth is where platform-native options lose.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

DPU-accelerated enforcement moves policy into programmable silicon outside the host's trust domain,
buying wire-rate east-west inspection and survivability against host compromise at the price of specific
hardware; Nutanix Flow delivers hypervisor-native segmentation for AHV estates quickly, provided the
design accounts for per-node licensing and the Prism Central policy boundary.

- [ ] I can explain why a DPU is a distinct trust boundary, not a faster agent.
- [ ] I can size a design against published stateful-inspection capacity.
- [ ] I can state the Prism Central scoping constraint and its DR consequence.
- [ ] I completed Labs 11.1–11.4 including each negative test.
