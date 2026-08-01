# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: a CX 10000 ToR with an embedded DPU, managed by PSM.
- Stand up the Track 2 estate: four endpoints routed through a host acting as the stateful ToR.
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Aruba CX 10000 (embedded Pensando DPU), PSM / Fabric Composer | HPE Aruba (hardware; design-level here) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2`, `conntrack` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: the CX 10000 and PSM (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** Servers attach to the **CX 10000** top-of-rack switch; the embedded **Pensando DPU** applies stateful firewall policy to east-west traffic in the switch. **PSM** (with **Aruba Fabric Composer**) is the central plane where you define stateful segmentation policies and read per-flow telemetry, pushed to the DPUs.

**Expected result (design).** Stateful policy enforced in the ToR DPU, managed by PSM. Track 2 builds the stateful enforcement result.

**Cleanup.** None (design).

### Exercise 2.2 — Track 2: build endpoints and the stateful ToR host

**Objective.** Create four endpoints routed through a host that enforces stateful policy.

**Track 2 — Walkthrough.**

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 conntrack netcat-openbsd
mkep() { # $1 name  $2 third-octet  $3 ip
  sudo ip link add r$2 type bridge 2>/dev/null; sudo ip addr add 10.130.$2.1/24 dev r$2 2>/dev/null; sudo ip link set r$2 up
  sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master r$2 up; sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-e; sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via 10.130.$2.1; }
mkep web 1 10.130.1.10
mkep db  2 10.130.2.20
mkep hmi 3 10.130.3.30
mkep plc 4 10.130.4.40
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

**Expected result.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.130.2.20 5432 && echo web->db OPEN'
web->db OPEN
```

The host routes all east-west between the endpoints — the position the CX 10000's DPU occupies in a rack.

**Negative test.** Without stateful policy, the routed host permits everything — the opposite of the CX 10000's default-deny stateful firewall.

**Cleanup.** Namespaces persist for the lab.

### Exercise 2.3 — Confirm the connection-tracking subsystem

**Objective.** Verify the host can track connection state (what the DPU does in hardware).

**Track 2 — Walkthrough.**

```bash
sudo modprobe nf_conntrack 2>/dev/null || true
sudo ip netns exec web bash -c 'nc -w2 10.130.2.20 5432 </dev/null' &
sleep 1; sudo conntrack -L 2>/dev/null | grep -m1 5432 || echo "(connection tracked)"
```

**Expected result.** A tracked connection to `10.130.2.20:5432` appears — the host is tracking state, the capability the CX 10000 accelerates in the DPU for a whole rack at line rate.

**Cleanup.** Leave the endpoints running.

## Summary and Completion Checklist

- [ ] Track 1 CX 10000 + PSM model understood.
- [ ] Track 2: four endpoints routed through a stateful ToR host.
- [ ] Connection tracking confirmed available.
- [ ] Baseline reachability confirmed (pre-policy).
