# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for the failures this lab produces.
- Rehearse a break-glass rollback before you need it.
- Tear the estate down cleanly and restore the host.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit, in order.

**Walkthrough.**

**Symptom 1 — an agent never comes online (Track 1).** Work the prerequisites by frequency:

1. **Resolution/reachability** to the management/aggregator address: `getent hosts <centra-mgmt-fqdn>` and `nc -vz <centra-mgmt-fqdn> <port>` (Linux), `Resolve-DnsName` / `Test-NetConnection` (Windows). No answer → fix DNS (`192.168.170.2`) first.
2. **Competing firewall (Windows)**: a third-party firewall or a GPO forcing the firewall will fight the agent. Confirm a single controller.
3. **Agent service health**: `systemctl status guardicore-agent` (Linux) or the service check (Windows).

**Symptom 2 — a policy change had no effect (Track 1).** Confirm the rule is enforced, not alert-only, and that policy has been published/distributed to the agent.

**Symptom 3 — a flow is blocked that should be allowed.** Read the evidence:

```bash
sudo journalctl -k | grep -E "GC-BLOCK|GC-FWD-BLOCK" | tail
sudo nft list table inet guardicore
```

```powershell
Get-Content "$env:SystemRoot\System32\LogFiles\Firewall\pfirewall.log" -Tail 20
```

Match the dropped 5-tuple against the intended rule; the mismatch is the bug (wrong label/set membership, wrong port, or a missing established/related accept).

**Expected result.** Each symptom maps to a first check.

**Negative test.** "Fix" a blocked flow by reverting to alert-only and declaring success — you removed the protection, not the bug. Re-enforce and fix the rule.

**Cleanup.** None.

### Lab 9.2 — Break-glass rollback

**Objective.** Prove you can restore service fast when a policy locks something out.

**Walkthrough.**

**Step 1 — out-of-band path.** Confirm the VMnet2 host adapter (`10.10.20.1`) still reaches the Data Center hosts regardless of policy:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 22
```

**Step 2 — revert to safety.** Rehearse each rollback:

- **Track 1:** switch the affected asset's protection from enforce back to **alert-only** (or revoke the policy) — enforcement stops immediately, telemetry continues.
- **Track 2:** flush the enforcement table: `sudo nft flush table inet guardicore`.
- **Last resort:** revert the VM to its `baseline` snapshot.

**Step 3.** Practice the Track 2 rollback on `gc-db01`, confirm the app flow returns, then re-enforce:

```bash
sudo nft flush table inet guardicore
~/checkdb.sh                    # app path restored: 3
sudo nft -f /etc/nftables.conf  # re-enforce
```

**Expected result.** You can move any host between enforced and open in seconds, by a route policy cannot sever.

**Negative test.** Enforce a default-deny on `gc-db01` that omits the SSH management allow, then try to manage it over the enforced path only; you are locked out until the out-of-band adapter or the snapshot. This is why both exist.

**Cleanup.** Ensure `gc-db01` is enforced again with the SSH management rule intact.

### Lab 9.3 — Teardown and host restoration

**Objective.** Return the host to its pre-lab state.

**Walkthrough.**

**Step 1.** If you deployed real agents, uninstall them so Centra does not keep stale assets (use the agent uninstaller from the console/installer, or remove from Apps on Windows).

**Step 2.** Power off all five VMs and delete them from disk (or keep the `baseline` snapshots to revisit the lab).

**Step 3.** In the Virtual Network Editor, remove VMnet2 and VMnet3 if you added them solely for this lab. Leave VMnet8 (NAT) alone.

**Step 4.** If you disabled VBS/Memory Integrity in Chapter 02 and this is a shared machine, re-enable it:

```powershell
bcdedit /set hypervisorlaunchtype auto
```

Then turn Core isolation back on and reboot.

**Expected result.** No lab VMs, no lab-only virtual networks, VBS restored if you had disabled it.

**Negative test.** Deleting the VMs but leaving VMnet3 configured is harmless but can surprise a later lab that reuses it. Clean it up.

**Cleanup.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom.
- [ ] Break-glass rollback rehearsed via the out-of-band path and a policy revert.
- [ ] Agents uninstalled (Track 1), VMs removed, lab networks cleaned up.
- [ ] VBS re-enabled if it had been disabled.

## Where to go next

This lab built Guardicore's model by hand. To place it among the alternatives — Illumio, ColorTokens, Cisco, VMware NSX, the open-source meshes, and the OT-specific platforms — see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
