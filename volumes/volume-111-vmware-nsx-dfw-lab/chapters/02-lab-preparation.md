# Chapter 02: Lab Preparation

## Learning Objectives

- Stand up the Track 1 estate: NSX Manager, an ESXi transport node, and four VMs on one segment.
- Stand up the Track 2 estate: four namespaces on one subnet, each ready to enforce its own ruleset.
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | NSX Manager + ESXi transport node (evaluation), vCenter, 4 VMs on one segment | VMware/Broadcom evaluation |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

Track 1 is resource-heavy (NSX Manager wants ~12 GB RAM and nested or physical ESXi). Track 2 models the *distributed* behavior on a laptop and is the recommended way to learn the concept quickly.

## Hands-On Lab

### Exercise 2.1 — Track 1: prepare NSX and the transport node

**Objective.** Get NSX enforcing on an ESXi host with four VMs on one segment.

**Track 1 — Walkthrough.** Deploy NSX Manager, register vCenter as a compute manager, prepare the ESXi host as a **transport node** (this installs the DFW kernel modules), create an overlay or VLAN segment `seg-app`, and attach the four VMs to it:

```text
nsx> (UI) System > Fabric > Hosts > prepare ESXi as transport node
nsx> (UI) Networking > Segments > add seg-app  (10.50.1.0/24)
# attach web/db/hmi/plc VMs to seg-app
```

**Expected result.** The host shows **NSX Configuration: Success** and DFW is running; all four VMs are on `seg-app`.

```text
esxi> esxcli network vswitch dvs vmware list | grep -i nsx     # NSX modules present
```

**Negative test.** A host not prepared as a transport node has no DFW — rules would exist in the manager but nothing enforces them. Preparation is what puts the firewall at the vNIC.

**Rollback.** Leave running.

### Exercise 2.2 — Track 2: build the distributed model on one subnet

**Objective.** Create four namespaces on a single subnet, each able to enforce its own nftables ruleset at its "vNIC".

**Track 2 — Walkthrough.** All four share one bridge (one L2 segment); crucially, there is **no routing host between them** — they are direct L2 peers, so any filtering must happen at each namespace itself, exactly like DFW at the vNIC:

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd
sudo ip link add seg-app type bridge; sudo ip link set seg-app up

mkvm() { # $1 name  $2 host-ip
  sudo ip netns add $1
  sudo ip link add $1-eth type veth peer name $1-br
  sudo ip link set $1-br master seg-app; sudo ip link set $1-br up
  sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up; }
mkvm web 10.50.1.10
mkvm db  10.50.1.20
mkvm hmi 10.50.1.30
mkvm plc 10.50.1.40
```

**Expected result.**

```bash
sudo ip netns exec hmi ping -c1 10.50.1.20 | grep -o "1 received"
1 received
```

All four are direct L2 peers on `10.50.1.0/24` — no gateway, so only a *distributed* control can filter them.

**Negative test.**

```bash
sudo ip netns exec web ping -c1 10.50.1.99 | grep -o "0 received"
0 received
```

**Rollback.** Namespaces persist for the lab.

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
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 5432 && echo DB-OPEN'
DB-OPEN
```

**Negative test.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 502 || echo DB-502-CLOSED'
DB-502-CLOSED
```

**Rollback.** Leave services running.

## Summary and Completion Checklist

- [ ] Track 1: ESXi prepared as a transport node; four VMs on one segment.
- [ ] Track 2: four namespaces as direct L2 peers on one subnet.
- [ ] Listeners up on db:5432 and plc:502.
- [ ] Baseline reachability confirmed (still flat — no DFW rules yet).
