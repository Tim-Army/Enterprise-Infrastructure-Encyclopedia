# Chapter 07: Dell Networking — PowerSwitch, SONiC, and Design

## Learning Objectives

- Deploy PowerSwitch data center fabrics on OS10: VLTi pairs, EVPN
  VXLAN, and the SmartFabric mode trade
- Deploy campus PowerSwitch and position Dell's enterprise networking
  against this encyclopedia's Cisco/Juniper volumes
- Operate Enterprise SONiC deployments and know why hyperscale NOS
  economics reached the enterprise
- Map the ladder: Networking Foundations D-NWG-FN-23, Design
  D-NWG-DS-00, PowerSwitch Data Center Deploy D-PDC-DY-23, Campus
  Deploy D-PCM-DY-23, SONiC Deploy D-SNC-DY-00

## Theory and Architecture

### OS10 and the familiar fabric

PowerSwitch data center networking is spine-leaf with the same
grammar as Volumes III/XXXI: eBGP underlays, EVPN-VXLAN overlays,
anycast gateways — plus Dell's **VLT** (Virtual Link Trunking) for
active-active dual-homing at the pair level and **SmartFabric**
mode, which turns a fabric into an appliance-managed system (the
VxRail/MX integration path). The Deploy exam certifies both modes
and the judgment of when each fits.

### SONiC changes the ownership model

Enterprise SONiC on PowerSwitch is the hyperscaler NOS
productized: containerized services over a Linux base, config as
JSON (config_db), fleet automation as a first-class citizen — the
Volume IX/XXXI automation doctrine with the vendor CLI layer
thinned. The SONiC Deploy exam lives in exactly that seam:
ZTP, config_db discipline, and EVPN on SONiC.

### Design is portfolio-neutral judgment

D-NWG-DS-00 tests the Volume II/VIII fundamentals wearing Dell
hardware: oversubscription math, failure domains, L2/L3 boundaries,
and where SmartFabric's simplicity beats CLI control (and where it
must not).

## Design Considerations

- VLT pairs are one failure domain with two boxes: draw them as one;
  EVPN multihoming supersedes VLT where fabric scale justifies it
- SmartFabric for appliance estates (VxRail/MX rows), full CLI/EVPN
  for general fabrics — mixing management models in one fabric is
  the classic operational trap
- SONiC where fleet automation maturity exists (Volume IX gate);
  OS10 where operational familiarity and TAC-style support decide
- MTU/VLAN prep per the Volume XXVI checklist before any deploy exam
  scenario — Dell's deploy failures are the same failures

## Implementation and Automation

```text
# OS10: VLT pair + EVPN leaf slice
configure terminal
vlt-domain 1
 backup destination 10.30.161.12
 peer-link port-channel 100
interface vlan 10
router bgp 65101
 neighbor 172.20.0.0 remote-as 65100
 address-family l2vpn evpn
  advertise-all-vni

# SONiC: config_db is the interface
show runningconfiguration all | head
config vlan add 10
config interface ip add Ethernet0 172.20.0.1/31
config save -y            # persists /etc/sonic/config_db.json
```

## Validation and Troubleshooting

- OS10: `show vlt 1` (peer/backup/mismatch checks) before any
  dual-homing theory; `show evpn evi` and BGP EVPN routes as in any
  fabric
- SONiC: container health (`docker ps` on-box), `show interfaces
  status`, config_db diffs under version control
- SmartFabric: validate from the owning appliance (VxRail/OME-M)
  first — the fabric is downstream of its manager
- Volume II's discipline stands: cabling/MTU/one-line diffs explain
  most fabric tickets

## Security and Best Practices

- Management plane on OOB with RADIUS/TACACS-backed RBAC; SONiC gets
  the Linux-hardening treatment (Volume IV) plus NOS controls
- ZTP artifacts signed and served from controlled infrastructure
- Fabric config in Git with pipeline pushes (Volume IX) — SONiC makes
  this native; OS10 supports it; use it on both

## References and Knowledge Checks

- Exam descriptions: D-NWG-FN-23, D-NWG-DS-00, D-PDC-DY-23,
  D-PCM-DY-23, D-SNC-DY-00 (Dell Learning catalog)
- OS10 and Enterprise SONiC configuration guides; SmartFabric
  services docs

Knowledge checks:

1. What does VLT solve, what does it cost as a failure domain, and
   what supersedes it at fabric scale?
2. Why is config_db-as-JSON an automation advantage over CLI-derived
   config, per Volume IX doctrine?
3. Name two estates where SmartFabric mode is correct and one where
   it is a mistake.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab spanning the **Dell Networking
exams — Foundations (D-NWG-FN-23), Design (D-NWG-DS-00), PowerSwitch Data Center and
Campus Deploy (D-PDC-DY-23, D-PCM-DY-23), and SONiC Deploy (D-SNC-DY-00)** — mapped in
the volume README's coverage tables. Labs use the Dell **OS10** CLI and SONiC. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 7.1–7.7** — two Dell PowerSwitch (S/Z-series)
switches running OS10, an OS10 or SONiC data-center fabric, and console/SSH access.
**Cost:** none beyond lab resources.

### Lab 7.1 — Networking foundations and OS10 (Networking Foundations)

**Objective:** Read the OS10 system and its Linux-based architecture.

```text
show version
show system
show interface status | head
```

**Expected result:** the OS10 version and interfaces — **Dell OS10** is a modular,
Linux-based (unmodified Debian) NOS on PowerSwitch hardware, with a standard CLI plus
programmability (the underlying Linux, plus REST/gNMI), the disaggregated foundation of
Dell networking.

**Negative test:** expect a monolithic proprietary OS; OS10 exposes the Linux
substrate (you can `sudo` to a shell) — the disaggregated model is a key foundations
concept.

**Cleanup:** none (read-only).

### Lab 7.2 — Layer 2 and VLANs (PowerSwitch Data Center Deploy)

**Objective:** Configure a VLAN and a trunk on OS10.

```text
configure terminal
interface vlan 10
 description SERVERS
 no shutdown
interface ethernet 1/1/1
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
end
show vlan
show interface ethernet 1/1/1 switchport
```

**Expected result:** VLAN 10 and the trunk carrying it — OS10 L2 bridges within VLANs
and tags on trunks (802.1Q), the access/aggregation foundation before the routed
overlay; the CLI mirrors industry-standard syntax.

**Negative test:** a trunk not allowing VLAN 10 drops that VLAN's frames even though
the link is up — the allowed-VLAN list gates trunk traffic.

**Cleanup:** `configure terminal; no interface vlan 10; commit`.

### Lab 7.3 — Layer 3 routing (PowerSwitch Data Center Deploy)

**Objective:** Configure OSPF (or BGP) and verify adjacency.

```text
configure terminal
router ospf 1
 router-id 10.0.0.1
interface ethernet 1/1/2
 no switchport
 ip address 10.0.0.1/30
 ip ospf 1 area 0
end
show ip ospf neighbor
show ip route ospf
```

**Expected result:** the OSPF neighbor `Full` and learned routes — OS10 routes with
OSPF, BGP, and static; a data-center leaf-spine underlay typically runs eBGP or OSPF
for ECMP reachability between VTEP loopbacks.

**Negative test:** an OSPF area/MTU mismatch stalls the adjacency below `Full` —
`show ip ospf neighbor` reveals the stuck state.

**Cleanup:** `configure terminal; no router ospf 1; commit`.

### Lab 7.4 — VLT multi-chassis link aggregation (PowerSwitch Data Center Deploy)

**Objective:** Configure and verify a VLT domain.

```text
configure terminal
vlt-domain 1
 backup destination 10.0.0.2
 discovery-interface ethernet 1/1/29-1/1/30
end
show vlt 1
show vlt 1 vlt-port-detail
```

**Expected result:** the VLT domain up with both peers and the VLTi — **VLT** (Virtual
Link Trunking) lets two OS10 switches present one logical LAG to downstream devices
(active/active, no spanning-tree blocking), the standard data-center redundancy at the
access/aggregation tier.

**Negative test:** a VLT with mismatched VLANs or a down VLTi causes inconsistency; the
peers cannot forward as one logical switch — the VLTi and consistent config are
required.

**Cleanup:** `configure terminal; no vlt-domain 1; commit`.

### Lab 7.5 — EVPN-VXLAN fabric (PowerSwitch Data Center Deploy)

**Objective:** Verify an EVPN-VXLAN overlay on the OS10 fabric.

```text
show nve vxlan-vni
show bgp evpn summary
show evpn mac-ip
```

**Expected result:** the VNIs, EVPN BGP peers, and MAC/IP routes — OS10 builds
spine-leaf **EVPN-VXLAN** fabrics (BGP control plane, VXLAN data plane) for scalable
multi-tenant data centers; **SmartFabric Services** can automate the fabric build and
lifecycle.

**Negative test:** inconsistent VNI-to-VLAN mapping on one leaf silently drops that
segment; the endpoints do not learn each other — the mapping must be fabric-consistent.

**Cleanup:** none (read-only).

### Lab 7.6 — Campus deployment (PowerSwitch Campus Deploy)

**Objective:** Verify campus features (PoE, QoS, access).

```text
show power-management-mode
show interface ethernet 1/1/1 poe
show qos maps type dscp-color
```

**Expected result:** PoE budget/allocation and QoS maps — campus PowerSwitch
deployment focuses on the wired access edge: **PoE** for phones/APs, **QoS** for
voice/video, VLAN/access control, and multi-gig uplinks, managed at scale (SmartFabric/
OME).

**Negative test:** connect more PoE devices than the switch's power budget allows;
lower-priority ports are denied power — the PoE budget/priority governs allocation.

**Cleanup:** none (read-only).

### Lab 7.7 — SONiC deployment (SONiC Deploy)

**Objective:** Read Dell Enterprise SONiC state via its CLI/config DB.

```text
show version
show interfaces status | head
show ip bgp summary
```

```bash
sonic-cfggen -d -v "DEVICE_METADATA.localhost.hwsku" 2>/dev/null
```

**Expected result:** the SONiC version, interfaces, and BGP — **SONiC** (Software for
Open Networking in the Cloud) is the community/open NOS Dell offers as **Enterprise
SONiC** on PowerSwitch: a Redis **config DB**-driven, containerized NOS for
hyperscale-style disaggregated data-center fabrics.

**Negative test:** expect the OS10 CLI syntax on SONiC; SONiC has its own CLI and a
config-DB model — the two NOS options on the same hardware differ operationally.

**Cleanup:** none (read-only).

## Lab Verification

Verification means dual-homing survived single-link and single-node
loss in both builds with evidence, the induced failures showed their
distinct signatures, and configs live in Git with the pipeline note.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] VLT and EVPN modes built or runbooked with failure evidence
- [ ] SONiC's config_db model operated under version control
- [ ] SmartFabric ownership seam articulated
- [ ] All five networking codes recorded from the verified table
