# Chapter 04: Behavioral Baseline and the Dangerous Write

## Learning Objectives

- Learn the process baseline: which functions are normal and the normal value range.
- Reproduce the dangerous action — an unauthorized write pushing a value out of range.
- Decide the protocol-aware policy the enforcer will apply.

## Baseline the process, not just the flow

Nozomi learns more than "hmi talks to plc": it learns that the operator normally **reads** register 0, that writes are rare control actions, and that the value normally sits in a range (say 20–80). That process baseline lets it treat an unexpected **write**, or a value **out of range**, as an incident — even though the *flow* (Modbus to the PLC) is permitted. This chapter records the baseline and reproduces the danger.

## Hands-On Lab

### Exercise 4.1 — Learn the normal range

**Objective.** Establish the register's normal operating range from observation.

**Track 1 — Walkthrough.** Guardian samples the process variable over time and learns its normal range and rate of change; deviations later become alerts.

**Track 2 — Walkthrough.** Sample the register a few times under normal operation and record the learned range:

```bash
for v in 40 55 60 48 72; do
  sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.40 502 $v >/dev/null   # normal setpoints
  sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.40 502
done
sudo tee /etc/nozomi/baseline > /dev/null <<'EOF'
register=0 fc_allowed=read range_lo=20 range_hi=80
EOF
cat /etc/nozomi/baseline
```

**Expected result.** Reads returning values in 40–72, and a recorded baseline: register 0 is normally **read**, and its value range is **20–80**.

**Negative test.** Too few samples give a too-narrow range and false anomalies later; a real baseline spans representative operation. This lab uses a small illustrative window.

**Rollback.** Keep the baseline.

### Exercise 4.2 — Reproduce the dangerous write

**Objective.** Show a write pushing the value out of its safe range — the attack.

**Track 2 — Walkthrough.** A compromised operator (or malware on the HMI) writes an out-of-range value:

```bash
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.40 502 250
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.40 502
```

**Expected result.**

```text
WRITE-ACK
READ value= 250
```

The control value is now 250 — far outside the safe range and potentially damaging to the physical process. Two things should have stopped or flagged this: the **write itself** (the operator should not write) and the **out-of-range value**.

**Negative test.** An L4 firewall permitting "hmi → plc:502" cannot prevent this — the malicious write is indistinguishable from a legitimate read at Layer 4. Only protocol/function awareness (Chapter 05) and process baselining (Chapter 06) catch it.

**Rollback.** The register is now 250; Chapter 05 blocks writes, Chapter 06 flags the out-of-range value.

### Exercise 4.3 — Decide the policy

**Objective.** Fix the protocol-aware policy from the baseline.

**Track 1 & 2 — Walkthrough.**

```text
hmi -> plc : Modbus READ (fc 3/4)   ALLOW
hmi -> plc : Modbus WRITE (fc 6/16) DENY   (control changes are not made from this workstation)
any -> plc : non-Modbus             DENY
process    : register 0 value outside 20-80  RAISE ANOMALY (do not silently pass)
```

**Expected result.** A four-line protocol-aware policy that an L4 firewall could not express — the read/write split and the value-range assertion are the Nozomi-specific parts.

**Negative test.** Writing this as "allow 502, deny everything else" loses the read/write distinction and the value check — the whole point is finer than a port.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Process baseline learned (read-normal, range 20–80).
- [ ] The dangerous out-of-range write reproduced.
- [ ] The protocol-aware policy (allow read, deny write, deny non-Modbus, flag out-of-range) decided.
- [ ] Why L4 cannot express this understood.
