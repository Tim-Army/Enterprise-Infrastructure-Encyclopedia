# Chapter 04: Network of One

## Learning Objectives

- Isolate every device so it has no direct Layer 2 peer — a network of one.
- Force all east-west traffic through the enforcement point.
- Confirm the flat VLAN is gone even though no VLAN or IP changed.

## Make every device an island

Airgap's core move is to make each device's only reachable neighbor the **enforcement point**, so there is no direct path between any two endpoints — even on the same subnet. In the real product this is done **agentlessly** by controlling ARP/DHCP. On Track 2 we achieve the same effect by giving each device a **host-scoped view** (`/32`) whose only route is the enforcer, so every packet to a peer is sent to the enforcer instead of directly. No agent runs on the devices; the change is at the network layer.

## Hands-On Lab

### Exercise 4.1 — Collapse each device to a network of one

**Objective.** Reconfigure each device so its only route is the enforcer.

**Track 1 — Walkthrough.** The Airgap enforcement point answers ARP for every address so each device believes the enforcer is its only neighbor; DHCP hands out a host route to the enforcer. No endpoint is modified by hand.

**Track 2 — Walkthrough.** Replace each device's on-link subnet with a `/32` plus a host route to the enforcer (the effect Airgap achieves via ARP/DHCP):

```bash
netone() { # $1 device  $2 ip
  sudo ip netns exec $1 ip addr flush dev $1-e
  sudo ip netns exec $1 ip addr add $2/32 dev $1-e
  sudo ip netns exec $1 ip route add 10.100.1.1 dev $1-e     # only neighbor: the enforcer
  sudo ip netns exec $1 ip route add default via 10.100.1.1; }
for d in web:10 db:20 hmi:30 plc:40 victim:50; do netone ${d%%:*} 10.100.1.${d##*:}; done
# the enforcer answers for the whole subnet
sudo sysctl -w net.ipv4.conf.all.proxy_arp=1 >/dev/null
```

**Expected result.** Each device now has exactly one route to a neighbor — the enforcer — and no on-link peers.

```bash
sudo ip netns exec victim ip route
# 10.100.1.1 dev victim-e
# default via 10.100.1.1 dev victim-e
```

**Negative test.** No VLAN was split and no device's IP changed (`victim` is still `10.100.1.50`) — proof the isolation is agentless and non-disruptive, exactly Airgap's selling point.

**Cleanup.** Keep the isolation.

### Exercise 4.2 — The flat VLAN is gone

**Objective.** Confirm devices can no longer reach each other directly (default-deny is implicit until policy is added).

**Track 2 — Walkthrough.** With no east-west policy yet on the enforcer, add a default-deny so the enforcer does not simply route everything:

```bash
sudo nft add table inet airgap
sudo nft add chain inet airgap forward '{ type filter hook forward priority 0 ; policy drop ; }'
sudo nft add rule inet airgap forward ct state established,related accept
# re-run the worm from Chapter 03
sudo ip netns exec victim bash -c '
for ip in 10.100.1.20 10.100.1.40; do nc -z -w1 $ip 502 2>/dev/null || nc -z -w1 $ip 5432 2>/dev/null && echo "reached $ip" || true; done; echo "worm sweep done"'
```

**Expected result.** The worm now reaches nothing — every east-west connection is dropped at the enforcer because there is no direct path and no policy permits it:

```bash
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.20 5432 && echo victim->db OPEN || echo victim->db BLOCKED'
victim->db BLOCKED
```

Every device is an island; the flat VLAN's lateral surface is gone.

**Negative test.** Even the *legitimate* `web → db` is now blocked — good: the network-of-one denies **everything** by default, and Chapter 05 re-permits only the one sanctioned flow. Isolation first, exceptions second.

**Cleanup.** Keep the isolation and default-deny.

## Summary and Completion Checklist

- [ ] Every device collapsed to a network of one (only neighbor: the enforcer).
- [ ] No VLAN or IP changed — agentless and non-disruptive.
- [ ] East-west lateral movement eliminated (default-deny).
- [ ] Ready to re-permit the single sanctioned flow.
