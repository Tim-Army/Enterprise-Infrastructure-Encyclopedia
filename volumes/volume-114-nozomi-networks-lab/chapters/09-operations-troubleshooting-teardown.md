# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for protocol-aware OT segmentation.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is protocol-aware segmentation healthy?"

**Track 1 — Walkthrough.** In Nozomi: Guardians are receiving traffic, the network graph and process baselines are current, assertions are as intended and pushed to the enforcers, and alerts (denials and anomalies) are flowing to Vantage.

**Track 2 — Walkthrough.**

```bash
cat /etc/nozomi/links /etc/nozomi/baseline                       # link + process policy
sudo ip netns exec plc nft list chain inet ot input | grep -E "accept|policy"   # PLC proxy-only
sudo ss -ltn | grep 1502 || echo "proxy not listening"           # enforcer up
grep -cE "DENY|ANOMALY" /tmp/mbproxy.log                          # events recorded
```

**Expected result.** Policy present, PLC isolated to the proxy, proxy listening, events recorded.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Reads fail | proxy down or PLC isolation too tight | proxy `ss`, plc nft rule |
| Writes succeed | `ALLOW_FC` includes a write code | proxy `ALLOW_FC` |
| Direct write bypasses the check | PLC not isolated to the proxy | plc nft `input` rule |
| No anomalies ever | range too wide, or values never sampled out | baseline range, proxy value check |
| Non-Modbus reaches the PLC | proxy not parsing / isolation missing | proxy function parse, nft |
| Encrypted OT not inspected | passive sensor cannot see the function | needs terminating proxy / endpoint agent |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The subtle failure is an **incomplete baseline**: a legitimate but rare write function (a scheduled setpoint change) denied because it was never learned. Learn a representative window, and make deliberate exceptions rather than widening the policy.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
sudo pkill -f mbproxy.py 2>/dev/null; sudo pkill -f mbserver.py 2>/dev/null
for ns in hmi plc; do sudo ip netns exec $ns nft flush ruleset 2>/dev/null; sudo ip netns del $ns 2>/dev/null; done
sudo ip link del ot 2>/dev/null
sudo rm -f /usr/local/bin/mbserver.py /usr/local/bin/mbclient.py /usr/local/bin/mbproxy.py /usr/local/bin/mbsniff.py
sudo rm -rf /etc/nozomi /tmp/mb.pcap /tmp/mbproxy.log /tmp/mbserver.log
echo "teardown complete"
```

**Expected result.** Processes, namespaces, bridge, scripts, and config removed.

**Negative test.** Leaving the proxy running keeps the PLC path open on the host; kill it and remove the scripts.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Segment by function, not just port.** Read-allowed, write-denied is an OT-protocol control an L4 firewall cannot express.
- **Baseline the process, not only the flows.** An out-of-range value is an incident on an allowed flow.
- **Passive detects; an OT-aware enforcer blocks.** Pair Nozomi with an inline OT IPS.
- **Complete SPAN and known protocols.** Depth needs coverage and a matching dissector.
- **Central assertions, fleet-wide.** Vantage authors once; enforcers apply at the cell boundaries.
- **Native + Nozomi.** Pair with inline OT enforcement (TXOne) and network/host segmentation (Volumes XCIII–CXI) for blocking and same-subnet coverage.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Function-aware segmentation plus process detection internalized.
- [ ] Track 2 processes, namespaces, scripts, and config removed.
