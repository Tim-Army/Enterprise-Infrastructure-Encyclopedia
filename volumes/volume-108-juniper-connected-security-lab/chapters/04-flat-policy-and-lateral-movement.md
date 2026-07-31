# Chapter 04: The Flat Policy and Lateral Movement

## Learning Objectives

- Open the firewall with a temporary permit-all to reproduce a flat network.
- Demonstrate the operator-to-database lateral movement.
- Name the legitimate flows the policy must preserve.

## The deliberately-open starting point

An SRX with zones but no policies denies all inter-zone traffic — which is the *end* state, not the start. To reproduce the flat network every volume in this series begins from, you will add a temporary **permit-any** policy, prove the lateral movement, then replace it in Chapter 05 with least-privilege rules. Starting open and tightening is the honest way to see the control work.

## Hands-On Lab

### Exercise 4.1 — Add a temporary permit-any and confirm flatness

**Objective.** Make every zone reach every zone, then show the lateral flow.

**Track 1 — Walkthrough.** Add a broad permit between the relevant zone pairs (or a global permit) as the flat baseline:

```text
[edit security policies]
set global policy allow-all match source-address any destination-address any application any
set global policy allow-all then permit
commit
```

Test the flows:

```text
srx> (from hmi) telnet 10.20.2.10 5432   -> connects  (lateral!)
srx> (from web) telnet 10.20.2.10 5432   -> connects  (legitimate)
srx> (from hmi) telnet 10.20.4.10 502    -> connects  (legitimate)
```

**Track 2 — Walkthrough.** Add a permissive forward chain:

```bash
sudo nft add chain inet jsec forward '{ type filter hook forward priority 0 ; policy accept ; }'
sudo ip netns exec web bash -c 'nc -z -w2 10.20.2.10 5432 && echo web->db REACH'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 5432 && echo hmi->db REACH (lateral!)'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.4.10 502  && echo hmi->plc REACH'
```

**Expected result.** All three flows REACH — the firewall is present but wide open. The `hmi->db` connection is the lateral movement.

**Negative test.** A flow to a closed port (`hmi->db:502`) fails because nothing listens, not because of policy. Distinguish "no service" from "denied."

**Cleanup.** Leave the permit-any in place until Chapter 05 replaces it.

### Exercise 4.2 — Name the legitimate flows

**Objective.** Record the permit list so tightening does not cause an outage.

**Track 1 & 2 — Walkthrough.**

```text
APP  -> DB   : tcp 5432    (web -> db)
MGMT -> OT   : tcp 502     (hmi -> plc)
```

Everything else inter-zone — most importantly `MGMT -> DB` (hmi -> db) — is illegitimate.

**Expected result.** A two-line permit list; the whole segmentation is those two flows.

**Negative test.** Write the APP→DB rule against the db IP and note it breaks if db scales or re-addresses; a rule against the `db` address-book object (or an `app-servers` set on the source) survives change.

**Cleanup.** None.

### Exercise 4.3 — Reproduce the lateral movement

**Objective.** Show the compromised operator pivoting to the database.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with permit-any, the operator reaches the database. Chapter 05 denies exactly this while preserving the app path.

**Negative test.** Re-run `web->db`; it also succeeds. Until policy distinguishes the sources, the firewall treats app and operator identically.

**Cleanup.** None — Chapter 05 authors least-privilege policy.

## Summary and Completion Checklist

- [ ] Temporary permit-any makes the network flat.
- [ ] The two legitimate flows named (APP→DB:5432, MGMT→OT:502).
- [ ] The MGMT→DB lateral movement reproduced.
- [ ] Ready to replace permit-any with least-privilege policy.
