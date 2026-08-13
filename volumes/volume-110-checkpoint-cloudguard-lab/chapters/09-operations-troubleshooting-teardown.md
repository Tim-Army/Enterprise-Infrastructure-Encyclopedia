# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two Check Point verification commands from memory.
- Work a troubleshooting playbook from symptom to cause.
- Tear down both tracks cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of commands that answer "is the policy working?"

**Track 1 — Walkthrough.**

```text
fw stat                                  # which policy is installed, and when?
mgmt_cli show access-rulebase name Network  # rules as intended?
fw ctl conntab                           # what is actually connected?
fw log                                   # accept/drop events
dynamic_objects -l                       # tag object membership
cpwd_admin list                          # are the processes up?
```

**Expected result.** Correct policy installed, rulebase as designed, connections only for permitted flows, tag objects populated. These commands localize almost any Check Point policy fault.

**Track 2 — Walkthrough.**

```bash
cat /etc/cpg/objects /etc/cpg/tags
sudo nft list chain inet cpg forward
sudo nft list set inet cpg role_db
```

**Expected result.** The artifacts mirror the Check Point commands.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| All transit dropped | only the Cleanup rule matches | `mgmt_cli show access-rulebase`, install |
| Legitimate flow dropped | wrong service/object, or rule order | rule position; `fw log` |
| Lateral flow still permitted | any-any accept not removed, or not installed | rulebase; `fw stat` install time |
| Edit made no difference | published but not installed | `fw stat`; re-run install-policy |
| Tag object empty | data-center source not connected / no tags | `dynamic_objects -l` |
| No connections during test | traffic bypasses the gateway / topology | `fw ctl conntab`, gateway topology |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The single most common Check Point mistake is editing and publishing without **installing** — the gateway keeps enforcing the last installed policy. Check `fw stat` install time first.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.3 — Teardown

**Objective.** Remove the lab cleanly.

**Track 1 — Walkthrough.** Delete the rules and objects, install a clean policy, and power off the eval VMs:

```text
mgmt> mgmt_cli delete access-rule name "web-to-db"  layer "Network" --session-id "$SID"
mgmt> mgmt_cli delete access-rule name "hmi-to-plc" layer "Network" --session-id "$SID"
mgmt> mgmt_cli delete host name web --session-id "$SID"
mgmt> mgmt_cli delete host name db  --session-id "$SID"
mgmt> mgmt_cli publish --session-id "$SID"
mgmt> mgmt_cli install-policy policy-package "Standard" access true targets gw --session-id "$SID"
gw> dynamic_objects -n role_web -d ; dynamic_objects -n role_db -d
```

**Expected result.** The rulebase is back to just the Cleanup rule and the tag objects are gone. Power the management and gateway eval VMs off; the 15-day eval lapses.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table inet cpg
for ns in web db hmi plc; do sudo ip netns del $ns; done
sudo rm -rf /etc/cpg
sudo nft list ruleset | grep -c cpg
```

**Expected result.** `0` — table, namespaces, and config removed.

**Negative test.** Deleting namespaces but leaving the `cpg` table leaves stale rules matching nothing yet persisting; remove the table too.

**Rollback.** This is the cleanup.

## Operational lessons for production

- **Ordered rulebase, explicit Cleanup drop, log it.** Default-deny you can see.
- **Publish then install — install is what enforces.** The classic Check Point gotcha.
- **Tag-based objects so policy follows workloads.** Onboarding becomes tagging, not a firewall change.
- **Identity Awareness for who, tags for what.** Combine workload and user identity.
- **One policy package, many gateways.** Central authoring, estate-wide enforcement.
- **Native + gateway.** Pair with host controls (Volumes XCIII–CVI) for intra-segment and bypassed traffic.

## Final Completion Checklist

- [ ] The day-two commands run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Track 1 rules/objects removed / eval VMs powered off.
- [ ] Track 2 table, namespaces, and config removed.
