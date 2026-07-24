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

This chapter carries a topic-level walkthrough lab for the automation exam
topics that map here — **CCNA Domain 6 (Automation and Programmability)**,
**ENCOR Domain 6 (Automation and AI) plus 4.6**, and **all of ENAUTO
(300-435 Enterprise Automation)** — mapped in the volume README's coverage
tables; the design exam **ENSLD (300-420)** is covered by the Design
Exercise below. Labs use IOS XE, Python, NETCONF/RESTCONF, Ansible, and the
Catalyst Center / vManage / Meraki REST APIs. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.37** — an IOS XE device with
`netconf-yang`/`restconf` enabled, a Python 3 host with `ncclient`,
`netmiko`, `requests`, and Ansible installed, and API access to Catalyst
Center (`$DNAC`), vManage (`$VMANAGE`), and a Meraki org (`$MERAKI_KEY`)
where noted. **Cost:** none beyond lab resources.

### Lab 8.1 — Use version control with git (ENAUTO 1.1)

**Objective:** Track configuration/scripts with git.

```bash
git init netauto && cd netauto
git add configs/ && git commit -m "baseline"
git clone https://example.com/net-templates.git
git log --oneline
```

**Expected result:** a versioned repo with a commit history — infrastructure
and scripts as code, with rollback.

**Negative test:** editing configs on the device with no git history leaves
no rollback point; commit before change.

**Cleanup:** `rm -rf netauto`.

### Lab 8.2 — Compare REST and RPC API styles (ENAUTO 1.2, ENCOR 6.5)

**Objective:** Read a REST response and its status code.

```bash
curl -sk -o /dev/null -w '%{http_code}\n' -u admin:pw https://$DEV/restconf/data/ietf-interfaces:interfaces
```

**Expected result:** a `200` (resource-oriented REST); RPC styles (NETCONF,
gRPC) instead call an operation — the two API paradigms.

**Negative test:** expecting a NETCONF `<edit-config>` RPC on a REST URL; the
styles are not interchangeable.

**Cleanup:** none (read-only).

### Lab 8.3 — Describe API consumption patterns (ENAUTO 1.3)

**Objective:** Handle pagination/rate-limits when consuming an API.

```bash
curl -sk -u admin:pw "https://$DNAC/dna/intent/api/v1/network-device?limit=10&offset=0" -H "X-Auth-Token: $DT" | jq '.response | length'
```

**Expected result:** a bounded page of results — the pattern (paginate, back
off on 429, cache tokens) for consuming large APIs.

**Negative test:** requesting all devices unpaginated can time out or hit
rate limits; paginate.

**Cleanup:** none (read-only).

### Lab 8.4 — Interpret a Python script (ENAUTO 1.4, ENCOR 6.1)

**Objective:** Read a script's data types, functions, and classes.

```bash
python3 - <<'PY'
devices = [{"name":"R1","role":"core"}]   # list of dicts
def by_role(d, role): return [x["name"] for x in d if x["role"]==role]
print(by_role(devices, "core"))
PY
```

**Expected result:** `['R1']` — list/dict data types and a function applied
to structured device data.

**Negative test:** indexing a dict with an integer key that does not exist
raises `KeyError`; know the data type before indexing.

**Cleanup:** none.

### Lab 8.5 — Use a Python virtual environment (ENAUTO 1.5)

**Objective:** Isolate script dependencies.

```bash
python3 -m venv venv && source venv/bin/activate
pip install ncclient netmiko requests
pip freeze | head
```

**Expected result:** an isolated venv with pinned libraries — reproducible,
conflict-free automation dependencies.

**Negative test:** installing globally can break other tools' dependencies;
the venv isolates them.

**Cleanup:** `deactivate && rm -rf venv`.

### Lab 8.6 — Describe network configuration tools (ENAUTO 1.6, ENCOR 6.7)

**Objective:** Contrast agent vs agentless config tools.

```bash
ansible --version | head -1   # agentless (SSH/NETCONF)
```

**Expected result:** Ansible (agentless, push over SSH/NETCONF) versus
Puppet/Chef (agent-based, pull) — the orchestration models the exam compares.

**Negative test:** expecting Ansible to run without SSH/API reachability to
the device; agentless still needs a transport.

**Cleanup:** none.

### Lab 8.7 — Identify JSON from a YANG model (ENAUTO 2.1, ENCOR 6.2)

**Objective:** Read a JSON instance of a YANG interface model.

```bash
curl -sk -u admin:pw https://$DEV/restconf/data/ietf-interfaces:interfaces -H 'Accept: application/yang-data+json' | jq '.["ietf-interfaces:interfaces"].interface[0].name'
```

**Expected result:** the interface name from a YANG-modeled JSON payload —
structured, model-validated data.

**Negative test:** hand-editing JSON that violates the YANG model is rejected
on write; the model is the schema.

**Cleanup:** none (read-only).

### Lab 8.8 — Identify XML from a YANG model (ENAUTO 2.2)

**Objective:** Read the XML instance of the same model over NETCONF.

```bash
curl -sk -u admin:pw https://$DEV/restconf/data/ietf-interfaces:interfaces -H 'Accept: application/yang-data+xml' | head -5
```

**Expected result:** the XML-encoded interface list — NETCONF's encoding of
the same YANG model.

**Negative test:** mixing JSON and XML content types in one request errors;
the Accept header selects one encoding.

**Cleanup:** none (read-only).

### Lab 8.9 — Interpret a YANG module tree (ENAUTO 2.3, ENCOR 6.3)

**Objective:** Render a YANG model as a tree (RFC 8340).

```bash
pyang -f tree ietf-interfaces.yang | head -20
```

**Expected result:** the module's container/list/leaf tree — the structure a
NETCONF/RESTCONF payload must follow.

**Negative test:** a config path not present in the tree is invalid; the tree
defines the addressable data.

**Cleanup:** none.

### Lab 8.10 — Compare data models (ENAUTO 2.4)

**Objective:** Distinguish native, IETF, and OpenConfig models.

```bash
curl -sk -u admin:pw https://$DEV/restconf/data/Cisco-IOS-XE-native:native -H 'Accept: application/yang-data+json' | jq 'keys' 2>/dev/null | head
```

**Expected result:** the Cisco native model (vs vendor-neutral OpenConfig/
IETF) — native exposes everything, OpenConfig standardizes across vendors.

**Negative test:** an OpenConfig path unsupported on the platform returns
empty/error; check model support per device.

**Cleanup:** none (read-only).

### Lab 8.11 — Compare NETCONF and RESTCONF (ENAUTO 2.5, ENCOR 4.6)

**Objective:** Confirm both interfaces on the device.

```text
DEV# show netconf-yang sessions
DEV# show platform software yang-management process
```

**Expected result:** NETCONF (SSH/830, transactional, candidate datastore)
and RESTCONF (HTTPS, resource-oriented) both running — two management APIs on
one YANG backend.

**Negative test:** expecting RESTCONF's per-resource edits to be transactional
like NETCONF's candidate/commit; RESTCONF commits per request.

**Cleanup:** none (read-only).

### Lab 8.12 — Manage a device with Netmiko (ENAUTO 3.1)

**Objective:** Push a command via SSH with Netmiko.

```bash
python3 - <<'PY'
from netmiko import ConnectHandler
d={"device_type":"cisco_ios","host":"R1","username":"admin","password":"pw"}
c=ConnectHandler(**d); print(c.send_command("show ip int brief")); c.disconnect()
PY
```

**Expected result:** the CLI output returned to Python — screen-scraping
automation for devices without an API.

**Negative test:** Netmiko against a device with a non-standard prompt hangs;
set the correct `device_type`.

**Cleanup:** none.

### Lab 8.13 — Configure with ncclient/NETCONF (ENAUTO 3.2)

**Objective:** Edit config in a single transaction over NETCONF.

```bash
python3 - <<'PY'
from ncclient import manager
cfg='<config><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>Loopback9</name><enabled>true</enabled></interface></interfaces></config>'
with manager.connect(host="R1",username="admin",password="pw",hostkey_verify=False) as m:
    print(m.edit_config(target="running",config=cfg).ok)
PY
```

**Expected result:** `True` — `Loopback9` created in a single transaction via
NETCONF.

**Negative test:** malformed XML that violates the model returns an
`rpc-error`; NETCONF validates before applying.

**Cleanup:** delete `Loopback9` via NETCONF.

### Lab 8.14 — Configure via RESTCONF with requests (ENAUTO 3.3)

**Objective:** Create config with a Python `requests` PUT.

```bash
python3 - <<'PY'
import requests; requests.packages.urllib3.disable_warnings()
url="https://R1/restconf/data/ietf-interfaces:interfaces/interface=Loopback8"
body={"ietf-interfaces:interface":{"name":"Loopback8","type":"iana-if-type:softwareLoopback","enabled":True}}
r=requests.put(url,json=body,auth=("admin","pw"),headers={"Content-Type":"application/yang-data+json"},verify=False)
print(r.status_code)
PY
```

**Expected result:** `201`/`204` — `Loopback8` created via RESTCONF.

**Negative test:** a PUT to a URL whose key does not match the body errors;
the resource key and payload must agree.

**Cleanup:** RESTCONF DELETE on the interface.

### Lab 8.15 — Configure with Ansible (ENAUTO 3.4)

**Objective:** Apply IOS XE config with an Ansible playbook.

```bash
cat > pb.yml <<'YAML'
- hosts: routers
  gather_facts: no
  tasks:
    - cisco.ios.ios_config:
        lines: ["ip domain name lab.example"]
YAML
ansible-playbook -i inventory pb.yml
```

**Expected result:** `changed=1` — the domain name pushed idempotently; a
re-run reports `ok` (no change).

**Negative test:** a playbook without idempotent modules (raw CLI every run)
re-applies unnecessarily; use the declarative modules.

**Cleanup:** remove the config and `rm pb.yml`.

### Lab 8.16 — Configure model-driven telemetry (ENAUTO 3.5)

**Objective:** Subscribe to interface counters via MDT.

```text
DEV(config)# telemetry ietf subscription 101
DEV(config-mdt-subs)# encoding encode-kvgpb
DEV(config-mdt-subs)# filter xpath /interfaces-state/interface/statistics
DEV(config-mdt-subs)# stream yang-push
DEV(config-mdt-subs)# update-policy periodic 1000
DEV(config-mdt-subs)# receiver ip address 10.0.0.80 57500 protocol grpc-tcp
DEV# show telemetry ietf subscription 101 detail
```

**Expected result:** subscription 101 streaming stats every 10s to the
collector — push-based telemetry replacing SNMP polling.

**Negative test:** an XPath that matches no data streams nothing; verify the
path against the YANG tree.

**Cleanup:** `no telemetry ietf subscription 101`.

### Lab 8.17 — Compare telemetry models (ENAUTO 3.6)

**Objective:** Distinguish dial-in from dial-out telemetry.

```text
DEV# show telemetry connection all
```

**Expected result:** dial-out (device initiates to the collector, as in Lab
8.16) vs dial-in (collector subscribes via gNMI/NETCONF) — the two
publication/subscription models.

**Negative test:** a dial-out subscription to an unreachable receiver keeps
retrying and streams nothing; the receiver must be up.

**Cleanup:** none (read-only).

### Lab 8.18 — Use telemetry data in troubleshooting (ENAUTO 3.7)

**Objective:** Correlate a telemetry metric to an event.

```text
DEV# show telemetry ietf subscription 101 receiver
```

**Expected result:** the receiver state and last-update time — streaming
telemetry gives sub-second resolution on a counter SNMP would sample too
coarsely.

**Negative test:** SNMP polled every 5 minutes misses a 10-second microburst
telemetry catches; the resolution is the point.

**Cleanup:** none (read-only).

### Lab 8.19 — Describe Day 0 provisioning (ENAUTO 3.8)

**Objective:** Read the ZTP/PnP onboarding state.

```text
DEV# show pnp status
DEV# show pnp profile
```

**Expected result:** the Plug-and-Play/ZTP profile a factory-fresh device
uses to fetch its config from a PnP/DHCP server — zero-touch onboarding.

**Negative test:** a device with an existing startup-config skips ZTP; Day 0
provisioning applies only to unconfigured devices.

**Cleanup:** none (read-only).

### Lab 8.20 — Compare traditional and software-defined networks (ENAUTO 4.1, CCNA 6.2)

**Objective:** Read the controller-managed vs device-by-device model.

```bash
curl -sk -H "X-Auth-Token: $DT" "$DNAC/dna/intent/api/v1/network-device/count" | jq '.response'
```

**Expected result:** a device count managed centrally by Catalyst Center — the
controller-based model versus box-by-box CLI.

**Negative test:** expecting central intent to reach a device Catalyst Center
does not manage; SDN control needs the device in inventory.

**Cleanup:** none (read-only).

### Lab 8.21 — Describe Catalyst Center features (ENAUTO 4.2, CCNA 6.3)

**Objective:** Read Catalyst Center's automation/assurance surface.

```bash
curl -sk -H "X-Auth-Token: $DT" "$DNAC/dna/intent/api/v1/site" | jq -r '.response[].name' | head
```

**Expected result:** the site hierarchy Catalyst Center automates
(design/policy/provision/assurance) — the controller's feature set.

**Negative test:** expecting assurance data for a site with no assigned
devices; features act on managed inventory.

**Cleanup:** none (read-only).

### Lab 8.22 — Implement Catalyst Center webhooks (ENAUTO 4.3)

**Objective:** Confirm an event webhook (outbound notification).

```bash
curl -sk -H "X-Auth-Token: $DT" "$DNAC/dna/intent/api/v1/event/subscription/rest" | jq -r '.[].name' 2>/dev/null | head
```

**Expected result:** a REST/webhook subscription pushing events to an
external system — event-driven automation.

**Negative test:** a webhook to an unreachable URL fails delivery silently;
verify the destination.

**Cleanup:** none (read-only).

### Lab 8.23 — Implement Catalyst Center API requests I (ENAUTO 4.4)

**Objective:** Run a template/command through the Catalyst Center API.

```bash
curl -sk -H "X-Auth-Token: $DT" "$DNAC/dna/intent/api/v1/network-device" | jq -r '.response[0] | "\(.hostname)\t\(.reachabilityStatus)"'
```

**Expected result:** device data returned via the Intent API — programmatic
network operations at controller scope.

**Negative test:** an expired auth token returns `401`; refresh the token
before the call.

**Cleanup:** none (read-only).

### Lab 8.24 — Implement Catalyst Center API requests II (ENAUTO 4.5)

**Objective:** Read command-runner/compliance via API.

```bash
curl -sk -H "X-Auth-Token: $DT" "$DNAC/dna/intent/api/v1/compliance" | jq -r '.response[0].complianceStatus' 2>/dev/null
```

**Expected result:** compliance status via API — automating audit at scale.

**Negative test:** a non-compliant device flagged by API but not remediated
stays out of policy; API read must pair with a remediation action.

**Cleanup:** none (read-only).

### Lab 8.25 — Troubleshoot Catalyst Center with the Intent API (ENAUTO 4.6)

**Objective:** Read a task's status to diagnose an automation failure.

```bash
curl -sk -H "X-Auth-Token: $DT" "$DNAC/dna/intent/api/v1/task/<taskId>" | jq -r '.response | "\(.isError)\t\(.progress)"'
```

**Expected result:** the task result (`isError`, progress) — the Intent API's
task object is where an automation failure's reason lives.

**Negative test:** assuming an API `202 Accepted` means success; it means
accepted — poll the task for the real outcome.

**Cleanup:** none (read-only).

### Lab 8.26 — Describe vManage API features (ENAUTO 5.1)

**Objective:** Read the vManage API surface.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device" | jq '.data | length'
```

**Expected result:** the device count via the vManage REST API — the SD-WAN
controller's programmable surface (config, monitoring, admin).

**Negative test:** calling the API without a valid session cookie returns
`403`; authenticate first.

**Cleanup:** none (read-only).

### Lab 8.27 — Script vManage API requests (ENAUTO 5.2)

**Objective:** Query vManage from Python.

```bash
python3 - <<'PY'
import requests,os; requests.packages.urllib3.disable_warnings()
s=requests.Session()
r=s.get(os.environ["VMANAGE"]+"/dataservice/device/monitor",cookies={"JSESSIONID":os.environ.get("JSID","")},verify=False)
print(r.status_code)
PY
```

**Expected result:** a `200` with device monitoring data — SD-WAN automation
in Python.

**Negative test:** a request missing the CSRF token on a POST is rejected;
GET works, mutating calls need the token.

**Cleanup:** none (read-only).

### Lab 8.28 — Construct vManage Administration API requests (ENAUTO 5.3)

**Objective:** Read admin data (users/settings) via API.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/admin/user" | jq -r '.data[].userName' | head
```

**Expected result:** the vManage users via the Administration API —
programmatic management-plane administration.

**Negative test:** an operator-role token cannot read admin endpoints;
RBAC scopes the API too.

**Cleanup:** none (read-only).

### Lab 8.29 — Script vManage configuration API requests (ENAUTO 5.4)

**Objective:** Read templates via the config API.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/template/device" | jq -r '.data[].templateName' | head
```

**Expected result:** device templates via the configuration API — automating
config-template lifecycle.

**Negative test:** pushing a template to a device with mismatched variables
fails attach; variables must resolve.

**Cleanup:** none (read-only).

### Lab 8.30 — Construct vManage Monitoring API requests (ENAUTO 5.5)

**Objective:** Read real-time monitoring via API.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device/bfd/sessions?deviceId=<ip>" | jq '.data | length'
```

**Expected result:** BFD session data via the Monitoring API — the telemetry
a dashboard or NOC tool consumes.

**Negative test:** a monitoring query for a device not in the fabric returns
empty; the device must be onboarded.

**Cleanup:** none (read-only).

### Lab 8.31 — Troubleshoot SD-WAN with vManage APIs (ENAUTO 5.6)

**Objective:** Diagnose an edge via the control-connections API.

```bash
curl -sk -b "$VT" "$VMANAGE/dataservice/device/control/connections?deviceId=<ip>" | jq -r '.data[] | "\(.["peer-type"])\t\(.state)"'
```

**Expected result:** control-connection state per controller via API — scripted
SD-WAN troubleshooting across many sites at once.

**Negative test:** reading one device's UI page does not scale to a 500-site
fabric; the API loops it.

**Cleanup:** none (read-only).

### Lab 8.32 — Describe Meraki features (ENAUTO 6.1)

**Objective:** Read the Meraki organizations via the Dashboard API.

```bash
curl -sk -H "X-Cisco-Meraki-API-Key: $MERAKI_KEY" "https://api.meraki.com/api/v1/organizations" | jq -r '.[].name'
```

**Expected result:** the cloud-managed orgs — Meraki's API-first, cloud
dashboard model.

**Negative test:** an API key without org access returns `404`/empty; the key
is scoped per admin.

**Cleanup:** none (read-only).

### Lab 8.33 — Create a network with the Meraki API (ENAUTO 6.2)

**Objective:** Create a Meraki network programmatically.

```bash
curl -sk -X POST -H "X-Cisco-Meraki-API-Key: $MERAKI_KEY" -H 'Content-Type: application/json' \
  "https://api.meraki.com/api/v1/organizations/<orgId>/networks" \
  -d '{"name":"lab-net","productTypes":["switch","wireless"]}' | jq -r '.id'
```

**Expected result:** a new network ID — zero-touch cloud provisioning via API.

**Negative test:** a POST exceeding the API rate limit returns `429`; back off
and retry.

**Cleanup:** DELETE the lab network.

### Lab 8.34 — Configure a network with the Meraki API (ENAUTO 6.3)

**Objective:** Push an SSID config via API.

```bash
curl -sk -X PUT -H "X-Cisco-Meraki-API-Key: $MERAKI_KEY" -H 'Content-Type: application/json' \
  "https://api.meraki.com/api/v1/networks/<netId>/wireless/ssids/0" \
  -d '{"name":"Lab-SSID","enabled":true,"authMode":"psk","psk":"<passphrase>"}' | jq -r '.name'
```

**Expected result:** the SSID configured cloud-side and pushed to APs — config
as an API call.

**Negative test:** a PSK below 8 chars is rejected by the API; the model
validates centrally.

**Cleanup:** disable the lab SSID.

### Lab 8.35 — Implement a Meraki alert webhook (ENAUTO 6.4)

**Objective:** Register a webhook receiver for Meraki alerts.

```bash
curl -sk -X POST -H "X-Cisco-Meraki-API-Key: $MERAKI_KEY" -H 'Content-Type: application/json' \
  "https://api.meraki.com/api/v1/networks/<netId>/webhooks/httpServers" \
  -d '{"name":"lab-hook","url":"https://collector.lab/meraki"}' | jq -r '.id'
```

**Expected result:** a webhook HTTP server registered — Meraki pushes alerts
(device down, config change) to the collector.

**Negative test:** a webhook URL that does not return 2xx is disabled after
repeated failures; the receiver must acknowledge.

**Cleanup:** DELETE the webhook HTTP server.

### Lab 8.36 — Explain AI/ML in network operations (CCNA 6.4)

**Objective:** Read an AI-driven insight from Catalyst Center.

```bash
curl -sk -H "X-Auth-Token: $DT" "$DNAC/dna/intent/api/v1/insight/networkDevices" 2>/dev/null | jq -r '.response[0]' 2>/dev/null || echo "AI insights endpoint (per release)"
```

**Expected result:** AI/ML-derived anomalies/trends (predictive) and
config/assurance recommendations (generative) — machine learning applied to
network operations.

**Negative test:** treating an AI recommendation as an automatic action; it
informs, and a human/automation gate should approve changes.

**Cleanup:** none (read-only).

### Lab 8.37 — Construct an EEM applet (ENCOR 6.6)

**Objective:** Automate a local reaction with Embedded Event Manager.

```text
DEV(config)# event manager applet SAVE-ON-CONFIG
DEV(config-applet)# event syslog pattern "CONFIGURED"
DEV(config-applet)# action 1.0 cli command "enable"
DEV(config-applet)# action 2.0 cli command "write memory"
DEV# show event manager policy registered
```

**Expected result:** an EEM applet that auto-saves the config on any change —
on-box, agentless automation triggered by a syslog event.

**Negative test:** an EEM applet with a too-broad event pattern fires
constantly and can loop; scope the trigger.

**Cleanup:** `no event manager applet SAVE-ON-CONFIG`.

### Lab 8.38 — NETCONF/RESTCONF query, telemetry, and EEM automation (integrative)

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

## Design Exercise

**ENSLD (300-420 Enterprise Design)** is a design exam covering enterprise
network design across campus, WAN, services, and automation. The
implementation labs throughout this volume are its build half; this exercise
is the reasoning half — designing from requirements, no lab required.

**Scenario.** Design the enterprise network for a company consolidating from
40 legacy branches and two data centers onto a modern Cisco architecture.
Requirements: a resilient three-tier (or collapsed-core where justified)
campus; a WAN that survives any single circuit or carrier failure; end-to-end
segmentation for corporate, IoT, and guest; sub-second convergence for the
routing core; centralized management and assurance; and an automation-first
operating model (no box-by-box CLI for routine change).

**Produce, defending each choice against a rejected alternative:**

1. **Campus design** — tier model, redundancy (StackWise/SSO, HSRP/GLBP), and
   the routing protocol choice (OSPF area design vs EIGRP), each traced to a
   convergence/scale requirement.
2. **WAN design** — SD-WAN vs traditional MPLS/DMVPN, transport mix
   (MPLS + internet), and the topology (hub-spoke, mesh, regional hubs) that
   meets the any-single-failure requirement.
3. **Segmentation design** — VRF/VN and SGT plan for corporate/IoT/guest,
   consistent from campus (SD-Access) through the WAN (SD-WAN segments).
4. **Services and QoS design** — the QoS model for voice/video and the network
   services (DHCP/DNS/NTP/NAT) placement.
5. **Management and automation design** — Catalyst Center + vManage as the
   controllers, model-driven telemetry for assurance, and where automation
   (Ansible/API) replaces manual change; name the operating model.

**Success looks like:** every design decision — tier count, protocol, WAN
topology, segmentation, controller — traces to a stated requirement with the
rejected alternative and its trade-off, the breadth-of-design standard ENSLD
applies.

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
