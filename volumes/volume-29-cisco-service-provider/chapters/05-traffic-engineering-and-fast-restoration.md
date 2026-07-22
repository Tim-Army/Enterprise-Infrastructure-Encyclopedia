# Chapter 05: Traffic Engineering and Fast Restoration

## Learning Objectives

- Explain traffic engineering's purpose and compare RSVP-TE with
  SR-TE
- Configure SR-TE policies: explicit paths, dynamic paths with
  constraints, and steering
- Design sub-50-ms protection: LFA, remote LFA, and TI-LFA, and
  explain why TI-LFA guarantees a backup
- Deploy BFD for fast failure detection independent of protocol
  hellos
- Validate protection and TE behavior with failure testing and
  evidence

## Theory and Architecture

### Why engineer traffic at all

IGP shortest-path routing sends everything over the lowest-metric
path, which can congest one link while parallel capacity sits idle,
and cannot honor latency or affinity constraints a service demands.
**Traffic engineering** steers specific traffic along chosen paths —
for capacity, for latency, or to avoid particular links. SPCOR folds
TE into the MPLS/SR domain; the SP reality is that TE and fast
restoration are how SLAs get met.

### RSVP-TE versus SR-TE

**RSVP-TE** signals explicit LSPs and reserves bandwidth hop by hop —
powerful but stateful: every P router holds per-tunnel state, and the
control plane scales poorly with tunnel count. **SR-TE** expresses the
path as a **segment list** (a stack of prefix- and adjacency-SIDs from
Chapter 04) imposed at the headend; the core holds no per-path state
because the packet carries its own path. This is the same state-removal
win as SR transport, applied to engineering, and it is why new
deployments are SR-TE.

An **SR-TE policy** is defined by (headend, color, endpoint): *color*
encodes intent (low-latency, high-bandwidth), and BGP routes colored
to match are automatically steered onto the policy — **on-demand next
hop (ODN)** builds policies as colored routes appear. Paths are
**explicit** (an operator-specified segment list) or **dynamic**
(computed to optimize a metric — IGP, TE, or latency — subject to
constraints/affinities), optionally computed by a **PCE** (path
computation element) for network-wide optimization.

### Fast restoration: the sub-50-ms promise

SLAs demand restoration faster than IGP reconvergence, so the data
plane must have a precomputed backup ready before failure:

- **LFA (Loop-Free Alternate)** — a precomputed backup next-hop that
  is loop-free by inequality; simple but does not cover every
  topology (ring topologies notoriously).
- **Remote LFA (rLFA)** — extends coverage using a targeted LDP/label
  session to a distant loop-free release point.
- **TI-LFA (Topology-Independent LFA)** — uses SR's ability to encode
  an explicit backup path as a label stack, so it **guarantees a
  loop-free backup in any topology**, along the post-convergence path
  (so traffic does not thrash when the IGP later reconverges). TI-LFA
  is the SR-era answer and the one the exam expects as default.

**BFD** detects failures in milliseconds independent of protocol
hellos, triggering the precomputed switch — detection plus TI-LFA
together deliver the sub-50-ms behavior.

## Design Considerations

- **TI-LFA everywhere as the protection baseline**: with SR, per-prefix
  TI-LFA is a few lines and covers any topology — there is little
  reason to run bare LFA in a new design.
- **SR-TE by color/intent, not by hand-built tunnels**: model intents
  (latency, disjointness) as colors and let ODN instantiate policies;
  hand-crafted explicit paths are for exceptions.
- **BFD timers matched to platform and SLA**: aggressive timers detect
  faster but cost CPU and risk false positives on congested links —
  tune per platform capability.
- **Disjointness for protected services**: dual-plane or SRLG-aware
  path computation so a primary and its backup do not share a fate.

## Implementation and Automation

TI-LFA and BFD on the Chapter 04 SR core:

```text
router isis CORE
 interface GigabitEthernet0/0/0/0
  bfd minimum-interval 50
  bfd multiplier 3
  address-family ipv4 unicast
   fast-reroute per-prefix
   fast-reroute per-prefix ti-lfa      ! guaranteed backup, any topology
```

An SR-TE policy — explicit low-latency path, and dynamic with a
constraint:

```text
segment-routing
 traffic-eng
  policy LOW-LATENCY-PE2
   color 100 end-point ipv4 10.0.0.2
   candidate-paths
    preference 100
     explicit segment-list AVOID-CORE1
    preference 50
     dynamic
      metric type latency
  !
  segment-list AVOID-CORE1
   index 10 mpls adjacency 10.1.12.2   ! adjacency-SIDs building a path
   index 20 mpls label 16002           ! prefix-SID of PE2
```

```text
! Validation
show segment-routing traffic-eng policy
show mpls forwarding tunnels
show bfd session
show isis fast-reroute ipv4 detail        ! TI-LFA backup paths
```

## Validation and Troubleshooting

Protection is validated by **breaking things and measuring**: confirm
TI-LFA has installed a backup for the loopbacks (`show isis
fast-reroute detail`), start a continuous stream, fail the primary
link, and measure the loss window — sub-50-ms means the data plane
switched to the precomputed path before the control plane reconverged.
BFD's role shows as the trigger: with BFD, detection is milliseconds;
without, you wait for IGP hellos. SR-TE validation: the policy is up
and its segment list resolves (`show segment-routing traffic-eng
policy`), colored traffic actually takes it (trace the label stack),
and ODN instantiates policies as colored routes arrive. Faults:
TI-LFA "no backup" for a prefix usually means a genuinely
unprotectable topology or an SR/label gap (Chapter 04); an SR-TE
policy "down" traces to an unresolvable SID in the list (an
adjacency-SID for a failed link, a prefix-SID that is missing);
BFD flaps on a congested link argue for less aggressive timers or a
QoS fix (Chapter 08).

## Security and Best Practices

- Protection and TE are availability controls, and availability is
  security: a resilient core resists both faults and certain attacks.
- PCE and controller interfaces (Chapter 09) are privileged — they
  can steer traffic network-wide — so their access and authentication
  are held to the management-plane standard.
- Validate that backup paths honor the same policy/security boundaries
  as primaries; a backup that bypasses a scrubbing or inspection point
  is a hole.

## References and Knowledge Checks

- SPCOR MPLS and Segment Routing (20%, TE portion); SPRI MPLS/SR (25%)
- Cisco IOS XR SR-TE and fast-reroute configuration guides
- RFC 7490 (rLFA), RFC 8402 (SR), TI-LFA drafts/guides

Knowledge checks:

1. Contrast RSVP-TE and SR-TE by where per-path state lives, and why
   that drives new deployments to SR-TE.
2. Why does TI-LFA guarantee a loop-free backup where plain LFA
   cannot, and what SR capability makes that possible?
3. What are BFD and TI-LFA each responsible for in a sub-50-ms
   restoration, and what happens if you have one without the other?
4. An SR-TE policy is down. Name two segment-list conditions that
   cause it and how you would confirm each.

## Hands-On Lab

On the Chapter 04 SR core: enable BFD and per-prefix TI-LFA on all
core links; verify backups are installed for every loopback. Run a
continuous measured stream between CE stubs, fail the primary core
link, and **measure the loss window** — demonstrate sub-50-ms
restoration and contrast it with the window when BFD is disabled
(hello-timer detection). Build one SR-TE policy: an explicit
low-latency path steering PE1→PE2 traffic off the default path (prove
the label stack differs), plus a dynamic latency-optimized candidate
as fallback. Break the explicit path's link and show the policy fall
back. Diagnose one deliberately broken policy (an adjacency-SID for a
downed link). Restore and export.

## Lab Verification

Verification means TI-LFA restoration was measured under 50 ms and
contrasted with the BFD-off case, the SR-TE policy steered and fell
back with label-stack evidence, and the broken policy was diagnosed
to its unresolved SID. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Traffic engineering steers traffic for capacity and latency, and
SR-TE does it with no core state by carrying the path as a segment
list; fast restoration meets SLAs with precomputed backups, where
TI-LFA guarantees coverage in any topology and BFD triggers the
switch in milliseconds. Together they are how a provider keeps its
promises, and they complete SPCOR's and SPRI's MPLS/SR domains.

- [ ] I can contrast RSVP-TE and SR-TE by state location
- [ ] TI-LFA + BFD gave me measured sub-50-ms restoration
- [ ] My SR-TE policy steered by color and fell back on failure
- [ ] I diagnosed a down policy to its unresolved segment
