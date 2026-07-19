# Chapter 1: Network Models and Protocol Architecture

![Lab flow for this chapter: the lab host runs tcpdump scoped to tcp port 80 or 443 while curl issues an HTTP GET to example.com (93.184.216.34:80); the capture is decoded with tshark -V, showing Frame, Ethernet II, IPv4, TCP, and HTTP sections in order, and a separate filter isolates the three-frame TCP handshake (SYN, SYN-ACK, ACK); a scapy-built IP()/TCP() packet is shown to match the same layer order. As a negative test, repeating the capture with an unused filter (tcp port 8443) yields zero matching packets, since an incorrect Layer 4 filter value silently discards traffic rather than erroring.](../../../diagrams/volume-02-network-engineering-foundations/chapter-01-packet-capture-osi-layer-decode-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: capturing, decoding, and constructing packets to confirm that theoretical OSI-layer encapsulation matches what appears on the wire.*

## Learning Objectives

- Explain why layered reference models exist and how they simplify design,
  interoperability, and troubleshooting across vendors.
- Map the seven OSI layers to their function and compare the OSI model against
  the four-layer TCP/IP model used by real-world networks.
- Trace encapsulation and de-encapsulation for a unicast IP packet from the
  application down to the physical medium and back up at the receiver.
- Identify the protocol data unit (PDU) name, addressing scheme, and key
  header fields carried at each layer.
- Distinguish connection-oriented from connectionless transport semantics and
  choose correctly between TCP and UDP for a given application behavior.
- Describe the role of standards bodies (IETF, IEEE, ISO/IEC, IANA) in
  producing the interoperable specifications that enterprise networks depend
  on.
- Use a packet capture to verify that observed traffic matches the layered
  model in theory.

## Theory and Architecture

### Why Layered Models Exist

Every enterprise network is an assembly of components built by different
vendors, running different software, on different physical media, that must
still interoperate predictably. Layering solves this by dividing the problem
of "get data from one application to another across a network" into
independent, stackable responsibilities. Each layer exposes a defined service
to the layer above it and consumes a defined service from the layer below it,
without needing to know how that service is implemented. A Layer 3 routing
process does not need to know whether the underlying medium is copper,
fiber, or a wireless channel; it only needs a Layer 2 service that can
deliver a frame to the next hop.

This separation of concerns delivers three practical benefits an engineer
relies on daily:

- **Interoperability.** Vendors can implement a single layer (for example, a
  Layer 2 switching ASIC) to a public specification and interoperate with any
  other vendor's implementation of the adjacent layer.
- **Isolated troubleshooting.** A fault can be localized to a layer (a bad
  cable is Layer 1; a VLAN mismatch is Layer 2; an unreachable subnet is
  Layer 3) instead of requiring the engineer to reason about the entire
  stack simultaneously.
- **Independent evolution.** Layer 1 media has evolved from coaxial cable to
  single-mode fiber to Wi-Fi 6E without requiring a rewrite of Layer 3 and
  above.

### The OSI Reference Model

The Open Systems Interconnection (OSI) model, published by ISO/IEC as
ISO/IEC 7498-1, defines seven layers. It is a conceptual and teaching model
more than an implementation blueprint, but its vocabulary — "Layer 2 issue,"
"Layer 7 firewall" — is the shared language of network operations.

| Layer | Name | Primary Responsibility | Example Units/Protocols |
| --- | --- | --- | --- |
| 7 | Application | Provides network services directly to end-user processes | HTTP, DNS, SMTP, SSH |
| 6 | Presentation | Data formatting, encryption, compression, character encoding | TLS record formatting, MIME, ASN.1 |
| 5 | Session | Establishes, manages, and tears down sessions between hosts | Session tokens, NetBIOS sessions, RPC |
| 4 | Transport | End-to-end delivery, segmentation, flow control, error recovery | TCP, UDP, QUIC |
| 3 | Network | Logical addressing and routing between networks | IPv4, IPv6, ICMP |
| 2 | Data Link | Framing, physical addressing, and media access within a segment | Ethernet, 802.11 MAC, ARP, VLAN tagging |
| 1 | Physical | Bit transmission over a physical medium | Copper, fiber, RF, connectors, line coding |

### The TCP/IP (DoD) Model

Real-world protocol suites are built on the TCP/IP model, a four-layer
architecture defined implicitly by the IETF's RFC series rather than a single
formal document. It predates OSI and is what actually ships in every
operating system's network stack.

| TCP/IP Layer | Rough OSI Equivalent | Function |
| --- | --- | --- |
| Application | Layers 5–7 | Application protocols and their session/formatting semantics |
| Transport | Layer 4 | End-to-end process-to-process delivery |
| Internet | Layer 3 | Logical addressing and routing (IP) |
| Link (Network Access) | Layers 1–2 | Framing and delivery on the local network segment |

### Mapping OSI to TCP/IP

The mapping is not a strict one-to-one correspondence, and engineers should
resist forcing it. TCP/IP's Application layer absorbs OSI's Session and
Presentation responsibilities into the application protocol itself — TLS,
for example, performs Presentation-layer encryption but is implemented and
discussed as part of the application stack, sitting logically between
Transport and Application. In practice, engineers use OSI layer numbers as
shorthand for scope of impact ("that's a Layer 4 problem") while the packets
on the wire follow the TCP/IP structure.

### Encapsulation and De-encapsulation

Data moving down the stack on a sending host is wrapped with a new header
(and sometimes a trailer) at every layer — a process called encapsulation.
Each layer treats everything handed to it by the layer above as an opaque
payload.

```text
Application data
  -> [TCP header | Application data]                      Segment
    -> [IP header | TCP header | Application data]         Packet
      -> [Ethernet header | IP header | ... | FCS]          Frame
        -> 0101100101011... on the wire                     Bits
```

On the receiving host, the reverse process — de-encapsulation — strips each
header as the frame moves up the stack, with each layer using its header
fields to decide how to hand the remaining payload to the layer above (for
example, the Ethernet EtherType field indicates IPv4 vs IPv6; the IP Protocol
field indicates TCP vs UDP; the TCP/UDP port number indicates the receiving
application).

### Protocol Data Units and Addressing at Each Layer

| Layer | PDU Name | Addressing | Header Highlights |
| --- | --- | --- | --- |
| Transport | Segment (TCP) / Datagram (UDP) | Port numbers | Source/destination port, sequence number (TCP), checksum |
| Network | Packet | IP address | Source/destination IP, TTL/Hop Limit, protocol number |
| Data Link | Frame | MAC address | Source/destination MAC, EtherType, Frame Check Sequence |
| Physical | Bit | N/A | Encoding, symbol rate, signal levels |

### Standards Bodies and RFC Process

Enterprise interoperability depends on open, versioned specifications:

- **IETF (Internet Engineering Task Force)** publishes Requests for Comments
  (RFCs) that define Internet and TCP/IP protocols — [RFC 791](https://www.rfc-editor.org/rfc/rfc791) (IPv4),
  [RFC 8200](https://www.rfc-editor.org/rfc/rfc8200) (IPv6), [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293) (TCP), [RFC 768](https://www.rfc-editor.org/rfc/rfc768) (UDP). RFCs progress through
  Internet-Draft, Proposed Standard, and Internet Standard maturity levels.
- **IEEE 802** working groups define Layer 1/2 standards for LANs, including
  802.3 (Ethernet) and 802.11 (wireless LAN).
- **ISO/IEC** publishes the OSI model itself and other cross-industry data
  communication standards.
- **IANA (Internet Assigned Numbers Authority)** allocates and registers the
  numbering spaces protocols depend on: IP address blocks, AS numbers, TCP/UDP
  port numbers, and protocol/EtherType values.

## Design Considerations

- **Encapsulation overhead and MTU.** Every layer adds header bytes. A
  standard Ethernet MTU of 1500 bytes leaves roughly 1460 bytes for TCP
  payload once IPv4 (20 bytes) and TCP (20 bytes) headers are subtracted;
  tunnel overlays (VXLAN, IPsec, GRE) subtract further and must be accounted
  for when sizing end-host MTU to avoid fragmentation or black-holed traffic.
- **Connection-oriented vs. connectionless transport.** TCP provides
  ordered, reliable, flow-controlled delivery at the cost of handshake
  latency and per-connection state; UDP provides minimal-overhead,
  unordered, best-effort delivery suited to latency-sensitive or
  application-managed-reliability traffic (VoIP, DNS, telemetry). Design
  decisions — load balancer algorithm, firewall statefulness, QoS
  classification — must match the transport the application actually uses.
- **Where to enforce policy.** Layered thinking should drive where a control
  is placed: broadcast/collision domain containment is a Layer 2 decision,
  reachability and route summarization are Layer 3 decisions, and
  application-aware inspection belongs at Layer 4–7. Placing a control at
  the wrong layer (for example, trying to solve a routing loop with an
  access-layer VLAN change) wastes operational effort.
- **Protocol selection for new services.** When onboarding a new
  application, confirm which transport and application-layer protocols it
  uses before it reaches production; this determines firewall rules, load
  balancer health checks, and capacity planning assumptions.

## Implementation and Automation

Vendor CLI syntax differs, but every enterprise network operating system
exposes the layered model through its interface and protocol status
commands. The following examples use a vendor-neutral pseudo-CLI
(`device#`) modeled on conventions shared across enterprise platforms;
vendor-specific syntax is covered in later volumes.

```text
device# show interface ethernet1/1
Ethernet1/1 is up, line protocol is up
  Hardware is 10GBase-SR, address is 0050.56aa.1122
  MTU 1500 bytes, BW 10000000 Kbit, full-duplex
  Encapsulation ARPA
```

Inspecting the layered stack directly with packet-capture tooling makes the
model concrete. `tcpdump` and `tshark` decode each header in order:

```bash
# Capture 10 packets on interface eth0, show layer-by-layer decode
sudo tcpdump -i eth0 -c 10 -nnvvXX
```

```bash
# tshark: print a compact per-layer summary for HTTP traffic
tshark -i eth0 -f "tcp port 80" -T fields \
  -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport
```

Automation and test tooling frequently need to build or inspect packets
programmatically rather than through a live NIC. Python's `scapy` library
mirrors the layered model directly in code — each protocol layer is a
composable Python object:

```python
from scapy.all import IP, TCP, Raw, send

# Construct a packet by stacking layers, exactly as encapsulation stacks headers
packet = (
    IP(src="10.0.0.10", dst="10.0.0.20")
    / TCP(sport=51000, dport=443, flags="S")
    / Raw(load=b"")
)
packet.show()   # Print the fully decoded layer stack before sending
send(packet, verbose=False)
```

Running `packet.show()` prints the Ethernet/IP/TCP layers exactly as they
will appear on the wire, which is a fast way to teach or verify encapsulation
order in an automation pipeline or CI-driven network test.

## Validation and Troubleshooting

Layered thinking gives troubleshooting a repeatable order of operations:
verify Layer 1, then Layer 2, then Layer 3, then Layer 4 and above, before
assuming an application defect.

| Symptom | Likely Layer | First Diagnostic Command |
| --- | --- | --- |
| Interface down/no link light | 1 | `show interface status` |
| Host on same subnet unreachable, interface up | 2 | `show mac address-table`, `arp -a` |
| Host on same subnet reachable, remote subnet unreachable | 3 | `traceroute`, `show ip route` |
| Host reachable by ping, application fails to connect | 4 | `ss -tan`, `telnet <host> <port>` |
| Connection opens but application errors | 5–7 | Application logs, `tshark` decode |

```bash
# Layer 3 reachability and path
ping -c 4 10.0.0.20
traceroute 10.0.0.20

# Layer 4 — confirm the TCP three-way handshake completes
sudo tcpdump -i eth0 -nn 'tcp port 443 and host 10.0.0.20'
```

A clean TCP handshake capture shows `[S]`, `[S.]`, `[.]` flags in sequence;
a repeating `[S]` with no `[S.]` response indicates the packet is not
reaching the destination stack (Layer 3 routing, an ACL, or a firewall
policy) rather than an application fault — a diagnosis that layered
reasoning reaches in seconds instead of by guesswork.

## Security and Best Practices

- Apply defense-in-depth mapped explicitly to layers: port security and
  802.1X at Layer 2, router ACLs and unicast reverse-path forwarding at
  Layer 3, stateful firewall policy at Layer 4, and application-aware
  inspection, WAF, or API gateways at Layer 7. A single layer of control is
  insufficient because compromise paths rarely respect layer boundaries.
- Disable or restrict protocols that are not in active use at each layer
  (unused VLANs, unnecessary routing protocols, legacy TLS versions) to
  shrink the attack surface described by the model.
- Treat protocol header fields as untrusted input from the network's
  perspective; validate assumptions (expected EtherType, expected IP
  protocol, expected port) explicitly in firewall and ACL policy rather than
  relying on default-permit behavior.
- When capturing traffic for troubleshooting, scope captures with explicit
  filters and time limits, and treat capture files as sensitive data — they
  can contain credentials or personal data in cleartext protocols.

## References and Knowledge Checks

**References**

- [RFC 791 — Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [RFC 8200 — Internet Protocol, Version 6 (IPv6) Specification](https://www.rfc-editor.org/rfc/rfc8200)
- [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293)
- [RFC 768 — User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768)
- [IEEE 802.3 Ethernet Standard](https://standards.ieee.org/ieee/802.3/7071/)
- [ISO/IEC 7498-1 — OSI Basic Reference Model](https://www.iso.org/standard/20269.html)
- [IANA Protocol Numbers Registry](https://www.iana.org/assignments/protocol-numbers/)

**Knowledge Checks**

1. Why does the TCP/IP model collapse OSI Layers 5–7 into a single
   Application layer, and what does this mean for how TLS is described?
2. Walk through the encapsulation of an HTTPS request from the browser to
   the wire, naming the PDU at each layer.
3. A host can ping its default gateway but not a remote subnet. Which
   layers are confirmed working, and where should troubleshooting focus
   next?
4. Why does a VXLAN overlay reduce the usable MTU for encapsulated traffic,
   and what happens if that is not accounted for?
5. Give two enterprise use cases where UDP is the correct transport choice
   over TCP, and justify each.
6. Which standards body is responsible for allocating TCP/UDP port numbers,
   and why does that matter when onboarding a new application?

## Hands-On Lab

**Objective.** Capture, decode, and construct packets to observe the
layered model directly, confirming that theoretical encapsulation matches
what appears on the wire.

**Prerequisites**

- A Linux host or VM with `sudo` access (any current distribution).
- `python3`, `pip`, `tcpdump`, and `tshark`/Wireshark CLI tools installed.
- Outbound network access for the `curl` step (a local web server also
  works if the lab environment is offline).

**Lab Steps**

1. Install the lab dependencies:

   ```bash
   sudo apt-get update && sudo apt-get install -y tcpdump tshark python3-pip
   python3 -m venv ~/netlab-venv
   source ~/netlab-venv/bin/activate
   pip install scapy
   ```

2. Start a background capture scoped to HTTP/HTTPS traffic on the primary
   interface (replace `eth0` with the lab host's interface name from
   `ip link`):

   ```bash
   sudo tcpdump -i eth0 -w /tmp/model-lab.pcap 'tcp port 80 or tcp port 443' &
   TCPDUMP_PID=$!
   sleep 2
   ```

3. Generate traffic to capture:

   ```bash
   curl -s -o /dev/null -w "HTTP status: %{http_code}\n" http://example.com
   sleep 2
   sudo kill "$TCPDUMP_PID"
   ```

4. Decode the capture layer by layer and confirm the expected header
   fields are present:

   ```bash
   tshark -r /tmp/model-lab.pcap -V -c 1 | less
   ```

   **Expected result:** the decode shows, in order, a Frame section, an
   Ethernet II section (source/destination MAC, EtherType `0x0800`), an
   Internet Protocol Version 4 section (source/destination IP, protocol
   `TCP (6)`), a Transmission Control Protocol section (source/destination
   port, sequence number, flags), and — for the HTTP request — a Hypertext
   Transfer Protocol section.

5. Confirm the TCP three-way handshake is visible as three distinct frames:

   ```bash
   tshark -r /tmp/model-lab.pcap -Y "tcp.flags.syn==1 or tcp.flags.fin==1" \
     -T fields -e frame.number -e tcp.flags -e tcp.seq -e tcp.ack
   ```

   **Expected result:** the first matching frame shows the `SYN` flag only;
   a subsequent frame from the server shows `SYN, ACK`; and the following
   frame from the client shows `ACK` only, completing the handshake.

6. Build and inspect a packet programmatically with `scapy` to compare the
   constructed layer stack against the captured one:

   ```bash
   python3 - <<'PYEOF'
   from scapy.all import IP, TCP, Raw

   packet = IP(dst="93.184.216.34") / TCP(dport=80, flags="S") / Raw(load=b"")
   packet.show()
   PYEOF
   ```

   **Expected result:** the printed layer stack shows `###[ IP ]###`
   followed by `###[ TCP ]###`, matching the header order observed in the
   `tshark` decode from step 4.

**Negative Test**

Repeat step 2 with an intentionally wrong filter (`'tcp port 8443'`, a port
nothing in the lab uses) and re-run the `curl` step. Confirm the resulting
`.pcap` file is empty of matching packets (`tshark -r` returns no records),
demonstrating that a capture filter operates at the same header-field level
described in this chapter — an incorrect Layer 4 filter value silently
discards all matching traffic rather than producing an error.

**Cleanup**

```bash
rm -f /tmp/model-lab.pcap
deactivate
rm -rf ~/netlab-venv
```

## Summary and Completion Checklist

This chapter established the layered vocabulary that the rest of the volume
builds on: the seven-layer OSI model as the shared troubleshooting language,
the four-layer TCP/IP model as what actually runs on the wire, and
encapsulation as the mechanical process that turns application data into
bits on a medium. Packet captures were used to confirm that the model is
observable, not just theoretical, and layer-based reasoning was applied to
both troubleshooting order of operations and security control placement.

**Completion Checklist**

- [ ] Can explain the difference between the OSI and TCP/IP models without
      forcing a strict layer-for-layer mapping.
- [ ] Can name the PDU, addressing scheme, and key header fields at Layers
      1 through 4.
- [ ] Can trace encapsulation and de-encapsulation for a sample packet from
      memory.
- [ ] Captured and decoded live traffic, confirming the theoretical header
      order against a real `tshark` decode.
- [ ] Constructed a packet with `scapy` and matched its layer stack to a
      captured packet.
- [ ] Can map at least one security control to each of Layers 2, 3, 4, and
      7.
