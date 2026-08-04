# Chapter 05: ACE Professional — Egress Security and FQDN Filtering

## Learning Objectives

- Cover the ACE Professional's egress pillar: controlling outbound traffic to the internet.
- Understand FQDN-based egress filtering versus IP-based rules, and why it matters.
- Build an FQDN-filtering egress model with free primitives.

## The egress problem

By default, workloads with an internet path can reach **anywhere** outbound — a data-exfiltration and malware-callback risk that native NAT gateways don't constrain. Aviatrix **egress control** filters outbound traffic, ideally by **fully-qualified domain name (FQDN)** rather than IP, because cloud service IPs are dynamic and numerous.

| Approach | Problem it solves / limitation |
|:---|:---|
| No egress control | Any workload reaches any internet host (exfiltration risk) |
| IP allowlist | Breaks as SaaS/CDN IPs rotate; unmanageable at scale |
| **FQDN allowlist (Aviatrix)** | Allow `*.amazonaws.com`, `updates.example.com`; the gateway resolves and enforces by name |

## Hands-On Lab

An nftables/dnsmasq model enforces egress by FQDN. **Cost:** none.

### Lab 5.1 — Default-open egress is the problem

**Objective:** Show an unfiltered workload reaching arbitrary destinations.

```bash
sudo ip netns add wl; sudo ip netns add egw   # workload + egress gateway
sudo ip link add wl-e type veth peer name egw-w
sudo ip link set wl-e netns wl; sudo ip link set egw-w netns egw
sudo ip netns exec wl ip addr add 10.50.1.10/24 dev wl-e; sudo ip netns exec wl ip link set wl-e up
sudo ip netns exec egw ip addr add 10.50.1.1/24 dev egw-w; sudo ip netns exec egw ip link set egw-w up
sudo ip netns exec wl ip route add default via 10.50.1.1
sudo ip netns exec egw ip link set lo up; sudo ip netns exec egw sysctl -w net.ipv4.ip_forward=1 >/dev/null
# with no egress policy on the gateway, the workload's default route reaches "anywhere"
sudo ip netns exec egw nft list ruleset | wc -l
echo "0 rules => open egress: the workload can initiate to any destination the gateway can route"
```

**Expected result:** An empty ruleset on the egress gateway — open egress. The workload can reach any internet destination its default route allows; the Professional exam frames this as the risk egress control closes.

**Negative test:** Relying on the workload's own host firewall for egress control — an attacker with the workload disables it; egress enforced **at the gateway** (outside the workload) is the point.

**Cleanup:** Keep for the next lab.

### Lab 5.2 — FQDN allowlist at the gateway

**Objective:** Permit only named destinations, deny the rest — the Aviatrix egress model.

```bash
# Model FQDN filtering: resolve allowed names to a set, default-deny egress at the gateway
sudo ip netns exec egw nft add table ip egress
sudo ip netns exec egw nft add set ip egress allowed '{ type ipv4_addr; flags timeout; }'
sudo ip netns exec egw nft 'add chain ip egress out { type filter hook forward priority 0; policy drop; }'
sudo ip netns exec egw nft add rule ip egress out ct state established,related accept
sudo ip netns exec egw nft add rule ip egress out ip daddr @allowed accept
sudo ip netns exec egw nft add rule ip egress out udp dport 53 accept   # allow DNS to resolve names
sudo ip netns exec egw nft add rule ip egress out counter drop
# "resolve" an allowed FQDN and add its IP to the set (Aviatrix's gateway does this continuously)
ALLOWED_IP=$(getent hosts example.com | awk '{print $1; exit}')
[ -n "$ALLOWED_IP" ] && sudo ip netns exec egw nft add element ip egress allowed "{ $ALLOWED_IP }"
sudo ip netns exec egw nft list chain ip egress out | grep -c drop
```

**Expected result:** A default-drop egress chain permitting only resolved allowlisted addresses (plus established and DNS) — the FQDN model: the gateway resolves permitted names and enforces by the resulting IPs, refreshing as they rotate. Aviatrix does this natively with wildcard FQDN rules.

**Negative test:** Allowlist by a hardcoded IP for a CDN-hosted service — it works until the CDN rotates IPs, then breaks; **FQDN** rules survive the rotation, which is the exam's core egress argument.

**Cleanup:** Keep for the next lab.

### Lab 5.3 — Verify allow-vs-deny

**Objective:** Prove the allowlist enforces.

```bash
# reachable allowed name vs a denied one (conceptually — the set holds only allowed IPs)
sudo ip netns exec egw nft list set ip egress allowed | grep -o "elements.*" | head -1
echo "traffic to an address in @allowed -> accept; any other outbound -> drop (default policy)"
sudo ip netns exec egw nft list chain ip egress out | tail -3
```

**Expected result:** The allowed set populated and the final `drop` rule present — permitted destinations pass, everything else is denied by default. That default-deny-plus-FQDN-allow posture is what egress control buys.

**Negative test:** Set the chain policy to `accept` "temporarily" — egress reverts to open; default-**deny** is the security property, and the exam checks you keep it.

**Cleanup:** `for ns in wl egw; do sudo ip netns del $ns 2>/dev/null; done`.

### Lab 5.4 — Egress patterns: centralized vs distributed

**Objective:** Understand where egress gateways sit.

```bash
cat <<'EOF'
Centralized egress: spokes route 0.0.0.0/0 to a shared egress VPC/gateway (one place to inspect/log)
Distributed egress: an egress gateway per spoke (lower latency, blast-radius contained, more to manage)
Aviatrix supports both; the Professional exam expects you to choose per requirement
  (compliance/central logging -> centralized; latency/scale -> distributed)
EOF
```

**Expected result:** The two egress designs and their trade-offs — centralized concentrates inspection and logging; distributed reduces latency and blast radius. Matching the pattern to the requirement is a Professional design skill.

**Negative test:** Centralized egress with no HA on the shared gateway — a single choke point becomes a single point of failure; egress gateways need the active-active HA of [Chapter 04](04-professional-multicloud-transit.md).

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The default-open egress risk demonstrated.
- [ ] FQDN allowlist (default-deny) built and verified — surviving IP rotation.
- [ ] Centralized vs distributed egress trade-offs understood.
