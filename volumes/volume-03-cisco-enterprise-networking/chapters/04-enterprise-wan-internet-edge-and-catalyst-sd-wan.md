# Chapter 04: Enterprise WAN, Internet Edge, and Catalyst SD-WAN

## Learning Objectives

- Compare traditional MPLS L3VPN, DMVPN, and Catalyst SD-WAN transport
  models for enterprise site connectivity.
- Configure a DMVPN hub-and-spoke overlay with IPsec protection.
- Describe the Catalyst SD-WAN control-plane and data-plane architecture
  (Manager, Controller, Validator, and cEdge devices) and its OMP control
  protocol.
- Design an internet edge with dual-ISP redundancy and appropriate NAT and
  routing policy.
- Explain application-aware routing and its relationship to traditional
  path-control mechanisms from [Chapter 3](03-cisco-enterprise-routing-and-path-control.md).

## Theory and Architecture

### WAN transport models

Enterprises reach branch and remote sites over one or more of the
following transport models, often in combination:

- **MPLS L3VPN** — a service-provider-operated Layer 3 VPN where the
  provider distributes customer routes between sites using MP-BGP; the
  customer's WAN edge router peers with the provider PE router (usually via
  eBGP) but does not participate in the provider's own MPLS core. MPLS
  L3VPN offers provider-managed any-to-any reachability and SLA-backed
  transport but at a materially higher cost per megabit than internet
  transport, and with less flexibility to add or resize sites quickly.
- **DMVPN (Dynamic Multipoint VPN)** — a Cisco overlay technology combining
  multipoint GRE (mGRE), Next Hop Resolution Protocol (NHRP), and IPsec to
  build an any-to-any or hub-and-spoke encrypted overlay across
  commodity internet transport. DMVPN remains a common, well-understood
  choice for organizations that need encrypted site-to-site connectivity
  without moving to a full SD-WAN controller-based operating model.
- **Catalyst SD-WAN** — Cisco's controller-managed SD-WAN fabric (formerly
  known by the Viptela product name) that separates control plane,
  management plane, orchestration plane, and data plane into distinct
  components, applies centralized, intent-based policy, and actively
  steers application traffic across multiple simultaneous transports
  (MPLS, broadband internet, LTE/5G) based on real-time path quality.

These models are not mutually exclusive: a common migration pattern keeps
MPLS as one transport member while adding internet-based DMVPN or Catalyst
SD-WAN transport as a second, cost-effective path, then uses
application-aware routing (Catalyst SD-WAN) or PBR/IP SLA tracking
([Chapter 3](03-cisco-enterprise-routing-and-path-control.md)) to prefer the right transport per application.

### DMVPN architecture

DMVPN Phase 3 (the current standard design) uses:

- **mGRE** on the hub, allowing one tunnel interface to terminate GRE
  encapsulation from many spokes without a dedicated point-to-point tunnel
  per spoke.
- **NHRP** so spokes register their real (NBMA) address with the hub and,
  in Phase 3, so the hub can redirect spokes to build direct
  spoke-to-spoke tunnels on demand instead of always hairpinning through
  the hub.
- **IPsec** (typically via a GRE-over-IPsec profile) to encrypt the overlay
  across untrusted internet transport.
- A **routing protocol** (commonly EIGRP or OSPF, per [Chapter 3](03-cisco-enterprise-routing-and-path-control.md)) running
  over the mGRE tunnel interface to distribute reachability between hub and
  spokes.

### Internet edge design

The internet edge is the enterprise's boundary with the public internet and
typically combines:

- **Dual-ISP peering** for transport redundancy, using either BGP
  ([Chapter 3](03-cisco-enterprise-routing-and-path-control.md)) for granular multihoming or a simpler floating-static/IP
  SLA–tracked design for smaller sites that don't need full-table policy.
- **NAT/PAT** to translate internal RFC 1918 addressing to public address
  space for outbound sessions, and static/destination NAT for any
  internet-facing services.
- **Perimeter security** (firewalling, intrusion prevention) — covered in
  architectural depth in [Volume X](../../volume-10-enterprise-cybersecurity/README.md) and [Volume XVI](../../volume-16-palo-alto-networks-security/README.md); this volume treats the
  Cisco IOS XE router/switch configuration of routing, NAT, and interface
  policy at the edge, not the firewall policy itself.

### Catalyst SD-WAN architecture

Catalyst SD-WAN divides the fabric into four logical planes, each mapped to
a distinct component:

| Plane | Component | Function |
| --- | --- | --- |
| Orchestration | Catalyst SD-WAN Validator (vBond) | Authenticates and onboards devices, brokers initial control-plane connections |
| Management | Catalyst SD-WAN Manager (vManage) | Centralized GUI/API for configuration, monitoring, and policy |
| Control | Catalyst SD-WAN Controller (vSmart) | Distributes OMP routes and centralized data-plane/control-plane policy to edge routers |
| Data | Catalyst SD-WAN Edge — cEdge (Catalyst 8000V/8200/8300 series running IOS XE SD-WAN) or vEdge (legacy Viptela hardware) | Terminates transport circuits, builds IPsec tunnels between sites, enforces policy, and forwards traffic |

Edge routers establish a permanent, authenticated control connection (DTLS
or TLS) to the Controller through the Validator's brokering, then exchange
reachability information using **Overlay Management Protocol (OMP)** — a
BGP-like protocol purpose-built for the SD-WAN control plane. Each transport
circuit an edge router owns is represented as a **TLOC (transport
locator)**; OMP advertises prefixes together with the TLOC(s) that can reach
them, and the Controller applies centralized policy before redistributing
routes to other edges, giving Catalyst SD-WAN the same "hub decides who
learns what" control model that BGP route reflectors provide in a
traditional network, but purpose-built for multi-transport path selection.

**Application-aware routing (AAR)** continuously measures loss, latency,
and jitter on each IPsec tunnel between sites (via periodic BFD probes) and
steers traffic per application (identified via NBAR2-based deep packet
inspection or explicit ACL match) onto the tunnel that currently meets a
defined SLA class — a controller-driven, continuously adaptive analog to
the static IP SLA–tracked PBR built in [Chapter 3](03-cisco-enterprise-routing-and-path-control.md).

## Design Considerations

- **Transport strategy** — choose MPLS-only when regulatory/SLA
  requirements mandate provider-guaranteed transport and cost is
  secondary; choose DMVPN when encrypted overlay connectivity over
  commodity internet is sufficient and a controller-based operating model
  isn't justified by the estate's size or churn; choose Catalyst SD-WAN
  when the organization has enough sites, enough transport diversity per
  site, or enough application-SLA sensitivity that centralized, adaptive
  policy pays for the added architecture and licensing.
- **Migration path** — because Catalyst SD-WAN cEdge devices run IOS XE,
  they can coexist with a traditional IOS XE WAN edge during a phased
  migration; plan a coexistence window rather than a hard cutover for any
  site of consequence.
- **Redundancy** — size the internet edge for the failure of any single
  ISP, any single edge router, and any single physical path (diverse
  carrier entry, not just diverse circuits from the same conduit).
- **NAT scope** — decide early whether NAT is applied per-site (traditional
  edge) or centrally (SD-WAN hub-breakout for internet-bound branch
  traffic); centralizing breakout simplifies security policy at the cost of
  extra backhaul latency for branch internet traffic.
- **Application SLA classes** — define a small number of SLA classes (for
  example, real-time voice/video, business-critical transactional, best
  effort) rather than a per-application policy for every single
  application; this keeps AAR policy auditable and keeps the number of
  measured tunnel-quality dimensions manageable.
- **Licensing and controller placement** — Catalyst SD-WAN controllers can
  be cloud-hosted (Cisco-managed) or on-premises; factor controller
  availability and DTLS/TLS reachability into the design the same way you
  would for any other critical control-plane dependency.

## Implementation and Automation

### DMVPN Phase 3 hub configuration

```text
HUB-01(config)# crypto ikev2 proposal DMVPN-PROP
HUB-01(config-ikev2-proposal)# encryption aes-cbc-256
HUB-01(config-ikev2-proposal)# integrity sha256
HUB-01(config-ikev2-proposal)# group 19
HUB-01(config-ikev2-proposal)# exit
HUB-01(config)# crypto ikev2 policy DMVPN-POLICY
HUB-01(config-ikev2-policy)# proposal DMVPN-PROP
HUB-01(config-ikev2-policy)# exit
HUB-01(config)# crypto ikev2 keyring DMVPN-KEYRING
HUB-01(config-ikev2-keyring)# peer ANY
HUB-01(config-ikev2-keyring-peer)# address 0.0.0.0 0.0.0.0
HUB-01(config-ikev2-keyring-peer)# pre-shared-key <PSK>
HUB-01(config-ikev2-keyring-peer)# exit
HUB-01(config)# crypto ikev2 profile DMVPN-IKEV2-PROFILE
HUB-01(config-ikev2-profile)# match identity remote address 0.0.0.0
HUB-01(config-ikev2-profile)# authentication local pre-share
HUB-01(config-ikev2-profile)# authentication remote pre-share
HUB-01(config-ikev2-profile)# keyring local DMVPN-KEYRING
HUB-01(config-ikev2-profile)# exit
HUB-01(config)# crypto ipsec transform-set DMVPN-TS esp-aes 256 esp-sha256-hmac
HUB-01(config)# mode transport
HUB-01(cfg-crypto-trans)# exit
HUB-01(config)# crypto ipsec profile DMVPN-IPSEC-PROFILE
HUB-01(ipsec-profile)# set transform-set DMVPN-TS
HUB-01(ipsec-profile)# set ikev2-profile DMVPN-IKEV2-PROFILE
HUB-01(ipsec-profile)# exit
HUB-01(config)# interface Tunnel0
HUB-01(config-if)# ip address 172.16.0.1 255.255.255.0
HUB-01(config-if)# ip mtu 1400
HUB-01(config-if)# ip nhrp network-id 100
HUB-01(config-if)# ip nhrp map multicast dynamic
HUB-01(config-if)# tunnel source GigabitEthernet0/0/0
HUB-01(config-if)# tunnel mode gre multipoint
HUB-01(config-if)# tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
HUB-01(config-if)# no shutdown
HUB-01(config-if)# exit
HUB-01(config)# router eigrp CAMPUS
HUB-01(config-router)# address-family ipv4 unicast autonomous-system 100
HUB-01(config-router-af)# network 172.16.0.0 0.0.0.255
HUB-01(config-router-af)# af-interface Tunnel0
HUB-01(config-router-af-interface)# no split-horizon
HUB-01(config-router-af-interface)# exit-af-interface
HUB-01(config-router-af)# exit-address-family
```

### DMVPN spoke configuration

```text
SPOKE-01(config)# interface Tunnel0
SPOKE-01(config-if)# ip address 172.16.0.11 255.255.255.0
SPOKE-01(config-if)# ip mtu 1400
SPOKE-01(config-if)# ip nhrp network-id 100
SPOKE-01(config-if)# ip nhrp nhs 172.16.0.1 nbma <HUB_PUBLIC_IP> multicast
SPOKE-01(config-if)# ip nhrp shortcut
SPOKE-01(config-if)# tunnel source GigabitEthernet0/0/0
SPOKE-01(config-if)# tunnel mode gre multipoint
SPOKE-01(config-if)# tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
SPOKE-01(config-if)# no shutdown
```

`ip nhrp shortcut` on the spoke is what enables Phase 3's dynamic
spoke-to-spoke tunnel building once the hub sends an NHRP redirect.

### Internet edge with dual-ISP NAT

```text
EDGE-01(config)# interface GigabitEthernet0/0/0
EDGE-01(config-if)# description ISP-A
EDGE-01(config-if)# ip address 203.0.113.2 255.255.255.252
EDGE-01(config-if)# ip nat outside
EDGE-01(config-if)# exit
EDGE-01(config)# interface GigabitEthernet0/0/1
EDGE-01(config-if)# description Inside
EDGE-01(config-if)# ip nat inside
EDGE-01(config-if)# exit
EDGE-01(config)# ip access-list standard NAT-INSIDE
EDGE-01(config-std-nacl)# permit 10.0.0.0 0.255.255.255
EDGE-01(config-std-nacl)# exit
EDGE-01(config)# ip nat inside source list NAT-INSIDE interface GigabitEthernet0/0/0 overload
EDGE-01(config)# ip sla 1
EDGE-01(config-ip-sla)# icmp-echo 203.0.113.1
EDGE-01(config-ip-sla-echo)# frequency 5
EDGE-01(config-ip-sla-echo)# exit
EDGE-01(config)# ip sla schedule 1 life forever start-time now
EDGE-01(config)# track 1 ip sla 1 reachability
EDGE-01(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1 track 1
EDGE-01(config)# ip route 0.0.0.0 0.0.0.0 198.51.100.1 210
```

The floating static route to the ISP-B next hop (administrative distance
210) only becomes active if the tracked ISP-A default route is withdrawn.

### Catalyst SD-WAN cEdge device-level bring-up

Full Catalyst SD-WAN policy authoring happens centrally in SD-WAN Manager,
but the device-side onboarding still uses IOS XE CLI concepts for the
system/SD-WAN process:

```text
cEdge-01(config)# system
cEdge-01(config-system)# system-ip 10.255.255.11
cEdge-01(config-system)# site-id 110
cEdge-01(config-system)# organization-name ENTERPRISE-ORG
cEdge-01(config-system)# vbond vbond.example.internal
cEdge-01(config-system)# exit
cEdge-01(config)# interface Tunnel1
cEdge-01(config-if)# ip unnumbered GigabitEthernet0/0/0
cEdge-01(config-if)# tunnel source GigabitEthernet0/0/0
cEdge-01(config-if)# tunnel mode sdwan
cEdge-01(config-if)# exit
cEdge-01(config)# sdwan
cEdge-01(config-sdwan)# interface GigabitEthernet0/0/0
cEdge-01(config-interface-GigabitEthernet0/0/0)# tunnel-interface
cEdge-01(config-tunnel-interface)# encapsulation ipsec
cEdge-01(config-tunnel-interface)# color biz-internet
cEdge-01(config-tunnel-interface)# allow-service all
cEdge-01(config-tunnel-interface)# exit
```

After this bootstrap, the device authenticates to the Validator, receives
its full configuration and policy from the Controller/Manager, and further
day-to-day policy changes are made centrally rather than per-device.

## Validation and Troubleshooting

```text
HUB-01# show dmvpn detail
HUB-01# show crypto ikev2 sa
HUB-01# show crypto ipsec sa
HUB-01# show ip nhrp
EDGE-01# show ip nat translations
EDGE-01# show track 1
EDGE-01# show ip route 0.0.0.0
cEdge-01# show sdwan control connections
cEdge-01# show sdwan bfd sessions
cEdge-01# show sdwan omp routes
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| DMVPN spoke never registers with hub | NHRP NHS address wrong, or IKEv2/IPsec failing before NHRP can run | `show dmvpn detail`, `show crypto ikev2 sa`; confirm PSK and tunnel source reachability |
| Spoke-to-spoke tunnel never builds (Phase 3) | Missing `ip nhrp shortcut`/`ip nhrp redirect` on spoke/hub, or ACL blocking direct spoke-to-spoke path | `show ip nhrp`, confirm NHRP redirect received and shortcut route installed |
| NAT not translating expected traffic | ACL in `ip nat inside source list` does not match the real inside subnet, or interface roles reversed | `show ip nat translations`, `show ip nat statistics`, confirm `ip nat inside`/`outside` placement |
| Floating static route to ISP-B never activates during ISP-A outage | Track object bound to the wrong route, or IP SLA target unreachable independent of ISP-A health | `show track 1`, confirm the IP SLA target is not itself downstream of the failure |
| cEdge control connection stuck `connecting` | Validator/Controller unreachable, certificate/organization-name mismatch, or NAT/firewall blocking DTLS | `show sdwan control connections`, `show sdwan control connections-history` |
| BFD session down between two SD-WAN sites | Underlying transport path down, or color/restrict policy preventing tunnel formation | `show sdwan bfd sessions`, confirm both sites' TLOC colors are compatible per policy |

## Security and Best Practices

- Always run DMVPN and equivalent GRE-based overlays with IPsec protection
  (`tunnel protection ipsec profile`); an unprotected GRE tunnel across the
  internet carries enterprise traffic in cleartext.
- Use IKEv2 with strong proposals (AES-256, SHA-256 or better, DH group 19
  or higher) and avoid legacy IKEv1 and weak DH groups on any new build.
- At the internet edge, apply anti-spoofing (uRPF) and explicit inbound
  ACLs on internet-facing interfaces; never expose a router's management
  plane (SSH, HTTP(S), SNMP) directly on an internet-facing interface —
  restrict management access to the out-of-band or VPN-reachable path
  established in [Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md).
- Rotate DMVPN pre-shared keys on a defined schedule, and prefer
  certificate-based IKEv2 authentication over PSK for larger deployments
  where key rotation at scale is operationally difficult.
- In Catalyst SD-WAN, restrict which transport colors are allowed to form
  tunnels to which other colors (for example, preventing a public-internet
  color from directly meshing with an MPLS-only private color) using
  centralized control policy, and enforce role-based access control in SD-WAN
  Manager so device template changes require appropriate approval.
- Keep WAN edge and cEdge software aligned with the Cisco IOS XE and
  Catalyst SD-WAN compatibility matrix; SD-WAN control/data plane
  components (Manager, Controller, Validator, edges) have interdependent
  minimum-version requirements that must be validated before any
  individual component upgrade.

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Dynamic Multipoint VPN (DMVPN) Design Guide*.
- Cisco, *Catalyst SD-WAN Design Guide* and *Catalyst SD-WAN Configuration
  Guide*, current release.
- RFC 4271 (BGP-4), used at MPLS L3VPN and internet-edge boundaries
  ([Chapter 3](03-cisco-enterprise-routing-and-path-control.md)).
- Cisco, *Catalyst 8000V Edge Software* and Catalyst 8200/8300 Series data
  sheets.

**Knowledge checks**

1. What are the three architectural building blocks of DMVPN, and what
   role does each play?
2. Why does DMVPN Phase 3 require `ip nhrp shortcut` on the spoke in
   addition to the standard NHS registration?
3. Name the four Catalyst SD-WAN planes and the component that implements
   each.
4. What is a TLOC, and how does it relate to OMP route advertisement?
5. Why is a floating static route with IP SLA tracking a reasonable
   internet-edge failover design for a small site that doesn't justify
   full BGP multihoming?

## Hands-On Lab

**Objective:** Build a DMVPN Phase 3 hub-and-spoke overlay with two spokes,
verify dynamic spoke-to-spoke tunnel formation, and add IP SLA–tracked
dual-path failover on the hub's internet edge.

**Prerequisites**

- Three IOS XE routers (or CML nodes) with crypto support: `HUB-01`,
  `SPOKE-01`, `SPOKE-02`, each with a routable (lab-simulated public)
  transport interface.
- Basic IP addressing across the simulated transport network and a
  loopback on each spoke representing a LAN subnet to advertise over
  DMVPN.

**Procedure**

1. Configure IKEv2 proposal, policy, keyring, profile, and the IPsec
   profile identically on all three routers, as shown in Implementation.

2. Configure the hub's `Tunnel0` as mGRE with NHRP network-id 100 and
   apply the IPsec profile; configure each spoke's `Tunnel0` pointing at
   the hub as NHS, with `ip nhrp shortcut` enabled.

3. Bring up EIGRP (or OSPF, per [Chapter 3](03-cisco-enterprise-routing-and-path-control.md)) over the tunnel interface on
   hub and both spokes, advertising each spoke's loopback LAN subnet.

4. Verify NHRP registration and routing convergence:

   ```text
   HUB-01# show dmvpn detail
   HUB-01# show ip eigrp neighbors
   ```

   **Expected result:** both spokes show as registered NHRP peers in
   `show dmvpn detail`, and both appear as EIGRP neighbors.

5. From `SPOKE-01`, generate traffic toward `SPOKE-02`'s loopback subnet
   (for example, a sustained ping), then check for a dynamic
   spoke-to-spoke tunnel:

   ```text
   SPOKE-01# ping 172.16.0.12 source 172.16.0.11 repeat 20
   SPOKE-01# show ip nhrp
   SPOKE-01# show dmvpn detail
   ```

   **Expected result:** after the initial hub-relayed packets, `show ip
   nhrp` shows a dynamic (shortcut) entry for `SPOKE-02`'s tunnel address,
   confirming Phase 3 spoke-to-spoke tunnel formation.

6. On `HUB-01`, configure the dual-path internet-edge NAT and IP
   SLA–tracked default route pair from Implementation, using a second,
   lab-simulated ISP path.

7. **Negative test:** administratively shut down the primary (ISP-A)
   transport interface on `HUB-01` and confirm failover:

   ```text
   HUB-01(config)# interface GigabitEthernet0/0/0
   HUB-01(config-if)# shutdown
   HUB-01# show track 1
   HUB-01# show ip route 0.0.0.0
   ```

   **Expected result:** the tracked object transitions to `Down`, the
   primary default route is withdrawn, and the floating static route
   through ISP-B becomes the active default route in the routing table.

8. Restore the primary interface and confirm the preferred route returns:

   ```text
   HUB-01(config)# interface GigabitEthernet0/0/0
   HUB-01(config-if)# no shutdown
   HUB-01# show ip route 0.0.0.0
   ```

**Cleanup**

- Remove the crypto, tunnel, NHRP, and routing configuration from all
  three routers if the lab devices are shared.
- Remove the NAT, IP SLA, tracking object, and floating static route
  configuration from `HUB-01`.
- Confirm no lingering IPsec security associations remain:

  ```text
  HUB-01# clear crypto ikev2 sa
  HUB-01# clear crypto ipsec sa
  ```

## Summary and Completion Checklist

Modern enterprise WAN design blends traditional provider-managed MPLS,
self-managed encrypted DMVPN overlays, and controller-driven Catalyst
SD-WAN, often within the same organization during a multi-year migration.
Regardless of which transport model a given site uses, the underlying
building blocks — encrypted tunnels, redundant paths with health-tracked
failover, and policy that steers traffic to the right path — are the same
concepts introduced in [Chapter 3](03-cisco-enterprise-routing-and-path-control.md) and extended here to multi-site and
multi-transport scale.

- [ ] Can compare MPLS L3VPN, DMVPN, and Catalyst SD-WAN and justify a
      transport choice for a given scenario.
- [ ] Can configure a DMVPN Phase 3 hub-and-spoke overlay with IPsec
      protection.
- [ ] Can explain the Catalyst SD-WAN four-plane architecture and OMP/TLOC
      concepts.
- [ ] Can configure a dual-ISP internet edge with NAT and IP SLA–tracked
      failover.
- [ ] Completed the hands-on lab, including verifying dynamic
      spoke-to-spoke tunnel formation and the failover negative test.
