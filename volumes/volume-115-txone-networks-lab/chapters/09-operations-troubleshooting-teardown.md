# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for inline OT protection and endpoint lockdown.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is inline + endpoint protection healthy?"

**Track 1 — Walkthrough.** In TXOne: EdgeIPS devices are inline and passing legitimate traffic, virtual-patch signatures and trust lists are current, StellarProtect is in lockdown with the right allowlist, and EdgeOne/StellarOne show the fleet healthy.

**Track 2 — Walkthrough.**

```bash
sudo ss -ltn | grep 1502 || echo "inline inspector down"          # inline device up
cat /etc/txone/signatures                                          # virtual-patch + command filters
sudo nft list chain ip txone filter | grep -E "drop|accept"        # trust list
cat /etc/txone/allowlist                                           # endpoint allowlist
sudo grep -cE "VIRTUAL-PATCH|UNTRUSTED" /tmp/edgeips.log           # inline blocks
```

**Expected result.** Inline inspector up, signatures/filters present, trust list in place, allowlist current, blocks recorded.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Legitimate traffic dropped | signature too broad, or trust list too tight | `/etc/txone/signatures`, nft rule |
| Exploit still lands | signature missing, or a path bypasses the device | signatures; routing/DNAT rule |
| Attacker reaches the PLC | trust-list rule missing or wrong source | nft `txone filter` |
| Approved app blocked | binary changed (hash mismatch) | re-approve hash in allowlist |
| Malware runs | app launched outside the lockdown launcher | enforce all launches via stellar-run |
| Traffic not inspected | DNAT/redirect not matching / device not in path | nft `prerouting`, topology |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The classic inline failure is a **bypass path**: a second route to the cell that skips the device. A perfect signature protects nothing on a path the device is not on. Verify placement covers every route first.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
sudo pkill -f edgeips.py 2>/dev/null; sudo pkill -f vulnplc.py 2>/dev/null
sudo nft delete table ip txone 2>/dev/null
for ns in hmi atk ews plc; do sudo ip netns del $ns 2>/dev/null; done
sudo ip link del ot 2>/dev/null; sudo ip link del cell 2>/dev/null
sudo rm -f /usr/local/bin/edgeips.py /usr/local/bin/vulnplc.py /usr/local/bin/stellar-run \
           /usr/local/bin/hmi-tool /usr/local/bin/evil-tool
sudo rm -rf /etc/txone /tmp/edgeips.log /tmp/vulnplc.log
echo "teardown complete"
```

**Expected result.** Processes, namespaces, bridges, scripts, and config removed.

**Negative test.** Leaving the DNAT/redirect table (`ip txone`) behind keeps intercepting traffic on the host; remove the table too.

**Rollback.** This is the cleanup.

## Operational lessons for production

- **Transparent inline means you can deploy in a live plant.** No re-addressing, no downtime.
- **Virtual patch the unpatchable.** Put the fix in the network, not the device.
- **Trust list plus command filter plus virtual patch — layered and independent.** Each fails alone, not together.
- **Lock down the hosts too.** Application allowlisting closes the EWS as an attack path.
- **Cover every path and host.** Inline protection is a placement problem; a bypass defeats it.
- **Enforce + monitor + broker.** Pair TXOne (enforce) with passive monitors (detect) and identity brokering (remote access) for a complete OT program.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Transparent inline, virtual patching, and endpoint lockdown internalized.
- [ ] Track 2 processes, namespaces, scripts, and config removed.
