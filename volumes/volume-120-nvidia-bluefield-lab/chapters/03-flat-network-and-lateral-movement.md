# Chapter 03: The Flat Network and Lateral Movement

## Learning Objectives

- Confirm that, before DPU policy, each workload reaches everything.
- Demonstrate the operator-to-database lateral movement.
- Name the two flows each DPU must permit.

## Before the DPU policy

The DPUs are in the path but not yet enforcing. This chapter proves the flat state, reproduces the lateral movement, and records the two flows the DPUs will permit.

## Hands-On Lab

### Exercise 3.1 — Confirm the flat network

**Objective.** Show each workload reaches targets it should not.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.20 5432 && echo "web->db REACH"'
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.40 502  && echo "web->plc REACH (should be denied)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.20 5432 && echo "hmi->db REACH (lateral!)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.40 502  && echo "hmi->plc REACH"'
```

**Expected result.** All REACH — before DPU policy, `web` reaches the PLC and `hmi` reaches the database, neither of which it should.

**Negative test.** A closed port fails for lack of a service, not policy.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.2 — Name the flows to permit

**Objective.** Record the per-workload permits.

**Track 1 & 2 — Walkthrough.**

```text
web (DPU-web) -> db:5432   permit
hmi (DPU-hmi) -> plc:502   permit
```

Everything else from each workload — `web → plc`, `hmi → db` — is illegitimate and will be denied at that workload's DPU.

**Expected result.** A two-line per-workload policy; each DPU enforces only its own workload's permitted flow.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.3 — Reproduce the lateral movement

**Objective.** Show the operator pivoting to the database.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.20 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with no DPU policy, the operator reaches the database. Chapter 04 denies this at the hmi DPU.

**Rollback.** None — Chapter 04 applies DPU policy.

## Summary and Completion Checklist

- [ ] All flows reach in the flat state.
- [ ] The two per-workload permits named.
- [ ] The hmi→db lateral movement reproduced.
- [ ] Ready to apply policy at each DPU.
