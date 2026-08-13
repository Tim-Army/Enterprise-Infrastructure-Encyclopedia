# Chapter 04: The Flat Network and Lateral Movement

## Learning Objectives

- Confirm that, with plain routing, any host reaches the legacy PLC and the database.
- Demonstrate an attacker reaching the unauthenticated PLC — the OT nightmare.
- Name the only two flows that should exist, expressed as identity grants.

## The brownfield problem, made concrete

Before any broker, the estate is a flat routed network: the database answers anyone who can reach 5432, and — worse — the **legacy PLC answers anyone who can reach 502**, with no authentication of its own. This chapter proves the exposure and captures the two flows that are actually legitimate, so the broker in Chapter 05 can permit exactly those and nothing else.

## Hands-On Lab

### Exercise 4.1 — Confirm the flat exposure

**Objective.** Show every source reaches db and plc directly.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.60.1.20 5432 && echo "web->db REACH"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.60.1.20 5432 && echo "hmi->db REACH (lateral!)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.60.9.40 502  && echo "hmi->plc REACH"'
sudo ip netns exec web bash -c 'nc -z -w2 10.60.9.40 502  && echo "web->plc REACH (should never happen!)"'
```

**Expected result.** All four REACH. Note the last one: the web tier can reach the OT controller directly — the flat network offers no protection to the legacy device.

**Negative test.** A closed port (`hmi->plc:22`) fails because the PLC runs nothing there — the PLC cannot be hardened; only an external control can protect it.

**Rollback.** None — Chapter 05 removes the direct path.

### Exercise 4.2 — Name the legitimate flows as identity grants

**Objective.** Record the two flows the brokers must allow, by identity.

**Track 1 & 2 — Walkthrough.**

```text
svc-web (the web app)      -> db:5432    brokered
op-hmi  (an operator)      -> plc:502    brokered
```

Everything else — most importantly any source to `plc:502` without the `op-hmi` identity, and `hmi -> db` — is illegitimate.

**Expected result.** A two-line, identity-based permit list; the whole segmentation is those two brokered flows.

**Negative test.** Expressing the plc rule as "10.60.1.30 may reach 502" (the operator's IP) is exactly the mistake Xage avoids — an IP can be spoofed or reassigned, and a stolen workstation keeps the grant. The grant must be to the *identity*, proven per connection.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 4.3 — Reproduce the attack on the legacy PLC

**Objective.** Show a compromised IT host reaching the OT controller.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.60.9.40 502 && echo "PIVOT: compromised web host opened plc:502"'
```

**Expected result.** `PIVOT: compromised web host opened plc:502` — an IT-side foothold reaches the OT controller directly. Chapter 05 makes the PLC reachable only through its broker, which no unauthenticated identity can pass.

**Negative test.** Re-run the legitimate `op-hmi` path — for now it also just "reaches" by IP, indistinguishable from the attack. Only identity brokering will separate them.

**Rollback.** None — Chapter 05 inserts the brokers.

## Summary and Completion Checklist

- [ ] Flat network exposes both db and the legacy plc to any source.
- [ ] The two legitimate flows named as identity grants.
- [ ] The attack on the unauthenticated PLC reproduced.
- [ ] Ready to remove the direct path and broker by identity.
