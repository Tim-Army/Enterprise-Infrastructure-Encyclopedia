# Chapter 14: OT and Cyber-Physical Segmentation

## Learning Objectives

- Explain why OT segmentation is a different problem from IT segmentation.
- Describe Xage, Claroty xDome, Nozomi Networks, TXOne, and Zscaler/Airgap as OT options.
- Distinguish visibility-and-detection platforms from enforcement platforms.
- Record cost model, implementation effort, FIPS, FedRAMP, and air-gap posture for each.
- Complete a walkthrough for each topic.

## Theory and Architecture

Operational technology inverts the priorities of IT security. Availability outranks confidentiality,
because stopping the plant is the incident. Devices run for decades, cannot be patched, cannot host
software, and often cannot tolerate an unexpected packet, let alone an active scan. Any segmentation
approach that assumes an agent, a maintenance window, or an aggressive discovery scan is inapplicable.

The vendors in this space divide into two groups that are frequently conflated.

**Visibility and detection.** **Nozomi Networks** and **Claroty** built their reputations on passive
monitoring: span or tap the traffic, fingerprint devices and protocols without touching them, build an
asset inventory, and detect anomalies. Claroty's **xDome** extends this into cyber-physical systems
management. This tier tells you what exists and what talks to what — the indispensable input to any
segmentation design — and increasingly recommends the policy, but the *enforcement* usually happens in
someone else's device.

**Enforcement.** **Xage Security** takes an identity-first approach with a distributed fabric that
brokers access to OT assets, enforcing authentication and authorization in front of equipment that has
none of its own. **TXOne Networks**, from a Trend Micro joint venture, focuses on OT endpoint and
network protection built for industrial constraints, including protection for un-patchable machines.
**Zscaler**, having acquired **Airgap Networks** in April 2024, offers agentless segmentation using an
intelligent **DHCP-proxy architecture** to isolate every device and control access by identity and
context, packaged with a **ransomware kill switch** that halts lateral movement without disrupting
operations. Chapter 07's ColorTokens Gatekeeper belongs to this group as well.

The practical architecture in most plants combines both: a passive platform supplies the asset inventory
and flow map, and an enforcement mechanism — a gateway, a broker, or the fabric of Chapter 10 — applies
the policy that inventory justifies.

## Pros, Cons, Compatibility, and Requirements

- **Pros:** built for devices that cannot host an agent; passive discovery is safe on fragile networks;
  deep industrial protocol awareness (Modbus, DNP3, EtherNet/IP, S7, BACnet) that IT tools lack;
  purpose-built for availability-first change control.
- **Cons:** the visibility tier does not enforce, and buying it expecting segmentation is the most
  common disappointment in this market; enforcement options put a device in the path of a process that
  cannot stop; industrial protocol coverage varies by vendor and by plant, so proof-of-concept on your
  own equipment is mandatory.
- **Compatibility:** all support passive span/tap collection; enforcement options need a defensible
  choke point — the Chapter 10 fabric, a gateway, or a broker. Zscaler/Airgap requires control of DHCP,
  which is a genuine architectural dependency to confirm early.
- **Requirements:** span/tap access or a network capture point; an asset inventory; and agreement with
  operations on a change window and rollback plan before any enforcement is enabled.

**Cost model.** None of these vendors publishes list pricing; all are quoted by site, asset count, or
throughput. Budget for professional services — in OT, deployment services are frequently a larger line
item than licenses, because the work is site surveys and process negotiation rather than software.

**Implementation time (estimate, not a vendor commitment).** Passive visibility is quick: **2–6 weeks**
per site to tap, collect, and produce an inventory. Enforcement is slow and governed by plant change
control, not technology: **6–18 months** for a multi-site industrial estate, with per-cell cutovers
scheduled around planned outages. Any plan that promises enforcement across a plant in weeks has not met
the operations team.

**FIPS 140-3.** Verified in the NIST CMVP registry:

- **Xage Security — validated.** Certificate **#5229**, *Xage Cryptographic Module for OpenSSL*,
  **FIPS 140-3**, validated **7 April 2026** (superseding certificate #4620 under FIPS 140-2, 29
  September 2023).
- **Nozomi Networks — no CMVP results** were returned for the vendor name at the time of writing.
- Claroty, TXOne, and Zscaler: verify the specific product and firmware in the
  [NIST CMVP list](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search).

**FedRAMP.** Status differs sharply and the distinction is consequential:

- **Claroty xDome for Government — *In Process*, not authorized.** The FedRAMP Marketplace records it at
  impact level **High**, Agency authorization path, Rev5, in the *Initial Implementation* phase with
  **zero ATO/ATU letters** as of 20 February 2026
  ([listing](https://www.fedramp.gov/marketplace/products/FR2323961436/)). "In Process" permits no
  federal use; only an authorization does.
- **Zscaler** maintains authorized government offerings, including Zscaler Private Access — Government
  ([listing](https://www.fedramp.gov/marketplace/products/FR1719759604/)); confirm the specific
  segmentation service you intend to buy is in scope of that authorization.
- Xage, Nozomi, and TXOne: check the [FedRAMP Marketplace](https://marketplace.fedramp.gov/) for current
  status.

**Air-gap.** This tier is the best represented, because many industrial sites are genuinely
disconnected. Nozomi, Claroty, TXOne, and Xage all support on-premises deployment with offline updates;
confirm the *update path* for threat content, since the value of detection decays without it. Cloud-only
management planes are the exception to watch for, and Zscaler's model is cloud-delivered by design —
confirm the on-premises enforcement story before assuming it fits a disconnected plant.

## Design Considerations

Decide explicitly whether you are buying visibility or enforcement, and write it down. Most OT programs
should buy visibility first, use it for a full production cycle, and only then choose an enforcement
mechanism — which may well be the fabric or gateway you already own rather than another product.

Never enable enforcement in an OT cell without an agreed rollback and a rehearsed break-glass. Chapter
09's rollout guidance applies with more force here, because the failure mode is a stopped process rather
than a failed login.

## Implementation and Automation

Feed the asset inventory from the visibility platform into the policy model as data, not as a report.
Both Claroty and Nozomi expose APIs; export the device and flow inventory, generate the group-to-group
matrix from Chapter 10's Lab 10.1, and review it with operations before it becomes policy.

## Validation and Troubleshooting

Validate that the passive collector sees the traffic you think it does — a span port configured on the
wrong VLAN produces a confident, incomplete inventory, which is worse than none. For enforcement,
validate the permitted control flow first and continuously, then the denials.

## Security and Best Practices

Keep enforcement out of band from safety systems. Preserve a documented manual override. Treat the
inventory as sensitive: a complete map of an industrial estate is itself a target, and it should not
leave the environment without a decision.

## Hands-On Lab

### Lab 14.1 — Separate visibility from enforcement

**Objective.** Classify each option by what it actually does.

```python
options = {
    "Nozomi Networks": ("visibility/detection", "enforces via integrations"),
    "Claroty xDome":   ("visibility/detection", "enforces via integrations"),
    "Xage Security":   ("enforcement", "identity broker in front of assets"),
    "TXOne":           ("enforcement", "OT endpoint and network protection"),
    "Zscaler/Airgap":  ("enforcement", "agentless via DHCP-proxy isolation"),
}
for name, (tier, how) in options.items():
    print(f"{name:<18}{tier:<22}{how}")
```

**Expected result.** Two visibility platforms, three enforcement platforms.

**Negative test.** Buy a visibility platform to "do microsegmentation." You will end the project with an
excellent inventory and no enforcement — the single most common OT procurement error.

**Cleanup.** None.

### Lab 14.2 — Check the DHCP dependency before designing

**Objective.** Test an architectural prerequisite that is easy to miss.

```python
sites = {"plant-a": {"dhcp": "central, we control"}, "plant-b": {"dhcp": "static addressing only"},
         "plant-c": {"dhcp": "vendor-managed PLC network"}}
for site, cfg in sites.items():
    ok = cfg["dhcp"] == "central, we control"
    print(f"{site:<10}{cfg['dhcp']:<32}{'DHCP-proxy model viable' if ok else 'NOT VIABLE - choose another mechanism'}")
```

**Expected result.** One of three sites supports the model; two need a different mechanism.

**Negative test.** Standardize on a DHCP-proxy approach estate-wide after a successful pilot at
plant-a. Two plants cannot adopt it — statically addressed and vendor-managed networks have no DHCP to
proxy. Confirm per site.

**Cleanup.** None.

### Lab 14.3 — Read a FedRAMP status correctly

**Objective.** Distinguish authorized from in-process before making a federal commitment.

```python
listings = {
    "Illumio Government Cloud": {"status": "Authorized", "level": "Moderate", "atos": 1},
    "Claroty xDome for Government": {"status": "In Process", "level": "High", "atos": 0},
}
for name, l in listings.items():
    usable = l["status"] == "Authorized" and l["atos"] >= 1
    print(f"{name:<32}{l['status']:<12}{l['level']:<10}ATOs={l['atos']}  "
          f"{'usable for federal data' if usable else 'NOT usable yet'}")
```

**Expected result.** One authorized and usable; one in process with zero ATOs and not usable.

**Negative test.** Treat a Marketplace listing as authorization. "In Process" appears on the same site
and looks similar at a glance; the status field and ATO count are what matter.

**Cleanup.** None.

### Lab 14.4 — Score the OT tier against the rubric

**Objective.** Score this tier on the five **constraint axes** used across Chapters 10–15 — a deliberate reduction of Chapter 02's eight-dimension rubric that promotes air-gap capability to a first-class axis, because it disqualifies options outright rather than merely scoring them.

```python
weights = {"agentless": 0.30, "granularity": 0.25, "coverage": 0.20,
           "air_gap": 0.15, "effort": 0.10}
ot = {"agentless": 5, "granularity": 3, "coverage": 3, "air_gap": 5, "effort": 1}
print(f"weighted score: {sum(weights[k] * ot[k] for k in weights):.2f} / 5.00")
```

**Expected result.** 3.70 — excellent agentless reach and air-gap support, worst-in-volume on effort,
which is an accurate reflection of plant change control.

**Negative test.** Drop the `effort` weight to zero and the tier looks unbeatable. Effort is precisely
what determines whether an OT program finishes; do not weight it away.

**Cleanup.** None.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OT segmentation splits into visibility platforms that map the estate and enforcement platforms that
constrain it; the tier is unmatched for agentless reach and disconnected operation, but is governed by
plant change control rather than technology, and its compliance posture must be read precisely — Xage
holds a current FIPS 140-3 certificate, while Claroty's federal offering is in process rather than
authorized.

- [ ] I can distinguish visibility platforms from enforcement platforms.
- [ ] I can test the DHCP-proxy architectural dependency per site.
- [ ] I can read a FedRAMP listing and tell authorized from in process.
- [ ] I completed Labs 14.1–14.4 including each negative test.
