# Chapter 07: Enforcement and Verification

## Learning Objectives

- Prove the hmi→db lateral flow is dropped while web→db and hmi→plc still work.
- Read the connections table and rule hit counts.
- Correlate a dropped flow with a SmartConsole / gateway log.

## Hands-On Lab

### Exercise 7.1 — The lateral flow is dropped

**Objective.** Confirm least privilege holds after install.

**Track 1 — Walkthrough.**

```text
# from web: nc db 5432  -> connects   web->db OPEN
# from hmi: nc db 5432  -> dropped     hmi->db BLOCKED (Cleanup rule)
# from hmi: nc plc 502  -> connects   hmi->plc OPEN
```

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.40.2.10 5432 && echo "web->db OPEN" || echo "web->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.2.10 5432 && echo "hmi->db OPEN" || echo "hmi->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.4.10 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
hmi->plc OPEN
```

The lateral path is dropped by the Cleanup rule; both legitimate flows are untouched.

**Negative test.** Change the `web-to-db` rule's service from PGSQL to SSH and watch web→db:5432 break while ssh would pass — proof the *service* match is part of the decision. Restore it and re-install.

**Cleanup.** Restore and re-install any temporary change.

### Exercise 7.2 — Connections and rule hits

**Objective.** See the gateway account for permits and drops.

**Track 1 — Walkthrough.**

```text
gw> fw ctl conntab | grep 5432
    ... 10.40.1.10 -> 10.40.2.10:5432   (web->db, accepted)
mgmt> (SmartConsole > Security Policies) shows per-rule Hits:
    web-to-db   : 6
    hmi-to-plc  : 4
    Cleanup rule: 3   (the hmi->db drops)
```

**Expected result.** A connection for web→db and non-zero hits on the permit rules and the Cleanup rule. Zero hits during an active test means traffic is not transiting the gateway (topology/routing).

**Track 2 — Walkthrough.**

```bash
sudo nft flush chain inet cpg forward
sudo nft add rule inet cpg forward ip saddr @role_web ip daddr @role_db tcp dport 5432 counter accept
sudo nft add rule inet cpg forward ip saddr 10.40.3.10 ip daddr 10.40.4.10 tcp dport 502 counter accept
sudo nft add rule inet cpg forward ip saddr 10.40.3.10 ip daddr 10.40.2.10 counter log prefix '"CPG-DENY "' drop
sudo nft add rule inet cpg forward ip saddr 10.40.0.0/16 ip daddr 10.40.0.0/16 counter drop
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.2.10 5432; true'
sudo nft list chain inet cpg forward | grep 'CPG-DENY'
```

**Expected result.** The deny rule's counter increments after the hmi→db attempt.

**Cleanup.** None.

### Exercise 7.3 — Correlate the drop in the log

**Objective.** Find the dropped flow in the log.

**Track 1 — Walkthrough.** With `track Log` on the Cleanup rule, the drop appears in the logs (SmartConsole Logs & Monitor, or `fw log` on the gateway):

```text
gw> fw log | grep -E "10.40.3.10.*10.40.2.10.*drop"
... src=10.40.3.10 dst=10.40.2.10 service=5432 rule="Cleanup rule" action=drop
```

**Expected result.** A log entry naming source (hmi), destination db:5432, the Cleanup rule, and action drop — the record that proves the control fired.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.40.2.10 5432; true'
sudo dmesg | grep -o 'CPG-DENY.*SRC=10.40.3.10.*DPT=5432' | tail -1
```

**Expected result.** A `CPG-DENY` line naming source 10.40.3.10 to port 5432.

**Negative test.** A rule with `track None` produces no log — you would see the failure but have no evidence. Log the Cleanup rule and denies during rollout.

**Cleanup.** Keep logging for Chapter 09.

## Summary and Completion Checklist

- [ ] hmi→db dropped; web→db and hmi→plc permitted.
- [ ] Connections table and per-rule hit counts observed.
- [ ] The dropped flow correlated in the log.
- [ ] Service-level match confirmed as part of the decision.
