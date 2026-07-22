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

On the Chapter 06–07 estate: build edge H-QoS for CUST-A — an ingress
policy that classifies, polices to a sold rate, and sets EXP in
**pipe** mode, and a parent shaper at the customer's aggregate with
child per-class queuing. Congest the link and prove (counters) that
VOICE is protected while class-default drops, and that ingress
policing caps the customer. Verify DiffServ pipe behavior by reading
DSCP at ingress and egress (customer marking restored) and EXP in the
core. Build provider multicast (PIM edges, a modern mVPN profile) and
prove a receiver at one site gets a source at another across the VPN.
Break and diagnose: switch the DiffServ mode to uniform and show the
changed egress marking; break the child policy nesting and show
queuing not applying. Restore.

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
