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
and AI 15%, and DCAUTO's domains — programmability foundation 10%,
controller-based 30%, device-centric 30%, compute 30% — are this
chapter's outline in exam form.

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
DCAUTO split — controller-based versus device-centric — is exactly
this section versus the previous one.

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
- DCAUTO 300-635 v1.1 exam topics (rebranding to DCNAUTO under CCNP
  Automation — same code)

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

Automate the volume's estate end to end: (1) NX-API queries returning
EVPN peer state as JSON from two leaves; (2) the Ansible role that
renders a *new* L2VNI onto all four leaves from a data-file entry,
with post-condition asserts — run it twice and prove the second run
changes nothing; (3) the Terraform configuration reproducing Chapter
03's tenant from empty state, with the plan artifact saved; (4) drift:
hand-edit one leaf's VNI config, and demonstrate detection (Ansible
check mode diff or NDFC compliance where available) before repairing
by re-run.

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
diffable, assertable state. The DCAUTO exam splits along the same
lines this chapter does — foundation, controller-based,
device-centric, compute — and the habits here (idempotency, external
truth, post-condition asserts) are what Chapters 07–09 assume.

- [ ] I pulled structured state through NX-API and knew which style I
      was using
- [ ] My VNI role is provably idempotent with built-in asserts
- [ ] Terraform holds my tenant as intent with plan artifacts
- [ ] I detected drift before repairing it
