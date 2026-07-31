# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for an observe-then-enforce estate.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is discovery-and-enforcement healthy?"

**Track 1 — Walkthrough.** In xDome: collectors are receiving traffic, the asset inventory is current, the baseline is stable, the derived policy matches what the enforcer has, and deviations are being alerted.

**Track 2 — Walkthrough.**

```bash
cat /etc/xdome/zones /etc/xdome/policy         # zones and derived policy
sudo nft list chain inet xdome forward | grep -E "tcp dport|drop"   # enforced rules
sudo dmesg | grep -c 'XDOME-DENY'              # deviations blocked
```

**Expected result.** Zones and policy present, enforced rules matching the policy, deviations counted.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Legitimate flow blocked | flow missing from the baseline window | re-baseline; `/tmp/baseline.txt` |
| Attack allowed | raw (uncurated) baseline enforced | review step; `/etc/xdome/policy` |
| No assets discovered | collector not on the SPAN / no mirror | capture interface, mirror config |
| Nothing enforced | no enforcer integration / no default-deny | enforcer rules, `policy drop` |
| Deviation not alerted | deny logging off | `XDOME-DENY` log rule |
| Same-subnet flow uncontrolled | central enforcer cannot see intra-VLAN | distributed enforcer needed |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The subtle failure is a **stale baseline**: the plant changed but the baseline did not, so legitimate new flows are blocked as deviations. Re-baseline on change, and treat deviations as review items, not automatic incidents.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table inet xdome 2>/dev/null
for ns in web db hmi plc; do sudo ip netns del $ns 2>/dev/null; done
sudo rm -rf /etc/xdome /tmp/span.pcap /tmp/span2.pcap /tmp/baseline*.txt
echo "teardown complete"
```

**Expected result.** Enforcer table, namespaces, captures, and derived files removed.

**Negative test.** Leaving the captures and baseline files behind leaves observed OT traffic on disk — sensitive in a real plant; remove them.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Observe, curate, then enforce.** A learned baseline is a record, not a policy, until a human sanctions it.
- **Zone-to-zone generalizes; per-asset is brittle.** Zones (Purdue-aligned) keep the policy stable as assets come and go.
- **Passive decides; the enforcer blocks.** No integration, no enforcement — pair visibility with a real enforcer.
- **Complete SPAN coverage.** The tool only knows what it sees.
- **Deviations are signals.** Treat them as review items; re-baseline on legitimate change.
- **Native + Claroty.** Pair with an OT-protocol IPS (TXOne) and host/distributed controls (Volumes XCIII–CXI) for command-level and same-subnet coverage.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Observe-curate-enforce internalized.
- [ ] Track 2 table, namespaces, captures, and files removed.
