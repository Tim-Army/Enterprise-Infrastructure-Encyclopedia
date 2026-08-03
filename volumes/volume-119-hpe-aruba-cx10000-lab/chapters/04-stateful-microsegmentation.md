# Chapter 04: Stateful Microsegmentation at the ToR

## Learning Objectives

- Apply a default-deny stateful firewall with permits for the two flows.
- Rely on connection state so return traffic needs no separate rule.
- Understand what the DPU offloads to enforce this at line rate.

## The stateful firewall in the switch

The CX 10000's DPU applies a **stateful** firewall to east-west traffic: a permit matches the **NEW** connection, and the DPU tracks it so the **return** direction is allowed by state — no mirror-image rule. This chapter builds that on Track 2 with nftables connection tracking, the same model the DPU accelerates in hardware.

## Hands-On Lab

### Exercise 4.1 — Apply the stateful policy

**Objective.** Default-deny, permit the two flows as stateful connections.

**Track 1 — Walkthrough.** In PSM you define a stateful security policy: default deny, permit `web → db` tcp/5432 and `hmi → plc` tcp/502; the DPU tracks each connection and permits its return automatically.

**Track 2 — Walkthrough.**

```bash
sudo nft add table inet cx
sudo nft add chain inet cx forward '{ type filter hook forward priority 0 ; policy drop ; }'
# stateful core: return/related traffic permitted by state
sudo nft add rule inet cx forward ct state established,related accept
sudo nft add rule inet cx forward ct state invalid drop
# permit the NEW connections for the two flows
sudo nft add rule inet cx forward ct state new ip saddr 10.130.1.10 ip daddr 10.130.2.20 tcp dport 5432 accept
sudo nft add rule inet cx forward ct state new ip saddr 10.130.3.30 ip daddr 10.130.4.40 tcp dport 502  accept
sudo nft add rule inet cx forward log prefix '"CX-DENY "' drop
sudo nft list chain inet cx forward
```

**Expected result.** The chain permits established/related by state, drops invalid, permits only the two NEW flows, and denies the rest — a stateful firewall.

**Negative test.** Note there is **no** reverse rule for `db → web` — the return traffic is permitted by `established`, not a second permit. On a stateless ACL fabric you would need both directions; the DPU's state tracking is what removes that.

**Cleanup.** Keep the policy.

### Exercise 4.2 — The stateful policy holds

**Objective.** Confirm the two flows work and the lateral flow is denied.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.130.2.20 5432 && echo "web->db OPEN"  || echo "web->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.2.20 5432 && echo "hmi->db OPEN"  || echo "hmi->db BLOCKED"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.130.4.40 502  && echo "hmi->plc OPEN" || echo "hmi->plc BLOCKED"'
```

**Expected result.**

```text
web->db OPEN
hmi->db BLOCKED
hmi->plc OPEN
```

The two flows pass (with return traffic auto-permitted by state); `hmi → db` is denied by default. This is firewall-grade east-west policy, enforced where a stateless ACL fabric would need a separate firewall.

**Cleanup.** Keep the policy for the stateful-advantage chapter.

## Summary and Completion Checklist

- [ ] Default-deny stateful firewall with two NEW-connection permits applied.
- [ ] Return traffic permitted by state, not a mirror rule.
- [ ] The two flows pass; the lateral flow denied.
- [ ] What the DPU offloads (state tracking at line rate) understood.
