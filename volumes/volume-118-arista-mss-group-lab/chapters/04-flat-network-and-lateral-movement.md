# Chapter 04: The Flat Network and Lateral Movement

## Learning Objectives

- Show that, before group policy, every group reaches every group.
- Demonstrate the operator-to-database lateral movement.
- Name the two group flows the policy must permit.

## Before group policy

Until MSS-Group policy is applied, the fabric forwards between all groups. This chapter proves the flat state, reproduces the lateral movement, and records the two flows the group policy will permit.

## Hands-On Lab

### Exercise 4.1 — Confirm the flat network

**Objective.** Show all group-to-group flows succeed.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.120.2.20 5432 && echo "web->db REACH"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.2.20 5432 && echo "hmi->db REACH (lateral!)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.4.40 502  && echo "hmi->plc REACH"'
```

**Expected result.** All REACH — every group reaches every other, including the operator reaching the database.

**Negative test.** A closed port fails for lack of a service, not for policy — distinguish "no service" from "denied."

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 4.2 — Name the group flows

**Objective.** Record the flows the group policy will permit.

**Track 1 & 2 — Walkthrough.**

```text
SG-Web  -> SG-DB : tcp 5432   (redirected through the firewall — MSS macro)
SG-Mgmt -> SG-OT : tcp 502
```

Everything else group-to-group — most importantly `SG-Mgmt -> SG-DB` (hmi -> db) — is illegitimate.

**Expected result.** A two-line group-policy plan.

**Negative test.** Writing the SG-Web→SG-DB rule against the db IP loses the group benefit; a rule against SG-DB covers any database that joins the group.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 4.3 — Reproduce the lateral movement

**Objective.** Show the operator pivoting to the database.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.2.20 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with no group policy, the operator reaches the database. Chapter 05 denies this by default.

**Rollback.** None — Chapter 05 applies group policy.

## Summary and Completion Checklist

- [ ] All group-to-group flows reach in the flat state.
- [ ] The two group flows named (SG-Web→SG-DB:5432, SG-Mgmt→SG-OT:502).
- [ ] The hmi→db lateral movement reproduced.
- [ ] Ready to apply MSS-Group policy.
