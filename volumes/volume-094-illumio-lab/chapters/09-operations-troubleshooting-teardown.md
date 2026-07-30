# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for the failures this lab actually produces.
- Rehearse a break-glass rollback before you need it.
- Tear the estate down cleanly and restore the host.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit, in order.

**Walkthrough.**

**Symptom 1 — a VEN never comes Online (Track 1).** Work the prerequisites in this order, because that is their frequency:

1. **DNS.** From the host, resolve the PCE FQDN: `getent hosts <pce-fqdn>` (Linux) or `Resolve-DnsName <pce-fqdn>` (Windows). No answer → fix DNS (`192.168.170.2`) first; a VEN that cannot resolve the PCE never pairs.
2. **Reachability.** `nc -vz <pce-fqdn> 8443`. Blocked → egress or the PCE is unreachable.
3. **Competing firewall (Windows).** A third-party firewall or a GPO forcing the firewall will fight the VEN. Confirm a single controller.
4. **VEN health.** `sudo /opt/illumio_ven/illumio-ven-ctl status` and `connectivity-check`.

**Symptom 2 — a policy change had no effect (Track 1).** You almost certainly did not **provision** the draft. Draft policy is inert until provisioned; check the provisioning indicator in the PCE and provision.

**Symptom 3 — a flow is blocked that should be allowed.** Read the evidence, do not guess:

```bash
# On the enforcing Linux host - what is being dropped?
sudo journalctl -k | grep "ILLUMIO-DENY" | tail
sudo nft list table inet illumio
```

```powershell
# On Windows - what did WFP drop?
Get-Content "$env:SystemRoot\System32\LogFiles\Firewall\pfirewall.log" -Tail 20
```

Match the dropped 5-tuple against your intended rule; the mismatch is your bug (wrong label/set membership, wrong port, or a missing established/related accept).

**Expected result.** Each symptom maps to a first check, not a shrug.

**Negative test.** "Fix" a blocked-flow problem by reverting to Visibility Only and declaring success. The flow works because nothing is enforced — you have removed the protection, not fixed the rule. Re-enforce and fix the actual rule.

**Cleanup.** None.

### Lab 9.2 — Break-glass rollback

**Objective.** Prove you can restore service fast when a policy locks something out — before it happens under pressure.

**Walkthrough.**

**Step 1 — the out-of-band path.** Confirm the VMnet2 host adapter (`10.10.20.1`) still reaches the Data Center hosts regardless of policy. This deliberate management path is your first-line recovery:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 22    # host -> db mgmt : expect True
```

**Step 2 — revert to safety.** Rehearse each rollback so you know which to reach for:

- **Track 1 fast rollback:** set the affected workload to **Visibility Only** and provision — enforcement stops immediately, telemetry continues.
- **Track 2 fast rollback:** flush the enforcement table on the affected host: `sudo nft flush table inet illumio` (then reload the scaffold when ready).
- **Last resort:** revert the VM to its `baseline` snapshot from Chapter 04.

**Step 3.** Practice the Track 2 rollback on `il-db01`, confirm the app flow returns, then re-apply enforcement:

```bash
sudo nft flush table inet illumio       # emergency: all-allow
~/checkdb.sh                             # confirm app path restored: 3
sudo nft -f /etc/nftables.conf          # re-enforce
```

**Expected result.** You can move any host between enforced and open in seconds, by a route that policy cannot sever.

**Negative test.** Enforce a default-deny on `il-db01` that omits the SSH management allow, then try to manage it over the enforced path only. You are locked out until you use the out-of-band adapter or the snapshot. This is why the management allow and the OOB path exist.

**Cleanup.** Ensure `il-db01` is back under enforcement with the SSH management rule intact.

### Lab 9.3 — Teardown and host restoration

**Objective.** Return the host to its pre-lab state.

**Walkthrough.**

**Step 1.** If you paired real VENs, unpair them first so the PCE does not keep stale workloads:

```bash
sudo /opt/illumio_ven/illumio-ven-ctl unpair open   # 'open' leaves the host firewall permissive
```

```powershell
# Windows: run the VEN's unpair from its install directory, or uninstall from Apps
```

**Step 2.** Power off all five VMs. In Workstation, delete them from disk (or keep the `baseline` snapshots if you want to revisit the lab).

**Step 3.** In the Virtual Network Editor, remove VMnet2 and VMnet3 if you added them solely for this lab. Leave VMnet8 (NAT) alone; other VMware work uses it.

**Step 4.** If you disabled VBS/Memory Integrity in Chapter 02 and this is a shared machine, re-enable it:

```powershell
bcdedit /set hypervisorlaunchtype auto
```

Then turn Core isolation back on in Windows Security and reboot.

**Expected result.** No lab VMs, no lab-only virtual networks, VBS restored if you had disabled it.

**Negative test.** Delete the VMs but leave VMnet3 configured with no host adapter; harmless, but a later lab that reuses VMnet3 may inherit surprising isolation. Clean it up to avoid confusion.

**Cleanup.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked at least once against a real symptom.
- [ ] Break-glass rollback rehearsed via the out-of-band path and a policy revert.
- [ ] VENs unpaired (Track 1), VMs removed, lab networks cleaned up.
- [ ] VBS re-enabled if it had been disabled.

## Where to go next

This lab built Illumio's model by hand. To place it among the alternatives — Cisco, VMware NSX, the open-source meshes, the OT-specific platforms — see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
