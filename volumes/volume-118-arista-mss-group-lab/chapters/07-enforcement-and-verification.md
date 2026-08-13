# Chapter 07: Enforcement and Verification

## Learning Objectives

- Verify the full matrix: group flows pass, lateral denied, redirected flow inspected.
- Read group-policy denies and firewall drops.
- Confirm the decision depends on group membership, not raw address.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Run every case and confirm the outcomes.

**Track 2 — Walkthrough.**

```bash
# A: SG-Web -> SG-DB clean (via firewall)
sudo ip netns exec web bash -c 'printf "SELECT 1\n" | nc -w2 10.120.2.20 5432 && echo "A:web->db OK"'
# B: SG-Web -> SG-DB malicious (firewall drops)
sudo ip netns exec web bash -c 'printf "EXPLOIT\n" | nc -w2 10.120.2.20 5432'; echo "(B above)"
# C: SG-Mgmt -> SG-DB uncontracted (group deny)
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.2.20 5432 && echo "C:hmi->db OPEN" || echo "C:hmi->db BLOCKED"'
# D: SG-Mgmt -> SG-OT (direct group policy)
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.4.40 502 && echo "D:hmi->plc OPEN" || echo "D:hmi->plc BLOCKED"'
```

**Expected result.**

```text
A:web->db OK
(B above)                 # dropped by the firewall (macro inspection)
C:hmi->db BLOCKED         # group default-deny
D:hmi->plc OPEN
```

The clean redirected flow works, the malicious one is dropped by the firewall, the uncontracted lateral flow is denied by group policy, and the direct group flow passes.

**Negative test.** Move `hmi` into `sg_web` and watch `hmi → db` start passing (through the firewall) — proof the decision is group membership. Restore it.

**Rollback.** Restore group membership.

### Exercise 7.2 — Read denies and firewall drops

**Objective.** See the two enforcement points logged.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.2.20 5432; true'
echo "== group policy denies =="; sudo dmesg | grep -o 'MSS-DENY.*SRC=10.120.3.30.*DPT=5432' | tail -1
echo "== firewall drops =="; sudo grep -c FW-DROP /tmp/mssfw.log
```

**Expected result.** An `MSS-DENY` line for the group-denied `hmi → db`, and a firewall drop count for the malicious redirected payloads — micro (group) and macro (firewall) enforcement both visible.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 7.3 — The decision follows the group

**Objective.** Prove group membership drives the outcome.

**Track 2 — Walkthrough.**

```bash
# add a new web server to SG-Web -> it inherits the SG-Web -> SG-DB policy
sudo nft add element inet mss sg_web '{ 10.120.1.11 }'
echo "10.120.1.11 joined SG-Web and now has the SG-Web -> SG-DB policy — no rule edit"
sudo nft delete element inet mss sg_web '{ 10.120.1.11 }'
```

**Expected result.** A new endpoint joining SG-Web gains the group policy by membership — the group, not an IP list, decides.

**Rollback.** Membership restored above.

## Summary and Completion Checklist

- [ ] Group flows pass; lateral denied; redirected flow inspected.
- [ ] Group denies and firewall drops observed.
- [ ] The decision confirmed to depend on group membership.
- [ ] Micro and macro enforcement verified together.
