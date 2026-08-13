# Chapter 05: MTCWE — Wireless

## Learning Objectives

- Explain the MTCWE/MTCEWE scope and RouterOS wireless.
- Configure an access point and station.
- Secure wireless with encryption profiles.
- Centralize management with CAPsMAN.
- Complete a walkthrough for each wireless topic.

## Theory and Architecture

**MTCWE** (Wireless Engineer) — and the enterprise-focused **MTCEWE** — cover RouterOS wireless. A
RouterOS radio runs in a **mode**: **ap-bridge** (access point serving clients), **station**
(client), **bridge**, or a wireless-link mode for point-to-point backhaul. Wireless is configured
under `/interface wireless` with **bands/channels/frequencies** (2.4/5 GHz), an **SSID**, and a
**security profile** (`/interface wireless security-profiles`) for **WPA2/WPA3** encryption. At
scale, **CAPsMAN** (Controlled Access Point system Manager) centralizes configuration: APs (CAPs)
register to a manager that pushes SSIDs, security, channels, and datapath, so a fleet of APs is
managed from one place instead of device by device. MTCWE also covers RF concepts —
signal/noise/CCQ, registration tables, and troubleshooting wireless links.

## Design Considerations

Use **ap-bridge** for serving clients and dedicated modes for **PtP backhaul**. Always attach a
**WPA2/WPA3 security profile** — never run open corporate wireless. Plan **channels** to avoid
co-channel interference. At scale, manage with **CAPsMAN** so config is consistent across APs.

## Implementation and Automation

The labs configure an AP with security, a station, and describe CAPsMAN.

## Validation and Troubleshooting

Confirm the wireless model:

```text
Modes: ap-bridge (AP), station (client), PtP backhaul. /interface wireless: band/channel/SSID.
Security: /interface wireless security-profiles (WPA2/WPA3). RF: signal/noise/CCQ, registration table.
CAPsMAN: central config for a fleet of CAPs. MTCWE / MTCEWE (enterprise).
```

Common pitfalls: an **open** wireless network (no security profile); and managing many APs
**individually** instead of with CAPsMAN.

## Security and Best Practices

Encrypt with **WPA2/WPA3** security profiles, plan **channels** for capacity, and centralize with
**CAPsMAN**. Separate guest to a constrained VLAN/profile. Monitor the **registration table** and
signal quality. Authorized administration throughout.

## Hands-On Lab

Wireless walkthroughs. **Shared prerequisites** — RouterOS with a wireless interface (a wireless-
capable RouterBOARD, or CHR for the configuration patterns), in a lab. **Cost:** none with
hardware/patterns.

### Lab 5.1 — Configure an access point with security

**Objective:** Serve a secured SSID.

```text
/interface wireless security-profiles add name=corp mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key=StrongPass123
/interface wireless set wlan1 mode=ap-bridge ssid=CorpWiFi band=5ghz-a/n/ac frequency=5180 security-profile=corp disabled=no
/interface wireless print
```

**Expected result:** an **ap-bridge** serving `CorpWiFi` with a **WPA2** security profile — a
secured AP.

**Negative test:** bring up the SSID with the **default (open)** security profile; attach a
**WPA2/WPA3** profile — never open for corporate.

**Rollback:** `/interface wireless set wlan1 disabled=yes; /interface wireless security-profiles remove corp`.

### Lab 5.2 — Configure a station

**Objective:** Connect a RouterOS client to the AP.

```text
/interface wireless security-profiles add name=corp-cl mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key=StrongPass123
/interface wireless set wlan1 mode=station ssid=CorpWiFi security-profile=corp-cl disabled=no
/interface wireless registration-table print
```

**Expected result:** the station **associated** to the AP (shown in the registration table) —
client connectivity.

**Negative test:** mismatch the **SSID or key**; association fails — match them.

**Rollback:** reset the interface.

### Lab 5.3 — Verify RF quality

**Objective:** Read signal and link quality.

```text
/interface wireless registration-table print detail
# Check signal-strength, tx/rx-ccq, and rates.
/interface wireless monitor wlan1 once
```

**Expected result:** **signal strength and CCQ** for the link — RF health for troubleshooting.

**Negative test:** judge a link by "it associated" alone; check **signal/CCQ** for real quality.

**Rollback:** none (read-only).

### Lab 5.4 — CAPsMAN centralization

**Objective:** Describe managing APs centrally.

```text
# CAPsMAN: a manager pushes configuration (SSID, security, channel, datapath) to CAPs that register
#   to it -> one place manages the whole AP fleet; consistent config and roaming.
"CAPsMAN: manager -> provisions CAPs -> fleet-wide consistent wireless"
```

**Expected result:** the **CAPsMAN** model — centralized, consistent management of many APs.

**Negative test:** configure each AP by hand across a campus; **CAPsMAN** centralizes it — use it
at scale.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MTCWE/MTCEWE cover RouterOS wireless: interface modes (ap-bridge/station/PtP), SSIDs and channels,
WPA2/WPA3 security profiles, RF quality (signal/CCQ), and CAPsMAN for centralized fleet management.
Always secure the SSID, plan channels, and centralize with CAPsMAN at scale.

- [ ] I can configure a secured access point.
- [ ] I can connect a station.
- [ ] I can verify RF signal and CCQ.
- [ ] I can explain CAPsMAN centralization.
- [ ] I completed Labs 5.1–5.4 including each negative test.
