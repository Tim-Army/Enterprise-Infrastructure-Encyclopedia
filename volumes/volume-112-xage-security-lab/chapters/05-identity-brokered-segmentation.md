# Chapter 05: Identity-Brokered Segmentation

## Learning Objectives

- Remove the direct path to the assets so they are reachable only through a broker.
- Stand up an identity-checking broker in front of the PLC (and the database).
- Prove a valid identity is brokered through and an invalid one is denied.
- Understand why this protects a device that has no security of its own.

## Remove the path, insert the broker

Xage's enforcement is two moves: **eliminate any direct route** to the asset, and **route all access through an enforcement point** that authenticates the identity and, only then, proxies the connection. This chapter builds both on Track 2 — nftables makes the PLC reachable only from the broker, and a small broker forwards to the PLC only for a valid, granted identity.

## Hands-On Lab

### Exercise 5.1 — Cut the direct path to the assets

**Objective.** Make plc reachable only from the broker, not from IT directly.

**Track 1 — Walkthrough.** The Xage enforcement node is placed as the **only** route into the OT cell; the cell has no other path. Access from IT terminates on the node, which brokers onward.

**Track 2 — Walkthrough.** Run the broker in a dedicated namespace attached to both segments, and drop any PLC traffic that does not come from the broker:

```bash
# broker namespace bridged to both IT and OT
sudo ip netns add broker
sudo ip link add br-it type veth peer name br-it-b; sudo ip link set br-it-b master it up; sudo ip link set br-it netns broker
sudo ip link add br-ot type veth peer name br-ot-b; sudo ip link set br-ot-b master ot up; sudo ip link set br-ot netns broker
sudo ip netns exec broker ip addr add 10.60.1.5/24 dev br-it
sudo ip netns exec broker ip addr add 10.60.9.5/24 dev br-ot
sudo ip netns exec broker ip link set br-it up; sudo ip netns exec broker ip link set br-ot up; sudo ip netns exec broker ip link set lo up
# PLC accepts 502 ONLY from the broker's OT-side address
sudo ip netns exec plc nft -f - <<'EOF'
table inet ot { chain input { type filter hook input priority 0 ; policy drop ;
  ct state established,related accept
  iif "lo" accept
  ip saddr 10.60.9.5 tcp dport 502 accept
} }
EOF
# stop the host from routing IT straight into the OT cell
sudo nft add table inet xage
sudo nft add chain inet xage forward '{ type filter hook forward priority -10 ; policy accept ; }'
sudo nft add rule inet xage forward ip daddr 10.60.9.40 ip saddr != 10.60.9.5 drop
```

**Expected result.**

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.60.9.40 502 || echo "web->plc direct BLOCKED"'
web->plc direct BLOCKED
```

The direct path to the PLC is gone; only the broker's address may reach it.

**Negative test.** `hmi -> plc:502` directly now also fails — good: *no one* reaches the PLC directly anymore, not even the legitimate operator. Access must go through the broker (next step).

**Rollback.** Keep the isolation.

### Exercise 5.2 — Broker by identity

**Objective.** Forward to the PLC only for a valid, granted identity.

**Track 2 — Walkthrough.** Run a broker that reads the caller's identity token, checks it against the policy, and only then proxies to the asset. A minimal broker script:

```bash
sudo tee /usr/local/bin/xbroker >/dev/null <<'SH'
#!/bin/bash
# usage: xbroker <listen-port> <asset-ip> <asset-port> <grant-key>
read -r ident token          # caller sends: "<identity> <token>"
grep -q "^$ident  *$token$" /etc/xage/identities || { echo "DENY: bad identity"; exit 1; }
grep -q "^$ident  *$4$" /etc/xage/policy 2>/dev/null || true
awk -v i="$ident" -v a="$2" -v p="$3" '$1==i && $2==a && $3==p{f=1} END{exit !f}' /etc/xage/policy \
  || { echo "DENY: no grant"; exit 1; }
exec socat - TCP:"$2":"$3"
SH
sudo chmod +x /usr/local/bin/xbroker
# broker listens for op-hmi -> plc on 1502, brokering to 10.60.9.40:502
sudo ip netns exec broker bash -c 'nohup socat TCP-LISTEN:1502,reuseaddr,fork \
  EXEC:"/usr/local/bin/xbroker 1502 10.60.9.40 502",pty >/tmp/xbroker.log 2>&1 &'
```

Now the operator connects **through the broker** with its identity:

```bash
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-7f3a\n" | nc -w2 10.60.1.5 1502 && echo "op-hmi brokered to plc:502 OK"'
```

**Expected result.** `op-hmi brokered to plc:502 OK` — the operator's proven identity is brokered through to the PLC; the connection is proxied, never direct.

**Negative test.** An attacker with no/invalid identity is denied at the broker:

```bash
sudo ip netns exec web bash -c 'printf "attacker NOPE\n" | nc -w2 10.60.1.5 1502'
DENY: bad identity
```

The legacy PLC — which has no authentication of its own — is now protected by the broker's identity check.

**Rollback.** Keep the broker; Chapter 06 hardens and generalizes it.

## Summary and Completion Checklist

- [ ] Direct path to the PLC removed; only the broker may reach it.
- [ ] A broker forwards to the asset only for a valid, granted identity.
- [ ] A valid identity brokered through; an invalid one denied.
- [ ] The legacy device protected without changing the device.
