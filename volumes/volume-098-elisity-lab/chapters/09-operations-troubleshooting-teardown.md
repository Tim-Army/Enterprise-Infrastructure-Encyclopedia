# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for the failures this lab produces.
- Rehearse a break-glass rollback before you need it.
- Tear the estate down cleanly and restore the host.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — a workload is denied that should be allowed.** The usual cause is a stale or wrong IdentityGraph. Confirm the asset is in the right group:

```bash
sudo nft list set inet elisity grp_appserver
sudo nft list set inet elisity grp_database
grep "$(hostname)" /etc/elisity/inventory.csv   # is the source correct?
sudo /usr/local/bin/build-identitygraph.sh      # rebuild from source
```

If the address changed but the source did not, the graph points at the old address — update the source and rebuild (Track 1: the connected source updates the graph automatically).

**Symptom 2 — the attack still works after enforcing.** Confirm the forward chain is enforcing (default-deny to the protected groups), not still in the observe (log-and-accept) state from Chapter 06:

```bash
sudo nft list chain inet elisity forward
```

**Symptom 3 — a flow is blocked at the network.** Read the evidence:

```bash
sudo journalctl -k | grep -E "ELISITY-DENY|ELISITY-WOULD-DENY" | tail
```

Match the dropped 5-tuple against the identity policy; the mismatch is a misclassification or a missing allow.

**Expected result.** Each symptom maps to a first check — and most point at the IdentityGraph, because in this model the graph *is* the policy.

**Negative test.** "Fix" a denied workload by adding its address directly to a rule instead of correcting its classification. You have reintroduced address-based policy and broken the identity model. Fix the classification.

**Cleanup.** None.

### Lab 9.2 — Break-glass rollback

**Objective.** Prove you can restore service fast when a policy locks something out.

**Walkthrough.**

**Step 1 — out-of-band paths.** Confirm the VMnet2 (`10.10.20.1`) and VMnet4 (`10.10.40.1`) host adapters still reach the Data Center and Database hosts. These management paths do not cross `el-gw`'s forward chain, so policy cannot sever them.

**Step 2 — revert to safety.**

- **Track 1:** move the policy back to simulation/monitor in Elisity Cloud — enforcement stops.
- **Track 2:** set the forward chain back to permissive: `sudo nft flush chain inet elisity forward` (then rebuild policy when ready).
- **Last resort:** revert the VM to its `baseline` snapshot.

**Step 3.** Practice the Track 2 rollback, confirm flows return, then re-enforce:

```bash
sudo nft flush chain inet elisity forward
# app path restored (from el-app01): ~/checkdb.sh -> 3
sudo nft -f /etc/nftables.conf                    # base ruleset
sudo /usr/local/bin/build-identitygraph.sh        # rebuild groups
# then re-apply the Chapter 07 enforcing forward rules
```

**Expected result.** You can move enforcement on and off in seconds, by paths policy cannot cut.

**Negative test.** Rely on a data-plane path (through `el-gw`) as your break-glass, then enforce a policy that denies it. Use the out-of-band host adapters instead — that is why they exist.

**Cleanup.** Ensure enforcement is restored.

### Lab 9.3 — Teardown and host restoration

**Objective.** Return the host to its pre-lab state.

**Walkthrough.**

**Step 1.** If you connected real identity sources or switches to an Elisity tenant, disconnect them so the tenant stops managing enforcement.

**Step 2.** Power off all five VMs and delete them from disk (or keep the `baseline` snapshots).

**Step 3.** In the Virtual Network Editor, remove VMnet2, VMnet3, and VMnet4 if you added them solely for this lab. Leave VMnet8 (NAT) alone.

**Step 4.** If you disabled VBS/Memory Integrity in Chapter 02 and this is a shared machine, re-enable it:

```powershell
bcdedit /set hypervisorlaunchtype auto
```

Then turn Core isolation back on and reboot.

**Expected result.** No lab VMs, no lab-only virtual networks, VBS restored if you had disabled it.

**Negative test.** Leaving VMnet4 configured is harmless but can surprise a later lab that reuses it. Clean it up.

**Cleanup.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom, most paths leading to the IdentityGraph.
- [ ] Break-glass rollback rehearsed via the out-of-band host adapters.
- [ ] Real sources/switches disconnected; VMs removed; the four lab networks cleaned up.
- [ ] VBS re-enabled if it had been disabled.

## Where to go next

This lab built Elisity's identity-based, network-enforced, agentless model by hand. To place it among the alternatives, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
