# Volume XX Glossary

Definitions for terms introduced in **Volume XX — Wireshark and Packet
Analysis**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Aggregating TAP** — A Test Access Point that merges the transmit and
receive directions of a full-duplex link onto a single monitor output,
which can silently drop packets once combined bidirectional utilization
exceeds the monitor port's capacity. Introduced in Chapter 02.

**ARP (Address Resolution Protocol)** — The protocol that resolves an
IPv4 address to a MAC address on the local segment via a broadcast
request and a unicast reply; it never crosses a Layer 3 boundary.
Introduced in Chapter 04.

**Bandwidth-delay product** — The amount of data that can be in flight on
a network path at once, computed as bandwidth multiplied by round-trip
time; a TCP window smaller than this value limits throughput even absent
packet loss. Introduced in Chapter 06.

**BPF (Berkeley Packet Filter)** — The filter syntax used by capture
filters and by `tcpdump`, applied by `dumpcap` before a packet is written
to disk, permanently discarding non-matching traffic. Introduced in
Chapter 02.

**Capture filter** — A BPF expression applied at capture time that
determines which packets are ever written to a capture file, distinct
from a display filter applied afterward. Introduced in Chapter 02.

**`capinfos`** — A Wireshark command-line utility that reports capture
file metadata: packet count, duration, encapsulation type, and file
hashes. Introduced in Chapter 01.

**Chain of custody** — Documented, unbroken control over a packet capture
from collection through analysis, required when a capture may support an
incident record, personnel action, or legal proceeding. Introduced in
Chapter 01.

**Coloring rule** — A named filter-and-color pair that visually highlights
matching packets in the packet list without hiding non-matching packets,
evaluated top-down by priority order. Introduced in Chapter 03.

**Configuration profile** — A named, switchable set of Wireshark
preferences (columns, coloring rules, saved filters, protocol
preferences) isolated from other profiles, letting one installation serve
multiple analysis roles. Introduced in Chapter 03.

**Decode As** — The Wireshark feature that forces a specific dissector
onto traffic on a non-standard port or encapsulation, without changing
the dissector's global default. Introduced in Chapter 03.

**DHCP DORA** — The four-message DHCPv4 lease exchange: Discover, Offer,
Request, Acknowledge. Introduced in Chapter 05.

**Display filter** — A Wireshark expression language, distinct from BPF,
evaluated against already-dissected packets to control what is shown; it
never discards data from the underlying file. Introduced in Chapter 03.

**Dissector** — A component of Wireshark's `epan` engine that parses a
specific protocol's bytes into the protocol tree shown in the Packet
Detail pane, chained to the next dissector by port, EtherType, or
heuristic. Introduced in Chapter 01.

**`dumpcap`** — The minimal, privileged capture process shared by
Wireshark and `tshark`; it writes raw packets and performs no protocol
dissection. Introduced in Chapter 01.

**`editcap`** — A Wireshark command-line utility that splits, filters,
deduplicates, time-shifts, or truncates packets in a capture file without
a live capture. Introduced in Chapter 08.

**Expert analysis flags** — Wireshark's built-in per-stream anomaly
detection (`tcp.analysis.*` fields) that flags retransmissions, duplicate
ACKs, out-of-order segments, and zero-window conditions. Introduced in
Chapter 06.

**Follow Stream** — A Wireshark feature that reassembles a full
bidirectional TCP, UDP, or TLS conversation into a readable view and
generates the corresponding stream-index filter. Introduced in Chapter
03.

**Fragment offset** — The IPv4 header field indicating a fragment's
position within the original datagram, used together with the More
Fragments flag to identify and reassemble fragmented traffic. Introduced
in Chapter 04.

**Gratuitous ARP** — An unprompted ARP request or reply announcing a
host's own IP-to-MAC mapping, normal after interface bring-up or
failover, but a possible spoofing signal when conflicting. Introduced in
Chapter 04.

**HTTP/2 framing** — HTTP/2's binary, stream-multiplexed structure
(`HEADERS`, `DATA`, `SETTINGS` frames tagged by stream ID) that replaces
HTTP/1.1's one-request-per-connection-segment model. Introduced in
Chapter 07.

**`http.time`** — A Wireshark-computed field measuring elapsed time
between a matched HTTP request and its response. Introduced in Chapter
07.

**ICMPv4** — Internet Control Message Protocol for IPv4, carrying both
diagnostic traffic (echo request/reply) and automatic error reporting
(destination unreachable, time exceeded). Introduced in Chapter 04.

**ICMPv6** — The IPv6 control-message protocol that also carries Neighbor
Discovery Protocol and Multicast Listener Discovery, absorbing
functionality IPv4 splits across ARP, IGMP, and ICMPv4. Introduced in
Chapter 05.

**Neighbor Discovery Protocol (NDP)** — The ICMPv6-carried set of
messages (Router/Neighbor Solicitation and Advertisement) that perform
IPv6 address resolution and router discovery, replacing ARP. Introduced
in Chapter 05.

**Network packet broker (NPB)** — A device that aggregates, deduplicates,
filters, and distributes traffic from multiple TAPs or SPAN ports to
multiple analysis tools; Gigamon GigaVUE is a common example (Volume
XVIII). Introduced in Chapter 02.

**Npcap** — The Windows packet capture driver bundled with Wireshark's
Windows installer, replacing the older WinPcap. Introduced in Chapter 01.

**pcapng** — Wireshark's default block-structured capture file format,
supporting multiple interfaces, name resolution, and embedded decryption
secrets per file, unlike legacy pcap. Introduced in Chapter 01.

**Port scan signature** — The packet-level pattern of one source
generating unanswered SYN packets to many distinct destination ports in a
short window. Introduced in Chapter 08.

**Protocol Hierarchy** — A Wireshark statistics view summarizing the
proportion of a capture occupied by each protocol, typically the first
view used when triaging an unfamiliar capture. Introduced in Chapter 03.

**Regeneration TAP** — A passive Test Access Point that duplicates each
direction of a full-duplex link to its own separate monitor port, without
merging them. Introduced in Chapter 02.

**Ring buffer** — A `dumpcap` capture mode that rotates through a fixed
set of files by size or duration, deleting the oldest file once the set
is full, bounding total disk usage for continuous capture. Introduced in
Chapter 02.

**Rogue DHCP server** — An unauthorized or misconfigured device answering
DHCP Discover messages, identified by more than one distinct source
address issuing Offers on the same segment. Introduced in Chapter 05.

**`rpcapd`** — The remote packet capture daemon that exposes a network
interface for direct remote capture from a Wireshark GUI's Capture
Options dialog. Introduced in Chapter 02.

**SNI (Server Name Indication)** — A TLS Client Hello extension carrying
the requested hostname, typically visible even in an otherwise fully
encrypted TLS session absent Encrypted Client Hello deployment.
Introduced in Chapter 07.

**SPAN / mirror port** — A switch feature that copies frames from one or
more source ports or VLANs to a destination port for monitoring, at
lowest switching priority and thus subject to silent drops under load.
Introduced in Chapter 02.

**`SSLKEYLOGFILE`** — An environment variable that instructs a
TLS-capable client to log per-session decryption secrets as connections
are made, which Wireshark can then use to decrypt the matching capture.
Introduced in Chapter 07.

**SYN flood signature** — The packet-level pattern of many distinct
sources generating half-open TCP connections to one destination.
Introduced in Chapter 08.

**TAP (Test Access Point)** — A physical inline device that splits a
link's signal to deliver a full-fidelity copy, including Layer 1 errors,
to one or more monitor ports. Introduced in Chapter 02.

**TCP window scaling** — A negotiated TCP option that multiplies the
16-bit window field by a power of two, allowing effective windows large
enough to fill high-bandwidth, high-latency paths. Introduced in Chapter
06.

**TCP zero window** — A condition where a receiver advertises a receive
window of zero, telling the sender to pause transmission, typically
indicating the receiving application is not draining its socket buffer
fast enough. Introduced in Chapter 06.

**TLS 1.3 one-round-trip handshake** — TLS 1.3's reduced handshake, in
which the client sends its key share in the initial Client Hello,
allowing application data after a single round trip instead of TLS 1.2's
two. Introduced in Chapter 07.

**Traceroute mechanism** — The technique of sending probes with
successively incrementing TTL/Hop Limit values and reading the resulting
ICMP Time Exceeded responses to map each intermediate hop. Introduced in
Chapter 04.

**`tshark`** — Wireshark's command-line sibling, built from the same
`epan` dissection engine, supporting capture filters, display filters,
and structured field extraction for scripted analysis. Introduced in
Chapter 01.

**VLAN tagging (802.1Q)** — A 4-byte tag inserted into an Ethernet frame
identifying its VLAN membership and priority, which some switch platforms
strip when mirroring traffic from an access port. Introduced in Chapter
04.

**WCA-101** — The Wireshark Certified Analyst Program's foundational
packet-analysis credential this volume is aligned to; always confirm the
current blueprint directly with the certifying program. Introduced in
Chapter 09.

**Window Scale option** — The TCP option, negotiated only in the SYN/
SYN-ACK exchange and never renegotiable mid-connection, that enables TCP
window scaling. Introduced in Chapter 06.
