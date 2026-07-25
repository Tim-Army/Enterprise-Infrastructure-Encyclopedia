# Chapter 03: Wireshark Interface, Profiles, Filters, and Analysis Workflows

![Lab flow for this chapter: a dedicated analysis profile isolates a lab-specific workflow with a saved display filter, a coloring rule, a custom column, and Follow TCP Stream reassembling a full conversation in a separate window. As a negative test, a deliberately misspelled filter field name is entered in the filter bar; the bar turns red and the filter does not apply at all, demonstrating Wireshark's syntax validation rejects an invalid field name outright rather than silently applying a filter that matches nothing.](../../../diagrams/volume-20-wireshark-packet-analysis/chapter-03-analysis-profile-filter-validation-flow.svg)

*Figure 3-1. Flow used throughout this chapter's Hands-On Lab: a dedicated Wireshark analysis profile with a saved filter, coloring rule, and custom column, tested against a misspelled filter field.*

## Learning Objectives

- Navigate Wireshark's packet list, packet detail, and packet bytes panes,
  and explain what each represents in the dissection pipeline introduced in
  [Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md).
- Build and apply display filter expressions using field names, comparison
  operators, and logical combinators, and distinguish a display filter from
  the capture filters covered in [Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md).
- Create and switch between configuration profiles so that analysis
  settings for different roles or investigations do not interfere with each
  other.
- Use coloring rules and custom columns to surface analytically significant
  packets without writing a filter for every question.
- Apply core statistics workflows — Protocol Hierarchy, Conversations,
  Endpoints, and Follow Stream — to move from a raw capture to an initial
  hypothesis.

## Theory and Architecture

[Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md) described Wireshark's dissection pipeline: `dumpcap` writes raw
frames, and the `epan` dissector engine parses them into a protocol tree.
The Wireshark GUI is the primary interactive consumer of that tree, and its
interface is organized around three synchronized panes:

| Pane | Shows | Selecting a row/field does |
| --- | --- | --- |
| Packet List | One line per packet: number, timestamp, source, destination, protocol, length, and a summary column (`Info`). | Loads that packet's full dissection into the Packet Detail pane. |
| Packet Detail | The dissected protocol tree for the selected packet, one expandable node per protocol layer, matching the encapsulation chain from [Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md). | Highlights the corresponding bytes in the Packet Bytes pane and offers "Apply as Filter" / "Copy" context actions keyed to that specific field. |
| Packet Bytes | The raw hex and ASCII representation of the selected packet. | Highlights the corresponding field in the Packet Detail pane (the relationship is bidirectional). |

This three-pane synchronization is what makes Wireshark's GUI more than a
`tshark` wrapper: an analyst can click a suspicious flag in the detail pane
and immediately see both its raw byte position and every other packet in
the list that carries the same value, once a filter is built from it.

### Display filters

A display filter is a boolean expression evaluated against the dissected
field tree of every packet already in memory. Unlike the capture filters
covered in [Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md), a display filter never discards data from the
file — it only controls what is currently shown, and can be changed,
cleared, or narrowed indefinitely without recapturing.

Display filter expressions follow a consistent grammar:

```text
<protocol>.<field> <comparison operator> <value>
```

```text
ip.addr == 10.0.20.15          # field equals value
tcp.port != 22                 # field not equal to value
frame.len > 1200               # numeric comparison
http.request.method == "GET"   # string comparison
tcp.flags.syn == 1             # single-bit field
dns                            # bare protocol name: matches if DNS present
```

Expressions combine with `&&` (and), `||` (or), and `!` (not); parentheses
group sub-expressions:

```text
(tcp.flags.syn == 1 && tcp.flags.ack == 0) && ip.dst == 10.0.20.15
!(arp || icmp)
```

Wireshark validates filter syntax as it is typed: a green background
indicates a syntactically valid expression, a red/pink background indicates
a syntax error, and a yellow background indicates a filter that is valid
but likely not what was intended (for example, a field that does not exist
in any loaded packet). `tshark -Y "<filter>"` applies the identical
expression language from the command line, which is why filters developed
interactively in the GUI transfer directly into the scripted workflows
covered in [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md).

### Configuration profiles

A configuration profile is a named, isolated set of Wireshark preferences:
column layout, coloring rules, saved filter buttons, and protocol
preferences. Profiles live under the user's configuration directory
(`~/.config/wireshark/profiles/<name>` on Linux,
`%APPDATA%\Wireshark\profiles\<name>` on Windows,
`~/.config/wireshark/profiles/<name>` on macOS) and are switched without
restarting Wireshark. Profiles exist because a single global configuration
cannot simultaneously serve every analysis role well — a security
investigation profile wants coloring rules that flag SYN scans and cleartext
credentials; a VoIP performance profile wants columns for jitter and RTP
sequence gaps; neither configuration is useful for the other's task.

## Design Considerations

- **One profile per recurring analysis role, not per investigation.** A
  `Security-Investigation` profile and a `TCP-Performance` profile that are
  reused across many captures are more valuable than a fresh profile
  created and discarded per incident. Reserve genuinely per-investigation
  customization (a saved display filter for one specific host) for that
  profile's saved filter list, not a new profile.
- **Coloring rules vs. display filters for triage.** Use coloring rules
  when multiple conditions need to remain simultaneously visible while
  scanning a large capture (retransmissions in one color, resets in
  another); use a display filter when the goal is to isolate one condition
  and hide everything else.
- **Custom columns cost screen width.** Every additional column reduces
  space for the ones that matter most; build columns deliberately per
  profile rather than accumulating them indefinitely in the default
  profile.
- **Profiles are portable but not automatically sanitized.** A profile
  exported to share with another analyst carries any saved filters, which
  may reference internal hostnames or IP ranges; review before sharing
  outside the immediate investigating team ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)'s evidence-handling
  guidance applies to profile content, not just capture content).
- **Statistics workflows scale down attention, not data.** Protocol
  Hierarchy and Conversations summarize an entire capture in seconds and
  should be the first step on any unfamiliar file, before applying a filter
  based on a guess about what is relevant.

## Implementation and Automation

Examples below reference Wireshark 4.4.x menu paths, per
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md); confirm against
**Help > About Wireshark** if a menu location has moved in a later point
release.

### Creating and switching profiles

1. Open **Edit > Configuration Profiles** (or press `Ctrl+Alt+P` /
   `Cmd+Option+P`).
2. Click **+** to create a new profile, name it (for example,
   `Security-Investigation`), and click **OK**.
3. Switch profiles at any time from the status bar's profile indicator in
   the bottom-right corner, or re-open **Edit > Configuration Profiles**.

### Building a display filter interactively

1. Right-click any field in the Packet Detail pane and choose **Apply as
   Filter > Selected** to generate a filter expression for that exact
   field/value pair.
2. Refine the generated expression in the filter bar directly, or combine
   it with a second field's **Apply as Filter > ... and Selected**.
3. Save a frequently used expression as a filter button: **Analyze >
   Display Filters**, or drag the filter bar's contents to the filter
   button toolbar.

### Adding a coloring rule

```text
Menu path: View > Coloring Rules > + 

Name:   TCP Retransmissions
Filter: tcp.analysis.retransmission
Color:  background = orange
```

Coloring rules are evaluated top-down; a packet is colored by the first
rule it matches, so order rules from most specific to most general.

### Adding a custom column

```text
Menu path: Edit > Preferences > Appearance > Columns > +

Title:   TCP Delta
Type:    Custom
Field:   tcp.time_delta
```

`tcp.time_delta` (time since the previous frame in the same TCP stream) is
one of the highest-value custom columns for performance analysis (Chapter
06) because it exposes per-packet latency without opening a graph.

### Core statistics workflows

```text
Statistics > Protocol Hierarchy   — proportion of the capture by protocol
Statistics > Conversations        — traffic grouped by endpoint pair, sortable by bytes/packets
Statistics > Endpoints            — traffic grouped by single endpoint
Statistics > IO Graph             — traffic volume over time, filterable per line
```

`tshark` exposes the same summaries non-interactively, which is the bridge
to [Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)'s automation workflows:

```bash
tshark -r capture.pcapng -q -z io,phs        # protocol hierarchy
tshark -r capture.pcapng -q -z conv,tcp       # TCP conversation summary
tshark -r capture.pcapng -q -z endpoints,ip   # IP endpoint summary
```

### Follow Stream

Right-click any packet in a TCP, UDP, HTTP, or TLS conversation and choose
**Follow > TCP Stream** (or the appropriate protocol) to reassemble the full
bidirectional application-layer conversation in a readable text or hex
view, with client and server data distinguished by color. This is the
fastest way to read what an application actually exchanged, and it
automatically generates the underlying stream-index filter
(`tcp.stream==<N>`) in the filter bar when the dialog is closed.

## Validation and Troubleshooting

- **Filter bar shows red/pink and refuses to apply.** A syntax error — most
  commonly a misspelled field name or a missing comparison operator (`dns`
  alone is valid as a protocol-presence test, but `dns ==` is not). Use
  autocomplete (start typing a field name) to confirm the exact field
  syntax.
- **Filter bar shows yellow but applies.** The expression is syntactically
  valid but references a field or value combination unlikely to be correct
  — commonly a field name valid for one protocol version applied to traffic
  using a different version (for example, an HTTP/1.1-specific field
  against an HTTP/2 stream).
- **A known-present protocol does not appear in Protocol Hierarchy.** The
  dissector may not have recognized the traffic due to a non-standard port;
  force dissection with **Analyze > Decode As** rather than assuming the
  protocol is absent from the capture.
- **Coloring rule does not apply to an expected packet.** Rule order
  matters — confirm no earlier, broader rule is matching first and
  suppressing the intended one; use **View > Colorize Conversation** as a
  temporary check independent of the saved rule set.
- **Profile changes do not appear after restart.** Confirm the correct
  profile is active in the status bar; edits made while the default profile
  is selected do not appear when a named profile is later activated.

## Security and Best Practices

- **Do not embed credentials or secrets in saved display filters or column
  definitions** that will be exported or shared; treat profile files with
  the same handling discipline as the captures they analyze.
- **Build a dedicated `Security-Investigation` profile** with coloring
  rules tuned to security-relevant conditions (SYN scans, cleartext
  authentication, TLS certificate anomalies) so triage does not depend on
  an analyst remembering to type each filter from scratch under time
  pressure.
- **Prefer Decode As over globally changing a dissector's default port**
  when investigating traffic on a non-standard port — a global preference
  change persists across the profile and can mis-dissect unrelated,
  legitimate traffic on that port in later analysis sessions.
- **Review Follow Stream output before pasting it into a ticket or
  report.** Reassembled application data frequently contains credentials,
  session tokens, or personal data that must be redacted before leaving
  the investigating team's controlled environment.
- **Keep the default profile close to Wireshark's shipped defaults.**
  Heavily customizing the default profile makes a workstation's Wireshark
  behave differently from every colleague's, complicating collaborative
  analysis; put customization in named, exportable profiles instead.

## References and Knowledge Checks

**References**

- [Wireshark User's Guide, "User Interface," "Working with Captured
  Packets," and "Configuration Profiles" chapters (current for the 4.4.x
  release line).](https://www.wireshark.org/docs/wsug_html_chunked/)
- [Wireshark Display Filter Reference (`https://www.wireshark.org/docs/dfref/`).](https://www.wireshark.org/docs/dfref/)
- [`man tshark`](https://www.wireshark.org/docs/man-pages/tshark.html) — `-Y`, `-z` option reference.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. What is the practical difference between applying a display filter and
   applying a coloring rule to the same condition?
2. Why do configuration profiles exist as named, switchable sets rather
   than a single global configuration?
3. What does a yellow filter-bar background communicate that a green
   background does not?
4. Which menu action reassembles a full bidirectional TCP conversation
   into readable application data, and what filter expression does closing
   that dialog generate?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **WCA-101 Domain 3.0 (capture and
display filters, 12%) and Domain 4.0 (configure/adapt the interface, 5%)** — display
filters, capture-vs-display filtering, profiles/columns/coloring, and advanced filter
expressions. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.4** — Wireshark/`tshark` installed and a sample
capture with mixed protocols (`sample.pcapng` below). **Cost:** none.

### Lab 3.1 — Display filters (Topic: Display filtering)

**Objective:** Filter a loaded capture down to what matters.

```bash
tshark -r sample.pcapng -Y "dns" | head
tshark -r sample.pcapng -Y "ip.addr == 192.168.1.10 && tcp.port == 80" | head
tshark -r sample.pcapng -Y "http.request.method == \"GET\"" -T fields -e http.host -e http.request.uri | head
```

**Expected result:** each display filter narrows the loaded packets non-destructively — `dns`
shows only DNS, the compound filter shows one host's web traffic, and the last extracts GET
hosts/URIs — display filters use protocol.field syntax and never alter the underlying file.

**Negative test:** type a capture-filter expression (`tcp port 80`) into a display-filter
context; it is rejected as invalid syntax — capture filters (BPF) and display filters
(protocol.field) are different languages for different stages.

**Cleanup:** none (read-only).

### Lab 3.2 — Capture filters versus display filters (Topic: Two filter languages)

**Objective:** See the difference between filtering at capture and at display.

```bash
# Capture filter (BPF) — decides what is stored:
dumpcap -i any -f "udp port 53" -c 20 -w /tmp/dns.pcapng
# Display filter (protocol.field) — decides what is shown from a stored file:
tshark -r /tmp/dns.pcapng -Y "dns.flags.response == 1"
```

**Expected result:** the capture filter stored only UDP/53; the display filter then showed
only the DNS *responses* within it — capture filters are coarse and permanent (data not
captured is gone), display filters are rich and reversible (all captured data remains
available).

**Negative test:** expect to display-filter for a protocol you excluded with a capture
filter; it is not in the file to show — once a capture filter drops traffic, no display
filter can recover it.

**Cleanup:** `rm /tmp/dns.pcapng`.

### Lab 3.3 — Profiles, columns, and coloring rules (Topic: Interface configuration)

**Objective:** Adapt the interface to a task with a profile.

```text
# Wireshark GUI: Edit > Configuration Profiles > New ("TCP-Perf").
#   Add custom columns (e.g. tcp.analysis.ack_rtt, tcp.window_size_value).
#   Add a coloring rule: filter "tcp.analysis.retransmission" -> red background.
#   Switch profiles from the status-bar bottom-right.
```

**Expected result:** the profile shows RTT and window columns and paints retransmissions red,
so problems are visible at a glance — profiles let one Wireshark install carry purpose-built
layouts (TCP performance, security, VoIP) you switch between per task.

**Negative test:** analyze every scenario with the default columns and no coloring; you scroll
past the anomalies that a task-specific profile would highlight — the interface is a diagnostic
tool, and configuring it is Domain 4.0's point.

**Cleanup:** delete the lab profile if created only for the exercise.

### Lab 3.4 — Advanced filter expressions (Topic: Filter operators)

**Objective:** Build filters with comparison, membership, and pattern operators.

```bash
tshark -r sample.pcapng -Y "tcp.flags.syn == 1 && tcp.flags.ack == 0"   # SYN (connection starts)
tshark -r sample.pcapng -Y "tcp.port in {80 443 8080}"                    # membership set
tshark -r sample.pcapng -Y "http.host contains \"example\""              # substring
tshark -r sample.pcapng -Y "dns.qry.name matches \"\\\\.ru$\""           # regex
```

**Expected result:** SYN-only packets (new connections), traffic on a set of ports,
substring host matches, and regex domain matches — display filters support comparison
(`==`,`>`), logical (`&&`,`||`,`!`), membership (`in {}`), `contains`, and `matches`
(regex), enough to express nearly any question about a capture.

**Negative test:** use `=` instead of `==` for equality; the filter fails to compile — the
operator grammar is exact, and the expression bar flags an invalid filter before applying it.

**Cleanup:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Wireshark GUI's value over raw `tshark` output is its synchronized
three-pane view and the workflows built on top of it: profiles that keep
analysis configurations separated by role, display filters that narrow an
already-captured file without discarding data, coloring rules and custom
columns that surface conditions passively while scanning, and statistics
views that summarize an entire capture before a single filter is typed.
[Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md) begins applying these workflows to specific protocol layers,
starting with Ethernet, ARP, IPv4, and ICMPv4.

- [ ] Can identify what each of the three main panes represents and how
      they stay synchronized.
- [ ] Can write and apply a display filter using field names, comparison
      operators, and logical combinators.
- [ ] Created a named configuration profile independent of the default.
- [ ] Added a coloring rule and a custom column.
- [ ] Used Follow Stream to reassemble and read a TCP conversation.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
