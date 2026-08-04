# Chapter 06: ACE Professional — Firewall Insertion (FireNet) and Distributed Cloud Firewall

## Learning Objectives

- Cover the ACE Professional's inspection pillar: FireNet (NGFW insertion) and Distributed Cloud Firewall (DCF).
- Understand transparent firewall insertion without re-architecting VPCs.
- Model traffic redirection through an inspection firewall.

## Two ways to firewall east-west and egress

| Model | What it is |
|:---|:---|
| **FireNet** | Aviatrix inserts third-party NGFWs (Palo Alto VM-Series, Fortinet, Check Point) into the traffic path; transit steers flows *through* the firewall for deep inspection, transparently |
| **Distributed Cloud Firewall (DCF)** | Aviatrix's own distributed, policy-based segmentation enforced *in the gateways* across the fabric — no separate firewall appliances |

FireNet is for **deep L7/IPS inspection** with an incumbent NGFW; DCF is for **native distributed segmentation** without appliance hairpinning. The Professional exam expects you to place each.

## Hands-On Lab

A namespace "firewall" plus policy routing models insertion. **Cost:** none.

### Lab 6.1 — FireNet: steer traffic through an inspection firewall

**Objective:** Redirect an inter-spoke flow through a firewall namespace transparently.

```bash
sudo ip link add fabric type bridge; sudo ip link set fabric up
# two spokes + a "firewall" that inspects between them
for n in spokeX spokeY fw; do sudo ip netns add $n
  sudo ip link add $n-e type veth peer name $n-b; sudo ip link set $n-b master fabric up
  sudo ip link set $n-e netns $n; sudo ip netns exec $n ip link set $n-e up; sudo ip netns exec $n ip link set lo up
done
sudo ip netns exec spokeX ip addr add 10.60.1.10/24 dev spokeX-e
sudo ip netns exec spokeY ip addr add 10.60.1.20/24 dev spokeY-e
sudo ip netns exec fw ip addr add 10.60.1.1/24 dev fw-e
sudo ip netns exec fw sysctl -w net.ipv4.ip_forward=1 >/dev/null
# transit "steers" spokeX->spokeY via the firewall (default route through fw)
sudo ip netns exec spokeX ip route add 10.60.1.20/32 via 10.60.1.1
sudo ip netns exec spokeY ip route add 10.60.1.10/32 via 10.60.1.1
sudo ip netns exec spokeX ping -c1 -W2 10.60.1.20 | grep -o "1 received" && echo "spokeX->spokeY traversed the firewall"
```

**Expected result:** `1 received` with the flow routed **through** the firewall namespace — FireNet's essence: the transit steers selected flows through the NGFW for inspection without the spokes knowing. The firewall sees and can inspect every packet.

**Negative test:** Remove the via-firewall routes and the spokes talk directly (uninspected) — FireNet's value is that the fabric *forces* the path through inspection; skip the steering and inspection is bypassed.

**Cleanup:** Keep for the next lab.

### Lab 6.2 — The firewall inspects and can block

**Objective:** Show the inserted firewall enforcing a policy on transited traffic.

```bash
sudo ip netns exec fw nft add table ip insp
sudo ip netns exec fw nft 'add chain ip insp fwd { type filter hook forward priority 0; policy accept; }'
# block a "malicious" port while allowing the sanctioned one
sudo ip netns exec fw nft add rule ip insp fwd tcp dport 23 counter drop     # deny telnet (policy)
sudo ip netns exec spokeY bash -c 'nohup nc -lk -p 22 >/dev/null 2>&1 &'
sudo ip netns exec spokeX bash -c 'nc -z -w2 10.60.1.20 22 && echo "22 allowed through firewall"'
sudo ip netns exec fw nft list chain ip insp fwd | grep dport
```

**Expected result:** Port 22 passes while the firewall holds a rule dropping port 23 — the inserted firewall enforces policy on flows the fabric steers through it (in production, an NGFW doing IPS/L7, not just port rules). FireNet gives incumbent firewalls a place in the cloud path.

**Negative test:** Assume the firewall inspects traffic that never traverses it — only steered flows are inspected; unsteered east-west or egress bypasses FireNet unless policy routes it in.

**Cleanup:** Keep for the next lab.

### Lab 6.3 — DCF: distributed segmentation in the gateways

**Objective:** Model policy-based segmentation without a separate appliance.

```bash
python3 - <<'EOF'
# DCF: tag-based, distributed policy evaluated at each gateway (no appliance hairpin)
tags = {"10.60.1.10":"web", "10.60.1.20":"db", "10.60.1.30":"analytics"}
# policy: web->db:5432 allow; everything else between tags deny
policy = [("web","db",5432,"allow")]
def decide(src, dst, port):
    s, d = tags.get(src), tags.get(dst)
    for (ps,pd,pp,act) in policy:
        if s==ps and d==pd and port==pp: return act.upper()
    return "DENY (default)"
print("web->db:5432 =>", decide("10.60.1.10","10.60.1.20",5432))
print("analytics->db:5432 =>", decide("10.60.1.30","10.60.1.20",5432))
EOF
```

**Expected result:**

```text
web->db:5432 => ALLOW
analytics->db:5432 => DENY (default)
```

DCF evaluates **tag/group-based policy distributed across the gateways** — segmentation enforced everywhere in the fabric at once, no hairpin to a central appliance. It is Aviatrix's answer to microsegmentation ([Volume LXXXVII](../../volume-087-microsegmentation-options/README.md) covers the landscape), and a growing Professional topic.

**Negative test:** Building the same segmentation as FireNet redirect rules — works but hairpins all east-west through the firewall (latency, cost); DCF distributes the enforcement instead.

**Cleanup:** `for ns in spokeX spokeY fw; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del fabric`.

## Summary and Completion Checklist

- [ ] FireNet insertion (steer flows through an NGFW) modeled and enforced.
- [ ] The difference between FireNet (appliance inspection) and DCF (distributed segmentation) understood.
- [ ] DCF tag-based distributed policy modeled.
