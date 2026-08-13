# Chapter 03: Switching Track

## Learning Objectives

- Explain the Switching track (ACA-S → ACP-S → ACX-S) on AOS-CX.
- Configure VLANs, trunks, and inter-VLAN routing on AOS-CX.
- Build switch redundancy with VSX and VSF.
- Use the AOS-CX REST API and database model.
- Complete a walkthrough for each Switching topic.

## Theory and Architecture

The **Switching** track certifies the AOS-CX platform itself, from **Associate (ACA-S,
HPE6-A86)** through **Professional (ACP-S, HPE7-A08)** to **Expert (ACX-S)**. **AOS-CX** is
Aruba's modern network OS built around a central **state database (OVSDB-style)** with a
**built-in REST API** — every CLI change is reflected in the database and readable over HTTPS,
which makes AOS-CX programmable by design. The track covers Layer-2 switching (VLANs, trunks,
spanning tree), Layer-3 routing (OSPF, BGP, VRFs), and Aruba's redundancy technologies:
**VSX** (Virtual Switching Extension) — two aggregation switches acting as one logical pair for
active-active, loop-free uplinks with independent control planes — and **VSF** (Virtual
Switching Framework) — stacking access switches into one managed unit. Mastery of AOS-CX
switching underpins the Campus Access and Data Center tracks.

## Design Considerations

Use **VSX** at aggregation/core for active-active redundancy without spanning-tree blocking,
and **VSF** to stack access switches for simpler management. Exploit the **REST API/database**
for automation and telemetry rather than screen-scraping the CLI. Route at the aggregation
layer with OSPF/BGP as the design requires.

## Implementation and Automation

The labs configure VLANs/trunks, inter-VLAN routing, VSX, and the REST API.

## Validation and Troubleshooting

Confirm the switching model:

```text
AOS-CX: state database + built-in REST API (programmable). L2 (VLAN/trunk/STP), L3 (OSPF/BGP/VRF).
Redundancy: VSX (active-active aggregation, dual control plane) and VSF (access stacking).
Codes: ACA-S HPE6-A86 -> ACP-S HPE7-A08 -> ACX-S.
```

Common pitfalls: expecting **VSX** to share one control plane like a stack (each keeps its
own); and forgetting AOS-CX exposes everything via **REST**.

## Security and Best Practices

Separate management from data with **VRFs**, secure the **REST API** with tokens over HTTPS,
and use **VSX** for gateway redundancy so a switch failure is transparent. Keep configuration in
version control and push via the API/Ansible.

## Hands-On Lab

Switching walkthroughs. **Shared prerequisites** — an AOS-CX switch (physical or virtual). Labs
3.4 uses the REST API. **Cost:** none with virtual.

### Lab 3.1 — VLANs and a trunk

**Objective:** Create VLANs and a tagged uplink.

```text
switch(config)# vlan 10,20
switch(config)# interface 1/1/48
switch(config-if)# no shutdown
switch(config-if)# vlan trunk native 1
switch(config-if)# vlan trunk allowed 10,20
switch# show vlan
```

**Expected result:** VLANs 10 and 20 carried on a **trunk** uplink — Layer-2 segmentation.

**Negative test:** allow all VLANs on the trunk by default; restrict with **`vlan trunk
allowed`** to only the needed VLANs.

**Rollback:** `configure terminal; no vlan 10,20`.

### Lab 3.2 — Inter-VLAN routing (SVIs)

**Objective:** Route between VLANs with switch virtual interfaces.

```text
switch(config)# interface vlan 10
switch(config-if-vlan)# ip address 10.10.10.1/24
switch(config)# interface vlan 20
switch(config-if-vlan)# ip address 10.10.20.1/24
switch# show ip interface brief
```

**Expected result:** SVIs for VLANs 10 and 20 routing between subnets — Layer-3 on the switch.

**Negative test:** expect hosts in different VLANs to talk with no SVI/gateway; inter-VLAN
traffic needs **routing** — add the SVIs.

**Rollback:** `configure terminal; no interface vlan 10; no interface vlan 20`.

### Lab 3.3 — VSX redundancy

**Objective:** Describe active-active aggregation.

```text
switch(config)# vsx
switch(config-vsx)# inter-switch-link lag 256
switch(config-vsx)# role primary
switch(config-vsx)# keepalive peer 10.0.0.2 source 10.0.0.1
switch# show vsx status
```

**Expected result:** a **VSX** pair (ISL + keepalive + roles) presenting one logical
aggregation to downstream switches — active-active, dual control plane.

**Negative test:** assume VSX merges the control planes like a stack; **each switch keeps its
own** — VSX synchronizes state, it does not stack.

**Rollback:** `configure terminal; no vsx`.

### Lab 3.4 — Read state via the AOS-CX REST API

**Objective:** Query the switch database over HTTPS.

```bash
curl -sk -H "Cookie: $AOSCX_COOKIE" \
  "https://10.0.0.1/rest/v10.08/system/vlans" 2>/dev/null \
  | python3 -c "import sys,json;print('VLANs via REST:',list(json.load(sys.stdin).keys()))" 2>/dev/null \
  || echo "AOS-CX exposes config/state at /rest/v10.xx (login for a session cookie first)"
```

**Expected result:** the VLAN list from the **AOS-CX REST API** — the switch is programmable.

**Negative test:** parse `show vlan` text for automation; **AOS-CX REST** returns structured
JSON — use the API.

**Rollback:** none (read-only).

### Lab 3.5 — VSF stacking concept

**Objective:** Describe stacking access switches.

```text
# VSF: link multiple AOS-CX access switches into one virtual chassis, one management IP,
#   one config; a conductor manages members. Simplifies access-layer operations.
"vsf: N access switches -> 1 logical stack (single mgmt/config)"
```

**Expected result:** the **VSF** stacking model — simplified access management.

**Negative test:** manage ten access switches individually; **VSF** collapses them into one
logical unit — stack them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Switching track certifies AOS-CX — a database-driven, REST-programmable switch OS — across
Layer-2/Layer-3 and Aruba's VSX (active-active aggregation) and VSF (access stacking)
redundancy, from ACA-S (HPE6-A86) to ACP-S (HPE7-A08) to ACX-S. Use VSX/VSF for resilience and
the REST API for automation.

- [ ] I can configure VLANs, trunks, and SVIs on AOS-CX.
- [ ] I can build a VSX pair and explain its dual control plane.
- [ ] I can read switch state via the REST API.
- [ ] I can explain VSF stacking.
- [ ] I completed Labs 3.1–3.5 including each negative test.
