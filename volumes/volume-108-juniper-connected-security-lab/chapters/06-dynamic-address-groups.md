# Chapter 06: Dynamic Address Groups and Connected Security

## Learning Objectives

- Understand how Connected Security reacts to threat signals by changing group membership, not rules.
- Add a compromised host to a **quarantine** dynamic address group that a policy denies.
- Confirm quarantine takes effect without editing any policy.
- Model the same reactive containment in Track 2.

## The "Connected" in Connected Security

The zone policies of Chapter 05 are static least privilege. The **Connected Security** idea adds *reaction*: when Security Director, Policy Enforcer, or a threat feed flags a host as infected, its address is added to a **dynamic address group**, and a standing policy that denies that group instantly contains it — no rule edit, no commit. This chapter builds that reflex by hand so you can see the mechanism.

## Hands-On Lab

### Exercise 6.1 — Create a quarantine group and a standing deny

**Objective.** Add a dynamic address group `quarantine` and a policy that denies it everywhere.

**Track 1 — Walkthrough.** Define a dynamic address group (fed by a feed or by Policy Enforcer) and a top-of-context deny that references it:

```text
[edit security dynamic-address]
set address-name quarantine profile category Infected-Hosts
# a standing deny from any zone the infected host lives in, placed first
[edit security policies from-zone MGMT to-zone DB]
insert policy deny-quarantine before policy deny-mgmt-db
set policy deny-quarantine match source-address quarantine destination-address any application any
set policy deny-quarantine then deny
commit
```

**Expected result.**

```text
srx> show security dynamic-address-group
Group: quarantine  Feed: Infected-Hosts  Members: (none yet)
```

The deny is armed but the group is empty, so nothing is contained yet.

**Negative test.** Placing `deny-quarantine` *after* a permit in the same context lets an infected host keep using an allowed flow — reactive denies must sit at the top of the policy order to pre-empt permits.

**Track 2 — Walkthrough.** Model the group as an nftables set consulted first in the chain:

```bash
sudo nft add set inet jsec quarantine '{ type ipv4_addr ; flags dynamic ; }'
sudo nft insert rule inet jsec forward ip saddr @quarantine drop
sudo nft list set inet jsec quarantine
```

**Expected result.** An empty `quarantine` set and a first-match drop rule referencing it.

**Rollback.** Keep the group and rule.

### Exercise 6.2 — Quarantine a compromised host

**Objective.** Add `hmi` to the quarantine group and watch its access disappear.

**Track 1 — Walkthrough.** Simulate the feed/Policy Enforcer flagging `hmi` (10.20.3.10) as infected by adding it to the group (via the feed API or a manual entry):

```text
srx> request security dynamic-address add-entry quarantine ip 10.20.3.10
srx> show security dynamic-address-group quarantine
Group: quarantine  Members: 10.20.3.10
```

Now `hmi → plc:502` (previously permitted) is denied because the quarantine deny is evaluated first.

**Expected result.** `hmi → plc:502` changes from permit to deny the instant the member is added — containment without a policy edit.

**Track 2 — Walkthrough.**

```bash
sudo nft add element inet jsec quarantine '{ 10.20.3.10 }'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.4.10 502 && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
```

**Expected result.** `hmi->plc BLOCKED` — the previously-legitimate flow is contained because `hmi` is now in the quarantine set, matched before the permit.

**Negative test.** Remove `hmi` from the group and its legitimate flow returns:

```bash
sudo nft delete element inet jsec quarantine '{ 10.20.3.10 }'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.20.4.10 502 && echo "hmi->plc OPEN"'
```

`hmi->plc OPEN` again — membership, not the rule, decided containment. That reversibility is the point: policy stays fixed while the response is dynamic.

**Rollback.** Leave `hmi` out of quarantine for the remaining chapters.

## Summary and Completion Checklist

- [ ] A quarantine dynamic address group and a top-of-order deny created.
- [ ] Adding a host to the group contained it without editing policy.
- [ ] Removing it restored access — reactive, reversible containment.
- [ ] The Connected Security reflex understood as membership-driven.
