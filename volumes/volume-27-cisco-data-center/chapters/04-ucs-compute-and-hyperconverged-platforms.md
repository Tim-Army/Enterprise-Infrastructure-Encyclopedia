# Chapter 04: UCS Compute and Hyperconverged Platforms

## Learning Objectives

- Describe the UCS building blocks — fabric interconnects, B-, C-, and
  X-Series servers, and the unified fabric that connects them
- Explain the service profile abstraction and why stateless compute
  changed server operations
- Distinguish UCS Manager and Intersight operating models and select
  appropriately
- Configure pools, policies, templates, and profiles in the order that
  scales
- Validate compute health, firmware alignment, and boot behavior, and
  troubleshoot the common failure classes

## Theory and Architecture

### The UCS idea: servers as rendered state

Before UCS, a server's identity — MAC addresses, WWNs, UUID, boot
order, firmware, BIOS settings — lived in hardware, so replacing a
failed blade meant rebuilding identity by hand across a dozen screens
and the SAN team's zoning. UCS moved identity into a **service
profile**: a document that renders onto any compatible blade. The
blade becomes anonymous capacity; the profile is the server. Swap
hardware, re-associate the profile, and the "same server" boots — same
MACs, same WWNs, same boot LUN.

This is the compute mirror of Chapter 03's policy inversion, and the
exam tests it the same way: know the abstraction's parts and the order
they compose.

### The hardware and the unified fabric

- **Fabric interconnects (FIs)** — the pair of switches every UCS
  domain hangs from; they carry Ethernet and Fibre Channel on one
  wire (FCoE internally), host UCS Manager, and uplink to the LAN and
  SAN. End-host mode is the default and the right answer nearly
  always: the FI looks like a giant NIC to the LAN, not a switch, so
  no spanning tree on the uplinks.
- **B-Series** blades in the 5108 chassis, connected through IOMs
  (fabric extenders — no local switching; everything goes up to the
  FIs). **C-Series** rack servers, integrated into the domain or run
  standalone through the CIMC. **X-Series** — the current modular
  chassis, designed for Intersight-first management and generational
  upgrades of compute, storage, and fabric independently.
- **VIC adapters** present virtual NICs and HBAs to the OS in whatever
  number and order the profile dictates — the mechanism that makes
  identity abstraction real.

### Two management planes

**UCS Manager** runs on the FIs, scopes to one domain, and speaks the
XML API automation generations were built on. **Intersight** is the
SaaS successor: domains claimed to the cloud (or to a Private Virtual
Appliance where data cannot leave), profiles and policies modeled
centrally, firmware orchestrated fleet-wide, with proactive TAC
integration. Cisco's direction is Intersight — new X-Series features
land there — but estates run mixed for years, so DCCOR expects
literacy in both, and the design decision is Chapter's-end material:
per-domain autonomy versus fleet consistency.

### Hyperconverged, briefly and honestly

HyperFlex was Cisco's HCI answer — UCS compute plus a distributed
log-structured filesystem, managed through Intersight. Cisco announced
its end-of-sale in 2024 in favor of Nutanix partnerships on UCS. The
blueprint still names compute broadly; what endures for the exam and
the field is the HCI *pattern* — storage collapsed into the compute
tier, scaled by adding nodes, dependent on the network for every
write — which is exactly why HCI clusters care about the Chapter 02
fabric's latency and MTU discipline.

## Design Considerations

- **Pools before policies before templates before profiles.** Define
  MAC/WWN/UUID pools with room to grow and a naming scheme that
  encodes site and fabric (A-side MACs ending in even octets is the
  kind of convention that saves troubleshooting hours later).
- **Updating templates cut both ways**: bind profiles to an updating
  template and a template change rolls to every server — which is
  either fleet consistency or a fleet-wide outage, depending entirely
  on your maintenance-policy settings. Set user-acknowledged
  maintenance policies so renders wait for a window.
- **Firmware as policy**: host firmware packages pin versions per
  profile, which is how you stage upgrades server-by-server instead of
  big-bang.
- **Choose Intersight for new estates** unless data-locality rules
  forbid SaaS; then the Private Virtual Appliance exists precisely for
  you.

## Implementation and Automation

The composition order, whether clicked or scripted:

```text
1. Pools:      MAC (fabric A / fabric B), WWNN, WWPN-A/B, UUID, mgmt IP
2. Policies:   boot (SAN boot first — it is what makes statelessness
               matter), BIOS, host firmware package, maintenance
               (user-ack), local disk, power
3. vNIC/vHBA templates: fabric side, VLANs/VSANs, MTU (9000 for
               storage and vMotion vNICs), pin groups if used
4. Service profile template: assembles all of the above
5. Profiles:   instantiated from the template, associated to blades
```

Intersight drives the same composition through Server Profiles and
attached policies; the API is first-class:

```bash
# Intersight API: list claimed servers and their firmware (abbrev.)
GET /api/v1/compute/PhysicalSummaries
GET /api/v1/firmware/RunningFirmwares?$filter=Component eq 'system'
```

```text
# UCS Manager CLI spot checks
show service-profile association     # which blade renders which profile
show server status                   # discovery / association state
show firmware system                 # FI, IOM, adapter alignment
```

## Validation and Troubleshooting

Work the association pipeline: discovery (blade seen, inventory
complete), qualification (does the blade meet the profile's
requirements), association (FSM renders identity — watch the FSM tab,
it names the failing step), boot (does the vHBA see the boot LUN).
The recurring failure classes: **association stuck in FSM** on a
firmware step (mismatched host firmware package versus catalog);
**SAN boot failing** with a healthy profile (WWPN not zoned or LUN not
masked — coordinate with Chapter 05's fabric, and check
`show flogi database` on the MDS side for the login); **vNIC order
surprises** after OS install (set consistent device naming and
placement policy explicitly); and **firmware drift** across a domain
(auditable in one Intersight view — use it before it becomes an
incident).

## Security and Best Practices

- FIs and CIMCs on the out-of-band management network; Intersight
  device connectors are outbound-only TLS, which is the argument that
  usually satisfies the security review.
- RBAC with locales and organizations in UCS Manager / Intersight —
  server admins do not need LAN-tab rights; the separation prevents
  the classic "compute change broke the uplinks" incident.
- KVM and CIMC sessions logged and behind AAA (TACACS+/LDAP);
  default local credentials rotated at deployment per the scope
  boundaries this encyclopedia documents — factory defaults are
  reference data, not production state.

## References and Knowledge Checks

- Cisco UCS configuration fundamentals and Intersight documentation
- DCCOR 350-601 v1.2 exam topics, Compute domain (25%)
- UCS Platform Emulator and Intersight free tier for practice

Knowledge checks:

1. A blade fails at 03:00. Narrate the recovery with service profiles,
   and name what does *not* need to be touched (SAN zoning among it).
2. Why is end-host mode the default on FI uplinks, and what problem
   returns if you flip to switching mode carelessly?
3. An updating template's VLAN change triggers immediate reboots
   across a domain. Which policy was mis-set, and to what?
4. Where does Intersight place data-locality-constrained estates?

## Hands-On Lab

Using the UCS Platform Emulator (and the Intersight free tier where
available): build the full composition — pools with fabric-encoded
naming, SAN-boot policy, user-ack maintenance policy, vNIC/vHBA
templates with jumbo MTU on storage vNICs, a service profile template
— and associate two profiles to emulated blades. Demonstrate
statelessness: disassociate a profile and re-associate it to a
different blade, capturing identical identities before and after.
Then break association deliberately with a conflicting host firmware
package and read the FSM failure; repair it. Claim the emulator into
Intersight (where licensing permits) and pull the same inventory via
the API.

## Lab Verification

Verification means both profiles associated, the migration preserved
every identity value, the FSM failure was induced, read, and repaired,
and inventory was retrieved via API. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

UCS made servers stateless: identity lives in profiles, hardware is
capacity, and the unified fabric carries LAN and SAN through one pair
of interconnects. Composition order — pools, policies, templates,
profiles — is both the exam's structure and the operational one, and
the management plane is tilting to Intersight while UCS Manager
literacy remains mandatory. Compute is 25% of DCCOR; this chapter and
Chapter 02 together are half the core exam.

- [ ] I can narrate blade replacement end to end via profiles
- [ ] I know the composition order and why maintenance policy guards it
- [ ] My lab proved identity persistence across hardware
- [ ] I can query the same estate through the Intersight API
