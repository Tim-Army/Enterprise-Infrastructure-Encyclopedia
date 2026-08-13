# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for agentless network-of-one isolation.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is the isolation healthy?"

**Track 1 — Walkthrough.** In Zscaler/Airgap: the enforcement point is controlling ARP/DHCP on the VLAN, every device is isolated, the east-west policy has only sanctioned flows, the kill switch is armed and disengaged, and denied attempts are logged.

**Track 2 — Walkthrough.**

```bash
sudo nft list chain inet airgap forward | grep -E "accept|drop|policy"      # policy: default drop + sanctioned
for d in web victim; do echo -n "$d routes: "; sudo ip netns exec $d ip route | tr '\n' ' '; echo; done
sudo dmesg | grep -c 'AIRGAP-DENY'                                          # lateral attempts logged
```

**Expected result.** Default-drop with only the sanctioned allow, every device routing solely via the enforcer, denied attempts recorded.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Devices still reach each other | not collapsed to /32, or direct L2 path remains | device routes; enforcer in path |
| Sanctioned flow blocked | allow rule missing or wrong 5-tuple | `nft list chain`, addresses |
| Everything blocked after kill switch | kill switch still engaged | remove `KILL-SWITCH` rule |
| Kill switch not total | rule not inserted above allows | rule order (insert at top) |
| No deny logs | log rule missing on the drop | `AIRGAP-DENY` rule |
| Device offline | host route to enforcer missing | `ip route` on the device |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The subtle failure is an **incomplete network-of-one**: a device that can still ARP a peer directly (static ARP entry, a second interface, an enforcement gap) has a lateral path the policy never sees. Verify the enforcer is the *only* neighbor before trusting the isolation.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table inet airgap 2>/dev/null
for d in web db hmi plc victim; do sudo ip netns del $d 2>/dev/null; done
sudo ip link del vlan 2>/dev/null
sudo sysctl -w net.ipv4.conf.all.proxy_arp=0 >/dev/null
sudo rm -f /tmp/airgap-policy.txt
echo "teardown complete"
```

**Expected result.** Policy table, namespaces, bridge, and proxy-ARP setting removed.

**Negative test.** Leaving `proxy_arp` enabled changes host ARP behavior beyond the lab; reset it as above.

**Rollback.** This is the cleanup.

## Operational lessons for production

- **Isolate by default; connectivity is the exception.** The network-of-one denies all east-west until policy permits.
- **Agentless and non-disruptive.** No endpoint software, no re-addressing — deployable in brownfield.
- **A kill switch for total containment.** One lever severs all east-west during an incident.
- **Cover every segment; verify ARP/DHCP control.** Isolation leaks through any uncontrolled path.
- **East-west isolation plus north-south ZTNA.** Pair Airgap with the Zero Trust Exchange for both directions.
- **Reach-isolation plus inspection plus endpoint.** Combine with an OT-protocol IPS (TXOne/Nozomi) and host controls for payload and endpoint protection.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Agentless network-of-one and the kill switch internalized.
- [ ] Track 2 table, namespaces, bridge, and proxy-ARP removed.
