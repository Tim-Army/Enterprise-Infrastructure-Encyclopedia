# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: an xDome collector on a SPAN and an integrated enforcer.
- Stand up the Track 2 estate: four zones routed through a host that both observes and enforces.
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Claroty xDome (SaaS), a collector on a SPAN/mirror, an integrated firewall/NAC | Claroty (commercial; design-level here) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2`, `tcpdump` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: collector, SPAN, and integration (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** In a real xDome deployment you place a **collector** on a **SPAN/mirror port** so it passively sees OT traffic without being inline; xDome discovers assets and baselines communications from that feed. Enforcement is delegated: xDome **integrates** with a firewall (Fortinet/Palo Alto/Check Point), NAC (Cisco ISE), or switch, and pushes the segmentation policy there:

```text
xdome> Collectors > add collector-1 (SPAN of the OT segment)
xdome> Integrations > add fw-1 (firewall)  /  ise-1 (NAC)
```

**Expected result (design).** A collector feeding xDome and at least one enforcer integration. Track 2 builds both roles on one host.

**Rollback.** None (design).

### Exercise 2.2 — Track 2: build zones, a collector, and an enforcer

**Objective.** Create four zone subnets routed through a host that captures all traffic and can filter it.

**Track 2 — Walkthrough.** The host is the router between four zone subnets, so every inter-zone flow passes it — that is both the **SPAN** (the host can `tcpdump` the traffic) and the **enforcer** (the host's nftables `forward` chain):

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 tcpdump netcat-openbsd

mkzone() { # $1 name  $2 third-octet  $3 host-ip
  sudo ip netns add $1
  sudo ip link add $1-e type veth peer name $1-b
  sudo ip addr add 10.70.$2.1/24 dev $1-b; sudo ip link set $1-b up
  sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-e
  sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via 10.70.$2.1; }
mkzone web 1 10.70.1.10     # IT-App
mkzone db  2 10.70.2.20     # IT-Data
mkzone hmi 3 10.70.3.30     # OT-Ops
mkzone plc 4 10.70.4.40     # OT-Control
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

**Expected result.**

```bash
sudo ip netns exec hmi ping -c1 10.70.2.20 | grep -o "1 received"
1 received
```

Every zone reaches every other through the host — the flat, unsegmented starting point a passive tool is dropped into.

**Negative test.** A packet between two zones must pass the host; there is no other path, which is what lets the host observe and later enforce.

**Rollback.** Namespaces persist for the lab.

### Exercise 2.3 — Start services

**Objective.** Put a listener on db:5432 and plc:502.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

**Expected result.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.70.2.20 5432 && echo DB-OPEN'
DB-OPEN
```

**Negative test.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.70.2.20 502 || echo DB-502-CLOSED'
DB-502-CLOSED
```

**Rollback.** Leave services running.

## Summary and Completion Checklist

- [ ] Track 1 collector/SPAN + integrated enforcer understood.
- [ ] Track 2: four zones routed through a host that both observes and enforces.
- [ ] Services up on db:5432 and plc:502.
- [ ] Baseline reachability confirmed (flat, pre-segmentation).
