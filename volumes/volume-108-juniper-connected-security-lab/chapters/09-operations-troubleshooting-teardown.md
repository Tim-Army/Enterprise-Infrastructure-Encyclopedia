# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two SRX verification commands from memory.
- Work a troubleshooting playbook from symptom to cause.
- Tear down both tracks cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of commands that answer "is the policy working?"

**Track 1 — Walkthrough.**

```text
show security zones                     # interfaces in the right zones?
show security policies                  # permits/denies as intended?
show security policies hit-count        # are rules matching?
show security flow session              # what is actually connected?
show security dynamic-address-group     # quarantine membership
show log security | match RT_FLOW       # permit/deny events
```

**Expected result.** Zones populated, policies as designed, hit counts moving, sessions only for permitted flows, quarantine as expected. These commands localize almost any SRX policy fault.

**Track 2 — Walkthrough.**

```bash
cat /etc/jsec/zones /etc/jsec/addresses
sudo nft list chain inet jsec forward
sudo nft list set inet jsec quarantine
```

**Expected result.** The three artifacts mirror the Junos commands.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| All inter-zone traffic dropped | interface not in a zone, or no permit policy | `show security zones`, `show security policies` |
| Legitimate flow denied | wrong application, wrong address object, or order | `show security policies hit-count` |
| Lateral flow still permitted | permit-any (`allow-all`) not removed | `show configuration security policies` |
| Ping to SRX fails | no `host-inbound-traffic ... ping` | zone host-inbound config |
| Quarantine has no effect | deny placed after a permit, or empty group | policy order; `show security dynamic-address-group` |
| No sessions during test | asymmetric routing / traffic bypasses SRX | `show security flow session`, routing |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** Rebooting the SRX rarely fixes a policy problem — SRX faults are almost always zone assignment, policy order, or a stray permit-any. Diagnose with the six commands first.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.3 — Teardown

**Objective.** Remove the lab cleanly.

**Track 1 — Walkthrough.** Roll back the security configuration and power off the eval VM:

```text
[edit]
delete security policies
delete security zones
delete security dynamic-address
delete security address-book global
commit
```

**Expected result.** `show security policies` returns the default deny-all with no user policies — the firewall is back to a clean state. Power the vSRX eval VM off; the 60-day eval simply lapses.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table inet jsec
for ns in web db hmi plc; do sudo ip netns del $ns; done
sudo rm -rf /etc/jsec
sudo nft list ruleset | grep -c jsec
```

**Expected result.** `0` — table, namespaces, and config removed.

**Negative test.** Deleting the namespaces but leaving the `jsec` table leaves stale rules that match nothing yet persist; remove the table too.

**Rollback.** This is the cleanup.

## Operational lessons for production

- **Default-deny between zones, permit by exception, scope the application.** Zone + address + application is the granularity.
- **Zone design decides what you can enforce.** Same-subnet peers never transit the firewall; separate them or enforce at the edge.
- **Static policy stops lateral movement; dynamic groups add reaction.** You need both.
- **Stage with logged permits before removing permit-any.** Junos has no monitor mode; logging is the safe path.
- **Centralize with Security Director / Policy Enforcer** to scale and automate containment.
- **Native + firewall.** Pair with host controls (Volumes XCIII–CVI) for intra-zone and bypassed traffic.

## Final Completion Checklist

- [ ] The day-two commands run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Track 1 rolled back / vSRX powered off.
- [ ] Track 2 table, namespaces, and config removed.
