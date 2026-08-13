# Chapter 07: Enforcement and Verification

## Learning Objectives

- Run the full matrix and confirm every outcome.
- Prove the category-driven property: a new VM's policy is decided by categorization alone.
- Confirm counters and outcomes tell one consistent story.

## Hands-On Lab

### Exercise 7.1 — The full matrix

**Objective.** Every flow, one table.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.20 5432 && echo "web->db  OPEN"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.40 502  && echo "hmi->plc OPEN"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 || echo "hmi->db  DENIED"'
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.40 502  || echo "web->plc DENIED"'
sudo ip netns exec db  bash -c 'nc -z -w2 10.150.0.40 502  || echo "db->plc  DENIED"'
sudo ip netns exec plc bash -c 'nc -z -w2 10.150.0.20 5432 || echo "plc->db  DENIED"'
```

**Expected result.**

| Flow | Outcome | Decided by |
|:---|:---|:---|
| web → db:5432 | OPEN | application policy |
| hmi → plc:502 | OPEN | application policy |
| hmi → db:5432 | DENIED | isolation (corp↔ot) |
| web → plc:502 | DENIED | isolation (corp↔ot) |
| db → plc:502 | DENIED | isolation (corp↔ot) |
| plc → db:5432 | DENIED | isolation (corp↔ot) |

**Negative test.** Unsolicited traffic *toward* a secured tier from within its own environment — `sudo ip netns exec db bash -c 'nc -z -w2 10.150.0.10 22 || echo "db->web DENIED"'` — dies at the default deny: no permit, no path.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 7.2 — The category-driven property

**Objective.** Add a second web server and show its policy is decided entirely by categorization — zero rule edits.

**Track 1 — Walkthrough.** Clone the web VM; the clone starts uncategorized (no policy applies it to the secured app). Assign `AppTier: web` and `Environment: corp` in Prism Central and it inherits the web tier's permits instantly.

**Track 2 — Walkthrough.**

```bash
mkvm() { sudo ip netns add $1; sudo ip link add $1-eth type veth peer name $1-br
  sudo ip link set $1-br master ahv0 up; sudo ip link set $1-eth netns $1
  sudo ip netns exec $1 ip addr add $2/24 dev $1-eth
  sudo ip netns exec $1 ip link set $1-eth up; sudo ip netns exec $1 ip link set lo up; }
mkvm web2 10.150.0.11
sudo ip netns exec web2 bash -c 'nc -z -w2 10.150.0.20 5432 || echo "web2->db DENIED (uncategorized)"'
sudo nft add element bridge flow apptier_web '{ 10.150.0.11 }'
sudo nft add element bridge flow env_corp   '{ 10.150.0.11 }'
sudo ip netns exec web2 bash -c 'nc -z -w2 10.150.0.20 5432 && echo "web2->db OPEN (categorized)"'
```

**Expected result.**

```text
web2->db DENIED (uncategorized)
web2->db OPEN (categorized)
```

Not one rule changed. Membership decided everything — the property that lets one policy govern a hundred web servers.

**Negative test.** Remove the category (`sudo nft delete element bridge flow apptier_web '{ 10.150.0.11 }'`) and the permit vanishes as instantly as it arrived. Re-add it for the teardown drills.

**Rollback.** `web2` persists until Chapter 09.

### Exercise 7.3 — Telemetry consistency

**Objective.** Confirm the counters and the observed outcomes agree.

**Track 1 — Walkthrough.** In Prism Central the policy view shows hit counts on permits and blocked-flow entries for denies; Security Central (SaaS) aggregates the same story across clusters.

**Track 2 — Walkthrough.**

```bash
sudo nft list chain bridge flow vswitch | grep counter
```

**Expected result.** Non-zero counters on: both isolation drops (the lateral attempts), both application permits (the sanctioned flows), and the final default-deny bucket (the in-environment unsolicited probe) — every observed outcome has a matching counter, and no counter contradicts an outcome.

**Negative test.** `sudo nft reset counters table bridge flow >/dev/null`, run only the sanctioned pair, re-list: only the two permit counters advance. Quiet policy, quiet counters.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Full matrix verified — six flows, every outcome explained by one policy layer.
- [ ] Category-driven property proven with web2: membership, not rules, decides policy.
- [ ] Telemetry agrees with enforcement.
