# Chapter 02: Campus Access Track

## Learning Objectives

- Explain the Campus Access track (ACA-CA → ACP-CA → ACX Campus Access).
- Configure AOS-CX access-layer switching for a campus.
- Onboard a switch to Aruba Central and read its state.
- Apply dynamic segmentation with roles and downloadable policy.
- Complete a walkthrough for each Campus Access topic.

## Theory and Architecture

The **Campus Access** track certifies the design and operation of a modern Aruba campus:
wired and wireless access unified under **AOS-CX** switches and **Aruba Central** cloud
management, with **dynamic segmentation** enforcing user/device **roles** end to end. The track
climbs from **Associate (ACA-CA, HPE6-A85)** — access-layer fundamentals — through
**Professional (ACP-CA, HPE7-A01)** — campus design, Central, and troubleshooting — to the
**Expert** Campus Access exams (Switching **HPE7-A06** and Mobility **HPE7-A07**). The campus is
built on AOS-CX access switches, aggregation with **VSX** redundancy, **Aruba Central** for
zero-touch provisioning and monitoring, and **dynamic segmentation** where a user's **role**
(from ClearPass or Central) follows them and is enforced by downloadable policy or by
redirecting traffic to a gateway.

## Design Considerations

Design the campus around **roles**, not ports — a role travels with the user and enforces the
same policy wherever they connect. Use **Aruba Central** as the single management plane and
**VSX** for loop-free active-active aggregation. Provision with **zero-touch** where possible.

## Implementation and Automation

The labs configure an AOS-CX access port, verify Central onboarding, apply a role, and read
campus state via the API.

## Validation and Troubleshooting

Confirm the campus model:

```text
Campus Access: AOS-CX access + VSX aggregation + Aruba Central (cloud mgmt/ZTP) +
dynamic segmentation (role follows user; enforced by policy/gateway).
Codes: ACA-CA HPE6-A85 -> ACP-CA HPE7-A01 -> ACX HPE7-A06 (Switching) / HPE7-A07 (Mobility).
```

Common pitfalls: port-based instead of **role-based** policy; and managing switches device by
device instead of through **Central**.

## Security and Best Practices

Enforce **dynamic segmentation** so unauthorized devices are contained by role, not trusted by
location. Keep switches in **Central** for consistent config and visibility. Authenticate access
with **802.1X**/ClearPass before assigning a role.

## Hands-On Lab

Campus Access walkthroughs. **Shared prerequisites** — an AOS-CX switch (physical, or virtual
via GNS3/containerlab) and, for Central labs, an Aruba Central account/trial. **Cost:** none
with virtual/trial.

### Lab 2.1 — Configure an AOS-CX access port

**Objective:** Set an access VLAN on an edge port.

```text
switch# configure terminal
switch(config)# vlan 100
switch(config-vlan-100)# name users
switch(config)# interface 1/1/1
switch(config-if)# no shutdown
switch(config-if)# vlan access 100
switch(config)# end
switch# show vlan 100
```

**Expected result:** interface 1/1/1 as an **access port** in VLAN 100 — campus edge
connectivity.

**Negative test:** put multiple VLANs on an access port; use `vlan trunk` for an uplink — an
access port carries **one** untagged VLAN.

**Rollback:** `configure terminal; no vlan 100`.

### Lab 2.2 — Verify Aruba Central onboarding

**Objective:** Confirm a switch is managed by Central.

```bash
curl -sS -H "Authorization: Bearer $CENTRAL_TOKEN" \
  "https://apigw-uswest4.central.arubanetworks.com/monitoring/v1/switches" 2>/dev/null \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('switches in Central:',len(d.get('switches',[])))" 2>/dev/null \
  || echo "query Aruba Central inventory via the monitoring REST API"
```

**Expected result:** the count of switches **managed by Central** — cloud visibility of the
campus.

**Negative test:** SSH into each switch to check status; **Central** shows the whole fleet from
one API — use it.

**Rollback:** none (read-only).

### Lab 2.3 — Apply a user role (dynamic segmentation)

**Objective:** Define a role that follows the user.

```text
switch(config)# port-access role employee
switch(config-pa-role)# vlan access 100
switch(config-pa-role)# exit
# ClearPass/Central assigns 'employee' on 802.1X auth; policy follows the user, not the port.
switch# show port-access role
```

**Expected result:** an **employee** role with its VLAN/policy — enforced wherever the user
connects.

**Negative test:** hard-code the VLAN per port; **roles** move with the user — assign by role,
not port.

**Rollback:** `configure terminal; no port-access role employee`.

### Lab 2.4 — Read campus health from the API

**Objective:** Pull access-layer state programmatically.

```bash
curl -sS -H "Authorization: Bearer $CENTRAL_TOKEN" \
  "https://apigw-uswest4.central.arubanetworks.com/monitoring/v1/clients" 2>/dev/null \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('connected clients:',len(d.get('clients',[])))" 2>/dev/null \
  || echo "query Central clients/health via the monitoring API for campus visibility"
```

**Expected result:** the connected-client count — campus health from Central's API.

**Negative test:** gauge campus health by walking the wiring closet; **Central's API** answers
it centrally — query it.

**Rollback:** none (read-only).

### Lab 2.5 — Zero-touch provisioning concept

**Objective:** Describe onboarding a new switch without touching it.

```text
# ZTP: new AOS-CX switch boots -> reaches Central -> pulls its config/group -> joins managed.
"ztp: unbox -> connect -> Central assigns group + config -> production"
```

**Expected result:** the **zero-touch** flow — a switch provisioned by Central on first boot.

**Negative test:** stage every switch by hand at a bench; **ZTP via Central** scales campus
rollout — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Campus Access track builds the Aruba campus on AOS-CX access, VSX aggregation, Aruba
Central management, and dynamic segmentation where roles follow users. It climbs ACA-CA
(HPE6-A85) → ACP-CA (HPE7-A01) → the Expert Campus Access exams. Design around roles, manage
through Central, and provision with zero-touch.

- [ ] I can configure an AOS-CX access port.
- [ ] I can verify Central onboarding via the API.
- [ ] I can apply a user role for dynamic segmentation.
- [ ] I can read campus health from Central's API.
- [ ] I completed Labs 2.1–2.5 including each negative test.
