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

This chapter carries a topic-level walkthrough lab for **every exam objective of
the JNCIS-DC (JN0-481) exam** — the Data Center specialist (EVPN-VXLAN and Juniper
Apstra) — mapped in the volume README's coverage tables. Labs use the Junos CLI on
QFX switches and the Apstra server/API. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.7** — a QFX spine-leaf fabric running EVPN-
VXLAN, and a Juniper Apstra server managing (a subset of) the fabric with device
agents installed. **Cost:** none beyond lab resources.

### Lab 5.1 — Data Center Architectures: IP Fabric and EVPN-VXLAN (Objective: Data Center Architectures)

**Objective:** Verify the IP fabric underlay and the EVPN-VXLAN overlay.

```text
show bgp summary
show evpn database
show ethernet-switching vxlan-tunnel-end-point remote
show route table bgp.evpn.0 | match "2:|5:"
```

**Expected result:** the underlay BGP (or IGP) ECMP paths, the EVPN MAC/IP database,
and remote VTEPs — a DC **IP fabric** is a routed spine-leaf with ECMP; **EVPN**
(BGP control plane) advertises MAC/IP (Type-2) and IP prefixes (Type-5) over
**VXLAN** (VNI-to-VLAN mapping, VTEP encapsulation), with ERB placing the L3 gateway
on the leaves.

**Negative test:** a leaf whose VNI-to-VLAN mapping differs from its peers cannot
bridge that segment; the endpoints do not learn each other — the VNI mapping must be
consistent fabric-wide.

**Cleanup:** none (read-only).

### Lab 5.2 — Juniper Apstra Architecture (Objective: Juniper Apstra Architecture)

**Objective:** Read the Apstra server, agents, and RBAC.

```bash
curl -sk -u admin:$PW "https://$APSTRA/api/systems" | jq -r '.items[]? | "\(.id) \(.status.agent_state)"' | head
curl -sk -u admin:$PW "https://$APSTRA/api/user/roles" 2>/dev/null | jq '.items | length'
```

**Expected result:** the managed systems with agent state and the RBAC roles —
**Apstra** is an intent-based DC controller: the **server** holds the single source
of truth (a graph), **device agents** on each switch apply and telemeter config, and
RBAC/event-log/syslog govern and record operations.

**Negative test:** a switch whose Apstra agent is disconnected shows `agent_state`
not connected; Apstra cannot deploy or telemeter it — the agent link is the control
path.

**Cleanup:** none (read-only).

### Lab 5.3 — Apstra Design Phase (Objective: Apstra Design Phase)

**Objective:** Read the design-phase objects (logical devices, rack types, templates).

```bash
curl -sk -u admin:$PW "https://$APSTRA/api/design/logical-devices" | jq -r '.items[]?.display_name' | head
curl -sk -u admin:$PW "https://$APSTRA/api/design/rack-types" | jq -r '.items[]?.display_name' | head
curl -sk -u admin:$PW "https://$APSTRA/api/design/templates" | jq -r '.items[]?.display_name' | head
```

**Expected result:** the logical devices, rack types, and templates — the Apstra
**design phase** builds reusable abstractions: **logical devices** (port roles/
speeds), **interface maps** (logical→physical via device profiles), **rack types**,
and **templates** (the fabric blueprint's shape and spine capacity), independent of
specific hardware.

**Negative test:** a rack type referencing a logical device with no matching
interface map/device profile cannot be built — the design abstractions must resolve
to real hardware.

**Cleanup:** none (read-only).

### Lab 5.4 — Apstra Build and Deploy Phases (Objective: Apstra Build and Deploy Phases)

**Objective:** Read a blueprint's device assignment and deploy mode.

```bash
BP=$(curl -sk -u admin:$PW "https://$APSTRA/api/blueprints" | jq -r '.items[0].id')
curl -sk -u admin:$PW "https://$APSTRA/api/blueprints/$BP/nodes?node_type=system" | jq -r '.nodes[]? | "\(.label) \(.deploy_mode)"' | head
```

**Expected result:** the fabric nodes with their deploy mode (deploy/ready/drain/
undeploy) — the **build/deploy phase** instantiates a blueprint from a template,
assigns real devices (agents, system IDs), maps cabling, and pushes config; deploy
mode controls whether a device is actively configured or drained.

**Negative test:** a node left in `ready` (not `deploy`) mode is modeled but not
configured on the device — the deploy mode gates whether intent reaches the switch.

**Cleanup:** none (read-only).

### Lab 5.5 — Blueprint Operations (Objective: Blueprint Operations)

**Objective:** Read staged vs active state and anomalies.

```bash
curl -sk -u admin:$PW "https://$APSTRA/api/blueprints/$BP/anomalies" | jq '.items | length'
curl -sk -u admin:$PW "https://$APSTRA/api/blueprints/$BP/diff-status" 2>/dev/null | jq '.'
```

**Expected result:** the anomaly count and the staged-vs-active diff — Apstra
blueprint operations separate **staged** (uncommitted intent) from **active**
(deployed), surface **service/probe anomalies**, and support **Time Voyager**
(revision rollback), configlets/property-sets, and adding racks/generic systems,
all with root-cause analysis.

**Negative test:** commit staged changes with unresolved build errors; Apstra blocks
the commit — intent must be consistent before it deploys.

**Cleanup:** none (read-only).

### Lab 5.6 — Data Center Multitenancy (Objective: Data Center Multitenancy)

**Objective:** Read routing zones (VRFs) and virtual networks for tenants.

```bash
curl -sk -u admin:$PW "https://$APSTRA/api/blueprints/$BP/security-zones" | jq -r '.items[]? | .label' | head
curl -sk -u admin:$PW "https://$APSTRA/api/blueprints/$BP/virtual-networks" | jq -r '.virtual_networks[]? | "\(.label) vni=\(.vn_id)"' | head
```

**Expected result:** the routing zones (VRFs) and virtual networks — Apstra
multitenancy uses **routing zones** (VRFs) and **virtual networks** (L2/L3 segments)
bound by **connectivity templates**, with per-tenant routing policy, security
policy, and Data Center Interconnect, isolating tenants over the shared fabric.

**Negative test:** two tenants sharing a routing zone can route between each other —
each tenant needs its own routing zone (VRF) for isolation.

**Cleanup:** none (read-only).

### Lab 5.7 — Intent-Based Analytics (Objective: Intent-Based Analytics)

**Objective:** Read an IBA probe and query the graph.

```bash
curl -sk -u admin:$PW "https://$APSTRA/api/blueprints/$BP/probes" | jq -r '.items[]?.label' | head
curl -sk -u admin:$PW -X POST "https://$APSTRA/api/blueprints/$BP/qe" -H 'Content-Type: application/json' \
  -d '{"query":"node(\"system\", name=\"system\").out(\"hosted_interfaces\")"}' | jq '.count'
```

**Expected result:** the IBA probes and a graph-query result — **Intent-Based
Analytics** continuously validates the fabric against intent: **probes** compute
metrics (e.g., traffic imbalance, missing BGP sessions) and raise anomalies, and the
**graph explorer/queries** let you ask the live model questions.

**Negative test:** a probe whose expected state does not match reality raises an
anomaly — IBA flags the deviation, which is the point of intent-based operation.

**Cleanup:** none (read-only).

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
