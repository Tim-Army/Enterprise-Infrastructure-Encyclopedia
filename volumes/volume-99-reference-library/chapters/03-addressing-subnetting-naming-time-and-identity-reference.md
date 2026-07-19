# Chapter 03: Addressing, Subnetting, Naming, Time, and Identity Reference

## Learning Objectives

- Calculate subnet boundaries, host counts, and wildcard masks for any
  IPv4 CIDR prefix without a calculator, and map IPv6 prefix lengths to
  their conventional use (point-to-point, subnet, site).
- Identify [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) private IPv4 ranges, IPv6 address scopes, and the
  reserved/special-use ranges that must never be assigned to production
  hosts.
- Apply a consistent enterprise naming convention (hostname, FQDN, DNS
  zone) across Linux, Windows, network devices, and cloud resources.
- Explain NTP stratum layering and select an appropriate time-source
  design for a multi-site enterprise.
- Read and construct an LDAP/Active Directory distinguished name, a
  Kerberos principal, and an AWS ARN, and know which volume treats each in
  depth.

## Theory and Architecture

Addressing, naming, time, and identity are four independent systems that
enterprise infrastructure engineers routinely need side by side — a
certificate is issued to a name, validated against a time window, and
often binds to an identity that resolves through directory services running
on a specific address. Treating them as one reference chapter reflects how
they are actually consumed during real work, even though each has its own
theoretical foundation covered in depth elsewhere ([Volume II](../../volume-02-network-engineering-foundations/README.md) for addressing,
[Volume IV](../../volume-04-enterprise-systems-administration/README.md) for identity and naming infrastructure).

- **IPv4 addressing** is a 32-bit space divided by a prefix length (CIDR)
  into a network portion and a host portion. Classless Inter-Domain
  Routing (CIDR, [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632)) replaced the old class A/B/C system; the prefix
  length, not the leading bits of the address, now determines the network
  boundary.
- **IPv6 addressing** is a 128-bit space designed around abundant address
  space rather than conservation: the conventional allocation is a /64 per
  subnet (leaving 64 bits for host/interface identifiers, often derived
  from EUI-64 or randomized per [RFC 7217](https://www.rfc-editor.org/rfc/rfc7217)), a /56 or /48 per site, and a
  /127 or /64 for point-to-point links depending on operator convention.
- **DNS naming** is a hierarchical, delegated namespace; an FQDN reads
  right-to-left in authority (root, top-level domain, registered domain,
  subdomain, host), and every enterprise should treat its internal DNS
  zone design as infrastructure, not as an afterthought of DHCP.
- **Time synchronization** underpins nearly every other system in this
  chapter: Kerberos tickets fail outside a default five-minute clock skew,
  TLS certificate validation depends on accurate wall-clock time, and log
  correlation across systems ([Chapter 06](06-troubleshooting-decision-aids-and-escalation.md)) is only possible if every source
  shares a time reference.
- **Identity** systems (LDAP/Active Directory, Kerberos, cloud IAM)
  layer a namespace of their own — a distinguished name, a principal, or
  an ARN — on top of addressing and naming, and each has its own syntax
  that engineers must read correctly even outside the platform that issued
  it.

## Design Considerations

- **Size subnets for the actual host count plus planned growth, not for
  round numbers.** A /24 (254 usable hosts) is a habit, not a requirement;
  right-sizing VLANs and subnets ([Volume II](../../volume-02-network-engineering-foundations/README.md)) reduces broadcast domain size
  and conserves address space in environments running out of [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918)
  space across many sites or environments (dev/stage/prod × multiple
  regions).
- **Reserve address ranges for function, not for convenience at
  allocation time.** A documented scheme (for example, third octet
  encodes site, fourth-octet ranges encode role: .1–.9 infrastructure,
  .10–.199 DHCP, .200–.254 static) makes an unfamiliar subnet
  self-documenting during an incident.
- **Adopt IPv6 dual-stack deliberately, not incidentally.** Many
  platforms in this encyclopedia (Kubernetes, cloud VPCs, RHEL 10, Ubuntu
  26.04) ship IPv6-capable by default; an explicit IPv6 addressing plan
  prevents undocumented link-local/ULA traffic from becoming an untracked
  attack surface.
- **Separate internal and external DNS namespaces**, either with a split
  zone or entirely distinct domains, so that internal hostnames are not
  disclosed by public DNS queries and so that internal resolution does not
  depend on internet reachability.
- **Design the NTP hierarchy before an incident forces it.** A single
  external NTP source with no internal stratum-2 distribution layer is a
  common single point of failure that only becomes visible when it is
  unreachable during a certificate or Kerberos-dependent outage.
- **Choose a directory and identity naming convention that survives
  mergers and reorganizations.** Distinguished names and UPN suffixes that
  encode a specific team or building name age poorly; prefer stable,
  organization-level naming.

## Implementation and Automation

### IPv4 CIDR quick-reference

| CIDR (/prefix) | Subnet Mask | Wildcard Mask | Usable Hosts | Common Use |
| --- | --- | --- | --- | --- |
| /30 | 255.255.255.252 | 0.0.0.3 | 2 | Point-to-point WAN/router link |
| /29 | 255.255.255.248 | 0.0.0.7 | 6 | Small point-to-multipoint segment |
| /28 | 255.255.255.240 | 0.0.0.15 | 14 | Small equipment/management subnet |
| /27 | 255.255.255.224 | 0.0.0.31 | 30 | Small office/branch subnet |
| /26 | 255.255.255.192 | 0.0.0.63 | 62 | Mid-size branch, small server VLAN |
| /25 | 255.255.255.128 | 0.0.0.127 | 126 | Medium VLAN |
| /24 | 255.255.255.0 | 0.0.0.255 | 254 | Standard server/user VLAN |
| /23 | 255.255.254.0 | 0.0.1.255 | 510 | Large user VLAN, two /24s combined |
| /22 | 255.255.252.0 | 0.0.3.255 | 1022 | Campus/site aggregate |
| /16 | 255.255.0.0 | 0.0.255.255 | 65534 | Site-wide or regional summary block |
| /8 | 255.0.0.0 | 0.255.255.255 | 16777214 | Enterprise-wide [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) allocation |

Usable hosts = 2^(32 − prefix) − 2 (network and broadcast addresses
reserved), except for /31 ([RFC 3021](https://www.rfc-editor.org/rfc/rfc3021), point-to-point, both addresses
usable, 2 hosts) and /32 (a single host route, 1 address).

### [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) and other special-use IPv4 ranges

| Range | CIDR | Purpose |
| --- | --- | --- |
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | Private use (large enterprise allocation) |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | Private use (mid-size allocation) |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | Private use (small office/branch allocation) |
| 169.254.0.0 – 169.254.255.255 | 169.254.0.0/16 | Link-local (APIPA); indicates failed DHCP, not a routable assignment |
| 127.0.0.0 – 127.255.255.255 | 127.0.0.0/8 | Loopback |
| 100.64.0.0 – 100.127.255.255 | 100.64.0.0/10 | Carrier-Grade NAT ([RFC 6598](https://www.rfc-editor.org/rfc/rfc6598)); increasingly used inside cloud/Kubernetes fabrics to avoid [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) collisions |
| 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 | — | TEST-NET-1/2/3; reserved for documentation and examples (used throughout this encyclopedia's sample configs) |
| 224.0.0.0 – 239.255.255.255 | 224.0.0.0/4 | Multicast |

### IPv6 address types and scopes

| Address Type | Prefix / Pattern | Scope | Notes |
| --- | --- | --- | --- |
| Global unicast | 2000::/3 | Global | Publicly routable; typically allocated by an RIR/ISP as a /32–/48 to an organization. |
| Unique local address (ULA) | fc00::/7 (fd00::/8 in practice) | Site-local, not globally routed | The IPv6 analog to [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) space for internal-only addressing. |
| Link-local | fe80::/10 | Single link only | Auto-configured on every interface; required for Neighbor Discovery and never routed. |
| Loopback | ::1/128 | Host-local | Equivalent to IPv4 127.0.0.1. |
| Unspecified | ::/128 | N/A | Source address before an address is assigned (used during DHCPv6/SLAAC). |
| Multicast | ff00::/8 | Varies by flag/scope field | Replaces IPv4 broadcast entirely; ff02::1 is all-nodes link-local, ff02::2 is all-routers link-local. |
| IPv4-mapped | ::ffff:0:0/96 | N/A | Represents an IPv4 address inside dual-stack socket APIs. |

### DNS and hostname naming conventions

| Element | Convention | Example |
| --- | --- | --- |
| Hostname | Lowercase, hyphen-separated, role-and-site encoded, no underscores (invalid in strict hostname parsing) | `web-use1-prod-01` |
| Internal DNS zone | A dedicated, non-publicly-resolvable zone or split-horizon view | `corp.internal`, or split-view `example.com` |
| FQDN | `<hostname>.<subdomain>.<domain>.<tld>` | `web-use1-prod-01.svc.example.com` |
| Active Directory domain | Matches or is a subdomain of the registered external domain to avoid split-brain surprises | `corp.example.com` |
| Kubernetes service DNS | `<service>.<namespace>.svc.cluster.local` | `api.payments.svc.cluster.local` |
| Certificate Subject Alternative Name | Must match the FQDN(s) actually used by clients, not just the primary hostname | `web-use1-prod-01.example.com` |

### NTP stratum design

| Stratum | Definition | Typical Role in an Enterprise |
| --- | --- | --- |
| 0 | Reference clocks themselves (GPS, atomic, radio) — not network-addressable | Hardware time source, not queried directly over NTP |
| 1 | Servers directly synchronized to a stratum 0 source | External public NTP pool servers, or an on-site GPS appliance |
| 2 | Servers synchronized to stratum 1 | Recommended internal enterprise NTP distribution layer (two to four servers, one per site or region) |
| 3+ | Servers synchronized to stratum 2 and below | Individual hosts, network devices, hypervisors — the majority of the fleet |

Design pattern: point every host and device at the internal stratum-2
layer, not directly at external stratum-1 sources; this bounds the blast
radius of an external NTP outage and keeps time-sensitive internal traffic
off the public internet path.

```bash
# Linux (chrony, RHEL 10 / Ubuntu 26.04 default) - verify sync status
chronyc tracking
chronyc sources -v
```

```text
! Cisco IOS XE - configure NTP client against an internal stratum-2 pair
ntp server 10.10.1.10 prefer
ntp server 10.10.1.11
```

### Identity namespace reference

| System | Format | Example | Primary Reference Volume |
| --- | --- | --- | --- |
| LDAP/AD Distinguished Name (DN) | `CN=<name>,OU=<org unit>,DC=<domain>,DC=<tld>` | `CN=Jane Doe,OU=Engineering,DC=corp,DC=example,DC=com` | [Volume IV](../../volume-04-enterprise-systems-administration/README.md) |
| User Principal Name (UPN) | `<user>@<UPN suffix>` | `jane.doe@corp.example.com` | [Volume IV](../../volume-04-enterprise-systems-administration/README.md) |
| Kerberos principal | `<primary>/<instance>@<REALM>` | `host/web-use1-prod-01.example.com@CORP.EXAMPLE.COM` | [Volume IV](../../volume-04-enterprise-systems-administration/README.md) |
| Service Principal Name (SPN) | `<service class>/<host>:<port>` | `HTTP/web-use1-prod-01.example.com` | [Volume IV](../../volume-04-enterprise-systems-administration/README.md) |
| AWS Amazon Resource Name (ARN) | `arn:<partition>:<service>:<region>:<account-id>:<resource>` | `arn:aws:iam::123456789012:role/DeployRole` | [Volume XVII](../../volume-17-aws-architecture-security/README.md) |
| X.509 certificate Subject | `CN=<name>, O=<org>, C=<country>` plus SAN extension for actual validated names | `CN=web-use1-prod-01.example.com, O=Example Corp, C=US` | [Volume X](../../volume-10-enterprise-cybersecurity/README.md) |
| Kubernetes RBAC subject | `ServiceAccount:<namespace>:<name>` or a federated identity (OIDC subject) | `system:serviceaccount:payments:api-deployer` | [Volume VIII](../../volume-08-containers-platform-engineering/README.md) |

## Validation and Troubleshooting

- **Confirm subnet math with a second method before applying a change.**
  Cross-check a manually calculated network/broadcast address against
  `ipcalc <CIDR>` (Linux) or an equivalent subnet calculator; misreading a
  CIDR boundary is one of the most common causes of an outage that "should
  have worked on paper."
  \* `ipcalc` may need to be installed separately (`dnf install ipcalc` /
  `apt install ipcalc`) and is not present on every base image.
- **Verify DNS resolution at both the resolver and authoritative
  layers.** `dig <name> @<resolver>` followed by `dig <name>
  @<authoritative-server>` isolates a caching/forwarding problem from an
  actual record error.
- **Check time skew before troubleshooting an authentication failure.**
  `chronyc tracking` (Linux) or `w32tm /query /status` (Windows) should be
  the first check when Kerberos authentication or TLS certificate
  validation fails intermittently; skew beyond the protocol's tolerance
  produces errors that look unrelated to time.
- **Validate a distinguished name or UPN with a directory query before
  assuming a typo is elsewhere.** `ldapsearch -x -b "<base DN>"
  "(userPrincipalName=<upn>)"` confirms the object exists and the DN is
  correctly formed.
- **Confirm IPv6 reachability separately from IPv4** on dual-stack hosts;
  `ping` (IPv4) succeeding does not confirm `ping6`/`ping -6` will, and
  silently broken IPv6 is a common source of intermittent, hard-to-explain
  latency when an application prefers IPv6 (Happy Eyeballs, [RFC 8305](https://www.rfc-editor.org/rfc/rfc8305)) but
  the path is actually broken.

## Security and Best Practices

- Never assign a link-local (169.254.0.0/16) or documentation range
  (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) address to a production
  host; both indicate a configuration failure or a documentation example
  respectively, and their presence in production logs is itself a signal
  worth alerting on.
- Restrict recursive DNS resolution and zone transfers to authorized
  internal clients only; an open resolver or an unrestricted zone
  transfer (`AXFR`) discloses internal naming and addressing structure to
  any requester.
- Run internal NTP through authenticated servers (NTS — Network Time
  Security, or at minimum symmetric-key authentication) where the
  platform supports it, since an attacker who can shift a host's clock can
  undermine certificate validation and Kerberos ticket lifetimes.
- Avoid encoding sensitive information (employee names, project
  codenames, security posture) directly in externally visible DNS names;
  internal-only naming detail belongs in the internal split-horizon zone.
- Scope Kerberos SPNs and AD delegation narrowly; an SPN registered
  against the wrong account or an over-broad constrained-delegation
  configuration is a well-documented Active Directory privilege-escalation
  path ([Volume IV](../../volume-04-enterprise-systems-administration/README.md), [Volume X](../../volume-10-enterprise-cybersecurity/README.md)).
- Rotate and scope cloud IAM identities referenced by ARNs to the minimum
  required resource and action; treat an ARN in a policy document as
  sensitive-adjacent, since it discloses account IDs and resource
  structure.

## References and Knowledge Checks

**References**

- [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) (private IPv4 address allocation), [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632) (CIDR), [RFC 3021](https://www.rfc-editor.org/rfc/rfc3021)
  (/31 point-to-point).
- [RFC 4291](https://www.rfc-editor.org/rfc/rfc4291) (IPv6 addressing architecture), [RFC 4193](https://www.rfc-editor.org/rfc/rfc4193) (unique local
  addresses), [RFC 7217](https://www.rfc-editor.org/rfc/rfc7217) (privacy-stable IPv6 interface identifiers).
- [RFC 5905](https://www.rfc-editor.org/rfc/rfc5905) (NTPv4), [RFC 8915](https://www.rfc-editor.org/rfc/rfc8915) (Network Time Security for NTP).
- [RFC 4120 (Kerberos V5), Microsoft Active Directory technical
  documentation (`learn.microsoft.com/windows-server/identity`).](https://learn.microsoft.com/en-us/windows-server/identity/identity-and-access)
- [AWS ARN format reference (`docs.aws.amazon.com/IAM`](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) — ARN general
  syntax).
- [Volume II](../../volume-02-network-engineering-foundations/README.md) — Network Engineering Foundations.
- [Volume IV](../../volume-04-enterprise-systems-administration/README.md) — Enterprise Systems Administration (identity and directory
  services).
- [Volume XVII](../../volume-17-aws-architecture-security/README.md) — AWS Architecture and Security (IAM and ARN scoping).

**Knowledge checks**

1. Calculate the network address, broadcast address, and usable host
   range for 10.20.30.64/27.
2. Why does an enterprise typically distribute NTP through an internal
   stratum-2 layer rather than pointing every host directly at an
   external stratum-1 source?
3. Write the Kerberos SPN you would expect for an HTTP service running on
   `app01.corp.example.com`.
4. A host is observed using an address in 169.254.0.0/16. What does this
   indicate, and what should be checked first?

## Hands-On Lab

**Objective:** Produce a validated addressing, naming, and time
quick-reference card for a lab or work subnet, and confirm identity
namespace values against a real directory or cloud account.

**Prerequisites:** A lab subnet you can address; access to `dig`/
`nslookup`; access to `chronyc` or `w32tm`; optional access to an LDAP/AD
directory or an AWS account for the identity section (substitute a local
example if unavailable).

1. Choose a lab CIDR block (for example a /26) and calculate its network
   address, broadcast address, usable host range, and wildcard mask by
   hand. **Expected result:** four values recorded.
2. Verify the calculation with `ipcalc` (or an equivalent tool) and
   record any discrepancy. **Expected result:** the manual calculation
   either matches or the error is identified and corrected.
3. Query DNS for three real hostnames in your environment using `dig`
   against both the internal resolver and, if permitted, the
   authoritative server directly. **Expected result:** both queries
   return consistent records, or a discrepancy is documented as a finding.
4. Run `chronyc tracking` (or `w32tm /query /status`) on a lab host and
   record the current stratum and offset. **Expected result:** offset is
   within an acceptable bound (generally well under one second); if not,
   record it as a finding requiring follow-up.
5. Look up or construct one example of each identity format in the table
   above (DN, UPN, SPN, ARN) using real or clearly-marked placeholder
   values from your environment. **Expected result:** four correctly
   formatted identity strings recorded.
6. Negative test: attempt to resolve a documentation-range address
   (`192.0.2.1`) in reverse DNS (`dig -x 192.0.2.1`) and record the
   result. **Expected result:** the query fails or returns no
   authoritative answer, confirming the range is non-routable/reserved as
   documented.
7. Assemble all findings into `addressing-identity-card.md` with clearly
   labeled sections for addressing, naming, time, and identity.
   **Expected result:** a single reference file covering all four systems
   for your environment.

**Cleanup:** Remove any captured directory query output containing real
personal data before storing or sharing the card; retain only the
structural format, not populated personal identifiers, if the card will
be shared outside your immediate team.

## Summary and Completion Checklist

This chapter consolidated four systems an enterprise engineer moves
between constantly: IPv4/IPv6 addressing and subnetting math, DNS/hostname
naming conventions, NTP stratum design, and the identity namespace formats
(DN, UPN, SPN, ARN, X.509 Subject) used by directory services, Kerberos,
and cloud IAM. The CIDR and [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918)/IPv6 scope tables function as a
standing calculator; the naming and identity tables function as a syntax
reference for reading and writing correctly formed names without
consulting the full per-volume treatment.

- [ ] I can calculate usable host count and boundaries for any IPv4 CIDR
      prefix without a lookup table.
- [ ] I can identify [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918), link-local, and documentation-range
      addresses on sight and explain why each must not appear in
      production.
- [ ] I can distinguish IPv6 global unicast, unique local, and link-local
      scopes.
- [ ] I can explain NTP stratum layering and why internal distribution is
      preferred over direct external synchronization for the whole fleet.
- [ ] I can read and construct a distinguished name, UPN, SPN, and AWS
      ARN.
- [ ] I produced a validated addressing/naming/time/identity reference
      card for a real or lab environment.
