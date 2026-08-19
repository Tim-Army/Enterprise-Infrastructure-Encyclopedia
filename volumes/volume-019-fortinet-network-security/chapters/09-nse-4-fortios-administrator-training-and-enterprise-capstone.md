# Chapter 09: NSE 4 FortiOS Administrator Training and Enterprise Capstone

![Lab flow for this chapter: a full validation checklist across licensing, HA, routing, SD-WAN health, and VPN sessions is recorded as a dated baseline, and a configuration backup exports to external storage. As a negative test, a specific, realistic misconfiguration is introduced without being documented in advance; the resulting symptom is worked through the layered troubleshooting decision tree step by step until the actual root cause is correctly identified without guessing. The fault is corrected and the affected traffic flow confirmed restored, and the original backup is restored as a final validation that recovery returns the device to the exact baseline state.](../../../diagrams/volume-019-fortinet-network-security/chapter-09-capstone-troubleshooting-restore-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: full end-to-end capstone validation with a configuration backup, tested against a deliberately undocumented misconfiguration and restored via backup.*

## Learning Objectives

- Map this volume's chapters to the NSE 4 FortiGate Security and FortiGate
  Infrastructure blueprint domains.
- Describe a complete, redundant enterprise reference architecture
  combining VDOMs, HA, SD-WAN, VPN, and security profiles.
- Configure FortiOS configuration backup and revision comparison as part
  of a change-management discipline.
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

- **A two-member FGCP HA pair** (FGT-LAB-01 / FGT-LAB-02) providing the
  perimeter and internal segmentation enforcement point, eliminating a
  single point of failure at the firewall layer ([Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md)).
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

### Configuration backup and restore

```text
FGT-LAB-01 # execute backup config flash capstone-baseline
FGT-LAB-01 # execute backup config tftp capstone-baseline.conf 10.30.99.50
```

The first form saves to the device's internal flash storage as a named
revision; the second exports to an external TFTP host for off-device,
durable storage — production environments should always retain an
off-device copy rather than relying on local flash alone.

```text
FGT-LAB-01 # execute revision list config
FGT-LAB-01 # execute restore config flash <revision-id>
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
FGT-LAB-01 # config system automation-trigger
FGT-LAB-01 (automation-trigger) # edit "Config-Change"
FGT-LAB-01 (Config-Change) # set event-type config-change
FGT-LAB-01 (Config-Change) # next
FGT-LAB-01 (automation-trigger) # end
FGT-LAB-01 # config system automation-action
FGT-LAB-01 (automation-action) # edit "Backup-Config-TFTP"
FGT-LAB-01 (Backup-Config-TFTP) # set action-type cli-script
FGT-LAB-01 (Backup-Config-TFTP) # set script "execute backup config tftp auto-backup.conf 10.30.99.50"
FGT-LAB-01 (Backup-Config-TFTP) # next
FGT-LAB-01 (automation-action) # end
FGT-LAB-01 # config system automation-stitch
FGT-LAB-01 (automation-stitch) # edit "Auto-Backup-On-Change"
FGT-LAB-01 (Auto-Backup-On-Change) # set trigger "Config-Change"
FGT-LAB-01 (Auto-Backup-On-Change) # config actions
FGT-LAB-01 (actions) # edit 1
FGT-LAB-01 (1) # set action "Backup-Config-TFTP"
FGT-LAB-01 (1) # next
FGT-LAB-01 (actions) # end
FGT-LAB-01 (Auto-Backup-On-Change) # next
FGT-LAB-01 (automation-stitch) # end
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
FGT-LAB-01 # get system status
FGT-LAB-01 # get system ha status
FGT-LAB-01 # diagnose sys ha status
FGT-LAB-01 # get router info routing-table all
FGT-LAB-01 # diagnose sys sdwan health-check
FGT-LAB-01 # diagnose sys sdwan service4
FGT-LAB-01 # diagnose vpn tunnel list
FGT-LAB-01 # get vpn ssl monitor
FGT-LAB-01 # diagnose firewall iprope list 100004
FGT-LAB-01 # diagnose sys session stat
FGT-LAB-01 # diagnose sys top
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

## Hands-On Lab

This chapter is the **NSE 4 (FortiOS 7.6 Administrator) capstone** — integrative
walkthroughs that combine the five exam objectives (Deployment & System Config, Firewall
Policies & Auth, Content Inspection, Routing, VPNs) into an end-to-end build, plus a
self-check that maps your running configuration back to the published objectives. Each
lab ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.3** — a FortiGate on FortiOS 7.6 with WAN + LAN,
a valid FortiGuard subscription, a client host, and a peer for the tunnel. **Cost:**
none beyond lab resources.

### Lab 9.1 — End-to-end secured-edge build (Capstone: all five objectives)

**Eval FortiGate — capable (with subscription caveats).** The end-to-end build runs on the eval; its threat-prevention steps return *live* verdicts only with active FortiGuard subscriptions (Chapter 07).

**Objective:** Stand up a protected edge that exercises every NSE 4 objective at once.

```text
# 1. Deployment: interfaces + default route (Objective: Deployment & System Config)
#    port1 needs a WAN IP in the gateway's subnet FIRST, or FortiOS marks the
#    static route inactive and it never appears in the routing table. Replace the
#    <placeholders> with your real WAN addressing.
config system interface
    edit port1
        set mode static
        set ip <wan-ip> <wan-mask>
    next
end
config router static
    edit 1
        set gateway <wan-gateway>
        set device port1
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
        set dstintf port1
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
— this capstone *reuses* that tunnel, since Lab 9.1 configures no new VPN, so it must already
be established (`diagnose vpn tunnel list` is empty otherwise). One policy path then
demonstrates all five objectives working together.

**Negative test:** enable `utm-status` but forget `set groups staff`; unauthenticated
users match and bypass identity control — every objective's control must be present for
the edge to be genuinely secured.

**Rollback:** delete policy 1 and revert lab routing/tunnels.

### Lab 9.2 — Security Fabric and Security Rating (Capstone: Fabric integration)

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

### Lab 9.3 — Exam-readiness self-check (Capstone: objective mapping)

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
assembled a complete redundant enterprise reference architecture combining
HA, VDOMs, SD-WAN, VPN, security profiles, and centralized management, and
added the configuration backup/restore and layered troubleshooting
discipline needed to operate that architecture reliably in production.
The hands-on lab exercised a full end-to-end validation pass, tested
backup and restore as a genuine recovery capability rather than an
assumed one, and used a deliberately introduced misconfiguration to
practice the layered troubleshooting decision tree this chapter
establishes as this volume's lasting operational reference. This
completes Volume XIX's progression from NSE 1 awareness through NSE 4
hands-on FortiOS administrator competency.

- [ ] Can map each of this volume's technical chapters to its
      corresponding NSE 4 blueprint domain.
- [ ] Can describe a complete, redundant enterprise FortiGate reference
      architecture and identify the redundancy mechanism at each layer.
- [ ] Can configure, schedule, and validate configuration backup and
      restore.
- [ ] Can apply the layered troubleshooting decision tree to diagnose a
      multi-subsystem fault without guessing.
- [ ] Completed the hands-on lab, including the negative test, and
      performed appropriate environment cleanup or retention decisions.
