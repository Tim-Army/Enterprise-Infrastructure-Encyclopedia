# Chapter 5: Core Network Services

![Lab topology for this chapter: ns-router runs dnsmasq, offering a single-address DHCP scope (10.90.0.100) with gateway and DNS server both set to 10.90.0.1 and a static record app.lab.internal -> 10.90.0.1; ns-client leases 10.90.0.100/24 by DHCP and resolves app.lab.internal via DNS; ns-router also MASQUERADEs 10.90.0.0/24 traffic out its 203.0.113.1/30 interface toward ns-wan (203.0.113.2/30), which never sees a route back to 10.90.0.0/24. As a negative test, a second client cannot obtain a lease from the exhausted single-address DHCP scope.](../../../diagrams/volume-002-network-engineering-foundations/chapter-05-dhcp-dns-pat-topology.svg)

*Figure 5-1. Topology used throughout this chapter's Hands-On Lab: one router namespace providing DHCP, DNS, and PAT for a client namespace, with a simulated internet host on the far side of the translation.*

## Learning Objectives

- Explain how DNS resolves names to addresses, including the difference
  between recursive and authoritative resolution and the role of caching
  and TTLs.
- Explain the DHCP four-message exchange (DORA), DHCP relay, and DHCPv6/SLAAC
  interaction introduced conceptually in [Chapter 2](02-ip-addressing-and-subnetting.md).
- Explain NTP's stratum hierarchy and why accurate time is a prerequisite
  for security, logging, and troubleshooting across the rest of this volume.
- Distinguish NAT and PAT, explain why NAT is a translation mechanism rather
  than a security control (as stated in [Chapter 2](02-ip-addressing-and-subnetting.md)), and identify when it is
  and is not required.
- Configure and validate DNS, DHCP, NTP, and NAT/PAT services using
  vendor-neutral tooling.
- Diagnose common failures in each service using layered troubleshooting
  reasoning established in [Chapter 1](01-network-models-and-protocol-architecture.md).
- Apply security hardening appropriate to each core service.

## Theory and Architecture

Every enterprise network depends on a small set of infrastructure services
that most users never interact with directly but that every application
depends on implicitly. If IP addressing ([Chapter 2](02-ip-addressing-and-subnetting.md)) and routing ([Chapter 4](04-ip-routing-fundamentals.md))
answer "how do packets get from A to B," the services in this chapter answer
"how does a host learn what B is called, what address it should use, what
time it is, and how it reaches a destination that does not share its address
space." A failure in any one of these services produces symptoms that look
like an application or network fault but are actually a core-services fault
— which is why they are grouped together here rather than treated as
peripheral topics.

### DNS: Namespace, Resolution, and Records

The Domain Name System (DNS), defined in [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035), maps hierarchical,
human-readable names to IP addresses (and other resource data) through a
distributed, delegated namespace. No single server holds the entire
namespace; instead, authority is delegated downward from the root zone
(`.`) to top-level domains (`.com`, `.internal`, etc.) to the
organization's own authoritative zone.

| Record Type | Purpose | Example |
| --- | --- | --- |
| A | Maps a name to an IPv4 address | `app01.example.internal. IN A 10.10.5.20` |
| AAAA | Maps a name to an IPv6 address | `app01.example.internal. IN AAAA 2001:db8:5::20` |
| CNAME | Aliases one name to another canonical name | `www IN CNAME app01.example.internal.` |
| PTR | Maps an address to a name (reverse lookup) | `20.5.10.10.in-addr.arpa. IN PTR app01.example.internal.` |
| MX | Identifies mail exchange targets and preference | `example.internal. IN MX 10 mail01.example.internal.` |
| SRV | Locates a service by protocol/port | `_ldap._tcp IN SRV 0 0 389 dc01.example.internal.` |
| NS | Delegates a zone to authoritative name servers | `example.internal. IN NS ns1.example.internal.` |
| SOA | Zone metadata: primary server, serial, refresh/retry/expire/TTL | one per zone |
| TXT | Free-form text, commonly used for SPF/DKIM/verification | `example.internal. IN TXT "v=spf1 -all"` |

**Recursive vs. authoritative resolution.** A client (stub resolver) sends a
query to a recursive resolver, which does the work of walking the namespace
on the client's behalf: querying a root server for the top-level domain's
name servers, querying that top-level domain for the organization's
authoritative name servers, and finally querying an authoritative server for
the actual record. The client only ever talks to the recursive resolver and
receives a single answer; the iterative walk between root, TLD, and
authoritative servers happens entirely on the resolver side.

```text
Client --(recursive query: "what is app01.example.internal?")--> Recursive Resolver
Recursive Resolver --(iterative query)--> Root server        --> referral to .internal TLD (or private root hint)
Recursive Resolver --(iterative query)--> example.internal NS --> referral to authoritative server
Recursive Resolver --(iterative query)--> Authoritative server for example.internal --> answer: 10.10.5.20
Recursive Resolver --(final answer, cached for the record's TTL)--> Client
```

**Caching and TTL.** Every DNS record carries a Time-To-Live in seconds. A
recursive resolver caches the answer for that duration, serving repeat
queries locally without re-walking the namespace. Short TTLs (60–300
seconds) support rapid failover and change agility at the cost of query
volume; long TTLs (3600+ seconds) reduce query load and external dependency
but slow propagation of intentional changes. Enterprises typically run
internal recursive resolvers (rather than pointing every host at a public
resolver) both for performance (cache locality) and to serve an internal,
non-publicly-resolvable zone for private resource names.

**Split-horizon (split-brain) DNS** serves different answers for the same
name depending on whether the query originates from inside or outside the
enterprise network — for example, an internal query for `app.example.com`
returns a private [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) address, while an external query returns a
public, NAT'd or load-balanced address. This is implemented as two separate
zones (internal-view and external-view) served by different resolver
infrastructure, not as a single zone with conditional records.

### DHCP: Automatic Address Assignment

Dynamic Host Configuration Protocol (DHCP), defined in [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131), automates
IPv4 address assignment along with related configuration (default gateway,
DNS servers, domain name, NTP servers, and vendor-specific options) so hosts
do not require manual addressing. The exchange is a four-message process
commonly abbreviated **DORA**:

```text
Client                                          DHCP Server
  |--- DHCPDISCOVER (broadcast: "any server?") ---------->|
  |<-- DHCPOFFER (server proposes an address) ------------|
  |--- DHCPREQUEST (broadcast: "I accept this offer") --->|
  |<-- DHCPACK (server confirms, lease begins) ------------|
```

The client broadcasts because it has no IP address yet and does not know
which server(s) exist; broadcasting `DHCPREQUEST` (rather than unicasting to
the offering server) also implicitly informs any other server that made a
competing offer that its offer was not accepted, so it can release the
reserved address.

**DHCP relay.** Because `DHCPDISCOVER` is a Layer 2 broadcast, it does not
cross a router boundary by default. A DHCP relay agent (typically configured
on the VLAN's default-gateway router or Layer 3 switch) listens for DHCP
broadcasts on the local segment and unicasts them to a centrally located
DHCP server, inserting the relay's own address in the packet's `giaddr`
field so the server knows which subnet's scope to assign from and can route
the reply back correctly. This is what allows one or two central DHCP
servers to serve an entire multi-site enterprise instead of requiring a
DHCP server on every subnet.

| Element | Purpose |
| --- | --- |
| Scope | The contiguous address range a DHCP server can assign from for a given subnet |
| Lease time | How long a client may use an assigned address before renewal is required |
| Exclusion range | Addresses within a scope reserved for static assignment (see [Chapter 2](02-ip-addressing-and-subnetting.md)'s addressing-by-function convention) |
| Reservation | A specific address bound to a specific MAC/client identifier, still delivered via DHCP |
| Option | Additional configuration delivered with the lease (Option 3 = router, Option 6 = DNS servers, Option 42 = NTP servers, Option 66/67 = PXE boot server/filename) |

**DHCPv6 and SLAAC.** [Chapter 2](02-ip-addressing-and-subnetting.md) introduced IPv6's Stateless Address
Autoconfiguration (SLAAC), in which a host derives its own address from a
Router Advertisement's prefix and generates its interface identifier
locally — no server assigns the address. DHCPv6 can operate in stateful mode
(assigning the full address, analogous to DHCPv4) or stateless mode
(supplying only DNS servers and other options while SLAAC handles
addressing). Enterprises must choose deliberately: SLAAC alone provides no
central record of which host holds which address unless DHCPv6 or another
tracking mechanism supplements it, which complicates IPAM and forensics.

### NTP: Time Synchronization and Stratum Hierarchy

Network Time Protocol (NTP), currently NTPv4 per [RFC 5905](https://www.rfc-editor.org/rfc/rfc5905), synchronizes
clocks across a network using a hierarchical stratum model:

| Stratum | Description |
| --- | --- |
| 0 | The reference clock itself (GPS receiver, atomic clock) — not on the network |
| 1 | A server directly connected to a stratum 0 reference source |
| 2 | A server that synchronizes from one or more stratum 1 servers |
| 3+ | Servers synchronizing from the stratum above; enterprise internal NTP servers are typically stratum 2 or 3 |

Accurate, synchronized time is a silent dependency of nearly everything else
in this volume and the chapters that follow: TLS certificate validation
depends on clock accuracy, Kerberos authentication fails outside a small
clock-skew tolerance, and — most relevant to [Chapter 8](08-network-validation-and-observability.md) and [Chapter 9](09-network-troubleshooting-and-operations.md) —
correlating syslog messages and flow records across multiple devices during
an incident is only possible if every device's clock agrees. A network
where every device free-runs its own clock cannot produce a trustworthy
timeline during troubleshooting or a security investigation.

Enterprises typically run two or more internal NTP servers that
synchronize from multiple external stratum 1/2 sources (for resilience
against any single upstream failure) and point all internal infrastructure
at the internal servers rather than having every device query the internet
directly — this reduces external dependency, external query volume, and
attack surface.

### NAT and PAT: Address Translation Mechanisms

Network Address Translation (NAT), defined conceptually in [RFC 3022](https://www.rfc-editor.org/rfc/rfc3022),
rewrites IP addresses (and, for PAT, transport-layer ports) as traffic
crosses a translation boundary, most commonly between private [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918)
address space and public, internet-routable address space.

| Term | Behavior |
| --- | --- |
| Static NAT | One private address maps permanently to one public address (1:1); used for servers that must be reachable inbound |
| Dynamic NAT | Private addresses draw from a pool of public addresses, still 1:1 per active translation |
| PAT (NAT Overload) | Many private addresses share one public address, distinguished by translated source port; the dominant form for outbound internet access |
| Destination NAT (DNAT) | Rewrites the destination address, commonly used to publish an internal service through a single public address/port |

```text
Before translation (inside):  10.1.2.50:51000  -> 93.184.216.34:443
After PAT (outside):          203.0.113.10:14022 -> 93.184.216.34:443
```

The router or firewall performing PAT maintains a translation table mapping
each `(inside address, inside port)` pair to a unique `(outside address,
outside port)` pair for the duration of the session, and reverses the
translation for return traffic. This is why PAT is inherently stateful and
why asymmetric routing — return traffic arriving at a different device than
the one that performed the outbound translation — breaks connectivity
outright rather than merely degrading it; the returning device has no
matching translation table entry.

As established in [Chapter 2](02-ip-addressing-and-subnetting.md), **NAT is a translation mechanism, not a
security boundary.** A PAT device only forwards return traffic that matches
an existing outbound-initiated translation, which incidentally behaves
similarly to a stateful firewall for unsolicited inbound traffic — but this
is a side effect of the translation table's statefulness, not a deliberate
security policy, and it provides none of the granular, auditable control
that dedicated firewall policy provides. IPv6's larger address space
generally removes the *address-scarcity* reason for NAT, but enterprises
still frequently deploy IPv6 firewall policy at the same boundary for
security reasons independent of translation.

## Design Considerations

- **Run at least two of every core service, on separate infrastructure.**
  A single DNS server, DHCP server, or NTP source is a single point of
  failure for name resolution, addressing, and time — three dependencies
  that silently underlie almost everything else in the network.
- **Size DHCP scopes with headroom, and set lease times deliberately.**
  Short lease times (minutes to hours) suit high-churn environments (guest
  Wi-Fi, BYOD) where address reclamation matters; longer lease times (days)
  reduce DHCP traffic in stable environments. A scope sized too close to
  actual demand exhausts under normal fluctuation, denying new clients
  addresses entirely.
- **Decide split-horizon DNS architecture at design time, not
  retroactively.** Determine which names must resolve differently
  inside vs. outside the enterprise before building the zone structure;
  retrofitting split-horizon onto a single flat zone is disruptive.
- **Treat internal NTP servers as infrastructure, not convenience.**
  Point every managed device at the same pair of internal NTP servers
  (rather than a mix of public/internal sources) so that clock skew between
  devices stays within the tolerance that log correlation ([Chapter 8](08-network-validation-and-observability.md)) and
  authentication protocols require.
- **Minimize NAT/PAT scope deliberately.** Use static NAT only for the
  specific services that must be reachable inbound; do not expose more
  through translation than the design requires. Evaluate whether IPv6
  removes the need for translation on new deployments, while recognizing
  that firewall policy at the boundary is still required regardless of
  whether translation is present.
- **Document DHCP option assignments (DNS, NTP, domain, PXE) alongside the
  IPAM record of address scopes**, since these options are how most hosts
  learn about every other service described in this chapter — an error in
  Option 6 or Option 42 silently misconfigures every DHCP client on that
  scope at once.

## Implementation and Automation

### DNS Zone File (BIND-Style, Vendor-Neutral)

```text
$TTL 300
@       IN      SOA     ns1.example.internal. hostmaster.example.internal. (
                        2026071801 ; serial
                        3600       ; refresh
                        900        ; retry
                        604800     ; expire
                        300 )      ; minimum/negative TTL
@       IN      NS      ns1.example.internal.
@       IN      NS      ns2.example.internal.
ns1     IN      A       10.10.1.10
ns2     IN      A       10.10.1.11
app01   IN      A       10.10.5.20
app01   IN      AAAA    2001:db8:5::20
www     IN      CNAME   app01.example.internal.
```

### DHCP Server Configuration (ISC Kea-Style, Vendor-Neutral)

```json
{
  "Dhcp4": {
    "interfaces-config": { "interfaces": ["eth1"] },
    "subnet4": [
      {
        "subnet": "10.1.2.128/26",
        "pools": [{ "pool": "10.1.2.150 - 10.1.2.190" }],
        "option-data": [
          { "name": "routers", "data": "10.1.2.129" },
          { "name": "domain-name-servers", "data": "10.10.1.10, 10.10.1.11" },
          { "name": "ntp-servers", "data": "10.10.1.20, 10.10.1.21" }
        ],
        "valid-lifetime": 28800
      }
    ]
  }
}
```

### NTP Client/Server Configuration (chrony-Style)

```text
# /etc/chrony.conf on an internal NTP server (stratum 2/3)
pool time.internal-pool.example.internal iburst
allow 10.0.0.0/8
local stratum 8

# /etc/chrony.conf on a standard managed device
server ns1.example.internal iburst
server ns2.example.internal iburst
```

### NAT/PAT Configuration (Vendor-Neutral Pseudo-CLI)

```text
device(config)# ip nat pool PUBLIC-POOL 203.0.113.10 203.0.113.10 prefix-length 29
device(config)# access-list 100 permit ip 10.1.0.0 0.0.255.255 any
device(config)# ip nat inside source list 100 pool PUBLIC-POOL overload
device(config)# interface gigabitethernet0/1
device(config-if)# ip nat inside
device(config)# interface gigabitethernet0/0
device(config-if)# ip nat outside
```

### Automating DNS Record Validation

```python
import dns.resolver  # dnspython

def resolve(name, rtype="A"):
    try:
        answers = dns.resolver.resolve(name, rtype)
        return sorted(str(rdata) for rdata in answers)
    except dns.resolver.NXDOMAIN:
        return None

expected = {"app01.example.internal": ["10.10.5.20"]}
for name, expected_ips in expected.items():
    actual = resolve(name)
    status = "OK" if actual == expected_ips else "MISMATCH"
    print(f"{name}: expected={expected_ips} actual={actual} [{status}]")
```

Configuration management (Ansible, or an IPAM tool's API as introduced in
[Chapter 2](02-ip-addressing-and-subnetting.md)) should generate DNS zone records, DHCP scopes, and NTP client
configuration from the same source-of-truth inventory used for IP address
allocation, so that a new subnet's addressing, naming, DHCP scope, and time
source are provisioned together rather than as four manually synchronized
steps.

## Validation and Troubleshooting

```bash
# DNS: query a specific resolver directly (bypasses local cache/search domain)
dig @10.10.1.10 app01.example.internal A +short

# DNS: confirm reverse lookup matches forward lookup
dig -x 10.10.5.20 +short

# DHCP: inspect the active lease on a Linux client
cat /var/lib/dhcp/dhclient.leases

# NTP: confirm synchronization state and current offset (chrony)
chronyc tracking
chronyc sources -v

# NAT: inspect active translations (vendor-neutral pseudo-CLI)
device# show ip nat translations
```

| Symptom | Likely Cause | Diagnostic |
| --- | --- | --- |
| Host can ping an IP but not a hostname | DNS resolution failure, not routing | `dig @<resolver> <name>`; compare against direct IP ping |
| `NXDOMAIN` for a record that should exist | Record missing, wrong zone/view served, or replication lag | Query the authoritative server directly with `dig @<auth-ns>` |
| Client gets an APIPA (`169.254.x.x`) address | No DHCP response reached the client — relay misconfigured or scope exhausted | Check relay `giaddr` config, check scope utilization |
| Client receives a lease but wrong DNS/gateway | Incorrect DHCP option data in the scope | Inspect scope options; compare against IPAM record of intended values |
| Devices' logs are out of order relative to real events | Clock skew between devices | `chronyc tracking` on each device; compare stratum and offset |
| Outbound internet access fails intermittently for some internal hosts | PAT port/address pool exhaustion | `show ip nat translations` count vs. pool capacity |
| Return traffic silently dropped after a routing change | Asymmetric routing broke a stateful NAT/firewall session | Confirm both directions traverse the same NAT device |

A layered read of these symptoms matters: "the application is down" is
frequently actually "DNS could not resolve the application's name" or "the
client never received a DHCP lease" — both of which are core-services
failures that will masquerade as an application or Layer 3 problem until a
`dig` or lease check narrows it down, consistent with the layered
troubleshooting order established in [Chapter 1](01-network-models-and-protocol-architecture.md).

## Security and Best Practices

- **DNS.** Restrict recursive resolution to trusted internal clients only
  (an open resolver is abused for DNS amplification attacks); consider
  DNSSEC for zones where response integrity matters, and DNS over
  TLS/HTTPS for resolver-to-client confidentiality where policy requires
  it. Rate-limit and monitor for anomalous query volume, which can indicate
  DNS tunneling used for data exfiltration.
- **DHCP.** Enable DHCP snooping on access-layer switches (Layer 2
  infrastructure covered in [Chapter 3](03-ethernet-switching-vlans-and-layer-2-resilience.md)) to prevent rogue DHCP servers from
  handing out malicious gateway or DNS options; combine with the IPv6
  Router Advertisement Guard and DHCPv6 Guard controls introduced in
  [Chapter 2](02-ip-addressing-and-subnetting.md).
- **NTP.** Restrict which hosts may query an internal NTP server (`allow`
  statements scoped to internal ranges) and consider NTP authentication
  (symmetric keys or NTS) for high-assurance environments, since an
  attacker who can shift a device's clock can undermine certificate
  validation and Kerberos authentication elsewhere in the environment.
- **NAT.** Log NAT translations with enough retention to support
  investigation — because many internal hosts share one public address
  under PAT, the translation log (source address, source port, translated
  port, timestamp) is frequently the only record that attributes an
  external connection back to a specific internal host.
- **General.** Apply least-privilege management access to DNS, DHCP, and
  NTP infrastructure specifically; compromise of any one of these services
  gives an attacker a durable foothold to redirect, misdirect, or
  desynchronize the rest of the environment.

## References and Knowledge Checks

**References**

- [RFC 1035 — Domain Names: Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035)
- [RFC 2131 — Dynamic Host Configuration Protocol](https://www.rfc-editor.org/rfc/rfc2131)
- [RFC 3315 — Dynamic Host Configuration Protocol for IPv6 (DHCPv6)](https://www.rfc-editor.org/rfc/rfc3315)
- [RFC 5905 — Network Time Protocol Version 4](https://www.rfc-editor.org/rfc/rfc5905)
- [RFC 3022 — Traditional IP Network Address Translator (Traditional NAT)](https://www.rfc-editor.org/rfc/rfc3022)
- [RFC 9210 — DNS Transport over TCP / DNSSEC operational guidance](https://www.rfc-editor.org/rfc/rfc9210)

**Knowledge Checks**

1. Explain the four messages in the DHCP DORA exchange and why
   `DHCPREQUEST` is broadcast rather than unicast to the offering server.
2. Why does a DHCP relay agent need to insert its own address (`giaddr`)
   into the relayed request?
3. What is the practical difference between recursive and authoritative
   DNS resolution, and which one does a typical enterprise host perform?
4. Why is accurate time synchronization a prerequisite for both security
   controls and troubleshooting, rather than a convenience feature?
5. Explain why asymmetric routing breaks a PAT translation, using the
   concept of a stateful translation table.
6. A user reports "the application is down," but the application server
   responds normally to a direct IP ping. What core service should be
   checked first, and with what command?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each core network service** — DHCP, DNS,
NTP, and NAT. Labs use standard client tools and lightweight servers. Each ends **`**Lab verified
by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.4** — a Linux host with `dig`, `chronyc`, and (for the DHCP/NAT
labs) `dnsmasq`/`nft` and `sudo`. **Cost:** none.

### Lab 5.1 — DHCP (Topic: Dynamic addressing)

**Objective:** Observe the DHCP lease process.

```bash
sudo dhclient -v eth0 2>&1 | grep -iE "DHCPDISCOVER|DHCPOFFER|DHCPREQUEST|DHCPACK|bound"
ip addr show eth0 | grep inet
```

**Expected result:** the four-message **DORA** exchange (Discover → Offer → Request → Ack) and a
bound lease with an address, gateway, and DNS — DHCP automates host addressing: the client broadcasts
Discover, a server Offers, the client Requests, the server acknowledges, and the host is configured with a
time-limited lease.

**Negative test:** expect a host to get an address with no DHCP server reachable on the segment;
Discover goes unanswered and the host self-assigns a useless link-local (169.254.x) — a reachable
DHCP server (or static config) is required.

**Cleanup:** none (or `sudo dhclient -r eth0` to release).

### Lab 5.2 — DNS resolution (Topic: Name resolution)

**Objective:** Trace how a name becomes an address.

```bash
dig +trace example.com A | tail -20        # walks root -> TLD -> authoritative
dig example.com A +short                    # the answer
dig -x 93.184.216.34 +short                 # reverse (PTR) lookup
```

**Expected result:** `+trace` shows the recursive resolution from the root servers down to the
authoritative answer, and reverse lookup maps IP→name — DNS is the distributed hierarchy that
resolves names to addresses; a resolver walks root → TLD → authoritative (or uses a cache) to answer.

**Negative test:** blame "the network" when a site fails but `dig` returns SERVFAIL or NXDOMAIN; the
failure is name resolution, not connectivity — `dig` distinguishes a DNS problem from a reachability
problem.

**Cleanup:** none (read-only).

### Lab 5.3 — NTP time synchronization (Topic: Time)

**Objective:** Confirm the host's clock is synchronized.

```bash
chronyc sources -v | head
chronyc tracking | grep -E "Reference|Stratum|System time"
timedatectl | grep -i synchronized
```

**Expected result:** reachable time sources with a selected synchronization source and a small system
offset — NTP keeps clocks synchronized to a reference (stratum hierarchy), which is required for logs
to correlate, TLS certificates to validate, and Kerberos/2FA to work.

**Negative test:** operate with an unsynchronized clock; log timestamps across hosts do not correlate
and certificate/time-sensitive auth fails — NTP is a quiet but critical core service.

**Cleanup:** none (read-only).

### Lab 5.4 — NAT (Topic: Address translation)

**Objective:** Translate a private subnet to a routable address.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo nft add table ip nat 2>/dev/null
sudo nft 'add chain ip nat postrouting { type nat hook postrouting priority 100 ; }'
sudo nft add rule ip nat postrouting oifname "eth0" masquerade
sudo nft list table ip nat
```

**Expected result:** private-source traffic egressing `eth0` is masqueraded to the host's public
address — **NAT** (masquerade/PAT) lets many private hosts share one routable address by rewriting the
source IP/port, which is how private IPv4 networks reach the internet.

**Negative test:** expect private (RFC 1918) addresses to be routable on the internet directly; they
are not — NAT (or IPv6 global addressing) is what gives private hosts external reachability.

**Cleanup:** `sudo nft delete table ip nat; sudo sysctl -w net.ipv4.ip_forward=0`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter covered the four core services every enterprise network
depends on but rarely notices when working correctly: DNS name resolution,
DHCP automatic addressing, NTP time synchronization, and NAT/PAT address
translation. The hands-on lab combined DHCP-assigned addressing, custom DNS
resolution, and PAT into a single working topology and reproduced a DHCP
scope exhaustion failure — a fault class that presents as "the network is
down" but is actually a core-services problem, reinforcing the layered
diagnostic habit from [Chapter 1](01-network-models-and-protocol-architecture.md).

**Completion Checklist**

- [ ] Can explain recursive vs. authoritative DNS resolution and the role
      of TTL-based caching.
- [ ] Can walk through the DHCP DORA exchange and explain the purpose of
      DHCP relay.
- [ ] Understands why NTP stratum and clock accuracy matter beyond simple
      convenience.
- [ ] Can distinguish static NAT, dynamic NAT, PAT, and DNAT, and explain
      why PAT requires stateful translation tracking.
- [ ] Implemented and validated DHCP, DNS, and PAT together in a single
      lab topology.
- [ ] Reproduced and correctly diagnosed a DHCP scope exhaustion failure.
