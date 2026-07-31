# Chapter 05: The Flat Network and Lateral Movement

## Learning Objectives

- Confirm that tags exist but, with an empty matrix, everything is still permitted.
- Reproduce the operator-to-database lateral movement you will later deny.
- Establish the legitimate flows the matrix must preserve.

## Tags without policy are just labels

You have assigned every endpoint an SGT and the enforcer knows all four bindings — but the egress policy matrix is empty, so the default is `Permit IP`. This is the crucial teaching point: **classification is not enforcement**. A tag by itself changes nothing; only an SGACL in the matrix restricts traffic. This chapter proves the network is still flat and captures the exact lateral path to close.

## Hands-On Lab

### Exercise 5.1 — Baseline: everything reaches everything

**Objective.** Show all east-west flows succeed while the matrix is empty.

**Track 1 — Walkthrough.** From the endpoints, test the key flows (using the switch's connectivity or host tools):

```bash
# web -> db (legitimate)
web:  nc -z -w2 10.10.1.20 5432 && echo "web->db:5432 REACH"
# hmi -> db (lateral, to be denied)
hmi:  nc -z -w2 10.10.1.20 5432 && echo "hmi->db:5432 REACH (lateral!)"
# hmi -> plc (legitimate operator control)
hmi:  nc -z -w2 10.10.1.40 502  && echo "hmi->plc:502 REACH"
```

On the enforcer, confirm the default is still permit:

```bash
show cts role-based permissions
# IPv4 Role-based permissions default: Permit IP-00
```

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.10.1.20 5432 && echo web->db REACH'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 5432 && echo hmi->db REACH (lateral!)'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.40 502  && echo hmi->plc REACH'
```

**Expected result.** All three REACH. The forward chain policy is still `accept`; classification is in place but nothing is enforced.

**Negative test.** A flow to a closed port fails regardless of tags — `hmi -> db:502` is refused because nothing listens there, not because of policy. Distinguish "no service" from "denied by policy"; only the latter is segmentation.

**Cleanup.** None.

### Exercise 5.2 — Name the legitimate flows

**Objective.** Write down the flows the matrix must keep open, so tightening does not cause an outage.

**Track 1 & 2 — Walkthrough.** The permit list for this estate:

```text
WEB (10) -> DB  (20) : tcp 5432     application to database
HMI (30) -> PLC (40) : tcp 502      operator to controller
<admin>  -> all      : tcp 22       management (out of band, not tagged here)
```

Everything else east-west — most importantly `HMI (30) -> DB (20)` — is illegitimate and will be denied by the matrix.

**Expected result.** A two-line permit list. The whole segmentation is the statement "only these two flows, plus management."

**Negative test.** Express the WEB→DB rule by IP instead of by SGT and note the fragility: the moment DB scales to a second address or moves VLAN, an IP rule breaks while `WEB → DB` by tag keeps working. Tags are why the policy survives change.

**Cleanup.** None.

### Exercise 5.3 — Reproduce the lateral movement

**Objective.** Demonstrate the compromised operator pivoting to the database — the attack the matrix stops.

**Track 1 & 2 — Walkthrough.** Simulate a foothold on `hmi` reaching the database and issuing a query probe:

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.10.1.20 5432 && echo "PIVOT: hmi opened db:5432"'
```

**Expected result.** `PIVOT: hmi opened db:5432` — with tags assigned but no SGACL, HMI still reaches DB. The tag records *what* HMI is; only the matrix will act on it.

**Negative test.** Re-run `web -> db:5432`; it also succeeds. Until the matrix distinguishes the two sources, the enforcer treats the app and the operator identically — which is the whole problem.

**Cleanup.** None — Chapter 06 authors the matrix, Chapter 07 proves enforcement.

## Summary and Completion Checklist

- [ ] All east-west flows reach while the matrix is empty.
- [ ] The two legitimate flows named (WEB→DB:5432, HMI→PLC:502).
- [ ] The HMI→DB lateral movement reproduced.
- [ ] Classification-is-not-enforcement understood.
