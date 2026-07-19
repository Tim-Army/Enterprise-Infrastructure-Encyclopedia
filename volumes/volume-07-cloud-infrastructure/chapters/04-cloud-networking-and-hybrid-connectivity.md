# Chapter 04: Cloud Networking and Hybrid Connectivity

## Learning Objectives

- Design a virtual network address plan (CIDR allocation, subnetting, and
  segmentation) that scales across environments without renumbering.
- Differentiate the routing, gateway, and peering constructs available for
  connecting virtual networks to each other and to on-premises networks.
- Explain the hub-and-spoke and transit-gateway topology patterns and
  choose correctly between them for a given scale and blast-radius
  requirement.
- Compare site-to-site VPN and dedicated private connectivity, and
  articulate the latency, bandwidth, and resilience trade-offs of each.
- Design DNS resolution across a hybrid environment, including split-horizon
  and centralized private-resolution patterns.
- Implement network segmentation as code using security groups and network
  access control lists, and diagnose a connectivity failure systematically.

## Theory and Architecture

### The virtual network as the addressing foundation

A virtual network (called a VPC, VNet, or equivalent depending on
provider) is a logically isolated, customer-defined IP address space
inside a cloud provider's physical network fabric. Everything else in this
chapter — subnetting, routing, peering, hybrid connectivity — is built on
top of the address plan chosen for that virtual network, which makes the
address plan the highest-leverage decision in this chapter: a poorly
planned address space is expensive to fix later because renumbering a live
network touches every dependent route table, security rule, DNS record,
and peering configuration simultaneously.

### CIDR allocation and subnetting

Plan address space top-down, before creating a single subnet:

1. Reserve a sufcient private address range (commonly from RFC 1918 space)
   per environment or region, sized generously — undersizing here is the
   single most common cloud networking mistake, because a virtual
   network's primary CIDR block is difficult or impossible to expand in
   place once subnets and peerings depend on it.
2. Subdivide by availability zone first, then by tier or function
   (public-facing, application, data), so that each zone's subnets are a
   contiguous, summarizable block — this keeps route tables and security
   rules short and readable.
3. Reserve headroom explicitly: leave unallocated CIDR blocks between
   environments and between zones rather than allocating contiguously to
   the last available address, so a future subnet can be added without a
   renumbering exercise.

```text
10.20.0.0/16   example-prod virtual network (65,536 addresses)
  10.20.0.0/20   zone-a reserved block
    10.20.0.0/24   zone-a public subnet
    10.20.1.0/24   zone-a app subnet
    10.20.2.0/24   zone-a data subnet
    10.20.8.0/21   zone-a headroom (unallocated)
  10.20.16.0/20  zone-b reserved block (mirrors zone-a layout)
  10.20.32.0/20  zone-c reserved block (mirrors zone-a layout)
  10.20.240.0/20 headroom for a future zone or shared-services subnet
```

Across an organization with multiple accounts/subscriptions, maintain a
single central CIDR allocation registry (a version-controlled file, not
tribal knowledge) so that no two virtual networks that might ever need to
peer or connect over VPN are allocated overlapping address space. Overlap
discovered after two networks are already in production is one of the most
disruptive classes of network remediation.

### Routing constructs

- **Route table** — the set of rules determining where traffic destined
  for a given CIDR block is sent next (locally within the virtual network,
  to an internet gateway, to a peering connection, to a VPN or dedicated
  connection gateway). Every subnet is associated with a route table,
  explicitly or by a default.
- **Internet gateway** — provides a path between a virtual network and the
  public internet; only subnets with a route to it (and resources with a
  public address or behind a NAT device) can reach or be reached from the
  internet.
- **NAT gateway** — allows resources without a public address to
  initiate outbound connections to the internet (for patching, calling
  external APIs) without being directly reachable from it.
- **Peering connection** — a direct, non-transitive routing relationship
  between two virtual networks. Non-transitive means peering A-to-B and
  B-to-C does not grant A a route to C; a full mesh of peerings grows as
  O(n²) with the number of networks, which is the primary driver toward
  the hub-and-spoke pattern below.
- **Transit gateway / virtual router hub** — a managed, transitive routing
  hub that many virtual networks and on-premises connections attach to
  once, gaining routed connectivity to every other attachment without a
  full peering mesh.

### Hub-and-spoke vs. transit-gateway topology

- **Hub-and-spoke with peering** — a central hub virtual network holds
  shared services (DNS resolvers, firewalls, VPN/dedicated-connection
  gateways); each spoke peers directly to the hub only. This scales
  linearly (one peering per spoke) instead of quadratically, and keeps
  routing simple, but spoke-to-spoke traffic must either be disallowed by
  policy or explicitly routed through a network appliance in the hub,
  since peering itself is non-transitive.
- **Transit gateway** — a managed routing hub that natively supports
  transitive routing between every attachment, including spoke-to-spoke
  traffic, without requiring an appliance in the path for basic routing
  (inspection appliances can still be inserted deliberately via route
  table design). This scales further than peering-based hub-and-spoke and
  centralizes route table management, at the cost of a new managed
  component that is itself a shared-fate dependency for every attached
  network — a transit gateway outage or misconfiguration can affect every
  spoke simultaneously.

Choose peering-based hub-and-spoke for a smaller estate where spoke-to-spoke
traffic is rare or intentionally restricted; choose a transit gateway once
the number of spokes or the need for native spoke-to-spoke routing makes a
peering mesh (even hub-mediated) operationally heavy.

### Hybrid connectivity: VPN vs. dedicated private connection

| Attribute | Site-to-site VPN | Dedicated private connection |
| --- | --- | --- |
| Underlying medium | Encrypted tunnel over the public internet | Private, provider-facilitated physical or logical circuit |
| Typical provisioning time | Minutes to hours | Days to weeks (physical cross-connect and carrier coordination) |
| Bandwidth | Limited by tunnel/internet-path throughput, typically lower and more variable | Higher, consistent, dedicated |
| Latency and jitter | Variable, subject to internet path conditions | Low and consistent |
| Cost model | Low fixed cost, pay for gateway and data transfer | Higher fixed cost (port/circuit), lower per-GB transfer cost at scale |
| Typical role | Primary connectivity for smaller sites, or backup path for a dedicated connection | Primary path for latency- or bandwidth-sensitive production traffic |

A common, resilient pattern uses both together: a dedicated private
connection as the primary path and a site-to-site VPN as an automatic
failover path, with routing protocol (typically BGP) preference values
tuned so traffic prefers the dedicated connection whenever it is healthy.
Relying on a single dedicated connection with no fallback path reintroduces
a single point of failure that the cloud's own multi-zone resilience does
not protect against, because the connection itself sits outside the
provider's zone redundancy.

### DNS across a hybrid environment

DNS resolution in a hybrid environment must resolve consistently regardless
of where the query originates — from a cloud workload, from an
on-premises workstation, or from a partner network reached over the same
connectivity. Two patterns dominate:

- **Centralized private DNS resolution** — a shared set of DNS
  resolvers, typically hosted in the network hub, that both cloud
  workloads and on-premises clients are configured (via DHCP option or
  conditional forwarding) to use, with forwarding rules directing queries
  for on-premises zones toward on-premises DNS servers and queries for
  cloud-hosted private zones toward the provider's resolver.
- **Split-horizon DNS** — the same domain name resolves to a different
  address depending on whether the query originates from inside the
  private network or from the public internet (for example, an internal
  load balancer address privately, a public load balancer address
  externally). Split-horizon requires careful conditional-forwarding
  configuration to avoid a client on the wrong side of the split receiving
  an unreachable address.

### Network segmentation constructs

- **Security group (instance/resource-level, typically stateful)** —
  attached directly to a resource (a compute instance, a load balancer, a
  managed database endpoint); evaluates allowed traffic per rule, and a
  reply to an allowed inbound (or outbound) flow is automatically
  permitted back out without a matching explicit rule, because the group
  is stateful.
- **Network access control list (subnet-level, typically stateless)** —
  attached to a subnet, evaluated in addition to any security group;
  because it is stateless, both the request and the reply direction need
  explicit rules, which makes it a coarser, defense-in-depth layer rather
  than the primary per-resource control.

Use security groups as the primary, fine-grained segmentation control, and
network ACLs as a coarse subnet-level backstop (for example, an explicit
deny of a known-bad CIDR block at the subnet boundary, so that a
misconfigured security group cannot alone permit traffic from that
source).

## Design Considerations

### Sizing the address plan for growth, not current state

Size the primary CIDR block for the virtual network against a multi-year
growth projection, not against the workload count at launch. The cost of
reserving too much address space is negligible (private address space is
free); the cost of undersizing is a disruptive future renumbering or a
forced, awkward secondary CIDR block attachment with its own routing
caveats.

### Choosing the topology as the estate grows

Start with peering-based hub-and-spoke for a small number of spokes; treat
the migration point to a transit gateway as a planned, deliberate project
rather than something to defer indefinitely — migrating routing topology
under an already-large, already-live spoke count is considerably more
disruptive than migrating early. Track spoke count and spoke-to-spoke
traffic patterns as a standing design-review input specifically to catch
this transition point before it becomes an emergency.

### Egress and inspection points

Decide deliberately where outbound internet traffic and inter-spoke
traffic are inspected (a centralized firewall or secure web gateway
appliance in the hub, versus distributed egress per spoke). Centralized
inspection simplifies policy management and logging but makes the
inspection point's own capacity and availability a shared-fate dependency
for every spoke; size and make that inspection layer redundant with the
same rigor applied to any other shared production service.

### Bandwidth and resilience for hybrid links

Size dedicated connection bandwidth against peak, not average, hybrid
traffic, and provision at least two physically diverse connections (or a
dedicated connection plus a VPN failover path) for any workload where
hybrid connectivity loss is unacceptable. A single connection, however
reliable individually, is a single point of failure for everything that
depends on hybrid reachability, including centralized DNS resolution if
that resolver only exists on one side of the link.

### DNS resolver placement and forwarding scope

Place shared DNS resolver infrastructure in the network hub so that both
directions of hybrid traffic reach it over the same connectivity already
provisioned for application traffic, rather than provisioning a separate
path for DNS. Scope conditional forwarding rules as narrowly as the actual
zone delegation requires — an overly broad forwarding rule can silently
route queries for zones with no delegation configured on the far side into
resolution failures that are difficult to distinguish from a network
reachability problem.

## Implementation and Automation

### Defining the address plan and virtual network as code

```hcl
# network.tf — illustrative provider-neutral virtual network and subnets.
variable "vnet_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

resource "cloud_virtual_network" "prod" {
  name          = "example-prod"
  address_space = [var.vnet_cidr]
}

locals {
  zones = ["a", "b", "c"]
  # Each zone gets a /20; each tier within a zone gets a /24.
  zone_blocks = { for i, z in local.zones : z => cidrsubnet(var.vnet_cidr, 4, i) }
}

resource "cloud_subnet" "app" {
  for_each = local.zone_blocks

  name              = "app-${each.key}"
  virtual_network_id = cloud_virtual_network.prod.id
  address_prefix    = cidrsubnet(each.value, 4, 1) # second /24 in the zone block
  availability_zone  = each.key
}
```

### Hub-and-spoke peering

```hcl
# peering.tf — illustrative hub-and-spoke peering; non-transitive.
resource "cloud_network_peering" "spoke_to_hub" {
  name                = "spoke-payments-to-hub"
  local_network_id      = cloud_virtual_network.payments_spoke.id
  remote_network_id      = cloud_virtual_network.hub.id
  allow_forwarded_traffic = false # deliberate: no transitive routing through this spoke
}
```

### Security group as the primary segmentation control

```hcl
# security-groups.tf — illustrative stateful security group.
resource "cloud_security_group" "app_tier" {
  name        = "app-tier-prod"
  network_id   = cloud_virtual_network.prod.id
  description = "Application tier: inbound from load balancer tier only."

  ingress_rule {
    protocol       = "tcp"
    port_range     = "8443"
    source_security_group = cloud_security_group.lb_tier.id
  }

  egress_rule {
    protocol         = "tcp"
    port_range       = "5432"
    destination_security_group = cloud_security_group.data_tier.id
  }
  # No default allow-all egress: every permitted flow is explicit.
}
```

### Hybrid connectivity with VPN failover behind a dedicated connection

```hcl
# hybrid.tf — illustrative dedicated connection with VPN failover,
# BGP preference tuned so the dedicated path is preferred when healthy.
resource "cloud_dedicated_connection" "primary" {
  name           = "hub-to-onprem-primary"
  bandwidth_mbps  = 1000
  bgp_asn         = 65010
  bgp_local_preference = 200 # higher preference: preferred path
}

resource "cloud_vpn_gateway" "failover" {
  name    = "hub-to-onprem-vpn-failover"
  network_id = cloud_virtual_network.hub.id
}

resource "cloud_vpn_connection" "failover" {
  name        = "hub-to-onprem-vpn"
  gateway_id   = cloud_vpn_gateway.failover.id
  peer_ip      = var.onprem_vpn_peer_ip
  bgp_asn      = 65010
  bgp_local_preference = 100 # lower preference: failover only
}
```

## Validation and Troubleshooting

- **Diagnose connectivity failures layer by layer.** Confirm, in order:
  (1) the source resource's security group permits the outbound flow, (2)
  the destination's security group permits the specific inbound flow from
  the source, (3) both subnets' network ACLs (if used) permit the flow in
  both directions, (4) the route table for the source subnet has a route
  to the destination CIDR, (5) for hybrid traffic, the connection (VPN or
  dedicated) is up and the routing protocol session is established.
  Working through this order avoids the common mistake of only checking
  the security group and assuming a routing problem is a firewall problem.
- **Use provider-native flow logging** (VPC/VNet flow logs or equivalent)
  to confirm whether traffic is being explicitly rejected by a security
  control or is simply not arriving — these look identical from the
  application's perspective (a connection timeout) but require different
  remediation.
- **Validate CIDR non-overlap before every new peering or VPN
  connection**, not only at initial design time — a new spoke or a newly
  acquired business unit's network is a common source of a late-discovered
  overlap.
- **Test hybrid failover deliberately and on a schedule.** Disable the
  primary dedicated connection in a maintenance window and confirm traffic
  actually shifts to the VPN path within the expected BGP convergence
  time; an untested failover path is a common source of an extended outage
  precisely when it is needed.
- **Diagnose DNS resolution failures separately from network
  reachability failures.** A resource that cannot resolve a name but can
  reach an IP address directly points at the resolver configuration or
  forwarding rule, not at routing or security groups.

## Security and Best Practices

- Default every security group to deny-by-default with explicit, narrow
  allow rules; avoid broad `0.0.0.0/0` inbound rules except for the
  specific public-facing resources that require them, and never for a
  database or internal management interface.
- Treat network ACLs as a defense-in-depth backstop, not the primary
  control — do not rely on a stateless subnet-level rule as the only
  protection for a sensitive resource.
- Encrypt all site-to-site VPN tunnels with current-generation ciphers and
  rotate pre-shared keys or certificates on a defined schedule; do not
  treat a VPN's encryption as a substitute for segmentation on top of it.
- Log and centralize network flow logs for every production virtual
  network; flow logs are frequently the fastest way to distinguish a
  security incident from a routine misconfiguration during an investigation.
- Restrict who can create or modify peering connections, transit gateway
  attachments, and route tables — a network topology change has
  organization-wide blast radius and deserves the same change-review
  rigor as an identity policy change.
- Avoid encoding trust in network location alone ("it's inside the VPC, so
  it's trusted"); pair network segmentation with the identity-based
  controls from [Chapter 03](03-cloud-identity-access-and-cryptographic-services.md) rather than treating either as sufficient
  alone.

## References and Knowledge Checks

### References

- RFC 1918, *Address Allocation for Private Internets*.
- RFC 4271, *A Border Gateway Protocol 4 (BGP-4)*.
- Each major provider's virtual network, peering, transit gateway, and
  dedicated-connection documentation — consult the current vendor source
  for exact limits and CLI/API syntax.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline.

### Knowledge checks

1. Why is undersizing a virtual network's primary CIDR block considered
   the most consequential early networking mistake in this chapter?
2. Explain why peering is non-transitive and how that property drives the
   choice between hub-and-spoke peering and a transit gateway as spoke
   count grows.
3. A production workload depends on a single dedicated private connection
   with no VPN failover. What specific risk does this create, and how
   would you validate a proposed fix?
4. What is the practical difference between a security group and a
   network access control list, and why is a network ACL alone
   insufficient for protecting a sensitive resource?
5. A resource can reach a destination by IP address but not by hostname.
   What class of problem does this narrow down to, and why?

## Hands-On Lab

### Lab 4.1 — CIDR allocation planning and overlap detection

This lab builds a small local tool that validates a proposed set of
virtual network CIDR allocations against two rules: no two networks may
overlap, and no network may exceed its assigned parent block. It uses only
Terraform's built-in `cidrhost`/`cidrsubnet` functions and local values, so
it requires no cloud account or credentials.

**Prerequisites**

- Terraform 1.9.x or later, or a compatible OpenTofu release.
- A POSIX shell.

**Steps**

1. Create the working directory:

   ```bash
   mkdir -p ~/labs/vol07-ch04 && cd ~/labs/vol07-ch04
   ```

2. Create `versions.tf`:

   ```hcl
   terraform {
     required_version = ">= 1.9.0"
   }
   ```

3. Create `main.tf` defining a set of candidate allocations and a
   validation check using Terraform's `check` block:

   ```hcl
   locals {
     allocations = {
       hub          = "10.20.0.0/20"
       payments     = "10.20.16.0/20"
       platform     = "10.20.32.0/20"
     }
   }

   check "no_cidr_overlap" {
     assert {
       condition = alltrue([
         for pair in setproduct(keys(local.allocations), keys(local.allocations)) :
         pair[0] == pair[1] || !(
           cidrhost(local.allocations[pair[0]], 0) == cidrhost(local.allocations[pair[1]], 0)
         )
       ])
       error_message = "Two or more allocations share an identical network address; investigate for overlap."
     }
   }

   output "allocations" {
     value = local.allocations
   }
   ```

4. Initialize and run a plan (this lab creates no real resources, only
   evaluates the `check` block against local data):

   ```bash
   terraform init
   terraform plan
   ```

   **Expected result:** Plan succeeds with `No changes.` and no check
   failure reported, confirming the three non-overlapping /20 allocations
   pass validation.

**Negative test**

5. Edit `main.tf` and change the `platform` allocation to
   `"10.20.16.0/20"` (an exact duplicate of the `payments` allocation),
   then re-run:

   ```bash
   terraform plan
   ```

   **Expected result:** Terraform reports the check failure with the
   message `Two or more allocations share an identical network address;
   investigate for overlap.`, demonstrating that the validation catches an
   accidental duplicate allocation before it is ever applied to a real
   network. Note this simplified check detects identical network
   addresses; a production-grade check would also need to detect partial
   overlap between differently sized blocks.

**Cleanup**

6. Remove the lab directory:

   ```bash
   cd ~ && rm -rf ~/labs/vol07-ch04
   ```

   **Expected result:** The directory no longer exists. No cloud network
   resources were created at any point in this lab.

## Summary and Completion Checklist

Cloud networking starts with a deliberately sized, centrally tracked
address plan and builds up through routing constructs, topology choice
(peering-based hub-and-spoke versus transit gateway), hybrid connectivity
(VPN versus dedicated connection, ideally combined for resilience), hybrid
DNS resolution, and layered segmentation with security groups and network
ACLs. [Chapter 05](05-cloud-compute-and-workload-placement.md) places compute workloads onto the networks designed here,
and [Chapter 07](07-hybrid-and-multicloud-architecture.md) extends these hybrid connectivity patterns to full
multicloud architecture.

- [ ] Can design a CIDR allocation plan with headroom for growth and
      registered centrally to prevent overlap.
- [ ] Can choose between peering-based hub-and-spoke and a transit gateway
      for a stated spoke count and traffic pattern.
- [ ] Can articulate the trade-offs between site-to-site VPN and dedicated
      private connectivity, and design a resilient combination of both.
- [ ] Can diagnose a connectivity failure using the layered
      security-group/ACL/route-table/connection checklist.
- [ ] Completed Lab 4.1, including the negative test and cleanup.
