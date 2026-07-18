# Volume II Glossary

Definitions for terms introduced in **Volume II — Network Engineering
Foundations**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Administrative Distance** — A per-protocol trustworthiness ranking (lower
is more preferred) a router uses to choose among routes to the same
destination learned from different sources, such as a static route versus
an OSPF-learned route. Introduced in Chapter 04.

**Authoritative Name Server** — A DNS server that holds the actual, source-
of-record data for a zone, as opposed to a recursive resolver that queries
on a client's behalf and caches the answer. Introduced in Chapter 05.

**Blameless Post-Incident Review** — A review of an incident's timeline and
contributing factors conducted with the explicit goal of improving systems
and process rather than evaluating individual performance. Introduced in
Chapter 09.

**BGP (Border Gateway Protocol)** — The path-vector routing protocol used
to exchange routes between autonomous systems, and the standard protocol
for a redundant, provider-independent enterprise WAN edge. Introduced in
Chapter 04; edge design use covered in Chapter 07.

**BSS (Basic Service Set) / ESS (Extended Service Set)** — A BSS is one
access point (identified by its BSSID) and its associated clients; an ESS
is a group of BSSs sharing one SSID, allowing a client to roam between
physical access points while remaining on one logical wireless network.
Introduced in Chapter 06.

**CAPWAP (Control and Provisioning of Wireless Access Points)** — The
protocol tunneling control traffic, and in centralized-forwarding
deployments client data traffic, between a lightweight access point and its
wireless LAN controller in a split-MAC architecture. Introduced in
Chapter 06.

**CIDR (Classless Inter-Domain Routing)** — The addressing scheme, defined
in RFC 4632, that replaced fixed Class A/B/C network boundaries with
arbitrary prefix lengths, enabling efficient allocation and route
summarization. Introduced in Chapter 02.

**Collapsed Core** — A network design that merges the distribution and core
tiers of the three-tier hierarchical model into one tier, appropriate for
smaller sites where a dedicated core is not justified. Introduced in
Chapter 07.

**DHCP (Dynamic Host Configuration Protocol)** — The protocol that
automates IPv4 address assignment and related configuration (gateway, DNS,
NTP, and other options) through a four-message DORA exchange. Introduced in
Chapter 05.

**DHCP Relay** — A function, typically on a VLAN's default-gateway router,
that forwards DHCP broadcasts from a local segment to a centrally located
DHCP server as a unicast, allowing one server to serve many subnets.
Introduced in Chapter 05.

**DNS (Domain Name System)** — The distributed, delegated system that
resolves hierarchical, human-readable names to IP addresses and other
resource data, defined in RFC 1035. Introduced in Chapter 05.

**DORA** — The four-message DHCP exchange — Discover, Offer, Request,
Acknowledge — through which a client obtains an IP address lease.
Introduced in Chapter 05.

**ECMP (Equal-Cost Multi-Path)** — A routing capability that installs and
actively uses multiple equal-cost next hops to the same destination
simultaneously, hashing flows across them rather than using only one path.
Introduced in Chapter 07.

**EIRP (Equivalent Isotropically Radiated Power)** — A wireless
transmitter's effective radiated power (transmit power plus antenna gain,
minus cable loss), often subject to regulatory limits. Introduced in
Chapter 06.

**Encapsulation** — The process of wrapping data with successive protocol
headers as it moves down the layered model toward the physical medium, with
each layer's Protocol Data Unit becoming the payload of the layer below it.
Introduced in Chapter 01.

**FHRP (First-Hop Redundancy Protocol)** — A protocol family (VRRP, HSRP,
GLBP) that presents a shared virtual IP and virtual MAC address backed by
two or more physical routers, so hosts have a single, stable default
gateway even if the router actively forwarding for it changes. Introduced
in Chapter 07.

**Five Whys** — A root cause analysis technique that repeatedly asks "why"
until the answer reaches a genuinely actionable, systemic cause rather than
stopping at the first proximate cause. Introduced in Chapter 09.

**Free Space Path Loss (FSPL)** — The attenuation a radio signal
experiences over distance in open space, which increases with both
distance and frequency — the physical reason higher-frequency Wi-Fi bands
(6 GHz) have shorter effective range than lower bands (2.4 GHz) at equal
transmit power. Introduced in Chapter 06.

**GLBP (Gateway Load Balancing Protocol)** — A Cisco-proprietary FHRP that
allows multiple group members to actively forward simultaneously, adding
load balancing on top of basic gateway redundancy. Introduced in
Chapter 07.

**HSRP (Hot Standby Router Protocol)** — A Cisco-proprietary FHRP in which
the highest-priority router becomes Active and others remain Standby,
conceptually similar to VRRP. Introduced in Chapter 07.

**IPFIX (IP Flow Information Export)** — The IETF-standardized,
template-based flow export protocol (RFC 7011) descended from NetFlow v9,
used to export summarized traffic flow records to a collector. Introduced
in Chapter 08.

**LACP (Link Aggregation Control Protocol)** — The IEEE 802.3ad standard
protocol for negotiating and maintaining a bundle of physical links as one
logical link between two switches. Introduced in Chapter 03.

**MAC Address Table** — A switch's per-port record of learned source MAC
addresses, used to make forwarding decisions instead of flooding every
frame out every port. Introduced in Chapter 03.

**NAT (Network Address Translation)** — A mechanism that rewrites IP
addresses as traffic crosses a translation boundary, most commonly between
private and public address space; a translation mechanism, not a security
boundary. Introduced in Chapter 02; expanded with PAT and DNAT in
Chapter 05.

**NetFlow** — Cisco-originated flow export technology; version 9
introduced the flexible, template-based record format that IPFIX later
standardized. Introduced in Chapter 08.

**Network Baseline** — A recorded profile of an environment's normal
behavior (utilization, route table size, flow volume) captured over a
representative period, without which a threshold-based alert has no valid
basis for distinguishing normal from anomalous. Introduced in Chapter 08.

**Network Change Lifecycle** — The network-specific application of change
management (request, risk classification, review, scheduled window,
pre/post-change validation, close or roll back) built on the change
management discipline established in Volume I. Introduced in Chapter 09.

**NTP (Network Time Protocol)** — The protocol, currently NTPv4 (RFC
5905), that synchronizes device clocks through a hierarchical stratum
model; accurate time underlies both security controls and reliable
multi-device log correlation. Introduced in Chapter 05.

**Observability** — The property of being able to understand a system's
internal state from external outputs, including states not anticipated in
advance, using richly correlatable telemetry — distinct from monitoring's
narrower, predefined threshold checks. Introduced in Chapter 08.

**OSI Reference Model** — The seven-layer conceptual model (Physical,
Data Link, Network, Transport, Session, Presentation, Application) used as
a shared vocabulary for describing network function and troubleshooting
order of operations. Introduced in Chapter 01.

**OSPF (Open Shortest Path First)** — A link-state Interior Gateway
Protocol that organizes routers into areas to bound the scope of
topology-change flooding and support summarization at area boundaries.
Introduced in Chapter 04.

**PAT (Port Address Translation / NAT Overload)** — A form of NAT in which
many private addresses share one public address, distinguished by
translated source port; the dominant mechanism for outbound internet
access from private address space. Introduced in Chapter 05.

**PMF (Protected Management Frames, 802.11w)** — A wireless standard that
cryptographically protects 802.11 management frames, preventing forged
deauthentication and disassociation frames used in common wireless denial-
of-service attacks. Introduced in Chapter 06.

**RADIUS (Remote Authentication Dial-In User Service)** — The
authentication, authorization, and accounting protocol (RFC 2865) used as
the authentication server in 802.1X-based wired and wireless enterprise
network access control. Introduced in Chapter 06.

**RCA (Root Cause Analysis)** — The discipline of identifying why an
incident occurred at a systemic level, distinct from the proximate fix that
restores service. Introduced in Chapter 09.

**Redistribution** — The controlled process of injecting routes learned by
one routing protocol into a different routing protocol's domain, requiring
explicit metric translation and filtering to avoid routing loops.
Introduced in Chapter 04.

**RFC 1918** — The IETF standard reserving three IPv4 ranges
(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) for private, non-globally-
routable use. Introduced in Chapter 02.

**Rollback Plan** — A specific, pre-written, tested set of steps to return
a network change to its pre-change state, prepared and reviewed as part of
the same change request rather than improvised after a failure. Introduced
in Chapter 09.

**Route Summarization** — Advertising one covering prefix in place of many
specific routes, which requires contiguous address allocation on
power-of-two boundaries and reduces routing table size and instability
blast radius. Introduced in Chapter 02.

**Runbook** — A pre-written, tested procedure for a specific, recurring
failure class, structured with trigger symptoms, prerequisites, numbered
diagnostic and resolution steps, and escalation criteria. Introduced in
Chapter 09.

**RSSI (Received Signal Strength Indicator)** — The signal power, in dBm,
that a wireless receiver measures from a given transmitter; a primary
input to coverage design, roaming decisions, and troubleshooting.
Introduced in Chapter 06.

**sFlow** — An independent, packet-sampled flow telemetry standard that
exports a statistical sample of packets plus interface counters, trading
exactness for lower device overhead compared to full flow accounting.
Introduced in Chapter 08.

**SLAAC (Stateless Address Autoconfiguration)** — An IPv6 mechanism, per
RFC 4862, by which a host derives its own address from a Router
Advertisement's prefix without a server assigning it, in contrast to
stateful DHCPv6. Introduced in Chapter 02; contrasted with DHCPv6 in
Chapter 05.

**SNMP (Simple Network Management Protocol)** — The long-standing polling-
based device management protocol, structured around MIBs and OIDs, with
SNMPv3's `authPriv` mode providing authenticated, encrypted polling in
place of SNMPv1/v2c's cleartext community strings. Introduced in
Chapter 08.

**Spanning Tree Protocol (STP)** — The Layer 2 protocol that prevents
bridging loops in a redundantly connected switched network by
algorithmically blocking redundant paths while preserving them for
failover. Introduced in Chapter 03.

**Spine-Leaf (Clos) Fabric** — A two-tier, fully meshed switching topology
in which every leaf switch connects to every spine switch, forwarding
traffic across all links simultaneously via ECMP rather than blocking
redundant paths as Spanning Tree does; the data-center-native alternative
to three-tier hierarchical design. Introduced conceptually in Chapter 03;
developed in Chapter 07.

**Split-Horizon (Split-Brain) DNS** — A DNS architecture serving different
answers for the same name depending on whether the query originates
inside or outside the enterprise network, implemented as separate internal
and external zones. Introduced in Chapter 05.

**Streaming Telemetry** — A push-based, model-driven telemetry pattern
(commonly transported via gNMI) in which a device continuously reports
state changes to a collector as they occur, in contrast to SNMP's
interval-based polling. Introduced in Chapter 08.

**Syslog** — The standard protocol (RFC 5424) for transporting log
messages, tagged with a facility and severity, from a device to a
centralized collector. Introduced in Chapter 08.

**TCP/IP (DoD) Model** — The four-layer model (Network Access, Internet,
Transport, Application) that actually governs how protocols are
implemented on the wire, collapsing the OSI model's top three layers into
one Application layer. Introduced in Chapter 01.

**Top-Down / Bottom-Up / Divide-and-Conquer Troubleshooting** — Three
strategies for choosing where in the layered stack to begin
troubleshooting, selected based on whether a symptom appears
application-specific, segment-wide, or ambiguous. Introduced in
Chapter 09.

**VLAN (Virtual LAN)** — A logical broadcast domain that segments a
physical switched network into multiple isolated Layer 2 domains, carried
across trunk links using 802.1Q tagging. Introduced in Chapter 03.

**VLSM (Variable Length Subnet Masking)** — The practice of allocating
subnet sizes matched to actual host requirements rather than a single
fixed mask, typically applied largest-block-first to preserve
summarizability. Introduced in Chapter 02.

**VRRP (Virtual Router Redundancy Protocol)** — The open, IETF-standard
(RFC 5798) First-Hop Redundancy Protocol in which the highest-priority
router in a group becomes Master and answers ARP for a shared virtual IP,
with a Backup router taking over on Master failure. Introduced in
Chapter 07.

**WPA3** — The current Wi-Fi Alliance security standard, replacing the
Pre-Shared Key of WPA2-Personal with SAE for forward secrecy and offline-
dictionary-attack resistance, and pairing with 802.1X/EAP for
WPA3-Enterprise. Introduced in Chapter 06.
