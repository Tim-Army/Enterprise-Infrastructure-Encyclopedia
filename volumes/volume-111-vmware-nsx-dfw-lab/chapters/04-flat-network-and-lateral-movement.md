# Chapter 04: The Flat Network and Lateral Movement

## Learning Objectives

- Confirm the default DFW allows everything, so the estate starts flat.
- Demonstrate the operator-to-database lateral movement across one subnet.
- Name the legitimate flows the rulebase must preserve.

## The flat starting point is the default

A freshly-prepared DFW ships with a **default rule of Allow** — every VM can talk to every VM, including same-subnet peers. That is the flat network the series begins from, and because all four workloads share one subnet with no gateway, it is also the case the earlier volumes could not segment. This chapter proves the flatness and captures the lateral path.

## Hands-On Lab

### Exercise 4.1 — Confirm the flat network

**Objective.** Show all east-west flows succeed with the default Allow.

**Track 1 — Walkthrough.** Confirm the DFW default rule is Allow, then test:

```text
nsx> GET /policy/api/v1/infra/domains/default/security-policies/default-layer3-section
     rules[].action: ALLOW    (default)
# from hmi: nc db 5432  -> connects (lateral!)
# from web: nc db 5432  -> connects (legitimate)
# from hmi: nc plc 502  -> connects (legitimate)
```

**Track 2 — Walkthrough.** With no per-namespace rules yet, the shared bridge forwards everything:

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.50.1.20 5432 && echo "web->db REACH"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 5432 && echo "hmi->db REACH (lateral!)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.40 502  && echo "hmi->plc REACH"'
```

**Expected result.** All three flows REACH. The `hmi->db` connection — between two VMs on the same subnet — is the lateral movement a distributed firewall will stop.

**Negative test.** A flow to a closed port (`hmi->db:502`) fails because nothing listens, not because of policy. Distinguish "no service" from "denied."

**Cleanup.** None — the default is left Allow until Chapter 05, where the default becomes Drop.

### Exercise 4.2 — Name the legitimate flows

**Objective.** Record the permit list so tightening does not cause an outage.

**Track 1 & 2 — Walkthrough.**

```text
Web (role=web)       -> Database (role=db)  : tcp 5432
Operators (role=hmi) -> OT (role=plc)       : tcp 502
```

Everything else east-west — most importantly `Operators -> Database` (hmi -> db) — is illegitimate.

**Expected result.** A two-line permit list; the whole segmentation is those two flows plus a Drop default.

**Negative test.** Write the Web→Database rule against the db IP and note it breaks if db is redeployed with a new address; a rule against the `Database` group (resolved by tag) survives redeploys — the point of dynamic groups.

**Cleanup.** None.

### Exercise 4.3 — Reproduce the lateral movement

**Objective.** Show the compromised operator pivoting to the database on the same subnet.

**Track 1 & 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 5432 && echo "PIVOT: hmi opened db:5432 (same subnet)"'
```

**Expected result.** `PIVOT: hmi opened db:5432 (same subnet)` — with the default Allow, the operator reaches the database directly, no gateway involved. Chapter 05 denies exactly this at the database's vNIC.

**Negative test.** Re-run `web->db`; it also succeeds. Until the DFW distinguishes the sources, the workloads are mutually reachable.

**Cleanup.** None — Chapter 05 authors the DFW rulebase.

## Summary and Completion Checklist

- [ ] The default Allow leaves the network flat.
- [ ] The two legitimate flows named (Web→Database:5432, Operators→OT:502).
- [ ] The same-subnet hmi→db lateral movement reproduced.
- [ ] Ready to author DFW rules with a Drop default.
