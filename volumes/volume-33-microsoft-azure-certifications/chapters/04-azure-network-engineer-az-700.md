# Chapter 04: Azure Network Engineer — AZ-700

## Learning Objectives

- Place AZ-700 as the networking depth beyond AZ-104's virtual-networking
  coverage, and identify who should sit it
- Design hybrid connectivity with VPN Gateway and ExpressRoute, and choose
  between them from stated requirements
- Explain hub-and-spoke topology, virtual network peering, and Azure
  Virtual WAN as three answers to the same scaling problem
- Distinguish the load-balancing services — Load Balancer, Application
  Gateway, Front Door, Traffic Manager — by layer and scope
- Verify routing and connectivity with Azure's own diagnostic tooling
  rather than by inference

## Theory and Architecture

### Where AZ-104 stops

[Chapter 03](03-azure-administrator-az-104.md)'s administrator configures
virtual networks, subnets, and network security groups. **AZ-700,
Microsoft Certified: Azure Network Engineer Associate**, is where the
network becomes the subject rather than a supporting service: hybrid
connectivity, routing design, private access to PaaS, and the
load-balancing portfolio. It carries no announced retirement date
(verified 23 July 2026) and renews annually.

Sit it if you design or operate connectivity between Azure and
on-premises, run a multi-region estate, or own the network in an
organization where that is a distinct role.

### Hybrid connectivity: two mechanisms, different guarantees

| | Site-to-Site VPN | ExpressRoute |
| --- | --- | --- |
| Path | Over the public internet, IPsec-encrypted | Private circuit via a connectivity provider |
| Bandwidth | Gateway SKU dependent, modest | Up to very high, provisioned |
| Latency | Variable — internet-dependent | Predictable |
| SLA | On the gateway | On the circuit, higher availability options |
| Typical use | Branch offices, lower-value links, backup path | Data center interconnect, latency- or compliance-sensitive workloads |

The examinable judgment is not which is "better" but which the stated
constraints require. A requirement naming *predictable latency* or
*traffic that must not traverse the public internet* points to
ExpressRoute; a requirement emphasizing cost and speed of provisioning
points to VPN. A common production design uses **both**, with VPN as the
failover path for an ExpressRoute circuit.

### Topology: peering, hub-and-spoke, and Virtual WAN

- **Virtual network peering** connects two virtual networks directly, with
  traffic staying on the Microsoft backbone. Peering is **not transitive**
  — this single fact drives most Azure topology design.
- **Hub-and-spoke** places shared services (firewall, gateways, DNS) in a
  hub virtual network with workload spokes peered to it. Because peering
  is not transitive, spoke-to-spoke traffic requires either a network
  virtual appliance or Azure Firewall in the hub with user-defined routes,
  or direct peering between the spokes.
- **Azure Virtual WAN** is Microsoft's managed alternative: a hub it
  operates, with transitive routing built in, which removes the manual
  route management hub-and-spoke demands at scale.

### Routing: system routes and what overrides them

Azure creates system routes automatically. **User-defined routes (UDRs)**
override them, most often to force traffic through an appliance. Route
selection follows longest-prefix match, and where prefixes tie, the order
is user-defined route, then BGP route, then system route. Getting this
order wrong is the classic cause of traffic mysteriously bypassing a
firewall.

### Private access to PaaS

Two mechanisms, frequently confused:

- **Service endpoints** extend the virtual network identity to the
  service; traffic still reaches a public endpoint but the service can
  restrict access to the subnet.
- **Private Endpoint** places a private IP from your subnet in front of
  the service, so the service is reachable over private address space and
  can be cut off from the public internet entirely. It is the stronger
  control and the direction Microsoft has moved.

### Load balancing: pick by layer and scope

| Service | Layer | Scope |
| --- | --- | --- |
| Azure Load Balancer | 4 (TCP/UDP) | Regional |
| Application Gateway | 7 (HTTP/S, with WAF) | Regional |
| Azure Front Door | 7 (HTTP/S, with WAF) | Global |
| Traffic Manager | DNS-based | Global |

Two axes decide it: **which layer** the routing decision needs (transport
or application) and **what scope** it spans (one region or many).

## Design Considerations

- **Design from the non-transitivity of peering.** Almost every Azure
  topology question reduces to it. Decide early whether the estate needs a
  hub with routing appliances or Virtual WAN's managed transitivity.
- **Choose hybrid links by constraint, not preference.** Let the stated
  latency, compliance, and bandwidth requirements select VPN or
  ExpressRoute; propose both where the design needs a failover path.
- **Prefer Private Endpoint for new designs.** Where the requirement is
  that a PaaS service must not be reachable publicly, service endpoints do
  not satisfy it and Private Endpoint does.
- **Place UDRs deliberately and document them.** A forced-tunnel route
  that nobody remembers is the hardest Azure networking fault to diagnose,
  because connectivity fails in a way that looks like a firewall problem.
- **Do not over-reach into AZ-104's ground.** If NSGs and basic virtual
  networks are still shaky, AZ-104 first; AZ-700 assumes them.

## Implementation and Automation

### Hub-and-spoke with non-transitive peering

```bash
az group create --name rg-az700-lab --location eastus
az network vnet create -g rg-az700-lab -n vnet-hub --address-prefix 10.0.0.0/16 \
  --subnet-name snet-shared --subnet-prefix 10.0.1.0/24
az network vnet create -g rg-az700-lab -n vnet-spoke1 --address-prefix 10.1.0.0/16 \
  --subnet-name snet-app --subnet-prefix 10.1.1.0/24
az network vnet create -g rg-az700-lab -n vnet-spoke2 --address-prefix 10.2.0.0/16 \
  --subnet-name snet-app --subnet-prefix 10.2.1.0/24
```

```bash
# Peer each spoke to the hub — but NOT to each other
for s in spoke1 spoke2; do
  az network vnet peering create -g rg-az700-lab -n hub-to-$s \
    --vnet-name vnet-hub --remote-vnet vnet-$s --allow-vnet-access
  az network vnet peering create -g rg-az700-lab -n $s-to-hub \
    --vnet-name vnet-$s --remote-vnet vnet-hub --allow-vnet-access
done
```

### Inspecting effective routes

```bash
# The authoritative view of what a NIC will actually do with a packet
az network nic show-effective-route-table --name <NIC_NAME> \
  -g rg-az700-lab -o table
```

### A user-defined route forcing traffic to an appliance

```bash
az network route-table create -g rg-az700-lab -n rt-spoke
az network route-table route create -g rg-az700-lab --route-table-name rt-spoke \
  -n to-hub-nva --address-prefix 0.0.0.0/0 \
  --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.1.4
```

## Validation and Troubleshooting

- **Effective routes are the truth.** `show-effective-route-table` states
  what the platform will do; a route table's contents state what you
  intended. When they disagree, the effective view wins.
- **Prove non-transitivity rather than trusting it.** The lab below tests
  spoke-to-spoke reachability explicitly, because the failure is silent
  and surprising the first time.
- **Use Connection Troubleshoot and NSG diagnostics.** Azure Network
  Watcher identifies whether an NSG rule, a route, or the destination
  itself dropped a flow — the three causes that look identical from a
  failed ping.
- **Check both directions of a peering.** Peering is configured per
  virtual network; a one-sided peering leaves the link in a
  non-connected state that is easy to overlook.
- **For hybrid links, verify at the gateway.** Connection status and BGP
  peer state on the gateway distinguish a tunnel problem from a routing
  problem inside Azure.

## Security and Best Practices

- Put shared security services in the hub and force spoke egress through
  them with UDRs; a spoke with a default route straight to the internet
  bypasses every control you built.
- Prefer Private Endpoint over service endpoints where the requirement is
  genuine network isolation of a PaaS service.
- Network security groups are stateful and evaluated by priority — write
  explicit deny rules rather than relying on the implicit default, so
  intent is readable.
- Treat ExpressRoute circuit identifiers and peering configuration as
  sensitive; they describe your private connectivity to a provider.
- Run the lab in the sandbox subscription. Gateways are among the more
  expensive Azure resources, so this chapter's lab deliberately uses
  peering rather than provisioning a gateway.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure Network Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-network-engineer-associate/) (AZ-700)
- [Azure networking documentation](https://learn.microsoft.com/en-us/azure/networking/)
- [Azure Network Watcher](https://learn.microsoft.com/en-us/azure/network-watcher/)
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 03](03-azure-administrator-az-104.md) for the virtual
  networking this builds on.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Why is virtual network peering's non-transitivity the central fact of
   Azure topology design?
2. Give one requirement that forces ExpressRoute over VPN, and one that
   does the reverse.
3. Distinguish a service endpoint from a Private Endpoint, and say which
   satisfies "must not be publicly reachable."
4. Choose between Application Gateway and Front Door for a requirement,
   and justify it on layer and scope.
5. Traffic is bypassing a hub firewall. What do you inspect first, and
   why?

## Hands-On Lab

**Objective:** Build a hub-and-spoke topology and prove for yourself that
peering is not transitive — then observe how effective routes describe it.

**Cost note:** Virtual networks and peerings are free; no gateway or
appliance is provisioned. Step 5 removes everything.

**Prerequisites**

- The sandbox subscription and budget alert from Chapter 01.
- Azure CLI authenticated.

**Steps**

1. **Build the topology (15 minutes).** Create the hub and two spokes and
   peer each spoke to the hub, using the Implementation commands. Do not
   peer the spokes to each other.

   **Expected result:** four peerings, all reporting `Connected`:

   ```bash
   az network vnet peering list -g rg-az700-lab --vnet-name vnet-hub \
     -o table --query '[].{name:name, state:peeringState}'
   ```

2. **Predict, then verify (10 minutes).** Write down whether spoke1 can
   reach spoke2 and why, *before* checking.

   **Expected result:** a written prediction to test.

3. **Negative test — prove non-transitivity (15 minutes).** Inspect the
   effective routes available in spoke1 and confirm there is no route to
   spoke2's address space through the hub:

   ```bash
   az network vnet peering list -g rg-az700-lab --vnet-name vnet-spoke1 \
     -o table --query '[].{remote:remoteVirtualNetwork.id, state:peeringState}'
   ```

   **Expected result:** spoke1 peers only with the hub. There is no path
   to 10.2.0.0/16 — peering did not become transitive through the hub.

4. **Design the fix (10 minutes).** In writing, state the two ways to make
   spoke-to-spoke traffic work, and the cost of each.

   **Expected result:** direct spoke peering (simple, but grows
   quadratically) or a hub appliance plus UDRs (scales, but adds a
   component and route management) — with Virtual WAN named as the managed
   alternative.

5. **Cleanup:**

   ```bash
   az group delete --name rg-az700-lab --yes --no-wait
   ```

   Confirm the group is gone and no gateway was left running.

## Lab Verification

Complete this sign-off once non-transitivity has been demonstrated and the
resource group removed. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

AZ-700 is the networking depth beyond AZ-104: hybrid connectivity, topology,
routing, private PaaS access, and load balancing. Its organizing fact is
that **virtual network peering is not transitive**, which is why hub-and-
spoke needs an appliance and user-defined routes, and why Azure Virtual WAN
exists as the managed alternative. Choose VPN or ExpressRoute from stated
latency, compliance, and bandwidth constraints rather than preference;
prefer Private Endpoint where a PaaS service must not be publicly
reachable; and pick a load balancer by the layer its decision needs and the
scope it spans. Diagnose with effective routes and Network Watcher, because
inference from a failed ping cannot separate an NSG rule from a route.

- [ ] Can explain why peering non-transitivity drives topology design.
- [ ] Can select VPN or ExpressRoute from stated requirements.
- [ ] Can distinguish service endpoints from Private Endpoint.
- [ ] Can choose among Load Balancer, Application Gateway, Front Door, and
      Traffic Manager by layer and scope.
- [ ] Has proven non-transitivity in a built topology.
- [ ] Completed the hands-on lab, including cleanup.
