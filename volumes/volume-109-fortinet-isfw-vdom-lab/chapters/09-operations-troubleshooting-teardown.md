# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two FortiGate verification commands from memory.
- Work a troubleshooting playbook from symptom to cause.
- Tear down both tracks cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of commands that answer "is the policy working?"

**Track 1 — Walkthrough.**

```text
show system zone                              # interfaces in the right zones?
show firewall policy                          # permits/denies as intended?
diagnose firewall iprope lookup <5-tuple>     # which policy matches a flow?
get system session list                       # what is actually connected?
diagnose sys vdom list                        # VDOMs and their interfaces
execute log display                           # permit/deny events
```

**Expected result.** Zones populated, policies as designed, lookups returning the right policy, sessions only for permitted flows, VDOMs as planned. These commands localize almost any FortiGate policy fault.

**Track 2 — Walkthrough.**

```bash
cat /etc/fgt/zones /etc/fgt/addresses
sudo nft list chain inet fgt forward
sudo nft list tables | grep fgt
```

**Expected result.** The artifacts mirror the FortiOS commands.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| All transit dropped | no matching policy (implicit deny) | `show firewall policy`, `iprope lookup` |
| Legitimate flow denied | wrong service, wrong srcintf/dstintf, or order | `diagnose firewall iprope lookup` |
| Lateral flow still permitted | permit-all (policy 100) not removed | `show firewall policy` |
| IT↔OT totally broken | VDOM split with no inter-VDOM link/policy | `diagnose sys vdom list`, vdom-link |
| No sessions during test | asymmetric routing / bypasses ISFW | `get system session list`, routing |
| Deny not logged | `logtraffic` not set on the policy | policy config |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** Rebooting the FortiGate rarely fixes a policy problem — faults are almost always policy order, service scope, interface/zone assignment, or a missing inter-VDOM link. Use the lookup first.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the lab cleanly.

**Track 1 — Walkthrough.** Delete the policies, VDOM split, zones, and objects, then power off the eval VM:

```text
FGT # config firewall policy
FGT (policy) # delete 1
FGT (policy) # delete 2
FGT (policy) # delete 3
FGT (policy) # delete 4
FGT (policy) # end
FGT # config global
FGT (global) # set vdom-mode no-vdom
FGT (global) # end
FGT # config system zone
FGT (zone) # delete APP
FGT (zone) # delete DB
FGT (zone) # delete MGMT
FGT (zone) # delete OT
FGT (zone) # end
```

**Expected result.** `show firewall policy` lists no user policies (only the implicit deny remains) and the FortiGate is back in single-VDOM mode. Power the FortiGate-VM eval off.

**Track 2 — Walkthrough.**

```bash
for t in fgt fgt_it fgt_ot; do sudo nft delete table inet $t 2>/dev/null; done
for ns in web db hmi plc; do sudo ip netns del $ns; done
sudo rm -rf /etc/fgt
sudo nft list ruleset | grep -c fgt
```

**Expected result.** `0` — tables, namespaces, and config removed.

**Negative test.** Deleting namespaces but leaving the `fgt` tables leaves stale rules matching nothing yet persisting; remove the tables too.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Implicit deny is your friend — permit by exception, scope the service.** Zone + address + service is the granularity.
- **VDOMs for hard separation; zones for softer segmentation.** Reach for VDOMs when two networks must be isolated by default (IT/OT).
- **Order matters; put explicit denies above broad permits, remove permit-alls.**
- **Automation stitches add reaction; static policy stops lateral movement.** You need both.
- **Scale with FortiManager and the Security Fabric.**
- **Native + ISFW.** Pair with host controls (Volumes XCIII–CVI) for intra-zone and bypassed traffic.

## Final Completion Checklist

- [ ] The day-two commands run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Track 1 policies/VDOMs removed / FortiGate-VM powered off.
- [ ] Track 2 tables, namespaces, and config removed.
