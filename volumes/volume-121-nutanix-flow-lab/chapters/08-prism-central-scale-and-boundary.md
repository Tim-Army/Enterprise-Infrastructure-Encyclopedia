# Chapter 08: Prism Central, Scale, and the Boundary

## Learning Objectives

- Understand the management model: Prism Central scope, per-node licensing, and the DR replication constraint.
- Show how categories carry scale: policy size is constant as the estate grows.
- State the honest boundary of hypervisor-tier enforcement.

## Hands-On Lab

### Exercise 8.1 — Prism Central scope and the DR constraint

**Objective.** Understand what Prism Central does and does not replicate.

**Track 1 — Walkthrough.** Prism Central is the single policy and visibility plane for every AHV cluster it manages; Flow Network Security is licensed **per node, for every node in a protected cluster** (partial licensing of a cluster is not a design). The operational catch: **categories and security policies do not replicate between Prism Central instances.** A disaster-recovery site with its own Prism Central starts with *no* Flow policy — it must be rebuilt or synchronized by external tooling, and that work belongs in the DR runbook, not the outage.

**Track 2 — Walkthrough.** Model the sync a second site needs — the policy exists only in this host's ruleset, and exporting it is an explicit act:

```bash
sudo nft list table bridge flow > /tmp/flow-policy-export.nft
grep -c "" /tmp/flow-policy-export.nft
```

**Expected result.** A file of a few dozen lines — the whole security posture. Nothing ships it to a second "Prism Central" automatically; if the export is not carried to the DR site, the DR site enforces nothing.

**Negative test.** Delete the export and the posture exists in exactly one place — the situation the DR runbook must never allow.

**Rollback.** Keep `/tmp/flow-policy-export.nft` for Chapter 09's restore drill.

### Exercise 8.2 — Categories carry the scale

**Objective.** Grow the web tier tenfold without touching a rule.

**Track 1 — Walkthrough.** In Prism Central, policy size is a function of tiers and flows, not VM count — a hundred web VMs categorized `AppTier: web` are one line in the policy.

**Track 2 — Walkthrough.**

```bash
RULES_BEFORE=$(sudo nft list chain bridge flow vswitch | grep -c counter)
sudo nft add element bridge flow apptier_web '{ 10.150.0.50, 10.150.0.51, 10.150.0.52, 10.150.0.53 }'
sudo nft add element bridge flow env_corp   '{ 10.150.0.50, 10.150.0.51, 10.150.0.52, 10.150.0.53 }'
RULES_AFTER=$(sudo nft list chain bridge flow vswitch | grep -c counter)
echo "rules before=$RULES_BEFORE after=$RULES_AFTER"
```

**Expected result.**

```text
rules before=7 after=7
```

Four more "web servers" joined the policy; the ruleset did not grow by one line. Address-based firewalls grow linearly with the estate — category-based policy does not.

**Negative test.** List the set (`sudo nft list set bridge flow apptier_web`) — membership grew from two to six; the *sets* absorb the scale so the *rules* never do.

**Rollback.** `sudo nft delete element bridge flow apptier_web '{ 10.150.0.50, 10.150.0.51, 10.150.0.52, 10.150.0.53 }'` and the same for `env_corp` — the placeholder addresses have no VMs.

### Exercise 8.3 — The honest boundary

**Objective.** Show what the virtual switch cannot see.

**Track 1 — Walkthrough.** Flow Network Security enforces on **AHV** only: ESXi or bare-metal workloads, cloud instances, and anything off the Nutanix fabric need a different control (the host-agent and fabric volumes of this program). And because enforcement is at the virtual switch, traffic that never crosses it — process-to-process inside one VM — is invisible.

**Track 2 — Walkthrough.** Prove the in-VM blind spot:

```bash
sudo nft reset counters table bridge flow >/dev/null
sudo ip netns exec db bash -c 'nc -z -w2 127.0.0.1 5432 && echo "db local connect OPEN"'
sudo nft list chain bridge flow vswitch | grep "counter packets [1-9]" | wc -l
```

**Expected result.**

```text
db local connect OPEN
0
```

The loopback connection succeeded and **no counter moved** — the virtual switch never saw it. In-guest activity is the tier above this control; pair it with EDR or in-guest controls where that matters.

**Negative test.** Any flow between two VMs *does* move a counter — the boundary is precisely the virtual switch, no wider and no narrower.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Prism Central scope, per-node licensing, and the no-replication DR constraint understood.
- [ ] Scale proven: rules constant while categories absorb growth.
- [ ] Boundary stated: AHV only; nothing inside the guest is visible.
