# Chapter 02: Lab Preparation

## Learning Objectives

- Stand up the Track 1 estate: a FortiGate-VM and four endpoint VMs across four segments.
- Stand up the Track 2 estate: a Linux host modeling four zones with nftables.
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | FortiGate-VM evaluation (KVM/ESXi/Workstation), 4 endpoint VMs, 5 vNICs | Fortinet support portal (VM eval) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

The FortiGate-VM evaluation runs without a purchased license in a limited mode sufficient for this lab; a 15-day trial license unlocks full throughput. Note the evaluation's crypto is limited to DES — enabling strong crypto, and with it IPsec/SSL-VPN, ZTNA, and the FortiClient EMS Security Fabric join over TLS, requires a paid license. None of those features are needed here: this lab is plaintext Layer 3/4 policy enforcement, which the unlicensed evaluation runs in full.

## Hands-On Lab

### Exercise 2.1 — Track 1: boot FortiGate-VM and address the interfaces

**Objective.** Get a FortiGate running with one interface per segment.

**Track 1 — Walkthrough.** Deploy the FortiGate-VM image with five interfaces (port1 management, port2–port5 data) and address the data interfaces:

```text
FGT # config system interface
FGT (interface) # edit port2
FGT (port2) # set ip 10.30.1.1/24
FGT (port2) # set allowaccess ping
FGT (port2) # next
FGT (interface) # edit port3
FGT (port3) # set ip 10.30.2.1/24
FGT (port3) # set allowaccess ping
FGT (port3) # next
FGT (interface) # edit port4
FGT (port4) # set ip 10.30.3.1/24
FGT (port4) # next
FGT (interface) # edit port5
FGT (port5) # set ip 10.30.4.1/24
FGT (port5) # end
```

**Expected result.**

```text
FGT # get system interface physical | grep -A1 "port[2-5]"
== [ port2 ]  ip: 10.30.1.1 255.255.255.0
== [ port3 ]  ip: 10.30.2.1 255.255.255.0
== [ port4 ]  ip: 10.30.3.1 255.255.255.0
== [ port5 ]  ip: 10.30.4.1 255.255.255.0
```

**Negative test.** With no firewall policy (next chapters), transit traffic between ports is dropped by the implicit deny — addressing the interfaces is necessary but not sufficient. The FortiGate forwards nothing until a policy permits it.

**Cleanup.** Leave running.

### Exercise 2.2 — Track 2: build the native zone host

**Objective.** Create four endpoint namespaces on four subnets, routed by the enforcer host.

**Track 2 — Walkthrough.**

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd

mkzone() { # $1 name  $2 subnet-3rd-octet  $3 host-ip
  sudo ip netns add $1
  sudo ip link add $1-eth type veth peer name $1-br
  sudo ip addr add 10.30.$2.1/24 dev $1-br; sudo ip link set $1-br up
  sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up
  sudo ip netns exec $1 ip route add default via 10.30.$2.1; }
mkzone web 1 10.30.1.10     # zone APP
mkzone db  2 10.30.2.10     # zone DB
mkzone hmi 3 10.30.3.10     # zone MGMT
mkzone plc 4 10.30.4.10     # zone OT
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

**Expected result.**

```bash
sudo ip netns exec hmi ping -c1 10.30.2.10 | grep -o "1 received"
1 received
```

**Negative test.**

```bash
sudo ip netns exec web ping -c1 10.30.9.9 | grep -o "0 received"
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
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432 && echo DB-OPEN'
DB-OPEN
```

**Negative test.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 502 || echo DB-502-CLOSED'
DB-502-CLOSED
```

**Cleanup.** Leave services running.

## Summary and Completion Checklist

- [ ] Track 1: FortiGate-VM up with four addressed data interfaces.
- [ ] Track 2: four zone namespaces routing through the enforcer host.
- [ ] Listeners up on db:5432 and plc:502.
- [ ] Baseline reachability confirmed (implicit deny still blocks transit on Track 1 until policy exists).
