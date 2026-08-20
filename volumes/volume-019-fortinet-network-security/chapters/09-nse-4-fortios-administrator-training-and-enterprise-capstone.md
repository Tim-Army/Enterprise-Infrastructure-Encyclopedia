# Chapter 09: NSE 4 FortiOS Administrator Training and Enterprise Capstone

![Lab flow for this chapter: a full validation checklist across licensing, HA, routing, SD-WAN health, and VPN sessions is recorded as a dated baseline, and a configuration backup exports to external storage. As a negative test, a specific, realistic misconfiguration is introduced without being documented in advance; the resulting symptom is worked through the layered troubleshooting decision tree step by step until the actual root cause is correctly identified without guessing. The fault is corrected and the affected traffic flow confirmed restored, and the original backup is restored as a final validation that recovery returns the device to the exact baseline state.](../../../diagrams/volume-019-fortinet-network-security/chapter-09-capstone-troubleshooting-restore-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: full end-to-end capstone validation with a configuration backup, tested against a deliberately undocumented misconfiguration and restored via backup.*

## Learning Objectives

- Map this volume's chapters to the NSE 4 FortiGate Security and FortiGate
  Infrastructure blueprint domains.
- Deploy FortiGate-VMs from scratch on a hypervisor and activate the
  evaluation license on each unit.
- Build both FGCP high-availability modes side by side — an active-passive
  cluster and an active-active cluster — and explain why HA membership is
  free on the eval while packet forwarding requires a per-member license.
- Describe a complete, redundant enterprise reference architecture
  combining VDOMs, HA, SD-WAN, VPN, and security profiles.
- Back up and restore the FortiOS configuration by every supported
  transport (flash revision, TFTP, FTP, SCP, USB, FortiManager) as part of
  a change-management discipline.
- Apply a structured, layered troubleshooting decision tree spanning
  physical connectivity through application-layer inspection.
- Execute an end-to-end validation pass across a full FortiGate deployment
  and recover from a deliberately introduced misconfiguration.

## Theory and Architecture

### NSE 4 blueprint domains and this volume's mapping

The Fortinet NSE 4 certification validates hands-on FortiOS administrator
competency across two self-paced training courses, **FortiGate Security**
and **FortiGate Infrastructure**. This volume's Chapters 04–08 were
sequenced to build toward exactly this blueprint, and this chapter's
purpose is to make that mapping explicit as a study and review reference,
without reproducing any proprietary exam question or licensed courseware
content:

| NSE 4 course | Blueprint domain area | Covered in |
| --- | --- | --- |
| FortiGate Security | Initial configuration, administrative access, and hardening | [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md) |
| FortiGate Security | Firewall policies, NAT, and firewall objects | Chapters 05–06 |
| FortiGate Security | Authentication (local, LDAP/RADIUS, FSSO) | [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) |
| FortiGate Security | SSL VPN and Zero Trust Access | [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) |
| FortiGate Security | Security profiles (AV, IPS, web filtering, application control) and SSL inspection | [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) |
| FortiGate Security | Logging and monitoring | Chapters 07–08 |
| FortiGate Infrastructure | Routing (static, policy-based, dynamic routing overview) | [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) |
| FortiGate Infrastructure | Virtual Domains (VDOMs) | [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) |
| FortiGate Infrastructure | High availability (FGCP) | [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) |
| FortiGate Infrastructure | SD-WAN | [Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) |
| FortiGate Infrastructure | Diagnostics and troubleshooting | Distributed across Chapters 04–08, consolidated in this chapter |

Always confirm the current official blueprint on Fortinet's NSE Training
Institute site before using this mapping for exam preparation — Fortinet
revises blueprint scope and course content independently of this
repository's release cycle, consistent with the caution in
[CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md).

### FortiOS configuration hierarchy recap

[Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md) introduced the `config`/`edit`/`set`/`next`/`end` model and the
distinction between `global` and per-VDOM configuration scope. A complete
administrator additionally needs fluency in the configuration
**lifecycle**: how a running configuration is captured, compared across
revisions, and restored — the subject this chapter adds to close out the
volume.

- **Running configuration** is the live, in-memory and flash-persisted
  configuration state a device is currently operating under.
- **Configuration backup** (`execute backup config`) exports the running
  configuration as a text file, either locally or centrally through
  FortiManager, functioning as both a disaster-recovery artifact and a
  point-in-time audit record.
- **Revision history** — on a device managed by FortiManager, or using
  FortiGate's own local revision tracking where available — allows an
  administrator to compare two configuration states directly, which is
  the same "diff before apply" discipline [Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) described for
  FortiManager's install preview, extended here to the device's own
  configuration history.

### Reference architecture: a redundant enterprise site

This chapter's capstone architecture combines every subsystem from
Chapters 04–08 into a single, coherent enterprise site design:

- **Two FGCP HA clusters built from scratch** — an **active-passive** pair
  (Cluster A: FGT-AP-1 / FGT-AP-2), the perimeter and internal-segmentation
  enforcement point, and an **active-active** pair (Cluster B: FGT-AA-1 /
  FGT-AA-2) that adds session-level inspection scaling — each eliminating
  the firewall as a single point of failure ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md)). The capstone
  lab deploys and licenses all four VMs before clustering them.
- **VDOM segmentation** separating corporate and DMZ traffic on the same
  physical HA pair, each with its own routing table and policy set
  ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md)).
- **Dual-ISP SD-WAN** providing WAN path redundancy and performance-aware
  routing across both circuits ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)), layered on top of the static
  and policy routing foundation ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md)).
- **Site-to-site IPsec and remote-access SSL VPN/ZTNA** providing secure
  connectivity for branch interconnection and remote users ([Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)).
- **A full FortiGuard security-profile stack with SSL inspection**
  providing threat prevention across every permitted traffic path
  ([Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)).
- **Centralized management and logging** via FortiManager and
  FortiAnalyzer, and REST API/Ansible automation for repeatable, reviewed
  change ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)).

Every layer in this design has redundancy or a defined, deliberate single
point of control: HA removes device-level single point of failure,
SD-WAN removes circuit-level single point of failure, and centralized
management ensures configuration state is reviewable and recoverable
rather than existing only as undocumented, device-local state.

### Active-passive vs. active-active, and the eval-license reality

The capstone builds **both** FGCP modes so their trade-off is concrete rather
than theoretical ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) develops each in depth):

- **Active-passive (A-P)** — one member forwards; the other is a hot standby
  holding a synchronized configuration and (with `session-pickup`) synchronized
  session state, so an established flow survives a device failure. This is the
  default choice for a perimeter/segmentation firewall where deterministic
  behavior and simple troubleshooting matter more than squeezing extra
  inspection throughput out of the pair.
- **Active-active (A-A)** — both members forward; the primary distributes
  sessions to the secondary per a configurable `schedule`. A-A raises aggregate
  inspection throughput across **many** sessions; it is **not** a bandwidth
  multiplier for a single flow, since one connection is pinned to one member.

Two facts about running either mode on evaluation-licensed FortiGate-VMs are
easy to get wrong, so this chapter states them from the volume's own
live-verified evidence rather than from the widely repeated myth that "the eval
license blocks HA":

- **HA membership is not license-gated; forwarding is.** Two eval VMs form a
  fully working, config-synced, failover-capable cluster
  ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Labs 5.6–5.7). But an **unlicensed** member joins, syncs,
  and shows a healthy heartbeat while forwarding **zero** transit packets — in
  active-active with a `leastconnection` schedule it silently blackholes its
  entire share. Every member you intend to carry traffic must read
  `License Status: Valid`.
- **The three-interface cap forces a shared-interface heartbeat.** An eval VM
  never instantiates a fourth vNIC, so there is no port to dedicate to
  heartbeat; set an existing pair of data interfaces as heartbeat devices
  (`set hbdev "port2" 50 "port3" 50`). A licensed unit lifts the cap and
  restores a dedicated heartbeat link. Firmware build must match exactly
  between members, and a hypervisor hard-reset corrupts the config partition —
  reboot only with `execute reboot`.

Because both clusters share one broadcast domain in the lab, they must carry
**distinct HA group IDs** (`11` for Cluster A, `22` for Cluster B) or their
heartbeats collide.

## Design Considerations

- **Full reference architecture walk-through.** For a fictitious
  enterprise ("NSE Lab Enterprises") with one headquarters site and two
  branch offices: HQ runs the HA pair with dual-ISP SD-WAN and VDOM
  segmentation; branches run a single FortiGate (or a smaller HA pair
  where budget allows) with site-to-site IPsec back to HQ and their own
  local SD-WAN for direct internet breakout of latency-sensitive SaaS
  traffic rather than backhauling everything through HQ. This mirrors the
  hub-and-spoke vs. direct-internet-breakout trade-off discussed for
  SASE architectures in [Volume XVI](../../volume-016-palo-alto-networks-security/README.md), applied to an on-premises SD-WAN
  design instead of a cloud-delivered security service.
- **Redundancy at every layer, deliberately, not by accident.** Review
  the architecture layer by layer and confirm each has an explicit
  redundancy decision (HA for device failure, dual circuits for WAN
  failure, dual heartbeat links for split-brain avoidance) rather than
  assuming redundancy exists because individual pieces were each
  configured correctly in isolation.
- **Build order and per-member licensing.** Deploy and license every unit
  *before* clustering, not after. HA membership forms on an unlicensed
  member and looks healthy, but that member forwards nothing — so a
  cluster that appears "up" can silently blackhole traffic until each
  member is individually licensed. Establish `License Status: Valid`
  on all four VMs as step one (Lab 9.1), then build the clusters
  (Labs 9.2–9.3), then layer configuration on top (Labs 9.4–9.7).
- **Change management and backup strategy.** Pair FortiManager's
  policy-package install workflow ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)) with a scheduled
  configuration backup cadence independent of FortiManager (a periodic
  `execute backup config` exported to secure off-device storage), so
  recovery does not depend solely on FortiManager's own availability.
- **Capacity planning recap.** Revisit [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)'s VM/model sizing
  guidance and [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)'s deep-inspection CPU cost together — the
  fully loaded capstone architecture (HA sync overhead, SD-WAN health-
  checks, deep inspection, VPN termination, and centralized log
  forwarding all running concurrently) has materially different capacity
  requirements than any single subsystem tested in isolation in earlier
  chapters.
- **DR and config backup automation.** Where the organization's change
  volume justifies it, trigger configuration backup automatically on
  every committed change (an automation stitch triggered on a
  `config-change` event, exporting to secure storage) rather than relying
  on administrators to remember a manual backup step.

## Implementation and Automation

### Building the two-cluster capstone fabric from scratch

The capstone platform is four FortiGate-VMs deployed from a blank hypervisor,
licensed individually, and paired into two clusters — an active-passive Cluster A
and an active-active Cluster B (the full walkthrough is Labs 9.1–9.3). The
minimal provisioning skeleton, per member, is deploy → address OOB management →
license → cluster:

```text
# after first-boot password change, on each VM:
config system global
    set hostname FGT-AP-1
end
config system interface
    edit port1                       # OOB management only (10.30.99.0/24)
        set mode static
        set ip 10.30.99.121 255.255.255.0
        set allowaccess ping https ssh
    next
end
execute vm-license-options account-id <forticloud-email>
execute vm-license-options account-password <forticloud-password>
execute vm-license                   # reboots; confirm License Status: Valid
config system ha
    set group-name HA-AP             # HA-AA / group-id 22 on Cluster B
    set group-id 11
    set mode a-p                     # a-a on Cluster B
    set password ISEisC00L123@2026
    set hbdev "port2" 50 "port3" 50  # shared heartbeat — eval 3-interface cap
    set session-pickup enable
    set priority 200                 # 100 on the second member
end
```

The two clusters use **distinct group IDs** (11 and 22) so their heartbeats do
not collide on a shared broadcast domain, and every member is licensed before it
is expected to forward — an unlicensed HA member joins and syncs but forwards
nothing (the design note above).

### Configuration backup and restore

```text
FGT-AP-1 # execute backup config flash capstone-baseline
FGT-AP-1 # execute backup config tftp capstone-baseline.conf 10.30.99.50
```

The first form saves to the device's internal flash storage as a named
revision; the second exports to an external TFTP host for off-device,
durable storage — production environments should always retain an
off-device copy rather than relying on local flash alone.

```text
FGT-AP-1 # execute revision list config
FGT-AP-1 # execute restore config flash <revision-id>
```

`execute restore config flash` reverts the running configuration to a
**numbered** flash revision — the flash argument is the numeric revision id, not
the backup comment, so list them first with `execute revision list config`; only
the off-device `tftp` copy is addressable by filename. This is the recovery
action a validated backup strategy exists to
support and should itself be tested periodically, not assumed to work
correctly the first time it is actually needed.

### Automated backup on configuration change

```text
FGT-AP-1 # config system automation-trigger
FGT-AP-1 (automation-trigger) # edit "Config-Change"
FGT-AP-1 (Config-Change) # set event-type config-change
FGT-AP-1 (Config-Change) # next
FGT-AP-1 (automation-trigger) # end
FGT-AP-1 # config system automation-action
FGT-AP-1 (automation-action) # edit "Backup-Config-TFTP"
FGT-AP-1 (Backup-Config-TFTP) # set action-type cli-script
FGT-AP-1 (Backup-Config-TFTP) # set script "execute backup config tftp auto-backup.conf 10.30.99.50"
FGT-AP-1 (Backup-Config-TFTP) # next
FGT-AP-1 (automation-action) # end
FGT-AP-1 # config system automation-stitch
FGT-AP-1 (automation-stitch) # edit "Auto-Backup-On-Change"
FGT-AP-1 (Auto-Backup-On-Change) # set trigger "Config-Change"
FGT-AP-1 (Auto-Backup-On-Change) # config actions
FGT-AP-1 (actions) # edit 1
FGT-AP-1 (1) # set action "Backup-Config-TFTP"
FGT-AP-1 (1) # next
FGT-AP-1 (actions) # end
FGT-AP-1 (Auto-Backup-On-Change) # next
FGT-AP-1 (automation-stitch) # end
```

This directly reuses the automation-trigger/action/stitch pattern
introduced in [Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md), applied here to configuration lifecycle
management rather than threat response — demonstrating that the same
automation primitives serve both security response and operational
hygiene use cases. Two FortiOS 7.6 specifics matter here: the stitch binds its
action through the **`config actions` sub-table** (`edit 1` / `set action …`),
not a scalar `set action` on the stitch; and the fixed TFTP filename keeps only
the *latest* config — for a real revision history, back up to flash instead
(`execute backup config flash <comment>`, which FortiOS auto-numbers) or embed a
per-run name in the TFTP target.

### End-to-end validation checklist (condensed CLI pass)

```text
FGT-AP-1 # get system status
FGT-AP-1 # get system ha status
FGT-AP-1 # diagnose sys ha status
FGT-AP-1 # get router info routing-table all
FGT-AP-1 # diagnose sys sdwan health-check
FGT-AP-1 # diagnose sys sdwan service4
FGT-AP-1 # diagnose vpn tunnel list
FGT-AP-1 # get vpn ssl monitor
FGT-AP-1 # diagnose firewall iprope list 100004
FGT-AP-1 # diagnose sys session stat
FGT-AP-1 # diagnose sys top
```

This condensed pass exercises licensing/status, HA health, routing,
SD-WAN health and path selection, both VPN types, policy presence, active
session volume, and current resource utilization in a single review
sequence — the practical equivalent of a pre-change or post-incident
health check across the whole stack.

## Validation and Troubleshooting

### A layered troubleshooting decision tree

When traffic does not behave as expected anywhere in this capstone
architecture, work through causes in this order rather than guessing at
the most "interesting" possible cause first:

1. **Physical/link layer.** Is the interface up? (`get system interface
   physical`) Is the correct cable/vNIC connected to the correct
   port/VLAN?
2. **IP/interface configuration.** Does the interface have the expected
   IP, and is it in the expected VDOM? (`show system interface`,
   `diagnose sys vd list`)
3. **Routing.** Does a route exist to the destination, and is it the
   route actually being selected? (`get router info routing-table all`,
   `diagnose firewall proute list`, `diagnose sys sdwan service4` if
   SD-WAN is involved)
4. **Firewall policy.** Does a policy exist that matches this traffic, in
   the correct order, before any broader policy or the implicit deny?
   (`diagnose firewall iprope list <policy-group>`, `diagnose debug flow`)
5. **NAT.** If translation is involved, is the correct pool/VIP being
   applied, and does the policy actually reference it?
   (`diagnose firewall ippool-all list` for SNAT pools, `show firewall vip`
   plus session-table inspection for DNAT/VIPs)
6. **Security profile.** Is a security profile blocking traffic that
   policy/NAT/routing otherwise permit? (profile-specific logs,
   `diagnose debug flow` showing the specific profile that acted)
7. **Application/session layer.** Is the issue actually inside the
   permitted, uninspected traffic itself (an application-layer problem
   unrelated to the FortiGate)? Confirm with a packet capture
   (`diagnose sniffer packet`) if every layer above appears correctly
   configured.

This ordering matters because a fault at an earlier layer produces
symptoms that can look like a fault at a later layer — for example,
missing return traffic can look like a security-profile block when the
actual cause is a missing reverse-direction firewall policy ([Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)),
and working through layers in order avoids chasing the wrong control.

### Common findings when validating the full capstone stack

- **HA formed but SD-WAN health-check reports failure only on the
  secondary.** Confirm SD-WAN member interfaces and gateways are
  configured identically on both HA members — HA synchronizes
  configuration, but a manually staged, not-yet-synchronized change on
  only one member will show exactly this symptom until synchronization
  completes or is corrected.
- **VPN tunnel up but internal hosts unreachable across it.** Almost
  always a routing or bidirectional-policy gap ([Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)) rather than a
  tunnel-layer fault once `diagnose vpn tunnel list` shows an established
  security association.
- **Deep inspection enabled but sessions timing out under load.**
  Revisit [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)'s capacity guidance; check `diagnose sys top` and
  `get system performance status` for CPU saturation correlated with the
  timeout pattern before assuming a profile misconfiguration.
- **FortiManager shows the device out of sync after a stitch-driven
  automated action.** An automation stitch ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) and this chapter)
  that modifies configuration directly on the device will diverge from
  FortiManager's last-known intended state; reconcile by retrieving the
  device's current configuration into FortiManager rather than
  force-installing the stale policy package over it.

## Security and Best Practices

- Consolidate the hardening guidance from every prior chapter as a single
  pre-production checklist: restricted administrative access and MFA
  ([Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)), reviewed and logged firewall policy with no unintended
  broad rules ([Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)), current FortiGuard licensing and a defined
  SSL inspection privacy posture ([Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md)), and scoped, piloted
  automation stitches with documented rollback ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)).
- Test configuration restore, not only backup, on a defined cadence —
  an untested backup is a documentation artifact, not a verified recovery
  capability.
- Treat the layered troubleshooting decision tree as an operational
  runbook artifact, not just a study aid; codifying it (in a wiki, a
  runbook repository, or directly alongside this encyclopedia's own
  documentation-as-code practice from [Volume I](../../volume-001-enterprise-engineering-foundations/README.md)) shortens incident
  response time for any administrator, not only the one who built the
  original configuration.
- Revisit Security Rating ([Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md)) after the full capstone build is
  complete — a device with every subsystem from Chapters 04–08 configured
  is exactly the point at which a best-practice regression (a forgotten
  logging setting, an overly permissive rule added during troubleshooting
  and never removed) is most likely to have crept in.
- For exam readiness specifically: prioritize hands-on repetition of the
  CLI patterns in this volume over memorization, since NSE 4 evaluates
  applied configuration competency; use Fortinet's own NSE Training
  Institute self-paced course labs as the authoritative, official practice
  environment alongside this volume's labs, and do not seek out or use
  any leaked or unofficial exam question content.

## References and Knowledge Checks

**References**

- [Fortinet NSE Training Institute, *NSE 4: FortiGate Security* and
  *NSE 4: FortiGate Infrastructure* self-paced courses.](https://training.fortinet.com/local/staticpage/view.php?page=nse_4)
- [Fortinet, *FortiOS Administration Guide*](https://docs.fortinet.com/product/fortigate/7.6.0) — configuration backup/restore
  and revision management.
- [Fortinet, *FortiOS CLI Reference*](https://docs.fortinet.com/document/fortigate/7.6.0/cli-reference) — `execute backup config`,
  `execute restore config`, `diagnose sniffer packet`.
- [Fortinet, *FortiOS Administration Guide — High Availability*](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/666376/high-availability) — FGCP
  active-passive and active-active clustering, heartbeat, and load balancing.
- [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) — this
  volume's live-verified FGCP labs (5.6 active-passive, 5.7 active-active), including the
  eval-license findings this chapter's HA labs build on.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  current blueprint mapping guidance and caution against reproducing
  proprietary exam content.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — FortiOS 7.6.x
  baseline used throughout this volume.

**Knowledge checks**

1. Which NSE 4 course (FortiGate Security or FortiGate Infrastructure)
   covers SD-WAN, and which covers SSL VPN?
2. Why is testing configuration restore, not just backup, part of a
   complete backup strategy?
3. Walk through the layered troubleshooting decision tree for a scenario
   where a site-to-site VPN tunnel shows as established but internal
   hosts across it cannot reach each other — which layer is the most
   likely cause, and why?
4. Why can an automation stitch that modifies device configuration
   directly cause a FortiManager-managed device to show as out of sync?
5. Two evaluation FortiGate-VMs form an active-active cluster that shows
   both members in-sync with a healthy heartbeat, yet a permitted path
   through the pair drops every session the scheduler assigns to the
   secondary. What is the most likely cause, and which single command
   confirms it on each member?
6. Why must two HA clusters that share the same broadcast domain be
   configured with different HA group IDs?

## Hands-On Lab

This chapter is the **NSE 4 (FortiOS 7.6 Administrator) capstone**. Unlike the earlier
chapters, which layered features onto an already-deployed appliance, this capstone
**starts from bare metal**: you deploy the FortiGate-VMs from scratch, license them,
cluster them for high availability in **both** FGCP modes, prove you can back the
configuration out by every supported transport, and only then layer the secured-edge
build and Security Fabric on top. Every command in Labs 9.4–9.7 is meant to run **against
the clusters you build in Labs 9.1–9.3**, so the capstone exercises a realistic
operational lifecycle end to end: **deploy → license → cluster → back up → secure →
validate**. The labs assume you (the learner) drive every FortiGate CLI/console step
yourself — the hands-on repetition is the point NSE 4 evaluates. Each lab ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Two clusters, two HA modes.** You build **four** FortiGate-VMs and pair them into
**two** clusters, so both FGCP modes are exercised side by side and become the platform
the remaining labs run on:

| Cluster | Members | HA mode | Group name / id | Role in this chapter |
| --- | --- | --- | --- | --- |
| **Cluster A** | FGT-AP-1 / FGT-AP-2 | **Active-passive (A-P)** | `HA-AP` / `11` | Primary enforcement point — Labs 9.4–9.7 run here |
| **Cluster B** | FGT-AA-1 / FGT-AA-2 | **Active-active (A-A)** | `HA-AA` / `22` | Session-load-balancing comparison cluster |

**Shared prerequisites** — a hypervisor able to host four FortiGate-VMs (1 vCPU / 2 GB
each), reachable management on the `10.30.99.0/24` VM-management network, a
FortiCloud/FortiCare account to activate each evaluation license, a TFTP/FTP/SCP server
(the lab uses `10.30.99.50`) for the backup lab, a client host on a data segment, and —
for the secured-edge lab — the [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) IPsec peer and [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) security
profiles. **Cost:** none beyond lab resources.

> **Eval-license reality — HA membership is free, but forwarding is licensed.** A common
> myth holds that the free evaluation license blocks HA outright (because eval VMs of the
> same FortiOS version can share a serial number). This volume's **live homelab run
> disproves it** ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Labs 5.6–5.7, confirmed Aug 2026): two eval VMs
> form a fully working, config-synced, failover-capable cluster — HA membership is **not**
> license-gated. What **is** license-gated is **packet forwarding**: an unlicensed member
> joins, syncs, and shows a healthy heartbeat yet blackholes every transit packet it is
> handed. That is exactly why Lab 9.1 licenses **all four** VMs before any clustering.
> The eval's one structural constraint is its **three-interface cap** — no spare port for
> a dedicated heartbeat, so heartbeat shares the data interfaces (`set hbdev "port2" 50
> "port3" 50`); firmware/build must match **exactly** between members; and you reboot only
> with `execute reboot` (a hypervisor hard-reset corrupts the config partition).

### Lab 9.1 — Deploy and license the four capstone FortiGate-VMs from scratch (Capstone: Deployment & System Config)

**Eval FortiGate — capable (per unit).** Each VM deploys and licenses on the free
evaluation license; the eval caps — 1 vCPU, 2 GB RAM, DES-only crypto, a three-interface
budget, and frozen FortiGuard databases — apply to every unit exactly as in [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md).
Nothing here needs a paid license *yet*; Labs 9.2–9.3 explain the one place licensing
becomes mandatory.

**Objective:** From a blank hypervisor, stand up the four FortiGate-VMs the rest of this
capstone runs on, bring each onto the out-of-band management network, and activate its
evaluation license.

**Step 1 — deploy four VMs (you do this on your hypervisor).** Import the FortiOS 7.6 VM
image four times — `FGT-AP-1`, `FGT-AP-2`, `FGT-AA-1`, `FGT-AA-2` — each with 1 vCPU /
2 GB RAM and **three** vNICs (the eval cap allows no more): `port1` on the
`10.30.99.0/24` VM-management segment, `port2` and `port3` on the two data segments.
Boot all four to the FortiOS login prompt. *(On Proxmox this is the `qm create …
--net0/--net1/--net2` recipe; on ESXi/Hyper-V/KVM use the equivalent — the interface
budget, not the hypervisor, is the constraint.)*

**Step 2 — first-boot bring-up (per VM, at the console).** Default login is `admin` with
no password; FortiOS forces a password change on first login. Then set the hostname and
the OOB management interface:

```text
config system global
    set hostname FGT-AP-1
end
config system interface
    edit port1
        set mode static
        set ip 10.30.99.121 255.255.255.0
        set allowaccess ping https ssh
    next
end
config router static
    edit 1
        set dst 10.30.12.0 255.255.255.0
        set gateway 10.30.99.1
        set device port1
    next
end
```

Repeat with `FGT-AP-2` / `10.30.99.122`, `FGT-AA-1` / `10.30.99.123`, `FGT-AA-2` /
`10.30.99.124`. The management route is a **scoped** route to the admin subnet, not a
default route — the management port carries management traffic only (the out-of-band
design from [Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) and this volume's homelab).

**Step 3 — license each unit (per VM).** The free evaluation license downloads from
FortiCare against your FortiCloud account — no `.lic` file and no token (that path is
[Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)'s Lab 4.2):

```text
execute vm-license-options account-id <forticloud-email>
execute vm-license-options account-password <forticloud-password>
execute vm-license
# the VM reboots to activate; after it returns:
execute vm-license-options reset    # clear the clear-text account password
```

**Step 4 — verify (per VM):**

```text
get system status        # Version: v7.6.x build…, License Status: Valid, Serial-Number
execute ping 10.30.99.1  # management gateway reachable
```

**Expected result:** four licensed FortiGate-VMs, each reachable at its `10.30.99.12x`
management address, each reporting `License Status: Valid`. Record every unit's
**firmware build** — Labs 9.2–9.3 require an *exact* build match between the two members
of each cluster.

**Negative test:** try to cluster two units in Lab 9.2 before licensing the second one.
HA membership will still form (it is not license-gated), but the unlicensed member cannot
forward traffic — the failure mode Lab 9.3 documents in detail. Confirm `License Status:
Valid` on **all four** units here, before any clustering.

**Rollback:** power off and delete the VMs at the hypervisor; a FortiGate-VM holds no
shared external state.

### Lab 9.2 — Cluster A: FGCP active-passive from scratch (Capstone: High Availability)

**Eval FortiGate — capable (both units licensed).** Two eval VMs form a working,
config-synced, failover-capable FGCP cluster — HA membership is **not** license-gated
(proven live in [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Lab 5.6). The eval's one real constraint is the
three-interface cap: there is no spare port for a dedicated heartbeat, so heartbeat
shares the data interfaces.

**Objective:** Cluster `FGT-AP-1` + `FGT-AP-2` into an active-passive pair that presents
one virtual firewall with stateful failover.

**Prerequisites:** both units licensed (Lab 9.1) and on the **exact** same firmware
build; `port2`/`port3` on shared data segments.

**Step 1 — configure HA on both units (identical except priority).** Give `FGT-AP-1` the
higher priority so it wins the election deterministically:

```text
config system ha
    set group-name HA-AP
    set group-id 11
    set mode a-p
    set password ISEisC00L123@2026
    set hbdev "port2" 50 "port3" 50
    set session-pickup enable
    set override enable
    set priority 200
end
```

On `FGT-AP-2`, run the same block with `set priority 100` (lower). The heartbeat shares
`port2`/`port3` because the eval cap leaves no dedicated port; a licensed unit would use a
separate heartbeat link. Cluster A uses `group-id 11` — Cluster B must use a **different**
id (Lab 9.3) or the two clusters' heartbeats collide on the shared broadcast domain.

**Step 2 — verify the cluster forms:**

```text
get system ha status
diagnose sys ha status
diagnose sys ha checksum cluster
```

**Expected result:** `get system ha status` shows **`Mode: HA A-P`**, two members with
`FGT-AP-1` primary and `FGT-AP-2` secondary, and matching checksums across members —
configuration syncs automatically from primary to secondary. `set override enable` plus
the higher priority makes `FGT-AP-1` reclaim primary whenever it is healthy.

**Step 3 — prove stateful failover.** From a segment host, hold a session open through
the cluster, then reboot the primary **gracefully** (`execute reboot` — never a hypervisor
hard-reset, which corrupts the config partition and traps the secondary in a sync loop).
The virtual MAC and interface IPs move to `FGT-AP-2`; the session survives because
`session-pickup` synchronized it.

**Negative test:** mismatch `group-name` or `group-id` between the two units — they never
cluster and both stay primary (split-brain). Matching HA parameters and a working
heartbeat are mandatory. (See [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Lab 5.6, for the full split-brain
walkthrough and live findings.)

**Rollback:** tear the cluster down **secondary first** to standalone — `set mode
standalone`, then clear `group-name`/`group-id`/`password`/`hbdev` (a bare `set mode
standalone` leaves the HA parameters behind); re-address or shut down the second unit
before returning it to a shared segment, since both hold identical synced IPs. Full
sequence in [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Lab 5.6.

### Lab 9.3 — Cluster B: FGCP active-active from scratch (Capstone: High Availability)

**Eval FortiGate — capable ONLY if both members are licensed.** This is the one place the
evaluation license bites hard: HA membership is not license-gated, but **packet forwarding
is**. An unlicensed A-A member joins, syncs, and shows a healthy heartbeat, yet
**blackholes every transit session the scheduler hands it** — measured live at 0/12 on a
permitted path ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Lab 5.7). With `schedule leastconnection` the trap
compounds: the dead member's session count stays at zero, so it is permanently "least
loaded" and keeps being handed new sessions. **Confirm `License Status: Valid` on both
members before running A-A.**

**Objective:** Cluster `FGT-AA-1` + `FGT-AA-2` into an active-active pair where both units
forward and the primary distributes sessions across them.

**Prerequisites:** both units licensed (Lab 9.1), exact firmware match, and — critically —
a **different HA group-id from Cluster A** so the two clusters' heartbeats do not collide
on the shared broadcast domain.

**Step 1 — configure A-A on both units:**

```text
config system ha
    set group-name HA-AA
    set group-id 22
    set mode a-a
    set password ISEisC00L123@2026
    set hbdev "port2" 50 "port3" 50
    set schedule leastconnection
    set load-balance-all enable
    set session-pickup enable
    set priority 200
end
```

Use `set priority 100` on `FGT-AA-2`. `set load-balance-all enable` extends distribution
to *all* firewall sessions (by default A-A load-balances only proxy-based UTM sessions),
which makes the effect visible in a lab that runs no UTM. `group-id 22` keeps this
cluster's heartbeat distinct from Cluster A's `11`.

**Step 2 — verify mode and membership:**

```text
get system ha status
diagnose sys ha status
```

**Expected result:** `get system ha status` reports **`Mode: HA A-A`**, two in-sync
members, heartbeat on `port2`/`port3`. Under transit load, `diagnose sys ha status` shows
**both** members carrying sessions — the scheduler assigns each new session to the
less-loaded unit.

**Step 3 — watch sessions distribute.** A-A distributes **transit** sessions only;
local/management sessions (your SSH, the heartbeat) stay on the primary. Push several
concurrent through-cluster sessions from a segment host, then read the per-unit load:

```text
diagnose sys ha status
get system ha status | grep -A6 "System Usage"
```

Use `-A6`, not `-A3` — three lines of context stop before the second member's `sessions=`
line and make the secondary look idle when it is not.

**Negative test:** run A-A with the secondary unlicensed (or freshly rebooted and still
warming up). The `leastconnection` scheduler steers new sessions onto the zero-session
member, which drops them — 100% loss on that share, not a graceful 50%. Both members must
be `License Status: Valid`; a cold-joining member also blackholes briefly (~20 s) until it
learns ARP/neighbors ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Lab 5.7). Also note: A-A does **not** double
single-flow throughput — it distributes *sessions*, not the packets of one flow.

**Rollback:** `set mode a-p` (or all the way to standalone, secondary first, per
[Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), Lab 5.6).

### Lab 9.4 — Configuration backup and restore via every supported method (Capstone: change management)

**Eval FortiGate — capable.** All backup transports run on the free/licensed evaluation
FortiGate-VM. USB is the one exception on a VM — see Method 7 — because a VM has no USB
controller by default.

**Objective:** Prove you can export and re-import the running configuration by *every*
transport FortiOS supports, so recovery never depends on a single mechanism, and validate
a restore rather than assuming one. Run this against the Cluster A primary (`FGT-AP-1`);
HA syncs the running config, so the cluster has one configuration to protect.

**Method 1 — GUI.** The backup/restore controls are in the **top-right admin menu** (click
the admin name in the banner) → **Configuration → Backup** — *not* under System Settings on
FortiOS 7.6. That same **Configuration** submenu also holds **Restore**, **Revisions** (the
flash revision history from Method 2), **Scripts**, and **Transactions**. The **Backup System
Configuration** dialog offers **Backup to** (*Local PC* or *USB Disk*), a **File format** choice
of *FortiOS* (the native `.conf`) or *YAML*, a **Password mask** toggle (redacts secrets from the
export), and an **Encryption** toggle (passphrase-protects the file); click **OK** to download.
**Restore** is the mirror — pick the file and supply the passphrase if the backup was encrypted.

**Method 2 — CLI to internal flash (numbered revision history).**

```text
execute backup config flash capstone-baseline
execute revision list config
```

Flash keeps a **numbered revision history** on the device — the fast, local rollback
point. Note the revision id from `execute revision list config`; you restore by **id**,
not by the comment.

**Method 3 — CLI to TFTP (off-device).**

```text
execute backup config tftp capstone.conf 10.30.99.50
```

**Method 4 — CLI to FTP (off-device, authenticated).**

```text
execute backup config ftp capstone.conf 10.30.99.50 <ftp-user> <ftp-password>
```

**Method 5 — SCP pull (client-initiated).** Enable the SCP service, then pull the config
from a client:

```text
config system global
    set admin-scp enable
end
# from the backup host on the admin subnet:
# scp admin@10.30.99.121:sys_config ./capstone-scp.conf
```

**Method 6 — FortiManager (central).** A FortiManager-managed unit backs up centrally
through the management tunnel (`execute backup config management-station <comment>`),
giving a fleet-wide revision store independent of any one device — the change-management
workflow from [Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md).

**Method 7 — USB (physical appliances only).** On a hardware FortiGate, `execute backup
config usb capstone.conf` writes to an inserted USB drive. A FortiGate-**VM** has no USB
controller by default, so this transport is unavailable in the VM lab — call it out so the
"all methods" checklist is honest about the one path that does not apply here.

**Restore-to-validate.** A backup that has never been restored is a documentation
artifact, not a recovery capability. Prove one path end to end:

```text
execute restore config tftp capstone.conf 10.30.99.50
# or, from a flash revision:
execute revision list config
execute restore config flash <revision-id>
```

The device reboots and returns on the restored configuration.

**Automate it.** For high-change environments, back up automatically on every committed
change with the config-change automation stitch shown earlier in this chapter's
*Implementation* section (trigger `config-change` → action `execute backup config tftp …`),
so no manual step is relied upon.

**Expected result:** the same running configuration is retrievable through flash, TFTP,
FTP, SCP, and (on hardware) USB or (when managed) FortiManager; and a test restore returns
the device to the captured baseline — a recovery capability you have *verified*, not
assumed.

**Negative test:** back up only to internal flash and treat that as your DR plan. A
chassis or VM loss takes the flash revisions with it — production always keeps an
**off-device** copy (TFTP/FTP/SCP/FortiManager) as well.

**Rollback:** delete the test backup files from the TFTP/FTP/SCP server, remove the flash
test revision (`execute revision delete config <revision-id>`) if you do not want to
retain it, and disable SCP (`set admin-scp disable`) if it was enabled only for the lab.

### Lab 9.5 — End-to-end secured-edge build (Capstone: all five objectives)

**Eval FortiGate — capable (with subscription caveats).** The end-to-end build runs on the eval; its threat-prevention steps return *live* verdicts only with active FortiGuard subscriptions (Chapter 07).

**Objective:** On **Cluster A** (the active-passive pair from Lab 9.2; HA syncs the config to the standby), stand up a protected edge that exercises every NSE 4 objective at once.

```text
# 1. Deployment: default route out the WAN-facing data interface (Objective: Deployment & System Config)
#    On the eval clusters port1 is management-only (Lab 9.1), so the edge egresses via a
#    DATA interface — port3 here. port3 needs an IP in the gateway's subnet FIRST, or
#    FortiOS marks the static route inactive and it never appears in the routing table.
#    (In this volume's homelab port3 is 10.30.163.124/24 via 10.30.163.1; substitute your
#    own WAN addressing.) edit 2 because edit 1 is the scoped management route from Lab 9.1.
config system interface
    edit port3
        set mode static
        set ip <wan-ip> <wan-mask>
        set allowaccess ping
    next
end
config router static
    edit 2
        set gateway <wan-gateway>
        set device port3
    next
end
# 2. Content Inspection: deep-inspection + AV + IPS + web filter (Objective: Content Inspection)
#    (profiles av-lab / ips-lab / block-malicious from Chapter 07; for SSL use the
#     built-in custom-deep-inspection — deep-lab can't be created on the eval, whose
#     ssl-ssh-profile table is capped, per Chapter 07)
# 3. Firewall policy with authentication (Objective: Firewall Policies & Auth)
config firewall policy
    edit 1
        set name secured-lan-egress
        set srcintf port2
        set dstintf port3
        set srcaddr all
        set dstaddr all
        set action accept
        set schedule always
        set service HTTP HTTPS
        # DNS is intentionally NOT in this group-restricted policy: captive-portal
        # auth only triggers on HTTP/HTTPS, so a separate policy permitting DNS
        # WITHOUT set groups must sit above this one, or pre-auth name resolution
        # (and thus the portal redirect) is dropped.
        set groups staff
        set nat enable
        set utm-status enable
        set ssl-ssh-profile custom-deep-inspection
        set av-profile av-lab
        set ips-sensor ips-lab
        set webfilter-profile block-malicious
        set logtraffic all
    next
end
# 4. Routing verification (Objective: Routing)
get router info routing-table all
# 5. VPN reachability (Objective: VPNs)
diagnose vpn tunnel list
```

**Expected result:** authenticated LAN users egress with full UTM inspection, the
routing table shows the default and any tunnel routes, and the IPsec tunnel **built in
[Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)** shows `up`
— this capstone *reuses* that tunnel, since Lab 9.5 configures no new VPN, so it must already
be established (`diagnose vpn tunnel list` is empty otherwise). One policy path then
demonstrates all five objectives working together.

**Negative test:** enable `utm-status` but forget `set groups staff`; unauthenticated
users match and bypass identity control — every objective's control must be present for
the edge to be genuinely secured.

**Rollback:** delete policy 1 and the port3 default route (`config router static / delete 2 / end`); the reused Chapter 06 tunnel stays as-is.

### Lab 9.6 — Security Fabric and Security Rating (Capstone: Fabric integration)

**Eval FortiGate — partial (FortiGuard-gated).** The CSF config and the manual
`diagnose report-runner-v2 security-rating trigger` run on the eval, but a full Security
Rating **score** requires the FortiGuard Security Rating entitlement — which the free eval
lacks — so expect an empty or incomplete rating.

**Objective:** Read the Security Rating to find configuration gaps.

```text
config system csf
    set status enable
    set group-name "Lab-Fabric"
end
diagnose sys csf global
diagnose report-runner-v2 security-rating trigger
```

**Expected result:** the Security Rating audits the Fabric against Fortinet and industry
best practices (admin hardening, unused policies, missing inspection) and scores it —
the operator's built-in gap analysis after a build.

**Negative test:** treat a green policy list as "secure" without running the rating;
gaps like clear-text admin or uninspected policies stay invisible — the rating is what
surfaces them.

**Rollback:** `set status disable` under `config system csf` if lab-only.

### Lab 9.7 — Exam-readiness self-check (Capstone: objective mapping)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Confirm your configuration touches every NSE 4 objective and weight.

```text
show firewall policy | grep edit          # Firewall Policies & Auth (20–25%)
show firewall ssl-ssh-profile | grep edit # Content Inspection (25–30%)
show vpn ipsec phase1-interface | grep edit  # VPNs (10–15%)
show router static | grep edit            # Routing (10–15%)
show system interface | grep edit         # Deployment & System Config (20–25%)
# Use show (not get — get prints no "edit N" lines) and plain grep (FortiOS grep
# has no -c count flag); each line above prints one "edit N" per object — count them.
```

**Expected result:** a non-zero count in each category, proving you have built and can
explain at least one artifact per objective — the exam samples across all five weighted
areas, so hands-on coverage of each is the readiness bar.

**Negative test:** study only Content Inspection because it is the largest slice; the
other 70–75% of the exam is untouched — the weights guide emphasis, not exclusion.

**Rollback:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This capstone chapter mapped every prior chapter in this volume to the
NSE 4 FortiGate Security and FortiGate Infrastructure blueprint domains,
then built the full deployment lifecycle from bare metal: four
FortiGate-VMs deployed and individually licensed from scratch, paired into
two clusters that exercise **both** FGCP modes (active-passive Cluster A and
active-active Cluster B), configuration protected by backup and restore
across **every** supported transport, and the secured-edge build, Security
Fabric, and exam-readiness self-check layered on top of that clustered
platform. Along the way it corrected a common misconception with the
volume's own live evidence — HA membership is not license-gated, but packet
forwarding is, so every cluster member must be individually licensed — and
consolidated the configuration backup/restore and layered troubleshooting
discipline needed to operate the architecture reliably in production. This
completes Volume XIX's progression from NSE 1 awareness through NSE 4
hands-on FortiOS administrator competency.

- [ ] Can map each of this volume's technical chapters to its
      corresponding NSE 4 blueprint domain.
- [ ] Can deploy a FortiGate-VM from scratch and activate its evaluation
      license, and explain why every HA member must be licensed to forward.
- [ ] Can build both an active-passive and an active-active FGCP cluster,
      including the eval three-interface shared-heartbeat constraint and
      distinct group IDs for co-located clusters.
- [ ] Can describe a complete, redundant enterprise FortiGate reference
      architecture and identify the redundancy mechanism at each layer.
- [ ] Can back up and restore the configuration by every supported
      transport and validate the restore, not just the backup.
- [ ] Can apply the layered troubleshooting decision tree to diagnose a
      multi-subsystem fault without guessing.
- [ ] Completed the hands-on lab, including the negative tests, and
      performed appropriate environment cleanup or retention decisions.
