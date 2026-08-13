# Chapter 05: The Out-of-Band Advantage

## Learning Objectives

- Show that a fully-compromised workload cannot disable its own DPU policy.
- Understand why an isolated trust domain beats a host agent an attacker can kill.
- Confirm the segmentation holds even with root on the host.

## Enforcement the attacker cannot reach

A host-agent microsegmentation product runs *on* the host — an attacker with root can stop the agent, flush its rules, or unload its module, and the segmentation is gone. The BlueField DPU enforces in a **separate trust domain**: the policy runs on the DPU's own cores, and the host CPU — even fully compromised — cannot see or change it. This chapter proves that property on Track 2 by attacking from inside the workload.

## Hands-On Lab

### Exercise 5.1 — Attack the policy from the compromised workload

**Objective.** As root inside `web`, try every way to disable the segmentation, and fail.

**Track 2 — Walkthrough.** Simulate a fully-owned `web` host trying to open its path to the PLC:

```bash
# attacker has root in the web namespace and tries to remove firewalling
sudo ip netns exec web nft flush ruleset 2>/dev/null; echo "flushed web's own ruleset"
sudo ip netns exec web nft add table inet x 2>/dev/null; sudo ip netns exec web nft add chain inet x y '{ type filter hook forward priority 0 ; policy accept ; }' 2>/dev/null
# attacker tries to reach the PLC it is not permitted to reach
sudo ip netns exec web bash -c 'nc -z -w2 10.140.0.40 502 && echo "web->plc OPEN (BROKEN)" || echo "web->plc STILL BLOCKED"'
```

**Expected result.**

```text
flushed web's own ruleset
web->plc STILL BLOCKED
```

The attacker flushed and rewrote firewall rules **in the web namespace** — and it changed nothing, because the enforcement is in `dpu-web`, a namespace `web` cannot touch. The segmentation holds on a fully-compromised host.

**Negative test.** Try to enter or edit the DPU namespace from the workload — it cannot:

```bash
sudo ip netns exec web bash -c 'ip netns list 2>/dev/null | grep dpu || echo "web cannot see the DPU namespace"'
```

`web` cannot even enumerate the DPU namespace, let alone edit its policy — the isolation is the point.

**Rollback.** None (web's stray table is harmless; it has no effect).

### Exercise 5.2 — Contrast with a host-agent model

**Objective.** See why an on-host control would have failed here.

**Track 2 — Walkthrough.** Model a host-agent by putting the enforcement *in* the workload namespace, then attack it:

```bash
# a host-agent style rule INSIDE the workload (what an on-host product would do)
sudo ip netns exec web nft add table inet agent 2>/dev/null
sudo ip netns exec web nft add chain inet agent out '{ type filter hook output priority 0 ; policy accept ; }'
sudo ip netns exec web nft add rule inet agent out ip daddr 10.140.0.40 drop   # "agent" blocks web->plc
# attacker with root simply removes the agent's rule
sudo ip netns exec web nft delete table inet agent
echo "attacker deleted the host agent's policy"
```

**Expected result.** The attacker deleted the "agent's" rule trivially — an on-host control is only as strong as the host, which a root attacker owns. The DPU's rule (Exercise 5.1) survived the same attack because it is out-of-band.

**Negative test.** This is the whole argument for DPU enforcement: identical policy, but one lives where the attacker is and one does not. Remove the stray tables when done:

```bash
sudo ip netns exec web nft flush ruleset 2>/dev/null; echo "cleaned web's namespace"
```

**Rollback.** Cleaned above; the DPU policy is untouched.

## Summary and Completion Checklist

- [ ] A root attacker in the workload could not disable the DPU policy.
- [ ] The workload cannot see or edit the DPU namespace.
- [ ] A host-agent-style rule was trivially removed by the same attacker.
- [ ] Why an isolated trust domain beats an on-host agent understood.
