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

These labs cover the **AZ-700 "Skills measured" outline** (Network
Engineer), domain by domain at Microsoft's weights. Each is a walkthrough:
run the `az network` command and compare against the stated result.
Mapping is in the
[volume README](../README.md#lab-coverage--az-700-network-engineer).

**Cost note:** VNets, subnets, peerings, NSGs, and route tables are free.
A Standard load balancer and a private DNS zone are negligible. A VPN
gateway is the one costly resource — Lab 4.9 provisions the gateway object
but you can read the expected result and skip it. Lab 4.16 deletes the
resource group.

**Prerequisites**

```bash
az group create --name rg-az700-lab --location eastus
az configure --defaults group=rg-az700-lab location=eastus
```

**Expected result:** `"provisioningState": "Succeeded"`.

### Domain 1 — Design and implement core networking infrastructure (25–30%)

### Lab 4.1 — Create and configure virtual networks and subnets *(topic 1)*

```bash
az network vnet create --name vnet-hub --address-prefix 10.0.0.0/16 \
  --subnet-name snet-shared --subnet-prefix 10.0.1.0/24
az network vnet subnet create --vnet-name vnet-hub --name GatewaySubnet \
  --address-prefix 10.0.255.0/27
az network vnet subnet list --vnet-name vnet-hub \
  --query "[].{name:name, prefix:addressPrefix}" -o table
```

**Expected result:** `snet-shared` and `GatewaySubnet`. The
`GatewaySubnet` name is mandatory and reserved — a VPN/ExpressRoute gateway
will not deploy without it.

### Lab 4.2 — Configure virtual network peering *(topic 1)*

```bash
az network vnet create --name vnet-spoke --address-prefix 10.1.0.0/16 \
  --subnet-name snet-app --subnet-prefix 10.1.1.0/24
az network vnet peering create --name hub-to-spoke --vnet-name vnet-hub \
  --remote-vnet vnet-spoke --allow-vnet-access
az network vnet peering create --name spoke-to-hub --vnet-name vnet-spoke \
  --remote-vnet vnet-hub --allow-vnet-access
az network vnet peering show --name hub-to-spoke --vnet-name vnet-hub \
  --query "peeringState" -o tsv
```

**Expected result:** `Connected`. Peering must be created from **both**
sides and is **not transitive** — two spokes peered to a hub cannot reach
each other without a gateway or route.

### Lab 4.3 — Configure public IPs and user-defined routes *(topic 1)*

```bash
az network route-table create --name rt-spoke
az network route-table route create --route-table-name rt-spoke --name to-nva \
  --address-prefix 0.0.0.0/0 --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.1.4
az network route-table route list --route-table-name rt-spoke \
  --query "[].{name:name, prefix:addressPrefix, hop:nextHopType}" -o table
```

**Expected result:** a `0.0.0.0/0` route to a VirtualAppliance. A UDR
overrides system routes — this is how spoke egress is forced through a
firewall in the hub.

### Domain 2 — Design, implement, and manage connectivity services (20–25%)

### Lab 4.4 — Create a Cloud Router equivalent (VPN gateway prerequisites)

```bash
az network public-ip create --name pip-vpngw --sku Standard --allocation-method Static
az network public-ip show --name pip-vpngw --query "{name:name, sku:sku.name, ip:ipAddress}" -o table
```

**Expected result:** a Standard static public IP. HA VPN gateways require
a Standard public IP; this is the prerequisite the gateway consumes.

### Lab 4.5 — Site-to-Site VPN gateway *(topic 2)*

```bash
az network vnet-gateway create --name vgw-az700 --vnet vnet-hub \
  --public-ip-addresses pip-vpngw --gateway-type Vpn --vpn-type RouteBased \
  --sku VpnGw1 --no-wait
az network vnet-gateway show --name vgw-az700 --query "provisioningState" -o tsv 2>/dev/null || echo "Provisioning (takes ~30 min)"
```

**Expected result:** `Updating`/`Succeeded` (creation is slow). Route-based
VPN is the type that supports coexistence and multiple tunnels — the
examinable default. ExpressRoute is the private-circuit alternative.

### Domain 3 — Design and implement private access to Azure services (10–15%)

### Lab 4.6 — Service endpoints vs private endpoints *(topic 3)*

```bash
SA="stpriv700$RANDOM"
az storage account create --name "$SA" --sku Standard_LRS --kind StorageV2
az network vnet subnet update --vnet-name vnet-spoke --name snet-app \
  --service-endpoints Microsoft.Storage
az network vnet subnet show --vnet-name vnet-spoke --name snet-app \
  --query "serviceEndpoints[].service" -o tsv
```

**Expected result:** `Microsoft.Storage`. A service endpoint extends the
subnet identity to the service (traffic still hits a public endpoint); a
**Private Endpoint** places a private IP in the subnet and removes the
public path — the stronger control, exercised next.

### Lab 4.7 — Private endpoint for a PaaS service *(topic 3)*

```bash
az network private-endpoint create --name pe-storage --vnet-name vnet-spoke \
  --subnet snet-app --private-connection-resource-id \
  "$(az storage account show --name "$SA" --query id -o tsv)" \
  --group-id blob --connection-name pe-conn
az network private-endpoint show --name pe-storage \
  --query "{name:name, ip:customDnsConfigs[0].ipAddresses[0]}" -o table
```

**Expected result:** a private endpoint with an IP from the subnet range.
Now the storage account is reachable over private space and can be cut off
from the internet — the answer to "must not be publicly reachable."

### Domain 4 — Design and implement network security (15–20%)

### Lab 4.8 — Network security groups and application security groups *(topic 4)*

```bash
az network nsg create --name nsg-app
az network nsg rule create --nsg-name nsg-app --name deny-inbound-internet \
  --priority 200 --access Deny --direction Inbound --source-address-prefixes Internet \
  --destination-port-ranges '*' --protocol '*'
az network nsg rule list --nsg-name nsg-app \
  --query "[].{name:name, access:access, src:sourceAddressPrefix}" -o table
```

**Expected result:** an explicit `Deny` from `Internet`. NSGs are
stateful, priority-ordered, with an implied allow-VNet / deny-Internet
baseline; explicit rules make intent auditable.

### Lab 4.9 — Azure Firewall and Bastion (secure access) *(topic 4)*

```bash
az network vnet subnet create --vnet-name vnet-hub --name AzureFirewallSubnet \
  --address-prefix 10.0.2.0/26
az network vnet subnet list --vnet-name vnet-hub --query "[].name" -o tsv | grep Firewall
```

**Expected result:** `AzureFirewallSubnet` (another reserved, mandatory
name). Azure Firewall centralizes egress control in the hub; Bastion
(`AzureBastionSubnet`) gives RDP/SSH without public IPs on VMs.

### Domain 5 — Design and implement application delivery services (15–20%)

### Lab 4.10 — Load balancer and its tiers *(topic 5)*

```bash
az network lb create --name lb-az700 --sku Standard \
  --frontend-ip-name fe --backend-pool-name be
az network lb show --name lb-az700 --query "{name:name, sku:sku.name}" -o table
echo "Delivery: Load Balancer (L4 regional) | App Gateway (L7+WAF regional) | Front Door (L7 global) | Traffic Manager (DNS global)"
```

**Expected result:** `lb-az700 Standard`, plus the selection table. Choose
by layer (transport vs application) and scope (regional vs global) — the
recurring AZ-700 decision.

### Lab 4.11 — Azure DNS and name resolution *(topic 5)*

```bash
az network private-dns zone create --name privatelink.blob.core.windows.net
az network private-dns link vnet create --zone-name privatelink.blob.core.windows.net \
  --name link-spoke --virtual-network vnet-spoke --registration-enabled false
az network private-dns zone show --name privatelink.blob.core.windows.net \
  --query "{zone:name, links:numberOfVirtualNetworkLinks}" -o table
```

**Expected result:** the private DNS zone linked to the spoke. This
`privatelink` zone is what makes the Lab 4.7 private endpoint resolvable by
name — private endpoints and private DNS are examined together.

### Lab 4.12 — Troubleshoot connectivity *(topic 1/5)*

```bash
az network watcher configure --locations eastus --enabled true 2>/dev/null || true
az network watcher list --query "[].{name:name, location:location}" -o table | head -3
```

**Expected result:** Network Watcher enabled in the region. Connection
Troubleshoot and IP Flow Verify identify whether an NSG rule, a route, or
the destination dropped a flow — the three causes a failed ping cannot
distinguish.

### Lab 4.13 — Negative test: prove peering is not transitive

```bash
az network vnet create --name vnet-spoke2 --address-prefix 10.2.0.0/16 \
  --subnet-name snet-b --subnet-prefix 10.2.1.0/24
az network vnet peering create --name hub-to-spoke2 --vnet-name vnet-hub \
  --remote-vnet vnet-spoke2 --allow-vnet-access
az network vnet peering create --name spoke2-to-hub --vnet-name vnet-spoke2 \
  --remote-vnet vnet-hub --allow-vnet-access
az network vnet peering list --vnet-name vnet-spoke \
  --query "[].remoteVirtualNetwork.id" -o tsv | grep -c spoke2
```

**Expected result:** `0` — spoke1 peers only with the hub, **not** with
spoke2, even though both peer the hub. Peering is not transitive; reaching
spoke2 from spoke1 needs a gateway/route or direct peering. That is the
fact all Azure topology design turns on.

### Lab 4.14 — Cleanup

```bash
az group delete --name rg-az700-lab --yes --no-wait
az group exists --name rg-az700-lab
```

**Expected result:** `false` shortly after — VNets, gateway, endpoints,
NSGs, DNS zone, and load balancer removed together.

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
