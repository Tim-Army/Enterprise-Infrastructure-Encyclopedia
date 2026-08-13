# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two checks for group-based fabric segmentation.
- Work a troubleshooting playbook from symptom to cause.
- Tear down the Track 2 lab cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is group policy working?"

**Track 1 — Walkthrough.** In CloudVision/EOS: group membership resolves as intended, MSS-Group policy is applied on the switches, redirected flows are traversing the firewall, and telemetry shows group hits and denies.

**Track 2 — Walkthrough.**

```bash
cat /etc/mss/groups                                              # group membership
for g in sg_web sg_db sg_mgmt sg_ot; do echo -n "$g: "; sudo nft list set inet mss $g | tr -d '\n' | grep -o 'elements = {[^}]*}'; echo; done
sudo nft list chain inet mss forward | grep -E "accept|drop|policy"   # group policy
sudo ss -ltn | grep 15432 || echo "firewall down"               # macro firewall up
sudo dmesg | grep -c 'MSS-DENY'                                 # group denies
```

**Expected result.** Groups populated, group policy with default-drop, firewall listening, denies recorded.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| All group traffic dropped | no group permit, or default-deny with empty groups | policy; group membership |
| Group flow blocked | wrong L4 match or group set | policy rule; `nft list set` |
| Lateral flow permitted | a too-broad group permit | policy L4 scope |
| Redirected flow not inspected | redirect rule missing / firewall down | `mssnat` rule; firewall `ss` |
| Endpoint gets wrong policy | resolved into the wrong group | membership criteria |
| Firewall a bottleneck | too many flows redirected | redirect selectively |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** The subtle failure is a **stale group**: an endpoint that moved but kept its old group gets the wrong policy. Verify group resolution before suspecting the policy.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 9.3 — Teardown

**Objective.** Remove the Track 2 lab cleanly.

**Track 2 — Walkthrough.**

```bash
sudo pkill -f mssfw.py 2>/dev/null
sudo nft delete table inet mss 2>/dev/null; sudo nft delete table ip mssnat 2>/dev/null
for ns in web db hmi plc fw; do sudo ip netns del $ns 2>/dev/null; done
for b in sg1 sg2 sg3 sg4 sg9; do sudo ip link del $b 2>/dev/null; done
sudo rm -f /usr/local/bin/mssfw.py; sudo rm -rf /etc/mss /tmp/mssfw.log
echo "teardown complete"
```

**Expected result.** Policy tables, namespaces, bridges, firewall, and config removed.

**Negative test.** Leaving the `mssnat` table behind keeps redirecting web→db on the host; remove it too.

**Rollback.** This is the cleanup.

## Operational lessons for production

- **Group policy at line rate.** Segment by group in the fabric — default-deny between groups, no hairpin.
- **Macro-redirect selectively.** Steer the flows that need inspection through a firewall; keep the bulk at line rate.
- **Author once in CloudVision.** Central groups and policy, fabric-wide telemetry.
- **Correct group resolution matters.** Wrong group, wrong policy — verify membership first.
- **On-fabric plus complementary controls.** Pair MSS with host/cloud controls (Volumes XCIII–CXVI) for off-fabric workloads.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Group policy (micro) plus firewall redirect (macro) internalized.
- [ ] Track 2 tables, namespaces, bridges, firewall, and config removed.
