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
notification, run a local CLI script) directly on the FortiGate. For
scheduled rather than event-driven execution, `config system auto-script`
runs a stored block of CLI commands on a fixed interval and retains their
output on the box. Every one of these surfaces runs *FortiOS commands*: the
appliance has no user shell and executes no uploaded `.sh`/`.py` files or
compiled binaries — a boundary examined under Implementation below.

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

### FortiOS scripting: what runs on the box, and what does not

A FortiGate is a closed appliance, not a general-purpose Linux host: there
is no user shell, and you cannot upload a `.sh`, `.py`, or compiled binary
and execute it the way you can on a managed endpoint. "Scripting" on
FortiOS means running **FortiOS CLI commands** (and, on FortiManager,
**Tcl**) through one of several native mechanisms — each of which operates
on configuration and operational commands, never arbitrary code.

**Plain CLI scripts.** The simplest script is an ordered batch of the same
`config`/`execute`/`get`/`diagnose` commands an operator would type. It can
be pasted into the console, or pushed from FortiManager (*Device Manager →
CLI Scripts*, run against the running configuration or the device database)
to target many devices at once.

**Scheduled on-box scripts — `config system auto-script`.** FortiOS stores
named command scripts and runs them itself on an interval, capturing a
bounded amount of output for later retrieval:

```text
FGT-LAB-01 # config system auto-script
FGT-LAB-01 (auto-script) # edit "healthcheck"
FGT-LAB-01 (healthcheck) # set interval 300
FGT-LAB-01 (healthcheck) # set repeat 0
FGT-LAB-01 (healthcheck) # set start auto
FGT-LAB-01 (healthcheck) # set output-size 10
FGT-LAB-01 (healthcheck) # set script "get system performance status
diagnose sys top 5"
FGT-LAB-01 (healthcheck) # next
FGT-LAB-01 (auto-script) # end

FGT-LAB-01 # diagnose system auto-script healthcheck
```

`interval` is in seconds, `repeat 0` runs indefinitely, `start auto` begins
the schedule at boot, and `output-size` caps retained output in KB;
`diagnose system auto-script <name>` prints the last captured run.

**Event-driven scripts — the CLI-script automation action.** Alongside the
`ban-ip` action shown above, an automation stitch can run a block of CLI
commands via the `cli-script` action type, so a log event, IPS detection,
schedule, or inbound webhook can reconfigure the device with no external
orchestrator. Trigger variables such as `%%log.srcip%%` are substituted
into the script at run time:

```text
FGT-LAB-01 # config system automation-action
FGT-LAB-01 (automation-action) # edit "Snapshot-On-Event"
FGT-LAB-01 (Snapshot-On-Event) # set action-type cli-script
FGT-LAB-01 (Snapshot-On-Event) # set script "get system status
diagnose sys session stat"
FGT-LAB-01 (Snapshot-On-Event) # next
FGT-LAB-01 (automation-action) # end
```

For logic that genuinely needs branching, loops, or variables — or that
must reach systems beyond the FortiGate — a stitch's `webhook`,
`aws-lambda`, or `azure-function` action hands off to a real program hosted
off-box, the supported way to run arbitrary code *from* an automation event
without running it on the appliance.

**Boot / zero-touch scripts — `config system auto-install`.** A
configuration file (`fgt_system.conf`) and, optionally, a firmware image
placed on a USB stick are applied automatically at boot — how a factory-
reset or field-replaced unit self-provisions with no operator at the
console.

**FortiManager and Tcl.** FortiManager CLI scripts come in two flavors,
plain *CLI* and *Tcl*, and Tcl is where real scripting logic (conditionals,
loops, per-device variables) lives; on the FortiGate itself Tcl support is
minimal, and CLI scripts, `auto-script`, and stitches are the practical
tools.

**Driven from outside.** In production, most "scripting" is external
config-management pushing state through the same REST API used above: the
Fortinet-published **Ansible** `fortinet.fortios` collection, the
**Terraform** `fortios` provider, and FortiManager's **JSON-RPC API**. None
of these run on the FortiGate; they render intended state and apply it over
the API.

**The boundary.** A hidden `fnsysctl` command exposes a few BusyBox-style
utilities (`ls`, `cat`, `df`, `ifconfig`) for low-level troubleshooting,
but it is not a scripting environment and is not a supported path to run
custom programs. If a task needs a language runtime or a third-party
binary, run it off-box and reach into the FortiGate through the REST API or
an Automation-Stitch webhook — the appliance executes FortiOS commands, and
nothing else.

> **Eval-VM note.** Both `config system auto-script` and Automation Stitches
> function under the FortiGate-VM evaluation license used throughout
> [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md),
> so the scheduled- and event-driven-script mechanisms here can be
> exercised on the same lab VM without a paid subscription.

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

**Eval FortiGate — capable (three-interface build).** SD-WAN needs at least two members. The evaluation
FortiGate-VM has three interfaces, so keep `port1` as the dedicated management/uplink and build the SD-WAN
from the other two — `port2` and `port3`. The eval has no second internet circuit, so those two members
front internal lab segments and the SLA probes (Lab 8.2) target reachable lab hosts; that is enough to
exercise zones, members, SLA, and steering without real dual-WAN.

**Objective:** Create an SD-WAN with two underlay members on the eval's spare interfaces.

```text
config system sdwan
    set status enable
    config zone
        edit virtual-wan-link
        next
    end
    config members
        edit 1
            set interface port2
            set zone virtual-wan-link
        next
        edit 2
            set interface port3
            set zone virtual-wan-link
        next
    end
end
diagnose sys sdwan member
```

`virtual-wan-link` is the built-in default SD-WAN zone, so the `edit virtual-wan-link` here re-enters the
existing zone rather than creating a new one. On a real dual-WAN box each member also takes `set gateway
<upstream-next-hop>` (the upstream router on that circuit); the eval's members are directly-connected lab
segments, so no member gateway is needed to probe a host on that member's own segment (Lab 8.2).

**Expected result:** `port2` and `port3` join the `virtual-wan-link` zone; `diagnose sys sdwan member`
lists both as sequence members — SD-WAN abstracts multiple underlays into one logical egress the rules
steer over, while `port1` stays out-of-band for management.

**Negative test:** try to bind a normal static route to `port2` (`config router static … set device
port2`) while it is an SD-WAN member; FortiOS **rejects** it — once an interface is an SD-WAN member you
route to it only through the zone (`set sdwan-zone virtual-wan-link`), never the member interface directly.
Membership changes how egress is expressed.

**Rollback:** `set status disable` under `config system sdwan` after the later labs.

### Lab 8.2 — Performance SLA and health checks (Topic: SD-WAN SLA)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Measure link health with an active SLA probe.

```text
config system sdwan
    config health-check
        edit lab-sla
            set server 10.30.1.10
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
`in-sla`/`out-of-sla` state. On the eval the probe host `10.30.1.10` sits on member 1's segment (`port2`),
so member 1 measures a real path and reports `in-sla`. Crucially, SD-WAN health-check probes are **pinned
to each member's egress interface** — they are not FIB-routed — so member 2's ping is forced out `port3`;
`10.30.1.10` is off `port3`'s subnet (`10.30.2.0/24`) with no gateway to reach it, so member 2 hits 100%
packet loss and shows `state: dead` (the extreme of failing SLA). That split is exactly the signal the
steering rule in Lab 8.3 uses to keep traffic on the healthy member. On a real dual-WAN, point `server` at
an internet host reachable over *both* circuits so each member is measured independently.

**Negative test:** build steering rules with no health-check; SD-WAN cannot tell a
brown-out link from a healthy one and keeps sending traffic into loss — the SLA probe is
what makes steering application-aware.

**Rollback:** removed with the SD-WAN block in Lab 8.1 cleanup.

### Lab 8.3 — SD-WAN steering rules (Topic: SD-WAN rules)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Steer an application over the best-quality member.

This rule binds to the `lab-sla` health-check from Lab 8.2 (`config sla / edit lab-sla`) — run 8.2 first,
or the SLA reference resolves to nothing and the rule can never enter `sla` mode.

```text
config system sdwan
    config service
        edit 1
            set name critical-apps
            set mode sla
            set dst all
            config sla
                edit lab-sla
                    set id 1
                next
            end
            set priority-members 1 2
        next
    end
end
diagnose sys sdwan service
```

**Expected result:** `critical-apps` traffic prefers the member meeting the SLA and fails over to the next
when it degrades; `diagnose sys sdwan service` shows the chosen member and order. On the eval, member 1
(`port2`) is the `in-sla` member from Lab 8.2, so the rule selects it first — rules translate link health
into per-application path selection.

**Negative test:** set `mode manual` pinned to one member and pull that link; traffic
is dropped instead of failing over — `mode sla` with priority members is what makes
steering resilient.

**Rollback:** removed with the SD-WAN block in Lab 8.1 cleanup.

### Lab 8.4 — Central management and automation (Topic: FortiManager / automation stitches)

**Eval FortiGate — mixed.** The automation-stitch half runs on the eval; **FortiManager** central management needs a separate FortiManager appliance (not part of the eval) — treat that portion as design.

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

**Rollback:** delete the stitch, action, and trigger; unset central-management if lab-only.

### Lab 8.5 — Structured troubleshooting (Topic: Troubleshooting)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

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

**Rollback:**

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
