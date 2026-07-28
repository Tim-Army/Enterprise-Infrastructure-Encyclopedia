# Chapter 04: Data Center — Engineering (EVPN/VXLAN)

## Learning Objectives

- Explain the Data Center Engineering specialist scope.
- Design a leaf-spine underlay.
- Build a VXLAN overlay with EVPN.
- Verify EVPN routes and VXLAN tunnels.
- Complete a walkthrough for each DC-Engineering topic.

## Theory and Architecture

The **Data Center Engineering (DC Eng)** specialization focuses on **designing and building**
Arista data-center fabrics — chiefly **EVPN/VXLAN**. The **underlay** is an IP leaf-spine
(often eBGP or OSPF) providing reachability between **VTEP** loopbacks. The **overlay** uses
**VXLAN** (L2/L3 tunnels over the IP underlay) with **BGP EVPN** as the control plane
(advertising MAC/IP routes — type-2 — and prefixes — type-5 — so VTEPs learn remote
endpoints without flooding). This delivers scalable multi-tenant L2/L3 across the fabric.
Engineering also covers **MLAG vs EVPN multihoming**, VRFs/tenants, and anycast gateways.

## Design Considerations

Build a clean **IP underlay** (unique loopbacks, ECMP), then the **EVPN control plane**
(BGP EVPN peering to spines/route-reflectors), and **VXLAN** VTEPs with symmetric IRB and
anycast gateways for tenant routing. Prefer **EVPN** over flood-and-learn for scale.

## Implementation and Automation

The labs configure the underlay, VXLAN VTEP, EVPN, and verify overlay state.

## Validation and Troubleshooting

Confirm the model:

```text
Underlay: IP leaf-spine (eBGP/OSPF) between VTEP loopbacks. Overlay: VXLAN + BGP EVPN control plane
(type-2 MAC/IP, type-5 prefix). Anycast gateway (IRB) for tenant routing; VRFs for multi-tenancy.
```

Common pitfalls: overlay before a working **underlay**; and flood-and-learn VXLAN (no EVPN)
at scale.

## Security and Best Practices

Get the **underlay** solid first, use **BGP EVPN** as the overlay control plane, deploy
**anycast gateways** and **VRFs** for tenants, and verify **type-2/type-5** routes. Automate
the fabric build (Chapter 07) for consistency.

## Hands-On Lab

DC-Engineering walkthroughs. **Shared prerequisites** — a cEOS leaf-spine (containerlab).
**Cost:** none.

### Lab 4.1 — Build the underlay (eBGP)

**Objective:** Establish leaf-spine IP reachability.

```text
leaf1(config)# interface Loopback0
leaf1(config-if-Lo0)# ip address 1.1.1.1/32
leaf1(config)# router bgp 65101
leaf1(config-router-bgp)# neighbor 10.0.0.0 remote-as 65100
leaf1(config-router-bgp)# network 1.1.1.1/32
leaf1# show ip bgp summary
```

**Expected result:** an eBGP session to the spine advertising the **VTEP loopback** — the
underlay.

**Negative test:** build VXLAN before the underlay carries loopbacks; **VTEPs can't reach
each other** — underlay first.

**Cleanup:** `no router bgp 65101`.

### Lab 4.2 — Configure a VXLAN VTEP

**Objective:** Define the VXLAN interface.

```text
leaf1(config)# interface Vxlan1
leaf1(config-if-Vxlan1)# vxlan source-interface Loopback0
leaf1(config-if-Vxlan1)# vxlan udp-port 4789
leaf1(config-if-Vxlan1)# vxlan vlan 100 vni 10100
leaf1# show interfaces Vxlan1
```

**Expected result:** a VXLAN VTEP mapping **VLAN 100 → VNI 10100** — the overlay data plane.

**Negative test:** map inconsistent VLAN↔VNI across leaves; **keep the mapping consistent**
fabric-wide.

**Cleanup:** `no interface Vxlan1`.

### Lab 4.3 — Enable BGP EVPN

**Objective:** Add the EVPN control plane.

```text
leaf1(config)# router bgp 65101
leaf1(config-router-bgp)# neighbor 10.0.0.0 send-community extended
leaf1(config-router-bgp)# address-family evpn
leaf1(config-router-bgp-af)# neighbor 10.0.0.0 activate
leaf1# show bgp evpn summary
```

**Expected result:** an **EVPN** address-family session — the overlay control plane learns
remote MAC/IP.

**Negative test:** rely on flood-and-learn; **EVPN** advertises endpoints without flooding
— enable it.

**Cleanup:** none.

### Lab 4.4 — Verify EVPN routes

**Objective:** Confirm type-2/type-5 learning.

```text
leaf1# show bgp evpn route-type mac-ip
leaf1# show vxlan address-table
```

**Expected result:** **type-2** MAC/IP routes and the VXLAN address table populated —
overlay reachability via EVPN.

**Negative test:** assume connectivity without checking EVPN routes; **verify type-2/5** are
present.

**Cleanup:** none (read-only).

### Lab 4.5 — Anycast gateway (tenant routing)

**Objective:** Provide distributed L3 gateway.

```text
leaf1(config)# ip virtual-router mac-address 00:1c:73:00:00:99
leaf1(config)# interface Vlan100
leaf1(config-if-Vl100)# ip address virtual 10.100.0.1/24
leaf1# show ip virtual-router
```

**Expected result:** an **anycast gateway** for VLAN 100 present on every leaf — optimal
tenant routing.

**Negative test:** centralize the gateway on one leaf; an **anycast gateway** routes locally
on each leaf — avoid tromboning.

**Cleanup:** `no interface Vlan100`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Data Center Engineering certifies designing/building Arista fabrics: an IP underlay, a VXLAN
overlay with BGP EVPN control plane (type-2/type-5), VRF multi-tenancy, and anycast
gateways. This chapter built the underlay, VXLAN, EVPN, and an anycast gateway.

- [ ] I can build an IP leaf-spine underlay.
- [ ] I can configure a VXLAN VTEP.
- [ ] I can enable and verify BGP EVPN.
- [ ] I can deploy an anycast gateway for tenants.
- [ ] I completed Labs 4.1–4.5 including each negative test.
