# Chapter 04: MPLS and Segment Routing Transport

## Learning Objectives

- Explain MPLS label switching: the label stack, LSPs, LFIB, and PHP
- Configure and validate LDP as the baseline label distribution
  protocol, and read the label bindings
- Explain Segment Routing (SR-MPLS): prefix and adjacency SIDs, the
  SRGB, and why SR removes LDP and RSVP state from the core
- Position SRv6 as the IPv6-native evolution and know where it fits
- Validate the label path end to end and troubleshoot the transport
  layer

## Theory and Architecture

### MPLS: the substrate services ride

MPLS forwards on **labels**, not IP lookups: an ingress **LSR** pushes
a label, core LSRs swap it (a fast, fixed lookup in the **LFIB**), and
the egress pops it — **penultimate hop popping (PHP)** usually strips
the last label one hop early so the egress does a single service
lookup. The value is not speed on modern hardware; it is that the core
forwards on labels while remaining ignorant of the millions of customer
routes those labels represent. **Every service in Chapters 06–08 is a
label stack**: a transport label to reach the egress PE, and a service
label identifying the VPN or pseudowire. SPCOR's MPLS and Segment
Routing domain (20%) and SPRI's (25%) live here.

### LDP: the traditional label distribution

**LDP** distributes labels for IGP loopbacks hop by hop, building an
LSP to every egress. It is simple and ubiquitous, and it is what a
brownfield network runs. Its limitations are exactly what Segment
Routing answers: LDP is another protocol to run and secure, it can
desynchronize from the IGP (the "LDP-IGP sync" problem — traffic
black-holes when the label plane and route plane disagree), and it
holds per-LSP state everywhere.

### Segment Routing: the modern transport

**SR-MPLS** moves the label information into the IGP (Chapter 02's
IS-IS, via TLV extensions — the reason IS-IS's extensibility matters):

- **Prefix-SID** — a globally significant label for a loopback,
  advertised by the IGP; every router computes the label path to it
  from the IGP topology. No LDP.
- **Adjacency-SID** — a locally significant label for a specific link,
  the building block of explicit paths (Chapter 05's TE).
- **SRGB (Segment Routing Global Block)** — the label range reserved
  for prefix-SIDs network-wide; consistent SRGB is a design
  precondition.

What SR buys: **no LDP, no RSVP-TE state in the core** — the ingress
encodes the path as a label stack and the core just forwards, so
per-flow/per-LSP state disappears from P routers. This is the
single biggest operational simplification in modern SP networking, and
the exam treats SR as the default, LDP as the incumbent.

### SRv6, briefly

**SRv6** carries the segment list in an IPv6 extension header (SRH),
using IPv6 addresses as SIDs — no MPLS label plane at all. It unifies
transport and services on IPv6 and is the forward direction Cisco's
platforms are moving toward; SPCOR expects positioning literacy — what
it is, why it exists (IPv6-native, simplified, programmable),
and that SR-MPLS remains the deployed majority.

## Design Considerations

- **Greenfield SR, brownfield migration**: new networks start SR-MPLS;
  existing LDP networks migrate with SR and LDP coexisting (SR
  preferred, LDP as fallback via mapping servers) rather than
  flag-day cutovers.
- **Consistent SRGB network-wide**: pick the range once; inconsistent
  SRGBs make prefix-SID labels differ per node and defeat the
  simplicity SR exists for.
- **Loopback = prefix-SID identity**: the Chapter 02 loopback discipline
  pays off here — each PE's prefix-SID is how every other node label-
  switches to it.
- **Retire LDP deliberately**: once SR is proven, removing LDP removes
  a protocol, its sync hazard, and its state — a real operational win
  worth planning.

## Implementation and Automation

Enable SR-MPLS on the Chapter 02 IS-IS core (this replaces LDP):

```text
segment-routing
 global-block 16000 23999            ! consistent SRGB, all nodes

router isis CORE
 address-family ipv4 unicast
  segment-routing mpls               ! SR in the IGP
 !
 interface Loopback0
  address-family ipv4 unicast
   prefix-sid index 1                ! PE1 = 16001; PE2 index 2 = 16002
```

LDP baseline (for the brownfield comparison the lab also builds):

```text
mpls ldp
 router-id 10.0.0.1
 interface GigabitEthernet0/0/0/0
```

```text
! Validation — the label path to a remote loopback
show mpls forwarding                       ! the LFIB
show segment-routing mpls connected-prefix-sid-map ipv4
show isis segment-routing label table
show mpls ldp bindings 10.0.0.2/32         ! LDP view (comparison)
traceroute mpls ipv4 10.0.0.2/32           ! prove the LSP end to end
```

## Validation and Troubleshooting

Validate the label path the way traffic uses it: pick a remote
loopback, confirm the LFIB has a label operation for it on every hop
(`show mpls forwarding`), and prove the LSP end to end with
`traceroute mpls`. SR-specific checks: prefix-SIDs resolve to
consistent labels (SRGB base + index) across the network, and the
label matches the IGP path. Classic faults: **SRGB inconsistency**
(the same loopback gets different labels on different nodes — SR's
signature misconfiguration); **LDP-IGP desync** in the brownfield case
(IGP route present, label absent → black hole — the exact problem SR
removes); **missing prefix-SID** on a loopback (that PE is reachable
by IP but not label-switched to, so its services fail while ping
works — a telling split); and **MTU** again (label stacks add bytes;
Chapter 02's MTU discipline protects the transport). Method: IP
reachability and label reachability are different questions — test
both, because services need the second.

## Security and Best Practices

- SR shrinks attack surface by removing LDP and RSVP — fewer protocols
  to secure is itself a hardening.
- Where LDP remains, authenticate it and enable IGP sync so desync
  cannot silently black-hole services.
- Label-space and SRGB documented and change-controlled; an SRGB
  change is a network-wide event, not a local edit.

## References and Knowledge Checks

- SPCOR MPLS and Segment Routing (20%); SPRI MPLS and Segment Routing
  (25%)
- Cisco IOS XR MPLS and Segment Routing configuration guides
- RFC 3031 (MPLS), RFC 8402 (Segment Routing architecture)

Knowledge checks:

1. Trace a packet's label operations ingress to egress, including
   PHP, and state what the core does and does not know.
2. What three problems does SR-MPLS remove versus LDP, and which IGP
   property made SR possible without a new protocol?
3. Ping to a PE's loopback works but its L3VPN is down. What
   transport condition does that point to, and how do you confirm it?
4. Why must the SRGB be consistent network-wide, and what breaks
   when it is not?

## Hands-On Lab

On the Chapter 02/03 core: first bring up **LDP** and prove label
switching to every loopback (LFIB + `traceroute mpls`), reading the
bindings — the incumbent baseline. Then migrate to **SR-MPLS**:
consistent SRGB, prefix-SIDs on loopbacks, `segment-routing mpls`
in IS-IS; verify prefix-SID labels are consistent everywhere and the
LSPs still prove end to end; then remove LDP and confirm services'
transport survives on SR alone. Break and diagnose: set an
inconsistent SRGB on one node (find the label inconsistency), and
remove a prefix-SID from one loopback (reproduce the ping-works-
service-fails split). Restore. Export — Chapters 05–08 build on this
SR transport.

## Lab Verification

Verification means both LDP and SR label paths were proven end to
end, the LDP-to-SR migration left transport intact, and both induced
faults were diagnosed by the IP-versus-label distinction. Until then,
the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MPLS lets the core forward on labels while ignorant of customer
routes; every service in this volume is a label stack on top of it.
LDP is the incumbent distribution; Segment Routing folds label
information into IS-IS and removes LDP, RSVP, and per-LSP core state —
the modern default — while SRv6 points at an IPv6-native future. This
chapter is a fifth of SPCOR and a quarter of SPRI, and the transport
Chapters 05–08 assume.

- [ ] I can trace a label stack including PHP and name core ignorance
- [ ] My SR-MPLS core has a consistent SRGB and prefix-SIDs
- [ ] I distinguished IP reachability from label reachability by test
- [ ] I migrated LDP→SR and retired LDP with transport intact
