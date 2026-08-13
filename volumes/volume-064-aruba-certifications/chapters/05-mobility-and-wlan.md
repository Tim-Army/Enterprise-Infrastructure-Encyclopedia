# Chapter 05: Mobility and WLAN

## Learning Objectives

- Explain the Campus Access Mobility Expert exam (ACX-CAM, HPE7-A07) and the WLAN stack.
- Configure a WLAN SSID with WPA3 and role assignment.
- Reason about RF design (channels, power, coverage) for a campus.
- Relate gateways/AOS-10 and Central to wireless operation.
- Complete a walkthrough for each Mobility topic.

## Theory and Architecture

**Mobility** is Aruba's wireless heritage, certified at the Expert level as **Campus Access
Mobility (ACX-CAM, HPE7-A07)**. The WLAN stack is **access points (APs)** running **AOS-10**,
managed by **Aruba Central** (or on-prem controllers), often anchored to **gateways** that
terminate tunnels and enforce policy. Wireless design has two halves: the **service** — SSIDs,
**WPA3**/802.1X security, and **role assignment** so wireless users get the same dynamic
segmentation as wired — and the **RF** — channel plan, transmit power, and AP placement so
coverage and capacity meet demand without co-channel interference. Aruba's **ClientMatch/AirMatch**
optimize RF automatically. Wireless and wired converge on the same roles and policy.

## Design Considerations

Secure SSIDs with **WPA3** (or WPA2-Enterprise) and 802.1X to ClearPass, assigning the same
**roles** as wired. Plan **RF** for capacity (enough APs, right channels/power), not just
coverage. Let **AirMatch** tune channel/power centrally. Terminate policy at **gateways** where
the design calls for tunneling.

## Implementation and Automation

The labs define a secure SSID, assign a role, reason about an RF plan, and read WLAN health from
Central.

## Validation and Troubleshooting

Confirm the WLAN model:

```text
WLAN: APs (AOS-10) + Central/controllers + gateways (tunnel/policy).
Service: SSID + WPA3/802.1X + role assignment (same roles as wired).
RF: channel plan + power + placement; AirMatch optimizes centrally.
Code: ACX Campus Access Mobility HPE7-A07.
```

Common pitfalls: designing for **coverage** but not **capacity**; and giving wireless users
different policy than wired (use the **same roles**).

## Security and Best Practices

Use **WPA3**/802.1X and per-user roles; avoid open or PSK SSIDs for corporate access. Separate
guest to a constrained role. Let **AirMatch** manage RF and monitor for interference. Keep AP
firmware current via Central.

## Hands-On Lab

Mobility walkthroughs. **Shared prerequisites** — Aruba APs managed by Central (or the
configuration patterns) and, for RF, a floor plan. **Cost:** none with trial/patterns.

### Lab 5.1 — Define a secure SSID

**Objective:** Create a WPA3-Enterprise WLAN.

```text
# Aruba Central (or AOS) WLAN config (conceptual):
ssid "corp"
  opmode wpa3-aes
  auth-server clearpass-radius
  set-role from-radius        # role returned by ClearPass
"ssid corp: WPA3-Enterprise -> 802.1X to ClearPass -> role assigned"
```

**Expected result:** a **WPA3-Enterprise** SSID that authenticates to ClearPass and assigns a
role — secure wireless access.

**Negative test:** stand up an open or PSK SSID for staff; use **WPA3/802.1X** with roles for
corporate access.

**Rollback:** remove the test SSID.

### Lab 5.2 — Assign a wireless role

**Objective:** Give wireless users the same segmentation as wired.

```text
# Role 'employee' returned by ClearPass applies to wireless just like wired:
"wireless employee role == wired employee role -> unified dynamic segmentation"
```

**Expected result:** wireless and wired share the **same role/policy** — unified segmentation.

**Negative test:** write separate wireless-only policy; converge on the **same roles** as wired.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — RF plan reasoning

**Objective:** Size a coverage/capacity plan.

```python
python3 - <<'PY'
users=120; users_per_ap=25
aps_needed=-(-users//users_per_ap)  # ceil
print(f"users={users} at {users_per_ap}/AP -> APs needed: {aps_needed}")
print("channels: non-overlapping (5GHz preferred); power: tuned by AirMatch")
PY
```

**Expected result:** the AP count for capacity (**5 APs** for 120 users) plus channel/power
guidance — an RF plan sized for demand.

**Negative test:** place APs only for coverage; high-density areas need **capacity** — size by
users per AP.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Read WLAN health from Central

**Objective:** Pull wireless state via the API.

```bash
curl -sS -H "Authorization: Bearer $CENTRAL_TOKEN" \
  "https://apigw-uswest4.central.arubanetworks.com/monitoring/v2/aps" 2>/dev/null \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('APs reporting to Central:',len(d.get('aps',[])))" 2>/dev/null \
  || echo "query Central APs/RF health via the monitoring API"
```

**Expected result:** the count of **APs reporting to Central** — wireless health centrally.

**Negative test:** check each AP's LED to judge health; **Central's API** reports the WLAN
centrally — query it.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Mobility certifies Aruba WLAN — APs on AOS-10 managed by Central with gateways for
tunnel/policy — at the Expert level (ACX-CAM, HPE7-A07). Secure SSIDs with WPA3/802.1X, assign
the same roles as wired, and plan RF for capacity with AirMatch optimizing centrally.

- [ ] I can define a WPA3-Enterprise SSID with role assignment.
- [ ] I can unify wireless and wired segmentation via roles.
- [ ] I can size an RF plan for capacity.
- [ ] I can read WLAN health from Central's API.
- [ ] I completed Labs 5.1–5.4 including each negative test.
