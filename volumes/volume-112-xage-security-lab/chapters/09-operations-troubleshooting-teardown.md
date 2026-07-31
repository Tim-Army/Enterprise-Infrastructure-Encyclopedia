# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for an identity-brokered estate.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is the brokering working?"

**Track 1 — Walkthrough.** In Xage: verify enforcement nodes are healthy and in the fabric, identities and their credentials are current, access policies are as intended, and the audit trail is recording brokered sessions.

**Track 2 — Walkthrough.**

```bash
cat /etc/xage/identities /etc/xage/policy          # identities and grants
sudo ip netns exec plc nft list chain inet ot input | grep -E "accept|policy"   # PLC broker-only
sudo ip netns exec broker ss -ltn | grep -E "1502|15432"                        # brokers listening
journalctl -t xbroker --no-pager | tail -3                                      # session log
```

**Expected result.** Grants correct, PLC accepting only from the broker, brokers listening, sessions logged.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Valid identity denied | token rotated / grant missing | `/etc/xage/identities`, `/etc/xage/policy` |
| Asset unreachable even via broker | isolation rule too broad / broker down | `nft list`, broker `ss -ltn` |
| Attacker still reaches asset | a direct path bypasses the broker | routing, second NIC, `forward` drop rule |
| No sessions in the log | logging not enabled on the broker | broker script `logger` lines |
| Any identity reaches any asset | grant check missing/loose | broker policy `awk` match |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The most dangerous failure is an *alternate path*: a broker that works perfectly is useless if the asset is reachable another way. Verify isolation (no direct route) first, brokering second.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
for ns in web db hmi plc broker; do sudo ip netns exec $ns nft flush ruleset 2>/dev/null; sudo ip netns del $ns 2>/dev/null; done
sudo nft delete table inet xage 2>/dev/null
sudo ip link del it 2>/dev/null ; sudo ip link del ot 2>/dev/null
sudo rm -f /usr/local/bin/xbroker ; sudo rm -rf /etc/xage
echo "teardown complete"
```

**Expected result.** Namespaces, bridges, brokers, and config removed.

**Negative test.** Leaving the broker binary or `/etc/xage` behind leaves stale identity data on the host; remove them too.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Broker by identity; never grant by IP.** Identity is the unit of policy and survives host changes.
- **Isolation and brokering are one control.** A bypass path defeats the broker; remove every alternate route.
- **Rotate credentials freely — the policy is separate.** Aggressive rotation without re-authoring segmentation.
- **Decentralize.** No central store whose breach unlocks the estate; nodes enforce locally.
- **Broker + inspect + monitor.** Pair identity brokering with an OT-protocol IPS and OT monitoring for full coverage.
- **Native + broker.** For anything the broker cannot sit in front of, pair with host or network controls (Volumes XCIII–CXI).

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Isolation-before-brokering internalized.
- [ ] Track 2 namespaces, bridges, brokers, and config removed.
