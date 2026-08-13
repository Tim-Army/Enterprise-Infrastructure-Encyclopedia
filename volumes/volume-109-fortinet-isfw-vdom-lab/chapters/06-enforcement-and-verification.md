# Chapter 06: Enforcement and Verification

## Learning Objectives

- Prove the MGMT→DB lateral flow is denied while APP→DB and MGMT→OT still work.
- Use the policy lookup and session list to see the decision.
- Correlate a denied flow with the forward-traffic log.

## Hands-On Lab

### Exercise 6.1 — The lateral flow is denied

**Objective.** Confirm least privilege holds after the permit-all is gone.

**Track 1 — Walkthrough.**

```text
# from web: nc db 5432   -> connects   web->db OPEN
# from hmi: nc db 5432   -> reset/timeout  hmi->db BLOCKED
# from hmi: nc plc 502   -> connects   hmi->plc OPEN (MGMT->OT zone policy)
```

Confirm the FortiGate's own view with a policy lookup:

```text
FGT # diagnose firewall iprope lookup 10.30.3.10 12345 10.30.2.10 5432 6 port4
<src [10.30.3.10-12345] dst [10.30.2.10-5432] proto 6 dev port4> matches policy id: 3
FGT # diagnose firewall iprope lookup 10.30.1.10 12345 10.30.2.10 5432 6 port2
<src [10.30.1.10-12345] dst [10.30.2.10-5432] proto 6 dev port2> matches policy id: 1
```

The lookup reports only the **matched policy id** — not its name or action. Map id `3` to `deny-mgmt-db` (deny) and id `1` to `web-to-db` (accept) with `show firewall policy`.

**Evaluation FortiGate.** The `iprope lookup` takes the *ingress interface* as its last argument — on the eval that is the VLAN subinterface: `v2003` for the `hmi` lookup (in place of `port4`) and `v2001` for the `web` lookup (in place of `port2`). The matched policy ids are identical.

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

**Rollback.** Restore any temporary change.

### Exercise 6.2 — Read the session list and policy hits

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

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 6.3 — Correlate the denial in the log

**Objective.** Find the denied flow in the forward-traffic log.

**Track 1 — Walkthrough.** With `set logtraffic all` on the deny policy, the drop appears in the forward-traffic log. `execute` commands take **no pipe** (`| grep` returns `pipe cannot be used here`), so filter with FortiOS's own `execute log filter` — set the criteria first, then display:

```text
FGT # execute log filter reset
FGT # execute log filter category traffic
FGT # execute log filter field srcip 10.30.3.10
FGT # execute log filter field dstip 10.30.2.10
FGT # execute log display
20 logs found.
10 logs returned.

1: date=... srcip=10.30.3.10 srcintf="port4" dstip=10.30.2.10 dstport=5432 proto=6 action="deny" policyid=3 policyname="deny-mgmt-db" service="PGSQL" ...
```

The `execute log filter …` lines are **silent setters** — they print nothing on success; run `execute log filter dump` to see the assembled predicate (`Filter: ( srcip … ) AND ( dstip … )`). Filter on `srcip`/`dstip`, not `action` — the FortiGate's own local-out traffic (NTP, DNS) is logged as `action="accept"` too and would bury the result. Two things the log makes plain: on the evaluation build `srcintf`/`dstintf` read the VLAN subinterfaces (`v2003`/`v2002`) rather than ports, and a *permitted* session logs several action values across its life (`accept`, then `close` or `server-rst` at teardown) — only `deny` is a block.

**Expected result.** A forward-traffic entry naming source (hmi), destination db:5432, `policyid=3`, `policyname="deny-mgmt-db"`, `action="deny"` — the record that proves the control fired.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.2.10 5432; true'
sudo dmesg | grep -o 'FGT-DENY.*SRC=10.30.3.10.*DPT=5432' | tail -1
```

**Expected result.** A `FGT-DENY` line naming source 10.30.3.10 to port 5432.

**Negative test.** Without `logtraffic`, drops are silent — you would see the failure but have no evidence. Log denies during rollout.

**Rollback.** Keep logging for Chapter 09.

## Summary and Completion Checklist

- [ ] MGMT→DB denied; APP→DB and MGMT→OT permitted.
- [ ] Policy lookup, session list, and hit counters observed.
- [ ] The denied flow correlated in the forward-traffic log.
- [ ] Service-level match confirmed as part of the decision.
