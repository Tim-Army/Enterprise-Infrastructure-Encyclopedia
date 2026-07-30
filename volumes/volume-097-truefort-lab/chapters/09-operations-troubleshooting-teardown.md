# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for the failures this lab produces.
- Rehearse a break-glass rollback before you need it.
- Tear the estate down cleanly and restore the host.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — a host reports no telemetry (Track 1).** TrueFort needs EDR or its own agent to see a host. Check the EDR integration or agent health, then reachability from the host to the console.

**Symptom 2 — the service-account binding blocks the legitimate app.** If `~/checkdb.sh` fails after Lab 7.2, you likely ran it as the wrong user. The owner match permits only `svcapp`; run it as `sudo -u svcapp /opt/svcapp/checkdb.sh`. Confirm the app service runs under `svcapp` in a real deployment.

**Symptom 3 — a flow is blocked that should be allowed.** Read the evidence:

```bash
sudo journalctl -k | grep -E "TF-DENY|TF-IDENTITY-DENY|TF-FWD-DENY" | tail
sudo nft list table inet truefort ; sudo nft list table inet tf_out
```

```powershell
Get-Content "$env:SystemRoot\System32\LogFiles\Firewall\pfirewall.log" -Tail 20
```

Match the dropped record against the baseline; a legitimate behavior missing from the baseline window is the usual cause — add it after review.

**Expected result.** Each symptom maps to a first check.

**Negative test.** "Fix" the identity block by removing the owner match. You have reopened the service account to every process on the host. Fix the *identity* of the caller instead.

**Cleanup.** None.

### Lab 9.2 — Break-glass rollback

**Objective.** Prove you can restore service fast when a policy locks something out.

**Walkthrough.**

**Step 1 — out-of-band path.** Confirm the VMnet2 host adapter (`10.10.20.1`) still reaches the Data Center hosts (the SSH management allow from Lab 7.1 preserves this).

**Step 2 — revert to safety.**

- **Track 1:** move the affected policy from enforce back to monitoring.
- **Track 2:** flush the enforcement tables: `sudo nft flush table inet truefort ; sudo nft flush table inet tf_out`.
- **Last resort:** revert the VM to its `baseline` snapshot.

**Step 3.** Practice the Track 2 rollback on `tf-db01`, confirm the app flow returns, then re-enforce:

```bash
sudo nft flush table inet truefort
sudo -u svcapp /opt/svcapp/checkdb.sh   # app path restored: 3
sudo nft -f /etc/nftables.conf          # re-enforce
```

**Expected result.** You can move any host between enforced and open in seconds.

**Negative test.** Enforce a default-deny on `tf-db01` that omits the SSH management allow, then try to manage it over the enforced path only; you are locked out until the out-of-band adapter or the snapshot.

**Cleanup.** Ensure `tf-db01` is enforced again with the SSH management rule intact.

### Lab 9.3 — Teardown and host restoration

**Objective.** Return the host to its pre-lab state.

**Walkthrough.**

**Step 1.** If you connected real hosts to a TrueFort deployment or an EDR, disconnect them so the deployment stops managing their firewalls.

**Step 2.** Power off all five VMs and delete them from disk (or keep the `baseline` snapshots).

**Step 3.** In the Virtual Network Editor, remove VMnet2 and VMnet3 if you added them solely for this lab. Leave VMnet8 (NAT) alone.

**Step 4.** If you disabled VBS/Memory Integrity in Chapter 02 and this is a shared machine, re-enable it:

```powershell
bcdedit /set hypervisorlaunchtype auto
```

Then turn Core isolation back on and reboot.

**Expected result.** No lab VMs, no lab-only virtual networks, VBS restored if you had disabled it.

**Negative test.** Leaving a host connected to a real deployment means it keeps being managed after the lab. Remove it.

**Cleanup.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Break-glass rollback rehearsed via the out-of-band path and a policy revert.
- [ ] Hosts disconnected from any real deployment; VMs removed; lab networks cleaned up.
- [ ] VBS re-enabled if it had been disabled.

## Where to go next

This lab built TrueFort's application-centric, identity-anchored model by hand. To place it among the alternatives, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
