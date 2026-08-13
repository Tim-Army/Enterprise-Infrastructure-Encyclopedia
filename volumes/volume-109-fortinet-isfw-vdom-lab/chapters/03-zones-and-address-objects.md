# Chapter 03: Zones and Address Objects

## Learning Objectives

- Group interfaces into zones so policy reads by role, not by port.
- Create named address objects and a custom service for the database.
- Confirm the zones and objects exist.
- Model the same zones and objects in Track 2.

## Hands-On Lab

### Exercise 3.1 — Create zones over the interfaces

**Objective.** Name each segment with a zone so policies reference `APP`, `DB`, `MGMT`, `OT`.

**Track 1 — Walkthrough.**

```text
FGT # config system zone
FGT (zone) # edit APP
FGT (APP) # set interface port2
FGT (APP) # next
FGT (zone) # edit DB
FGT (DB) # set interface port3
FGT (DB) # next
FGT (zone) # edit MGMT
FGT (MGMT) # set interface port4
FGT (MGMT) # next
FGT (zone) # edit OT
FGT (OT) # set interface port5
FGT (OT) # end
```

**Expected result.**

```text
FGT # show system zone
    edit "APP"  set interface "port2"
    edit "DB"   set interface "port3"
    edit "MGMT" set interface "port4"
    edit "OT"   set interface "port5"
```

*(On the evaluation build the members read `v2001`–`v2004` instead of `port2`–`port5`.)*

**Negative test.** Adding an interface that already belongs to another zone is rejected — an interface lives in exactly one zone, so zone membership is unambiguous, just like an endpoint's group.

**Evaluation FortiGate.** On the eval build the zone members are the VLAN subinterfaces created in Chapter 02, not physical ports: `set interface v2001` for `APP`, `v2002` for `DB`, `v2003` for `MGMT`, `v2004` for `OT`. The zone names — and everything downstream in this chapter (the `web`/`db`/`hmi`/`plc` address objects and the `PGSQL`/`MODBUS` services, which reference IP addresses, not interfaces) — are identical.

**Track 2 — Walkthrough.** Record the zone table the policy chain will consult:

```bash
sudo mkdir -p /etc/fgt
sudo tee /etc/fgt/zones > /dev/null <<'EOF'
10.30.1.0/24 APP
10.30.2.0/24 DB
10.30.3.0/24 MGMT
10.30.4.0/24 OT
EOF
cat /etc/fgt/zones
```

**Expected result.** Four subnet→zone rows.

**Rollback.** Keep the zones.

### Exercise 3.2 — Address objects and a custom service

**Objective.** Name the endpoints and define the PostgreSQL service.

**Track 1 — Walkthrough.**

```text
FGT # config firewall address
FGT (address) # edit web
FGT (web) # set subnet 10.30.1.10/32
FGT (web) # next
FGT (address) # edit db
FGT (db) # set subnet 10.30.2.10/32
FGT (db) # next
FGT (address) # edit hmi
FGT (hmi) # set subnet 10.30.3.10/32
FGT (hmi) # next
FGT (address) # edit plc
FGT (plc) # set subnet 10.30.4.10/32
FGT (plc) # end
FGT # config firewall service custom
FGT (custom) # edit PGSQL
FGT (PGSQL) # set tcp-portrange 5432
FGT (PGSQL) # next
FGT (custom) # edit MODBUS
FGT (MODBUS) # set tcp-portrange 502
FGT (MODBUS) # end
```

**Expected result.**

```text
FGT # show firewall address | grep edit
    edit "web"
    edit "db"
    edit "hmi"
    edit "plc"
FGT # show firewall service custom | grep PGSQL
    edit "PGSQL"
FGT # show firewall service custom | grep MODBUS
    edit "MODBUS"
```

**Negative test.** A policy that references an address name not defined here fails — objects must exist before a policy can name them, so typos surface at configuration time.

**Track 2 — Walkthrough.**

```bash
sudo tee /etc/fgt/addresses > /dev/null <<'EOF'
web 10.30.1.10
db  10.30.2.10
hmi 10.30.3.10
plc 10.30.4.10
EOF
sudo nft add table inet fgt
cat /etc/fgt/addresses
```

**Expected result.** Four named addresses; the `fgt` table exists for the policy chain.

**Rollback.** Keep the objects.

## Summary and Completion Checklist

- [ ] Four zones created over the data interfaces.
- [ ] Address objects web/db/hmi/plc and services PGSQL/MODBUS defined.
- [ ] One-interface-per-zone confirmed.
- [ ] Track 2 zone table and addresses mirror the FortiOS config.
