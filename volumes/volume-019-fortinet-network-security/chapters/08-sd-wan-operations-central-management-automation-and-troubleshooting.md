# Chapter 08: SD-WAN, Operations, Central Management, Automation, and Troubleshooting

![Lab topology for this chapter: an SD-WAN zone with two members and a health-check reports both within SLA thresholds, with a critical-application rule currently selecting the primary WAN member. As a negative test, the primary WAN interface is administratively brought down to simulate an outage; the health-check reports that member failed, and the rule automatically selects the secondary WAN member with no manual intervention. Restoring the primary interface returns path selection to it once its SLA is met again. Separately, the device registers to central management and a read-only-scoped API token successfully retrieves system status via the REST API.](../../../diagrams/volume-019-fortinet-network-security/chapter-08-sdwan-failover-topology.svg)

*Figure 8-1. Topology used throughout this chapter's Hands-On Lab: an SD-WAN zone with SLA-based path selection, tested against a simulated WAN outage, plus central management and REST API validation.*

## Learning Objectives

- Configure an SD-WAN zone with multiple WAN members, a performance SLA
  health-check, and an SLA-based SD-WAN rule.
- Register a FortiGate to FortiManager for centralized policy management.
- Call the FortiOS REST API and describe how Ansible automates FortiGate
  configuration at scale.
- Configure an automation stitch that reacts to a security event.
- Diagnose SD-WAN path selection, central management sync, and automation
  failures.

## Theory and Architecture

### SD-WAN architecture on FortiGate

FortiGate's SD-WAN implementation converges WAN path selection and
security enforcement on the same device, rather than treating SD-WAN as a
separate overlay appliance in front of a firewall. Its building blocks:

- **SD-WAN zone** — a logical grouping of WAN-facing interfaces (the
  default zone is commonly named `virtual-wan-link`) that participate in
  SD-WAN path selection as a set.
- **SD-WAN members** — the individual physical or logical interfaces
  (`wan1`, `wan2`, an IPsec tunnel interface, or an LTE/5G backup
  interface) assigned to a zone, each with a configured gateway and an
  optional cost/weight used by rule logic.
- **Performance SLA health-check** — active probing (ICMP, HTTP, TCP echo,
  DNS, or a specific application-aware probe) against defined targets,
  measuring latency, jitter, and packet loss per member continuously, not
  just link up/down state.
- **SD-WAN rules (`config system sdwan` `config service`)** — policies
  that select which member(s) carry traffic matching specific criteria
  (source, destination, application, or internet service), using a
  strategy such as lowest latency/jitter/packet-loss within an SLA target,
  best-quality among available members, lowest cost, or manual load
  balancing.

This architecture directly extends the policy-routing concept from
[Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md): an SD-WAN rule is, structurally, an application- and
performance-aware policy route, continuously re-evaluated against live
health-check telemetry rather than a static, always-on preference.

### Central management with FortiManager

**FortiManager** centralizes policy authoring, device configuration, and
firmware management across a fleet of FortiGates. Key concepts:

- **ADOM (Administrative Domain)** — a logical grouping of managed devices
  (commonly by business unit, region, or customer in a managed-service
  context) with its own policy packages and version alignment, preventing
  one group's changes from unintentionally affecting another.
- **Device Manager** — the inventory and per-device configuration view,
  including firmware and installation status.
- **Policy Packages** — a named set of firewall policies and objects
  authored centrally in FortiManager and installed to one or more managed
  FortiGates as a unit, giving a single reviewable change ("install
  preview") before it is pushed to production devices.
- **Installation workflow** — FortiManager computes and displays a diff
  between the intended policy package and each target device's current
  configuration before install, supporting a plan/review/apply pattern
  consistent with the infrastructure-as-code discipline covered in
  Volume IX.

**FortiAnalyzer** complements FortiManager as the centralized logging and
analytics plane — FortiGates forward logs to FortiAnalyzer for long-term
retention, correlation, and reporting beyond what local FortiGate log
storage supports, and its output feeds SIEM/SOC workflows covered
vendor-neutrally in [Volume XI](../../volume-011-observability-enterprise-operations/README.md).

### Automation surfaces

FortiOS exposes configuration and monitoring through a **REST API**
(`/api/v2/cmdb` for configuration, `/api/v2/monitor` for operational
state), authenticated with an API administrator account and token, in
addition to community-maintained and Fortinet-published **Ansible
collections** (`fortinet.fortios`) that wrap the same API surface into
idempotent playbook tasks. **Automation stitches**
(`config system automation-trigger`, `automation-action`,
`automation-stitch`) provide on-box, event-driven automation without an
external orchestrator — a trigger (a specific log event, IPS detection, or
schedule) fires one or more actions (quarantine a host, send a
notification, run a local CLI script) directly on the FortiGate.

## Design Considerations

- **SD-WAN member weighting and dual-ISP failover vs. load balancing.**
  Decide deliberately whether dual WAN circuits are intended as an
  active/backup failover pair or as simultaneous load-shared capacity —
  this determines whether SD-WAN rules use a priority-based strategy
  (preferring one member until its SLA is violated) or a load-balancing
  strategy (distributing sessions across both under normal conditions).
- **ADOM and firmware version alignment.** Keep devices within an ADOM on
  firmware versions FortiManager's own version supports for policy
  package installation; a significant version skew between FortiManager
  and managed devices is a common source of installation failures and
  unsupported feature gaps.
- **Change control via policy package workflow.** Use FortiManager's
  install preview and (where licensed) workflow-mode approval step as the
  organization's actual change control gate for firewall policy changes at
  scale, rather than allowing direct per-device CLI changes that
  FortiManager's view of "intended state" does not know about and will
  overwrite or conflict with on the next centrally managed install.
- **Log retention sizing on FortiAnalyzer.** Size FortiAnalyzer storage
  and retention against actual log volume from every security profile
  enabled in [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) (deep inspection and IPS in particular generate
  substantially more log volume than a bare permit/deny policy) and
  against the organization's compliance-driven retention requirement, not
  just device count.
- **Automation guardrails.** An automation stitch that can quarantine a
  host or ban an IP is powerful and also capable of a self-inflicted
  outage if its trigger is too broad (for example, treating a single
  IPS false positive as grounds for automatically banning a business-
  critical internal server's IP); scope triggers narrowly and test in a
  non-production or monitor-only mode before enabling destructive actions
  broadly.

## Implementation and Automation

### SD-WAN zone, members, and health-check

```text
FGT-LAB-01 # config system sdwan
FGT-LAB-01 (sdwan) # set status enable
FGT-LAB-01 (sdwan) # config zone
FGT-LAB-01 (zone) # edit "virtual-wan-link"
FGT-LAB-01 (virtual-wan-link) # next
FGT-LAB-01 (zone) # end
FGT-LAB-01 (sdwan) # config members
FGT-LAB-01 (members) # edit 1
FGT-LAB-01 (1) # set interface "port1"
FGT-LAB-01 (1) # set zone "virtual-wan-link"
FGT-LAB-01 (1) # set gateway 203.0.113.1
FGT-LAB-01 (1) # next
FGT-LAB-01 (members) # edit 2
FGT-LAB-01 (2) # set interface "port6"
FGT-LAB-01 (2) # set zone "virtual-wan-link"
FGT-LAB-01 (2) # set gateway 198.51.100.1
FGT-LAB-01 (2) # next
FGT-LAB-01 (members) # end
FGT-LAB-01 (sdwan) # config health-check
FGT-LAB-01 (health-check) # edit "Internet"
FGT-LAB-01 (Internet) # set server "8.8.8.8" "1.1.1.1"
FGT-LAB-01 (Internet) # set protocol ping
FGT-LAB-01 (Internet) # set members 1 2
FGT-LAB-01 (Internet) # config sla
FGT-LAB-01 (sla) # edit 1
FGT-LAB-01 (1) # set latency-threshold 150
FGT-LAB-01 (1) # set jitter-threshold 30
FGT-LAB-01 (1) # set packetloss-threshold 2
FGT-LAB-01 (1) # next
FGT-LAB-01 (sla) # end
FGT-LAB-01 (Internet) # next
FGT-LAB-01 (health-check) # end
FGT-LAB-01 (sdwan) # end
```

### SD-WAN rule (SLA-based path selection)

```text
FGT-LAB-01 # config system sdwan
FGT-LAB-01 (sdwan) # config service
FGT-LAB-01 (service) # edit 1
FGT-LAB-01 (1) # set name "Critical-Apps"
FGT-LAB-01 (1) # set mode sla
FGT-LAB-01 (1) # set src "LAN-SUBNET"
FGT-LAB-01 (1) # set dst "all"
FGT-LAB-01 (1) # config sla
FGT-LAB-01 (sla) # edit "Internet"
FGT-LAB-01 (Internet) # set id 1
FGT-LAB-01 (Internet) # next
FGT-LAB-01 (sla) # end
FGT-LAB-01 (1) # set priority-members 1 2
FGT-LAB-01 (1) # next
FGT-LAB-01 (service) # end
FGT-LAB-01 (sdwan) # end
```

`Critical-Apps` prefers member 1 (`port1`/WAN1) as long as it meets the
`Internet` health-check's SLA target 1, falling back to member 2
(`port6`/WAN2) automatically if WAN1 violates the configured latency,
jitter, or packet-loss thresholds.

### Registering to FortiManager

```text
FGT-LAB-01 # config system central-management
FGT-LAB-01 (central-management) # set type fortimanager
FGT-LAB-01 (central-management) # set fmg "172.16.99.20"
FGT-LAB-01 (central-management) # set mode normal
FGT-LAB-01 (central-management) # end
```

Registration additionally requires an authorization step on the
FortiManager side (accepting the device into an ADOM's Device Manager
inventory); once authorized, policy package installs from FortiManager
become available for this device.

### REST API automation example

```bash
# Retrieve system status via the FortiOS REST API using an API token.
curl -k -X GET "https://172.16.99.1/api/v2/monitor/system/status" \
  -H "Authorization: Bearer <API_TOKEN>"
```

```yaml
# ansible-playbook example using the fortinet.fortios collection
# to create a firewall address object idempotently.
- name: Ensure BRANCH-03 address object exists on FGT-LAB-01
  hosts: fortigates
  connection: httpapi
  vars:
    ansible_httpapi_use_ssl: true
    ansible_httpapi_validate_certs: false
    ansible_network_os: fortinet.fortios.fortios
  tasks:
    - name: Create firewall address object
      fortinet.fortios.fortios_firewall_address:
        vdom: "root"
        state: present
        firewall_address:
          name: "BRANCH-03-SUBNET"
          subnet: "10.30.10.0 255.255.255.0"
```

### Automation stitch: auto-quarantine on repeated IPS detection

```text
FGT-LAB-01 # config system automation-trigger
FGT-LAB-01 (automation-trigger) # edit "IPS-Critical-Event"
FGT-LAB-01 (IPS-Critical-Event) # set event-type ips-traffic
FGT-LAB-01 (IPS-Critical-Event) # next
FGT-LAB-01 (automation-trigger) # end
FGT-LAB-01 # config system automation-action
FGT-LAB-01 (automation-action) # edit "Ban-Source-IP"
FGT-LAB-01 (Ban-Source-IP) # set action-type ban-ip
FGT-LAB-01 (Ban-Source-IP) # set duration 3600
FGT-LAB-01 (Ban-Source-IP) # next
FGT-LAB-01 (automation-action) # end
FGT-LAB-01 # config system automation-stitch
FGT-LAB-01 (automation-stitch) # edit "IPS-AutoBlock"
FGT-LAB-01 (IPS-AutoBlock) # set trigger "IPS-Critical-Event"
FGT-LAB-01 (IPS-AutoBlock) # set actions "Ban-Source-IP"
FGT-LAB-01 (IPS-AutoBlock) # next
FGT-LAB-01 (automation-stitch) # end
```

Consistent with the automation guardrail design consideration above, pilot
this stitch in a monitor/logging-only configuration and review triggered
events before enabling the `ban-ip` action against production traffic.

## Validation and Troubleshooting

- **SD-WAN health-check and member status.** `diagnose sys sdwan
  health-check status` shows real-time latency/jitter/packet-loss per
  member against configured SLA thresholds; `diagnose sys sdwan member`
  shows current member state and selection eligibility.
- **SD-WAN rule path selection.** `diagnose sys sdwan service` shows which
  member an SD-WAN rule (service) is currently selecting and why; use this
  to confirm `Critical-Apps` is actually preferring WAN1 under normal
  conditions before testing failover.
- **FortiManager registration/install issues.** `diagnose debug
  application fmsyncd -1` traces the synchronization process between a
  managed device and FortiManager; a device stuck in "unauthorized" or
  "out of sync" state in FortiManager's Device Manager most often traces
  to a configuration change made directly on the device's CLI that
  FortiManager's intended-state view does not know about — retrieve the
  device's current configuration into FortiManager (rather than force-
  pushing the stale policy package) to reconcile.
- **REST API authentication failures.** A `401`/`403` response typically
  indicates an invalid or expired API token, an API administrator account
  missing sufficient accprofile permissions, or the calling host not
  included in that API administrator's `trusthost` restriction
  ([Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)); a CSRF-token-related failure on session-cookie-based (as
  opposed to bearer-token) API calls indicates the client is not handling
  the `X-CSRFTOKEN` header FortiOS expects for that authentication mode.
- **Automation stitch not firing.** Confirm the trigger's `event-type` and
  any log-filter criteria actually match the log events being generated
  (`diagnose test application <daemon>` or the relevant event log review
  in the GUI); a stitch that appears configured but never fires is very
  often a filter criteria mismatch rather than a stitch-engine fault.

## Security and Best Practices

- Restrict REST API access to a dedicated API administrator account with
  the minimum required `accprofile` scope, HTTPS only, and a `trusthost`
  restriction limiting which management hosts may present that token —
  treat an API token with the same sensitivity as an administrator
  password.
- Rotate API tokens on a defined schedule and immediately upon any
  suspected exposure (a token committed to a public repository, for
  example), and prefer short-lived tokens issued by an automation
  pipeline over long-lived tokens stored in a script.
- Enforce FortiManager policy package installation as the actual change
  path for centrally managed devices, and treat direct CLI changes to a
  centrally managed device as an exception requiring reconciliation, not
  a routine practice.
- Test SD-WAN failover behavior on a defined cadence rather than assuming
  it works because it was validated once at initial deployment — ISP
  circuit changes, routing changes upstream, and FortiOS upgrades can all
  alter failover behavior.
- Scope automation stitches narrowly, pilot destructive actions
  (`ban-ip`, `quarantine`) in a logging/monitor-only mode first, and
  maintain a documented rollback (how to unban an IP or release a
  quarantined host) for every stitch capable of a disruptive action.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiOS Administration Guide*](https://docs.fortinet.com/product/fortigate/8.0.0) — SD-WAN, central management,
  and automation stitches.
- [Fortinet, *FortiManager Administration Guide*](https://docs.fortinet.com/product/fortimanager/8.0) — ADOMs, Device Manager,
  and policy packages.
- [Fortinet, *FortiOS REST API* reference documentation.](https://docs.fortinet.com/document/fortigate/8.0.0/administration-guide/940602/using-apis)
- [Fortinet, `fortinet.fortios` Ansible Collection documentation.](https://galaxy.ansible.com/fortinet/fortios)
- [Fortinet NSE Training Institute, *NSE 4: FortiGate Infrastructure*
  course (SD-WAN and central management domains).](https://training.fortinet.com/local/staticpage/view.php?page=nse_4)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — FortiOS 7.6.x
  baseline used throughout this volume.

**Knowledge checks**

1. How does an SD-WAN health-check differ from a simple interface up/down
   status check, and why does that distinction matter for path
   selection?
2. What problem does FortiManager's install preview solve for a
   multi-device fleet, and how does it relate to the plan/apply
   separation pattern introduced in [Volume I](../../volume-001-enterprise-engineering-foundations/README.md)?
3. Name two things to check when a REST API call returns a `401`/`403`
   response.
4. Why should a new automation stitch capable of a `ban-ip` action be
   piloted in a monitor-only mode before enabling the action broadly?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each task under SD-WAN, central
management, automation, and troubleshooting** — the operational half of the NSE 4
*Routing* objective plus the day-two skills the exam expects — mapped in the volume
README's coverage tables. Every command is a real FortiOS 7.6 CLI action; each lab ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.5** — a FortiGate on FortiOS 7.6 with two WAN
interfaces (for SD-WAN), FortiGuard reachability, and admin access. **Cost:** none
beyond lab resources.

### Lab 8.1 — SD-WAN zones and members (Topic: SD-WAN setup)

**Objective:** Create an SD-WAN with two underlay members.

```text
config system sdwan
    set status enable
    config zone
        edit virtual-wan-link
        next
    end
    config members
        edit 1
            set interface port1
            set zone virtual-wan-link
            set gateway 203.0.113.1
        next
        edit 2
            set interface port4
            set zone virtual-wan-link
            set gateway 198.51.100.1
        next
    end
end
diagnose sys sdwan member
```

**Expected result:** `port1` and `port4` join the SD-WAN zone; `diagnose sys sdwan
member` lists both as sequence members — SD-WAN abstracts multiple underlays into one
logical egress the rules steer over.

**Negative test:** reference `port1` in a normal static route while it is an SD-WAN
member; FortiOS steers via SD-WAN rules instead — membership changes how egress is
selected.

**Cleanup:** `set status disable` under `config system sdwan` after the later labs.

### Lab 8.2 — Performance SLA and health checks (Topic: SD-WAN SLA)

**Objective:** Measure link health with an active SLA probe.

```text
config system sdwan
    config health-check
        edit fgd-ping
            set server 208.91.112.53
            set members 1 2
            set protocol ping
            config sla
                edit 1
                    set latency-threshold 150
                    set packetloss-threshold 3
                next
            end
        next
    end
end
diagnose sys sdwan health-check
```

**Expected result:** each member reports live latency, jitter, and packet loss, and an
`in-sla`/`out-of-sla` state — the SLA is the signal SD-WAN rules use to keep sessions on
links that meet the application's requirements.

**Negative test:** build steering rules with no health-check; SD-WAN cannot tell a
brown-out link from a healthy one and keeps sending traffic into loss — the SLA probe is
what makes steering application-aware.

**Cleanup:** removed with the SD-WAN block in Lab 8.1 cleanup.

### Lab 8.3 — SD-WAN steering rules (Topic: SD-WAN rules)

**Objective:** Steer an application over the best-quality member.

```text
config system sdwan
    config service
        edit 1
            set name critical-apps
            set mode sla
            set dst all
            config sla
                edit fgd-ping
                    set id 1
                next
            end
            set priority-members 1 2
        next
    end
end
diagnose sys sdwan service
```

**Expected result:** `critical-apps` traffic prefers the member meeting the SLA and
fails over to the next when it degrades; `diagnose sys sdwan service` shows the chosen
member and order — rules translate link health into per-application path selection.

**Negative test:** set `mode manual` pinned to one member and pull that link; traffic
is dropped instead of failing over — `mode sla` with priority members is what makes
steering resilient.

**Cleanup:** removed with the SD-WAN block in Lab 8.1 cleanup.

### Lab 8.4 — Central management and automation (Topic: FortiManager / automation stitches)

**Objective:** Enable FortiManager management and build an automation stitch.

```text
config system central-management
    set type fortimanager
    set fmg 10.0.0.240
end
config system automation-trigger
    edit admin-login-trigger
        set event-type event-log
        set logid 32001
    next
end
config system automation-action
    edit notify-admins
        set action-type email
        set email-to soc@example.com
        set email-subject "FortiGate admin login"
    next
end
config system automation-stitch
    edit login-alert
        set trigger admin-login-trigger
        set action notify-admins
    next
end
```

**Expected result:** the FortiGate is registerable to FortiManager for centralized
policy, and the stitch fires an email whenever an admin logs in — automation turns Fabric
events into responses without an operator watching logs.

**Negative test:** define a trigger with no action (or vice versa); nothing happens —
the stitch must bind a trigger to an action to automate.

**Cleanup:** delete the stitch, action, and trigger; unset central-management if lab-only.

### Lab 8.5 — Structured troubleshooting (Topic: Troubleshooting)

**Objective:** Trace a flow end-to-end with debug flow.

```text
diagnose debug reset
diagnose debug flow filter addr 10.10.10.20
diagnose debug flow show function-name enable
diagnose debug flow trace start 20
diagnose debug enable
# generate traffic from 10.10.10.20, then:
diagnose debug disable
```

**Expected result:** a step-by-step trace showing the ingress interface, the matched
policy, any NAT, the route lookup, and the egress interface — `diagnose debug flow` is
the definitive tool for answering "why is this traffic allowed/denied/misrouted?"

**Negative test:** guess at the cause by reading policies alone; `debug flow` shows the
*actual* matched policy and route, which often differs from the assumed one — trace,
don't guess.

**Cleanup:**

```text
diagnose debug reset
diagnose debug disable
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter added SD-WAN path selection on top of the routing foundation
from [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), validated automatic failover with a deliberate WAN1
outage, connected FGT-LAB-01 to centralized FortiManager management, and
exercised both REST API and Ansible-style automation, including an
event-driven automation stitch with an explicit guardrail discussion.
[Chapter 09](09-nse-4-fortios-administrator-training-and-enterprise-capstone.md) draws every subsystem from Chapters 04 through 08 together into
an end-to-end capstone build and validation exercise aligned to the NSE 4
blueprint.

- [ ] Can configure an SD-WAN zone, members, health-check, and an
      SLA-based rule.
- [ ] Can validate SD-WAN failover behavior using diagnostic commands.
- [ ] Can register a FortiGate to FortiManager and explain the policy
      package install workflow.
- [ ] Can call the FortiOS REST API and describe how Ansible automates
      FortiGate configuration.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
