# Chapter 05: Security Policies

## Learning Objectives

- Replace permit-any with least-privilege zone-to-zone policies.
- Permit only APP→DB:5432 and MGMT→OT:502; deny the MGMT→DB lateral flow.
- Rely on the SRX default inter-zone deny for everything else.
- Build the equivalent zone-pair ruleset in Track 2.

## Policy is ordered, and the default is deny

An SRX security policy is evaluated **top to bottom within a from-zone/to-zone context**; the first match wins, and if nothing matches, the **default policy denies**. Microsegmentation is therefore two moves: permit the exact flows you need, and make sure the permit-any from Chapter 04 is gone so the default deny governs the rest.

## Hands-On Lab

### Exercise 5.1 — Permit the two legitimate flows

**Objective.** Author narrow permits for APP→DB and MGMT→OT.

**Track 1 — Walkthrough.**

```text
[edit security policies]
# APP -> DB : only PostgreSQL
set from-zone APP to-zone DB policy web-to-db match source-address web destination-address db application junos-postgresql
set from-zone APP to-zone DB policy web-to-db then permit
# MGMT -> OT : only Modbus (define the app if needed)
set applications application modbus protocol tcp destination-port 502
set from-zone MGMT to-zone OT policy hmi-to-plc match source-address hmi destination-address plc application modbus
set from-zone MGMT to-zone OT policy hmi-to-plc then permit
commit
```

**Expected result.**

```text
srx> show security policies
From zone: APP, To zone: DB
  Policy: web-to-db  Source: web  Destination: db  Application: junos-postgresql  Action: permit
From zone: MGMT, To zone: OT
  Policy: hmi-to-plc Source: hmi  Destination: plc Application: modbus  Action: permit
```

**Negative test.** A policy that uses `application any` instead of `junos-postgresql` would permit every port between APP and DB — always scope the application, not just the zones and addresses. Zone plus address plus application is the granularity that makes this microsegmentation.

**Track 2 — Walkthrough.**

```bash
sudo nft flush chain inet jsec forward
# APP -> DB : only 5432
sudo nft add rule inet jsec forward ip saddr 10.20.1.10 ip daddr 10.20.2.10 tcp dport 5432 accept
# MGMT -> OT : only 502
sudo nft add rule inet jsec forward ip saddr 10.20.3.10 ip daddr 10.20.4.10 tcp dport 502 accept
```

**Expected result.** Two accept rules — the exact legitimate flows.

**Cleanup.** Keep the permits.

### Exercise 5.2 — Remove permit-any and confirm default deny

**Objective.** Delete the Chapter 04 permit-any so the default inter-zone deny governs everything else, including MGMT→DB.

**Track 1 — Walkthrough.**

```text
[edit security policies]
delete global policy allow-all
commit
```

Optionally make the deny explicit and logged for MGMT→DB:

```text
set from-zone MGMT to-zone DB policy deny-mgmt-db match source-address any destination-address any application any
set from-zone MGMT to-zone DB policy deny-mgmt-db then deny
set from-zone MGMT to-zone DB policy deny-mgmt-db then log session-init
commit
```

**Expected result.**

```text
srx> show security policies from-zone MGMT to-zone DB
  Policy: deny-mgmt-db  Action: deny (log)
  Default policy: deny-all
```

The lateral zone pair now denies, explicitly and by default.

**Negative test.** Leaving the `global allow-all` policy in place would keep permitting MGMT→DB regardless of the specific permits — a global permit above the zone contexts defeats least privilege. The permit-any must go.

**Track 2 — Walkthrough.**

```bash
# explicit logged deny for the lateral pair, then default drop for inter-zone
sudo nft add rule inet jsec forward ip saddr 10.20.3.10 ip daddr 10.20.2.10 log prefix '"JSEC-DENY " ' drop
sudo nft add rule inet jsec forward ip saddr 10.20.0.0/16 ip daddr 10.20.0.0/16 drop
sudo nft chain inet jsec forward '{ policy accept ; }'
sudo nft list chain inet jsec forward
```

**Expected result.** The forward chain permits the two flows, logs-and-drops MGMT→DB, and drops all other inter-zone traffic.

**Cleanup.** Keep the ruleset; Chapter 07 verifies enforcement.

## Summary and Completion Checklist

- [ ] APP→DB:5432 and MGMT→OT:502 permitted with scoped applications.
- [ ] Permit-any removed; default inter-zone deny in force.
- [ ] MGMT→DB explicitly denied and logged.
- [ ] Track 2 zone-pair ruleset matches the SRX policy.
