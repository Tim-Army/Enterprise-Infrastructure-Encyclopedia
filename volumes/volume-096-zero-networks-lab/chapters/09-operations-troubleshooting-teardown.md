# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for the failures this lab produces.
- Rehearse a break-glass rollback before you need it.
- Tear the estate down cleanly and restore the host.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — the platform cannot manage a host (Track 1).** Agentless enforcement needs privileged reach to the host's firewall management interface. Check, in order:

1. **Reachability** from the platform to the host's management path (the VMnet2 segment here).
2. **Privilege**: the service account must be able to manage the host's firewall (Windows RPC / Linux SSH).
3. **A single controller** of the native firewall — a conflicting GPO or third-party firewall will fight the platform.

**Symptom 2 — an administrative connection is refused when you expected access.** By design, admin ports are closed until a just-in-time grant. Confirm you completed the MFA/grant step and that the grant has not expired (`sudo nft list set inet zeronet jit_ssh`).

**Symptom 3 — a flow is blocked that should be allowed.** Read the evidence:

```bash
sudo journalctl -k | grep -E "ZN-DENY|ZN-FWD-DENY" | tail
sudo nft list table inet zeronet
```

```powershell
Get-Content "$env:SystemRoot\System32\LogFiles\Firewall\pfirewall.log" -Tail 20
```

Match the dropped 5-tuple against the learned allow-list; a legitimate flow that was missing from the learning window is the usual cause — add it to the reviewed rules.

**Expected result.** Each symptom maps to a first check.

**Negative test.** "Fix" a blocked admin connection by adding a standing allow. You have removed the just-in-time control. Use a grant instead.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Break-glass rollback

**Objective.** Prove you can restore service fast when a policy locks something out.

**Walkthrough.**

**Step 1 — out-of-band path.** Confirm the VMnet2 host adapter (`10.10.20.1`) still reaches the Data Center hosts. Because admin ports are JIT-gated, your break-glass here is the console/host, not standing SSH — an important operational distinction with this platform.

**Step 2 — revert to safety.**

- **Track 1:** move the affected host from Protected back to **Monitoring** — enforcement stops, observation continues.
- **Track 2:** flush the enforcement table: `sudo nft flush table inet zeronet`.
- **Last resort:** revert the VM to its `baseline` snapshot.

**Step 3.** Practice the Track 2 rollback on `zn-db01`, confirm the app flow returns, then re-enforce:

```bash
sudo nft flush table inet zeronet
~/checkdb.sh                    # app path restored: 3
sudo nft -f /etc/nftables.conf  # re-enforce
```

**Expected result.** You can move any host between enforced and open in seconds.

**Negative test.** Rely on standing SSH as your break-glass, then enforce a policy that (correctly) closes it. You are locked out until the console grant or the snapshot. With just-in-time access, plan your break-glass around the console or the host adapter, not a standing port.

**Rollback.** Ensure `zn-db01` is enforced again.

### Lab 9.3 — Teardown and host restoration

**Objective.** Return the host to its pre-lab state.

**Walkthrough.**

**Step 1.** If you connected real hosts to a Zero Networks deployment, remove them from the deployment so it stops managing their firewalls, and confirm each host's firewall returns to your intended baseline.

**Step 2.** Power off all five VMs and delete them from disk (or keep the `baseline` snapshots).

**Step 3.** In the Virtual Network Editor, remove VMnet2 and VMnet3 if you added them solely for this lab. Leave VMnet8 (NAT) alone.

**Step 4.** If you disabled VBS/Memory Integrity in Chapter 02 and this is a shared machine, re-enable it:

```powershell
bcdedit /set hypervisorlaunchtype auto
```

Then turn Core isolation back on and reboot.

**Expected result.** No lab VMs, no lab-only virtual networks, VBS restored if you had disabled it.

**Negative test.** Leaving a host connected to a real deployment means it keeps managing that host's firewall after the lab. Remove it.

**Rollback.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Break-glass rollback rehearsed, with the JIT-access caveat understood.
- [ ] Hosts removed from any real deployment; VMs removed; lab networks cleaned up.
- [ ] VBS re-enabled if it had been disabled.

## Where to go next

This lab built Zero Networks' agentless, learn-then-enforce, MFA-gated model by hand. To place it among the alternatives, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
