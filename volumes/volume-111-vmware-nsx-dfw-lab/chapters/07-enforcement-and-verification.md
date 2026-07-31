# Chapter 07: Enforcement and Verification

## Learning Objectives

- Read DFW rule hit counts and per-vNIC programmed rules.
- Correlate a dropped flow with a DFW log.
- Confirm the decision depends on group membership (tag), not IP.

## Hands-On Lab

### Exercise 7.1 — Rule hits and programmed rules

**Objective.** See the DFW account for permits and drops.

**Track 1 — Walkthrough.**

```text
nsx> GET .../security-policies/microseg/rules/web-to-db/statistics
     hit_count: 6   (packets allowed)
nsx> GET .../default-layer3-section/rules/default-rule/statistics
     hit_count: 3   (the hmi->db drops)
esxi> vsipioctl getrules -f <db-vnic-filter>    # rules actually programmed at db's vNIC
```

**Expected result.** Non-zero hits on `web-to-db` and on the default Drop rule; the db vNIC shows the allow-from-Web rule and the drop default. Zero hits during an active test means the host is not enforcing (transport-node prep) — DFW hit counts are the ground truth.

**Track 2 — Walkthrough.** Add counters to db's ingress rules and read them:

```bash
sudo ip netns exec db nft add rule inet vnic input ip saddr @g_web tcp dport 5432 counter accept 2>/dev/null || true
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 5432; true'
sudo ip netns exec db nft list chain inet vnic input | grep -E "counter|policy drop"
```

**Expected result.** The drop policy counter increments for the `hmi → db` attempt; the accept counter increments for `web → db`.

**Cleanup.** None.

### Exercise 7.2 — Correlate the drop in a DFW log

**Objective.** Find the dropped flow in the log.

**Track 1 — Walkthrough.** Enable logging on the default (or a specific deny) rule; drops appear in the DFW log (`/var/log/dfwpktlogs.log` on the host, or the NSX log view):

```text
esxi> tail -f /var/log/dfwpktlogs.log | grep 10.50.1.30
      ... DROP ... 10.50.1.30/.. -> 10.50.1.20/5432 ... rule <default>
```

**Expected result.** A DROP entry naming source (hmi), destination db:5432, and the rule — the record that proves the vNIC filter fired.

**Track 2 — Walkthrough.** Log drops at db's vNIC:

```bash
sudo ip netns exec db nft insert rule inet vnic input ip saddr 10.50.1.30 tcp dport 5432 log prefix '"DFW-DROP "' drop
sudo ip netns exec hmi bash -c 'nc -z -w2 10.50.1.20 5432; true'
sudo dmesg | grep -o 'DFW-DROP.*SRC=10.50.1.30.*DPT=5432' | tail -1
```

**Expected result.** A `DFW-DROP` line naming source 10.50.1.30 to port 5432.

**Negative test.** A rule without logging enabled produces no entry — enable logging on denies during a rollout so a working policy is distinguishable from a broken path.

**Cleanup.** Keep logging for Chapter 09.

### Exercise 7.3 — The decision follows the tag

**Objective.** Prove membership (tag), not IP, decides.

**Track 1 — Walkthrough.** Remove the `role=web` tag from the web VM and watch `web → db` start failing — the DFW rule references the `Web` group, and web is no longer a member. Re-tag to restore.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec db nft delete element inet vnic g_web '{ 10.50.1.10 }'
sudo ip netns exec web bash -c 'nc -z -w2 10.50.1.20 5432 && echo web->db OPEN || echo web->db BLOCKED'
sudo ip netns exec db nft add element inet vnic g_web '{ 10.50.1.10 }'
```

**Expected result.** After removing web from `g_web`, `web → db` is `BLOCKED`; re-adding restores it. The rule never changed — only group membership did.

**Cleanup.** Restore membership.

## Summary and Completion Checklist

- [ ] Rule hit counts and per-vNIC programmed rules observed.
- [ ] The dropped flow correlated in a DFW log.
- [ ] The decision confirmed to depend on tag-driven group membership, not IP.
- [ ] Enforcement located at the destination vNIC.
