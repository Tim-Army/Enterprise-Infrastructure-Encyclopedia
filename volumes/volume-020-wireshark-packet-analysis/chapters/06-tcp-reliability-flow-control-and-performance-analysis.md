# Chapter 06: TCP Reliability, Flow Control, and Performance Analysis

![Lab flow for this chapter: a file transfer's handshake shows Window Scale and SACK Permitted options, TCP Stream Graphs plot RTT and throughput for the transfer, and a retransmission filter records a baseline count. As a negative test, artificial packet loss is introduced on the capture interface and the transfer repeated; the same retransmission filter now shows a nonzero count in the new capture, contrasted directly against the loss-free baseline, confirming Wireshark's expert-flag analysis correctly detects retransmissions caused by genuinely induced loss.](../../../diagrams/volume-020-wireshark-packet-analysis/chapter-06-tcp-retransmission-induced-loss-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: TCP handshake options, RTT, and throughput analyzed on a real transfer, then contrasted against a transfer with deliberately induced packet loss.*

## Learning Objectives

- Decode the TCP header and explain how sequence numbers, acknowledgment
  numbers, and flags implement reliable, ordered delivery.
- Read a TCP three-way handshake and a connection teardown, and identify a
  handshake that fails or never completes.
- Use Wireshark's TCP analysis expert flags to identify retransmissions,
  duplicate ACKs, fast retransmits, and zero-window conditions.
- Explain window scaling and its effect on achievable throughput on
  high-bandwidth, high-latency paths.
- Build a round-trip-time and throughput picture of a TCP conversation
  using Wireshark's graphing tools and `tshark` field extraction.

## Theory and Architecture

Where Chapters 04 and 05 covered IPv4/IPv6 and their directly-attached
protocols, this chapter treats TCP itself as the primary object of
analysis. TCP is the protocol most enterprise performance investigations
ultimately come back to, because it is the layer responsible for turning an
imperfect network (loss, reordering, variable latency) into a reliable
byte stream — and its own mechanisms for doing that are exactly what an
analyst reads to diagnose why an application feels slow.

### TCP header and the three-way handshake

```text
Transmission Control Protocol, Src Port: 51234, Dst Port: 443, Seq: 0, Ack: 0, Len: 0
    Source Port: 51234
    Destination Port: 443
    Sequence Number: 0    (relative)
    Acknowledgment Number: 0
    Header Length: 40 bytes
    Flags: 0x002 (SYN)
    Window: 65535
    Checksum: [validation disabled]
    Options: (Maximum segment size, SACK permitted, Timestamps, No-Operation, Window scale)
```

Wireshark displays sequence and acknowledgment numbers **relative to the
start of each captured stream by default** (`tcp.seq` shown as an offset
from 0), which is far more readable than raw 32-bit values; the absolute
values remain available via
**Edit > Preferences > Protocols > TCP > Relative sequence numbers**
(uncheck to see raw values) when working from a partial capture that lacks
the initial SYN.

The three-way handshake establishes a connection and negotiates options
both ends will use for its lifetime:

```text
1. Client → Server:  SYN                Seq=0
2. Server → Client:  SYN, ACK           Seq=0, Ack=1
3. Client → Server:  ACK                Seq=1, Ack=1
```

Options negotiated in the SYN/SYN-ACK — Maximum Segment Size (MSS), Window
Scale, SACK Permitted, and Timestamps — are visible in the Packet Detail
pane under each handshake packet's Options node and are frequently the
first thing to check in a performance investigation, since a mismatch or
absence (for example, one side not offering Window Scale) caps performance
for the entire connection.

### Flags and connection teardown

| Flag | Meaning |
| --- | --- |
| SYN | Synchronize — connection establishment |
| ACK | Acknowledgment field is valid |
| FIN | Sender has finished sending data (graceful close) |
| RST | Abrupt termination — no further communication expected |
| PSH | Push buffered data to the application immediately |
| URG | Urgent pointer field is valid (rarely used in modern traffic) |

A graceful close is a four-step exchange (FIN/ACK from each side,
sometimes combined), while an RST tears the connection down immediately
without acknowledgment of prior data — an RST appearing where a FIN was
expected is itself a diagnostic signal (an application crash, a firewall
reset, or a deliberate abort).

### Reliability and Wireshark's TCP analysis expert flags

TCP guarantees ordered, complete delivery using sequence numbers (each byte
sent is numbered) and acknowledgment numbers (each ACK states the next
expected byte). Wireshark's `epan` dissector tracks every TCP stream's
sequence space and flags anomalies with a built-in expert-analysis layer,
visible both as colored packets (with the default coloring rules) and as
`tcp.analysis.*` fields:

| Expert flag | `tcp.analysis` field | Meaning |
| --- | --- | --- |
| Retransmission | `tcp.analysis.retransmission` | A segment was resent because its ACK was not seen within the sender's retransmission timeout. |
| Fast Retransmission | `tcp.analysis.fast_retransmission` | A segment was resent after three duplicate ACKs, faster than waiting for a timeout. |
| Duplicate ACK | `tcp.analysis.duplicate_ack` | The receiver re-acknowledged the same byte, signaling a gap in received data. |
| Out-of-Order | `tcp.analysis.out_of_order` | A segment arrived with a sequence number lower than one already seen, indicating reordering. |
| Zero Window | `tcp.analysis.zero_window` | The receiver advertised a receive window of 0, telling the sender to stop sending until the window reopens. |
| Window Update / Window Full | `tcp.analysis.window_update` | The sender has filled the receiver's advertised window and is waiting for it to grow. |

A single retransmission is normal on any real network; a *pattern* of
retransmissions concentrated at one point in a stream, or a rising rate
over the connection's life, is what separates ordinary loss from a genuine
performance problem worth escalating.

### Window scaling and the bandwidth-delay product

TCP's original 16-bit window field caps the unacknowledged data a sender
can have in flight at 65,535 bytes — far too small for high-bandwidth,
high-latency (long fat network) paths. The Window Scale option (negotiated
in the SYN/SYN-ACK, never renegotiable mid-connection) multiplies the
window field by a power of two, allowing effective windows up to roughly 1
GB. The bandwidth-delay product — the amount of data that can be "in
flight" on a path — sets the minimum window needed to keep a link full:

```text
Bandwidth-Delay Product (bytes) = Bandwidth (bytes/sec) × RTT (sec)
```

A connection whose advertised window is smaller than the path's
bandwidth-delay product is window-limited: the sender is idle waiting for
ACKs even though neither the network nor the application is otherwise
constrained — a common, easily misdiagnosed cause of "slow" transfers on
long-distance or satellite links.

## Design Considerations

- **Single-ended vs. dual-ended capture changes what can be distinguished.**
  A capture taken only at the client cannot by itself distinguish "the
  network dropped this segment" from "the capture point itself dropped it"
  ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)); a simultaneous capture at both ends, correlated by
  timestamp, is the only way to conclusively localize loss to a specific
  segment of the path.
- **Retransmission rate is a relative, not absolute, metric.** Baseline a
  connection type's normal retransmission rate for the environment before
  treating any nonzero rate as anomalous; a bulk transfer across a WAN
  link legitimately retransmits more than an application call on a local
  segment.
- **Zero-window conditions point at the receiver, not the network.** A
  sustained zero window indicates the receiving application is not
  draining its socket buffer fast enough (CPU starvation, disk I/O
  backpressure, or an application-level stall) — investigate the receiving
  host, not the path, when this pattern dominates a capture.
- **Window scaling requires both ends to support it, every hop to pass
  it, and the option to be checked, not assumed.** Some legacy or
  misconfigured middleboxes strip TCP options, silently disabling window
  scaling for the entire connection; confirm the option is actually
  present in the captured SYN/SYN-ACK before assuming it is in effect.
- **Throughput graphs summarize; expert flags localize.** Use the IO Graph
  or TCP Stream Graphs (Implementation and Automation, below) to see
  *that* a slowdown occurred, then use expert-flag filters to find
  *exactly which segment* caused it.

## Implementation and Automation

### Core TCP filters

```text
tcp.flags.syn==1 && tcp.flags.ack==0        # SYN (connection attempts)
tcp.flags.syn==1 && tcp.flags.ack==1        # SYN-ACK
tcp.flags.fin==1                             # graceful close in progress
tcp.flags.reset==1                           # RST — abrupt termination
tcp.port == 443
tcp.stream == 4                              # one specific conversation
```

### Expert-flag filters

```text
tcp.analysis.retransmission
tcp.analysis.fast_retransmission
tcp.analysis.duplicate_ack
tcp.analysis.out_of_order
tcp.analysis.zero_window
tcp.analysis.window_update
tcp.analysis.flags                           # any expert-analysis condition
```

Summarize expert-flag conditions across a capture from the command line:

```bash
tshark -r capture.pcapng -Y "tcp.analysis.flags" -T fields \
  -e frame.number -e tcp.stream -e tcp.analysis.retransmission \
  -e tcp.analysis.duplicate_ack -e tcp.analysis.zero_window
```

### Reading the handshake and options

```text
tcp.flags.syn==1 && tcp.stream==4
```

Expand the **Options** node under each matched SYN/SYN-ACK in the Packet
Detail pane to confirm MSS, Window Scale, SACK Permitted, and Timestamps
were negotiated symmetrically.

### Round-trip time and graphing

Wireshark computes per-segment RTT automatically for TCP streams with
timestamps enabled, exposed as `tcp.analysis.ack_rtt`:

```text
tcp.analysis.ack_rtt > 0.2      # ACKs taking over 200ms — investigate
```

```text
Menu path: Statistics > TCP Stream Graphs > Round Trip Time
Menu path: Statistics > TCP Stream Graphs > Window Scaling
Menu path: Statistics > TCP Stream Graphs > Throughput
```

These graphs plot per-stream metrics over time and are the fastest way to
correlate a visible slowdown with a specific point in the connection's
life before drilling into individual packets.

### Command-line throughput and retransmission summary

```bash
# Per-conversation byte/packet totals and duration.
tshark -r capture.pcapng -q -z conv,tcp

# Retransmission count per stream.
tshark -r capture.pcapng -Y "tcp.analysis.retransmission" -T fields -e tcp.stream \
  | sort | uniq -c | sort -rn
```

## Validation and Troubleshooting

- **Connection never completes past the SYN.** Filter
  `tcp.flags.syn==1 && tcp.stream==<N>`; a client SYN with no SYN-ACK
  response indicates the server is unreachable, not listening on that
  port, or a firewall/ACL is silently dropping the SYN — an RST in reply
  instead indicates the port is reachable but actively refusing (nothing
  listening, or an explicit deny-with-reset policy).
- **High retransmission rate concentrated on one stream.** Correlate
  `tcp.analysis.retransmission` timestamps against the same stream's
  `tcp.analysis.ack_rtt` — a rising RTT immediately preceding
  retransmissions points to congestion; retransmissions with stable RTT
  point more toward a lossy link segment or a flaky physical connection.
- **Throughput plateaus well below link capacity with no visible
  loss.** Check the negotiated window scale in the handshake and compute
  the bandwidth-delay product for the path; a window smaller than the BDP
  reproduces exactly this symptom without any retransmissions at all.
- **Sustained zero-window packets from one endpoint.** Confirm which side
  is advertising the zero window (`tcp.analysis.zero_window` plus the
  source address) and investigate that host's CPU, memory, and
  application-level consumption rate, not the network path.
- **Duplicate ACKs without a subsequent fast retransmission.** Fewer than
  three duplicate ACKs will not trigger fast retransmit under standard TCP
  behavior; this is expected for isolated reordering and does not by
  itself indicate a problem worth escalating.

## Security and Best Practices

- **Unexplained RSTs mid-conversation can indicate active interference.**
  A pattern of RSTs injected mid-stream, particularly with sequence
  numbers that do not match the legitimate stream's expected next byte,
  is a known signature of some network-based blocking/tampering
  mechanisms; compare the RST's sequence number against the legitimate
  stream state before assuming it originated from the real endpoint.
- **A high rate of half-open connections (SYN with no completing ACK)
  from many sources is a SYN flood signature**, covered further with
  `tshark`-based detection in [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md); distinguish this from a simple
  client-side misconfiguration by checking source diversity.
- **Do not tune window scaling or buffer sizes based on a single
  capture.** Confirm a window-limited finding across multiple samples and,
  where possible, at both ends of the path before recommending an OS-level
  TCP tuning change, since aggressive buffer increases have their own
  memory-pressure trade-offs.
- **Redact application data before sharing a capture showing
  retransmitted or reassembled payloads.** Retransmission investigations
  frequently require Follow Stream ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)) on the affected
  conversation, which reassembles application data that may contain
  sensitive content.
- **Treat consistent packet loss concentrated at a specific capture point
  as an infrastructure finding, not just a performance one.** A TAP or
  SPAN oversubscription ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)) can masquerade as network-induced
  retransmission; rule out the capture point itself before reporting a
  path-loss conclusion.

## References and Knowledge Checks

**References**

- [Wireshark User's Guide, "TCP Analysis" and "Statistics" chapters
  (current for the 4.4.x release line).](https://www.wireshark.org/docs/wsug_html_chunked/)
- IETF [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293) (TCP), [RFC 7323](https://www.rfc-editor.org/rfc/rfc7323) (TCP Extensions for High Performance —
  window scaling and timestamps), [RFC 2018](https://www.rfc-editor.org/rfc/rfc2018) (TCP Selective Acknowledgment).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. What is the difference between a retransmission triggered by a timeout
   and a fast retransmission, and which `tcp.analysis` field identifies
   each?
2. Why does a sustained zero-window condition point an investigation at
   the receiving host rather than the network path?
3. What is the bandwidth-delay product, and why can a connection be
   throughput-limited by its TCP window even when no packet loss is
   present?
4. What is the practical difference, from a troubleshooting standpoint,
   between a connection attempt that receives no response and one that
   receives an RST?

## Hands-On Lab

This chapter is the **highest-value chapter for WCA-101**: TCP is scored at **17% on its own**
within Domain 5.0, and TCP troubleshooting anchors Domain 6.0 (20%). It carries a lab for
each core TCP behavior — handshake/options, retransmissions, flow control, teardown/reset,
and performance — all runnable `tshark` analyses using Wireshark's TCP expert filters. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.5** — `tshark` and a capture of a real TCP session,
ideally one with some loss (generate one by throttling/interrupting a download). **Cost:**
none.

### Lab 6.1 — The three-way handshake and TCP options (Topic: TCP setup)

**Objective:** Read connection establishment and negotiated options.

```bash
tshark -r tcp.pcapng -Y "tcp.flags.syn == 1" \
  -T fields -e ip.src -e ip.dst -e tcp.flags.syn -e tcp.flags.ack \
  -e tcp.options.mss_val -e tcp.options.wscale.shift -c 6
```

**Expected result:** SYN, SYN-ACK, then the client's ACK, with MSS and window-scale options
in the SYNs — the handshake negotiates the sequence numbers and options (MSS, window scaling,
SACK-permitted) that govern the whole connection; options only present in the SYNs bind both
ends for the session's life.

**Negative test:** expect window scaling to apply when only one side offered it in its SYN;
scaling requires both SYNs to carry the option — a one-sided offer means no scaling, capping
throughput on high-BDP paths.

**Cleanup:** none (read-only).

### Lab 6.2 — Retransmissions and duplicate ACKs (Topic: TCP reliability)

**Objective:** Identify loss recovery in the capture.

```bash
tshark -r tcp.pcapng -Y "tcp.analysis.retransmission || tcp.analysis.fast_retransmission" \
  -T fields -e frame.number -e ip.src -e tcp.seq -e tcp.analysis.rto | head
tshark -r tcp.pcapng -Y "tcp.analysis.duplicate_ack" -T fields -e frame.number -e tcp.analysis.duplicate_ack_num | head
```

**Expected result:** retransmitted segments and the duplicate ACKs that triggered fast
retransmit — Wireshark's `tcp.analysis.*` expert fields flag loss recovery directly; three
duplicate ACKs driving a fast retransmit is the classic packet-loss signature, and the RTO
field shows timeout-based recovery.

**Negative test:** read raw sequence numbers by hand to find loss; you will miss it — the
`tcp.analysis` expert layer is what makes retransmission and dup-ACK patterns visible at a
glance, and it is what the exam expects you to use.

**Cleanup:** none (read-only).

### Lab 6.3 — Window size and flow control (Topic: TCP flow control)

**Objective:** Detect receiver-side flow-control stalls.

```bash
tshark -r tcp.pcapng -Y "tcp.analysis.zero_window || tcp.analysis.window_full" \
  -T fields -e frame.number -e ip.src -e tcp.window_size_value | head
tshark -r tcp.pcapng -Y "tcp.analysis.window_update" -T fields -e frame.number | head
```

**Expected result:** zero-window events (the receiver's buffer is full, advertising window 0)
and the later window updates that reopen the flow — TCP flow control is the receiver
throttling the sender via the advertised window; a zero window is the receiver, not the
network, stalling the transfer.

**Negative test:** blame the network or the sender for a stall that the capture shows as a
receiver zero-window; adding bandwidth changes nothing — the receiving application is not
draining its socket, which only the window view reveals.

**Cleanup:** none (read-only).

### Lab 6.4 — Connection teardown and resets (Topic: TCP teardown)

**Objective:** Distinguish graceful close from abortive reset.

```bash
tshark -r tcp.pcapng -Y "tcp.flags.fin == 1" -T fields -e frame.number -e ip.src -e ip.dst | head
tshark -r tcp.pcapng -Y "tcp.flags.reset == 1" -T fields -e frame.number -e ip.src -e ip.dst | head
```

**Expected result:** FIN/ACK exchanges (graceful four-way close) versus RST packets (abortive
termination) — a FIN is an orderly shutdown, while a RST is an abrupt abort (port closed,
application crash, or policy drop), so which one ended a connection tells you *how* it died.

**Negative test:** treat a mid-transfer RST as a normal close; it is an abort that usually
means the application or a firewall killed the connection — FIN and RST are different failure
stories, and conflating them hides the cause.

**Cleanup:** none (read-only).

### Lab 6.5 — TCP performance: RTT, throughput, and expert info (Topic: TCP performance)

**Objective:** Quantify a connection's performance from the capture.

```bash
tshark -r tcp.pcapng -q -z conv,tcp                       # per-conversation bytes/duration
tshark -r tcp.pcapng -Y "tcp" -T fields -e tcp.analysis.ack_rtt | sort -n | tail    # worst RTTs
tshark -r tcp.pcapng -q -z expert                         # aggregated expert warnings/notes
```

**Expected result:** the TCP conversation table (bytes, duration → throughput), the largest
ACK RTTs, and the expert summary counting retransmissions/zero-windows/resets — together these
turn "it feels slow" into measured RTT, throughput, and a ranked list of protocol problems,
which is the Domain 6.0 troubleshooting deliverable.

**Negative test:** report "the network is slow" with no numbers; the conversation and expert
views give measured throughput and a specific fault (loss, zero window, high RTT) — measurement
replaces speculation.

**Cleanup:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

TCP's sequence numbers, acknowledgment numbers, and window mechanism are
what turn an unreliable network into a reliable byte stream, and
Wireshark's expert-analysis layer translates that mechanism directly into
actionable flags — retransmission, duplicate ACK, zero window — that
localize a performance problem to a specific segment, endpoint, or path
characteristic rather than leaving "the network is slow" as the final
answer. [Chapter 07](07-application-protocol-tls-and-service-response-analysis.md) moves one layer higher, applying the same investigative
discipline to application protocols, TLS, and service response time.

- [ ] Can decode TCP header fields and read a three-way handshake and
      teardown.
- [ ] Can identify retransmissions, duplicate ACKs, and zero-window
      conditions using Wireshark's expert-analysis flags.
- [ ] Can explain window scaling and compute a path's bandwidth-delay
      product.
- [ ] Can build an RTT and throughput picture of a TCP conversation using
      Statistics graphs and `tshark` field extraction.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
