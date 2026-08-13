# Chapter 02: ACE Associate — Cloud-Native Networking Foundations

## Learning Objectives

- Cover the ACE Associate's first pillar: the native networking constructs of AWS, Azure, GCP, and OCI.
- Understand what each cloud calls its VPC, subnets, gateways, and transit — and where they differ.
- Model the constructs with free Linux primitives.

## The four clouds' building blocks

The Associate expects you to speak all four providers' networking dialects. The Rosetta stone:

| Concept | AWS | Azure | Google Cloud | OCI |
|:---|:---|:---|:---|:---|
| Virtual network | VPC | VNet | VPC (global) | VCN |
| Subnet | Subnet (AZ-scoped) | Subnet | Subnet (region-scoped) | Subnet |
| Internet egress | IGW + NAT GW | Internet/NAT | Cloud NAT + IGW | Internet/NAT GW |
| Private on-ramp | VGW / DX | VPN GW / ExpressRoute | Cloud VPN / Interconnect | DRG / FastConnect |
| Cloud-native transit | Transit Gateway (TGW) | Virtual WAN / VNet peering | Network Connectivity Center | DRG |
| Routing | Route tables | Route tables / UDR | Routes | Route tables |

Two facts the exam leans on: **AWS subnets are AZ-scoped, GCP subnets are region-scoped** (a GCP subnet spans zones), and **native transit differs per cloud** (TGW vs Virtual WAN vs NCC vs DRG) — which is exactly the inconsistency Aviatrix's overlay hides.

## Hands-On Lab

Free Linux primitives model the constructs. **Cost:** none.

### Lab 2.1 — Model a VPC with subnets and a gateway

**Objective:** Build the universal shape — a virtual network, two subnets, a router.

```bash
sudo ip netns add vpc-rtr        # the "VPC router" (route table)
sudo ip link add vpc-br type bridge; sudo ip link set vpc-br up
mksubnet() { # $1 name  $2 cidr-host
  sudo ip netns add $1
  sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master vpc-br up
  sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-e
  sudo ip netns exec $1 ip link set $1-e up; sudo ip netns exec $1 ip link set lo up; }
mksubnet public 10.10.1.10
mksubnet private 10.10.2.10
sudo ip netns exec public ip addr show public-e | grep inet
```

**Expected result:** Two "subnets" (public/private namespaces) on one "VPC" bridge — the model every cloud shares: a virtual network, subnets, and a routing layer. The public/private split (route to an internet gateway vs not) is the first design decision in all four clouds.

**Negative test:** Give both subnets the same host address — collision; subnets within a VPC must use non-overlapping ranges, the constraint that becomes painful across merged clouds (overlapping CIDRs).

**Rollback:** Keep for the next lab.

### Lab 2.2 — Route tables decide public vs private

**Objective:** Show that the route table, not the subnet, defines "public."

```bash
# a shared "internet gateway" namespace with forwarding
sudo ip netns add igw
sudo ip link add igw-e type veth peer name igw-b
sudo ip link set igw-b master vpc-br up; sudo ip link set igw-e netns igw
sudo ip netns exec igw ip addr add 10.10.0.1/24 dev igw-e; sudo ip netns exec igw ip link set igw-e up
sudo ip netns exec igw sysctl -w net.ipv4.ip_forward=1 >/dev/null
# public subnet gets a default route to the IGW; private does not
sudo ip netns exec public ip route add default via 10.10.0.1
sudo ip netns exec public ip route | grep default && echo "public: has internet path"
sudo ip netns exec private ip route | grep -q default || echo "private: no default route (no internet)"
```

**Expected result:** `public` has a default route to the IGW; `private` does not — the exam's core routing lesson: **a subnet is "public" only because its route table points at an internet gateway.** Same subnet construct, different route table, different reachability.

**Negative test:** Add the IGW default route to `private` too — it becomes internet-facing, the accidental-exposure mistake native networking makes easy (and Aviatrix egress control prevents).

**Rollback:** Namespaces persist for the chapter.

### Lab 2.3 — Peering vs transit

**Objective:** Contrast full-mesh peering with hub transit — the scaling problem Aviatrix solves.

```bash
python3 - <<'EOF'
# Full-mesh peering grows O(n^2); a transit hub grows O(n)
for n in [3, 5, 10, 50]:
    mesh = n*(n-1)//2
    hub = n
    print(f"{n} VPCs: full-mesh peerings={mesh}, transit attachments={hub}")
EOF
```

**Expected result:**

```text
3 VPCs: full-mesh peerings=3, transit attachments=3
5 VPCs: full-mesh peerings=10, transit attachments=5
10 VPCs: full-mesh peerings=45, transit attachments=10
50 VPCs: full-mesh peerings=1225, transit attachments=50
```

Full-mesh peering explodes quadratically; a **transit hub** grows linearly — why every cloud added a transit construct (TGW/vWAN/NCC/DRG) and why Aviatrix transit unifies them. This is the Associate's central architectural argument.

**Negative test:** Peering also isn't transitive (A–B and B–C does not give A–C) — a fact the exam tests and a reason hubs win.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — The multicloud problem statement

**Objective:** Name the native constraints Aviatrix exists to solve.

```bash
cat <<'EOF'
Native multicloud pain (ACE Associate themes):
  - route table limits (e.g. AWS route-table entry caps)
  - overlapping CIDRs when orgs/clouds merge (native peering forbids overlap)
  - inconsistent transit (TGW vs vWAN vs NCC vs DRG) and per-cloud feature gaps
  - no unified egress control, encryption, or visibility across clouds
Aviatrix overlay answer: gateways + Controller programming consistent transit, NAT for overlaps,
  encryption in flight, egress FQDN filtering, and CoPilot visibility — one model, four clouds
EOF
```

**Expected result:** The problem/solution framing the Associate builds toward — native networking works per-cloud but fragments across clouds; the Aviatrix overlay restores consistency. [Chapter 03](03-associate-aviatrix-architecture.md) covers how.

**Negative test:** Assuming native peering handles overlapping CIDRs — it refuses them; the overlay's NAT is what makes merged/overlapping estates work.

**Rollback:** `for ns in public private igw vpc-rtr; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del vpc-br`.

## Summary and Completion Checklist

- [ ] The four clouds' networking constructs and their differences mapped.
- [ ] Route-table-defines-public and peering-vs-transit lessons drilled.
- [ ] The native multicloud constraints (limits, overlaps, inconsistent transit) named.
