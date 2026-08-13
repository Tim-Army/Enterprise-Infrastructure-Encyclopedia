# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: an AHV cluster with Prism Central and Flow Network Security enabled.
- Stand up the Track 2 estate: four namespaces on one bridge, with the host ready to enforce at the "virtual switch".
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Nutanix AHV cluster + Prism Central with Flow Network Security | Nutanix (Community Edition for study; licensed per node in production) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

Track 1 can be studied on **Nutanix Community Edition** (free, registration required) on capable hardware; in production, Flow Network Security is an **annual per-node subscription, and every node in a protected cluster must be licensed**. Track 2 models the enforcement behavior on a laptop and is the recommended way to learn the concept quickly.

## Hands-On Lab

### Exercise 2.1 — Track 1: AHV, Prism Central, and Flow (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** Deploy an AHV cluster and register it to **Prism Central**; in Prism Central, enable **Flow Network Security** (Settings → Microsegmentation). From that point, every AHV host in the managed cluster enforces the security policies Prism Central distributes — there is nothing to install in any guest:

```text
pc> Settings > Microsegmentation > Enable
pc> (four VMs on one AHV subnet: web, db, hmi, plc)
```

**Expected result (design).** Flow shows as enabled; the four VMs run on AHV with no security policy yet defined. Track 2 reproduces the enforcement point.

**Rollback.** None (design).

### Exercise 2.2 — Track 2: build the AHV model

**Objective.** Create the "virtual switch" (a bridge) and four "VMs" (namespaces) on one subnet.

**Track 2 — Walkthrough.** All four namespaces attach to one bridge, exactly like VMs on one AHV subnet; the **host** owns the bridge and will enforce policy on bridged traffic — the guests will never hold a rule:

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd
sudo ip link add ahv0 type bridge; sudo ip link set ahv0 up

mkvm() { # $1 name  $2 ip
  sudo ip netns add $1
  sudo ip link add $1-eth type veth peer name $1-br
  sudo ip link set $1-br master ahv0 up
  sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up
  sudo ip netns exec $1 ip link set lo up; }
mkvm web 10.150.0.10
mkvm db  10.150.0.20
mkvm hmi 10.150.0.30
mkvm plc 10.150.0.40
```

**Expected result.**

```bash
sudo ip netns exec web ping -c1 10.150.0.20 | grep -o "1 received"
1 received
```

**Negative test.**

```bash
sudo ip netns exec web ping -c1 10.150.0.99 | grep -o "0 received"
0 received
```

**Rollback.** Namespaces persist for the lab.

### Exercise 2.3 — Start the workload services

**Objective.** Put a listener on db:5432 and plc:502 and confirm the flat state.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

On Track 1, run PostgreSQL on the db VM and a Modbus simulator on the plc VM.

**Expected result.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.20 5432 && echo "web->db OPEN"'
web->db OPEN
```

**Negative test.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.20 502 || echo "db-502 CLOSED"'
db-502 CLOSED
```

**Rollback.** Leave services running.

## Summary and Completion Checklist

- [ ] Track 1: AHV + Prism Central with Flow enabled (design); per-node licensing noted.
- [ ] Track 2: four namespaces on the `ahv0` bridge, host ready to enforce.
- [ ] Listeners up on db:5432 and plc:502.
- [ ] Baseline reachability confirmed (still flat — no policy yet).
