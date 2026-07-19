# Chapter 06: Panorama Installation, Central Management, and Logging

## Learning Objectives

- Describe Panorama's deployment modes (Panorama, Log Collector, Management
  Only) and choose an appropriate mode and platform (M-Series appliance vs.
  Panorama virtual appliance) for a given fleet size.
- Design a device group hierarchy and a template stack that separates
  policy management from network/device configuration management.
- Onboard a managed firewall to Panorama and push device-group and
  template configuration to it.
- Configure a Collector Group so managed firewalls forward logs to
  Panorama (or a dedicated Log Collector) instead of retaining logs only
  locally.
- Validate a Panorama push, diagnose a failed commit-and-push, and describe
  Panorama's own high-availability model.

## Theory and Architecture

Chapters 01–05 configured a single firewall end to end. Real enterprise
deployments run dozens to thousands of firewalls, and configuring each one
individually does not scale and does not produce consistent policy.
**Panorama** is Palo Alto Networks' centralized management platform for
PAN-OS firewalls, addressing exactly this problem: one console (and API)
that manages policy, network/device configuration, software and content
deployment, and log aggregation across the entire fleet.

### Panorama deployment modes and platforms

Panorama runs as a dedicated M-Series hardware appliance or as a virtual
appliance (VM-Series-adjacent, but a distinct Panorama image) on the same
hypervisor/cloud targets covered in [Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md). Independent of hardware vs.
virtual, Panorama operates in one of three modes:

| Mode | Function |
| --- | --- |
| Panorama mode | Full management plane: device group/template policy management, software/content deployment, plus local log collection |
| Log Collector mode | Dedicated exclusively to receiving and storing logs from managed firewalls (a "Dedicated Log Collector," or DLC); does not perform policy management |
| Management Only mode | Full policy/device management, but explicitly does not store logs locally — logs are forwarded to separate Log Collectors |

Small deployments commonly run a single Panorama appliance in Panorama
mode, combining management and log collection. Larger fleets separate
concerns: a Management Only Panorama pair handles policy and push
operations, while one or more Dedicated Log Collectors (individually or
organized into a **Collector Group** for redundancy and load distribution)
absorb the log volume, which scales independently and can be sized to the
fleet's actual logging rate rather than the management appliance's compute
profile.

### Device groups: policy hierarchy

A **device group** is Panorama's unit of policy management — a logical
grouping of managed firewalls (or, more precisely, of virtual systems on
managed firewalls) that share a common policy scope. Device groups form a
hierarchy: a top-level "Shared" scope applies to every managed firewall
regardless of device group, and device groups themselves can be nested
(a parent device group's rules apply to all of its child device groups).

Policy within a device group is split into **pre-rules** (evaluated before
any rules defined locally on the firewall) and **post-rules** (evaluated
after local rules, typically used for a catch-all deny/log rule that
cannot be overridden or bypassed by local configuration). This ordering —
Shared pre-rules, then parent device group pre-rules, then local device
group pre-rules, then any rules configured locally on the firewall itself,
then local device group post-rules, then parent device group post-rules,
then Shared post-rules — lets an organization enforce non-negotiable global
security controls (in Shared and parent pre-rules) while still allowing
site-specific policy flexibility in local device group rules, all resolved
in a single predictable evaluation order.

### Templates and template stacks: network/device configuration

While device groups manage security, NAT, and decryption *policy*,
**templates** manage *network and device configuration* — interfaces,
zones, virtual routers, HA settings, and device-level settings like NTP and
DNS (the constructs from [Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md), plus system settings from [Chapter 01](01-cybersecurity-apprentice-foundations.md)).
A **template stack** combines multiple templates in a defined priority
order (higher-priority templates override lower-priority ones for any
overlapping setting), which is how Panorama expresses "every firewall gets
this base network template, and branch-office firewalls additionally get
this branch-specific template layered on top."

Device groups and template stacks are independent hierarchies serving
different configuration domains, and a managed firewall is typically
assigned to exactly one device group and one template stack simultaneously
— together they define the complete pushed configuration for that
firewall.

### Managed device onboarding

A firewall becomes Panorama-managed either through the bootstrap
mechanism from [Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md) (`panorama-server`, `tplname`, `dgname` in
`init-cfg.txt`) or by manually pointing an already-configured firewall at
Panorama and approving it from the Panorama console. Once managed,
Panorama tracks each device's connection status, software/content
versions, and HA state (if applicable) from a single inventory view,
which is also the foundation for the fleet-wide operational tasks covered
in [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md).

### Panorama high availability

Panorama itself supports an active/passive HA pair, conceptually similar
to firewall HA ([Chapter 04](04-pan-os-networking-nat-routing-and-high-availability.md)) but without a data-plane session-synchronization
requirement — Panorama HA synchronizes the management database (device
group, template, and object configuration) between peers rather than live
traffic sessions. A Panorama HA pair eliminates the management plane as a
single point of failure; it does not, on its own, provide log redundancy —
that is the Collector Group's responsibility, covered below.

## Design Considerations

- **When Panorama becomes necessary.** A small handful of standalone
  firewalls can be managed individually, but the value of Panorama —
  consistent policy, centralized visibility, and coordinated software/content
  lifecycle — grows sharply with fleet size. Most organizations deploying
  more than a handful of firewalls, or any organization with a
  multi-site/branch topology, should plan for Panorama from the outset
  rather than retrofitting it after individual-firewall policy drift has
  already accumulated.
- **Device group hierarchy design.** Mirror the hierarchy to the
  organization's actual policy governance structure, not its org chart —
  common patterns include a hierarchy by risk tier (data center, branch,
  DMZ) or by business unit, with Shared rules reserved for genuinely
  universal controls (for example, a block rule for known-malicious
  categories) that every device group must inherit without exception.
  Avoid a flat, single-level device group structure for anything beyond a
  small fleet — it forces every policy difference into local, unmanaged
  per-firewall rules, defeating the purpose of centralized management.
- **Template stack layering.** Keep a small number of reusable templates
  (a common base template covering NTP/DNS/logging settings, plus one
  template per site archetype — branch, data center, cloud) combined into
  stacks per firewall role, rather than one bespoke template per firewall.
  Bespoke templates reintroduce the same per-device drift problem
  Panorama is meant to solve.
- **Management Only vs. combined Panorama mode.** Choose Management Only
  Panorama with separate Dedicated Log Collectors once log volume or
  retention requirements would otherwise strain a combined appliance's
  resources, or once the organization's log retention/compliance
  requirements justify independently scaling log storage. Smaller,
  single-site deployments can reasonably run combined Panorama mode
  indefinitely.
- **Collector Group sizing and redundancy.** Size Collector Groups against
  actual sustained log rate (events per second) from the fleet, not peak
  burst alone, and configure more than one Log Collector per Collector
  Group where log retention is compliance-relevant, so a single collector
  failure does not create a retention gap.
- **Panorama HA is a management-plane control, not a logging control.**
  Do not assume a Panorama HA pair alone satisfies a log-redundancy
  requirement; that is a Collector Group design decision, addressed
  separately.

## Implementation and Automation

### Creating a device group hierarchy

```text
admin@panorama01# set devicegroups Global-Baseline
admin@panorama01# set devicegroups Branch-Offices parent Global-Baseline
admin@panorama01# set devicegroups DataCenter parent Global-Baseline
admin@panorama01# commit
```

### Adding a Shared pre-rule enforced across every device group

```text
admin@panorama01# set shared pre-rulebase security rules Block-Known-Malicious from any to any source any destination any application any category [ malware phishing command-and-control ] action deny
admin@panorama01# set shared pre-rulebase security rules Block-Known-Malicious log-end yes
admin@panorama01# commit
```

### Adding a device-group-scoped pre-rule

```text
admin@panorama01# set devicegroups Branch-Offices pre-rulebase security rules Allow-Branch-Web from trust to untrust source any destination any application [ web-browsing ssl ] service application-default action allow
admin@panorama01# set devicegroups Branch-Offices pre-rulebase security rules Allow-Branch-Web profile-setting group Standard-Inspection
admin@panorama01# commit
```

### Creating a template and a template stack

```text
admin@panorama01# set template Base-Network config deviceconfig system dns-setting servers primary 10.10.10.2
admin@panorama01# set template Base-Network config deviceconfig system ntp-servers ntp-server-1 ntp-server-address pool.ntp.org
admin@panorama01# set template Branch-Network config network virtual-router default routing-table ip static-route default destination 0.0.0.0/0 nexthop ip-address 203.0.113.1
admin@panorama01# set template-stack Branch-Stack templates [ Base-Network Branch-Network ]
admin@panorama01# commit
```

### Onboarding a managed firewall

On Panorama, after the firewall has connected (via bootstrap or manual
`panorama-server` configuration on the firewall itself):

```text
admin@panorama01> request batch-fetch device-info
admin@panorama01# set devices 0011C1234567 hostname pa-branch-01
admin@panorama01# set devicegroups Branch-Offices devices 0011C1234567
admin@panorama01# set template-stack Branch-Stack devices 0011C1234567
admin@panorama01# commit
```

### Pushing configuration to managed devices

Panorama configuration changes are staged with `commit` (to Panorama's own
candidate configuration) and then explicitly pushed to managed firewalls
with a separate action:

```text
admin@panorama01# commit description "Add branch web-access rule"
admin@panorama01> request batch-push device-group Branch-Offices
```

Pushing device-group and template-stack changes are distinct operations;
a change to a template requires its own push action targeting the
affected template stack, and Panorama's Web UI (and the equivalent CLI
job-status commands) reports per-device push success or failure rather
than a single fleet-wide result.

### Configuring a Collector Group for log forwarding

```text
admin@panorama01# set log-collector-group Branch-Collectors log-collectors LC-01
admin@panorama01# set log-collector-group Branch-Collectors log-collectors LC-02
admin@panorama01# set log-collector-group Branch-Collectors min-retention-days 90
admin@panorama01# commit
```

On each managed firewall's template (or template stack), point log
forwarding at the Collector Group:

```text
admin@panorama01# set template Base-Network config deviceconfig system panorama-server 10.20.30.10
admin@panorama01# set template Base-Network config deviceconfig system panorama-server-2 10.20.30.11
admin@panorama01# commit
```

## Validation and Troubleshooting

- **Push completes but firewall does not reflect the change.** Check the
  push job status (`show jobs id <id>` on Panorama, or the Web UI Task
  Manager) for a per-device result; a device-level push failure (commit
  validation error on the target firewall, connectivity loss mid-push) is
  reported separately from Panorama's own local commit success and is a
  common point of confusion for engineers who only check the Panorama
  commit result.
- **Managed device shows "Disconnected" or "Out of Sync."** Confirm
  network reachability between the firewall's management interface and
  Panorama (or, if configured, that the management traffic is routed over
  a data interface via `panorama-server` bound to that interface),
  and confirm the firewall's system clock is reasonably in sync with
  Panorama — significant clock drift can affect certificate validation
  between the two.
- **Logs not appearing in Panorama.** Confirm the Collector Group
  assignment is actually pushed to the firewall's template (a common
  mistake configures the Collector Group on Panorama but never pushes the
  corresponding `panorama-server`/log-forwarding setting to the managed
  device's template), and confirm the Collector Group's own commit
  (distinct from a device-group/template push) has been applied — Collector
  Group configuration changes require a Panorama-local commit that
  specifically includes the Collector Group scope.
- **Policy behaves differently than expected on one firewall in a device
  group.** Check for a locally defined rule on that specific firewall
  (rules created directly on the firewall's own Web UI/CLI outside
  Panorama management) — local rules are evaluated between device-group
  pre-rules and post-rules and can produce a result that looks like a
  device-group policy bug but is actually local drift; `show config
  running` on the firewall itself reveals any such local additions.
- **Template push succeeds but a network setting appears unchanged.**
  Confirm template stack priority order — a lower-priority template's
  setting is silently overridden by a higher-priority template in the same
  stack for any overlapping configuration path; review the stack's
  template order before assuming the push itself failed.

## Security and Best Practices

- Scope Panorama administrator accounts with role-based access control and
  **access domains**, which restrict which device groups and templates a
  given administrator can view or modify — a regional administrator should
  not have edit access to a global Shared pre-rule scope.
- Reserve Shared and top-level parent device group pre-rules for controls
  the organization requires to be non-negotiable and unbypassable by any
  child device group or local firewall configuration.
- Require change descriptions on every Panorama commit (`commit
  description "..."`) and treat the Panorama config audit log with the
  same rigor as any change-management record — Panorama centralizes not
  just enforcement but also the audit trail for who changed what, fleet-wide.
- Encrypt and restrict access to Panorama-to-managed-device communication
  paths; place Panorama itself on a protected management segment, not a
  general-purpose data VLAN, consistent with the management-plane
  hardening guidance from [Chapter 01](01-cybersecurity-apprentice-foundations.md).
- Size and redundantly configure Collector Groups to meet the
  organization's actual log-retention compliance requirement, and test
  Panorama HA failover (and Collector Group member failure) in a
  non-production window before relying on it during an actual incident.
- Back up the Panorama configuration (`request panorama backup` or the
  equivalent scheduled export) on a defined cadence independent of the
  managed firewalls' own configurations, since a Panorama-only backup gap
  can silently outlast individual firewall backups if not tracked
  separately.

## References and Knowledge Checks

**References**

- [Palo Alto Networks, *Panorama Administrator's Guide* (version 11.1).](https://docs.paloaltonetworks.com/panorama/11-1/panorama-admin)
- [Palo Alto Networks, *Panorama Deployment Modes and Sizing* documentation.](https://docs.paloaltonetworks.com/panorama/11-1/panorama-admin/panorama-overview/panorama-models)
- [Palo Alto Networks, *Manage Log Collection* documentation (Collector
  Groups, Dedicated Log Collectors).](https://docs.paloaltonetworks.com/panorama/11-1/panorama-admin/manage-log-collection)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Panorama 11.x
  baseline used throughout this volume.

**Knowledge checks**

1. What is the practical difference between a device group and a template
   stack, and why does a managed firewall typically need both?
2. In what order are Shared, parent device group, local device group, and
   locally defined firewall rules evaluated?
3. Why might a Collector Group configuration change be committed
   successfully on Panorama but still fail to deliver logs from a managed
   firewall?
4. What does Panorama HA synchronize between peers, and what does it
   explicitly not provide on its own?

## Hands-On Lab

**Objective:** Build a two-level device group hierarchy with a Shared
pre-rule and a device-group-scoped rule, create a template stack, onboard a
lab firewall, push both device group and template configuration, and
configure log forwarding to Panorama — including a negative test that
demonstrates local device drift overriding expected behavior.

**Prerequisites**

- A lab Panorama instance (virtual appliance is sufficient) reachable from
  the lab firewall(s) built in Chapters 03–05.
- At least one managed firewall available for onboarding, either freshly
  bootstrapped ([Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md)) or manually pointed at Panorama.
- Administrative access to both Panorama and the managed firewall for the
  duration of the lab.

**Steps**

1. On Panorama, create a two-level device group hierarchy:

   ```text
   admin@panorama01# set devicegroups Global-Baseline
   admin@panorama01# set devicegroups Branch-Offices parent Global-Baseline
   admin@panorama01# commit
   ```

2. Add a Shared pre-rule blocking known-malicious categories:

   ```text
   admin@panorama01# set shared pre-rulebase security rules Block-Known-Malicious from any to any source any destination any application any category [ malware phishing command-and-control ] action deny
   admin@panorama01# commit
   ```

3. Add a device-group-scoped allow rule under `Branch-Offices`:

   ```text
   admin@panorama01# set devicegroups Branch-Offices pre-rulebase security rules Allow-Branch-Web from trust to untrust source any destination any application [ web-browsing ssl ] service application-default action allow
   admin@panorama01# commit
   ```

4. Create a base template and a template stack:

   ```text
   admin@panorama01# set template Base-Network config deviceconfig system dns-setting servers primary 10.10.10.2
   admin@panorama01# set template-stack Branch-Stack templates Base-Network
   admin@panorama01# commit
   ```

5. Onboard the lab firewall, assigning it to the device group and template
   stack:

   ```text
   admin@panorama01# set devicegroups Branch-Offices devices <FIREWALL_SERIAL>
   admin@panorama01# set template-stack Branch-Stack devices <FIREWALL_SERIAL>
   admin@panorama01# commit
   ```

6. Push both the device group and the template stack:

   ```text
   admin@panorama01> request batch-push device-group Branch-Offices
   admin@panorama01> request batch-push template-stack Branch-Stack
   ```

   **Expected result:** The push job reports success for the target
   firewall; on the firewall itself, `show rulebase security rules` lists
   `Block-Known-Malicious` and `Allow-Branch-Web` as Panorama-pushed rules.

7. Configure log forwarding by pointing the template's `panorama-server`
   setting at the Panorama management IP, then push again:

   ```text
   admin@panorama01# set template Base-Network config deviceconfig system panorama-server 10.20.30.10
   admin@panorama01# commit
   admin@panorama01> request batch-push template-stack Branch-Stack
   ```

8. Generate test traffic on the firewall and confirm logs appear in
   Panorama's traffic log viewer (`Monitor > Logs > Traffic` on Panorama,
   filtered to the onboarded device).

9. **Negative test:** On the managed firewall itself (not through
   Panorama), add a local rule above where the pushed rules land in
   evaluation order, permitting an application the Shared pre-rule should
   block for demonstration purposes, and observe that a locally created
   rule is preserved independently of Panorama's device-group rules:

   ```text
   admin@pa-branch-01# set rulebase security rules Local-Test-Rule from trust to untrust source any destination any application any action allow
   admin@pa-branch-01# commit
   ```

   **Expected result:** `show config running` on the firewall shows
   `Local-Test-Rule` alongside the Panorama-pushed rules, confirming that
   local configuration persists independently and underscoring why
   uncontrolled local changes cause policy drift in a Panorama-managed
   fleet. Remove it:

   ```text
   admin@pa-branch-01# delete rulebase security rules Local-Test-Rule
   admin@pa-branch-01# commit
   ```

10. **Cleanup:** If this lab environment will be reused in [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md),
    leave the device group, template stack, and log forwarding
    configuration in place; otherwise remove the lab-only device group
    assignment and pushed rules from Panorama:

    ```text
    admin@panorama01# delete devicegroups Branch-Offices pre-rulebase security rules Allow-Branch-Web
    admin@panorama01# delete shared pre-rulebase security rules Block-Known-Malicious
    admin@panorama01# commit
    admin@panorama01> request batch-push device-group Branch-Offices
    ```

## Summary and Completion Checklist

Panorama turns individually configured firewalls into a governed fleet:
device groups centralize security, NAT, and decryption policy with a
predictable pre-rule/local/post-rule evaluation order; template stacks
centralize network and device configuration with layered priority; and
Collector Groups centralize log retention independent of the management
plane's own sizing. [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md) builds on this foundation for fleet-wide
operational tasks — coordinated software and content upgrades, scheduled
maintenance, and automation via the PAN-OS and Panorama XML/REST APIs.

- [ ] Can design a device group hierarchy that separates non-negotiable
      global policy from site-specific local policy.
- [ ] Can build a template stack and explain template priority ordering.
- [ ] Can onboard a managed firewall and push both device-group and
      template-stack configuration to it.
- [ ] Can configure a Collector Group and verify logs are being forwarded
      from a managed firewall.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
