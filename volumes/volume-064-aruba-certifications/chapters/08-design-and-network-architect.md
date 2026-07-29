# Chapter 08: Design and the Network Architect Tier

## Learning Objectives

- Explain the HPE Aruba Certified Network Architect design tier (HPE7-A03 Campus, HPE7-A04 Data Center).
- Translate requirements into an Aruba campus or data-center design.
- Design for redundancy, segmentation, and scale.
- Justify design trade-offs against requirements.
- Complete a design exercise for each architect topic.

## Theory and Architecture

Above the Expert tier sits the **HPE Aruba Certified Network Architect** design credential —
**Campus Access (HPE7-A03)** and **Data Center (HPE7-A04)**. Where the operational exams test
configuration, the architect exams test **design**: taking business and technical requirements
(users, sites, applications, security posture, growth) and producing an Aruba architecture —
which AOS-CX platforms, how leaf-spine or campus aggregation is built, where **VSX** and
**anycast gateways** go, how **dynamic segmentation** and **ClearPass** enforce policy, how
**Aruba Central** manages it, and how it all scales and survives failure. Design is about
**trade-offs**: redundancy vs cost, centralization vs distribution (e.g., CX 10000 in-fabric
firewalling vs a central appliance), and simplicity vs feature richness — each justified against
the requirements.

## Design Considerations

Start from **requirements**, not products. Make **redundancy** and **segmentation** first-class.
Prefer designs that **scale horizontally** (leaf-spine, Central-managed groups) and **fail
gracefully** (VSX, anycast). Document every trade-off and tie it to a requirement.

## Implementation and Automation

The exercises translate requirements into a topology, a redundancy plan, and a segmentation
design.

## Validation and Troubleshooting

Confirm the design method:

```text
Requirements -> platforms (AOS-CX) -> topology (leaf-spine/campus) -> redundancy (VSX/anycast)
-> segmentation (roles/ClearPass/PEF/CX 10000) -> management (Central) -> scale + failure analysis.
Codes: Network Architect Campus HPE7-A03; Data Center HPE7-A04.
```

Common pitfalls: designing **product-first** instead of requirement-first; and omitting a
**failure analysis**.

## Security and Best Practices

Bake **Zero-Trust segmentation** into the design (authenticate, role, enforce everywhere).
Ensure no **single point of failure** in the path. Keep the design **documented and traceable**
to requirements so it can be reviewed and defended.

## Hands-On Lab

Design walkthroughs. **Shared prerequisites for Labs 8.1–8.3** — a shell with `python3` and a
requirements sheet. **Cost:** none.

### Lab 8.1 — Requirements-to-topology

**Objective:** Choose a topology from requirements.

```python
python3 - <<'PY'
req={"sites":1,"servers":400,"east_west_heavy":True,"growth":"2x in 3y"}
topology="leaf-spine EVPN-VXLAN" if req["servers"]>100 or req["east_west_heavy"] else "collapsed core"
print("requirements:",req)
print("topology:",topology,"(scales horizontally; anycast gateway)")
PY
```

**Expected result:** a **leaf-spine EVPN-VXLAN** choice justified by scale and east-west traffic
— design from requirements.

**Negative test:** pick a two-tier collapsed core for 400 east-west-heavy servers; that does not
scale — choose **leaf-spine**.

**Cleanup:** none.

### Lab 8.2 — Redundancy plan

**Objective:** Remove single points of failure.

```python
python3 - <<'PY'
plan={"aggregation":"VSX pair","gateway":"anycast (every leaf)","uplinks":"dual to spine",
      "management":"Central (cloud, multi-region)"}
spof=[k for k,v in plan.items() if "single" in v.lower()]
for k,v in plan.items(): print(f"{k:12}: {v}")
print("single points of failure:", spof or "none")
PY
```

**Expected result:** a redundancy plan with **no single point of failure** (VSX, anycast, dual
uplinks) — a resilient design.

**Negative test:** single-home the core gateway; distribute with **VSX/anycast** — no SPOF.

**Cleanup:** none.

### Lab 8.3 — Segmentation design

**Objective:** Design role-based Zero-Trust segmentation.

```python
python3 - <<'PY'
roles={"employee":"corp apps","contractor":"limited","iot":"NVR/controller only","guest":"internet only"}
enforce="ClearPass role -> PEF (gateway/AOS-CX) + CX 10000 east-west in DC"
for r,access in roles.items(): print(f"{r:11}: {access}")
print("enforcement:",enforce)
PY
```

**Expected result:** a role-to-access map enforced by **ClearPass + PEF + CX 10000** — Zero-Trust
segmentation by design.

**Negative test:** flat network with perimeter-only security; design **role-based** segmentation
enforced in the fabric.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Network Architect tier (HPE7-A03 Campus, HPE7-A04 Data Center) tests design: translate
requirements into an Aruba architecture with the right platforms, topology, redundancy,
segmentation, management, and a scale/failure analysis — justifying every trade-off. Design
requirement-first, remove single points of failure, and bake in Zero-Trust segmentation.

- [ ] I can choose a topology from requirements.
- [ ] I can produce a no-SPOF redundancy plan.
- [ ] I can design role-based segmentation.
- [ ] I can justify design trade-offs against requirements.
- [ ] I completed Labs 8.1–8.3 including each negative test.
