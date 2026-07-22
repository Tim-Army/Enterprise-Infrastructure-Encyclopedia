# Chapter 05: Data Center Fabrics — EVPN-VXLAN and the DC Track

## Learning Objectives

- Build an IP fabric on QFX: eBGP underlay, EVPN-VXLAN overlay, and
  the routing models (edge-routed vs. centrally-routed bridging)
- Explain EVPN route types 2, 3, and 5 well enough to troubleshoot
  from `show evpn database`
- Operate fabrics with Apstra intent — and know what the exams expect
  you to do by hand
- Map JNCIA-DC (JN0-281), JNCIS-DC (JN0-481), and JNCIP-DC (JN0-683)
  to this material, with JNCIE-DC (JPR-981) as Chapter 09's target

## Theory and Architecture

### The track in one sentence

The Data Center track certifies spine-leaf fabrics on QFX: an IP
underlay whose only job is loopback reachability, an EVPN control
plane distributing MAC and IP reachability in BGP, and VXLAN
encapsulation stretching Layer 2 without stretching failure domains.
JNCIA-DC (JN0-281) sets the concepts; JNCIS-DC (JN0-481) builds
single-fabric competence; JNCIP-DC (JN0-683) adds DCI, multicast
optimization, and advanced troubleshooting. All 90-minute/65-question
written exams; notably, **JNCIS-ENT is an accepted alternative
prerequisite for JNCIP-DC** — the tracks share the EVPN core (codes
and the cross-track prerequisite verified on Juniper's pages, 22 July
2026).

### Underlay/overlay, ruthlessly separated

The underlay is eBGP per link, private ASN per switch, advertising
loopbacks — nothing else. The overlay is multihop eBGP (or iBGP+RR)
between loopbacks carrying family `evpn`. Type-2 routes carry
MAC(+IP) — the fabric's ARP suppression and mobility; Type-3 builds
the flood lists for BUM traffic; Type-5 carries IP prefixes for
routing in and out. **ESI-LAG** gives servers active-active dual
homing with the fabric, not MC-LAG, holding the state.

### Where routing happens

**Edge-routed bridging (ERB)** puts anycast IRB gateways on every
leaf — the default modern answer, local routing, symmetric IRB with
Type-5. **Centrally-routed (CRB)** keeps gateways on spines/border
leaves — simpler leaves, hairpin costs. JNCIP-DC scenarios turn on
choosing and defending one against requirements.

## Design Considerations

- 3-stage for a pod; 5-stage (super-spines) only when pod count
  demands; never stretch a fabric where a Type-5-stitched DCI belongs
- Fabric-wide MTU with headroom for the VXLAN outer header — the
  classic silent killer
- **Apstra** (Juniper's intent system) designs, deploys, and
  continuously validates fabrics; the exams still require the
  underlying Junos literacy Apstra renders — learn hand-built first,
  then let intent own day 2

## Implementation and Automation

```text
# One leaf's slice of an ERB fabric (abridged)
set policy-options policy-statement EXPORT-LO term 1 from route-filter 10.30.255.0/24 orlonger
set policy-options policy-statement EXPORT-LO term 1 then accept
set protocols bgp group UNDERLAY type external export EXPORT-LO
set protocols bgp group UNDERLAY neighbor 172.20.0.0 peer-as 65101
set protocols bgp group OVERLAY type external multihop no-nexthop-change
set protocols bgp group OVERLAY local-address 10.30.255.11 family evpn signaling
set protocols bgp group OVERLAY neighbor 10.30.255.1 peer-as 65100

set protocols evpn encapsulation vxlan
set protocols evpn extended-vni-list all
set switch-options vtep-source-interface lo0.0
set switch-options route-distinguisher 10.30.255.11:1
set switch-options vrf-target target:65000:1

set vlans V10 vlan-id 10 vxlan vni 10010
set vlans V10 l3-interface irb.10
set interfaces irb unit 10 virtual-gateway-address 10.30.10.1
set interfaces irb unit 10 family inet address 10.30.10.11/24
```

## Validation and Troubleshooting

- Underlay first: `show bgp summary` — every fabric problem that is
  actually an underlay problem announces itself here
- `show evpn database mac-address <mac>` — which VTEP owns the MAC,
  and did mobility sequence numbers move it?
- `show ethernet-switching vxlan-tunnel-end-point remote` — the VTEP
  flood list Type-3 built
- `show route table bgp.evpn.0 match-prefix 5:*` — Type-5 presence
  when inter-subnet routing fails
- Silent large-packet loss with working pings = MTU; prove it with
  size-swept ping before touching config

## Security and Best Practices

- Fabric management out of band; underlay ASN/prefix hygiene so a leaf
  can never become transit
- Tenant separation with per-VRF Type-5 routing instances and distinct
  route targets; firewall inter-tenant traffic at a services leaf, not
  on anycast gateways
- Storm control and BPDU protect on server ports — EVPN loops are
  rarer but louder

## References and Knowledge Checks

- JNCIA-DC (JN0-281), JNCIS-DC (JN0-481), JNCIP-DC (JN0-683)
  objectives on Juniper's certification pages
- Junos EVPN-VXLAN user guide; Juniper validated designs for ERB
  fabrics; Apstra documentation

Knowledge checks:

1. A VM moves leaves; some hosts still send traffic to the old leaf.
   Which EVPN mechanism should have fixed this, and what do you check
   in the database?
2. Why does ERB pair naturally with symmetric IRB and Type-5 routes?
3. Defend using eBGP for both underlay and overlay in one fabric —
   and name the knob that keeps overlay next-hops unchanged.

## Hands-On Lab

Five vJunos-switch instances: two spines, three leaves. eBGP underlay
(unique ASN per switch), multihop eBGP EVPN overlay, two tenant VLANs
with anycast IRBs in ERB, one server dual-homed via ESI-LAG. Prove
same-VLAN and inter-VLAN flows across leaves; then induce an
asymmetric-MTU failure on one spine link and a withdrawn loopback
export on one leaf, capturing both distinct signatures before repair.

## Lab Verification

Verification means the EVPN database shows every host MAC on the
expected VTEP, ESI-LAG carries traffic with either uplink down, both
induced failures produced the predicted evidence (size-swept ping
loss; overlay session down with underlay still up), and the fabric
returned to a clean `show bgp summary`.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Underlay/overlay separation built and explained
- [ ] EVPN route types 2/3/5 used in real troubleshooting
- [ ] ERB vs. CRB decision defended; ESI-LAG proven
- [ ] DC exam ladder (JN0-281/481/683) and the ENT cross-prerequisite
      recorded
- [ ] Lab failures induced, evidenced, repaired
