# Chapter 09: Automation, Assurance, and Certification Readiness

## Learning Objectives

- Automate IOS XR with model-driven interfaces: NETCONF, RESTCONF,
  gNMI, and YANG data models
- Stream model-driven telemetry and explain why it replaces SNMP
  polling for assurance
- Apply orchestration to provider services with Cisco NSO and the
  device-to-controller spectrum
- Operate the network as a system: deliberate change on IOS XR,
  validation, and rollback at scale
- Assemble a personal readiness plan for SPCOR and a chosen
  concentration from the verified blueprints

## Theory and Architecture

### Why automation is survival, not luxury, at SP scale

Chapter 01 named the scale: tens of thousands of devices, millions of
routes, SLAs measured in milliseconds of restoration. No team hand-
configures that, and no human polls it fast enough to meet an
assurance SLA. SPCOR's Automation and Assurance domain (15%) and the
whole of the retired SPAUTO (its four domains outline this chapter) treat
programmability as the operating model, and IOS XR — structured,
committed, model-native (Chapter 01) — is built for it.

### The model-driven interfaces

IOS XR exposes its configuration and state through **YANG** data
models over three transports, and knowing which fits what is exam and
job material:

- **NETCONF** (XML, SSH) — transactional configuration with candidate/
  commit semantics that map naturally onto XR's two-stage model.
- **RESTCONF** (HTTP verbs on YANG) — lighter, good for simple
  integrations and quick reads.
- **gNMI** (gRPC) — the modern high-performance interface, especially
  for **telemetry** subscriptions.

Models come in flavors: **native** (Cisco-XR YANG, full feature
coverage) versus **OpenConfig** (vendor-neutral, portable across a
multi-vendor core — the reason many providers prefer it). SPAUTO's
Automation APIs and Protocols and Network Device Programmability
domains (30% each) are exactly this.

### Model-driven telemetry: assurance that keeps up

**MDT** streams operational state — interface counters, BGP neighbor
states, LSP status, queue depths — from the device on subscription
(dial-out or dial-in via gNMI), continuously, instead of SNMP's
request/response polling. The difference is assurance-grade: sub-second
visibility, no polling gaps, and a data shape (structured, timestamped)
that a time-series pipeline consumes directly. SLA measurement,
capacity trending, and fast anomaly detection all depend on it — the
provider analog of Volume XXVII's "buy the telemetry" for AI fabrics.

### Orchestration: NSO and the spectrum

Beyond per-device automation, **Cisco NSO** (Network Services
Orchestrator) models *services* — an L3VPN, an EVPN, an SR-TE policy —
as intent, renders device configuration across every involved node,
and keeps a reconciled view (it knows what it deployed and detects
drift). The spectrum runs device-scripting (NETCONF/gNMI directly) →
configuration management → service orchestration (NSO) → closed-loop
(telemetry feeding automated remediation). SPAUTO's Automation and
Orchestration Platforms domain (30%) lives at the NSO end; the habits
below span all of it.

### The habits, unchanged

The automation discipline is the encyclopedia's throughout: idempotent
operations, secrets vaulted not scripted, post-condition asserts,
diff-before-apply, and change artifacts — the same rules Volumes IX,
XXVII, and XXVIII apply, here made easier by XR's native commit/
rollback and confirmed-commit.

## Design Considerations

- **OpenConfig where multi-vendor, native where feature-deep**: choose
  the model flavor for the estate; mixing is fine if deliberate.
- **Telemetry pipeline as core infrastructure**: collectors, a time-
  series store, dashboards, and alerting designed in — an assurance
  SLA with no telemetry is a promise with no instrument.
- **Service models over device scripts at scale**: NSO (or equivalent)
  for the services customers buy, so provisioning is consistent and
  auditable and drift is visible.
- **Closed-loop carefully**: automated remediation is powerful and
  dangerous — start with detect-and-alert, promote to auto-remediate
  only what you have rehearsed.

## Implementation and Automation

gNMI telemetry subscription and a NETCONF change on the volume's XR
estate:

```text
! Model-driven telemetry: stream BGP + interface state via gRPC dial-out
telemetry model-driven
 destination-group DC1
  address-family ipv4 10.50.0.5 port 57500
  encoding self-describing-gpb
 sensor-group SP-HEALTH
  sensor-path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/.../neighbors
  sensor-path Cisco-IOS-XR-infra-statsd-oper:infra-statistics/.../generic-counters
 subscription SP-SUB
  sensor-group-id SP-HEALTH sample-interval 5000
  destination-id DC1
```

```python
# NETCONF edit-config maps onto XR's candidate/commit (ncclient)
from ncclient import manager
with manager.connect(host="pe1", username="auto", key_filename="…",
                     hostkey_verify=True) as m:
    m.edit_config(target="candidate", config=vrf_payload)   # stage
    m.commit(confirmed=True, timeout="120")                 # confirmed commit
    assert bgp_vrf_up(m, "CUST-A"), "post-condition: VRF must be up"
    m.commit()                                              # confirm
```

```text
! OpenConfig read for portability
show yang-library
# gnmic -a pe1 get --path 'openconfig-interfaces:interfaces/interface'
```

## Validation and Troubleshooting

Automation is validated like any change plus its own layer:
**diff before apply** (NETCONF `show configuration` on the candidate,
NSO dry-run), **assert after** (the post-condition in the snippet —
the VRF must actually come up, mirroring Chapter 06's isolation
proof), and **confirmed commit** so a change that breaks reachability
rolls itself back (Chapter 01's safety, wired into automation).
Telemetry validation: the subscription is established and data is
arriving at the collector (gaps mean transport/encoding or a bad
sensor path). Troubleshooting: NETCONF/gNMI errors name the failing
YANG path precisely — more honest than screen-scraping; OpenConfig-
versus-native mismatches surface as unsupported paths (check
`show yang-library`); NSO out-of-sync means someone changed a device
by hand (reconcile, then find who and fix the process — the Chapter
09 lesson of Volume XXVII, restated for XR).

## Security and Best Practices

- gNMI/NETCONF over TLS in production (the lab's `no-tls`/`no-tls`
  shortcuts are flagged as lab-only, as in Chapter 01); mutual auth
  where the platform supports it.
- Automation accounts with XR task-group authorization scoped to what
  they manage; tokens and keys vaulted; no credentials in repositories.
- Telemetry and orchestration controllers are privileged network-wide
  — hold them to the management-plane standard of Chapter 08, and
  audit their actions.

## References and Knowledge Checks

- SPCOR 350-501 v1.1 Automation and Assurance (15%); SPAUTO 300-535
  v1.1 (all four domains) — retired 2026, kept for the record
- Cisco IOS XR programmability and telemetry configuration guides;
  Cisco NSO documentation; OpenConfig models

Knowledge checks:

1. Match NETCONF, RESTCONF, and gNMI to their best-fit tasks, and say
   which pairs naturally with XR's commit model and which with
   telemetry.
2. Why does model-driven telemetry meet an assurance SLA that SNMP
   polling cannot?
3. What does NSO know that a device-scripting approach does not, and
   how does that surface drift?
4. Build a weight-ordered SPCOR study sequence from this volume's
   README and defend the ordering.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **Domain 5 (Automation
and Assurance) of SPCOR 350-501 v1.1, Domain 5 (Service Assurance and
Optimization) of SPCNI 300-540 v1.0, and every objective of the SPAUTO 300-535
v1.1 exam guide** — mapped in the volume README's coverage tables. **SPAUTO
retired in 2026** under the Automation restructure, but SP automation remains
core to the track and CCIE SP; its labs are kept as a complete reference. Labs
use the IOS XR CLI, NETCONF/RESTCONF/gNMI, YANG tooling, NSO, and Python. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.46** — an IOS XR router with
NETCONF/gRPC/RESTCONF enabled, a Python 3 workstation with `git`, `ncclient`,
`netmiko`, `ydk`, `pyang`, and Ansible, a telemetry collector, and access to
Cisco NSO. **Cost:** none beyond lab resources.

### Lab 9.1 — Describe the programmable APIs (SPCOR Objective 5.1)

**Objective:** Enumerate the management interfaces the router exposes.

```text
show running-config netconf-yang 2>/dev/null; show netconf-yang statistics 2>/dev/null | head
show grpc 2>/dev/null | head
```

**Expected result:** the enabled programmable interfaces — IOS XR exposes
**NETCONF** (SSH/XML), **RESTCONF** (HTTP/JSON or XML), **gNMI/gRPC** (protobuf),
and CLI/XML, all driven by **YANG** models, so automation reads/writes structured
config and state instead of screen-scraping.

**Negative test:** script against the CLI text output and a version bump changes the
format, breaking the parser — the YANG-modeled APIs return stable structured data.

**Cleanup:** none (read-only).

### Lab 9.2 — Interpret an external script using a REST API (SPCOR Objective 5.2)

**Objective:** Read a RESTCONF GET and reason about its structure.

```bash
curl -sk -u admin:PW --location \
  "https://$XR/restconf/data/Cisco-IOS-XR-ip-static-cfg:router-static" \
  -H 'Accept: application/yang-data+json' | jq '.' | head
```

**Expected result:** the static-route config as JSON keyed by the YANG model — a
REST API script builds a URL from the model's path, sets Accept/Content-Type, and
parses the JSON/XML response; interpreting it means mapping the URL and body back
to the YANG structure.

**Negative test:** a path that does not match the model returns `404`; the RESTCONF
URL must follow the YANG hierarchy exactly.

**Cleanup:** none (read-only GET).

### Lab 9.3 — Describe the role of Network Services Orchestrator (SPCOR Objective 5.3)

**Objective:** Read NSO's device and service model.

```bash
# NSO CLI (ncs_cli)
ncs_cli -u admin -C -e "show devices list" 2>/dev/null | head
ncs_cli -u admin -C -e "show running-config services" 2>/dev/null | head
```

**Expected result:** NSO's managed devices and services — **NSO** is a
model-driven service orchestrator: it holds a synchronized config database (CDB)
of devices, renders **services** (a service model + template/mapping) into
per-device config transactionally, and reconciles drift, the SP's multivendor
automation control point.

**Negative test:** edit a device out-of-band; NSO's `check-sync` reports it
out-of-sync — NSO is the intended source of truth and detects divergence.

**Cleanup:** none (read-only).

### Lab 9.4 — Describe a data modeling language such as YANG (SPCOR Objective 5.4)

**Objective:** Read a YANG model's tree.

```bash
pyang -f tree Cisco-IOS-XR-ifmgr-cfg.yang | head -30
```

**Expected result:** the model tree (containers, lists, leaves, keys) — **YANG**
defines the schema for config and state: hierarchical, typed, with constraints and
`rw`/`ro` nodes; every NETCONF/RESTCONF/gNMI operation manipulates data conforming
to a YANG model.

**Negative test:** send data with a value violating a YANG type/range; the device
rejects it — YANG's type system validates input the CLI would also reject.

**Cleanup:** none.

### Lab 9.5 — Describe configuration management tools (SPCOR Objective 5.5)

**Objective:** Contrast Ansible (push) and Terraform (state) for XR.

```bash
ansible --version | head -1
ansible-playbook --check xr.yml 2>/dev/null | tail -3
terraform plan -no-color 2>/dev/null | tail -3
```

**Expected result:** Ansible's task run and Terraform's state diff — **Ansible**
(agentless, idempotent tasks over SSH/NETCONF) and **Terraform** (declarative,
state-tracked) both automate XR config; Ansible fits procedural changes, Terraform
fits declarative infrastructure with drift detection.

**Negative test:** re-run an idempotent Ansible play; `changed=0` — a raw script
would re-apply blindly, the difference config-management tools provide.

**Cleanup:** none (check/plan make no changes).

### Lab 9.6 — Describe Secure ZTP (SPCOR Objective 5.6)

**Objective:** Read the Secure Zero-Touch Provisioning bootstrap.

```text
show ztp status 2>/dev/null | head
show logging | include -i ztp | head
```

**Expected result:** the ZTP bootstrap state — **Secure ZTP** (RFC 8572) lets a
factory router securely fetch its image and config at first boot: it validates the
bootstrap server via the vendor certificate (ownership voucher), so provisioning is
automated and authenticated.

**Negative test:** a ZTP bootstrap without ownership-voucher/cert validation could
load attacker config; Secure ZTP's voucher chain prevents that — plain ZTP trusts
the network.

**Cleanup:** none (read-only).

### Lab 9.7 — Configure gRPC/gNMI dial-in/out with TLS/mTLS (SPCOR Objective 5.7)

**Objective:** Verify a secured gRPC/gNMI session (TLS, mTLS certs).

```text
show grpc | include "port|tls|address"
show tls session 2>/dev/null | head
```

```bash
gnmic -a $XR:57400 --tls-cert client.pem --tls-key client.key --tls-ca ca.pem get --path "/interfaces" | head
```

**Expected result:** the gRPC server on its TLS port and a successful mTLS gNMI GET
— gRPC/gNMI carries dial-in (client connects) and dial-out (device streams
telemetry); TLS encrypts it and **mTLS** (client + server certs) mutually
authenticates for secure automation.

**Negative test:** connect without the client cert to an mTLS-required server; the
handshake fails — mTLS rejects unauthenticated clients, unlike one-way TLS.

**Cleanup:** none (read-only).

### Lab 9.8 — Configure and verify NetFlow/IPFIX (SPCOR Objective 5.8)

**Objective:** Enable flow export and confirm records leave the router.

```text
show flow monitor <name> cache 2>/dev/null | head
show flow exporter <name> 2>/dev/null | include "packets|state"
```

**Expected result:** flow cache entries and the exporter sending records — NetFlow/
**IPFIX** samples traffic into flows (5-tuple + counters) and exports them to a
collector for traffic analysis, capacity planning, and DDoS detection.

**Negative test:** an exporter pointing at an unreachable collector shows records
built but not sent; `show flow exporter` reveals the transport failure — flow data
is only useful if it reaches the collector.

**Cleanup:** none (read-only).

### Lab 9.9 — Configure and verify NETCONF and RESTCONF (SPCOR Objective 5.9)

**Objective:** Confirm both YANG-driven interfaces work.

```bash
ssh -s admin@$XR -p 830 netconf <<'XML'
<rpc message-id="1"><get-config><source><running/></source></get-config></rpc>
XML
curl -sk -u admin:PW "https://$XR/restconf/data/Cisco-IOS-XR-shellutil-oper:system-time" -H 'Accept: application/yang-data+json'
```

**Expected result:** NETCONF returns the running config (XML/SSH), RESTCONF returns
system-time (JSON/HTTP) — both operate on YANG models; NETCONF has candidate/commit
and datastores, RESTCONF is a simpler HTTP CRUD over the same models.

**Negative test:** call NETCONF without `netconf-yang agent ssh` enabled; the port
830 connection is refused — the agent must be enabled.

**Cleanup:** none (read-only).

### Lab 9.10 — Configure and verify SNMP v2c/v3 (SPCOR Objective 5.10)

**Objective:** Verify SNMP polling and (for v3) auth/priv.

```text
show snmp
show snmp users 2>/dev/null
```

```bash
snmpget -v3 -l authPriv -u spuser -a SHA -A authpass -x AES -X privpass $XR sysUpTime.0
```

**Expected result:** the SNMP engine and a successful v3 get — SNMP still monitors
SP devices; **v3** adds authentication (SHA) and encryption (AES) with per-user
security, where **v2c** is community-string only (cleartext).

**Negative test:** poll with SNMP v2c across the internet; the community string is
cleartext and readable — v3 authPriv is required off the management network.

**Cleanup:** none (read-only).

### Lab 9.11 — Describe network assurance (SPCNI Objective 5.1)

**Objective:** Read the assurance telemetry/state for a service.

```text
show telemetry model-driven subscription 2>/dev/null | head
show segment-routing traffic-eng policy all | include "Admin|Oper|Metric"
```

**Expected result:** the streaming subscriptions and SR-TE policy health — network
assurance continuously validates that the network delivers intent: streaming
telemetry feeds an assurance engine (e.g., Crosswork) that checks SLA (latency,
loss) and flags deviations proactively.

**Negative test:** rely on periodic SNMP polls for assurance; a transient SLA
breach between polls is missed — streaming telemetry catches it, which is why
assurance uses push.

**Cleanup:** none (read-only).

### Lab 9.12 — Describe cloud infrastructure and performance monitoring (SPCNI Objective 5.2)

**Objective:** Read NFVI/cloud performance metrics.

```bash
virsh domstats vnf-router 2>/dev/null | head
! Collector (Prometheus/Grafana) scrapes host + VNF CPU, memory, and packet stats
```

**Expected result:** the VNF's CPU/memory/IO stats — cloud/NFVI monitoring tracks
host and VNF resource use, throughput, and drops, correlating infrastructure health
with service performance so capacity and faults are visible.

**Negative test:** monitor only the VNF and miss host-level CPU steal starving it;
the VNF looks under-loaded while the host is saturated — both layers must be
monitored.

**Cleanup:** none (read-only).

### Lab 9.13 — Diagnose NFVI errors and events (SPCNI Objective 5.3)

**Objective:** Correlate an NFVI event with a service impact.

```bash
virsh domstate vnf-router 2>/dev/null
journalctl -u libvirtd --since "10 min ago" 2>/dev/null | grep -iE "error|fail" | head
```

**Expected result:** the VNF state and host events — diagnosing NFVI issues
correlates hypervisor/host events (OOM, NIC errors, live-migration) with VNF/service
symptoms; a service blip often traces to an infrastructure event, not the network
config.

**Negative test:** debug routing for a service outage caused by a VNF the hypervisor
OOM-killed — read the NFVI events before the network state.

**Cleanup:** none (read-only).

### Lab 9.14 — Describe VNF optimization (SPCNI Objective 5.4)

**Objective:** Read the data-path optimization on a VNF.

```bash
ethtool -k eth0 2>/dev/null | grep -iE "sr-iov|offload" | head
virsh dumpxml vnf-router 2>/dev/null | grep -iE "hugepages|cpuset|driver name='vfio'" | head
```

**Expected result:** SR-IOV/DPDK, hugepages, and CPU pinning — VNF optimization
raises forwarding performance with **SR-IOV/DPDK** (bypass the host stack),
**hugepages** (fewer TLB misses), **CPU pinning/NUMA** alignment, and offloads, so
a software VNF approaches line rate.

**Negative test:** run a forwarding VNF on virtio with no pinning across NUMA nodes;
throughput and latency suffer — the optimizations are what make NFV viable at SP
scale.

**Cleanup:** none (read-only).

### Lab 9.15 — Git version-control operations (SPAUTO Objective 1.1)

**Objective:** Exercise add, clone, commit, diff, branch, merge.

```bash
git init sp-auto && cd sp-auto
echo "hostname pe1" > pe1.cfg && git add . && git commit -m "base"
git switch -c change && echo "hostname pe1-new" > pe1.cfg && git commit -am "rename"
git switch main && git diff change -- pe1.cfg | head; cd .. && rm -rf sp-auto
```

**Expected result:** the diff between branches — Git versions SP automation code and
config-as-code; branch/merge/diff underpin peer review and safe rollout of network
changes.

**Negative test:** `git push` with no remote fails — a remote must be configured
first.

**Cleanup:** `rm -rf sp-auto`.

### Lab 9.16 — Describe API styles: REST and RPC (SPAUTO Objective 1.2)

**Objective:** Call XR two ways — RESTCONF (REST) and NETCONF (RPC).

```bash
curl -sk -u admin:PW "https://$XR/restconf/data/Cisco-IOS-XR-shellutil-oper:system-time" -H 'Accept: application/yang-data+json'
ssh -s admin@$XR -p 830 netconf <<'XML'
<rpc message-id="1"><get><filter><system-time xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-oper"/></filter></get></rpc>
XML
```

**Expected result:** REST returns a resource (RESTCONF/JSON); NETCONF invokes an
RPC (`get`) — REST is resource/URL-oriented, RPC is method-oriented; both drive the
same YANG models but with different interaction styles.

**Negative test:** POST a NETCONF RPC body to the RESTCONF endpoint; it rejects it
— the styles are distinct.

**Cleanup:** none (read-only).

### Lab 9.17 — Describe sync vs async API patterns (SPAUTO Objective 1.3)

**Objective:** Contrast a synchronous GET with an async NSO commit/job.

```bash
time curl -sk -u admin:PW "https://$XR/restconf/data/Cisco-IOS-XR-shellutil-oper:system-time" -o /dev/null -H 'Accept: application/yang-data+json'
# async: NSO commit with commit-queue returns a queue id to track
ncs_cli -u admin -C -e "show commit-queue" 2>/dev/null | head
```

**Expected result:** the GET returns inline; the NSO commit-queue tracks async
device pushes — small reads are synchronous; large multi-device provisioning is
async (NSO commit-queue) so the client is not blocked and failures are tracked per
device.

**Negative test:** assume an async commit-queue job finished on submit; devices
update as the queue drains — you must track the queue item to completion.

**Cleanup:** none (read-only).

### Lab 9.18 — Interpret Python scripts (SPAUTO Objective 1.4)

**Objective:** Read a script exercising data types, functions, classes, loops.

```bash
python3 - <<'PY'
class PE:
    def __init__(self, name, asn): self.name, self.asn = name, asn
pes=[PE("pe1",65001), PE("pe2",65002)]
for p in pes:
    if p.asn == 65001: print(p.name, "home-AS")
PY
```

**Expected result:** `pe1 home-AS` — the script uses a class, a loop, a condition,
and a list, the constructs SPAUTO expects you to interpret in automation code.

**Negative test:** reference an undefined attribute; Python raises `AttributeError`
— reading the traceback is part of the skill.

**Cleanup:** none.

### Lab 9.19 — Describe Python virtual environments (SPAUTO Objective 1.5)

**Objective:** Create an isolated venv for XR SDKs.

```bash
python3 -m venv xrenv && source xrenv/bin/activate
pip install -q ncclient ydk 2>/dev/null; which python; deactivate
```

**Expected result:** `which python` points inside `xrenv/` — a venv isolates SDK
versions (ncclient, ydk, netmiko) per project, avoiding conflicts across automation
codebases.

**Negative test:** install SDKs system-wide and two projects needing different
versions clash — the venv is the isolation.

**Cleanup:** `rm -rf xrenv`.

### Lab 9.20 — Benefits of Ansible and Terraform (SPAUTO Objective 1.6)

**Objective:** Show idempotence (Ansible) and plan (Terraform) for XR.

```bash
ansible-playbook -i inv xr.yml | grep -E 'changed=0|ok='
```

**Expected result:** a second run reports `changed=0` — idempotence means repeated
runs converge without redundant change, the core benefit for repeatable SP config;
Terraform adds state tracking and drift detection.

**Negative test:** a shell script re-applies everything each run (no idempotence) —
the declarative tools' convergence is the advantage.

**Cleanup:** none.

### Lab 9.21 — Describe YANG data models: OpenConfig, IETF, native (SPAUTO Objective 2.1)

**Objective:** Compare a native and an OpenConfig model tree.

```bash
pyang -f tree Cisco-IOS-XR-ifmgr-cfg.yang | head
pyang -f tree openconfig-interfaces.yang | head
```

**Expected result:** the native (vendor-specific) and OpenConfig (vendor-neutral)
trees — **native** models expose full platform features; **OpenConfig** and
**IETF** models are vendor-neutral for multivendor automation; SP automation
chooses based on the feature and the fleet.

**Negative test:** expect full XR feature coverage from OpenConfig; some
platform-specific features exist only in native models — the model choice trades
neutrality for coverage.

**Cleanup:** none.

### Lab 9.22 — Describe HTTP authentication mechanisms (SPAUTO Objective 2.2)

**Objective:** Contrast basic, token, and OAuth auth on RESTCONF/APIs.

```bash
# Basic: credentials each request
curl -sk -u admin:PW "https://$XR/restconf/data/..." -o /dev/null -w '%{http_code}\n'
# Token/OAuth: obtain a token, then present it as a bearer header (e.g., to NSO/Crosswork)
```

**Expected result:** basic auth succeeds with credentials — **basic** sends
user:pass (over TLS) each call; **token** presents a pre-issued token; **OAuth**
exchanges credentials for a scoped, expiring access token; controllers (NSO,
Crosswork) commonly use token/OAuth.

**Negative test:** use basic auth without TLS; credentials are exposed — basic must
run over HTTPS, and token/OAuth reduce credential exposure.

**Cleanup:** none (read-only).

### Lab 9.23 — Compare data types: JSON, XML, YAML, gRPC, protobuf (SPAUTO Objective 2.3)

**Objective:** Encode the same data three ways.

```bash
python3 - <<'PY'
d={"interface":"GigabitEthernet0/0/0/0","enabled":True}
import json, yaml
print("JSON:", json.dumps(d))
print("YAML:", yaml.safe_dump(d).strip())
print("XML : <interface><name>...</name><enabled>true</enabled></interface>")
PY
```

**Expected result:** JSON (RESTCONF/gNMI), YAML (Ansible/human config), XML
(NETCONF) — text encodings differ in verbosity and use; **protobuf/gRPC** is a
compact binary encoding for high-volume telemetry where text would be too large.

**Negative test:** stream high-rate telemetry as JSON text; the overhead is large —
GPB/protobuf is used for volume, which is why gNMI defaults to it.

**Cleanup:** none.

### Lab 9.24 — Interpret a JSON instance from a YANG model (SPAUTO Objective 2.4)

**Objective:** Map a RESTCONF JSON response back to its YANG model.

```bash
curl -sk -u admin:PW "https://$XR/restconf/data/Cisco-IOS-XR-ifmgr-cfg:interface-configurations" -H 'Accept: application/yang-data+json' | jq '.' | head
```

**Expected result:** JSON keyed by `module:container/list` matching the YANG tree —
interpreting it means recognizing that each JSON key is a YANG node and list keys
identify list entries, so you can read or construct valid instances.

**Negative test:** a JSON body missing a required list key is rejected on write —
the YANG model's keys are mandatory.

**Cleanup:** none (read-only).

### Lab 9.25 — Interpret an XML instance from a YANG model (SPAUTO Objective 2.5)

**Objective:** Map a NETCONF XML reply to its YANG model.

```bash
ssh -s admin@$XR -p 830 netconf <<'XML' | xmllint --format - | head
<rpc message-id="1"><get-config><source><running/></source><filter><interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"/></filter></get-config></rpc>
XML
```

**Expected result:** XML elements namespaced to the YANG module — the XML mirrors the
YANG tree with namespaces per module; interpreting it means mapping elements to
containers/leaves and namespaces to modules.

**Negative test:** omit the module namespace on a write; NETCONF cannot resolve the
element — the namespace binds the XML to its model.

**Cleanup:** none (read-only).

### Lab 9.26 — Interpret a YANG module tree from pyang (SPAUTO Objective 2.6)

**Objective:** Generate and read a model tree with pyang.

```bash
pyang -f tree Cisco-IOS-XR-ip-static-cfg.yang | head -25
```

**Expected result:** the tree with `+--rw`/`+--ro`, containers, lists (`*`), and
keys `[...]` — pyang's tree output is the fastest way to understand a model's
structure and build valid NETCONF/RESTCONF payloads or XPaths.

**Negative test:** guess a path without the tree and hit a non-existent node; the
device errors — the pyang tree prevents that by showing the real structure.

**Cleanup:** none.

### Lab 9.27 — Configuration/operation management with RESTCONF (SPAUTO Objective 2.7)

**Objective:** Write config via RESTCONF and read it back.

```bash
curl -sk -u admin:PW -X PATCH "https://$XR/restconf/data/Cisco-IOS-XR-ip-static-cfg:router-static" \
  -H 'Content-Type: application/yang-data+json' \
  -d '{"router-static":{"default-vrf":{"address-family":{"vrfipv4":{"vrf-unicast":{"vrf-prefixes":{"vrf-prefix":[{"prefix":"203.0.113.0","prefix-length":24,"vrf-route":{"vrf-next-hop-table":{"vrf-next-hop-next-hop-address":[{"next-hop-address":"10.0.0.2"}]}}}]}}}}}}}'
curl -sk -u admin:PW "https://$XR/restconf/data/Cisco-IOS-XR-ip-static-cfg:router-static" -H 'Accept: application/yang-data+json' | jq '.' | head
```

**Expected result:** the static route added then read back — RESTCONF manages config
(GET/POST/PATCH/PUT/DELETE) and operational state over HTTP with YANG-modeled JSON/
XML, a simple CRUD automation interface.

**Negative test:** PATCH a leaf that violates a YANG constraint; RESTCONF returns a
`400` with the error path — the model validates writes.

**Cleanup:** DELETE the test static route.

### Lab 9.28 — Configuration/operation management with NETCONF (SPAUTO Objective 2.8)

**Objective:** Edit-config via NETCONF with candidate/commit.

```bash
python3 - <<'PY'
from ncclient import manager
cfg='''<config><router-static xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg">
 </router-static></config>'''
with manager.connect(host="XR",port=830,username="admin",password="PW",hostkey_verify=False) as m:
    print(m.get_config(source='running').data_xml[:120])
PY
```

**Expected result:** the running config retrieved (and edit-config/commit available)
— NETCONF supports datastore operations (get-config, edit-config, commit, lock) with
transactional candidate→running semantics on platforms that support candidate.

**Negative test:** edit-config with malformed XML returns an `rpc-error` the script
must handle — NETCONF gives structured errors, not silent failure.

**Cleanup:** discard candidate / remove test config.

### Lab 9.29 — Compare NETCONF datastores (SPAUTO Objective 2.9)

**Objective:** Read the datastores the device exposes.

```bash
ssh -s admin@$XR -p 830 netconf <<'XML' | xmllint --format - | grep -iE "running|candidate|startup" 
<rpc message-id="1"><get><filter><netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"><datastores/></netconf-state></filter></get></rpc>
XML
```

**Expected result:** the supported datastores — **running** (active config),
**candidate** (edit then commit atomically), **startup** (persisted boot config);
IOS XR's two-stage commit maps to candidate→running, enabling safe transactional
changes.

**Negative test:** expect a candidate datastore on a platform that only exposes
running with `:writable-running`; the edit applies directly — capabilities dictate
the datastore model.

**Cleanup:** none (read-only).

### Lab 9.30 — Deploy and validate with ncclient (SPAUTO Objective 3.1)

**Objective:** Push config and validate operational state via ncclient.

```bash
python3 - <<'PY'
from ncclient import manager
with manager.connect(host="XR",port=830,username="admin",password="PW",hostkey_verify=False) as m:
    state=m.get(filter=('subtree','<interfaces xmlns="http://openconfig.net/yang/interfaces"/>')).data_xml
    print("oper-state bytes:", len(state))
PY
```

**Expected result:** config applied and the operational state read back — ncclient
(Python NETCONF) is the workhorse for deploy-then-validate: edit-config to push, then
get to confirm the intended operational state, closing the loop.

**Negative test:** deploy without a validation `get`; a commit can succeed while the
feature stays down (e.g., dependency missing) — always validate operational state.

**Cleanup:** remove the test config.

### Lab 9.31 — Python NETCONF with YDK and YANG Suite (SPAUTO Objective 3.2)

**Objective:** Use YDK model bindings to configure XR.

```bash
python3 - <<'PY'
# YDK generates Python classes from YANG; you set attributes, YDK renders NETCONF
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
print("YDK maps YANG models to Python objects; YANG Suite helps build/test payloads")
PY
```

**Expected result:** YDK model objects driving a CRUD operation — **YDK** turns YANG
models into typed Python classes so you build config as objects (not raw XML), and
**YANG Suite** helps explore models and generate/test payloads.

**Negative test:** a YDK bundle version mismatched to the device's model fails to
render valid config — the YDK model bundle must match the platform.

**Cleanup:** remove the test config.

### Lab 9.32 — Deploy and validate with NetMiko (SPAUTO Objective 3.3)

**Objective:** Push CLI config and read state via NetMiko (SSH).

```bash
python3 - <<'PY'
from netmiko import ConnectHandler
dev={"device_type":"cisco_xr","host":"XR","username":"admin","password":"PW"}
c=ConnectHandler(**dev)
print(c.send_command("show ipv4 interface brief").splitlines()[0])
# c.send_config_set([...]); c.commit()   # XR requires commit
c.disconnect()
PY
```

**Expected result:** the CLI output over SSH — **NetMiko** automates the CLI (SSH)
for platforms/tasks without a YANG path, handling XR's `commit`; it validates by
parsing `show` output.

**Negative test:** send config with NetMiko to XR and forget `commit()`; the change
is not applied — XR's two-stage commit still applies to CLI automation.

**Cleanup:** remove the test config.

### Lab 9.33 — Deploy and validate with an Ansible playbook (SPAUTO Objective 3.4)

**Objective:** Configure XR with `cisco.iosxr` and confirm idempotence.

```bash
cat > xr.yml <<'YML'
- hosts: xr
  gather_facts: no
  tasks:
    - cisco.iosxr.iosxr_logging_global:
        config: {hosts: [{host: 10.0.0.200, severity: info}]}
        state: merged
YML
ansible-playbook -i inv xr.yml | grep -E 'changed|ok='
```

**Expected result:** first run `changed=1`, second `changed=0` — the `cisco.iosxr`
collection deploys config declaratively (NETCONF/CLI) and idempotently, validating by
re-running.

**Negative test:** run with `state: deleted` — the config is removed; declarative
state covers add and remove symmetrically.

**Cleanup:** re-run with `state: deleted`.

### Lab 9.34 — Compare gNMI with NETCONF and gRPC (SPAUTO Objective 3.5)

**Objective:** Contrast the three interfaces on XR.

```bash
gnmic -a $XR:57400 -u admin -p PW --insecure get --path "/interfaces/interface" | head
```

**Expected result:** gNMI GET over gRPC returning structured data — **gNMI** is a
gRPC-based config/telemetry protocol (compact protobuf, streaming) atop **gRPC**
(the transport); **NETCONF** is SSH/XML with rich datastore semantics. gNMI excels at
telemetry and simple config; NETCONF at transactional multi-datastore config.

**Negative test:** expect NETCONF's candidate/commit semantics from gNMI Set; gNMI's
model is simpler (replace/update/delete) — choose per the operation's needs.

**Cleanup:** none (read-only).

### Lab 9.35 — Python RESTCONF with YANG Suite (SPAUTO Objective 3.6)

**Objective:** Build and send a RESTCONF request from Python.

```bash
python3 - <<'PY'
import requests, urllib3; urllib3.disable_warnings()
r=requests.get("https://XR/restconf/data/Cisco-IOS-XR-shellutil-oper:system-time",
  auth=("admin","PW"), headers={"Accept":"application/yang-data+json"}, verify=False)
print(r.status_code, r.json())
PY
```

**Expected result:** `200` and the JSON body — a Python RESTCONF client builds the
YANG-path URL, sets headers, and parses JSON; YANG Suite helps generate the correct
path/payload from the model before coding it.

**Negative test:** a wrong Accept header (plain `application/json`) may be rejected;
RESTCONF expects `application/yang-data+json` — the media type matters.

**Cleanup:** none (read-only).

### Lab 9.36 — Construct XPath notation (SPAUTO Objective 3.7)

**Objective:** Write an XPath for a YANG node and use it in a subscription.

```bash
# XPath to an interface's oper counters:
echo '/interfaces/interface[name="GigabitEthernet0/0/0/0"]/state/counters'
gnmic -a $XR:57400 -u admin -p PW --insecure get --path '/interfaces/interface[name=GigabitEthernet0/0/0/0]/state/counters' | head
```

**Expected result:** the counters returned for the XPath-selected node — **XPath**
addresses a node or list instance (with predicates `[key=value]`) in a YANG tree; it
is how telemetry subscriptions and NETCONF filters select exactly the data wanted.

**Negative test:** an XPath predicate on a non-key leaf may not select as expected;
list selection uses the key — the predicate must match the model's key.

**Cleanup:** none (read-only).

### Lab 9.37 — Diagnose model-driven telemetry with gRPC on XR (SPAUTO Objective 3.8)

**Objective:** Verify a streaming telemetry subscription and its stream.

```text
show telemetry model-driven subscription
show telemetry model-driven sensor-group
show telemetry model-driven destination
```

**Expected result:** the subscription streaming a sensor-path to a collector — MDT
on XR pushes YANG-modeled state (interface counters, BGP) at an interval or on-change
over gRPC/GPB; diagnosing it checks the sensor-path, destination reachability, and
the collector's receipt.

**Negative test:** a subscription whose destination is unreachable shows the
transport failing in `show telemetry ... destination` — the stream is only as good as
the collector link.

**Cleanup:** none (read-only).

### Lab 9.38 — Describe ETSI NFV (SPAUTO Objective 4.1)

**Objective:** Map the ETSI NFV components in the deployment.

```bash
osm vnfd-list 2>/dev/null | head || echo "ETSI MANO: NFVO + VNFM + VIM; VNFD/NSD descriptors"
```

**Expected result:** the descriptors/orchestrator roles — **ETSI NFV** defines the
architecture: **NFVI** (compute/storage/network), **VNFs**, and **MANO** (NFVO
orchestrates network services, VNFM manages VNF lifecycle, VIM controls the
infrastructure), driven by VNFD/NSD descriptors.

**Negative test:** conflate the VIM (infrastructure, e.g., OpenStack) with the NFVO
(service orchestration); they are separate MANO functions — mixing them breaks the
architecture model.

**Cleanup:** none (read-only).

### Lab 9.39 — Describe NSO architecture (SPAUTO Objective 4.2)

**Objective:** Read NSO's CDB, NEDs, and service/device managers.

```bash
ncs_cli -u admin -C -e "show ncs-state version" 2>/dev/null
ncs_cli -u admin -C -e "show packages package package-version" 2>/dev/null | head
```

**Expected result:** the NSO version and loaded packages (NEDs/services) — NSO's
architecture: the **CDB** (config database), **NEDs** (Network Element Drivers,
per-platform), the **device manager** (sync/deploy), and the **service manager**
(model + mapping rendering intent to device config transactionally).

**Negative test:** manage a device with no matching NED; NSO cannot render config to
it — the NED for that platform/version is required.

**Cleanup:** none (read-only).

### Lab 9.40 — Describe Cisco Crosswork Network Controller (SPAUTO Objective 4.3)

**Objective:** Read Crosswork's role and inventory.

```bash
curl -sk -H "Authorization: Bearer $CW" "https://$CROSSWORK/crosswork/inventory/v1/nodes" 2>/dev/null | jq '.' | head
```

**Expected result:** the devices Crosswork manages — **Crosswork Network Controller**
is Cisco's SP automation/assurance suite: topology and inventory, **SR-PCE**-driven
SR-TE optimization, service provisioning (with NSO), and closed-loop assurance from
telemetry.

**Negative test:** expect Crosswork to optimize SR-TE without SR-PCE/telemetry
inputs; it needs the topology and path-computation feed — the components work
together.

**Cleanup:** none (read-only).

### Lab 9.41 — Configure a device using the NSO RESTCONF API in Python (SPAUTO Objective 4.4)

**Objective:** Drive NSO's northbound RESTCONF from Python.

```bash
python3 - <<'PY'
import requests, urllib3; urllib3.disable_warnings()
r=requests.get("https://NSO:8888/restconf/data/tailf-ncs:devices/device",
  auth=("admin","admin"), headers={"Accept":"application/yang-data+json"}, verify=False)
print(r.status_code)
PY
```

**Expected result:** NSO returning its device list over RESTCONF — NSO exposes a
northbound RESTCONF API (the `tailf-ncs` model) so scripts create services and manage
devices programmatically, and NSO renders the per-device config.

**Negative test:** POST a service instance whose service model/package is not loaded;
NSO rejects it — the service package must be present.

**Cleanup:** delete the test service instance.

### Lab 9.42 — Describe Cisco ESC management and automation (SPAUTO Objective 4.5)

**Objective:** Read Elastic Services Controller's VNF lifecycle role.

```bash
curl -sk -u admin:PW "https://$ESC:8443/ESCManager/v0/deployments" 2>/dev/null | head || echo "ESC: VNF lifecycle (deploy, monitor, heal, scale)"
```

**Expected result:** the ESC-managed deployments — **Cisco ESC** is a VNF Manager
(VNFM): it deploys VNFs onto a VIM from a deployment template, then **monitors,
heals** (restart on failure), and **scales** them, automating the VNF lifecycle under
MANO.

**Negative test:** expect ESC to orchestrate a multi-VNF network service end to end;
that is the NFVO's job (NSO/OSM) — ESC manages VNF lifecycle, one layer down.

**Cleanup:** none (read-only).

### Lab 9.43 — Implement SR-PCE / topology transfer (SPAUTO Objective 4.6)

**Objective:** Verify SR-PCE learning the topology and computing paths.

```text
show pce ipv4 topology summary
show pce lsp
show segment-routing traffic-eng pcc ipv4 peer 2>/dev/null
```

**Expected result:** the SR-PCE topology and computed LSPs — **SR-PCE** (formerly
XTC) is a stateful path computation element: it learns the topology (via BGP-LS/IGP),
computes SR-TE paths on request (from a PCC or Crosswork), and can be delegated LSP
control for centralized optimization.

**Negative test:** an SR-PCE with no BGP-LS/IGP topology feed cannot compute paths;
`show pce ipv4 topology` is empty — the topology feed is the prerequisite.

**Cleanup:** none (read-only).

### Lab 9.44 — Describe Cisco WAE (SPAUTO Objective 4.7)

**Objective:** Read the WAN Automation Engine's planning/optimization role.

```bash
curl -sk -u admin:PW "https://$WAE:8443/wae/api/networks" 2>/dev/null | head || echo "WAE: WAN modeling, what-if, and bandwidth optimization"
```

**Expected result:** the WAE network model — **Cisco WAE** builds a model of the WAN
(topology, traffic matrix) for **what-if planning**, failure simulation, and
**bandwidth optimization**, feeding SR-TE/RSVP path placement for capacity planning.

**Negative test:** use WAE's plan without an accurate traffic matrix; optimizations
are wrong — WAE needs a current demand matrix (from telemetry/NetFlow) to be useful.

**Cleanup:** none (read-only).

### Lab 9.45 — Construct a service template using NSO (SPAUTO Objective 4.8)

**Objective:** Read an NSO service model and its device template.

```bash
ncs_cli -u admin -C -e "show running-config services" 2>/dev/null | head
# A service = YANG service model + XML device template + optional Python/Java mapping
```

**Expected result:** the service instances and their template mapping — an NSO
service template maps service intent (the YANG service model's inputs) to device
config via an XML template with variables, so one service instance renders consistent
config across many devices.

**Negative test:** a template referencing a device model path that a NED does not
support fails to render on that device — the template must match each device's model.

**Cleanup:** none (read-only).

### Lab 9.46 — Deploy a service package using NSO (SPAUTO Objective 4.9)

**Objective:** Load a service package and instantiate a service.

```bash
ncs_cli -u admin -C -e "packages reload" 2>/dev/null | head
ncs_cli -u admin -C -e "show packages package oper-status" 2>/dev/null | head
```

**Expected result:** the package loaded `up` and available — deploying an NSO service
package means placing it in the packages directory, `packages reload`, confirming
`oper-status up`, then creating service instances that render device config through
the package.

**Negative test:** reload a package with a compile error; `oper-status` shows it down
with the error — the package must compile before its services are usable.

**Cleanup:** remove the test service instance.

## Lab Verification

Verification means the NETCONF provisioning was idempotent with its
assert and confirmed-commit, telemetry showed sub-second state and
beat polling on a failure, the SLA alert fired on demand, and the
study plan exists. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

At provider scale, automation and assurance are the operating model:
YANG over NETCONF/RESTCONF/gNMI configures the network, model-driven
telemetry observes it fast enough to keep SLAs, and NSO orchestrates
the services customers buy while detecting drift — all riding IOS XR's
native commit, confirm, and rollback. This closes SPCOR's Automation
and Assurance domain and the whole of the retired SPAUTO, and with
the core and concentrations verified, mapped, and practiced, the CCNP
Service Provider track is yours to schedule.

- [ ] I can match the model-driven interfaces to their tasks
- [ ] My provisioning is idempotent, asserted, and confirm-committed
- [ ] My telemetry beat polling on a real failure
- [ ] My exam plan is weight-ordered against the verified blueprints
