# Chapter 03: Security Groups

## Learning Objectives

- Define the four security groups and build the group sets the fabric policy uses.
- Confirm each endpoint resolves to its group.
- Understand why group membership decouples policy from addressing.

## Groups are the unit of policy

MSS-Group policy is written between **security groups**, not addresses. A group can be populated by subnet, VLAN, interface, or learned identity; the policy then reads "SG-Web may reach SG-DB on 5432" and covers any endpoint in SG-Web. This chapter builds the four groups on Track 2 as the sets the enforcement chain references.

## Hands-On Lab

### Exercise 3.1 — Define the security groups

**Objective.** Create SG-Web, SG-DB, SG-Mgmt, SG-OT and populate them.

**Track 1 — Walkthrough.** In EOS/CloudVision you define security groups and their membership criteria (subnet/VLAN/interface/tag); the switches resolve endpoints into groups and enforce policy by group.

**Track 2 — Walkthrough.** Build an nftables set per group from the membership file:

```bash
sudo nft add table inet mss
mkset() { sudo nft add set inet mss $1 '{ type ipv4_addr ; }'; sudo nft add element inet mss $1 "{ $2 }"; }
mkset sg_web 10.120.1.10
mkset sg_db  10.120.2.20
mkset sg_mgmt 10.120.3.30
mkset sg_ot  10.120.4.40
sudo nft list set inet mss sg_web
```

**Expected result.** Four group sets, each containing its endpoint — the groups policy will reference.

**Negative test.** Two groups cannot claim the same endpoint with conflicting policy; an endpoint resolves to exactly one security group at a time.

**Cleanup.** Keep the groups.

### Exercise 3.2 — Confirm group resolution

**Objective.** Verify an endpoint maps to its group.

**Track 2 — Walkthrough.**

```bash
sudo nft get element inet mss sg_db '{ 10.120.2.20 }'
awk '$1=="10.120.3.30"{print "10.120.3.30 -> "$2}' /etc/mss/groups
```

**Expected result.** `10.120.2.20` is in `sg_db`, and the membership file confirms `10.120.3.30 → SG-Mgmt` — resolution is by group, not by a rule listing IPs.

**Negative test.** A new server added to SG-Web would inherit SG-Web's policy automatically; a policy written against IPs would not cover it — the point of group-based policy.

**Cleanup.** Keep the groups.

## Summary and Completion Checklist

- [ ] Four security groups defined and populated.
- [ ] Each endpoint resolves to its group.
- [ ] Group-decoupling-from-addressing understood.
- [ ] Groups ready for policy.
