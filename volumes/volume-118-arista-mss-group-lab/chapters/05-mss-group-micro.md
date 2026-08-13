# Chapter 05: MSS-Group Micro-Segmentation

## Learning Objectives

- Apply group-to-group policy that permits only the two flows.
- Rely on default-deny between groups, enforced in the fabric.
- Build the equivalent group-policy ruleset in Track 2.

## Group policy at line rate

MSS-Group enforces a **default-deny between groups**, with explicit group-to-group permits enforced in the switch ASIC — no hairpin, no performance penalty. This chapter applies the two permits and denies the rest by group.

## Hands-On Lab

### Exercise 5.1 — Author the group policy

**Objective.** Permit SG-Web→SG-DB:5432 and SG-Mgmt→SG-OT:502 by group.

**Track 1 — Walkthrough.** In CloudVision/EOS you write MSS-Group policy: source group, destination group, L4 match, permit; the default between groups is deny, pushed to the switches:

```text
eos# (CloudVision) MSS-Group policy:
     SG-Web -> SG-DB permit tcp/5432
     SG-Mgmt -> SG-OT permit tcp/502
     default: deny
```

**Track 2 — Walkthrough.**

```bash
sudo nft add chain inet mss forward '{ type filter hook forward priority 0 ; policy drop ; }'
sudo nft add rule inet mss forward ct state established,related accept
sudo nft add rule inet mss forward ip saddr @sg_web  ip daddr @sg_db tcp dport 5432 accept
sudo nft add rule inet mss forward ip saddr @sg_mgmt ip daddr @sg_ot tcp dport 502  accept
sudo nft add rule inet mss forward ip saddr 10.120.0.0/16 ip daddr 10.120.0.0/16 log prefix '"MSS-DENY "' drop
sudo nft list chain inet mss forward
```

**Expected result.** The forward chain permits exactly the two group flows (matched by set membership) and denies everything else between groups.

**Negative test.** A permit with no L4 match (any port) would open every port between the groups — scope each group permit to its ports.

**Rollback.** Keep the policy.

### Exercise 5.2 — The group policy holds

**Objective.** Confirm group flows work and the lateral flow is denied.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.120.2.20 5432 && echo "web->db OPEN"  || echo "web->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.2.20 5432 && echo "hmi->db OPEN"  || echo "hmi->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.120.4.40 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
hmi->plc OPEN
```

The two group flows pass; `SG-Mgmt → SG-DB` (hmi → db) is denied by default — group policy, enforced in the fabric.

**Negative test.** Because the permit matches the `sg_web` set, adding a new web server to `sg_web` grants it the policy automatically — group membership, not an IP list, decides.

**Rollback.** Keep the policy for the macro-segmentation chapter.

## Summary and Completion Checklist

- [ ] Group policy permits only the two flows; default-deny between groups.
- [ ] Group flows pass; the lateral flow denied.
- [ ] Policy matches by group membership, not IP.
- [ ] Ready to add MSS macro firewall-redirect.
