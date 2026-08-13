# Chapter 02: Lab Preparation

## Learning Objectives

- Stand up the Track 1 estate: a Check Point Management server and a Security Gateway.
- Stand up the Track 2 estate: a Linux host modeling four segments with nftables.
- Establish trust (SIC) between management and gateway, and confirm baseline reachability.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Check Point Management + Security Gateway (15-day eval, R81.x), 4 endpoint VMs, 5 vNICs | Check Point evaluation |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

A single "standalone" deployment (management + gateway on one VM) is fine for the lab; a distributed deployment is closer to production.

## Hands-On Lab

### Exercise 2.1 — Track 1: deploy management and gateway, establish SIC

**Objective.** Get a management server and gateway running with trust between them.

**Track 1 — Walkthrough.** Deploy the Gaia images, run First Time Configuration Wizard on each (management as a Management Server, gateway as a Security Gateway), then in SmartConsole create the gateway object and establish **SIC** (Secure Internal Communication) with the one-time password set during the wizard:

```text
mgmt> (SmartConsole) New > Gateway > Wizard
      name: gw   IPv4: 10.40.0.2
      Establish SIC with one-time password: <otp>
mgmt> mgmt_cli login user admin password <pw> > sid.txt   # API session for later
```

**Expected result.** The gateway object shows **SIC status: Trust established**; `mgmt_cli` login returns a session id. Management can now push policy to the gateway.

**Negative test.** A wrong SIC one-time password leaves the gateway "SIC: not communicating" and no policy can install — trust is the prerequisite for everything that follows.

**Rollback.** Leave running.

### Exercise 2.2 — Track 1: address the gateway's segment interfaces

**Objective.** Give the gateway one interface per segment.

**Track 1 — Walkthrough.** In Gaia (or SmartConsole topology), address eth1–eth4:

```text
gw> set interface eth1 ipv4-address 10.40.1.1 mask-length 24
gw> set interface eth2 ipv4-address 10.40.2.1 mask-length 24
gw> set interface eth3 ipv4-address 10.40.3.1 mask-length 24
gw> set interface eth4 ipv4-address 10.40.4.1 mask-length 24
gw> save config
```

Set the interface topology (which interface faces which segment) on the gateway object and install the database.

**Expected result.**

```text
gw> show interfaces | grep -E "eth[1-4]"
eth1  10.40.1.1/24   eth2  10.40.2.1/24
eth3  10.40.3.1/24   eth4  10.40.4.1/24
```

**Negative test.** Until a policy is installed (next chapters), the gateway's default posture drops unmatched transit — addressing alone forwards nothing.

**Rollback.** Leave running.

### Exercise 2.3 — Track 2: build the native segment host

**Objective.** Create four endpoint namespaces on four subnets, routed by the enforcer host.

**Track 2 — Walkthrough.**

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd

mkseg() { # $1 name  $2 subnet-3rd-octet  $3 host-ip
  sudo ip netns add $1
  sudo ip link add $1-eth type veth peer name $1-br
  sudo ip addr add 10.40.$2.1/24 dev $1-br; sudo ip link set $1-br up
  sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up
  sudo ip netns exec $1 ip route add default via 10.40.$2.1; }
mkseg web 1 10.40.1.10
mkseg db  2 10.40.2.10
mkseg hmi 3 10.40.3.10
mkseg plc 4 10.40.4.10
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
```

**Expected result.**

```bash
sudo ip netns exec hmi ping -c1 10.40.2.10 | grep -o "1 received"
1 received
```

**Negative test.**

```bash
sudo ip netns exec web ping -c1 10.40.9.9 | grep -o "0 received"
0 received
```

**Rollback.** Namespaces persist for the lab.

### Exercise 2.4 — Start the workload services

**Objective.** Put a listener on db:5432 and plc:502.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

On Track 1, run PostgreSQL on the db VM and a Modbus simulator on the plc VM.

**Expected result.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.2.10 5432 && echo DB-OPEN'
DB-OPEN
```

**Negative test.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.2.10 502 || echo DB-502-CLOSED'
DB-502-CLOSED
```

**Rollback.** Leave services running.

## Summary and Completion Checklist

- [ ] Track 1: management and gateway up with SIC trust established.
- [ ] Track 1: gateway interfaces addressed per segment.
- [ ] Track 2: four segment namespaces routing through the enforcer host.
- [ ] Listeners up on db:5432 and plc:502.
