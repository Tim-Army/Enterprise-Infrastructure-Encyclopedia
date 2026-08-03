# Chapter 02: Lab Preparation

## Learning Objectives

- Understand the Track 1 estate: an APIC (or ACI Simulator) driving a Nexus fabric.
- Stand up the Track 2 estate: four endpoints in four subnets routed through a host that acts as the fabric.
- Confirm baseline reachability before any contracts exist.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | APIC + Nexus 9000 fabric, or the ACI Simulator (control-plane) | Cisco (commercial; design-level here) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: APIC and the fabric (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** The **APIC** cluster is the single point of configuration for the Nexus 9000 spine-leaf fabric. You model applications as **tenants → application profiles → EPGs**, connect EPGs to **bridge domains**, and control traffic with **contracts**. The **ACI Simulator** reproduces the APIC control plane for practising configuration, though it does not forward data-plane traffic — which is why Track 2 builds the enforcement result.

**Expected result (design).** An APIC managing EPGs and contracts. Track 2 makes the whitelist enforcement concrete.

**Cleanup.** None (design).

### Exercise 2.2 — Track 2: build endpoints and the fabric host

**Objective.** Create four endpoints (one per EPG) routed through a host that enforces contracts.

**Track 2 — Walkthrough.** Each endpoint is on its own subnet (its EPG's bridge domain); the host is the fabric that routes and enforces:

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd
mkepg() { # $1 name  $2 third-octet  $3 host-ip
  sudo ip link add bd$2 type bridge 2>/dev/null; sudo ip addr add 10.110.$2.1/24 dev bd$2 2>/dev/null; sudo ip link set bd$2 up
  sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master bd$2 up; sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-e; sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via 10.110.$2.1; }
mkepg web 1 10.110.1.10     # EPG-Web
mkepg db  2 10.110.2.20     # EPG-DB
mkepg hmi 3 10.110.3.30     # EPG-Mgmt
mkepg plc 4 10.110.4.40     # EPG-OT
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

**Expected result.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.110.2.20 5432 && echo "web->db OPEN"'
web->db OPEN
```

All endpoints reach each other (routed) — the pre-contract state.

**Negative test.** Without a fabric policy, the routed network permits everything — the opposite of ACI's whitelist default, which Chapter 05 imposes.

**Cleanup.** Namespaces persist for the lab.

### Exercise 2.3 — Record the EPG membership

**Objective.** Map each endpoint to its EPG.

**Track 2 — Walkthrough.**

```bash
sudo mkdir -p /etc/aci
sudo tee /etc/aci/epgs > /dev/null <<'EOF'
10.110.1.10 EPG-Web
10.110.2.20 EPG-DB
10.110.3.30 EPG-Mgmt
10.110.4.40 EPG-OT
EOF
cat /etc/aci/epgs
```

**Expected result.** Four endpoints mapped to four EPGs — the groups contracts will apply between.

**Cleanup.** Keep the membership.

## Summary and Completion Checklist

- [ ] Track 1 APIC/fabric model understood.
- [ ] Track 2: four endpoints in four EPG subnets routed through the fabric host.
- [ ] EPG membership recorded.
- [ ] Baseline reachability confirmed (pre-contract, flat).
