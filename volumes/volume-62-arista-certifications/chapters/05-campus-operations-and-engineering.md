# Chapter 05: Campus — Operations and Engineering

## Learning Objectives

- Explain the Campus track specializations.
- Configure campus access (PoE, VLANs, wired).
- Design a campus fabric and segmentation.
- Manage campus with CloudVision.
- Complete a walkthrough for each Campus topic.

## Theory and Architecture

The **Campus Track** offers **Specialist** credentials in **Campus Operations** and
**Campus Engineering**. Arista's campus uses the same **EOS** and **CloudVision** as the
data center, extending them to wired access, **PoE**, and (with Arista Wi-Fi / cognitive
access points) wireless. **Operations** covers running campus access — VLANs, PoE,
authentication (802.1X), and monitoring; **Engineering** covers designing the **campus
fabric** (spline/leaf-spine campus, EVPN/VXLAN for macro-segmentation), **segmentation**
(MSS — Macro-Segmentation Service — inserts security policy), and CloudVision-driven
provisioning. A single OS and management plane across DC and campus is Arista's
differentiator.

## Design Considerations

Operate campus access with **PoE**, **VLANs**, and **802.1X**; engineer the campus with a
**fabric** and **segmentation** (VXLAN/MSS) driven by **CloudVision**. Reuse DC skills — one
EOS, one management plane.

## Implementation and Automation

The labs configure PoE/access, describe campus fabric/segmentation, and use CloudVision.

## Validation and Troubleshooting

Confirm the scope:

```text
Campus Ops: access (VLANs, PoE, 802.1X), monitoring. Campus Eng: campus fabric (EVPN/VXLAN),
segmentation (MSS), CloudVision provisioning. Same EOS + CloudVision as the data center.
```

Common pitfalls: treating campus as a separate skill set (it's the same **EOS/CloudVision**);
and open access ports with no **802.1X**.

## Security and Best Practices

Secure access with **802.1X**, power devices with **PoE**, segment with **VXLAN/MSS**,
provision and monitor with **CloudVision**, and reuse the DC fabric patterns. Enforce
policy at the access edge.

## Hands-On Lab

Campus walkthroughs. **Shared prerequisites** — a cEOS campus switch (or the patterns).
**Cost:** none.

### Lab 5.1 — Configure PoE access

**Objective:** Enable power and access on a port.

```text
switch(config)# interface Ethernet5
switch(config-if-Et5)# switchport access vlan 30
switch(config-if-Et5)# poe priority high
switch# show poe interface Ethernet5
```

**Expected result:** an access port in VLAN 30 with **PoE** enabled — powered campus access.

**Negative test:** connect an AP/phone to a port with PoE disabled; it **won't power on** —
enable PoE.

**Cleanup:** `default interface Ethernet5`.

### Lab 5.2 — 802.1X authentication

**Objective:** Require authentication at the edge.

```text
switch(config)# interface Ethernet5
switch(config-if-Et5)# dot1x pae authenticator
switch(config-if-Et5)# dot1x port-control auto
switch# show dot1x interface Ethernet5
```

**Expected result:** the port in **802.1X auto** mode — authenticated access.

**Negative test:** leave access ports open; **802.1X** authenticates endpoints — enforce it.

**Cleanup:** `default interface Ethernet5`.

### Lab 5.3 — Campus fabric and segmentation

**Objective:** Describe campus fabric with segmentation.

```text
# Campus fabric: leaf-spine campus with EVPN/VXLAN; MSS (Macro-Segmentation Service)
#   steers traffic through firewalls per policy from CloudVision.
"campus: EVPN/VXLAN fabric + MSS segmentation, managed by CloudVision"
```

**Expected result:** the campus **fabric + MSS segmentation** model — the engineering scope.

**Negative test:** rely on VLAN ACLs alone for security; **MSS** inserts stateful policy —
use it for macro-segmentation.

**Cleanup:** none.

### Lab 5.4 — CloudVision provisioning

**Objective:** Manage campus via CloudVision.

```text
# CloudVision (CVP): configlets + Studios provision campus switches at scale;
#   streaming telemetry monitors them; Change Control gates deployments.
"cloudvision: Studios/configlets provision; telemetry monitors; change control gates"
```

**Expected result:** CloudVision **provisioning + telemetry + change control** for campus —
fleet management.

**Negative test:** configure each campus switch by hand; **CloudVision** provisions and
monitors them centrally.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Campus track certifies operating (PoE, VLANs, 802.1X, monitoring) and engineering
(campus fabric, EVPN/VXLAN, MSS segmentation, CloudVision) Arista campus networks on the
same EOS/CloudVision platform as the data center. This chapter configured PoE/802.1X and
described the fabric, MSS, and CloudVision.

- [ ] I can configure PoE access ports.
- [ ] I can enforce 802.1X at the edge.
- [ ] I can describe campus fabric and MSS segmentation.
- [ ] I can manage campus with CloudVision.
- [ ] I completed Labs 5.1–5.4 including each negative test.
