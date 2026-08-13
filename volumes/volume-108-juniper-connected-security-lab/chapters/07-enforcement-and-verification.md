# Chapter 07: Enforcement and Verification

## Learning Objectives

- Prove the MGMT→DB lateral flow is denied while APP→DB and MGMT→OT still work.
- Read the session table and policy hit counters.
- Correlate a denied flow with a security log.

## Hands-On Lab

### Exercise 7.1 — The lateral flow is denied

**Objective.** Confirm least privilege holds after the permit-any is gone.

**Track 1 — Walkthrough.**

```text
srx> (from web) telnet 10.20.2.10 5432  -> connects    web->db OPEN
srx> (from hmi) telnet 10.20.2.10 5432  -> refused/timeout  hmi->db BLOCKED
srx> (from hmi) telnet 10.20.4.10 502   -> connects    hmi->plc OPEN
```

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.20.2.10 5432 && echo "web->db OPEN" || echo "web->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 5432 && echo "hmi->db OPEN" || echo "hmi->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.4.10 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
hmi->plc OPEN
```

The lateral path is closed by the zone policy; both legitimate flows are untouched.

**Negative test.** Change the `web-to-db` policy application from `junos-postgresql` to `junos-ssh` and watch `web->db:5432` break while ssh would pass — proof the *application* match, not just the zone pair, is doing the work. Restore it.

**Rollback.** Restore any temporary change.

### Exercise 7.2 — Read the session table and hit counts

**Objective.** See the firewall account for permits and denies.

**Track 1 — Walkthrough.**

```text
srx> show security flow session
  Session ID 12  Policy web-to-db  In: 10.20.1.10/.. --> 10.20.2.10/5432  ...
srx> show security policies hit-count
  web-to-db  : 6
  hmi-to-plc : 4
  deny-mgmt-db : 3
```

**Expected result.** Active sessions for the permitted flows and a non-zero hit count on `deny-mgmt-db` — the lateral drop is visible and counted.

**Negative test.** No session and a zero hit-count during an active test means traffic is not transiting the SRX (routing/zone assignment), not that policy is working. Zero counters during testing is a misconfiguration signal.

**Track 2 — Walkthrough.**

```bash
sudo nft flush chain inet jsec forward
sudo nft add rule inet jsec forward ip saddr 10.20.1.10 ip daddr 10.20.2.10 tcp dport 5432 counter accept
sudo nft add rule inet jsec forward ip saddr 10.20.3.10 ip daddr 10.20.4.10 tcp dport 502 counter accept
sudo nft add rule inet jsec forward ip saddr 10.20.3.10 ip daddr 10.20.2.10 counter log prefix '"JSEC-DENY "' drop
sudo nft add rule inet jsec forward ip saddr 10.20.0.0/16 ip daddr 10.20.0.0/16 counter drop
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 5432; true'
sudo nft list chain inet jsec forward | grep -A0 'JSEC-DENY'
```

**Expected result.** The deny rule's counter increments after the `hmi->db` attempt.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 7.3 — Correlate the denial in the log

**Objective.** Find the denied flow in the security log.

**Track 1 — Walkthrough.** With `then log session-init` on `deny-mgmt-db` and traffic logging configured, the drop appears in the security log:

```text
srx> show log security | match RT_FLOW | match 10.20.3.10
RT_FLOW_SESSION_DENY ... source 10.20.3.10 destination 10.20.2.10/5432 policy deny-mgmt-db
```

**Expected result.** An `RT_FLOW_SESSION_DENY` entry naming the source (hmi), destination db:5432, and the `deny-mgmt-db` policy — the record that proves the control fired.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.2.10 5432; true'
sudo dmesg | grep -o 'JSEC-DENY.*SRC=10.20.3.10.*DPT=5432' | tail -1
```

**Expected result.** A `JSEC-DENY` line naming source 10.20.3.10 to port 5432.

**Negative test.** Without logging, drops are silent — you would see the failure but have no evidence. Log denies during rollout so a working policy is distinguishable from a broken path.

**Rollback.** Keep logging for Chapter 09.

## Summary and Completion Checklist

- [ ] MGMT→DB denied; APP→DB and MGMT→OT permitted.
- [ ] Session table and policy hit counts observed.
- [ ] The denied flow correlated in the security log.
- [ ] Application-level match confirmed as part of the decision.
