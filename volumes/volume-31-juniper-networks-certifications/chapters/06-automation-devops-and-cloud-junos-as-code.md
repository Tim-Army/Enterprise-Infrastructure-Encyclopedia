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

Against the Chapter 05 fabric (or two vJunos boxes): enable NETCONF;
inventory in YAML; Jinja2 template rendering per-device BGP config;
Ansible playbook pushing with commit-confirmed; JSNAPy pre/post
asserting BGP Established and interface error deltas of zero; a gnmic
subscription streaming one interface's counters during a traffic test.
Break the push once — bad template variable — and show the pipeline
failing safely with the device untouched after the confirm window.

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
