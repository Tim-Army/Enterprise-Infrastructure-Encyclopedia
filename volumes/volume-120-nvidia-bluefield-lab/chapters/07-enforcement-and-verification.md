# Chapter 07: Enforcement and Verification

## Learning Objectives

- Verify the full matrix: each workload reaches only its sanctioned target.
- Confirm the DPU deny logs record the lateral attempts.
- Re-confirm the out-of-band property holds under the full matrix.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Run every case and confirm the outcomes.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.20 5432 && echo "A:web->db OPEN"  || echo "A:web->db BLOCKED"'
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.40 502  && echo "B:web->plc OPEN" || echo "B:web->plc BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.20 5432 && echo "C:hmi->db OPEN"  || echo "C:hmi->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.40 502  && echo "D:hmi->plc OPEN" || echo "D:hmi->plc BLOCKED"'
```

**Expected result.**

```text
A:web->db OPEN
B:web->plc BLOCKED
C:hmi->db BLOCKED
D:hmi->plc OPEN
```

Each workload reaches only its sanctioned target; every lateral flow is denied at that workload's own DPU.

**Negative test.** Change `dpu-web`'s permit to target the PLC and watch `web → plc` open while `web → db` closes — proof the decision is the DPU policy, enforced per workload. Restore it.

**Cleanup.** Restore any changed DPU rule.

### Exercise 7.2 — Read the DPU deny logs

**Objective.** See the lateral attempts recorded by the DPUs.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.40 502; true'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.140.0.20 5432; true'
sudo dmesg | grep -oE 'DPU-(WEB|HMI)-DENY.*DPT=[0-9]+' | tail -2
```

**Expected result.** `DPU-WEB-DENY ... DPT=502` and `DPU-HMI-DENY ... DPT=5432` — each DPU logs its own workload's blocked lateral attempts, giving per-server visibility.

**Cleanup.** None.

### Exercise 7.3 — Out-of-band holds under load

**Objective.** Re-confirm a compromised workload still cannot break out.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web nft flush ruleset 2>/dev/null
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.40 502 && echo "web->plc OPEN (BROKEN)" || echo "web->plc STILL BLOCKED"'
```

**Expected result.** `web->plc STILL BLOCKED` — even after the workload flushes its own rules again, the DPU policy denies the lateral flow. The property from Chapter 05 is not a one-off.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Each workload reaches only its sanctioned target.
- [ ] The DPUs log each workload's lateral attempts.
- [ ] The out-of-band property re-confirmed.
- [ ] Per-workload DPU enforcement verified end to end.
