# Chapter 08: Provider QoS, Multicast, and the Edge

## Learning Objectives

- Design the provider QoS model: the DiffServ tunneling modes and the
  edge-conditioning-plus-core-trust pattern
- Configure hierarchical QoS on IOS XR: classification, policing,
  shaping, and queuing at the provider edge
- Implement provider multicast: PIM, mVPN, and the label/BGP-based
  multicast that scales it
- Harden the provider control plane with LPTS and infrastructure ACLs
- Validate QoS behavior and multicast delivery, and troubleshoot the
  edge

## Theory and Architecture

### QoS as a wholesale contract

An enterprise marks and queues its own traffic (Volume III); a
provider sells a **QoS contract** to many customers and must condition
what they inject and honor what it promised, at scale. The model
splits by role: **the edge (PE) conditions** — classifies customer
traffic into the provider's class scheme, polices to the sold rate,
and marks the core-facing header — while **the core (P) trusts** those
markings and queues fast. This mirrors Volume XXVII's trust-boundary
thinking and Chapter 03's "the CE is untrusted": the PE is where the
provider imposes its will.

**DiffServ tunneling** is the exam-critical mechanism. When customer
traffic enters an MPLS L3VPN/L2VPN, the provider sets the MPLS EXP
(Traffic Class) bits, and the relationship between the customer's
DSCP and the provider's EXP is one of three **modes**:

- **Uniform** — customer and provider markings are coupled; a change
  in one reflects in the other (the provider's re-marking propagates
  back to the customer on egress). One coherent QoS domain.
- **Pipe** — provider markings are independent and hidden; the
  customer's original marking is restored on egress, but the core
  queues on the provider's EXP. The provider's QoS is invisible to the
  customer.
- **Short-pipe** — like pipe, but egress queuing uses the customer's
  marking rather than the provider's.

Choosing the mode is choosing whose markings govern where — a wholesale
policy decision SPCOR tests directly.

### Hierarchical QoS at the edge

Providers sell tiered rates per customer per class, which needs
**H-QoS**: a parent shaper enforcing the customer's total sold rate,
with child policies queuing per class inside it. IOS XR expresses this
as nested policy-maps — parent shape, child class queuing — so one
physical port serves many customers each with their own contract.

### Provider multicast

Delivering multicast across a VPN core (SPRI's Multicast Routing, 15%)
uses **PIM** at the edges and, in the core, **mVPN**: either
**Draft-Rosen** (GRE-based, legacy) or the modern **BGP/MPLS mVPN**
(profiles using MP-BGP multicast address families and P-tunnels — mLDP
or SR — to build provider multicast trees). The scaling idea matches
the whole volume: push state to the edge, keep the core carrying
aggregate trees, not per-customer-per-group state.

### The provider edge is a boundary

The PE is where security, QoS, and services all concentrate, and
control-plane protection matters most because the PE terminates
untrusted customer sessions. On IOS XR, **LPTS** (Local Packet
Transport Services) automatically polices control-plane traffic to the
RP — the XR analog of CoPP, largely built-in but tunable — and
**infrastructure ACLs (iACLs)** at the edge keep the core's addressing
unreachable from customers.

## Design Considerations

- **Pick the DiffServ mode per service tier deliberately**: pipe for
  wholesale where the provider's QoS must be invisible and
  authoritative; uniform where one coherent domain with the customer
  is intended.
- **Edge conditions, core trusts** — never re-classify deep in the
  core; if the edge did its job, the core just queues.
- **H-QoS parent = sold rate, exactly**: like Volume XXVIII's CAC-
  equals-LLQ discipline, the shaper and the contract must match or the
  SLA is fiction.
- **mVPN profile chosen for scale and platform**: modern BGP/MPLS
  profiles over Draft-Rosen for new builds; consistency across the
  core is mandatory.

## Implementation and Automation

Edge H-QoS with DiffServ pipe mode on an IOS XR PE:

```text
class-map match-any VOICE
 match dscp ef
class-map match-any BUSINESS
 match dscp af31 af32

policy-map CHILD-CUST-A
 class VOICE
  priority level 1
  police rate 10 mbps
 class BUSINESS
  bandwidth percent 40
 class class-default
  bandwidth percent 20

policy-map PARENT-CUST-A
 class class-default
  shape average 100 mbps          ! the customer's sold aggregate rate
  service-policy CHILD-CUST-A

interface GigabitEthernet0/0/0/3
 service-policy input CUST-A-INGRESS-MARK   ! classify+police+set EXP (pipe)
 service-policy output PARENT-CUST-A
```

```text
! Validation
show policy-map interface GigabitEthernet0/0/0/3 output
show qos interface GigabitEthernet0/0/0/3 output
show mpls forwarding labels ... detail       ! EXP handling
show lpts pifib hardware police               ! control-plane policing
show mrib route / show pim neighbor           ! multicast health
```

## Validation and Troubleshooting

QoS validation is counter-driven: offer congestion and confirm the
priority class is protected while lower classes drop
(`show policy-map interface` queue/drop counters), and confirm the
policer meters customer ingress to the sold rate. DiffServ-mode
validation: send marked traffic through the VPN and confirm egress
markings match the chosen mode (pipe restores customer DSCP; uniform
propagates provider changes) — read the DSCP/EXP at ingress, core, and
egress. Multicast: `show pim neighbor` and `show mrib route` for the
tree, and confirm receivers actually get the stream (the provider
analog of Volume XXVIII's MOH check). Faults: H-QoS parent/child
misnesting (child queuing not taking effect — read the applied
policy); wrong DiffServ mode (customer sees provider markings they
should not, or vice versa); LPTS drops of legitimate control traffic
under attack/load (tune the flow-type policers); and mVPN trees not
building (profile mismatch or P-tunnel/label issue — Chapter 04
transport again).

## Security and Best Practices

- LPTS/iACL as the edge's control-plane defense — the PE faces
  untrusted customers, so this is not optional hardening.
- Policing at ingress is a security control too: it caps a customer's
  ability to flood the core, intentionally or not.
- uRPF at customer-facing interfaces to blunt spoofed-source attacks
  from the CE; BCP 38 ingress filtering is provider hygiene.
- Multicast admission and boundary controls so a customer cannot
  source into the provider's multicast where they should not.

## References and Knowledge Checks

- SPCOR Services (20%, QoS portion) and Networking; SPRI Multicast
  Routing (15%)
- Cisco IOS XR QoS (H-QoS, MPLS DiffServ) and multicast/mVPN
  configuration guides
- RFC 3270 (MPLS DiffServ), RFC 6513/6514 (BGP/MPLS mVPN)

Knowledge checks:

1. Contrast uniform, pipe, and short-pipe DiffServ modes by whose
   marking governs core queuing and egress, and give a use case for
   pipe.
2. Why does the edge condition and the core trust, and what goes
   wrong if the core reclassifies?
3. In H-QoS, what enforces the customer's total sold rate versus the
   per-class treatment, and how must the parent relate to the
   contract?
4. What does LPTS protect, and why does the PE need it more than a
   core P router does?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **the QoS, security,
IPv6-transition, and multicast objectives of SPCOR 350-501 v1.1, Domain 2
(Multicast) of SPRI 300-510 v1.1, and Domain 4 (Security) of SPCNI 300-540 v1.0**
— mapped in the volume README's coverage tables. Labs use the IOS XR CLI. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.15** — an IOS XR edge/core with MQC QoS
policies, LPTS/CoPP, uRPF and ACLs, a PIM-SM multicast domain, CGNAT for IPv6
transition, and an NFVI for the SPCNI security labs. **Cost:** none beyond lab
resources.

### Lab 8.1 — Describe QoS architecture (SPCOR Objective 1.4)

**Objective:** Read the ingress/egress QoS policy chain.

```text
show policy-map interface <intf> input
show policy-map interface <intf> output
show qos interface <intf> output
```

**Expected result:** classification/marking on ingress and queuing/shaping on
egress — the SP QoS architecture classifies and marks (DSCP/MPLS EXP/traffic-class)
at the edge, then the core trusts and queues by class; MQC (class-map/policy-map/
service-policy) expresses it.

**Negative test:** trust customer markings at the edge without a policing/re-mark
policy; a customer can mark all traffic to the priority class — the edge must
condition and re-mark untrusted traffic.

**Cleanup:** none (read-only).

### Lab 8.2 — Implement QoS services (SPCOR Objective 4.5)

**Objective:** Apply an egress QoS policy (priority + bandwidth) and verify.

```text
show policy-map interface <core-intf> output
show qos interface <core-intf> output | include "queue|drop|priority"
```

**Expected result:** the priority (LLQ) queue for real-time and weighted queues
for the rest, with counters — SP QoS services deliver per-class SLAs: strict
priority for voice/video, bandwidth guarantees for business classes, and WRED for
TCP-friendly drop in best-effort.

**Negative test:** a priority class with no policer under overload starves other
queues; conversely an undersized priority queue drops real-time traffic — size the
priority class to the committed rate.

**Cleanup:** none (read-only).

### Lab 8.3 — Configure and verify control-plane security (SPCOR Objective 1.5)

**Objective:** Verify LPTS/CoPP protecting the route processor.

```text
show lpts pifib hardware police location 0/RP0/CPU0 | head
show lpts flows | head
```

**Expected result:** the LPTS policers rate-limiting punted control traffic — IOS
XR protects the control plane with **LPTS** (Local Packet Transport Services),
hardware-policing each protocol's punt path so a flood cannot overwhelm the RP; it
is CoPP done in the data plane.

**Negative test:** disable/raise an LPTS policer for a protocol and a flood of that
traffic can spike RP CPU — the policers are the control-plane protection.

**Cleanup:** none (read-only).

### Lab 8.4 — Describe management-plane security (SPCOR Objective 1.6)

**Objective:** Read the management-plane hardening.

```text
show run ssh 2>/dev/null; show ssh
show run | include "management-plane|mpp"
show run aaa 2>/dev/null | head
```

**Expected result:** SSH-only access, Management Plane Protection (MPP) limiting
which interfaces accept management, and AAA — management-plane security restricts
management protocols to specific interfaces/subnets, uses SSH/HTTPS/NETCONF over
TLS, and authenticates via AAA with role-based access.

**Negative test:** leave management reachable on all interfaces including customer-
facing ones; the RP is exposed to customers — MPP must scope management to the
management network.

**Cleanup:** none (read-only).

### Lab 8.5 — Implement data-plane security (SPCOR Objective 1.7)

**Objective:** Verify uRPF and edge ACLs protecting the data plane.

```text
show run interface <edge-intf> | include "rpf|access-group"
show access-lists <name> hardware ingress 2>/dev/null | head
show cef <spoofed-prefix> | include "drop|RPF"
```

**Expected result:** uRPF and an infrastructure/anti-spoofing ACL — data-plane
security uses **uRPF** (drop packets whose source is not routed back out the
ingress), edge ACLs (BCP38 anti-spoofing, infrastructure ACLs protecting core
addresses), and RTBH for attack mitigation.

**Negative test:** loose-mode uRPF on an asymmetric multihomed edge over-drops
legitimate traffic; strict uRPF fits single-homed, loose fits multihomed — the
mode must match the topology.

**Cleanup:** none (read-only).

### Lab 8.6 — Describe IPv6 transition mechanisms (SPCOR Objective 2.7)

**Objective:** Read a CGNAT / IPv6-transition translation.

```text
show cgn nat44 statistics 2>/dev/null | head
show nat64 statistics 2>/dev/null | head
show cgn nat44 inside-translation 2>/dev/null | head
```

**Expected result:** the translation counters — SP IPv6 transition uses
**NAT44/CGNAT** (extend IPv4 life via carrier-grade NAT), **NAT64**/**464XLAT**,
**MAP-T** (stateless), and **DS-Lite** (IPv4 over IPv6 with CGN) to carry IPv4
customers over an IPv6 (or exhausted-IPv4) network.

**Negative test:** deploy stateful CGNAT without logging/port-block allocation and
you cannot map a session back to a subscriber for lawful intercept/abuse — port-
block logging is required at SP scale.

**Cleanup:** none (read-only).

### Lab 8.7 — Implement multicast services (SPCOR Objective 4.4)

**Objective:** Verify multicast forwarding on the provider network.

```text
show mrib route summary
show mfib route summary
show pim neighbor
```

**Expected result:** the MRIB/MFIB state and PIM neighbors — SP multicast services
deliver one-to-many (IPTV, market data) efficiently; PIM builds the distribution
tree and the MFIB forwards, with the SP choosing SSM/ASM and RP placement.

**Negative test:** expect multicast delivery with PIM neighbors up but no RP (for
ASM) reachable; (*,G) state cannot build — ASM needs a reachable RP (or use SSM to
avoid it).

**Cleanup:** none (read-only).

### Lab 8.8 — Compare multicast concepts (SPRI Objective 2.1)

**Objective:** Contrast ASM, SSM, and BIDIR.

```text
show pim group-map
show mrib route <group> | include "SSM|Bidir|Sparse"
```

**Expected result:** the group-to-mode mapping — **ASM** (any-source, needs an RP
and shared tree, switches to shortest-path), **SSM** (source-specific, no RP, host
signals (S,G) via IGMPv3), **BIDIR** (bidirectional shared tree, scales many
senders) — each fits a different SP service.

**Negative test:** run IPTV (well-known sources) as ASM with RP complexity when SSM
removes the RP entirely — the mode should match the application's source model.

**Cleanup:** none (read-only).

### Lab 8.9 — Describe multicast concepts (SPRI Objective 2.2)

**Objective:** Read RPF, the distribution tree, and RP discovery.

```text
show pim rpf <source>
show mrib route <group> | include "RPF|Incoming|Outgoing"
show pim rp mapping
```

**Expected result:** the RPF interface, the tree's incoming/outgoing list, and RP
mapping — multicast forwards by **RPF** (accept only from the interface toward the
source), builds shared/shortest-path trees, and discovers RPs (static, Auto-RP,
BSR) for ASM.

**Negative test:** an RPF failure (the source is reachable via a different
interface than multicast arrives on) drops the stream — unicast routing and the
multicast path must agree, or use a static mroute.

**Cleanup:** none (read-only).

### Lab 8.10 — Implement PIM-SM operations (SPRI Objective 2.3)

**Objective:** Verify PIM-SM shared-to-shortest-path tree behavior.

```text
show pim neighbor
show mrib route <group>          ! (*,G) then (S,G)
show pim rp mapping
```

**Expected result:** a (*,G) via the RP that transitions to (S,G) shortest-path —
PIM-SM starts on the shared tree rooted at the RP, then the last-hop router joins
the source's shortest-path tree and prunes off the shared tree once traffic flows.

**Negative test:** a first-hop router that never registers to the RP leaves the
source invisible on the shared tree; receivers get nothing until SPT — the source
registration to the RP is required for ASM.

**Cleanup:** none (read-only).

### Lab 8.11 — Troubleshoot multicast routing (SPRI Objective 2.4)

**Objective:** Diagnose a receiver not getting the stream.

```text
show igmp groups <group>
show mrib route <group> | include "Outgoing|Incoming|RPF"
show pim rpf <source>
```

**Expected result:** the IGMP membership, the OIL, and the RPF — no stream traces
to missing IGMP join (receiver side), an empty outgoing-interface list (no tree
built), or an RPF failure (unicast path mismatch); the three checks localize the
tier.

**Negative test:** blame the source for a receiver with no IGMP membership on its
last-hop router — the receiver never asked for the group; check IGMP first.

**Cleanup:** none (read-only).

### Lab 8.12 — Implement infrastructure security (SPCNI Objective 4.1)

**Objective:** Verify infrastructure hardening across the NFVI/fabric.

```text
show access-lists <infra-acl> hardware ingress 2>/dev/null | head
show run | include "rpf|ssh|mpp|snmp-server"
```

**Expected result:** the infrastructure ACL, uRPF, and hardened management — NFVI/
infrastructure security layers anti-spoofing (uRPF, iACLs protecting the core),
management hardening (SSH/MPP/AAA), and control-plane protection (LPTS), so the
shared infrastructure resists attack.

**Negative test:** an NFVI management network reachable from tenant workloads lets
a compromised VNF attack the infrastructure — the management plane must be isolated
from tenant data planes.

**Cleanup:** none (read-only).

### Lab 8.13 — Describe DoS mitigation techniques (SPCNI Objective 4.2)

**Objective:** Read the DoS/DDoS mitigation controls.

```text
show cef <victim>/32 | include "drop|Null0"       ! RTBH
show flowspec ipv4 2>/dev/null | head              ! BGP FlowSpec rules
show lpts pifib hardware police location 0/RP0/CPU0 | head
```

**Expected result:** RTBH/FlowSpec rules and LPTS policing — DoS mitigation uses
**RTBH** (blackhole the victim or source via a triggered /32 to Null0), **BGP
FlowSpec** (distribute granular drop/rate-limit filters), scrubbing centers, and
LPTS/uRPF for infrastructure protection.

**Negative test:** destination-based RTBH completes the attacker's goal (the victim
is unreachable); source-based RTBH or FlowSpec drops only the attack — choose the
mitigation that preserves the service.

**Cleanup:** none (read-only).

### Lab 8.14 — Describe NFVI security (SPCNI Objective 4.3)

**Objective:** Read the NFVI isolation and trust controls.

```bash
virsh domiflist vnf-router 2>/dev/null | head
! Confirm tenant network isolation (VLAN/VXLAN), secure boot, and hypervisor hardening
```

**Expected result:** the VNF's isolated networks — NFVI security isolates tenants
(segmentation), secures the hypervisor/host (secure boot, minimal attack surface),
protects the VIM/orchestrator (RBAC, API auth), and validates VNF images, so one
tenant cannot reach another or the infrastructure.

**Negative test:** two VNFs sharing an unsegmented management bridge can reach each
other's control interfaces — tenant and management isolation must be enforced in the
NFVI.

**Cleanup:** none (read-only).

### Lab 8.15 — Describe cloud security solutions (SPCNI Objective 4.4)

**Objective:** Read the cloud-edge security controls (DNS security, etc.).

```bash
dig +dnssec example.com @<resolver> | grep -E "ad|RRSIG" | head
! Confirm DNS security (DNSSEC/DNS-layer filtering), zero-day/AV, and virtual FW/IPS at the edge
```

**Expected result:** DNSSEC/secure-resolver behavior and the security stack —
cloud security solutions add **DNS-layer security** (DNSSEC, malicious-domain
filtering), **zero-day/AV** (sandboxing, threat intel), and **virtualized
firewall/IPS** at the cloud edge, protecting tenant workloads and subscribers.

**Negative test:** rely on perimeter firewalls alone for cloud workloads; east-west
traffic between VNFs bypasses the perimeter — microsegmentation/virtual FW is needed
inside the cloud too.

**Cleanup:** none (read-only).

## Lab Verification

Verification means QoS counters proved protection and policing, the
DiffServ mode's egress behavior was read and confirmed, provider
multicast delivered across the VPN, and both induced faults were
diagnosed. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Provider QoS is a wholesale contract: the edge conditions untrusted
customer traffic and sets the core-facing marking, the core trusts and
queues, and DiffServ tunneling modes decide whose markings govern
where. H-QoS sells tiered rates per customer, mVPN scales multicast by
keeping per-group state at the edge, and LPTS/iACL/uRPF harden the PE
boundary. This completes SPCOR's Services domain and SPRI's multicast
domain.

- [ ] I can choose and justify a DiffServ tunneling mode per tier
- [ ] My H-QoS parent equals the sold rate and protects VOICE under
      load
- [ ] Provider multicast delivered across the VPN in my lab
- [ ] LPTS/iACL protect my PE's control plane by design
