# Chapter 06: Data Center Automation: NX-API, Models, and Tooling

## Learning Objectives

- Use NX-API in both CLI and REST styles, and know when each fits
- Explain model-driven programmability on NX-OS: YANG, NETCONF and
  RESTCONF, and streaming telemetry
- Automate the three planes of this volume — NX-OS fabrics, the APIC,
  and UCS/Intersight — with Ansible and Terraform
- Describe NDFC's role as fabric controller and API surface for NX-OS
  estates
- Build idempotent, testable automation and validate what it changed

## Theory and Architecture

### Why data center automation is its own chapter

Volume IX teaches automation as a discipline; this chapter applies it
to the platforms of Chapters 02–05, because the data center is where
automation stops being optional. A VXLAN EVPN leaf takes ~200 lines of
patterned configuration; a tenant onboarding touches fabric, ACI, UCS,
and zoning; and drift between "the standard" and "what is on box 47"
is how outages incubate. The blueprint agrees: DCCOR gives Automation
and AI 15%, and DCNAUTO's v2.0 domains — automation foundation 15%,
infrastructure as code 25%, element programmability 25%, operations
25%, AI in automation 15% — are this chapter's outline in exam form.

### The device APIs

**NX-API** exposes NX-OS over HTTPS in two styles. *NX-API CLI* wraps
show/config commands in JSON — the low-friction entry that returns
structured versions of what you already know. *NX-API REST* addresses
the same object model DME holds internally — closer to ACI's style.
Practical rule: CLI style for operational queries and quick tooling,
REST or models for configuration state you intend to manage.

**Model-driven programmability** replaces screen-scraping with typed
state: **YANG** models describe configuration and operational data,
**NETCONF** (XML, transactional, candidate configs) and **RESTCONF**
(HTTP verbs on the same models) transport it. The payoff compounds
with **model-driven telemetry**: the switch streams counters and state
(gNMI/gRPC dial-out) instead of being polled — the difference between
watching the fabric and asking it occasionally.

### The controller APIs

The **APIC** is one big REST API — Chapter 03's JSON payloads are the
native tongue, and everything the UI does maps to objects under
`/api/mo/uni`. **Intersight** is API-first SaaS with typed SDKs.
**NDFC** (on Nexus Dashboard) is the controller for NX-OS fabrics:
underlay/overlay provisioning from templates, configuration compliance
(it diffs actual against intended and can enforce), imaging, and a
REST API that makes "fabric as data" real for non-ACI estates. The
DCNAUTO split — controller-level versus device-level programmability —
is exactly this section versus the previous one.

### The tools

**Ansible** with `cisco.nxos`, `cisco.aci`, `cisco.ucs`, and
`cisco.intersight` collections: task-oriented, agentless, right for
config rendering and operational orchestration. **Terraform** with ACI
and Intersight providers: state-managed intent, right where you want
plan/apply semantics and drift detection for controller objects.
**Python** with `requests`/SDKs for everything glue. Choose per plane:
Terraform shines against controllers (ACI tenants, Intersight
profiles); Ansible shines against device fleets and mixed workflows;
both beat artisanal SSH loops everywhere.

## Design Considerations

- **Idempotency is the entry bar**: a playbook run twice must change
  nothing the second time — that is what makes automation safe to run
  on Fridays.
- **Source of truth outside the devices**: variables (VNIs, tenants,
  pools) in git-versioned data files (or NetBox — Volume XXVI built
  one); templates render config; devices hold rendered output, never
  the master.
- **Test against virtual first**: the CML fabric and ACI Simulator
  are CI targets; production fabrics get changes that already passed
  somewhere.
- **Read scale honestly**: streaming telemetry and NDFC compliance
  find drift; without them your automation is write-only and blind.

## Implementation and Automation

NX-API CLI style — structured operational state in four lines:

```python
import requests
payload = {"ins_api": {"version": "1.0", "type": "cli_show",
  "chunk": "0", "sid": "1", "input": "show bgp l2vpn evpn summary",
  "output_format": "json"}}
r = requests.post("https://leaf1/ins", json=payload,
                  auth=("automation", "…"), verify=False)
peers = r.json()["ins_api"]["outputs"]["output"]["body"]
```

Ansible rendering the Chapter 02 leaf pattern from data:

```yaml
# group_vars/leaves.yml defines vnis: [{vlan: 2001, vni: 20001, ...}]
- name: Render VXLAN EVPN leaf configuration
  hosts: leaves
  gather_facts: false
  tasks:
    - name: Ensure VLAN-to-VNI mappings
      cisco.nxos.nxos_vlans:
        config: "{{ vnis | map(attribute='vlan_cfg') | list }}"
        state: merged
    - name: Ensure NVE members
      cisco.nxos.nxos_config:
        src: templates/nve_members.j2   # loops vnis, ingress-replication
    - name: Verify EVPN peers after change
      cisco.nxos.nxos_command:
        commands: [show bgp l2vpn evpn summary | json]
      register: evpn
    - name: Fail if any peer is not Established
      ansible.builtin.assert:
        that: "'Idle' not in evpn.stdout[0] and 'Active' not in evpn.stdout[0]"
```

Terraform expressing a Chapter 03 tenant as intent:

```hcl
resource "aci_tenant" "tenant_a" { name = "TENANT-A" }
resource "aci_vrf" "vrf_a" {
  tenant_dn = aci_tenant.tenant_a.id
  name      = "VRF-A"
}
resource "aci_bridge_domain" "bd_web" {
  tenant_dn          = aci_tenant.tenant_a.id
  name               = "BD-WEB"
  relation_fv_rs_ctx = aci_vrf.vrf_a.id
}
# terraform plan now *is* the change review artifact.
```

## Validation and Troubleshooting

Automation gets validated like any other change, plus its own layer:
**assert after apply** (the playbook above fails itself if EVPN peers
drop — post-conditions belong in the automation, not in hope);
**diff before apply** (Terraform plan, Ansible `--check --diff`, NDFC
compliance preview); **drift detection on a schedule**, because the
fabric someone hand-edited is the fabric your next run reverts at an
unexpected moment — which is an argument for alerting on drift, not
silently enforcing. Troubleshooting the tooling itself: NX-API 400s
are usually feature-not-enabled or malformed chunked commands; APIC
API errors name the failing object and are more honest than most
UIs; Ansible idempotency failures ("changed" every run) trace to
templates fighting device-default rendering — compare against
`show run` semantics, not your intentions.

## Security and Best Practices

- Dedicated automation accounts, AAA-backed, least-privileged (NDFC
  and APIC both scope tokens/roles); no shared human credentials in
  vaults, no credentials at all in repositories.
- Certificates verified in production requests — the `verify=False`
  in lab snippets is a lab artifact, flagged so it never migrates.
- Every automated change leaves an artifact: plan output, diff, or
  assert results attached to the change record. Auditable automation
  is the kind that survives its first incident review.

## References and Knowledge Checks

- Cisco NX-OS programmability guide (NX-API, NETCONF, telemetry)
- Cisco DevNet: ACI, NDFC, and Intersight API documentation and
  sandboxes
- DCNAUTO 300-635 v2.0 exam topics (formerly DCAUTO v1.1 — same
  code)

Knowledge checks:

1. NX-API CLI versus REST style: what does each address, and which
   would you pick for managing configuration state long-term?
2. What do PFC-style guarantees have in common with idempotency —
   why is each the precondition for trusting the layer above it?
3. Where should the VNI numbering for a fabric live, and what role do
   the switches then play with respect to truth?
4. Your tenant playbook reports "changed" on every run against an
   unchanged fabric. Name two likely causes and the diagnosis path.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **Objectives 4.1–4.2 of
DCCOR 350-601 v1.2 (automation) and every objective of the DCNAUTO 300-635 v2.0
exam guide** — YANG models, NETCONF/gNMI/gRPC, Infrastructure as Code
(Jinja2/Ansible/Terraform), NX-OS programmability, model-driven telemetry,
source of truth, and AI-in-automation — mapped in the volume README's coverage
tables. DCNAUTO v2.0 is a shared concentration for **CCNP Data Center and the
CCNP Automation** track. Labs use a Linux workstation with Python 3, `git`,
`ansible`, `terraform`, `pyats`, and `ncclient`, plus reachable NX-OS, APIC, and
Nexus Dashboard endpoints. Each ends **`**Lab verified by:** *pending*`** until
a human runs it.

**Shared prerequisites for Labs 6.1–6.28** — a workstation with Python 3.11+,
`git`, Ansible with `cisco.aci`/`cisco.nxos`/`cisco.dcnm` collections, Terraform
with the `ciscodevnet/aci` and `dcnm` providers, `pyats[full]`, `ncclient`,
`pyang`, and YANG Suite; an NX-OS switch with NETCONF/gNMI/NX-API at `$NXOS`, an
APIC at `$APIC`, and a Nexus Dashboard at `$ND`. **Cost:** none beyond lab
resources.

### Lab 6.1 — Implement automation and scripting tools (DCCOR Objective 4.1)

**Objective:** Push a config change to NX-OS via NX-API from a script.

```bash
curl -sk -u admin:$PW https://$NXOS/ins -H 'Content-Type: application/json-rpc' -d '
[{"jsonrpc":"2.0","method":"cli","params":{"cmd":"show version","version":1},"id":1}]' \
 | jq -r '.result.body."kickstart_ver_str"'
```

**Expected result:** the NX-OS version returned as JSON — NX-API turns the CLI
into a programmable REST/JSON-RPC endpoint scripts can drive.

**Negative test:** call NX-API without `feature nxapi` enabled; the connection
is refused — the feature must be on.

**Cleanup:** none (read-only call).

### Lab 6.2 — Evaluate automation and orchestration technologies (DCCOR Objective 4.2)

**Objective:** Contrast a configuration tool (Ansible, push) with an
orchestrator (Terraform, declarative state).

```bash
ansible --version | head -1
terraform version | head -1
terraform plan -no-color | tail -5
```

**Expected result:** Ansible reports its version (imperative, agentless push);
Terraform's plan shows a desired-state diff (`+/-/~`) — orchestration tracks
state and converges, configuration management runs tasks.

**Negative test:** run `terraform apply` with drift introduced out-of-band; the
next `plan` shows the drift as changes to reconcile — state tracking is the
difference from a fire-and-forget script.

**Cleanup:** none (plan does not modify infrastructure).

### Lab 6.3 — Describe OpenConfig, IETF, and native YANG models (DCNAUTO Objective 1.1)

**Objective:** List the YANG models a switch supports and compare native to
OpenConfig.

```bash
ssh -s admin@$NXOS netconf <<'XML'
<rpc message-id="1"><get-schema xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"/></rpc>
XML
pyang -f tree Cisco-NX-OS-device.yang | head
pyang -f tree openconfig-interfaces.yang | head
```

**Expected result:** the model list and two trees — the **native**
(`Cisco-NX-OS-device`) model exposes platform-specific structure, while
**OpenConfig** and **IETF** models are vendor-neutral; DCNAUTO expects you to
know when each applies.

**Negative test:** request a model the switch does not implement; NETCONF
returns `data-missing` — you can only drive models the device supports.

**Cleanup:** none (read-only).

### Lab 6.4 — Describe ACI network-centric mode: EPG, BD, contracts, VRFs (DCNAUTO Objective 1.2)

**Objective:** Read the ACI objects a network-centric deployment maps VLANs to.

```bash
curl -sk -b cookie.txt "https://$APIC/api/class/fvBD.json" | jq -r '.imdata[].fvBD.attributes.name' | head
curl -sk -b cookie.txt "https://$APIC/api/class/vzBrCP.json" | jq -r '.imdata[].vzBrCP.attributes.name' | head
```

**Expected result:** bridge domains and contracts (`vzBrCP`) — in
network-centric mode each VLAN becomes a BD+EPG and contracts replace ACLs, the
1:1 mapping that eases migration from a traditional fabric.

**Negative test:** two EPGs with no contract between them cannot communicate —
network-centric mode still enforces the ACI allow-list model, unlike a flat
VLAN.

**Cleanup:** none (read-only).

### Lab 6.5 — Describe DPUs in data center network switches (DCNAUTO Objective 1.3)

**Objective:** Identify a smart-NIC/DPU and the services it offloads.

```bash
ssh admin@$NXOS 'show inventory | include DPU|SmartNIC' 2>/dev/null
lspci | grep -iE 'DPU|BlueField|Pensando'    # on a DPU-equipped host
```

**Expected result:** the DPU/smart-NIC present in the switch or host — a DPU
offloads networking, security, and storage services from the host CPU
(east-west firewalling, encryption, telemetry) at line rate.

**Negative test:** a server with a standard NIC shows no DPU; those services
fall back to host CPU, consuming cores the workload needs — the contrast is the
DPU's value.

**Cleanup:** none (read-only).

### Lab 6.6 — Describe NETCONF, gNMI, gRPC, and gNOI (DCNAUTO Objective 1.4)

**Objective:** Exercise a NETCONF get and a gNMI get against the same switch.

```bash
# NETCONF (SSH/XML, RFC 6241)
ssh -s admin@$NXOS netconf <<'XML'
<rpc message-id="1"><get><filter><System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"/></filter></get></rpc>
XML
# gNMI (gRPC transport, protobuf)
gnmic -a $NXOS:50051 -u admin -p $PW --insecure get --path "/interfaces/interface" | head
```

**Expected result:** NETCONF returns XML over SSH; gNMI returns structured data
over gRPC — NETCONF/gNMI are configuration protocols, gRPC is the transport, and
gNOI carries operational RPCs (reboot, ping); knowing which does what is the
objective.

**Negative test:** call gNMI without `feature grpc`; the gRPC dial fails — each
protocol needs its feature enabled.

**Cleanup:** none (read-only).

### Lab 6.7 — Construct a gRPC payload from a YANG module (DCNAUTO Objective 1.5)

**Objective:** Use pyang/YANG Suite to build a valid gNMI payload from a model.

```bash
pyang -f sample-xml-skeleton openconfig-interfaces.yang -o skeleton.xml
gnmic -a $NXOS:50051 -u admin -p $PW --insecure set \
  --update-path "/interfaces/interface[name=eth1/5]/config/description" \
  --update-value "set-by-gnmi"
gnmic -a $NXOS:50051 -u admin -p $PW --insecure get --path "/interfaces/interface[name=eth1/5]/config/description"
```

**Expected result:** the description read back as `set-by-gnmi` — YANG Suite and
pyang generate the path/payload from the model so you construct valid gRPC/gNMI
requests instead of guessing structure.

**Negative test:** send a payload with a path not in the model; the device
rejects it with a schema error — the YANG model is the contract.

**Cleanup:** clear the test description.

### Lab 6.8 — Describe Infrastructure as Code and GitOps (DCNAUTO Objective 2.1)

**Objective:** Model a fabric change as code in Git and show the GitOps flow.

```bash
git init fabric-iac && cd fabric-iac
echo "interface eth1/5\n description prod" > eth1_5.cfg
git add . && git commit -m "declare eth1/5"
git log --oneline
```

**Expected result:** the config committed with history — IaC treats
configuration as version-controlled source; GitOps makes the Git repo the
desired-state authority a pipeline reconciles onto the fabric.

**Negative test:** change the device out-of-band; without a reconcile pipeline
the repo and fabric diverge — GitOps requires the pipeline to close the loop.

**Cleanup:** `cd .. && rm -rf fabric-iac`.

### Lab 6.9 — Construct Jinja2 configuration templates (DCNAUTO Objective 2.2)

**Objective:** Render device config from a Jinja2 template with loops and
conditionals.

```bash
python3 - <<'PY'
from jinja2 import Template
t=Template("""{% for v in vlans %}vlan {{ v.id }}
  name {{ v.name|upper }}
{% if v.svi %}interface Vlan{{ v.id }}
  ip address {{ v.svi }}{% endif %}
{% endfor %}""")
print(t.render(vlans=[{"id":10,"name":"web","svi":"10.0.10.1/24"},{"id":20,"name":"db","svi":None}]))
PY
```

**Expected result:** rendered config with VLAN 10 getting an SVI and VLAN 20 not
— loops, conditionals, and the `upper` filter turn structured data into device
config, the core of templated automation.

**Negative test:** reference an undefined variable in the template; Jinja2
raises `UndefinedError` (with `StrictUndefined`) — catching template errors
before push is the point.

**Cleanup:** none.

### Lab 6.10 — Construct an Ansible playbook with controller and device collections (DCNAUTO Objective 2.3)

**Objective:** Use `cisco.dcnm` (controller) and `cisco.nxos` (device) in one
play.

```bash
cat > play.yml <<'YML'
- hosts: dcnm
  gather_facts: no
  tasks:
    - cisco.dcnm.dcnm_network: {fabric: FAB1, state: query}
- hosts: nxos
  gather_facts: no
  tasks:
    - cisco.nxos.nxos_vlans:
        config: [{vlan_id: 30, name: AUTO30}]
        state: merged
YML
ansible-playbook -i inv play.yml | grep -E 'changed|ok='
```

**Expected result:** the controller task queries NDFC fabrics and the device
task merges VLAN 30 — controller collections drive the fabric intent, device
collections drive box-level config, and both are idempotent.

**Negative test:** run the device task against a switch already having VLAN 30;
`changed=0` — merged state only acts on drift.

**Cleanup:** re-run the device task with `state: deleted` for VLAN 30.

### Lab 6.11 — Construct a Terraform plan with controller and device providers (DCNAUTO Objective 2.4)

**Objective:** Author a plan using the ACI (controller) and DCNM providers.

```bash
cat > main.tf <<'TF'
terraform { required_providers {
  aci  = { source = "ciscodevnet/aci" }
  dcnm = { source = "CiscoDevNet/dcnm" } } }
resource "aci_tenant" "t" { name = "TF-DC" }
TF
terraform init -no-color >/dev/null && terraform plan -no-color | grep -E 'aci_tenant.t|Plan:'
```

**Expected result:** `Plan: 1 to add` — the controller provider declares fabric
intent (a tenant) as tracked state, versus the device provider that manages
box-level resources; both converge to declared state.

**Negative test:** `plan` again after apply/import; `0 to add` — state tracking
prevents duplicate creation.

**Cleanup:** `terraform destroy` or delete tenant `TF-DC`.

### Lab 6.12 — Troubleshoot Ansible and Terraform automation (DCNAUTO Objective 2.5)

**Objective:** Diagnose a failing IaC run to its layer.

```bash
ansible-playbook -i inv play.yml -vvv 2>&1 | grep -E 'FAILED|401|403|Unreachable'
terraform plan -no-color 2>&1 | grep -E 'Error:|will be'
```

**Expected result:** the failing task/HTTP status or provider error —
`401/403` is credentials/RBAC, `Unreachable` is connectivity/feature, and a
Terraform `Error:` names the provider issue or state drift; the signal localizes
the layer.

**Negative test:** rewrite playbook logic when the cause is a `403` (account
lacks a role) — check auth and reachability before logic.

**Cleanup:** fix the named cause; re-run to a clean result.

### Lab 6.13 — Python automation with ncclient (DCNAUTO Objective 3.1)

**Objective:** Manage and monitor NX-OS config via NETCONF from Python.

```bash
python3 - <<'PY'
from ncclient import manager
with manager.connect(host="NXOS",port=830,username="admin",password="PW",
                     hostkey_verify=False,device_params={'name':'nexus'}) as m:
    cfg = m.get_config(source='running').data_xml
    print("running config bytes:", len(cfg))
PY
```

**Expected result:** the running config retrieved over NETCONF — `ncclient` is
the Python NETCONF client for programmatic get/edit-config with candidate/commit
semantics.

**Negative test:** `edit-config` malformed XML; NETCONF returns an `rpc-error`
the script must handle — structured errors, unlike screen-scraping.

**Cleanup:** discard any candidate changes (no commit).

### Lab 6.14 — Day-0 provisioning with POAP (DCNAUTO Objective 3.2)

**Objective:** Read the POAP path a switch uses at first boot.

```text
show boot
dir bootflash: | include poap
show file bootflash:poap_script.py | head
```

**Expected result:** the POAP script staged on bootflash — at Day-0 the switch
DHCPs, downloads this script, and pulls its image/config unattended, the
zero-touch device-level provisioning DCNAUTO expects.

**Negative test:** a switch with a saved startup-config skips POAP entirely —
POAP runs only on an unprovisioned box.

**Cleanup:** none (read-only).

### Lab 6.15 — On-box programmability and automation with NX-OS (DCNAUTO Objective 3.3)

**Objective:** Run a Python script from the switch's on-box interpreter.

```text
python3
>>> from cli import cli
>>> print(cli("show interface brief | include up | count"))
>>> exit()
```

**Expected result:** the count of up interfaces printed from Python running *on*
the switch — the on-box `cli`/`clid` bindings let EEM and scripts act locally,
including scheduled and event-driven automation.

**Negative test:** call `cli()` with an invalid command; it raises an exception
the script must catch — on-box scripts still get CLI errors.

**Cleanup:** none.

### Lab 6.16 — Describe templates and policies in Nexus Dashboard (DCNAUTO Objective 3.4)

**Objective:** Read the fabric/network templates NDFC applies.

```bash
curl -sk -H "Authorization: $NDFC_TOK" \
  "https://$ND/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates" \
  | jq -r '.[].name' | head
```

**Expected result:** the template names (e.g., `Easy_Fabric`,
`Default_Network_Universal`) — NDFC drives fabric intent through templates and
policies, so a change to a template re-renders config across the fabric
consistently.

**Negative test:** edit a switch's config directly out-of-band; NDFC flags it as
**out-of-sync** against the template — the template, not the box, is the
authority.

**Cleanup:** none (read-only).

### Lab 6.17 — Construct network configuration templates with Nexus Dashboard (DCNAUTO Objective 3.5)

**Objective:** Create a network via the NDFC template API and attach it.

```bash
curl -sk -X POST -H "Authorization: $NDFC_TOK" -H 'Content-Type: application/json' \
  "https://$ND/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/FAB1/networks" \
  -d '{"networkName":"AUTO-NET","networkTemplate":"Default_Network_Universal",
       "networkTemplateConfig":"{\"vlanId\":\"310\",\"vrfName\":\"TF-DC\"}"}'
curl -sk -H "Authorization: $NDFC_TOK" ".../networks/AUTO-NET" | jq '.networkName'
```

**Expected result:** the network created from the universal template — NDFC
renders the per-switch config from the template so the automation declares
intent, not device syntax.

**Negative test:** POST with a VLAN outside the fabric's pool; NDFC rejects it —
templates validate against fabric settings.

**Cleanup:** DELETE the `AUTO-NET` network.

### Lab 6.18 — Describe the capabilities and features of NX-API (DCNAUTO Objective 3.6)

**Objective:** Compare NX-API CLI (JSON-RPC) and NX-API REST (DME) on one
switch.

```bash
# NX-API CLI: wraps show/config commands as JSON-RPC
curl -sk -u admin:$PW https://$NXOS/ins -d '[{"jsonrpc":"2.0","method":"cli","params":{"cmd":"show hostname","version":1},"id":1}]' | jq '.result'
# NX-API REST: the DME object model
curl -sk -u admin:$PW "https://$NXOS/api/mo/sys/intf.json?rsp-subtree=children" | jq '.imdata | length'
```

**Expected result:** JSON-RPC returns command output; NX-API REST returns DME
managed objects — NX-API exposes both a command-oriented and a model-oriented
interface over HTTP(S).

**Negative test:** call the DME path with a wrong class; the switch returns an
error — the DME model, like ACI's, is closed.

**Cleanup:** none (read-only).

### Lab 6.19 — Describe network topology simulation for operations (DCNAUTO Objective 4.1)

**Objective:** Stand up a simulated topology to validate automation before
production.

```bash
# Cisco Modeling Labs API: list running simulations
curl -sk -u admin:$PW "https://$CML/api/v0/labs" | jq -r '.[]' | head
containerlab inspect 2>/dev/null | head    # or a containerlab topology
```

**Expected result:** the simulated labs/nodes — CML or containerlab reproduces
the fabric so playbooks and Terraform plans are validated against a digital twin
before touching production.

**Negative test:** run destructive automation straight at production with no
simulation stage; there is no safe rollback rehearsal — simulation is the safety
net the objective teaches.

**Cleanup:** stop the test simulation.

### Lab 6.20 — Change validation with pyATS (DCNAUTO Objective 4.2)

**Objective:** Snapshot state before/after a change and diff it with pyATS.

```bash
pyats learn interface --testbed-file tb.yml --output pre
# ... apply the change ...
pyats learn interface --testbed-file tb.yml --output post
pyats diff pre post
```

**Expected result:** a structured diff of interface state pre vs post — pyATS
turns "did my change do only what I intended" into an automated, repeatable
check, the operational guardrail for automation.

**Negative test:** apply a change that alters state you did not intend; the diff
surfaces the unexpected delta — validation catches side effects a blind push
misses.

**Cleanup:** `rm -rf pre post`.

### Lab 6.21 — Describe model-driven telemetry architecture (DCNAUTO Objective 4.3)

**Objective:** Identify the sensor-group, destination, and subscription
components.

```text
show telemetry control database
show telemetry control database sensor-groups
show telemetry control database destination-groups
```

**Expected result:** the three MDT building blocks — a **sensor-group** (what
YANG paths), a **destination-group** (where/encoding/transport), and a
**subscription** (cadence tying them) — the architecture push telemetry is built
from.

**Negative test:** a subscription referencing a nonexistent sensor-group streams
nothing — every component must resolve.

**Cleanup:** none (read-only).

### Lab 6.22 — Configure a model-driven telemetry subscription on NX-OS (DCNAUTO Objective 4.4)

**Objective:** Configure a gNMI/gRPC MDT subscription and confirm it streams.

```text
config t
 feature telemetry
 telemetry
  sensor-group 20
   path "sys/intf" depth 1
  destination-group 20
   ip address 10.0.0.200 port 57500 protocol gRPC encoding GPB
  subscription 20
   snsr-grp 20 sample-interval 10000
   dst-grp 20
end
show telemetry control database subscriptions
```

**Expected result:** subscription 20 streaming interface state every 10s over
gRPC — the configured push pipeline a collector consumes.

**Negative test:** point the destination at an unreachable collector;
`show telemetry transport` shows the connection failing — telemetry is only as
good as the receiver.

**Cleanup:** `no feature telemetry`.

### Lab 6.23 — Integrate with a network source of truth (DCNAUTO Objective 4.5)

**Objective:** Drive automation from NetBox (SoT) as the inventory authority.

```bash
curl -s -H "Authorization: Token $NB_TOK" "https://$NETBOX/api/dcim/devices/?role=leaf" \
  | jq -r '.results[] | "\(.name) \(.primary_ip.address)"'
ansible-inventory -i netbox_inventory.yml --list | jq '.leaf.hosts'
```

**Expected result:** the leaf inventory pulled from NetBox and fed to Ansible —
a source of truth makes the SoT (not a hand-edited file) the authority for
inventory and intended state, so automation and reality stay aligned.

**Negative test:** run automation from a stale static inventory; it targets
decommissioned or missing devices — the SoT integration is what prevents drift.

**Cleanup:** none (read-only).

### Lab 6.24 — Python script retrieving health via CLI and Nexus Dashboard (DCNAUTO Objective 4.6)

**Objective:** Pull health data from NX-OS and Nexus Dashboard in one script.

```bash
python3 - <<'PY'
import requests, json, urllib3; urllib3.disable_warnings()
# device-level via NX-API
r=requests.post("https://NXOS/ins",auth=("admin","PW"),verify=False,
  json=[{"jsonrpc":"2.0","method":"cli","params":{"cmd":"show system resources","version":1},"id":1}])
print("cpu idle:", r.json()["result"]["body"].get("cpu_state_idle"))
# fabric-level via Nexus Dashboard Insights (token in header)
h=requests.get("https://ND/sedgeapi/v1/cisco-nir/api/api/telemetry/v2/anomalies/summary",
  headers={"Authorization":"TOK"},verify=False)
print("anomalies:", h.json().get("totalItemsCount"))
PY
```

**Expected result:** CPU idle from the device and the fabric anomaly count from
Nexus Dashboard — a health-collection script correlates box-level and
fabric-level signals programmatically.

**Negative test:** an expired ND token returns `401`; the script must
re-authenticate — robust health collectors handle token refresh.

**Cleanup:** none (read-only).

### Lab 6.25 — Troubleshoot packet flow for containerized workloads on Linux (DCNAUTO Objective 4.7)

**Objective:** Trace a container's path through veth, bridge, bond, and VLAN
subinterfaces.

```bash
ip -br link show type veth
bridge link show
ip -d link show bond0 ; ip -d link show bond0.100
ip netns exec pod1 ip route
```

**Expected result:** the veth pair into the bridge, the bond and its `.100` VLAN
subinterface, and the pod's route — the Linux constructs a container's traffic
traverses to reach the fabric.

**Negative test:** a pod whose veth is not enslaved to the bridge has no
connectivity; `bridge link` omits it — the missing enslavement is the fault.

**Cleanup:** none (read-only).

### Lab 6.26 — Describe AI-assisted code development for network automation (DCNAUTO Objective 5.1)

**Objective:** Use an AI assistant to draft automation, then validate it.

```bash
# an AI assistant drafts a playbook; you validate before trusting it
ansible-lint drafted_play.yml
ansible-playbook --syntax-check drafted_play.yml
ansible-playbook --check drafted_play.yml   # dry run
```

**Expected result:** lint/syntax/dry-run results on AI-generated code — AI
accelerates authoring, but the objective is that generated automation is
**validated** (lint, syntax, check-mode) before it ever runs against the fabric.

**Negative test:** apply AI-drafted automation without review; a hallucinated
module or wrong idempotence can change unintended state — validation is
mandatory, not optional.

**Cleanup:** none (check mode makes no changes).

### Lab 6.27 — Describe security risks in AI-based network automation (DCNAUTO Objective 5.2)

**Objective:** Enumerate and check for the risks in an AI-automation pipeline.

```bash
git secrets --scan drafted_play.yml 2>/dev/null || grep -nE 'password|token|api[_-]?key' drafted_play.yml
ansible-playbook --check drafted_play.yml 2>&1 | grep -iE 'delete|erase|reload|no shutdown'
```

**Expected result:** any hardcoded secrets and any destructive tasks surfaced —
the risks are leaked credentials in prompts/output, over-broad or destructive
generated actions, prompt injection, and unvetted supply-chain modules; scanning
and dry-run are the controls.

**Negative test:** feed production credentials into an external AI prompt; they
may be logged or retained — never send secrets to an AI service, the core risk
this objective names.

**Cleanup:** none.

### Lab 6.28 — Describe AI-agent integration with devices, controllers, and platforms (DCNAUTO Objective 5.3)

**Objective:** Read how an AI agent reaches the fabric through an MCP/API layer.

```bash
# an agent calls tools that wrap the same governed APIs a human uses
curl -sk -H "Authorization: $NDFC_TOK" "https://$ND/appcenter/cisco/ndfc/api/v1/.../fabrics" | jq 'length'
echo "agent -> tool(API) -> controller -> fabric, with the API's RBAC/audit intact"
```

**Expected result:** the agent operating through the **same authenticated,
RBAC-governed, audited APIs** (NDFC, Intersight, NX-API) a human or script uses
— integration means the AI agent is another API client, not an unaudited side
channel.

**Negative test:** an agent given raw device credentials bypassing the
controller loses RBAC and audit — integration must preserve the governance the
platform APIs enforce.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the twice-run role was idempotent with asserts
passing, Terraform recreated the tenant from nothing, and the induced
drift was detected before it was repaired. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The data center automates or it drifts. NX-API and YANG models make
switches addressable, the APIC, Intersight, and NDFC make estates
addressable, and Ansible and Terraform turn patterns into rendered,
diffable, assertable state. The DCNAUTO exam splits along the same
lines this chapter does — foundation, infrastructure as code, element
programmability, operations, AI — and the habits here (idempotency, external
truth, post-condition asserts) are what Chapters 07–09 assume.

- [ ] I pulled structured state through NX-API and knew which style I
      was using
- [ ] My VNI role is provably idempotent with built-in asserts
- [ ] Terraform holds my tenant as intent with plan artifacts
- [ ] I detected drift before repairing it
