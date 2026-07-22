# Chapter 02: Nexus Switching, vPC, and VXLAN EVPN Fabrics

## Learning Objectives

- Configure NX-OS Layer 2 and Layer 3 features that differ from IOS XE,
  including the feature model and VRF-lite
- Build and validate a virtual port channel (vPC) domain, and explain
  its split-brain protections
- Explain VXLAN encapsulation and why a fabric needs an EVPN control
  plane rather than flood-and-learn
- Configure a working VXLAN EVPN fabric: NVE interfaces, L2VNIs,
  L3VNIs, and the distributed anycast gateway
- Validate overlay reachability end to end and troubleshoot the classic
  failure modes

## Theory and Architecture

### NX-OS for the IOS XE-trained

NX-OS is modular and opt-in: nothing runs until `feature` enables it,
processes restart independently, and every routing feature is
VRF-aware by default. The practical differences that matter daily:
interfaces default to Layer 3 on many platforms (`no switchport` is
the natural state of a fabric link), `show run` displays only
non-default configuration, and the management interface lives
permanently in VRF `management`.

### vPC: multichassis link aggregation done carefully

A **vPC domain** lets two Nexus switches present one port channel to a
downstream device — active-active forwarding without spanning tree
blocking. Its anatomy is exam-favorite material because each piece
answers a specific failure:

- **Peer link** — carries the state synchronization (CFS) and, in
  failure cases, data; always a port channel of at least two links.
- **Peer keepalive** — an out-of-band heartbeat (ideally via mgmt0)
  whose only job is distinguishing "peer link failed" from "peer
  died."
- **Role priority** — elects primary/secondary; matters only during
  failures, which is exactly when it matters enormously.

When the peer link fails but the keepalive still passes, the
**secondary suspends its vPC member ports** — the split-brain
protection. When the whole peer dies, the survivor keeps forwarding.
Orphan ports (single-homed devices) are the perennial gotcha: they live
on one peer only, and a peer-link failure can strand them, which is why
`vpc orphan-port suspend` exists.

### VXLAN: the overlay, and why flood-and-learn was not enough

VXLAN encapsulates Ethernet frames in UDP (port 4789), adding a 24-bit
**VNI** — 16 million segments against 802.1Q's 4094 — and letting
Layer 2 segments span a routed fabric between **VTEPs**. Early VXLAN
learned MAC-to-VTEP mappings by flooding, which merely relocated the
scaling problem. **BGP EVPN** replaces it with a control plane: VTEPs
advertise MAC and IP reachability as BGP routes (Type-2 for hosts,
Type-3 for VTEP discovery and BUM replication, Type-5 for IP
prefixes). The fabric learns before it floods.

The standard NX-OS arrangement: OSPF or IS-IS as underlay, iBGP EVPN
with the spines as route reflectors, **anycast distributed gateway** on
every leaf (same gateway IP and MAC everywhere, so a workload's first
hop is always its local leaf), and symmetric IRB through an **L3VNI**
per VRF for routed traffic between leaves.

### Multi-site

VXLAN EVPN Multi-Site interconnects fabrics through **border gateways**
that re-originate EVPN routes and stitch VNIs site to site, keeping
each site's BUM and failure domains its own. It is the NX-OS answer to
the question ACI answers with Multi-Site Orchestrator, and the DCCOR
blueprint expects you to know both exist and when each applies.

## Design Considerations

- **Underlay IGP choice is less important than underlay discipline.**
  OSPF and IS-IS both work; /31 links, jumbo MTU, and BFD everywhere
  are what actually determine stability.
- **Route reflectors on spines** keep the EVPN mesh flat: every leaf
  peers with two RRs, not with every other leaf.
- **Replication mode:** ingress replication is simpler and fine at
  moderate scale; underlay multicast serves large BUM-heavy fabrics.
  Pick one per fabric; mixing them is misery.
- **vPC in EVPN fabrics** uses an anycast VTEP address shared by the
  pair — the fabric sees one logical VTEP, which is elegant, and one
  more reason the keepalive design must be right.

## Implementation and Automation

The volume lab: leaf pair as a vPC domain, VXLAN EVPN across all four
leaves, one tenant VRF with two segments.

```text
! vPC domain on each peer (mirror on both, roles differ)
feature vpc
vpc domain 10
  peer-keepalive destination 192.0.2.2 source 192.0.2.1 vrf management
  peer-switch
  peer-gateway
  auto-recovery
interface port-channel1
  switchport mode trunk
  vpc peer-link
```

```text
! EVPN fabric pieces on a leaf
feature bgp
feature nv overlay
feature vn-segment-vlan-based
nv overlay evpn

vlan 2001
  vn-segment 20001          ! L2VNI for segment A
vlan 3999
  vn-segment 39999          ! L3VNI for the tenant VRF

vrf context TENANT-A
  vni 39999
  rd auto
  address-family ipv4 unicast
    route-target both auto evpn

interface Vlan2001
  vrf member TENANT-A
  ip address 10.20.1.1/24
  fabric forwarding mode anycast-gateway

interface nve1
  source-interface loopback1
  host-reachability protocol bgp
  member vni 20001
    ingress-replication protocol bgp
  member vni 39999 associate-vrf

router bgp 65001
  address-family l2vpn evpn
  neighbor 10.0.0.1 remote-as 65001
    address-family l2vpn evpn
      send-community extended
```

Automation note: this is exactly the configuration NDFC templates and
the Chapter 06 Ansible roles generate — build it by hand once so the
generated version is readable to you forever after.

## Validation and Troubleshooting

Validate in dependency order:

```text
show vpc                          ! peer status, consistency, orphan ports
show vpc consistency-parameters global
show bgp l2vpn evpn summary       ! EVPN peers Established?
show nve peers                    ! VTEP discovery (Type-3 routes arrived)
show l2route evpn mac all         ! MAC learning via BGP, not flooding
show bgp l2vpn evpn route-type 2  ! host advertisements
ping 10.20.1.50 vrf TENANT-A      ! end-to-end through the L3VNI
```

Classic failures, in the order they actually occur: **Type-1
consistency mismatch** suspends vPC VLANs (compare
`consistency-parameters`, fix the mismatched side); **NVE peers absent**
with BGP up means missing `send-community extended` (Type-3 routes
carry their information in extended communities); **silent unicast
loss with ARP working** is almost always an MTU hole in one underlay
path — ECMP means one bad link fails intermittently; **anycast gateway
duplicate-IP alarms** trace to a VLAN missing
`fabric forwarding mode anycast-gateway` on one leaf.

## Security and Best Practices

- Storm control and BPDU Guard on host-facing ports; the fabric's
  loop-freedom does not protect against a looped access cable.
- First-hop security (DHCP snooping, ARP inspection where supported)
  belongs at the leaf edge; inside the fabric, trust the control
  plane, not the hosts.
- The underlay is infrastructure: OSPF/IS-IS authentication and BGP
  passwords are cheap insurance against a mis-cabled or malicious
  device joining the fabric.

## References and Knowledge Checks

- Cisco NX-OS VXLAN EVPN configuration guide (Nexus 9000)
- RFC 7432 (BGP MPLS-Based Ethernet VPN) and RFC 8365 (EVPN overlays)
- Cisco Live BRKDCN sessions on EVPN design and troubleshooting

Knowledge checks:

1. The peer link fails; the keepalive is healthy. What does each vPC
   peer do, and why is the keepalive's independence essential?
2. Which EVPN route type distributes VTEP membership for BUM
   replication, and what breaks when extended communities are not sent?
3. Why does symmetric IRB need an L3VNI, and what traffic uses it?
4. A host moves between leaves. How does the fabric learn the move,
   and what suppresses the stale entry?

## Hands-On Lab

On the Chapter 01 fabric: build the vPC domain (peer link, keepalive in
VRF management, a downstream vPC to a test host), then the full EVPN
overlay above — two L2VNIs and the TENANT-A L3VNI with anycast gateway
on all leaves. Prove: MAC routes present as Type-2 on a remote leaf,
NVE peers discovered on all four, end-to-end routed ping between
segments on different leaves. Then break it twice: remove
`send-community extended` from one spine session and capture the NVE
peer loss; set one underlay link to MTU 1500 and demonstrate the
intermittent-loss signature. Repair both.

## Lab Verification

Verification means the overlay passed end-to-end routed traffic, both
induced failures were demonstrated with their distinct signatures, and
both were repaired. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NX-OS gives the fabric its device model, vPC removes spanning tree
from the access without inviting split-brain, and VXLAN EVPN turns a
routed spine-leaf into a scalable multi-tenant fabric with a control
plane that learns before it floods. This chapter is the heaviest single
block of DCCOR's Network domain and the foundation Chapter 03 contrasts
ACI against.

- [ ] I can draw the vPC anatomy and narrate each failure mode
- [ ] I can explain Type-2, Type-3, and Type-5 EVPN routes and their
      jobs
- [ ] My lab fabric routes between segments through the L3VNI
- [ ] I demonstrated and repaired both induced failures
