# Chapter 07: Automation — Foundations and Advanced

## Learning Objectives

- Explain the Automation track and the Professional accreditation.
- Automate EOS with eAPI and Python (pyeapi).
- Configure devices with Ansible (arista.eos) and Jinja.
- Build fabrics with Arista Validated Designs (AVD).
- Complete a walkthrough for each Automation topic.

## Theory and Architecture

The **Automation Track** has **Foundations** and **Advanced** specializations; passing all
Automation Specialist exams earns the **Professional (Automation)** accreditation. It
centers on Arista's automation stack: **eAPI** (JSON-RPC) and **pyeapi** (Python) for
programmatic control, **Ansible** with the **`arista.eos`** collection for declarative
config, **Jinja** templates and **Git** for config-as-code, **CloudVision** (CVP) as the
management/telemetry plane, and **AVD (Arista Validated Designs)** — an Ansible collection
that generates and deploys entire validated leaf-spine/EVPN fabrics from a small data model.
This is the network-as-code path for Arista.

## Design Considerations

Drive config from **data + templates** (Jinja/AVD) in **Git**, deploy with **Ansible/
CloudVision**, and validate with AVD's built-in tests. Use **eAPI/pyeapi** for custom
tooling. Treat the fabric as **code** — one data model generates consistent configs.

## Implementation and Automation

The labs use eAPI/pyeapi, Ansible arista.eos, Jinja, and AVD.

## Validation and Troubleshooting

Confirm the stack:

```text
eAPI (JSON-RPC) + pyeapi (Python). Ansible arista.eos (declarative). Jinja + Git (config-as-code).
CloudVision (deploy/telemetry). AVD: data model -> generated + validated EVPN/VXLAN fabric.
```

Common pitfalls: imperative one-off scripts instead of **AVD/Ansible**; and config drift
without a **Git** source of truth.

## Security and Best Practices

Keep the fabric **data model in Git**, generate configs with **AVD/Jinja**, deploy through
**Ansible/CloudVision** with review, and validate with **AVD tests**. Store credentials in a
vault; use eAPI/CloudVision over TLS.

## Hands-On Lab

Automation walkthroughs. **Shared prerequisites** — Python (`pip install pyeapi`), Ansible
(`ansible-galaxy collection install arista.eos arista.avd`); a cEOS switch with eAPI.
**Cost:** none.

### Lab 7.1 — eAPI with pyeapi

**Objective:** Query EOS from Python.

```python
import pyeapi
node = pyeapi.connect(transport="https", host="10.0.0.11", username="admin", password="admin")
print(node.execute(["show version"])["result"][0]["version"])
```

**Expected result:** the **EOS version** via pyeapi — programmatic control.

**Negative test:** screen-scrape CLI over SSH for structured data; **eAPI/pyeapi** returns
JSON — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Configure with Ansible arista.eos

**Objective:** Declaratively set a VLAN.

```yaml
- hosts: arista
  gather_facts: false
  tasks:
    - arista.eos.eos_vlans:
        config:
          - vlan_id: 100
            name: users
        state: merged
```

**Expected result:** VLAN 100 configured idempotently via **`arista.eos`** — declarative
config.

**Negative test:** push CLI lines with a raw command module; **`eos_vlans`** is idempotent
and structured — prefer resource modules.

**Rollback:** set `state: deleted` for the VLAN.

### Lab 7.3 — Jinja template + Git

**Objective:** Generate config from data.

```jinja
hostname {{ inventory_hostname }}
{% for v in vlans %}vlan {{ v.id }}
   name {{ v.name }}
{% endfor %}
```

**Expected result:** rendered EOS config from a **data model** (kept in Git) — config-as-
code.

**Negative test:** hand-edit each switch's config; **template from data in Git** for
consistency and review.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Build a fabric with AVD

**Objective:** Generate an EVPN fabric from a data model.

```yaml
# group_vars: define spines, leaves, and the fabric; then:
# ansible-playbook -i inventory build.yml   # AVD generates + deploys configs, runs tests
```

**Expected result:** AVD **generates and validates** the full leaf-spine/EVPN config from a
concise data model — network-as-code at fabric scale.

**Negative test:** hand-build every leaf/spine config; **AVD** generates consistent,
validated configs from one model — use it.

**Rollback:** tear down the lab fabric.

### Lab 7.5 — Deploy via CloudVision

**Objective:** Push validated config through CVP.

```text
# AVD/Ansible can deploy through CloudVision: configs staged as a Change Control,
#   reviewed, then executed fleet-wide with rollback.
"deploy: AVD -> CloudVision Change Control (review + execute + rollback)"
```

**Expected result:** config deployed through **CloudVision Change Control** — governed
fleet deployment.

**Negative test:** push directly to switches with no review/rollback; **CloudVision Change
Control** adds governance — use it in production.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Automation track (Foundations + Advanced → Professional) certifies Arista network-as-
code: eAPI/pyeapi, Ansible `arista.eos`, Jinja/Git config-as-code, AVD fabric generation,
and CloudVision-governed deployment. This chapter automated with each tool.

- [ ] I can query EOS with eAPI/pyeapi.
- [ ] I can configure with Ansible arista.eos.
- [ ] I can template config from data in Git.
- [ ] I can build a fabric with AVD and deploy via CloudVision.
- [ ] I completed Labs 7.1–7.5 including each negative test.
