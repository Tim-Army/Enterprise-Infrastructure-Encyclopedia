# Chapter 06: DNS, DHCP, and IP Address Management

## Learning Objectives

- Configure AD-integrated DNS zones, records, forwarders, and DNSSEC.
- Explain how AD relies on DNS locator records and how to keep them healthy.
- Deploy DHCP scopes, reservations, options, policies, and failover.
- Integrate DHCP with DNS dynamic updates safely.
- Centralize address management and auditing with IP Address Management (IPAM).

## Theory and Architecture

**DNS** is the naming system Active Directory depends on absolutely.
Domain controllers publish **service (SRV) locator records** under
`_msdcs.<forest>` so clients can find a DC, a global catalog, or the PDC
Emulator; if these records are wrong or unreachable, logon and replication
fail. Windows DNS zones are usually **AD-integrated**, meaning the zone data
lives in an AD application partition and replicates with the directory
(multi-master, secure), rather than in a flat file with a single writable
primary. Zones hold records — **A/AAAA** (host), **PTR** (reverse),
**CNAME** (alias), **MX**, **SRV**, and **TXT**. **Forwarders** send queries
the server is not authoritative for to an upstream resolver;
**conditional forwarders** send queries for a specific domain to a specific
server (used for trusts and split-DNS). **DNSSEC** signs zone data so
resolvers can validate that answers are authentic and untampered.

**DHCP** leases IP configuration to clients. A **scope** defines a range of
addresses for a subnet, with a subnet mask, lease duration, and **options**
(default gateway 003, DNS servers 006, DNS domain 015, and many more)
delivered at scope, reservation, or server level. **Reservations** tie a
MAC/DUID to a fixed address. **DHCP policies** hand out different options or
ranges based on client attributes (vendor class, MAC prefix). **DHCP
failover** pairs two servers for a scope in **load-balance** (both active,
split load) or **hot-standby** (one active, one standby) mode so a single
server outage does not stop leasing. DHCP can perform **dynamic DNS
updates** on behalf of clients, which must be configured carefully to avoid
stale or hijacked records.

**IPAM** is a management layer that discovers DNS and DHCP servers across
the forest, inventories address space, tracks utilization, and centralizes
auditing and configuration — the single pane for "what is using
10.10.5.0/24 and who changed this scope."

## Design Considerations

Make DNS **AD-integrated** for secure dynamic updates and multi-master
resilience, and ensure every DC that is a DNS server points its **DNS
client** at another DC first (and itself second) to avoid the "island"
problem where a DC only trusts its own possibly-stale copy at boot. Use
**forwarders** to a reliable upstream and **conditional forwarders** for
trusted domains; enable **DNSSEC** where answer authenticity matters.

Size **DHCP scopes** with headroom and set lease durations to match churn —
short for guest/wireless, long for stable wired. Use **failover** for every
production scope (hot-standby across sites, load-balance within a site).
Prefer **reservations** over static addresses for servers that must be
predictable but centrally managed. Configure **DNS dynamic update
credentials** on DHCP (a dedicated low-privilege account) and enable
**name protection** so a rogue client cannot overwrite another's record.
Deploy **IPAM** once you have more than a couple of DNS/DHCP servers — the
audit trail and utilization data pay for themselves.

## Implementation and Automation

Create an AD-integrated zone and records:

```powershell
Add-DnsServerPrimaryZone -Name "corp.contoso.lab" -ReplicationScope Forest
Add-DnsServerResourceRecordA -ZoneName "corp.contoso.lab" -Name "app01" -IPv4Address 10.10.0.50 -CreatePtr
Add-DnsServerConditionalForwarderZone -Name "partner.example" -MasterServers 10.99.0.10
Add-DnsServerForwarder -IPAddress 1.1.1.1, 9.9.9.9
```

Stand up DHCP with a scope, options, and failover:

```powershell
Install-WindowsFeature DHCP -IncludeManagementTools
Add-DhcpServerv4Scope -Name "LAN" -StartRange 10.10.0.100 -EndRange 10.10.0.200 -SubnetMask 255.255.255.0
Set-DhcpServerv4OptionValue -ScopeId 10.10.0.0 -DnsServer 10.10.0.10 -Router 10.10.0.1 -DnsDomain "corp.contoso.lab"
Add-DhcpServerv4Failover -Name "LAN-FO" -ScopeId 10.10.0.0 -PartnerServer "DHCP02" -LoadBalancePercent 50
Add-DhcpServerInDC   # authorize the server in AD
```

Enable and validate DNSSEC signing:

```powershell
Invoke-DnsServerZoneSign -ZoneName "corp.contoso.lab" -SignWithDefault
Get-DnsServerZone "corp.contoso.lab" | Select-Object ZoneName, IsSigned
```

## Validation and Troubleshooting

Verify the locator records AD depends on, then leasing:

```powershell
Resolve-DnsName -Name "_ldap._tcp.dc._msdcs.corp.contoso.lab" -Type SRV
nltest /dsgetdc:corp.contoso.lab           # which DC does the locator return?
Get-DhcpServerv4Scope | Select-Object ScopeId, State
Get-DhcpServerv4ScopeStatistics 10.10.0.0  # in-use vs free
```

The SRV query should return the DCs; if it fails, DNS is broken and logon
will be too. `nltest /dsgetdc` confirms DC location and which site the
client is mapped to. Common issues: a DC pointing its DNS **only** at itself
(island problem) so it never learns others; **stale records** from clients
that changed IP without deregistering (enable scavenging carefully); a DHCP
server **not authorized** in AD (`Add-DhcpServerInDC`) so it refuses to
lease; **overlapping scopes** or exhausted pools; and dynamic-update failures
where DHCP's update account lacks rights or name protection blocks an
overwrite. `dcdiag /test:DNS` runs a DNS-specific health battery on a DC.

## Security and Best Practices

Require **secure dynamic updates** on AD-integrated zones so only
authenticated principals can change records. Enable **DNSSEC** for zones
where spoofing is a concern, and **DNS query resolution policies** or
Response Rate Limiting to blunt abuse. Run DHCP's dynamic DNS updates under
a **dedicated, low-privilege service account**, enable **name protection**,
and authorize DHCP servers explicitly. Restrict **zone transfers** to known
secondaries (or avoid them entirely with AD-integrated replication). Use
**IPAM role-based access** to give scope-level operators the minimum needed
and to keep an audit trail of every DHCP/DNS change. Monitor for rogue DHCP
servers, which IPAM and DHCP server authorization help contain.

## References and Knowledge Checks

- Microsoft Learn: *DNS Server*; *DHCP*; *DNSSEC*; *IP Address Management (IPAM)*.
- Microsoft Learn: AZ-800 — *Implement and manage on-premises and hybrid networking infrastructure*.

**Knowledge checks**

1. Which DNS records let a client find a domain controller, and where do they live?
2. What is the DNS "island" problem and how does DC DNS-client ordering avoid it?
3. When would you choose DHCP hot-standby failover over load-balance?

## Hands-On Lab

Topic-level walkthroughs for AZ-800's networking-services skills.

**Shared prerequisites for Labs 6.1–6.4** — `DC01` (DNS) in
`corp.contoso.lab`, a server for DHCP, and Domain Admin rights. **Cost:** none.

### Lab 6.1 — Create an AD-integrated record and a conditional forwarder (Topic: Manage DNS)

**Objective:** Add a host record and route a domain to a specific server.

```powershell
Add-DnsServerResourceRecordA -ZoneName "corp.contoso.lab" -Name "app01" -IPv4Address 10.10.0.50 -CreatePtr
Add-DnsServerConditionalForwarderZone -Name "partner.example" -MasterServers 10.99.0.10
Resolve-DnsName app01.corp.contoso.lab
```

**Expected result:** `app01` resolves to `10.10.0.50` and the conditional
forwarder appears in `Get-DnsServerZone` — AD-integrated records replicate to
every DC automatically.

**Negative test:** add a duplicate A record with a different IP; resolution
becomes non-deterministic (round-robin) — avoid conflicting A records for one
name.

**Cleanup:** remove the record and conditional forwarder.

### Lab 6.2 — Verify domain-controller locator records (Topic: Support AD with DNS)

**Objective:** Prove the SRV records AD depends on exist.

```powershell
Resolve-DnsName "_ldap._tcp.dc._msdcs.corp.contoso.lab" -Type SRV
nltest /dsgetdc:corp.contoso.lab
```

**Expected result:** the SRV query returns `DC01` and `nltest` reports the
located DC and site — these records are how clients find a DC; without them,
logon fails.

**Negative test:** stop the `Netlogon` service on the DC and re-run after a
scavenge; the SRV records can disappear and location fails — Netlogon
registers the locator records.

**Cleanup:** restart `Netlogon` and run `ipconfig /registerdns` / `dcdiag /fix`.

### Lab 6.3 — Deploy a DHCP scope with options and authorize the server (Topic: Manage DHCP)

**Objective:** Lease addresses with correct gateway and DNS.

```powershell
Install-WindowsFeature DHCP -IncludeManagementTools
Add-DhcpServerv4Scope -Name "LAN" -StartRange 10.10.0.100 -EndRange 10.10.0.200 -SubnetMask 255.255.255.0
Set-DhcpServerv4OptionValue -ScopeId 10.10.0.0 -Router 10.10.0.1 -DnsServer 10.10.0.10 -DnsDomain "corp.contoso.lab"
Add-DhcpServerInDC
Get-DhcpServerv4Scope | Select-Object ScopeId, State
```

**Expected result:** the scope is `Active` and the server is authorized;
clients receive an address plus gateway and DNS options — an unauthorized
DHCP server will not lease in an AD environment.

**Negative test:** skip `Add-DhcpServerInDC`; the DHCP service starts but
refuses to lease and logs an "unauthorized" event — AD authorization is
mandatory.

**Cleanup:** `Remove-DhcpServerv4Scope -ScopeId 10.10.0.0 -Force`.

### Lab 6.4 — Configure DHCP failover (Topic: High-availability DHCP)

**Objective:** Pair two DHCP servers for a scope.

```powershell
Add-DhcpServerv4Failover -Name "LAN-FO" -ScopeId 10.10.0.0 -PartnerServer "DHCP02" `
  -LoadBalancePercent 50 -SharedSecret "SharedPair2026"
Get-DhcpServerv4Failover | Select-Object Name, Mode, PartnerServer, State
```

**Expected result:** a load-balance failover relationship exists and both
servers can lease the scope — failover removes the single-server outage risk.

**Negative test:** create failover with mismatched shared secrets; the
relationship fails to establish — both partners must share the secret.

**Cleanup:** `Remove-DhcpServerv4Failover -Name "LAN-FO"`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

DNS underpins Active Directory through SRV locator records; AD-integrated
zones give secure, multi-master replication, with forwarders, conditional
forwarders, and DNSSEC for resolution and integrity. DHCP leases
configuration through scopes, options, reservations, policies, and
failover, and can update DNS on clients' behalf. IPAM centralizes and audits
it all. Health checks (`Resolve-DnsName` SRV, `nltest`, scope statistics)
catch the failures that break logon and connectivity.

- [ ] I can manage AD-integrated DNS zones, records, and forwarders.
- [ ] I can explain and verify DC locator records.
- [ ] I can deploy DHCP with options, authorization, and failover.
- [ ] I can describe safe DHCP-to-DNS dynamic updates and IPAM's role.
- [ ] I completed Labs 6.1–6.4 including each negative test.
