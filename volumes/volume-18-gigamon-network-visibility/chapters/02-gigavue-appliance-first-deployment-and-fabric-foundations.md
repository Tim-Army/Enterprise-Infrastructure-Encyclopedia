# Chapter 02: GigaVUE Appliance First Deployment and Fabric Foundations

## Learning Objectives

- Identify the physical GigaVUE node families (TA Series and HC Series),
  their form factors, and the deployment role each is suited to.
- Perform first-touch console access and initial network configuration on
  a physical GigaVUE node using GigaVUE-OS CLI.
- Explain GigaVUE-OS port addressing (box/slot/port) and the difference
  between network, tool, hybrid, and stack port roles.
- Form a basic cluster of GigaVUE nodes and explain why clustering matters
  for fabric-wide Flow Mapping.
- Apply a first, minimal Flow Map to confirm traffic moves from a network
  port to a tool port before handing the node off to GigaVUE-FM management
  in Chapter 04.

## Theory and Architecture

### The physical node families

Gigamon's physical visibility nodes fall into two series with distinct
design goals:

- **GigaVUE TA Series.** Fixed-configuration, commercial-off-the-shelf
  (COTS) switch-ASIC-based nodes optimized for high port density and
  line-rate aggregation at the acquisition edge. TA Series nodes (for
  example, the TA25, TA40, TA100, and TA200 class of platforms, spanning
  1 Gb through 100 Gb port speeds) do not host GigaSMART processing
  engines; they perform Flow Mapping — filtering, aggregation, and
  replication — at wire speed in hardware, and are the typical first hop
  for high-density access and aggregation-layer tapping.
- **GigaVUE HC Series.** The HCT, HC1, HC1-Plus, and HC3 platforms add the
  ability to host one or more **GigaSMART** traffic-intelligence engines
  (Chapter 06) alongside Flow Mapping. The HC3 is the highest-capacity,
  most port-dense platform in the family and supports multiple GigaSMART
  engines per chassis; the HC1 and HC1-Plus are compact 1RU platforms for
  small-to-mid-sized deployments and distributed sites; the HCT is a
  half-width, low size/weight/power (SWaP) platform built for edge,
  mobile, and tactical deployments.

A common design pattern places TA Series nodes at high-density acquisition
points (top-of-rack, access aggregation) and feeds their tool-port output
into HC Series nodes over stack links, so that GigaSMART processing — which
only HC Series nodes provide — is applied centrally rather than replicated
at every acquisition point. This is not a mandatory topology, but it is the
most common cost-efficient pattern once GigaSMART features (deduplication,
masking, decryption) are required.

### GigaVUE-OS: the node operating system

Every physical (and virtual) GigaVUE node runs **GigaVUE-OS**, which
exposes a CLI with an operational mode and a configuration mode, similar in
spirit to other network-operating-system CLIs an infrastructure engineer
will already be familiar with from Volume III. GigaVUE-OS is the layer
responsible for port management, Flow Mapping rule enforcement, GigaSMART
application configuration on capable platforms, and clustering. GigaVUE-FM
(Chapter 04) is a management layer on top of GigaVUE-OS — it does not
replace the CLI, and experienced operators frequently use both: GigaVUE-FM
for fabric-wide visibility and bulk operations, and the CLI for
node-local troubleshooting and initial bring-up.

### Port addressing and roles

GigaVUE-OS addresses ports using a `box/slot/port` (or `box/bay/port` on
modular platforms) convention, commonly rendered as, for example,
`1/1/x1` for box 1, slot 1, port x1. Ports are assigned one of several
roles:

| Port role | Purpose |
| --- | --- |
| Network port | Ingress from a TAP or SPAN destination — traffic entering the fabric |
| Tool port | Egress toward a connected out-of-band monitoring or security tool |
| Hybrid port | Configurable as either a network or a tool port, adding deployment flexibility on fixed-port platforms |
| Stack port | Interconnects two or more GigaVUE nodes so Flow Mapping can span node boundaries as a single logical fabric |
| Inline network / inline tool port | Used specifically for inline bypass deployments (Chapter 07); carries bidirectional production traffic through an in-path tool |

A port's role and administrative state (enabled/disabled, speed,
auto-negotiation) are configured before it participates in any Flow
Mapping rule, and changing a port's role after it is referenced by an
active map requires removing that reference first — GigaVUE-OS will not
silently reassign a port role out from under a live map.

### Why clustering matters

A single GigaVUE node has a finite number of physical ports. As an
enterprise visibility fabric grows past what one chassis can host,
multiple nodes are interconnected over stack ports and joined into a
**cluster** — a group of nodes that GigaVUE-FM (and, for basic operations,
the CLI of a designated leader node) treats as a single logical fabric.
Clustering matters for two reasons beyond simple port-count scaling:

1. **Fabric-wide Flow Mapping.** A map can reference a network port on one
   physical node and a tool port on another node in the same cluster —
   traffic acquired at a remote acquisition node can be forwarded across
   stack links to a centralized tool farm without the operator manually
   engineering the intermediate hop-by-hop path for every rule.
2. **Centralized operational visibility.** A cluster reports consolidated
   health, licensing, and statistics to GigaVUE-FM as one fabric entity,
   which is materially easier to operate than a set of independently
   managed boxes at scale.

Clustering requires stack ports to be cabled with sufficient bandwidth to
carry the aggregate cross-node traffic a map might generate — under-sized
stack links are a common source of unexpected drops once a fabric grows
past a single chassis, and stack-link capacity planning belongs in the
same design pass as tool-port oversubscription planning from Chapter 01.

## Design Considerations

- **Right-size the node family to the acquisition point, not the whole
  fabric.** A high-density access aggregation point is usually better
  served by a TA Series node feeding a centralized HC Series node than by
  an HC Series node at every edge location — GigaSMART licensing and
  processing capacity are worth concentrating rather than distributing
  thinly.
- **Reserve stack and hybrid ports up front.** Configuring every physical
  port as a network or tool port on day one leaves no headroom to add
  cluster members or convert a port's role later without a maintenance
  window. Reserve at least one hybrid or stack-capable port pair per node
  during initial deployment planning.
- **Plan management-network placement before racking.** GigaVUE-OS
  management access (CLI over SSH/console, and the interface GigaVUE-FM
  uses to reach the node) belongs on an out-of-band management network,
  consistent with how any other infrastructure control plane is isolated
  — never on the same VLAN as acquired traffic.
- **Decide the cluster's leader/standby model early.** A cluster elects
  (or is configured with) a leader node that owns the fabric-wide control
  plane relationship with GigaVUE-FM; plan which physical node is the
  leader based on placement (favor a node in a well-connected, resilient
  location) rather than defaulting to whichever node happened to be
  configured first.
- **Match licensing to the features actually needed at first cutover.**
  GigaVUE-OS advanced-feature licensing (extended map-rule counts,
  GigaSMART application licenses) is per-node; over-licensing every node
  identically is simpler to administer but often wastes budget compared
  to licensing GigaSMART features only on the HC Series nodes that will
  run them.

## Implementation and Automation

### First-touch console access

Physical GigaVUE nodes ship with console access via a serial port at the
standard default settings (9600 baud, 8 data bits, no parity, 1 stop bit,
no flow control). Console access is the recommended first-touch method
because it does not depend on any prior IP configuration.

```text
login: admin
password: <factory-default or documented initial password>
```

Change the default administrative credential immediately — this is
covered again in Security and Best Practices, but it is the first
operational action to take after console login on any new node.

### Entering configuration mode and setting management addressing

GigaVUE-OS CLI mirrors the operational-mode/configuration-mode pattern
common to enterprise network operating systems:

```text
(admin) # enable
(admin) # configure terminal
(admin) (config) # hostname hc3-dc1-fab01
(admin) (config) # mgmt ip address 10.20.10.5 /24
(admin) (config) # mgmt route add default 10.20.10.1
(admin) (config) # dns-server add 10.20.10.2
(admin) (config) # write memory
```

`write memory` persists the running configuration to non-volatile
storage — GigaVUE-OS, like most network operating systems, distinguishes
between the active running configuration and the saved/startup
configuration, and an uncommitted configuration is lost across a reload.

### Configuring port roles

```text
(admin) (config) # port 1/1/x1 params admin enable
(admin) (config) # port 1/1/x1 type network
(admin) (config) # port 1/1/x2 params admin enable
(admin) (config) # port 1/1/x2 type network
(admin) (config) # port 1/1/g1 params admin enable
(admin) (config) # port 1/1/g1 type tool
```

### Building a first, minimal Flow Map

Before handing a node to GigaVUE-FM for centralized management, confirm
basic connectivity with a minimal all-pass map — one that forwards every
packet arriving on a network port to a tool port, with no filtering. This
is the fastest way to prove the physical cabling, port roles, and node
health are correct before introducing filtering logic in Chapter 05.

```text
(admin) (config) # map alias first-touch-verify
(admin) (config map alias first-touch-verify) # type regular
(admin) (config map alias first-touch-verify) # source 1/1/x1
(admin) (config map alias first-touch-verify) # destination 1/1/g1
(admin) (config map alias first-touch-verify) # rule add pass any
(admin) (config map alias first-touch-verify) # exit
(admin) (config) # write memory
```

### Forming a two-node cluster

```text
# On the intended leader node:
(admin) (config) # cluster name dc1-visibility-fabric
(admin) (config) # cluster admin-password set
(admin) (config) # exit

# On the joining node, after cabling stack ports 1/1/q1 <-> 1/1/q1:
(admin) (config) # port 1/1/q1 type stack
(admin) (config) # cluster join dc1-visibility-fabric
```

Confirm cluster membership and health before proceeding:

```text
(admin) # show cluster
Cluster Name: dc1-visibility-fabric
Members: 2
  hc3-dc1-fab01 (leader)  -  healthy
  hc3-dc1-fab02 (member)  -  healthy
```

> Exact command syntax, prompts, and cluster-health output formatting can
> vary between GigaVUE-OS releases; treat the commands above as
> representative of the workflow and confirm against the documentation
> for the specific GigaVUE-OS release in use, consistent with the 6.x
> baseline recorded in [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md).

## Validation and Troubleshooting

- **Port shows administratively enabled but no link.** Confirm SFP/QSFP
  transceiver seating and cable type match the port's configured speed;
  `show port 1/1/x1` (or the equivalent GigaVUE-OS status command) reports
  link state, negotiated speed, and transceiver diagnostics, and is the
  first command to run before suspecting a Flow Mapping issue.
- **First-touch map shows zero packets forwarded.** Verify the network
  port referenced by the map is actually the port cabled to the TAP or
  SPAN destination (a swapped-cable or copy-paste port-ID error in the
  map definition is the most common cause), then confirm the map's rule
  is `pass any` and not an unintentionally narrow rule.
- **Cluster join fails or member shows unhealthy.** Confirm the stack
  port is configured with `type stack` on both ends and that a supported
  cable/transceiver combination is used at the stack link's negotiated
  speed; a stack port left in its default (typically network or tool)
  role will not establish cluster connectivity.
- **Configuration lost after a power cycle.** This almost always means
  `write memory` (or the equivalent save/commit action) was never issued
  after making changes — GigaVUE-OS, like other network operating
  systems in this encyclopedia, keeps the running and saved
  configurations distinct.
- **Management interface unreachable after an addressing change.**
  Exactly as with any network appliance, changing the management IP from
  an active SSH session drops that session on commit; always retain
  console access when changing management addressing on a node that is
  not yet redundantly reachable.

## Security and Best Practices

- Change default administrative credentials on first login, and create
  named, role-scoped administrator accounts for each engineer rather than
  sharing a single account — this becomes centrally enforceable once
  GigaVUE-FM's RBAC and directory integration are configured in Chapter 04,
  but do not leave a factory-default credential active in the interim.
- Place GigaVUE-OS management interfaces on a dedicated, access-controlled
  out-of-band management network, and restrict SSH/HTTPS management
  reachability to a known administrative subnet.
- Disable unused ports administratively rather than leaving them enabled
  with no role assigned; an enabled, unassigned port on a visibility node
  is unnecessary exposed surface.
- Record every port's role, connected device, and cluster membership in
  the same version-controlled inventory introduced in Chapter 01, so a
  node's configuration can be reconstructed or audited without relying on
  tribal knowledge.
- Apply firmware updates to GigaVUE-OS on a defined maintenance cadence,
  tracked against the baseline in
  [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md); do not run
  visibility-fabric nodes indefinitely on an end-of-support release,
  since they sit in the path of security-relevant traffic even when
  deployed purely out-of-band.
- Treat cluster administrative credentials as tier-0 infrastructure
  secrets — compromise of a cluster leader's credentials exposes Flow
  Mapping control for the entire fabric, not just one node.

## References and Knowledge Checks

**References**

- Gigamon, *GigaVUE HC Series Data Sheet* — HCT/HC1/HC1-Plus/HC3 platform
  specifications and GigaSMART engine capacity.
- Gigamon, *About the GigaVUE HC Series and GigaVUE TA Series* —
  platform overview and port-role documentation.
- Gigamon, *GigaVUE-OS CLI Reference* — full command syntax for the
  GigaVUE-OS release in use.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline (GigaVUE-OS versions are aligned to the same
  release train).

**Knowledge checks**

1. What distinguishes a TA Series node from an HC Series node, and why
   would an architect commonly feed TA Series tool-port output into a
   centralized HC Series node?
2. Name the four common port roles in GigaVUE-OS and give a one-sentence
   purpose for each.
3. Why does clustering matter beyond simply adding port count, and what
   physical prerequisite must be in place before two nodes can join the
   same cluster?
4. What is the practical risk of skipping `write memory` after making CLI
   configuration changes?

## Hands-On Lab

**Objective:** Perform first-touch configuration of a lab GigaVUE node
(physical or a lab/virtual GigaVUE-OS instance), configure network and
tool ports, and validate a minimal Flow Map moves traffic end to end,
including a deliberate misconfiguration to observe the resulting failure
mode.

**Prerequisites**

- A lab GigaVUE node with console or SSH access at a documented
  management address — a physical evaluation unit, or a virtual
  GigaVUE-OS lab instance if no physical hardware is available.
- A traffic source cabled or connected to a designated network port (a
  TAP, SPAN destination, or a simple lab packet generator).
- A packet capture tool (for example, `tcpdump` or Wireshark, covered in
  depth in Volume XX) connected to the designated tool port to observe
  forwarded traffic.
- An isolated lab network segment — do not perform this lab against a
  production visibility fabric.

**Steps**

1. Connect to console and log in with the default or documented initial
   credential.
2. Enter configuration mode and set the hostname and management
   addressing:

   ```text
   (admin) # configure terminal
   (admin) (config) # hostname gv-lab-node01
   (admin) (config) # mgmt ip address 10.50.10.5 /24
   ```

3. Configure one port as a network port and one as a tool port:

   ```text
   (admin) (config) # port 1/1/x1 params admin enable
   (admin) (config) # port 1/1/x1 type network
   (admin) (config) # port 1/1/g1 params admin enable
   (admin) (config) # port 1/1/g1 type tool
   ```

4. Save the configuration:

   ```text
   (admin) (config) # write memory
   ```

   **Expected result:** the save command completes without error; a
   subsequent `show running-config` (or equivalent) reflects the port
   role changes.

5. Create a minimal all-pass Flow Map from the network port to the tool
   port, following the pattern in Implementation and Automation.
6. Start a packet capture on the tool used to verify forwarding, connected
   to the tool port.
7. Generate or confirm live traffic at the tapped source.
   **Expected result:** the capture tool shows packets matching the tapped
   source's traffic, confirming acquisition, mapping, and delivery are all
   functioning.
8. **Negative test:** change the map's rule from `pass any` to a narrow
   rule that cannot match the generated traffic (for example, a specific
   host IP address not present in the lab traffic), and re-save the
   configuration.

   ```text
   (admin) (config map alias first-touch-verify) # no rule add pass any
   (admin) (config map alias first-touch-verify) # rule add pass ipv4 host-source 192.0.2.250
   ```

   **Expected result:** the capture tool now shows zero new packets,
   confirming the map — not the physical cabling or port configuration —
   is the traffic-selection control point, and demonstrating the failure
   mode of an overly narrow map rule.
9. **Cleanup:** restore the map to `pass any` (or remove it if the node
   will be reused for Chapter 04's onboarding exercises), and if the node
   is a shared lab resource, remove any lab-only configuration:

   ```text
   (admin) (config map alias first-touch-verify) # no rule add pass ipv4 host-source 192.0.2.250
   (admin) (config map alias first-touch-verify) # rule add pass any
   (admin) (config) # write memory
   ```

## Summary and Completion Checklist

Physical GigaVUE nodes come in two families — TA Series for dense,
fixed-configuration aggregation and HC Series for GigaSMART-capable
processing — sharing a common GigaVUE-OS CLI, port-addressing scheme, and
clustering model. First-touch deployment establishes management
addressing, assigns port roles, and validates a minimal Flow Map before a
node is handed off to centralized GigaVUE-FM management, which Chapter 04
covers next. Clustering extends Flow Mapping across node boundaries and is
the mechanism that lets a fabric scale past a single chassis's port count.

- [ ] Can distinguish TA Series and HC Series nodes and state a typical
      deployment pattern combining them.
- [ ] Can perform first-touch console access and set management
      addressing on a GigaVUE-OS node.
- [ ] Can explain box/slot/port addressing and the four common port
      roles.
- [ ] Can form a basic cluster and explain why fabric-wide mapping
      requires it.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
