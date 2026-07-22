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

vSRX pair plus a vJunos switch: three zones (TRUST, DMZ, UNTRUST),
policies with a logged final deny, interface source NAT outbound, and
destination NAT publishing one DMZ service; a route-based IPsec tunnel
to a second vSRX with OSPF over st0. Lock yourself out once by
omitting host-inbound SSH — recover via console and codify the lesson
— then break phase 2 with a proposal mismatch and prove the signature
before repairing.

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
