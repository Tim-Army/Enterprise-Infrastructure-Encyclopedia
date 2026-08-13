# Chapter 03: ACE Associate — Aviatrix Architecture and Design Patterns

## Learning Objectives

- Cover the ACE Associate's second pillar: the Aviatrix overlay — Controller, CoPilot, gateways.
- Understand the core design patterns: transit, spoke attachment, encryption, and the single control plane.
- Model the overlay's routing behavior with free primitives.

## The overlay, assembled

Aviatrix inserts a software data plane (**gateways**) into cloud-native networks and programs it from a central **Controller**, observed through **CoPilot**. The Associate expects you to explain each piece and the patterns they form.

| Pattern | What it is |
|:---|:---|
| **Transit gateway (Aviatrix)** | A gateway pair in a transit VPC/VNet forming the multicloud backbone; active-active HA |
| **Spoke attachment** | Workload VPCs attach to transit via spoke gateways; the Controller programs the routes |
| **Encryption** | Aviatrix encrypts inter-gateway traffic (IPsec/high-performance encryption) — including over native links that don't encrypt by default |
| **Single control plane** | One Controller programs routing/policy across all clouds; CoPilot shows one topology |
| **Insertion points** | Egress, FireNet, and DCF hang off the transit/spoke gateways (later chapters) |

The value proposition the Associate must articulate: **consistent behavior and one operational model across clouds**, with encryption and visibility native networking lacks.

## Hands-On Lab

Free primitives model the overlay's routing and encryption behavior. **Cost:** none.

### Lab 3.1 — Transit-and-spoke topology

**Objective:** Build the hub-and-spoke the Aviatrix overlay creates.

```bash
sudo ip link add transit type bridge; sudo ip link set transit up
sudo ip netns add tgw   # the Aviatrix transit gateway (router)
sudo ip link add tgw-e type veth peer name tgw-b; sudo ip link set tgw-b master transit up
sudo ip link set tgw-e netns tgw; sudo ip netns exec tgw ip addr add 100.64.0.1/24 dev tgw-e
sudo ip netns exec tgw ip link set tgw-e up; sudo ip netns exec tgw ip link set lo up
sudo ip netns exec tgw sysctl -w net.ipv4.ip_forward=1 >/dev/null
mkspoke() { # $1 name  $2 tgw-side-ip  $3 workload-cidr
  sudo ip netns add $1
  sudo ip link add $1-t type veth peer name $1-tb; sudo ip link set $1-tb master transit up
  sudo ip link set $1-t netns $1; sudo ip netns exec $1 ip addr add $2/24 dev $1-t
  sudo ip netns exec $1 ip link set $1-t up; sudo ip netns exec $1 ip link set lo up
  sudo ip netns exec $1 ip addr add $3 dev lo          # the spoke's "workload" address
  sudo ip netns exec $1 ip route add default via 100.64.0.1
  sudo ip netns exec $1 sysctl -w net.ipv4.ip_forward=1 >/dev/null
  sudo ip netns exec tgw ip route add ${3%/*}/32 via $2; }   # controller programs the transit route
mkspoke aws-spoke   100.64.0.11 10.20.1.1/32
mkspoke azure-spoke 100.64.0.12 10.30.1.1/32
```

**Expected result:** Two spokes (modeling AWS and Azure workload VPCs) attached to one transit gateway, with the "Controller" programming each spoke's route into the transit — the hub-and-spoke the Aviatrix overlay builds. The transit holds routes to every spoke; spokes default toward transit.

**Negative test:** Attach a spoke but skip the transit-side route (`ip route add` in tgw) — traffic reaches the transit and dies; the Controller's job is programming those routes, and forgetting them is the overlay's version of an unattached spoke.

**Rollback:** Keep for the next lab.

### Lab 3.2 — Prove any-to-any transit reachability

**Objective:** Show spokes reach each other only through transit (never directly).

```bash
sudo ip netns exec aws-spoke ping -c1 -W2 10.30.1.1 | grep -o "1 received" && echo "aws-spoke -> azure-spoke via transit OK"
sudo ip netns exec tgw ip route | grep -E "10.20.1.1|10.30.1.1"
```

**Expected result:** `1 received` — the AWS spoke reaches the Azure spoke's workload address **through the transit hub**, with the transit route table listing both. This is multicloud transit in miniature: spokes never peer directly; the hub carries everything, so adding a spoke is O(1).

**Negative test:** Remove the Azure spoke's route from transit — the ping fails though both spokes are "up"; reachability is a property of the transit route table the Controller programs, not of the attachment alone.

**Rollback:** Keep for the next lab.

### Lab 3.3 — Encryption in flight

**Objective:** Model the Aviatrix property native transit often lacks — encryption between gateways.

```bash
# Model the concept: a WireGuard tunnel between two "gateways" (stands in for Aviatrix encrypted transit)
sudo apt-get install -y wireguard-tools 2>/dev/null || echo "wireguard-tools models encrypted gateway-to-gateway"
cat <<'EOF'
Aviatrix encrypts inter-gateway traffic (IPsec / high-performance encryption), even across native
links that are cleartext by default (e.g. some intra-region paths). The concept: workload traffic
rides an encrypted tunnel between gateways, so the backbone is confidential end to end.
EOF
sudo ip netns exec tgw sh -c 'echo "transit gateway would terminate encrypted tunnels from each spoke"'
```

**Expected result:** The encryption model stated and gateway roles confirmed — the Associate must know Aviatrix provides **encryption between gateways** (a differentiator over native transit that may not encrypt), scaling to high throughput with its accelerated encryption.

**Negative test:** Assuming native cloud transit is always encrypted — it isn't uniformly; the exam tests knowing where Aviatrix adds confidentiality.

**Rollback:** Keep for the next lab.

### Lab 3.4 — The single control plane and CoPilot

**Objective:** Articulate what the Controller and CoPilot each own.

```bash
cat <<'EOF'
Controller (control plane):  deploys gateways, programs transit/spoke routing, holds policy,
  manages overlaps (NAT), pushes config to every cloud from one place.
CoPilot (operations plane):  topology map, FlowIQ flow visibility, latency/throughput, alerts,
  audit and compliance views — one pane across AWS/Azure/GCP/OCI.
Together: define once on the Controller, observe everywhere in CoPilot.
EOF
sudo ip netns exec tgw ip route | wc -l   # the "controller-programmed" route count on transit
```

**Expected result:** A clear split — Controller programs, CoPilot observes — and the transit's programmed-route count as a stand-in for what one control plane manages. The Associate's closing theme: **one control plane, one observability plane, all clouds.**

**Negative test:** Conflating CoPilot (observe) with the Controller (configure) — the exam separates configuration from visibility; changes are made on the Controller, not in CoPilot.

**Rollback:** `for ns in tgw aws-spoke azure-spoke; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del transit`.

## Summary and Completion Checklist

- [ ] The Aviatrix overlay (Controller, CoPilot, gateways) and its patterns internalized.
- [ ] Transit-and-spoke built and any-to-any reachability proven through the hub.
- [ ] Encryption-in-flight and the Controller-vs-CoPilot split understood.
- [ ] ACE Associate coverage complete across Chapters 02–03.
