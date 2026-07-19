# Chapter 06: Cisco Network Services, QoS, and Application Delivery

![Lab flow for this chapter: an IP phone on ACCESS-01's trust boundary (trust device cisco-phone) marks voice traffic, which flows through DIST-01 to a WAN-edge device applying the WAN-EDGE-OUT policy-map (VOICE, VIDEO, CALL-SIGNALING, BUSINESS-CRITICAL classes with LLQ/CBWFQ) outbound; under sustained best-effort congestion plus a DSCP EF-marked test stream, the VOICE class shows near-zero drops while class-default absorbs tail-drops. As a negative test, removing the service-policy from the WAN interface and repeating the test shows the EF stream now drops/jitters proportionally to the congestion, proving the queuing policy — not the marking alone — protected voice.](../../../diagrams/volume-03-cisco-enterprise-networking/chapter-06-qos-trust-boundary-wan-edge-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: QoS marking at the access trust boundary carried through to a WAN-edge LLQ/CBWFQ policy, tested under congestion with and without the queuing policy applied.*

## Learning Objectives

- Configure core network services — DHCP snooping/relay, NTP, and IP
  multicast — that campus and WAN designs depend on.
- Explain the DiffServ QoS model and how trust boundaries, classification,
  and marking establish consistent per-hop behavior across a network.
- Configure the Modular QoS CLI (MQC) to classify, mark, queue, shape, and
  police traffic on Catalyst 9000 and IOS XE WAN platforms.
- Use Network-Based Application Recognition (NBAR2) to classify traffic by
  application rather than by port number alone.
- Configure PIM sparse mode and IGMP snooping to deliver multicast traffic
  efficiently across a campus.
- Validate QoS policy behavior and diagnose the most common queuing and
  marking failures.

## Theory and Architecture

### Core network services

Every campus and WAN design in this volume depends on a small set of
always-on infrastructure services:

- **DHCP** — most enterprise designs run DHCP relay (`ip helper-address`)
  on distribution-layer SVIs pointing at a centralized DHCP server rather
  than running the DHCP server role on every switch; **DHCP snooping**
  (Security and Best Practices, below) builds a trusted binding table used
  by several downstream security features.
- **NTP** — every device in this volume assumes accurate, synchronized time
  for logging correlation, certificate validation, and 802.1X/RADIUS
  timestamp accuracy; NTP is a day-0 configuration item, not an
  afterthought.
- **IP multicast** — delivers one-to-many traffic (video, market data
  feeds, certain IoT and building-management protocols) without
  replicating the stream once per receiver; **PIM sparse mode** is the
  current standard multicast routing protocol for enterprise campus and
  WAN designs.

### The DiffServ QoS model

Cisco enterprise QoS designs implement **Differentiated Services
(DiffServ)**, in which traffic is classified once (as close to the source
as practical) and then receives consistent **per-hop behavior (PHB)** at
every downstream device based on a marking carried in the packet itself,
rather than requiring every hop to re-classify traffic from scratch:

- **Layer 2 marking** — the 3-bit **Class of Service (CoS)** field in the
  802.1Q tag ([Chapter 2](02-catalyst-campus-switching-and-resiliency.md)), significant only within a Layer 2 domain.
- **Layer 3 marking** — the 6-bit **Differentiated Services Code Point
  (DSCP)** field in the IP header, which survives Layer 3 hops end to end
  and is the primary marking used for policy decisions in current designs.
  Common DSCP values include `EF` (Expedited Forwarding, voice), `AF41`
  (video), and `CS3`/`AF31` (call signaling/business-critical data).

A **trust boundary** is the point in the network where a device either
trusts an incoming CoS/DSCP marking or re-classifies traffic from scratch.
The trust boundary should sit as close to the source as the source can be
trusted — a Cisco IP phone is generally trusted to mark its own voice
traffic correctly, but an ordinary user's PC port should not be trusted,
since a user application could otherwise mark its own traffic as
high-priority voice and unfairly starve real voice traffic.

### QoS mechanisms

Four mechanisms work together, applied through the **Modular QoS CLI
(MQC)** three-part model (`class-map` classifies, `policy-map` defines
per-class actions, `service-policy` applies the policy to an interface):

- **Classification** — identifying traffic by ACL match, DSCP/CoS value,
  or NBAR2 application signature.
- **Marking** — setting or rewriting the CoS/DSCP value once classified.
- **Queuing** — Catalyst and IOS XE platforms use **Class-Based Weighted
  Fair Queuing (CBWFQ)** for guaranteed-bandwidth classes and a strict-
  priority **Low Latency Queuing (LLQ)** class for traffic (voice) that
  cannot tolerate queuing delay at all; LLQ traffic is policed to its
  configured rate so it cannot starve every other class during a burst.
- **Shaping and policing** — **shaping** delays traffic above a configured
  rate (buffering it to smooth bursts, commonly used outbound on a WAN
  edge to match a provider's committed rate); **policing** drops or
  re-marks traffic above a configured rate instantly, with no buffering.

**Congestion avoidance** — **Weighted Random Early Detection (WRED)**
drops packets probabilistically as a queue approaches capacity, favoring
lower-priority traffic first, so TCP sessions back off gradually instead
of the synchronized "global sync" pattern caused by a queue that fills and
tail-drops indiscriminately.

### NBAR2

**Network-Based Application Recognition (NBAR2)** classifies traffic using
deep packet inspection signatures (protocol behavior, not just port
number), which matters because modern applications frequently share port
443 with unrelated traffic. NBAR2 classification can feed both QoS
marking/queuing decisions and read-only visibility (`show ip nbar
protocol-discovery`) without any enforcement action at all — useful during
a QoS design's discovery phase, before any policy is enforced.

### IP multicast fundamentals

- **IGMP (Internet Group Management Protocol)** — the protocol hosts use
  to join/leave a multicast group; **IGMP snooping** on a Layer 2 switch
  listens to IGMP messages so it forwards multicast traffic only out
  ports with an active receiver, instead of flooding it to every port in
  the VLAN.
- **PIM (Protocol Independent Multicast)** — the Layer 3 protocol that
  builds the actual multicast distribution tree between routers.
  **PIM sparse mode (PIM-SM)** is the enterprise standard: routers join a
  shared tree rooted at a **Rendezvous Point (RP)** only when a receiver
  actually requests a group, rather than flooding multicast everywhere
  (as PIM dense mode does).
- **RP redundancy** — production designs use either **Anycast RP** (MSDP
  or PIM-based, multiple routers share one RP address for load-sharing and
  failover) or a well-monitored single static RP; **Auto-RP** and
  **BSR (Bootstrap Router)** provide dynamic RP discovery for designs that
  prefer not to statically configure the RP address on every router.

## Design Considerations

- **Trust boundary placement** — trust CoS/DSCP from known-good sources
  (IP phones, dedicated video endpoints, servers behind an access-controlled
  port) and re-classify/re-mark everything else at the first hop; never
  trust an ordinary user-facing access port by default.
- **Class model size** — use a small, standardized set of QoS classes
  (commonly voice/EF, video/AF41, call-signaling/CS3, business-critical
  data/AF31, and a best-effort default) applied consistently campus-wide
  and WAN-wide, rather than a bespoke policy per site, so behavior stays
  predictable and troubleshootable.
- **LLQ sizing** — size the priority (LLQ) queue bandwidth to the actual
  measured voice/video bandwidth requirement, not a round number; an
  oversized LLQ queue can starve every other class during sustained load,
  defeating the purpose of having other classes at all.
- **Shaping vs. policing at the WAN edge** — shape outbound traffic to
  match (or slightly undershoot) a provider's committed rate on
  lower-speed WAN circuits to avoid provider-side tail drops; use policing
  primarily for inbound rate enforcement or for classes that should be
  hard-capped rather than smoothed.
- **NBAR2 as a discovery tool first** — run NBAR2 in protocol-discovery
  (visibility only) mode before authoring an enforcement policy from it, so
  the policy is based on the site's actual measured traffic mix.
- **Multicast RP placement** — place the RP topologically central to
  sources and receivers, and always plan RP redundancy (Anycast RP is
  the current best practice) before a design goes into production, since
  an RP outage with no redundancy silently breaks every active multicast
  group.
- **IGMP snooping as the default** — enable IGMP snooping on every VLAN
  carrying multicast traffic; without it, a Layer 2 switch treats
  multicast like broadcast and floods it to every port, which does not
  scale past a handful of receivers.

## Implementation and Automation

### DHCP relay and NTP

```text
DIST-01(config)# interface Vlan10
DIST-01(config-if)# ip helper-address 10.10.99.53
DIST-01(config-if)# exit
DIST-01(config)# ntp server 10.10.99.10 prefer
DIST-01(config)# ntp server 10.10.99.11
DIST-01(config)# clock timezone EST -5
```

### DHCP snooping (trust anchor for downstream security features)

```text
DIST-01(config)# ip dhcp snooping
DIST-01(config)# ip dhcp snooping vlan 10,20,99
DIST-01(config)# interface Port-channel1
DIST-01(config-if)# ip dhcp snooping trust
DIST-01(config-if)# exit
ACCESS-01(config)# interface range GigabitEthernet1/0/1-48
ACCESS-01(config-if-range)# ip dhcp snooping limit rate 15
```

Uplinks toward the DHCP server (or toward the relay agent) are trusted;
every user-facing access port is untrusted by default, which is what
allows DHCP snooping to block rogue DHCP servers plugged into an access
port (Security and Best Practices).

### NBAR2 protocol discovery

```text
DIST-01(config)# interface Port-channel1
DIST-01(config-if)# ip nbar protocol-discovery
DIST-01# show ip nbar protocol-discovery interface Port-channel1
```

### Classification, marking, and LLQ/CBWFQ policy

```text
DIST-01(config)# class-map match-any VOICE
DIST-01(config-cmap)# match dscp ef
DIST-01(config-cmap)# exit
DIST-01(config)# class-map match-any VIDEO
DIST-01(config-cmap)# match dscp af41
DIST-01(config-cmap)# exit
DIST-01(config)# class-map match-any CALL-SIGNALING
DIST-01(config-cmap)# match dscp cs3
DIST-01(config-cmap)# exit
DIST-01(config)# class-map match-any BUSINESS-CRITICAL
DIST-01(config-cmap)# match protocol nbar ssl
DIST-01(config-cmap)# match dscp af31
DIST-01(config-cmap)# exit

DIST-01(config)# policy-map WAN-EDGE-OUT
DIST-01(config-pmap)# class VOICE
DIST-01(config-pmap-c)# priority level 1 percent 10
DIST-01(config-pmap-c)# exit
DIST-01(config-pmap)# class VIDEO
DIST-01(config-pmap-c)# priority level 2 percent 20
DIST-01(config-pmap-c)# exit
DIST-01(config-pmap)# class CALL-SIGNALING
DIST-01(config-pmap-c)# bandwidth percent 5
DIST-01(config-pmap-c)# exit
DIST-01(config-pmap)# class BUSINESS-CRITICAL
DIST-01(config-pmap-c)# bandwidth percent 30
DIST-01(config-pmap-c)# random-detect dscp-based
DIST-01(config-pmap-c)# exit
DIST-01(config-pmap)# class class-default
DIST-01(config-pmap-c)# bandwidth percent 25
DIST-01(config-pmap-c)# random-detect
DIST-01(config-pmap-c)# exit
DIST-01(config-pmap)# exit
DIST-01(config)# interface GigabitEthernet0/0/0
DIST-01(config-if)# description WAN edge to MPLS/DMVPN transport
DIST-01(config-if)# service-policy output WAN-EDGE-OUT
```

`priority level 1` and `level 2` allow two independent low-latency
queues (voice ahead of video) rather than mixing both into a single LLQ
class, which keeps voice protected even during a heavy video burst.

### Access-edge trust and marking

```text
ACCESS-01(config)# interface GigabitEthernet1/0/1
ACCESS-01(config-if)# description User port with IP phone
ACCESS-01(config-if)# switchport voice vlan 20
ACCESS-01(config-if)# trust device cisco-phone
ACCESS-01(config-if)# mls qos trust cos
```

`trust device cisco-phone` extends CoS/DSCP trust to a verified Cisco IP
phone specifically (via CDP negotiation) while leaving the PC daisy-chained
behind the phone's own switchport untrusted by default.

### Shaping at a WAN edge

```text
DIST-01(config)# policy-map WAN-SHAPE
DIST-01(config-pmap)# class class-default
DIST-01(config-pmap-c)# shape average 8000000
DIST-01(config-pmap-c)# service-policy WAN-EDGE-OUT
DIST-01(config-pmap-c)# exit
DIST-01(config-pmap)# exit
DIST-01(config)# interface GigabitEthernet0/0/0
DIST-01(config-if)# service-policy output WAN-SHAPE
```

Nesting `WAN-EDGE-OUT` as a child policy inside the shaper's
`class-default` applies the queuing/priority behavior within the shaped
8 Mbps envelope, matching a circuit whose physical interface speed exceeds
its purchased committed rate.

### PIM sparse mode and Anycast RP

```text
CORE-01(config)# ip multicast-routing
CORE-01(config)# interface Loopback0
CORE-01(config-if)# ip pim sparse-mode
CORE-01(config-if)# exit
CORE-01(config)# interface TenGigabitEthernet1/0/1
CORE-01(config-if)# ip pim sparse-mode
CORE-01(config-if)# exit
CORE-01(config)# ip pim rp-address 10.255.255.1 override
CORE-01(config)# interface Vlan10
CORE-01(config-if)# ip pim sparse-mode
CORE-01(config-if)# exit
ACCESS-01(config)# ip igmp snooping
ACCESS-01(config)# ip igmp snooping vlan 10
```

`ip igmp snooping` is enabled globally by default on Catalyst 9000
switches; the explicit `vlan 10` line is shown for clarity and is required
only if snooping was previously disabled on that VLAN.

## Validation and Troubleshooting

```text
DIST-01# show policy-map interface GigabitEthernet0/0/0
DIST-01# show policy-map interface GigabitEthernet0/0/0 output class VOICE
DIST-01# show mls qos interface GigabitEthernet1/0/1
DIST-01# show ip nbar protocol-discovery interface Port-channel1
DIST-01# show ip dhcp snooping binding
CORE-01# show ip pim neighbor
CORE-01# show ip mroute
ACCESS-01# show ip igmp snooping groups
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Voice quality degrades under load despite an LLQ policy | LLQ class undersized against actual voice bandwidth, or policy not applied on the correct (egress WAN) interface | `show policy-map interface`, confirm drops/matches on the `VOICE` class and correct interface/direction |
| DSCP markings reset to 0 somewhere in the path | An intermediate device re-marking/clearing DSCP, or a trust boundary misconfigured to distrust an already-trusted source | `show mls qos interface`, trace marking hop by hop with packet captures ([Volume XX](../../volume-20-wireshark-packet-analysis/README.md)) |
| Client PC's traffic unexpectedly prioritized as voice | Access port trusting CoS/DSCP from an untrusted host instead of only the verified phone | `show mls qos interface`, confirm `trust device cisco-phone` (not blanket `mls qos trust cos`) on phone-attached ports |
| Rogue DHCP server hands out incorrect leases | DHCP snooping not enabled, or the rogue server's port marked trusted | `show ip dhcp snooping binding`, `show ip dhcp snooping`, confirm the offending port is untrusted |
| Multicast receiver never gets traffic | No PIM neighbor relationship, RP unreachable, or IGMP snooping suppressing the join upstream | `show ip pim neighbor`, `show ip mroute`, `show ip igmp snooping groups` |
| Multicast works from a wired receiver but not from a specific VLAN | `ip pim sparse-mode` missing on that VLAN's SVI | `show ip pim interface`, confirm PIM is enabled on every SVI carrying multicast receivers/sources |

## Security and Best Practices

- Enable DHCP snooping on every VLAN that serves untrusted endpoints and
  mark only server-facing/uplink ports as trusted; DHCP snooping is also a
  prerequisite for **Dynamic ARP Inspection (DAI)** and **IP Source
  Guard**, both covered in [Chapter 7](07-cisco-identity-access-control-and-segmentation.md) as segmentation/identity controls.
- Never leave an access port's QoS trust set to blanket `mls qos trust
  cos` or `trust dscp`; use `trust device cisco-phone` (or leave the port
  untrusted and re-mark) so an end user cannot self-mark traffic as
  high-priority.
- Rate-limit DHCP requests per port (`ip dhcp snooping limit rate`) to
  blunt a DHCP-exhaustion attack from a single compromised or malicious
  endpoint.
- Restrict NTP to authenticated, known-good time sources (`ntp
  authenticate` with keys) at the WAN/internet edge, since an unauthenticated
  time source can be used to disrupt certificate validation and log
  correlation across the estate.
- Apply Control Plane Policing (CoPP, [Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md)) alongside data-plane QoS;
  QoS protects application traffic from other application traffic, while
  CoPP protects the device's own control plane (including PIM, IGMP, and
  NTP protocol traffic) from being starved or attacked.
- Filter multicast group ranges at the network edge (`ip multicast
  boundary`) so internal-only multicast applications cannot leak
  advertisements to or receive traffic from an external network.

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Enterprise QoS Solution Reference Network Design (SRND)*.
- [RFC 2474](https://www.rfc-editor.org/rfc/rfc2474)/2475, *Definition of the Differentiated Services Field*.
- [RFC 4601](https://www.rfc-editor.org/rfc/rfc4601), *Protocol Independent Multicast - Sparse Mode (PIM-SM)*.
- Cisco, *IP Multicast Design and Anycast RP Configuration Guide*.

**Knowledge checks**

1. Why does DiffServ classify traffic once, close to the source, instead
   of at every hop?
2. What is the practical difference between shaping and policing, and
   when would a WAN edge use each?
3. Why should an ordinary user access port never be trusted for CoS/DSCP,
   while a verified IP phone port can be?
4. What role does IGMP snooping play at Layer 2, and how does it differ
   from PIM's role at Layer 3?
5. Why does Anycast RP improve on a single static RP for production
   multicast designs?

## Hands-On Lab

**Objective:** Build an end-to-end QoS policy from an access-layer trust
boundary through a WAN-edge LLQ/CBWFQ policy, and verify a low-priority
class is throttled under congestion while the priority class is protected.

**Prerequisites**

- The distribution/access topology from [Chapter 2](02-catalyst-campus-switching-and-resiliency.md)'s lab (or an equivalent
  CML topology), plus one router or Layer 3 switch acting as a WAN edge
  with a rate-limited or shaped outbound interface.
- A traffic generator (a second host, `iperf3`, or equivalent) capable of
  generating sustained best-effort traffic and separate DSCP-marked test
  traffic.

**Procedure**

1. Configure DHCP snooping and NTP as shown in Implementation, and confirm
   the snooping binding table populates after a client lease renewal:

   ```text
   DIST-01# show ip dhcp snooping binding
   ```

   **Expected result:** at least one binding entry appears for a live
   client lease.

2. Configure the access-port trust boundary (`trust device cisco-phone`)
   on a port with an IP phone attached, or simulate it with `mls qos trust
   cos` on a lab-only test port if no phone is available, and confirm:

   ```text
   ACCESS-01# show mls qos interface GigabitEthernet1/0/1
   ```

   **Expected result:** the interface shows the configured trust state.

3. Configure the `VOICE`, `VIDEO`, `CALL-SIGNALING`, and
   `BUSINESS-CRITICAL` class maps and the `WAN-EDGE-OUT` policy-map on the
   WAN-edge device, and apply it outbound on the WAN interface.

4. Generate sustained best-effort traffic toward the WAN interface to
   push it into congestion, while separately sending a stream of
   DSCP EF–marked test traffic (for example, `iperf3` with `--tos 0xb8`)
   across the same path.

5. Verify class-based queue statistics during the congested test:

   ```text
   DIST-01# show policy-map interface GigabitEthernet0/0/0
   ```

   **Expected result:** the `VOICE` class shows near-zero drops and
   consistent throughput at its configured rate, while `class-default`
   shows drops/tail-drops as it absorbs the congestion.

6. **Negative test:** remove the `service-policy output` from the WAN
   interface and repeat the same congested test.

   ```text
   DIST-01(config)# interface GigabitEthernet0/0/0
   DIST-01(config-if)# no service-policy output WAN-EDGE-OUT
   ```

   **Expected result:** the EF-marked stream now experiences drops/jitter
   proportional to the best-effort congestion, demonstrating the queuing
   policy — not the marking alone — is what protected voice traffic in
   step 5.

7. Re-apply `service-policy output WAN-EDGE-OUT` to restore protection.

**Cleanup**

- Remove the lab-only class-maps and policy-map if the WAN-edge device is
  shared:

  ```text
  DIST-01(config)# interface GigabitEthernet0/0/0
  DIST-01(config-if)# no service-policy output WAN-EDGE-OUT
  DIST-01(config)# no policy-map WAN-EDGE-OUT
  ```

- Stop the traffic generator and confirm interface utilization returns to
  baseline.

## Summary and Completion Checklist

Consistent application delivery in an enterprise network depends on
services most users never see directly — DHCP, NTP, and multicast routing
— plus a DiffServ QoS model that classifies traffic once and enforces it
consistently at every hop through MQC-based marking, LLQ/CBWFQ queuing,
and shaping or policing at bandwidth-constrained edges. NBAR2 extends
classification beyond simple port matching, and IGMP snooping paired with
PIM sparse mode delivers multicast efficiently instead of flooding it like
broadcast traffic.

- [ ] Can configure DHCP relay/snooping and NTP as baseline network
      services.
- [ ] Can explain the DiffServ trust-boundary model and why it matters.
- [ ] Can build an MQC classification, marking, and LLQ/CBWFQ policy and
      apply shaping at a WAN edge.
- [ ] Can configure PIM sparse mode and IGMP snooping for efficient
      multicast delivery.
- [ ] Completed the hands-on lab, including the negative test showing
      queuing policy protects priority traffic under congestion.
