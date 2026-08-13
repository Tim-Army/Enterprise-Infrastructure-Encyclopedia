# Chapter 04: The Flat Policy and Lateral Movement

## Learning Objectives

- Add a temporary permit-all policy to reproduce a flat network.
- Demonstrate the operator-to-database lateral movement.
- Name the legitimate flows the policy must preserve.

## Starting open to see the control work

A FortiGate with zones but no policies denies all transit (the implicit deny) — the *end* state. To reproduce the flat network the series begins from, add a temporary broad **permit** policy, prove the lateral movement, then replace it in Chapter 05 with least privilege.

## Hands-On Lab

### Exercise 4.1 — Add a temporary permit-all and confirm flatness

**Objective.** Make every zone reach every zone, then show the lateral flow.

**Track 1 — Walkthrough.**

```text
FGT # config firewall policy
FGT (policy) # edit 100
FGT (100) # set name allow-all
FGT (100) # set srcintf any
FGT (100) # set dstintf any
FGT (100) # set srcaddr all
FGT (100) # set dstaddr all
FGT (100) # set service ALL
FGT (100) # set action accept
FGT (100) # set schedule always
FGT (100) # set logtraffic all
FGT (100) # end
```

Test the flows:

```text
FGT # diagnose sniffer packet any 'host 10.30.2.10 and port 5432' 4
# (from hmi) nc db 5432  -> session builds  (lateral!)
# (from web) nc db 5432  -> session builds  (legitimate)
# (from hmi) nc plc 502  -> session builds  (legitimate)
```

**Track 2 — Walkthrough.**

```bash
sudo nft add chain inet fgt forward '{ type filter hook forward priority 0 ; policy accept ; }'
sudo ip netns exec web bash -c 'nc -z -w2 10.30.2.10 5432 && echo "web->db REACH"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432 && echo "hmi->db REACH (lateral!)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.4.10 502  && echo "hmi->plc REACH"'
```

**Expected result.** All three flows REACH — the ISFW is in the path but wide open. The `hmi->db` connection is the lateral movement.

**Negative test.** A flow to a closed port (`hmi->db:502`) fails because nothing listens, not because of policy. Distinguish "no service" from "denied."

**Rollback.** Leave the permit-all until Chapter 05 replaces it.

### Exercise 4.2 — Name the legitimate flows

**Objective.** Record the permit list so tightening does not cause an outage.

**Track 1 & 2 — Walkthrough.**

```text
APP  -> DB  : PGSQL (tcp 5432)    web -> db
MGMT -> OT  : MODBUS (tcp 502)    hmi -> plc
```

Everything else east-west — most importantly `MGMT -> DB` (hmi -> db) — is illegitimate.

**Expected result.** A two-line permit list; the whole segmentation is those two flows.

**Negative test.** Write the APP→DB rule against the db IP rather than the `db` address object and note it breaks if db re-addresses; the named object survives change.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 4.3 — Reproduce the lateral movement

**Objective.** Show the compromised operator pivoting to the database.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with permit-all, the operator reaches the database. Chapter 05 denies exactly this while preserving the app path.

**Negative test.** Re-run `web->db`; it also succeeds. Until policy distinguishes the sources, the firewall treats app and operator identically.

**Rollback.** None — Chapter 05 authors least-privilege policy.

## Summary and Completion Checklist

- [ ] Temporary permit-all makes the network flat.
- [ ] The two legitimate flows named (APP→DB PGSQL, MGMT→OT MODBUS).
- [ ] The MGMT→DB lateral movement reproduced.
- [ ] Ready to replace permit-all with least-privilege policy.
