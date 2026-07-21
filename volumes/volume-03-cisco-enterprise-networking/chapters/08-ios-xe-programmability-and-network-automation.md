# Chapter 08: IOS XE Programmability and Network Automation

![Lab flow for this chapter: a workstation queries DIST-01's Vlan10 interface over RESTCONF with curl, receiving a JSON response matching the CLI's running-config; a model-driven telemetry subscription (ID 101) streams state to the workstation, showing State Valid and an incrementing Sent Records counter; an Ansible playbook run against the cisco.ios collection reports changed on its first run (VLANs created) and ok with no changed tasks on a second, identical run, confirming idempotency. As a negative test, the same RESTCONF query repeated with an intentionally wrong password returns HTTP 401 Unauthorized, confirming RESTCONF enforces the same AAA credentials as CLI/SSH.](../../../diagrams/volume-03-cisco-enterprise-networking/chapter-08-netconf-restconf-telemetry-ansible-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: programmatic access to a Catalyst 9000 switch over RESTCONF, model-driven telemetry, and an idempotent Ansible playbook run.*

## Learning Objectives

- Explain the model-driven programmability stack — YANG data models,
  NETCONF, RESTCONF, and gNMI — available on IOS XE and how each differs
  from traditional CLI-based automation.
- Configure and query a Catalyst 9000 switch over NETCONF and RESTCONF.
- Configure model-driven telemetry to stream operational state to a
  collector without polling.
- Use IOS XE's on-box automation surfaces — Embedded Event Manager (EEM)
  and the Guest Shell Python environment — for local automation tasks.
- Automate IOS XE configuration from off-box tooling using the Cisco
  `ios` Ansible collection.
- Validate programmability sessions and diagnose common NETCONF/RESTCONF
  and telemetry failures.

## Theory and Architecture

### Why model-driven programmability

The CLI configuration shown throughout this volume is precise and
familiar, but it is text meant for a human, not a well-defined data
structure — parsing `show` command output reliably across IOS XE releases
is fragile, and CLI has no native mechanism to notify an external system
when state changes. IOS XE's model-driven programmability stack solves
both problems: configuration and operational state are defined by
**YANG** data models, and three protocols let external tooling read and
write against those models directly, without CLI screen-scraping.

### YANG data models

**YANG ([RFC 7950](https://www.rfc-editor.org/rfc/rfc7950))** is a data modeling language that defines the
structure, types, and constraints of configuration and operational data
as a hierarchical, strongly typed tree. IOS XE ships three families of
YANG models:

- **Native (Cisco-IOS-XE) models** — a near-1:1 mapping to the IOS XE
  CLI's own configuration tree; the most complete coverage of
  platform-specific features, at the cost of being Cisco-specific.
- **OpenConfig models** — vendor-neutral models developed by a
  multi-vendor working group, covering common configuration areas
  (interfaces, BGP, ACLs) with the same schema across supporting vendors,
  trading some platform-specific depth for portability across a
  multi-vendor estate.
- **IETF models** — standards-track models (for example,
  `ietf-interfaces`) with the broadest cross-vendor support but the
  narrowest feature coverage.

A design that must stay portable across vendors favors OpenConfig/IETF
models where they cover the needed feature; a design that needs full
access to Cisco-specific features (StackWise Virtual state, TrustSec
configuration) uses native models.

### NETCONF, RESTCONF, and gNMI

Three transport protocols expose the same underlying YANG-modeled data,
each suited to a different automation style:

| Protocol | Transport/encoding | Operating model | Typical use |
| --- | --- | --- | --- |
| NETCONF ([RFC 6241](https://www.rfc-editor.org/rfc/rfc6241)) | SSH, XML | Full transactional config (candidate/running datastores, validate, commit) | Configuration management tools needing atomic, validated changes |
| RESTCONF ([RFC 8040](https://www.rfc-editor.org/rfc/rfc8040)) | HTTPS, XML or JSON | Stateless REST-style CRUD over the same YANG models | Scripts and web-style integrations that want simple GET/PATCH/POST semantics |
| gNMI | gRPC (HTTP/2), Protobuf | Unified get/set/subscribe in one protocol | High-performance streaming telemetry and configuration from modern automation/observability platforms |

NETCONF's candidate-datastore model is the closest analog to a database
transaction: a client edits the candidate datastore, validates it, and
only then commits it to running configuration — meaning a partially
invalid change can be caught and discarded before it ever touches the
live device, something raw CLI paste cannot guarantee.

### Model-driven telemetry

Traditional monitoring polls a device on an interval (`show` commands or
SNMP `GET`), which trades data freshness for polling overhead and always
lags real device state by at least the polling interval. **Model-driven
telemetry (MDT)** instead has the device **push** YANG-modeled
operational data to a collector as it changes, using one of two delivery
models:

- **Dial-out (device-initiated)** — the device establishes the
  subscription and streaming session to a statically configured collector
  address; simplest to reason about and does not require the collector to
  reach the device.
- **Dial-in (collector-initiated)** — the collector establishes a gRPC
  (gNMI) or NETCONF session to the device and subscribes; better suited
  to environments where the collector's address changes or scales
  dynamically.

Telemetry subscriptions can stream **on-change** (only when a value
changes — efficient for state that is normally static) or **periodic**
(fixed interval — appropriate for continuously varying counters like
interface utilization).

### On-box automation: Guest Shell and EEM

IOS XE runs on Linux ([Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md)), and two features expose that underlying
platform for local automation:

- **Guest Shell** — a Linux container (CentOS/IOx-based application
  sandbox) running alongside IOSd, with Python pre-installed and a Python
  API (`cli` module) for issuing IOS XE CLI commands programmatically from
  inside the container. Useful for on-box scripts that react to local
  conditions faster than an off-box system could, or that need to run
  even if off-box connectivity is temporarily unavailable.
- **Embedded Event Manager (EEM)** — a native IOS XE event-action engine
  that triggers a defined action (CLI command, syslog message, email,
  or a Tcl/Python script) when a specified event occurs (a syslog
  pattern match, an interface state change, a CLI command being entered,
  a scheduled timer). EEM is the right tool for small, deterministic,
  device-local reactions; Guest Shell Python is the right tool for
  anything that benefits from a full Python environment and libraries.

### Off-box automation

Most enterprise-scale configuration management still originates off-box,
where changes are authored, reviewed, and version-controlled before being
pushed to devices ([Volume IX](../../volume-09-infrastructure-automation/README.md) covers the general automation architecture
this pattern belongs to). The **Cisco `ios` Ansible collection**
(`cisco.ios`) is the most common off-box tool for IOS XE specifically,
offering resource modules (`ios_vlans`, `ios_l3_interfaces`,
`ios_bgp_global`, and others) that manage configuration idempotently —
each module compares desired state to current state and only issues the
commands needed to close the gap, the same idempotency principle
introduced in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md). **pyATS/Genie**, Cisco's Python test and
automation framework, complements this for validation-focused automation
— parsing `show` command output into structured data for automated
post-change verification.

### Plug and Play (PnP) day-0 provisioning

[Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md) introduced day-0 bring-up conceptually; **Cisco Network Plug
and Play (PnP)** is the mechanism that removes even the initial
touch-per-device step. An unconfigured switch, on first boot, discovers a
PnP server (via DHCP option 43, DNS, or Cisco's cloud redirection
service) and downloads its initial configuration and software image
automatically — the foundation Catalyst Center's onboarding workflow
([Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md)) builds on for zero-touch fleet provisioning.

## Design Considerations

- **Protocol selection** — choose NETCONF when a tool needs transactional,
  validate-then-commit configuration changes; choose RESTCONF for simple
  scripted integrations that map naturally to REST semantics; choose gNMI
  when the priority is high-volume streaming telemetry, or when the
  automation platform is already gNMI-native.
- **Native vs. OpenConfig model choice** — default to OpenConfig/IETF
  models for anything that must remain portable to non-Cisco platforms in
  a multi-vendor estate; accept the Cisco-specific native models where a
  feature (StackWise Virtual, TrustSec, wireless tags from [Chapter 5](05-catalyst-wireless-architecture-and-operations.md)) has
  no OpenConfig equivalent.
- **Telemetry delivery model** — prefer dial-out telemetry for
  predictable, centrally located collectors; reserve dial-in for
  environments where the collector's reachability or address is not
  stable enough for the device to dial toward reliably.
- **EEM scope discipline** — treat EEM applets as an emergency/tactical
  tool for a specific device-local condition, not a substitute for
  proper off-box automation and version-controlled configuration; EEM
  logic that only exists on one device's running configuration is
  invisible to code review and easy to lose during a device replacement.
- **Guest Shell resource allocation** — Guest Shell shares the platform's
  CPU/memory with IOSd; size and monitor any on-box Python workload so it
  cannot starve the control plane, and prefer off-box execution for
  anything resource-intensive or long-running.
- **RBAC for programmability interfaces** — NETCONF/RESTCONF/gNMI
  sessions authenticate through the same AAA framework as CLI access
  ([Chapter 7](07-cisco-identity-access-control-and-segmentation.md)); scope automation service accounts to the minimum privilege
  and command/model access actually required, the same least-privilege
  principle applied to human administrator accounts.

## Implementation and Automation

### Enabling NETCONF, RESTCONF, and gNMI

```text
DIST-01(config)# netconf-yang
DIST-01(config)# restconf
DIST-01(config)# ip http secure-server
DIST-01(config)# gnmi-yang
DIST-01(config)# gnmi-yang server
```

RESTCONF requires the HTTPS server; never enable `ip http server`
(unencrypted) as a substitute — RESTCONF traffic must run over TLS.

### Querying interface state with RESTCONF

```bash
curl -k -u netadmin:<PASSWORD> \
  -H "Accept: application/yang-data+json" \
  https://10.10.99.2/restconf/data/ietf-interfaces:interfaces/interface=Vlan10
```

Example response (abbreviated):

```json
{
  "ietf-interfaces:interface": {
    "name": "Vlan10",
    "type": "iana-if-type:l3ipvlan",
    "enabled": true,
    "ietf-ip:ipv4": {
      "address": [
        { "ip": "10.10.10.2", "netmask": "255.255.255.0" }
      ]
    }
  }
}
```

### Pushing configuration with NETCONF

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target><candidate/></target>
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Vlan>
            <name>30</name>
            <description>IOT-DEVICES</description>
            <ip>
              <address>
                <primary>
                  <address>10.10.30.1</address>
                  <mask>255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Vlan>
        </interface>
      </native>
    </config>
  </edit-config>
</rpc>
```

A NETCONF client (a Python script using `ncclient`, or a broader
orchestration platform) sends this `edit-config` against the candidate
datastore, issues `validate`, and only then issues `commit` — the
transactional workflow described in Theory and Architecture.

### Model-driven telemetry (dial-out, gRPC)

```text
DIST-01(config)# telemetry ietf subscription 101
DIST-01(config-mdt-subs)# encoding encode-kvgpb
DIST-01(config-mdt-subs)# filter xpath /interfaces-ios-xe-oper:interfaces/interface
DIST-01(config-mdt-subs)# source-address 10.10.99.2
DIST-01(config-mdt-subs)# stream yang-push
DIST-01(config-mdt-subs)# update-policy periodic 3000
DIST-01(config-mdt-subs)# receiver ip address 10.10.99.50 57500 protocol grpc-tcp
```

`update-policy periodic 3000` streams the subscribed path every 30
seconds (in hundredths of a second); an on-change policy is used instead
for state that should only stream when it actually changes.

### Guest Shell Python

```text
DIST-01# guestshell enable
DIST-01# guestshell run bash
[guestshell@DIST-01 ~]$ python3
>>> from cli import cli
>>> print(cli("show version | include Version"))
```

### EEM applet example

```text
DIST-01(config)# event manager applet UPLINK-DOWN-NOTIFY
DIST-01(config-applet)# event syslog pattern "%LINK-3-UPDOWN: Interface Port-channel1, changed state to down"
DIST-01(config-applet)# action 1.0 syslog msg "Primary uplink Port-channel1 went down - paging on-call"
DIST-01(config-applet)# action 2.0 cli command "enable"
DIST-01(config-applet)# action 3.0 cli command "show etherchannel summary"
```

### Ansible playbook using the `cisco.ios` collection

```yaml
---
- name: Configure standard VLANs across access switches
  hosts: catalyst_access
  gather_facts: false
  connection: network_cli
  vars:
    ansible_network_os: cisco.ios.ios
  tasks:
    - name: Ensure standard VLANs exist
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 10
            name: USERS
          - vlan_id: 20
            name: VOICE
          - vlan_id: 99
            name: MGMT
        state: merged
```

Running this playbook against the same inventory repeatedly changes
nothing after the first successful run — the resource module compares
desired to actual state before issuing any command, the idempotency
guarantee introduced in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md) and required of any production
automation workflow.

## Validation and Troubleshooting

```text
DIST-01# show netconf-yang sessions
DIST-01# show netconf-yang statistics
DIST-01# show platform software yang-management process state
DIST-01# show restconf
DIST-01# show telemetry ietf subscription 101 detail
DIST-01# guestshell status
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| NETCONF session refused | `netconf-yang` not enabled, or SSH/AAA authentication failing for the automation account | `show netconf-yang sessions`, confirm the account authenticates via normal SSH first |
| RESTCONF request returns 404 for a valid path | URL path doesn't match the YANG model's actual container/list hierarchy, or wrong model family (native vs. IETF) used in the path | Confirm the exact YANG path with `show platform software yang-management process state` or the model's `.yang` file |
| RESTCONF request returns 401/403 | Local or AAA credentials invalid, or the account lacks sufficient privilege/authorization for the requested path | Confirm the account authenticates via TACACS+/local per [Chapter 7](07-cisco-identity-access-control-and-segmentation.md) and holds adequate privilege |
| Telemetry subscription shows `0` records sent | `source-address` unreachable from the collector, receiver port/protocol mismatch, or the filtered Xpath never changes (on-change policy with static data) | `show telemetry ietf subscription 101 detail`, confirm receiver reachability and the update-policy type |
| Guest Shell won't enable | Insufficient flash/bootflash space for the IOx container image | `show guestshell`, `dir bootflash:`, free space before retrying |
| Ansible playbook reports a task changed on every run (never converges) | A resource module receiving values it cannot fully represent (for example, a manually configured setting outside the module's managed attributes) causing a false diff each run | Run in `--check --diff` mode, compare against `running-config`, narrow the module's `config` scope to match what is actually managed |

## Security and Best Practices

- Never enable `ip http server` (plaintext); RESTCONF and any web-based
  management must run over `ip http secure-server` (TLS) only.
- Scope a dedicated automation service account per platform/protocol
  through the same TACACS+/RADIUS AAA framework from [Chapter 7](07-cisco-identity-access-control-and-segmentation.md), rather
  than reusing a human administrator's credentials for scripted access.
- Store NETCONF/RESTCONF/Ansible credentials and API tokens in a managed
  secrets store ([Volume IX](../../volume-09-infrastructure-automation/README.md)), never in plaintext playbooks or scripts
  committed to a repository.
- Restrict which hosts can reach NETCONF (port 830), RESTCONF (443), and
  gNMI (default 50051 or as configured) using management-plane ACLs
  (`control-plane host` or interface ACLs on the management VLAN), since
  these are configuration-write-capable interfaces equivalent in
  sensitivity to SSH.
- Review EEM applets and Guest Shell scripts with the same change-control
  rigor as off-box automation; a poorly written EEM applet with a broad
  syslog pattern match or an unbounded action loop can degrade or disable
  a device.
- Treat telemetry collector endpoints as sensitive infrastructure — a
  compromised collector receiving streamed operational state (interface
  counters, routing state, authentication session data) gains
  significant reconnaissance value against the network.
- Pin Ansible collection and pyATS/Genie versions in a lockfile-equivalent
  manner ([Volume IX](../../volume-09-infrastructure-automation/README.md)'s automation architecture) so a collection upgrade
  cannot silently change module behavior in a production pipeline.

## References and Knowledge Checks

**Authoritative references**

- Cisco, *IOS XE Programmability Configuration Guide*, current release.
- [RFC 7950](https://www.rfc-editor.org/rfc/rfc7950) (YANG 1.1), [RFC 6241](https://www.rfc-editor.org/rfc/rfc6241) (NETCONF), [RFC 8040](https://www.rfc-editor.org/rfc/rfc8040) (RESTCONF).
- OpenConfig Working Group, published YANG models (openconfig.net).
- Cisco `cisco.ios` Ansible Collection documentation (Ansible Galaxy /
  Cisco DevNet).

**Knowledge checks**

1. What advantage does NETCONF's candidate/commit workflow provide over
   pasting configuration directly into a CLI session?
2. When would a design choose OpenConfig models over Cisco native YANG
   models, and what is given up by doing so?
3. What is the practical difference between dial-out and dial-in
   telemetry, and when would a design prefer each?
4. When is an EEM applet the right tool versus an off-box Ansible
   playbook?
5. Why does a resource module like `ios_vlans` need to be idempotent, and
   what does a non-idempotent playbook run indicate about how it was
   written?

## Hands-On Lab

**Objective:** Enable NETCONF and RESTCONF on a Catalyst 9000 switch,
query and modify configuration over RESTCONF, configure a model-driven
telemetry subscription, and run an idempotent Ansible playbook against
the same device.

**Prerequisites**

- One Catalyst 9000 switch (or CML/virtual node) with IOS XE 17.x and
  console/SSH access.
- A workstation with `curl`, Python 3, `ansible-core`, and the
  `cisco.ios` collection installed (`ansible-galaxy collection install
  cisco.ios`).
- Network reachability from the workstation to the device's management
  interface.

**Procedure**

1. Enable NETCONF, RESTCONF, and the HTTPS server as shown in
   Implementation, then confirm both services report ready:

   ```text
   DIST-01# show netconf-yang sessions
   DIST-01# show restconf
   ```

2. From the workstation, query the device's VLAN 10 interface over
   RESTCONF:

   ```bash
   curl -k -u netadmin:<PASSWORD> \
     -H "Accept: application/yang-data+json" \
     https://<DEVICE_IP>/restconf/data/ietf-interfaces:interfaces/interface=Vlan10
   ```

   **Expected result:** a JSON response describing `Vlan10`'s
   configuration, matching what `show running-config interface Vlan10`
   reports on the device.

3. Configure the model-driven telemetry subscription from Implementation,
   pointing `receiver ip address` at the workstation (or a lab collector
   listening on the specified port), and confirm delivery:

   ```text
   DIST-01# show telemetry ietf subscription 101 detail
   ```

   **Expected result:** `State` shows `Valid` and `Sent Records`
   increments over successive checks.

4. Write the `catalyst_access` Ansible inventory and playbook from
   Implementation, then run it:

   ```bash
   ansible-playbook -i inventory.ini configure-vlans.yml
   ```

   **Expected result:** the play reports `changed` for the target host on
   the first run (VLANs created).

5. Re-run the identical playbook and confirm idempotency:

   ```bash
   ansible-playbook -i inventory.ini configure-vlans.yml
   ```

   **Expected result:** the play reports `ok` (no `changed` tasks),
   confirming the module correctly detected the desired state already
   matches actual state.

6. **Negative test:** attempt the same RESTCONF query from step 2 using
   an intentionally incorrect password.

   ```bash
   curl -k -u netadmin:WrongPassword \
     -H "Accept: application/yang-data+json" \
     https://<DEVICE_IP>/restconf/data/ietf-interfaces:interfaces/interface=Vlan10
   ```

   **Expected result:** the request returns HTTP `401 Unauthorized`,
   confirming RESTCONF enforces the same AAA credentials as CLI/SSH
   access rather than allowing an unauthenticated read.

**Cleanup**

- Remove the lab telemetry subscription and lab-created VLAN if the
  device is shared:

  ```text
  DIST-01(config)# no telemetry ietf subscription 101
  DIST-01(config)# no vlan 30
  ```

- Disable Guest Shell if it was enabled only for this lab:

  ```text
  DIST-01# guestshell destroy
  ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

IOS XE's programmability stack — YANG-modeled data exposed through
NETCONF, RESTCONF, and gNMI, plus on-box automation through Guest Shell
and EEM — gives automation tooling a structured, versionable alternative
to CLI screen-scraping for both configuration and telemetry. Off-box
tools like the `cisco.ios` Ansible collection build on that same
model-driven foundation to deliver the idempotent, version-controlled
configuration management pattern established across this encyclopedia in
[Volume I](../../volume-01-enterprise-engineering-foundations/README.md) and [Volume IX](../../volume-09-infrastructure-automation/README.md).

- [ ] Can explain the YANG/NETCONF/RESTCONF/gNMI stack and when to choose
      each transport.
- [ ] Can enable and query a device over RESTCONF and push a change over
      NETCONF.
- [ ] Can configure a model-driven telemetry subscription.
- [ ] Can distinguish appropriate use of EEM/Guest Shell on-box automation
      from off-box Ansible automation.
- [ ] Completed the hands-on lab, including the idempotency check and the
      unauthorized-access negative test.
