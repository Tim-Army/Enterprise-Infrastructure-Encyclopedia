# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two TrustSec verification commands from memory.
- Work a troubleshooting playbook from symptom to cause.
- Tear down both tracks cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of commands that answer "is TrustSec working?"

**Track 1 — Walkthrough.**

```bash
show cts environment-data            # groups learned from ISE? state COMPLETE
show cts role-based sgt-map all      # are bindings present (SXP/local)?
show cts role-based permissions      # is the matrix downloaded? default Deny IP?
show cts role-based counters         # are permits/denies incrementing?
show cts sxp connections brief       # is SXP up?
```

**Expected result.** Environment `COMPLETE`, bindings present, matrix with `default: Deny IP`, counters moving, SXP `On`. Those five commands localize almost any TrustSec fault.

**Track 2 — Walkthrough.**

```bash
cat /etc/cts/sgt-names               # group catalogue
sudo nft list map inet cts sgtmap    # bindings
sudo nft list chain inet cts forward # matrix + counters
```

**Expected result.** The three artifacts mirror the five Cisco commands.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Environment data `INCOMPLETE` | `cts credentials` mismatch or PAC not provisioned | `show cts pacs`, re-enter credentials |
| No bindings on enforcer | SXP down or speaker/listener both same role | `show cts sxp connections brief` |
| Matrix empty though authored in ISE | not deployed, or NAD not in the right ISE deployment | ISE **Deploy**; check RADIUS |
| Counters all zero during test | enforcement off or asymmetric path | `show cts role-based permissions`, verify egress path |
| Legitimate flow denied | SGACL missing trailing structure or wrong cell | re-read `show cts role-based permissions` |
| Everything permitted | matrix default still `Permit IP` | set default cell to Deny IP |

**Expected result.** A symptom-to-cause table you can work top to bottom.

**Negative test.** Restarting ISE or the NAD to "fix" a policy problem usually wastes 40 minutes and changes nothing — TrustSec faults are almost always trust, binding, or matrix-deploy issues, not stuck processes. Diagnose with the five commands first.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the lab cleanly.

**Track 1 — Walkthrough.** Back the NAD out of enforcement and clear TrustSec state, then power off the eval VMs:

```text
nad(config)# no cts role-based enforcement
nad(config)# no cts sxp enable
nad(config)# no cts role-based sgt-map ... (any static maps)
```

Delete the SGTs, SGACLs, mappings, and matrix cells in ISE if you plan to reuse the node; otherwise power the ISE eval VM off. The 90-day eval simply lapses.

**Expected result.** `show cts role-based permissions` returns to `default: Permit IP` with no cells — the fabric is back to flat.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table inet cts
for ns in web db hmi plc; do sudo ip netns del $ns; done
sudo ip link del fabric
sudo rm -rf /etc/cts
sudo nft list ruleset | grep -c cts
```

**Expected result.** `0` — the table, namespaces, bridge, and config are gone.

**Negative test.** Deleting the namespaces but leaving the `cts` table means stale rules match nothing and quietly persist; remove the table too so no orphaned policy lingers.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Classify everywhere, enforce at the edge.** A binding without an enforcing access-layer device is a label with no teeth.
- **Default-deny the matrix, permit by exception.** The default cell is the whole posture.
- **Monitor mode first, always.** Preview drops before enforcing them.
- **SXP for reach, inline CMD for fidelity.** Real estates are hybrid; both feed one matrix.
- **Log denies during rollout.** Silent drops are indistinguishable from bugs.
- **Native + fabric.** Pair TrustSec with host controls (Volumes XCIII–CVI) for endpoints and segments the fabric cannot tag.

## Final Completion Checklist

- [ ] The five day-two commands run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Track 1 returned to flat / eval VMs powered off.
- [ ] Track 2 table, namespaces, and config removed.
