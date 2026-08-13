# Chapter 07: Enforcement and Verification

## Learning Objectives

- Confirm only the two brokered, identity-checked flows succeed.
- Read the broker's per-session access log.
- Confirm the decision depends on identity, not source address.

## Hands-On Lab

### Exercise 7.1 — Only brokered identities succeed

**Objective.** Verify the full matrix: valid brokered flows work, everything else fails.

**Track 2 — Walkthrough.**

```bash
# legitimate, brokered by identity
sudo ip netns exec web bash -c 'printf "svc-web TOKEN-WEB-9c21\n" | nc -w2 10.60.1.5 15432 && echo "A:web(svc-web)->db OK"'
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-7f3a\n"  | nc -w2 10.60.1.5 1502  && echo "B:hmi(op-hmi)->plc OK"'
# direct (no broker) — blocked by isolation
sudo ip netns exec hmi bash -c 'nc -z -w2 10.60.9.40 502 || echo "C:hmi->plc DIRECT blocked"'
# wrong identity to the broker — denied
sudo ip netns exec web bash -c 'printf "svc-web TOKEN-WEB-9c21\n" | nc -w2 10.60.1.5 1502 || echo "D:svc-web->plc DENIED (no grant)"'
```

**Expected result.**

```text
A:web(svc-web)->db OK
B:hmi(op-hmi)->plc OK
C:hmi->plc DIRECT blocked
D:svc-web->plc DENIED (no grant)
```

The only two working paths are the granted identity→asset pairs, both brokered; direct access and ungranted identities fail.

**Negative test.** Present `op-hmi`'s identity from the **web** namespace to the plc broker — it still works, because the grant is to the identity, not the host. That is intended: identity is portable and is exactly what should authorize access (in production the identity is bound to strong credentials/MFA, not a copyable token).

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 7.2 — Read the access log

**Objective.** See every brokered session recorded.

**Track 1 — Walkthrough.** The Xage Fabric logs every brokered session — identity, asset, time, allow/deny — to its audit trail, giving per-connection accountability even for protocols (like Modbus) that have none.

**Track 2 — Walkthrough.** Add logging to the broker and read it:

```bash
sudo sed -i 's#exec socat#logger -t xbroker "ALLOW $ident -> $2:$3"; exec socat#' /usr/local/bin/xbroker
sudo sed -i 's#echo "DENY: bad identity"; exit 1#logger -t xbroker "DENY bad-identity $ident"; echo "DENY: bad identity"; exit 1#' /usr/local/bin/xbroker
sudo ip netns exec web bash -c 'printf "attacker NOPE\n" | nc -w2 10.60.1.5 1502' ; true
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-7f3a\n" | nc -w2 10.60.1.5 1502' ; true
journalctl -t xbroker --no-pager | tail -2
```

**Expected result.** An `ALLOW op-hmi -> 10.60.9.40:502` line and a `DENY bad-identity attacker` line — per-session, per-identity accountability for a device that logs nothing itself.

**Negative test.** Without the broker, a direct connection to the PLC would leave no identity in any log — the broker is what creates the audit trail.

**Rollback.** Keep logging for Chapter 09.

### Exercise 7.3 — The decision follows the identity, not the IP

**Objective.** Prove access depends on the presented identity.

**Track 2 — Walkthrough.**

```bash
# same host, valid identity -> allowed
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-7f3a\n" | nc -w2 10.60.1.5 1502 && echo OK-with-identity'
# same host, no valid identity -> denied
sudo ip netns exec hmi bash -c 'printf "op-hmi WRONGTOKEN\n"    | nc -w2 10.60.1.5 1502 || echo DENIED-without-identity'
```

**Expected result.** The same source IP is allowed with a valid identity and denied without one — proof the control is identity, not address.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Only the two granted, brokered identity flows succeed.
- [ ] Every brokered session logged with its identity.
- [ ] The decision confirmed to depend on identity, not IP.
- [ ] The legacy PLC now has a per-connection audit trail.
