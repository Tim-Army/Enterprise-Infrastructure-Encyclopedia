# Chapter 06: Process Anomaly Detection

## Learning Objectives

- Detect a process value outside its learned range even on a permitted read.
- Understand why behavioral detection complements function-aware segmentation.
- See that detection fires on the *value*, not just the flow or function.

## The flow is allowed, the value is wrong

Function-aware segmentation stops the disallowed **write**. But a permitted **read** can still return a value that indicates trouble — the process drifted, a sensor failed, or an earlier write (from somewhere the enforcer did not cover) pushed it out of range. Nozomi's process baseline catches exactly this: the read is allowed, but the value `250` is outside the learned range `20–80`, so it raises an **anomaly**. This is detection layered on top of enforcement.

## Hands-On Lab

### Exercise 6.1 — Trigger and see the value anomaly

**Objective.** Read the out-of-range value and find the anomaly in the log.

**Track 1 — Walkthrough.** Guardian compares the live process variable to its learned range and raises a process-anomaly alert with the register, value, and expected range — independent of whether any flow was blocked.

**Track 2 — Walkthrough.** The register is still `250` from Chapter 04. Read it through the proxy and check the anomaly log:

```bash
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read 10.80.1.1 1502
sudo grep -m1 ANOMALY /tmp/mbproxy.log
```

**Expected result.**

```text
READ value= 250
ANOMALY value=250 out of [20,80]
```

The read is permitted (it is a legitimate function), yet the proxy flags the value as outside the learned range — a process anomaly that pure segmentation would miss.

**Negative test.** Read a value inside the range and confirm no anomaly fires. First restore a normal value directly on the PLC (simulating the process returning to normal), then read:

```bash
sudo ip netns exec plc python3 -c "import socket,struct; s=socket.socket(); s.connect(('127.0.0.1',502)); s.sendall(struct.pack('>HHHBBHH',1,0,6,1,6,0,55)); s.recv(64)"
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read 10.80.1.1 1502
tail -1 /tmp/mbproxy.log
```

A read returning 55 produces no new `ANOMALY` line — only out-of-range values are flagged.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 6.2 — Why both controls are needed

**Objective.** See that segmentation and detection catch different things.

**Track 1 & 2 — Walkthrough.** Compare the two events:

```text
- Chapter 05: hmi WRITE denied         -> segmentation stopped an unauthorized control action
- Chapter 06: read value 250 flagged    -> detection caught a bad process state on an allowed flow
```

**Expected result.** A clear split: **function-aware segmentation** prevents disallowed actions; **process-behavioral detection** surfaces bad states that slip through on allowed actions. Nozomi does both; an L4 firewall does neither.

**Negative test.** Relying on segmentation alone would miss the drifted value; relying on detection alone would let the unauthorized write through and only alert after the fact. Both together is the OT-security posture.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] An out-of-range value flagged on a permitted read.
- [ ] In-range values produce no anomaly.
- [ ] Segmentation (block action) and detection (flag state) distinguished.
- [ ] Why OT security needs both understood.
