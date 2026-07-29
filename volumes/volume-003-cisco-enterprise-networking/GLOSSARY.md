# Volume III Glossary

Definitions for terms introduced in **Volume III — Cisco Enterprise
Networking**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**802.1X** — The IEEE port-based network access control standard, in
which a supplicant (endpoint), authenticator (switch port), and
authentication server (RADIUS) exchange EAP-over-LAN messages to
authenticate an endpoint before granting network access. Introduced in
Chapter 07.

**AAA (Authentication, Authorization, and Accounting)** — The framework
IOS XE uses to control device administration and network access,
typically implemented with TACACS+ for device administration and RADIUS
for network access. Introduced in Chapter 07.

**Anycast RP** — A multicast Rendezvous Point redundancy design in which
multiple routers share the same RP address, using MSDP or PIM to
synchronize active source state between them for load-sharing and
failover. Introduced in Chapter 06.

**Application-aware routing (AAR)** — Catalyst SD-WAN's continuous,
BFD-probe-driven measurement of loss, latency, and jitter per transport
tunnel, used to steer application traffic onto the tunnel currently
meeting a defined SLA class. Introduced in Chapter 04.

**Border Node** — The SD-Access fabric role that translates between the
fabric's VXLAN/SGT overlay and networks outside the fabric, serving as
the fabric site's exit point. Introduced in Chapter 09.

**Bundle mode** — An IOS XE software packaging mode that boots directly
from a consolidated `.bin` file without extracting individual packages;
simpler than install mode but does not support ISSU. Introduced in
Chapter 01.

**CAPWAP (Control and Provisioning of Wireless Access Points)** — The
protocol (RFC 5415) carrying the control and data tunnels between a
lightweight access point and its wireless controller in Cisco's
split-MAC architecture. Introduced in Chapter 05.

**Catalyst Center** — Cisco's centralized management, automation, and
Assurance controller for the Catalyst estate, providing device discovery
and inventory, underlay/fabric automation, and continuous telemetry
correlation. Introduced in Chapter 09.

**CleanAir** — A Cisco AP capability that classifies non-Wi-Fi RF
interference sources and feeds that data into RRM and Assurance.
Introduced in Chapter 05.

**Closed mode (802.1X)** — The 802.1X deployment mode in which a port
blocks all traffic except EAPoL/MAB exchanges until authentication
succeeds; the typical end state of a phased 802.1X rollout. Introduced in
Chapter 07.

**Control Plane Node** — The SD-Access fabric role running LISP to
maintain a host-tracking database mapping each endpoint to its current
fabric edge node. Introduced in Chapter 09.

**Diffusing Update Algorithm (DUAL)** — EIGRP's loop-free path
computation algorithm, which pre-computes feasible successor routes to
achieve fast convergence without a full topology recomputation.
Introduced in Chapter 03.

**Differentiated Services Code Point (DSCP)** — The 6-bit field in the IP
header used to mark a packet's QoS treatment; it survives Layer 3 hops
end to end, unlike the Layer-2-only CoS field. Introduced in Chapter 06.

**DMVPN (Dynamic Multipoint VPN)** — A Cisco overlay technology combining
multipoint GRE, NHRP, and IPsec to build an encrypted any-to-any or
hub-and-spoke overlay across commodity internet transport. Introduced in
Chapter 04.

**Downloadable ACL (dACL)** — A session-specific IP-based ACL that a
RADIUS/ISE authorization policy pushes to a single switch at
authentication time. Introduced in Chapter 07.

**Edge Node** — The SD-Access fabric role where endpoints physically
connect; performs VXLAN encapsulation/decapsulation and applies SGT-based
policy closest to the endpoint. Introduced in Chapter 09.

**Embedded Event Manager (EEM)** — A native IOS XE event-action engine
that triggers a defined action when a specified device-local event
occurs, such as a syslog pattern match or interface state change.
Introduced in Chapter 08.

**EtherChannel** — A logical interface bundling 2–8 physical links for
bandwidth aggregation and resiliency, most commonly negotiated with LACP
(IEEE 802.3ad). Introduced in Chapter 02.

**Fabric WLC** — A Catalyst 9800 controller integrated into an SD-Access
fabric site, whose access points act as fabric edge nodes carrying
wireless traffic in the same VXLAN overlay as wired traffic. Introduced
in Chapter 09.

**FlexConnect** — An access point mode that switches client traffic
locally at a branch site instead of tunneling it back to a central WLC,
keeping clients served during a WAN outage. Introduced in Chapter 05.

**gNMI** — A gRPC-based protocol unifying get/set/subscribe operations
against YANG-modeled device data in a single high-performance protocol,
commonly used for streaming telemetry. Introduced in Chapter 08.

**Guest Shell** — A Linux container running alongside IOSd on IOS XE,
providing an on-box Python environment and CLI-scripting API for local
automation tasks. Introduced in Chapter 08.

**HSRP (Hot Standby Router Protocol)** — Cisco's proprietary first-hop
redundancy protocol, in which one router is active and one is standby per
group, with multiple groups used to spread active-gateway load across
VLANs. Introduced in Chapter 02.

**Install mode** — The IOS XE software packaging mode that boots from an
extracted set of individual packages plus a `packages.conf` pointer file;
required for ISSU/ISSD and the operational standard on Catalyst 9000
switches. Introduced in Chapter 01.

**IOSd** — The traditional IOS control-plane binary, running as a
protected process under IOS XE's Linux kernel, enabling process-level
resiliency independent of other platform processes. Introduced in
Chapter 01.

**ISE (Identity Services Engine)** — Cisco's policy server for network
access control, combining Policy Administration (PAN), Policy Service
(PSN), and Monitoring and Troubleshooting (MnT) roles to evaluate
authentication and authorization requests. Introduced in Chapter 07.

**LISP (Locator/ID Separation Protocol)** — The control-plane protocol
used by SD-Access to separate an endpoint's identity (IP address) from
its location (the RLOC of its attached fabric edge node), enabling
mobility without routing reconvergence. Introduced in Chapter 09.

**Low Latency Queuing (LLQ)** — A strict-priority QoS queue, policed to
its configured rate, used for traffic such as voice that cannot tolerate
queuing delay. Introduced in Chapter 06.

**MAC Authentication Bypass (MAB)** — A fallback authentication method in
which a switch authenticates an endpoint's MAC address against RADIUS
when no 802.1X supplicant response arrives, used for devices that cannot
run 802.1X. Introduced in Chapter 07.

**Model-driven telemetry (MDT)** — A telemetry model in which a device
pushes YANG-modeled operational data to a collector as it changes,
instead of the collector polling the device on an interval. Introduced in
Chapter 08.

**Modular QoS CLI (MQC)** — The IOS XE three-part QoS configuration model
— `class-map` (classification), `policy-map` (per-class actions), and
`service-policy` (interface application). Introduced in Chapter 06.

**Multiple Spanning Tree (MST)** — An IEEE 802.1s spanning-tree variant
that maps many VLANs onto a small number of spanning-tree instances,
keeping control-plane overhead flat as VLAN count grows. Introduced in
Chapter 02.

**NBAR2 (Network-Based Application Recognition)** — Deep-packet-inspection-based
traffic classification that identifies applications by protocol behavior
rather than port number alone, feeding both QoS policy and visibility
tooling. Introduced in Chapter 06.

**NETCONF** — An XML-based configuration management protocol (RFC 6241)
offering transactional, validate-then-commit changes against a device's
candidate datastore. Introduced in Chapter 08.

**Open mode (802.1X)** — An 802.1X deployment mode in which a port stays
open by default while a pre-authentication ACL limits access, and full
policy applies once authentication succeeds; a staging step before closed
mode. Introduced in Chapter 07.

**OpenConfig** — A set of vendor-neutral YANG data models developed by a
multi-vendor working group, trading some platform-specific depth for
portability across a multi-vendor estate. Introduced in Chapter 08.

**OSPFv2** — A vendor-neutral, link-state interior gateway protocol (RFC
2328) that floods link-state advertisements within an area and computes
shortest paths with Dijkstra's algorithm. Introduced in Chapter 03.

**Overlay Management Protocol (OMP)** — Catalyst SD-WAN's BGP-like
control protocol, used by edge routers to exchange reachability
information and centralized policy with the SD-WAN Controller. Introduced
in Chapter 04.

**Path Trace** — A Catalyst Center Assurance tool that reports the actual
forwarding path between two endpoints, including per-hop QoS treatment
and ACL/SGACL enforcement encountered. Introduced in Chapter 09.

**PIM sparse mode (PIM-SM)** — The enterprise-standard IP multicast
routing protocol, in which routers join a shared tree rooted at a
Rendezvous Point only when a receiver requests a group. Introduced in
Chapter 06.

**Plug and Play (PnP)** — Cisco's zero-touch provisioning mechanism, in
which an unconfigured switch discovers a PnP server on first boot and
downloads its initial configuration and software image automatically.
Introduced in Chapter 08.

**Policy-Based Routing (PBR)** — A forwarding override that routes
traffic based on a route map matched against source/destination address,
protocol, or interface, instead of the default longest-prefix-match
decision. Introduced in Chapter 03.

**Radio Resource Management (RRM)** — The WLC function that continuously
tunes channel assignment (DCA), transmit power (TPC), and coverage hole
mitigation (CHDM) across joined access points. Introduced in Chapter 05.

**Rapid PVST+** — Cisco's default per-VLAN spanning-tree variant (IEEE
802.1w), converging in the sub-second range using a proposal/agreement
handshake. Introduced in Chapter 02.

**RESTCONF** — A stateless, REST-style protocol (RFC 8040) exposing
YANG-modeled device data over HTTPS using standard GET/PATCH/POST
semantics. Introduced in Chapter 08.

**Routed access** — A campus design that extends Layer 3 to the access
switch, replacing the access-to-distribution trunk with a routed uplink
to remove STP convergence time from that boundary. Introduced in
Chapter 01.

**Security Group ACL (SGACL)** — A TrustSec access-control entry keyed on
a source-SGT/destination-SGT pair rather than source/destination IP
address, enforced anywhere that tag pair appears in the network.
Introduced in Chapter 07.

**Security Group Tag (SGT)** — A TrustSec tag assigned to traffic at its
ingress point (via 802.1X/MAB authorization or static mapping), used for
identity-based micro-segmentation independent of IP address or VLAN.
Introduced in Chapter 07.

**SGT Exchange Protocol (SXP)** — A protocol that propagates
IP-address-to-SGT bindings over a TCP session to devices that cannot
inline-tag traffic in the Ethernet frame. Introduced in Chapter 07.

**Smart Licensing Using Policy (SLP)** — The current default Cisco
licensing model on IOS XE 17.x, reporting usage to Cisco Smart Software
Manager directly, via satellite/on-prem, or via offline synchronization.
Introduced in Chapter 01.

**StackWise Virtual (SVL)** — A logical-single-switch architecture
joining two physically separate chassis over a high-bandwidth SVL link
plus a dedicated Dual-Active Detection link. Introduced in Chapter 01.

**Transit (SD-Access)** — The connection type joining multiple SD-Access
fabric sites into a fabric domain: IP-based transit re-applies policy at
each site's border, while SD-Access transit extends the VXLAN/SGT overlay
between sites directly. Introduced in Chapter 09.

**Transport locator (TLOC)** — In Catalyst SD-WAN, the identifier
representing one transport circuit an edge router owns; OMP advertises
prefixes together with the TLOCs that can reach them. Introduced in
Chapter 04.

**TrustSec** — Cisco's architecture for identity-based micro-segmentation,
tagging traffic with Security Group Tags at ingress and enforcing policy
downstream via SGACLs, independent of IP addressing. Introduced in
Chapter 07.

**Trust boundary (QoS)** — The point in a network where a device either
trusts an incoming CoS/DSCP marking or re-classifies traffic from
scratch; it should sit as close to a verified traffic source as the
source can be trusted. Introduced in Chapter 06.

**VRF-lite (Virtual Routing and Forwarding)** — A technique for creating
multiple independent routing tables on one physical router or switch,
used as the single-device building block for macro-segmentation.
Introduced in Chapter 03.

**VTP (VLAN Trunking Protocol)** — A Cisco protocol for propagating VLAN
database changes across a domain; most current designs run it in
transparent mode or disable it in favor of automation-managed, per-switch
VLAN configuration. Introduced in Chapter 02.

**VXLAN (Virtual Extensible LAN)** — The data-plane encapsulation (RFC
7348) SD-Access uses to carry an endpoint's original frame, Virtual
Network (VNI), and SGT across the fabric's routed underlay. Introduced in
Chapter 09.

**Weighted Random Early Detection (WRED)** — A congestion-avoidance
mechanism that drops packets probabilistically as a queue approaches
capacity, favoring lower-priority traffic first to avoid synchronized TCP
back-off. Introduced in Chapter 06.

**Wireless management interface** — The Catalyst 9800 controller
interface that terminates CAPWAP tunnels from joined access points.
Introduced in Chapter 05.

**WPA3** — The current Wi-Fi Alliance security standard, using
Simultaneous Authentication of Equals (SAE) for personal networks and
required outright (with Protected Management Frames) on the 6 GHz band.
Introduced in Chapter 05.

**YANG** — A data modeling language (RFC 7950) defining the structure,
types, and constraints of configuration and operational data as a
hierarchical tree, underlying NETCONF, RESTCONF, and gNMI. Introduced in
Chapter 08.
