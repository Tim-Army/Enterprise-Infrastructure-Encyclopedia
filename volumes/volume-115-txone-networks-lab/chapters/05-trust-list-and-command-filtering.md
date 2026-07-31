# Chapter 05: Trust List and Command Filtering

## Learning Objectives

- Restrict which sources may reach the PLC inline (a trust list).
- Filter which OT commands are allowed, dropping dangerous ones.
- Combine the trust list with the virtual patch for layered inline protection.

## Only trusted sources, only safe commands

Virtual patching stops a known exploit; a **trust list** stops everyone who has no business reaching the PLC at all, and **command filtering** stops dangerous operations even from a trusted source. EdgeIPS/EdgeFire do both inline. This chapter restricts the PLC to the operator and permits only safe commands.

## Hands-On Lab

### Exercise 5.1 — Trust list: only the operator may reach the PLC

**Objective.** Drop any source except the operator at the inline device.

**Track 1 — Walkthrough.** EdgeFire (or EdgeIPS policy) permits only the operator/EWS addresses toward the PLC; all other sources are dropped inline, transparently.

**Track 2 — Walkthrough.** Add a trust-list rule at the inline point so only `hmi` reaches the redirected PLC path; drop the attacker before it even hits the inspector:

```bash
sudo nft add chain ip txone filter '{ type filter hook forward priority -10 ; policy accept ; }'
sudo nft add rule ip txone filter ip daddr 10.90.2.40 tcp dport 502 ip saddr != 10.90.1.30 log prefix '"TXONE-UNTRUSTED "' drop
```

**Expected result.** The operator still reaches the PLC; the attacker is dropped as untrusted:

```bash
sudo ip netns exec hmi bash -c 'printf "READ\n" | nc -w2 10.90.2.40 502'          # trusted
sudo ip netns exec atk bash -c 'printf "READ\n" | nc -w2 10.90.2.40 502 || echo "atk DROPPED (untrusted)"'
```

```text
VALUE=50
atk DROPPED (untrusted)
```

**Negative test.** Even a *clean* (non-exploit) request from the attacker is now dropped — the trust list denies the source regardless of payload, a second independent layer from the virtual patch.

**Cleanup.** Keep the trust list.

### Exercise 5.2 — Command filtering: deny dangerous operations

**Objective.** Permit safe commands and deny dangerous ones even from a trusted source.

**Track 1 — Walkthrough.** EdgeIPS parses the OT protocol and can permit read/status commands while denying writes, firmware operations, or stop commands — protocol-aware allow-listing at the command level.

**Track 2 — Walkthrough.** Extend the inline inspector's policy: permit `READ`, deny a `STOP` control command. Append to `/etc/txone/signatures` the dangerous command as a blocked pattern, or add a command allowlist to the inspector. Here, add `STOP` as a blocked command marker:

```bash
printf 'STOP\n' | sudo tee -a /etc/txone/signatures >/dev/null
# a trusted operator READ is fine
sudo ip netns exec hmi bash -c 'printf "READ\n" | nc -w2 10.90.2.40 502'
# a dangerous STOP command is dropped inline, even from the operator
sudo ip netns exec hmi bash -c 'printf "STOP now\n" | nc -w2 10.90.2.40 502'; echo "(STOP result above)"
sudo grep -m1 "sig=STOP" /tmp/edgeips.log
```

**Expected result.**

```text
VALUE=50
(STOP result above)                      # dropped: dangerous command
VIRTUAL-PATCH DROP sig=STOP
```

The read passes; the dangerous command is blocked inline even though the source is trusted — protection at the command level, not just the source.

**Negative test.** Blocking by source alone (trust list) would let a trusted-but-compromised operator send `STOP`; command filtering is what stops the dangerous operation itself. Both layers are needed.

**Cleanup.** Keep the command filter.

## Summary and Completion Checklist

- [ ] Trust list drops untrusted sources inline, regardless of payload.
- [ ] Command filtering drops dangerous operations even from trusted sources.
- [ ] Trust list, command filter, and virtual patch layered together.
- [ ] The independence of the layers understood.
