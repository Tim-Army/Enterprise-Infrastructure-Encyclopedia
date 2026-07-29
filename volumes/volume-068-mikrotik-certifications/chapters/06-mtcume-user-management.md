# Chapter 06: MTCUME — User Management

## Learning Objectives

- Explain the MTCUME scope: PPP, hotspot, and RADIUS.
- Configure a PPPoE server for subscriber access.
- Configure a hotspot with a login portal.
- Centralize authentication with RADIUS (User Manager).
- Complete a walkthrough for each user-management topic.

## Theory and Architecture

**MTCUME** (User Management Engineer) covers authenticating and managing **users/subscribers** — the
ISP and guest-access side of RouterOS. **PPP** underpins it: **PPPoE** (PPP over Ethernet) is the
classic subscriber-access method, where each user authenticates and gets an IP from a **profile**;
**PPP secrets** (or RADIUS) store credentials, and **profiles** define address pools, rate limits,
and settings. The **hotspot** provides captive-portal access (walled garden, login page,
usage/time limits) for guest Wi-Fi and public access. **RADIUS** centralizes AAA — RouterOS can be
a RADIUS **client**, and MikroTik's **User Manager** is a RADIUS **server** for managing users,
profiles, and accounting across many routers. MTCUME ties access methods to centralized user
control.

## Design Considerations

Use **PPPoE** for subscriber access with **profiles** for rate/address policy, and **hotspot** for
guest/public captive-portal access. Centralize credentials with **RADIUS/User Manager** rather than
local secrets per router. Apply **rate limits** via profiles. Keep accounting for usage.

## Implementation and Automation

The labs configure a PPPoE server, a hotspot, and RADIUS client settings.

## Validation and Troubleshooting

Confirm the user-management model:

```text
PPP: PPPoE server + profiles (address pool, rate-limit) + secrets (or RADIUS). Hotspot: captive portal.
RADIUS: RouterOS as client; User Manager as RADIUS server (AAA + accounting). MTCUME.
```

Common pitfalls: a PPPoE server with **no profile/pool** (users get no address/policy); and local
secrets **per router** where RADIUS should centralize.

## Security and Best Practices

Centralize with **RADIUS/User Manager**, enforce **rate limits** via profiles, and secure the
**hotspot** login (HTTPS portal). Keep **accounting** for audit. Use strong credentials and
per-user policy. Authorized administration throughout.

## Hands-On Lab

MTCUME walkthroughs. **Shared prerequisites** — a RouterOS node (CHR), in a lab. **Cost:** none.

### Lab 6.1 — PPPoE server with a profile

**Objective:** Offer subscriber access with policy.

```text
/ip pool add name=pppoe-pool ranges=10.10.10.2-10.10.10.254
/ppp profile add name=basic local-address=10.10.10.1 remote-address=pppoe-pool rate-limit=10M/10M
/interface pppoe-server server add service-name=isp interface=ether2 default-profile=basic disabled=no
/ppp secret add name=user1 password=pass1 profile=basic service=pppoe
/interface pppoe-server server print
```

**Expected result:** a **PPPoE server** with a rate-limited profile and a subscriber secret —
authenticated subscriber access.

**Negative test:** enable PPPoE with **no profile/pool**; users can't get an address/policy —
define them.

**Cleanup:** remove the server, profile, pool, and secret.

### Lab 6.2 — Hotspot captive portal

**Objective:** Provide guest login access.

```text
/ip hotspot setup
# Walks through: hotspot interface, address pool, certificate, DNS, and a local login user.
/ip hotspot user add name=guest password=guest limit-uptime=1h
/ip hotspot print
```

**Expected result:** a **hotspot** with a captive-portal login and a time-limited guest — controlled
public access.

**Negative test:** put guests straight on the LAN with no portal/limits; use a **hotspot** for
controlled access.

**Cleanup:** remove the hotspot and user.

### Lab 6.3 — RADIUS client

**Objective:** Centralize authentication.

```text
/radius add service=ppp,hotspot address=10.0.0.50 secret=RadiusSecret
/ppp aaa set use-radius=yes
/radius print
```

**Expected result:** RouterOS using **RADIUS** for PPP/hotspot AAA — centralized authentication.

**Negative test:** manage credentials as **local secrets** on every router; **RADIUS** centralizes
them — point AAA at it.

**Cleanup:** `/ppp aaa set use-radius=no; /radius remove [find address=10.0.0.50]`.

### Lab 6.4 — User Manager concept

**Objective:** Describe RADIUS-server-side management.

```text
# User Manager (MikroTik) is a RADIUS SERVER: manage users, profiles, limits, and accounting
#   centrally, serving many RouterOS RADIUS clients (PPPoE/hotspot).
"User Manager = RADIUS server -> central users/profiles/accounting for many routers"
```

**Expected result:** the **User Manager** model — central RADIUS-server-side user management.

**Negative test:** scale subscriber management with per-router secrets; **User Manager** centralizes
it — use it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MTCUME covers user/subscriber management: PPPoE with profiles, the hotspot captive portal, and
RADIUS (RouterOS as client, User Manager as server) for centralized AAA and accounting. Use
profiles for policy, hotspots for guests, and RADIUS/User Manager to centralize.

- [ ] I can configure a PPPoE server with a profile.
- [ ] I can set up a hotspot captive portal.
- [ ] I can point AAA at RADIUS.
- [ ] I can explain User Manager as a RADIUS server.
- [ ] I completed Labs 6.1–6.4 including each negative test.
