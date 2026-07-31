# Chapter 02: Lab Preparation

## Learning Objectives

- Stand up the Track 1 estate: a vSRX firewall and four endpoint VMs across four zones.
- Stand up the Track 2 estate: a Linux host modeling four zones with nftables.
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | vSRX 3.0 evaluation (KVM/ESXi/Workstation), 4 endpoint VMs, 4 vNICs/segments | Juniper vSRX eval download |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: boot vSRX and address the interfaces

**Objective.** Get a vSRX running with one interface per zone.

**Track 1 — Walkthrough.** Deploy the vSRX image, attach four data interfaces (one per segment), and address them in Junos configuration mode:

```text
[edit]
set interfaces ge-0/0/0 unit 0 family inet address 10.20.1.1/24   # APP
set interfaces ge-0/0/1 unit 0 family inet address 10.20.2.1/24   # DB
set interfaces ge-0/0/2 unit 0 family inet address 10.20.3.1/24   # MGMT
set interfaces ge-0/0/3 unit 0 family inet address 10.20.4.1/24   # OT
commit
```

**Expected result.**

```text
srx> show interfaces terse | match ge-0/0
ge-0/0/0.0  up up inet 10.20.1.1/24
ge-0/0/1.0  up up inet 10.20.2.1/24
ge-0/0/2.0  up up inet 10.20.3.1/24
ge-0/0/3.0  up up inet 10.20.4.1/24
```

**Negative test.** Interfaces without a zone assignment (next chapter) drop all transit traffic — SRX will not forward through an interface that is not in a security zone. Addressing is necessary but not sufficient.

**Cleanup.** Leave running.

### Exercise 2.2 — Track 2: build the native zone host

**Objective.** Create four endpoint namespaces on four subnets, routed by the enforcer host that will hold the zone policy.

**Track 2 — Walkthrough.**

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd

mkzone() { # $1 name  $2 subnet-3rd-octet  $3 host-ip
  sudo ip netns add $1
  sudo ip link add $1-eth type veth peer name $1-br
  sudo ip addr add 10.20.$2.1/24 dev $1-br; sudo ip link set $1-br up
  sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up
  sudo ip netns exec $1 ip route add default via 10.20.$2.1; }
mkzone web 1 10.20.1.10     # zone APP
mkzone db  2 10.20.2.10     # zone DB
mkzone hmi 3 10.20.3.10     # zone MGMT
mkzone plc 4 10.20.4.10     # zone OT
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

**Expected result.**

```bash
sudo ip netns exec hmi ping -c1 10.20.2.10 | grep -o "1 received"
1 received
```

Each endpoint routes through the enforcer host — the flat starting network.

**Negative test.**

```bash
sudo ip netns exec web ping -c1 10.20.9.9 | grep -o "0 received"
0 received
```

**Cleanup.** Namespaces persist for the lab.

### Exercise 2.3 — Start the workload services

**Objective.** Put a listener on db:5432 and plc:502.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

On Track 1, run PostgreSQL on the db VM and a Modbus simulator on the plc VM.

**Expected result.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 5432 && echo DB-OPEN'
DB-OPEN
```

**Negative test.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 502 || echo DB-502-CLOSED'
DB-502-CLOSED
```

**Cleanup.** Leave services running.

## Summary and Completion Checklist

- [ ] Track 1: vSRX up with four addressed interfaces.
- [ ] Track 2: four zone namespaces routing through the enforcer host.
- [ ] Listeners up on db:5432 and plc:502.
- [ ] Baseline reachability confirmed (still flat — no policy yet).
