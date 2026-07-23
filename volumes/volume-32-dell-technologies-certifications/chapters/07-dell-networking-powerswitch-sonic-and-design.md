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

Where OS10/SONiC virtual images are entitled (both exist for labs):
build a two-leaf/one-spine mini-fabric on the Volume XXVI host — VLT
pair with a dual-homed test VM, then the same dual-homing as EVPN
ESI on SONiC; induce a peer-link failure and a config_db typo,
capturing both signatures. Otherwise: full runbooks for both builds
with expected outputs.

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
