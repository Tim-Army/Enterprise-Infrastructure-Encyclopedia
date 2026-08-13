# Chapter 03: The Flat Network and Lateral Movement

## Learning Objectives

- Demonstrate that with no security policy, every VM reaches every other VM.
- Walk the lateral-movement path the attacker would take.
- Confirm the guests are truly agentless — there is nothing inside a VM to configure or to kill.

## Hands-On Lab

### Exercise 3.1 — The flat reachability matrix

**Objective.** Prove the pre-policy estate is wide open.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.20 5432 && echo "web->db  OPEN (sanctioned)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.40 502  && echo "hmi->plc OPEN (sanctioned)"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 && echo "hmi->db  OPEN (lateral!)"'
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.40 502  && echo "web->plc OPEN (lateral!)"'
```

**Expected result.** All four print OPEN — the two sanctioned flows and the two lateral ones are indistinguishable to a flat network.

**Negative test.** There is nothing to test negatively yet: no control exists.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.2 — Walk the attacker's path

**Objective.** Make the lateral path concrete.

**Track 2 — Walkthrough.** The operator workstation (`hmi`) is phished. From it, the attacker reaches the database directly — a flow no business process ever needed:

```bash
sudo ip netns exec hmi bash -c 'echo "SELECT * FROM payroll;" | nc -w2 10.150.0.20 5432 && echo "exfil path exists"'
exfil path exists
```

**Expected result.** The "query" reaches the db listener. On the flat estate, compromising any VM yields the whole subnet.

**Negative test.** None — this is the problem statement the rest of the volume fixes.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.3 — Confirm the guests are agentless

**Objective.** Show no guest holds any firewall state — the enforcement this volume builds lives entirely beneath them.

**Track 2 — Walkthrough.**

```bash
for vm in web db hmi plc; do echo "== $vm =="; sudo ip netns exec $vm nft list ruleset | wc -l; done
```

**Expected result.** Every guest reports `0` — no rules, no agent. When policy arrives in Chapter 05 it will appear only in the host's `bridge` table, exactly as FNS policy exists only in the AHV host, never in the VM.

**Negative test.** Contrast with the host-agent volumes (XCIII–C): there, each workload enforced its own ruleset — protection an attacker with root in the guest could flush. Here the guest has nothing to flush.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Flat matrix proven: all four flows OPEN.
- [ ] Lateral path walked (hmi → db).
- [ ] Guests confirmed agentless — enforcement will live beneath them.
