# Chapter 06: Automation, DevOps, and Cloud — Junos as Code

## Learning Objectives

- Drive Junos programmatically: NETCONF/XML, PyEZ, and the REST and
  gRPC surfaces
- Put configurations under version control and push them with Ansible;
  validate state with JSNAPy before and after change
- Understand Junos telemetry (gNMI/OpenConfig) as the streaming
  replacement for SNMP polling
- Map JNCIA-DevOps (JN0-224), JNCIS-DevOps (JN0-423), and JNCIA-Cloud
  (JN0-214) onto this toolchain

## Theory and Architecture

### The track in one sentence

The Automation and DevOps track certifies operating Junos as a
programmable system: structured data instead of screen-scraping,
declarative pushes instead of typed sessions, and testable state
instead of eyeballed show output. JNCIA-DevOps (JN0-224) covers the
concepts and core tools; JNCIS-DevOps (JN0-423, written to Junos OS
24.4) goes to production depth. JNCIA-Cloud (JN0-214) — the Cloud
track's single current rung — adds the adjacent vocabulary:
virtualization, containers, SDN, and Juniper's cloud-touching
portfolio. All 90-minute/65-question exams (verified 22 July 2026).

### Junos was built for this

Every Junos CLI command is a veneer over XML RPCs — append `| display
xml rpc` and the device tells you its own API. NETCONF (RFC 6241)
wraps those RPCs with transactions that inherit the commit model:
lock, edit candidate, validate, commit-confirmed, unlock. **PyEZ**
(`junos-eznc`) makes this Pythonic — facts, RPC calls returning lxml
trees, and Tables/Views that turn operational output into structured
objects. Above that, the **Junos Ansible collection**
(`juniper.device`) gives idempotent config push and RPC modules, and
**JSNAPy** snapshots operational state and asserts invariants —
pre/post change, in CI.

### Telemetry: from polling to streaming

SNMP asks; telemetry tells. Junos streams OpenConfig paths over gRPC
(gNMI subscribe) at second-scale cadence — interface counters, BGP
state, environmentals — feeding the observability stack Volume XI
built. The JNCIS-DevOps expects the model paths and the subscription
mechanics, not just the buzzword.

## Design Considerations

- **Source of truth** lives in Git, not on boxes: templated intent
  (Jinja2 + YAML inventory) rendered per device, pushed via NETCONF
  with commit-confirmed, gated by JSNAPy pre/post — the pipeline this
  encyclopedia's Volume IX generalizes, specialized to Junos
- **Config replace over merge** for owned sections: `load override`
  or `load replace` semantics keep drift from accumulating
- **Read paths are production too:** rate-limit and scope gNMI
  collectors like any client; telemetry is cheap, not free

## Implementation and Automation

```python
# PyEZ: facts, one RPC, one guarded config push
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

with Device(host="10.30.10.21", user="auto", ssh_private_key_file="~/.ssh/lab") as dev:
    print(dev.facts["hostname"], dev.facts["version"])
    ospf = dev.rpc.get_ospf_neighbor_information()
    assert ospf.findall(".//ospf-neighbor"), "no OSPF neighbors!"
    with Config(dev, mode="exclusive") as cu:
        cu.load("set system services netconf rfc-compliant", format="set")
        if cu.diff():
            cu.commit(comment="netconf hardening", confirm=2)
            cu.commit_check() and cu.commit()   # confirm inside the window
```

```yaml
# JSNAPy: assert the fabric's invariants around any change
tests_include:
  - check_bgp
check_bgp:
  - rpc: get-bgp-summary-information
  - iterate:
      xpath: //bgp-peer
      tests:
        - is-equal: peer-state, Established
          err: "BGP peer <{{post['peer-address']}}> not Established"
```

## Validation and Troubleshooting

- `show system services netconf` and an `ssh -s ... netconf` hello by
  hand when automation "cannot connect"
- PyEZ exceptions are precise: `ConnectAuthError` vs `RpcTimeoutError`
  route you immediately
- `show system commit` — automation-driven commits carry their
  comments; an uncommented commit is a process escape
- JSNAPy diff output is the change review: no green, no merge
- For telemetry: `show agent sensors` and a one-path gnmic subscribe
  before blaming the collector

## Security and Best Practices

- Dedicated automation account with a scoped login class; SSH keys,
  never passwords, in vaulted storage
- `commit confirmed` in every unattended push; the pipeline confirms
  only after post-checks pass
- NETCONF over SSH only from the automation subnet (loopback filter
  term, Chapter 02's discipline)
- Junos upgrades validated in the pipeline against vJunos before
  metal — the DevOps track's whole thesis in one habit

## References and Knowledge Checks

- JNCIA-DevOps (JN0-224), JNCIS-DevOps (JN0-423), JNCIA-Cloud
  (JN0-214) objectives on Juniper's certification pages
- Juniper PyEZ and Ansible collection documentation; JSNAPy README;
  *Day One: Automating Junos with Ansible*

Knowledge checks:

1. Why does NETCONF on Junos give automation transactional safety that
   REST-style per-line config APIs cannot?
2. Your Ansible push succeeded but the change is absent an hour later.
   Name the Junos mechanism that explains it and the flag that was
   missed.
3. Where do JSNAPy assertions belong in a change pipeline, and what do
   they replace from manual operations?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every exam objective of
the JNCIS-DevOps (JN0-423) exam** (written to Junos OS 24.4), plus the foundational
NETCONF/PyEZ, REST, and cloud/SDN skills of the JNCIA-DevOps (JN0-224) and
JNCIA-Cloud (JN0-214) associate exams — mapped in the volume README's coverage
tables. Labs use the Junos CLI, Python (PyEZ), Ansible, and gNMI/NETCONF. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.8** — a Junos device with NETCONF and gRPC
enabled, a workstation with Python 3, `junos-eznc` (PyEZ), Ansible with the
`juniper.device` collection, `pyang`, and a telemetry collector. **Cost:** none
beyond lab resources.

### Lab 6.1 — Platform Automation Overview (Objective: Platform Automation Overview)

**Objective:** Identify the Junos automation entry points (mgd, JET, Terraform).

```text
show configuration system services | match "netconf|rest|ssh"
show system schema module juniper-command 2>/dev/null | match module
```

```bash
terraform providers 2>/dev/null | grep -i junos || echo "junos-terraform / Juniper.Device provider"
```

**Expected result:** the enabled management services — Junos automation runs through
the **management process (mgd)** for config (NETCONF/RESTCONF/CLI over the candidate
DB), the **Juniper Extension Toolkit (JET)** service process for on-box apps, and
declarative tooling like **Terraform**; each is an entry point for a different style.

**Negative test:** automate against a device with all management services disabled;
every off-box tool fails to connect — a management service (NETCONF/REST/gRPC) must
be on.

**Cleanup:** none (read-only).

### Lab 6.2 — gRPC and gNMI (Objective: gRPC)

**Objective:** Use gNMI/gRPC for config and streaming telemetry.

```bash
gnmic -a $JUNOS:32767 -u admin -p $PW --insecure get --path "/interfaces/interface[name=ge-0/0/0]/state/counters"
gnmic -a $JUNOS:32767 -u admin -p $PW --insecure subscribe --path "/interfaces/interface/state/counters" --stream-mode sample --sample-interval 10s
```

**Expected result:** the interface counters via gNMI GET and a streaming
subscription — **gRPC** (with protobuf) carries **gNMI** for OpenConfig-modeled
config/telemetry; sensor paths stream to a collector (the TIG stack — Telegraf/
InfluxDB/Grafana), pushing state rather than polling.

**Negative test:** subscribe to an OpenConfig path the device does not model; the
subscription returns nothing — the sensor path must exist in a supported model.

**Cleanup:** stop the subscription.

### Lab 6.3 — Ansible (Objective: Ansible)

**Objective:** Configure Junos with Ansible and validate with JSNAPy.

```bash
cat > pb.yml <<'YML'
- hosts: junos
  connection: local
  gather_facts: no
  tasks:
    - juniper.device.config:
        load: set
        lines: ["set system host-name AUTO-R1"]
        commit: true
YML
ansible-playbook -i inv pb.yml | grep -E 'changed|ok='
```

**Expected result:** the play applying and committing the change idempotently —
**Ansible** automates Junos via the `juniper.device` collection: playbooks load
config (with Jinja2 templates and Vault for secrets) and **JSNAPy** snapshots and
diffs operational state to validate a change did only what was intended.

**Negative test:** re-run the same play; `changed=0` — idempotence means no redundant
change, and JSNAPy would flag any unexpected state delta.

**Cleanup:** revert the host-name via a follow-up play or `rollback`.

### Lab 6.4 — Junos Automation Scripts (Objective: Junos Automation Scripts)

**Objective:** Read on-box automation scripts (commit/op/event/SNMP).

```text
show configuration system scripts
show system scripts op 2>/dev/null
show system commit
```

**Expected result:** the configured scripts and commit history — on-box scripts
extend Junos: **commit scripts** enforce/adjust config at commit, **op scripts** add
custom operational commands, **event scripts** react to syslog events, and **SNMP
scripts** serve custom OIDs — all running in the RE (SLAX/Python).

**Negative test:** a commit script that raises an error aborts the commit — commit
scripts can enforce policy by failing non-compliant candidate configs.

**Cleanup:** none (read-only).

### Lab 6.5 — YANG (Objective: YANG)

**Objective:** Read a Junos/OpenConfig YANG model tree.

```bash
pyang -f tree junos-conf-interfaces.yang 2>/dev/null | head -20 || \
  echo "Junos ships native + OpenConfig YANG; load OpenConfig with 'set system services ...'"
```

**Expected result:** the model tree (containers/lists/leaves) — Junos config and
state are described by **YANG** (native `junos-conf-*` models and **OpenConfig**);
every NETCONF/RESTCONF/gNMI operation manipulates YANG-modeled data, and pyang
renders the schema for building payloads.

**Negative test:** send config for an OpenConfig path without loading the OpenConfig
package/translation; the device rejects it — the model must be supported/loaded.

**Cleanup:** none.

### Lab 6.6 — NETCONF and PyEZ (Foundational: JNCIA-DevOps)

**Objective:** Connect with PyEZ and read/change config over NETCONF.

```bash
python3 - <<'PY'
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
with Device(host="JUNOS", user="admin", passwd="PW") as dev:
    print("model:", dev.facts["model"], "version:", dev.facts["version"])
    with Config(dev, mode="exclusive") as cu:
        cu.load("set system host-name PYEZ-R1", format="set")
        print(cu.diff())
        cu.rollback()   # discard for the lab
PY
```

**Expected result:** the device facts and a candidate diff (then rolled back) —
**PyEZ** (`junos-eznc`) is Juniper's Python NETCONF library: it gathers facts, loads
and commits config (with locking and diff), and runs RPCs, the foundation of
off-box Junos automation.

**Negative test:** load malformed `set` syntax; PyEZ raises a `ConfigLoadError` with
the parse error — structured errors, not silent failure.

**Cleanup:** the script rolls back; no change persists.

### Lab 6.7 — REST API (Foundational: JNCIA-DevOps)

**Objective:** Call the Junos REST API to run an RPC.

```bash
curl -sk -u admin:$PW "https://$JUNOS:3443/rpc/get-software-information" -H 'Accept: application/json' | jq '.' | head
```

**Expected result:** the software information as JSON — the Junos **REST API** (once
`set system services rest` is enabled) exposes every operational RPC and config over
HTTP(S), returning XML or JSON, so simple HTTP clients automate Junos without a
NETCONF library.

**Negative test:** call the REST API without `set system services rest http/https`;
the connection is refused — the REST service must be enabled and (best practice)
TLS-secured.

**Cleanup:** none (read-only RPC).

### Lab 6.8 — Cloud and SDN Foundations (Foundational: JNCIA-Cloud)

**Objective:** Identify SDN/NFV/cloud constructs (containers, overlay, CN2).

```bash
kubectl get pods -n contrail 2>/dev/null | head || kubectl get pods -A | head
kubectl get virtualnetworks -A 2>/dev/null | head
```

**Expected result:** the SDN controller/CNI pods and virtual networks — the cloud
track covers **SDN** (a controller programming the fabric — Juniper CN2/Contrail),
**NFV** (network functions as software), and **cloud-native** networking (Kubernetes
CNI, overlay virtual networks), the substrate DevOps automation targets.

**Negative test:** expect pod-to-pod policy without a CNI that enforces it; a default
CNI may allow all — the SDN/CNI provides the segmentation the cloud design needs.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the rendered config matched intent, the guarded
push confirmed only after JSNAPy passed, the induced template failure
rolled back automatically with proof from `show system commit`, and
one telemetry stream captured a live counter series.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] NETCONF/PyEZ round trip working with structured data
- [ ] Git-sourced template push with commit-confirmed guardrails
- [ ] JSNAPy pre/post checks gating the change
- [ ] gNMI telemetry subscription demonstrated
- [ ] DevOps and Cloud exam scopes (JN0-224/423/214) recorded
