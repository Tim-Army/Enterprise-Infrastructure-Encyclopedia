# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for the failures this lab produces.
- Rehearse a break-glass rollback before you need it.
- Tear the estate down cleanly and restore the host.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — a workload reports no telemetry (Track 1).** The agent must reach the cluster/SaaS. Check agent health and connectivity from the host to `<cluster-fqdn>`, then confirm the workload appears in the scope.

**Symptom 2 — the discovered policy is wrong.** ADM learned whatever the telemetry window contained. If a rule permits something it should not, your collection captured abnormal traffic; re-collect over clean traffic and re-run ADM, and always compare against ground truth before enforcing. Policy analysis (Lab 7.1) is the place to catch this.

**Symptom 3 — a flow is blocked that should be allowed.** Read the evidence:

```bash
sudo journalctl -k | grep -E "CW-DENY|CW-FWD-DENY" | tail
sudo iptables -L CW-SEG -n --line-numbers
sudo ipset list db_clients
```

A legitimate client missing from the `ipset` is the usual cause — add it to the set (the group), not a new rule.

**Expected result.** Each symptom maps to a first check: telemetry reach, the discovery window, or the ipset membership.

**Negative test.** "Fix" a blocked flow by flushing enforcement. You removed the protection, not the cause. Fix the ipset membership or the rule instead.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Break-glass rollback

**Objective.** Prove you can restore service fast when a policy locks something out.

**Walkthrough.**

**Step 1 — out-of-band path.** Confirm the VMnet2 host adapter (`10.10.20.1`) still reaches the Data Center hosts (the SSH management allow in Lab 7.2 preserves this).

**Step 2 — revert to safety.**

- **Track 1:** set the workspace back to **analysis** (non-enforced) — enforcement stops, telemetry continues.
- **Track 2:** flush the enforcement chains: `sudo iptables -F CW-SEG ; sudo iptables -F CW-FWD`.
- **Last resort:** revert the VM to its `baseline` snapshot.

**Step 3.** Practice on `cw-db01`, confirm the app flow returns, then re-enforce:

```bash
sudo iptables -F CW-SEG
~/checkdb.sh          # from cw-app01: app path restored -> 3
# then re-apply the Chapter 07 CW-SEG rules
```

**Expected result.** You can move enforcement on and off in seconds, by a route policy cannot sever.

**Negative test.** Enforce a default-deny that omits the SSH management allow, then try to manage the host over the enforced path only; you are locked out until the out-of-band adapter or the snapshot.

**Rollback.** Ensure `cw-db01` is enforced again with the management allow intact.

### Lab 9.3 — Teardown and host restoration

**Objective.** Return the host to its pre-lab state.

**Walkthrough.**

**Step 1.** If you installed real agents, uninstall them so the cluster stops counting and managing the workloads.

**Step 2.** Power off all five VMs and delete them from disk (or keep the `baseline` snapshots).

**Step 3.** In the Virtual Network Editor, remove VMnet2 and VMnet3 if you added them solely for this lab. Leave VMnet8 (NAT) alone.

**Step 4.** If you disabled VBS/Memory Integrity in Chapter 02 and this is a shared machine, re-enable it:

```powershell
bcdedit /set hypervisorlaunchtype auto
```

Then turn Core isolation back on and reboot.

**Expected result.** No lab VMs, no lab-only virtual networks, VBS restored if you had disabled it.

**Negative test.** Leaving an agent installed means the cluster keeps managing that workload after the lab. Uninstall it.

**Rollback.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Break-glass rollback rehearsed via the out-of-band path and a policy revert.
- [ ] Agents uninstalled (Track 1), VMs removed, lab networks cleaned up.
- [ ] VBS re-enabled if it had been disabled.

## Where to go next

This lab built Secure Workload's telemetry-driven, discover-then-enforce model by hand. To place it among the alternatives, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
