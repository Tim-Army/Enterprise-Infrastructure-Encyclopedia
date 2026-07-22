# Volume XXIX Glossary

Definitions for terms introduced in **Volume XXIX — Cisco Service
Provider**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Adjacency-SID** — A locally significant Segment Routing label for a
specific link, used to build explicit paths in SR-TE. Introduced in
Chapter 04.

**BFD (Bidirectional Forwarding Detection)** — A lightweight protocol
detecting link/path failure in milliseconds independent of routing-
protocol hellos, triggering precomputed protection. Introduced in
Chapter 05.

**CE (Customer Edge)** — The customer's router at the provider
boundary, often outside provider control; the PE-CE relationship is a
routing contract. Introduced in Chapter 01.

**DiffServ tunneling mode** — The relationship (uniform, pipe, or
short-pipe) between a customer's DSCP and the provider's MPLS EXP
marking, deciding whose markings govern core queuing and egress.
Introduced in Chapter 08.

**EVPN (Ethernet VPN)** — A BGP-based L2VPN control plane that learns
MAC/IP in the control plane and enables all-active multihoming;
route types 1–4 carry auto-discovery, MAC/IP, multicast, and Ethernet
segment information. Introduced in Chapter 07.

**H-QoS (Hierarchical QoS)** — Nested QoS policy where a parent shaper
enforces a customer's total sold rate and child policies queue per
class within it. Introduced in Chapter 08.

**IOS XR** — Cisco's service-provider operating system, with a
two-stage (candidate/commit) configuration model, process modularity,
and native model-driven interfaces. Introduced in Chapter 01.

**IS-IS** — The link-state IGP favored in provider cores: data-link
based, address-family agnostic, and TLV-extensible (the basis for
Segment Routing's IGP extensions). Introduced in Chapter 02.

**LDP (Label Distribution Protocol)** — The traditional MPLS label
distribution protocol, binding labels to IGP prefixes hop by hop;
superseded by Segment Routing in modern designs. Introduced in
Chapter 04.

**LPTS (Local Packet Transport Services)** — IOS XR's built-in
control-plane policing, protecting the route processor from
control-plane floods (the XR analog of CoPP). Introduced in Chapter 08.

**Model-driven telemetry (MDT)** — Streaming of structured, timestamped
operational state from devices on subscription (via gNMI), replacing
SNMP polling for assurance. Introduced in Chapter 09.

**mVPN** — Multicast VPN: delivering customer multicast across the
provider core, via Draft-Rosen (legacy) or modern BGP/MPLS profiles.
Introduced in Chapter 08.

**NSO (Network Services Orchestrator)** — Cisco's service orchestration
platform, modeling services as intent, rendering device configuration,
and detecting drift. Introduced in Chapter 09.

**P (Provider) router** — A core label-switching router that carries
no customer state and runs the IGP and label transport. Introduced in
Chapter 01.

**PE (Provider Edge) router** — The router where customers attach and
services (VRFs, pseudowires, QoS) are configured. Introduced in
Chapter 01.

**PHP (Penultimate Hop Popping)** — Stripping the transport label one
hop before the egress LSR so the egress performs a single service
lookup. Introduced in Chapter 04.

**Prefix-SID** — A globally significant Segment Routing label for a
loopback, advertised by the IGP so every router computes the label
path to it. Introduced in Chapter 04.

**Pseudowire** — A point-to-point emulated circuit carrying a
customer's Layer 2 frames across the MPLS core as a label stack.
Introduced in Chapter 07.

**RD (Route Distinguisher)** — A value prepended to a customer prefix
to make it globally unique in VPNv4/VPNv6 BGP; it does not control
import/export. Introduced in Chapter 06.

**Route reflector (RR)** — An iBGP speaker that re-advertises routes to
clients, replacing the iBGP full mesh; kept loop-free by ORIGINATOR_ID
and CLUSTER_LIST. Introduced in Chapter 03.

**RPL (Route Policy Language)** — IOS XR's structured routing-policy
language for matching and manipulating BGP attributes. Introduced in
Chapter 03.

**RT (Route Target)** — The extended community that controls which VRFs
import which VPN routes, expressing VPN topology. Introduced in
Chapter 06.

**Segment Routing (SR-MPLS)** — Source routing in which the ingress
encodes the path as a stack of SIDs carried by IGP extensions,
removing LDP/RSVP and per-LSP core state. Introduced in Chapter 04.

**SR-TE** — Segment-Routing Traffic Engineering: expressing an
engineered path as a segment list imposed at the headend, with no
per-path core state; policies keyed by (headend, color, endpoint).
Introduced in Chapter 05.

**SRGB (Segment Routing Global Block)** — The network-wide label range
reserved for prefix-SIDs; must be consistent across all nodes.
Introduced in Chapter 04.

**SRv6** — Segment Routing over IPv6, carrying the segment list in an
IPv6 extension header using IPv6 SIDs, with no MPLS label plane.
Introduced in Chapter 04.

**TI-LFA (Topology-Independent Loop-Free Alternate)** — SR-based fast
reroute that guarantees a loop-free backup along the post-convergence
path in any topology. Introduced in Chapter 05.

**VPLS (Virtual Private LAN Service)** — A multipoint L2VPN emulating a
shared LAN across the provider core. Introduced in Chapter 07.

**VPWS (Virtual Private Wire Service)** — A point-to-point L2VPN
(Ethernet line) delivered as a pseudowire. Introduced in Chapter 07.

**VRF (VPN Routing and Forwarding)** — A per-customer routing table and
interface set on a PE, isolating customers even with overlapping
address space. Introduced in Chapter 06.

**6VPE** — IPv6 L3VPN over an MPLS core using the VPNv6 address family,
reusing the L3VPN RD/RT/two-label machinery. Introduced in Chapter 06.
