# Chapter 04: Network Security Track

## Learning Objectives

- Explain the Network Security track (ACA-NS → ACP-NS → ACX-NS).
- Authenticate access with 802.1X and ClearPass (RADIUS).
- Enforce role-based dynamic segmentation with the Policy Enforcement Firewall.
- Profile and posture devices for network access control.
- Complete a walkthrough for each Network Security topic.

## Theory and Architecture

The **Network Security** track certifies Aruba's access-security stack from **Associate (ACA-NS,
HPE6-A78)** through **Professional (ACP-NS)** to **Expert (ACX-NS, HPE7-A10)**. Its center is
**ClearPass** — Aruba's network access control (NAC) and policy platform — which authenticates
users and devices (**802.1X**, MAC auth, captive portal) over **RADIUS**, **profiles** devices
to identify what they are, checks **posture**, and returns a **role** and enforcement policy.
That role drives **dynamic segmentation**: the **Policy Enforcement Firewall (PEF)** on Aruba
gateways and AOS-CX applies per-role access so a device only reaches what its role permits,
regardless of where it connects. The result is identity-based, Zero-Trust-aligned access —
authenticate, authorize to a role, and enforce that role everywhere.

## Design Considerations

Authenticate **before** access with 802.1X where possible, MAC auth or captive portal
otherwise. Author policy on **roles**, not IPs. Use **profiling** to catch unmanaged/IoT
devices and assign constrained roles. Enforce with **PEF** at the gateway/switch so segmentation
follows the user.

## Implementation and Automation

The labs configure 802.1X to ClearPass, define a role/enforcement, profile a device, and query
ClearPass via its API.

## Validation and Troubleshooting

Confirm the security model:

```text
ClearPass: 802.1X/MAC/portal auth over RADIUS -> profile + posture -> return role + policy.
Enforcement: PEF (gateway/AOS-CX) applies per-role access = dynamic segmentation.
Codes: ACA-NS HPE6-A78 -> ACP-NS -> ACX-NS HPE7-A10.
```

Common pitfalls: allowing access **before** authentication; and writing firewall rules by **IP**
instead of by **role**.

## Security and Best Practices

Default to **deny** and grant by role. Profile every device (especially IoT) and give it the
**least** access its role needs. Log auth and enforcement for audit. Keep RADIUS shared secrets
and ClearPass admin access tightly controlled.

## Hands-On Lab

Network Security walkthroughs. **Shared prerequisites** — an AOS-CX switch or Aruba gateway, and
a ClearPass instance (or the eval VM/patterns). **Cost:** none with eval.

### Lab 4.1 — 802.1X to ClearPass (RADIUS)

**Objective:** Point switch authentication at ClearPass.

```text
switch(config)# radius-server host 10.1.1.10 key plaintext SECRET
switch(config)# aaa authentication port-access dot1x authenticator
switch(config)# interface 1/1/1
switch(config-if)# aaa authentication port-access dot1x authenticator enable
switch# show port-access clients
```

**Expected result:** the port authenticates users via **802.1X to ClearPass** — identity before
access.

**Negative test:** leave the port open with no 802.1X; unauthenticated devices get on the
network — **enable authentication**.

**Rollback:** `configure terminal; no radius-server host 10.1.1.10`.

### Lab 4.2 — Role and enforcement (dynamic segmentation)

**Objective:** Bind an authenticated role to access policy.

```text
# ClearPass enforcement profile returns role 'iot-camera' -> switch/gateway applies its policy:
switch(config)# port-access role iot-camera
switch(config-pa-role)# vlan access 900
switch(config-pa-role)# # PEF: permit to NVR only; deny lateral
switch# show port-access role iot-camera
```

**Expected result:** the **iot-camera** role constrains the device to its NVR — dynamic
segmentation by role.

**Negative test:** give the camera full VLAN access; enforce **least privilege** by role via
PEF.

**Rollback:** `configure terminal; no port-access role iot-camera`.

### Lab 4.3 — Device profiling

**Objective:** Identify an unmanaged device.

```text
# ClearPass profiles endpoints (DHCP fingerprint, MAC OUI, active scans) to classify them:
"profile: fingerprint -> category=IP-Camera -> assign constrained role automatically"
```

**Expected result:** the device is **profiled** and auto-assigned a constrained role — visibility
and control over unmanaged/IoT gear.

**Negative test:** treat every unknown MAC as trusted; **profile** it and constrain by role.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Query ClearPass via the API

**Objective:** Read access sessions programmatically.

```bash
curl -sk -H "Authorization: Bearer $CPPM_TOKEN" \
  "https://clearpass.example.com/api/session?filter=%7B%22acctstoptime%22%3Anull%7D" 2>/dev/null \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('active sessions:',d.get('count','see items'))" 2>/dev/null \
  || echo "ClearPass exposes sessions/endpoints via its REST API (OAuth2 token)"
```

**Expected result:** the active access sessions from **ClearPass's REST API** — programmatic
visibility.

**Negative test:** read the ClearPass GUI to audit sessions at scale; the **API** answers it
programmatically — use it.

**Rollback:** none (read-only).

### Lab 4.5 — Posture check concept

**Objective:** Gate access on device health.

```text
# Posture: ClearPass checks endpoint health (patch, AV, disk encryption) before full access;
#   noncompliant -> quarantine role with remediation only.
"posture: healthy -> full role; unhealthy -> quarantine + remediate"
```

**Expected result:** compliant devices get their role; noncompliant devices are **quarantined**
— health-based access.

**Negative test:** grant full access without a posture check; gate on **health** for
Zero-Trust access.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Network Security track certifies Aruba's identity-based access: ClearPass authenticates
(802.1X/MAC/portal over RADIUS), profiles, and postures devices, returns a role, and the Policy
Enforcement Firewall enforces that role as dynamic segmentation — from ACA-NS (HPE6-A78) to
ACP-NS to ACX-NS (HPE7-A10). Authenticate first, author by role, enforce least privilege.

- [ ] I can point switch 802.1X at ClearPass.
- [ ] I can bind a role to enforcement (dynamic segmentation).
- [ ] I can explain profiling and posture.
- [ ] I can query ClearPass via its API.
- [ ] I completed Labs 4.1–4.5 including each negative test.
