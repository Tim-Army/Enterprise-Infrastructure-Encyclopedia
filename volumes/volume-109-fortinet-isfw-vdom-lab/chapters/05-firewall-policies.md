# Chapter 05: Firewall Policies

## Learning Objectives

- Replace permit-all with least-privilege zone-to-zone firewall policies.
- Permit only APP→DB (PGSQL) and MGMT→OT (MODBUS); deny the MGMT→DB lateral flow.
- Rely on the FortiGate implicit deny for everything else.
- Build the equivalent zone-pair ruleset in Track 2.

## Ordered policies and the implicit deny

FortiOS evaluates firewall policies **top to bottom**; the first match wins, and after the last policy an **implicit deny** drops anything unmatched. Microsegmentation is therefore: author the exact permits, place any explicit denies above broad permits, and remove the permit-all so the implicit deny governs the rest.

**Two FortiOS requirements before you start.** First, because Chapter 03 put the interfaces into zones, a policy references the **zone** (`APP`/`DB`/`MGMT`/`OT`), not the member interface — `set srcintf port2` (or `set srcintf v2001` on the evaluation build) is rejected once that interface belongs to a zone (`node_check_object fail`). Second, **every policy must carry a schedule**: omit `set schedule always` and FortiOS refuses to save the rule at `next`/`end` with `Attribute 'schedule' MUST be set` (return code -56), silently leaving the rule uncommitted. Both are easy to trip over — the walkthroughs below use zones and set a schedule on every rule, including the deny.

## Hands-On Lab

### Exercise 5.1 — Permit the two legitimate flows

**Objective.** Author narrow permits for APP→DB and MGMT→OT.

**Track 1 — Walkthrough.**

```text
FGT # config firewall policy
FGT (policy) # edit 1
FGT (1) # set name web-to-db
FGT (1) # set srcintf APP
FGT (1) # set dstintf DB
FGT (1) # set srcaddr web
FGT (1) # set dstaddr db
FGT (1) # set service PGSQL
FGT (1) # set action accept
FGT (1) # set schedule always
FGT (1) # set logtraffic all
FGT (1) # next
FGT (policy) # edit 2
FGT (2) # set name hmi-to-plc
FGT (2) # set srcintf MGMT
FGT (2) # set dstintf OT
FGT (2) # set srcaddr hmi
FGT (2) # set dstaddr plc
FGT (2) # set service MODBUS
FGT (2) # set action accept
FGT (2) # set schedule always
FGT (2) # set logtraffic all
FGT (2) # end
```

**Expected result.**

```text
FGT # show firewall policy | grep name
    set name "web-to-db"
    set name "hmi-to-plc"
FGT # show firewall policy | grep service
    set service "PGSQL"
    set service "MODBUS"
```

*FortiOS's built-in `grep` accepts only a single pattern — no `-E`, no `|` alternation — so filter one field at a time. (`grep -f <term>` is the variant that keeps a match's surrounding config block and flags it with `<---`.)*

**Negative test.** Using `set service ALL` instead of `PGSQL` would permit every port between APP and DB — scope the service, not just the zones and addresses. Zone + address + service is what makes this microsegmentation.

**Track 2 — Walkthrough.**

```bash
sudo nft flush chain inet fgt forward
sudo nft add rule inet fgt forward ip saddr 10.30.1.10 ip daddr 10.30.2.10 tcp dport 5432 accept
sudo nft add rule inet fgt forward ip saddr 10.30.3.10 ip daddr 10.30.4.10 tcp dport 502 accept
```

**Expected result.** Two accept rules — the exact legitimate flows.

**Cleanup.** Keep the permits.

### Exercise 5.2 — Remove permit-all and confirm implicit deny

**Objective.** Delete the Chapter 04 permit-all so the implicit deny governs everything else, including MGMT→DB.

**Track 1 — Walkthrough.**

```text
FGT # config firewall policy
FGT (policy) # delete 100
FGT (policy) # end
```

Optionally add an explicit logged deny for MGMT→DB above the implicit deny:

```text
FGT # config firewall policy
FGT (policy) # edit 3
FGT (3) # set name deny-mgmt-db
FGT (3) # set srcintf MGMT
FGT (3) # set dstintf DB
FGT (3) # set srcaddr hmi
FGT (3) # set dstaddr db
FGT (3) # set service ALL
FGT (3) # set action deny
FGT (3) # set schedule always
FGT (3) # set logtraffic all
FGT (3) # end
```

**Expected result.**

```text
FGT # show firewall policy | grep name
    set name "web-to-db"
    set name "hmi-to-plc"
    set name "deny-mgmt-db"
FGT # show firewall policy | grep action
    set action accept
    set action accept
# only two 'set action' lines — deny-mgmt-db has none, because deny is the FortiOS default
```

**Negative test.** Leaving policy 100 (allow-all) in place keeps permitting MGMT→DB regardless of the specific permits — a broad accept above the specifics defeats least privilege. The permit-all must go.

**Track 2 — Walkthrough.**

```bash
sudo nft add rule inet fgt forward ip saddr 10.30.3.10 ip daddr 10.30.2.10 log prefix '"FGT-DENY " ' drop
sudo nft add rule inet fgt forward ip saddr 10.30.0.0/16 ip daddr 10.30.0.0/16 drop
sudo nft chain inet fgt forward '{ policy accept ; }'
sudo nft list chain inet fgt forward
```

**Expected result.** The forward chain permits the two flows, logs-and-drops MGMT→DB, and drops all other east-west traffic.

**Cleanup.** Keep the ruleset; Chapter 06 verifies enforcement.

## Summary and Completion Checklist

- [ ] APP→DB (PGSQL) and MGMT→OT (MODBUS) permitted with scoped services.
- [ ] Permit-all removed; implicit deny in force.
- [ ] MGMT→DB explicitly denied and logged.
- [ ] Track 2 zone-pair ruleset matches the FortiOS policy.
