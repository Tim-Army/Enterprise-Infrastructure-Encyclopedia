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

This chapter carries a topic-level walkthrough lab for **the MPLS and Segment
Routing objectives of SPCOR 350-501 v1.1 (Domain 3) and Domain 4 of SPRI 300-510
v1.1** — mapped in the volume README's coverage tables. Labs use the IOS XR CLI.
Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.5** — an IOS XR core with an IGP,
label-switching enabled (LDP and/or Segment Routing), and SRv6 support on the
platform for the SRv6 lab. **Cost:** none beyond lab resources.

### Lab 4.1 — Implement MPLS (SPCOR Objective 3.1)

**Objective:** Verify label distribution and an LSP end to end.

```text
show mpls interfaces
show mpls ldp neighbor brief
show mpls forwarding
```

**Expected result:** LDP neighbors up and label bindings in the forwarding table —
MPLS builds LSPs by distributing labels (LDP, or SR without a separate protocol);
`show mpls forwarding` shows the local→outgoing label swap that switches packets.

**Negative test:** an interface carrying IGP but not enabled for MPLS/LDP breaks
the LSP; `show mpls interfaces` omits it — every core link on the path must be
label-enabled.

**Cleanup:** none (read-only).

### Lab 4.2 — Describe segment routing (SPCOR Objective 3.3)

**Objective:** Read the SR prefix/adjacency SIDs distributed by the IGP.

```text
show isis segment-routing label table
show segment-routing local-block
show mpls forwarding labels <prefix-SID>
```

**Expected result:** prefix-SIDs (global, from the SRGB) and adjacency-SIDs
(local) — Segment Routing sources the path in the packet as a label stack, so no
LDP/RSVP state is held in the core; the IGP advertises SIDs and each node label-
switches by SID.

**Negative test:** mismatched SRGB ranges between nodes cause label confusion; SR
requires a consistent global block — the local-block/SRGB must align network-wide.

**Cleanup:** none (read-only).

### Lab 4.3 — Troubleshoot MPLS (SPRI Objective 4.1)

**Objective:** Diagnose a broken LSP / label path.

```text
show mpls forwarding prefix <prefix>
traceroute mpls ipv4 <prefix>/32
show mpls ldp bindings <prefix> 2>/dev/null
```

**Expected result:** the label path and where it breaks — an MPLS forwarding
failure shows as a missing label binding (LDP not converged), an IGP/label
mismatch, or a broken LSP mid-path; `traceroute mpls` (LSP ping/traceroute)
localizes the hop.

**Negative test:** blame the egress PE for a VPN outage that is really a core LSP
break — the PE-PE LSP must be intact for any label VPN service to work.

**Cleanup:** none (read-only).

### Lab 4.4 — Implement segment routing (SPRI Objective 4.2)

**Objective:** Enable SR-MPLS on the IGP and verify SID assignment.

```text
show isis segment-routing label table
show route ipv4 <loopback> detail | include "SR|label"
show cef <loopback>
```

**Expected result:** the prefix-SID assigned to each loopback and installed in
CEF — implementing SR means enabling `segment-routing mpls` under the IGP,
assigning prefix-SIDs to loopbacks, and confirming label-switched reachability
without LDP.

**Negative test:** enable SR on some nodes but not all; SR/LDP interworking (a
mapping server or ti-lfa) is needed across the boundary — a partial SR domain
without interworking breaks label continuity.

**Cleanup:** none (read-only).

### Lab 4.5 — Implement Segment Routing v6 / SRv6 (SPRI Objective 4.4)

**Objective:** Verify SRv6 locators and SIDs on an IPv6 data plane.

```text
show segment-routing srv6 locator
show segment-routing srv6 sid
show route ipv6 <locator>
```

**Expected result:** the SRv6 locator and its SIDs (End, End.X, End.DT4/DT6) —
SRv6 encodes segments as IPv6 addresses (locators + function), so the IPv6 data
plane itself carries source routing and service functions, no MPLS labels needed.

**Negative test:** expect SRv6 forwarding on a platform without SRv6 data-plane
support; the SIDs do not install in hardware — SRv6 needs platform/ASIC support,
unlike SR-MPLS on legacy label hardware.

**Cleanup:** none (read-only).

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
