# Chapter 06: Enforcing via Integration

## Learning Objectives

- Push the derived policy to the enforcer (the "integrated firewall/NAC").
- Confirm the two baseline flows pass and the lateral flow is denied.
- Understand that Claroty produces the policy; the enforcer applies it.

## Claroty decides; the enforcer blocks

Because xDome is passive, it does not drop packets itself — it **integrates** with an enforcer and pushes the zone policy there. In Track 2 the enforcer is the host's nftables `forward` chain (standing in for the integrated firewall or NAC). This chapter compiles the derived zone policy into enforcer rules and applies them, closing the loop from observation to enforcement.

## Hands-On Lab

### Exercise 6.1 — Compile and push the policy to the enforcer

**Objective.** Turn the zone policy into firewall rules and apply them, default-deny.

**Track 1 — Walkthrough.** xDome pushes the policy to the integrated firewall/NAC — as firewall rules, SGT assignments, or NAC authorization profiles — which then enforces it. Claroty monitors that the enforcement matches the intended policy.

**Track 2 — Walkthrough.** Compile the zone policy back to concrete allow rules (resolving zones to the asset addresses) and install them with a default drop:

```bash
sudo nft add table inet xdome
sudo nft add chain inet xdome forward '{ type filter hook forward priority 0 ; policy drop ; }'
sudo nft add rule inet xdome forward ct state established,related accept
# one accept per sanctioned baseline flow
while read src arrow dstport; do
  dst="${dstport%%:*}"; port="${dstport##*:}"
  sudo nft add rule inet xdome forward ip saddr "$src" ip daddr "$dst" tcp dport "$port" accept
done < <(sed 's/ -> / /; s/:/ :/' /tmp/baseline.txt | awk '{print $1" -> "$2":"$4}')
# log the denies so deviations are visible (Chapter 07)
sudo nft add rule inet xdome forward ip saddr 10.70.0.0/16 ip daddr 10.70.0.0/16 log prefix '"XDOME-DENY "' drop
sudo nft list chain inet xdome forward
```

**Expected result.** The forward chain permits exactly the two sanctioned flows and drops (with logging) everything else — the derived policy, now enforced.

**Negative test.** Installing the policy without a default drop would leave the network flat regardless of the allow rules — enforcement is allow-list + default-deny, not just the allows. The default drop is the segmentation.

**Rollback.** Keep the enforced policy.

### Exercise 6.2 — Verify baseline flows pass and the lateral flow is denied

**Objective.** Confirm the observe-then-enforce loop worked.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.70.2.20 5432 && echo "web->db OPEN" || echo "web->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.70.4.40 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.70.2.20 5432 && echo "hmi->db OPEN" || echo "hmi->db BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
hmi->plc OPEN
hmi->db BLOCKED
```

The two sanctioned flows pass; the lateral flow — which the curated baseline excluded — is denied by the derived policy. Observation became enforcement.

**Negative test.** Had you enforced the *raw* baseline from Chapter 04, `hmi->db` would be OPEN — the curation step is what makes the enforced policy safe.

**Rollback.** Keep the enforcement for Chapter 07.

## Summary and Completion Checklist

- [ ] The derived zone policy compiled to enforcer rules with default-deny.
- [ ] The two baseline flows pass; the lateral flow is denied.
- [ ] The passive-decides / enforcer-blocks split understood.
- [ ] The observe-then-enforce loop closed end to end.
