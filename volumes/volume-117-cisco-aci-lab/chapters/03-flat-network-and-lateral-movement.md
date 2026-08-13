# Chapter 03: The Flat Network and Lateral Movement

## Learning Objectives

- Show that, before contracts, every EPG reaches every EPG.
- Demonstrate the operator-to-database lateral movement.
- Name the two flows the contracts must permit.

## Before the whitelist

ACI is whitelist by default *once enforcement is on*, but to see the control work we start from the flat, routed state of Chapter 02 (or, on a real fabric, an unenforced VRF) where every EPG reaches every other. This chapter proves the flatness, reproduces the lateral movement, and records the two flows contracts will permit.

## Hands-On Lab

### Exercise 3.1 — Confirm the flat network

**Objective.** Show all EPG-to-EPG flows succeed.

**Track 1 — Walkthrough.** With a VRF in unenforced mode (or before contracts are applied), the fabric forwards between all EPGs — the state you tighten by moving to enforced mode with contracts.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.110.2.20 5432 && echo "web->db REACH"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.2.20 5432 && echo "hmi->db REACH (lateral!)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.4.40 502  && echo "hmi->plc REACH"'
```

**Expected result.** All REACH — every EPG reaches every other, including the operator reaching the database.

**Negative test.** A closed port (`hmi->db:502`) fails because nothing listens, not because of policy — distinguish "no service" from "denied."

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.2 — Name the contracted flows

**Objective.** Record the flows the contracts will permit.

**Track 1 & 2 — Walkthrough.**

```text
EPG-Web  -> EPG-DB  : tcp 5432   (contract web-db)
EPG-Mgmt -> EPG-OT  : tcp 502    (contract mgmt-ot)
```

Everything else EPG-to-EPG — most importantly `EPG-Mgmt -> EPG-DB` (hmi -> db) — is illegitimate and denied by the whitelist default once contracts govern the fabric.

**Expected result.** A two-line contract plan; the whole segmentation is those two flows plus the implicit deny.

**Negative test.** Writing the web-db permit against the db IP rather than the EPG loses ACI's application-centric benefit — a rule against the EPG covers any endpoint that joins EPG-DB, including new database servers.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.3 — Reproduce the lateral movement

**Objective.** Show the operator pivoting to the database.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.2.20 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with no contract governing the fabric, the operator reaches the database. Chapter 04 denies this by making contracts the only permitted paths.

**Rollback.** None — Chapter 04 applies contracts.

## Summary and Completion Checklist

- [ ] All EPG-to-EPG flows reach in the flat state.
- [ ] The two contracted flows named (Web→DB:5432, Mgmt→OT:502).
- [ ] The hmi→db lateral movement reproduced.
- [ ] Ready to apply contracts and the whitelist default.
