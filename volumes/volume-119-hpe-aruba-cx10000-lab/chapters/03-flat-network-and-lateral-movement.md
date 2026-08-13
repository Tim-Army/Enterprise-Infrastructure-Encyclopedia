# Chapter 03: The Flat Network and Lateral Movement

## Learning Objectives

- Show that, before policy, every endpoint reaches every endpoint.
- Demonstrate the operator-to-database lateral movement.
- Name the two flows the stateful policy must permit.

## Before the stateful firewall

Until the DPU's stateful policy is applied, the ToR forwards all east-west traffic. This chapter proves the flat state, reproduces the lateral movement, and records the two flows the stateful policy will permit.

## Hands-On Lab

### Exercise 3.1 — Confirm the flat network

**Objective.** Show all east-west flows succeed.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.130.2.20 5432 && echo "web->db REACH"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.2.20 5432 && echo "hmi->db REACH (lateral!)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.4.40 502  && echo "hmi->plc REACH"'
```

**Expected result.** All REACH — every endpoint reaches every other, including the operator reaching the database.

**Negative test.** A closed port fails for lack of a service, not policy.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.2 — Name the flows to permit

**Objective.** Record the two stateful permits.

**Track 1 & 2 — Walkthrough.**

```text
web -> db : tcp 5432   (return traffic auto-permitted by state)
hmi -> plc : tcp 502
```

Everything else east-west — most importantly `hmi -> db` — is illegitimate.

**Expected result.** A two-line policy plan; return traffic will be handled by connection state, not a second rule.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.3 — Reproduce the lateral movement

**Objective.** Show the operator pivoting to the database.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.2.20 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with no stateful policy, the operator reaches the database. Chapter 04 denies this at the ToR.

**Rollback.** None — Chapter 04 applies stateful policy.

## Summary and Completion Checklist

- [ ] All east-west flows reach in the flat state.
- [ ] The two flows to permit named (web→db:5432, hmi→plc:502).
- [ ] The hmi→db lateral movement reproduced.
- [ ] Ready to apply the stateful firewall at the ToR.
