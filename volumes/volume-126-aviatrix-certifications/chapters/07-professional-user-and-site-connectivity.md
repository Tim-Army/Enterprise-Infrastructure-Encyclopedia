# Chapter 07: ACE Professional — Secure User and Site Connectivity

## Learning Objectives

- Cover the ACE Professional's connectivity pillar: remote user access and site-to-cloud.
- Understand Aviatrix's user VPN, Site2Cloud, and edge/backbone options.
- Model VPN connectivity and split-tunnel behavior with free primitives.

## Getting users and sites into the cloud securely

| Need | Aviatrix construct |
|:---|:---|
| Remote users → cloud apps | **User VPN** (OpenVPN-based; SAML/MFA; per-user profiles and policy) |
| Branch/data center → cloud | **Site2Cloud** (IPsec tunnels from on-prem to Aviatrix gateways) |
| Edge/on-prem into the transit backbone | **Secure Edge / Cloud Backbone** (extend the overlay to the edge) |
| Overlapping on-prem/cloud CIDRs | Aviatrix NAT on the tunnel (mapped/virtual addresses) |

The exam expects you to connect users and sites, apply per-user or per-site policy, and handle the perennial overlapping-CIDR problem.

## Hands-On Lab

WireGuard/OpenVPN and namespaces model the tunnels. **Cost:** none.

### Lab 7.1 — User VPN with split tunnel

**Objective:** Model a remote user reaching only cloud CIDRs (split tunnel), not all their traffic.

```bash
sudo apt-get install -y wireguard-tools 2>/dev/null || echo "wireguard models the user VPN tunnel"
# generate a user + gateway keypair (models per-user VPN profiles)
wg genkey | tee user.key | wg pubkey > user.pub
wg genkey | tee gw.key   | wg pubkey > gw.pub
cat <<EOF
[User VPN profile — split tunnel]
[Interface]   # the remote user
PrivateKey = $(cat user.key)
Address = 10.99.0.2/32
[Peer]        # the Aviatrix user-VPN gateway
PublicKey = $(cat gw.pub)
AllowedIPs = 10.20.0.0/16, 10.30.0.0/16   # ONLY cloud CIDRs -> split tunnel
Endpoint = gw.example:51820
EOF
```

**Expected result:** A VPN profile whose `AllowedIPs` are **only the cloud CIDRs** — split tunnel: the user's cloud-bound traffic goes through the VPN, their internet traffic doesn't. Aviatrix user VPN does this with SAML/MFA and per-user policy; the exam tests split vs full tunnel and when each is appropriate.

**Negative test:** Set `AllowedIPs = 0.0.0.0/0` (full tunnel) when only cloud access is needed — you backhaul all the user's internet traffic through the cloud (latency, egress cost); split tunnel is the default for cloud-app access.

**Cleanup:** `rm -f user.key user.pub gw.key gw.pub`.

### Lab 7.2 — Site2Cloud IPsec tunnel

**Objective:** Model a branch-to-cloud IPsec tunnel and the routes it carries.

```bash
sudo ip netns add branch; sudo ip netns add cloudgw
sudo ip link add s2c-a type veth peer name s2c-b
sudo ip link set s2c-a netns branch; sudo ip link set s2c-b netns cloudgw
sudo ip netns exec branch ip addr add 172.16.0.1/30 dev s2c-a; sudo ip netns exec branch ip link set s2c-a up
sudo ip netns exec cloudgw ip addr add 172.16.0.2/30 dev s2c-b; sudo ip netns exec cloudgw ip link set s2c-b up
sudo ip netns exec branch ip link set lo up; sudo ip netns exec cloudgw ip link set lo up
# the tunnel carries routes: branch reaches cloud CIDR, cloud reaches branch LAN
sudo ip netns exec branch ip route add 10.20.0.0/16 via 172.16.0.2
sudo ip netns exec cloudgw ip route add 192.168.10.0/24 via 172.16.0.1
sudo ip netns exec branch ip route | grep 10.20
sudo ip netns exec branch ping -c1 -W2 172.16.0.2 | grep -o "1 received"
```

**Expected result:** A point-to-point "tunnel" carrying the branch→cloud and cloud→branch routes, with connectivity confirmed — Site2Cloud: an IPsec tunnel from on-prem to an Aviatrix gateway, exchanging the routes each side needs. Production adds IKE/IPsec parameters and HA.

**Negative test:** Bring the tunnel up but forget to advertise the branch LAN route to the cloud side — cloud→branch fails though the tunnel is "up"; the exam tests that connectivity needs both the tunnel *and* the routes.

**Cleanup:** Keep for the next lab.

### Lab 7.3 — Overlapping CIDRs across the tunnel

**Objective:** Model the NAT that makes overlapping on-prem/cloud ranges work.

```bash
python3 - <<'EOF'
# Branch LAN 10.20.0.0/16 overlaps a cloud spoke 10.20.0.0/16 -> ambiguous without NAT
# Aviatrix maps the branch behind a virtual (non-overlapping) range on the tunnel
branch_real = "10.20.5.5"
virtual_map = "100.127.5.5"   # the address the cloud side actually sees
print(f"branch host {branch_real} appears to cloud as {virtual_map} (Site2Cloud NAT / mapped CIDR)")
print("cloud routes to 100.127.0.0/16 -> gateway un-NATs to the branch's real 10.20.0.0/16")
EOF
```

**Expected result:** The branch's overlapping range presented to the cloud behind a **virtual/mapped CIDR** — Aviatrix's answer to the overlapping-CIDR problem native peering can't solve. The exam expects you to reach for mapped/virtual NAT when ranges collide.

**Negative test:** Connecting two overlapping 10.20.0.0/16 networks without NAT — routing is ambiguous and breaks; the mapped CIDR is mandatory, not optional.

**Cleanup:** `for ns in branch cloudgw; do sudo ip netns del $ns 2>/dev/null; done`.

### Lab 7.4 — Edge and backbone (design)

**Objective:** Place Secure Edge / Cloud Backbone.

```text
Secure Edge / Cloud Backbone: extend the Aviatrix overlay to on-prem/edge sites so the SAME
  transit, encryption, segmentation, and CoPilot visibility reach edge-to-cloud — not just cloud-to-cloud.
  Use when: many branches, consistent policy edge-to-cloud, or replacing MPLS/SD-WAN backhaul.
```

**Expected result:** The edge/backbone role — extending the overlay past the clouds to the edge, so one model spans everything. It is the focus of the **ACE Cloud Backbone** focused course ([Chapter 08](08-professional-automation-and-operations.md) touches automation/ops).

**Negative test:** Treating edge sites as unmanaged tunnels — you lose the unified policy/visibility that is the overlay's whole point; the backbone extends the model, not just the reachability.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] User VPN split-tunnel profile modeled; split vs full tunnel understood.
- [ ] Site2Cloud tunnel and its route exchange drilled.
- [ ] Overlapping-CIDR NAT (mapped/virtual) modeled.
- [ ] Secure Edge / Cloud Backbone placement understood.
