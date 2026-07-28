# Chapter 06: Data Center Track

## Learning Objectives

- Explain the Data Center track (ACP-DC, HPE7-A05) and Network Architect DC (HPE7-A04).
- Build a leaf-spine fabric with EVPN-VXLAN on AOS-CX.
- Apply VSX for redundant leaves and gateways.
- Describe the CX 10000 distributed services switch.
- Complete a walkthrough for each Data Center topic.

## Theory and Architecture

The **Data Center** track certifies Aruba's data-center switching — **Professional (ACP-DC,
HPE7-A05)** and, at the design tier, **HPE Aruba Certified Network Architect – Data Center
(HPE7-A04)**. Modern Aruba data centers are **leaf-spine** fabrics running **EVPN-VXLAN**: an
IP underlay (OSPF/eBGP) carries **VXLAN** overlays whose MAC/IP reachability is distributed by
**BGP EVPN**, with **anycast gateways** so any leaf routes locally. **VSX** provides redundant
leaves and border gateways. Aruba's differentiator is the **CX 10000** — a "distributed services
switch" with an embedded **Pensando DPU** that runs a **stateful firewall and services in the
switch ASIC path**, so east-west segmentation and telemetry happen at line rate at the leaf
instead of hair-pinning to a central firewall.

## Design Considerations

Build a **leaf-spine** with an eBGP/OSPF underlay and **EVPN-VXLAN** overlay; use **anycast
gateways** for optimal routing. Deploy **VSX** for redundant leaves/borders. Where east-west
security matters, place **CX 10000** leaves so segmentation runs **in the fabric**, not through a
choke-point firewall.

## Implementation and Automation

The labs configure a VXLAN VTEP, the EVPN control plane, VSX for leaves, and describe CX 10000
services.

## Validation and Troubleshooting

Confirm the DC model:

```text
Leaf-spine: IP underlay (eBGP/OSPF) + VXLAN overlay + BGP EVPN + anycast gateway.
Redundancy: VSX leaves/borders. CX 10000: in-switch stateful firewall (Pensando DPU) for east-west.
Codes: ACP-DC HPE7-A05; Network Architect DC HPE7-A04.
```

Common pitfalls: a VXLAN overlay with **no EVPN** control plane (flood-and-learn does not
scale); and hair-pinning east-west traffic to a central firewall where **CX 10000** could
enforce in-fabric.

## Security and Best Practices

Distribute the gateway (**anycast**) and the firewall (**CX 10000**) so routing and segmentation
happen at the leaf. Keep the underlay simple and stable; let **EVPN** carry reachability. Secure
east-west with in-fabric stateful policy.

## Hands-On Lab

Data Center walkthroughs. **Shared prerequisites** — AOS-CX switches (physical or virtual) for a
small leaf-spine. **Cost:** none with virtual.

### Lab 6.1 — Configure a VXLAN VTEP

**Objective:** Define the tunnel endpoint and a VNI.

```text
switch(config)# interface loopback 0
switch(config-loopback-if)# ip address 10.0.0.11/32
switch(config)# interface vxlan 1
switch(config-vxlan-if)# source ip 10.0.0.11
switch(config-vxlan-if)# vni 10100
switch# show interface vxlan 1
```

**Expected result:** a **VTEP** on loopback 0 mapping VNI 10100 — the overlay data plane.

**Negative test:** source the VXLAN from a physical port IP; use a **loopback** so the VTEP
survives link failures.

**Cleanup:** `configure terminal; no interface vxlan 1`.

### Lab 6.2 — EVPN control plane

**Objective:** Distribute overlay reachability with BGP EVPN.

```text
switch(config)# router bgp 65001
switch(config-bgp)# neighbor 10.0.0.1 remote-as 65000
switch(config-bgp)# address-family l2vpn evpn
switch(config-bgp-l2vpn-evpn)# neighbor 10.0.0.1 activate
switch# show bgp l2vpn evpn summary
```

**Expected result:** an **EVPN** session advertising MAC/IP routes — a scalable, control-plane
overlay.

**Negative test:** rely on flood-and-learn with no EVPN; **BGP EVPN** distributes reachability —
enable the address family.

**Cleanup:** `configure terminal; no router bgp 65001`.

### Lab 6.3 — VSX for redundant leaves

**Objective:** Pair two leaves for active-active.

```text
switch(config)# vsx
switch(config-vsx)# role primary
switch(config-vsx)# inter-switch-link lag 256
switch(config-vsx)# keepalive peer 10.1.0.2 source 10.1.0.1
switch# show vsx status
```

**Expected result:** a **VSX** leaf pair presenting redundant, active-active connectivity to
hosts — no single point of failure at the leaf.

**Negative test:** single-home servers to one leaf; dual-home to a **VSX** pair for redundancy.

**Cleanup:** `configure terminal; no vsx`.

### Lab 6.4 — CX 10000 in-switch services

**Objective:** Describe distributed stateful segmentation.

```text
# CX 10000 embeds a Pensando DPU: stateful firewall + telemetry run IN the switch data path,
#   enforcing east-west segmentation at the leaf at line rate (no central firewall hair-pin).
"CX 10000: leaf-level stateful firewall (DPU) -> east-west policy in the fabric"
```

**Expected result:** the **CX 10000** model — east-west security enforced in the switch, not a
central choke point.

**Negative test:** route all east-west traffic to a central firewall; **CX 10000** enforces it
in-fabric at line rate — distribute it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Data Center track certifies Aruba leaf-spine fabrics — EVPN-VXLAN with anycast gateways,
VSX redundancy, and the CX 10000 distributed-services switch that enforces stateful east-west
segmentation in the fabric — at ACP-DC (HPE7-A05) and Network Architect DC (HPE7-A04).
Distribute the gateway and the firewall to the leaf.

- [ ] I can configure a VXLAN VTEP on AOS-CX.
- [ ] I can bring up the BGP EVPN control plane.
- [ ] I can pair redundant leaves with VSX.
- [ ] I can explain CX 10000 in-switch segmentation.
- [ ] I completed Labs 6.1–6.4 including each negative test.
