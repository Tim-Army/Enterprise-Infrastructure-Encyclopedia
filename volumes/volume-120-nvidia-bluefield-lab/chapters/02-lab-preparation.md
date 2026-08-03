# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: BlueField DPUs on each server, managed via DOCA.
- Stand up the Track 2 estate: workloads whose only path to the network is a separate **DPU namespace** they cannot access.
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Servers with NVIDIA BlueField DPUs, DOCA, a management plane | NVIDIA (hardware; design-level here) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: BlueField and DOCA (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** Each server has a **BlueField DPU** on its network adapter; the DPU runs its own OS (Arm cores) via **DOCA** and enforces segmentation/firewall policy on the host's traffic before it reaches the network. Policy is deployed and managed to the DPUs out-of-band of the host OS — the host cannot see or change it.

**Expected result (design).** Per-server DPUs enforcing policy in an isolated trust domain. Track 2 reproduces the out-of-band property.

**Cleanup.** None (design).

### Exercise 2.2 — Track 2: build workloads behind DPU namespaces

**Objective.** Create a network, target servers, and two workloads each behind its own DPU namespace.

**Track 2 — Walkthrough.** The target servers (db, plc) sit on the network; each protected workload (web, hmi) reaches the network **only through its DPU namespace**, which the workload cannot access:

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd
# the "network" with the target servers
sudo ip link add net type bridge; sudo ip addr add 10.140.0.1/24 dev net; sudo ip link set net up
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
target() { sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master net up; sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-e; sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via 10.140.0.1; }
target db  10.140.0.20
target plc 10.140.0.40
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'

# a protected workload behind its own DPU namespace
mkdpu() { # $1 workload  $2 wl-subnet-octet  $3 wl-ip  $4 dpu-net-ip(last octet)
  sudo ip netns add $1; sudo ip netns add dpu-$1
  sudo ip link add $1-w type veth peer name dpu-$1-w        # workload <-> dpu (inner)
  sudo ip link set $1-w netns $1; sudo ip link set dpu-$1-w netns dpu-$1
  sudo ip link add dpu-$1-n type veth peer name dpu-$1-nb   # dpu <-> net (outer)
  sudo ip link set dpu-$1-nb master net up; sudo ip link set dpu-$1-n netns dpu-$1
  # workload side
  sudo ip netns exec $1 ip addr add $3/24 dev $1-w; sudo ip netns exec $1 ip link set $1-w up
  sudo ip netns exec $1 ip link set lo up; sudo ip netns exec $1 ip route add default via 10.140.$2.1
  # dpu side: inner + outer + forwarding
  sudo ip netns exec dpu-$1 ip addr add 10.140.$2.1/24 dev dpu-$1-w
  sudo ip netns exec dpu-$1 ip addr add 10.140.0.$4/24 dev dpu-$1-n
  sudo ip netns exec dpu-$1 ip link set dpu-$1-w up; sudo ip netns exec dpu-$1 ip link set dpu-$1-n up
  sudo ip netns exec dpu-$1 ip link set lo up
  sudo ip netns exec dpu-$1 sysctl -w net.ipv4.ip_forward=1 >/dev/null
  sudo ip netns exec dpu-$1 ip route add default via 10.140.0.1
  # the network must know how to return to the workload subnet (via its DPU)
  sudo ip route add 10.140.$2.0/24 via 10.140.0.$4; }
mkdpu web 1 10.140.1.10 11
mkdpu hmi 3 10.140.3.30 13
```

**Expected result.** Two protected workloads (`web`, `hmi`), each reaching the network only through its DPU namespace (`dpu-web`, `dpu-hmi`); the targets (`db`, `plc`) on the network:

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.20 5432 && echo web->db OPEN'
web->db OPEN
```

**Negative test.** The workload namespace (`web`) has no interface into `dpu-web` beyond the one veth; it cannot enter or configure the DPU namespace — the separation the out-of-band property depends on.

**Cleanup.** Namespaces persist for the lab.

### Exercise 2.3 — Confirm the flat state

**Objective.** Show that, with no DPU policy, workloads reach everything.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.40 502  && echo web->plc REACH (should be denied later)'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.20 5432 && echo hmi->db REACH (lateral!)'
```

**Expected result.** Both REACH — before DPU policy, the workloads reach targets they should not. Chapter 04 denies these at each DPU.

**Cleanup.** Leave running.

## Summary and Completion Checklist

- [ ] Track 1 BlueField/DOCA model understood.
- [ ] Track 2: workloads behind isolated DPU namespaces, targets on the network.
- [ ] The workload cannot access its DPU namespace.
- [ ] Baseline reachability confirmed (pre-policy).
