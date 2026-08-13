# Chapter 04: Ethernet, ARP, IPv4, and ICMPv4 Analysis

![Lab flow for this chapter: a capture scoped to ARP and ICMP shows one broadcast ARP request followed by one unicast reply resolving the gateway's MAC address; a ping sequence isolates to matched Echo Request/Reply pairs, and a traceroute isolates to a Time Exceeded hop ladder ending in the destination's reply. As a negative test, a filter for an original Echo Request TTL value never actually used in this lab's traffic returns zero matches, confirming the filter correctly produces an empty result rather than matching unrelated packets.](../../../diagrams/volume-020-wireshark-packet-analysis/chapter-04-arp-icmp-traceroute-filter-flow.svg)

*Figure 4-1. Flow used throughout this chapter's Hands-On Lab: ARP, ICMP echo, and traceroute captured and isolated with targeted display filters, tested against a TTL value that cannot appear.*

## Learning Objectives

- Decode an Ethernet II frame's fields in Wireshark and explain what each
  reveals about the local segment.
- Read and validate an ARP request/reply exchange, and recognize the
  packet-level signature of ARP spoofing.
- Decode the IPv4 header fields that matter most for troubleshooting:
  TTL, fragmentation flags/offset, DSCP, and protocol number.
- Interpret ICMPv4 type/code combinations for both diagnostic (echo,
  traceroute) and error-reporting (unreachable, time exceeded) traffic.
- Build display filters that isolate Ethernet, ARP, IPv4, and ICMPv4
  conditions for troubleshooting and security triage.

## Theory and Architecture

This chapter is the first of two (with [Chapter 05](05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md)) that apply the interface
and filtering skills from [Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md) to specific protocol layers, working
bottom-up through the encapsulation chain introduced in [Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md). This
chapter covers the IPv4 protocol family; [Chapter 05](05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) covers its IPv6
counterpart plus the transport- and application-layer protocols that ride
on both.

### Ethernet II framing

Wireshark's Packet Detail pane shows the Ethernet II header as the
outermost layer for traffic captured on a wired or switched segment:

```text
Ethernet II
    Destination: <MAC>
    Source: <MAC>
    Type: IPv4 (0x0800)
```

| Field | Significance |
| --- | --- |
| Destination/Source MAC | Locally significant addresses; the first three octets (the OUI) identify the manufacturer and can help fingerprint unknown devices via Wireshark's built-in OUI database. |
| EtherType | Identifies the next-layer protocol (`0x0800` IPv4, `0x0806` ARP, `0x86DD` IPv6, `0x8100` 802.1Q tag). This is the field the dissector engine uses to select the next dissector in the chain. |

An 802.1Q-tagged frame inserts a 4-byte tag between the source MAC and the
original EtherType, visible in Wireshark as a nested `802.1Q Virtual LAN`
layer carrying the VLAN ID and priority bits — the field the `vlan.id`
filter matches against.

### ARP

Address Resolution Protocol resolves an IPv4 address to a MAC address on
the local segment. A normal exchange is two frames:

```text
ARP request (broadcast, ff:ff:ff:ff:ff:ff):
    Who has 10.0.20.15? Tell 10.0.20.1

ARP reply (unicast, to the requester's MAC):
    10.0.20.15 is at aa:bb:cc:dd:ee:ff
```

A **gratuitous ARP** — a reply or request sent unprompted, announcing a
host's own IP-to-MAC mapping — is normal after an interface comes up, an IP
address changes, or a failover event (VRRP/HSRP) promotes a new active
node. It becomes a security signal when the same IP address is announced
with two different MAC addresses in a short window from hosts that have no
legitimate failover relationship — the packet-level signature of ARP
spoofing/cache poisoning, covered further in [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md).

### IPv4 header fields

```text
Internet Protocol Version 4, Src: 10.0.20.15, Dst: 10.0.30.20
    Version: 4
    Header Length: 20 bytes
    Differentiated Services Field: DSCP: CS0, ECN: Not-ECT
    Total Length: 60
    Identification: 0x4a2f
    Flags: 0x2, Don't fragment
    Fragment Offset: 0
    Time to Live: 64
    Protocol: TCP (6)
    Header Checksum: [validation disabled]
    Source: 10.0.20.15
    Destination: 10.0.30.20
```

| Field | Use in analysis |
| --- | --- |
| TTL | Decrements once per router hop; a TTL that is unexpectedly low for a known-local destination indicates extra hops (routing loop or unexpected path); TTL is also a coarse OS fingerprint (common starting values: 64 Linux/macOS, 128 Windows, 255 many network appliances). |
| Flags (Don't Fragment / More Fragments) and Fragment Offset | Identify fragmented traffic; `ip.flags.mf==1` matches non-final fragments, and a nonzero `ip.frag_offset` matches every fragment after the first. Fragmentation is frequently a Path MTU problem ([Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md)) rather than a protocol-level issue. |
| DSCP | Differentiated Services value used for QoS marking/remarking verification — confirm a marking policy is applied at the expected point in the path rather than assuming it based on configuration alone. |
| Protocol | Identifies the next-layer protocol (1 ICMP, 6 TCP, 17 UDP) and is what the dissector engine uses to hand off to the transport-layer dissector. |
| Header Checksum | Wireshark can validate this, but many NICs perform checksum offload, which means the value captured at the sending host is frequently `0x0000` and not actually invalid — see Validation and Troubleshooting. |

### ICMPv4

ICMP carries both deliberate diagnostic traffic and automatic error
reporting generated by routers and hosts:

| Type | Common code(s) | Meaning |
| --- | --- | --- |
| 0 | 0 | Echo Reply (`ping` response) |
| 3 | 0–15 | Destination Unreachable (0 = network unreachable, 1 = host unreachable, 3 = port unreachable, 4 = fragmentation needed and DF set) |
| 5 | 0–3 | Redirect (a router informing a host of a better next hop) |
| 8 | 0 | Echo Request (`ping`) |
| 11 | 0–1 | Time Exceeded (0 = TTL expired in transit — the mechanism `traceroute`/`tracert` relies on) |

`traceroute` (Linux/macOS, UDP- or ICMP-based) and `tracert` (Windows,
ICMP-based) both work by sending probes with successively incrementing TTL
values and reading the Type 11 Time Exceeded responses from each
intermediate hop; a capture of a traceroute session shows this pattern
directly as a ladder of increasing source addresses replying to increasing
TTL values.

## Design Considerations

- **Capture point changes what TTL and fragmentation reveal.** A capture
  taken close to the sender shows the original TTL and fragmentation
  decision; a capture taken further along the path shows the effect of
  every intermediate hop's decrement and any path-MTU-driven
  fragmentation. State the capture point explicitly when reporting TTL- or
  fragmentation-based findings.
- **ARP is inherently local-segment-only.** ARP traffic never crosses a
  Layer 3 boundary; if an ARP-based finding (spoofing, excessive
  broadcast) needs to be correlated across segments, it must be captured
  independently on each segment's mirror/TAP point ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)).
  Gratuitous ARP baselines should be established per segment, since normal
  failover patterns (VRRP/HSRP) differ by environment.
- **Checksum offload changes what "invalid checksum" means.** Deciding
  whether to trust Wireshark's checksum validation column requires knowing
  whether the capture point is upstream or downstream of the sending NIC's
  offload engine (see Validation and Troubleshooting).
- **ICMP filtering policy affects what a capture can show.** Many
  enterprise firewalls rate-limit or block ICMP; a capture that shows no
  Time Exceeded responses from certain hops may reflect a filtering policy
  rather than routing behavior — confirm the organization's ICMP policy
  before concluding a hop is unreachable.

## Implementation and Automation

### Ethernet and VLAN filters

```text
eth.addr == aa:bb:cc:dd:ee:ff        # either source or destination MAC
eth.src == aa:bb:cc:dd:ee:ff
eth.dst == ff:ff:ff:ff:ff:ff         # broadcast frames
vlan.id == 20                        # 802.1Q-tagged traffic on VLAN 20
eth.type == 0x0806                   # ARP by EtherType
```

### ARP filters and gratuitous ARP detection

```text
arp                                  # all ARP traffic
arp.opcode == 1                      # ARP requests
arp.opcode == 2                      # ARP replies
arp.src.proto_ipv4 == arp.dst.proto_ipv4   # gratuitous ARP (announcing own IP)
```

`tshark` scripted extraction of every IP-to-MAC mapping observed in a
capture, useful as an ARP-spoofing baseline (expanded in [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)):

```bash
tshark -r capture.pcapng -Y "arp.opcode==2" \
  -T fields -e arp.src.proto_ipv4 -e arp.src.hw_mac | sort -u
```

A given IPv4 address appearing with more than one MAC address in this
output — outside a known VRRP/HSRP virtual MAC pattern — is the signature
to investigate further.

### IPv4 filters

```text
ip.addr == 10.0.20.15                # either source or destination
ip.src == 10.0.20.15 && ip.dst == 10.0.30.20
ip.ttl < 10                          # unusually low TTL
ip.flags.mf == 1 || ip.frag_offset > 0   # fragmented traffic (any fragment)
ip.dsfield.dscp == 46                # DSCP EF (expedited forwarding) marking
ip.proto == 1                        # ICMP
```

### ICMPv4 filters

```text
icmp                                  # all ICMPv4 traffic
icmp.type == 8                        # echo requests
icmp.type == 0                        # echo replies
icmp.type == 3 && icmp.code == 3      # port unreachable
icmp.type == 11 && icmp.code == 0     # TTL exceeded (traceroute hop)
```

Correlate an ICMP error back to the packet that triggered it: Wireshark
automatically parses the original packet's headers embedded in the ICMP
error payload and exposes them as `icmp` sub-fields (for example,
`ip.dst` inside the quoted original datagram), which the Packet Detail
pane displays as a nested "Internet Protocol Version 4" node under the
ICMP layer.

### Capturing and reading a traceroute

```bash
# Linux/macOS
tshark -i <INTERFACE_NUMBER> -f "icmp or udp portrange 33434-33534" \
  -w traceroute-capture.pcapng &
traceroute 8.8.8.8
```

```text
Filter to read the result in order:
icmp.type==11 || icmp.type==0 || icmp.type==8
```

## Validation and Troubleshooting

- **Header checksum shows as "unverified" or incorrect on outbound
  traffic.** This is expected, not a fault, when capturing on the sending
  host with checksum offload enabled — the NIC calculates the real
  checksum after the OS hands the packet to the driver, so Wireshark sees
  a placeholder value. Validate checksums using a capture taken further
  along the path (a TAP or a different host's NIC) instead of the sender's
  own loopback-adjacent capture point.
- **ARP requests with no replies.** Confirm the target IP is actually
  present and answering ARP on that segment (`arping` or a similar tool);
  persistent unanswered ARP for a known-live host suggests a segment
  mismatch, a down interface, or a security control (port security, ARP
  inspection) discarding the reply.
- **Fragmented traffic appears as multiple unrelated-looking IP packets.**
  Enable **Edit > Preferences > Protocols > IPv4 > Reassemble fragmented
  IPv4 datagrams** (enabled by default in 4.4.x) so Wireshark reassembles
  fragments before handing them to the transport-layer dissector; without
  reassembly, only the first fragment shows transport-layer details.
- **Traceroute capture shows gaps in the hop ladder.** A missing Time
  Exceeded response from one hop is often rate limiting or ICMP
  filtering at that specific hop, not a path failure — confirm by checking
  whether later hops still respond.
- **TTL values look inconsistent with the known path length.** Confirm
  which capture point produced the trace; TTL reflects hops *between the
  sender and the capture point*, not the sender's original value, once any
  router has forwarded the packet.

## Security and Best Practices

- **Baseline normal ARP behavior per segment** (Implementation and
  Automation, above) before an incident, so that a spoofing investigation
  has a known-good comparison rather than starting from zero.
- **Treat unsolicited gratuitous ARP as worth investigating, not
  automatically malicious.** VRRP/HSRP failover, DHCP lease events, and
  legitimate NIC teaming failover all generate gratuitous ARP; correlate
  with change records before escalating.
- **Watch for ICMP-based reconnaissance and tunneling signatures.** A high
  volume of ICMP Echo traffic to sequential addresses in a short window is
  host discovery (network sweep); unusually large or irregular ICMP Echo
  payloads can indicate data exfiltration over an ICMP tunnel — both are
  covered further with `tshark` scripted detection in [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md).
- **Do not disable ICMP entirely as a blanket hardening measure.** Blocking
  Type 3 Code 4 (fragmentation needed and DF set) breaks Path MTU
  Discovery for legitimate traffic; if ICMP must be restricted, permit the
  specific diagnostic types the environment depends on rather than
  dropping all ICMP.
- **Verify DSCP markings at trust boundaries.** A capture taken just inside
  and just outside a QoS trust boundary confirms whether markings are
  honored, remarked, or stripped as documented, rather than assuming the
  configured policy matches observed behavior.

## References and Knowledge Checks

**References**

- [Wireshark User's Guide, "Protocol Reference" appendix (Ethernet, ARP,
  IPv4, ICMPv4 dissectors).](https://www.wireshark.org/docs/wsug_html_chunked/)
- IETF [RFC 826](https://www.rfc-editor.org/rfc/rfc826) (ARP), [RFC 791](https://www.rfc-editor.org/rfc/rfc791) (IPv4), [RFC 792](https://www.rfc-editor.org/rfc/rfc792) (ICMP).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. What EtherType values identify IPv4, ARP, and 802.1Q-tagged frames, and
   which field does the dissector engine use to choose the next dissector?
2. What packet-level pattern distinguishes normal gratuitous ARP (VRRP/
   HSRP failover) from a likely ARP-spoofing attempt?
3. Why can a checksum that Wireshark reports as invalid be entirely
   correct in practice, and what capture-point change resolves the
   ambiguity?
4. Which ICMPv4 type and code combination does `traceroute`/`tracert` rely
   on to identify each intermediate hop?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each Layer-2/3 protocol in WCA-101
Domain 5.0 (identify and explain common protocols, 43%)** — Ethernet, ARP, IPv4, and
ICMPv4. Every step is a runnable `tshark` display-filter analysis. Each ends **`**Lab
verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.4** — `tshark` and a capture containing local LAN
traffic (`lan.pcapng`); the Wireshark SampleCaptures wiki has per-protocol examples.
**Cost:** none.

### Lab 4.1 — Ethernet frame analysis (Topic: Ethernet)

**Objective:** Read the Ethernet header and identify frame types.

```bash
tshark -r lan.pcapng -T fields -e eth.src -e eth.dst -e eth.type -c 20
tshark -r lan.pcapng -Y "eth.dst == ff:ff:ff:ff:ff:ff" | head    # broadcast frames
```

**Expected result:** source/destination MACs and the EtherType (0x0800 IPv4, 0x0806 ARP,
0x86dd IPv6), plus the broadcast frames — the Ethernet header's addressing and EtherType are
how the frame is delivered on the segment and demultiplexed to the right L3 protocol.

**Negative test:** assume a frame to `ff:ff:ff:ff:ff:ff` is unicast; it is a broadcast every
host on the segment processes — the destination MAC's form (unicast/multicast/broadcast)
determines the delivery scope.

**Rollback:** none (read-only).

### Lab 4.2 — ARP analysis (Topic: ARP)

**Objective:** Follow address resolution and spot ARP anomalies.

```bash
tshark -r lan.pcapng -Y "arp" -T fields -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4 | head
tshark -r lan.pcapng -Y "arp.duplicate-address-detected" | head    # Wireshark flags dup IPs
```

**Expected result:** ARP requests (opcode 1, "who has") and replies (opcode 2, "is at") map
IPs to MACs; Wireshark's `arp.duplicate-address-detected` flags two MACs claiming one IP — a
misconfiguration or ARP-spoofing signal — showing how ARP both resolves addresses and reveals
L2 attacks.

**Negative test:** ignore a burst of gratuitous ARPs re-mapping the gateway IP to a new MAC;
that is the classic ARP-spoofing man-in-the-middle pattern — ARP has no authentication, so the
capture is where you catch it.

**Rollback:** none (read-only).

### Lab 4.3 — IPv4 header and fragmentation (Topic: IPv4)

**Objective:** Read the IPv4 header and identify fragmentation.

```bash
tshark -r lan.pcapng -Y "ip" -T fields -e ip.src -e ip.dst -e ip.ttl -e ip.len -c 20
tshark -r lan.pcapng -Y "ip.flags.mf == 1 || ip.frag_offset > 0" | head   # fragments
```

**Expected result:** source/destination, TTL (hop budget / rough OS fingerprint), and total
length per packet, plus any fragments (More-Fragments flag set or non-zero offset) — the IPv4
header carries routing, lifetime, and fragmentation state that explain path and MTU behavior.

**Negative test:** blame an application for failures actually caused by fragmentation black-
holing (fragments dropped by a firewall); only the `ip.flags`/`ip.frag_offset` view reveals
it — fragmentation problems are invisible above L3.

**Rollback:** none (read-only).

### Lab 4.4 — ICMPv4 analysis (Topic: ICMPv4)

**Objective:** Interpret ICMP control messages.

```bash
tshark -r lan.pcapng -Y "icmp" -T fields -e icmp.type -e icmp.code -e ip.src -e ip.dst | head
tshark -r lan.pcapng -Y "icmp.type == 3" -T fields -e icmp.code -e ip.src   # destination unreachable
```

**Expected result:** echo request/reply (types 8/0), destination unreachable (type 3, with a
code such as 3 = port unreachable or 4 = fragmentation-needed), and TTL-exceeded (type 11) —
ICMP carries the network's error and diagnostic signaling, so these types are the network
telling you why traffic failed.

**Negative test:** overlook an ICMP type 3 code 4 (fragmentation needed, DF set) while chasing
an application timeout; that ICMP *is* the root cause (a PMTU black hole) — reading ICMP is
often the fastest path to the real fault.

**Rollback:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Ethernet, ARP, IPv4, and ICMPv4 are the layers every other protocol in this
volume rides on, and Wireshark's dissection of them turns abstract
concepts — address resolution, TTL, fragmentation, path diagnostics — into
directly observable fields. [Chapter 05](05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) extends this same bottom-up analysis
to IPv6, ICMPv6, UDP, DHCP, and DNS; [Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md) builds on the IPv4/IPv6
foundation here to analyze TCP's reliability and performance behavior in
depth.

- [ ] Can decode an Ethernet II frame's addressing and EtherType fields.
- [ ] Can read an ARP request/reply exchange and identify the signature of
      likely ARP spoofing.
- [ ] Can decode IPv4 TTL, fragmentation, DSCP, and protocol fields and
      explain their troubleshooting significance.
- [ ] Can interpret common ICMPv4 type/code combinations, including the
      mechanism behind traceroute.
- [ ] Built and applied display filters for Ethernet, ARP, IPv4, and
      ICMPv4 conditions.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
