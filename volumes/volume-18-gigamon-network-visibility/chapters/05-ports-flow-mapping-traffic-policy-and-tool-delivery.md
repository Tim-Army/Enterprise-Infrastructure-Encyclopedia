# Chapter 05: Ports, Flow Mapping, Traffic Policy, and Tool Delivery

![Lab flow for this chapter: a first-level map filters one network source down to a specific subnet, and a second-level map forwards that output to a GigaStream group of tool ports with an egress VLAN tag applied; matching traffic appears at both tools correctly tagged, and traffic outside the filter correctly produces no output. As a negative test, a broad pass-any rule is added at a lower priority number than the existing filter; the previously excluded traffic now appears at the tool farm, reproducing the rule-order failure mode where a badly prioritized rule silently reopens a path the filter was designed to close.](../../../diagrams/volume-18-gigamon-network-visibility/chapter-05-two-level-map-rule-order-flow.svg)

*Figure 5-1. Flow used throughout this chapter's Hands-On Lab: a two-level filtered Flow Map feeding a tagged GigaStream tool group, tested against a rule-order defect.*

## Learning Objectives

- Explain the Flow Mapping rule model in depth: map types, rule matching
  criteria, rule priority, and first-level/second-level map chaining.
- Design and implement filtered Flow Maps that deliver only relevant
  traffic to a given tool, rather than an unfiltered all-pass copy.
- Configure GigaStream to load-balance traffic across a tool group and
  explain why it solves the tool-port oversubscription problem introduced
  in [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md).
- Apply source-identifying tagging so a tool receiving aggregated traffic
  from many acquisition points can still distinguish where each packet
  originated.
- Diagnose common Flow Mapping faults: rule-order conflicts, unintentional
  overlap, and oversubscription-driven drops.

## Theory and Architecture

### The Flow Mapping rule model

Flow Mapping is the packet-forwarding policy engine introduced
conceptually in [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md) and used in minimal form in Chapters 02–04. A
**map** binds one or more source ports (network ports, tunnel endpoints,
or, on a cluster, ports on other member nodes) to one or more destination
ports (tool ports, or another map for chained processing), governed by an
ordered list of **rules** that determine which packets the map actually
forwards.

Three map types recur throughout GigaVUE-OS and GigaVUE-FM configuration:

| Map type | Behavior |
| --- | --- |
| `map` (regular) | Forwards packets matching the map's rule set; the most common map type for filtered delivery |
| `map-passall` | Forwards all traffic from the source unconditionally, bypassing rule evaluation — used for a first-touch validation ([Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md)) or where a tool genuinely needs an unfiltered copy |
| `map-scollector` (shared collector) | A map whose destination is shared across multiple source maps, commonly used to funnel several filtered sources into one common GigaSMART processing stage or tool group without duplicating destination configuration for every source |

### Rule matching and priority

A rule matches on packet header fields available at the point Flow
Mapping evaluates the packet: source/destination MAC or IP address,
VLAN ID, IP protocol, TCP/UDP port, and, on platforms/releases supporting
it, deeper criteria exposed through GigaSMART pre-processing ([Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md))
such as application identification. Rules within a map are evaluated in
priority order, and — critically — GigaVUE-OS supports both **pass** and
**drop** rule actions within the same map, allowing an operator to express
"forward everything except this excluded subset" as a small number of
drop rules ahead of a broader pass rule, rather than enumerating every
permitted combination explicitly.

```text
rule 10  drop   ipv4 destination-port 123        (exclude NTP chatter)
rule 20  drop   ipv4 destination-port 53          (exclude routine DNS)
rule 30  pass   any                               (forward everything else)
```

Rule order matters the same way it does in a firewall policy ([Volume X](../../volume-10-enterprise-cybersecurity/README.md),
[Volume XVI](../../volume-16-palo-alto-networks-security/README.md)) or an access control list ([Volume II](../../volume-02-network-engineering-foundations/README.md), [Volume III](../../volume-03-cisco-enterprise-networking/README.md)): the first
matching rule wins, and a broad pass rule placed before a narrower drop
rule silently defeats the drop rule's intent. This is the single most
common Flow Mapping authoring mistake and is covered further in
Validation and Troubleshooting.

### First-level and second-level maps (map chaining)

A single map can forward directly from a network port to a tool port, but
non-trivial fabrics commonly chain maps in two levels:

1. **First-level maps** perform initial filtering close to the
   acquisition point — narrowing a high-volume source down to the subset
   of traffic that might need further processing.
2. **Second-level maps** take the first-level map's output as their
   source and apply GigaSMART processing ([Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md)) — slicing, masking,
   deduplication, decryption — before final delivery to tool ports.

This two-level pattern keeps GigaSMART processing capacity (a finite,
licensed resource) focused only on traffic that survived first-level
filtering, rather than spending processing cycles on traffic that will be
dropped anyway.

```text
Network port 1/1/x1 ──▶ [first-level map: filter to internal-subnet HTTPS]
                              │
                              ▼
                    [second-level map: GigaSMART SSL decrypt + mask PAN field]
                              │
                              ▼
                         Tool port 1/1/g4 (DLP appliance)
```

### GigaStream: solving tool-port oversubscription

[Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md) introduced the oversubscription problem: several high-speed
network links aggregated toward a smaller number of tool ports can exceed
any single tool port's capacity. **GigaStream** solves this by grouping
multiple physical tool ports into one logical load-balanced bundle — a
map's destination becomes the GigaStream group rather than a single port,
and GigaVUE-OS distributes flows across the group's member ports using a
hashing algorithm that keeps a given flow's packets consistently on the
same member port (preserving packet order within a flow, which matters to
most monitoring and security tools). A tool farm behind a GigaStream group
therefore scales horizontally: adding a member port and a corresponding
tool instance increases aggregate capacity without re-authoring the Flow
Map itself.

### Preserving source context: tagging

When traffic from many acquisition points is aggregated onto a shared set
of tool ports (or a shared GigaStream group), a downstream tool can lose
the ability to tell which original network segment a given packet came
from — a problem for any tool whose analysis or alerting depends on
source context (for example, an NDR platform correlating an alert back to
a specific site or VLAN). GigaVUE-OS addresses this with **source
tagging**, most commonly VLAN-based: a map can be configured to
insert or rewrite a VLAN tag identifying the original acquisition point
before forwarding to a shared tool destination, letting the tool (or an
upstream filter on the tool side) recover source context from the tag
without the fabric needing a dedicated, unshared tool port per
acquisition point.

## Design Considerations

- **Filter before you aggregate, not after.** Applying filtering at the
  first-level map — close to acquisition — keeps unnecessary traffic out
  of shared tool-port capacity and GigaSMART processing entirely, rather
  than forwarding everything and relying on the tool itself to discard
  what it doesn't need. This is both a cost and a resiliency decision:
  every byte filtered out at the first level is a byte that cannot
  contribute to oversubscription downstream.
- **Design rule order deliberately and document the intent.** A Flow Map
  with a dozen rules and no accompanying documentation of why each rule
  exists and in what order is a maintenance liability; treat map rule
  design with the same change-review discipline as firewall policy
  changes elsewhere in this encyclopedia — an unreviewed rule change can
  just as easily flood the wrong tool or silently withhold traffic a
  tool depends on.
- **Size GigaStream groups for headroom, not just current throughput.**
  A GigaStream group sized to exactly match today's aggregate tool-port
  demand leaves no room to add a network source or a burst in traffic
  without immediate oversubscription; provision at least one additional
  member port's worth of headroom where the platform and licensing allow.
- **Decide tagging strategy before scaling past a handful of acquisition
  points.** Retrofitting source tagging onto an already-large set of maps
  feeding a shared tool destination is disruptive; agree on a VLAN-tagging
  convention (which tag range identifies which site or segment) as part
  of the same design pass as the tap inventory in [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md).
- **Reserve first-level/second-level map chaining for cases that actually
  need GigaSMART processing.** Not every map needs a two-level chain —
  adding an unnecessary hop increases configuration complexity and
  troubleshooting surface without benefit for traffic that requires no
  transformation.

## Implementation and Automation

### Building a filtered regular map

```text
(admin) (config) # map alias dc1-web-tier-to-ids
(admin) (config map alias dc1-web-tier-to-ids) # type regular
(admin) (config map alias dc1-web-tier-to-ids) # source 1/1/x1
(admin) (config map alias dc1-web-tier-to-ids) # destination 1/1/g2
(admin) (config map alias dc1-web-tier-to-ids) # rule add priority 10 drop ipv4 destination-port 123
(admin) (config map alias dc1-web-tier-to-ids) # rule add priority 20 drop ipv4 destination-port 53
(admin) (config map alias dc1-web-tier-to-ids) # rule add priority 30 pass ipv4 destination-net 10.10.20.0/24
(admin) (config map alias dc1-web-tier-to-ids) # exit
(admin) (config) # write memory
```

### Chaining first-level and second-level maps

```text
# First-level: filter to internal HTTPS traffic bound for GigaSMART
(admin) (config) # map alias fl-internal-https
(admin) (config map alias fl-internal-https) # type regular
(admin) (config map alias fl-internal-https) # source 1/1/x2
(admin) (config map alias fl-internal-https) # destination gsgroup1
(admin) (config map alias fl-internal-https) # rule add priority 10 pass ipv4 destination-port 443
(admin) (config map alias fl-internal-https) # exit

# Second-level: GigaSMART-processed output to the DLP tool
(admin) (config) # map alias sl-dlp-delivery
(admin) (config map alias sl-dlp-delivery) # type regular
(admin) (config map alias sl-dlp-delivery) # source gsgroup1
(admin) (config map alias sl-dlp-delivery) # destination 1/1/g4
(admin) (config map alias sl-dlp-delivery) # rule add priority 10 pass any
(admin) (config map alias sl-dlp-delivery) # exit
(admin) (config) # write memory
```

### Configuring a GigaStream tool group

```text
(admin) (config) # gigastream alias tool-farm-ndr
(admin) (config gigastream alias tool-farm-ndr) # member 1/1/g5
(admin) (config gigastream alias tool-farm-ndr) # member 1/1/g6
(admin) (config gigastream alias tool-farm-ndr) # member 1/1/g7
(admin) (config gigastream alias tool-farm-ndr) # hash-method 5-tuple
(admin) (config gigastream alias tool-farm-ndr) # exit

(admin) (config) # map alias dc1-agg-to-ndr-farm
(admin) (config map alias dc1-agg-to-ndr-farm) # type regular
(admin) (config map alias dc1-agg-to-ndr-farm) # source 1/1/x1
(admin) (config map alias dc1-agg-to-ndr-farm) # destination gigastream tool-farm-ndr
(admin) (config map alias dc1-agg-to-ndr-farm) # rule add priority 10 pass any
(admin) (config map alias dc1-agg-to-ndr-farm) # exit
(admin) (config) # write memory
```

### Applying source tagging

```text
(admin) (config map alias dc1-agg-to-ndr-farm) # egress-vlan-tag 210
(admin) (config map alias dc1-agg-to-ndr-farm) # exit
(admin) (config) # write memory
```

A downstream tool (or a filter on the tool's ingest pipeline) can then
distinguish traffic tagged VLAN 210 as originating from the DC1
aggregation point, even though it arrives interleaved with traffic from
other acquisition points sharing the same GigaStream group.

> As with prior chapters, exact CLI keyword syntax and GigaVUE-FM UI
> workflow for map and GigaStream authoring can vary between GigaVUE-OS
> and GigaVUE-FM releases; verify against the documentation for the
> specific release in use.

## Validation and Troubleshooting

- **A drop rule appears to have no effect.** Check rule priority order
  first — a broader pass rule with a lower priority number (evaluated
  earlier) than the intended drop rule will match and forward the traffic
  before the drop rule is ever evaluated. This is the most common Flow
  Mapping defect and is functionally identical to an out-of-order ACL or
  firewall rule. Re-order the rule list so the drop rule evaluates first,
  and validate against the affected tools before deploying the change
  more broadly.
- **A tool receives less traffic than expected after adding a GigaStream
  member.** Confirm the hash method is consistent and that existing flows
  were not expected to rebalance — most hash methods intentionally keep
  an established flow pinned to its original member port to preserve
  packet order, so adding capacity primarily benefits new flows, not
  already-established long-lived sessions.
- **Tool-port drops under load despite GigaStream being configured.**
  Confirm the GigaStream group's aggregate member bandwidth genuinely
  exceeds the offered load; GigaStream distributes load across existing
  members but does not increase the group's total capacity beyond the
  sum of its members — the fix is adding member ports (and matching tool
  capacity), not re-tuning the hash method.
- **A shared tool cannot distinguish traffic from two different sites.**
  Confirm source tagging (VLAN or equivalent) is actually applied on
  every map feeding that shared destination; a map added later that
  forgets to apply the organization's tagging convention is a common
  regression as a fabric grows.
- **Second-level map shows no traffic despite a healthy first-level map.**
  Confirm the first-level map's destination correctly references the
  GigaSMART group or intermediate construct the second-level map expects
  as its source — a mismatched intermediate identifier breaks the chain
  silently rather than producing an obvious error.

## Security and Best Practices

- Apply the same change-review rigor to Flow Mapping rule changes as to
  firewall policy changes — an overly broad pass rule or a misordered
  drop rule can either flood a tool with irrelevant traffic (masking
  genuine signal) or, worse, silently withhold traffic a security tool
  was depending on.
- Avoid `map-passall` in production delivery paths except where a tool
  genuinely requires a fully unfiltered copy; a passall map bypasses the
  filtering discipline that keeps sensitive data scoped only to the tools
  that need it.
- Apply source tagging consistently across every map feeding a shared
  tool destination, and audit for gaps periodically — an untagged source
  sharing a destination with tagged sources undermines the ability to
  attribute traffic during an investigation.
- Document the intent of every rule in a map (even informally, in the map
  alias naming convention or accompanying change record) so a future
  operator can distinguish a deliberate exclusion from an oversight.
- Periodically review maps for rules referencing decommissioned
  acquisition points or retired tools; stale map entries are both a
  configuration-hygiene and a minor information-exposure risk if a
  decommissioned tool port is later repurposed without the old rule being
  removed first.

## References and Knowledge Checks

**References**

- [Gigamon, *Flow Mapping* product page and *Flow Mapping FAQ*](https://www.gigamon.com/products/optimize-traffic/traffic-intelligence/gigavue-os/flow-mapping.html) —
  map types, rule model, and chaining concepts.
- [Gigamon, *GigaStream* product page](https://www.gigamon.com/products/optimize-traffic/traffic-intelligence/gigavue-os/gigastream.html) — load-balanced tool-group
  architecture.
- [Gigamon, *GigaVUE-OS CLI Reference*](https://docs.gigamon.com/doclib/Content/GV-OS-CLI/GV_OS_CLI_Home.html) — map, gigastream, and rule command
  syntax for the release in use.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline.

**Knowledge checks**

1. What is the practical difference between `map`, `map-passall`, and
   `map-scollector`, and when would an operator choose each?
2. Why does rule order matter in Flow Mapping, and what failure mode
   results from placing a broad pass rule ahead of a narrower drop rule?
3. Explain how GigaStream solves tool-port oversubscription without
   requiring the operator to re-author the Flow Map every time a member
   port is added.
4. Why does aggregating traffic from multiple acquisition points onto a
   shared tool destination create a need for source tagging?

## Hands-On Lab

**Objective:** Build a two-level filtered Flow Map feeding a GigaStream
tool group with source tagging applied, on a lab GigaVUE node from
[Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) or 03, and validate both correct filtering behavior and a
deliberate rule-order defect.

**Prerequisites**

- A lab GigaVUE node (physical or virtual) with at least two network-port
  traffic sources and three tool-port-equivalent destinations available
  (or simulated with a lab packet generator and multiple capture
  listeners).
- Access to GigaVUE-FM or direct CLI access to the lab node.
- A packet capture tool for each simulated tool-port destination.

**Steps**

1. Configure a first-level map filtering one network source down to a
   specific subnet or port range of interest, following the pattern in
   Implementation and Automation.
2. Configure a GigaStream group with two member tool ports, and a
   second-level map forwarding the first-level map's output to the
   GigaStream group.
3. Apply an egress source tag (VLAN tag) to the second-level map.
4. Generate lab traffic matching the first-level filter criteria (for
   example, traffic to the configured subnet or port).
5. Confirm traffic appears at both capture tools connected to the
   GigaStream group's member ports, and confirm the expected VLAN tag is
   present.
   **Expected result:** traffic is visible at the tool farm with the
   correct source tag, confirming the two-level chain and GigaStream
   distribution both function.
6. Generate lab traffic that does **not** match the first-level filter
   (for example, traffic to an excluded port).
   **Expected result:** no corresponding traffic appears at either
   capture tool, confirming the first-level filter correctly excludes
   non-matching traffic before it reaches GigaStream.
7. **Negative test:** intentionally introduce a rule-order defect by
   adding a broad `pass any` rule at a lower priority number (evaluated
   before) the first-level map's existing filter rule, then re-run the
   excluded-traffic test from step 6.

   ```text
   (admin) (config map alias fl-internal-https) # rule add priority 5 pass any
   ```

   **Expected result:** the previously excluded traffic now appears at
   the tool farm, reproducing the rule-order failure mode described in
   Validation and Troubleshooting.
8. Remove the defect rule and confirm the excluded-traffic test from
   step 6 passes again.

   ```text
   (admin) (config map alias fl-internal-https) # no rule add priority 5 pass any
   ```

9. **Cleanup:** remove the lab maps and GigaStream group if the node will
   be reused for later chapters' exercises, or leave them in place with
   clear naming if they will serve as a foundation for [Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md)'s
   GigaSMART exercises.

## Summary and Completion Checklist

Flow Mapping is the rule engine that decides which traffic reaches which
tool, and its correctness depends on disciplined rule ordering, deliberate
filtering close to the acquisition point, and — once traffic from
multiple sources shares tool-port capacity — GigaStream load balancing
and source tagging to preserve both throughput and context. These
mechanics are the operational core of a Gigamon fabric and the foundation
[Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md)'s GigaSMART processing builds directly on top of.

- [ ] Can explain the three common map types and when each is
      appropriate.
- [ ] Can design a rule set with correct priority ordering, including
      pass/drop interaction.
- [ ] Can configure a GigaStream tool group and explain how it resolves
      oversubscription.
- [ ] Can apply source tagging and explain why it matters once tool ports
      are shared across acquisition points.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
