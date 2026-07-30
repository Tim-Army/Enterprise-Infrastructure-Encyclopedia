# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Work a structured troubleshooting playbook for the overlay failures this lab produces.
- Rehearse a break-glass rollback before you need it.
- Tear the estate down cleanly and restore the host.

## Hands-On Lab

### Lab 9.1 — Troubleshooting playbook

**Objective.** Diagnose the three failure modes you are most likely to hit.

**Walkthrough.**

**Symptom 1 — an agent's overlay tunnel will not come up.** Work it in this order:

1. **Keys.** Each side must have the other's *public* key. `sudo wg show` on both ends: a peer with no recent handshake usually means a wrong or missing key.
2. **Endpoint reachability.** The spoke must reach the hub's underlay endpoint: `nc -vzu 10.10.20.254 51820` — but note cloaking may block your test traffic; check from the hub with `sudo wg show` for a handshake instead.
3. **Cloaking too tight.** If you applied `policy drop` before allowing `udp dport 51820`, the tunnel can never form. Confirm the WireGuard port and the `wg0` interface are permitted in the input chain.

**Symptom 2 — a device is unreachable even over the overlay.** Confirm it is authorized. Overlay connectivity (a handshake) is necessary but not sufficient; the hub's forward policy (Chapter 07) or the gateway policy (Chapter 08) must also permit the specific relationship. Check:

```bash
sudo journalctl -k | grep -E "AIRWALL-DENY" | tail
sudo nft list chain inet airwall forward
```

**Symptom 3 — you locked yourself out of a cloaked host.** This is why the break-glass path exists (Lab 9.2).

**Expected result.** Each symptom maps to a first check: keys and cloaking for connectivity, forward policy for authorization.

**Negative test.** "Fix" a tunnel that will not form by disabling cloaking entirely (`policy accept`). The tunnel forms, but you have un-cloaked the host and reopened the underlay. Permit only the WireGuard port instead.

**Cleanup.** None.

### Lab 9.2 — Break-glass rollback

**Objective.** Prove you can restore service fast when the overlay or cloaking locks something out.

**Walkthrough.**

**Step 1 — the out-of-band underlay path.** The cloaking rules deliberately kept `ip saddr 10.10.20.1 tcp dport 22 accept` — the VMnet2 host adapter can still SSH to the Data Center hosts even when they are dark to everyone else. Confirm it:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 22   # from the host: expect True
```

**Step 2 — revert to safety.**

- **Track 1:** in the Conductor, move the agent to a bypass/monitoring state or remove it from enforcement.
- **Track 2:** bring the overlay and cloaking down on the affected host: `sudo systemctl stop wg-quick@wg0 ; sudo nft flush table inet airwall`. The host returns to the plain underlay.
- **Last resort:** revert the VM to its `baseline` snapshot.

**Step 3.** Practice on `aw-db01`, confirm the underlay path returns, then re-enable protection:

```bash
sudo nft flush table inet airwall              # un-cloak (emergency)
# db is reachable on the underlay again for recovery
sudo nft -f /etc/nftables.conf                 # re-cloak
sudo systemctl restart wg-quick@wg0            # re-join the overlay
```

**Expected result.** You can drop back to the plain underlay in seconds via a path the overlay never covered.

**Negative test.** Remove the `10.10.20.1` break-glass allow from the cloaking rules, then lock yourself out with a bad overlay change. Recovery now requires the snapshot. Keep the break-glass allow.

**Cleanup.** Ensure `aw-db01` is cloaked and on the overlay again.

### Lab 9.3 — Teardown and host restoration

**Objective.** Return the host to its pre-lab state.

**Walkthrough.**

**Step 1.** If you provisioned real Airwall Agents/Gateways against a Conductor, deprovision them so the Conductor stops managing the identities.

**Step 2.** Power off all five VMs and delete them from disk (or keep the `baseline` snapshots).

**Step 3.** In the Virtual Network Editor, remove VMnet2 and VMnet3 if you added them solely for this lab. Leave VMnet8 (NAT) alone.

**Step 4.** If you disabled VBS/Memory Integrity in Chapter 02 and this is a shared machine, re-enable it:

```powershell
bcdedit /set hypervisorlaunchtype auto
```

Then turn Core isolation back on and reboot.

**Expected result.** No lab VMs, no lab-only virtual networks, VBS restored if you had disabled it.

**Negative test.** Leaving a real agent provisioned means the Conductor still counts and manages that identity after the lab. Deprovision it.

**Cleanup.** Host restored.

## Summary and Completion Checklist

- [ ] Troubleshooting playbook worked against a real symptom, separating connectivity from authorization.
- [ ] Break-glass rollback rehearsed via the out-of-band underlay path.
- [ ] Real agents/gateways deprovisioned; VMs removed; lab networks cleaned up.
- [ ] VBS re-enabled if it had been disabled.

## Where to go next

This lab built Airwall's HIP encrypted-overlay model by hand with WireGuard. To place it among the alternatives, see [Volume LXXXVII, Microsegmentation Options](../../volume-087-microsegmentation-options/README.md), whose Chapter 15 comparison matrix links each option to its own build-it-yourself lab in this series.
