# Chapter 04: ACE Professional — Multicloud Transit and High Availability

## Learning Objectives

- Cover the ACE Professional's transit pillar: multicloud transit peering, route propagation, and HA.
- Understand active-active gateways, ECMP, and failover behavior.
- Model transit routing and failover with free routing tools.

## The exam in brief

**ACE Professional** is 3 days of instructor-led, hands-on training (prerequisite: ACE Associate + ~1 year cloud experience). Its objectives are practical: build multicloud transit, insert firewalls, control egress, and connect users/sites. This chapter covers **transit and HA**; [Chapter 05](05-professional-egress-security.md)–[Chapter 07](07-professional-user-and-site-connectivity.md) cover egress, firewall insertion, and connectivity.

## Transit at scale

| Concept | Behavior |
|:---|:---|
| **Transit peering** | Aviatrix transit gateways in different regions/clouds peer to form one backbone |
| **Route propagation** | The Controller propagates spoke routes across peered transits (with filtering) |
| **Active-active HA** | Transit and spoke gateways run as pairs; both forward (ECMP), not active-standby |
| **Gateway failover** | On failure, the surviving gateway carries the load; the Controller re-programs routes |
| **Segmentation** | Network domains on transit keep spoke groups isolated unless a connection policy allows |

## Hands-On Lab

FRR (or iproute2 + ECMP) models transit routing and failover. **Cost:** none.

### Lab 4.1 — Two transits peered into one backbone

**Objective:** Model transit-to-transit peering across "clouds."

```bash
sudo ip link add t1 type bridge; sudo ip link add t2 type bridge
sudo ip link set t1 up; sudo ip link set t2 up
# transit gateways in "cloud A" and "cloud B", peered by a veth
sudo ip netns add tgwA; sudo ip netns add tgwB
sudo ip link add peer-a type veth peer name peer-b
sudo ip link set peer-a netns tgwA; sudo ip link set peer-b netns tgwB
sudo ip netns exec tgwA ip addr add 169.254.0.1/30 dev peer-a; sudo ip netns exec tgwA ip link set peer-a up
sudo ip netns exec tgwB ip addr add 169.254.0.2/30 dev peer-b; sudo ip netns exec tgwB ip link set peer-b up
sudo ip netns exec tgwA ip link set lo up; sudo ip netns exec tgwB ip link set lo up
sudo ip netns exec tgwA sysctl -w net.ipv4.ip_forward=1 >/dev/null
sudo ip netns exec tgwB sysctl -w net.ipv4.ip_forward=1 >/dev/null
# each transit owns a spoke CIDR; propagate across the peering
sudo ip netns exec tgwA ip route add 10.30.0.0/16 via 169.254.0.2   # reach cloud B's spokes
sudo ip netns exec tgwB ip route add 10.20.0.0/16 via 169.254.0.1   # reach cloud A's spokes
sudo ip netns exec tgwA ip route | grep 10.30
```

**Expected result:** Two transit gateways peered, each carrying a route to the other's spoke CIDR — the multicloud backbone. In Aviatrix the Controller does this propagation automatically (with route filtering); here you see the routes it would program.

**Negative test:** Propagate without filtering and include an overlapping CIDR — ambiguous routing; Aviatrix transit uses route filtering and NAT to keep overlapping estates deterministic, a Professional topic.

**Cleanup:** Keep for the next lab.

### Lab 4.2 — Active-active with ECMP

**Objective:** Model two forwarding gateways sharing load (not active-standby).

```bash
# a spoke reaching a destination via TWO equal-cost next hops (the active-active gateway pair)
sudo ip netns add spoke-ha
sudo ip link add sha-1 type veth peer name sha-1b; sudo ip link add sha-2 type veth peer name sha-2b
sudo ip link set sha-1 netns spoke-ha; sudo ip link set sha-2 netns spoke-ha
sudo ip netns exec spoke-ha ip addr add 192.168.1.2/30 dev sha-1
sudo ip netns exec spoke-ha ip addr add 192.168.2.2/30 dev sha-2
sudo ip netns exec spoke-ha ip link set sha-1 up; sudo ip netns exec spoke-ha ip link set sha-2 up
sudo ip netns exec spoke-ha ip route add 10.0.0.0/8 \
  nexthop via 192.168.1.1 weight 1 nexthop via 192.168.2.1 weight 1
sudo ip netns exec spoke-ha ip route get 10.5.5.5 2>/dev/null | head -1
sudo ip netns exec spoke-ha ip route show 10.0.0.0/8
```

**Expected result:** A multipath route with two equal-cost next hops — active-active HA: **both gateways forward**, load-shared by ECMP, unlike active-standby where one sits idle. This is the Aviatrix HA model the Professional exam expects.

**Negative test:** Configure a single next hop "with a standby" — you lose half your throughput and add failover delay; active-active is why Aviatrix HA both scales and fails over fast.

**Cleanup:** Keep for the next lab.

### Lab 4.3 — Failover

**Objective:** Prove traffic survives losing one gateway.

```bash
# drop one next hop (simulate a gateway failure); the route falls back to the survivor
sudo ip netns exec spoke-ha ip route replace 10.0.0.0/8 nexthop via 192.168.2.1 weight 1
sudo ip netns exec spoke-ha ip route show 10.0.0.0/8 | grep -c 192.168.2.1
echo "surviving gateway now carries all traffic — the Controller would re-converge routes"
```

**Expected result:** The route now points only at the surviving next hop — failover. In Aviatrix, gateway health is monitored and the Controller re-programs routing on failure; workloads keep flowing on the survivor.

**Negative test:** A design with a single gateway (no HA pair) — the failure is an outage, not a failover; the Professional exam expects HA pairs everywhere in the transit/spoke path.

**Cleanup:** Keep for the next lab.

### Lab 4.4 — Network segmentation on transit

**Objective:** Model transit network domains isolating spoke groups.

```bash
python3 - <<'EOF'
# Aviatrix segmentation: spokes are placed in network domains; only allowed domain-pairs connect
domains = {"prod": ["spoke-a","spoke-b"], "dev": ["spoke-c"], "shared": ["spoke-svc"]}
policy = {("prod","shared"), ("dev","shared")}   # prod<->shared and dev<->shared allowed; prod<->dev NOT
def can_talk(d1, d2):
    return d1 == d2 or (d1,d2) in policy or (d2,d1) in policy
for a in ["prod","dev","shared"]:
    for b in ["prod","dev","shared"]:
        if a < b: print(f"{a} <-> {b}: {'ALLOW' if can_talk(a,b) else 'DENY'}")
EOF
```

**Expected result:**

```text
dev <-> prod: DENY
dev <-> shared: ALLOW
prod <-> shared: ALLOW
```

Transit **network domains** segment spoke groups: prod and dev are isolated, both reach shared services — segmentation in the fabric, not per-VPC ACLs. This is the Professional's segmentation model (and the on-ramp to Distributed Cloud Firewall in [Chapter 06](06-professional-firewall-insertion.md)).

**Negative test:** Placing prod and dev in the same domain "to simplify" — they gain full reachability; domains exist precisely to prevent that lateral path.

**Cleanup:** `for ns in tgwA tgwB spoke-ha; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del t1; sudo ip link del t2`.

## Summary and Completion Checklist

- [ ] Multicloud transit peering and route propagation modeled.
- [ ] Active-active HA (ECMP) and failover drilled — both gateways forward.
- [ ] Transit network-domain segmentation understood.
