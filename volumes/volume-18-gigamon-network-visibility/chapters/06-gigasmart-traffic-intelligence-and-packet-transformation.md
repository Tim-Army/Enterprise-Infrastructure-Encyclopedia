# Chapter 06: GigaSMART Traffic Intelligence and Packet Transformation

## Learning Objectives

- Explain GigaSMART's role as a processing engine distinct from Flow
  Mapping's forwarding decisions, and which node platforms host it.
- Describe the core GigaSMART traffic-intelligence applications: packet
  slicing, masking, deduplication, header stripping/tunnel termination,
  and Application Metadata Intelligence.
- Explain how GigaSMART reduces tool load and licensing cost by
  transforming traffic before delivery, rather than relying on every tool
  to perform its own reduction.
- Configure a representative set of GigaSMART applications and chain them
  into a second-level map, building on [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md)'s mapping model.
- Diagnose common GigaSMART faults: engine oversubscription, licensing
  gaps, and unexpected data loss from misapplied slicing or masking.

## Theory and Architecture

### GigaSMART as a processing layer, not a forwarding layer

[Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md) established that Flow Mapping decides **which** traffic reaches
**which** destination. **GigaSMART** answers a different question: what
should happen to the traffic's content along the way? GigaSMART is a
traffic-intelligence processing engine that runs on GigaSMART-capable
node platforms (the HC Series introduced in [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md), and the
equivalent processing capability built into V Series virtual nodes,
[Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md)) and operates on traffic that a first-level map has already
selected, transforming or enriching it before a second-level map delivers
it to its final tool destination — the two-level chaining pattern
introduced in [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md).

GigaSMART capacity is a finite, licensed resource distinct from raw port
bandwidth: a node can have ample network and tool port capacity while
still being GigaSMART-constrained if too much traffic is routed through
its processing engine relative to its licensed and physical processing
capacity. This is why [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md)'s filter-before-you-aggregate design
principle matters especially for any traffic destined for GigaSMART
processing — every byte filtered out at the first level is a byte GigaSMART
never has to touch.

### Core GigaSMART applications

| Application | Function | Primary benefit |
| --- | --- | --- |
| Packet slicing | Truncates each packet after a specified point (commonly after a named protocol header, such as the end of the TCP/IP header) while preserving headers needed for analysis | Reduces tool storage and processing load for tools that only need header-level visibility (flow/session analysis) rather than full payload |
| Masking | Overwrites specific packet fields with a fixed pattern before delivery | Removes sensitive data (payment card numbers, personal data) from what a tool ever receives, supporting data-minimization and compliance requirements |
| De-duplication | Identifies and drops duplicate copies of the same packet, commonly produced when multiple TAPs or SPAN sessions overlap in coverage | Reduces tool load and storage consumption without losing unique traffic |
| Header stripping / tunnel termination | Removes encapsulation headers (VLAN tags, MPLS labels, VXLAN/GRE tunnel headers, mobile GTP headers) so a tool sees the traffic it understands rather than an encapsulated wrapper | Lets tools that cannot natively parse a given encapsulation still analyze the traffic inside it |
| Application Metadata Intelligence | Inspects traffic to identify the application in use and generates IPFIX-based metadata records describing session attributes, without requiring the full payload to be delivered | Feeds NDR and SIEM platforms with rich session context at a fraction of the bandwidth and storage cost of full packet capture |
| Adaptive/Application Session Filtering | Filters traffic based on identified application or session characteristics rather than static header fields alone | Allows a first-level map to select traffic by application (for example, a specific SaaS application) even when that traffic cannot be distinguished by IP/port alone |
| SSL/TLS decryption | Decrypts TLS-protected traffic centrally, using configured server certificates and keys, so downstream out-of-band tools that cannot decrypt on their own can inspect plaintext content | Removes the need for every individual out-of-band tool to independently manage decryption keys; covered further in [Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md) alongside inline decryption |
| Tunneling (L2GRE/VXLAN) | Re-encapsulates selected traffic for delivery across a routed network to a distant tool farm | Extends visibility delivery beyond directly cabled tool ports, complementing the virtual/cloud tunneling model from [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md) |

### Why transform traffic in the fabric instead of at the tool

Every one of these applications could, in principle, be implemented
independently inside each consuming tool. Centralizing them in GigaSMART
instead has three durable advantages:

1. **Consistency.** A masking policy protecting a specific data field is
   applied once, centrally, rather than configured — and potentially
   configured inconsistently — inside every tool that receives that
   traffic.
2. **Cost.** Many security and monitoring tools are licensed by ingested
   throughput; slicing, deduplication, and metadata generation all reduce
   the volume a tool actually has to ingest, directly reducing licensing
   and storage cost.
3. **Tool capability independence.** Not every tool can terminate a VXLAN
   tunnel, decrypt TLS, or parse a mobile GTP header natively. GigaSMART
   normalizes traffic into a form any subscribed tool can consume,
   decoupling tool selection from the acquisition environment's
   encapsulation choices.

### Application Metadata Intelligence in more depth

Application Metadata Intelligence deserves particular attention because
it represents a shift from "deliver a copy of traffic" to "deliver a
structured description of traffic." Rather than forwarding full packets,
GigaSMART inspects sessions, identifies the application, and exports
IPFIX-based metadata records — attributes such as application identity,
session duration, byte counts, and protocol-specific fields — to a tool
designed to consume that metadata (typically an NDR platform or a SIEM).
This is materially cheaper to transport and store than full packet
capture, and is often sufficient for detection and correlation use cases
that do not require payload-level forensic detail — while full packet
capture (undiminished by slicing) remains available on a separate map for
the subset of traffic that does warrant deep forensic retention.

## Design Considerations

- **Budget GigaSMART processing capacity as a first-class sizing input,
  not an afterthought.** Node and license selection ([Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md)) should
  account for how much traffic will actually traverse GigaSMART
  processing, not just raw port throughput — a node with abundant port
  capacity but insufficient GigaSMART engine capacity for the traffic
  volume routed to it will drop or queue traffic at the processing stage.
- **Match the transformation to the tool's actual requirement.** Full
  packet capture platforms need unsliced payload; an NDR platform
  consuming metadata does not. Sending unsliced full payload to every
  tool regardless of need wastes GigaSMART capacity, tool-port bandwidth,
  and tool storage simultaneously.
- **Treat masking policy as a compliance control, not just a technical
  feature.** Which fields are masked, for which tools, should be
  reviewed with the same rigor as a data classification policy — masking
  configured once and never revisited can drift out of alignment as
  regulatory requirements or the underlying application's data format
  changes.
- **Decide where SSL/TLS decryption happens deliberately.** Centralized
  GigaSMART decryption for out-of-band tools (this chapter) is a
  different design decision, with different key-management and risk
  implications, than inline decryption ahead of an in-path security tool
  ([Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md)) or the newer Precryption model that avoids centralized key
  handling entirely — do not conflate the two without considering which
  is appropriate for a given tool's deployment mode.
- **Plan for application identification's inherent uncertainty.**
  Application-aware filtering and metadata generation rely on signatures
  and heuristics that are updated over time (similar in spirit to App-ID
  content updates on a Palo Alto Networks firewall, [Volume XVI](../../volume-16-palo-alto-networks-security/README.md)) and are
  not infallible; do not build a security control's sole detection logic
  on GigaSMART application identification without a compensating control.

## Implementation and Automation

### Configuring packet slicing

```text
(admin) (config) # gsgroup alias gs-engine-01
(admin) (config gsgroup alias gs-engine-01) # gsop alias slice-after-l4
(admin) (config gsgroup gsop alias slice-after-l4) # type slice
(admin) (config gsgroup gsop alias slice-after-l4) # slice-length after-header tcp
(admin) (config gsgroup gsop alias slice-after-l4) # exit
(admin) (config gsgroup alias gs-engine-01) # exit
(admin) (config) # write memory
```

### Configuring masking

```text
(admin) (config gsgroup alias gs-engine-01) # gsop alias mask-pan-field
(admin) (config gsgroup gsop alias mask-pan-field) # type mask
(admin) (config gsgroup gsop alias mask-pan-field) # mask-pattern offset 40 length 16 value 0xFF
(admin) (config gsgroup gsop alias mask-pan-field) # exit
```

### Configuring de-duplication

```text
(admin) (config gsgroup alias gs-engine-01) # gsop alias dedup-overlap
(admin) (config gsgroup gsop alias dedup-overlap) # type dedup
(admin) (config gsgroup gsop alias dedup-overlap) # dedup-window 5ms
(admin) (config gsgroup gsop alias dedup-overlap) # exit
```

### Configuring Application Metadata Intelligence export

```text
(admin) (config gsgroup alias gs-engine-01) # gsop alias app-metadata-export
(admin) (config gsgroup gsop alias app-metadata-export) # type app-metadata-intelligence
(admin) (config gsgroup gsop alias app-metadata-export) # export-destination 10.30.5.40 udp 4739
(admin) (config gsgroup gsop alias app-metadata-export) # exit
(admin) (config gsgroup alias gs-engine-01) # exit
(admin) (config) # write memory
```

### Chaining GigaSMART applications into the Flow Mapping model

Once GigaSMART operations (`gsop`) are defined within a `gsgroup`, they
are referenced as the destination of a first-level map — exactly the
pattern introduced in [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md) — and the GigaSMART group's output
becomes the source of the second-level map that delivers processed
traffic to its final tool destination:

```text
(admin) (config) # map alias fl-web-tier-to-gigasmart
(admin) (config map alias fl-web-tier-to-gigasmart) # type regular
(admin) (config map alias fl-web-tier-to-gigasmart) # source 1/1/x1
(admin) (config map alias fl-web-tier-to-gigasmart) # destination gsgroup gs-engine-01
(admin) (config map alias fl-web-tier-to-gigasmart) # rule add priority 10 pass ipv4 destination-port 443
(admin) (config map alias fl-web-tier-to-gigasmart) # exit

(admin) (config) # map alias sl-gigasmart-to-dlp
(admin) (config map alias sl-gigasmart-to-dlp) # type regular
(admin) (config map alias sl-gigasmart-to-dlp) # source gsgroup gs-engine-01
(admin) (config map alias sl-gigasmart-to-dlp) # destination 1/1/g4
(admin) (config map alias sl-gigasmart-to-dlp) # rule add priority 10 pass any
(admin) (config map alias sl-gigasmart-to-dlp) # exit
(admin) (config) # write memory
```

> As in prior chapters, exact `gsop`/`gsgroup` keyword syntax and
> available GigaSMART application types vary by GigaVUE-OS release and
> licensed feature set; confirm the current syntax and licensing
> requirements against the documentation for the release in use.

## Validation and Troubleshooting

- **GigaSMART-processed traffic shows drops under load that raw port
  statistics do not explain.** Check GigaSMART engine utilization
  specifically (a separate statistic from port utilization) — an
  oversubscribed GigaSMART engine drops traffic at the processing stage
  even when network and tool ports themselves are well within capacity.
  The remediation is tighter first-level filtering or additional
  GigaSMART engine capacity, not a Flow Mapping change.
- **A tool reports missing payload it used to receive.** Confirm no
  packet-slicing operation was applied (or was applied with a shorter
  slice length than the tool requires) upstream of that tool's map path;
  this is a common regression when a shared `gsgroup` is reused for a new
  tool with different payload requirements than the tools it was
  originally designed for.
- **Masked data still appears in tool output.** Confirm the mask
  operation's offset and length actually align with the target field for
  the traffic in question — a masking rule tuned for one application's
  packet format will not correctly mask a different application's field
  at a different offset, even if both are nominally "the same kind of
  data."
- **Deduplication drops traffic that was not actually duplicate.** Check
  the configured dedup window — a window set too wide can treat two
  distinct packets with coincidentally similar characteristics as
  duplicates in high-volume, low-entropy traffic patterns; narrow the
  window and validate against known traffic before trusting deduplication
  output for evidentiary use cases.
- **Application Metadata Intelligence export shows no records at the
  collector.** Confirm network reachability and port configuration
  between the GigaSMART engine and the configured export destination, and
  confirm the collector is actually listening on the configured
  protocol/port — this is frequently a straightforward network
  reachability issue rather than a GigaSMART configuration fault.

## Security and Best Practices

- Treat masking configuration as a data-protection control subject to
  periodic compliance review, not a one-time technical setup; revisit
  masked field definitions whenever the underlying application's data
  format changes or a new regulatory requirement is introduced.
- Restrict who can modify GigaSMART operations feeding masking or
  decryption to the same administrative rigor as Flow Mapping changes
  ([Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md)'s RBAC model) — a change to a masking offset is
  functionally a change to what sensitive data a tool receives.
- Log and periodically audit which tools receive decrypted (plaintext)
  traffic via GigaSMART SSL/TLS decryption, and confirm that list still
  matches the tools with a legitimate, current need for that visibility.
- Do not rely solely on packet slicing or masking as a substitute for
  encrypting data at rest on the receiving tool — GigaSMART transformation
  reduces what a tool receives, but the tool's own storage and access
  controls remain the tool operator's responsibility.
- Validate Application Metadata Intelligence and application-aware
  filtering signature/content updates on the same cadence as other
  security-relevant content updates in this encyclopedia (compare
  App-ID content updates in [Volume XVI](../../volume-16-palo-alto-networks-security/README.md)), since stale application
  identification content degrades both filtering accuracy and metadata
  quality over time.

## References and Knowledge Checks

**References**

- Gigamon, *GigaSMART for Network Traffic Intelligence* product page —
  full application catalog and architecture.
- Gigamon, *Packet Slicing*, *Data Masking*, and *De-Duplication* product
  pages — per-application behavior detail.
- Gigamon, *GigaSMART Data Sheet* — licensing and platform capacity
  reference.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline.

**Knowledge checks**

1. What is the functional difference between what Flow Mapping decides
   and what GigaSMART does, and why does the two-level map pattern from
   [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md) exist specifically to connect them?
2. Name three GigaSMART applications and, for each, state one concrete
   benefit to a downstream tool or to overall fabric cost.
3. Why is GigaSMART engine capacity a separate sizing concern from
   network- and tool-port bandwidth?
4. Why should masking configuration be reviewed periodically rather than
   configured once and left unchanged indefinitely?

## Hands-On Lab

**Objective:** Configure a GigaSMART processing chain — packet slicing
and masking — on a lab node, feed it from the two-level map pattern built
in [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md), and validate both correct transformation and a deliberate
misconfiguration that exposes unmasked data.

**Prerequisites**

- A lab GigaVUE HC Series node (or lab-equivalent) with GigaSMART
  licensed and available, continuing from the [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) and [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md)
  labs.
- A packet capture tool at the final tool-port destination.
- A lab traffic generator capable of sending a payload containing a
  recognizable test pattern (for example, a fixed 16-byte value standing
  in for a sensitive field) at a known, fixed offset in the packet.

**Steps**

1. Configure a `gsgroup` with a slicing operation that truncates packets
   shortly after the TCP/IP header, following the pattern in
   Implementation and Automation.
2. Configure a masking operation within the same `gsgroup` targeting the
   offset of your test payload pattern.
3. Configure a first-level map sourcing lab traffic into the `gsgroup`,
   and a second-level map delivering the `gsgroup` output to a tool port
   connected to your capture tool, following the two-level chaining
   pattern.
4. Generate lab traffic containing the test payload pattern at the
   expected offset.
5. Inspect the capture at the tool port.
   **Expected result:** the captured packets are truncated at the
   configured slice point (payload beyond the slice length is absent),
   and the test pattern — if it falls within the retained slice length —
   appears masked (overwritten with the configured fixed value) rather
   than as the original test pattern.
6. **Negative test:** intentionally misconfigure the masking operation's
   offset (shift it by a fixed number of bytes so it no longer aligns
   with the test pattern's actual position), re-apply the configuration,
   and regenerate the same lab traffic.

   ```text
   (admin) (config gsgroup gsop alias mask-pan-field) # mask-pattern offset 60 length 16 value 0xFF
   ```

   **Expected result:** the captured packets now show the original,
   unmasked test pattern at its true offset, reproducing the
   misaligned-masking failure mode described in Validation and
   Troubleshooting — demonstrating why offset/length must be validated
   against actual traffic, not assumed from documentation alone.
7. Correct the masking offset back to the validated value from step 2 and
   confirm masked output resumes.
8. **Cleanup:** remove or retain the lab `gsgroup`, first-level map, and
   second-level map depending on whether the lab node will be reused for
   [Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md)'s inline and decryption exercises; if disposing of the
   configuration, remove the `gsgroup` reference from both maps before
   deleting the `gsgroup` itself.

## Summary and Completion Checklist

GigaSMART is the traffic-intelligence engine that transforms and enriches
traffic between acquisition and delivery — slicing, masking, deduplicating,
stripping encapsulation, decrypting, and generating application metadata
— centralizing work that would otherwise need to be duplicated,
inconsistently, inside every consuming tool. GigaSMART capacity is a
distinct, licensed sizing dimension from port bandwidth, and its
configuration — especially masking and decryption — carries data-protection
and compliance weight that warrants the same review discipline as Flow
Mapping itself. [Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md) extends this traffic-intelligence layer into
the inline path, where GigaSMART decryption and bypass resiliency work
together to protect production traffic.

- [ ] Can explain the distinction between Flow Mapping's forwarding
      decisions and GigaSMART's traffic transformation.
- [ ] Can describe packet slicing, masking, deduplication, and
      Application Metadata Intelligence and state a benefit of each.
- [ ] Can configure a GigaSMART operation and chain it into a two-level
      Flow Map.
- [ ] Can explain why GigaSMART engine capacity must be sized separately
      from port bandwidth.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
