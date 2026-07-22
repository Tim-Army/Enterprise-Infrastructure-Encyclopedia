# Chapter 03: Unified CM On-Premises Call Control Foundations

## Learning Objectives

- Operate the CUCM cluster: publisher/subscriber roles, database
  replication, and the services that constitute call processing
- Integrate users from LDAP and understand synchronization and
  authentication boundaries
- Provision devices: phones, soft clients, and device pools with
  their cascading defaults
- Configure regions, locations, and codec policy as the estate's
  bandwidth governance
- Build SIP trunks between systems and validate registration and
  intra-cluster calling

## Theory and Architecture

### The cluster as a system

CUCM is a distributed database with a call-processing brain. The
**publisher** owns writes; **subscribers** replicate reads and run
services; **IDS replication** keeps them coherent (state 2 in
`utils dbreplication runtimestate` is the number you memorize).
Services that matter daily: **Cisco CallManager** (call processing),
**TFTP** (device configuration files), **CTIManager** (application
control of devices), **AXL Web Service** (the provisioning API), plus
Serviceability's trace collection. Activation is deliberate
(Serviceability > Service Activation) — a node does what you
activated, nothing more.

Device registration distributes by **Unified CM Groups** (ordered
server lists) referenced by **device pools** — the mechanism behind
Chapter 01's availability design. Registration follows the group
order; failover walks it.

### Users: LDAP as the source of truth

Enterprises synchronize users from Active Directory/LDAP: **LDAP
synchronization** imports identities on a schedule and marks them
LDAP-managed (immutable locally — the exam's favorite trap);
**LDAP authentication** delegates password checks to the directory
while CUCM keeps authorization. What stays local: application users
(service accounts for integrations), and PINs. Design consequence:
user lifecycle (joiner/mover/leaver) becomes a directory process,
which is exactly where it belongs.

### Devices and the cascade of defaults

A phone is a device record: identity (MAC or activation), **device
pool** (region, location, CM group, date/time, SRST reference),
phone security profile, and lines (DNs with their own partitions —
Chapter 04). The design skill is the cascade: set behavior at the
**device pool** and **common device configuration** level so that
site-wide intent lives in a handful of objects, and per-device
overrides are exceptions with reasons. Estates that configure phones
individually are estates that cannot change anything safely.

### Regions and locations: codec and bandwidth governance

**Regions** decide the maximum codec between pairs of device groups
(wideband within a site, efficient codecs across the WAN — the
Chapter 02 policy, implemented). **Locations** implement
call admission control: each location has bandwidth pools; calls
that would exceed them are denied or rerouted (AAR) rather than
degrading everyone already talking. Enhanced Locations CAC models the
WAN as a topology of links and weights. The principle CLCOR tests:
**admission control is a design feature, not an error** — a busy
signal is better than ten calls at MOS 2.

### Trunks

**SIP trunks** connect CUCM to CUBE, to Unity Connection, IM&P, CMS,
Expressway, and to other clusters — each a device with its own
security profile, SIP profile (timers, options ping, early media
behavior), and destination addressing. OPTIONS ping keeps trunk
state honest: a trunk that answers OPTIONS is up; one that does not
is out of rotation before a user finds it.

## Design Considerations

- **Device pool granularity = site granularity**: one pool per
  site/failover-domain is the norm; more granular only with a reason.
- **Region matrix discipline**: define region relationships by
  site-class (campus↔campus, campus↔branch), not per-site pairs, or
  the matrix grows quadratically.
- **CAC that matches the WAN**: locations bandwidth must reflect the
  QoS voice queue actually provisioned (Chapter 08) — CAC lying about
  the network is worse than no CAC.
- **Trunk topology**: hub clusters and SME designs exist for
  multi-cluster estates; for this volume's scale, direct trunks with
  OPTIONS ping and clear routing responsibilities suffice.

## Implementation and Automation

Foundational build, in dependency order (UI paths named once,
AXL-automatable always):

```text
1. Enterprise/Service Parameters: cluster defaults (auto-registration
   off in production; on, fenced, in the lab)
2. Unified CM Group: PUB-SUB order per failover domain
3. Date/Time Group, Region (G722/Opus intra-site, G.711 inter-site
   for the lab), Location (bandwidth per branch)
4. Device Pool: assembles 2-3
5. LDAP: System > LDAP Directory (sync agreement), LDAP
   Authentication (bind for auth)
6. Phone Security Profile (TLS where the lab CA allows)
7. Device + Line: register the Chapter 02 endpoints properly
8. SIP Trunk: to Unity Connection (Chapter 06 will use it), OPTIONS
   ping enabled
```

The AXL expression of step 7 — the shape Chapter 09 automates in
bulk:

```xml
<ns:addPhone>
  <phone>
    <name>SEP001122334455</name>
    <product>Cisco 8841</product>
    <class>Phone</class>
    <protocol>SIP</protocol>
    <devicePoolName>DP-HQ</devicePoolName>
    <securityProfileName>Universal Device Template - Model-independent Security Profile</securityProfileName>
    <lines><line><index>1</index>
      <dirn><pattern>2001</pattern>
        <routePartitionName>PT-INTERNAL</routePartitionName></dirn>
    </line></lines>
  </phone>
</ns:addPhone>
```

Verification set:

```text
utils dbreplication runtimestate          # 2 everywhere, always
show risdb query phone                    # registration inventory
# Trunk state: Device > Trunk shows OPTIONS status; or
show perf query class "Cisco SIP Trunk" 
```

## Validation and Troubleshooting

Registration failures walk Chapter 01's chain, then the CUCM layers:
device record exists (name matches identity), security profile
matches what the device offers (TLS vs TCP mismatches read as
mysterious timeouts), CM group reachable, and licensing headroom.
Replication faults (state ≠ 2) explain "it works on some phones":
fix replication before chasing ghosts —
`utils dbreplication repair` and patience, in that order. LDAP sync
surprises: users vanishing on sync because the filter or search base
changed — the audit log names the sync agreement; treat directory
changes as change-controlled events for collaboration too. Trunk
issues: OPTIONS down means transport/TLS/trust, not dial plan —
prove reachability and certificates before touching routing.

## Security and Best Practices

- Mixed-mode cluster (CTL/tokenless) enables TLS/SRTP for endpoints
  — plan it early; retrofitting security modes across thousands of
  devices is a project.
- Application users per integration, least-privilege access control
  groups, and no human use of service accounts.
- Auto-registration: off in production, or fenced to a quarantine
  partition/pool when used for provisioning waves.
- Change discipline: BAT/AXL bulk changes rehearsed on the lab
  cluster first — Chapter 09 formalizes the pipeline.

## References and Knowledge Checks

- CLCOR 350-801 v2.0 domain 3 (On-Premises Call Control, 30%)
- Cisco Unified CM administration and system guides; SRND call
  control chapters
- DevNet AXL schema reference

Knowledge checks:

1. Which writes does a subscriber accept when the publisher is down,
   and what does that imply for provisioning during maintenance?
2. A user object is grayed-out/immutable in CUCM. Why, and where is
   the change made?
3. Two sites get G.729 between them when policy says Opus. Which two
   objects do you inspect, in which order?
4. Why is OPTIONS ping on trunks a user-experience feature, not just
   monitoring?

## Hands-On Lab

On the Chapter 01 estate: activate services deliberately (document
which node runs what); build the dependency chain (groups, region
matrix by site-class, locations with honest bandwidth, device
pools); integrate LDAP sync + authentication against the lab
directory; re-home Chapter 02's endpoints into proper pools with TLS
security profiles; and build the OPTIONS-pinged trunk to Unity
Connection. Prove: registration walkover by rebooting the primary
subscriber mid-call (call survives, re-registration follows the
group), CAC denial by setting a location to one call's bandwidth and
placing two, and an AXL addPhone that registers a third endpoint.

## Lab Verification

Verification means failover behaved per the CM group order, CAC
denied the second call by design, and the AXL-provisioned phone
registered without UI touches. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CUCM is a replicated system whose defaults cascade: clusters and
groups give availability, LDAP gives identity, device pools give
manageable sites, regions and locations govern codecs and bandwidth,
and trunks federate the estate. Build the foundations so Chapter 04
can spend its entire budget on the dial plan — the craft at the
center of the track.

- [ ] Replication is 2 everywhere and I know what breaks when it
      is not
- [ ] My defaults cascade; per-device exceptions have reasons
- [ ] CAC denied by design in my lab and I can defend that behavior
- [ ] AXL provisioned a device end to end
