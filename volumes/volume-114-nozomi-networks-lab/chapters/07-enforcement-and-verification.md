# Chapter 07: Enforcement and Verification

## Learning Objectives

- Verify the full protocol-aware matrix: read allowed, write denied, non-Modbus denied.
- Confirm anomalies are recorded distinctly from denials.
- Read the enforcer/sensor log as the single source of truth.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Run every case and confirm the outcomes.

**Track 2 — Walkthrough.**

```bash
# A: permitted read via proxy
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.1 1502
# B: denied write via proxy (function blocked)
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.1 1502 40
# C: denied direct-to-PLC (isolation)
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.40 502 40
# D: denied non-Modbus via proxy
sudo ip netns exec hmi bash -c 'printf "hello\n" | nc -w2 10.80.1.1 1502'; echo "(D dropped)"
```

**Expected result.**

```text
READ value= 55            (A: allowed)
NO-RESPONSE (denied?)     (B: write blocked at function)
NO-RESPONSE (denied?)     (C: direct path isolated)
(D dropped)               (D: non-Modbus rejected)
```

Only the Modbus read succeeds; writes (via proxy or direct) and non-Modbus are denied — the protocol-aware policy in full.

**Negative test.** Change `ALLOW_FC` in the proxy to include `6` and watch the write start succeeding — proof the decision is the function code, not the port. Restore `ALLOW_FC = {3, 4}`.

**Cleanup.** Restore the proxy if changed, and restart it.

### Exercise 7.2 — Denials vs anomalies in the log

**Objective.** See that a blocked function and a bad value are distinct events.

**Track 2 — Walkthrough.**

```bash
# generate a blocked write and an out-of-range read
sudo ip netns exec plc python3 -c "import socket,struct; s=socket.socket(); s.connect(('127.0.0.1',502)); s.sendall(struct.pack('>HHHBBHH',1,0,6,1,6,0,300)); s.recv(64)"  # push value out of range on the PLC
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.1 1502 40 >/dev/null   # blocked
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.1 1502 >/dev/null       # allowed but out of range
echo "== enforcer/sensor log =="; grep -E "DENY|ANOMALY" /tmp/mbproxy.log | tail -2
```

**Expected result.**

```text
DENY fc=6 (write/non-read blocked)
ANOMALY value=300 out of [20,80]
```

A `DENY` (segmentation) and an `ANOMALY` (detection) — two different event types from one tool, exactly the pairing Nozomi provides.

**Cleanup.** Restore a normal value if you wish (`write` directly on the PLC to 55).

### Exercise 7.3 — The decision is the function and the value, not the address

**Objective.** Prove protocol/process awareness, not L3/L4, drives the outcome.

**Track 2 — Walkthrough.** From the same source and to the same port, a read is allowed and a write is denied:

```bash
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py read  10.80.1.1 1502 && echo "read OK"
sudo ip netns exec hmi python3 /usr/local/bin/mbclient.py write 10.80.1.1 1502 40 || true; echo "write handled by function policy"
```

**Expected result.** Identical source and destination:port, opposite outcomes — the function code decided, which is the whole difference from an L4 firewall.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Read allowed; write and non-Modbus denied (via proxy and direct).
- [ ] Denials and anomalies recorded as distinct events.
- [ ] The decision confirmed to depend on function and value, not address.
- [ ] The enforcer/sensor log used as the source of truth.
