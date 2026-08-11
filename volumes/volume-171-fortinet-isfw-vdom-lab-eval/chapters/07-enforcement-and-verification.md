# Chapter 07: Enforcement and Verification

## Learning Objectives

- Prove the MGMT→DB lateral flow is denied while APP→DB and MGMT→OT still work.
- Use the policy lookup and session list to see the decision.
- Correlate a denied flow with the forward-traffic log.

## Hands-On Lab

### Exercise 7.1 — The lateral flow is denied

**Objective.** Confirm least privilege holds after the permit-all is gone.

**Track 1 — Walkthrough.**

```text
# from web: nc db 5432   -> connects   web->db OPEN
# from hmi: nc db 5432   -> reset/timeout  hmi->db BLOCKED
# from hmi: nc plc 502   -> connects   hmi->plc OPEN (over inter-VDOM link)
```

Confirm the FortiGate's own view with a policy lookup:

```text
FGT # diagnose firewall iprope lookup 10.30.3.10 12345 10.30.2.10 5432 6 v2003
# policy id: 3 (deny-mgmt-db)  action: deny
FGT # diagnose firewall iprope lookup 10.30.1.10 12345 10.30.2.10 5432 6 v2001
# policy id: 1 (web-to-db)  action: accept
```

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.30.2.10 5432 && echo "web->db OPEN" || echo "web->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432 && echo "hmi->db OPEN" || echo "hmi->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.4.10 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
hmi->plc OPEN
```

The lateral path is closed; both legitimate flows are untouched.

**Negative test.** Change policy 1's service from `PGSQL` to `SSH` and watch `web->db:5432` break while ssh would pass — proof the *service* match, not just the zone pair, is doing the work. Restore it.

**Cleanup.** Restore any temporary change.

### Exercise 7.2 — Read the session list and policy hits

**Objective.** See the firewall account for permits and denies.

**Track 1 — Walkthrough.**

```text
FGT # get system session list | grep 5432
# tcp  ... 10.30.1.10:.. -> 10.30.2.10:5432   (web->db, permitted)
FGT # diagnose firewall iprope show 100004 1
# policy 1 (web-to-db)  pkts/bytes counters incrementing
```

**Expected result.** A session for the permitted `web->db` flow and incrementing counters on policy 1; the deny policy 3 shows drops. Zero counters during an active test means traffic is not transiting the FortiGate.

**Track 2 — Walkthrough.**

```bash
sudo nft flush chain inet fgt forward
sudo nft add rule inet fgt forward ip saddr 10.30.1.10 ip daddr 10.30.2.10 tcp dport 5432 counter accept
sudo nft add rule inet fgt forward ip saddr 10.30.3.10 ip daddr 10.30.4.10 tcp dport 502 counter accept
sudo nft add rule inet fgt forward ip saddr 10.30.3.10 ip daddr 10.30.2.10 counter log prefix '"FGT-DENY "' drop
sudo nft add rule inet fgt forward ip saddr 10.30.0.0/16 ip daddr 10.30.0.0/16 counter drop
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432; true'
sudo nft list chain inet fgt forward | grep 'FGT-DENY'
```

**Expected result.** The deny rule's counter increments after the `hmi->db` attempt.

**Cleanup.** None.

### Exercise 7.3 — Correlate the denial in the log

**Objective.** Find the denied flow in the forward-traffic log.

**Track 1 — Walkthrough.** With `set logtraffic all` on the deny policy, the drop appears in the forward log:

```text
FGT # execute log filter category traffic
FGT # execute log display | grep -E "10.30.3.10.*10.30.2.10.*deny"
... srcip=10.30.3.10 dstip=10.30.2.10 dstport=5432 policyid=3 action=deny
```

**Expected result.** A forward-traffic log entry naming source (hmi), destination db:5432, `policyid=3`, `action=deny` — the record that proves the control fired.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432; true'
sudo dmesg | grep -o 'FGT-DENY.*SRC=10.30.3.10.*DPT=5432' | tail -1
```

**Expected result.** A `FGT-DENY` line naming source 10.30.3.10 to port 5432.

**Negative test.** Without `logtraffic`, drops are silent — you would see the failure but have no evidence. Log denies during rollout.

**Cleanup.** Keep logging for Chapter 09.

## Summary and Completion Checklist

- [ ] MGMT→DB denied; APP→DB and MGMT→OT permitted.
- [ ] Policy lookup, session list, and hit counters observed.
- [ ] The denied flow correlated in the forward-traffic log.
- [ ] Service-level match confirmed as part of the decision.
