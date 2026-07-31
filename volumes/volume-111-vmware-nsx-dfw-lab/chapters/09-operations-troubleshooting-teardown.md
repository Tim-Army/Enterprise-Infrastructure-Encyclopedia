# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Run the day-two NSX DFW verification commands from memory.
- Work a troubleshooting playbook from symptom to cause.
- Tear down both tracks cleanly.

## Hands-On Lab

### Exercise 9.1 — The day-two verification set

**Objective.** Know the handful of checks that answer "is the DFW working?"

**Track 1 — Walkthrough.**

```text
# manager view
GET .../security-policies/microseg/rules            # rules as intended?
GET .../groups/Database/members/virtual-machines    # membership resolving?
GET .../rules/<id>/statistics                       # hit counts moving?
# host view
vsipioctl getrules -f <vnic-filter>                 # rules programmed at the vNIC?
tail /var/log/dfwpktlogs.log                        # allow/drop events
```

**Expected result.** Rules as designed, groups resolving from tags, hits moving, rules programmed at each vNIC. These localize almost any DFW fault.

**Track 2 — Walkthrough.**

```bash
cat /etc/nsx/tags
for ns in web db hmi plc; do echo "== $ns =="; sudo ip netns exec $ns nft list chain inet vnic input 2>/dev/null | grep -E "accept|policy"; done
```

**Expected result.** Each namespace shows its own distributed ruleset.

**Cleanup.** None.

### Exercise 9.2 — Troubleshooting playbook

**Objective.** Map symptoms to causes.

**Walkthrough.**

| Symptom | Likely cause | Check |
|:---|:---|:---|
| Rules exist but nothing enforced | host not prepared as transport node | host prep status |
| Legitimate flow dropped | group membership empty (tag missing) | `.../groups/<g>/members` |
| Lateral flow still allowed | default rule still Allow | default-layer3 rule action |
| Group empty though VM tagged | wrong tag scope/value in criterion | group membership criteria |
| Wrong rule matched | rule order / Applied To scope | rule sequence, Applied To |
| No hits during test | vNIC not filtered / VM not on prepared host | `vsipioctl getrules` |

**Expected result.** A symptom-to-cause table to work top to bottom.

**Negative test.** Reinstalling NSX rarely fixes a policy problem — DFW faults are almost always missing tags/empty groups, the default rule still Allow, or a host not prepared. Check membership and the default rule first.

**Cleanup.** None.

### Exercise 9.3 — Teardown

**Objective.** Remove the lab cleanly.

**Track 1 — Walkthrough.** Delete the security policy and groups, set the default rule back to Allow (or leave zero-trust), remove tags, and optionally unprepare the host:

```text
nsx> DELETE .../security-policies/microseg
nsx> DELETE .../groups/Web ; DELETE .../groups/Database ; ...
nsx> PATCH  .../default-layer3-section/rules/default-rule action=ALLOW
# remove role tags from the VMs; unprepare the transport node if done
```

**Expected result.** The DFW returns to a default-Allow with no user policy; groups and tags are gone. Power the eval VMs off.

**Track 2 — Walkthrough.**

```bash
for ns in web db hmi plc; do sudo ip netns exec $ns nft flush ruleset 2>/dev/null; sudo ip netns del $ns; done
sudo nft delete table inet nsx 2>/dev/null
sudo ip link del seg-app
sudo rm -rf /etc/nsx
echo "teardown complete"
```

**Expected result.** Namespaces, the bridge, the group table, and config are gone.

**Negative test.** Deleting namespaces but leaving `/etc/nsx` and the `nsx` group table leaves stale membership data; remove them too.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Enforce at the vNIC — no blind spot for same-subnet east-west.** This is DFW's defining advantage.
- **Zero-trust means the default rule is Drop.** Specific allows over an Allow default is not microsegmentation.
- **Tags for what, Identity Firewall for who, context profiles for L7.** Rich, workload-centric policy.
- **Membership is the onboarding action.** Scale by tagging, not by editing rules.
- **Enforcement follows the VM across hosts.** vMotion does not create a gap.
- **Native + DFW.** Pair with NSX Gateway Firewall, container integration, or host agents (Volumes XCIII–CVI) for physical, containerized, or unmanaged workloads.

## Final Completion Checklist

- [ ] The day-two checks run and understood.
- [ ] The troubleshooting playbook worked at least once.
- [ ] Track 1 policy/groups/tags removed / eval VMs powered off.
- [ ] Track 2 namespaces, bridge, table, and config removed.
