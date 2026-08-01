# Chapter 06: Intra-EPG Isolation

## Learning Objectives

- Deny traffic *within* an EPG so members cannot talk to each other.
- Understand why intra-EPG isolation closes the last lateral path inside a group.
- Combine intra-EPG isolation with contracts and uSeg for full micro-segmentation.

## Even peers in a group should not trust each other

Contracts govern traffic *between* EPGs, but by default members of the *same* EPG can talk freely — a lateral path if one is compromised. **Intra-EPG isolation** denies traffic between members of an EPG (optionally with an intra-EPG contract for the few flows that are legitimate). For a group of database servers that never need to talk to each other, isolation removes the peer-to-peer path entirely. This chapter adds a second database endpoint and isolates the EPG.

## Hands-On Lab

### Exercise 6.1 — Add a second member and show intra-EPG reachability

**Objective.** Put a second endpoint in `EPG-DB` and show the two members can reach each other by default.

**Track 2 — Walkthrough.** Add `db2` to the EPG-DB subnet and confirm peer reachability:

```bash
sudo ip netns add db2; sudo ip link add db2-e type veth peer name db2-b
sudo ip link set db2-b master bd2 up; sudo ip link set db2-e netns db2
sudo ip netns exec db2 ip addr add 10.110.2.21/24 dev db2-e; sudo ip netns exec db2 ip link set db2-e up
sudo ip netns exec db2 ip route add default via 10.110.2.1
sudo ip netns exec db2 bash -c 'nohup nc -lk -p 5432 >/dev/null 2>&1 &'
sudo ip netns exec db bash -c 'nc -z -w2 10.110.2.21 5432 && echo db->db2 REACH (intra-EPG)'
```

**Expected result.** `db->db2 REACH (intra-EPG)` — two members of the same EPG reach each other, a lateral path if one is compromised.

**Negative test.** Contracts did not stop this — they govern *inter*-EPG traffic; intra-EPG traffic needs a separate control.

**Cleanup.** Keep db2.

### Exercise 6.2 — Enforce intra-EPG isolation

**Objective.** Deny traffic between members of EPG-DB.

**Track 1 — Walkthrough.** On the APIC, set the EPG-DB to **Intra EPG Isolation: Enforced**; members can no longer talk to each other (an intra-EPG contract can re-permit specific flows if needed).

**Track 2 — Walkthrough.** Add a rule denying intra-subnet (intra-EPG) traffic for EPG-DB:

```bash
sudo nft insert rule inet aci forward ip saddr 10.110.2.0/24 ip daddr 10.110.2.0/24 log prefix '"INTRA-EPG-DENY "' drop
sudo ip netns exec db bash -c 'nc -z -w2 10.110.2.21 5432 && echo db->db2 OPEN || echo db->db2 ISOLATED'
```

**Expected result.** `db->db2 ISOLATED` — members of EPG-DB can no longer reach each other, closing the intra-group lateral path. The `web → db` contract still works because it is inter-EPG:

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.110.2.20 5432 && echo web->db OPEN (contract intact)'
```

**Negative test.** Intra-EPG isolation without an intra-EPG contract denies *all* peer traffic; if two members legitimately must talk, add a narrow intra-EPG contract rather than disabling isolation.

**Cleanup.** Keep isolation for verification.

## Summary and Completion Checklist

- [ ] Intra-EPG reachability shown, then denied with isolation.
- [ ] The inter-EPG contract confirmed still working.
- [ ] The intra-group lateral path closed.
- [ ] Contracts + uSeg + intra-EPG isolation combined for full micro-segmentation.
