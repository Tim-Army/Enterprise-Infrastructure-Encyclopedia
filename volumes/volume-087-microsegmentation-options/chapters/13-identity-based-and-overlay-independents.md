# Chapter 13: Identity-Based and Overlay Independents

## Learning Objectives

- Explain Elisity's identity-based model and how it differs from Zero Networks.
- Explain the HIP-based encrypted overlay model as implemented by Tempered Airwall.
- Recognize vendors that are no longer viable options, and why they still appear in comparisons.
- Record cost model, implementation effort, FIPS, FedRAMP, and air-gap posture for each.
- Complete a walkthrough for each topic.

## Theory and Architecture

Beyond the large platform vendors sit independents that solved segmentation from a different starting
point. Two remain viable; two do not, and knowing which is which is the practical value of this chapter.

**Elisity** enforces identity-based policy through **existing access switches** — no agents, no new
inline hardware, no re-architecture. Its **IdentityGraph** aggregates the identity and behavior of every
asset discovered on the network, enriched with context from connected systems such as directory
services, EDR, and the CMDB, then pushes least-privilege policy down to the switching already in place.
It is the closest structural competitor to Zero Networks (Chapter 05): both are agentless and
identity-first, but Zero Networks enforces at the host firewall while Elisity enforces in the network
fabric, which is why Elisity reaches devices that have no host firewall to program.

**Tempered Airwall** implements a cryptographic overlay based on the **Host Identity Protocol (HIP)**.
Every protected endpoint sits behind an Airwall gateway, and communication is permitted only between
explicitly paired identities inside an encrypted overlay — devices are effectively invisible to anything
not in their overlay, which is a different guarantee from a firewall rule denying traffic. Policy is
managed from the **Airwall Conductor** console, which exposes an API. Tempered Networks was acquired by
**Johnson Controls** and embedded into the OpenBlue platform, and since 2023 Airwall has integrated with
**Nozomi Networks**, mirroring encrypted overlay traffic to Nozomi for analysis while remediation can be
driven back through the Conductor API.

### Options that are no longer viable

Two vendors appear in nearly every microsegmentation comparison written before 2025 and should no longer
be evaluated as products.

**vArmour — discontinued.** vArmour pioneered application relationship management and held a substantial
patent portfolio, but the company disbanded in August 2024 following its chief executive's departure. In
January 2025 **Fenix24 acquired the intellectual property and source code — explicitly not the team and
not the customer contracts** — and folded the technology into its Argos99 cyber-resilience and recovery
offering. There is no vArmour microsegmentation product to buy, and no vendor supporting one.

**Unisys Stealth — absorbed.** Stealth was an identity-driven, cryptographic microsegmentation product
with a long public reference history. Unisys no longer lists a product by that name; microsegmentation
now appears only as a capability inside a broader **Secure Network Access** managed service. If a
comparison or an incumbent proposal names Stealth as a shrink-wrapped product, it is working from stale
information.

The lesson generalizes: microsegmentation has consolidated hard, and a vendor's presence in a two-year-old
analyst grid says nothing about whether you can buy and be supported on it today. Confirm current
product status before shortlisting, every time.

## Pros, Cons, Compatibility, and Requirements

- **Pros (Elisity):** agentless and hardware-neutral, reusing installed switching; identity built from
  systems you already run; reaches unmanaged and OT devices that cannot host software; vendor positions
  deployment in weeks rather than quarters.
- **Cons (Elisity):** enforcement granularity is bounded by what the switch can express; depends on the
  quality of the identity sources feeding IdentityGraph; a smaller company than the platform vendors,
  which matters for multi-year procurement risk.
- **Pros (Airwall):** identity-based encrypted overlay makes protected devices unaddressable rather than
  merely filtered; excellent for legacy and remote OT assets and for traffic crossing untrusted
  networks; strong OT integration story.
- **Cons (Airwall):** requires gateways in the path — this is inline hardware or software to deploy and
  operate; the overlay is a parallel network to run; now positioned within a building-systems portfolio
  rather than as a general-purpose enterprise product.
- **Compatibility:** Elisity works with mainstream campus switching (Cisco, Juniper, Arista). Airwall
  supports physical, virtual, and cloud gateways fronting essentially any IP device.
- **Requirements:** Elisity needs supported switching plus identity sources. Airwall needs Conductor
  plus a gateway in front of everything protected.

**Cost model.** Neither publishes list pricing. Elisity quotes by deployment size, endpoint count,
feature set, and subscription term. Airwall is quoted through Johnson Controls channels. Treat both as
**quote required**, and for Airwall include the gateway hardware in the model.

**Implementation time (estimate, not a vendor commitment).** Elisity is among the faster options because
it installs nothing on endpoints and adds no inline hardware — **4–10 weeks** to discovery and initial
enforcement on a supported access layer is realistic; the vendor claims "weeks." Airwall is gated by
gateway placement: **6–16 weeks**, longer where gateways must be installed at remote or industrial
sites.

**FIPS 140-3.** A CMVP search for **Elisity returns no validated modules**. Verify Airwall's current
status, and any Elisity change, directly in the
[NIST CMVP list](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search)
before relying on either in a regulated environment.

**FedRAMP.** No FedRAMP listing was found for either vendor. Check the
[FedRAMP Marketplace](https://marketplace.fedramp.gov/) for current status before a federal engagement;
absence of a listing means the service cannot be used for federal data at the corresponding impact
level, not merely that it is undocumented.

**Air-gap.** Airwall is strong: the overlay is self-contained and Conductor can run on-premises, which
suits disconnected industrial sites. Elisity's control plane is cloud-delivered, so a fully air-gapped
deployment requires explicit confirmation from the vendor — do not assume it.

## Design Considerations

Elisity earns a place on the shortlist when the estate is switch-rich, agent-hostile, and needs results
quickly — particularly healthcare and manufacturing campuses. Airwall earns one when assets must be made
invisible rather than merely filtered, or when protected traffic crosses networks you do not control.

Weigh vendor longevity explicitly for independents. The evidence in this chapter is that two of four
independents from the previous generation no longer exist as products; assume a multi-year commitment
carries that risk and ask for a written statement of product roadmap and support term.

## Implementation and Automation

Both expose APIs — Elisity for policy and identity, Airwall through the Conductor API. Keep policy in
version control and drive it programmatically. For Airwall, automate overlay membership from the same
inventory that drives the rest of your segmentation, so one source of truth defines who may talk.

## Validation and Troubleshooting

For Elisity, validate the identity first: if IdentityGraph has the asset in the wrong group, the policy
was never wrong. For Airwall, validate overlay membership and pairing before examining rules — a device
outside the overlay is not blocked by policy, it is simply unreachable, which produces different
symptoms.

## Security and Best Practices

Protect the identity sources: in an identity-based model, write access to the CMDB or directory is
equivalent to write access to firewall policy. Retain an out-of-band path. For overlays, plan
certificate and pairing lifecycle before deployment, not after.

## Hands-On Lab

### Lab 13.1 — Compare agentless enforcement points

**Objective.** Distinguish Elisity from Zero Networks on the one axis that matters.

```python
assets = {"windows server": "has host firewall", "linux server": "has host firewall",
          "mri scanner": "no host firewall", "plc": "no host firewall",
          "ip camera": "no host firewall"}
for a, cap in assets.items():
    host_fw = cap == "has host firewall"
    print(f"{a:<16}{cap:<20}zero-networks: {'yes' if host_fw else 'NO':<4}elisity: yes")
```

**Expected result.** Both cover the servers; only the fabric-enforced option covers the three devices
with no host firewall to program.

**Negative test.** Assume "agentless" means "covers everything." It does not — agentless describes what
is *installed*, not where enforcement *happens*. Ask where the rule lands.

**Cleanup.** None.

### Lab 13.2 — Model overlay invisibility versus filtering

**Objective.** Show why HIP overlay membership differs from a deny rule.

```python
def firewall(src, dst, allowed):
    return "REACHABLE (blocked at port)" if not allowed else "REACHABLE"
def overlay(src_in, dst_in):
    return "REACHABLE" if (src_in and dst_in) else "NOT ADDRESSABLE (no overlay path)"
print("firewall model:", firewall("scanner", "plc", allowed=False))
print("overlay model: ", overlay(src_in=False, dst_in=True))
```

**Expected result.** The firewall model leaves the target discoverable and blocked; the overlay model
leaves it unaddressable — a scanner sees nothing to attack.

**Negative test.** Treat the two as equivalent in a risk assessment. They differ in attack surface:
blocked-but-visible still exposes the stack to whatever reaches the port.

**Cleanup.** None.

### Lab 13.3 — Check vendor viability before shortlisting

**Objective.** Make product-status verification a required step.

```python
candidates = {
    "Elisity":        {"status": "current",    "vendor": "Elisity"},
    "Tempered Airwall": {"status": "current",  "vendor": "Johnson Controls"},
    "vArmour":        {"status": "discontinued", "vendor": "IP held by Fenix24"},
    "Unisys Stealth": {"status": "absorbed",   "vendor": "Unisys (managed service only)"},
}
for name, c in candidates.items():
    verdict = "SHORTLIST" if c["status"] == "current" else "REJECT - " + c["status"]
    print(f"{name:<18}{c['vendor']:<32}{verdict}")
```

**Expected result.** Two shortlisted, two rejected — half of the previous generation of independents.

**Negative test.** Build the shortlist from a two-year-old analyst grid without checking status. Two of
four entries cannot be bought or supported, and you discover it during procurement.

**Cleanup.** None.

### Lab 13.4 — Score the independents against the rubric

**Objective.** Score this tier on the five **constraint axes** used across Chapters 10–15 — a deliberate reduction of Chapter 02's eight-dimension rubric that promotes air-gap capability to a first-class axis, because it disqualifies options outright rather than merely scoring them.

```python
weights = {"agentless": 0.30, "granularity": 0.25, "coverage": 0.20,
           "air_gap": 0.15, "effort": 0.10}
options = {"elisity": {"agentless": 5, "granularity": 3, "coverage": 4, "air_gap": 2, "effort": 4},
           "airwall": {"agentless": 4, "granularity": 4, "coverage": 3, "air_gap": 5, "effort": 2}}
for name, s in options.items():
    print(f"{name:<10}{sum(weights[k] * s[k] for k in weights):.2f} / 5.00")
```

**Expected result.** elisity 3.75, airwall 3.75 — tied overall, for opposite reasons: Elisity on speed
and reach, Airwall on air-gap and enforcement strength.

**Negative test.** Pick on total score alone. A tie hides the fact that one is disqualified outright in
a disconnected site; read the component scores against your constraints.

**Cleanup.** None.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Elisity enforces identity-based policy through switching you already own, and Tempered Airwall makes
protected devices unaddressable inside a HIP overlay — while vArmour and Unisys Stealth, still common in
older comparisons, are no longer products you can buy, which makes verifying current vendor status a
mandatory step rather than a courtesy.

- [ ] I can explain where Elisity enforces and why that differs from Zero Networks.
- [ ] I can explain overlay invisibility versus filtering.
- [ ] I can state the current status of vArmour and Unisys Stealth and its procurement consequence.
- [ ] I completed Labs 13.1–13.4 including each negative test.
