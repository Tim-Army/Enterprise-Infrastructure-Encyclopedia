# Chapter 03: Network and Hypervisor-Based Options

## Learning Objectives

- Explain VMware NSX Distributed Firewall (DFW) microsegmentation.
- Explain Cisco ACI contract-based segmentation.
- Compare hypervisor and network-fabric enforcement.
- State the pros, cons, compatibility, and requirements of each.
- Complete a walkthrough for each network/hypervisor topic.

## Theory and Architecture

**Network- and hypervisor-based** microsegmentation enforces policy without touching the guest OS.
**VMware NSX** implements a **Distributed Firewall (DFW)**: a stateful firewall in every hypervisor
kernel that filters each VM's virtual NIC, with policy written against **security groups** and dynamic
membership (tags, VM names, OS) rather than IPs. Because enforcement is in the kernel, it is **agentless
for VMs** and runs at line rate; policy follows the VM across hosts (vMotion). **Cisco ACI** enforces in
the **network fabric**: workloads are placed in **Endpoint Groups (EPGs)**, and traffic between EPGs is
denied unless a **contract** permits it (an allowlist between groups) — a whitelist model at the fabric
level. Both keep enforcement off the workload, which is ideal where you cannot or will not install
agents — but each is bound to its platform (NSX to vSphere/NSX, ACI to the Cisco fabric).

## Pros, Cons, Compatibility, and Requirements

**VMware NSX DFW**

- **Pros:** agentless for VMs; kernel line-rate enforcement; policy follows the VM (vMotion); rich
  dynamic grouping (tags/name/OS); mature; multi-cloud via NSX. Good L4 and some L7 (context-aware,
  identity firewall, service insertion).
- **Cons:** VMware/vSphere-centric — limited for bare-metal, cloud-native, and OT/IoT outside NSX;
  requires NSX licensing and design maturity; subject to Broadcom/VMware licensing changes.
- **Compatibility:** vSphere VMs under NSX; containers/bare-metal via additional NSX components;
  multi-hypervisor limited.
- **Requirements:** NSX (Manager, control/data plane) on a supported vSphere estate; NSX licensing;
  distributed switch.

**Cisco ACI**

- **Pros:** enforcement in the fabric (no host touch); allowlist contracts between EPGs; strong for
  data-center east-west at scale; integrates with the Cisco ecosystem.
- **Cons:** requires the Cisco ACI fabric (Nexus 9000 + APIC); coarser than host/process-level; complex;
  data-center-bound (not cloud/OT/endpoint).
- **Compatibility:** workloads attached to the ACI fabric (physical or virtual); limited off-fabric.
- **Requirements:** ACI fabric (spine/leaf Nexus 9000, APIC controllers); EPG/contract design.

## Design Considerations

Use **NSX DFW** when your estate is VMware-heavy and you want agentless per-VM policy that follows
workloads. Use **ACI contracts** when segmentation should live in the data-center fabric and you already
run ACI. Neither covers cloud-native, endpoints, or OT well on its own — pair with another model
(Chapters 05–08) for full coverage. Model groups by **tag/EPG**, not IP, so policy survives change.

## Implementation and Automation

The labs model an NSX DFW security-group policy and an ACI contract, and compare the two enforcement
points — the network/hypervisor options in the rubric.

## Validation and Troubleshooting

Confirm network/hypervisor enforcement:

```text
NSX DFW: kernel firewall per vNIC; security groups (tags/name/OS); agentless for VMs; follows vMotion
Cisco ACI: EPGs + contracts (default-deny between EPGs); fabric enforcement; DC-bound
Both: off-workload enforcement; platform-bound (NSX=vSphere/NSX, ACI=Nexus/APIC)
```

Common pitfalls: writing NSX rules against **IP addresses** instead of dynamic groups (breaks on
change); and assuming ACI contracts cover endpoints/cloud they never see.

## Security and Best Practices

Off-host enforcement is a strength (nothing to tamper with on the workload) — protect the NSX Manager /
APIC controllers accordingly. Default-deny between groups/EPGs; allow only contracts you need. All work
is authorized administration of your own fabric.

## Hands-On Lab

Network/hypervisor walkthroughs. **Shared prerequisites** — `python3` (policy modeling; representative
NSX/ACI object structures). **Cost:** none.

### Lab 3.1 — Model an NSX DFW security-group policy

**Objective:** Write policy against dynamic groups, not IPs.

```python
python3 - <<'PY'
groups = {
  "sg-web": "tag == 'tier:web'",
  "sg-app": "tag == 'tier:app'",
  "sg-db":  "tag == 'tier:db'",
}
dfw = [
  ("sg-web","sg-app","tcp/8080","allow"),
  ("sg-app","sg-db","tcp/5432","allow"),
  ("any","sg-db","any","deny"),          # default-deny to the DB tier
]
for g,expr in groups.items(): print(f"{g}: {expr}")
for s,d,svc,act in dfw: print(f"DFW: {s} -> {d} {svc} {act}")
PY
```

**Expected result:** tier-to-tier allow rules with a default-deny to the DB, expressed by **tag** — NSX
membership updates automatically as VMs are tagged.

**Negative test:** pin rules to VM IPs; a re-IP or new VM slips policy — use **tag-based** security
groups.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Model a Cisco ACI contract

**Objective:** Allowlist traffic between EPGs.

```python
python3 - <<'PY'
epgs = ["epg-web", "epg-app", "epg-db"]
contracts = [
  ("epg-web","epg-app","http-8080"),
  ("epg-app","epg-db","pgsql-5432"),
]
print("EPGs:", ", ".join(epgs))
print("Default between EPGs: DENY (no contract = no traffic)")
for provider, consumer, c in contracts:
    print(f"Contract {c}: {consumer} --consumes--> {provider}")
PY
```

**Expected result:** contracts permitting only web→app and app→db; all other inter-EPG traffic denied by
default.

**Negative test:** put all workloads in one EPG for convenience; intra-EPG traffic is unrestricted —
separate tiers into distinct EPGs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Compare the two enforcement points

**Objective:** Match each to a fit.

```python
python3 - <<'PY'
compare = {
  "NSX DFW": {"where":"hypervisor kernel","agent":"none (for VMs)","best":"VMware-heavy VM estates"},
  "Cisco ACI":{"where":"network fabric","agent":"none","best":"Cisco DC fabric east-west"},
}
for tool, a in compare.items():
    print(f"{tool:10}: enforce@{a['where']:18} agent={a['agent']:12} best={a['best']}")
print("Neither covers cloud-native / endpoints / OT alone -> pair with another model")
PY
```

**Expected result:** the two off-host options contrasted, with the shared gap (cloud/endpoint/OT).

**Negative test:** rely on NSX or ACI alone for a hybrid estate with cloud and OT; add a complementary
model for those assets.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Reason about requirements and lock-in

**Objective:** Weigh platform requirements.

```python
python3 - <<'PY'
reqs = {
  "NSX DFW": ["NSX Manager + control/data plane","supported vSphere","NSX licensing"],
  "Cisco ACI":["Nexus 9000 spine/leaf","APIC controllers","EPG/contract design"],
}
for tool, r in reqs.items():
    print(f"{tool}: {'; '.join(r)}")
print("Trade-off: strong off-host enforcement, but bound to (and licensed for) the platform")
PY
```

**Expected result:** the platform requirements that come with each option — the cost of off-host
enforcement.

**Negative test:** plan NSX DFW without NSX licensing, or ACI without the fabric; both require their
platform — budget it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Network- and hypervisor-based microsegmentation enforces off the workload: NSX DFW filters each VM in
the hypervisor kernel with tag-based security groups (agentless for VMs, follows vMotion), and Cisco ACI
denies inter-EPG traffic without a contract in the fabric. Both are strong but platform-bound and need
pairing for cloud, endpoint, and OT coverage.

- [ ] I can explain NSX DFW and ACI contract enforcement.
- [ ] I can model a tag-based NSX policy and an ACI contract.
- [ ] I can state the pros, cons, compatibility, and requirements of each.
- [ ] I completed Labs 3.1–3.4 including each negative test.
