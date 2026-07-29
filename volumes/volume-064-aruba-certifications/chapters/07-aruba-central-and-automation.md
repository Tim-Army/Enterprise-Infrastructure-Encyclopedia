# Chapter 07: Aruba Central and Automation

## Learning Objectives

- Explain Aruba Central's role and the Advanced Product Certification (APC-Central).
- Automate AOS-CX with the REST API and the pyaoscx SDK.
- Configure switches declaratively with Ansible (arubanetworks.aos_cx).
- Describe NetConductor fabric orchestration from Central.
- Complete a walkthrough for each automation topic.

## Theory and Architecture

**Aruba Central** is the cloud-native management, monitoring, and **AIOps** plane across Aruba
switches, APs, and gateways, and the subject of the **Advanced Product Certification
(APC-Central)**. Central provisions with **groups and templates**, streams telemetry for AIOps
insights, and exposes a full **REST API** so the fleet is programmable. Below Central, each
**AOS-CX** switch is independently automatable through its **built-in REST API** and Aruba's
official Python SDK, **pyaoscx**, and through the certified **Ansible collection
`arubanetworks.aos_cx`** for declarative configuration. Central also orchestrates fabrics with
**NetConductor**, building overlays (EVPN-VXLAN, roles) from intent. Together these make Aruba a
network-as-code platform: model config as data, push it with Ansible/API, and manage the fleet
from Central.

## Design Considerations

Manage the fleet through **Central groups/templates** for consistency, and drive per-device
change through **pyaoscx/Ansible** from a Git source of truth. Prefer **declarative** resource
modules over raw CLI. Use **NetConductor** to build fabrics from intent rather than by hand.

## Implementation and Automation

The labs use the AOS-CX REST API, pyaoscx, Ansible aos_cx, and the Central API.

## Validation and Troubleshooting

Confirm the automation stack:

```text
Central: groups/templates + telemetry/AIOps + REST API + NetConductor (fabric from intent).
AOS-CX: built-in REST API + pyaoscx (Python SDK) + Ansible arubanetworks.aos_cx (declarative).
Pattern: config-as-data in Git -> push via Ansible/API -> manage fleet in Central.
```

Common pitfalls: automating with **raw CLI over SSH** instead of the **REST/pyaoscx**; and
per-device config drift with no **Git** source of truth.

## Security and Best Practices

Store credentials/tokens in a vault; use the **REST API over HTTPS**. Keep the **data model in
Git**, review changes, and push through Ansible/Central. Scope API tokens least-privilege.

## Hands-On Lab

Automation walkthroughs. **Shared prerequisites** — Python (`pip install pyaoscx`), Ansible
(`ansible-galaxy collection install arubanetworks.aos_cx`), and an AOS-CX switch with the REST
API enabled. **Cost:** none with virtual.

### Lab 7.1 — Configure a VLAN with pyaoscx

**Objective:** Create a VLAN from Python.

```python
from pyaoscx.session import Session
from pyaoscx.vlan import Vlan
s = Session("10.0.0.1", "10.08")
s.open("admin", "admin")
Vlan(s, 100, name="users").create()
print("VLAN 100 created via pyaoscx")
s.close()
```

**Expected result:** VLAN 100 created through the **pyaoscx SDK** — programmatic AOS-CX config.

**Negative test:** send `configure`/`vlan 100` over SSH with a screen-scraper; **pyaoscx/REST**
is structured and idempotent — use it.

**Cleanup:** delete VLAN 100 (`Vlan(s,100).delete()`).

### Lab 7.2 — Declarative config with Ansible

**Objective:** Set a VLAN with the certified collection.

```yaml
- hosts: aoscx
  collections: [arubanetworks.aos_cx]
  tasks:
    - aoscx_vlan:
        vlan_id: 100
        name: users
        state: create
```

**Expected result:** VLAN 100 configured idempotently via **`arubanetworks.aos_cx`** —
declarative, repeatable config.

**Negative test:** push raw CLI lines with a generic module; the **aos_cx** resource modules are
idempotent — prefer them.

**Cleanup:** set `state: delete`.

### Lab 7.3 — Read state via the AOS-CX REST API

**Objective:** Query the switch database directly.

```bash
curl -sk -X POST "https://10.0.0.1/rest/v10.08/login?username=admin&password=admin" -c cj.txt >/dev/null 2>&1
curl -sk -b cj.txt "https://10.0.0.1/rest/v10.08/system?attributes=hostname,software_version" 2>/dev/null \
  | python3 -m json.tool 2>/dev/null || echo "AOS-CX REST returns structured system state (login first for a cookie)"
```

**Expected result:** hostname and software version as **JSON** from the REST API — the switch is
programmable.

**Negative test:** parse `show version` text; **REST** returns structured data — query it.

**Cleanup:** `rm -f cj.txt`.

### Lab 7.4 — Provision through Aruba Central groups

**Objective:** Describe fleet-wide config via templates.

```text
# Central: assign a switch to a GROUP with a TEMPLATE -> config applied fleet-wide, consistently.
"central: group + template -> consistent config across the fleet (not per-device)"
```

**Expected result:** the **group/template** model — consistent, scalable provisioning from
Central.

**Negative test:** configure each switch individually in Central; use **groups/templates** for
consistency at scale.

**Cleanup:** none.

### Lab 7.5 — NetConductor fabric from intent

**Objective:** Describe orchestrated overlays.

```text
# NetConductor (Central) builds EVPN-VXLAN overlays and roles from intent, then deploys to the
#   fabric switches — network-as-code for the campus/DC fabric.
"netconductor: intent -> generated EVPN-VXLAN + roles -> deployed to fabric"
```

**Expected result:** the **NetConductor** model — fabric overlays built from intent, not by
hand.

**Negative test:** hand-build every VTEP/EVPN peer; **NetConductor** generates the fabric from
intent — use it for scale.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Aruba Central manages, monitors, and orchestrates the fleet (groups/templates, AIOps, REST API,
NetConductor), while AOS-CX is automatable through its REST API, the pyaoscx SDK, and the
Ansible arubanetworks.aos_cx collection — the network-as-code stack behind APC-Central. Model
config as data in Git and push through Central/Ansible/API.

- [ ] I can configure AOS-CX with pyaoscx.
- [ ] I can configure AOS-CX declaratively with Ansible.
- [ ] I can read switch state via the REST API.
- [ ] I can explain Central groups/templates and NetConductor.
- [ ] I completed Labs 7.1–7.5 including each negative test.
