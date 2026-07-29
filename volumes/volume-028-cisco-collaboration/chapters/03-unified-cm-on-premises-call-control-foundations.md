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

This chapter carries a topic-level walkthrough lab for **every objective in
Domain 3 (On-Premises Call Control) of the CLCOR 350-801 v2.0 exam guide** —
mapped in the volume README's coverage tables. Labs use the Unified CM
administration/CLI, the Dialed Number Analyzer, and the AXL/USM API. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.7** — a Unified CM cluster at `$CUCM` with
a working dial plan (partitions, CSS, route patterns), an LDAP directory for
sync, a Unity Connection server, and AXL enabled with an application user in
`$AXL`. **Cost:** none beyond lab resources.

### Lab 3.1 — Describe the call routing process in Cisco UCM (Objective 3.1)

**Objective:** Trace digit analysis for a dialed number end to end.

```text
! Cisco Unified CM Dialed Number Analyzer (DNA): analyze a called number
admin:run sql select rp.name as pattern, p.name as partition from routepattern rp \
  inner join numplan np on rp.fknumplan=np.pkid inner join routepartition p on np.fkroutepartition=p.pkid
```

**Expected result:** the matching route pattern and its partition — UCM routing
is closest-match digit analysis scoped by the calling device's **CSS** against
**partitions**; DNA shows the exact pattern selected and the resulting route
list/gateway.

**Negative test:** a device whose CSS omits the pattern's partition cannot reach
it even though the pattern exists — reachability is CSS∩partition, not the
pattern alone.

**Cleanup:** none (read-only).

### Lab 3.2 — Implement toll fraud prevention in Cisco UCM (Objective 3.2)

**Objective:** Verify the controls that block unauthorized external calling.

```text
admin:run sql select name,tkservice from service where name like '%Transfer%'
! Check: block off-net to off-net transfer, FAC/CMC, time-of-day, partition scoping
admin:run sql select name from routepartition
```

**Expected result:** the toll-fraud controls in force — blocking off-net-to-
off-net transfers/conferences, Forced Authorization Codes on toll patterns,
time-of-day routing, and partition/CSS scoping so only authorized devices reach
toll patterns.

**Negative test:** leave "Block OffNet to OffNet Transfer" at the permissive
default; an external caller can transfer to another external number, the classic
toll-fraud vector — the control is what closes it.

**Cleanup:** revert any test service-parameter change.

### Lab 3.3 — Configure globalized call routing in Cisco UCM (Objective 3.3)

**Objective:** Confirm E.164 normalization to and from a global dial plan.

```text
admin:run sql select dnorpattern,e164mask from device where e164mask is not null limit 5
! Verify: called-party transforms to +E.164, calling-party globalization, localization at egress
```

**Expected result:** DID-to-+E.164 masks and transformation patterns —
globalized routing stores and routes numbers as `+E.164` internally and
localizes only at the gateway egress, so a multi-site dial plan scales without
overlapping patterns.

**Negative test:** mix localized (non-+E.164) and globalized patterns in one
cluster; inbound caller-ID and callback break — globalization must be consistent
end to end.

**Cleanup:** none (read-only).

### Lab 3.4 — Troubleshoot dial-plan issues with monitoring tools (Objective 3.4)

**Objective:** Use DNA and traces to find a misrouted call.

```text
! Dialed Number Analyzer: run the failing dialed string from the source device
admin:file tail activelog /cm/trace/ccm/sdi/  ! digit analysis in SDL/SDI trace
```

**Expected result:** the digit-analysis result showing the pattern matched (or
"no match") — a call routed to the wrong gateway traces to an unexpected
closest-match pattern or a CSS scoping the wrong partition; DNA makes the match
explicit.

**Negative test:** blame the gateway for a call that DNA shows matching a more
specific wrong pattern — the dial plan, not the gateway, selected the route.

**Cleanup:** none (read-only).

### Lab 3.5 — Describe Cisco USM APIs (Objective 3.5)

**Objective:** Query UCM through the AXL (USM) SOAP API.

```bash
curl -sk -u $AXL_USER:$AXL_PW -H 'Content-Type: text/xml' \
  -H 'SOAPAction: CUCM:DB ver=14.0 getUser' https://$CUCM:8443/axl/ \
  -d '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/14.0"><soapenv:Body><ns:listPhone><searchCriteria><name>SEP%</name></searchCriteria><returnedTags><name/><description/></returnedTags></ns:listPhone></soapenv:Body></soapenv:Envelope>' | xmllint --format - | head
```

**Expected result:** the phones returned as XML — AXL is UCM's provisioning SOAP
API (the "USM"/administrative XML layer) that automates moves/adds/changes and
config queries programmatically.

**Negative test:** call AXL with an app user lacking the "Standard AXL API
Access" role; UCM returns `403` — AXL access is role-gated.

**Cleanup:** none (read-only `list` call).

### Lab 3.6 — Configure Cisco Unity Connection (Objective 3.6)

**Objective:** Verify a Unity Connection voicemail user and UCM integration.

```text
! On Unity Connection CLI:
run cuc dbquery unitydirdb select alias,dtmfaccessid from vw_mailbox limit 5
show cuc jetty status
! Confirm the SIP/SCCP voicemail port group and MWI to UCM
```

**Expected result:** mailbox users with their extensions and the messaging
ports — Unity Connection provides voicemail; UCM integrates via a SIP trunk (or
ports) with a voicemail pilot, profile, and MWI on/off.

**Negative test:** a mailbox with no UCM voicemail-profile association gets no
MWI and calls do not forward to voicemail — the UCM-side integration objects are
required, not just the mailbox.

**Cleanup:** remove the test mailbox if one was created.

### Lab 3.7 — Configure on-premises user management (Objective 3.7)

**Objective:** Confirm LDAP directory sync and end-user provisioning.

```text
admin:run sql select name,scheduleunit,nextexectime from directorypluginconfig
admin:run sql select count(*) from enduser where fkdirectorypluginconfig is not null
utils ldap status 2>/dev/null || show packages active | grep -i dirsync
```

**Expected result:** the LDAP sync agreement, its schedule, and the count of
synced users — on-prem user management imports users from LDAP (read-only) and
optionally authenticates against LDAP, with feature/line association done in
UCM.

**Negative test:** a user synced from LDAP cannot have their core fields edited
in UCM (they are LDAP-owned); editing must happen in the directory — the sync
model dictates the source of truth.

**Cleanup:** none (read-only).

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
