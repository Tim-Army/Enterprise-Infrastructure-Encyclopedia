# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: a Xage Fabric with enforcement nodes in front of assets.
- Stand up the Track 2 estate: endpoints, an isolated OT segment, and a broker host.
- Confirm the legacy PLC is initially reachable directly — the problem to fix.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Xage Fabric Manager + enforcement nodes, protected assets | Xage (commercial; design-level here) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2`, `socat` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: the Xage Fabric estate (design)

**Objective.** Understand what the real deployment looks like.

**Track 1 — Walkthrough.** In a real Xage deployment you install the **Fabric Manager**, join one or more **enforcement nodes** to the fabric, and place a node in the path to each protected asset (inline, or as the only route to an isolated OT cell). Assets, identities, and policies are registered in the Fabric Manager; the nodes pull policy from the decentralized fabric:

```text
xage> Fabric Manager > Nodes > enroll node-ot (guards the OT cell)
xage> Assets > add plc (10.60.1.40, Modbus/502) reachable only via node-ot
xage> Assets > add db  (10.60.1.20, PostgreSQL/5432) via node-it
```

**Expected result (design).** Each asset sits behind an enforcement node; there is no unbrokered path to it. This is the shape Track 2 builds concretely.

**Rollback.** None (design).

### Exercise 2.2 — Track 2: build endpoints, an isolated OT cell, and a broker

**Objective.** Create web/db/hmi and an isolated plc reachable only through a broker.

**Track 2 — Walkthrough.** Put web/db/hmi on an IT segment and plc on an **isolated OT segment** whose only neighbor is a **broker** host that will enforce identity:

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd socat

# IT segment 10.60.1.0/24
sudo ip link add it type bridge; sudo ip addr add 10.60.1.1/24 dev it; sudo ip link set it up
# OT cell 10.60.9.0/24 (isolated)
sudo ip link add ot type bridge; sudo ip addr add 10.60.9.1/24 dev ot; sudo ip link set ot up
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null

mkns() { sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master $2; sudo ip link set $1-b up
  sudo ip link set $1-e netns $1; sudo ip netns exec $1 ip addr add $3/24 dev $1-e
  sudo ip netns exec $1 ip link set $1-e up; sudo ip netns exec $1 ip route add default via $4; }
mkns web it 10.60.1.10 10.60.1.1
mkns db  it 10.60.1.20 10.60.1.1
mkns hmi it 10.60.1.30 10.60.1.1
mkns plc ot 10.60.9.40 10.60.9.1
```

**Expected result.**

```bash
sudo ip netns list | sort | tr '\n' ' '
db hmi plc web
```

**Negative test.** The OT cell and IT segment are separate bridges; without routing/brokering the host is the only thing between them — exactly where the broker will sit.

**Rollback.** Namespaces persist for the lab.

### Exercise 2.3 — Start services and show the legacy PLC is exposed

**Objective.** Run the listeners and demonstrate the pre-Xage problem: the PLC is directly reachable.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
# with plain routing enabled, anyone in IT can hit the legacy PLC directly
sudo ip netns exec hmi bash -c 'nc -z -w2 10.60.9.40 502 && echo "hmi -> plc:502 REACH (no identity check!)"'
```

**Expected result.** `hmi -> plc:502 REACH (no identity check!)` — the legacy PLC answers anyone who can route to it. That is the brownfield-OT exposure Xage closes by removing the direct path and inserting a broker.

**Negative test.** `nc -z -w2 10.60.9.40 22` fails (no ssh) — the PLC has *no* services to authenticate with; it cannot defend itself, which is precisely why an external broker is needed.

**Rollback.** Leave services running; Chapter 05 inserts the broker.

## Summary and Completion Checklist

- [ ] Track 1 Xage Fabric shape understood (assets behind enforcement nodes).
- [ ] Track 2: IT segment, isolated OT cell, and broker host built.
- [ ] The legacy PLC shown directly reachable (the problem).
- [ ] Ready to add identities and a broker.
