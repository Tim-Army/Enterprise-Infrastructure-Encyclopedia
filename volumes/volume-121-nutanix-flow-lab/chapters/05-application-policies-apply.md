# Chapter 05: Applying the Application Policies

## Learning Objectives

- Move the policy from monitor to **apply**: default-deny with the two sanctioned permits.
- Verify the sanctioned flows survive and the lateral flow dies.
- Confirm the guests still hold no rules — enforcement is entirely beneath them.

## Hands-On Lab

### Exercise 5.1 — Apply the policy

**Objective.** Turn observation into enforcement.

**Track 1 — Walkthrough.** In Prism Central, open each policy and switch it from **Monitor** to **Apply**. Every AHV host now enforces: traffic to a secured tier that no rule permits is dropped at the virtual switch:

```text
pc> Network & Security > Security Policies > (each policy) > Actions > Apply
```

**Track 2 — Walkthrough.** Replace the count-only chain with an enforcing one — same category rules, `policy drop`. Connection tracking permits return traffic, and ARP must be allowed explicitly because the bridge hook sees every frame:

```bash
sudo modprobe nf_conntrack_bridge
sudo nft delete chain bridge flow monitor
sudo nft add chain bridge flow vswitch '{ type filter hook forward priority 0; policy drop; }'
sudo nft add rule bridge flow vswitch ether type arp accept
sudo nft add rule bridge flow vswitch ct state established,related accept
sudo nft add rule bridge flow vswitch ip saddr @apptier_web ip daddr @apptier_db  tcp dport 5432 counter accept
sudo nft add rule bridge flow vswitch ip saddr @apptier_hmi ip daddr @apptier_plc tcp dport 502  counter accept
sudo nft add rule bridge flow vswitch counter
```

The final bare `counter` rule counts everything that falls through to the default drop — the applied policy's deny telemetry.

**Expected result.** The `vswitch` chain enforces default-deny on all bridged traffic with exactly two permits.

**Negative test.** Attempt the policy from the wrong place: the rules exist only in the host's table — `sudo ip netns exec web nft list ruleset` still prints nothing. The guest cannot even see the policy that governs it.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 5.2 — Verify: sanctioned lives, lateral dies

**Objective.** Prove apply mode changed the estate.

**Track 2 — Walkthrough.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.20 5432 && echo "web->db  OPEN"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.40 502  && echo "hmi->plc OPEN"'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 || echo "hmi->db  DENIED"'
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.40 502  || echo "web->plc DENIED"'
```

**Expected result.**

```text
web->db  OPEN
hmi->plc OPEN
hmi->db  DENIED
web->plc DENIED
```

The two application flows work; both lateral paths are dropped at the virtual switch. The deny counter has advanced:

```bash
sudo nft list chain bridge flow vswitch | grep -A1 "502 counter" | tail -1
counter packets 4 bytes 240
```

**Negative test.** Ping between guests now also dies (`sudo ip netns exec web ping -c1 -W2 10.150.0.30` reports `0 received`) — ICMP is not in any permit, and default-deny means *default*.

**Rollback.** None — the applied policy is the estate's steady state.

## Summary and Completion Checklist

- [ ] Policies applied: default-deny with two category-driven permits.
- [ ] Sanctioned flows verified OPEN; lateral flows DENIED.
- [ ] Guests still rule-free — enforcement is invisible to the workload.
