# Volume XXVII Glossary

Definitions for terms introduced in **Volume XXVII — Cisco Data
Center**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**ACI (Application Centric Infrastructure)** — Cisco's
controller-based data center fabric: policy objects on the APIC
describe intent, and the fabric renders them, deny-by-default.
Introduced in Chapter 03.

**APIC (Application Policy Infrastructure Controller)** — The
clustered controller holding ACI policy and health; deliberately
outside the data plane, so forwarding survives its loss. Introduced
in Chapter 03.

**Anycast gateway** — The same gateway IP and MAC configured on every
leaf, so a workload's first hop is always local regardless of
placement or moves. Introduced in Chapter 02.

**Bridge domain (BD)** — ACI's Layer 2 flood boundary, holding
subnets and attached EPGs; related to but deliberately not a VLAN.
Introduced in Chapter 03.

**Collective operation** — A synchronized data exchange (all-reduce,
all-gather) among every GPU in a training job; the traffic pattern
that makes tail latency the controlling metric of AI fabrics.
Introduced in Chapter 07.

**Contract** — ACI's permission object between EPGs; without one,
inter-EPG traffic does not pass. Introduced in Chapter 03.

**CoPP (Control Plane Policing)** — Rate-limiting of traffic punted
to a switch supervisor, protecting the control plane from floods and
abuse. Introduced in Chapter 08.

**COOP (Council of Oracle Protocol)** — The spine-resident endpoint
database ACI uses instead of flood-and-learn; leaves report local
endpoints, and unknown traffic goes to the spine proxy. Introduced in
Chapter 03.

**DCBX (Data Center Bridging Exchange)** — The negotiation protocol
carrying PFC and ETS settings between peers, so both ends agree on
which traffic classes are lossless. Introduced in Chapter 05.

**DCQCN** — ECN-based congestion control for RoCEv2 fabrics: early
marking slows senders before PFC pause is needed. Introduced in
Chapter 07.

**ECMP (Equal-Cost Multipath)** — Routing across all equal-cost
fabric paths simultaneously; with spine-leaf, the property that keeps
every link forwarding. Introduced in Chapter 01.

**EPG (Endpoint Group)** — ACI's atom of policy: endpoints with
identical policy requirements, attached to a bridge domain.
Introduced in Chapter 03.

**EVPN (Ethernet VPN)** — The BGP address family serving as VXLAN's
control plane: Type-2 routes advertise hosts, Type-3 VTEP membership,
Type-5 IP prefixes. Introduced in Chapter 02.

**Fabric interconnect (FI)** — The paired switches at the head of a
UCS domain, carrying unified LAN and SAN traffic and hosting UCS
Manager. Introduced in Chapter 04.

**FLOGI (Fabric Login)** — An N_Port's login to the Fibre Channel
fabric, yielding its FCID; first rung of the FLOGI/PLOGI/PRLI ladder.
Introduced in Chapter 05.

**GIR (Graceful Insertion and Removal)** — NX-OS maintenance mode:
protocols withdraw gracefully so a node can be serviced without
traffic loss. Introduced in Chapter 09.

**Intersight** — Cisco's SaaS management plane for UCS and adjacent
infrastructure; API-first, with a Private Virtual Appliance for
data-locality-constrained estates. Introduced in Chapter 04.

**L3Out** — ACI's external routed connectivity object: border-leaf
peering plus an external EPG whose contracts admit outside traffic.
Introduced in Chapter 03.

**L3VNI** — The per-VRF VNI carrying routed traffic between leaves in
symmetric IRB. Introduced in Chapter 02.

**NDFC (Nexus Dashboard Fabric Controller)** — The controller for
NX-OS-mode fabrics: template-driven provisioning, configuration
compliance, imaging, and a REST API. Introduced in Chapter 06.

**NPIV / NPV** — N_Port ID Virtualization lets one physical port
carry many fabric logins; N_Port Virtualization mode lets an edge
switch forward logins upstream without consuming a domain ID.
Introduced in Chapter 05.

**NVMe over Fabrics** — Extending NVMe's queue model across FC
(FC-NVMe), TCP, or RDMA transports, removing SCSI translation from
the flash path. Introduced in Chapter 05.

**NX-API** — NX-OS's HTTPS API, in CLI-wrapping and REST-object
styles. Introduced in Chapter 06; enabled in Chapter 01.

**PFC (Priority Flow Control)** — Per-class Ethernet pause: the
no-drop class for FCoE and RoCEv2 while other classes drop normally.
Introduced in Chapter 05.

**RoCEv2** — RDMA over Converged Ethernet, routable over UDP/IP; the
standard transport of AI backend fabrics, dependent on PFC and ECN
for its loss intolerance. Introduced in Chapter 07.

**Rails (rail-aligned design)** — Backend fabric organization where
each GPU's NIC *n* connects to rail-*n* switching, matching
collective traffic patterns. Introduced in Chapter 07.

**Service profile** — UCS's portable server identity — MACs, WWNs,
UUID, boot, firmware, BIOS policy — rendered onto anonymous hardware.
Introduced in Chapter 04.

**Smart zoning** — MDS zoning that expands device-alias member roles
(initiator/target) into pairwise enforcement without manual
single-initiator zones. Introduced in Chapter 05.

**Spine-leaf (Clos)** — The two-tier fabric in which every leaf
connects to every spine and nothing else: uniform paths, horizontal
scale, all links forwarding. Introduced in Chapter 01.

**TEP pool** — The address pool from which ACI assigns tunnel
endpoints during fabric discovery. Introduced in Chapter 03.

**uSeg EPG** — A microsegmentation EPG whose membership follows
endpoint attributes (IP, MAC, VM name) rather than port attachment.
Introduced in Chapter 08.

**VMM domain** — ACI's integration with a virtual machine manager:
port groups per EPG, endpoint visibility, policy that follows VM
mobility. Introduced in Chapter 03.

**vPC (virtual Port Channel)** — Two Nexus switches presenting one
port channel downstream, with peer link, out-of-band keepalive, and
split-brain protections. Introduced in Chapter 02.

**VTEP** — A VXLAN tunnel endpoint, encapsulating and decapsulating
overlay frames; NVE interfaces on leaves, anycast VTEPs on vPC pairs.
Introduced in Chapter 02.

**VXLAN** — UDP-encapsulated Layer 2 over routed fabrics with a
24-bit VNI space; the data plane of both NX-OS EVPN fabrics and ACI.
Introduced in Chapter 02.

**X-Series** — UCS's current modular chassis, Intersight-first, with
independently upgradable compute, fabric, and storage modules.
Introduced in Chapter 04.
