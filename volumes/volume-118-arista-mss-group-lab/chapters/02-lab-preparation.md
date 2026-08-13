# Chapter 02: Lab Preparation

**Host setup — creating these VMs on your hypervisor.** The per-hypervisor steps to create each VM (install from an ISO or boot a cloud image), size it, and map its NICs to the segments in this lab are the same for every hypervisor and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

## Learning Objectives

- Understand the Track 1 estate: an EOS fabric managed by CloudVision, with a firewall for MSS macro.
- Stand up the Track 2 estate: four endpoints in four groups routed through a fabric host, plus a firewall namespace.
- Confirm baseline reachability before any policy exists.

## What you need

| Track | Components | Source |
|:---|:---|:---|
| 1 | Arista EOS (cEOS/vEOS) fabric, CloudVision, a firewall for redirect | Arista (account/commercial; design-level here) |
| 2 | One Ubuntu 22.04 host with `nftables`, `iproute2` | free |

## Hands-On Lab

### Exercise 2.1 — Track 1: EOS, CloudVision, and the firewall (design)

**Objective.** Understand the real deployment.

**Track 1 — Walkthrough.** EOS switches form the fabric; **CloudVision** is the management and telemetry plane where **security groups** and **MSS/MSS-Group** policy are defined and pushed. For **MSS macro-segmentation**, a firewall is attached to the fabric and CloudVision programs the switches to **redirect** selected inter-group flows through it — no re-cabling of endpoints.

**Expected result (design).** Groups and group policy in CloudVision, a firewall available for redirect. Track 2 builds the enforcement result.

**Rollback.** None (design).

### Exercise 2.2 — Track 2: build endpoints, groups, and a firewall

**Objective.** Create four endpoints (one per group) and a firewall namespace, routed through the fabric host.

**Track 2 — Walkthrough.**

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd
mksg() { # $1 name  $2 third-octet  $3 host-ip
  sudo ip link add sg$2 type bridge 2>/dev/null; sudo ip addr add 10.120.$2.1/24 dev sg$2 2>/dev/null; sudo ip link set sg$2 up
  sudo ip netns add $1; sudo ip link add $1-e type veth peer name $1-b
  sudo ip link set $1-b master sg$2 up; sudo ip link set $1-e netns $1
  sudo ip netns exec $1 ip addr add $3/24 dev $1-e; sudo ip netns exec $1 ip link set $1-e up
  sudo ip netns exec $1 ip route add default via 10.120.$2.1; }
mksg web 1 10.120.1.10     # SG-Web
mksg db  2 10.120.2.20     # SG-DB
mksg hmi 3 10.120.3.30     # SG-Mgmt
mksg plc 4 10.120.4.40     # SG-OT
mksg fw  9 10.120.9.90     # inspection firewall (for MSS macro)
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
sudo ip netns exec db  bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec plc bash -c 'nohup nc -lk -p 502  >/dev/null 2>&1 &'
```

**Expected result.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.120.2.20 5432 && echo "web->db OPEN"'
web->db OPEN
```

**Negative test.** Without group policy, the routed fabric permits everything — the opposite of MSS-Group's default-deny.

**Rollback.** Namespaces persist for the lab.

### Exercise 2.3 — Record group membership

**Objective.** Map each endpoint to its security group.

**Track 2 — Walkthrough.**

```bash
sudo mkdir -p /etc/mss
sudo tee /etc/mss/groups > /dev/null <<'EOF'
10.120.1.10 SG-Web
10.120.2.20 SG-DB
10.120.3.30 SG-Mgmt
10.120.4.40 SG-OT
EOF
cat /etc/mss/groups
```

**Expected result.** Four endpoints mapped to four security groups.

**Rollback.** Keep the membership.

## Summary and Completion Checklist

- [ ] Track 1 EOS/CloudVision + firewall model understood.
- [ ] Track 2: four group subnets + a firewall namespace routed through the fabric host.
- [ ] Group membership recorded.
- [ ] Baseline reachability confirmed (pre-policy).
