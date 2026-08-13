# Chapter 07: Anomaly Detection and Verification

## Learning Objectives

- See a denied lateral attempt raised as a **deviation from the baseline**.
- Distinguish enforcement (the block) from detection (the alert).
- Confirm that new, unbaselined flows are both denied and flagged.

## Two outcomes from one event

When the operator attempts `hmi → db` after enforcement, two things happen: the enforcer **blocks** it, and — because it deviates from the learned baseline — Claroty **flags** it as an anomaly. Detection matters even where enforcement exists: a deviation is a signal that something changed (a new device, a misconfiguration, or an intrusion), and it is the same signal that would fire in monitor-only deployments where enforcement is not yet in place.

## Hands-On Lab

### Exercise 7.1 — Trigger and see the deviation

**Objective.** Attempt the lateral flow and find it in the deviation log.

**Track 1 — Walkthrough.** xDome compares live traffic to the baseline continuously; an attempt to open a never-seen flow raises an alert with the assets, zones, and protocol, whether or not an enforcer blocked it.

**Track 2 — Walkthrough.** The enforcer already logs denies (Chapter 06); a deny for a flow not in the baseline *is* the deviation. Trigger it and read the log:

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.70.2.20 5432; true'
sudo dmesg | grep -o 'XDOME-DENY.*SRC=10.70.3.30.*DST=10.70.2.20.*DPT=5432' | tail -1
```

**Expected result.** An `XDOME-DENY ... SRC=10.70.3.30 ... DST=10.70.2.20 ... DPT=5432` line — the `hmi → db` deviation, blocked and recorded.

**Negative test.** A *sanctioned* flow (`web → db`) produces no deviation — it matches the baseline, so it neither blocks nor alerts. Only departures from normal are flagged.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 7.2 — A new asset appears (unbaselined)

**Objective.** Show that a brand-new flow is denied and flagged even if it is not obviously malicious.

**Track 2 — Walkthrough.** Simulate a new engineering laptop appearing in OT-Ops and trying to reach the PLC — legitimate-looking, but never baselined:

```bash
sudo ip netns exec hmi ip addr add 10.70.3.31/24 dev hmi-e 2>/dev/null
sudo ip netns exec hmi bash -c 'nc -s 10.70.3.31 -z -w2 10.70.4.40 502; true'
sudo dmesg | grep -o 'XDOME-DENY.*SRC=10.70.3.31.*DPT=502' | tail -1
```

**Expected result.** An `XDOME-DENY ... SRC=10.70.3.31 ... DPT=502` — the new source is denied and flagged because it was not in the baseline, even though the *destination and port* are sanctioned for the known operator. Segmentation is per-source, and new sources are surfaced for review.

**Negative test.** If the policy were destination-only ("anything may reach plc:502"), the new laptop would pass silently — the value of baselining the *source* is that unknown devices are caught. Restore by removing the extra address:

```bash
sudo ip netns exec hmi ip addr del 10.70.3.31/24 dev hmi-e 2>/dev/null
```

**Rollback.** Extra address removed above.

### Exercise 7.3 — Confirm the enforced policy matches the intent

**Objective.** Verify enforcement equals the derived policy.

**Track 2 — Walkthrough.**

```bash
echo "== intended (derived) policy =="; cat /etc/xdome/policy
echo "== enforced rules =="; sudo nft list chain inet xdome forward | grep -E "tcp dport|drop"
```

**Expected result.** The enforced accept rules correspond one-to-one with the derived zone policy, plus the default drop — enforcement matches intent, which is exactly what Claroty continuously checks against drift.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The denied lateral attempt seen as a baseline deviation.
- [ ] Enforcement (block) and detection (alert) distinguished.
- [ ] A new, unbaselined source denied and flagged.
- [ ] Enforced rules confirmed to match the derived policy.
