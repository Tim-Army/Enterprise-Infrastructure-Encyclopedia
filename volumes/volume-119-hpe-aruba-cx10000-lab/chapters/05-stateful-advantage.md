# Chapter 05: The Stateful Advantage

## Learning Objectives

- Show return traffic permitted by state, with no reverse rule.
- Show an unsolicited/invalid packet dropped that a stateless ACL would pass.
- Understand why stateful enforcement is stronger than L3/L4 ACLs.

## State closes the holes ACLs leave open

A stateless ACL fabric permits by 5-tuple in each direction; to allow a reply it must open the reverse direction too, which also lets an attacker send **unsolicited** packets on that reverse tuple. A **stateful** firewall permits the reply only because it belongs to a tracked connection, so an unsolicited packet on the "reply" ports is dropped. This chapter demonstrates both halves of that advantage.

## Hands-On Lab

### Exercise 5.1 — Return traffic works without a reverse rule

**Objective.** Confirm the db's reply reaches web though no `db → web` permit exists.

**Track 2 — Walkthrough.** The `web → db` connection carries a reply; confirm data flows both ways over the single stateful permit:

```bash
# db echoes back what web sends; the reply returns by state, not a rule
sudo ip netns exec db bash -c 'pkill -f "nc -lk -p 5432"; nohup bash -c "while true; do nc -l -p 5432 -q1 -e /bin/cat; done" >/dev/null 2>&1 &' 2>/dev/null || \
  sudo ip netns exec db bash -c 'nohup ncat -lk -p 5432 --exec /bin/cat >/dev/null 2>&1 &' 2>/dev/null || true
echo "hello" | sudo ip netns exec web nc -w2 10.130.2.20 5432
```

**Expected result.** `hello` echoes back — the reply from db reached web over the **established** state of the connection web opened, with no `db → web` rule. That is the stateful behavior the DPU provides.

**Negative test.** Delete the `established,related accept` rule and watch even the reply of a permitted connection fail — the reverse direction is carried entirely by state.

```bash
h=$(sudo nft -a list chain inet cx forward | awk '/ct state established/{print $NF; exit}')
sudo nft delete rule inet cx forward handle "$h"
echo "hello" | sudo ip netns exec web nc -w2 10.130.2.20 5432 || echo "reply BLOCKED without state rule"
sudo nft insert rule inet cx forward index 0 ct state established,related accept   # restore
```

**Rollback.** State rule restored above.

### Exercise 5.2 — Unsolicited traffic on the reply tuple is dropped

**Objective.** Show a packet that a stateless "allow the reply" rule would pass, dropped by state.

**Track 2 — Walkthrough.** Have db try to *initiate* to web on the same ports the replies use — a stateless reverse-allow would permit it, but state does not:

```bash
sudo ip netns exec db bash -c 'nc -z -w2 10.130.1.10 5432 && echo "db->web OPEN" || echo "db->web BLOCKED (no state)"'
```

**Expected result.** `db->web BLOCKED (no state)` — db cannot open a new connection to web, because there is no permit and no existing state; only genuine replies to web's connections are allowed. A stateless fabric that opened the reverse tuple would have permitted this.

**Negative test.** This is the exact hole stateful enforcement closes: reply-permitting without state is an inbound hole; the DPU's tracking removes it while still allowing legitimate replies.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Return traffic confirmed permitted by state, no reverse rule.
- [ ] Unsolicited traffic on the reply tuple dropped by state.
- [ ] The stateful-vs-stateless advantage understood.
- [ ] Why the DPU firewall is stronger than an ACL fabric internalized.
