# Chapter 07: Enforcement and Verification

## Learning Objectives

- Verify the full matrix: contracted flows pass; lateral, quarantined, and intra-EPG traffic denied.
- Read contract hit counters and denied-flow logs.
- Confirm the decision depends on EPG/attribute, not raw address.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Run every case and confirm the outcomes.

**Track 2 — Walkthrough.**

```bash
# A: contracted web -> db
sudo ip netns exec web bash -c 'nc -z -w2 10.110.2.20 5432 && echo A:web->db OPEN || echo A:web->db BLOCKED'
# B: uncontracted hmi -> db (whitelist deny)
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.2.20 5432 && echo B:hmi->db OPEN || echo B:hmi->db BLOCKED'
# C: contracted hmi -> plc
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.4.40 502  && echo C:hmi->plc OPEN || echo C:hmi->plc BLOCKED'
# D: intra-EPG db -> db2 (isolation)
sudo ip netns exec db  bash -c 'nc -z -w2 10.110.2.21 5432 && echo D:db->db2 OPEN || echo D:db->db2 ISOLATED'
```

**Expected result.**

```text
A:web->db OPEN
B:hmi->db BLOCKED
C:hmi->plc OPEN
D:db->db2 ISOLATED
```

Only the two contracted inter-EPG flows pass; the uncontracted lateral flow and the intra-EPG peer flow are denied.

**Negative test.** Quarantine `web` (add to the uSeg set) and watch even its contracted `web → db` break — the uSeg override beats the contract. Release it afterward.

**Cleanup.** Ensure `web` is not quarantined.

### Exercise 7.2 — Contract hits and denied flows

**Objective.** See the fabric account for permits and denies.

**Track 1 — Walkthrough.** The APIC shows per-contract statistics (permitted packets) and the fabric logs policy drops (contract deny / implicit deny), so you can confirm which contract carried a flow and what the whitelist dropped.

**Track 2 — Walkthrough.**

```bash
# add counters to the contract rules and read after traffic
sudo ip netns exec hmi bash -c 'nc -z -w2 10.110.2.20 5432; true'    # denied
sudo dmesg | grep -o 'ACI-DENY.*SRC=10.110.3.30.*DPT=5432' | tail -1
echo "== quarantine + intra-EPG denies =="; sudo dmesg | grep -cE 'USEG-QUARANTINE|INTRA-EPG-DENY'
```

**Expected result.** An `ACI-DENY` entry for the uncontracted `hmi → db`, plus counts for any uSeg/intra-EPG denies — the whitelist's drops are visible and attributable.

**Cleanup.** None.

### Exercise 7.3 — The decision follows the EPG, not the address

**Objective.** Prove group/attribute drives the outcome.

**Track 2 — Walkthrough.** Move a new web server into EPG-Web and it inherits the contract automatically:

```bash
sudo nft add rule inet aci forward ip saddr 10.110.1.11 ip daddr 10.110.2.20 tcp dport 5432 accept  # new web member
echo "new EPG-Web member 10.110.1.11 now has the web-db contract — no contract edit needed"
```

**Expected result.** A new endpoint joining EPG-Web gains the `web-db` contract by membership — proof the policy is by EPG, not by listing IPs. (On a real fabric, joining the EPG is enough; no rule is added by hand.)

**Cleanup.** Remove the demo rule if you added it.

## Summary and Completion Checklist

- [ ] Contracted flows pass; lateral, intra-EPG, and quarantined traffic denied.
- [ ] Contract hits and denied flows observed.
- [ ] The decision confirmed to depend on EPG/attribute membership.
- [ ] The whitelist model verified end to end.
