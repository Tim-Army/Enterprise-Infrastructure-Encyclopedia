# Chapter 04: Enterprise WAN, Internet Edge, and Catalyst SD-WAN

![Lab topology for this chapter: HUB-01 runs a multipoint GRE Tunnel0 (NHRP network-id 100) over IPsec, with SPOKE-01 (tunnel 172.16.0.11) and SPOKE-02 (tunnel 172.16.0.12) registered as NHRP peers and EIGRP neighbors; traffic between the spokes is initially hub-relayed, then NHRP shortcut resolves a dynamic spoke-to-spoke tunnel directly between them. Separately, HUB-01's internet edge uses IP SLA-tracked dual paths (ISP-A primary, ISP-B floating static). As a negative test, shutting down the ISP-A transport interface transitions the tracked object to Down and the floating static route through ISP-B becomes the active default route.](../../../diagrams/volume-03-cisco-enterprise-networking/chapter-04-dmvpn-phase3-hub-spoke-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: a DMVPN Phase 3 hub-and-spoke overlay with dynamic spoke-to-spoke tunneling and a dual-ISP, IP SLA-tracked internet edge on the hub.*

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
- **NAT/PAT** to translate internal [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) addressing to public address
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
- [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271) (BGP-4), used at MPLS L3VPN and internet-edge boundaries
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

This chapter carries a topic-level walkthrough lab for the WAN, transport,
and SD-WAN exam topics that map here — **ENARSI Domain 2 (VPN
Technologies)**, **ENCOR SD-WAN/virtualization**, and **all of ENSDWI
(300-415)** — mapped in the volume README's coverage tables. "Describe"
topics use a read-only inspection (IOS XE SD-WAN CLI or a vManage API query);
"Configure" topics build and verify. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.30** — Catalyst 8000v/CSR IOS XE
SD-WAN edges, a vManage/SD-WAN Manager controller reachable at `$VMANAGE`
with a session cookie/token in `$VT`, and classic-IOS routers for the
MPLS/DMVPN labs. **Cost:** none beyond lab resources; each lab removes its
config.

### Lab 4.1 — Describe MPLS operations (ENARSI 2.1)

**Objective:** Read the label forwarding information base on an LSR.

```text
PE1# show mpls forwarding-table
PE1# show mpls ldp neighbor
```

**Expected result:** local/outgoing label bindings and an LDP neighbor in
`Oper` state — the LSR is label-switching packets along an LSP.

**Negative test:** an interface without `mpls ip` has no label bindings and
falls back to IP forwarding — MPLS must be enabled per link.

**Cleanup:** none (read-only).

### Lab 4.2 — Describe MPLS Layer 3 VPN (ENARSI 2.2)

**Objective:** Read a customer VRF and its VPNv4 routes on a PE.

```text
PE1# show ip route vrf CUST-A
PE1# show bgp vpnv4 unicast all
```

**Expected result:** per-customer routes in VRF `CUST-A` carried as VPNv4
with route targets — customer isolation across a shared MPLS core.

**Negative test:** mismatched import/export route targets; the remote PE's
routes never appear in the VRF — RTs control the VPN topology.

**Cleanup:** none (read-only).

### Lab 4.3 — Configure and verify DMVPN single hub (ENARSI 2.3, ENCOR 2.2)

**Objective:** Build a Phase 3 DMVPN hub with mGRE and NHRP.

```text
HUB(config)# interface tunnel0
HUB(config-if)# ip nhrp network-id 1
HUB(config-if)# ip nhrp redirect
HUB(config-if)# tunnel mode gre multipoint
HUB(config-if)# tunnel protection ipsec profile DMVPN
HUB# show dmvpn
```

**Expected result:** spokes registered to the hub via NHRP; `show dmvpn`
lists dynamic spoke mappings.

**Negative test:** omit `ip nhrp redirect`/`shortcut`; spoke-to-spoke stays
hairpinned through the hub (Phase 1 behavior) — Phase 3 needs the redirect.

**Cleanup:** `no interface tunnel0` on the hub and spokes.

### Lab 4.4 — Describe Cisco SD-WAN architecture and components (ENSDWI 1.1)

**Objective:** Read the four SD-WAN planes from the controller.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/system/device/controllers" | jq -r '.data[] | "\(.["device-type"])\t\(.["system-ip"])\t\(.reachability)"'
```

**Expected result:** vManage (management), vSmart (control), vBond
(orchestration), and WAN Edge (data) devices — the SD-WAN plane separation.

**Negative test:** treating vManage as the control plane; vSmart (not
vManage) distributes OMP routes and policy — the planes are distinct.

**Cleanup:** none (read-only).

### Lab 4.5 — Describe SD-WAN Edge platforms and capabilities (ENSDWI 1.2)

**Objective:** List the WAN Edge devices and their models.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device" | jq -r '.data[] | select(.["device-type"]=="vedge") | "\(.["device-model"])\t\(.version)"' | sort -u
```

**Expected result:** the edge platforms (Catalyst 8000v, ISR/ASR) and
software versions — the data-plane hardware the fabric runs on.

**Negative test:** expecting a controller-mode-only feature on an
autonomous-mode router; the device mode determines its SD-WAN capabilities.

**Cleanup:** none (read-only).

### Lab 4.6 — Describe SD-WAN Cloud OnRamp (ENSDWI 1.3)

**Objective:** Read any configured Cloud OnRamp for SaaS/multicloud.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/template/cloudx/manage/apps" | jq -r '.data[]?.appType' 2>/dev/null | head
```

**Expected result:** the Cloud OnRamp application list (SaaS optimization) —
the feature that steers cloud/SaaS traffic on best-quality paths.

**Negative test:** without Cloud OnRamp, SaaS traffic follows the default
route regardless of path quality; OnRamp is what adds per-app path choice.

**Cleanup:** none (read-only).

### Lab 4.7 — Describe controller cloud deployment (ENSDWI 2.1)

**Objective:** Confirm the controllers' hosting and certificates.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/system/device/controllers" | jq -r '.data[] | "\(.["device-type"])\t\(.["cert-install-status"])"'
```

**Expected result:** controllers with `Installed` certificate status —
cloud-hosted controllers reachable and trusted.

**Negative test:** a controller with an uninstalled/expired certificate
cannot form control connections; the whole overlay depends on the PKI.

**Cleanup:** none (read-only).

### Lab 4.8 — Describe controller on-premises deployment (ENSDWI 2.2)

**Objective:** Read control-connection state to on-prem controllers.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device/control/connections?deviceId=<edge-ip>" | jq -r '.data[] | "\(.["peer-type"])\t\(.state)"'
```

**Expected result:** control connections to vSmart/vBond in `up` state —
an edge fully onboarded whether controllers are cloud or on-prem.

**Negative test:** an on-prem controller behind NAT without the correct
vBond mapping never completes control connections — orchestration must
resolve the public reachability.

**Cleanup:** none (read-only).

### Lab 4.9 — Configure certificates and device lists (ENSDWI 2.3)

**Objective:** Confirm the valid/staging device list state.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/certificate/vedge/list" | jq -r '.data[] | "\(.["chasisNumber"])\t\(.validity)"' | head
```

**Expected result:** WAN Edges marked `valid` in the device list — the trust
allowlist that lets a device join the overlay.

**Negative test:** an edge left in `staging`/`invalid` cannot form data-plane
tunnels; the device list is the admission control.

**Cleanup:** none (read-only).

### Lab 4.10 — Troubleshoot control plane connectivity (ENSDWI 2.4)

**Objective:** Diagnose why an edge has no control connections.

```text
Edge# show sdwan control connections
Edge# show sdwan control connection-history
```

**Expected result:** connection state per controller; the history reveals the
failure reason (e.g. `DCONFAIL`, `VB_TMO`, certificate error).

**Negative test:** blaming the data plane when `connection-history` shows a
control-plane certificate/DTLS failure — control comes first.

**Cleanup:** none (read-only).

### Lab 4.11 — Describe WAN Edge deployment (ENSDWI 3.1)

**Objective:** Read an edge's onboarding/config-sync state.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device/system/status?deviceId=<edge-ip>" | jq -r '.data[0] | "\(.vdevice_name)\t\(.["config-operation"])"' 2>/dev/null
```

**Expected result:** the edge in sync with its intended config — deployed
via ZTP/PnP and managed by vManage.

**Negative test:** an out-of-sync edge (local CLI changes) drifts from the
template; vManage flags it and can revert — controller-managed config wins.

**Cleanup:** none (read-only).

### Lab 4.12 — Configure the SD-WAN data plane (ENSDWI 3.2)

**Objective:** Verify IPsec data-plane (BFD) tunnels between edges.

```text
Edge# show sdwan bfd sessions
Edge# show sdwan ipsec outbound-connections
```

**Expected result:** BFD sessions `up` between TLOCs — the encrypted
data-plane overlay carrying site-to-site traffic.

**Negative test:** a firewall blocking the negotiated IPsec/UDP ports drops
the data plane while control stays up — check both planes separately.

**Cleanup:** none (read-only).

### Lab 4.13 — Configure OMP (ENSDWI 3.3)

**Objective:** Read Overlay Management Protocol routes and TLOCs.

```text
Edge# show sdwan omp routes
Edge# show sdwan omp tlocs
```

**Expected result:** OMP routes (prefixes) and TLOCs (transport locators)
advertised via vSmart — the SD-WAN control-plane routing.

**Negative test:** an OMP route with no matching TLOC is unusable; the prefix
and its transport locator must both be present.

**Cleanup:** none (read-only).

### Lab 4.14 — Configure TLOCs (ENSDWI 3.4)

**Objective:** Read the transport-locator colors on an edge.

```text
Edge# show sdwan control local-properties | include color|tloc
```

**Expected result:** each WAN transport with its `color` (mpls, biz-internet,
public-internet) — the TLOC attributes policy steers on.

**Negative test:** two transports sharing a color break restrict/preference
logic; colors must be assigned deliberately per transport.

**Cleanup:** none (read-only).

### Lab 4.15 — Configure feature templates (ENSDWI 3.6, 3.7)

**Objective:** List vManage feature templates / configuration groups.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/template/feature" | jq -r '.data[] | "\(.templateName)\t\(.templateType)"' | head
```

**Expected result:** the feature templates (and, in newer releases,
configuration groups and feature profiles) that build device configs —
config as reusable, versioned objects.

**Negative test:** editing an attached template pushes to every device using
it; scope changes with a device-specific template to avoid a fleet-wide
change.

**Cleanup:** none (read-only).

### Lab 4.16 — Configure control policies (ENSDWI 4.1)

**Objective:** Read the centralized control policy applied at vSmart.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/template/policy/vsmart" | jq -r '.data[] | .policyName' 2>/dev/null | head
```

**Expected result:** control policies that shape OMP route/TLOC advertisement
(topology: hub-spoke, mesh) — vSmart enforces them centrally.

**Negative test:** a control policy not applied to a vSmart list has no
effect; it must be activated and referenced by site list.

**Cleanup:** none (read-only).

### Lab 4.17 — Configure data policies (ENSDWI 4.2)

**Objective:** Read data policies that act on the data plane.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/template/policy/definition/data" | jq -r '.data[] | .name' 2>/dev/null | head
```

**Expected result:** data policies (traffic steering, service chaining) that
apply at the edge to matched flows — distinct from control policy.

**Negative test:** a data policy applied in the wrong direction (from-service
vs from-tunnel) matches nothing; direction is part of the match.

**Cleanup:** none (read-only).

### Lab 4.18 — Configure end-to-end segmentation (ENSDWI 4.3)

**Objective:** Read the VPN segments carried across the fabric.

```text
Edge# show sdwan omp routes | include VPN
Edge# show ip vrf
```

**Expected result:** multiple service VPNs (VRFs) mapped to OMP — end-to-end
segmentation without per-hop VRF config in the underlay.

**Negative test:** two segments sharing a VPN ID leak between tenants; the
VPN ID is the isolation boundary across the overlay.

**Cleanup:** none (read-only).

### Lab 4.19 — Configure application-aware routing (ENSDWI 4.4)

**Objective:** Read the AAR policy and SLA class results.

```text
Edge# show sdwan app-route sla-class
Edge# show sdwan app-route stats
```

**Expected result:** SLA classes (loss/latency/jitter) and per-tunnel
measured stats — traffic is steered to the tunnel meeting the app's SLA.

**Negative test:** an SLA class no tunnel can meet leaves traffic on the
backup/last-resort path; the SLA must be achievable on some transport.

**Cleanup:** none (read-only).

### Lab 4.20 — Configure direct Internet access (ENSDWI 4.5)

**Objective:** Confirm a DIA NAT path at the branch.

```text
Edge# show sdwan policy from-vsmart
Edge# show ip nat translations
```

**Expected result:** branch internet traffic NATed locally to the transport
instead of backhauled — DIA offloads the hub.

**Negative test:** DIA without a local security policy exposes the branch;
DIA must pair with edge security (Lab 4.22).

**Cleanup:** none (read-only).

### Lab 4.21 — Configure service insertion (ENSDWI 5.1)

**Objective:** Read advertised network services for service chaining.

```text
Edge# show sdwan omp services
```

**Expected result:** services (firewall, IDP) advertised into OMP so control
policy can chain traffic through them — service insertion across the fabric.

**Negative test:** a service advertised from a down node drops chained
traffic; service tracking must remove it on failure.

**Cleanup:** none (read-only).

### Lab 4.22 — Describe SD-WAN security features (ENSDWI 5.2)

**Objective:** Read the edge security policy (enterprise firewall, IPS).

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/template/policy/definition/zonebasedfw" | jq -r '.data[]?.name' 2>/dev/null | head
```

**Expected result:** zone-based firewall / security policies bound to edges —
on-box security for DIA and east-west traffic.

**Negative test:** relying on the hub firewall for DIA traffic that never
reaches the hub; DIA needs edge security.

**Cleanup:** none (read-only).

### Lab 4.23 — Describe cloud security integration (ENSDWI 5.3)

**Objective:** Read any SIG (Secure Internet Gateway) tunnels.

```text
Edge# show sdwan secure-internet-gateway tunnels
```

**Expected result:** automatic SIG tunnels to a cloud security provider
(Umbrella/third-party) — cloud-delivered security for branch internet
traffic.

**Negative test:** DIA without a SIG or on-box security sends branch traffic
to the internet uninspected; integrate one of them.

**Cleanup:** none (read-only).

### Lab 4.24 — Configure QoS on WAN Edge (ENSDWI 5.4)

**Objective:** Read the localized QoS policy on the edge.

```text
Edge# show sdwan policy access-list-counters
Edge# show policy-map interface GigabitEthernet1
```

**Expected result:** class queues with match/drop counters on the WAN
interface — QoS applied at the SD-WAN edge.

**Negative test:** a QoS map with no shaper on a sub-line-rate circuit lets
bulk traffic starve voice; shape to the circuit rate first.

**Cleanup:** none (read-only).

### Lab 4.25 — Describe Application Quality of Experience (ENSDWI 5.5)

**Objective:** Read AppQoE (TCP optimization/DRE) status.

```text
Edge# show sdwan appqoe status
```

**Expected result:** AppQoE services (TCP optimization, DRE) active on the
edge — improving perceived application performance over the WAN.

**Negative test:** enabling AppQoE without the required resource profile
fails to activate; the platform must have the capacity.

**Cleanup:** none (read-only).

### Lab 4.26 — Describe authentication, monitoring, and reporting (ENSDWI 6.1)

**Objective:** Read vManage users and roles.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/admin/user" | jq -r '.data[] | "\(.userName)\t\(.group|join(","))"' | head
```

**Expected result:** vManage users mapped to role groups (netadmin,
operator) — RBAC on the management plane.

**Negative test:** an operator-role user cannot push templates; role scope
limits management actions.

**Cleanup:** none (read-only).

### Lab 4.27 — Configure authentication, monitoring, and reporting (ENSDWI 6.2)

**Objective:** Confirm vManage's external AAA (RADIUS/TACACS) setting.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/admin/vmanage" | jq -r '.data | keys[]' 2>/dev/null | grep -i auth
```

**Expected result:** the configured external authentication server for
vManage logins — centralized admin auth for the controller.

**Negative test:** external AAA with no local fallback locks admins out when
the server is unreachable; keep a local netadmin.

**Cleanup:** none (read-only).

### Lab 4.28 — Describe REST API monitoring (ENSDWI 6.3)

**Objective:** Query device statistics through the vManage REST API.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device/counters?deviceId=<edge-ip>" | jq -r '.data[0] | {omp:.ompPeers, bfd:.bfdSessions}' 2>/dev/null
```

**Expected result:** OMP peer and BFD session counts via REST — the API that
automation and monitoring dashboards consume.

**Negative test:** polling the API without a valid session token returns
`403`; the token/cookie is the auth boundary.

**Cleanup:** none (read-only).

### Lab 4.29 — Describe software image management (ENSDWI 6.4)

**Objective:** Read the software images in the vManage repository.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device/action/software" | jq -r '.data[]?.versionName' 2>/dev/null | head
```

**Expected result:** the image repository vManage uses to upgrade edges
fleet-wide — centralized, staged software management.

**Negative test:** upgrading all edges at once risks a fleet outage on a bad
image; stage to a canary site first.

**Cleanup:** none (read-only).

### Lab 4.30 — DMVPN Phase 3 overlay with tracked failover (integrative)

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

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

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
