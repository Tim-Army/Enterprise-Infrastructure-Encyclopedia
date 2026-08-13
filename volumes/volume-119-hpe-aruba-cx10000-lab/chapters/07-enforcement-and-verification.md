# Chapter 07: Enforcement and Verification

## Learning Objectives

- Verify the full matrix: permitted flows work with stateful returns, lateral and unsolicited denied.
- Confirm the connection table and deny log tell a consistent story.
- Confirm the stateful behavior matches what the DPU would enforce.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Run every case and confirm the outcomes.

**Track 2 — Walkthrough.**

```bash
# A: permitted web -> db (with stateful reply)
sudo ip netns exec web bash -c 'nc -z -w2 10.130.2.20 5432 && echo "A:web->db OPEN" || echo "A:web->db BLOCKED"'
# B: lateral hmi -> db (default deny)
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.2.20 5432 && echo "B:hmi->db OPEN" || echo "B:hmi->db BLOCKED"'
# C: permitted hmi -> plc
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.4.40 502  && echo "C:hmi->plc OPEN" || echo "C:hmi->plc BLOCKED"'
# D: unsolicited db -> web (no state, no permit)
sudo ip netns exec db  bash -c 'nc -z -w2 10.130.1.10 5432 && echo "D:db->web OPEN" || echo "D:db->web BLOCKED"'
```

**Expected result.**

```text
A:web->db OPEN
B:hmi->db BLOCKED
C:hmi->plc OPEN
D:db->web BLOCKED
```

The two permitted flows work; the lateral flow and the unsolicited reverse flow are both denied — the latter is the stateful advantage over an ACL fabric.

**Negative test.** Add a stateless-style reverse permit (`db → web:5432 accept`) and watch D start passing — proof that stateful enforcement, not a reverse ACL, is what keeps the reverse direction closed. Remove it afterward.

**Rollback.** Remove any reverse permit added.

### Exercise 7.2 — Connection table and deny log agree

**Objective.** Cross-check the two views.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -w2 10.130.2.20 5432 </dev/null' & sleep 1
echo "== permitted (connection table) =="; sudo conntrack -L 2>/dev/null | grep -m1 5432
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.2.20 5432; true'
echo "== denied (log) =="; sudo dmesg | grep -o 'CX-DENY.*SRC=10.130.3.30.*DPT=5432' | tail -1
```

**Expected result.** The permitted `web → db` appears as a tracked connection and the denied `hmi → db` appears in the log — enforcement and telemetry agree.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 7.3 — Confirm no hairpin

**Objective.** Note that enforcement is inline at the ToR, not hair-pinned to a firewall.

**Track 1 & 2 — Walkthrough.** On the real CX 10000, the stateful policy is applied by the DPU as traffic crosses the switch — the flow never leaves the ToR to reach a separate firewall. On Track 2 the enforcing host is the routing point, modeling the same inline position.

```bash
echo "east-west is firewalled at the ToR/DPU — no hairpin to an external firewall"
```

**Expected result.** A confirmation that stateful east-west policy is enforced in the switch itself, the architectural benefit of the DPU.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Permitted flows work with stateful returns; lateral and unsolicited denied.
- [ ] Connection table and deny log consistent.
- [ ] Inline (no-hairpin) enforcement understood.
- [ ] The stateful firewall verified end to end.
