# Chapter 07: Enforcement and Verification

## Learning Objectives

- Verify the full matrix: sanctioned flow works, all lateral movement blocked, kill switch total.
- Read the enforcement log of denied east-west attempts.
- Confirm isolation held without agents or VLAN changes.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Run every case and confirm the outcomes.

**Track 2 — Walkthrough.**

```bash
# A: sanctioned flow
sudo ip netns exec web    bash -c 'nc -z -w2 10.100.1.20 5432 && echo A:web->db OPEN || echo A:web->db BLOCKED'
# B: worm to database (blocked)
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.20 5432 && echo B:victim->db OPEN || echo B:victim->db BLOCKED'
# C: worm to PLC (blocked)
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.40 502  && echo C:victim->plc OPEN || echo C:victim->plc BLOCKED'
# D: operator to PLC, no sanctioned east-west rule (blocked)
sudo ip netns exec hmi    bash -c 'nc -z -w2 10.100.1.40 502  && echo D:hmi->plc OPEN || echo D:hmi->plc BLOCKED'
```

**Expected result.**

```text
A:web->db OPEN
B:victim->db BLOCKED
C:victim->plc BLOCKED
D:hmi->plc BLOCKED
```

Only the one sanctioned flow succeeds; every lateral path is isolated, including flows that merely lack a rule.

**Negative test.** Add a second sanctioned flow (`hmi → plc:502`) and watch only it open — the model grants exactly what you permit, nothing adjacent. Remove it afterward to keep the plan.

**Cleanup.** Remove any temporary rule.

### Exercise 7.2 — Read the enforcement log

**Objective.** See denied east-west attempts recorded.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec victim bash -c 'for p in 22 502 5432; do nc -z -w1 10.100.1.20 $p 2>/dev/null; done; true'
sudo dmesg | grep -o 'AIRGAP-DENY.*SRC=10.100.1.50.*DPT=[0-9]*' | tail -3
```

**Expected result.** `AIRGAP-DENY` lines for the victim's attempts — every blocked lateral connection is recorded, giving visibility into who tried to move laterally.

**Negative test.** The sanctioned `web → db` produces no deny line — only unpermitted east-west is logged, so the log is a clean feed of lateral-movement attempts.

**Cleanup.** None.

### Exercise 7.3 — Confirm it was agentless and non-disruptive

**Objective.** Verify no device changed its address or ran an agent.

**Track 2 — Walkthrough.**

```bash
for d in web db hmi plc victim; do
  echo -n "$d: "; sudo ip netns exec $d ip -4 -o addr show dev $d-e | awk '{print $4}'
done
```

**Expected result.** Every device still has its original `10.100.1.x` address (now `/32`), and none is running any security software — the segmentation came entirely from the network layer, exactly Airgap's agentless promise.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Sanctioned flow works; all lateral movement blocked.
- [ ] Denied east-west attempts recorded in the log.
- [ ] Isolation confirmed agentless and non-disruptive.
- [ ] The network-of-one model verified end to end.
