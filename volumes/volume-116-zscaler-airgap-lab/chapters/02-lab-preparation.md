# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: an Airgap enforcement point controlling ARP/DHCP on a VLAN.
- Stand up the Track 2 estate: five devices on one flat VLAN plus an enforcement point.
- Confirm the flat VLAN before any isolation exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Airgap enforcement point (Zscaler), the VLAN it protects | Zscaler/Airgap (commercial; design-level here) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: the Airgap enforcement point (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** The Airgap enforcement point is inserted on the VLAN and takes over **ARP/DHCP** so that it becomes the only device every endpoint can resolve; all east-west traffic is thereby drawn to it and brokered. No agent is installed on any endpoint and no subnet changes — the endpoints keep their addresses and are unaware.

**Expected result (design).** Every device isolated into a network of one, brokered by the enforcement point. Track 2 reproduces this with per-device routing.

**Cleanup.** None (design).

### Exercise 2.2 — Track 2: build the flat VLAN and the enforcement point

**Objective.** Create five devices on one subnet and a host that will become the enforcement point.

**Track 2 — Walkthrough.**

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd
sudo ip link add vlan type bridge; sudo ip addr add 10.100.1.1/24 dev vlan; sudo ip link set vlan up
mkdev() { sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master vlan up; sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-e; sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via 10.100.1.1; }
mkdev web    10.100.1.10
mkdev db     10.100.1.20
mkdev hmi    10.100.1.30
mkdev plc    10.100.1.40
mkdev victim 10.100.1.50
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

Start the services on db and plc:

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

**Expected result.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.100.1.20 5432 && echo web->db OPEN'
web->db OPEN
```

All five devices are on `10.100.1.0/24` and can reach each other directly — the flat VLAN an attacker loves.

**Negative test.** These devices run no security software of their own; there is nothing to install an agent on. Any protection must come from the network layer — which is Airgap's premise.

**Cleanup.** Namespaces persist for the lab.

### Exercise 2.3 — Confirm the flat VLAN

**Objective.** Show that every device reaches every other directly at Layer 2.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.20 5432 && echo victim->db REACH'
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.40 502  && echo victim->plc REACH'
sudo ip netns exec hmi    bash -c 'nc -z -w2 10.100.1.20 5432 && echo hmi->db REACH'
```

**Expected result.** All REACH — on a flat VLAN, a compromised `victim` can reach the database, the PLC, and everything else. This is the lateral surface Chapter 04 eliminates.

**Negative test.** Even devices with no business talking (victim → plc) reach each other — the flat VLAN grants universal east-west by default, the opposite of zero trust.

**Cleanup.** Leave the devices running.

## Summary and Completion Checklist

- [ ] Track 1 Airgap ARP/DHCP-control model understood.
- [ ] Track 2: five devices on one flat VLAN plus an enforcement-point host.
- [ ] Universal east-west reachability confirmed (the flat VLAN).
- [ ] Ready to isolate every device into a network of one.
