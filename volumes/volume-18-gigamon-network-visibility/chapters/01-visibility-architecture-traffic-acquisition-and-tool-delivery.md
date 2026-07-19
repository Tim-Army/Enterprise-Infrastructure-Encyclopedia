# Chapter 01: Visibility Architecture, Traffic Acquisition, and Tool Delivery

## Learning Objectives

- Explain why a dedicated visibility fabric exists between the production
  network and the security/monitoring tool ecosystem, and what problems it
  solves that SPAN ports alone cannot.
- Describe the three logical planes of a Gigamon deployment — traffic
  acquisition, the visibility fabric, and tool delivery — and how GigaVUE
  nodes and GigaVUE-FM fit into each.
- Differentiate TAP-based and SPAN-based acquisition, and state the
  trade-offs of each.
- Explain many-to-many traffic mapping: N:1 aggregation, 1:N replication,
  and tool chaining, and why they reduce tool sprawl and port cost.
- Identify the physical and virtual node families that make up the GigaVUE
  portfolio and where each fits in an enterprise topology.

## Theory and Architecture

### The blind-spot problem

Every enterprise network eventually accumulates a long list of tools that
need a copy of live traffic to do their job: an intrusion detection system
(IDS), a network detection and response (NDR) platform, a data loss
prevention (DLP) appliance, an application performance monitoring (APM)
probe, a packet capture and forensics platform, a network performance
management (NPM) tool, and often several generations of all of the above
as the organization evolves. Each of these tools traditionally wanted its
own tap point on the network — its own SPAN session, its own physical
cable run, its own port on a switch that was never designed to be a
distribution point for a dozen consumers.

This creates two compounding problems. First, **SPAN port scarcity**: a
typical access or core switch has a small number of monitor sessions
available, and every additional tool competes for that same limited
resource, often forcing operators to choose which tool gets visibility into
which segment rather than giving every tool visibility into everything it
needs. Second, **production risk**: a SPAN session runs on production
switching hardware, competing for the same ASIC resources, backplane
bandwidth, and CPU cycles as the traffic the switch is actually there to
forward. A misconfigured monitor session, or a monitoring tool that floods
a SPAN destination, can degrade the very traffic it was meant to observe.

A visibility fabric — the architecture Gigamon builds — solves both
problems by inserting a dedicated layer of purpose-built hardware and
software between the points where traffic can be copied from the network
and the tools that consume those copies. That layer acquires traffic once
per tap point, and then maps, filters, transforms, and replicates it to as
many tools as need it, independent of production switching capacity and
without adding load to production network elements.

### Three logical planes

A Gigamon deployment is best understood as three logical planes, each
covered in depth by a later chapter in this volume:

1. **Traffic acquisition** — the physical and virtual mechanisms that
   obtain a copy of network traffic without altering the original path:
   optical/copper TAPs, SPAN/mirror ports, and virtual taps inside
   hypervisors, cloud VPCs, and container platforms. This chapter and
   [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md) cover acquisition in depth.
2. **The visibility fabric** — the GigaVUE nodes (physical appliances and
   virtual nodes) and the GigaSMART traffic-intelligence engine that
   receive acquired traffic, apply Flow Mapping rules, optionally
   transform the traffic (slicing, masking, deduplication, decryption),
   and forward it toward tool ports. GigaVUE-FM is the centralized control
   plane for this fabric. Chapters 02–06 cover the fabric.
3. **Tool delivery** — the mechanisms that get the right traffic, in the
   right volume and format, to each connected tool: load-balanced tool
   groups (GigaStream), VLAN or header tagging that preserves source
   context, and inline arrangements for tools that must sit directly in
   the traffic path. Chapters 05 and 07 cover delivery mechanics in depth.

Traffic flows through these planes in one direction for out-of-band (OOB)
monitoring tools — acquisition into the fabric, fabric out to tools — and
bidirectionally, in-path, for inline security tools such as intrusion
prevention systems (IPS) that must be able to block or modify a packet
before it reaches its destination. Both models exist within the same
physical fabric; [Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md) covers inline design specifically.

### TAP versus SPAN acquisition

| Characteristic | Physical TAP | SPAN / mirror port |
| --- | --- | --- |
| Traffic fidelity | Full line-rate copy, including physical-layer errors and micro-bursts | Subject to switch ASIC mirroring priority; can silently drop under load |
| Production impact | None — a passive optical/copper TAP does not consume switch CPU or backplane capacity | Consumes switch resources; a busy switch can throttle or disable a SPAN session |
| Visibility to Layer 1/2 errors | Yes (CRC errors, runts, physical-layer faults are copied) | No — the switch typically discards frames with these characteristics before mirroring |
| Full-duplex capture | Requires either an aggregating TAP or two fabric network ports (one per direction) | A single SPAN destination naturally interleaves both directions |
| Points of presence | Requires physical insertion at every link to be observed | Reuses existing switch mirror capability, no cabling change |
| Typical use | Core, WAN edge, data center aggregation links, inline security segments | Access-layer and lower-priority links where TAP insertion is impractical |

Neither method is universally superior; most mature Gigamon deployments use
both. Physical TAPs are the default choice for high-value links — data
center interconnects, internet edge, and any segment where a security team
cannot tolerate a switch silently dropping traffic under mirroring load.
SPAN is retained where physical TAP insertion is operationally difficult
(for example, a remote-office access switch with no scheduled maintenance
window) or where the visibility requirement is lower-stakes.

### The aggregation and replication problem

Once traffic is acquired from dozens or hundreds of tap points, the fabric
must solve a many-to-many mapping problem:

- **N:1 aggregation.** Traffic from many network ports (many tap points)
  is aggregated onto a smaller number of tool ports, because most tools do
  not need a dedicated physical connection per tap point — an IDS sensor
  that can process 40 Gbps of traffic can reasonably consume the
  aggregated output of a dozen 1 Gbps or 10 Gbps access links.
- **1:N replication.** A single tap point's traffic is often needed by
  several tools simultaneously — the same data center interconnect link
  might feed a packet capture platform, an NDR sensor, and a DLP appliance
  concurrently, each seeing an identical copy.
- **Filtered delivery.** Not every tool needs every byte. A DLP appliance
  may only need traffic matching specific applications or subnets, while a
  packet capture platform may need everything. The fabric applies
  per-tool filtering so each tool receives only the traffic relevant to
  its function, reducing tool licensing cost (many security tools are
  licensed by ingested throughput) and tool CPU load.
- **Tool chaining.** Traffic can be forwarded from one inline or
  out-of-band tool to the next in a defined sequence, rather than the
  fabric replicating the same traffic to every tool independently — useful
  when one tool's output (for example, a decryption engine) is a
  precondition for a downstream tool's input.

This N:M mapping is implemented by **Flow Mapping**, the packet-forwarding
rule engine built into every GigaVUE node's operating system (GigaVUE-OS)
and centrally authored through GigaVUE-FM. Flow Mapping is covered in
architectural depth in [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md).

### The GigaVUE portfolio at a glance

| Component | Role | Covered in |
| --- | --- | --- |
| GigaVUE TA Series | Fixed-configuration, COTS-switch-based traffic aggregation nodes; high port density at the acquisition edge | [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) |
| GigaVUE HC Series (HCT, HC1, HC1-Plus, HC3) | Modular/chassis-capable nodes hosting GigaSMART traffic-intelligence engines | [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) |
| GigaVUE V Series (virtual nodes) | Software visibility nodes for hypervisors, private cloud, and public cloud VPCs | [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md) |
| GigaVUE Cloud Suite / Universal Cloud Tap (UCT) | Cloud-native and container tapping for AWS, Azure, GCP, OpenStack, and Kubernetes | [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md) |
| GigaVUE-FM | Centralized fabric manager: configuration, Flow Mapping authoring, RBAC, licensing, monitoring, and REST API | [Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md) |
| GigaSMART | Traffic-intelligence processing engine: slicing, masking, deduplication, metadata generation, SSL/TLS decryption | [Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md) |

## Design Considerations

- **Start from the tool inventory, not the topology.** Before designing tap
  points, enumerate every tool that currently — or will soon — need a copy
  of traffic, its required throughput, whether it must see full packets or
  can consume sampled/metadata traffic, and whether it must operate inline
  or out-of-band. Sizing the fabric around today's SPAN sessions and
  retrofitting tools later leads to under-provisioned tool ports.
- **Segment by criticality, not convenience.** Internet edge, data center
  interconnects, and any segment carrying regulated data typically justify
  physical TAPs; lower-value access segments can often run on SPAN until
  a maintenance window allows TAP insertion.
- **Plan for oversubscription early.** Aggregating several 10/25/40 Gbps
  network links onto a shared set of tool ports is normal, but the fabric
  operator must consciously decide how oversubscription is handled — via
  filtering (send only relevant traffic), via GigaStream load balancing
  across multiple tool-port members, or via GigaSMART traffic reduction
  (slicing, deduplication) — rather than allowing silent drops at a
  saturated tool port.
- **Decide inline scope deliberately.** Only traffic that must be blocked
  or modified in real time (IPS, inline DLP enforcement, inline
  decryption for downstream OOB tools) belongs on an inline path. Placing
  a tool inline that does not require it introduces an unnecessary
  single point of failure into the production path; [Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md) covers the
  resiliency mechanisms (bypass, heartbeat) that make inline deployment
  safe when it is genuinely required.
- **Model growth in tap points, not just throughput.** A fabric sized for
  today's port count but with no free network or tool ports on the nodes
  themselves forces a forklift upgrade at the first expansion request.
  Reserve headroom on physical nodes and license capacity on GigaVUE-FM
  for the growth already on the infrastructure roadmap.

## Implementation and Automation

Formal implementation begins in [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) (physical node deployment) and
[Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md) (GigaVUE-FM), but the acquisition-layer decisions below are made
before any node is racked, because they determine cabling and site
requirements.

### Choosing and placing a TAP

A typical enterprise TAP deployment follows this sequence:

1. Identify the physical link to observe (for example, the uplink between
   a data center distribution switch and the core).
2. Select a TAP appropriate to the media and speed — optical TAPs split a
   fraction of the light signal to two monitor ports (one per direction)
   without any active component in the production path; copper TAPs are
   typically active (repeating) devices because a passive electrical split
   degrades signal integrity at 1 Gbps and above.
3. Insert the TAP in-line with the production link during a maintenance
   window. A TAP failure mode should be fail-safe for the **production**
   link (traffic continues to flow between the two production ports even
   if the TAP loses power), which is a property of purpose-built network
   TAPs and a key differentiator from simply looping through an
   unmanaged device.
4. Cable both monitor ports (A and B directions) to network ports on a
   GigaVUE node.

```text
Production switch A ──▶ [ TAP ] ──▶ Production switch B
                           │    │
                    (Tx copy) (Rx copy)
                           ▼    ▼
                    GigaVUE network port 1/1/x1  (A → B direction)
                    GigaVUE network port 1/1/x2  (B → A direction)
```

### Choosing and configuring a SPAN session

Where a TAP is not yet feasible, a SPAN/mirror session on the source
switch is configured to send a copy of one or more source interfaces (or a
VLAN) to a destination interface that is cabled to a GigaVUE network port.
Exact SPAN syntax is switch-platform-specific (see [Volume III](../../volume-03-cisco-enterprise-networking/README.md) for Cisco
IOS XE monitor-session configuration); regardless of platform, record the
following for every SPAN session created for Gigamon acquisition:

- Source interface(s) or VLAN(s) being mirrored.
- Direction mirrored (ingress, egress, or both) — mirroring both
  directions of a full-duplex link onto a single destination port can
  itself cause oversubscription on the SPAN destination if the source
  link is heavily utilized in both directions simultaneously.
- The destination switch port and the GigaVUE network port it connects to,
  recorded in the fabric's port-mapping documentation ([Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md)
  introduces the node/slot/port addressing scheme used throughout this
  volume).

### Mapping the tap inventory

Every organization operating a Gigamon fabric should maintain a
version-controlled inventory mapping each acquisition point to its
GigaVUE network port, acquisition method (TAP or SPAN), and the tools
subscribed to that traffic. A minimal structure:

```yaml
# tap-inventory.yaml
- tap_id: dc1-core-agg-01
  method: optical_tap
  link_description: "DC1 Core to Aggregation, 40G"
  gigavue_node: hc3-dc1-fab01
  network_ports: ["1/1/x1", "1/1/x2"]
  subscribed_tools:
    - ndr-sensor-01
    - packet-capture-01
- tap_id: branch12-access-uplink
  method: span
  link_description: "Branch 12 access switch uplink"
  gigavue_node: ta200-branch-hub
  network_ports: ["1/1/c4"]
  subscribed_tools:
    - ids-sensor-branch
```

This inventory becomes the source of truth reconciled against GigaVUE-FM's
live configuration ([Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md) covers GigaVUE-FM's REST API and how to
automate that reconciliation) and prevents "mystery cables" — TAPs or SPAN
sessions nobody can explain — from accumulating over the fabric's life.

## Validation and Troubleshooting

- **No traffic at the tool despite a configured tap.** Confirm the TAP or
  SPAN source is actually carrying traffic (check switch interface
  counters first), then confirm the GigaVUE network port shows incrementing
  receive counters (`show port stats` in GigaVUE-OS CLI or the equivalent
  GigaVUE-FM port statistics view). A silent zero at the network port
  usually points to a cabling or SPAN-direction misconfiguration rather
  than a fabric mapping problem.
- **Partial traffic loss under load.** If a SPAN-sourced tap shows gaps
  correlated with switch CPU or ASIC utilization spikes, the switch is
  deprioritizing the mirror session under load — this is expected SPAN
  behavior, not a fabric fault, and is the strongest argument for
  migrating that link to a physical TAP.
- **Duplicate or asymmetric traffic.** A full-duplex TAP cabled to only
  one network port (instead of both A and B directions) will show only
  one direction of a conversation at the tool, which some tools interpret
  as broken sessions. Confirm both TAP monitor ports are cabled and mapped.
- **Tool receiving unexpected traffic volume.** Before assuming a fabric
  mapping error, confirm whether the tap point itself changed — a new
  VLAN trunked onto an already-tapped uplink, or a new SPAN source added
  by another team without updating the tap inventory, is a more common
  root cause than a Flow Mapping misconfiguration.

## Security and Best Practices

- Treat the tap inventory as sensitive documentation — it is effectively a
  map of where an adversary could intercept traffic if fabric access were
  compromised, and belongs in an access-controlled repository, not a
  shared drive.
- Physically secure TAP insertion points and GigaVUE node management
  interfaces to the same standard as the production network gear they
  observe; a visibility fabric that touches regulated data inherits that
  data's compliance scope.
- Prefer TAPs over SPAN for any link carrying data subject to regulatory
  retention or chain-of-custody requirements (payment card data, health
  records, classified or controlled unclassified information), because
  SPAN's potential for silent drop under load undermines evidentiary
  completeness.
- Restrict who can create or modify SPAN sessions on production switches
  feeding the visibility fabric; an unauthorized SPAN change is both a
  production-risk and a data-exposure event.
- Document acquisition points that carry traffic to inline (in-path)
  security tools separately from purely out-of-band taps, since inline
  paths carry additional availability risk covered in [Chapter 07](07-inline-bypass-tls-decryption-and-production-safety.md).

## References and Knowledge Checks

**References**

- Gigamon, *GigaVUE-OS and GigaVUE-FM Documentation Library* —
  architecture and Flow Mapping overview.
- Gigamon, *GigaVUE Fabric Management Data Sheet* — GigaVUE-FM capability
  summary.
- Gigamon, *Flow Mapping* product page — mapping engine concepts and
  terminology.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline.

**Knowledge checks**

1. What two production risks does a dedicated visibility fabric remove
   compared to relying on SPAN ports alone for every monitoring tool?
2. Name one scenario favoring a physical TAP and one scenario where a SPAN
   session is the more practical choice.
3. Explain the difference between N:1 aggregation and 1:N replication in
   Flow Mapping, and give a one-sentence example of each.
4. Why should a tap inventory be treated as access-controlled
   documentation rather than general reference material?

## Hands-On Lab

**Objective:** Design and document a small visibility fabric acquisition
plan for a simulated two-segment network, then validate the plan's logic
with a tabletop trace of expected traffic flow — no physical GigaVUE
hardware is required for this planning-level lab (physical configuration
begins in [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md)).

**Prerequisites**

- A text editor and a local Git-tracked scratch directory (or the
  `tap-inventory.yaml` pattern shown above).
- A simple network diagram: one core switch, one access switch feeding a
  server VLAN, and one internet edge router — hand-drawn or produced with
  any diagramming tool is sufficient.

**Steps**

1. On your diagram, mark two candidate acquisition points: the uplink
   between the access switch and the core (a candidate SPAN source), and
   the internet edge router's WAN-facing link (a candidate TAP point).
2. For each acquisition point, write one sentence justifying the
   acquisition method chosen, referencing the TAP-vs-SPAN comparison table
   in this chapter (for example: "internet edge — physical TAP, because
   loss of visibility during a security incident is unacceptable and the
   link is business-critical").
3. Create a `tap-inventory.yaml` file following the schema shown in
   Implementation and Automation, with one entry per acquisition point.
   Assign each a placeholder `gigavue_node` name and at least one
   `subscribed_tools` entry (for example, an IDS sensor and a packet
   capture platform).
4. For the internet-edge TAP entry, add both monitor-port directions
   (`network_ports: ["1/1/x1", "1/1/x2"]`) and note in a comment which
   port carries inbound versus outbound traffic.
5. **Validate the plan with a tabletop trace:** pick a hypothetical
   outbound HTTPS session from an internal server to an external host.
   Trace it on paper through both acquisition points and confirm your
   inventory correctly shows it visible to every tool that should see it
   (both the IDS at the internet edge and the packet capture tool per
   your entries).
   **Expected result:** the trace confirms every subscribed tool in your
   inventory has a documented, unbroken acquisition path to the session;
   any tool without a path indicates a missing acquisition point or
   subscription entry.
6. **Negative test:** remove the `network_ports` entry for one direction
   of the internet-edge TAP and re-run the tabletop trace for a
   bidirectional session (for example, a TCP handshake). Confirm — and
   write down — that the trace now shows only one direction of traffic
   reaching the tools, reproducing the asymmetric-visibility failure mode
   described in Validation and Troubleshooting. Restore the removed entry
   afterward.
7. **Cleanup:** none required beyond retaining or discarding your
   `tap-inventory.yaml` scratch file; no production or lab infrastructure
   was touched in this lab.

## Summary and Completion Checklist

A Gigamon visibility fabric exists to solve two problems SPAN-only
designs cannot: limited mirror-session capacity and the production risk
of running monitoring on switching hardware that was never sized for it.
Understanding the three logical planes — acquisition, fabric, and tool
delivery — and the many-to-many mapping problem they solve (N:1
aggregation, 1:N replication, filtered delivery, tool chaining) is the
conceptual foundation the rest of this volume builds on, starting with
physical node deployment in [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md).

- [ ] Can explain why a dedicated visibility fabric reduces both tool
      sprawl and production risk compared to SPAN-only designs.
- [ ] Can describe the three logical planes of a Gigamon deployment and
      name the primary component in each.
- [ ] Can choose between TAP and SPAN acquisition for a given link based
      on criticality and operational constraints.
- [ ] Can explain N:1 aggregation, 1:N replication, and tool chaining with
      an example of each.
- [ ] Completed the hands-on lab, including the negative test.
