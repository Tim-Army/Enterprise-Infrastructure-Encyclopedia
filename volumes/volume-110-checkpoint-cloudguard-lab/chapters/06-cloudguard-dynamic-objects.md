# Chapter 06: CloudGuard Dynamic Objects

## Learning Objectives

- Understand how CloudGuard data-center / dynamic objects import membership from tags.
- Convert the rulebase to tag-based objects so policy follows workloads.
- Prove that re-tagging a workload changes its access without editing a rule.
- Model tag-driven membership in Track 2.

## Objects that follow the workload

The rules of Chapter 05 name static host objects. The **CloudGuard** distinction is the **data-center object** (and its on-gateway cousin, the **dynamic object**): its membership is imported from a cloud, vCenter, or Kubernetes source by **tag**, and updates automatically. Write a rule against `role=db` and any workload carrying that tag is covered — new instances included, decommissioned ones removed — with no rule edit or re-install. This is how Check Point makes a static rulebase track a dynamic estate.

## Hands-On Lab

### Exercise 6.1 — Create tag-based objects and rewrite the rules

**Objective.** Replace the static host objects in the rules with objects keyed on `role` tags.

**Track 1 — Walkthrough.** Define a CloudGuard data-center object (or dynamic object) per role, bound to the tag, then update the rules to use them:

```text
# on the gateway, dynamic objects updated from the data-center source by tag:
gw> dynamic_objects -n role_web -r 10.40.1.10 10.40.1.10 -a
gw> dynamic_objects -n role_db  -r 10.40.2.10 10.40.2.10 -a
gw> dynamic_objects -n role_hmi -r 10.40.3.10 10.40.3.10 -a
gw> dynamic_objects -n role_plc -r 10.40.4.10 10.40.4.10 -a
# rewrite the rules to use the tag objects
mgmt> mgmt_cli set access-rule name "web-to-db"  layer "Network" source role_web destination role_db --session-id "$SID"
mgmt> mgmt_cli set access-rule name "hmi-to-plc" layer "Network" source role_hmi destination role_plc --session-id "$SID"
mgmt> mgmt_cli publish --session-id "$SID"
mgmt> mgmt_cli install-policy policy-package "Standard" access true targets gw --session-id "$SID"
```

In a real CloudGuard deployment the `role_*` membership is imported from AWS/Azure/vCenter/Kubernetes tags automatically rather than set by hand.

**Expected result.** The rulebase now reads `role_web → role_db` and `role_hmi → role_plc`; enforcement is unchanged (web→db still permitted, hmi→db still dropped) but the objects are now tag-driven.

**Negative test.** Delete the static `db` host object while a rule still references it — the install fails until the rule uses the tag object; migrate references before removing the old objects.

**Track 2 — Walkthrough.** Model a tag object as an nftables named set whose members come from a tag file:

```bash
sudo tee /etc/cpg/tags > /dev/null <<'EOF'
role_web 10.40.1.10
role_db  10.40.2.10
role_hmi 10.40.3.10
role_plc 10.40.4.10
EOF
sudo nft add set inet cpg role_web '{ type ipv4_addr ; elements = { 10.40.1.10 } }'
sudo nft add set inet cpg role_db  '{ type ipv4_addr ; elements = { 10.40.2.10 } }'
sudo nft flush chain inet cpg forward
sudo nft add rule inet cpg forward ip saddr @role_web ip daddr @role_db tcp dport 5432 accept
sudo nft add rule inet cpg forward ip saddr 10.40.3.10 ip daddr 10.40.2.10 log prefix '"CPG-DENY " ' drop
sudo nft add rule inet cpg forward ip saddr 10.40.0.0/16 ip daddr 10.40.0.0/16 drop
```

**Expected result.** The permit rule now matches the `role_web`/`role_db` sets — policy by tag, not by literal IP.

**Cleanup.** Keep the tag objects.

### Exercise 6.2 — Prove policy follows a re-tagged workload

**Objective.** Show that changing a workload's tag changes its access with no rule edit.

**Track 1 — Walkthrough.** Add a second web instance to the `role_web` object (as the data-center source would when a new tagged VM appears) and confirm it immediately gains web→db access; remove the `role_web` tag from the original and watch its access drop — all without touching a rule:

```text
gw> dynamic_objects -n role_web -r 10.40.1.11 10.40.1.11 -a   # new tagged web instance
```

**Expected result.** 10.40.1.11 can reach db:5432 the moment it joins `role_web`; a host removed from `role_web` loses that access — membership, not the rulebase, decides.

**Track 2 — Walkthrough.**

```bash
sudo nft add element inet cpg role_web '{ 10.40.1.11 }'
sudo nft get element inet cpg role_web '{ 10.40.1.11 }'
sudo nft delete element inet cpg role_web '{ 10.40.1.10 }'
sudo ip netns exec web bash -c 'nc -z -w2 10.40.2.10 5432 && echo "web->db OPEN" || echo "web->db BLOCKED"'
```

**Expected result.** After removing 10.40.1.10 from `role_web`, the original web host is `BLOCKED` from db — the rule is unchanged; only the tag membership moved. Re-add it to restore access.

**Negative test.** Assume editing the rule is required to onboard a new server. It is not — that is the whole point of tag-based objects: onboarding is a tagging action, not a firewall change. Restore membership when done.

**Cleanup.** Restore `role_web` to contain 10.40.1.10 for later chapters.

## Summary and Completion Checklist

- [ ] Tag-based (data-center/dynamic) objects created per role.
- [ ] Rulebase rewritten to use tag objects; enforcement unchanged.
- [ ] Re-tagging a workload changed its access with no rule edit.
- [ ] The "policy follows the workload" property understood.
