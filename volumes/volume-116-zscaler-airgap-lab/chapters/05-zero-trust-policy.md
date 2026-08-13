# Chapter 05: Zero-Trust East-West Policy

## Learning Objectives

- Re-permit only the single sanctioned east-west flow at the enforcement point.
- Confirm the sanctioned flow works and everything else stays blocked.
- Understand why isolation-by-default plus explicit exceptions is true zero trust.

## Connectivity is the exception

The network of one denies all east-west by default; **policy grants the exceptions**. Because the default is deny, you cannot accidentally leave a lateral path open — you only ever add the flows you intend. This chapter re-permits `web → db:5432` at the enforcement point and confirms nothing else opens.

## Hands-On Lab

### Exercise 5.1 — Permit the one sanctioned flow

**Objective.** Allow `web → db:5432` and nothing else.

**Track 1 — Walkthrough.** In Airgap policy you add an allow rule for the sanctioned flow (by device identity/group); the enforcement point begins brokering just that conversation, everything else staying isolated.

**Track 2 — Walkthrough.**

```bash
sudo nft add rule inet airgap forward ip saddr 10.100.1.10 ip daddr 10.100.1.20 tcp dport 5432 accept
sudo nft add rule inet airgap forward log prefix '"AIRGAP-DENY "' drop
sudo nft list chain inet airgap forward
```

**Expected result.** The forward chain permits exactly `web → db:5432`, accepts established/related return traffic, and logs-and-drops everything else.

**Negative test.** Note there is no `victim → db` or `hmi → db` rule — with default-deny, absent a rule they are simply blocked; you never write a deny for them. Zero trust is the *absence* of a permit, not the presence of a deny.

**Rollback.** Keep the policy.

### Exercise 5.2 — Sanctioned works, lateral stays blocked

**Objective.** Verify the matrix after re-permitting the one flow.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web    bash -c 'nc -z -w2 10.100.1.20 5432 && echo "web->db OPEN"    || echo "web->db BLOCKED"'
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.20 5432 && echo "victim->db OPEN" || echo "victim->db BLOCKED"'
sudo ip netns exec hmi    bash -c 'nc -z -w2 10.100.1.40 502  && echo "hmi->plc OPEN"   || echo "hmi->plc BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
victim->db BLOCKED
hmi->plc BLOCKED
```

The one sanctioned flow works; the worm's path to the database and every other east-west pair remain isolated. The application runs; the blast radius is zero.

**Negative test.** Compare with the flat VLAN of Chapter 03, where `victim → db` and `victim → plc` both reached — the network-of-one has closed every lateral path while keeping the app alive.

**Rollback.** Keep the policy for the kill-switch chapter.

## Summary and Completion Checklist

- [ ] Only `web → db:5432` re-permitted; everything else isolated.
- [ ] The sanctioned flow works; lateral movement stays blocked.
- [ ] Zero trust understood as isolate-by-default plus explicit exceptions.
- [ ] Ready to add the ransomware kill switch.
