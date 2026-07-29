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

This chapter carries a topic-level walkthrough lab for **every objective in
Domain 1 (Network) of the DCCOR 350-601 v1.2 exam guide** — all eleven
objectives, from routing and switching through overlay, packet flow, and
Nexus Dashboard assurance — mapped in the volume README's coverage tables.
Labs use the NX-OS CLI on a Nexus 9000 fabric. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 2.1–2.11** — the Chapter 01 spine-leaf fabric
(two spines, four leaves) running NX-OS 10.x, a vPC leaf pair, an OSPF
underlay, and iBGP EVPN with the spines as route reflectors. A management
station can reach a Nexus Dashboard cluster at `$ND`. **Cost:** none beyond
lab resources.

### Lab 2.1 — Apply routing protocols (Objective 1.1)

**Objective:** Verify the OSPF underlay that carries VTEP reachability.

```text
show ip ospf neighbors
show ip route 10.0.0.4
```

**Expected result:** every spine-leaf adjacency in `FULL` state, and the
remote leaf's loopback (the VTEP source) learned via OSPF — the underlay is
what the overlay rides on.

**Negative test:** shut one underlay link (`interface eth1/1 ; shutdown`);
the neighbor drops to `DOWN` and the route reconverges via ECMP — confirming
the second path, not a black hole.

**Cleanup:** `no shutdown` the link; confirm the adjacency returns to `FULL`.

### Lab 2.2 — Apply switching protocols such as RSTP+, LACP, and vPC (Objective 1.2)

**Objective:** Validate the vPC domain and its member port channel.

```text
show vpc brief
show port-channel summary
show spanning-tree vlan 2001
```

**Expected result:** `peer status: peer adjacency formed ok`, the vPC role,
zero consistency mismatches, and the member port channel `(SU)`; RSTP shows
the vPC pair as a single logical bridge.

**Negative test:** set a mismatched MTU on one peer's vPC VLAN; `show vpc
brief` reports a **Type-2 consistency** warning and suspends the VLAN on the
secondary — the protection working as designed.

**Cleanup:** restore the MTU; confirm `show vpc consistency-parameters vlans`
is clean.

### Lab 2.3 — Apply overlay protocols such as VXLAN EVPN (Objective 1.3)

**Objective:** Prove the EVPN control plane learns hosts before flooding.

```text
show nve peers
show bgp l2vpn evpn summary
show l2route evpn mac all
```

**Expected result:** NVE peers for every remote VTEP, EVPN neighbors
`Established`, and MAC addresses learned as Type-2 routes — control-plane
learning, not flood-and-learn.

**Negative test:** remove `send-community extended` from one spine session;
`show nve peers` loses the peer because Type-3 routes carry their VTEP
information in extended communities.

**Cleanup:** restore `send-community extended`; confirm NVE peers return.

### Lab 2.4 — Apply ACI concepts (Objective 1.4)

**Objective:** Contrast the NX-OS fabric with the ACI object model by reading
an APIC's tenant tree (the same fabric, controller-driven).

```text
icurl -k 'https://apic/api/class/fvTenant.json?rsp-subtree=children' | python3 -m json.tool | head
```

**Expected result:** tenants returned as managed objects (`fvTenant`) with
child EPGs and bridge domains — ACI models intent as a policy tree, where
NX-OS models it as per-device CLI.

**Negative test:** query a class that does not exist (`fvNope`); the APIC
returns an empty `imdata` array — the object model is closed, unlike free-form
CLI.

**Cleanup:** none (read-only).

### Lab 2.5 — Analyze packet flow: unicast, multicast, broadcast (Objective 1.5)

**Objective:** Trace how the fabric forwards each traffic class.

```text
show forwarding route 10.20.1.50 vrf TENANT-A
show ip mroute 239.1.1.1
show mac address-table dynamic vlan 2001
```

**Expected result:** unicast resolved to an NVE next-hop, multicast showing
the (S,G) with an outgoing interface list, and broadcast/BUM handled by
ingress replication or the underlay multicast group — the three flows take
distinct paths.

**Negative test:** ping a host in a VLAN with no anycast gateway configured on
the local leaf; the flow black-holes — proving first-hop routing depends on
the distributed gateway.

**Cleanup:** none (read-only).

### Lab 2.6 — Describe cloud service and deployment models per NIST 800-145 (Objective 1.6)

**Objective:** Classify the data center's Intersight/Nexus Dashboard
consumption against the NIST model.

```text
show system resources
curl -s -H "Authorization: Bearer $INTERSIGHT" https://intersight.com/api/v1/aaa/Sessions | jq '.Results | length'
```

**Expected result:** the on-prem fabric is **private-cloud IaaS**, while
Intersight is a **public-cloud SaaS** control plane — a hybrid model in NIST
800-145 terms (on-demand self-service, broad network access, resource
pooling, elasticity, measured service).

**Negative test:** an air-gapped fabric with no Intersight reachability is
pure private cloud; the SaaS call times out — the classification changes with
connectivity.

**Cleanup:** none (read-only).

### Lab 2.7 — Describe software updates and their impacts (Objective 1.7)

**Objective:** Run an NX-OS upgrade impact check before committing.

```text
show install all impact nxos bootflash:nxos64-cs.10.4.3.bin
```

**Expected result:** a per-module report showing whether the upgrade is
**disruptive or non-disruptive** (ISSU) and which modules reset — the impact
analysis you run before any maintenance window.

**Negative test:** attempt ISSU with a single supervisor or an incompatible
EPLD; the impact check flags it as **disruptive**, not hitless.

**Cleanup:** none (impact check does not modify the system).

### Lab 2.8 — Implement network configuration management (Objective 1.8)

**Objective:** Checkpoint and roll back configuration on NX-OS.

```text
checkpoint pre-change
configure terminal ; interface Vlan2001 ; shutdown ; end
show diff rollback-patch checkpoint pre-change running-config
rollback running-config checkpoint pre-change
```

**Expected result:** the checkpoint captures the running config, the diff
shows the single `shutdown` you introduced, and rollback reverts it — NX-OS
configuration management without external tooling.

**Negative test:** roll back to a checkpoint taken before a `feature` was
enabled while that feature is in use; NX-OS reports dependency errors rather
than silently breaking — verify with `show rollback log`.

**Cleanup:** `clear checkpoint database` to remove the test checkpoint.

### Lab 2.9 — Implement infrastructure monitoring with NetFlow, SPAN, and Nexus Dashboard (Objective 1.9)

**Objective:** Configure a SPAN session and confirm flow export.

```text
monitor session 1
  source interface Ethernet1/10 both
  destination interface Ethernet1/48
  no shut
show monitor session 1
show flow exporter EXPORTER-1
```

**Expected result:** the SPAN session `up` with source and destination bound,
and the NetFlow exporter reporting sent packets — the traffic-visibility
plumbing Nexus Dashboard Insights consumes.

**Negative test:** point the SPAN destination at a port that is also a vPC
member; NX-OS rejects it — SPAN destinations must be dedicated.

**Cleanup:** `no monitor session 1`.

### Lab 2.10 — Explain network assurance such as streaming telemetry (Objective 1.10)

**Objective:** Enable model-driven telemetry and confirm the subscription.

```text
feature telemetry
telemetry
  destination-group 1
    ip address 10.0.0.200 port 57000 protocol gRPC encoding GPB
  sensor-group 1
    data-source DME
    path sys/intf depth 0
  subscription 1
    dst-grp 1
    snsr-grp 1 sample-interval 30000
show telemetry control database subscriptions
```

**Expected result:** the subscription in `show telemetry control database`
with a valid destination and a 30-second cadence — push-based assurance,
versus SNMP polling.

**Negative test:** point the destination at an unreachable collector; the
subscription shows a connection failure in `show telemetry transport` —
telemetry is only as good as the receiver.

**Cleanup:** `no feature telemetry`.

### Lab 2.11 — Describe the capabilities and features of Nexus Dashboard (Objective 1.11)

**Objective:** Read the fabric's onboarding state in Nexus Dashboard.

```text
curl -sk -b cookie.txt "https://$ND/api/v1/infra/fabrics" | jq -r '.items[] | "\(.spec.name) \(.status.health)"'
```

**Expected result:** each onboarded fabric with a health score — Nexus
Dashboard unifies Insights (assurance), Orchestrator (multi-fabric policy),
and Fabric Controller (NDFC provisioning) over the fabrics it manages.

**Negative test:** query before onboarding any fabric; the `items` array is
empty — Nexus Dashboard assures only what it manages.

**Cleanup:** none (read-only).

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
