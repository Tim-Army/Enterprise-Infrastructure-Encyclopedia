# Chapter 04: Juniper Security — SRX from JNCIA-SEC to JNCIP-SEC

## Learning Objectives

- Configure the SRX flow model: zones, security policies, and the
  session table that changes how you troubleshoot
- Deploy NAT in its Junos forms — source, destination, static — and
  IPsec VPNs site-to-site
- Layer on advanced services: AppSecure, IDP, unified policies, and
  where ATP Cloud fits
- Map the three written rungs — JNCIA-SEC (JN0-232), JNCIS-SEC
  (JN0-336), JNCIP-SEC (JN0-637) — to this material

## Theory and Architecture

### The track in one sentence

The Security track certifies the SRX family — branch to data-center
firewalls plus vSRX — and the operational model built around **zones**
and **flow processing**. JNCIA-SEC (JN0-232) establishes zones,
policies, NAT, and IPsec basics; JNCIS-SEC (JN0-336, written to Junos
OS 24.4) adds AppSecure, IDP, HA clustering, and unified policies;
JNCIP-SEC (JN0-637, Junos 22.2) goes to advanced VPNs (ADVPN,
Auto-VPN), advanced NAT, and troubleshooting at depth. All are
90-minute, 65-question exams; JNCIA-SEC has no prerequisite (codes and
versions verified against Juniper's track pages, 22 July 2026).

### Zones and flow: the SRX mental model

Interfaces join **security zones**; policy is written zone-pair by
zone-pair (`from-zone TRUST to-zone UNTRUST`) and evaluated top-down
for the **first packet of a session** — after which the session table
forwards both directions statelessly fast. That one fact reorders
troubleshooting: a policy change does not touch established sessions,
return traffic does not need a reverse policy, and `show security flow
session` outranks the policy view when "it should work" but does not.
Host-inbound traffic (SSH, ping to the box) is separately gated per
zone or per interface — the most common lab lockout in the track.

### Services above the flow

**AppSecure** identifies applications regardless of port (AppID) and
lets policy match them (AppFW, unified policies with dynamic
applications); **IDP** brings signature inspection inline; **ATP
Cloud** adds verdicts from sandboxing feeding SecIntel feeds the SRX
enforces. Chassis clusters pair two SRX into one logical firewall —
redundancy groups, reth interfaces, and the control/fabric links whose
health is half of HA troubleshooting.

## Design Considerations

- **Zone granularity** is policy granularity: a flat TRUST hides
  everything; per-function zones (USERS, SERVERS, MGMT, DMZ) make the
  policy table legible and the exams' scenarios tractable
- **Unified policies vs. AppFW:** new designs write dynamic
  applications directly into security policies; legacy AppFW rulesets
  still appear in JNCIS-SEC scenarios — know both directions
- **Cluster or not:** branch SRX often rides single-box with
  commit-confirmed discipline; anything customer-facing pairs up.
  Reth interfaces demand identical member wiring — design the cabling
  before the config

## Implementation and Automation

```text
# Zones, one policy pair, source NAT to the egress interface
set security zones security-zone TRUST interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh
set security zones security-zone TRUST interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
set security zones security-zone UNTRUST interfaces ge-0/0/0.0

set security policies from-zone TRUST to-zone UNTRUST policy OUT match source-address any destination-address any application any
set security policies from-zone TRUST to-zone UNTRUST policy OUT then permit

set security nat source rule-set S2U from zone TRUST
set security nat source rule-set S2U to zone UNTRUST
set security nat source rule-set S2U rule R1 match source-address 10.30.0.0/16
set security nat source rule-set S2U rule R1 then source-nat interface

# Site-to-site IPsec, route-based (st0)
set security ike proposal P1 authentication-method pre-shared-keys dh-group group20 authentication-algorithm sha-256 encryption-algorithm aes-256-cbc
set security ike policy IKE-POL proposals P1
set security ike gateway GW-B ike-policy IKE-POL address 203.0.113.2 external-interface ge-0/0/0.0
set security ipsec vpn TO-B ike gateway GW-B
set security ipsec vpn TO-B bind-interface st0.0
set interfaces st0 unit 0 family inet address 172.31.0.1/30
```

## Validation and Troubleshooting

- `show security flow session destination-prefix <ip>` — the session
  is the truth; no session, check policy; session but no reply, check
  the return path
- `show security policies hit-count` — the rule you thought matched
  versus the one that did
- `show security ike security-associations` then `ipsec
  security-associations` — phase order is diagnosis order
- `show security nat source rule all` translation counters — NAT rules
  that never increment are ordering bugs
- Flow traceoptions with a tight packet-filter — the last resort that
  answers everything, used surgically

## Security and Best Practices

- Explicit inter-zone deny-and-log final policies; silent drops hide
  incidents
- Host-inbound-traffic minimal per zone; management via a dedicated
  zone/VRF, never UNTRUST
- IKEv2 with group20/sha-256/aes-256 floors; certificate
  authentication where scale permits
- Screens (SYN flood, IP sweep) on internet-facing zones — the SRX
  DoS toolkit the associate exam names and real edges need

## References and Knowledge Checks

- JNCIA-SEC (JN0-232), JNCIS-SEC (JN0-336), JNCIP-SEC (JN0-637)
  objectives on Juniper's certification pages
- Junos Security user guides: flow, NAT, IPsec, AppSecure, chassis
  cluster; *Day One: SRX Series Up and Running*

Knowledge checks:

1. A policy permitting the traffic exists, yet `show security flow
   session` shows nothing for the flow. Give two SRX-specific causes
   that are not routing.
2. Why does route-based VPN with st0 interfaces scale policy better
   than policy-based VPN on Junos?
3. In a chassis cluster, which failures move a redundancy group and
   which merely degrade it? Name the monitoring knobs involved.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every exam objective of
the JNCIS-SEC (JN0-336) exam** — the Security specialist (SRX, written to Junos OS
24.4) — mapped in the volume README's coverage tables. Labs use the Junos CLI on
SRX Series firewalls. Each ends **`**Lab verified by:** *pending*`** until a human
runs it.

**Shared prerequisites for Labs 4.1–4.7** — two SRX firewalls (for the cluster
lab), configured security zones and policies, a peer for IPsec, and an ATP Cloud /
Security Director realm for those labs. **Cost:** none beyond lab resources.

### Lab 4.1 — Intrusion Detection and Prevention (Objective: IDP)

**Objective:** Apply an IDP policy and confirm inspection.

```text
configure
set security idp idp-policy LAB-IDP rulebase-ips rule r1 match application default
set security idp idp-policy LAB-IDP rulebase-ips rule r1 then action drop-packet
set security policies from-zone trust to-zone untrust policy P1 then permit application-services idp-policy LAB-IDP
commit and-quit
show security idp status
show security idp attack table
```

**Expected result:** the IDP engine running and attack counters — SRX **IDP**
inspects permitted traffic against a signature database, matching an IPS rulebase
and taking action (drop/close); the database must be downloaded and the policy
attached to a security policy.

**Negative test:** attach an IDP policy without downloading the signature database;
`show security idp status` shows no policy loaded — the attack database is required.

**Cleanup:** `configure; delete security idp; delete security policies from-zone
trust to-zone untrust policy P1 then permit application-services; commit`.

### Lab 4.2 — IPsec VPN (Objective: IPsec VPN)

**Objective:** Build a route-based site-to-site IPsec VPN and verify.

```text
configure
set security ike proposal P1 authentication-method pre-shared-keys dh-group group14 encryption-algorithm aes-256-cbc
set security ike policy POL proposals P1
set security ike gateway GW ike-policy POL address 198.51.100.2 external-interface ge-0/0/0.0
set security ipsec vpn VPN bind-interface st0.0
set security ipsec vpn VPN ike gateway GW
commit and-quit
show security ike security-associations
show security ipsec security-associations
```

**Expected result:** the IKE (phase 1) and IPsec (phase 2) SAs up — a route-based
IPsec VPN establishes IKE, negotiates IPsec SAs, and binds to a secure tunnel
interface (`st0`); traffic routed into `st0` is encrypted, and Juniper Secure Connect
extends this to remote clients.

**Negative test:** mismatched phase-1 proposals (DH group/encryption) between peers
leave IKE in negotiation; `show security ike security-associations` shows no SA —
proposals must match.

**Cleanup:** `configure; delete security ike; delete security ipsec; commit`.

### Lab 4.3 — Juniper ATP Cloud (Objective: Juniper Advanced Threat Prevention Cloud)

**Objective:** Enroll the SRX and verify the ATP Cloud security feeds.

```text
show services advanced-anti-malware status
show services advanced-anti-malware policy
show security dynamic-address category-name CC 2>/dev/null | match "address|feed"
```

**Expected result:** the SRX enrolled with ATP Cloud and its feeds — **ATP Cloud**
sends suspicious files to a cloud sandbox and feeds the SRX C&C/infected-host/
GeoIP/custom feeds for blocking, with Encrypted Traffic Insights, DNS/IoT security,
and adaptive threat profiling.

**Negative test:** a policy referencing ATP Cloud while the SRX is not enrolled
(no realm) does nothing; `show services advanced-anti-malware status` shows not
connected — enrollment to the cloud realm is required.

**Cleanup:** none (read-only).

### Lab 4.4 — High Availability Clustering (Objective: HA Clustering)

**Objective:** Verify an SRX chassis cluster's redundancy state.

```text
show chassis cluster status
show chassis cluster interfaces
show chassis cluster statistics
```

**Expected result:** the redundancy groups with a primary/secondary node and the
fabric/control links — an SRX **chassis cluster** joins two nodes into one logical
firewall: RG0 (control plane) and RG1+ (data plane) fail over independently, with
RTO state (sessions) synchronized over the fabric link so failover is stateful.

**Negative test:** a cluster whose control or fabric link is down splits (both nodes
primary), risking a session-table conflict — the control and fabric links are
essential to the cluster.

**Cleanup:** none (read-only).

### Lab 4.5 — Identity-Aware Security Policies (Objective: Identity-Aware Security Policies)

**Objective:** Verify user-identity-based policy via JIMS.

```text
show services user-identification active-directory-access active-directory-authentication-table all
show security match-policies from-zone trust to-zone untrust source-ip 10.10.10.50 destination-ip 8.8.8.8 protocol tcp source-port 1024 destination-port 443
```

**Expected result:** the user-to-IP mappings and the matched identity-aware policy —
**JIMS** (Juniper Identity Management Service) feeds the SRX user/group-to-IP
mappings from AD, so security policies match on **user identity** (source-identity)
rather than just IP.

**Negative test:** a policy matching a user whose IP-to-user mapping JIMS has not
learned falls through to the non-identity policy — the mapping must exist for
identity matching.

**Cleanup:** none (read-only).

### Lab 4.6 — SSL Proxy (Objective: SSL Proxy)

**Objective:** Verify SSL forward-proxy decryption for inspection.

```text
show services ssl proxy statistics
show services ssl proxy counters
show security policies detail | match "ssl-proxy"
```

**Expected result:** the SSL proxy session counters — **SSL forward proxy** lets the
SRX decrypt outbound TLS (using a CA the clients trust) so IDP/content security can
inspect the plaintext, then re-encrypts; server protection decrypts inbound TLS to a
protected server.

**Negative test:** clients that do not trust the proxy CA get certificate warnings on
every HTTPS site — the proxy CA must be distributed to clients for forward proxy to
work cleanly.

**Cleanup:** none (read-only).

### Lab 4.7 — Security Director (Objective: Security Director)

**Objective:** Read the SRX's management by Junos Space Security Director.

```text
show system services outbound-ssh
show configuration system services netconf
```

**Expected result:** the management channel to Space — **Security Director**
(Junos Space) centrally manages SRX policy: it onboards devices (via NETCONF/
outbound-SSH), authors and pushes security policies, NAT, and VPNs at scale, and
reports on them, so many firewalls share one policy source of truth.

**Negative test:** an SRX with no NETCONF/outbound-SSH to Space cannot be managed by
Security Director; policy pushes fail — the management channel is the prerequisite.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the session table shows each permitted flow with
the expected NAT translation, the published DMZ service answers from
UNTRUST, OSPF adjacency runs over the tunnel, and both induced
failures (host-inbound lockout, phase-2 mismatch) were evidenced and
repaired.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Zones, policies, and flow-first troubleshooting internalized
- [ ] Source/destination NAT and route-based IPsec working
- [ ] AppSecure/IDP/cluster concepts mapped to JNCIS/JNCIP scope
- [ ] All three exam codes and versions recorded from primary source
- [ ] Lab lockout and VPN failure evidenced and repaired
