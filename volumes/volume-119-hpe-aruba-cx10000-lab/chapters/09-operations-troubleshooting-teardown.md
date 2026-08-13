# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for stateful ToR segmentation.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is the stateful firewall working?"

**Track 1 — Walkthrough.** In PSM/Fabric Composer: each CX 10000's DPU has the current stateful policy, the connection tables show only sanctioned flows, telemetry is flowing, and denies are logged.

**Track 2 — Walkthrough.**

```bash
sudo nft list chain inet cx forward | grep -E "ct state|accept|drop|policy"   # stateful policy
sudo conntrack -L 2>/dev/null | grep -cE '5432|502'                            # tracked sanctioned flows
sudo dmesg | grep -c 'CX-DENY'                                                 # denies recorded
```

**Expected result.** Stateful policy with default-drop and the two permits, sanctioned flows tracked, denies recorded.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Return traffic blocked | `established,related` rule missing | `nft list chain` for the state rule |
| Legitimate flow blocked | NEW permit wrong 5-tuple | permit rules; addresses |
| Reverse direction open | a stateless reverse permit added | remove reverse permit; rely on state |
| Lateral flow permitted | a too-broad permit | permit L4 scope |
| No connections tracked | conntrack module not loaded / no traffic | `modprobe nf_conntrack`; generate traffic |
| Off-ToR server unprotected | not attached to a CX 10000 | topology/coverage |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The classic stateful mistake is adding a **reverse permit** "to make replies work" — replies already work by state, and the reverse permit opens an inbound hole. Rely on `established,related`, not a mirror rule.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table inet cx 2>/dev/null
for ns in web db hmi plc; do sudo ip netns del $ns 2>/dev/null; done
for b in r1 r2 r3 r4; do sudo ip link del $b 2>/dev/null; done
echo "teardown complete"
```

**Expected result.** Policy table, namespaces, and bridges removed.

**Negative test.** Leaving the `cx` table behind keeps enforcing on the host; remove it too.

**Rollback.** This is the cleanup.

## Operational lessons for production

- **Stateful east-west in the fabric.** The DPU firewalls the rack at line rate — no hairpin, connection-tracked.
- **Rely on state, not reverse rules.** Replies flow by `established`; a reverse permit is a hole.
- **Per-flow telemetry comes with it.** The DPU sees every east-west connection inline.
- **Scale with the fabric.** A DPU per ToR; no central firewall bottleneck.
- **Stateful DPU plus stateless fabric plus host L7.** Layer the models for speed, statefulness, and depth.
- **Off-ToR needs complementary controls.** Pair with host/cloud controls (Volumes XCIII–CXVI) for servers not behind a CX 10000.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Stateful enforcement and the no-reverse-rule rule internalized.
- [ ] Track 2 table, namespaces, and bridges removed.
