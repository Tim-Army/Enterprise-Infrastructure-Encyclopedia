# Chapter 06: The Ransomware Kill Switch

## Learning Objectives

- Sever all east-west traffic instantly with a single action.
- Confirm even the sanctioned flow is cut during a kill-switch event.
- Restore normal policy after containment.

## One switch, total containment

Even with least-privilege east-west policy, an incident may call for **cutting everything** — instantly isolating every device from every other while responders work. Airgap provides a **ransomware kill switch** that does exactly this with one action, and because the enforcement point already brokers all east-west, the switch is immediate and total. This chapter builds and exercises the switch, then restores normal policy.

## Hands-On Lab

### Exercise 6.1 — Throw the kill switch

**Objective.** Sever all east-west traffic at once.

**Track 1 — Walkthrough.** In Airgap, the kill switch is a single control that drops all east-west at the enforcement point across the protected VLAN; north-south management access can be preserved so responders keep working.

**Track 2 — Walkthrough.** Insert a top-priority drop for all east-west, atomically:

```bash
# save the current policy so it can be restored
sudo nft list chain inet airgap forward > /tmp/airgap-policy.txt
# KILL SWITCH: drop all east-west between VLAN devices, above every allow
sudo nft insert rule inet airgap forward ip saddr 10.100.1.0/24 ip daddr 10.100.1.0/24 log prefix '"KILL-SWITCH "' drop
echo "KILL SWITCH ENGAGED"
```

**Expected result.** Every east-west flow, including the sanctioned one, is now severed:

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.100.1.20 5432 && echo web->db OPEN || echo web->db CUT'
web->db CUT
```

`web → db` — the one flow that was permitted — is now cut too. During a live ransomware event, total containment beats keeping the app running.

**Negative test.** Confirm the switch caught the flow in the log:

```bash
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.20 5432; true'
sudo dmesg | grep -o 'KILL-SWITCH.*DST=10.100.1.20' | tail -1
```

A `KILL-SWITCH` log line confirms the sever is active and total.

**Cleanup.** The switch stays until you disengage it in Exercise 6.2.

### Exercise 6.2 — Disengage and restore

**Objective.** Remove the kill switch and confirm normal policy returns.

**Track 2 — Walkthrough.** Delete the kill-switch rule (the highest-priority handle) and confirm the sanctioned flow returns:

```bash
handle=$(sudo nft -a list chain inet airgap forward | awk '/KILL-SWITCH/{print $NF; exit}')
sudo nft delete rule inet airgap forward handle "$handle"
sudo ip netns exec web    bash -c 'nc -z -w2 10.100.1.20 5432 && echo web->db OPEN || echo web->db CUT'
sudo ip netns exec victim bash -c 'nc -z -w2 10.100.1.20 5432 && echo victim->db OPEN || echo victim->db BLOCKED'
```

**Expected result.**

```text
web->db OPEN
victim->db BLOCKED
```

Normal least-privilege policy is back: the sanctioned flow works, lateral movement stays blocked. The kill switch is a temporary containment lever, not a policy change.

**Negative test.** Disengaging the kill switch must restore the *prior* policy exactly — if it left east-west open, containment would end in an unsafe state. The saved policy (`/tmp/airgap-policy.txt`) is the reference to verify against.

**Cleanup.** Kill switch disengaged; normal policy restored.

## Summary and Completion Checklist

- [ ] The kill switch severed all east-west instantly, including the sanctioned flow.
- [ ] The sever confirmed in the log.
- [ ] The switch disengaged and normal least-privilege policy restored.
- [ ] The kill switch understood as a containment lever, not a policy edit.
