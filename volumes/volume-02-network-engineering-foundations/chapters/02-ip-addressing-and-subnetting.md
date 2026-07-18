# Chapter 2: IP Addressing and Subnetting

## Learning Objectives

- Decompose an IPv4 address into network and host portions using a subnet
  mask or CIDR prefix, and compute subnet boundaries by hand.
- Apply Variable Length Subnet Masking (VLSM) to allocate address space
  efficiently across links and sites of differing host counts.
- Summarize (aggregate) a block of contiguous subnets into the smallest
  correct supernet route.
- Explain the structure and scope of IPv6 addressing, including global
  unicast, link-local, unique local, and multicast address types.
- Distinguish public, private (RFC 1918), and shared/carrier-grade address
  space, and explain when NAT is and is not required.
- Design an IP addressing plan for a multi-site enterprise that supports
  route summarization and future growth.
- Verify address configuration and reachability using standard host and
  device commands.

## Theory and Architecture

### IPv4 Address Structure

An IPv4 address is a 32-bit value, conventionally written in dotted-decimal
notation as four octets (for example, `10.20.30.40`). Every address is
divided into a network portion and a host portion; the boundary between them
is defined by a subnet mask or, equivalently, a CIDR prefix length. A `/24`
prefix (mask `255.255.255.0`) dedicates the first 24 bits to the network and
the remaining 8 bits to host addressing, yielding 256 total addresses per
subnet, 254 of which are usable after subtracting the network address (all
host bits zero) and the broadcast address (all host bits one).

```text
10.20.30.40 /24
Binary:  00001010.00010100.00011110.00101000
Mask:    11111111.11111111.11111111.00000000
Network: 10.20.30.0
Broadcast: 10.20.30.255
Usable range: 10.20.30.1 - 10.20.30.254
```

### CIDR and Prefix Notation

Classless Inter-Domain Routing (CIDR), defined in RFC 4632, replaced the
rigid Class A/B/C boundaries of early IPv4 with arbitrary prefix lengths
(`/1` through `/31` for point-to-point or host routes, `/32` for a single
host route). CIDR is what makes route summarization and efficient address
allocation possible; a `/22` block, for example, covers four contiguous
`/24`s and can be advertised as a single route.

| Prefix | Mask | Usable Hosts | Common Use |
| --- | --- | --- | --- |
| /30 | 255.255.255.252 | 2 | Point-to-point WAN/router links |
| /29 | 255.255.255.248 | 6 | Small service subnets |
| /27 | 255.255.255.224 | 30 | Small branch LAN |
| /24 | 255.255.255.0 | 254 | Standard access-layer VLAN |
| /23 | 255.255.254.0 | 510 | Larger access-layer VLAN |
| /16 | 255.255.0.0 | 65,534 | Regional or campus aggregate block |

### Variable Length Subnet Masking (VLSM)

VLSM allocates subnet sizes that match actual host requirements instead of
using one fixed mask everywhere, avoiding the waste of assigning a `/24`
(254 usable hosts) to a WAN link that needs exactly two addresses. The
standard VLSM workflow is to sort requirements from largest to smallest,
allocate the largest blocks first from a contiguous parent block, and
subdivide remaining space for smaller requirements — this keeps the
allocation summarizable.

**Worked example.** Given `10.1.0.0/22` (1,024 addresses) to serve one site
with a 400-host user VLAN, a 100-host voice VLAN, a 50-host server VLAN, and
three point-to-point WAN links:

| Requirement | Hosts Needed | Assigned Block | Usable Range |
| --- | --- | --- | --- |
| User VLAN | 400 | 10.1.0.0/23 | 10.1.0.1–10.1.1.254 |
| Voice VLAN | 100 | 10.1.2.0/25 | 10.1.2.1–10.1.2.126 |
| Server VLAN | 50 | 10.1.2.128/26 | 10.1.2.129–10.1.2.190 |
| WAN link 1 | 2 | 10.1.2.192/30 | 10.1.2.193–10.1.2.194 |
| WAN link 2 | 2 | 10.1.2.196/30 | 10.1.2.197–10.1.2.198 |
| WAN link 3 | 2 | 10.1.2.200/30 | 10.1.2.201–10.1.2.202 |

The entire allocation still fits inside and summarizes to `10.1.0.0/22`,
which is what a distribution or core router advertises upstream instead of
six individual routes.

### Route Summarization

Summarization (aggregation) reduces routing table size and limits the blast
radius of instability by advertising one covering prefix instead of many
specific ones. Correct summarization requires contiguous address blocks
allocated on power-of-two boundaries — this is why a deliberate,
hierarchical addressing plan (regional block → site block → VLAN block)
matters more than it might appear during initial design; retrofitting
summarization onto ad hoc allocations later is disruptive.

### IPv6 Address Structure

IPv6 addresses are 128 bits, written as eight groups of four hexadecimal
digits separated by colons, with two shorthand rules: leading zeros in a
group may be omitted, and one contiguous run of all-zero groups may be
collapsed to `::` (only once per address).

```text
Full:        2001:0db8:0000:0001:0000:0000:0000:0100
Compressed:  2001:db8:0:1::100
```

| Address Type | Prefix / Marker | Scope | Purpose |
| --- | --- | --- | --- |
| Global Unicast Address (GUA) | `2000::/3` | Global | Internet-routable, RFC 4291/RFC 3587 |
| Unique Local Address (ULA) | `fc00::/7` (used: `fd00::/8`) | Site-local | RFC 1918-equivalent private addressing |
| Link-Local Address (LLA) | `fe80::/10` | Single link | Auto-assigned, required on every interface |
| Multicast | `ff00::/8` | Varies by scope | Replaces IPv4 broadcast entirely |
| Loopback | `::1/128` | Host | Equivalent to `127.0.0.1` |

A standard enterprise IPv6 subnet uses a `/64` prefix regardless of expected
host count; this is a deliberate design constant (not a VLSM decision) so
that Stateless Address Autoconfiguration (SLAAC) and the 64-bit interface
identifier space work as specified in RFC 4862. Enterprises typically
receive a `/48` or `/56` from their upstream provider or RIR and subnet on
the boundary between `/48`/`/56` and `/64` — nibble-aligned on hex digit
boundaries for readability.

### Public, Private, and Shared Address Space

RFC 1918 reserves three IPv4 ranges for private use, none of which are
globally routable:

| Range | Prefix | Typical Use |
| --- | --- | --- |
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | Large enterprise internal addressing |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | Medium networks, common in lab/vendor defaults |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | Small office/branch/home |

RFC 6598 additionally reserves `100.64.0.0/10` as Shared Address Space for
carrier-grade NAT (CGNAT), which enterprises must recognize as neither
private nor safely assumed unique — overlapping use across an ISP's CGNAT
customers is expected behavior, which affects VPN and merger/acquisition
address-conflict planning. Address translation (NAT/PAT, covered in Chapter
5) bridges private space to public, routable space at a network's edge.

## Design Considerations

- **Plan hierarchically before assigning a single address.** A regional
  block subdivided into site blocks subdivided into function-based VLAN
  blocks is what makes summarization, ACL design, and troubleshooting scale;
  addressing "as you go" produces fragmentation that cannot be summarized
  later without renumbering.
- **Size for the actual growth horizon, not just current headcount.**
  Allocating a `/23` instead of a `/24` for a user VLAN expected to double in
  three years avoids a disruptive future re-IP; over-allocating everything
  to `/16` wastes address space and enlarges broadcast domains unnecessarily
  (see Chapter 3).
- **Reserve address ranges by function within each subnet** (for example,
  `.1–.9` for gateways/HSRP/VRRP virtual IPs, `.10–.19` for infrastructure,
  `.20–.199` for DHCP scope, `.200–.254` for static assignments) so that
  operational staff can infer a device's role from its address.
- **Decide the IPv6 strategy deliberately, not as an afterthought.**
  Dual-stack (IPv4 and IPv6 concurrently) is the common enterprise approach
  during transition; determine at design time whether IPv6-only segments are
  in scope, since this affects DHCPv6/SLAAC choice and DNS AAAA record
  planning.
- **NAT is a translation mechanism, not a security boundary.** Design
  network segmentation and firewall policy independently of whether NAT is
  present; do not rely on private addressing alone to prevent unwanted
  reachability.

## Implementation and Automation

### Manual Subnetting Workflow

Given a requirement for 500 usable hosts, find the smallest prefix that
covers it: usable hosts = 2^(32-prefix) - 2, so 2^9 - 2 = 510 satisfies 500
usable hosts, meaning a `/23` is required (9 host bits). This calculation is
the daily building block of every VLSM plan.

### Verifying Configuration on End Hosts

```bash
# Linux: show configured addresses and prefix lengths
ip -brief address show

# Linux: show the active default route
ip route show default

# Windows: show interface IP configuration
ipconfig /all
```

### Configuring an Interface (Vendor-Neutral Pseudo-CLI)

```text
device(config)# interface vlan 20
device(config-if)# ip address 10.1.2.129 255.255.255.192
device(config-if)# ipv6 address 2001:db8:0:20::1/64
device(config-if)# no shutdown
```

### Automating Subnet Planning

Manual VLSM arithmetic does not scale past a handful of sites. Python's
`ipaddress` standard library module (no external dependency) both validates
and subdivides address plans programmatically:

```python
import ipaddress

site_block = ipaddress.ip_network("10.1.0.0/22")

# Split into /24 subnets for a multi-VLAN site
subnets = list(site_block.subnets(new_prefix=24))
for subnet in subnets:
    print(subnet, "usable hosts:", subnet.num_addresses - 2)

# Confirm summarization: does this list of routes collapse to one supernet?
routes = [ipaddress.ip_network(n) for n in
          ["10.1.0.0/24", "10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]]
print(list(ipaddress.collapse_addresses(routes)))
```

```bash
# Command-line equivalent for a quick subnet check
python3 -c "import ipaddress; n = ipaddress.ip_network('10.1.2.128/26'); \
print(f'{n.network_address} - {n.broadcast_address}, {n.num_addresses - 2} usable')"
```

Infrastructure-as-code IP address management (IPAM) tools such as
NetBox or phpIPAM store the allocation plan as source of truth and expose an
API that automation (DHCP scope creation, DNS record generation, firewall
object creation) can consume, keeping the addressing plan and its
downstream configuration consistent as the network changes.

## Validation and Troubleshooting

```bash
# Confirm the host has the expected address and prefix
ip -4 -brief address show eth0
ip -6 -brief address show eth0

# Confirm the default gateway is reachable at Layer 3
ping -c 4 10.1.2.190

# Confirm the subnet mask two hosts believe they share actually matches
# (a mismatched mask on either side is a common silent misconfiguration)
```

| Symptom | Likely Cause | Diagnostic |
| --- | --- | --- |
| Host cannot reach anything, including its own gateway | Wrong subnet mask/prefix places gateway outside the host's calculated subnet | Compare host address+mask against gateway address by hand |
| Two hosts on the "same" VLAN cannot reach each other | Mismatched subnet mask — one host calculates a smaller subnet than the other | `ip addr show` on both hosts, compare prefix length |
| Overlapping subnet error when adding a new site | Address plan was not centrally tracked (no IPAM) | Check IPAM/spreadsheet of record before allocating |
| Route summarization advertises addresses that do not exist | Subnets allocated outside the intended summarizable block | Recompute the covering prefix with `ipaddress.collapse_addresses` |
| SLAAC-assigned IPv6 host cannot reach off-link destinations | Router not advertising a default route in Router Advertisements | `show ipv6 interface`, check RA configuration |

A frequent real-world fault is a subnet mask mismatch between two devices
intended to be on the same segment: if one host is configured with a `/25`
and the peer with a `/24` using an address that falls outside the first
host's calculated range, the first host will send an ARP request for a
next-hop it treats as off-link, producing an apparent "can't reach my
neighbor" symptom that looks like a Layer 2 problem but is actually a Layer
3 addressing error — always confirm the mask before escalating to a
cabling or switchport investigation.

## Security and Best Practices

- Do not assume RFC 1918 space is inherently trusted; internal segmentation,
  ACLs, and firewall policy must still enforce least privilege between
  subnets regardless of address family.
- Avoid overlapping RFC 1918 ranges across sites that may eventually merge,
  peer, or connect via VPN/M&A activity; a deliberate, centrally tracked
  addressing plan prevents costly renumbering later.
- Filter or rate-limit unnecessary broadcast/multicast traffic at Layer 3
  boundaries; oversized subnets amplify the blast radius of broadcast-based
  issues and attacks (see Chapter 3 for Layer 2 containment).
- For IPv6, explicitly evaluate SLAAC vs. DHCPv6 vs. DHCPv6 with
  Prefix Delegation for address assignment; unmanaged SLAAC can allow
  unexpected host addressing if Router Advertisement Guard and DHCPv6 Guard
  are not enabled on access switches (covered further in Chapter 3).
- Document and enforce address reservation conventions (gateway addresses,
  infrastructure ranges, DHCP scopes) in the IPAM system of record so
  automation and humans do not collide on the same address.

## References and Knowledge Checks

**References**

- [RFC 791 — Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [RFC 4632 — Classless Inter-Domain Routing (CIDR)](https://www.rfc-editor.org/rfc/rfc4632)
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918)
- [RFC 6598 — IANA-Reserved IPv4 Prefix for Shared Address Space](https://www.rfc-editor.org/rfc/rfc6598)
- [RFC 4291 — IP Version 6 Addressing Architecture](https://www.rfc-editor.org/rfc/rfc4291)
- [RFC 4862 — IPv6 Stateless Address Autoconfiguration](https://www.rfc-editor.org/rfc/rfc4862)

**Knowledge Checks**

1. Given a requirement for 90 usable hosts, what is the smallest CIDR prefix
   that satisfies it, and what is the resulting usable host count?
2. Why must VLSM allocations be planned largest-block-first to remain
   summarizable?
3. A site is allocated `10.5.4.0/22`. What is the single covering summary
   route, and which four `/24`s does it contain?
4. Explain why a `/64` is the standard IPv6 subnet size even for a
   point-to-point link with only two hosts.
5. What is the practical difference between RFC 1918 private space and RFC
   6598 shared (CGNAT) space from an enterprise addressing-conflict
   perspective?
6. Two hosts on the same physical segment are configured with different
   subnet masks. Describe the symptom this produces and how to diagnose it.

## Hands-On Lab

**Objective.** Design, allocate, implement, and validate a VLSM addressing
plan for a simulated three-VLAN site using Linux network namespaces, and
confirm the plan summarizes correctly.

**Prerequisites**

- A Linux host with `sudo` access and the `iproute2` package (`ip` command).
- `python3` with the standard library (no external packages required for
  this lab).

**Lab Steps**

1. Design the addressing plan on paper first: from `10.50.0.0/24`, allocate
   a `/26` for a "Users" segment, a `/27` for a "Servers" segment, and a
   `/30` for a simulated point-to-point link, using the VLSM method from
   this chapter (largest block first).

2. Validate the plan programmatically before implementing it:

   ```bash
   python3 - <<'PYEOF'
   import ipaddress

   parent = ipaddress.ip_network("10.50.0.0/24")
   users = ipaddress.ip_network("10.50.0.0/26")
   servers = ipaddress.ip_network("10.50.0.64/27")
   p2p = ipaddress.ip_network("10.50.0.96/30")

   for name, net in [("users", users), ("servers", servers), ("p2p", p2p)]:
       assert net.subnet_of(parent), f"{name} is not inside {parent}"
       print(f"{name}: {net} usable={net.num_addresses - 2}")
   PYEOF
   ```

   **Expected result:** three lines print with no `AssertionError`,
   confirming each block is a valid subset of the `/24` parent.

3. Build two network namespaces connected by a veth pair to represent the
   "Users" and "Servers" segments joined through a simulated router
   namespace:

   ```bash
   sudo ip netns add ns-users
   sudo ip netns add ns-servers
   sudo ip netns add ns-router

   sudo ip link add veth-u type veth peer name veth-ur
   sudo ip link add veth-s type veth peer name veth-sr
   sudo ip link set veth-u netns ns-users
   sudo ip link set veth-ur netns ns-router
   sudo ip link set veth-s netns ns-servers
   sudo ip link set veth-sr netns ns-router
   ```

4. Address each interface according to the validated plan (using the first
   usable address in each block as the gateway):

   ```bash
   sudo ip netns exec ns-users ip addr add 10.50.0.2/26 dev veth-u
   sudo ip netns exec ns-users ip link set veth-u up
   sudo ip netns exec ns-users ip link set lo up

   sudo ip netns exec ns-servers ip addr add 10.50.0.65/27 dev veth-s
   sudo ip netns exec ns-servers ip link set veth-s up
   sudo ip netns exec ns-servers ip link set lo up

   sudo ip netns exec ns-router ip addr add 10.50.0.1/26 dev veth-ur
   sudo ip netns exec ns-router ip addr add 10.50.0.66/27 dev veth-sr
   sudo ip netns exec ns-router ip link set veth-ur up
   sudo ip netns exec ns-router ip link set veth-sr up
   sudo ip netns exec ns-router sysctl -w net.ipv4.ip_forward=1
   ```

5. Add default routes on the endpoint namespaces pointing at the router
   namespace, then validate end-to-end reachability across the two
   VLSM-derived subnets:

   ```bash
   sudo ip netns exec ns-users ip route add default via 10.50.0.1
   sudo ip netns exec ns-servers ip route add default via 10.50.0.66

   sudo ip netns exec ns-users ping -c 3 10.50.0.65
   ```

   **Expected result:** 3 packets transmitted, 3 received, 0% packet loss —
   confirming that the "Users" `/26` and "Servers" `/27` segments, though
   different sizes, correctly route through the shared router namespace.

**Negative Test**

Add a fourth namespace addressed from an overlapping range that was not
validated in step 2 (for example, `10.50.0.30/26` on a new namespace,
which collides with the already-allocated "Users" block):

```bash
sudo ip netns add ns-conflict
sudo ip link add veth-c type veth peer name veth-cr
sudo ip link set veth-c netns ns-conflict
sudo ip link set veth-cr netns ns-router
sudo ip netns exec ns-conflict ip addr add 10.50.0.30/26 dev veth-c
sudo ip netns exec ns-conflict ip link set veth-c up
sudo ip netns exec ns-router ip addr add 10.50.0.30/26 dev veth-cr
```

**Expected result:** the second `ip addr add` on `ns-router` fails with
`RTNETLINK answers: File exists`, because `10.50.0.30/26` overlaps an
address already assigned to `veth-ur` in the same namespace — this
reproduces, in miniature, the overlapping-allocation failure that an
un-tracked IPAM process produces at enterprise scale.

**Cleanup**

```bash
sudo ip netns del ns-users
sudo ip netns del ns-servers
sudo ip netns del ns-router
sudo ip netns del ns-conflict 2>/dev/null || true
```

## Summary and Completion Checklist

This chapter covered IPv4 and IPv6 address structure, CIDR notation, VLSM
allocation, and route summarization — the arithmetic and planning
discipline that underlies every routing and switching decision later in
this volume. The hands-on lab translated a paper VLSM plan into a working,
validated topology and demonstrated what an overlapping allocation looks
like when it collides in practice.

**Completion Checklist**

- [ ] Can calculate the smallest CIDR prefix that satisfies a given
      usable-host requirement.
- [ ] Can perform a largest-block-first VLSM allocation from a parent
      block and verify it summarizes correctly.
- [ ] Can describe IPv6 GUA, ULA, link-local, and multicast address scopes.
- [ ] Understands why `/64` is the standard IPv6 subnet size.
- [ ] Implemented and validated a VLSM plan across simulated network
      namespaces, including a reproduced overlapping-allocation failure.
- [ ] Can explain why RFC 1918 addressing is not itself a security
      boundary.
