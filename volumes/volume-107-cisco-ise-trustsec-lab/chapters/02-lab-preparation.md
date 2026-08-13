# Chapter 02: Lab Preparation

## Learning Objectives

- Stand up the Track 1 estate: an ISE evaluation VM and an IOS-XE enforcement device.
- Stand up the Track 2 estate: a Linux enforcement host and four endpoint namespaces.
- Confirm baseline reachability before any tagging exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Cisco ISE 3.x OVA (90-day eval), IOS-XE device (Catalyst 9000v in CML, or physical Cat9300/CSR/Cat9k), 4 endpoint VMs | software.cisco.com (eval), Cisco Modeling Labs |
| 2 | One Linux host (Ubuntu 22.04) with `nftables`, `iproute2` | free |

Track 2 needs no Cisco account and runs entirely on one laptop.

## Hands-On Lab

### Exercise 2.1 — Track 1: import and boot Cisco ISE

**Objective.** Get the ISE policy node running and reachable.

**Track 1 — Walkthrough.** Import the ISE OVA into your hypervisor (ESXi/Workstation/CML), allocate at least 4 vCPU and 16 GB RAM (eval minimum), and run the setup dialog on first boot:

```text
ise/admin> (first-boot setup)
  hostname: ise
  ip address: 10.10.0.10  /24
  gateway: 10.10.0.1
  dns / ntp: <your values>
  admin password: <set>
```

After services start (30–45 min), confirm the application is up:

```bash
show application status ise
# ... Application Server   running
# ... Profiler Database    running
```

**Expected result.** `show application status ise` lists the Application Server as `running`; the admin UI answers at `https://10.10.0.10`.

**Negative test.** Browsing to the UI before services finish shows a "still initializing" page — ISE is slow to start; wait for the Application Server to report `running`, not just the OS login.

**Rollback.** Leave ISE running; it is the policy engine for the whole lab.

### Exercise 2.2 — Track 1: bring up the IOS-XE enforcer

**Objective.** Boot an IOS-XE device that will download and enforce SGACLs.

**Track 1 — Walkthrough.** In CML, add a Catalyst 9000v (or CSR1000v/Cat8000v) node, connect it to the ISE management network and to the four endpoints, and give it a management IP:

```text
nad# configure terminal
nad(config)# hostname nad
nad(config)# interface GigabitEthernet1
nad(config-if)#  ip address 10.10.0.2 255.255.255.0
nad(config-if)#  no shutdown
nad(config)# aaa new-model
nad(config)# ip routing
```

**Expected result.**

```bash
ping 10.10.0.10
# !!!!!  Success rate is 100 percent
```

The enforcer can reach ISE (required for RADIUS and SGACL download).

**Negative test.** With `aaa new-model` absent, later `cts` and RADIUS commands are rejected — TrustSec rides on the AAA subsystem, so enable it first.

**Rollback.** Leave running.

### Exercise 2.3 — Track 2: build the native enforcement host

**Objective.** Create a Linux host that will model SXP bindings and the SGACL matrix, plus four endpoint namespaces.

**Track 2 — Walkthrough.** On one Ubuntu host, create four network namespaces as the endpoints and a bridge as the "fabric," with the host acting as the router/enforcer:

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd

# fabric bridge + host-side enforcer address
sudo ip link add fabric type bridge
sudo ip addr add 10.10.1.1/24 dev fabric
sudo ip link set fabric up

# helper: make an endpoint ns with an address on the fabric
mkns() { sudo ip netns add $1
  sudo ip link add $1-eth type veth peer name $1-br
  sudo ip link set $1-br master fabric; sudo ip link set $1-br up
  sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up
  sudo ip netns exec $1 ip route add default via 10.10.1.1; }
mkns web 10.10.1.10
mkns db  10.10.1.20
mkns hmi 10.10.1.30
mkns plc 10.10.1.40
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

**Expected result.**

```bash
sudo ip netns list
# plc
# hmi
# db
# web
sudo ip netns exec hmi ping -c1 10.10.1.20 | grep -o "1 received"
1 received
```

All four endpoints exist and route through the enforcer host.

**Negative test.**

```bash
sudo ip netns exec web ping -c1 10.10.1.99 | grep -o "0 received"
0 received
```

A non-existent endpoint is unreachable — the fabric only carries what you created.

**Rollback.** Namespaces persist for the lab. Teardown is Chapter 09.

### Exercise 2.4 — Start the workload services

**Objective.** Put a listening service on each endpoint so reachability tests mean something.

**Track 1 & 2 — Walkthrough.** Run a PostgreSQL-like listener on `db:5432` and a Modbus-like listener on `plc:502`. On Track 2:

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

On Track 1, install PostgreSQL on the db VM and a Modbus simulator on the plc VM as in the other volumes.

**Expected result.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 5432 && echo DB-OPEN'
DB-OPEN
```

**Negative test.** Nothing listens on `db:502`:

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 502 || echo DB-502-CLOSED'
DB-502-CLOSED
```

**Rollback.** Leave services running.

## Summary and Completion Checklist

- [ ] Track 1: ISE running, IOS-XE enforcer reaching ISE.
- [ ] Track 2: four endpoint namespaces routing through the enforcer host.
- [ ] Workload listeners up on db:5432 and plc:502.
- [ ] Baseline reachability confirmed (still flat — no tags yet).
