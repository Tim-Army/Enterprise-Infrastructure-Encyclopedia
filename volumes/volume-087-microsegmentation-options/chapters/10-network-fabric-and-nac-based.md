# Chapter 10: Network-Fabric and NAC-Based Segmentation

## Learning Objectives

- Explain group-tag segmentation, where the tag is assigned and where it is enforced.
- Compare the fabric options: Cisco TrustSec, Arista MSS, HPE Aruba, Juniper, Fortinet, Check Point.
- State the switch-hardware gate that decides whether a fabric option is viable at all.
- Record cost model, implementation effort, FIPS, FedRAMP, and air-gap posture for each.
- Complete a walkthrough for each fabric topic.

## Theory and Architecture

Fabric-based microsegmentation moves enforcement off the workload and into the network the workload is
already attached to. Nothing is installed on the host, which is the entire appeal for estates full of
appliances, medical devices, and machines nobody will let you touch.

**Cisco TrustSec** is the reference implementation of the *group-tag* model. Identity Services Engine
(ISE) authenticates an endpoint (802.1X or MAB), assigns it a **Security Group Tag (SGT)**, propagates
the tag either inline in the frame or out-of-band via **SXP**, and enforces it at the egress device with
a **Security Group ACL (SGACL)**. Policy is written as group-to-group — "Medical-Device may reach
Imaging-Server on 104/tcp" — and survives re-addressing, which is the point.

**Arista MSS-Group** implements the same idea on EOS switches with **CloudVision** as the policy plane —
MSS Studio, Policy Manager, Policy Builder, Policy Monitor, and the MSS Dashboard — backed by Arista's
NetDL state store. Groups are discovered dynamically from identity sources including Arista AGNI, VMware
vCenter, ServiceNow, Infoblox, and plain CSV, so an existing CMDB becomes the group definition.

**HPE Aruba** splits into two products. Campus **dynamic segmentation** pairs ClearPass policy with
AOS-CX switches and tunnels traffic to a gateway for enforcement. The data-center answer is the **CX
10000** covered in Chapter 11, which is a different model entirely because enforcement happens in
silicon.

**Juniper** offers Connected Security with **cSRX** containerized firewalls for east-west inspection and
**Apstra** intent-based fabric policy. **Fortinet** does internal segmentation with **VDOMs** and the
internal segmentation firewall (ISFW) pattern, tying identity in through FortiNAC. **Check Point
CloudGuard** provides east-west inspection for virtualized and cloud fabrics under the same policy
console as the perimeter estate.

## Pros, Cons, Compatibility, and Requirements

- **Pros:** no agent, so unmanaged and unpatchable devices are covered; enforcement is line-rate; policy
  is decoupled from IP addressing; one policy plane for campus and data center; usually reuses switching
  the organization already owns and staffs.
- **Cons:** coverage stops at the network — traffic that never crosses an enforcement point (same-host
  VM-to-VM, same-port devices) is invisible; policy granularity is coarser than a host agent's
  per-process view; **hardware support is a hard gate**; multi-vendor estates fragment the model.
- **Compatibility:** Cisco inline tagging requires Catalyst 9200/9300/9400/9500 or Nexus 9000 — Catalyst
  3850, 4500, and most third-party switches **do not** support it, forcing SXP and its scale limits.
  Arista MSS requires EOS switches plus CloudVision. Aruba dynamic segmentation requires AOS-CX plus
  ClearPass.
- **Requirements:** an identity source (802.1X/MAB, or a CMDB feed); a policy plane (ISE, CloudVision,
  ClearPass); switch models on the supported list; and an accurate device inventory before any policy is
  written.

**Cost model.** Cisco TrustSec requires **ISE Advantage licensing, priced per endpoint** measured as
concurrent active sessions — a 10,000-endpoint campus needs 10,000 Advantage licenses. Arista MSS
licensing is not publicly published (CloudVision subscription plus EOS features; quote required).
Aruba, Juniper, Fortinet, and Check Point all quote per appliance or per subscription; none publish list
pricing for the segmentation capability alone. Budget the *switch refresh* separately — for many
estates it dominates the software cost.

**Scale limits worth knowing.** A standalone ISE 3595 supports a maximum of **20,000 SXP bindings**. In
an estate where inline tagging is unavailable, that ceiling — not the license count — is what caps the
design.

**Implementation time (estimate, not a vendor commitment).** Fabric segmentation is gated by device
onboarding, not by software installation. A realistic campus rollout runs **3–9 months**: inventory and
identity first, then monitor-only tagging, then enforcement ring by ring. Data-center fabric policy on
an already-instrumented estate is faster, **6–12 weeks**.

**FIPS 140-3.** All of these vendors maintain CMVP validations, but validation is granted per platform
and firmware version, not per feature. Never accept a datasheet claim — search the vendor and the exact
model in the
[NIST CMVP validated modules list](https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search)
and match the firmware you will actually run.

**FedRAMP.** Fabric switching is on-premises and therefore out of FedRAMP scope; FedRAMP applies to the
vendors' SaaS control planes (CloudVision as-a-Service, cloud-hosted ClearPass, Fortinet and Check Point
cloud management). Check the specific service in the
[FedRAMP Marketplace](https://marketplace.fedramp.gov/) rather than assuming the vendor's authorization
covers the management plane you intend to use.

**Air-gap.** This tier is the strongest of any in this volume for disconnected sites. ISE, CloudVision,
ClearPass, Apstra, and FortiManager all support fully on-premises deployment with offline licensing and
manual signature/update import. Where a vendor's SaaS-only control plane is the sole option, the answer
becomes no — which is exactly why CloudVision-on-premises matters for classified estates.

## Design Considerations

Choose this tier when the assets cannot take an agent and you already own the switching. Do not choose
it expecting host-level granularity. The decisive question is not which vendor — it is **which switches
are installed**, because the tag must be carried and enforced by hardware that understands it. Survey
the access layer before shortlisting anything.

The second question is where enforcement happens relative to the threat. A tag enforced only at the
distribution layer does nothing about two infected devices on the same access switch port group. Ask the
vendor to state, precisely, which traffic paths are enforced and which are not.

## Implementation and Automation

Model the policy as a group-to-group matrix before touching a switch: source group, destination group,
protocol, port, decision. That matrix is portable across all six vendors and is what you will hand to
the policy plane. Build it from observed flows, never from memory of what the application "should" do.

## Validation and Troubleshooting

Validate in three places, in order: the tag was assigned (check the authentication session), the tag
arrived (check the SGT/group on the enforcing device), and the policy matched (check counters on the
SGACL or group policy). Most failures are the middle step — the tag was assigned but never propagated,
because one switch in the path does not carry it.

## Security and Best Practices

Run monitor-only long enough to see a full business cycle, including month-end and backup windows.
Retain an out-of-band management path that no group policy can deny. Treat the identity source as
security-critical: whoever can change a device's group membership can change its permissions.

## Hands-On Lab

### Lab 10.1 — Build a group-to-group policy matrix

**Objective.** Produce the vendor-neutral artifact every fabric option consumes.

```python
groups = ["hmi", "plc", "app", "db", "it-laptop"]
allow = {("hmi", "plc"): "tcp/502", ("app", "db"): "tcp/5432"}
print(f"{'src':<10}{'dst':<10}{'decision'}")
for s in groups:
    for d in groups:
        if s == d:
            continue
        rule = allow.get((s, d))
        print(f"{s:<10}{d:<10}{'ALLOW ' + rule if rule else 'DENY'}")
```

**Expected result.** Twenty ordered pairs, two allowed, eighteen denied — a default-deny matrix.

**Negative test.** Add `("it-laptop", "plc"): "tcp/502"` and re-run. An IT laptop may now reach an
industrial controller. Over-broad groups are how fabric policy quietly fails; remove it.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 10.2 — Test the switch-support gate

**Objective.** Decide whether inline tagging is even available to you.

```python
access_layer = {"cat9300": 40, "cat9200": 12, "cat3850": 18, "third-party": 6}
inline_capable = {"cat9300", "cat9200", "cat9400", "cat9500", "nexus9000"}
total = sum(access_layer.values())
capable = sum(n for m, n in access_layer.items() if m in inline_capable)
print(f"inline-capable: {capable}/{total} switches ({capable/total:.0%})")
print("SXP required for the remainder" if capable < total else "inline tagging end to end")
```

**Expected result.** 52 of 76 (68%) — inline tagging is unavailable estate-wide, so SXP is mandatory.

**Negative test.** Assume the 3850s and third-party switches carry tags anyway. Policy silently fails
open on 24 switches, because an untagged frame matches no SGACL. Verify per model, never per vendor.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 10.3 — Size the SXP binding ceiling

**Objective.** Check a design against a published scale limit before committing to it.

```python
ISE_3595_SXP_MAX = 20000          # published limit for a standalone ISE 3595
endpoints, inline_pct = 34000, 0.68
sxp_bindings = int(endpoints * (1 - inline_pct))
print(f"SXP bindings required: {sxp_bindings}  ceiling: {ISE_3595_SXP_MAX}")
print("WITHIN LIMIT" if sxp_bindings <= ISE_3595_SXP_MAX else "EXCEEDS - redesign or add nodes")
```

**Expected result.** 10,880 bindings against a 20,000 ceiling — within limit.

**Negative test.** Set `inline_pct = 0.2`. Required bindings become 27,200 and the design exceeds the
ceiling; the fix is more inline-capable hardware, not more licenses.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 10.4 — Score the fabric tier against the rubric

**Objective.** Score this tier on the five **constraint axes** used across Chapters 10–15 — a deliberate reduction of Chapter 02's eight-dimension rubric that promotes air-gap capability to a first-class axis, because it disqualifies options outright rather than merely scoring them.

```python
weights = {"agentless": 0.30, "granularity": 0.25, "coverage": 0.20,
           "air_gap": 0.15, "effort": 0.10}
fabric = {"agentless": 5, "granularity": 2, "coverage": 3, "air_gap": 5, "effort": 2}
score = sum(weights[k] * fabric[k] for k in weights)
print(f"weighted score: {score:.2f} / 5.00")
```

**Expected result.** 3.45 — strong on agentless reach and air-gap, weak on granularity and effort.

**Negative test.** Re-weight with `granularity` at 0.50 and the tier falls behind host-agent options.
The rubric encodes your priorities; changing them changes the winner, which is the point.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Fabric and NAC-based segmentation enforces group-to-group policy in switching you already own, covering
devices that can never take an agent — but its granularity is coarser than a host agent's, and its
viability is decided by the access-layer hardware rather than by the vendor shortlist.

- [ ] I can explain SGT assignment, propagation, and SGACL enforcement.
- [ ] I can test an estate against the inline-tagging hardware gate.
- [ ] I can state the cost model, air-gap posture, and where to verify FIPS and FedRAMP.
- [ ] I completed Labs 10.1–10.4 including each negative test.
