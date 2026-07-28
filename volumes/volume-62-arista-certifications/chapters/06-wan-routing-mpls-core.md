# Chapter 06: WAN Routing — MPLS Core

## Learning Objectives

- Explain the WAN Routing (MPLS Core) specialist scope.
- Configure MPLS label switching with LDP.
- Build L3VPNs over MPLS.
- Verify labels and VPN routes.
- Complete a walkthrough for each MPLS topic.

## Theory and Architecture

The **WAN Routing Track** leads to a **Specialist: MPLS Core** credential, covering
service-provider and enterprise-WAN routing on Arista EOS. **MPLS** forwards packets by
**labels** rather than IP lookup: an IGP (OSPF/IS-IS) provides reachability, **LDP** (or
segment routing) distributes labels to build **LSPs** (label-switched paths), and **MP-BGP**
carries **L3VPN** routes (VPNv4/VPNv6) so customer VRFs are isolated across a shared core.
Arista EOS supports MPLS, LDP, segment routing, and L3VPN for high-scale WAN/core roles.

## Design Considerations

Build a solid **IGP** core, distribute labels with **LDP** (or SR), and layer **MP-BGP
L3VPN** with **VRFs** per customer and route targets for import/export. Verify the **label
stack** end to end.

## Implementation and Automation

The labs enable MPLS/LDP, build an L3VPN, and verify labels/VPN routes.

## Validation and Troubleshooting

Confirm the model:

```text
MPLS: IGP (OSPF/IS-IS) reachability + LDP/SR labels -> LSPs. L3VPN: MP-BGP VPNv4 + VRFs + route targets.
Forwarding by label swap; PE imposes/removes the VPN label.
```

Common pitfalls: **LDP** not enabled on core links (no LSP); and missing **route targets**
(VPN routes not imported).

## Security and Best Practices

Enable **LDP/SR** on all core links, isolate customers with **VRFs + route targets**, verify
the **label stack**, and secure the control plane (BGP/LDP authentication). Keep the IGP
stable — LSPs depend on it.

## Hands-On Lab

MPLS walkthroughs. **Shared prerequisites** — a cEOS core (containerlab) with MPLS support,
or the patterns. **Cost:** none.

### Lab 6.1 — Enable MPLS and LDP

**Objective:** Turn on label switching.

```text
core(config)# mpls ip
core(config)# interface Ethernet1
core(config-if-Et1)# mpls ip
core(config)# mpls ldp
core# show mpls ldp neighbor
```

**Expected result:** an **LDP neighbor** on the core link — labels being distributed.

**Negative test:** enable MPLS but not **LDP** on a link; no labels are exchanged there — no
LSP forms.

**Cleanup:** `no mpls ldp`.

### Lab 6.2 — Verify the label-switched path

**Objective:** Confirm labels are installed.

```text
core# show mpls lfib
core# show mpls ldp bindings
```

**Expected result:** the **LFIB** and label bindings populated — a working LSP.

**Negative test:** assume MPLS forwarding without checking the **LFIB**; verify labels are
installed.

**Cleanup:** none (read-only).

### Lab 6.3 — Build an L3VPN

**Objective:** Isolate a customer VRF over MPLS.

```text
pe(config)# vrf instance CUST-A
pe(config)# router bgp 65000
pe(config-router-bgp)# vrf CUST-A
pe(config-router-bgp-vrf)# rd 65000:100
pe(config-router-bgp-vrf)# route-target import 65000:100
pe(config-router-bgp-vrf)# route-target export 65000:100
pe# show bgp vpn-ipv4 summary
```

**Expected result:** a **VRF + MP-BGP VPNv4** config with route targets — customer isolation
over the shared core.

**Negative test:** omit **route targets**; VPN routes aren't imported/exported — the VPN
doesn't connect.

**Cleanup:** `no vrf instance CUST-A`.

### Lab 6.4 — Verify VPN routes

**Objective:** Confirm VPNv4 routes and labels.

```text
pe# show bgp vpn-ipv4
pe# show ip route vrf CUST-A
```

**Expected result:** VPNv4 routes with **VPN labels** and the VRF route table populated —
end-to-end L3VPN.

**Negative test:** check only the global table; **VPN routes live in the VRF/VPNv4 tables**
— look there.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

WAN Routing (MPLS Core) certifies label switching on EOS: an IGP core with LDP/SR labels
building LSPs, and MP-BGP L3VPNs with VRFs and route targets isolating customers. This
chapter enabled MPLS/LDP, verified the LSP, built an L3VPN, and checked VPN routes.

- [ ] I can enable MPLS and LDP.
- [ ] I can verify the label-switched path (LFIB).
- [ ] I can build an MP-BGP L3VPN with VRFs.
- [ ] I can verify VPNv4 routes and labels.
- [ ] I completed Labs 6.1–6.4 including each negative test.
