# Chapter 06: Legacy OT and the Decentralized Fabric

## Learning Objectives

- Broker the database with the `svc-web` identity, completing the estate.
- Understand why the decentralized fabric has no single point of compromise.
- See that policy travels with the enforcement node, so it holds even if the manager is offline.

## Hands-On Lab

### Exercise 6.1 — Broker the database by service identity

**Objective.** Make db reachable only by `svc-web`, mirroring the PLC protection for the IT tier.

**Track 2 — Walkthrough.** Restrict the database to the broker and run a second broker instance for `svc-web → db`:

```bash
sudo ip netns exec db nft -f - <<'EOF'
table inet it { chain input { type filter hook input priority 0 ; policy drop ;
  ct state established,related accept
  iif "lo" accept
  ip saddr 10.60.1.5 tcp dport 5432 accept
} }
EOF
sudo nft add rule inet xage forward ip daddr 10.60.1.20 ip saddr != 10.60.1.5 drop
sudo ip netns exec broker bash -c 'nohup socat TCP-LISTEN:15432,reuseaddr,fork \
  EXEC:"/usr/local/bin/xbroker 15432 10.60.1.20 5432",pty >/tmp/xbroker-db.log 2>&1 &'
```

The web app connects through the broker with its service identity:

```bash
sudo ip netns exec web bash -c 'printf "svc-web TOKEN-WEB-9c21\n" | nc -w2 10.60.1.5 15432 && echo "svc-web brokered to db:5432 OK"'
```

**Expected result.** `svc-web brokered to db:5432 OK`, while a direct `web -> db:5432` is now blocked — the database, like the PLC, is reachable only through an identity-checked broker.

**Negative test.** `op-hmi` presenting its (valid) identity to the db broker is denied — there is no `op-hmi → db` grant. A valid identity is not a universal key; each grant is specific.

```bash
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-7f3a\n" | nc -w2 10.60.1.5 15432'
DENY: no grant
```

**Cleanup.** Keep both brokers.

### Exercise 6.2 — Decentralized policy: no single point of compromise (design + model)

**Objective.** Understand why the fabric is resilient and how policy survives a manager outage.

**Track 1 — Walkthrough (design).** The Xage Fabric distributes identity and policy across many nodes with a tamper-resistant, replicated store; there is no central database whose breach unlocks every asset, and enforcement nodes keep enforcing the last-known policy if the manager is unreachable. Compromising one node does not yield the policy for others.

**Track 2 — Walkthrough (model).** Model "policy travels with the node" by giving the broker its own copy of the grants and showing enforcement continues when the central store is removed:

```bash
sudo cp /etc/xage/policy /etc/xage/policy.node   # the node's local replica
sudo mv /etc/xage/policy /etc/xage/policy.bak     # simulate the central manager going offline
# broker still enforces from its local replica
sudo sed -i 's#/etc/xage/policy#/etc/xage/policy.node#g' /usr/local/bin/xbroker
sudo ip netns exec hmi bash -c 'printf "op-hmi TOKEN-HMI-7f3a\n" | nc -w2 10.60.1.5 1502 && echo "still brokered with manager offline"'
sudo mv /etc/xage/policy.bak /etc/xage/policy
sudo sed -i 's#/etc/xage/policy.node#/etc/xage/policy#g' /usr/local/bin/xbroker
```

**Expected result.** `still brokered with manager offline` — enforcement continues from the node's local policy even with the central store gone. That resilience is the point of a decentralized fabric.

**Negative test.** If the broker had to call a central server for every decision, that server would be both a bottleneck and a single point of failure — the centralized model this architecture deliberately avoids.

**Cleanup.** Restore the single policy file (done above).

## Summary and Completion Checklist

- [ ] Database brokered by `svc-web`; a valid-but-ungranted identity denied.
- [ ] The decentralized, tamper-resistant fabric understood.
- [ ] Policy shown to survive a central-manager outage.
- [ ] Both assets now reachable only by identity, through brokers.
