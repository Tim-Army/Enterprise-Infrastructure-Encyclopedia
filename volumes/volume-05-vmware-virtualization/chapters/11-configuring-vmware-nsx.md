# Chapter 11: Configuring VMware NSX

## Learning Objectives

- Explain segments (overlay and VLAN-backed) and how they attach to
  gateways to form a logical topology.
- Configure a Tier-0 gateway with BGP peering and a Tier-1 gateway
  attached beneath it.
- Explain Tier-0/Tier-1 gateway high-availability modes (active/active
  versus active/standby) and select correctly between them.
- Configure NAT and DHCP services on NSX gateways and segments.
- Extend Distributed Firewall (DFW) policy design from [Chapter 8](08-vsphere-and-nsx-security-architecture.md) into full
  rule construction, including applied-to scoping.
- Use Traceflow and the Port Connection tool to diagnose logical
  connectivity failures.
- Explain NSX Federation's purpose and scope at a conceptual level.

## Theory and Architecture

[Chapter 10](10-installing-vmware-nsx.md) established the NSX transport fabric — a manager cluster,
prepared transport nodes, and Edge nodes with validated TEP connectivity.
This chapter configures the logical networking and security objects that
actually carry workload traffic on top of that fabric: segments, Tier-0
and Tier-1 gateways, routing, NAT, DHCP, and the full Distributed Firewall
rule model [Chapter 8](08-vsphere-and-nsx-security-architecture.md) introduced from a security-architecture angle.

### Segments

A **segment** is NSX's logical switch — the object a VM's vNIC actually
connects to, equivalent in role to a vSphere port group but implemented as
a distributed logical entity across every transport node in scope rather
than a per-host construct. Two segment types exist, corresponding to the
transport zone types from [Chapter 10](10-installing-vmware-nsx.md):

- **Overlay segment** — backed by an overlay transport zone, using Geneve
  encapsulation between TEPs so that a segment's Layer 2 domain exists
  independent of the physical network's VLAN structure; two VMs on the
  same overlay segment communicate at Layer 2 regardless of which
  transport nodes (and, by extension, which physical racks/VLANs) they
  actually run on.
- **VLAN-backed segment** — backed by a VLAN transport zone, mapping
  directly to a physical VLAN, used where a workload needs direct
  attachment to an existing physical VLAN (bridging into non-NSX
  infrastructure, or edge/uplink-facing connectivity) rather than overlay
  isolation.

Segments attach to a **Tier-1 gateway** (the common pattern for workload
segments) or can remain unattached to any gateway (used for pure Layer 2
extension scenarios, or VLAN-backed segments serving as an Edge's
northbound uplink, which do not need a Tier-1/Tier-0 attachment in the
usual workload sense).

### Tier-0 and Tier-1 gateways

NSX's routing architecture is deliberately two-tiered:

- **Tier-0 gateway** — the top-level gateway, owning the boundary between
  the NSX overlay fabric and the physical/upstream network. A Tier-0
  gateway runs on Edge nodes (it requires Edge capacity; it cannot run
  purely distributed across every hypervisor host the way DFW does) and
  is where north-south routing protocol peering (BGP, or static routes)
  with the physical network happens.
- **Tier-1 gateway** — a second-tier gateway sitting beneath one Tier-0
  gateway, typically owned by a specific tenant, application, or
  organizational boundary, to which workload segments attach. A Tier-1
  gateway handles routing between its own attached segments (inter-segment
  routing happens here, distributed, without necessarily needing to
  transit an Edge at all for East-West traffic between segments on the
  same Tier-1) and forwards traffic destined outside its attached
  segments up to its parent Tier-0.

This two-tier split exists specifically to separate **provider-level**
concerns (Tier-0: physical network peering, overall north-south policy,
typically managed by a central network/platform team) from
**tenant-level** concerns (Tier-1: per-application or per-tenant routing,
NAT, and firewall policy, which can be delegated to application teams or
automated per-tenant provisioning without touching the shared Tier-0).

| Characteristic | Tier-0 gateway | Tier-1 gateway |
| --- | --- | --- |
| Position | Top of the routing hierarchy, faces the physical network | Beneath a Tier-0, faces workload segments |
| Routing protocol peering | Yes — BGP (or static routes) to upstream/physical routers | No direct physical peering; routes to its Tier-0 |
| Runs on | Edge nodes only | Distributed across transport nodes for East-West traffic; Edge nodes only when a centralized service (NAT, LB) is attached |
| Typical ownership | Central network/platform team | Application/tenant team, or automated per-tenant provisioning |

### High-availability modes: active/active versus active/standby

Both Tier-0 and Tier-1 gateways support two HA modes when deployed on
Edge nodes:

- **Active/active** — multiple Edge nodes simultaneously forward traffic
  for the same gateway, typically combined with **ECMP (Equal-Cost
  Multi-Path)** routing on the Tier-0's BGP sessions for aggregate
  throughput and faster failure convergence. Active/active is not
  available for a gateway with certain centralized stateful services
  attached (most notably, when using NAT or a stateful firewall in a mode
  that requires session-state consistency that active/active's
  multi-node forwarding cannot guarantee) — check the specific service
  compatibility before assuming active/active is always the preferred
  mode.
- **Active/standby** — one Edge node actively forwards for the gateway
  while a second holds standby state, taking over on detected failure.
  Required for Tier-1 (or Tier-0) gateways using services that need
  strict session-state consistency, and often the simpler, more
  predictable choice even where active/active would be technically
  available.

### Routing: BGP and static routes

A Tier-0 gateway peers with upstream physical routers using **BGP** (the
standard choice for any topology needing dynamic route exchange and fast
convergence) or, for simpler topologies, **static routes**. BGP peering is
configured per Edge node uplink interface, with route redistribution
policy controlling which NSX-internal routes (Tier-1 subnets, NAT'd
addresses) are advertised upstream versus kept internal to the NSX
fabric — redistribution policy is a deliberate security and routing-
hygiene boundary, not a default-everything setting.

### NAT

NSX gateways support **SNAT (Source NAT)**, **DNAT (Destination NAT)**,
and **reflexive NAT**, configurable at either the Tier-0 or Tier-1 level
depending on where the translation boundary logically belongs (Tier-1 NAT
is the common pattern for per-tenant outbound SNAT and per-application
DNAT; Tier-0 NAT is used for provider-level, shared translation needs).
NAT rule evaluation order and scope (which gateway, which direction)
follow the same general policy-based-evaluation model as DFW rules
described below.

### DHCP services

NSX can provide **DHCP server** function directly on a segment (a
centralized service, requiring Edge capacity) or **DHCP relay** (forwarding
DHCP requests to an existing external DHCP infrastructure, keeping IP
address management centralized outside NSX). DHCP relay is the more common
enterprise pattern where IPAM/DHCP is already centrally managed;
NSX-native DHCP server is more common in self-contained or lab
environments, or where per-tenant DHCP scope automation is itself part of
the value NSX-based automation is providing.

### Distributed Firewall: full rule construction

[Chapter 8](08-vsphere-and-nsx-security-architecture.md) introduced the DFW's dynamic security groups and basic rule
concept from a security-architecture standpoint. Operationally, a DFW rule
is defined by:

- **Source and destination** — can reference IP addresses/subnets, or
  (the more powerful and common pattern) **NSX Groups**, which
  dynamically populate membership based on criteria such as VM tags,
  segment membership, or other object properties, so that a rule's
  effective scope updates automatically as tagged VMs are added or
  removed rather than requiring manual rule maintenance.
- **Services** — the Layer 4 (or Layer 7, with the Distributed IDS/IPS
  and application-identification capability referenced in [Chapter 8](08-vsphere-and-nsx-security-architecture.md))
  definition of what traffic the rule matches.
- **Applied To** — critically, DFW rules can be scoped to apply only to
  specific groups rather than every workload in the environment, which
  both improves performance (the rule is only evaluated where relevant)
  and lets different rule sets exist for different application tiers
  without one team's rules affecting another's traffic evaluation.
- **Action** — Allow, Drop, or Reject (Reject sends a response, such as a
  TCP RST or ICMP unreachable, rather than Drop's silent discard —
  meaningfully different behavior for application timeout characteristics
  and worth choosing deliberately rather than defaulting to one
  universally).

DFW policies are organized into ordered **sections**, evaluated top to
bottom with first-match semantics, ending in a default rule (commonly set
to Drop in a zero-trust micro-segmentation design, consistent with the
default-deny posture recommended in [Chapter 8](08-vsphere-and-nsx-security-architecture.md)).

### NSX Federation (conceptual overview)

**NSX Federation** extends NSX management and networking/security policy
across multiple, geographically distributed NSX deployments (each with
its own local NSX Manager cluster) through a **Global Manager**, which
defines policy intended to span sites and pushes it down to each site's
local NSX Manager for local enforcement. Federation's primary use cases
are multi-site disaster recovery (consistent network/security policy
already in place at a DR site before a failover event, rather than
reconstructed after) and centrally governed multi-site micro-segmentation
policy. Federation is an architectural extension on top of everything
described in this chapter, not a replacement for it — each federated
site still has its own local NSX Manager cluster, transport fabric, and
gateways, configured using the same concepts covered here.

## Design Considerations

- **Tier-0/Tier-1 ownership boundary as an organizational decision, not
  only a technical one.** Decide, deliberately, which team owns Tier-0
  (typically central network/platform) versus which teams can provision
  their own Tier-1 gateways and segments (typically application/tenant
  teams, potentially through self-service automation) — this boundary is
  as much about operational delegation as network topology.
  gateways.
- **Active/active versus active/standby by service requirement, not
  default preference.** Confirm whether the specific stateful services
  planned for a gateway (NAT, load balancing) are compatible with
  active/active before designing around it purely for the throughput/
  ECMP benefit; a gateway that needs strict session-state consistency
  should use active/standby regardless of the throughput trade-off.
- **Route redistribution scope.** Decide explicitly which internal routes
  get redistributed upstream via BGP — over-redistribution (advertising
  every internal Tier-1 subnet upstream indiscriminately) unnecessarily
  expands the physical network's routing table and exposure; under-
  redistribution breaks reachability for legitimately external-facing
  workloads. This is a deliberate policy, reviewed like a firewall rule
  set, not a default-on setting.
- **DHCP relay versus NSX-native DHCP.** Prefer DHCP relay to existing
  centralized IPAM/DHCP infrastructure in most enterprise environments to
  avoid maintaining IP address management in two places; NSX-native DHCP
  is justified where per-tenant, fully self-contained network automation
  is a specific design goal.
- **DFW Applied To scoping discipline.** Avoid a DFW policy design that
  defaults every rule to "Applied To: DFW" (every workload everywhere) —
  deliberate Applied To scoping by application tier/group is both a
  performance consideration (evaluation cost) and a blast-radius
  consideration (a rule change affecting only its intended scope, not the
  entire environment).
- **Federation as an intentional multi-site commitment.** Do not adopt
  Federation for a single-site deployment or as a default "just in case"
  future-proofing measure — it adds real operational complexity (a Global
  Manager to operate, cross-site policy synchronization to reason about)
  that should be justified by an actual multi-site requirement.

## Implementation and Automation

### Creating an overlay segment attached to a Tier-1 gateway

```bash
# curl against the NSX Manager Policy API: create an overlay segment
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/segments/seg-app-tier-01 \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "seg-app-tier-01",
        "transport_zone_path": "/infra/sites/default/enforcement-points/default/transport-zones/tz-overlay-01",
        "subnets": [{"gateway_address": "172.16.10.1/24"}],
        "connectivity_path": "/infra/tier-1s/t1-app-tenant-a"
      }'
```

### Creating a Tier-0 gateway with BGP

```bash
# curl against the NSX Manager Policy API: create a Tier-0 gateway (active/active)
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/tier-0s/t0-corp-01 \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "t0-corp-01",
        "ha_mode": "ACTIVE_ACTIVE",
        "edge_cluster_path": "/infra/sites/default/enforcement-points/default/edge-clusters/edge-cluster-01"
      }'

# Configure a BGP neighbor on the Tier-0's locale-services
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/tier-0s/t0-corp-01/locale-services/default/bgp/neighbors/nbr-upstream-01 \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "nbr-upstream-01",
        "neighbor_address": "10.10.70.1",
        "remote_as_num": "65001",
        "hold_down_time": 180,
        "keep_alive_time": 60
      }'
```

### Creating a Tier-1 gateway and attaching it to the Tier-0

```bash
# curl against the NSX Manager Policy API: create a Tier-1 gateway (active/standby)
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/tier-1s/t1-app-tenant-a \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "t1-app-tenant-a",
        "tier0_path": "/infra/tier-0s/t0-corp-01",
        "route_advertisement_types": ["TIER1_CONNECTED", "TIER1_NAT"]
      }'
```

### Configuring SNAT on a Tier-1 gateway

```bash
# curl against the NSX Manager Policy API: create an SNAT rule
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/tier-1s/t1-app-tenant-a/nat/USER/nat-rules/snat-outbound-01 \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "snat-outbound-01",
        "action": "SNAT",
        "source_network": "172.16.10.0/24",
        "translated_network": "203.0.113.10"
      }'
```

### Configuring DHCP relay on a segment

```bash
# curl against the NSX Manager Policy API: configure DHCP relay pointing at existing enterprise DHCP
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PATCH \
  https://nsx-vip.corp.example/policy/api/v1/infra/segments/seg-app-tier-01 \
  -H "Content-Type: application/json" \
  -d '{
        "dhcp_config_path": "/infra/dhcp-relay-configs/dhcp-relay-corp-01"
      }'
```

### Creating a DFW policy section and a scoped rule

```bash
# curl against the NSX Manager Policy API: create a DFW policy section
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/domains/default/security-policies/sp-app-tier-a \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "sp-app-tier-a",
        "category": "Application"
      }'

# Add a scoped rule: allow app-tier to db-tier on 5432 only, applied to both groups only
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/domains/default/security-policies/sp-app-tier-a/rules/rule-app-to-db \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "app-to-db-postgres",
        "source_groups": ["/infra/domains/default/groups/grp-app-tier"],
        "destination_groups": ["/infra/domains/default/groups/grp-db-tier"],
        "services": ["/infra/services/PostgreSQL"],
        "scope": ["/infra/domains/default/groups/grp-app-tier", "/infra/domains/default/groups/grp-db-tier"],
        "action": "ALLOW"
      }'
```

## Validation and Troubleshooting

- **BGP neighbor status.** The Tier-0 gateway's routing status page in the
  NSX Manager UI, or `get bgp neighbor summary` from the active Edge
  node's CLI, reports session state (`Idle`, `Connect`, `Established`); a
  session stuck below `Established` most commonly traces to an AS number
  mismatch, an unreachable neighbor IP, or a physical/VLAN uplink
  misconfiguration on the Edge's northbound interface rather than an NSX
  routing-configuration fault per se.

  ```bash
  # Edge node CLI: check BGP neighbor state
  get bgp neighbor summary
  ```

- **Traceflow.** **Traceflow** injects a synthetic packet at a specified
  source and traces its actual path — hop by hop, including which DFW
  rule (if any) dropped it — through the logical topology to a specified
  destination. It is the single most useful NSX-specific diagnostic tool
  for "why can't VM A reach VM B" questions, since it shows definitively
  whether a packet is being dropped by routing, a DFW rule, or never
  leaving the source segment, rather than requiring the same conclusion to
  be inferred indirectly from multiple separate log sources.
- **Port Connection tool.** Reports the full logical path (segment,
  gateway, uplink) a given VM's vNIC is actually connected through,
  useful for confirming a VM landed on the segment/gateway an
  administrator intended versus a misconfigured template or automation
  step attaching it elsewhere.
- **DFW rule hit counters and rule order.** A traffic flow unexpectedly
  blocked should be checked against DFW rule hit counters (visible per
  rule in the NSX Manager UI) to confirm which specific rule (including
  an unintended earlier match in first-match rule evaluation order, or
  the final default-drop rule) is actually being hit, rather than assuming
  the intended "allow" rule further down the section is the one being
  evaluated.
- **NAT translation verification.** `get nat rule` on the Edge node CLI
  and NAT-specific statistics counters confirm whether a NAT rule is
  actually being matched and translating as expected — a common failure
  pattern is a correctly configured NAT rule that is simply never reached
  because upstream routing or a DFW rule already dropped the packet
  first, which Traceflow will distinguish clearly from an actual NAT
  misconfiguration.

## Security and Best Practices

- Default DFW policy to Drop (or Reject, chosen deliberately per use
  case) at the end of every section, consistent with the zero-trust,
  default-deny posture established in [Chapter 8](08-vsphere-and-nsx-security-architecture.md), and scope every rule's
  Applied To field deliberately rather than leaving it environment-wide
  by default.
- Scope BGP route redistribution deliberately — do not redistribute every
  internal Tier-1 subnet upstream by default; treat redistribution policy
  with the same review rigor as a firewall rule set, since it directly
  controls what becomes reachable from outside the NSX fabric.
- Use Reject rather than silent Drop where a clear, fast failure signal to
  legitimate clients is preferable to the connection-timeout behavior
  Drop produces, and use Drop where minimizing information disclosure to
  a potential attacker (no distinguishable response between "blocked" and
  "does not exist") is the higher priority.
- Restrict who can modify Tier-0 gateway configuration (BGP peering,
  route redistribution, NAT at the provider level) separately from who
  can modify Tier-1/segment/DFW configuration within their own tenant
  scope, using NSX's own RBAC model — this mirrors the organizational
  ownership boundary discussed in Design Considerations.
- Treat NSX Groups used as DFW rule sources/destinations as security-
  relevant configuration in their own right — a dynamic group's matching
  criteria (a VM tag, for instance) is effectively part of the access
  control policy, and unauthorized ability to apply that tag to a VM is
  equivalent to unauthorized ability to grant that VM the access the
  group's associated rules provide.
- Evaluate NSX Federation's Global Manager access control with the same
  rigor as any other multi-site, policy-propagating control plane —
  compromise or misconfiguration at the Global Manager level has a
  multi-site blast radius by design.

## References and Knowledge Checks

**References**

- VMware NSX 4.x Documentation — *Segments*.
- VMware NSX 4.x Documentation — *Tier-0 and Tier-1 Gateways*, *Routing*
  (BGP), *NAT*, *DHCP*.
- VMware NSX 4.x Documentation — *Distributed Firewall* and *Traceflow*.
- VMware NSX 4.x Documentation — *NSX Federation*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for the DFW/Gateway Firewall security-architecture
  foundation this chapter builds full rule construction on.
- See [Chapter 10](10-installing-vmware-nsx.md) for the transport fabric (transport zones, transport
  nodes, Edge nodes) this chapter's logical objects run on top of.

**Knowledge checks**

1. Why does NSX separate Tier-0 and Tier-1 gateways rather than using a
   single-tier routing model, in terms of organizational ownership?
2. Under what circumstance is active/standby required rather than merely
   preferred for a gateway's HA mode?
3. What specifically does Traceflow show that DFW rule hit counters and
   BGP neighbor status individually cannot, when diagnosing a
   connectivity failure?
4. Why is DHCP relay generally preferred over NSX-native DHCP server
   function in an enterprise environment that already has centralized
   IPAM?
5. What is the practical difference between Drop and Reject as a DFW rule
   action, and when would an architect deliberately choose Reject?

## Hands-On Lab

**Objective:** Build a Tier-0 gateway (BGP to a simulated upstream), a
Tier-1 gateway beneath it, an overlay segment with DHCP relay, verify VM
connectivity, build and test a scoped DFW rule using Traceflow, and
validate a negative test (blocked traffic) before allowing it.

**Prerequisites**

- The transport fabric from the [Chapter 10](10-installing-vmware-nsx.md) lab (prepared host, Edge node,
  overlay transport zone) already in place, or an equivalent lab NSX
  environment.
- A simulated upstream BGP router reachable from the Edge node's uplink
  (a lab router, or a second NSX Edge/VM running a BGP daemon such as
  FRRouting, is sufficient for AS-peering validation).
- Two test VMs deployable onto the lab overlay segment, and a lab DHCP
  server reachable for the DHCP relay test.

**Steps**

1. Create the Tier-0 gateway and configure a BGP neighbor toward the lab
   upstream router, using the example in Implementation and Automation
   adjusted to lab addressing and AS numbers.

   **Expected result:** `get bgp neighbor summary` on the Edge node CLI
   reports the neighbor as `Established`.

2. Create the Tier-1 gateway attached to the Tier-0, and an overlay
   segment attached to the Tier-1, with DHCP relay pointed at the lab
   DHCP server.

   **Expected result:** the segment appears under `Networking > Segments`
   with the Tier-1 shown as its connectivity, and the Tier-1 shows the
   Tier-0 as its parent.

3. Deploy two test VMs (`test-app-01`, `test-db-01`) onto the new segment
   and confirm both obtain DHCP-relayed addresses from the lab DHCP
   server.

   **Expected result:** both VMs receive IP addresses in the expected lab
   subnet, and can ping each other and the segment's gateway address.

4. Create a DFW policy section and a default-deny rule at the bottom of
   the section (`Applied To` the segment's group), then attempt
   connectivity between the two test VMs on a specific port (for example,
   TCP 5432):

   **Expected result (negative test):** the connection fails/times out,
   and the DFW rule hit counter for the default-deny rule increments.

5. Use Traceflow to trace the blocked flow from `test-app-01` to
   `test-db-01` on TCP 5432:

   **Expected result:** Traceflow reports the packet reaching the
   destination segment but being dropped by the default-deny DFW rule,
   confirming the block is a firewall decision rather than a routing
   failure.

6. Add a scoped Allow rule above the default-deny rule permitting
   `test-app-01`'s group to reach `test-db-01`'s group on TCP 5432 only,
   using the example in Implementation and Automation as a model.

   **Expected result:** the connection now succeeds, and re-running
   Traceflow for the same flow shows the packet reaching the destination
   with the new Allow rule (not the default-deny rule) as the matching
   rule.

7. Confirm the Allow rule's scope is correctly limited: attempt the same
   connection from a third, out-of-group test VM if available, and
   confirm it is still blocked by the default-deny rule — demonstrating
   the Applied To scoping is working as intended rather than
   inadvertently permissive.

8. **Cleanup:** delete the test VMs, remove the DFW policy section and its
   rules, delete the segment, Tier-1 gateway, and Tier-0 gateway (and its
   BGP neighbor configuration) if these were created solely for this lab.

## Summary and Completion Checklist

NSX's logical networking layer builds directly on the transport fabric
from [Chapter 10](10-installing-vmware-nsx.md): segments (overlay or VLAN-backed) attach to Tier-1
gateways, which in turn attach to a Tier-0 gateway that owns north-south
routing (via BGP or static routes) to the physical network — a deliberate
two-tier split separating provider-level and tenant-level concerns. NAT
and DHCP (server or relay) round out per-segment/per-gateway services, and
the Distributed Firewall's full rule model — source/destination groups,
services, deliberate Applied To scoping, and first-match ordered
evaluation ending in default-deny — extends the security-architecture
foundation from [Chapter 8](08-vsphere-and-nsx-security-architecture.md) into concrete, operational policy. Traceflow and
the Port Connection tool are the primary diagnostic instruments for
tracing exactly where in this logical topology a connectivity problem
actually originates, and NSX Federation extends the same concepts across
multiple sites through a Global Manager for organizations with a genuine
multi-site requirement.

- [ ] Can explain the Tier-0/Tier-1 gateway split and its organizational
      rationale.
- [ ] Can configure BGP peering on a Tier-0 gateway and create an
      attached Tier-1 gateway and segment.
- [ ] Can configure NAT and DHCP relay correctly for a given topology.
- [ ] Can construct a scoped DFW rule using dynamic groups and Applied To.
- [ ] Can use Traceflow to distinguish a routing failure from a firewall
      drop.
- [ ] Can describe NSX Federation's purpose and when it is justified.
- [ ] Completed the hands-on lab, including the default-deny negative
      test, scoped-allow validation, and full cleanup.
