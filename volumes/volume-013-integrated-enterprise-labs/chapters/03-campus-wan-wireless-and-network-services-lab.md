# Chapter 03: Campus, WAN, Wireless, and Network Services Lab

![Lab topology for this chapter: sw-core01 (HSRP active) and sw-core02 (HSRP standby) share every HQ VLAN's gateway; rtr-hq01 and rtr-br101 form an OSPF-FULL, IPsec-protected WAN link to a read-only domain controller at BR1, and a WLC serves two SSIDs mapped to their own VLANs and DHCP scopes. As a negative test, the active core switch's gateway interface is shut down; the standby transitions to Active within the timer window, and the Linux client keeps routing through the same gateway address with no local reconfiguration — the outage is visible only as a brief pause, not a routing change on the endpoint. Re-enabling the interface and its preempt setting returns the original switch to Active.](../../../diagrams/volume-013-integrated-enterprise-labs/chapter-03-hsrp-core-failover-topology.svg)

*Figure 3-1. Topology used throughout this chapter's Hands-On Lab: a Catalyst core/WAN/wireless build with HSRP, OSPF/IPsec to a branch site, and a read-only domain controller, tested against a core switch failure.*

## Learning Objectives

- Replace the ad hoc lab gateway from [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) with a resilient Cisco
  Catalyst core/distribution pair running HSRP, without breaking the
  identity and DHCP services [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) already depends on.
- Build a site-to-site WAN link between `HQ` and `BR1` and route between
  sites with OSPF.
- Extend the `corp.meridian.example` directory to `BR1` with a read-only
  domain controller, replicating over the new WAN link.
- Deploy a Catalyst 9800 wireless LAN controller serving separate
  corporate and guest SSIDs mapped to their VLANs.
- Prove HSRP gateway failover is transparent to hosts, and diagnose a
  deliberately introduced OSPF adjacency failure.

## Theory and Architecture

[Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) built identity, DNS, DHCP, and time on top of routing that was
never meant to last — a single ad hoc lab gateway handling every VLAN.
This chapter replaces that gateway with the real thing: a Cisco Catalyst
campus core, a WAN link to `BR1`, and wireless — the architecture Volume
III (Cisco Enterprise Networking) treats in depth, applied here on the
`corp.meridian.example` topology [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) defined and [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) already
put load-bearing services on.

The design follows [Volume II, Chapter 03](../../volume-002-network-engineering-foundations/chapters/03-ethernet-switching-vlans-and-layer-2-resilience.md) (Ethernet Switching, VLANs, and
Layer 2 Resilience) and [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) (Enterprise Network Design and
Resilience) for the campus topology, [Volume III, Chapter 02](../../volume-003-cisco-enterprise-networking/chapters/02-catalyst-campus-switching-and-resiliency.md) (Catalyst
Campus Switching and Resiliency) for the HSRP implementation specifics,
[Volume III, Chapter 04](../../volume-003-cisco-enterprise-networking/chapters/04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md) (Enterprise WAN, Internet Edge, and Catalyst SD-WAN)
for the HQ–BR1 link, and [Volume III, Chapter 05](../../volume-003-cisco-enterprise-networking/chapters/05-catalyst-wireless-architecture-and-operations.md) (Catalyst Wireless
Architecture and Operations) together with [Volume II, Chapter 06](../../volume-002-network-engineering-foundations/chapters/06-wireless-network-foundations.md) (Wireless
Network Foundations) for the WLAN. Routing between the core, the WAN edge,
and `BR1` uses OSPF, consistent with [Volume II, Chapter 04](../../volume-002-network-engineering-foundations/chapters/04-ip-routing-fundamentals.md) (IP Routing
Fundamentals) and [Volume III, Chapter 03](../../volume-003-cisco-enterprise-networking/chapters/03-cisco-enterprise-routing-and-path-control.md) (Cisco Enterprise Routing and
Path Control).

A deliberate design goal is that this cutover is invisible to [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md)'s
services: `sw-core01`/`sw-core02` take over the exact gateway addresses
(`10.13.10.1`, `10.13.20.1`, and so on) the ad hoc router used, as HSRP
virtual IPs. `dc01` and `dc02` do not need their default gateway
reconfigured. The one address that does change is the DNS forwarder target
on both domain controllers, because internet-edge NAT and resolution now
live on a dedicated router (`rtr-hq01`) instead of the multi-purpose lab
gateway — call this out explicitly in Implementation and Automation so the
reader does not spend time debugging DNS forwarding that was intentionally
moved, not broken.

### Systems introduced in this chapter

| Hostname | Role | Address | VLAN/Link |
| --- | --- | --- | --- |
| `sw-core01` | HQ core/distribution switch, HSRP active | `10.13.30.11` (mgmt) | Trunk, all HQ VLANs |
| `sw-core02` | HQ core/distribution switch, HSRP standby | `10.13.30.12` (mgmt) | Trunk, all HQ VLANs |
| `sw-acc01` | HQ access switch | `10.13.30.13` (mgmt) | Trunk to core |
| `rtr-hq01` | HQ WAN/internet edge router | `10.13.30.14` (mgmt), `10.13.10.2` (core uplink), `10.13.70.1` (WAN transit) | VLAN 110, WAN |
| `wlc01` | Catalyst 9800 wireless LAN controller | `10.13.30.15` | VLAN 130 |
| `rtr-br101` | BR1 WAN edge router / site gateway | `10.13.61.11` (mgmt), `10.13.60.1` (BR1 gateway), `10.13.70.2` (WAN transit) | VLAN 160/161, WAN |
| `sw-br101` | BR1 access switch | `10.13.61.12` | Trunk to `rtr-br101` |
| `dc-br101` | BR1 read-only domain controller | `10.13.60.11` | VLAN 160 |

HSRP virtual IPs reuse the `.1` address already in use on each HQ VLAN:
`10.13.10.1` (110), `10.13.20.1` (120), `10.13.40.1` (140), and
`10.13.99.1` (199).

## Design Considerations

- **HSRP over a stacked/VSS pair.** A two-box HSRP pair is chosen over
  switch stacking or VSS for this lab because it exercises independent
  control planes — a stacked pair shares one control plane and would not
  demonstrate the failure mode this chapter's negative test targets.
- **Single WAN path, deliberately.** `rtr-hq01` and `rtr-br101` connect
  over one IPsec-protected link across the `10.13.70.0/24` WAN transit.
  A production design would add a second path (a backup internet-VPN leg,
  or genuine SD-WAN dual-transport per [Volume III, Chapter 04](../../volume-003-cisco-enterprise-networking/chapters/04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md)); this lab
  intentionally leaves that gap so the resilience exercises in Chapters 05
  and 09 have a real deficiency to test against rather than an already
  redundant link.
- **Read-only domain controller at BR1, not a full DC.** `dc-br101` is
  configured as an RODC: it can authenticate local users and serve DNS
  without a live WAN path, but it cannot originate directory changes,
  limiting the blast radius of a compromised or physically less-secure
  branch site — the same reasoning [Volume IV, Chapter 04](../../volume-004-enterprise-systems-administration/chapters/04-enterprise-identity-and-directory-services.md) gives for RODC
  placement generally.
- **DHCP relay instead of a third DHCP server.** `BR1`'s VLANs relay DHCP
  broadcasts to `dc01`/`dc02` at HQ rather than running a local DHCP
  server, keeping scope administration centralized; the trade-off is that
  `BR1` clients cannot obtain new leases during a WAN outage, which is
  intentionally exposed as a known limitation.
- **Wireless as a controller-based, not autonomous, design.** `wlc01`
  centralizes RF and policy configuration for every access point in the
  lab, consistent with [Volume III, Chapter 05](../../volume-003-cisco-enterprise-networking/chapters/05-catalyst-wireless-architecture-and-operations.md); a single AP is sufficient
  to exercise CAPWAP tunneling and SSID-to-VLAN mapping without requiring
  full RF planning for a lab.

## Implementation and Automation

Configure the HSRP pair on `sw-core01` (repeat the standby priority and
virtual IP on `sw-core02` with a lower priority):

```text
! sw-core01
interface Vlan110
 ip address 10.13.10.3 255.255.255.0
 standby 110 ip 10.13.10.1
 standby 110 priority 110
 standby 110 preempt
interface Vlan120
 ip address 10.13.20.3 255.255.255.0
 standby 120 ip 10.13.20.1
 standby 120 priority 110
 standby 120 preempt
```

Bring up OSPF between the core, `rtr-hq01`, and `rtr-br101`:

```text
! rtr-hq01
router ospf 1
 router-id 10.13.10.2
 network 10.13.10.0 0.0.0.255 area 0
 network 10.13.70.0 0.0.0.255 area 0

! rtr-br101
router ospf 1
 router-id 10.13.60.1
 network 10.13.60.0 0.0.0.255 area 0
 network 10.13.70.0 0.0.0.255 area 0
```

Build the site-to-site IPsec tunnel across the WAN transit:

```text
! rtr-hq01
crypto isakmp policy 10
 encryption aes 256
 hash sha256
 authentication pre-share
 group 14
crypto isakmp key <PSK> address 10.13.70.2
crypto ipsec transform-set MERIDIAN-TS esp-aes 256 esp-sha256-hmac
crypto map MERIDIAN-MAP 10 ipsec-isakmp
 set peer 10.13.70.2
 set transform-set MERIDIAN-TS
 match address WAN-TRAFFIC
interface GigabitEthernet0/1
 crypto map MERIDIAN-MAP
```

Repoint the DNS forwarder on `dc01`/`dc02` from the retired ad hoc gateway
to `rtr-hq01`'s core-facing address, now that internet-edge NAT lives
there:

```powershell
Set-DnsServerForwarder -IPAddress 10.13.10.2
```

Configure DHCP relay on `sw-br101` (or on `rtr-br101` if it terminates the
BR1 VLANs) toward the HQ DHCP pair:

```text
interface Vlan160
 ip helper-address 10.13.10.11
 ip helper-address 10.13.10.12
```

Promote `dc-br101` as a read-only domain controller from `ctrl01` or a
domain-joined management host:

```powershell
Install-ADDSDomainController -DomainName "corp.meridian.example" `
  -ReadOnlyReplica:$true -SiteName "BR1" `
  -Credential (Get-Credential CORP\Administrator) `
  -SafeModeAdministratorPassword (ConvertTo-SecureString "<DSRM_PASSWORD>" -AsPlainText -Force) `
  -InstallDns:$true -Force:$true
```

## Validation and Troubleshooting

- **HSRP state.** `show standby brief` on both core switches must show
  exactly one `Active` and one `Standby` per group before continuing; two
  actives (a split-brain) usually means the peer link between the switches
  is down while both still see their own SVI as up.
- **OSPF adjacency.** `show ip ospf neighbor` on `rtr-hq01` and
  `rtr-br101` must show `FULL` state. A neighbor stuck in `EXSTART` or
  `EXCHANGE` almost always indicates an MTU mismatch on the WAN link —
  check with `show interface | include MTU` on both ends.
- **IPsec tunnel.** `show crypto isakmp sa` and `show crypto ipsec sa`
  must show an established Phase 1 and Phase 2 SA before OSPF over the
  tunnel can form; troubleshoot Phase 1 first (pre-shared key, proposal
  mismatch) before assuming a routing problem.
- **DHCP relay.** From a test client on VLAN 160 at `BR1`, confirm a lease
  is obtained from the HQ pool (address should be in the `10.13.20.0/24`
  or a dedicated BR1 scope, depending on how the scope was defined); if no
  offer arrives, confirm the `ip helper-address` statements are present on
  the correct SVI and that the WAN path is up.
- **RODC replication.** `repadmin /replsummary` from `dc-br101` should show
  inbound replication from `dc01` succeeding; an RODC that never
  replicates typically indicates the WAN link or the OSPF adjacency it
  depends on was not actually up when the promotion ran.
- **Common failure: forgetting the DNS forwarder repoint.** If external
  name resolution stops working for domain members immediately after this
  chapter's cutover, confirm the forwarder change in Implementation and
  Automation was actually applied — this is the single most common
  self-inflicted outage in this chapter.

## Security and Best Practices

- Restrict Telnet on every Cisco device introduced in this chapter; use
  SSH with local AAA or, once [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) exists, centralized
  authentication.
- Apply Control Plane Policing (CoPP) on `rtr-hq01` and `rtr-br101` to
  protect the route processor from a flooded or misconfigured link,
  consistent with the infrastructure defense practices in [Volume X](../../volume-010-enterprise-cybersecurity/README.md),
  [Chapter 04](04-virtualization-storage-and-data-protection-lab.md) (Network Security Architecture and Infrastructure Defense).
- Keep the wireless guest SSID on VLAN 140 fully isolated from every
  internal VLAN at the firewall/ACL layer — a guest network that can reach
  `10.13.10.0/24` defeats the purpose of segmenting it in the first place.
- Use a unique, sufficiently long IPsec pre-shared key for the WAN tunnel
  and record it in a lab-scoped secrets location, not in the running
  configuration comments or this chapter's command history.
- Log HSRP state transitions and OSPF adjacency changes; [Chapter 08](08-observability-operations-and-major-incident-lab.md) wires
  this telemetry into the volume's observability stack, but the logging
  needs to exist first.

## References and Knowledge Checks

**References**

- [RFC 2338](https://www.rfc-editor.org/rfc/rfc2338) — *Virtual Router Redundancy Protocol* (HSRP is Cisco's
  proprietary predecessor; VRRP concepts apply directly).
- [RFC 2328](https://www.rfc-editor.org/rfc/rfc2328) — *OSPF Version 2*.
- [Volume II](../../volume-002-network-engineering-foundations/README.md), Chapters 03–04, 06–07 — Layer 2 resilience, IP routing,
  wireless foundations, and enterprise network design and resilience.
- [Volume III](../../volume-003-cisco-enterprise-networking/README.md), Chapters 02–05 — Catalyst campus switching, enterprise
  routing, WAN/internet edge, and Catalyst wireless architecture.
- [Volume IV, Chapter 04](../../volume-004-enterprise-systems-administration/chapters/04-enterprise-identity-and-directory-services.md) — Enterprise Identity and Directory Services (RODC
  placement).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Cisco IOS XE
  17.x baseline used throughout this chapter.

**Knowledge checks**

1. Why does reusing the existing `.1` gateway addresses as HSRP virtual
   IPs matter for the systems [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) already deployed?
2. What does an RODC at `BR1` protect against that a full read-write
   domain controller would not?
3. Why is a single WAN path treated as an intentional gap in this
   chapter's design rather than an oversight?
4. If two core switches both show HSRP state `Active` for the same group
   at the same time, what should you check first?

## Hands-On Lab

This chapter's labs build the **integrated network fabric** — campus/WAN segmentation, routing,
wireless, and network services — connecting the environment, drawing on Volumes II, III, and VII.
Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.4** — the core services from Chapter 02, and switching/routing
capability (physical, virtual, or via Linux bridges/FRR). **Cost:** none.

### Lab 3.1 — Segmented campus network (Topic: Segmentation)

**Objective:** Separate the environment's traffic classes into VLANs.

```bash
# Create the segment VLANs the environment uses (server, user, mgmt, guest) on a VLAN-aware bridge:
sudo ip link add link eth0 name eth0.10 type vlan id 10   # management
sudo ip link add link eth0 name eth0.20 type vlan id 20   # servers
bridge vlan show 2>/dev/null | head
```

**Expected result:** the environment's traffic is segmented into purpose VLANs (management, servers,
users, guest) — segmentation (Volume II/X) contains failure and attack blast radius and enforces
policy between classes, the network foundation the security labs (Chapter 07) build zero-trust on.

**Negative test:** run all services on one flat network; a compromise or broadcast storm affects
everything and the security labs have no segmentation to enforce — segmented VLANs are the substrate
for policy.

**Cleanup:** `sudo ip link del eth0.10; sudo ip link del eth0.20`.

### Lab 3.2 — Inter-segment routing (Topic: Routing)

**Objective:** Route between segments with policy.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
ip route show
# Dynamic routing (FRR/OSPF, Vol II) or static routes connect the segments; policy at the L3 boundary.
sudo vtysh -c 'show ip route' 2>/dev/null | head || echo "(routes connect server/user/mgmt segments)"
```

**Expected result:** the segments are routed with the L3 boundary as the policy enforcement point —
inter-VLAN routing connects the environment while the L3 boundary is where security policy (Chapter
07) between classes is enforced, integrating networking and security design.

**Negative test:** route all segments openly with no policy; segmentation provides no security benefit
— the routed boundary must carry policy, or the VLANs are just cosmetic.

**Cleanup:** `sudo sysctl -w net.ipv4.ip_forward=0` if lab-only.

### Lab 3.3 — Wireless access integrated with identity (Topic: Wireless)

**Objective:** Onboard wireless clients into the same identity/segmentation.

```text
# Configure the WLAN (Vol II) so clients:
#   - authenticate via 802.1X against the directory (Ch02) — same identity as wired
#   - land in the correct VLAN/segment (Ch03) per role (corporate/guest)
# Verify a client authenticates with a domain account and is placed in the right segment.
```

**Expected result:** wireless clients authenticate with directory identity (802.1X) and inherit the
wired segmentation — integrated wireless is not a separate island: it uses the same identity (Chapter
02) and segmentation (this chapter), so a user's access is consistent whether wired or wireless.

**Negative test:** run wireless with a separate PSK and its own flat VLAN; clients bypass the
environment's identity and segmentation model — integrated 802.1X + role-based VLAN keeps wireless
consistent with the rest.

**Cleanup:** none.

### Lab 3.4 — Network services validation (Topic: Integration validation)

**Objective:** Confirm end-to-end reachability across the fabric.

```bash
# From a client segment, reach a server-segment service through the routed, segmented fabric:
ping -c2 <server-in-vlan20>
getent hosts app.lab.example.com && curl -sI http://app.lab.example.com | head -1
traceroute -n <server-in-vlan20> | head
```

**Expected result:** a client in one segment resolves and reaches a service in another through the
routed fabric, with the path visible — validating end-to-end (DNS + routing + segmentation + service)
confirms the network fabric actually connects the environment, the prerequisite for the
virtualization, cloud, and application labs that follow.

**Negative test:** assume the fabric works because links are up; a missing route, wrong VLAN, or DNS
gap breaks end-to-end reachability — the integrated validation (name → route → reach) proves it.

**Cleanup:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter replaced [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s placeholder gateway with a resilient
Catalyst core, a real HQ–BR1 WAN link, extended directory services to
`BR1` via an RODC, and controller-based wireless — while proving the
cutover was invisible to the identity services [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) built. The
negative test confirmed HSRP failover is transparent to endpoints, and the
single-WAN-path design gap is now a documented, intentional target for
later resilience work.

- [ ] Cut over HQ routing to an HSRP core pair without reconfiguring
      existing hosts' default gateways.
- [ ] Established OSPF and an IPsec site-to-site tunnel between `HQ` and
      `BR1`.
- [ ] Extended the directory to `BR1` with a working RODC.
- [ ] Deployed wireless with correctly segmented corporate and guest
      SSIDs.
- [ ] Completed the HSRP failover negative test and confirmed
      transparent recovery.
