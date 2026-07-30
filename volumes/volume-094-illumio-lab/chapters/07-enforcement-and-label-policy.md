# Chapter 07: Enforcement and Label-Based Policy

## Learning Objectives

- Author a ruleset against labels and provision it.
- Move a workload from Visibility Only to Full Enforcement and confirm the intended flow survives while the attack is blocked.
- Prove that label-based policy scales: a new workload inherits protection with no rule change.
- Enforce on Windows through the Windows Filtering Platform.

You validated the boundary in Visibility Only in Chapter 06. Now you enforce it, always confirming the legitimate flow still works before and after each change.

## Hands-On Lab

### Lab 7.1 — Ring-fence the database and enforce it

**Objective.** Permit Web→Database on 5432 and deny every other path into the database, then move `il-db01` to Full Enforcement.

**Track 1 — Real Illumio.**

**Step 1.** In the PCE, create a **Ruleset** named `ILLab-App`. Scope it to Application **ILLab**, Environment **Development**, Location **DC**.

**Step 2.** Add a **rule**: Providers = Role **Database**, Consumers = Role **Web**, Service = **PostgreSQL (TCP 5432)**. This is the only ingress the database needs.

**Step 3.** **Provision** the draft (the draft/active split means nothing takes effect until you provision — your change-control gate). While `il-db01` is still in Visibility Only, open its Illumination view and confirm the simulation shows win01→db 5432 as *would-block* and app→db 5432 as *allowed*.

**Step 4.** Change `il-db01`'s enforcement state to **Full Enforcement**. Provision.

**Track 2 — Native equivalent.**

**Step 1.** On `il-db01`, rewrite the ruleset with the ring-fence expressed *and* the segmentation chain now ending in `drop` (Full Enforcement):

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

define DB_PORT = 5432

table inet illumio {
    set role_web {
        type ipv4_addr
        elements = { 10.10.20.11 }        # il-app01 - the ONLY legitimate db client
    }

    chain input {
        type filter hook input priority 0; policy drop;   # default-deny (Full Enforcement)
        ct state established,related accept
        iif "lo" accept
        tcp dport 22 accept                # keep management SSH (break-glass)
        jump segmentation
    }

    chain segmentation {
        # Legitimate: Web role -> database port.
        ip saddr @role_web tcp dport $DB_PORT accept
        # Everything else falls through to the chain's end and is dropped by policy.
        log prefix "ILLUMIO-DENY db: " level warn
    }
}
EOF
sudo nft -f /etc/nftables.conf
```

**Step 2.** Confirm the legitimate flow survives and the attack is now blocked. From `il-app01`:

```bash
~/checkdb.sh          # expect: 3
```

From `il-win01` (the attacker):

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432   # expect TcpTestSucceeded : False
```

**Expected result.** `~/checkdb.sh` still prints `3`; the HMI's probe to 5432 now fails; `il-db01`'s log shows `ILLUMIO-DENY db:` lines for the blocked attempts. The lateral movement from Chapter 05 is dead.

**Negative test.** Add `10.10.20.21` to `role_web` "to be safe", reload, and re-run the attack — it succeeds again. An over-broad group re-authorizes the exact movement you set out to stop. Remove it.

**Cleanup.** Keep the enforced ruleset.

### Lab 7.2 — Prove label-based policy scales

**Objective.** Show that policy written against a label protects a *new* workload automatically, with no rule edit — the property that separates label-based policy from address-based ACLs.

**Track 1 — Real Illumio.**

**Step 1.** Imagine a second web server `il-app02` (10.10.20.13). Pair it and label it Role **Web**, Application **ILLab**. Because the rule names the **Web** role, `il-app02` may reach the database the instant it is labelled — no rule change.

**Step 2.** Now relabel it Role **HMI**. Provision. It immediately loses database access. The policy did not change; the label did.

**Track 2 — Native equivalent (demonstration).**

You do not need to build a whole VM to see the mechanism. On `il-db01`, add and remove a would-be web host from the set and watch access follow membership:

```bash
# A new 'web' host is authorized simply by joining the set:
sudo nft add element inet illumio role_web '{ 10.10.20.13 }'
sudo nft list set inet illumio role_web
# ...and de-authorized by leaving it:
sudo nft delete element inet illumio role_web '{ 10.10.20.13 }'
```

**Expected result.** Membership of the set (the label) — not an edit to the rule — decides access. This is why Illumio policy survives cloning, autoscaling, and re-addressing.

**Negative test.** Rewrite the rule to name the address `10.10.20.11` directly instead of the `role_web` set. It works today, but the day the app is rebuilt with a new address, the rule silently fails open or closed. Address-based rules are the technical debt label-based policy exists to retire. Revert to the set.

**Cleanup.** Ensure `role_web` contains only `10.10.20.11`.

### Lab 7.3 — Enforce on Windows through the Windows Filtering Platform

**Objective.** Bring `il-win01` to Full Enforcement so nothing may reach the HMI and the HMI may only do its one legitimate job (poll the PLC).

**Track 1 — Real Illumio.** In the PCE, add a rule allowing the HMI its outbound PLC poll (Consumers = Role **HMI**, Providers = the PLC unmanaged workload, Service = **Modbus TCP 502**), then set `il-win01` to **Full Enforcement** and provision. The VEN programs WFP accordingly.

**Track 2 — Native equivalent.** Program WFP directly to the same posture: default-deny inbound, allow only the HMI's outbound Modbus and DNS/established:

```powershell
# Default-deny inbound; keep outbound controlled by explicit allow rules
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Block -DefaultOutboundAction Block

# Allow the one legitimate job: HMI -> PLC on Modbus 502
New-NetFirewallRule -DisplayName "ILLUMIO HMI->PLC 502" -Direction Outbound `
    -RemoteAddress 10.10.30.50 -Protocol TCP -RemotePort 502 -Action Allow

# Allow DNS and existing connections so management does not break
New-NetFirewallRule -DisplayName "ILLUMIO DNS out" -Direction Outbound `
    -RemotePort 53 -Protocol UDP -Action Allow
New-NetFirewallRule -DisplayName "ILLUMIO mgmt RDP in" -Direction Inbound `
    -RemoteAddress 10.10.20.1 -Protocol TCP -LocalPort 3389 -Action Allow
```

**Step 2.** Verify the HMI can still do its job but nothing else:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True  (legitimate)
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # expect False (blocked outbound)
```

**Expected result.** HMI→PLC 502 succeeds; HMI→DB 5432 fails from the *source* side now too — even before the database's own rule is consulted, the HMI's own enforcement forbids the connection. Defense in depth: the attack is blocked at both ends.

**Negative test.** Remove the inbound management RDP allow and the `10.10.20.1` break-glass rule, then reboot; you may lock yourself out of the HMI. This is why Lab 9.2 rehearses break-glass. Re-add the management rule before continuing.

**Cleanup.** Keep the enforced Windows posture.

### Lab 7.4 — Draft, provision, and selective enforcement (Design Exercise)

**Objective.** Reason about two Illumio capabilities that have no faithful native stand-in: the **draft/active provisioning** model and **Selective Enforcement** via **enforcement boundaries**.

**Design Exercise.**

1. **Provisioning.** Illumio keeps policy in a **draft** state until you **provision** it; the PCE then compiles it and pushes rules to VENs. Explain why a change-control boundary between authoring and enforcing matters in a 5,000-workload estate, and what the native Track 2 loses by applying `nft -f` immediately.
2. **Selective Enforcement.** An **enforcement boundary** lets you enforce a *specific* service (say, block RDP everywhere) while leaving every other flow in visibility. Contrast this with Full Enforcement (default-deny everything). When would you phase a rollout with selective enforcement rather than moving straight to Full?

**Model answer.**

1. Draft/active decouples *deciding* policy from *imposing* it: reviewers can inspect exactly which flows a provision will newly block (the PCE shows this), changes can be staged and provisioned in a window, and a bad change is a un-provision away from rollback. Immediate `nft -f` has no such gate — the rule is live the instant it loads, so Track 2 substitutes discipline (snapshots, a tested rollback) for the product's built-in staging.
2. Selective enforcement is the phased path: you block one dangerous service fleet-wide (RDP, SMB) to get immediate risk reduction without the blast radius of default-deny, prove nothing broke, then progress workloads to Full Enforcement application by application. You move straight to Full only for a well-understood, low-dependency workload like the lab's database.

**Expected result.** A written justification for both mechanisms.

**Negative test.** Argue that provisioning is needless overhead and Track 2's immediacy is superior. In a lab of five hosts it feels that way; at enterprise scale, an ungated change that default-denies the wrong label is an outage. The overhead is the safety.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] `il-db01` at Full Enforcement; app→db works, HMI→db blocked.
- [ ] Label-based policy demonstrated to follow set/label membership, not addresses.
- [ ] `il-win01` enforced through WFP; HMI→PLC 502 works, HMI→db blocked at source.
- [ ] Draft/provision and selective enforcement reasoned through.
