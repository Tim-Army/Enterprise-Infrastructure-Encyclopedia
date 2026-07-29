# Chapter 01: Data Center Architecture and the CCNP Data Center Track

## Learning Objectives

- Explain why data center networking diverged from campus networking,
  and what spine-leaf topologies solve that three-tier designs could not
- Identify the Cisco data center platform families — Nexus switching,
  MDS storage switching, UCS compute, ACI, Nexus Dashboard, and
  Intersight — and what each manages
- Distinguish the three operational models: device-centric NX-OS,
  controller-based ACI, and SaaS-delivered Intersight
- Describe the CCNP Data Center track structure and choose a
  concentration exam deliberately
- Stand up the lab environment used throughout this volume

## Theory and Architecture

### Why the data center is its own discipline

Campus networks move traffic between people and services; data center
networks move traffic between services. The consequences invert most
campus assumptions. Traffic is dominantly **east-west** (server to
server) rather than north-south. Failure domains must be small because
one rack hosts hundreds of workloads. Oversubscription that is
tolerable at a campus access layer breaks distributed applications that
expect uniform any-to-any bandwidth. And change velocity is set by
application teams deploying daily, not by a quarterly network change
window.

The classic three-tier design — access, aggregation, core — answered
north-south patterns with hierarchy. It scaled poorly east-west:
traffic between two access switches traversed the aggregation layer,
spanning tree blocked half the links, and the aggregation pair became
both a bottleneck and a large failure domain.

### Spine-leaf: the answer the whole industry converged on

A **spine-leaf** (Clos) fabric has two roles only. Every **leaf**
connects to every **spine**; leaves never connect to each other, spines
never connect to each other. Endpoints, services, and external routers
attach at leaves. The properties that follow are why the design won:

- **Uniform path length.** Any leaf is exactly two hops from any other,
  so latency and bandwidth are predictable regardless of placement.
- **Horizontal scale.** Need more capacity? Add a spine. Need more
  ports? Add a leaf. Neither disturbs the existing fabric.
- **All links forwarding.** The fabric routes at Layer 3 with ECMP
  across every spine; nothing is blocked by spanning tree.
- **Small failure domains.** A leaf failure strands one rack's uplinks;
  a spine failure removes one ECMP path fabric-wide.

What runs *over* that routed underlay is the overlay — VXLAN with an
EVPN control plane in NX-OS fabrics, or ACI's policy-driven fabric —
and that split between underlay and overlay organizes Chapters 02 and
03.

### The platform landscape

| Platform | Role | Managed by |
| --- | --- | --- |
| Nexus 9000 | Data center switching; runs NX-OS standalone or ACI mode | CLI/NX-API, NDFC, or APIC |
| Nexus Dashboard (with NDFC) | Fabric controller for NX-OS mode: underlay/overlay provisioning, imaging, telemetry | Web UI / API |
| APIC | The ACI fabric's controller cluster; the single point of policy | Web UI / API |
| MDS 9000 | Dedicated Fibre Channel storage switching | CLI, DCNM/NDFC |
| UCS (B-, C-, X-Series) | Servers: blades, racks, and the modular X-Series | UCS Manager or Intersight |
| Intersight | SaaS management for UCS and HyperFlex; increasingly the default | Cloud portal / API |

### Three operational models, one building

The exam track and real estates both mix three ways of running this
gear. **Device-centric NX-OS** — each switch configured directly, with
automation layered on top; maximum control and the model Chapter 02
teaches first. **Controller-based ACI** — the APIC holds intent as
policy and renders it onto the fabric; the admin configures the
controller, never the switch (Chapter 03). **Cloud-operated
Intersight** — management plane as SaaS, with the API as the primary
interface (Chapters 04 and 06). A working engineer moves among all
three daily; the track's concentration exams essentially let you pick
which one to go deepest in.

## Design Considerations

- **Fabric sizing starts from ports and oversubscription, not
  models.** Count server-facing ports, decide the leaf-to-spine
  oversubscription ratio the applications tolerate (3:1 is a common
  general-purpose target; AI clusters demand 1:1 — Chapter 07), and the
  spine count falls out.
- **Border placement is a decision, not a default.** External
  connectivity concentrates at border leaves; making every leaf a
  border spreads complexity everywhere.
- **Pick the operational model per fabric, deliberately.** ACI rewards
  estates that will actually use its policy model and integrations;
  NX-OS with NDFC suits teams who want EVPN semantics they can read.
  Running ACI as a "fancy VLAN fabric" buys its complexity without its
  payoff.
- **Management network first.** Out-of-band management for every
  switch, APIC, and fabric interconnect is the precondition for
  everything else in this volume, including recovery from your own
  mistakes.

## Implementation and Automation

The volume's running lab is built in Cisco Modeling Labs with Nexus
9000v images: two spines, four leaves, all point-to-point routed links.
Verify the baseline before Chapter 02 builds on it:

```text
! Each fabric link is a routed interface — no switchport, jumbo MTU,
! because VXLAN adds 50 bytes and storage and AI traffic want 9216.
interface Ethernet1/1
  no switchport
  mtu 9216
  ip address 10.1.1.1/31
  no shutdown
```

```text
# From a leaf, confirm every spine adjacency and ECMP path:
show ip ospf neighbors
show ip route 10.0.0.0/8 | include ecmp|via
# Platform identity and image train — know what you are running:
show module
show version | include NXOS
```

Automation enters immediately, not in Chapter 06: enable NX-API now so
later chapters can drive the same lab programmatically.

```text
feature nxapi
nxapi https port 443
```

## Validation and Troubleshooting

Structured validation of a new fabric follows its layers: physical
(interfaces up, MTU consistent — `show interface status`,
`show interface | include MTU`), underlay routing (all spine
adjacencies full, ECMP route count matches spine count), and only then
overlay and services. The most common bring-up faults are MTU mismatch
(underlay pings pass, VXLAN traffic silently fails — test with
`ping ... df-bit packet-size 9000`) and /31 addressing mistakes that
leave OSPF stuck in INIT. Troubleshooting method — isolate the layer,
prove it independently, move up — is developed into a full methodology
in Chapter 09.

## Security and Best Practices

- Out-of-band management on a dedicated VRF (`management` exists for
  this); never manage the fabric in-band through the workloads it
  carries.
- AAA against TACACS+ from day one; local accounts are break-glass
  only. Chapter 08 builds the full model.
- Disable unused services (`feature` is opt-in on NX-OS — keep it
  that way) and set login banners and NTP before the first workload
  lands, because forensic timelines depend on synchronized clocks.

## References and Knowledge Checks

- Cisco Learning Network — CCNP Data Center track and exam-topics pages
  for DCCOR 350-601 v1.2 and the five concentrations
- Cisco Nexus 9000 NX-OS configuration guides (platform documentation)
- Cisco Live sessions on spine-leaf and VXLAN EVPN design (BRKDCN track)

Knowledge checks:

1. Why does a spine-leaf fabric need no spanning tree between fabric
   nodes, and what replaces its loop prevention?
2. A design shows two leaves cabled to each other "for redundancy."
   What property of the Clos design does that break?
3. Which operational model puts intent on a controller and renders it
   to switches — and what is the admin no longer allowed to do?
4. Your VXLAN traffic fails but underlay pings succeed. What is the
   first parameter to check, and with what test?

## Hands-On Lab

Build the volume's running topology in CML: two Nexus 9000v spines,
four leaves, /31 routed links, MTU 9216 everywhere, OSPF (or IS-IS if
you prefer — the volume shows OSPF) as the underlay IGP, NX-API
enabled. Capture `show ip ospf neighbors` and the ECMP route table from
two leaves. Deliberately misconfigure one fabric link's MTU to 1500,
prove the failure mode with a df-bit ping, and restore it. Export the
lab topology file; every later chapter reuses it.

## Lab Verification

Verification means the topology converged with full ECMP, the MTU
failure was demonstrated and repaired, and the exported topology loads
cleanly. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Data center networking is its own discipline because its traffic,
failure-domain, and change-velocity assumptions all differ from the
campus. Spine-leaf answers them with uniform paths, horizontal scale,
and routed ECMP; the platform landscape layers three operational models
over that fabric; and the CCNP Data Center track certifies the whole
stack — core plus one chosen concentration.

- [ ] I can explain spine-leaf properties and why leaf-to-leaf links
      are wrong
- [ ] I can name each platform family and its management plane
- [ ] I know which concentration exam matches my role
- [ ] The CML baseline fabric is built, converged, and exported
