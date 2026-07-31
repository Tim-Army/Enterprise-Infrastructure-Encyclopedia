# Chapter 04: The Flat Network and Lateral Movement

## Learning Objectives

- Add a temporary any-any accept rule to reproduce a flat network.
- Demonstrate the operator-to-database lateral movement.
- Name the legitimate flows the rulebase must preserve.

## Starting open to see the control work

Chapter 03 left the estate default-deny. To reproduce the flat network the series begins from, add a temporary **any-any accept** rule above the Cleanup rule, install, prove the lateral movement, then replace it in Chapter 05 with least privilege.

## Hands-On Lab

### Exercise 4.1 — Add a temporary any-any accept and confirm flatness

**Objective.** Make every segment reach every segment, then show the lateral flow.

**Track 1 — Walkthrough.**

```text
mgmt> mgmt_cli add access-rule layer "Network" position top name "allow-all" \
        source Any destination Any service Any action Accept track Log --session-id "$SID"
mgmt> mgmt_cli publish --session-id "$SID"
mgmt> mgmt_cli install-policy policy-package "Standard" access true targets gw --session-id "$SID"
```

Test the flows (from the endpoints):

```text
# from hmi: nc db 5432  -> connects  (lateral!)
# from web: nc db 5432  -> connects  (legitimate)
# from hmi: nc plc 502  -> connects  (legitimate)
```

**Track 2 — Walkthrough.**

```bash
sudo nft flush chain inet cpg forward
sudo nft add rule inet cpg forward ip saddr 10.40.0.0/16 ip daddr 10.40.0.0/16 accept
sudo ip netns exec web bash -c 'nc -z -w2 10.40.2.10 5432 && echo web->db REACH'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.2.10 5432 && echo hmi->db REACH (lateral!)'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.4.10 502  && echo hmi->plc REACH'
```

**Expected result.** All three flows REACH — the gateway is in the path but the top rule accepts everything. The `hmi->db` connection is the lateral movement.

**Negative test.** A flow to a closed port (`hmi->db:502`) fails because nothing listens, not because of policy. Distinguish "no service" from "denied."

**Cleanup.** Leave the any-any accept until Chapter 05 replaces it.

### Exercise 4.2 — Name the legitimate flows

**Objective.** Record the permit list so tightening does not cause an outage.

**Track 1 & 2 — Walkthrough.**

```text
web -> db  : PGSQL (tcp 5432)
hmi -> plc : MODBUS (tcp 502)
```

Everything else east-west — most importantly `hmi -> db` — is illegitimate.

**Expected result.** A two-line permit list; the whole segmentation is those two flows plus the Cleanup drop.

**Negative test.** Write the web→db rule against the db IP rather than the `db` object and note it breaks if db re-addresses; the named object (and, in Chapter 06, the tag) survives change.

**Cleanup.** None.

### Exercise 4.3 — Reproduce the lateral movement

**Objective.** Show the compromised operator pivoting to the database.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.2.10 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with the any-any accept, the operator reaches the database. Chapter 05 denies exactly this while preserving the app path.

**Negative test.** Re-run `web->db`; it also succeeds. Until the rulebase distinguishes the sources, the gateway treats app and operator identically.

**Cleanup.** None — Chapter 05 authors the segmentation rulebase.

## Summary and Completion Checklist

- [ ] Temporary any-any accept makes the network flat.
- [ ] The two legitimate flows named (web→db PGSQL, hmi→plc MODBUS).
- [ ] The hmi→db lateral movement reproduced.
- [ ] Ready to replace any-any with least-privilege rules.
