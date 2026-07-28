# Chapter 08: Security, Switching, and IPv6 (MTCSE, MTCSWE, MTCIPv6E)

## Learning Objectives

- Explain the MTCSE, MTCSWE, and MTCIPv6E certificates.
- Harden RouterOS and build an IPsec tunnel (MTCSE).
- Configure VLANs and switching (MTCSWE).
- Configure IPv6 addressing and routing (MTCIPv6E).
- Complete a walkthrough for each of these specialist topics.

## Theory and Architecture

Three focused specialist certificates round out the program. **MTCSE** (Security Engineer) covers
**hardening** RouterOS (disabling unused services, securing management, strong firewalling) and
**IPsec** for encrypted site-to-site and remote-access VPNs (phase 1/phase 2, peers, policies,
proposals). **MTCSWE** (Switching Engineer) covers Layer-2: **VLANs** (802.1Q), **bridge VLAN
filtering** (RouterOS's modern VLAN-aware bridge), **spanning tree** (RSTP/MSTP), and hardware
**switch-chip** offload. **MTCIPv6E** (IPv6 Engineer) covers IPv6 **addressing** (GUA/ULA/
link-local), **SLAAC** and DHCPv6, **neighbor discovery**, and IPv6 **routing and firewalling** —
increasingly required as IPv4 exhausts. Each is a self-contained add-on to MTCNA that deepens a
specific domain.

## Design Considerations

**Harden** every router (MTCSE): least services, firewalled management, secure IPsec. Use
**VLAN-aware bridges** (MTCSWE) for modern L2 and switch-chip offload for performance. Deploy
**IPv6** (MTCIPv6E) with proper addressing (GUA + ULA), SLAAC/DHCPv6, and an **IPv6 firewall** —
don't leave IPv6 unfiltered.

## Implementation and Automation

The labs harden with IPsec, configure a VLAN-aware bridge, and set up IPv6.

## Validation and Troubleshooting

Confirm the specialist model:

```text
MTCSE: hardening (disable unused services, secure mgmt) + IPsec (phase1/phase2, peer, policy, proposal).
MTCSWE: VLANs (802.1Q), bridge VLAN filtering, RSTP/MSTP, switch-chip offload.
MTCIPv6E: IPv6 addressing (GUA/ULA/link-local), SLAAC/DHCPv6, ND, IPv6 firewall.
```

Common pitfalls: an **unfiltered IPv6** stack (firewall IPv6 too); and VLANs without **bridge VLAN
filtering** on a VLAN-aware bridge.

## Security and Best Practices

Harden management and **firewall both IPv4 and IPv6**, encrypt site links with **IPsec**, and use
**VLAN filtering** for L2 segmentation. Apply the same least-privilege discipline to IPv6 as IPv4.
Defensive administration throughout.

## Hands-On Lab

Specialist walkthroughs. **Shared prerequisites** — RouterOS nodes (CHR), in a lab. **Cost:** none.

### Lab 8.1 — Hardening and IPsec (MTCSE)

**Objective:** Secure the router and build an IPsec tunnel.

```text
# Harden: disable unused services, restrict WinBox/API.
/ip service disable telnet,ftp,www,api-ssl
/ip service set winbox address=10.0.0.0/24
# IPsec site-to-site (simplified):
/ip ipsec peer add name=siteB address=203.0.113.2/32 exchange-mode=ike2
/ip ipsec policy add src-address=192.168.88.0/24 dst-address=192.168.99.0/24 tunnel=yes peer=siteB
/ip ipsec policy print
```

**Expected result:** unused services **disabled**, management **restricted**, and an **IPsec**
policy for the site tunnel — a hardened, encrypted router.

**Negative test:** leave telnet/ftp/www and open WinBox on the WAN; **harden** — disable and
restrict them.

**Cleanup:** re-enable services as needed and remove the IPsec peer/policy (in a lab).

### Lab 8.2 — VLAN-aware bridge (MTCSWE)

**Objective:** Configure 802.1Q with bridge VLAN filtering.

```text
/interface bridge add name=br-vlan vlan-filtering=no
/interface bridge port add bridge=br-vlan interface=ether2 pvid=10
/interface bridge port add bridge=br-vlan interface=ether3 pvid=20
/interface bridge vlan add bridge=br-vlan vlan-ids=10 tagged=br-vlan untagged=ether2
/interface bridge vlan add bridge=br-vlan vlan-ids=20 tagged=br-vlan untagged=ether3
/interface bridge set br-vlan vlan-filtering=yes
/interface bridge vlan print
```

**Expected result:** a **VLAN-aware bridge** with access ports in VLAN 10 and 20 — proper 802.1Q
segmentation.

**Negative test:** rely on `pvid` alone with **vlan-filtering=no**; enable **VLAN filtering** for
real 802.1Q isolation.

**Cleanup:** `/interface bridge remove br-vlan`.

### Lab 8.3 — IPv6 addressing and firewall (MTCIPv6E)

**Objective:** Bring up IPv6 with a firewall.

```text
/ipv6 address add address=2001:db8:0:1::1/64 interface=ether2 advertise=yes
/ipv6 firewall filter add chain=input connection-state=established,related action=accept
/ipv6 firewall filter add chain=input in-interface=ether1 action=drop
/ipv6 address print
```

**Expected result:** an **IPv6 GUA** with router advertisement and an **IPv6 firewall** protecting
input — dual-stack done safely.

**Negative test:** enable IPv6 with **no firewall**; IPv6 needs filtering **too** — add IPv6 rules.

**Cleanup:** remove the IPv6 address and firewall rules.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MTCSE (security/IPsec), MTCSWE (VLANs/switching), and MTCIPv6E (IPv6) are focused add-ons to MTCNA.
Harden and encrypt (MTCSE), segment with VLAN-aware bridges (MTCSWE), and deploy IPv6 with proper
addressing and a firewall (MTCIPv6E) — filtering IPv6 as rigorously as IPv4.

- [ ] I can harden RouterOS and build an IPsec tunnel.
- [ ] I can configure a VLAN-aware bridge.
- [ ] I can bring up IPv6 with a firewall.
- [ ] I can explain each specialist certificate's focus.
- [ ] I completed Labs 8.1–8.3 including each negative test.
