# Chapter 05: IPv6, ICMPv6, UDP, DHCP, and DNS Analysis

![Lab flow for this chapter: a capture scoped to DHCP and DNS shows the full four-message DORA exchange in order, and a DNS query for a real domain shows a successful response code with at least one answer record. As a negative test, a query for a domain guaranteed not to exist is captured the same way; the filter for that domain matches a response with an NXDOMAIN response code, confirming the filter correctly distinguishes a failed resolution from the successful one captured moments earlier.](../../../diagrams/volume-20-wireshark-packet-analysis/chapter-05-dhcp-dns-nxdomain-flow.svg)

*Figure 5-1. Flow used throughout this chapter's Hands-On Lab: DHCP DORA and DNS resolution captured and isolated with targeted filters, tested against a deliberately unresolvable domain.*

## Learning Objectives

- Decode an IPv6 header and its extension header chain, and explain how it
  differs structurally from the IPv4 header covered in [Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md).
- Read ICMPv6 Neighbor Discovery Protocol (NDP) exchanges and map them to
  the ARP functionality they replace.
- Decode UDP's minimal header and explain why UDP-based protocol analysis
  depends entirely on the application-layer dissector above it.
- Analyze a complete DHCP DORA exchange (IPv4) and a DHCPv6 exchange, and
  identify common lease-assignment failures.
- Analyze DNS query/response traffic, including response codes, record
  types, and the conditions that force DNS onto TCP.

## Theory and Architecture

[Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md) covered the IPv4 protocol family; this chapter covers its IPv6
counterpart and the two UDP-based protocols — DHCP and DNS — every IP host
depends on before it can do useful work on the network. All four topics
share a theme: each simplifies or restructures something IPv4-era protocols
handled less elegantly, and Wireshark's dissection makes that restructuring
directly visible.

### IPv6 header structure

```text
Internet Protocol Version 6, Src: 2001:db8:20::15, Dst: 2001:db8:30::20
    Version: 6
    Traffic Class: 0x00
    Flow Label: 0x00000
    Payload Length: 40
    Next Header: TCP (6)
    Hop Limit: 64
    Source: 2001:db8:20::15
    Destination: 2001:db8:30::20
```

The IPv6 base header is fixed at 40 bytes and deliberately omits several
IPv4 fields: there is no header checksum (integrity is left to the link
layer and to upper-layer checksums), no built-in fragmentation fields
(fragmentation is instead an optional extension header, since routers no
longer fragment in transit), and `Hop Limit` replaces `TTL` with identical
semantics. `Next Header` replaces IPv4's `Protocol` field and also chains
to optional **extension headers** (Hop-by-Hop Options, Routing, Fragment,
Destination Options, and finally the transport-layer protocol), each
dissected by Wireshark as its own nested layer between the IPv6 header and
the transport header.

### ICMPv6 and Neighbor Discovery Protocol

ICMPv6 absorbs functionality that IPv4 split across ARP, IGMP, and ICMPv4.
The subset an enterprise analyst uses most is Neighbor Discovery Protocol
(NDP):

| Message | ICMPv6 Type | Role |
| --- | --- | --- |
| Router Solicitation (RS) | 133 | Host asks for router configuration on startup. |
| Router Advertisement (RA) | 134 | Router announces itself, prefixes, and whether SLAAC or DHCPv6 should be used. |
| Neighbor Solicitation (NS) | 135 | Address resolution (the direct IPv6 replacement for ARP request) and duplicate address detection. |
| Neighbor Advertisement (NA) | 136 | Address resolution reply (the IPv6 replacement for ARP reply). |
| Redirect | 137 | Router informs a host of a better next hop, equivalent to ICMPv4 Redirect. |

NS/NA replace ARP's request/reply function entirely — there is no ARP on
an IPv6-only segment. Multicast Listener Discovery (MLD), also carried over
ICMPv6, manages IPv6 multicast group membership, functionally paralleling
IGMP in IPv4.

### UDP

```text
User Datagram Protocol, Src Port: 68, Dst Port: 67
    Source Port: 68
    Destination Port: 67
    Length: 300
    Checksum: 0x8f21 [correct]
```

UDP's header carries only ports, length, and an optional checksum — no
sequencing, acknowledgment, or flow control. This means Wireshark's
transport-layer view of a UDP conversation is nearly empty of diagnostic
information by itself; nearly everything an analyst needs comes from the
application-layer dissector chained above it (DHCP, DNS, SNMP, RTP, and so
on), which is why UDP-based troubleshooting is really application-protocol
troubleshooting from the first packet.

### DHCP (and DHCPv6)

DHCP for IPv4 is the four-message DORA exchange, all on UDP ports 67
(server) and 68 (client), broadcast until an IP address is usable:

```text
DHCP Discover  (client → broadcast): "I need an address"
DHCP Offer     (server → client):    "You can have 10.0.20.100"
DHCP Request   (client → broadcast): "I'm accepting 10.0.20.100"
DHCP Ack       (server → client):    "Confirmed, lease time: 86400s"
```

DHCPv6 (UDP ports 546/547) follows an analogous but differently named
four-message exchange (Solicit, Advertise, Request, Reply), and coexists
with SLAAC — an RA's flags (the "Managed" and "Other" bits) tell hosts
whether to use DHCPv6 for addressing, only for other configuration (DNS
servers), or neither.

### DNS

DNS resolves names to addresses (and the reverse) over UDP port 53 by
default, falling back to TCP port 53 when a response exceeds the UDP
payload size the resolver advertised (via EDNS0) or when a zone transfer
(`AXFR`) is requested. Wireshark's DNS dissector exposes the query name,
type, and the full answer section, plus the response code:

| `dns.flags.rcode` value | Meaning |
| --- | --- |
| 0 | NOERROR — successful resolution |
| 2 | SERVFAIL — server-side resolution failure |
| 3 | NXDOMAIN — name does not exist |
| 5 | REFUSED — server declined to answer (commonly a policy/ACL decision) |

## Design Considerations

- **Dual-stack captures need both address families filtered together.**
  An environment running IPv4 and IPv6 concurrently can have the same
  logical conversation appear as two unrelated flows in a capture; use
  `ip.addr` and `ipv6.addr` together, or filter by hostname resolution,
  when correlating a dual-stack session.
- **NDP cache behavior differs from ARP cache behavior.** IPv6 neighbor
  cache states (reachable, stale, probe, delay) are more granular than
  IPv4's ARP cache, and NDP includes built-in Duplicate Address Detection
  (DAD) — a burst of Neighbor Solicitations for a host's own tentative
  address immediately after interface bring-up is expected DAD behavior,
  not a fault.
- **UDP protocol identification depends on port convention, not the
  transport header.** Because UDP carries no protocol-identifying field of
  its own, a UDP-based service on a non-standard port requires **Decode
  As** ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)) to dissect correctly; do not assume Wireshark's default
  protocol column reflects the true application if the port is unusual.
- **DHCP relay changes what a single-segment capture can show.** If DHCP
  traffic is relayed (`giaddr` populated, UDP port 67 unicast from a relay
  agent) across a router boundary, a capture on the client segment alone
  will not show server-side detail; correlate with a capture nearer the
  DHCP server when lease failures are suspected to originate there.
- **DNS over TCP vs. UDP affects capture filter design.** A capture filter
  or display filter written only for `udp.port==53` silently misses
  TCP-fallback DNS traffic (zone transfers, large/DNSSEC-signed
  responses); default to `dns` as a protocol-name filter, which matches
  regardless of transport.

## Implementation and Automation

### IPv6 and NDP filters

```text
ipv6.addr == 2001:db8:20::15
ipv6.nxt == 6                          # Next Header indicates TCP follows
icmpv6.type == 135                     # Neighbor Solicitation
icmpv6.type == 136                     # Neighbor Advertisement
icmpv6.type == 134                     # Router Advertisement
icmpv6.nd.ra.flags.m == 1              # RA "Managed" flag set (use DHCPv6)
```

Extract the prefixes advertised in Router Advertisements across a capture:

```bash
tshark -r capture.pcapng -Y "icmpv6.type==134" \
  -T fields -e ipv6.src -e icmpv6.opt.prefix.length -e icmpv6.opt.prefix
```

### UDP and Decode As

```text
udp.port == 53
udp.length > 512                       # unusually large UDP payload
```

Force a non-standard-port UDP service to dissect correctly:
**Analyze > Decode As**, set the UDP port and target protocol for the
current session, or persist it via
**Edit > Preferences > Protocols > <Protocol> > Ports**.

### DHCP DORA filters

```text
dhcp                                    # all DHCP traffic (IPv4)
dhcp.option.dhcp == 1                   # DHCP Discover
dhcp.option.dhcp == 2                   # DHCP Offer
dhcp.option.dhcp == 3                   # DHCP Request
dhcp.option.dhcp == 5                   # DHCP Ack
dhcp.option.dhcp == 6                   # DHCP Nak (lease rejected)
```

```bash
tshark -r capture.pcapng -Y "dhcp" -T fields \
  -e frame.time_relative -e dhcp.option.dhcp -e dhcp.option.requested_ip_address \
  -e dhcp.ip.your
```

DHCPv6 equivalents:

```text
dhcpv6.msgtype == 1     # Solicit
dhcpv6.msgtype == 2     # Advertise
dhcpv6.msgtype == 3     # Request
dhcpv6.msgtype == 7     # Reply
```

### DNS filters

```text
dns                                     # all DNS, UDP or TCP
dns.flags.response == 0                 # queries only
dns.flags.response == 1                 # responses only
dns.qry.name == "example.com"
dns.flags.rcode != 0                    # any non-success response code
dns.qry.type == 28                      # AAAA queries
dns.count.answers > 0 && dns.flags.rcode == 0   # successful answers
```

```bash
# Summarize DNS response codes across a capture.
tshark -r capture.pcapng -Y "dns.flags.response==1" -T fields -e dns.flags.rcode \
  | sort | uniq -c | sort -rn
```

## Validation and Troubleshooting

- **Client sends Router Solicitation but no Router Advertisement
  appears.** Confirm an IPv6-capable router/RA-suppressing switch feature is
  not filtering RAs (`icmpv6.type==134`), and confirm the capture point is
  on the same broadcast/multicast domain as the router.
- **DHCP client stuck repeating Discover.** Filter `dhcp.option.dhcp==1`
  and confirm no corresponding Offer arrives; this points to either no
  DHCP server/relay reachable on that segment or a scope exhausted of
  addresses (confirmed on the server side, outside what the client-segment
  capture alone can show).
- **DHCP client receives an Offer but never completes with a Request/
  Ack.** Often a second, unexpected DHCP server responding on the same
  segment (a rogue or misconfigured server); filter `dhcp.option.dhcp==2`
  and inspect `ip.src` for every Offer — more than one distinct server
  address answering the same Discover is the signature.
- **DNS query times out with no response visible in the capture.**
  Distinguish "no response sent" from "response sent but not received" by
  checking the capture point relative to the resolver; a capture taken at
  the client will not show a response that was dropped by a firewall
  between the client and the resolver.
- **Expected DNS answer missing even though `dns.flags.rcode==0`.**
  NOERROR with an empty answer section (`dns.count.answers==0`) is a valid,
  common response for a query type with no matching record (for example,
  an AAAA query for a name with only an A record) — this is not a failure,
  and should not be conflated with NXDOMAIN.

## Security and Best Practices

- **Watch for NDP spoofing analogous to ARP spoofing.** The same
  investigative approach from [Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md) — baselining IP-to-MAC mappings
  and flagging conflicting Neighbor Advertisements for the same address —
  applies to IPv6 segments; NDP has no built-in authentication any more
  than ARP does, absent RA Guard/SEND deployment.
- **Treat rogue DHCP servers as a standing risk, not a one-time
  check.** The Offer-source-address check above should be part of a
  recurring segment baseline, since a rogue server can redirect clients to
  attacker-controlled DNS and gateway addresses via a single malicious
  Offer.
- **Correlate unusual DNS query patterns with exfiltration/tunneling.**
  A high volume of long, high-entropy subdomain labels queried against a
  single domain, or an unusually high TXT/NULL record query rate, is the
  classic DNS-tunneling signature; `dns.qry.name` length and query-rate
  statistics ([Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)) are the starting filters for that investigation.
- **Confirm DNSSEC validation behavior deliberately rather than
  assuming it.** A capture showing `dns.flags.authenticated==1` (the AD
  bit) reflects the resolver's own validation, not the capturing analyst's
  independent verification — treat it as informative, not authoritative,
  without corroboration.
- **Do not disable IPv6 as a substitute for securing it.** A segment with
  IPv6 disabled at the OS level can still process router advertisements
  and NDP traffic at the link layer on unmanaged switches; confirm the
  actual traffic observed in a capture rather than relying on
  configuration intent alone.

## References and Knowledge Checks

**References**

- [Wireshark User's Guide, "Protocol Reference" appendix (IPv6, ICMPv6,
  UDP, DHCP, DHCPv6, DNS dissectors).](https://www.wireshark.org/docs/wsug_html_chunked/)
- IETF [RFC 8200](https://www.rfc-editor.org/rfc/rfc8200) (IPv6), [RFC 4861](https://www.rfc-editor.org/rfc/rfc4861) (Neighbor Discovery Protocol), [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131)
  (DHCP), [RFC 8415](https://www.rfc-editor.org/rfc/rfc8415) (DHCPv6), [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035) (DNS).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. Which two ICMPv6 message types together perform the function ARP
   performs in IPv4, and what additional function does one of them provide
   that ARP does not?
2. Why does UDP-based protocol troubleshooting depend almost entirely on
   the application-layer dissector rather than the UDP header itself?
3. What packet-level pattern in a DHCP capture indicates a rogue DHCP
   server rather than a single legitimate one?
4. Under what two conditions does DNS fall back from UDP to TCP, and why
   does a `udp.port==53`-only filter risk missing relevant traffic?

## Hands-On Lab

**Objective:** Capture and analyze a DHCP DORA exchange and a DNS
resolution sequence, including IPv6 Neighbor Discovery if a dual-stack
segment is available.

**Prerequisites**

- Wireshark and `tshark` installed with capture rights ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)).
- A network segment providing DHCP; administrative ability to release/renew
  the local DHCP lease.

**Steps**

1. Start a capture scoped to DHCP and DNS:

   ```bash
   tshark -i <INTERFACE_NUMBER> -f "udp port 67 or udp port 68 or port 53" \
     -w lab05.pcapng &
   ```

2. Force a DHCP lease renewal to generate a DORA exchange:

   ```bash
   # Linux
   sudo dhclient -r && sudo dhclient

   # macOS
   sudo ipconfig set en0 DHCP

   # Windows (PowerShell, run as Administrator)
   ipconfig /release
   ipconfig /renew
   ```

3. Generate a DNS resolution:

   ```bash
   nslookup example.com     # or: dig example.com
   ```

4. Stop the capture:

   ```bash
   kill %1
   ```

5. Open `lab05.pcapng` and confirm the full DORA exchange:

   ```text
   dhcp
   ```

   **Expected result:** four DHCP messages in order — Discover, Offer,
   Request, Ack — each from the expected source (client broadcasts,
   single consistent server address in Offer and Ack).

6. Confirm the DNS query/response pair:

   ```text
   dns.qry.name == "example.com"
   ```

   **Expected result:** one query (`dns.flags.response==0`) and one
   response (`dns.flags.response==1`) with `dns.flags.rcode==0` and at
   least one answer record.

7. **Negative test:** Query a domain guaranteed not to resolve, capturing
   the same way, and confirm the response code:

   ```bash
   nslookup this-domain-should-not-exist-lab05.invalid
   ```

   ```text
   dns.qry.name contains "lab05" && dns.flags.rcode == 3
   ```

   **Expected result:** the response matches with `rcode==3` (NXDOMAIN),
   confirming the filter correctly distinguishes a failed resolution from
   the successful one captured in step 6.

8. **Cleanup:** Remove the lab capture:

   ```bash
   rm -f lab05.pcapng
   ```

## Summary and Completion Checklist

IPv6 restructures IPv4's header into a leaner base header plus optional
extension headers, ICMPv6/NDP absorbs ARP's function along with built-in
duplicate address detection, and both DHCP and DNS remain the two UDP-based
protocols every host depends on before any application traffic can flow.
Because UDP itself carries almost no diagnostic information, effective
analysis of DHCP and DNS traffic is really analysis of their
application-layer dissectors from the first captured packet. [Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md)
turns to TCP, where the transport header itself — not just the protocol
riding on it — is the primary object of analysis.

- [ ] Can decode an IPv6 header and identify chained extension headers.
- [ ] Can read an NDP Neighbor Solicitation/Advertisement exchange and
      relate it to ARP's function.
- [ ] Can explain why UDP-based troubleshooting depends on the
      application-layer dissector.
- [ ] Can identify all four messages of a DHCP DORA exchange and recognize
      a rogue-server signature.
- [ ] Can interpret DNS response codes and explain when DNS falls back to
      TCP.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
